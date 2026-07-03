"""
Markdown Draft Generator
Produces a patch roundup article draft in the style of tayvensec.com articles.
"""

import json
from datetime import datetime
from pathlib import Path


DATA_DIR = Path(__file__).parent / "data"
LATEST_DIR = DATA_DIR / "latest"
ARCHIVE_DIR = DATA_DIR / "archive"


def _windows_section(data: dict) -> str:
    if not data or data.get("error"):
        return "## Windows Updates\n\n> ⚠️ Data collection failed for this platform.\n\n"

    lines = [f"# Windows Updates – {data.get('month', '')}\n"]

    cves = data.get("cves", [])
    critical = [c for c in cves if c.get("severity", "").lower() == "critical"]
    important = [c for c in cves if c.get("severity", "").lower() == "important"]

    lines.append(f"Microsoft addressed **{data.get('total_cves', 0)} CVEs** this month — "
                 f"**{len(critical)} Critical** and **{len(important)} Important**.\n")

    kb_articles = data.get("kb_articles", [])
    if kb_articles:
        lines.append("\n## Key KB Articles\n")
        for kb in kb_articles[:8]:
            lines.append(f"- **{kb.get('name', '')}**")

    if critical:
        lines.append("\n## Critical CVEs\n")
        for cve in critical[:10]:
            lines.append(f"- **{cve['cve_id']}** — {cve.get('title', 'No title')}")

    lines.append("\n### Recommended Actions\n")
    lines.append("- Apply Windows and Windows Server updates via Windows Update or WSUS\n"
                 "- Prioritise Critical CVEs — especially any remote code execution or privilege escalation\n"
                 "- Validate Secure Boot and BitLocker configurations post-update\n")

    return "\n".join(lines) + "\n"


def _apple_section(data: dict) -> str:
    if not data or data.get("error"):
        return "## Apple Security Updates\n\n> ⚠️ Data collection failed for this platform.\n\n"

    lines = [f"# Apple Security Updates – {data.get('month', '')}\n"]
    updates = data.get("updates", [])

    if not updates:
        lines.append("No Apple security releases found this month.\n")
        return "\n".join(lines) + "\n"

    for upd in updates:
        lines.append(f"\n## {upd['name']}\n")
        lines.append(f"**Release date:** {upd.get('date', 'Unknown')}  ")
        lines.append(f"**CVEs addressed:** {upd.get('cve_count', 0)}\n")
        if upd.get("link"):
            lines.append(f"[View Apple security release]({upd['link']})\n")
        if upd.get("cves"):
            lines.append("\n**Selected CVEs:** " + ", ".join(upd["cves"][:8]))

    lines.append("\n### Recommended Actions\n")
    lines.append("- Apply iOS and macOS updates via Settings → General → Software Update\n"
                 "- Update watchOS and tvOS via their respective device settings\n"
                 "- Enterprise: push updates via MDM (Jamf, Mosyle, etc.)\n")

    return "\n".join(lines) + "\n"


def _android_section(data: dict) -> str:
    if not data or data.get("error"):
        return "## Android Security Bulletin\n\n> ⚠️ Data collection failed for this platform.\n\n"

    lines = [f"# Android Security Bulletin – {data.get('month', '')}\n"]
    severity = data.get("severity_counts", {})

    lines.append(f"Google's {data.get('month', '')} bulletin addresses **{data.get('total_cves', 0)} CVEs** "
                 f"across Framework, System, Kernel, and vendor components.\n")
    lines.append(f"- **Critical:** {severity.get('Critical', 0)}")
    lines.append(f"- **High:** {severity.get('High', 0)}")
    lines.append(f"- **Moderate:** {severity.get('Moderate', 0)}\n")

    patch_levels = data.get("patch_levels", [])
    if patch_levels:
        lines.append(f"**Patch levels:** {', '.join(patch_levels[:3])}\n")

    vulns = data.get("vulnerabilities", [])
    critical_vulns = [v for v in vulns if v.get("severity") == "Critical"]
    if critical_vulns:
        lines.append("\n## Critical Vulnerabilities\n")
        for v in critical_vulns[:8]:
            lines.append(f"- **{v['cve_id']}** — {v.get('type', '')} ({v.get('component', '')})")

    lines.append("\n### Recommended Actions\n")
    lines.append("- Update Android devices to the latest patch level\n"
                 "- Enterprise: enforce patch compliance via MDM\n"
                 "- Check vendor-specific bulletins (Samsung, Pixel, etc.)\n")

    return "\n".join(lines) + "\n"


