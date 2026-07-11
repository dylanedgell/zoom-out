"""Build zipcodes.js from GeoNames' public US postal-centroid dataset.

Downloads https://download.geonames.org/export/zip/US.zip (CC BY 4.0),
parses the tab-separated US.txt, and writes a compact
    window.ZIPS = {"72801":[35.28,-93.13], ...}
lookup used by index.html. Run once; re-run to refresh.

Usage: python3 build_zipcodes.py
"""
import io
import json
import os
import urllib.request
import zipfile

URL = "https://download.geonames.org/export/zip/US.zip"
OUT = os.path.join(os.path.dirname(__file__), "zipcodes.js")

# GeoNames postal file columns (tab-separated), 0-indexed:
# 1=postal_code, 9=latitude, 10=longitude
COL_ZIP, COL_LAT, COL_LON = 1, 9, 10


def main() -> None:
    print(f"Downloading {URL} ...")
    raw = urllib.request.urlopen(URL, timeout=60).read()
    zf = zipfile.ZipFile(io.BytesIO(raw))
    text = zf.read("US.txt").decode("utf-8")

    zips: dict[str, list[float]] = {}
    for line in text.splitlines():
        parts = line.split("\t")
        if len(parts) <= COL_LON:
            continue
        code = parts[COL_ZIP].strip()
        # Keep 5-digit US ZIPs only; skip territories' longer/odd codes.
        if len(code) != 5 or not code.isdigit():
            continue
        if code in zips:  # first occurrence wins (stable centroid)
            continue
        try:
            lat = round(float(parts[COL_LAT]), 4)
            lon = round(float(parts[COL_LON]), 4)
        except ValueError:
            continue
        zips[code] = [lat, lon]

    # Compact JSON (no spaces) keeps the file ~1 MB.
    payload = json.dumps(zips, separators=(",", ":"))
    with open(OUT, "w") as f:
        f.write("window.ZIPS=")
        f.write(payload)
        f.write(";\n")
    size_kb = os.path.getsize(OUT) / 1024
    print(f"Wrote {len(zips):,} ZIPs to {OUT} ({size_kb:.0f} KB)")


if __name__ == "__main__":
    main()
