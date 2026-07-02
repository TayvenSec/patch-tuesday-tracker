"""
GitHub Pages Site Generator
Builds a minimal, clean HTML site from the collected patch data archive.
Output goes to /docs/ which GitHub Pages serves automatically.
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path


DATA_DIR = Path(__file__).parent / "data"
ARCHIVE_DIR = DATA_DIR / "archive"
LATEST_DIR = DATA_DIR / "latest"
DOCS_DIR = Path(__file__).parent / "docs"


CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, sans-serif;
    font-size: 16px;
    line-height: 1.6;
    color: #1a1a2e;
    background: #f8f9fa;
}
header {
    background: #1a1a2e;
    color: #fff;
    padding: 2rem 1rem;
    text-align: center;
}
header h1 { font-size: 1.8rem; font-weight: 700; letter-spacing: -0.5px; }
header p { color: #a0aec0; margin-top: 0.5rem; font-size: 0.95rem; }
.container { max-width: 900px; margin: 0 auto; padding: 2rem 1rem; }
.month-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 1.25rem;
    margin-top: 1.5rem;
}
.month-card {
    background: #fff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 1.25rem;
    transition: box-shadow 0.2s;
}
.month-card:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
.month-card h2 { font-size: 1.1rem; font-weight: 600; color: #1a1a2e; }
.month-card .meta { font-size: 0.8rem; color: #718096; margin-top: 0.25rem; }
.month-card .stats { margin-top: 0.75rem; display: flex; flex-wrap: wrap; gap: 0.4rem; }
.badge {
    display: inline-block;
    padding: 0.15rem 0.5rem;
    border-radius: 4px;
    font-size: 0.75rem;
    font-weight: 600;
}
.badge-critical { background: #fff5f5; color: #c53030; border: 1px solid #feb2b2; }
.badge-platform { background: #ebf8ff; color: #2b6cb0; border: 1px solid #bee3f8; }
.month-card .links { margin-top: 1rem; display: flex; gap: 0.75rem; }
.btn {
    display: inline-block;
    padding: 0.35rem 0.75rem;
    border-radius: 5px;
    font-size: 0.82rem;
    font-weight: 500;
    text-decoration: none;
    border: 1px solid #e2e8f0;
    color: #4a5568;
    background: #f7fafc;
    transition: background 0.15s;
}
.btn:hover { background: #edf2f7; }
.btn-primary { background: #1a1a2e; color: #fff; border-color: #1a1a2e; }
.btn-primary:hover { background: #2d3748; }
.section-title { font-size: 1.1rem; font-weight: 600; color: #4a5568; margin-top: 2rem; margin-bottom: 0.5rem; border-bottom: 2px solid #e2e8f0; padding-bottom: 0.5rem; }
.platform-table { width: 100%; border-collapse: collapse; margin-top: 1rem; font-size: 0.9rem; }
.platform-table th { text-align: left; padding: 0.5rem 0.75rem; background: #edf2f7; color: #4a5568; font-weight: 600; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; }
.platform-table td { padding: 0.6rem 0.75rem; border-bottom: 1px solid #e2e8f0; color: #2d3748; }
.platform-table tr:last-child td { border-bottom: none; }
.severity-critical { color: #c53030; font-weight: 600; }
.severity-high { color: #c05621; font-weight: 600; }
footer { text-align: center; padding: 2rem 1rem; color: #a0aec0; font-size: 0.82rem; border-top: 1px solid #e2e8f0; margin-top: 3rem; }
footer a { color: #718096; }
"""


def _severity_badge(count: int, label: str) -> str:
    if count == 0:
        return ""
    return f'<span class="badge badge-critical">{count} {label}</span>'


def _platform_badge(name: str) -> str:
    return f'<span class="badge badge-platform">{name}</span>'


def _build_index(months: list) -> str:
    cards = []
    for m in sorted(months, key=lambda x: x["prefix"], reverse=True):
        platforms = m.get("platforms", {})
        total_cves = sum(p.get("total_cves", 0) for p in platforms.values() if isinstance(p, dict))
        critical_total = sum(
            p.get("critical_count", 0) or p.get("severity_counts", {}).get("Critical", 0)
            for p in platforms.values() if isinstance(p, dict)
        )
        platform_names = [k.replace("_", " ").title() for k in platforms.keys() if platforms[k] and not platforms[k].get("error")]

        badges_html = "".join(_platform_badge(p) for p in platform_names[:5])
        critical_badge = _severity_badge(critical_total, "Critical") if critical_total else ""

        cards.append(f"""
        <div class="month-card">
            <h2>{m['month_label']}</h2>
            <div class="meta">Collected {m.get('collected_at', '')[:10]}</div>
            <div class="stats">
                {critical_badge}
                <span class="badge badge-platform">{total_cves}+ CVEs</span>
            </div>
            <div class="stats" style="margin-top:0.4rem">{badges_html}</div>
            <div class="links">
                <a href="{m['prefix']}.html" class="btn btn-primary">View Details</a>
                <a href="https://github.com/TayvenSec/patch-tuesday-tracker/blob/main/data/archive/{m['prefix']}-patch-draft.md" class="btn">Article Draft</a>
                <a href="https://github.com/TayvenSec/patch-tuesday-tracker/blob/main/data/archive/{m['prefix']}-patch-data.json" class="btn">JSON</a>
            </div>
        </div>""")

    cards_html = "\n".join(cards) if cards else "<p>No data collected yet. Run the collector to get started.</p>"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Patch Tuesday Tracker</title>
