"""Download the six NYC Uber pickup CSVs for April–September 2014.

Source: FiveThirtyEight's uber-tlc-foil-response repository.
The source revision is pinned so the input files do not silently change.
"""
from __future__ import annotations

import argparse
import csv
import shutil
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent
RAW_DIR = ROOT / "data" / "raw"
SOURCE_BASE = (
    "https://raw.githubusercontent.com/fivethirtyeight/"
    "uber-tlc-foil-response/63bb878b76f47f69b4527d50af57aac26dead983/"
    "uber-trip-data/"
)
FILES = [
    "uber-raw-data-apr14.csv",
    "uber-raw-data-may14.csv",
    "uber-raw-data-jun14.csv",
    "uber-raw-data-jul14.csv",
    "uber-raw-data-aug14.csv",
    "uber-raw-data-sep14.csv",
]
EXPECTED_COLUMNS = ["Date/Time", "Lat", "Lon", "Base"]


def is_valid_csv(path: Path) -> bool:
    if not path.exists() or path.stat().st_size == 0:
        return False
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.reader(handle)
            header = next(reader)
            first_row = next(reader)
        return header == EXPECTED_COLUMNS and len(first_row) == 4
    except (OSError, StopIteration, csv.Error):
        return False


def download_file(filename: str, force: bool = False) -> None:
    destination = RAW_DIR / filename
    if is_valid_csv(destination) and not force:
        print(f"Already present: {destination.relative_to(ROOT)}")
        return

    # Reuse the April CSV already tracked at the repository root.
    legacy_april = ROOT / filename
    if filename == FILES[0] and is_valid_csv(legacy_april) and not force:
        shutil.copy2(legacy_april, destination)
        print(f"Copied existing April file to {destination.relative_to(ROOT)}")
        return

    url = SOURCE_BASE + filename
    temporary = destination.with_suffix(destination.suffix + ".part")
    print(f"Downloading {filename} ...")
    try:
        with requests.get(url, stream=True, timeout=(30, 180)) as response:
            response.raise_for_status()
            with temporary.open("wb") as output:
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        output.write(chunk)
        if not is_valid_csv(temporary):
            raise ValueError(f"Downloaded file failed CSV header validation: {filename}")
        temporary.replace(destination)
        print(f"Saved {destination.relative_to(ROOT)} ({destination.stat().st_size / (1024**2):.1f} MB)")
    except Exception:
        temporary.unlink(missing_ok=True)
        raise


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--force", action="store_true",
        help="Download every file again, even if a valid local copy exists.",
    )
    args = parser.parse_args()

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    for filename in FILES:
        download_file(filename, force=args.force)

    print("\nAll six monthly files are ready in data/raw/.")


if __name__ == "__main__":
    main()