def _ubuntu_section(data: dict) -> str:
    if not data or data.get("error"):
        return "## Ubuntu Security Notices\n\n> ⚠️ Data collection failed for this platform.\n\n"

    lines = [f"# Ubuntu Security Notices – {data.get('month', '')}\n"]
    notices = data.get("notices", [])

    lines.append(f"Canonical published **{data.get('total_notices', 0)} USNs** covering "
                 f"**{data.get('total_cves', 0)} CVEs** this month.\n")

    if notices:
        lines.append("\n## Key Security Notices\n")
        for notice in notices[:10]:
            lines.append(f"\n### {notice.get('usn_id', '')} – {notice.get('title', '')}")
            lines.append(f"**Severity:** {notice.get('severity', 'Unknown')}  "
                         f"**CVEs:** {notice.get('cve_count', 0)}")
            if notice.get("link"):
                lines.append(f"[View USN]({notice['link']})")
            if notice.get("cves"):
                lines.append("**CVE IDs:** " + ", ".join(notice["cves"][:6]))

    lines.append("\n### Recommended Actions\n")
    lines.append("- Run `sudo apt update && sudo apt upgrade` on all Ubuntu systems\n"
                 "- Prioritise kernel USNs — may require reboot\n"
                 "- Review USNs affecting your specific Ubuntu LTS version\n")

    return "\n".join(lines) + "\n"


def _redhat_section(data: dict) -> str:
    if not data or data.get("error"):
        return "## Red Hat Security Advisories\n\n> ⚠️ Data collection failed for this platform.\n\n"

    lines = [f"# Red Hat Security Advisories – {data.get('month', '')}\n"]
    severity = data.get("severity_counts", {})

    lines.append(f"Red Hat published **{data.get('total_advisories', 0)} RHSAs** covering "
                 f"**{data.get('total_cves', 0)} CVEs** — "
                 f"Critical: {severity.get('Critical', 0)}, Important: {severity.get('Important', 0)}.\n")

    advisories = data.get("advisories", [])
    critical = [a for a in advisories if a.get("severity") == "Critical"]
    if critical:
        lines.append("\n## Critical Advisories\n")
        for adv in critical[:6]:
            lines.append(f"- **{adv['advisory_id']}** — {adv.get('title', '')}")
            if adv.get("link"):
                lines.append(f"  [View advisory]({adv['link']})")

    lines.append("\n### Recommended Actions\n")
    lines.append("- Apply updates via `dnf update` or `yum update`\n"
                 "- Prioritise Critical and Important RHSAs\n"
                 "- RHEL subscribers can use Red Hat Satellite or Insights for fleet management\n")

    return "\n".join(lines) + "\n"


def _debian_section(data: dict) -> str:
    if not data or data.get("error"):
        return "## Debian Security Advisories\n\n> ⚠️ Data collection failed for this platform.\n\n"

    lines = [f"# Debian Security Advisories – {data.get('month', '')}\n"]

    lines.append(f"Debian published **{data.get('total_advisories', 0)} DSAs** covering "
                 f"**{data.get('total_cves', 0)} CVEs** this month.\n")

    advisories = data.get("advisories", [])
    if advisories:
        lines.append("\n## Key DSAs\n")
        for adv in advisories[:8]:
            lines.append(f"- **{adv.get('dsa_id', '')}** — {adv.get('package', '')} "
                         f"({adv.get('cve_count', 0)} CVEs)")

    lines.append("\n### Recommended Actions\n")
    lines.append("- Run `sudo apt update && sudo apt upgrade` on Debian systems\n"
                 "- Check [Debian Security Tracker](https://security-tracker.debian.org) for package-level detail\n")

    return "\n".join(lines) + "\n"


