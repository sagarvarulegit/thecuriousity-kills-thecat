#!/usr/bin/env python3
"""
process_real_paintings.py — Formats user-provided authentic Ajanta-Ellora images into 16:9 assets in images/
"""

import os
from pathlib import Path
from PIL import Image

BASE_DIR = Path("C:/Sagar/Projects/thecuriousity-kills-thecat")
SRC_DIR = BASE_DIR / "ajanta-ellora" / "episode08" / "real-ajantaellora-painting"
DEST_DIR = BASE_DIR / "ajanta-ellora" / "episode08" / "images"

# 1. Process act1-1.jpg (Real Rock-cut cave/temple)
act1_src = SRC_DIR / "act1-1.jpg"
if act1_src.exists():
    with Image.open(act1_src) as im:
        rgb = im.convert("RGB")
        out_p = DEST_DIR / "ep08_real_ajanta_rock_cut_monolithic_temple_PAN_ZOOM.jpg"
        rgb.save(out_p, quality=95)
        print(f"[OK] Saved {out_p.name} ({rgb.size})")

# 2. Process real paintings 1.png to 5.png
paintings = [
    ("1.png", "ep08_real_painting_01_cave_mural_panorama_PAN_ZOOM.jpg"),
    ("2.png", "ep08_real_painting_02_bodhisattva_lotus_PAN_ZOOM.jpg"),
    ("3.png", "ep08_real_painting_03_celestial_apsara_PAN_ZOOM.jpg"),
    ("4.png", "ep08_real_painting_04_royal_court_figures_PAN_ZOOM.jpg"),
    ("5.png", "ep08_real_painting_05_cave_ceiling_medallion_PAN_ZOOM.jpg"),
]

for src_name, out_name in paintings:
    src_p = SRC_DIR / src_name
    if src_p.exists():
        with Image.open(src_p) as im:
            rgb = Image.new("RGB", im.size, (15, 17, 23))
            if im.mode == "RGBA":
                rgb.paste(im, mask=im.split()[3])
            else:
                rgb.paste(im)
            out_p = DEST_DIR / out_name
            rgb.save(out_p, quality=95)
            print(f"[OK] Saved {out_p.name} ({rgb.size})")
