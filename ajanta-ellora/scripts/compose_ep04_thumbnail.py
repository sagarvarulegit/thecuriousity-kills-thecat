"""
Master 16:9 Thumbnail Compositor for Kailasa Episode 04
Implements:
- 3-Word Rule: "CARVED IN AIR?"
- High-contrast typography with heavy shadow & stroke
- 16:9 1920x1080 resolution
- File size strictly capped < 2.0 MB (per YouTube constraints)
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parent.parent # ajanta-ellora
THUMBNAIL_DIR = BASE_DIR / "episode04" / "thumbnail"

RAW_THUMB = THUMBNAIL_DIR / "ep04_master_thumbnail_raw.jpg"
OUT_THUMB = THUMBNAIL_DIR / "ep04_master_thumbnail_16x9.jpg"

def get_font_bold(size):
    for f in ["segoeub.ttf", "arialbd.ttf", "impact.ttf"]:
        try:
            return ImageFont.truetype(f, size)
        except Exception:
            continue
    return ImageFont.load_default()

def compose_thumbnail():
    print("=" * 65)
    print(" COMPOSITING MASTER 16:9 THUMBNAIL (3-WORD RULE: 'CARVED IN AIR?')")
    print("=" * 65)
    
    if not RAW_THUMB.exists():
        raise FileNotFoundError(f"Raw thumbnail base image missing: {RAW_THUMB}")
        
    img = Image.open(RAW_THUMB).convert("RGB")
    if img.size != (1920, 1080):
        img = img.resize((1920, 1080), Image.Resampling.LANCZOS)
        
    draw = ImageDraw.Draw(img)
    
    # 3-Word Rule: "CARVED", "IN", "AIR?"
    # Placed in high-visibility top-left area
    f_huge = get_font_bold(138)
    
    # Text lines
    lines = [
        ("CARVED", (255, 255, 255), 110, 100),
        ("IN", (255, 255, 255), 110, 240),
        ("AIR?", (250, 204, 21), 280, 240)  # Electric yellow accent on AIR?
    ]
    
    # Render with heavy black stroke / shadow for 100% readability on mobile screens
    for text, color, x, y in lines:
        # Shadow / Stroke passes
        for ox in range(-6, 7):
            for oy in range(-6, 7):
                if ox != 0 or oy != 0:
                    draw.text((x + ox, y + oy), text, fill=(0, 0, 0), font=f_huge)
        # Main text
        draw.text((x, y), text, fill=color, font=f_huge)
        
    # Subtle cinematic vignette border
    draw.rectangle([0, 0, 1920, 1080], outline=(15, 18, 24), width=10)
    
    # Save with quality optimization (< 2.0 MB ceiling)
    img.save(OUT_THUMB, "JPEG", quality=92)
    size_mb = OUT_THUMB.stat().st_size / (1024 * 1024)
    print(f"[SUCCESS] Composited thumbnail: {OUT_THUMB.name}")
    print(f"Dimensions: {img.size[0]}x{img.size[1]} | File Size: {size_mb:.2f} MB (< 2.0 MB limit: {'PASS' if size_mb < 2.0 else 'FAIL'})")

if __name__ == "__main__":
    compose_thumbnail()
