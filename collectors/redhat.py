"""
Red Hat Collector — Red Hat Security Advisories (RHSA)
Source: Red Hat Security RSS Feed (official)
URL: https://access.redhat.com/security/team/updates/advisory.atom
"""

import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import re


RHSA_RSS_URL = "https://access.redhat.com/security/team/updates/advisory.atom"
NS = {"atom": "http://www.w3.org/2005/Atom"}


def collect(year: int = None, month: int = None) -> dict:
    now = datetime.utcnow()
    year = year or now.year
    month = month or now.month

    month_str = datetime(year, month, 1).strftime("%B %Y")

    try:
        resp = requests.get(RHSA_RSS_URL, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
        resp.raise_for_status()
    except Exception as e:
        return {"platform": "redhat", "month": month_str, "advisories": [], "summary": f"Collection failed: {e}"}

    root = ET.fromstring(resp.content)
    advisories = []
    severity_counts = {"Critical": 0, "Important": 0, "Moderate": 0, "Low": 0}

    for entry in root.findall("atom:entry", NS):
        title = entry.findtext("atom:title", "", NS).strip()
        link_el = entry.find("atom:link", NS)
        link = link_el.get("href", "") if link_el is not None else ""
        updated_str = entry.findtext("atom:updated", "", NS).strip()
        summary_text = entry.findtext("atom:summary", "", NS).strip()

        # Parse date
        try:
            updated = datetime.strptime(updated_str[:19], "%Y-%m-%dT%H:%M:%S")
        except Exception:
            continue

        if updated.year != year or updated.month != month:
            continue

        # Only include RHSA (security advisories), skip RHBA (bug) and RHEA (enhancement)
        if not title.startswith("RHSA"):
            continue

        # Extract severity from title e.g. "RHSA-2026:1234 Critical: ..."
        severity = "Unknown"
        for sev in ("Critical", "Important", "Moderate", "Low"):
            if sev in title:
                severity = sev
                if sev in severity_counts:
                    severity_counts[sev] += 1
                break

        # Extract CVEs
        cves = list(set(re.findall(r"CVE-\d{4}-\d+", summary_text)))

        # Extract advisory ID
        advisory_match = re.search(r"RHSA-[\d:]+", title)
        advisory_id = advisory_match.group(0) if advisory_match else title

        advisories.append({
            "advisory_id": advisory_id,
            "title": title,
            "severity": severity,
            "date": updated.strftime("%Y-%m-%d"),
            "link": link,
            "cves": cves[:10],
            "cve_count": len(cves)
        })

    total_cves = sum(a["cve_count"] for a in advisories)
    summary = (
        f"Red Hat published {len(advisories)} security advisories in {month_str}. "
        f"Critical: {severity_counts['Critical']}, Important: {severity_counts['Important']}, "
        f"Moderate: {severity_counts['Moderate']}. Total CVEs: {total_cves}."
        if advisories else f"No Red Hat advisories found for {month_str}."
    )

    return {
        "platform": "redhat",
        "month": month_str,
        "source": RHSA_RSS_URL,
        "total_advisories": len(advisories),
        "total_cves": total_cves,
        "severity_counts": severity_counts,
        "summary": summary,
        "advisories": advisories
    }


if __name__ == "__main__":
    import json
    result = collect()
    print(json.dumps(result, indent=2))
