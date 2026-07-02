"""
Android Collector — Android Security Bulletins
Source: Google Android Security Bulletins page
URL: https://source.android.com/docs/security/bulletin
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re


BULLETIN_INDEX = "https://source.android.com/docs/security/bulletin"


def collect(year: int = None, month: int = None) -> dict:
    now = datetime.utcnow()
    year = year or now.year
    month = month or now.month

    month_str = datetime(year, month, 1).strftime("%B %Y")
    month_url_str = datetime(year, month, 1).strftime("%Y-%m")  # e.g. 2026-06

    # Try to fetch the specific month's bulletin directly
    bulletin_url = f"https://source.android.com/docs/security/bulletin/{month_url_str}"

    try:
        resp = requests.get(bulletin_url, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
        resp.raise_for_status()
    except Exception:
        # Fall back to index page
        try:
            resp = requests.get(BULLETIN_INDEX, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
            resp.raise_for_status()
            bulletin_url = BULLETIN_INDEX
        except Exception as e:
            return {"platform": "android", "month": month_str, "vulnerabilities": [], "summary": f"Collection failed: {e}"}

    soup = BeautifulSoup(resp.text, "html.parser")
    vulnerabilities = []
    patch_levels = []
    severity_counts = {"Critical": 0, "High": 0, "Moderate": 0, "Low": 0}

    # Find all CVE references in the page
    all_cves = list(set(re.findall(r"CVE-\d{4}-\d+", resp.text)))

    # Find severity tables
    tables = soup.find_all("table")
    for table in tables:
        headers = [th.get_text(strip=True).lower() for th in table.find_all("th")]
        if not any(h in headers for h in ["cve", "severity", "type"]):
            continue

        for row in table.find_all("tr")[1:]:
            cols = [td.get_text(strip=True) for td in row.find_all("td")]
            if len(cols) < 2:
                continue

            cve_col = cols[0] if cols else ""
            cve_ids = re.findall(r"CVE-\d{4}-\d+", cve_col)
            if not cve_ids:
                continue

            severity = "Unknown"
            for col in cols:
                if col in ("Critical", "High", "Moderate", "Low"):
                    severity = col
                    break

            vuln_type = cols[2] if len(cols) > 2 else ""
            component = cols[-2] if len(cols) > 3 else ""

            if severity in severity_counts:
                severity_counts[severity] += len(cve_ids)

            for cve in cve_ids:
                vulnerabilities.append({
                    "cve_id": cve,
                    "severity": severity,
                    "type": vuln_type,
                    "component": component
                })

    # Find patch levels mentioned
    patch_level_matches = re.findall(r"\d{4}-\d{2}-\d{2} security patch level", resp.text)
    patch_levels = list(set(patch_level_matches))

    total_cves = len(set(v["cve_id"] for v in vulnerabilities)) or len(all_cves)

    summary = (
        f"Android Security Bulletin for {month_str}: {total_cves} CVEs. "
        f"Critical: {severity_counts['Critical']}, High: {severity_counts['High']}, "
        f"Moderate: {severity_counts['Moderate']}."
    )

    return {
        "platform": "android",
        "month": month_str,
        "source": bulletin_url,
        "total_cves": total_cves,
        "severity_counts": severity_counts,
        "patch_levels": patch_levels,
        "summary": summary,
        "vulnerabilities": vulnerabilities[:60]
    }


if __name__ == "__main__":
    import json
    result = collect()
    print(json.dumps(result, indent=2))
