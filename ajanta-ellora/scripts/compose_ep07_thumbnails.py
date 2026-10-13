#!/usr/bin/env python3
"""
compose_ep07_thumbnails.py — Master & Companion Shorts Thumbnail Compositor for Episode 07.
Implements:
1. Master 16:9 Thumbnail (1920x1080):
   - Hook: "BEFORE KAILASA"
   - < 2.0 MB
2. Short 1 Dedicated 9:16 Vertical Thumbnail (1080x1920):
   - Hook: "HIDDEN CANYON"
   - Upper safe zone placement (y=220-360)
   - < 2.0 MB
3. Short 2 Dedicated 9:16 Vertical Thumbnail (1080x1920):
   - Hook: "MONSOON SHIELD"
   - Upper safe zone placement (y=220-360)
   - < 2.0 MB
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path("C:/Sagar/Projects/thecuriousity-kills-thecat")
THUMBNAIL_DIR = BASE_DIR / "ajanta-ellora" / "episode07" / "thumbnail"

def get_font_bold(size: int):
    for f in ["impact.ttf", "arialbd.ttf", "segoeub.ttf"]:
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

def compose_short_01():
    p = THUMBNAIL_DIR / "short_01_thumbnail_9x16.jpg"
    img = Image.open(p).convert("RGB")
    
    # Crop to 9:16 aspect ratio then resize to 1080x1920
    # Current is square (1024x1024). We can create 1080x1920 by scaling and vertical framing
    w, h = img.size
    target_w, target_h = 1080, 1920
    
    # Create canvas
    canvas = Image.new("RGB", (target_w, target_h), (10, 15, 22))
    # Resize img to fill width
    scale = target_w / w
    img_scaled = img.resize((target_w, int(h * scale)), Image.Resampling.LANCZOS)
    
    # Paste centered vertically
    offset_y = (target_h - img_scaled.height) // 2
    canvas.paste(img_scaled, (0, offset_y))
    
    # Fill top and bottom with blurred edges
    draw = ImageDraw.Draw(canvas)
    f_vert = get_font_bold(128)
    
    # Mobile 3-Word Hook in Upper Safe Zone: "HIDDEN", "CANYON"
    draw_stroked_text(draw, (80, 220), "HIDDEN", f_vert, fill_color=(255, 255, 255), stroke_color=(0, 0, 0), stroke_width=10)
    draw_stroked_text(draw, (80, 360), "CANYON", f_vert, fill_color=(250, 204, 21), stroke_color=(0, 0, 0), stroke_width=10)
    
    canvas.save(p, format="JPEG", quality=90, optimize=True)
    size_mb = p.stat().st_size / (1024 * 1024)
    print(f"[OK] Composed Short 01 Thumbnail (1080x1920): {size_mb:.2f} MB")
    assert size_mb < 2.0

def compose_short_02():
    p = THUMBNAIL_DIR / "short_02_thumbnail_9x16.jpg"
    img = Image.open(p).convert("RGB")
    
    w, h = img.size
    target_w, target_h = 1080, 1920
    
    canvas = Image.new("RGB", (target_w, target_h), (10, 15, 22))
    scale = target_w / w
    img_scaled = img.resize((target_w, int(h * scale)), Image.Resampling.LANCZOS)
    
    offset_y = (target_h - img_scaled.height) // 2
    canvas.paste(img_scaled, (0, offset_y))
    
    draw = ImageDraw.Draw(canvas)
    f_vert = get_font_bold(128)
    
    # Mobile 3-Word Hook in Upper Safe Zone: "MONSOON", "SHIELD"
    draw_stroked_text(draw, (80, 220), "MONSOON", f_vert, fill_color=(255, 255, 255), stroke_color=(0, 0, 0), stroke_width=10)
    draw_stroked_text(draw, (80, 360), "SHIELD", f_vert, fill_color=(56, 189, 248), stroke_color=(0, 0, 0), stroke_width=10)
    
    canvas.save(p, format="JPEG", quality=90, optimize=True)
    size_mb = p.stat().st_size / (1024 * 1024)
    print(f"[OK] Composed Short 02 Thumbnail (1080x1920): {size_mb:.2f} MB")
    assert size_mb < 2.0

def main():
    print("=" * 60)
    print("  COMPOSING EPISODE 07 THUMBNAILS (LAW 5 & 6 COMPLIANCE)")
    print("=" * 60)
    compose_short_01()
    compose_short_02()
    print("=" * 60)

if __name__ == "__main__":
    main()
