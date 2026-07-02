"""
Ubuntu Collector — Ubuntu Security Notices (USN)
Source: Ubuntu USN RSS Feed (official Canonical feed)
URL: https://usn.ubuntu.com/rss.xml
"""

import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import re


USN_RSS_URL = "https://ubuntu.com/security/notices/rss.xml"


def collect(year: int = None, month: int = None) -> dict:
    now = datetime.utcnow()
    year = year or now.year
    month = month or now.month

    month_str = datetime(year, month, 1).strftime("%B %Y")

    try:
        resp = requests.get(USN_RSS_URL, timeout=30)
        resp.raise_for_status()
    except Exception as e:
        return {"platform": "ubuntu", "month": month_str, "notices": [], "summary": f"Collection failed: {e}"}

    root = ET.fromstring(resp.content)
    channel = root.find("channel")
    notices = []

    for item in channel.findall("item"):
        title = item.findtext("title", "").strip()
        link = item.findtext("link", "").strip()
        pub_date_str = item.findtext("pubDate", "").strip()
        description = item.findtext("description", "").strip()

        # Parse date
        try:
            # RSS date format: "Mon, 09 Jun 2026 12:00:00 +0000"
            pub_date = datetime.strptime(pub_date_str[:25].strip(), "%a, %d %b %Y %H:%M:%S")
        except Exception:
            continue

        if pub_date.year != year or pub_date.month != month:
            continue

        # Extract CVEs from description
        cves = list(set(re.findall(r"CVE-\d{4}-\d+", description)))

        # Extract USN ID
        usn_match = re.search(r"USN-[\d-]+", title)
        usn_id = usn_match.group(0) if usn_match else ""

        # Determine severity from keywords
        severity = "Unknown"
        desc_lower = description.lower()
        if "critical" in desc_lower:
            severity = "Critical"
        elif "high" in desc_lower:
            severity = "High"
        elif "medium" in desc_lower:
            severity = "Medium"
        elif "low" in desc_lower:
            severity = "Low"

        notices.append({
            "usn_id": usn_id,
            "title": title,
            "date": pub_date.strftime("%Y-%m-%d"),
            "link": link,
            "severity": severity,
            "cve_count": len(cves),
            "cves": cves[:15],
            "summary": description[:300].strip()
        })

    total_cves = sum(n["cve_count"] for n in notices)
    summary = (
        f"Ubuntu published {len(notices)} security notices in {month_str} covering {total_cves} CVEs."
        if notices else f"No Ubuntu security notices found for {month_str}."
    )

    return {
        "platform": "ubuntu",
        "month": month_str,
        "source": USN_RSS_URL,
        "total_notices": len(notices),
        "total_cves": total_cves,
        "summary": summary,
        "notices": notices
    }


if __name__ == "__main__":
    import json
    result = collect()
    print(json.dumps(result, indent=2))
