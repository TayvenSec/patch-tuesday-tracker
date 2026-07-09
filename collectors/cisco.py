"""
Cisco Collector — Cisco Security Advisories
Primary: PSIRT openVuln API (optional, needs CISCO_CLIENT_ID/SECRET)
Fallback: Official Cisco PSIRT RSS feed (no auth)
"""

import os
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import re

CISCO_RSS_URL = "https://sec.cloudapps.cisco.com/security/center/psirtrss20/CiscoSecurityAdvisory.xml"
CISCO_API_TOKEN_URL = "https://id.cisco.com/oauth2/default/v1/token"
CISCO_API_URL = "https://api.cisco.com/security/advisories/v2"

# Set to True to only track IOS/IOS XE/network-OS advisories.
# False = all Cisco advisories (recommended: matches what Cisco actually
# publishes month to month; big IOS bundles only land in March/September).
IOS_ONLY = False
IOS_PATTERN = r"IOS|Catalyst|ASA|Firepower|NX-OS|SD-WAN"


def _get_api_token(client_id, client_secret):
    try:
        resp = requests.post(CISCO_API_TOKEN_URL, data={
            "grant_type": "client_credentials",
            "client_id": client_id, "client_secret": client_secret}, timeout=15)
        resp.raise_for_status()
        return resp.json().get("access_token")
    except Exception as e:
        print(f"[Cisco] API token fetch failed: {e}")
        return None


def _collect_api(year, month, token):
    advisories = []
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    try:
        resp = requests.get(f"{CISCO_API_URL}/year/{year}", headers=headers, timeout=30)
        resp.raise_for_status()
        for adv in resp.json().get("advisories", []):
            try:
                pub = datetime.strptime(adv.get("firstPublished", "")[:10], "%Y-%m-%d")
            except ValueError:
                continue
            if pub.month != month:
                continue
            affected = " ".join(adv.get("productNames", []))
            if IOS_ONLY and not re.search(IOS_PATTERN, affected, re.I):
                continue
            advisories.append({
                "advisory_id": adv.get("advisoryId", ""),
                "title": adv.get("advisoryTitle", ""),
                "severity": adv.get("sir", "Unknown"),
                "date": pub.strftime("%Y-%m-%d"),
                "link": adv.get("publicationUrl", ""),
                "cves": adv.get("cves", [])[:10],
                "cve_count": len(adv.get("cves", [])),
            })
    except Exception as e:
        print(f"[Cisco] API collection error: {e}")
    return advisories


def _collect_rss(year, month):
    advisories = []
    try:
        resp = requests.get(CISCO_RSS_URL, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
        resp.raise_for_status()
        root = ET.fromstring(resp.content)
    except Exception as e:
        print(f"[Cisco] RSS fetch failed: {e}")
        return []

    channel = root.find("channel")
    items = channel.findall("item") if channel is not None else root.findall(".//item")

    for item in items:
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        pub_str = (item.findtext("pubDate") or "").strip()
        desc = re.sub(r"<[^>]+>", " ", item.findtext("description") or "")

        try:
            pub = datetime.strptime(pub_str[:25].strip(), "%a, %d %b %Y %H:%M:%S")
        except ValueError:
            continue
        if pub.year != year or pub.month != month:
            continue

        combined = title + " " + desc
        if IOS_ONLY and not re.search(IOS_PATTERN, combined, re.I):
            continue

        severity = "Unknown"
        for sev in ("Critical", "High", "Medium", "Low"):
            if re.search(rf"\b{sev}\b", combined, re.I):
                severity = sev
                break

        cves = list(set(re.findall(r"CVE-\d{4}-\d+", combined)))
        id_match = re.search(r"cisco-sa-[\w-]+", link + " " + combined, re.I)

        advisories.append({
            "advisory_id": id_match.group(0) if id_match else "",
            "title": title,
            "severity": severity,
            "date": pub.strftime("%Y-%m-%d"),
            "link": link,
            "cves": cves[:10],
            "cve_count": len(cves),
        })
    return advisories


def collect(year: int = None, month: int = None) -> dict:
    now = datetime.utcnow()
    year = year or now.year
    month = month or now.month
    month_str = datetime(year, month, 1).strftime("%B %Y")

    client_id = os.environ.get("CISCO_CLIENT_ID")
    client_secret = os.environ.get("CISCO_CLIENT_SECRET")

    advisories, source_used, api_mode = [], CISCO_RSS_URL, False
    if client_id and client_secret:
        token = _get_api_token(client_id, client_secret)
        if token:
            advisories = _collect_api(year, month, token)
            source_used, api_mode = CISCO_API_URL, True
    if not advisories:
        advisories = _collect_rss(year, month)
        source_used, api_mode = CISCO_RSS_URL, False

    severity_counts = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
    for a in advisories:
        if a["severity"] in severity_counts:
            severity_counts[a["severity"]] += 1

    scope = "IOS/IOS XE" if IOS_ONLY else "security"
    summary = (
        f"Cisco published {len(advisories)} {scope} advisories in {month_str}. "
        f"Critical: {severity_counts['Critical']}, High: {severity_counts['High']}."
        if advisories else f"No Cisco {scope} advisories found for {month_str}."
    )

    return {
        "platform": "cisco", "month": month_str, "source": source_used,
        "api_mode": api_mode, "total_advisories": len(advisories),
        "total_cves": sum(a["cve_count"] for a in advisories),
        "severity_counts": severity_counts, "summary": summary,
        "advisories": advisories,
    }


if __name__ == "__main__":
    import json
    print(json.dumps(collect(), indent=2))
