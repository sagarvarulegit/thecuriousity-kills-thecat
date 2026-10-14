"""
Generate high-retention documentary technical infographic and blueprint cards
for Kailasa Episode 4: The Floating Bridges of Kailasa using PIL.
These cards provide visual variety and architectural evidence without
speculative engineering equations, maintaining strict zero-repetition.

Saves cards directly to ajanta-ellora/episode04/images/
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parent.parent # ajanta-ellora
IMAGES_DIR = BASE_DIR / "episode04" / "images"
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

def create_base_canvas(subhead="THE SUSPENDED ROCK SPANS"):
    img = Image.new("RGB", (WIDTH, HEIGHT), color=(12, 16, 22))
    draw = ImageDraw.Draw(img)
    
    # Outer cinematic border
    draw.rectangle([40, 40, WIDTH-40, HEIGHT-40], outline=(55, 70, 90), width=2)
    draw.rectangle([48, 48, WIDTH-48, HEIGHT-48], outline=(28, 38, 50), width=1)
    
    # Header branding
    f_sub = get_font(19)
    draw.text((70, 65), "KAILASA TEMPLE ARCHAEOLOGICAL & ARCHITECTURAL DOSSIER // ELLORA CAVE 16", fill=(120, 155, 190), font=f_sub)
    draw.text((WIDTH - 490, 65), f"SERIES EPISODE 04: {subhead}", fill=(195, 150, 75), font=f_sub)
    draw.line([(70, 95), (WIDTH - 70, 95)], fill=(45, 60, 75), width=1)
    
    # Blueprint grid
    for x in range(100, WIDTH - 100, 150):
        draw.line([(x, 110), (x, HEIGHT - 80)], fill=(18, 24, 32), width=1)
    for y in range(120, HEIGHT - 80, 120):
        draw.line([(70, y), (WIDTH - 70, y)], fill=(18, 24, 32), width=1)
        
    return img, draw

def make_card_01_courtyard_spatial_void():
    img, draw = create_base_canvas(subhead="COURTYARD VOID & ISOLATED MASSES")
    f_title = get_font_bold(40)
    f_h2 = get_font_bold(24)
    f_body = get_font(20)
    f_num = get_font_bold(44)
    
    draw.text((70, 125), "THE EXCAVATED COURTYARD VOID", fill=(240, 245, 255), font=f_title)
    draw.text((70, 180), "SPATIAL SEPARATION OF FREESTANDING MONOLITHIC PAVILIONS (8TH CENTURY CE)", fill=(195, 150, 75), font=f_h2)
    
    cx, cy = 960, 500
    # Trench void bounding box
    draw.rectangle([cx - 520, cy - 180, cx + 520, cy + 240], outline=(160, 100, 40), width=2, fill=(16, 20, 28))
    
    # Three isolated rock masses: Gateway, Nandi Mandapa, Maha Mandapa
    # Gateway (West)
    draw.rectangle([cx - 460, cy - 90, cx - 340, cy + 150], outline=(75, 165, 245), width=3, fill=(24, 32, 44))
    draw.text((cx - 450, cy + 10), "ENTRANCE\nGATEWAY", fill=(255, 255, 255), font=f_h2)
    
    # Bridge 1 (Gateway to Nandi)
    draw.rectangle([cx - 340, cy - 20, cx - 200, cy + 30], outline=(240, 200, 90), width=3, fill=(45, 55, 75))
    draw.text((cx - 315, cy - 55), "BRIDGE 1", fill=(240, 200, 90), font=f_body)
    
    # Nandi Mandapa (Central)
    draw.rectangle([cx - 200, cy - 90, cx - 40, cy + 150], outline=(75, 165, 245), width=3, fill=(24, 32, 44))
    draw.text((cx - 180, cy + 10), "NANDI\nPAVILION", fill=(255, 255, 255), font=f_h2)
    
    # Bridge 2 (Nandi to Hall)
    draw.rectangle([cx - 40, cy - 20, cx + 120, cy + 30], outline=(240, 200, 90), width=3, fill=(45, 55, 75))
    draw.text((cx + 10, cy - 55), "BRIDGE 2", fill=(240, 200, 90), font=f_body)
    
    # Maha Mandapa (Main Temple Hall)
    draw.rectangle([cx + 120, cy - 130, cx + 460, cy + 190], outline=(75, 165, 245), width=3, fill=(24, 32, 44))
    draw.text((cx + 200, cy + 10), "MAHA MANDAPA\n(MAIN ASSEMBLY HALL)", fill=(255, 255, 255), font=f_h2)
    
    # Void callouts
    draw.text((cx - 290, cy + 170), "◄── OPEN COURTYARD FLOOR ──►", fill=(130, 160, 190), font=f_body)
    draw.text((cx + 20, cy + 170), "◄── OPEN COURTYARD FLOOR ──►", fill=(130, 160, 190), font=f_body)
    
    # Metric Summary Boxes
    draw.rectangle([70, 840, 480, 970], fill=(20, 26, 36), outline=(60, 80, 110))
    draw.text((95, 855), "SUSPENDED", fill=(75, 165, 245), font=f_num)
    draw.text((95, 920), "Bridges Spanning Open Air", fill=(180, 195, 215), font=f_body)
    
    draw.rectangle([540, 840, 950, 970], fill=(20, 26, 36), outline=(60, 80, 110))
    draw.text((565, 855), "SINGLE MASS", fill=(240, 200, 90), font=f_num)
    draw.text((565, 920), "Hewn from Basalt Bedrock", fill=(180, 195, 215), font=f_body)
    
    draw.rectangle([1010, 840, 1420, 970], fill=(20, 26, 36), outline=(60, 80, 110))
    draw.text((1035, 855), "UP TO 33m", fill=(230, 100, 60), font=f_num)
    draw.text((1035, 920), "Surrounding Trench Depth", fill=(180, 195, 215), font=f_body)
    
    draw.rectangle([1480, 840, 1850, 970], fill=(20, 26, 36), outline=(60, 80, 110))
    draw.text((1505, 855), "SUBTRACTIVE", fill=(140, 220, 140), font=f_num)
    draw.text((1505, 920), "Void Removed Around Passage", fill=(180, 195, 215), font=f_body)
    
    out = IMAGES_DIR / "ep04_infographic_01_courtyard_spatial_void.jpg"
    img.save(out, quality=95)
    print(f"Generated: {out.name}")

def make_card_02_continuous_stone_vs_masonry():
    img, draw = create_base_canvas(subhead="MONOLITHIC CONTINUITY VS MASONRY")
    f_title = get_font_bold(40)
    f_h2 = get_font_bold(24)
    f_body = get_font(20)
    f_num = get_font_bold(40)
    
    draw.text((70, 125), "SUBTRACTIVE MONOLITH VS CONSTRUCTED MASONRY", fill=(240, 245, 255), font=f_title)
    draw.text((70, 180), "STRUCTURAL DIFFERENCE BETWEEN ASSEMBLED ARCHES AND LIVING ROCK BRIDGES", fill=(195, 150, 75), font=f_h2)
    
    # Left Box: Constructed Masonry Arch
    draw.rectangle([100, 250, 900, 780], outline=(180, 80, 80), width=2, fill=(18, 22, 30))
    draw.text((130, 275), "ASSEMBLED MASONRY ARCH (CONVENTIONAL)", fill=(235, 100, 100), font=f_h2)
    
    # Draw segmented stone blocks and keystone
    cx1, cy1 = 500, 520
    draw.arc([cx1 - 250, cy1 - 150, cx1 + 250, cy1 + 250], start=180, end=360, fill=(200, 150, 100), width=45)
    # Radiating joint lines
    for angle_offset in [-60, -40, -20, 0, 20, 40, 60]:
        import math
        rad = math.radians(270 + angle_offset)
        x1 = cx1 + 210 * math.cos(rad)
        y1 = cy1 + 50 + 210 * math.sin(rad)
        x2 = cx1 + 270 * math.cos(rad)
        y2 = cy1 + 50 + 270 * math.sin(rad)
        draw.line([(x1, y1), (x2, y2)], fill=(12, 16, 22), width=4)
        
    draw.text((cx1 - 60, cy1 - 140), "KEYSTONE", fill=(240, 200, 90), font=f_body)
    draw.text((140, 680), "• Composed of individual dressed voussoirs", fill=(190, 205, 225), font=f_body)
    draw.text((140, 715), "• Relies on mortar joints & lateral thrust forces", fill=(190, 205, 225), font=f_body)
    draw.text((140, 750), "• Requires temporary falsework wooden centering", fill=(190, 205, 225), font=f_body)
    
    # Right Box: Living Rock Subtractive Monolith
    draw.rectangle([1020, 250, 1820, 780], outline=(75, 165, 245), width=2, fill=(18, 24, 34))
    draw.text((1050, 275), "LIVING ROCK MONOLITH (KAILASA CAVE 16)", fill=(100, 190, 255), font=f_h2)
    
    # Draw solid continuous rock slab
    cx2, cy2 = 1420, 520
    # Left pavilion anchor
    draw.rectangle([cx2 - 320, cy2 - 100, cx2 - 180, cy2 + 100], fill=(45, 60, 80), outline=(100, 170, 240), width=2)
    # Right hall anchor
    draw.rectangle([cx2 + 180, cy2 - 100, cx2 + 320, cy2 + 100], fill=(45, 60, 80), outline=(100, 170, 240), width=2)
    # Continuous bridge span
    draw.rectangle([cx2 - 180, cy2 - 40, cx2 + 180, cy2 + 20], fill=(55, 75, 100), outline=(240, 200, 90), width=3)
    
    draw.text((cx2 - 110, cy2 - 15), "CONTINUOUS BASALT", fill=(255, 255, 255), font=f_h2)
    draw.text((cx2 - 110, cy2 + 60), "NO INTERIOR JOINTS", fill=(240, 200, 90), font=f_body)
    
    draw.text((1060, 680), "• ZERO mortar lines, ZERO separate blocks", fill=(190, 205, 225), font=f_body)
    draw.text((1060, 715), "• Spans remain part of original Deccan basalt formation", fill=(190, 205, 225), font=f_body)
    draw.text((1060, 750), "• Subtracted from bedrock; space below hollowed out", fill=(190, 205, 225), font=f_body)
    
    # Bottom metric callout
    draw.rectangle([70, 830, 1850, 960], fill=(22, 28, 38), outline=(60, 80, 110))
    draw.text((100, 855), "NEGATIVE EVIDENCE IN STONE", fill=(240, 200, 90), font=f_h2)
    draw.text((100, 895), "No independent pier or central column beneath the span. The bridge functions structurally as a continuous rock entity.", fill=(200, 215, 230), font=f_body)
    
    out = IMAGES_DIR / "ep04_infographic_02_continuous_stone_vs_masonry.jpg"
    img.save(out, quality=95)
    print(f"Generated: {out.name}")

def make_card_03_staged_subtraction_reconstruction():
    img, draw = create_base_canvas(subhead="HYPOTHETICAL CUTTING STAGES")
    f_title = get_font_bold(38)
    f_h2 = get_font_bold(22)
    f_body = get_font(18)
    f_num = get_font_bold(34)
    
    draw.text((70, 125), "STAGED EXCAVATION SEQUENCE (ARCHITECTURAL RECONSTRUCTION)", fill=(240, 245, 255), font=f_title)
    draw.text((70, 180), "CONTROLLED REMOVAL OF SURROUNDING BASALT WHILE PRESERVING STRUCTURAL ROUTE", fill=(195, 150, 75), font=f_h2)
    
    stages = [
        ("STAGE 1: TOP TRENCHING", "Sink outer perimeter trenches from cliff rim; isolate central raw monolith core.", (75, 165, 245)),
        ("STAGE 2: FLANK CHANNELING", "Chisel side channels along bridge corridor leaving horizontal rock strip intact.", (240, 200, 90)),
        ("STAGE 3: UNDERBELLY UNDERCUT", "Controlled undercutting of basalt beneath the span opening the courtyard void.", (230, 100, 60)),
        ("STAGE 4: FINE DRESSING", "Sculpt ornamental moldings, balustrades, and lower plinth details.", (140, 220, 140))
    ]
    
    box_w = 410
    for i, (title, desc, col) in enumerate(stages):
        bx = 70 + i * (box_w + 35)
        by = 250
        draw.rectangle([bx, by, bx + box_w, by + 530], outline=col, width=2, fill=(18, 24, 34))
        draw.rectangle([bx, by, bx + box_w, by + 65], fill=(28, 36, 50))
        draw.text((bx + 15, by + 18), title, fill=col, font=f_h2)
        
        # Diagram representing each stage
        dx = bx + box_w // 2
        dy = by + 230
        
        # Raw bedrock outline
        draw.rectangle([dx - 160, dy - 100, dx + 160, dy + 100], outline=(60, 75, 95), fill=(22, 28, 38))
        
        if i == 0:
            # Trench cuts on sides
            draw.rectangle([dx - 160, dy - 100, dx - 100, dy + 30], fill=(12, 16, 22), outline=(180, 90, 40))
            draw.rectangle([dx + 100, dy - 100, dx + 160, dy + 30], fill=(12, 16, 22), outline=(180, 90, 40))
            draw.text((dx - 80, dy - 20), "SOLID CORE", fill=(180, 195, 215), font=f_body)
        elif i == 1:
            # Side channels leaving bridge strip
            draw.rectangle([dx - 160, dy - 100, dx - 70, dy + 60], fill=(12, 16, 22), outline=(180, 90, 40))
            draw.rectangle([dx + 70, dy - 100, dx + 160, dy + 60], fill=(12, 16, 22), outline=(180, 90, 40))
            draw.rectangle([dx - 70, dy - 100, dx + 70, dy - 40], fill=(45, 60, 85), outline=(240, 200, 90), width=2)
            draw.text((dx - 55, dy - 80), "BRIDGE STRIP", fill=(240, 200, 90), font=f_body)
        elif i == 2:
            # Undercutting void beneath
            draw.rectangle([dx - 160, dy - 100, dx + 160, dy + 80], fill=(12, 16, 22))
            # Preserved bridge
            draw.rectangle([dx - 90, dy - 100, dx + 90, dy - 40], fill=(45, 60, 85), outline=(240, 200, 90), width=2)
            # Retained end walls
            draw.rectangle([dx - 160, dy - 100, dx - 90, dy + 80], fill=(30, 40, 55))
            draw.rectangle([dx + 90, dy - 100, dx + 160, dy + 80], fill=(30, 40, 55))
            draw.text((dx - 65, dy + 10), "VOID EXPANDING", fill=(230, 100, 60), font=f_body)
        elif i == 3:
            # Fully sculpted bridge and courtyard
            draw.rectangle([dx - 160, dy - 100, dx + 160, dy + 100], fill=(12, 16, 22))
            draw.rectangle([dx - 90, dy - 90, dx + 90, dy - 40], fill=(55, 75, 105), outline=(140, 220, 140), width=2)
            draw.rectangle([dx - 160, dy - 100, dx - 90, dy + 100], fill=(35, 48, 65))
            draw.rectangle([dx + 90, dy - 100, dx + 160, dy + 100], fill=(35, 48, 65))
            draw.text((dx - 70, dy - 75), "FINISHED BRIDGE", fill=(140, 220, 140), font=f_body)
            draw.text((dx - 70, dy + 50), "COURTYARD FLOOR", fill=(150, 175, 200), font=f_body)
            
        # Description
        draw.text((bx + 15, by + 400), desc, fill=(185, 200, 220), font=f_body)
        
    # Bottom Note
    draw.rectangle([70, 820, 1850, 960], fill=(22, 28, 38), outline=(60, 80, 110))
    draw.text((100, 845), "ARCHAEOLOGICAL NOTE // INTERPRETIVE RECONSTRUCTION", fill=(195, 150, 75), font=f_h2)
    draw.text((100, 885), "No 8th-century builder logbook survives. This diagram represents a logical engineering sequence based on preserved chisel horizons and architectural continuity, not an eyewitness historical record.", fill=(200, 215, 230), font=f_body)
    
    out = IMAGES_DIR / "ep04_infographic_03_staged_subtraction_reconstruction.jpg"
    img.save(out, quality=95)
    print(f"Generated: {out.name}")

def make_card_04_southern_span_lost_route():
    img, draw = create_base_canvas(subhead="THE COLLAPSED SOUTHERN CONNECTION")
    f_title = get_font_bold(40)
    f_h2 = get_font_bold(24)
    f_body = get_font(20)
    f_num = get_font_bold(40)
    
    draw.text((70, 125), "THE MISSING SOUTHERN BRIDGE", fill=(240, 245, 255), font=f_title)
    draw.text((70, 180), "FORENSIC SITE PLAN: SURVIVING SPANS VS COLLAPSED CLIFF CONNECTION", fill=(195, 150, 75), font=f_h2)
    
    cx, cy = 960, 500
    # Courtyard boundary
    draw.rectangle([cx - 500, cy - 200, cx + 500, cy + 240], outline=(150, 90, 40), width=2, fill=(16, 20, 28))
    
    # Northern Cliff Wall
    draw.rectangle([cx - 500, cy - 200, cx + 500, cy - 140], fill=(25, 32, 42))
    draw.text((cx - 140, cy - 180), "NORTHERN CLIFF SCARP", fill=(130, 150, 180), font=f_body)
    
    # Southern Cliff Wall (Where the span reached)
    draw.rectangle([cx - 500, cy + 180, cx + 500, cy + 240], fill=(25, 32, 42))
    draw.text((cx - 140, cy + 205), "SOUTHERN CLIFF SCARP (GALLERIES)", fill=(130, 150, 180), font=f_body)
    
    # Maha Mandapa (Central Assembly Hall)
    draw.rectangle([cx - 120, cy - 80, cx + 240, cy + 120], outline=(75, 165, 245), width=3, fill=(28, 38, 52))
    draw.text((cx - 30, cy + 10), "MAHA MANDAPA\n(MAIN HALL)", fill=(255, 255, 255), font=f_h2)
    
    # Nandi Mandapa & Surviving Bridge
    draw.rectangle([cx - 360, cy - 50, cx - 220, cy + 90], outline=(75, 165, 245), width=3, fill=(28, 38, 52))
    draw.text((cx - 330, cy + 10), "NANDI\nMANDAPA", fill=(255, 255, 255), font=f_body)
    
    # Surviving Northern/Central Bridge
    draw.rectangle([cx - 220, cy - 10, cx - 120, cy + 40], fill=(45, 60, 85), outline=(140, 220, 140), width=3)
    draw.text((cx - 210, cy - 45), "SURVIVING BRIDGE", fill=(140, 220, 140), font=f_body)
    
    # The Lost Southern Bridge (Dashed / Warning Line)
    # Extends from Maha Mandapa south side toward Southern Scarp
    bx1, by1 = cx + 60, cy + 120
    bx2, by2 = cx + 60, cy + 180
    draw.rectangle([bx1 - 25, by1, bx1 + 25, by2], outline=(235, 80, 80), width=2, fill=(40, 20, 24))
    # Draw dashed diagonal cross representing collapse
    draw.line([(bx1 - 25, by1), (bx1 + 25, by2)], fill=(240, 100, 100), width=2)
    draw.line([(bx1 + 25, by1), (bx1 - 25, by2)], fill=(240, 100, 100), width=2)
    
    draw.text((bx1 + 45, by1 + 15), "◄── COLLAPSED SOUTHERN SPAN", fill=(240, 90, 90), font=f_h2)
    draw.text((bx1 + 45, by1 + 45), "(Fractured basalt scar survives on wall)", fill=(200, 150, 150), font=f_body)
    
    # Metric Summary Boxes
    draw.rectangle([70, 830, 580, 960], fill=(22, 28, 38), outline=(60, 80, 110))
    draw.text((95, 845), "FRACTURE SCAR", fill=(235, 90, 90), font=f_h2)
    draw.text((95, 890), "Clear physical anchorage evidence confirms the original bridge connection.", fill=(185, 200, 220), font=f_body)
    
    draw.rectangle([640, 830, 1240, 960], fill=(22, 28, 38), outline=(60, 80, 110))
    draw.text((665, 845), "UNKNOWN COLLAPSE DATE", fill=(240, 200, 90), font=f_h2)
    draw.text((665, 890), "No inscription dates the collapse. Seismic activity or weathering are likely causes.", fill=(185, 200, 220), font=f_body)
    
    draw.rectangle([1300, 830, 1850, 960], fill=(22, 28, 38), outline=(60, 80, 110))
    draw.text((1325, 845), "EVIDENCE DISCIPLINE", fill=(140, 220, 140), font=f_h2)
    draw.text((1325, 890), "Absence leaves an architectural question, not proof of lost machines.", fill=(185, 200, 220), font=f_body)
    
    out = IMAGES_DIR / "ep04_infographic_04_southern_span_lost_route.jpg"
    img.save(out, quality=95)
    print(f"Generated: {out.name}")

def make_card_05_processional_axis_sequence():
    img, draw = create_base_canvas(subhead="THE SACRED RITUAL AXIS")
    f_title = get_font_bold(40)
    f_h2 = get_font_bold(24)
    f_body = get_font(20)
    f_num = get_font_bold(38)
    
    draw.text((70, 125), "ARCHITECTURE AS PROCESSION: THE LINEAR AXIS", fill=(240, 245, 255), font=f_title)
    draw.text((70, 180), "THE BRIDGES TRANSFORM SEPARATE ROCK MASSES INTO A DIRECTED RITUAL PATH", fill=(195, 150, 75), font=f_h2)
    
    # 4 Sequential Stations with 2 Connecting Bridges
    stations = [
        ("STATION 1: GOPURAM", "Two-Storeyed Outer Gateway\n(Threshold into sacred precinct)", (75, 165, 245)),
        ("STATION 2: NANDI MANDAPA", "Sacred Bull Pavilion\n(Guardian facing the Lord)", (240, 200, 90)),
        ("STATION 3: MAHA MANDAPA", "16-Pillared Assembly Hall\n(Devotional gathering hall)", (230, 120, 60)),
        ("STATION 4: VIMANA / SANCTUM", "Towering Monolithic Spire\n(Garbhagriha Shiva Lingam)", (140, 220, 140))
    ]
    
    y = 340
    st_w = 340
    gap = 120
    
    for i, (title, sub, col) in enumerate(stations):
        x = 90 + i * (st_w + gap)
        draw.rectangle([x, y, x + st_w, y + 260], outline=col, width=3, fill=(20, 26, 36))
        draw.rectangle([x, y, x + st_w, y + 55], fill=(30, 40, 55))
        draw.text((x + 15, y + 15), title, fill=col, font=f_h2)
        draw.text((x + 15, y + 80), sub, fill=(190, 205, 225), font=f_body)
        
        # Draw connecting bridges between stations 0-1 and 1-2
        if i < 2:
            bx = x + st_w
            by = y + 110
            draw.rectangle([bx, by, bx + gap, by + 40], fill=(50, 70, 95), outline=(240, 200, 90), width=2)
            draw.text((bx + 15, by - 30), f"BRIDGE {i+1}", fill=(240, 200, 90), font=f_body)
            # Arrow
            draw.polygon([(bx + gap - 10, by + 10), (bx + gap, by + 20), (bx + gap - 10, by + 30)], fill=(240, 200, 90))
            
    # Procession direction banner
    draw.rectangle([90, 650, 1830, 730], fill=(24, 32, 44), outline=(50, 70, 95))
    draw.text((120, 675), "EASTWARD DIRECTION OF WORSHIP ───────► (THRESHOLD ──► GUARDIAN ──► ASSEMBLY ──► SANCTUARY)", fill=(240, 200, 90), font=f_h2)
    
    # Bottom Note
    draw.rectangle([70, 780, 1850, 960], fill=(22, 28, 38), outline=(60, 80, 110))
    draw.text((100, 805), "INFRASTRUCTURE AS SACRED ART", fill=(140, 220, 140), font=f_h2)
    draw.text((100, 850), "In constructed Hindu temples, these shrines stand on an elevated stone plinth. At Kailasa, the upper bridges allow the same ceremonial sequence to be walked thirty feet in the air, connecting spaces hewn from a single mountain.", fill=(200, 215, 230), font=f_body)
    
    out = IMAGES_DIR / "ep04_infographic_05_processional_axis_sequence.jpg"
    img.save(out, quality=95)
    print(f"Generated: {out.name}")

def main():
    print("=" * 65)
    print(" GENERATING EPISODE 04 TECHNICAL INFOGRAPHIC & BLUEPRINT CARDS")
    print("=" * 65)
    make_card_01_courtyard_spatial_void()
    make_card_02_continuous_stone_vs_masonry()
    make_card_03_staged_subtraction_reconstruction()
    make_card_04_southern_span_lost_route()
    make_card_05_processional_axis_sequence()
    print("\n[SUCCESS] Generated all 5 Episode 04 technical infographic cards.")

if __name__ == "__main__":
    main()
