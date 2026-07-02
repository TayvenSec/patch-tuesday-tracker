# 🛡️ Patch Tuesday Tracker

Automated security patch data collector across 9 major platforms. Runs daily via GitHub Actions, builds a GitHub Pages site, and generates a markdown article draft in the style of the [Tayven Cyber Security Patch Management Series](https://tayvensec.com/patch-management/).

Dashboard - https://tayvensec.github.io/patch-tuesday-tracker/index.html

## Platforms Covered

| Platform | Source | Method |
|---|---|---|
| Windows / Windows Server | [MSRC API](https://api.msrc.microsoft.com) | REST API (public) |
| Apple (iOS, macOS, watchOS, tvOS) | [Apple HT201222](https://support.apple.com/en-us/111900) | HTML scrape |
| Android | [Android Security Bulletin](https://source.android.com/docs/security/bulletin) | HTML scrape |
| Ubuntu | [Ubuntu USN RSS](https://usn.ubuntu.com/rss.xml) | RSS feed |
| Red Hat | [RHSA Atom Feed](https://access.redhat.com/security/team/updates/advisory.atom) | RSS/Atom feed |
| Debian | [Debian DSA RSS](https://www.debian.org/security/dsa-long) | RSS feed |
| Chrome OS | [Chrome Releases Blog](https://chromereleases.googleblog.com) | RSS feed |
| Palo Alto Networks | [PAN Security Advisories](https://security.paloaltonetworks.com) | RSS / HTML scrape |
| Cisco IOS / IOS XE | [Cisco Advisories](https://sec.cloudapps.cisco.com/security/center/publicationListing.x) | HTML scrape + optional API |

---

## What Gets Generated

Each run produces:

- **`data/latest/patch-data.json`** — Combined patch data from all platforms
- **`data/latest/patch-draft.md`** — Article draft in Tayven Cyber Security article format
- **`data/archive/YYYY-MM-patch-data.json`** — Monthly archived JSON
- **`data/archive/YYYY-MM-patch-draft.md`** — Monthly archived draft
- **`docs/`** — GitHub Pages site (auto-published)
- **GitHub Issue** — Notification when new data is detected

---

## Setup Guide

### Step 1: Fork or clone this repo

```bash
git clone https://github.com/TayvenSec/patch-tuesday-tracker.git
cd patch-tuesday-tracker
```

### Step 2: Enable GitHub Pages

1. Go to your repo on GitHub
2. Click **Settings** → **Pages**
3. Under **Source**, select **Deploy from a branch**
4. Branch: `main`, Folder: `/docs`
5. Click **Save**

Your site will be live at: `https://TayvenSec.github.io/patch-tuesday-tracker/`

### Step 3: Enable GitHub Actions

1. Go to **Actions** tab in your repo
2. If prompted, click **Enable GitHub Actions**
3. The workflow will now run automatically each day at 08:00 UTC

### Step 4: Set up issue notifications (automatic)

The workflow auto-creates a GitHub Issue when new patch data is detected.  
To receive email notifications:
1. Go to your repo → **Watch** → **All Activity**  
   OR  
2. Go to GitHub **Settings** → **Notifications** → ensure Issues notifications are enabled for email

### Step 5 (Optional): Add Cisco API credentials

For richer Cisco IOS/IOS XE data, register for the [Cisco PSIRT OpenVuln API](https://developer.cisco.com/docs/psirt/):

1. Register at [developer.cisco.com](https://developer.cisco.com/)
2. Create a new app and note your **Client ID** and **Client Secret**
3. In your GitHub repo: **Settings** → **Secrets and variables** → **Actions** → **New repository secret**
   - Name: `CISCO_CLIENT_ID` — Value: your Client ID
   - Name: `CISCO_CLIENT_SECRET` — Value: your Client Secret

Without these, the collector falls back to HTML scraping (still works, just less detail).

---

## Running Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run for current month
python collect.py

# Run for a specific month
python collect.py 2026 6

# Generate draft only (from existing data)
python generate_draft.py

# Build site only (from existing data)
python generate_site.py
```

---

## Repo Structure

```
patch-tuesday-tracker/
├── .github/
│   └── workflows/
│       └── collect-patches.yml   # Daily GitHub Actions workflow
├── collectors/
│   ├── msrc.py                   # Windows / Windows Server
│   ├── apple.py                  # iOS, macOS, watchOS, tvOS
│   ├── ubuntu.py                 # Ubuntu USN
│   ├── android.py                # Android Security Bulletin
│   ├── redhat.py                 # Red Hat RHSA
│   ├── debian.py                 # Debian DSA
│   ├── chromeos.py               # Chrome OS
│   ├── palo_alto.py              # Palo Alto Networks
│   └── cisco.py                  # Cisco IOS / IOS XE
├── data/
│   ├── latest/                   # Most recent collection
│   └── archive/                  # Monthly archive (grows over time)
├── docs/                         # GitHub Pages output
├── collect.py                    # Main orchestrator
├── generate_draft.py             # Markdown article draft generator
├── generate_site.py              # GitHub Pages site builder
├── requirements.txt
└── README.md
```

---

## Adding More Platforms

Each collector follows the same interface:

```python
# collectors/my_platform.py
def collect(year: int = None, month: int = None) -> dict:
    return {
        "platform": "my_platform",
        "month": "June 2026",
        "source": "https://...",
        "total_cves": 42,
        "summary": "One-line summary for the article draft",
        # ... platform-specific fields
    }
```

Then add it to `collect.py` in the `collectors` dict and add a section function to `generate_draft.py`.

---

## Article Draft Format

The generated `patch-draft.md` mirrors the structure of the Tayven Cyber Security patch roundup articles:

1. **Title** — `MONTH YEAR SECURITY PATCH ROUNDUP`
2. **Intro paragraph** — total CVE count across all platforms
3. **Per-platform sections** — Windows → Apple → Android → Ubuntu → Red Hat → Debian → ChromeOS → Palo Alto → Cisco
4. **Recommended Actions** — for Individuals / Businesses / Admins
5. **Closing Thoughts** — placeholder for your editorial commentary

---

## Acknowledgements

Built for the [Tayven Cyber Security](https://tayvensec.com) Patch Management Series.  
Data sourced from official vendor security feeds — no scraping of paywalled or non-public content.

---

## License

MIT — free to use, fork, and build on.
