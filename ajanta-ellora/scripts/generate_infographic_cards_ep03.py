"""
Generate high-retention documentary technical infographic and blueprint cards
for Kailasa Episode 3 using PIL.
These cards provide visual variety, breaking up still paintings like Vox/Lemmino,
and ensuring zero repetitive visuals in the documentary.
All cards are saved directly to ajanta-ellora/episode03/images/
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parent.parent # ajanta-ellora
IMAGES_DIR = BASE_DIR / "episode03" / "images"
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

WIDTH, HEIGHT = 1920, 1080

def get_font(size):
    try:
        return ImageFont.truetype("arial.ttf", size)
    except Exception:
        return ImageFont.load_default()

def get_font_bold(size):
    try:
        return ImageFont.truetype("arialbd.ttf", size)
    except Exception:
        return ImageFont.load_default()

def create_base_canvas(subhead="THE FIRST CUT // TOP-DOWN SPIRE SCULPTING"):
    img = Image.new("RGB", (WIDTH, HEIGHT), color=(12, 16, 22))
    draw = ImageDraw.Draw(img)
    
    # Outer cinematic border
    draw.rectangle([40, 40, WIDTH-40, HEIGHT-40], outline=(55, 70, 90), width=2)
    draw.rectangle([48, 48, WIDTH-48, HEIGHT-48], outline=(28, 38, 50), width=1)
    
    # Header branding
    f_sub = get_font(19)
    draw.text((70, 65), "KAILASA TEMPLE ARCHAEOLOGICAL & ENGINEERING DOSSIER // ELLORA CAVE 16", fill=(120, 155, 190), font=f_sub)
    draw.text((WIDTH - 460, 65), f"SERIES EPISODE 03: {subhead}", fill=(195, 150, 75), font=f_sub)
    draw.line([(70, 95), (WIDTH - 70, 95)], fill=(45, 60, 75), width=1)
    
    # Blueprint grid
    for x in range(100, WIDTH - 100, 150):
        draw.line([(x, 110), (x, HEIGHT - 80)], fill=(18, 24, 32), width=1)
    for y in range(120, HEIGHT - 80, 120):
        draw.line([(70, y), (WIDTH - 70, y)], fill=(18, 24, 32), width=1)
        
    return img, draw

def make_card_01_monolith_dimensions():
    img, draw = create_base_canvas(subhead="THE RAW MONOLITH ISLAND")
    f_title = get_font_bold(42)
    f_h2 = get_font_bold(26)
    f_body = get_font(21)
    f_num = get_font_bold(50)
    
    draw.text((70, 125), "THE MONOLITHIC ISLAND IN THE ABYSS", fill=(240, 245, 255), font=f_title)
    draw.text((70, 180), "POST-EXCAVATION CORE GEOMETRY PRIOR TO SPIRE HEWING (8TH CENTURY CE)", fill=(195, 150, 75), font=f_h2)
    
    # Diagram: 3D Isometric-style wireframe of isolated block
    cx, cy = 960, 520
    # Deep trench abyss
    draw.rectangle([cx - 440, cy - 200, cx + 440, cy + 260], outline=(180, 110, 45), width=2, fill=(16, 20, 28))
    # Monolith core
    draw.rectangle([cx - 280, cy - 140, cx + 280, cy + 180], outline=(75, 165, 245), width=4, fill=(24, 32, 44))
    
    draw.text((cx - 160, cy - 20), "CENTRAL MONOLITHIC ISLAND", fill=(255, 255, 255), font=f_h2)
    draw.text((cx - 150, cy + 20), "(RAW BASALT // UNCARVED CORE)", fill=(130, 175, 220), font=f_body)
    
    # Caliper arrows
    draw.text((cx - 220, cy - 175), "<─────── ~50 METERS LENGTH ───────>", fill=(240, 200, 90), font=f_body)
    draw.text((cx + 295, cy + 10), "~33 METERS\nWIDTH", fill=(240, 200, 90), font=f_body)
    draw.text((cx - 430, cy + 20), "UP TO 33m\nREAR SCARP DROP", fill=(220, 130, 50), font=f_body)
    
    # Metric Boxes
    draw.rectangle([70, 840, 480, 970], fill=(20, 26, 36), outline=(60, 80, 110))
    draw.text((95, 855), "~50 METERS", fill=(75, 165, 245), font=f_num)
    draw.text((95, 920), "Monolith Core Length (~164 Ft)", fill=(180, 195, 215), font=f_body)
    
    draw.rectangle([540, 840, 950, 970], fill=(20, 26, 36), outline=(60, 80, 110))
    draw.text((565, 855), "~33 METERS", fill=(240, 200, 90), font=f_num)
    draw.text((565, 920), "Monolith Width & Deepest Scarp", fill=(180, 195, 215), font=f_body)
    
    draw.rectangle([1010, 840, 1420, 970], fill=(20, 26, 36), outline=(60, 80, 110))
    draw.text((1035, 855), "~100 FEET", fill=(230, 100, 60), font=f_num)
    draw.text((1035, 920), "Total Monolithic Spire Height", fill=(180, 195, 215), font=f_body)
    
    draw.rectangle([1480, 840, 1850, 970], fill=(20, 26, 36), outline=(60, 80, 110))
    draw.text((1505, 855), "SUBTRACTIVE", fill=(140, 220, 140), font=f_num)
    draw.text((1505, 920), "Bedrock Acts As Scaffolding", fill=(180, 195, 215), font=f_body)
    
    out = IMAGES_DIR / "ep03_infographic_01_monolith_island_dimensions.jpg"
    img.save(out, quality=95)
    print(f"Generated: {out.name}")

def make_card_02_bottom_up_vs_top_down():
    img, draw = create_base_canvas(subhead="THE INVERTED PARADIGM")
    f_title = get_font_bold(42)
    f_h2 = get_font_bold(26)
    f_body = get_font(21)
    
    draw.text((70, 125), "ADDITIVE MASONRY VS SUBTRACTIVE EXCAVATION", fill=(240, 245, 255), font=f_title)
    draw.text((70, 180), "COMPARATIVE STRUCTURAL PHYSICS OF CONVENTIONAL VS ROCK-CUT TEMPLE ARCHITECTURE", fill=(195, 150, 75), font=f_h2)
    
    # Left Box: Additive Masonry (Traditional)
    draw.rectangle([100, 240, 920, 780], fill=(18, 24, 34), outline=(75, 120, 170), width=2)
    draw.text((130, 270), "CONVENTIONAL ADDITIVE MASONRY (GROUND-UP)", fill=(85, 175, 250), font=f_h2)
    draw.line([(130, 310), (890, 310)], fill=(45, 60, 80), width=1)
    
    points_left = [
        ("Foundation Precedes Structure", "Earth is excavated first; foundation footings are leveled on solid ground before any wall rises."),
        ("External Timber Scaffolding", "Scaffolding rises from the ground upward. Requires massive timber forests for high spires."),
        ("Modular Error Correction", "If a carved ashlar block cracks or has a flaw, it is discarded and replaced before mortaring."),
        ("Hoisting Capstones via Winches", "The heavy crowning finial (Kalasha) is hauled to the apex using timber cranes and ropes.")
    ]
    y_pos = 330
    for title, desc in points_left:
        draw.text((130, y_pos), f"- {title}:", fill=(240, 200, 90), font=f_h2)
        y_pos += 32
        words = desc.split()
        lines = []
        cur = ""
        for w in words:
            if len(cur + " " + w) < 38:
                cur += (" " if cur else "") + w
            else:
                lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        for l in lines:
            draw.text((150, y_pos), l, fill=(210, 220, 235), font=f_body)
            y_pos += 26
        y_pos += 10
        
    # Right Box: Subtractive Architecture (Kailasa)
    draw.rectangle([980, 240, 1800, 780], fill=(24, 18, 18), outline=(220, 90, 60), width=2)
    draw.text((1010, 270), "KAILASA SUBTRACTIVE EXCAVATION (TOP-DOWN)", fill=(245, 100, 75), font=f_h2)
    draw.line([(1010, 310), (1770, 310)], fill=(80, 45, 45), width=1)
    
    points_right = [
        ("Finial Precedes Courtyard", "The crowning stupi is carved before the courtyard floor even exists beneath the rock."),
        ("The Mountain IS the Scaffolding", "Artisans stand directly on the solid bedrock they are carving, descending layer by layer."),
        ("Absolute Zero Error Margin", "Every chisel stroke is irreversible. A single cracked load-bearing beam cannot be replaced."),
        ("Finial Anchored to Earth", "The crowning finial was never hoisted; it is permanently part of the original volcanic crust.")
    ]
    y_pos = 330
    for title, desc in points_right:
        draw.text((1010, y_pos), f"- {title}:", fill=(245, 160, 90), font=f_h2)
        y_pos += 32
        words = desc.split()
        lines = []
        cur = ""
        for w in words:
            if len(cur + " " + w) < 38:
                cur += (" " if cur else "") + w
            else:
                lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        for l in lines:
            draw.text((1030, y_pos), l, fill=(235, 215, 210), font=f_body)
            y_pos += 26
        y_pos += 10

    # Bottom Banner
    draw.rectangle([90, 830, 1830, 960], fill=(22, 28, 38), outline=(75, 165, 245), width=2)
    draw.text((120, 855), "CORE ENGINEERING PRINCIPLE:", fill=(75, 165, 245), font=f_h2)
    draw.text((120, 895), "In subtractive carving, architecture is not an assembly of parts—it is the revelation of a mathematical void inside living stone.", fill=(220, 230, 245), font=f_body)
    
    out = IMAGES_DIR / "ep03_infographic_02_bottom_up_vs_top_down.jpg"
    img.save(out, quality=95)
    print(f"Generated: {out.name}")

def make_card_03_zero_error_margin():
    img, draw = create_base_canvas(subhead="GEOTECHNICAL HAZARD MATRIX")
    f_title = get_font_bold(42)
    f_h2 = get_font_bold(26)
    f_body = get_font(21)
    
    draw.text((70, 125), "THE PHYSICS OF ZERO MARGIN FOR ERROR", fill=(240, 245, 255), font=f_title)
    draw.text((70, 180), "CATASTROPHIC FAILURE MODES IN SUBTRACTIVE BASALT EXCAVATION", fill=(195, 150, 75), font=f_h2)
    
    # 3 Hazard Cards
    hazards = [
        {
            "num": "HAZARD 01",
            "title": "BLIND COLUMN OVERCUT",
            "desc": "If a mason removes excess stone from an internal pillar core, compressive load exceeds tensile strength of volcanic basalt (~140 MPa), triggering progressive structural shear.",
            "impact": "IRREVERSIBLE COLLAPSE OF OVERHEAD ROOF",
            "col": (230, 90, 70)
        },
        {
            "num": "HAZARD 02",
            "title": "THERMAL FISSURE PROPAGATION",
            "desc": "Misapplied fire-setting or uneven water quenching can propagate microscopic hairline fault fractures across ceiling strata, destabilizing multi-ton suspended spans.",
            "impact": "CATASTROPHIC CEILING DELAMINATION",
            "col": (240, 150, 50)
        },
        {
            "num": "HAZARD 03",
            "title": "AXIAL SKEW / GNOMON DRIFT",
            "desc": "A 0.5-degree orientation deviation at the summit vimana translates to a multi-meter structural misalignment at the courtyard floor 30 meters below.",
            "impact": "TOTAL GEOMETRIC FAILURE OF TEMPLE COMPLEX",
            "col": (240, 200, 70)
        }
    ]
    
    for i, h in enumerate(hazards):
        x = 90 + i * 590
        draw.rectangle([x, 240, x + 550, 780], fill=(20, 26, 36), outline=h["col"], width=2)
        draw.text((x + 25, 270), h["num"], fill=h["col"], font=f_h2)
        draw.text((x + 25, 310), h["title"], fill=(245, 245, 255), font=f_h2)
        draw.line([(x + 25, 350), (x + 525, 350)], fill=(50, 65, 85), width=1)
        
        draw.text((x + 25, 380), "FAILURE MECHANISM:", fill=(140, 165, 195), font=f_body)
        words = h["desc"].split()
        lines = []
        cur = ""
        for w in words:
            if len(cur + " " + w) < 32:
                cur += (" " if cur else "") + w
            else:
                lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
            
        y_txt = 415
        for l in lines:
            draw.text((x + 25, y_txt), l, fill=(205, 215, 230), font=f_body)
            y_txt += 32
            
        draw.rectangle([x + 20, 680, x + 530, 750], fill=(30, 22, 22), outline=h["col"])
        draw.text((x + 35, 695), "CONSEQUENCE:", fill=h["col"], font=f_body)
        draw.text((x + 35, 720), h["impact"], fill=(255, 255, 255), font=get_font_bold(18))

    # Bottom Stat
    draw.rectangle([90, 830, 1830, 960], fill=(22, 28, 38), outline=(75, 165, 245), width=2)
    draw.text((120, 855), "SHILPA SHASTRA MANDATE (MANASARA CH. 11):", fill=(75, 165, 245), font=f_h2)
    draw.text((120, 895), "A rock-cut sanctuary that suffers fracture during hewing brings ruin to the patron, blindness to the architect, and drought to the kingdom.", fill=(220, 230, 245), font=f_body)

    out = IMAGES_DIR / "ep03_infographic_03_zero_error_margin.jpg"
    img.save(out, quality=95)
    print(f"Generated: {out.name}")

def make_card_04_shanku_cardinal_alignment():
    img, draw = create_base_canvas(subhead="THE ASTRONOMICAL SURVEY")
    f_title = get_font_bold(42)
    f_h2 = get_font_bold(26)
    f_body = get_font(21)
    f_num = get_font_bold(36)
    
    draw.text((70, 125), "THE SHANKU SOLAR GNOMON & CARDINAL AXIS", fill=(240, 245, 255), font=f_title)
    draw.text((70, 180), "SOLAR SHADOW BISECTION METHOD // LOCKING THE TEMPLE TO TRUE EAST (8TH CENTURY CE)", fill=(195, 150, 75), font=f_h2)
    
    # Visual Diagram of Shanku shadow circle
    cx, cy = 600, 520
    r = 220
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(60, 90, 130), width=2)
    # Center gnomon pin
    draw.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=(245, 180, 60), outline=(255, 255, 255))
    draw.text((cx - 45, cy + 20), "SHANKU (PIN)", fill=(245, 180, 60), font=f_body)
    
    # Shadow arc line
    draw.line([(cx - 190, cy - 110), (cx + 190, cy - 110)], fill=(220, 100, 50), width=3)
    draw.ellipse([cx - 195, cy - 115, cx - 185, cy - 105], fill=(240, 90, 50))
    draw.text((cx - 240, cy - 145), "MORNING SHADOW (A)", fill=(240, 90, 50), font=f_body)
    
    draw.ellipse([cx + 185, cy - 115, cx + 195, cy - 105], fill=(240, 90, 50))
    draw.text((cx + 110, cy - 145), "EVENING SHADOW (B)", fill=(240, 90, 50), font=f_body)
    
    # East-West Axis
    draw.line([(cx - 260, cy), (cx + 260, cy)], fill=(75, 175, 250), width=3)
    draw.text((cx + 275, cy - 12), "TRUE WEST", fill=(75, 175, 250), font=f_num)
    draw.text((cx - 380, cy - 12), "TRUE EAST", fill=(75, 175, 250), font=f_num)
    
    # North-South Meridian
    draw.line([(cx, cy - 260), (cx, cy + 260)], fill=(120, 160, 200), width=2)
    draw.text((cx - 50, cy - 290), "TRUE NORTH", fill=(180, 200, 220), font=f_body)
    draw.text((cx - 50, cy + 270), "TRUE SOUTH", fill=(180, 200, 220), font=f_body)
    
    # Right-Hand Explanation Box
    draw.rectangle([1060, 240, 1830, 780], fill=(20, 26, 36), outline=(60, 80, 110), width=2)
    draw.text((1090, 270), "MATHEMATICAL STEPS OF THE SUTRADHARA", fill=(245, 175, 65), font=f_h2)
    draw.line([(1090, 310), (1800, 310)], fill=(45, 60, 80), width=1)
    
    steps = [
        "1. Erect a vertical wooden gnomon (Shanku) at sunrise on the virgin summit peak.",
        "2. Scribe a circle around the gnomon using a compass cord of length 2x gnomon height.",
        "3. Mark Point A where morning shadow enters the circle, and Point B where evening shadow exits.",
        "4. Draw intersecting circles from Points A and B to create the 'Fish-Head' (Timi) fish-shape.",
        "5. The line connecting the intersection points establishes TRUE ASTRONOMICAL EAST-WEST.",
        "6. Snapping vermilion chalk cords creates the 64-Square Vastu-Purusha Mandala across the peak."
    ]
    y_pos = 335
    for s in steps:
        words = s.split()
        lines = []
        cur = ""
        for w in words:
            if len(cur + " " + w) < 42:
                cur += (" " if cur else "") + w
            else:
                lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        for l in lines:
            draw.text((1090, y_pos), l, fill=(215, 225, 240), font=f_body)
            y_pos += 29
        y_pos += 8

    # Bottom Metric
    draw.rectangle([90, 830, 1830, 960], fill=(22, 28, 38), outline=(75, 165, 245), width=2)
    draw.text((120, 855), "ASTRONOMICAL ALIGNMENT ACCURACY (ELLORA CAVE 16):", fill=(75, 165, 245), font=f_h2)
    draw.text((120, 895), "Modern surveys verify that the primary east-west axis of Kailasa aligns closely with true solar cardinal orientation across the Charanandri ridge.", fill=(220, 230, 245), font=f_body)

    out = IMAGES_DIR / "ep03_infographic_04_shanku_cardinal_alignment.jpg"
    img.save(out, quality=95)
    print(f"Generated: {out.name}")

def make_card_05_dravidian_vimana_tiers():
    img, draw = create_base_canvas(subhead="THE 4 TIERS OF THE VIMANA")
    f_title = get_font_bold(42)
    f_h2 = get_font_bold(26)
    f_body = get_font(21)
    
    draw.text((70, 125), "ANATOMY OF THE 30-METER MONOLITHIC VIMANA", fill=(240, 245, 255), font=f_title)
    draw.text((70, 180), "DESCENDING STRATIGRAPHY OF THE DRAVIDIAN SHIKHARA CARVED FROM THE PEAK", fill=(195, 150, 75), font=f_h2)
    
    # Left Visual Stepped Pyramid Diagram
    cx = 500
    tiers = [
        {"y": 250, "w": 140, "h": 60, "name": "TIER 0: STUPI / KALASHA", "tag": "Monolithic Finial Vase", "col": (245, 190, 70)},
        {"y": 320, "w": 240, "h": 70, "name": "TIER 1: GRIVA (OCTAGONAL NECK)", "tag": "4 Flanking Monolithic Nandi Bulls", "col": (230, 140, 60)},
        {"y": 400, "w": 380, "h": 90, "name": "TIER 2: UPPER HARANTARA", "tag": "Miniature Kuta & Sala Aedicules", "col": (85, 175, 250)},
        {"y": 500, "w": 540, "h": 110, "name": "TIER 3: MIDDLE STOREY", "tag": "Niche Reliefs of Shiva Manifestations", "col": (130, 195, 140)},
        {"y": 620, "w": 720, "h": 140, "name": "TIER 4: GARBHAGRIHA ROOF SLAB", "tag": "Massive Suspended Solid Ceiling", "col": (190, 150, 220)}
    ]
    
    for t in tiers:
        draw.rectangle([cx - t["w"]//2, t["y"], cx + t["w"]//2, t["y"] + t["h"]], fill=(20, 26, 36), outline=t["col"], width=3)
        draw.text((cx - len(t["name"])*6, t["y"] + 15), t["name"], fill=t["col"], font=f_body)
    
    # Right-Hand Details Table
    draw.rectangle([940, 240, 1830, 780], fill=(20, 26, 36), outline=(60, 80, 110), width=2)
    draw.text((970, 265), "HEWING SEQUENCE & STRUCTURAL INTEGRATION", fill=(245, 175, 65), font=f_h2)
    draw.line([(970, 305), (1800, 305)], fill=(45, 60, 80), width=1)
    
    tier_descs = [
        ("1. The Stupi / Kalasha Finial", "Carved directly out of the apex stone block. Unlike built masonry where capstones are hoisted with winches, this finial was never lifted; it remains bedrock-anchored."),
        ("2. The Octagonal Griva & Nandi Bulls", "The neck of the spire features eight polished facets crowned by four resting bulls carved in relief at cardinal corners, guarding the sacred vimana."),
        ("3. The Stepped Harantara Storeys", "Carved with rhythmic sequences of Kuta (square pavilion shrines) and Sala (barrel-vaulted oblong shrines) connected by covered cloister walls."),
        ("4. The Garbhagriha Hollow Core", "Masons entered horizontally beneath the finished vimana to hollow the womb chamber, checking ceiling thickness with acoustic mallets.")
    ]
    
    y_pos = 325
    for title, desc in tier_descs:
        draw.text((970, y_pos), title, fill=(240, 200, 90), font=f_h2)
        y_pos += 34
        words = desc.split()
        lines = []
        cur = ""
        for w in words:
            if len(cur + " " + w) < 46:
                cur += (" " if cur else "") + w
            else:
                lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        for l in lines:
            draw.text((970, y_pos), l, fill=(210, 220, 235), font=f_body)
            y_pos += 27
        y_pos += 12

    # Bottom Metric
    draw.rectangle([90, 830, 1830, 960], fill=(22, 28, 38), outline=(75, 165, 245), width=2)
    draw.text((120, 855), "STRUCTURAL DIMENSIONS // DRAVIDIAN VIMANA (CAVE 16):", fill=(75, 165, 245), font=f_h2)
    draw.text((120, 895), "Total Height: ~30.0 meters (~98 feet) // Monolithic sanctuary carved entirely out of solid Deccan trap basalt without mortar or joints.", fill=(220, 230, 245), font=f_body)

    out = IMAGES_DIR / "ep03_infographic_05_dravidian_vimana_tiers.jpg"
    img.save(out, quality=95)
    print(f"Generated: {out.name}")

def make_card_06_acoustic_sounding():
    img, draw = create_base_canvas(subhead="NON-DESTRUCTIVE GEOTECHNICAL TESTING")
    f_title = get_font_bold(42)
    f_h2 = get_font_bold(26)
    f_body = get_font(21)
    f_num = get_font_bold(38)
    
    draw.text((70, 125), "ACOUSTIC RESONANCE SOUNDING & CEILING THICKNESS", fill=(240, 245, 255), font=f_title)
    draw.text((70, 180), "NON-DESTRUCTIVE MALLET SOUNDING USED TO PREVENT SANCTUM CEILING FAILURE", fill=(195, 150, 75), font=f_h2)
    
    # Left Comparison: Hollow Ring vs Solid Thud
    draw.rectangle([100, 240, 920, 780], fill=(18, 24, 34), outline=(240, 90, 60), width=2)
    draw.text((130, 270), "HIGH HOLLOW RING // CEILING DANGER ZONE", fill=(240, 90, 60), font=f_h2)
    draw.line([(130, 310), (890, 310)], fill=(60, 35, 35), width=1)
    
    pts_danger = [
        ("Acoustic Frequency", "Higher acoustic pitch (>500 Hz) reverberating through the basalt."),
        ("Physical Meaning", "Ceiling thickness has dropped below 0.5 meters (thin diaphragm)."),
        ("Structural Risk", "Extreme risk of overhead shear fracture under the weight of the vimana."),
        ("Mason Command", "'STHAGAYA' (HALT) — Immediately cease upward chisel strikes!")
    ]
    y_pos = 330
    for title, desc in pts_danger:
        draw.text((130, y_pos), f"- {title}:", fill=(240, 150, 80), font=f_h2)
        y_pos += 32
        words = desc.split()
        lines = []
        cur = ""
        for w in words:
            if len(cur + " " + w) < 38:
                cur += (" " if cur else "") + w
            else:
                lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        for l in lines:
            draw.text((150, y_pos), l, fill=(210, 220, 235), font=f_body)
            y_pos += 26
        y_pos += 10

    # Right Comparison: Solid Deep Thud
    draw.rectangle([980, 240, 1800, 780], fill=(18, 28, 24), outline=(75, 195, 130), width=2)
    draw.text((1010, 270), "LOW SOLID THUD // STRUCTURAL CONTINUITY", fill=(75, 195, 130), font=f_h2)
    draw.line([(1010, 310), (1770, 310)], fill=(35, 60, 45), width=1)
    
    pts_safe = [
        ("Acoustic Frequency", "Low damped thud (<150 Hz) dissipating rapidly into mountain bedrock."),
        ("Physical Meaning", "Adequate basalt thickness (>1.0 meter) supporting overhead strata."),
        ("Structural Safety", "Tensile and compressive stress safely distributed across uncarved mass."),
        ("Mason Command", "'KHARATAYA' (PROCEED) — Carefully continue leveling ceiling plane.")
    ]
    y_pos = 330
    for title, desc in pts_safe:
        draw.text((1010, y_pos), f"- {title}:", fill=(140, 220, 140), font=f_h2)
        y_pos += 32
        words = desc.split()
        lines = []
        cur = ""
        for w in words:
            if len(cur + " " + w) < 38:
                cur += (" " if cur else "") + w
            else:
                lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        for l in lines:
            draw.text((1030, y_pos), l, fill=(215, 235, 220), font=f_body)
            y_pos += 26
        y_pos += 10

    # Bottom Stat
    draw.rectangle([90, 830, 1830, 960], fill=(22, 28, 38), outline=(75, 165, 245), width=2)
    draw.text((120, 855), "GEOTECHNICAL PRINCIPLE OF SUBTERRANEAN SOUNDING:", fill=(75, 165, 245), font=f_h2)
    draw.text((120, 895), "Without ultrasound or laser scanning, ancient Indian sculptors used the acoustic velocity of sound in basalt (~5,000 m/s) to gauge rock thickness by ear.", fill=(220, 230, 245), font=f_body)

    out = IMAGES_DIR / "ep03_infographic_06_acoustic_sounding_thickness.jpg"
    img.save(out, quality=95)
    print(f"Generated: {out.name}")

if __name__ == "__main__":
    print("=" * 60)
    print("  GENERATING EPISODE 3 TECHNICAL BLUEPRINT CARDS (PIL)")
    print("=" * 60)
    make_card_01_monolith_dimensions()
    make_card_02_bottom_up_vs_top_down()
    make_card_03_zero_error_margin()
    make_card_04_shanku_cardinal_alignment()
    make_card_05_dravidian_vimana_tiers()
    make_card_06_acoustic_sounding()
    print("\nAll 6 bespoke technical blueprint cards successfully generated!")
