"""
compose_ep06_thumbnails.py — Master & Companion Shorts Thumbnail Compositor for Kailasa Episode 06
Implements:
1. Master 16:9 Thumbnail (1920x1080):
   - Mobile 3-Word Rule: "CARVED IN MID-AIR"
   - High-contrast typography with heavy shadow & stroke
   - File size strictly capped < 2.0 MB
2. Short 1 Dedicated 9:16 Vertical Thumbnail (1080x1920):
   - Mobile 3-Word Rule: "SKY BRIDGES"
   - Upper-third safe zone placement
   - File size strictly capped < 2.0 MB
3. Short 2 Dedicated 9:16 Vertical Thumbnail (1080x1920):
   - Mobile 3-Word Rule: "1,000 MEN FAILED"
   - Upper-third safe zone placement
   - File size strictly capped < 2.0 MB
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parent.parent # ajanta-ellora
THUMBNAIL_DIR = BASE_DIR / "episode06" / "thumbnail"

RAW_MASTER = THUMBNAIL_DIR / "ep06_master_thumbnail_raw.jpg"
OUT_MASTER = THUMBNAIL_DIR / "ep06_master_thumbnail_16x9.jpg"

RAW_SHORT_01 = THUMBNAIL_DIR / "short_01_thumbnail_raw_9x16.jpg"
OUT_SHORT_01 = THUMBNAIL_DIR / "short_01_thumbnail_9x16.jpg"

RAW_SHORT_02 = THUMBNAIL_DIR / "short_02_thumbnail_raw_9x16.jpg"
OUT_SHORT_02 = THUMBNAIL_DIR / "short_02_thumbnail_9x16.jpg"

def get_font_bold(size: int):
    for f in ["segoeub.ttf", "arialbd.ttf", "impact.ttf"]:
        try:
            return ImageFont.truetype(f, size)
        except Exception:
            continue
    return ImageFont.load_default()

def draw_stroked_text(draw, pos, text, font, fill_color, stroke_color, stroke_width):
    x, y = pos
    for dx in range(-stroke_width, stroke_width + 1):
        for dy in range(-stroke_width, stroke_width + 1):
            if dx != 0 or dy != 0:
                draw.text((x + dx, y + dy), text, font=font, fill=stroke_color)
    draw.text((x, y), text, font=font, fill=fill_color)

def compose_master():
    print("--- COMPOSITING MASTER 16:9 THUMBNAIL ---")
    if not RAW_MASTER.exists():
        # Fallback to blueprint or image if raw still generating
        print(f"[WARN] Raw master {RAW_MASTER.name} not found yet.")
        return
        
    img = Image.open(RAW_MASTER).convert("RGB")
    if img.size != (1920, 1080):
        img = img.resize((1920, 1080), Image.Resampling.LANCZOS)
        
    draw = ImageDraw.Draw(img)
    f_huge = get_font_bold(135)
    
    # 3-Word Rule: "CARVED", "IN", "MID-AIR"
    lines = [
        ("CARVED", (255, 255, 255), 110, 100),
        ("IN", (255, 255, 255), 110, 245),
        ("MID-AIR", (250, 204, 21), 290, 245)  # Electric yellow accent on MID-AIR
    ]
    
    for text, color, x, y in lines:
        draw_stroked_text(draw, (x, y), text, f_huge, color, stroke_color=(0, 0, 0), stroke_width=8)
        
    OUT_MASTER.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT_MASTER, format="JPEG", quality=90, optimize=True)
    size_mb = OUT_MASTER.stat().st_size / (1024 * 1024)
    print(f"[OK] Master Thumbnail created: {OUT_MASTER.name} ({size_mb:.2f} MB)")
    assert size_mb < 2.0, f"Master thumbnail exceeds 2.0 MB ({size_mb:.2f} MB)"

def compose_short_01():
    print("--- COMPOSITING SHORT 01 9:16 VERTICAL THUMBNAIL ---")
    if not RAW_SHORT_01.exists():
        print(f"[WARN] Raw short 01 {RAW_SHORT_01.name} not found yet.")
        return
        
    img = Image.open(RAW_SHORT_01).convert("RGB")
    if img.size != (1080, 1920):
        img = img.resize((1080, 1920), Image.Resampling.LANCZOS)
        
    draw = ImageDraw.Draw(img)
    f_vert = get_font_bold(118)
    
    # Upper Safe Zone Typography: "SKY", "BRIDGES"
    draw_stroked_text(draw, (80, 220), "SKY", f_vert, fill_color=(255, 255, 255), stroke_color=(0, 0, 0), stroke_width=8)
    draw_stroked_text(draw, (80, 350), "BRIDGES", f_vert, fill_color=(250, 204, 21), stroke_color=(0, 0, 0), stroke_width=8)
    
    OUT_SHORT_01.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT_SHORT_01, format="JPEG", quality=90, optimize=True)
    size_mb = OUT_SHORT_01.stat().st_size / (1024 * 1024)
    print(f"[OK] Short 01 Thumbnail created: {OUT_SHORT_01.name} ({size_mb:.2f} MB)")
    assert size_mb < 2.0, f"Short 01 thumbnail exceeds 2.0 MB ({size_mb:.2f} MB)"

def compose_short_02():
    print("--- COMPOSITING SHORT 02 9:16 VERTICAL THUMBNAIL ---")
    if not RAW_SHORT_02.exists():
        print(f"[WARN] Raw short 02 {RAW_SHORT_02.name} not found yet.")
        return
        
    img = Image.open(RAW_SHORT_02).convert("RGB")
    if img.size != (1080, 1920):
        img = img.resize((1080, 1920), Image.Resampling.LANCZOS)
        
    draw = ImageDraw.Draw(img)
    f_vert = get_font_bold(105)
    
    # Upper Safe Zone Typography: "1,000 MEN", "FAILED"
    draw_stroked_text(draw, (70, 220), "1,000 MEN", f_vert, fill_color=(255, 255, 255), stroke_color=(0, 0, 0), stroke_width=8)
    draw_stroked_text(draw, (70, 345), "FAILED", f_vert, fill_color=(250, 204, 21), stroke_color=(0, 0, 0), stroke_width=8)
    
    OUT_SHORT_02.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT_SHORT_02, format="JPEG", quality=90, optimize=True)
    size_mb = OUT_SHORT_02.stat().st_size / (1024 * 1024)
    print(f"[OK] Short 02 Thumbnail created: {OUT_SHORT_02.name} ({size_mb:.2f} MB)")
    assert size_mb < 2.0, f"Short 02 thumbnail exceeds 2.0 MB ({size_mb:.2f} MB)"

def main():
    print("=" * 65)
    print("  KAILASA EPISODE 06 THUMBNAIL COMPOSITING SUITE")
    print("=" * 65)
    compose_master()
    compose_short_01()
    compose_short_02()
    print("\n[COMPLETE] All Episode 06 Thumbnails composited with Mobile 3-Word Rule!")

if __name__ == "__main__":
    main()
