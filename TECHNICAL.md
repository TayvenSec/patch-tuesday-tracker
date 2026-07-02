# Technical Breakdown — Patch Tuesday Tracker

This document explains how the Patch Tuesday Tracker works under the hood: the architecture, each data collector, the scheduling and automation, the outputs, and how to extend it.

**Companion post:** [Introducing the Patch Tuesday Tracker](https://tayvensec.com/) · **Live dashboard:** [tayvensec.github.io/patch-tuesday-tracker](https://tayvensec.github.io/patch-tuesday-tracker/)

---

## Architecture at a Glance

```
┌─────────────────────────────────────────────────────────┐
│                 GitHub Actions (daily cron)             │
│                     08:00 UTC / 6 PM AEST               │
└──────────────────────────┬──────────────────────────────┘
                           ▼
                     collect.py (orchestrator)
                           │
     ┌──────┬──────┬──────┼──────┬──────┬──────┬──────┐
     ▼      ▼      ▼      ▼      ▼      ▼      ▼      ▼
   msrc  apple ubuntu android redhat debian chromeos pan/cisco
   (API) (HTML) (RSS)  (HTML)  (Atom) (RSS)  (RSS)  (RSS/API)
     │      │      │      │      │      │      │      │
     └──────┴──────┴──────┴──────┴──────┴──────┴──────┘
                           │
                           ▼
              Combined JSON (data/latest + archive)
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
     generate_draft.py          generate_site.py
     (markdown article)         (GitHub Pages HTML)
                           │
                           ▼
          Change detected? → commit + GitHub Issue notification
```

There are no servers, databases, or external services. The entire system is:

- **Python 3.11** — collectors and generators (~1,500 lines total)
- **GitHub Actions** — free scheduler and compute
- **GitHub Pages** — free static hosting for the dashboard
- **The git repo itself** — acts as the database (JSON files, versioned)

Total running cost: **$0**. Public repos get unlimited GitHub Actions minutes, and a full run takes ~2 minutes.

---

## The Collectors

Each platform has a self-contained collector in `collectors/`, all exposing the same interface:

```python
def collect(year: int = None, month: int = None) -> dict
```

Each returns a dict with at minimum: `platform`, `month`, `source`, `summary`, and platform-specific fields (CVE lists, advisories, severity counts). Failures are isolated — if one vendor's page changes or is unreachable, the other eight still collect normally and the failure is flagged in the output rather than crashing the run.

### Data sources by method

| Collector | Source | Method | Notes |
|---|---|---|---|
| `msrc.py` | [MSRC CVRF API](https://api.msrc.microsoft.com) | REST API | Official Microsoft API, no auth. Fetches the monthly CVRF document (e.g. `2026-Jul`), parses CVEs, severities, and KB articles. |
| `apple.py` | [Apple security releases](https://support.apple.com/en-us/111900) | HTML scrape | Parses the releases table, filters to current month, then fetches each release page to count CVEs. |
| `ubuntu.py` | [Ubuntu security notices](https://ubuntu.com/security/notices/rss.xml) | RSS | Official Canonical feed. Extracts USN IDs, CVEs, and severity keywords. |
| `android.py` | [Android Security Bulletin](https://source.android.com/docs/security/bulletin) | HTML scrape | Fetches the month's bulletin directly (`/bulletin/YYYY-MM`), parses severity tables and patch levels. |
| `redhat.py` | [RHSA Atom feed](https://access.redhat.com/security/team/updates/advisory.atom) | Atom | Filters to RHSA (security) advisories only, skipping RHBA/RHEA. Severity parsed from advisory titles. |
| `debian.py` | [Debian DSA feed](https://www.debian.org/security/dsa-long) | RSS | Long-form DSA feed with descriptions; extracts DSA IDs, packages, and CVEs. |
| `chromeos.py` | [Chrome Releases blog](https://chromereleases.googleblog.com/feeds/posts/default) | RSS (feedparser) | Filters posts to ChromeOS / Stable channel / LTS entries; extracts CVEs and version numbers. |
| `palo_alto.py` | [PAN security advisories](https://security.paloaltonetworks.com) | RSS → HTML fallback | Tries the RSS feed first; falls back to scraping the advisories listing if the feed fails. |
| `cisco.py` | [Cisco PSIRT openVuln API](https://developer.cisco.com/docs/psirt/) or [public advisories page](https://sec.cloudapps.cisco.com/security/center/publicationListing.x) | API → HTML fallback | If `CISCO_CLIENT_ID`/`CISCO_CLIENT_SECRET` secrets are set, uses the official OAuth2 API (much richer data). Otherwise scrapes the public listing. Filters to IOS/IOS XE/Catalyst/ASA/Firepower. |

### Common parsing patterns

- **CVE extraction** — regex `CVE-\d{4}-\d+` against page/feed content, deduplicated
- **Month filtering** — every collector filters items to the requested year+month, so a single run only ever represents one patch cycle
- **Severity detection** — from structured fields where available (MSRC, Cisco API), otherwise keyword matching in titles/descriptions
- **Politeness** — one request per source per day (Apple makes a handful extra to count CVEs per release), 15–30s timeouts, standard user-agent

---

## The Orchestrator (`collect.py`)

The daily entry point. It:

1. Runs all nine collectors for the current month (or a specific month via `python collect.py 2026 6`)
2. Combines results into a single JSON document with a UTC timestamp
3. **Detects change** — hashes the `platforms` payload (ignoring the timestamp) and compares against the previously saved file. This is what prevents daily notification spam: no new vendor data → no commit, no issue.
4. Saves to both `data/latest/` (always-current) and `data/archive/YYYY-MM-*` (permanent monthly record)
5. Calls the two generators (below)
6. Writes a `.data_changed` flag file if anything changed — the GitHub Actions workflow uses this to decide whether to open a notification issue

### Data layout

```
data/
├── latest/
│   ├── patch-data.json    # current month, always overwritten
│   └── patch-draft.md     # current month's article draft
└── archive/
    ├── 2026-07-patch-data.json
    ├── 2026-07-patch-draft.md
    └── ...                # grows by exactly 2 files per month
```

Within a month, files are **overwritten in place** as data accumulates — so `2026-07-patch-draft.md` gets progressively more complete through July, then freezes when August begins.

---

## The Generators

### `generate_draft.py` — article draft

Transforms the combined JSON into a markdown article mirroring the [Tayven Cyber Security patch roundup format](https://tayvensec.com/patch-management/):

1. Title + intro with combined CVE count
2. Per-platform sections (Windows → Apple → Android → Ubuntu → Red Hat → Debian → ChromeOS → Palo Alto → Cisco), each with key CVEs/advisories and platform-specific recommended actions
3. Consolidated Recommended Actions (Individuals / Businesses / Admins)
4. Closing Thoughts placeholder for editorial commentary

Each platform has its own section-builder function, so the format of one platform can be tweaked without touching the others.

### `generate_site.py` — dashboard

Builds the static GitHub Pages site into `docs/`:

- **`index.html`** — card grid of every archived month, with total CVE and Critical counts per month
- **`YYYY-MM.html`** — per-month detail page: platform summary table (totals, criticals, collection status, source links) plus per-platform summaries

The site is plain HTML + inline CSS — no JavaScript framework, no build step, no external dependencies. A `.nojekyll` file tells GitHub Pages to serve it as-is without running Jekyll.

---

## Automation (`.github/workflows/collect-patches.yml`)

The single workflow does everything:

```yaml
on:
  schedule:
    - cron: "0 8 * * *"     # daily 08:00 UTC = 6 PM AEST
  workflow_dispatch:         # manual runs, with optional year/month inputs
```

**Steps:** checkout → Python 3.11 setup → `pip install` → run `collect.py` → commit `data/` and `docs/` if changed → open a GitHub Issue if the `.data_changed` flag exists.

**Permissions:** the workflow requests only `contents: write` (to commit data) and `issues: write` (to create notifications) — the minimum needed.

**Secrets:** two optional repository secrets, `CISCO_CLIENT_ID` and `CISCO_CLIENT_SECRET`, upgrade the Cisco collector from scraping to the official API. No other credentials exist anywhere in the system.

**Notifications:** when new data lands, the workflow opens an issue titled "📋 New Patch Data: [Month]" containing each platform's one-line summary and links to the draft and dashboard. Watching the repo turns these into emails. In practice, expect a cluster of activity around Patch Tuesday (second Tuesday of the month) and scattered updates from the Linux distros throughout.

**Turning it off:** Actions tab → Collect Patch Data → ⋯ → Disable workflow. GitHub also auto-pauses scheduled workflows after 60 days of repo inactivity (it emails a warning first).

---

## Design Decisions

**Why daily, not hourly?** Vendors publish on monthly cycles; daily collection captures everything within 24 hours of publication while staying an extremely polite consumer of vendor sites. There is no scenario where hourly polling of monthly data adds value.

**Why git as the database?** The dataset is small (two files per month), naturally versioned, and benefits from being human-readable and diffable. Every historical change to the data is preserved in commit history for free.

**Why official feeds over scraping wherever possible?** Five of nine sources are RSS/Atom/API — formats vendors publish *specifically* for machine consumption. They're stable, structured, and immune to page redesigns. Scraping is used only where no feed exists (Apple, Android) and always against public advisory pages.

**Why isolate collector failures?** Vendor pages change. A redesigned Apple page shouldn't cost you that month's Ubuntu data. Failed collectors report an error string in their section of the JSON and the draft flags them with a ⚠️, making breakage visible rather than silent.

**Why overwrite monthly files instead of appending daily snapshots?** The meaningful unit for patch management is the monthly cycle. Daily snapshots would multiply files 30× while adding no analytical value — and git history preserves the intermediate states anyway.

---

## Extending It

### Adding a platform

1. Create `collectors/newplatform.py` implementing `collect(year, month) -> dict` with the standard keys (`platform`, `month`, `source`, `summary`, plus your data)
2. Register it in the `collectors` dict in `collect.py`
3. Add a `_newplatform_section()` function to `generate_draft.py` and register it in the `section_funcs` list

Prefer an official RSS/Atom feed or API if the vendor offers one. The Ubuntu or Red Hat collectors are the best templates for feed-based sources; Android for scrape-based ones.

### Changing the schedule

Edit the cron line in the workflow. Examples: `"0 8,20 * * *"` (twice daily), `"0 8 * * 2,3"` (Tuesdays and Wednesdays only).

### Running locally

```bash
pip install -r requirements.txt
python collect.py            # current month
python collect.py 2026 6     # specific month
```

Outputs land in `data/` and `docs/` exactly as they do in CI.

---

## Dependencies

Four Python packages, all mainstream and actively maintained:

- `requests` — HTTP
- `beautifulsoup4` + `lxml` — HTML parsing
- `feedparser` — RSS/Atom parsing

---

## Limitations & Honest Caveats

- **Scrapers can break.** Apple, Android, Palo Alto (fallback), and Cisco (fallback) depend on page structure. Breakage shows up as a flagged error, not silent bad data — but it requires a small code fix when it happens.
- **Severity heuristics vary.** Where vendors don't expose structured severity (Ubuntu, Debian feeds), it's inferred from keywords and should be treated as indicative.
- **CVE counts are approximate for scraped sources.** Regex extraction over a page can occasionally over- or under-count relative to the vendor's official tally.
- **Not a vulnerability scanner.** This tracks *published patches and advisories* — it tells you what vendors released, not what's exploited or what your environment is exposed to.

---

*Built for the [Tayven Cyber Security Patch Management Series](https://tayvensec.com/patch-management/). MIT licensed — fork it, run it, improve it.*
