"""
Cisco Collector — Cisco IOS / IOS XE Security Advisories
Source: Cisco Security Advisories page + optional Cisco PSIRT OpenVuln API
URL: https://sec.cloudapps.cisco.com/security/center/publicationListing.x

OPTIONAL API: The Cisco PSIRT OpenVuln API gives structured data.
To use it:
  1. Register at https://developer.cisco.com/
  2. Create an app and get Client ID + Client Secret
  3. Set env vars: CISCO_CLIENT_ID and CISCO_CLIENT_SECRET

Without the API, this collector falls back to scraping the public advisories page.
"""

import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re


CISCO_PUBLIC_URL = "https://sec.cloudapps.cisco.com/security/center/publicationListing.x"
CISCO_API_TOKEN_URL = "https://id.cisco.com/oauth2/default/v1/token"
CISCO_API_URL = "https://api.cisco.com/security/advisories/v2"


def _get_api_token(client_id: str, client_secret: str) -> str | None:
    try:
        resp = requests.post(
            CISCO_API_TOKEN_URL,
            data={
                "grant_type": "client_credentials",
                "client_id": client_id,
                "client_secret": client_secret
            },
            timeout=15
        )
        resp.raise_for_status()
        return resp.json().get("access_token")
    except Exception as e:
        print(f"[Cisco] API token fetch failed: {e}")
        return None


def _collect_api(year: int, month: int, token: str) -> list:
    """Use Cisco PSIRT OpenVuln API — requires registered API credentials."""
    advisories = []
    month_str_short = datetime(year, month, 1).strftime("%Y-%m")

    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

    try:
        # Get advisories by year
        url = f"{CISCO_API_URL}/year/{year}"
        resp = requests.get(url, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        for adv in data.get("advisories", []):
            pub_date_str = adv.get("firstPublished", "")
            try:
                pub_date = datetime.strptime(pub_date_str[:10], "%Y-%m-%d")
            except Exception:
                continue

            if pub_date.month != month:
                continue

            # Filter to IOS / IOS XE products only
            affected = " ".join(adv.get("productNames", []))
            if not re.search(r"IOS|IOS XE|Catalyst|ASA|Firepower", affected, re.I):
                continue

            cves = adv.get("cves", [])
            severity = adv.get("sir", "Unknown")  # SIR = Security Impact Rating

            advisories.append({
                "advisory_id": adv.get("advisoryId", ""),
                "title": adv.get("advisoryTitle", ""),
                "severity": severity,
                "date": pub_date.strftime("%Y-%m-%d"),
                "link": adv.get("publicationUrl", ""),
                "cves": cves[:10],
                "cve_count": len(cves),
                "affected_products": adv.get("productNames", [])[:5]
            })

    except Exception as e:
        print(f"[Cisco] API collection error: {e}")

    return advisories


def _collect_html(year: int, month: int) -> list:
    """Fallback: scrape the public Cisco advisories listing page."""
    advisories = []
    month_str = datetime(year, month, 1).strftime("%B %Y")

    try:
        resp = requests.get(
            CISCO_PUBLIC_URL,
            timeout=30,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        resp.raise_for_status()
    except Exception as e:
        print(f"[Cisco] HTML scrape failed: {e}")
        return []

    soup = BeautifulSoup(resp.text, "html.parser")

    # Look for advisory rows — Cisco's table has date, title, severity columns
    for row in soup.select("tr, .advisoryListRow"):
        cols = row.find_all("td")
        if len(cols) < 3:
            continue

        text = row.get_text(" ", strip=True)

        # Date check
        date_match = re.search(r"(\d{4}-\d{2}-\d{2}|\w+ \d{1,2}, \d{4})", text)
        if not date_match:
            continue

        date_raw = date_match.group(0)
        try:
            try:
                pub_date = datetime.strptime(date_raw, "%Y-%m-%d")
            except ValueError:
                pub_date = datetime.strptime(date_raw, "%B %d, %Y")
        except Exception:
            continue

        if pub_date.year != year or pub_date.month != month:
            continue

        # Filter IOS-related
        if not re.search(r"IOS|Catalyst|ASA|Firepower|NX-OS", text, re.I):
            continue

        link_tag = row.find("a")
        link = link_tag["href"] if link_tag else ""
        if link and not link.startswith("http"):
            link = "https://sec.cloudapps.cisco.com" + link

        cves = list(set(re.findall(r"CVE-\d{4}-\d+", text)))

        severity = "Unknown"
        for sev in ("Critical", "High", "Medium", "Low"):
            if sev.lower() in text.lower():
                severity = sev
                break

        title_tag = row.find("a")
        title = title_tag.get_text(strip=True) if title_tag else text[:100]

        cisco_id_match = re.search(r"cisco-sa-[\w-]+", link + text, re.I)
        cisco_id = cisco_id_match.group(0) if cisco_id_match else ""

        advisories.append({
            "advisory_id": cisco_id,
            "title": title,
            "severity": severity,
            "date": pub_date.strftime("%Y-%m-%d"),
            "link": link,
            "cves": cves[:10],
            "cve_count": len(cves)
        })

    return advisories


def collect(year: int = None, month: int = None) -> dict:
    now = datetime.utcnow()
    year = year or now.year
    month = month or now.month

    month_str = datetime(year, month, 1).strftime("%B %Y")

    # Try API first if credentials are set
    client_id = os.environ.get("CISCO_CLIENT_ID")
    client_secret = os.environ.get("CISCO_CLIENT_SECRET")

    advisories = []
    source_used = "html_scrape"

    if client_id and client_secret:
        print("[Cisco] API credentials found — using PSIRT OpenVuln API")
        token = _get_api_token(client_id, client_secret)
        if token:
            advisories = _collect_api(year, month, token)
            source_used = CISCO_API_URL
    
    if not advisories:
        print("[Cisco] Falling back to HTML scrape")
        advisories = _collect_html(year, month)
        source_used = CISCO_PUBLIC_URL

    severity_counts = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
    for adv in advisories:
        sev = adv.get("severity", "")
        if sev in severity_counts:
            severity_counts[sev] += 1

    total_cves = sum(a.get("cve_count", 0) for a in advisories)

    api_note = "" if (client_id and client_secret) else " (Set CISCO_CLIENT_ID + CISCO_CLIENT_SECRET env vars for full API access.)"
    summary = (
        f"Cisco published {len(advisories)} IOS/IOS XE advisories in {month_str}. "
        f"Critical: {severity_counts['Critical']}, High: {severity_counts['High']}."
        f"{api_note}"
        if advisories
        else f"No Cisco advisories found for {month_str}.{api_note}"
    )

    return {
        "platform": "cisco",
        "month": month_str,
        "source": source_used,
        "api_mode": source_used != CISCO_PUBLIC_URL,
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
