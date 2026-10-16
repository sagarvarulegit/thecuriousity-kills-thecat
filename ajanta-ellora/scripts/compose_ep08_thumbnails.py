#!/usr/bin/env python3
"""
compose_ep08_thumbnails.py — Master & Companion Shorts Thumbnail Compositor for Episode 08.
Series: Ajanta & Ellora: The Subterranean Titans (Act II: The Lost Predecessor)
Channel: thecuriousity-kills-thecat

Features:
1. Master 16:9 Thumbnail (1920x1080):
   - Replaces the corrupted / logo-bearing draft with a clean, high-CTR, 16:9 master asset.
   - Zero trademark logos or watermarks (100% compliant).
   - Obey the Mobile 3-Word Rule ("PAINTED IN DARKNESS").
   - Enhanced contrast & saturation on the lapis lazuli mineral blue.
   - File size strictly capped < 2.0 MB.
2. 3-Way A/B/C Test Packaging (Law 13 Compliant):
   - Variant A (Painted in Darkness - Default Master)
   - Variant B (Impossible Chemistry)
   - Variant C (Forbidden Blue)
3. Short 01 Dedicated 9:16 Vertical Thumbnail (1080x1920):
   - Hook: "MUD CHEMISTRY SECRET" in upper safe zone (y=230-370).
   - Frosted blur background with sharp center framing.
   - File size < 2.0 MB.
4. Short 02 Dedicated 9:16 Vertical Thumbnail (1080x1920):
   - Hook: "PAINTED WITH SUNLIGHT" in upper safe zone (y=230-370).
   - Polished bronze mirror lighting array visual.
   - File size < 2.0 MB.
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

BASE_DIR = Path("C:/Sagar/Projects/thecuriousity-kills-thecat")
EPISODE_DIR = BASE_DIR / "ajanta-ellora" / "episode08"
IMAGES_DIR = EPISODE_DIR / "images"
THUMBNAIL_DIR = EPISODE_DIR / "thumbnail"

def get_font_bold(size: int):
    for f in ["impact.ttf", "arialbd.ttf", "arial.ttf"]:
        try:
            return ImageFont.truetype(f, size)
        except Exception:
            continue
    return ImageFont.load_default()

def draw_stroked_text(draw, pos, text, font, fill_color, stroke_color=(0, 0, 0), stroke_width=8):
    x, y = pos
    for dx in range(-stroke_width, stroke_width + 1):
        for dy in range(-stroke_width, stroke_width + 1):
            if dx != 0 or dy != 0:
                draw.text((x + dx, y + dy), text, font=font, fill=stroke_color)
    draw.text((x, y), text, font=font, fill=fill_color)

def compose_16x9_master(bg_path: Path, lines: list, out_path: Path):
    target_w, target_h = 1920, 1080
    raw = Image.open(bg_path).convert("RGB")
    w, h = raw.size
    
    # Scale to cover 1920x1080
    scale = max(target_w / w, target_h / h)
    new_w, new_h = int(w * scale), int(h * scale)
    resized = raw.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    # Center crop
    left = (new_w - target_w) // 2
    top = (new_h - target_h) // 2
    canvas = resized.crop((left, top, left + target_w, top + target_h))
    
    # Boost contrast and saturation slightly for cinematic documentary grade
    canvas = ImageEnhance.Contrast(canvas).enhance(1.15)
    canvas = ImageEnhance.Color(canvas).enhance(1.18)
    
    # Left-side dark raking vignette to maximize typography contrast
    vignette = Image.new("L", (target_w, target_h), 0)
    draw_v = ImageDraw.Draw(vignette)
    for x in range(950):
        alpha = int(150 * (1.0 - (x / 950.0)))
        draw_v.line([(x, 0), (x, target_h)], fill=alpha)
    black_left = Image.new("RGB", (target_w, target_h), (5, 6, 12))
    canvas = Image.composite(black_left, canvas, vignette)
    
    # Draw typography
    draw = ImageDraw.Draw(canvas)
    f_huge = get_font_bold(135)
    
    y_start = 120
    for text, color, x_offset in lines:
        draw_stroked_text(draw, (x_offset, y_start), text, f_huge, color, stroke_color=(0, 0, 0), stroke_width=10)
        y_start += 150
        
    out_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out_path, format="JPEG", quality=92, optimize=True)
    size_mb = out_path.stat().st_size / (1024 * 1024)
    print(f"  [OK] Master Thumbnail Saved: {out_path.name} | {size_mb:.2f} MB | {canvas.size}")
    assert size_mb < 2.0, f"Exceeded 2.0 MB limit! ({size_mb:.2f} MB)"

def compose_9x16_vertical(bg_path: Path, lines: list, out_path: Path):
    target_w, target_h = 1080, 1920
    raw = Image.open(bg_path).convert("RGB")
    
    # Create blurred background to fill 1080x1920
    bg_scale = max(target_w / raw.width, target_h / raw.height)
    bg_w, bg_h = int(raw.width * bg_scale), int(raw.height * bg_scale)
    bg_resized = raw.resize((bg_w, bg_h), Image.Resampling.LANCZOS)
    bg_left = (bg_w - target_w) // 2
    bg_top = (bg_h - target_h) // 2
    bg_cropped = bg_resized.crop((bg_left, bg_top, bg_left + target_w, bg_top + target_h))
    bg_blurred = bg_cropped.filter(ImageFilter.GaussianBlur(radius=32))
    bg_dimmed = ImageEnhance.Brightness(bg_blurred).enhance(0.55)
    
    # Foreground sharp image (center-framed)
    fg_w = target_w
    fg_h = int(raw.height * (target_w / raw.width))
    fg_resized = raw.resize((fg_w, fg_h), Image.Resampling.LANCZOS)
    
    fg_y = (target_h - fg_h) // 2
    canvas = bg_dimmed.copy()
    canvas.paste(fg_resized, (0, fg_y))
    
    # Upper-third vignette for typography readability
    top_vignette = Image.new("L", (target_w, target_h), 0)
    draw_v = ImageDraw.Draw(top_vignette)
    for y in range(650):
        alpha = int(180 * (1.0 - (y / 650.0)))
        draw_v.line([(0, y), (target_w, y)], fill=alpha)
    black_top = Image.new("RGB", (target_w, target_h), (5, 6, 12))
    canvas = Image.composite(black_top, canvas, top_vignette)
    
    # Typography in upper safe zone (y=230-370)
    draw = ImageDraw.Draw(canvas)
    f_vert = get_font_bold(115)
    
    y_pos = 230
    for text, color in lines:
        draw_stroked_text(draw, (80, y_pos), text, f_vert, color, stroke_color=(0, 0, 0), stroke_width=9)
        y_pos += 140
        
    out_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out_path, format="JPEG", quality=90, optimize=True)
    size_mb = out_path.stat().st_size / (1024 * 1024)
    print(f"  [OK] Vertical Short Thumbnail Saved: {out_path.name} | {size_mb:.2f} MB | {canvas.size}")
    assert size_mb < 2.0, f"Exceeded 2.0 MB limit! ({size_mb:.2f} MB)"

def main():
    print("=" * 65)
    print("  COMPOSING EPISODE 08 CLEAN PRODUCTION THUMBNAILS")
    print("  (Zero Trademarks, Law 5, 6, 13 & 20 Compliant)")
    print("=" * 65)
    
    # 1. Primary Master 16:9 Thumbnail
    master_bg = IMAGES_DIR / "ep08_gf_19_painting_blue_lotus_padmapani_GENERATE_VIDEO.jpg"
    primary_master = THUMBNAIL_DIR / "ep08_thumbnail_16x9_the_secret_chemistry.jpg"
    compose_16x9_master(
        master_bg,
        [("PAINTED IN", (255, 255, 255), 90), ("DARKNESS", (250, 204, 21), 90)],
        primary_master
    )
    
    # 2. Variant A (Scale Contrast / Painted in Darkness)
    var_a = THUMBNAIL_DIR / "thumbnail_variant_a_scale_contrast.jpg"
    compose_16x9_master(
        master_bg,
        [("PAINTED IN", (255, 255, 255), 90), ("DARKNESS", (250, 204, 21), 90)],
        var_a
    )
    
    # 3. Variant B (Impossible Chemistry)
    var_b_bg = IMAGES_DIR / "ep08_gf_17_artisan_spreading_lime_plaster_finish_GENERATE_VIDEO.jpg"
    var_b = THUMBNAIL_DIR / "thumbnail_variant_b_impossible_chemistry.jpg"
    compose_16x9_master(
        var_b_bg,
        [("IMPOSSIBLE", (255, 255, 255), 90), ("CHEMISTRY", (250, 204, 21), 90)],
        var_b
    )
    
    # 4. Variant C (Curiosity Gap / Forbidden Blue)
    var_c_bg = IMAGES_DIR / "ep08_archive_06_padmapani_3d_shading_face_macro_PAN_ZOOM.jpg"
    var_c = THUMBNAIL_DIR / "thumbnail_variant_c_curiosity_gap.jpg"
    compose_16x9_master(
        var_c_bg,
        [("FORBIDDEN", (255, 255, 255), 90), ("BLUE", (56, 189, 248), 90)],
        var_c
    )
    
    # 5. Short 01 Vertical Thumbnail (9:16, 1080x1920)
    short_01_bg = IMAGES_DIR / "ep08_gf_04_plaster_kneading_cowdung_matrix_GENERATE_VIDEO.jpg"
    short_01_out = THUMBNAIL_DIR / "short_01_thumbnail_9x16.jpg"
    compose_9x16_vertical(
        short_01_bg,
        [("MUD CHEMISTRY", (255, 255, 255)), ("SECRET", (250, 204, 21))],
        short_01_out
    )
    
    # 6. Short 02 Vertical Thumbnail (9:16, 1080x1920)
    short_02_bg = IMAGES_DIR / "ep08_gf_07_bronze_mirror_sunlight_beam_GENERATE_VIDEO.jpg"
    short_02_out = THUMBNAIL_DIR / "short_02_thumbnail_9x16.jpg"
    compose_9x16_vertical(
        short_02_bg,
        [("PAINTED WITH", (255, 255, 255)), ("SUNLIGHT", (250, 204, 21))],
        short_02_out
    )
    
    print("\n" + "=" * 65)
    print("  [SUCCESS] All Episode 08 Thumbnails Successfully Generated!")
    print("=" * 65)

if __name__ == "__main__":
    main()
