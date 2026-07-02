"""
Chrome OS Collector — ChromeOS / Chrome Browser Security Updates
Source: Google Chrome Releases Blog
URL: https://chromereleases.googleblog.com/
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import feedparser


CHROME_FEED = "https://chromereleases.googleblog.com/feeds/posts/default"


def collect(year: int = None, month: int = None) -> dict:
    now = datetime.utcnow()
    year = year or now.year
    month = month or now.month

    month_str = datetime(year, month, 1).strftime("%B %Y")

    try:
        feed = feedparser.parse(CHROME_FEED)
    except Exception as e:
        return {"platform": "chromeos", "month": month_str, "releases": [], "summary": f"Collection failed: {e}"}

    releases = []

    for entry in feed.entries:
        title = entry.get("title", "").strip()
        link = entry.get("link", "")
        content = entry.get("content", [{}])[0].get("value", "") or entry.get("summary", "")
        published_str = entry.get("published", "")

        # Parse date from feedparser's parsed time
        try:
            pub_struct = entry.get("published_parsed")
            if pub_struct:
                pub_date = datetime(*pub_struct[:6])
            else:
                continue
        except Exception:
            continue

        if pub_date.year != year or pub_date.month != month:
            continue

        # Filter to ChromeOS / Stable channel updates
        title_lower = title.lower()
        if not any(kw in title_lower for kw in ["chrome os", "chromeos", "stable channel", "long-term support"]):
            continue

        # Extract CVEs
        cves = list(set(re.findall(r"CVE-\d{4}-\d+", content)))

        # Extract version numbers
        versions = re.findall(r"\d{3,4}\.\d+\.\d+\.\d+", content)

        # Count security fixes
        security_fix_count = len(re.findall(r"\[\$[\d,]+\]|security fix|CVE", content, re.IGNORECASE))

        releases.append({
            "title": title,
            "date": pub_date.strftime("%Y-%m-%d"),
            "link": link,
            "versions": list(set(versions))[:5],
            "cves": cves[:20],
            "cve_count": len(cves),
            "security_fix_count": security_fix_count
        })

    total_cves = sum(r["cve_count"] for r in releases)
    summary = (
        f"ChromeOS released {len(releases)} updates in {month_str} covering {total_cves} CVEs."
        if releases else f"No ChromeOS security releases found for {month_str}."
    )

    return {
        "platform": "chromeos",
        "month": month_str,
        "source": CHROME_FEED,
        "total_releases": len(releases),
        "total_cves": total_cves,
        "summary": summary,
        "releases": releases
    }


if __name__ == "__main__":
    import json
    result = collect()
    print(json.dumps(result, indent=2))
