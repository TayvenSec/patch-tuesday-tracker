"""
Palo Alto Networks Collector — Security Advisories
Source: Palo Alto Networks Security Advisories
URL: https://security.paloaltonetworks.com/
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re


PAN_URL = "https://security.paloaltonetworks.com/"
PAN_RSS = "https://security.paloaltonetworks.com/rss.xml"


def collect(year: int = None, month: int = None) -> dict:
    now = datetime.utcnow()
    year = year or now.year
    month = month or now.month

    month_str = datetime(year, month, 1).strftime("%B %Y")

    # Try RSS first, fall back to HTML scrape
    advisories = _collect_rss(year, month, month_str)
    if not advisories:
        advisories = _collect_html(year, month, month_str)

    severity_counts = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
    for adv in advisories:
        sev = adv.get("severity", "")
        if sev in severity_counts:
            severity_counts[sev] += 1

    total_cves = sum(a.get("cve_count", 0) for a in advisories)
    summary = (
        f"Palo Alto Networks published {len(advisories)} advisories in {month_str}. "
        f"Critical: {severity_counts['Critical']}, High: {severity_counts['High']}. "
        f"Total CVEs: {total_cves}."
        if advisories else f"No Palo Alto Networks advisories found for {month_str}."
    )

    return {
        "platform": "palo_alto",
        "month": month_str,
        "source": PAN_URL,
        "total_advisories": len(advisories),
        "total_cves": total_cves,
        "severity_counts": severity_counts,
        "summary": summary,
        "advisories": advisories
    }


def _collect_rss(year, month, month_str):
    try:
        import feedparser
        feed = feedparser.parse(PAN_RSS)
        advisories = []

        for entry in feed.entries:
            title = entry.get("title", "").strip()
            link = entry.get("link", "")
            summary = entry.get("summary", "")

            pub_struct = entry.get("published_parsed")
            if not pub_struct:
                continue
            pub_date = datetime(*pub_struct[:6])

            if pub_date.year != year or pub_date.month != month:
                continue

            cves = list(set(re.findall(r"CVE-\d{4}-\d+", title + " " + summary)))

            # PAN severity in title e.g. "PAN-SA-2026-0001 HIGH: ..."
            severity = "Unknown"
            for sev in ("Critical", "High", "Medium", "Low"):
                if sev.upper() in title.upper():
                    severity = sev
                    break

            pan_id_match = re.search(r"PAN-SA-[\d-]+", title)
            pan_id = pan_id_match.group(0) if pan_id_match else ""

            advisories.append({
                "advisory_id": pan_id,
                "title": title,
                "severity": severity,
                "date": pub_date.strftime("%Y-%m-%d"),
                "link": link,
                "cves": cves,
                "cve_count": len(cves)
            })

        return advisories
    except Exception:
        return []


def _collect_html(year, month, month_str):
    try:
        resp = requests.get(PAN_URL, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        advisories = []

        # Look for advisory links and rows in the main table
        for row in soup.find_all(["tr", "li", "div"], class_=re.compile(r"advisory|row|item", re.I)):
            text = row.get_text(strip=True)
            cves = list(set(re.findall(r"CVE-\d{4}-\d+", text)))
            pan_ids = re.findall(r"PAN-SA-[\d-]+", text)
            
            # Try to find date in text
            date_match = re.search(r"\d{4}-\d{2}-\d{2}", text)
            if date_match:
                date_str = date_match.group(0)
                try:
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                    if date_obj.year != year or date_obj.month != month:
                        continue
                except Exception:
                    continue

            if pan_ids:
                link_tag = row.find("a")
                link = link_tag["href"] if link_tag else ""
                if link and not link.startswith("http"):
                    link = "https://security.paloaltonetworks.com" + link

                advisories.append({
                    "advisory_id": pan_ids[0] if pan_ids else "",
                    "title": text[:150],
                    "severity": "Unknown",
                    "date": date_match.group(0) if date_match else "",
                    "link": link,
                    "cves": cves,
                    "cve_count": len(cves)
                })

        return advisories
    except Exception:
        return []


if __name__ == "__main__":
    import json
    result = collect()
    print(json.dumps(result, indent=2))
