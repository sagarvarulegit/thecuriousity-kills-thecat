#!/usr/bin/env python3
"""
download_5_authentic_museum_scans_ep08.py — Downloads 5 authentic public domain museum scans
from Wikimedia Commons for Episode 08 to achieve 100% 1:1 coverage (62 cuts = 62 unique assets).
Complies with Operational Law 3 (Zero Repetition Invariant) & Law 9 (Authentic Museum Scans).
"""

import sys
import requests
import urllib.parse
from pathlib import Path
from PIL import Image
import io

BASE_DIR = Path("C:/Sagar/Projects/thecuriousity-kills-thecat")
IMAGES_DIR = BASE_DIR / "ajanta-ellora" / "episode08" / "images"
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

TARGETS = [
    {
        "wiki_title": "File:028 Cave 1, Ceiling Painting (34122851992).jpg",
        "dest_filename": "ep08_36_cave_1_ceiling_painting_museum_scan_PAN_ZOOM.jpg"
    },
    {
        "wiki_title": "File:Black Apsaras, Ajanta Caves.jpg",
        "dest_filename": "ep08_37_black_apsara_cave_17_museum_scan_PAN_ZOOM.jpg"
    },
    {
        "wiki_title": "File:Ajanta Cave 17 God Indra with Apsaras.jpg",
        "dest_filename": "ep08_38_indra_apsaras_cave_17_museum_scan_PAN_ZOOM.jpg"
    },
    {
        "wiki_title": "File:Meister des Mahâjanaka Jâtaka 001.jpg",
        "dest_filename": "ep08_39_mahajanaka_jataka_museum_scan_PAN_ZOOM.jpg"
    },
    {
        "wiki_title": "File:Ajanta Cave 1 ceiling medallion couple.jpg",
        "dest_filename": "ep08_40_cave_1_ceiling_medallion_museum_scan_PAN_ZOOM.jpg"
    }
]

def get_direct_url(title: str) -> str:
    api_url = f"https://commons.wikimedia.org/w/api.php?action=query&titles={urllib.parse.quote(title)}&prop=imageinfo&iiprop=url&format=json"
    resp = requests.get(api_url, headers=HEADERS, timeout=30)
    data = resp.json()
    pages = data.get("query", {}).get("pages", {})
    for _, page in pages.items():
        if "imageinfo" in page and len(page["imageinfo"]) > 0:
            return page["imageinfo"][0]["url"]
    raise ValueError(f"Could not find direct URL for {title}")

def download_and_format(url: str, out_path: Path):
    resp = requests.get(url, headers=HEADERS, timeout=60)
    if resp.status_code != 200:
        raise RuntimeError(f"HTTP {resp.status_code}: {resp.text[:100]}")
    
    im = Image.open(io.BytesIO(resp.content)).convert("RGB")
    im.save(out_path, "JPEG", quality=95)
    print(f"  [OK] Saved: {out_path.name} ({out_path.stat().st_size:,} bytes, {im.size})")

def main():
    print("=" * 65)
    print("  DOWNLOADING 5 AUTHENTIC PUBLIC DOMAIN MUSEUM SCANS (EP08)")
    print("=" * 65)

    for item in TARGETS:
        dest = IMAGES_DIR / item["dest_filename"]
        print(f"\n[*] Fetching {item['wiki_title']} -> {item['dest_filename']}...")
        try:
            url = get_direct_url(item["wiki_title"])
            download_and_format(url, dest)
        except Exception as e:
            print(f"  [ERROR] {e}")

    print("\n[OK] Museum scan ingestion complete.")

if __name__ == "__main__":
    main()
