"""
Debian Collector — Debian Security Advisories (DSA)
Source: Debian Security RSS Feed (official)
URL: https://www.debian.org/security/dsa-long
"""

import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import re


DSA_RSS_URL = "https://www.debian.org/security/dsa-long"


def collect(year: int = None, month: int = None) -> dict:
    now = datetime.utcnow()
    year = year or now.year
    month = month or now.month

    month_str = datetime(year, month, 1).strftime("%B %Y")

    try:
        resp = requests.get(DSA_RSS_URL, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
        resp.raise_for_status()
    except Exception as e:
        return {"platform": "debian", "month": month_str, "advisories": [], "summary": f"Collection failed: {e}"}

    root = ET.fromstring(resp.content)
    advisories = []

    # RSS 2.0 format
    channel = root.find("channel")
    items = channel.findall("item") if channel else root.findall(".//item")

    for item in items:
        title = item.findtext("title", "").strip()
        link = item.findtext("link", "").strip()
        pub_date_str = item.findtext("pubDate", "").strip()
        description = item.findtext("description", "").strip()

        # Parse date
        try:
            pub_date = datetime.strptime(pub_date_str[:25].strip(), "%a, %d %b %Y %H:%M:%S")
        except Exception:
            continue

        if pub_date.year != year or pub_date.month != month:
            continue

        # Extract CVEs
        cves = list(set(re.findall(r"CVE-\d{4}-\d+", description)))

        # Extract DSA ID
        dsa_match = re.search(r"DSA-[\d-]+", title)
        dsa_id = dsa_match.group(0) if dsa_match else ""

        # Extract affected package from title e.g. "DSA-1234-1 openssl -- security update"
        package = ""
        title_parts = title.split(" -- ")
        if len(title_parts) > 0:
            pkg_part = title_parts[0].replace(dsa_id, "").strip()
            package = pkg_part.strip()

        advisories.append({
            "dsa_id": dsa_id,
            "title": title,
            "package": package,
            "date": pub_date.strftime("%Y-%m-%d"),
            "link": link,
            "cves": cves[:10],
            "cve_count": len(cves),
            "summary": description[:250].strip()
        })

    total_cves = sum(a["cve_count"] for a in advisories)
    summary = (
        f"Debian published {len(advisories)} security advisories (DSAs) in {month_str} covering {total_cves} CVEs."
        if advisories else f"No Debian security advisories found for {month_str}."
    )

    return {
        "platform": "debian",
        "month": month_str,
        "source": DSA_RSS_URL,
        "total_advisories": len(advisories),
        "total_cves": total_cves,
        "summary": summary,
        "advisories": advisories
    }


if __name__ == "__main__":
    import json
    result = collect()
    print(json.dumps(result, indent=2))