<style>{CSS}</style>
</head>
<body>
<header>
    <h1>🛡️ Patch Tuesday Tracker</h1>
    <p>Automated security patch data across Windows, Apple, Android, Linux, and network platforms</p>
</header>
<div class="container">
    <p class="section-title">Monthly Patch Roundups</p>
    <div class="month-grid">
        {cards_html}
    </div>
    <p style="margin-top:2rem;font-size:0.85rem;color:#718096;">
        Data collected daily via GitHub Actions. Sources: MSRC API, Apple HT201222, Ubuntu USN, 
        Android Security Bulletins, Red Hat RHSA, Debian DSA, Chrome Releases, Palo Alto Networks, Cisco.
    </p>
</div>
<footer>
    <p>
        <a href="https://github.com/TayvenSec/patch-tuesday-tracker">View on GitHub</a> · 
        <a href="https://tayvensec.com/patch-management/">Tayven Cyber Security</a>
    </p>
</footer>
</body>
</html>"""


def _build_month_page(combined: dict, prefix: str) -> str:
    month_label = combined.get("month_label", "")
    collected_at = combined.get("collected_at", "")[:10]
    platforms = combined.get("platforms", {})

    rows = []
    for key, data in platforms.items():
        if not isinstance(data, dict):
            continue
        name = key.replace("_", " ").title()
        total = data.get("total_cves", data.get("total_advisories", data.get("total_notices", data.get("total_releases", "—"))))
        critical = (
            data.get("critical_count") or
            data.get("severity_counts", {}).get("Critical", 0)
        )
        status = "⚠️ Error" if data.get("error") else "✅ OK"
        source = data.get("source", "")
        source_html = f'<a href="{source}" target="_blank">Source</a>' if source else "—"

        critical_html = f'<span class="severity-critical">{critical}</span>' if critical else "0"

        rows.append(f"""
        <tr>
            <td><strong>{name}</strong></td>
            <td>{total}</td>
            <td>{critical_html}</td>
            <td>{status}</td>
            <td>{source_html}</td>
        </tr>""")

    table_rows = "\n".join(rows)

    platform_sections = []
    for key, data in platforms.items():
        if not isinstance(data, dict) or data.get("error"):
            continue
        name = key.replace("_", " ").title()
        summary = data.get("summary", "")
        platform_sections.append(f"""
        <div style="margin-top:1.5rem;padding:1rem;background:#fff;border:1px solid #e2e8f0;border-radius:8px;">
            <strong>{name}</strong>
            <p style="margin-top:0.5rem;font-size:0.9rem;color:#4a5568;">{summary}</p>
        </div>""")

    sections_html = "\n".join(platform_sections)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{month_label} – Patch Tuesday Tracker</title>
<style>{CSS}</style>
</head>
<body>
<header>
    <h1>🛡️ {month_label} Patch Roundup</h1>
    <p>Collected {collected_at} · <a href="index.html" style="color:#a0aec0;">← All months</a></p>
</header>
<div class="container">
    <p class="section-title">Platform Summary</p>
    <table class="platform-table">
        <thead>
            <tr>
                <th>Platform</th>
                <th>Total CVEs / Advisories</th>
                <th>Critical</th>
                <th>Status</th>
                <th>Source</th>
            </tr>
        </thead>
        <tbody>
            {table_rows}
        </tbody>
    </table>

    <p class="section-title">Summaries</p>
    {sections_html}

    <div style="margin-top:2rem;display:flex;gap:1rem;flex-wrap:wrap;">
        <a href="https://github.com/TayvenSec/patch-tuesday-tracker/blob/main/data/archive/{prefix}-patch-draft.md" 
           class="btn btn-primary">📝 View Article Draft</a>
        <a href="https://github.com/TayvenSec/patch-tuesday-tracker/blob/main/data/archive/{prefix}-patch-data.json" 
           class="btn">⬇️ Download JSON</a>
        <a href="index.html" class="btn">← All Months</a>
    </div>
</div>
<footer>
    <p>
        <a href="https://github.com/TayvenSec/patch-tuesday-tracker">View on GitHub</a> · 
        <a href="https://tayvensec.com/patch-management/">Tayven Cyber Security</a>
    </p>
</footer>
</body>
</html>"""


def build():
    """Build the full GitHub Pages site from all archived data files."""
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    months = []

    # Load all archived JSON files
    if ARCHIVE_DIR.exists():
        for json_file in sorted(ARCHIVE_DIR.glob("*-patch-data.json")):
            prefix = json_file.stem.replace("-patch-data", "")
            try:
                combined = json.loads(json_file.read_text())
                months.append({**combined, "prefix": prefix})

                # Build per-month page
                month_html = _build_month_page(combined, prefix)
                out_path = DOCS_DIR / f"{prefix}.html"
                out_path.write_text(month_html)
                print(f"[SITE] Built {out_path.name}")

            except Exception as e:
                print(f"[SITE] Failed to build page for {json_file.name}: {e}")

    # Build index
    index_html = _build_index(months)
    (DOCS_DIR / "index.html").write_text(index_html)
    print(f"[SITE] Built index.html ({len(months)} months)")

    return DOCS_DIR


if __name__ == "__main__":
    build()
    print("Site built successfully.")
