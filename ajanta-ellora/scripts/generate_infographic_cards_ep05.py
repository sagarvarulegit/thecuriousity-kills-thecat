"""
Generate high-retention documentary technical infographic and blueprint cards
for Kailasa Episode 05: The Elephants Beneath Kailasa using PIL.
These cards provide visual variety and architectural evidence without
speculative engineering equations, maintaining strict zero-repetition.

Saves cards directly to ajanta-ellora/episode05/images/
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parent.parent # ajanta-ellora
IMAGES_DIR = BASE_DIR / "episode05" / "images"
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

WIDTH, HEIGHT = 1920, 1080

def get_font(size):
    for f in ["arial.ttf", "segoeui.ttf", "tahoma.ttf"]:
        try:
            return ImageFont.truetype(f, size)
        except Exception:
            continue
    return ImageFont.load_default()

def get_font_bold(size):
    for f in ["arialbd.ttf", "segoeuib.ttf", "impact.ttf"]:
        try:
            return ImageFont.truetype(f, size)
        except Exception:
            continue
    return ImageFont.load_default()

def create_base_canvas(subhead="THE ELEPHANTS BENEATH KAILASA"):
    img = Image.new("RGB", (WIDTH, HEIGHT), color=(12, 16, 22))
    draw = ImageDraw.Draw(img)
    
    # Outer cinematic border
    draw.rectangle([40, 40, WIDTH-40, HEIGHT-40], outline=(55, 70, 90), width=2)
    draw.rectangle([48, 48, WIDTH-48, HEIGHT-48], outline=(28, 38, 50), width=1)
    
    # Header branding
    f_sub = get_font(19)
    draw.text((70, 65), "KAILASA TEMPLE ARCHAEOLOGICAL & ARCHITECTURAL DOSSIER // ELLORA CAVE 16", fill=(120, 155, 190), font=f_sub)
    draw.text((WIDTH - 550, 65), f"SERIES EPISODE 05: {subhead}", fill=(195, 150, 75), font=f_sub)
    draw.line([(70, 95), (WIDTH - 70, 95)], fill=(45, 60, 75), width=1)
    
    # Blueprint grid
    for x in range(100, WIDTH - 100, 150):
        draw.line([(x, 110), (x, HEIGHT - 80)], fill=(18, 24, 32), width=1)
    for y in range(120, HEIGHT - 80, 120):
        draw.line([(70, y), (WIDTH - 70, y)], fill=(18, 24, 32), width=1)
        
    return img, draw

def make_card_01_plinth_elevation_profile():
    img, draw = create_base_canvas(subhead="PLINTH ELEVATION & BASEMENT PROFILE")
    f_title = get_font_bold(38)
    f_h2 = get_font_bold(22)
    f_body = get_font(18)
    f_num = get_font_bold(40)
    
    draw.text((70, 125), "MONUMENTAL PLINTH ELEVATION ARCHITECTURE", fill=(240, 245, 255), font=f_title)
    draw.text((70, 175), "VERTICAL STRATIGRAPHY OF THE ROCK-CUT LOWER STOREY (8TH CENTURY CE)", fill=(195, 150, 75), font=f_h2)
    
    cx, cy = 960, 500
    
    # Main elevation schematic
    # Courtyard base line
    draw.line([(cx - 650, cy + 240), (cx + 650, cy + 240)], fill=(160, 180, 200), width=4)
    draw.text((cx - 640, cy + 250), "EXCAVATED COURTYARD FLOOR (BEDROCK LEVEL 0.0m)", fill=(140, 160, 180), font=f_body)
    
    # Plinth Base Moulding (Upapitha / Adhisthana)
    draw.rectangle([cx - 450, cy + 180, cx + 450, cy + 240], fill=(22, 30, 42), outline=(75, 165, 245), width=2)
    draw.text((cx - 430, cy + 200), "LOWEST MOULDED CORNICE (UPAPITHA FOUNDATION BAND)", fill=(180, 205, 235), font=f_body)
    
    # Central Elephant Frieze Band (Monumental High Relief)
    draw.rectangle([cx - 450, cy - 80, cx + 450, cy + 180], fill=(30, 42, 60), outline=(240, 200, 90), width=3)
    draw.text((cx - 430, cy - 60), "MONUMENTAL SCULPTURAL FRIEZE: LIFE-SIZED ELEPHANTS & LIONS (HEIGHT: ~8.0m)", fill=(255, 220, 120), font=f_h2)
    
    # Elephant silhouette representation blocks
    for i in range(5):
        bx = cx - 400 + i * 165
        draw.rectangle([bx, cy - 20, bx + 140, cy + 160], fill=(45, 62, 88), outline=(255, 204, 0), width=2)
        draw.text((bx + 20, cy + 20), f"ELEPHANT\nRELIEF #{i+1}", fill=(240, 240, 255), font=f_body)
        draw.text((bx + 20, cy + 80), "High Relief\n(60-90cm)", fill=(190, 210, 230), font=get_font(14))
    
    # Projecting Upper Cornice Moulding
    draw.rectangle([cx - 480, cy - 140, cx + 480, cy - 80], fill=(35, 48, 68), outline=(75, 165, 245), width=2)
    draw.text((cx - 430, cy - 120), "PROJECTING OVERHANGING LEDGE (CORNICE SUPPORT ILLUSION)", fill=(180, 220, 255), font=f_body)
    
    # Upper Temple Hall (Maha Mandapa floor)
    draw.rectangle([cx - 420, cy - 230, cx + 420, cy - 140], fill=(20, 28, 40), outline=(100, 130, 160), width=2)
    draw.text((cx - 350, cy - 195), "UPPER SANCTUARY & MANDAPA STOREY (RESTING APPARENTLY ON ELEPHANTS)", fill=(220, 230, 245), font=f_h2)
    
    # Metric Summary Boxes
    draw.rectangle([70, 840, 480, 970], fill=(20, 26, 36), outline=(60, 80, 110))
    draw.text((95, 855), "~8.0 METERS", fill=(75, 165, 245), font=f_num)
    draw.text((95, 920), "Monumental Plinth Height", fill=(180, 195, 215), font=f_body)
    
    draw.rectangle([540, 840, 950, 970], fill=(20, 26, 36), outline=(60, 80, 110))
    draw.text((565, 855), "CONTINUOUS", fill=(240, 200, 90), font=f_num)
    draw.text((565, 920), "Integral Basalt Bedrock Core", fill=(180, 195, 215), font=f_body)

    draw.rectangle([1010, 840, 1420, 970], fill=(20, 26, 36), outline=(60, 80, 110))
    draw.text((1035, 855), "NON-STRUCTURAL", fill=(130, 220, 140), font=f_num)
    draw.text((1035, 920), "Sculpted Relief Exterior Shell", fill=(180, 195, 215), font=f_body)

    draw.rectangle([1480, 840, 1850, 970], fill=(20, 26, 36), outline=(60, 80, 110))
    draw.text((1505, 855), "360° BAND", fill=(250, 140, 100), font=f_num)
    draw.text((1505, 920), "Wraps Entire Temple Perimeter", fill=(180, 195, 215), font=f_body)

    out_path = IMAGES_DIR / "ep05_infographic_01_plinth_elevation_profile.jpg"
    img.save(out_path, "JPEG", quality=95)
    print(f"Generated: {out_path.name}")

def make_card_02_monolithic_subtractive_plinth():
    img, draw = create_base_canvas(subhead="SUBTRACTIVE BEDROCK VS ADDITIVE MASONRY")
    f_title = get_font_bold(38)
    f_h2 = get_font_bold(22)
    f_body = get_font(18)
    f_num = get_font_bold(38)
    
    draw.text((70, 125), "STRUCTURAL REALITY: SUBTRACTIVE VS ADDITIVE", fill=(240, 245, 255), font=f_title)
    draw.text((70, 175), "WHY THE ELEPHANTS ARE NOT STRUCTURAL PILLARS (DECCAN TRAP BASALT)", fill=(195, 150, 75), font=f_h2)
    
    cx = 960
    
    # Left Box: Standard Built Temple (Additive Masonry)
    draw.rectangle([100, 240, cx - 40, 780], fill=(16, 22, 30), outline=(220, 100, 80), width=2)
    draw.text((130, 265), "CONSTRUCTED TEMPLE (ADDITIVE MASONRY)", fill=(245, 130, 110), font=f_h2)
    draw.text((130, 310), "Separate ashlar blocks transported, hoisted, and stacked.", fill=(180, 195, 210), font=f_body)
    
    # Graphic of assembled blocks with joints
    for r in range(5):
        y0 = 360 + r * 55
        for c in range(4):
            x0 = 150 + c * 160 + (40 if r%2==1 else 0)
            draw.rectangle([x0, y0, min(x0 + 150, cx - 80), y0 + 45], fill=(30, 40, 54), outline=(180, 80, 80), width=2)
    draw.text((150, 660), "❌ Mortar & mechanical joints between blocks", fill=(240, 150, 150), font=f_body)
    draw.text((150, 695), "❌ Differential ground settlement vulnerability", fill=(240, 150, 150), font=f_body)
    draw.text((150, 730), "❌ Freestanding columns bear direct vertical point load", fill=(240, 150, 150), font=f_body)
    
    # Right Box: Kailasa Monolith (Subtractive Rock-cut)
    draw.rectangle([cx + 40, 240, WIDTH - 100, 780], fill=(16, 22, 30), outline=(75, 165, 245), width=2)
    draw.text((cx + 70, 265), "KAILASA CAVE 16 (SUBTRACTIVE BEDROCK)", fill=(100, 185, 255), font=f_h2)
    draw.text((cx + 70, 310), "Excavated from solid mountain ridge top-down into basalt.", fill=(180, 195, 210), font=f_body)
    
    # Graphic of solid continuous bedrock with elephant relief carved on outer face
    draw.rectangle([cx + 70, 360, WIDTH - 150, 620], fill=(35, 48, 66), outline=(75, 165, 245), width=2)
    draw.rectangle([cx + 90, 420, cx + 240, 580], fill=(50, 70, 95), outline=(240, 200, 90), width=2)
    draw.text((cx + 105, 470), "SCULPTED\nELEPHANT\n(RELIEF)", fill=(255, 215, 0), font=f_body)
    
    draw.rectangle([cx + 250, 400, WIDTH - 180, 600], fill=(25, 35, 48), outline=(60, 90, 120), width=1)
    draw.text((cx + 330, 480), "CONTINUOUS SOLID BASALT CORE\n(CARRIES 100% OF TEMPLE LOAD)", fill=(160, 210, 255), font=f_h2)
    
    draw.text((cx + 70, 660), "✔ ZERO joints, ZERO mortar, ZERO structural seams", fill=(130, 220, 140), font=f_body)
    draw.text((cx + 70, 695), "✔ Continuous Deccan trap basalt formation (140 MPa strength)", fill=(130, 220, 140), font=f_body)
    draw.text((cx + 70, 730), "✔ Sculptures are relief carvings, NOT independent weight pillars", fill=(130, 220, 140), font=f_body)
    
    # Bottom callout
    draw.rectangle([70, 840, WIDTH - 70, 970], fill=(20, 26, 36), outline=(60, 80, 110))
    draw.text((95, 860), "THE ARCHITECTURAL ILLUSION:", fill=(240, 200, 90), font=f_num)
    draw.text((95, 915), "The elephants appear to bear the monument on their backs; in engineering reality, the bedrock mountain bears both the temple and the elephants.", fill=(200, 215, 235), font=f_body)

    out_path = IMAGES_DIR / "ep05_infographic_02_monolithic_subtractive_plinth.jpg"
    img.save(out_path, "JPEG", quality=95)
    print(f"Generated: {out_path.name}")

def make_card_03_courtyard_sightlines_scale():
    img, draw = create_base_canvas(subhead="PRADAKSHINA AMBULATORY SIGHTLINES")
    f_title = get_font_bold(38)
    f_h2 = get_font_bold(22)
    f_body = get_font(18)
    f_num = get_font_bold(38)
    
    draw.text((70, 125), "COURTYARD AMBULATORY & SIGHTLINE PHENOMENOLOGY", fill=(240, 245, 255), font=f_title)
    draw.text((70, 175), "HOW VISITOR EYE-LEVEL EXPERIENCES MONUMENTAL PLINTH SCALE (COURTYARD AMBULATORY)", fill=(195, 150, 75), font=f_h2)
    
    cx, cy = 960, 520
    
    # Courtyard Cross Section Diagram
    # Left outer trench cliff wall
    draw.rectangle([120, 240, 240, cy + 240], fill=(25, 32, 42), outline=(90, 110, 135), width=2)
    draw.text((140, 260), "VERTICAL\nCLIFF SCARP\n(32m HIGH)", fill=(160, 185, 210), font=f_body)
    
    # Floor
    draw.line([(240, cy + 240), (WIDTH - 150, cy + 240)], fill=(160, 180, 200), width=4)
    draw.text((280, cy + 260), "NARROW COURTYARD AMBULATORY TRENCH (WIDTH: ~9m - 12m)", fill=(140, 165, 190), font=f_body)
    
    # Pilgrim human figure
    px = 380
    draw.ellipse([px-12, cy + 130, px+12, cy + 154], fill=(240, 200, 90)) # head
    draw.line([(px, cy + 154), (px, cy + 205)], fill=(240, 200, 90), width=4) # body
    draw.line([(px, cy + 205), (px - 10, cy + 240)], fill=(240, 200, 90), width=3) # left leg
    draw.line([(px, cy + 205), (px + 10, cy + 240)], fill=(240, 200, 90), width=3) # right leg
    draw.text((px - 70, cy + 100), "VISITOR EYE LEVEL\n(1.65m - 1.70m)", fill=(240, 200, 90), font=f_body)
    
    # Temple Plinth Face
    tx = 650
    draw.rectangle([tx, cy - 60, tx + 750, cy + 240], fill=(32, 44, 62), outline=(75, 165, 245), width=2)
    draw.text((tx + 40, cy + 180), "PLINTH BASEMENT (~8.0m HEIGHT)", fill=(200, 220, 245), font=f_h2)
    
    # Elephant Relief Profile on Plinth
    draw.rectangle([tx - 60, cy + 20, tx + 180, cy + 180], fill=(48, 66, 92), outline=(255, 215, 0), width=2)
    draw.text((tx - 40, cy + 60), "CARVED ELEPHANT\nPROJECTING HEAD\n& TUSKS (2.5m - 3.0m)", fill=(255, 230, 140), font=f_body)
    
    # Sightline 1 (Direct eye to elephant eye)
    draw.line([(px + 12, cy + 140), (tx - 50, cy + 80)], fill=(255, 120, 80), width=2)
    draw.text((450, cy + 60), "Direct Sightline: Monumental Animal at Eye Level", fill=(255, 140, 100), font=get_font(16))
    
    # Sightline 2 (Upward gaze to upper temple cornice)
    draw.line([(px + 12, cy + 140), (tx + 120, cy - 220)], fill=(120, 220, 140), width=2)
    draw.text((450, cy - 100), "Upward Angle: 65°–75° Forced Perspective (Temple Appears Soaring)", fill=(130, 225, 150), font=get_font(16))
    
    # Upper Mandapa Wall
    draw.rectangle([tx + 100, cy - 260, tx + 750, cy - 60], fill=(22, 32, 46), outline=(90, 120, 150), width=2)
    draw.text((tx + 150, cy - 180), "UPPER SANCTUARY LEVEL\n(MANDAPA STOREY: 30m SUMMIT ABOVE)", fill=(180, 205, 230), font=f_h2)

    # Summary Cards
    draw.rectangle([70, 840, 580, 970], fill=(20, 26, 36), outline=(60, 80, 110))
    draw.text((95, 855), "FORCED VERTICALITY", fill=(75, 165, 245), font=f_num)
    draw.text((95, 920), "Narrow 10m Trench Amplifies Sensation of Height", fill=(180, 195, 215), font=f_body)

    draw.rectangle([640, 840, 1200, 970], fill=(20, 26, 36), outline=(60, 80, 110))
    draw.text((665, 855), "PRADAKSHINA RHYTHM", fill=(240, 200, 90), font=f_num)
    draw.text((665, 920), "Clockwise Circumambulation Unfolds Frieze Beat by Beat", fill=(180, 195, 215), font=f_body)

    draw.rectangle([1260, 840, 1850, 970], fill=(20, 26, 36), outline=(60, 80, 110))
    draw.text((1285, 855), "HUMAN ENCOUNTER", fill=(130, 220, 140), font=f_num)
    draw.text((1285, 920), "Colossal Beast Heads Loom Directly Overhead", fill=(180, 195, 215), font=f_body)

    out_path = IMAGES_DIR / "ep05_infographic_03_courtyard_sightlines_scale.jpg"
    img.save(out_path, "JPEG", quality=95)
    print(f"Generated: {out_path.name}")

def make_card_04_cosmic_diggajas_iconography():
    img, draw = create_base_canvas(subhead="COSMIC DIGGAJAS ICONOGRAPHY")
    f_title = get_font_bold(38)
    f_h2 = get_font_bold(22)
    f_body = get_font(18)
    f_num = get_font_bold(38)
    
    draw.text((70, 125), "COSMIC DIGGAJAS: GUARDIANS OF THE EIGHT DIRECTIONS", fill=(240, 245, 255), font=f_title)
    draw.text((70, 175), "TRADITIONAL INDIAN COSMOLOGY: ELEPHANTS BEARING MOUNT MERU & KAILASA", fill=(195, 150, 75), font=f_h2)
    
    cx, cy = 960, 500
    
    # Cosmic Compass / Mandala diagram
    draw.ellipse([cx - 260, cy - 260, cx + 260, cy + 260], outline=(75, 165, 245), width=2, fill=(16, 24, 34))
    draw.ellipse([cx - 160, cy - 160, cx + 160, cy + 160], outline=(240, 200, 90), width=2, fill=(24, 34, 48))
    
    draw.text((cx - 120, cy - 35), "MOUNT KAILASA\n(AXIS MUNDI)", fill=(255, 230, 140), font=f_h2)
    
    # 8 Cardinal Points and Diggajas
    directions = [
        ("NORTH (KUBERA)", "SARVABHAUMA", cx, cy - 230),
        ("NORTH-EAST (ISHANA)", "SUPRATIKA", cx + 170, cy - 170),
        ("EAST (INDRA)", "AIRAVATA", cx + 230, cy),
        ("SOUTH-EAST (AGNI)", "PUNDARIKA", cx + 170, cy + 170),
        ("SOUTH (YAMA)", "VAMANA", cx, cy + 230),
        ("SOUTH-WEST (NIRRITI)", "KUMUDA", cx - 170, cy + 170),
        ("WEST (VARUNA)", "ANJANA", cx - 230, cy),
        ("NORTH-WEST (VAYU)", "PUSHPADANTA", cx - 170, cy - 170),
    ]
    
    for dir_name, elephant, x, y in directions:
        draw.rectangle([x - 110, y - 25, x + 110, y + 25], fill=(30, 42, 58), outline=(240, 200, 90), width=1)
        draw.text((x - 95, y - 20), dir_name, fill=(130, 190, 245), font=get_font(13))
        draw.text((x - 95, y - 2), elephant, fill=(255, 255, 255), font=get_font_bold(16))
        # Line pointing to center
        draw.line([(x, y), (cx, cy)], fill=(45, 70, 95), width=1)

    # Explanation panels on left and right
    draw.rectangle([70, 240, 420, 780], fill=(18, 25, 35), outline=(60, 85, 115))
    draw.text((95, 265), "COSMIC FOUNDATION", fill=(240, 200, 90), font=f_h2)
    draw.text((95, 310), "In Puranic tradition, eight divine\nelephants (Diggajas) anchor the\ncardinal and intermediate points,\npreventing the cosmos from trembling.", fill=(180, 200, 220), font=f_body)
    draw.text((95, 430), "At Kailasa, carving a herd of\nelephants at the base visually\nmanifests the temple as Mount Meru\nsustained by cosmic powers.", fill=(180, 200, 220), font=f_body)
    draw.text((95, 550), "Lions and composite vyalas are\ninterspersed, signifying supreme\nsovereign Rashtrakuta strength.", fill=(180, 200, 220), font=f_body)

    draw.rectangle([WIDTH - 420, 240, WIDTH - 70, 780], fill=(18, 25, 35), outline=(60, 85, 115))
    draw.text((WIDTH - 395, 265), "SACRED & SECULAR", fill=(75, 165, 245), font=f_h2)
    draw.text((WIDTH - 395, 310), "Royal Auspiciousness (Gaja):\nElephants symbolize sovereign\npower, rain clouds (Megha), and\nLakshmi's blessing (Gajalakshmi).", fill=(180, 200, 220), font=f_body)
    draw.text((WIDTH - 395, 430), "Multiple valid interpretations:\n• Cosmic pillar support\n• Rain clouds below summit\n• Imperial military prestige\n• Living mythological boundary", fill=(180, 200, 220), font=f_body)

    # Bottom summary
    draw.rectangle([70, 840, WIDTH - 70, 970], fill=(20, 26, 36), outline=(60, 80, 110))
    draw.text((95, 860), "ICONOGRAPHIC AMBIGUITY:", fill=(240, 200, 90), font=f_num)
    draw.text((95, 915), "No 8th-century builder manual dictates a single reading. The sculpture operates simultaneously on cosmic, mythological, and aesthetic planes.", fill=(200, 215, 235), font=f_body)

    out_path = IMAGES_DIR / "ep05_infographic_04_cosmic_diggajas_iconography.jpg"
    img.save(out_path, "JPEG", quality=95)
    print(f"Generated: {out_path.name}")

def make_card_05_basalt_compression_vs_relief():
    img, draw = create_base_canvas(subhead="BASALT COMPRESSION VS SCULPTURAL RELIEF")
    f_title = get_font_bold(38)
    f_h2 = get_font_bold(22)
    f_body = get_font(18)
    f_num = get_font_bold(38)
    
    draw.text((70, 125), "MATERIAL SCIENCE: BASALT LOAD BEARING CAPACITY", fill=(240, 245, 255), font=f_title)
    draw.text((70, 175), "DECCAN VOLCANIC BEDROCK COMPRESSION VS ZERO SCULPTURAL RELIEF LOAD", fill=(195, 150, 75), font=f_h2)
    
    cx, cy = 960, 500
    
    # Graphic section: Central rock core vs outer frieze
    draw.rectangle([cx - 400, cy - 220, cx + 400, cy + 220], fill=(24, 34, 48), outline=(75, 165, 245), width=2)
    
    # Core zone
    draw.rectangle([cx - 200, cy - 220, cx + 200, cy + 220], fill=(36, 50, 70), outline=(130, 220, 140), width=3)
    draw.text((cx - 150, cy - 100), "SOLID BASALT\nCENTRAL CORE\n(UNTOUCHED BEDROCK)", fill=(150, 230, 160), font=f_h2)
    draw.text((cx - 150, cy + 20), "120 – 160 MPa\nCompressive Strength\nCarries 100% of temple mass", fill=(220, 245, 230), font=f_body)
    
    # Downward force arrows on core
    for ax in [cx - 100, cx, cx + 100]:
        draw.line([(ax, cy - 200), (ax, cy - 140)], fill=(130, 220, 140), width=4)
        draw.polygon([(ax - 8, cy - 140), (ax + 8, cy - 140), (ax, cy - 120)], fill=(130, 220, 140))
        
    # Left & Right Sculpted Relief zones
    # Left relief
    draw.rectangle([cx - 380, cy - 80, cx - 210, cy + 180], fill=(50, 68, 94), outline=(240, 200, 90), width=2)
    draw.text((cx - 365, cy - 50), "OUTER RELIEF\nELEPHANT", fill=(255, 215, 0), font=f_h2)
    draw.text((cx - 365, cy + 30), "Load: 0.0 MPa\n(Cantilevered\nDecorative\nCarving)", fill=(230, 235, 245), font=f_body)
    
    # Right relief
    draw.rectangle([cx + 210, cy - 80, cx + 380, cy + 180], fill=(50, 68, 94), outline=(240, 200, 90), width=2)
    draw.text((cx + 225, cy - 50), "OUTER RELIEF\nELEPHANT", fill=(255, 215, 0), font=f_h2)
    draw.text((cx + 225, cy + 30), "Load: 0.0 MPa\n(Cantilevered\nDecorative\nCarving)", fill=(230, 235, 245), font=f_body)

    # Metrics Summary Boxes
    draw.rectangle([70, 840, 480, 970], fill=(20, 26, 36), outline=(60, 80, 110))
    draw.text((95, 855), "140 MPa", fill=(130, 220, 140), font=f_num)
    draw.text((95, 920), "Basalt Bedrock Ultimate Strength", fill=(180, 195, 215), font=f_body)
    
    draw.rectangle([540, 840, 950, 970], fill=(20, 26, 36), outline=(60, 80, 110))
    draw.text((565, 855), "0.0 kN", fill=(240, 200, 90), font=f_num)
    draw.text((565, 920), "Vertical Load on Elephant Heads", fill=(180, 195, 215), font=f_body)

    draw.rectangle([1010, 840, 1420, 970], fill=(20, 26, 36), outline=(60, 80, 110))
    draw.text((1035, 855), "MONOLITHIC", fill=(75, 165, 245), font=f_num)
    draw.text((1035, 920), "Zero Shear Failure Plane Risk", fill=(180, 195, 215), font=f_body)

    draw.rectangle([1480, 840, 1850, 970], fill=(20, 26, 36), outline=(60, 80, 110))
    draw.text((1505, 855), "SCULPTURAL", fill=(250, 140, 100), font=f_num)
    draw.text((1505, 920), "Visual Rhetoric of Weight & Lift", fill=(180, 195, 215), font=f_body)

    out_path = IMAGES_DIR / "ep05_infographic_05_basalt_compression_vs_relief.jpg"
    img.save(out_path, "JPEG", quality=95)
    print(f"Generated: {out_path.name}")

def make_card_06_havell_cloud_hypothesis():
    img, draw = create_base_canvas(subhead="HAVELL'S CLOUD HYPOTHESIS VS EVIDENCE")
    f_title = get_font_bold(38)
    f_h2 = get_font_bold(22)
    f_body = get_font(18)
    f_num = get_font_bold(38)
    
    draw.text((70, 125), "E.B. HAVELL'S CLOUD INTERPRETATION (1920) VS EVIDENCE", fill=(240, 245, 255), font=f_title)
    draw.text((70, 175), "POETIC METAPHOR OF MONSOON CLOUDS BEARING A HIMALAYAN PEAK", fill=(195, 150, 75), font=f_h2)
    
    cx = 960
    
    # Left Box: Havell's Poetic Interpretation
    draw.rectangle([100, 240, cx - 40, 780], fill=(16, 22, 30), outline=(240, 200, 90), width=2)
    draw.text((130, 265), "HAVELL'S POETIC READING (1920)", fill=(255, 215, 0), font=f_h2)
    draw.text((130, 310), "From 'The Himalayas in Indian Art', p. 27", fill=(180, 195, 210), font=f_body)
    
    draw.rectangle([130, 360, cx - 70, 520], fill=(28, 38, 52), outline=(180, 150, 60))
    quote = (
        '"The great elephants carved along the base represent\n'
        'the rain clouds gathered round the foot of the\n'
        'sacred mountain, seeming to waft it upward into\n'
        'the heavens..."'
    )
    draw.text((150, 385), quote, fill=(240, 230, 180), font=f_body)
    
    draw.text((130, 550), "• Poetic association between elephants (gaja) and rain clouds (megha)", fill=(200, 215, 230), font=f_body)
    draw.text((130, 595), "• Temple vimana treated as sacred snow-peak of Mount Kailasa", fill=(200, 215, 230), font=f_body)
    draw.text((130, 640), "• Beautiful literary synthesis of Sanskrit poetry and architecture", fill=(200, 215, 230), font=f_body)
    draw.text((130, 690), "Status: Valid 20th-century aesthetic interpretation", fill=(255, 204, 0), font=get_font_bold(17))

    # Right Box: Physical Archaeological Record
    draw.rectangle([cx + 40, 240, WIDTH - 100, 780], fill=(16, 22, 30), outline=(75, 165, 245), width=2)
    draw.text((cx + 70, 265), "PHYSICAL ARCHAEOLOGICAL RECORD", fill=(100, 185, 255), font=f_h2)
    draw.text((cx + 70, 310), "Direct evidence preserved in stone and epigraphy", fill=(180, 195, 210), font=f_body)
    
    draw.text((cx + 70, 370), "✔ Deeply chiseled basalt relief: Elephants gathering lotus flowers", fill=(140, 220, 150), font=f_body)
    draw.text((cx + 70, 420), "✔ Fighting lions and vyalas interspersed: Royal martial emblem", fill=(140, 220, 150), font=f_body)
    draw.text((cx + 70, 470), "✔ Rashtrakuta royal charters: Celebrate King Krishna I's divine glory", fill=(140, 220, 150), font=f_body)
    draw.text((cx + 70, 520), "✔ Upapitha structural base: Classical Dravidian basement moulding", fill=(140, 220, 150), font=f_body)
    draw.text((cx + 70, 580), "❓ Zero written inscriptions mention rain-cloud allegory", fill=(250, 160, 120), font=f_body)
    draw.text((cx + 70, 630), "❓ Cloud metaphor is not an engineering or artisan manual directive", fill=(250, 160, 120), font=f_body)
    draw.text((cx + 70, 690), "Status: Rigorous historical distinction required", fill=(100, 185, 255), font=get_font_bold(17))

    # Bottom summary
    draw.rectangle([70, 840, WIDTH - 70, 970], fill=(20, 26, 36), outline=(60, 80, 110))
    draw.text((95, 860), "EDITORIAL INTEGRITY PRINCIPLE:", fill=(240, 200, 90), font=f_num)
    draw.text((95, 915), "We present Havell's reading as a resonant interpretation, not an established 8th-century fact. Good documentary honors both poetry and evidence.", fill=(200, 215, 235), font=f_body)

    out_path = IMAGES_DIR / "ep05_infographic_06_havell_cloud_hypothesis.jpg"
    img.save(out_path, "JPEG", quality=95)
    print(f"Generated: {out_path.name}")

def make_card_07_relief_undercutting_profile():
    img, draw = create_base_canvas(subhead="HIGH RELIEF UNDERCUTTING PROFILE")
    f_title = get_font_bold(38)
    f_h2 = get_font_bold(22)
    f_body = get_font(18)
    f_num = get_font_bold(38)
    
    draw.text((70, 125), "SCULPTURAL TECHNIQUE: HIGH RELIEF UNDERCUTTING", fill=(240, 245, 255), font=f_title)
    draw.text((70, 175), "HOW RASHTRAKUTA STONECUTTERS FREED 3D BODIES FROM BEDROCK", fill=(195, 150, 75), font=f_h2)
    
    cx, cy = 960, 500
    
    # Cross section of elephant trunk / underbelly carving
    draw.rectangle([cx - 450, cy - 200, cx + 450, cy + 200], fill=(20, 28, 40), outline=(75, 165, 245), width=2)
    
    # Bedrock backing
    draw.rectangle([cx - 450, cy - 200, cx - 150, cy + 200], fill=(30, 42, 60), outline=(60, 80, 110))
    draw.text((cx - 420, cy - 20), "SOLID UNTOUCHED\nBASALT BEDROCK", fill=(160, 190, 220), font=f_h2)
    
    # Deeply undercut cavity
    draw.rectangle([cx - 150, cy - 120, cx - 20, cy + 150], fill=(10, 14, 20), outline=(240, 200, 90), width=2)
    draw.text((cx - 140, cy - 20), "DEEP\nUNDERCUT\n(60-90cm\nVOID)", fill=(255, 215, 0), font=f_body)
    
    # Elephant Forequarter Projecting Outward
    draw.rectangle([cx - 20, cy - 150, cx + 380, cy + 170], fill=(45, 65, 90), outline=(255, 204, 0), width=3)
    draw.text((cx + 20, cy - 80), "PROJECTING ELEPHANT HEAD & TRUNK", fill=(255, 230, 130), font=f_h2)
    draw.text((cx + 20, cy - 20), "• Full 3D anatomical volume in front\n• Ears flared outwards from rock plane\n• Curled trunk clasping lotus flower\n• Weathering on exposed basalt tusks", fill=(210, 225, 240), font=f_body)

    # Metrics Summary
    draw.rectangle([70, 840, 480, 970], fill=(20, 26, 36), outline=(60, 80, 110))
    draw.text((95, 855), "60 – 90 CM", fill=(75, 165, 245), font=f_num)
    draw.text((95, 920), "Maximum Relief Undercut Depth", fill=(180, 195, 215), font=f_body)
    
    draw.rectangle([540, 840, 950, 970], fill=(20, 26, 36), outline=(60, 80, 110))
    draw.text((565, 855), "SHADOW PLAY", fill=(240, 200, 90), font=f_num)
    draw.text((565, 920), "Cavities Create Deep Natural Shadow", fill=(180, 195, 215), font=f_body)

    draw.rectangle([1010, 840, 1420, 970], fill=(20, 26, 36), outline=(60, 80, 110))
    draw.text((1035, 855), "CHISEL MARKS", fill=(130, 220, 140), font=f_num)
    draw.text((1035, 920), "Fine Point Pick & Claw Chisel Finishes", fill=(180, 195, 215), font=f_body)

    draw.rectangle([1480, 840, 1850, 970], fill=(20, 26, 36), outline=(60, 80, 110))
    draw.text((1505, 855), "INTEGRAL", fill=(250, 140, 100), font=f_num)
    draw.text((1505, 920), "Rear Rooted Directly into Bedrock", fill=(180, 195, 215), font=f_body)

    out_path = IMAGES_DIR / "ep05_infographic_07_relief_undercutting_profile.jpg"
    img.save(out_path, "JPEG", quality=95)
    print(f"Generated: {out_path.name}")

def make_card_08_plinth_sculptural_fauna_survey():
    img, draw = create_base_canvas(subhead="PLINTH SCULPTURAL FAUNA SURVEY")
    f_title = get_font_bold(38)
    f_h2 = get_font_bold(22)
    f_body = get_font(18)
    f_num = get_font_bold(38)
    
    draw.text((70, 125), "PLINTH SCULPTURAL FAUNA & ICONOGRAPHIC CENSUS", fill=(240, 245, 255), font=f_title)
    draw.text((70, 175), "DISTRIBUTION OF ANIMALS ACROSS THE KAILASA BASEMENT PERIMETER", fill=(195, 150, 75), font=f_h2)
    
    # 4 Species Panels
    panels = [
        ("ASIAN ELEPHANT (GAJA)", "DOMINANT SPECIES", "Bearing mountain mass; grasping lotus stems;\ncalm majestic stances alternating with\ndynamic head turns toward courtyard.", (240, 200, 90), 100),
        ("LION (SIMHA / SHARDULA)", "SOVEREIGN PREDATOR", "Attacking elephants, grappling at flanks;\nsymbolizing Rashtrakuta imperial conquest\nand victorious solar ferocity.", (75, 165, 245), 520),
        ("MYTHICAL VYALA (YALI)", "COMPOSITE CREATURE", "Leogryphs with horned heads and leonine\nbodies; celestial guardians defending\nthe cosmic axis from demonic entry.", (130, 220, 140), 940),
        ("FIGHTING DUELS", "NARRATIVE ACTION", "Dynamic combat groups chiseled into corners;\ndemonstrating stonecutter virtuosity\nin complex multi-body choreography.", (250, 140, 100), 1360)
    ]
    
    for title, subtitle, desc, col, px in panels:
        draw.rectangle([px, 240, px + 400, 780], fill=(18, 25, 36), outline=col, width=2)
        draw.rectangle([px + 20, 260, px + 380, 320], fill=(28, 38, 52), outline=col, width=1)
        draw.text((px + 30, 275), title, fill=col, font=get_font_bold(19))
        draw.text((px + 30, 340), subtitle, fill=(180, 200, 225), font=get_font(15))
        draw.text((px + 30, 390), desc, fill=(210, 225, 240), font=f_body)
        
        # Bottom small box
        draw.rectangle([px + 20, 680, px + 380, 750], fill=(12, 18, 26), outline=(60, 80, 100))
        draw.text((px + 35, 700), "Carved in Situ (8th c. CE)", fill=(160, 180, 200), font=get_font(16))

    # Bottom summary
    draw.rectangle([70, 840, WIDTH - 70, 970], fill=(20, 26, 36), outline=(60, 80, 110))
    draw.text((95, 860), "PLINTH CENSUS OVERVIEW:", fill=(240, 200, 90), font=f_num)
    draw.text((95, 915), "Over one hundred sculpted animal figures wrap the perimeter of Kailasa's lower storey, transforming heavy rock into an animated tableau.", fill=(200, 215, 235), font=f_body)

    out_path = IMAGES_DIR / "ep05_infographic_08_plinth_sculptural_fauna_survey.jpg"
    img.save(out_path, "JPEG", quality=95)
    print(f"Generated: {out_path.name}")

def main():
    print("=" * 65)
    print(" GENERATING EPISODE 05 TECHNICAL INFOGRAPHIC BLUEPRINT CARDS")
    print("=" * 65)
    make_card_01_plinth_elevation_profile()
    make_card_02_monolithic_subtractive_plinth()
    make_card_03_courtyard_sightlines_scale()
    make_card_04_cosmic_diggajas_iconography()
    make_card_05_basalt_compression_vs_relief()
    make_card_06_havell_cloud_hypothesis()
    make_card_07_relief_undercutting_profile()
    make_card_08_plinth_sculptural_fauna_survey()
    print("=" * 65)
    print(" ALL 8 TECHNICAL INFOGRAPHIC CARDS GENERATED SUCCESSFULLY!")
    print("=" * 65)

if __name__ == "__main__":
    main()
