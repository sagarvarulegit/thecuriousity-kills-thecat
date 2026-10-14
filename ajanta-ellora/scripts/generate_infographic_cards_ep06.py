#!/usr/bin/env python3
"""
generate_infographic_cards_ep06.py — PIL Technical Infographic & Blueprint Generator (Episode 06)
Generates 6 broadcast-grade 1920x1080 2D architectural blueprint cards for Episode 06:
1. ep06_infographic_01_sky_bridge_structural_elevation.jpg
2. ep06_infographic_02_kokasa_top_down_timeline.jpg
3. ep06_infographic_03_bridge_underbelly_excavation_mechanics.jpg
4. ep06_infographic_04_dhwajasthambha_quarry_isolation.jpg
5. ep06_infographic_05_white_chuna_plaster_stratigraphy.jpg
6. ep06_infographic_06_aurangzeb_demolition_structural_comparison.jpg
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

WORKSPACE_ROOT = Path("C:/Sagar/Projects/thecuriousity-kills-thecat")
IMAGES_DIR = WORKSPACE_ROOT / "ajanta-ellora" / "episode06" / "images"
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

WIDTH, HEIGHT = 1920, 1080

def get_font(size: int):
    for f in ["arial.ttf", "segoeui.ttf", "tahoma.ttf"]:
        try:
            return ImageFont.truetype(f, size)
        except Exception:
            continue
    return ImageFont.load_default()

def get_font_bold(size: int):
    for f in ["arialbd.ttf", "segoeuib.ttf", "impact.ttf"]:
        try:
            return ImageFont.truetype(f, size)
        except Exception:
            continue
    return ImageFont.load_default()

def create_base_canvas(subhead: str = "THE SKY BRIDGES OF KAILASA"):
    img = Image.new("RGB", (WIDTH, HEIGHT), color=(12, 16, 22))
    draw = ImageDraw.Draw(img)
    
    # Outer cinematic border
    draw.rectangle([40, 40, WIDTH-40, HEIGHT-40], outline=(55, 70, 90), width=2)
    draw.rectangle([48, 48, WIDTH-48, HEIGHT-48], outline=(28, 38, 50), width=1)
    
    # Header branding
    f_sub = get_font(19)
    draw.text((70, 65), "KAILASA TEMPLE ARCHITECTURAL & LITHIC DOSSIER // ELLORA CAVE 16", fill=(120, 155, 190), font=f_sub)
    draw.text((WIDTH - 580, 65), f"SERIES EPISODE 06: {subhead}", fill=(195, 150, 75), font=f_sub)
    draw.line([(70, 95), (WIDTH - 70, 95)], fill=(45, 60, 75), width=1)
    
    # Blueprint grid
    for x in range(100, WIDTH - 100, 150):
        draw.line([(x, 110), (x, HEIGHT - 80)], fill=(18, 24, 32), width=1)
    for y in range(120, HEIGHT - 80, 120):
        draw.line([(70, y), (WIDTH - 70, y)], fill=(18, 24, 32), width=1)
        
    return img, draw

def make_card_01_sky_bridge_structural_elevation():
    img, draw = create_base_canvas(subhead="MONOLITHIC SKY BRIDGE ELEVATION")
    f_title = get_font_bold(38)
    f_h2 = get_font_bold(22)
    f_body = get_font(18)
    f_num = get_font_bold(36)
    
    draw.text((70, 125), "MONOLITHIC SKY BRIDGE STRUCTURAL ELEVATION", fill=(240, 245, 255), font=f_title)
    draw.text((70, 175), "AERIAL SUSPENSION CROSS-SECTION: GOPURAM TO NANDI MANDAPA (DEPTH -15m)", fill=(195, 150, 75), font=f_h2)
    
    cx, cy = 960, 500
    
    # Ground Courtyard line (-33m)
    draw.line([(200, cy + 300), (1720, cy + 300)], fill=(140, 160, 180), width=3)
    draw.text((220, cy + 315), "COURTYARD FLOOR BEDROCK LEVEL (-33.0m DATUM)", fill=(120, 140, 160), font=f_body)
    
    # Left Pillar/Gopuram structure
    draw.rectangle([250, cy - 200, 500, cy + 300], fill=(24, 32, 44), outline=(70, 140, 220), width=2)
    draw.text((270, cy - 170), "ENTRANCE GOPURAM", fill=(210, 230, 255), font=f_h2)
    draw.text((270, cy - 130), "Western Gatehouse Mass", fill=(150, 175, 200), font=f_body)
    draw.text((270, cy + 20), "Monolithic Anchor Wall", fill=(120, 150, 180), font=f_body)
    
    # Right Structure: Nandi Mandapa (Two Story)
    draw.rectangle([1100, cy - 200, 1450, cy + 300], fill=(24, 32, 44), outline=(70, 140, 220), width=2)
    draw.text((1120, cy - 170), "NANDI MANDAPA (UPPER LEVEL)", fill=(210, 230, 255), font=f_h2)
    draw.text((1120, cy - 130), "Pavilion Anchor & Pier", fill=(150, 175, 200), font=f_body)
    draw.text((1120, cy + 120), "Lower Pavilion Storey", fill=(120, 150, 180), font=f_body)
    
    # Central Suspended Aerial Bridge Span
    # Bridge Walkway thickness: 2.2m
    draw.rectangle([500, cy - 120, 1100, cy - 40], fill=(45, 65, 95), outline=(240, 200, 80), width=3)
    draw.text((620, cy - 105), "MONOLITHIC AERIAL BRIDGE SPAN (6.5m LENGTH)", fill=(255, 220, 110), font=f_h2)
    draw.text((630, cy - 75), "Zero Mortar // Zero Separate Arches // Zero Keystones", fill=(200, 225, 255), font=f_body)
    
    # 30-Foot Void Beneath Span
    draw.rectangle([500, cy - 40, 1100, cy + 300], fill=(16, 22, 30, 120), outline=(200, 75, 75), width=2)
    draw.text((650, cy + 80), "EXCAVATED VOID // 30-FOOT AIR GAP", fill=(255, 110, 110), font=f_h2)
    draw.text((610, cy + 120), "Rock mass cleared beneath hanging span", fill=(180, 160, 160), font=f_body)
    draw.text((590, cy + 150), "Tensile strength of Deccan Basalt: 120-140 MPa", fill=(180, 210, 240), font=f_body)
    
    # Tension callout arrows
    draw.line([(500, cy - 160), (1100, cy - 160)], fill=(240, 180, 60), width=2)
    draw.polygon([(500, cy - 160), (515, cy - 166), (515, cy - 154)], fill=(240, 180, 60))
    draw.polygon([(1100, cy - 160), (1085, cy - 166), (1085, cy - 154)], fill=(240, 180, 60))
    draw.text((710, cy - 195), "SPAN: ~6.5 METERS", fill=(240, 180, 60), font=f_body)
    
    # Height callout arrow
    draw.line([(1500, cy - 40), (1500, cy + 300)], fill=(80, 200, 160), width=2)
    draw.polygon([(1500, cy - 40), (1494, cy - 25), (1506, cy - 25)], fill=(80, 200, 160))
    draw.polygon([(1500, cy + 300), (1494, cy + 285), (1506, cy + 285)], fill=(80, 200, 160))
    draw.text((1520, cy + 120), "VOID CLEARANCE:\n9.1 METERS (30 FT)", fill=(80, 200, 160), font=f_body)
    
    # Footer metrics box
    draw.rectangle([70, HEIGHT - 130, WIDTH - 70, HEIGHT - 65], fill=(20, 28, 40), outline=(50, 75, 105), width=1)
    draw.text((100, HEIGHT - 110), "STRUCTURAL FACTOR:", fill=(140, 170, 200), font=f_body)
    draw.text((320, HEIGHT - 115), "HOMOGENEOUS VOLCANIC MONOLITH", fill=(240, 220, 100), font=f_h2)
    draw.text((780, HEIGHT - 110), "SHEAR FAILURE RISK:", fill=(140, 170, 200), font=f_body)
    draw.text((1000, HEIGHT - 115), "COOLING JOINTS (REQUIRING ZERO THERMAL FRACTURE)", fill=(255, 130, 130), font=f_h2)
    
    out_p = IMAGES_DIR / "ep06_infographic_01_sky_bridge_structural_elevation.jpg"
    img.save(out_p, quality=95)
    print(f"[OK] Generated: {out_p.name}")

def make_card_02_kokasa_top_down_timeline():
    img, draw = create_base_canvas(subhead="THE 7-DAY SHIKHARA SEQUENCING")
    f_title = get_font_bold(38)
    f_h2 = get_font_bold(22)
    f_body = get_font(18)
    
    draw.text((70, 125), "KOKASA'S TOP-DOWN EXCAVATION PROTOCOL", fill=(240, 245, 255), font=f_title)
    draw.text((70, 175), "THE 7-DAY SHIKHARA REVELATION VS CONVENTIONAL MASONRY CONSTRUCTION", fill=(195, 150, 75), font=f_h2)
    
    # 3 Phase panels
    stages = [
        {
            "num": "PHASE 1 (DAYS 1-7)",
            "title": "SUMMIT SHIKHARA REVELATION",
            "desc": "Kokasa traces geometry on summit.\nPinnacle finial (Kalasha) & spire\nsculpted first out of mountain peak.\nQueen's vow fulfilled while mountain\nbeneath remains untouched solid rock.",
            "color": (240, 200, 80),
            "depth": "0.0m to -6.0m Datum"
        },
        {
            "num": "PHASE 2 (YEARS 1-8)",
            "title": "AERIAL BRIDGES & ROOF VAULTS",
            "desc": "Quarrymen cut three vertical trenches.\nCeilings, upper mandapa pillars, and\nhanging sky bridges sculpted.\nUnderbelly void hollowed with picks\nwhile courtyard floor is still bedrock.",
            "color": (80, 180, 240),
            "depth": "-6.0m to -20.0m Depth"
        },
        {
            "num": "PHASE 3 (YEARS 8-25)",
            "title": "COURTYARD FLOOR & MONOLITHS",
            "desc": "Trench floor cleared to -33m base.\nTwin 17m Dhwajasthambhas & elephants\nisolated as free-standing monoliths.\nMonumental 8m elephant plinth\ncompleted without ground scaffolding.",
            "color": (90, 220, 160),
            "depth": "-20.0m to -33.0m Depth"
        }
    ]
    
    col_w = 540
    gap = 40
    start_x = 90
    y_top = 240
    y_bot = 880
    
    for i, s in enumerate(stages):
        x = start_x + i * (col_w + gap)
        draw.rectangle([x, y_top, x + col_w, y_bot], fill=(20, 26, 36), outline=s["color"], width=2)
        draw.rectangle([x, y_top, x + col_w, y_top + 60], fill=(28, 38, 52))
        draw.text((x + 20, y_top + 18), s["num"], fill=s["color"], font=f_h2)
        
        draw.text((x + 20, y_top + 80), s["title"], fill=(240, 245, 255), font=f_h2)
        draw.line([(x + 20, y_top + 120), (x + col_w - 20, y_top + 120)], fill=(45, 60, 80), width=1)
        
        # Draw descriptive text
        lines = s["desc"].split("\n")
        cur_y = y_top + 140
        for l in lines:
            draw.text((x + 20, cur_y), l, fill=(180, 205, 230), font=f_body)
            cur_y += 36
            
        # Depth box at bottom
        draw.rectangle([x + 20, y_bot - 80, x + col_w - 20, y_bot - 20], fill=(14, 20, 28), outline=(60, 80, 105), width=1)
        draw.text((x + 35, y_bot - 65), f"STRATIGRAPHY: {s['depth']}", fill=s["color"], font=f_body)
        
    # Bottom comparison summary
    draw.rectangle([70, HEIGHT - 130, WIDTH - 70, HEIGHT - 65], fill=(20, 28, 40), outline=(50, 75, 105), width=1)
    draw.text((100, HEIGHT - 110), "KEY STRUCTURAL ADVANTAGE:", fill=(140, 170, 200), font=f_body)
    draw.text((380, HEIGHT - 115), "ZERO CENTERING FALSEWORK // SOLID ROCK ACTS AS NATURAL SCAFFOLDING", fill=(240, 220, 100), font=f_h2)
    
    out_p = IMAGES_DIR / "ep06_infographic_02_kokasa_top_down_timeline.jpg"
    img.save(out_p, quality=95)
    print(f"[OK] Generated: {out_p.name}")

def make_card_03_bridge_underbelly_excavation():
    img, draw = create_base_canvas(subhead="CARVING THE VOID // UNDERBELLY LOGISTICS")
    f_title = get_font_bold(38)
    f_h2 = get_font_bold(22)
    f_body = get_font(18)
    
    draw.text((70, 125), "UNDERBELLY EXCAVATION & ACOUSTIC SOUNDING", fill=(240, 245, 255), font=f_title)
    draw.text((70, 175), "HOW QUARRYMEN CLEARED 30 FEET OF VOID BENEATH THE HANGING BRIDGE", fill=(195, 150, 75), font=f_h2)
    
    # Split Diagram: Left Mechanics, Right Acoustic Diagnostic
    cx = 960
    
    # Left: Mechanical harness & pick technique
    draw.rectangle([80, 230, 920, 880], fill=(20, 27, 38), outline=(60, 90, 130), width=2)
    draw.text((110, 255), "1. TENSION-HARNESS SUSPENSION RIG", fill=(240, 210, 90), font=f_h2)
    draw.line([(110, 290), (890, 290)], fill=(45, 60, 80), width=1)
    
    harness_points = [
        "• Hemp Rope Harnesses: Braided hemp ropes anchored to upper",
        "  parapets of the gopuram and Nandi terrace.",
        "• Inverse Percussion: Stonecutters worked upside down and sideways,",
        "  chipping basalt away from ceiling toward floor void.",
        "• Prohibition of Fire-Setting: Thermal shock creates micro-fissures;",
        "  bridge underbelly strictly cleared by pointed cold chisels.",
        "• Wedge-Driven Slicing: Horizontal slot-holes drilled to cleave",
        "  sub-blocks away without inducing upward shockwaves."
    ]
    cur_y = 310
    for p in harness_points:
        draw.text((110, cur_y), p, fill=(190, 215, 240), font=f_body)
        cur_y += 34
        
    # Technical box left
    draw.rectangle([110, 680, 890, 850], fill=(14, 20, 28), outline=(70, 140, 210), width=1)
    draw.text((130, 705), "TOOLING ARSENAL (UNDERBELLY VOID):", fill=(70, 180, 245), font=f_h2)
    draw.text((130, 745), "• Carbonized-iron punches (1.5 kg)", fill=(180, 200, 220), font=f_body)
    draw.text((130, 775), "• Basalt handheld impact pestles for stone dressing", fill=(180, 200, 220), font=f_body)
    draw.text((130, 805), "• Steel-tipped slot wedges driven by bronze mallets", fill=(180, 200, 220), font=f_body)
    
    # Right: Acoustic Resonance Testing
    draw.rectangle([980, 230, 1840, 880], fill=(20, 27, 38), outline=(60, 90, 130), width=2)
    draw.text((1010, 255), "2. ACOUSTIC INTEGRITY DIAGNOSTIC", fill=(90, 220, 160), font=f_h2)
    draw.line([(1010, 290), (1810, 290)], fill=(45, 60, 80), width=1)
    
    acoustic_points = [
        "Ancient masons used sonic feedback to gauge stone thickness:",
        "",
        "A. HIGH-PITCH CLEAR RING (Solid Bedrock > 2.0m):",
        "   Indicates homogeneous, high-density tholeiitic basalt.",
        "   Compressive load safe for aerial bridge arch.",
        "",
        "B. DULL, HOLLOW THUD (Thin Basalt < 0.8m or Fissure):",
        "   Warned carvers to cease deep chipping immediately.",
        "   Indicated proximity to a hidden cooling joint or pocket.",
        "",
        "C. WATER SEEPAGE QUENCH TEST:",
        "   Cold water poured on joints under angled oil-lamp light.",
        "   Capillary action reveals micro-fractures before load release."
    ]
    cur_y = 310
    for p in acoustic_points:
        col = (255, 120, 120) if "DULL" in p else ((240, 220, 100) if "HIGH-PITCH" in p else (190, 215, 240))
        draw.text((1010, cur_y), p, fill=col, font=f_body)
        cur_y += 34
        
    out_p = IMAGES_DIR / "ep06_infographic_03_bridge_underbelly_excavation_mechanics.jpg"
    img.save(out_p, quality=95)
    print(f"[OK] Generated: {out_p.name}")

def make_card_04_dhwajasthambha_isolation():
    img, draw = create_base_canvas(subhead="THE 17-METER VICTORY PILLARS")
    f_title = get_font_bold(38)
    f_h2 = get_font_bold(22)
    f_body = get_font(18)
    
    draw.text((70, 125), "MONOLITHIC VICTORY PILLARS (DHWAJASTHAMBHAS)", fill=(240, 245, 255), font=f_title)
    draw.text((70, 175), "ISOLATING 17-METER FREESTANDING OBELISKS FROM VERTICAL BEDROCK", fill=(195, 150, 75), font=f_h2)
    
    cx, cy = 960, 520
    
    # Left Pillar Graphic
    px = 350
    draw.line([(150, cy + 280), (1770, cy + 280)], fill=(120, 150, 180), width=3)
    draw.text((160, cy + 295), "COURTYARD BASE LEVEL (-33.0m)", fill=(120, 140, 160), font=f_body)
    
    # Pillar Shape
    # Pedestal
    draw.rectangle([px - 70, cy + 180, px + 70, cy + 280], fill=(30, 42, 60), outline=(240, 200, 90), width=2)
    draw.text((px - 60, cy + 225), "PLINTH BASE", fill=(240, 200, 90), font=f_body)
    # Shaft (Fluted)
    draw.rectangle([px - 45, cy - 220, px + 45, cy + 180], fill=(22, 32, 48), outline=(70, 150, 230), width=2)
    draw.text((px - 35, cy - 20), "FLUTED\nSHAFT\n17m", fill=(210, 230, 255), font=f_h2)
    # Capital (Trident finial)
    draw.rectangle([px - 60, cy - 260, px + 60, cy - 220], fill=(45, 65, 95), outline=(240, 200, 90), width=2)
    draw.polygon([(px, cy - 290), (px - 35, cy - 260), (px + 35, cy - 260)], fill=(240, 200, 90))
    
    # Callout lines on Pillar
    draw.line([(px + 100, cy - 290), (px + 100, cy + 280)], fill=(80, 220, 160), width=2)
    draw.polygon([(px + 100, cy - 290), (px + 94, cy - 275), (px + 106, cy - 275)], fill=(80, 220, 160))
    draw.polygon([(px + 100, cy + 280), (px + 94, cy + 265), (px + 106, cy + 265)], fill=(80, 220, 160))
    draw.text((px + 120, cy - 10), "HEIGHT: 17 METERS\n(OVER 55 FEET)\nSOLID BASALT", fill=(80, 220, 160), font=f_h2)
    
    # Right Information Panels
    rx = 850
    draw.rectangle([rx, 230, 1840, 840], fill=(20, 27, 38), outline=(60, 90, 130), width=2)
    draw.text((rx + 30, 260), "THE NEGATIVE-SPACE ISOLATION CHALLENGE", fill=(240, 210, 90), font=f_h2)
    draw.line([(rx + 30, 295), (1810, 295)], fill=(45, 60, 80), width=1)
    
    points = [
        "1. No Additive Erection:",
        "   Unlike Roman columns or Ashokan pillars, these were never quarried",
        "   elsewhere, transported on rollers, or hoisted upright with timber cranes.",
        "",
        "2. The Island Strategy:",
        "   As the 100-foot chasm descended, builders marked a 4-meter square cylinder.",
        "   Tens of thousands of tons of basalt were removed around this cylinder,",
        "   leaving a vertical island standing isolated in the open courtyard.",
        "",
        "3. Zero-Tolerance Fluting:",
        "   Sculptors carved the complex sixteen-sided fluted shaft, floral garlands,",
        "   and crowning trishula finial while standing on stepped rock rings that",
        "   were progressively chipped away downward.",
        "",
        "4. Twin Alignment:",
        "   The northern and southern pillars match within millimeters of geometric symmetry",
        "   relative to the central axis of the Nandi pavilion."
    ]
    cur_y = 315
    for p in points:
        col = (240, 200, 90) if p.startswith(("1.", "2.", "3.", "4.")) else (190, 215, 240)
        draw.text((rx + 30, cur_y), p, fill=col, font=f_body)
        cur_y += 32
        
    out_p = IMAGES_DIR / "ep06_infographic_04_dhwajasthambha_quarry_isolation.jpg"
    img.save(out_p, quality=95)
    print(f"[OK] Generated: {out_p.name}")

def make_card_05_white_chuna_plaster():
    img, draw = create_base_canvas(subhead="THE WHITE HIMALAYAN ILLUSION")
    f_title = get_font_bold(38)
    f_h2 = get_font_bold(22)
    f_body = get_font(18)
    
    draw.text((70, 125), "THE WHITE SHELL-LIME PLASTER (CHUNA) FORMULA", fill=(240, 245, 255), font=f_title)
    draw.text((70, 175), "HOW RASHTRAKUTA ARTISANS TURNED VOLCANIC BASALT INTO A SNOW-WHITE MOUNTAIN", fill=(195, 150, 75), font=f_h2)
    
    # Chemical & Material Layers Diagram
    layers = [
        {
            "title": "LAYER 3: HIGH-GLOSS INTONACO SLIP (0.5 – 1.0 mm)",
            "comp": "Micro-calcined river shells + powdered white marble dust + gum arabic",
            "func": "Agate-stone burnished to porcelain finish. Reflected 85% of solar radiation.",
            "color": (255, 255, 255),
            "bg": (45, 55, 75)
        },
        {
            "title": "LAYER 2: CEMENTING COAT (2.0 – 5.0 mm)",
            "comp": "Slaked lime (calcium hydroxide) + crushed quartz sand + jaggery/methi extracts",
            "func": "Organic saccharide fermentation slowed drying, preventing shrinkage micro-cracks.",
            "color": (230, 230, 210),
            "bg": (35, 45, 60)
        },
        {
            "title": "LAYER 1: MECHANICAL KEYING (BEDROCK SURFACE)",
            "comp": "Tholeiitic Volcanic Basalt pitted with angled carbon-steel pick punches",
            "func": "10,000 tiny chisel pits per square meter to anchor the mineral plaster matrix.",
            "color": (160, 180, 200),
            "bg": (22, 30, 42)
        }
    ]
    
    y = 240
    for l in layers:
        draw.rectangle([100, y, 1820, y + 140], fill=l["bg"], outline=l["color"], width=2)
        draw.text((130, y + 20), l["title"], fill=l["color"], font=f_h2)
        draw.text((130, y + 60), f"Composition: {l['comp']}", fill=(200, 220, 245), font=f_body)
        draw.text((130, y + 95), f"Function:    {l['func']}", fill=(180, 200, 220), font=f_body)
        y += 170
        
    # The Visual Result Box
    draw.rectangle([100, y + 10, 1820, HEIGHT - 110], fill=(16, 22, 32), outline=(240, 200, 90), width=2)
    draw.text((130, y + 30), "THE HISTORICAL REVELATION (8TH – 13TH CENTURIES CE):", fill=(240, 200, 90), font=f_h2)
    draw.text((130, y + 70), "• Under the fierce Deccan sun, the entire temple did not appear as dark volcanic stone.", fill=(220, 235, 255), font=f_body)
    draw.text((130, y + 105), "• It glowed like an iceberg—a breathtaking earthly replica of snow-clad Mount Kailash in Tibet.", fill=(220, 235, 255), font=f_body)
    draw.text((130, y + 140), "• Centuries of heavy monsoon rains washed away the soft lime, revealing the basalt skeleton we see today.", fill=(180, 205, 230), font=f_body)
    
    out_p = IMAGES_DIR / "ep06_infographic_05_white_chuna_plaster_stratigraphy.jpg"
    img.save(out_p, quality=95)
    print(f"[OK] Generated: {out_p.name}")

def make_card_06_aurangzeb_demolition_comparison():
    img, draw = create_base_canvas(subhead="THE INDESTRUCTIBLE MONOLITH // 1682 SIEGE")
    f_title = get_font_bold(38)
    f_h2 = get_font_bold(22)
    f_body = get_font(18)
    
    draw.text((70, 125), "STRUCTURAL RESILIENCE: MONOLITH VS MASONRY", fill=(240, 245, 255), font=f_title)
    draw.text((70, 175), "WHY 1,000 WORKERS OVER ONE FULL YEAR FAILED TO DEMOLISH CAVE 16", fill=(195, 150, 75), font=f_h2)
    
    # Side-by-side comparison
    mid = 960
    
    # Left: Conventional Masonry Building
    draw.rectangle([80, 230, mid - 20, 870], fill=(24, 20, 24), outline=(220, 90, 90), width=2)
    draw.text((110, 260), "CONVENTIONAL CONSTRUCTED TEMPLE", fill=(255, 110, 110), font=f_h2)
    draw.text((110, 300), "Assembled Stone Blocks & Mortar Joints", fill=(200, 170, 170), font=f_body)
    draw.line([(110, 335), (mid - 50, 335)], fill=(60, 40, 40), width=1)
    
    c_points = [
        "• Assembled Parts: Thousands of individual stone blocks",
        "  held together by mortar, gravity, and dowels.",
        "• Critical Failure Points: Destroying 2 or 3 load-bearing",
        "  pillars collapses the architraves and brings down the roof.",
        "• Joint Vulnerability: Iron crowbars easily pry blocks apart",
        "  along weak mortar lines.",
        "• Demolition Timeline: A 1,000-man army can demolish a 30m",
        "  masonry temple within 3 to 6 weeks."
    ]
    cur_y = 360
    for p in c_points:
        draw.text((110, cur_y), p, fill=(230, 200, 200), font=f_body)
        cur_y += 44
        
    # Right: Kailasa Monolith
    draw.rectangle([mid + 20, 230, WIDTH - 80, 870], fill=(18, 28, 38), outline=(80, 200, 140), width=2)
    draw.text((mid + 50, 260), "KAILASA MONOLITHIC TEMPLE (CAVE 16)", fill=(90, 230, 160), font=f_h2)
    draw.text((mid + 50, 300), "Subtractive Rock-Cut Continental Basalt", fill=(170, 210, 200), font=f_body)
    draw.line([(mid + 50, 335), (WIDTH - 110, 335)], fill=(40, 60, 60), width=1)
    
    k_points = [
        "• Unified Mountain Core: Zero joints, zero mortar seams,",
        "  and zero freestanding modular blocks.",
        "• Infinite Bedrock Redundancy: Breaking a pillar does not",
        "  collapse the ceiling; the ceiling is rooted in the mountain.",
        "• High Compressive Basalt: 120–150 MPa hardness blunted and",
        "  shattered steel chisels and iron sledgehammers.",
        "• Demolition Failure (1682): After a full year of continuous attack,",
        "  workers only chipped surface reliefs. The structure remained."
    ]
    cur_y = 360
    for p in k_points:
        draw.text((mid + 50, cur_y), p, fill=(200, 240, 220), font=f_body)
        cur_y += 44
        
    out_p = IMAGES_DIR / "ep06_infographic_06_aurangzeb_demolition_structural_comparison.jpg"
    img.save(out_p, quality=95)
    print(f"[OK] Generated: {out_p.name}")

def main():
    print("=" * 65)
    print("  GENERATING EPISODE 06 2D BLUEPRINT INFOGRAPHIC CARDS")
    print("=" * 65)
    make_card_01_sky_bridge_structural_elevation()
    make_card_02_kokasa_top_down_timeline()
    make_card_03_bridge_underbelly_excavation()
    make_card_04_dhwajasthambha_isolation()
    make_card_05_white_chuna_plaster()
    make_card_06_aurangzeb_demolition_comparison()
    print("\n[SUCCESS] All 6 Technical Infographic Cards rendered to episode06/images/!")

if __name__ == "__main__":
    main()