def _chromeos_section(data: dict) -> str:
    if not data or data.get("error"):
        return "## Chrome OS Updates\n\n> ⚠️ Data collection failed for this platform.\n\n"

    lines = [f"# Chrome OS Updates – {data.get('month', '')}\n"]

    lines.append(f"Google released **{data.get('total_releases', 0)} ChromeOS updates** covering "
                 f"**{data.get('total_cves', 0)} CVEs** this month.\n")

    releases = data.get("releases", [])
    for rel in releases[:5]:
        lines.append(f"\n## {rel.get('title', '')}")
        lines.append(f"**Date:** {rel.get('date', '')}  **CVEs:** {rel.get('cve_count', 0)}")
        if rel.get("versions"):
            lines.append(f"**Version(s):** {', '.join(rel['versions'][:3])}")
        if rel.get("link"):
            lines.append(f"[View release notes]({rel['link']})")

    lines.append("\n### Recommended Actions\n")
    lines.append("- ChromeOS updates automatically; verify via Settings → About ChromeOS\n"
                 "- Enterprise: manage rollouts via Google Admin Console\n")

    return "\n".join(lines) + "\n"


def _palo_alto_section(data: dict) -> str:
    if not data or data.get("error"):
        return "## Palo Alto Networks Advisories\n\n> ⚠️ Data collection failed for this platform.\n\n"

    lines = [f"# Palo Alto Networks Advisories – {data.get('month', '')}\n"]
    severity = data.get("severity_counts", {})

    lines.append(f"Palo Alto Networks published **{data.get('total_advisories', 0)} advisories** — "
                 f"Critical: {severity.get('Critical', 0)}, High: {severity.get('High', 0)}.\n")

    advisories = data.get("advisories", [])
    high_crit = [a for a in advisories if a.get("severity") in ("Critical", "High")]
    if high_crit:
        lines.append("\n## Critical & High Advisories\n")
        for adv in high_crit[:6]:
            lines.append(f"- **{adv.get('advisory_id', '')}** [{adv.get('severity', '')}] — {adv.get('title', '')[:100]}")

    lines.append("\n### Recommended Actions\n")
    lines.append("- Review advisories at [security.paloaltonetworks.com](https://security.paloaltonetworks.com)\n"
                 "- Update PAN-OS via Panorama or device console\n"
                 "- Apply threat prevention content updates\n")

    return "\n".join(lines) + "\n"


def _cisco_section(data: dict) -> str:
    if not data or data.get("error"):
        return "## Cisco IOS / IOS XE Advisories\n\n> ⚠️ Data collection failed for this platform.\n\n"

    lines = [f"# Cisco IOS / IOS XE Advisories – {data.get('month', '')}\n"]
    severity = data.get("severity_counts", {})

    api_note = "" if data.get("api_mode") else " *(HTML scrape — set CISCO_CLIENT_ID/SECRET for full API data)*"
    lines.append(f"Cisco published **{data.get('total_advisories', 0)} IOS/IOS XE advisories** — "
                 f"Critical: {severity.get('Critical', 0)}, High: {severity.get('High', 0)}.{api_note}\n")

    advisories = data.get("advisories", [])
    high_crit = [a for a in advisories if a.get("severity") in ("Critical", "High")]
    if high_crit:
        lines.append("\n## Critical & High Advisories\n")
        for adv in high_crit[:6]:
            lines.append(f"- **{adv.get('advisory_id', '')}** [{adv.get('severity', '')}] — {adv.get('title', '')[:100]}")

    lines.append("\n### Recommended Actions\n")
    lines.append("- Review advisories at [sec.cloudapps.cisco.com](https://sec.cloudapps.cisco.com/security/center/publicationListing.x)\n"
                 "- Apply IOS XE updates via `install add file` process\n"
                 "- Use Cisco's Software Checker tool for version impact analysis\n")

    return "\n".join(lines) + "\n"


