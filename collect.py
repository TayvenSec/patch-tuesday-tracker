"""
Main Collector — Patch Tuesday Tracker
Runs all platform collectors and saves combined JSON + markdown draft.
"""

import json
import os
import sys
import hashlib
from datetime import datetime
from pathlib import Path

# Add parent dir to path so collectors are importable
sys.path.insert(0, str(Path(__file__).parent))

from collectors import msrc, apple, ubuntu, android, redhat, debian, chromeos, palo_alto, cisco


DATA_DIR = Path(__file__).parent / "data"
LATEST_DIR = DATA_DIR / "latest"
ARCHIVE_DIR = DATA_DIR / "archive"


def run_all_collectors(year: int = None, month: int = None) -> dict:
    now = datetime.utcnow()
    year = year or now.year
    month = month or now.month

    print(f"\n{'='*60}")
    print(f"  Patch Tuesday Tracker — Collecting {datetime(year, month, 1).strftime('%B %Y')}")
    print(f"{'='*60}\n")

    results = {}
    collectors = {
        "windows": msrc,
        "apple": apple,
        "ubuntu": ubuntu,
        "android": android,
        "debian": debian,
        "chromeos": chromeos,
        "palo_alto": palo_alto,
        "cisco": cisco,
    }

    for name, module in collectors.items():
        print(f"[{'OK':>4}] Collecting {name}...")
        try:
            data = module.collect(year, month)
            results[name] = data
            print(f"       → {data.get('summary', 'Done')}")
        except Exception as e:
            print(f"[FAIL] {name}: {e}")
            results[name] = {"platform": name, "error": str(e), "summary": f"Collection failed: {e}"}

    print(f"\n{'='*60}")
    print(f"  Collection complete — {len(results)} platforms")
    print(f"{'='*60}\n")

    return {
        "collected_at": datetime.utcnow().isoformat() + "Z",
        "year": year,
        "month": month,
        "month_label": datetime(year, month, 1).strftime("%B %Y"),
        "platforms": results
    }


def _platforms_hash(data: dict) -> str:
    """Stable hash of the platforms payload only (ignores collected_at timestamp)."""
    payload = json.dumps(data.get("platforms", {}), sort_keys=True)
    return hashlib.md5(payload.encode()).hexdigest()


def has_data_changed(new_data: dict, existing_path: Path) -> bool:
    """Compare new platforms data against the previously saved file (like-for-like)."""
    if not existing_path.exists():
        return True

    try:
        existing = json.loads(existing_path.read_text())
        return _platforms_hash(existing) != _platforms_hash(new_data)
    except Exception:
        return True


def save_data(combined: dict) -> tuple[Path, Path]:
    """Save combined JSON to latest/ and archive/. Returns (json_path, md_path)."""
    LATEST_DIR.mkdir(parents=True, exist_ok=True)
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

    year = combined["year"]
    month = combined["month"]
    prefix = f"{year}-{month:02d}"

    # Save JSON
    json_latest = LATEST_DIR / "patch-data.json"
    json_archive = ARCHIVE_DIR / f"{prefix}-patch-data.json"

    json_str = json.dumps(combined, indent=2)
    json_latest.write_text(json_str)
    json_archive.write_text(json_str)

    print(f"[SAVE] JSON → {json_latest}")
    print(f"[SAVE] JSON → {json_archive}")

    return json_latest, json_archive


def main():
    # Allow override: python collect.py 2026 6
    args = sys.argv[1:]
    year = int(args[0]) if len(args) > 0 else None
    month = int(args[1]) if len(args) > 1 else None

    # Run collectors
    combined = run_all_collectors(year, month)

    # Check if data changed vs last run
    latest_json = LATEST_DIR / "patch-data.json"
    changed = has_data_changed(combined, latest_json)

    # Save data
    json_path, _ = save_data(combined)

    # Generate markdown draft
    from generate_draft import generate
    md_path = generate(combined)

    # Generate GitHub Pages site
    from generate_site import build
    build()

    # Signal for GitHub Actions: write a flag file if data changed
    flag_path = Path(__file__).parent / ".data_changed"
    if changed:
        flag_path.write_text("true")
        print("\n[INFO] New patch data detected — notification will be triggered.")
    else:
        if flag_path.exists():
            flag_path.unlink()
        print("\n[INFO] No new patch data since last run.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
