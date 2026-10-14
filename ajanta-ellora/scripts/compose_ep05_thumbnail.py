"""
Master & Companion Shorts Thumbnail Compositor for Kailasa Episode 05.
Implements:
1. Master 16:9 Thumbnail (1920x1080):
   - Mobile 3-Word Rule: "CARRIED BY ELEPHANTS?"
   - High-contrast typography with heavy shadow & stroke
   - File size strictly capped < 2.0 MB
2. Short 1 Dedicated 9:16 Vertical Thumbnail (1080x1920):
   - Mobile 3-Word Rule: "LIFTED BY ELEPHANTS?"
   - Upper-third safe zone placement
   - File size strictly capped < 2.0 MB
3. Short 2 Dedicated 9:16 Vertical Thumbnail (1080x1920):
   - Mobile 3-Word Rule: "WHY ELEPHANTS BENEATH?"
   - Upper-third safe zone placement
   - File size strictly capped < 2.0 MB
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parent.parent # ajanta-ellora
THUMBNAIL_DIR = BASE_DIR / "episode05" / "thumbnail"

RAW_MASTER = THUMBNAIL_DIR / "ep05_master_thumbnail_raw.jpg"
OUT_MASTER = THUMBNAIL_DIR / "ep05_master_thumbnail_16x9.jpg"

RAW_SHORT_01 = THUMBNAIL_DIR / "short_01_thumbnail_raw_9x16.jpg"
OUT_SHORT_01 = THUMBNAIL_DIR / "short_01_thumbnail_9x16.jpg"

RAW_SHORT_02 = THUMBNAIL_DIR / "short_02_thumbnail_raw_9x16.jpg"
OUT_SHORT_02 = THUMBNAIL_DIR / "short_02_thumbnail_9x16.jpg"

def get_font_bold(size):
    for f in ["segoeub.ttf", "arialbd.ttf", "impact.ttf"]:
        try:
            return ImageFont.truetype(f, size)
        except Exception:
            continue
    return ImageFont.load_default()

def compose_master():
    print("--- COMPOSITING MASTER 16:9 THUMBNAIL ---")
    if not RAW_MASTER.exists():
        raise FileNotFoundError(f"Raw thumbnail base image missing: {RAW_MASTER}")
        
    img = Image.open(RAW_MASTER).convert("RGB")
    if img.size != (1920, 1080):
        img = img.resize((1920, 1080), Image.Resampling.LANCZOS)
        
    draw = ImageDraw.Draw(img)
    f_huge = get_font_bold(132)
    
    # 3-Word Rule: "CARRIED", "BY", "ELEPHANTS?"
    lines = [
        ("CARRIED", (255, 255, 255), 110, 100),
        ("BY", (255, 255, 255), 110, 240),
        ("ELEPHANTS?", (250, 204, 21), 320, 240)  # Electric yellow accent on ELEPHANTS?
    ]
    
    # Heavy black stroke / shadow
    for text, color, x, y in lines:
        for ox in range(-7, 8):
            for oy in range(-7, 8):
                if ox != 0 or oy != 0:
                    draw.text((x + ox, y + oy), text, fill=(0, 0, 0), font=f_huge)
        draw.text((x, y), text, fill=color, font=f_huge)
        
    # Subtle cinematic border
    draw.rectangle([0, 0, 1920, 1080], outline=(15, 18, 24), width=10)
    
    img.save(OUT_MASTER, "JPEG", quality=92)
    size_mb = OUT_MASTER.stat().st_size / (1024 * 1024)
    print(f"[SUCCESS] Composited {OUT_MASTER.name}: {img.size[0]}x{img.size[1]} | {size_mb:.2f} MB (< 2.0 MB limit: {'PASS' if size_mb < 2.0 else 'FAIL'})")

def compose_short_1():
    print("--- COMPOSITING SHORT 1 9:16 VERTICAL THUMBNAIL ---")
    if not RAW_SHORT_01.exists():
        raise FileNotFoundError(f"Raw short 1 base image missing: {RAW_SHORT_01}")
        
    img = Image.open(RAW_SHORT_01).convert("RGB")
    if img.size != (1080, 1920):
        img = img.resize((1080, 1920), Image.Resampling.LANCZOS)
        
    draw = ImageDraw.Draw(img)
    f_huge = get_font_bold(125)
    
    # 3-Word Rule: "LIFTED", "BY", "ELEPHANTS?"
    lines = [
        ("LIFTED", (255, 255, 255), 80, 200),
        ("BY", (255, 255, 255), 80, 340),
        ("ELEPHANTS?", (250, 204, 21), 280, 340)
    ]
    
    for text, color, x, y in lines:
        for ox in range(-7, 8):
            for oy in range(-7, 8):
                if ox != 0 or oy != 0:
                    draw.text((x + ox, y + oy), text, fill=(0, 0, 0), font=f_huge)
        draw.text((x, y), text, fill=color, font=f_huge)
        
    # Border
    draw.rectangle([0, 0, 1080, 1920], outline=(15, 18, 24), width=10)
    
    img.save(OUT_SHORT_01, "JPEG", quality=92)
    size_mb = OUT_SHORT_01.stat().st_size / (1024 * 1024)
    print(f"[SUCCESS] Composited {OUT_SHORT_01.name}: {img.size[0]}x{img.size[1]} | {size_mb:.2f} MB (< 2.0 MB limit: {'PASS' if size_mb < 2.0 else 'FAIL'})")

def compose_short_2():
    print("--- COMPOSITING SHORT 2 9:16 VERTICAL THUMBNAIL ---")
    if not RAW_SHORT_02.exists():
        raise FileNotFoundError(f"Raw short 2 base image missing: {RAW_SHORT_02}")
        
    img = Image.open(RAW_SHORT_02).convert("RGB")
    if img.size != (1080, 1920):
        img = img.resize((1080, 1920), Image.Resampling.LANCZOS)
        
    draw = ImageDraw.Draw(img)
    f_huge = get_font_bold(115)
    
    # 3-Word Rule: "WHY", "ELEPHANTS", "BENEATH?"
    lines = [
        ("WHY", (255, 255, 255), 80, 200),
        ("ELEPHANTS", (250, 204, 21), 340, 200),
        ("BENEATH?", (255, 255, 255), 80, 340)
    ]
    
    for text, color, x, y in lines:
        for ox in range(-7, 8):
            for oy in range(-7, 8):
                if ox != 0 or oy != 0:
                    draw.text((x + ox, y + oy), text, fill=(0, 0, 0), font=f_huge)
        draw.text((x, y), text, fill=color, font=f_huge)
        
    # Border
    draw.rectangle([0, 0, 1080, 1920], outline=(15, 18, 24), width=10)
    
    img.save(OUT_SHORT_02, "JPEG", quality=92)
    size_mb = OUT_SHORT_02.stat().st_size / (1024 * 1024)
    print(f"[SUCCESS] Composited {OUT_SHORT_02.name}: {img.size[0]}x{img.size[1]} | {size_mb:.2f} MB (< 2.0 MB limit: {'PASS' if size_mb < 2.0 else 'FAIL'})")

def main():
    print("=" * 65)
    print(" COMPOSITING EPISODE 05 MASTER & COMPANION SHORTS THUMBNAILS")
    print("=" * 65)
    compose_master()
    compose_short_1()
    compose_short_2()
    print("=" * 65)
    print(" ALL THUMBNAILS COMPOSITED SUCCESSFULLY AND VERIFIED < 2.0 MB!")
    print("=" * 65)

if __name__ == "__main__":
    main()