def generate(combined: dict = None) -> Path:
    """Generate a markdown draft article from combined patch data."""

    # Load from file if not passed directly
    if combined is None:
        latest_json = LATEST_DIR / "patch-data.json"
        if not latest_json.exists():
            raise FileNotFoundError("No patch data found. Run collect.py first.")
        combined = json.loads(latest_json.read_text())

    platforms = combined.get("platforms", {})
    month_label = combined.get("month_label", "")
    year = combined.get("year", datetime.utcnow().year)
    month = combined.get("month", datetime.utcnow().month)

    # --- Build the article ---
    lines = []

    # Title
    lines.append(f"# {month_label.upper()} SECURITY PATCH ROUNDUP – Windows, iOS, macOS, Android, Linux & More\n")

    # Intro
    total_cves = sum(
        p.get("total_cves", 0) for p in platforms.values() if isinstance(p, dict)
    )
    lines.append(
        f"{month_label}'s patch cycle brings updates across all major platforms. "
        f"This month's roundup covers Windows, Apple, Android, Ubuntu, Red Hat, Debian, "
        f"ChromeOS, Palo Alto Networks, and Cisco IOS/IOS XE. "
        f"Combined, this month addresses approximately **{total_cves}+ CVEs** across the ecosystem.\n"
    )
    lines.append("Below is the full breakdown.\n")
    lines.append("---\n")

    # Per-platform sections
    section_funcs = [
        ("windows", _windows_section),
        ("apple", _apple_section),
        ("android", _android_section),
        ("ubuntu", _ubuntu_section),
        ("debian", _debian_section),
        ("chromeos", _chromeos_section),
        ("palo_alto", _palo_alto_section),
        ("cisco", _cisco_section),
    ]

    for key, fn in section_funcs:
        lines.append(fn(platforms.get(key, {})))
        lines.append("---\n")

    # Recommended Actions summary
    lines.append("# Recommended Actions\n")
    lines.append("## For Individuals\n")
    lines.append("- Apply Windows 10/11 and iOS/macOS updates immediately\n"
                 "- Update Android devices to the latest available patch level\n"
                 "- Ensure ChromeOS devices have auto-update enabled\n")
    lines.append("\n## For Businesses\n")
    lines.append("- Prioritise kernel updates across Windows Server and Linux distributions\n"
                 "- Patch network appliances (Palo Alto, Cisco) — these are high-value targets\n"
                 "- Enforce patch compliance across Android fleets via MDM\n"
                 "- Review Red Hat and Debian advisories relevant to your server stack\n")
    lines.append("\n## For Admins\n")
    lines.append("- Use WSUS, SCCM, or Intune to validate Windows patch rollout\n"
                 "- Test kernel updates in non-prod before rolling to production Linux hosts\n"
                 "- Check Cisco Software Checker for IOS XE version impact\n"
                 "- Monitor PAN-OS advisories — Critical severity warrants emergency patching\n")

    lines.append("\n---\n")

    # Closing thoughts
    lines.append("# Closing Thoughts\n")
    lines.append(
        f"> ✏️ *Writer's note: Add your closing commentary here — key themes from this month, "
        f"what stood out, and what to watch for next month.*\n"
    )
    lines.append(
        "\n## Explore the Full Patch Management Series\n"
        "[View the Patch Management Series](https://tayvensec.com/patch-management/)\n"
    )

    # Footer metadata
    lines.append(f"\n---\n*Data collected automatically via [patch-tuesday-tracker](https://github.com/YOUR_USERNAME/patch-tuesday-tracker). "
                 f"Generated: {combined.get('collected_at', '')}*\n")

    # Save
    LATEST_DIR.mkdir(parents=True, exist_ok=True)
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

    prefix = f"{year}-{month:02d}"
    md_latest = LATEST_DIR / "patch-draft.md"
    md_archive = ARCHIVE_DIR / f"{prefix}-patch-draft.md"

    content = "\n".join(lines)
    md_latest.write_text(content)
    md_archive.write_text(content)

    print(f"[SAVE] Markdown → {md_latest}")
    print(f"[SAVE] Markdown → {md_archive}")

    return md_latest


if __name__ == "__main__":
    path = generate()
    print(f"\nDraft saved to: {path}")
