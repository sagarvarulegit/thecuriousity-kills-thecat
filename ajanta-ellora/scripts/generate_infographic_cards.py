"""
Generate high-retention documentary technical infographic and blueprint cards
for Kailasa Episode 2 using PIL.
These cards provide visual variety, breaking up still paintings like Vox/Lemmino,
and ensuring zero repetitive visuals in the documentary.
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parent.parent
IMAGES_DIR = BASE_DIR / "assets" / "episode-02" / "images"
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

WIDTH, HEIGHT = 1920, 1080

def get_font(size):
    try:
        # Common Windows fonts
        return ImageFont.truetype("arial.ttf", size)
    except Exception:
        return ImageFont.load_default()

def get_font_bold(size):
    try:
        return ImageFont.truetype("arialbd.ttf", size)
    except Exception:
        return ImageFont.load_default()

def create_base_canvas(theme="dark_slate"):
    img = Image.new("RGB", (WIDTH, HEIGHT), color=(14, 17, 23))
    draw = ImageDraw.Draw(img)
    
    # Outer cinematic border
    draw.rectangle([40, 40, WIDTH-40, HEIGHT-40], outline=(60, 75, 95), width=2)
    draw.rectangle([48, 48, WIDTH-48, HEIGHT-48], outline=(30, 40, 52), width=1)
    
    # Header branding
    f_sub = get_font(20)
    draw.text((70, 65), "KAILASA TEMPLE ARCHAEOLOGICAL & ENGINEERING DOSSIER // ELLORA CAVE 16", fill=(120, 150, 180), font=f_sub)
    draw.text((WIDTH - 380, 65), "SERIES: THE INFERNO IN THE TRENCHES", fill=(180, 140, 70), font=f_sub)
    draw.line([(70, 95), (WIDTH - 70, 95)], fill=(50, 65, 80), width=1)
    
    # Grid lines (blueprint grid)
    for x in range(100, WIDTH - 100, 150):
        draw.line([(x, 110), (x, HEIGHT - 80)], fill=(20, 26, 35), width=1)
    for y in range(120, HEIGHT - 80, 120):
        draw.line([(70, y), (WIDTH - 70, y)], fill=(20, 26, 35), width=1)
        
    return img, draw

def make_card_01_three_trenches():
    img, draw = create_base_canvas()
    f_title = get_font_bold(44)
    f_h2 = get_font_bold(28)
    f_body = get_font(22)
    f_num = get_font_bold(56)
    
    draw.text((70, 130), "THE THREE PERIMETER TRENCHES", fill=(240, 245, 255), font=f_title)
    draw.text((70, 185), "TOP-DOWN MONOLITHIC EXCAVATION SPECIFICATION (756 CE)", fill=(190, 150, 80), font=f_h2)
    
    # Visual diagram: Central Island & 3 Trenches
    cx, cy = 960, 560
    # Trench outer box
    draw.rectangle([cx - 400, cy - 250, cx + 400, cy + 250], outline=(180, 120, 50), width=3, fill=(18, 22, 30))
    # Monolith core
    draw.rectangle([cx - 260, cy - 250, cx + 260, cy + 180], outline=(70, 160, 240), width=4, fill=(28, 36, 48))
    
    # Labels inside diagram
    draw.text((cx - 150, cy - 40), "CENTRAL ROCK MONOLITH", fill=(255, 255, 255), font=f_h2)
    draw.text((cx - 120, cy + 5), "(TEMPLE TO BE CARVED HERE)", fill=(140, 180, 220), font=f_body)
    
    # Trench dimensions
    draw.text((cx - 380, cy - 10), "NORTH TRENCH\n(90 METERS)", fill=(220, 140, 60), font=f_body)
    draw.text((cx + 280, cy - 10), "SOUTH TRENCH\n(90 METERS)", fill=(220, 140, 60), font=f_body)
    draw.text((cx - 110, cy + 200), "REAR CLIFF SCARP (50 METERS DEEP)", fill=(220, 140, 60), font=f_body)
    
    # Metric Callout Boxes
    draw.rectangle([100, 860, 480, 980], fill=(22, 28, 38), outline=(60, 80, 110))
    draw.text((120, 875), "VERTICAL DEPTH", fill=(140, 160, 180), font=f_body)
    draw.text((120, 905), "33 METERS", fill=(255, 180, 70), font=f_num)
    draw.text((120, 955), "Over 100 vertical feet sheer drop", fill=(100, 120, 140), font=get_font(16))
    
    draw.rectangle([520, 860, 900, 980], fill=(22, 28, 38), outline=(60, 80, 110))
    draw.text((540, 875), "COURTYARD SPAN", fill=(140, 160, 180), font=f_body)
    draw.text((540, 905), "47 METERS", fill=(70, 190, 255), font=f_num)
    draw.text((540, 955), "Surrounding trench width buffer", fill=(100, 120, 140), font=get_font(16))
    
    draw.rectangle([940, 860, 1380, 980], fill=(22, 28, 38), outline=(60, 80, 110))
    draw.text((960, 875), "INITIAL TRENCH DEBRIS", fill=(140, 160, 180), font=f_body)
    draw.text((960, 905), "100,000 TONS", fill=(255, 110, 90), font=f_num)
    draw.text((960, 955), "Extracted before temple sculpting began", fill=(100, 120, 140), font=get_font(16))
    
    draw.rectangle([1420, 860, 1820, 980], fill=(22, 28, 38), outline=(60, 80, 110))
    draw.text((1440, 875), "MANPOWER DEPLOYED", fill=(140, 160, 180), font=f_body)
    draw.text((1440, 905), "10,000 MEN", fill=(120, 230, 160), font=f_num)
    draw.text((1440, 955), "Quarrymen, woodcutters & haulers", fill=(100, 120, 140), font=get_font(16))
    
    out = IMAGES_DIR / "ep02_infographic_01_three_trenches.jpg"
    img.save(out, quality=95)
    print(f"Generated {out.name}")

def make_card_02_basalt_strength():
    img, draw = create_base_canvas()
    f_title = get_font_bold(44)
    f_h2 = get_font_bold(28)
    f_body = get_font(22)
    f_num = get_font_bold(54)
    
    draw.text((70, 130), "MATERIAL SCIENCE: BASALT vs. CHISEL STEEL", fill=(240, 245, 255), font=f_title)
    draw.text((70, 185), "COMPRESSIVE STRENGTH & HARDNESS COMPARISON AT ELLORA", fill=(190, 150, 80), font=f_h2)
    
    # Comparison Bar Chart
    bars = [
        ("DECCAN THOLEIITIC BASALT", 140, (255, 90, 70), "140 MPa Compressive Strength // Ultra-Dense Plagioclase Matrix"),
        ("ANCIENT WOOTZ CHISEL TIP", 75, (70, 180, 255), "75 MPa Effective Shear Limit // Rapid Mushrooming on Cold Rock"),
        ("STANDARD ANCIENT IRON CHISEL", 40, (180, 190, 200), "40 MPa // Fractured or Blunted within 3 to 5 Hammer Strikes"),
        ("STANDARD GRANITE", 100, (140, 140, 170), "100 MPa Reference // Basalt is 40% denser and more abrasive")
    ]
    
    y = 280
    for name, val, col, desc in bars:
        draw.text((120, y), name, fill=(240, 240, 240), font=f_h2)
        # Bar width
        bw = int((val / 150.0) * 850)
        draw.rectangle([120, y + 40, 120 + bw, y + 75], fill=col)
        draw.rectangle([120 + bw, y + 40, 120 + 850, y + 75], fill=(30, 36, 46))
        draw.text((150 + bw, y + 42), f"{val} MPa", fill=col, font=get_font_bold(24))
        draw.text((120, y + 85), desc, fill=(130, 150, 170), font=f_body)
        y += 135
        
    # Technical Conclusion box on right
    draw.rectangle([1180, 280, 1820, 800], fill=(22, 28, 38), outline=(200, 100, 60), width=2)
    draw.text((1210, 310), "THE MECHANICAL IMPASSE", fill=(255, 120, 80), font=f_h2)
    txt = (
        "Cold chiseling at Ellora required over\n"
        "100 chisel strikes to displace a single\n"
        "cubic inch of basalt.\n\n"
        "At this rate, excavating 400,000 tons\n"
        "would have taken 120+ years and exhausted\n"
        "the Rashtrakuta kingdom's entire iron\n"
        "and steel supply.\n\n"
        "A thermodynamic breakthrough was\n"
        "mandatory: AGNI-KARMA (Thermal Shock)."
    )
    draw.text((1210, 370), txt, fill=(210, 220, 230), font=f_body, spacing=8)
    
    out = IMAGES_DIR / "ep02_infographic_02_basalt_strength.jpg"
    img.save(out, quality=95)
    print(f"Generated {out.name}")

def make_card_03_thermal_shock():
    img, draw = create_base_canvas()
    f_title = get_font_bold(44)
    f_h2 = get_font_bold(28)
    f_body = get_font(22)
    f_num = get_font_bold(52)
    
    draw.text((70, 130), "AGNI-KARMA: THE SCIENCE OF THERMAL SHOCK", fill=(240, 245, 255), font=f_title)
    draw.text((70, 185), "ANCIENT VEDIC PYRO-ENGINEERING (RECORDED IN SHILPA SHASTRAS)", fill=(255, 140, 50), font=f_h2)
    
    # 3-Step Process Cards
    steps = [
        ("PHASE 1: HEATING", "600°C - 800°C", (255, 90, 40), 
         "Acacia and Tamarind bonfires stacked\ndirectly against trench bedrock.\nDifferential mineral expansion forces\nintense internal compressive stress."),
        ("PHASE 2: QUENCHING", "ΔT = 575°C", (70, 190, 255), 
         "Tens of thousands of gallons of cold water\ndashed onto glowing bedrock.\nFlash evaporation causes explosive surface\ncontraction while core remains expanded."),
        ("PHASE 3: SHATTERING", "90% LESS FORCE", (120, 230, 140), 
         "Micro-fracture web propagates across basalt.\nStone cleaves into brittle flakes\nand crumbly 2-ton slabs, easily levered\nwith wooden pry-bars in minutes.")
    ]
    
    x = 100
    for title, metric, col, text in steps:
        draw.rectangle([x, 280, x + 530, 780], fill=(20, 26, 36), outline=col, width=2)
        draw.rectangle([x, 280, x + 530, 350], fill=(30, 38, 50))
        draw.text((x + 25, 300), title, fill=(255, 255, 255), font=f_h2)
        draw.text((x + 25, 380), metric, fill=col, font=f_num)
        draw.line([(x + 25, 460), (x + 505, 460)], fill=(50, 65, 80), width=1)
        draw.text((x + 25, 490), text, fill=(210, 220, 235), font=f_body, spacing=10)
        x += 580
        
    out = IMAGES_DIR / "ep02_infographic_03_thermal_shock.jpg"
    img.save(out, quality=95)
    print(f"Generated {out.name}")

def make_card_04_gravity_engine():
    img, draw = create_base_canvas()
    f_title = get_font_bold(44)
    f_h2 = get_font_bold(28)
    f_body = get_font(22)
    f_num = get_font_bold(52)
    
    draw.text((70, 130), "GRAVITY AS AN ENGINE: DEBRIS CLEARANCE", fill=(240, 245, 255), font=f_title)
    draw.text((70, 185), "HOW 400,000 TONS OF ROCK WERE REMOVED WITHOUT CRANES", fill=(120, 210, 160), font=f_h2)
    
    # Comparison: Kailasa vs Great Pyramid
    draw.rectangle([100, 270, 920, 780], fill=(20, 25, 35), outline=(70, 170, 240), width=2)
    draw.text((130, 300), "THE KAILASA LOGISTIC ADVANTAGE", fill=(70, 190, 255), font=f_h2)
    adv_text = (
        "Unlike the Pyramids of Giza, where stones had to be\n"
        "hauled UPWARD against gravity,\n"
        "Kailasa Temple was excavated TOP-DOWN.\n\n"
        "• Gravity worked WITH the builders.\n"
        "• Greased timber chutes carried 2-ton basalt slabs\n"
        "  downhill into the valley at zero muscle expenditure.\n"
        "• 100,000 tons cleared in the first trenching phase\n"
        "  alone, completely clearing the temple courtyard."
    )
    draw.text((130, 370), adv_text, fill=(210, 225, 240), font=f_body, spacing=10)
    
    draw.rectangle([980, 270, 1820, 780], fill=(20, 25, 35), outline=(240, 150, 70), width=2)
    draw.text((1010, 300), "WHERE DID 400,000 TONS GO?", fill=(255, 170, 80), font=f_h2)
    dest_text = (
        "The mystery of missing Ellora debris solved:\n\n"
        "1. Valley Agricultural Terraces: Basalt gravel leveled\n"
        "   into fertile step-terraces for local crops.\n\n"
        "2. Ellora Fortifications & Roads: Paved royal highways\n"
        "   connecting Ellora to the Rashtrakuta capital Manyakheta.\n\n"
        "3. Water Reservoirs & Dams: Crushed basalt packed\n"
        "   into earthen bunds, creating permanent monsoon lakes."
    )
    draw.text((1010, 370), dest_text, fill=(210, 225, 240), font=f_body, spacing=8)
    
    out = IMAGES_DIR / "ep02_infographic_04_gravity_engine.jpg"
    img.save(out, quality=95)
    print(f"Generated {out.name}")

def make_card_05_monolith_dimensions():
    img, draw = create_base_canvas()
    f_title = get_font_bold(44)
    f_h2 = get_font_bold(28)
    f_body = get_font(22)
    f_num = get_font_bold(52)
    
    draw.text((70, 130), "THE MONOLITHIC ISLAND: FINAL EXCAVATION STATE", fill=(240, 245, 255), font=f_title)
    draw.text((70, 185), "ACT 8 CLIMAX: A FREE-STANDING STONE MOUNTAIN (THE PREPARATION FOR CARVING)", fill=(255, 200, 70), font=f_h2)
    
    # 4 Key Dimension Cards
    dims = [
        ("LENGTH", "60 METERS", "200 Feet Long", (70, 180, 255)),
        ("WIDTH", "30 METERS", "100 Feet Wide", (120, 230, 150)),
        ("HEIGHT", "33 METERS", "107 Feet Tall", (255, 170, 60)),
        ("MASS ISOLATED", "200,000 TONS", "Raw Intact Block", (255, 100, 90))
    ]
    
    x = 100
    for label, val, sub, col in dims:
        draw.rectangle([x, 300, x + 390, 520], fill=(20, 26, 36), outline=col, width=2)
        draw.text((x + 25, 325), label, fill=(150, 170, 190), font=f_body)
        draw.text((x + 25, 375), val, fill=col, font=f_num)
        draw.text((x + 25, 455), sub, fill=(220, 230, 240), font=f_h2)
        x += 440
        
    draw.rectangle([100, 570, 1820, 800], fill=(25, 32, 45), outline=(100, 140, 190), width=1)
    draw.text((140, 600), "THE ARCHITECT'S NEXT IMPOSSIBLE CHALLENGE (EPISODE 3 PREVIEW)", fill=(255, 215, 0), font=f_h2)
    c_text = (
        "With the three perimeter trenches cleared and 100,000 tons of rock removed,\n"
        "Kokasa achieved what every other royal architect called impossible:\n"
        "A freestanding, 100-foot monolith completely separated from the mountain.\n\n"
        "Now, with zero scaffolding from the ground and zero margin for error, carving will begin...\n"
        "FROM THE TOP OF THE SPIRE DOWNWARD."
    )
    draw.text((140, 650), c_text, fill=(210, 230, 250), font=f_body, spacing=6)
    
    out = IMAGES_DIR / "ep02_infographic_05_monolith_dimensions.jpg"
    img.save(out, quality=95)
    print(f"Generated {out.name}")

def main():
    print("Generating Documentary Infographic Cards for Episode 2...")
    make_card_01_three_trenches()
    make_card_02_basalt_strength()
    make_card_03_thermal_shock()
    make_card_04_gravity_engine()
    make_card_05_monolith_dimensions()
    print("All 5 Documentary Infographic Cards generated successfully!")

if __name__ == "__main__":
    main()
