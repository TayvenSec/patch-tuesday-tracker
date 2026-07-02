"""
MSRC Collector — Windows & Windows Server
Source: Microsoft Security Response Center API (public, no auth required)
API docs: https://api.msrc.microsoft.com/cvrf/v3.0/swagger/index.html
"""

import requests
from datetime import datetime


def get_patch_tuesday_date(year: int, month: int) -> str:
    """Returns the MSRC document ID for the given month's Patch Tuesday (YYYY-MMM)."""
    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    return f"{year}-{months[month - 1]}"


def collect(year: int = None, month: int = None) -> dict:
    now = datetime.utcnow()
    year = year or now.year
    month = month or now.month

    doc_id = get_patch_tuesday_date(year, month)
    url = f"https://api.msrc.microsoft.com/cvrf/v3.0/cvrf/{doc_id}"

    headers = {"Accept": "application/json"}

    try:
        resp = requests.get(url, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()
    except requests.exceptions.HTTPError as e:
        if resp.status_code == 404:
            print(f"[MSRC] No data yet for {doc_id} — Patch Tuesday may not have occurred yet.")
            return {"platform": "windows", "month": doc_id, "updates": [], "cves": [], "summary": "No data available yet."}
        raise e

    updates = []
    cves = []

    # Parse vulnerabilities
    for vuln in data.get("Vulnerability", []):
        cve_id = vuln.get("CVE", "")
        title = vuln.get("Title", {}).get("Value", "")
        
        # Get severity
        severity = "Unknown"
        for threat in vuln.get("Threats", []):
            if threat.get("Type") == 3:  # Severity type
                severity = threat.get("Description", {}).get("Value", "Unknown")
                break

        # Get affected products
        products = []
        for score in vuln.get("CVSSScoreSets", []):
            prod_id = score.get("ProductID", [])
            products.extend(prod_id)

        cves.append({
            "cve_id": cve_id,
            "title": title,
            "severity": severity,
            "products": products[:5]  # cap to keep output clean
        })

    # Parse KB articles from ProductTree
    product_tree = data.get("ProductTree", {})
    for branch in product_tree.get("Branch", []):
        for item in branch.get("Items", []):
            name = item.get("Name", "")
            if "KB" in name or "Windows" in name or "Server" in name:
                updates.append({"name": name, "product_id": item.get("ProductID", "")})

    # Severity breakdown
    critical = [c for c in cves if c["severity"].lower() == "critical"]
    important = [c for c in cves if c["severity"].lower() == "important"]

    summary = (
        f"Microsoft released {len(cves)} CVEs for {doc_id}. "
        f"{len(critical)} Critical, {len(important)} Important."
    )

    return {
        "platform": "windows",
        "month": doc_id,
        "source": url,
        "total_cves": len(cves),
        "critical_count": len(critical),
        "important_count": len(important),
        "summary": summary,
        "cves": cves[:50],  # top 50 for brevity
        "kb_articles": updates[:20]
    }


if __name__ == "__main__":
    import json
    result = collect()
    print(json.dumps(result, indent=2))
