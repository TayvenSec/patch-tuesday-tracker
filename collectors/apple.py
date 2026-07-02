"""
Apple Collector — iOS, macOS, watchOS, tvOS, visionOS
Source: Apple Security Releases page (HT201222)
URL: https://support.apple.com/en-us/111900
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re


APPLE_URL = "https://support.apple.com/en-us/111900"


def collect(year: int = None, month: int = None) -> dict:
    now = datetime.utcnow()
    year = year or now.year
    month = month or now.month

    month_str = datetime(year, month, 1).strftime("%B %Y")  # e.g. "June 2026"

    try:
        resp = requests.get(APPLE_URL, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
        resp.raise_for_status()
    except Exception as e:
        return {"platform": "apple", "month": month_str, "updates": [], "summary": f"Collection failed: {e}"}

    soup = BeautifulSoup(resp.text, "html.parser")
    updates = []

    # Apple's page uses a table with Name, Link, Date columns
    table = soup.find("table")
    if not table:
        return {"platform": "apple", "month": month_str, "updates": [], "summary": "Could not parse Apple releases page."}

    rows = table.find_all("tr")
    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 2:
            continue

        name_cell = cols[0]
        date_cell = cols[-1]

        name = name_cell.get_text(strip=True)
        date_text = date_cell.get_text(strip=True)
        link_tag = name_cell.find("a")
        link = "https://support.apple.com" + link_tag["href"] if link_tag and link_tag.get("href", "").startswith("/") else (link_tag["href"] if link_tag else "")

        # Filter to current month/year
        if month_str[:3] not in date_text and datetime(year, month, 1).strftime("%b") not in date_text:
            continue
        if str(year) not in date_text:
            continue

        # Try to get CVE count from linked page (quick scrape)
        cve_count = 0
        cves = []
        if link:
            try:
                detail_resp = requests.get(link, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
                cve_matches = re.findall(r"CVE-\d{4}-\d+", detail_resp.text)
                cves = list(set(cve_matches))
                cve_count = len(cves)
            except Exception:
                pass

        updates.append({
            "name": name,
            "date": date_text,
            "link": link,
            "cve_count": cve_count,
            "cves": cves[:20]
        })

    if updates:
        total_cves = sum(u["cve_count"] for u in updates)
        summary = f"Apple released {len(updates)} updates in {month_str} covering {total_cves} CVEs across {', '.join(u['name'] for u in updates[:4])}."
    else:
        summary = f"No Apple security releases found for {month_str}."

    return {
        "platform": "apple",
        "month": month_str,
        "source": APPLE_URL,
        "total_updates": len(updates),
        "summary": summary,
        "updates": updates
    }


if __name__ == "__main__":
    import json
    result = collect()
    print(json.dumps(result, indent=2))
