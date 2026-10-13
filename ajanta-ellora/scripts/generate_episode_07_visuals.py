#!/usr/bin/env python3
"""
generate_episode_07_visuals.py — Visual Asset & Google Flow Action Stills Generator (Episode 07)
Generates:
1. 8 Google Flow Kinetic Action Candidate Stills (_GENERATE_VIDEO) isolated into google_flow_input_images/
2. 2 Broadcast-grade PIL Architectural Infographics (Law 9 strictly compliant)
3. Master cinematic 16:9 stills (_PAN_ZOOM)
4. Master 16:9 YouTube Thumbnail & 2 Companion Shorts 9:16 Vertical Thumbnails
5. Google Flow copy-paste prompt sheet: GOOGLE_FLOW_PROMPT_SHEET.md
"""

import os
import sys
import time
import shutil
from pathlib import Path
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont
from google import genai

# Fix Windows console UTF-8 encoding
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

load_dotenv()

WORKSPACE_ROOT = Path("C:/Sagar/Projects/thecuriousity-kills-thecat")
EP07_DIR = WORKSPACE_ROOT / "ajanta-ellora" / "episode07"
IMAGES_DIR = EP07_DIR / "images"
GOOGLE_FLOW_INPUT = EP07_DIR / "google_flow_input_images"
THUMBNAIL_DIR = EP07_DIR / "thumbnail"

IMAGES_DIR.mkdir(parents=True, exist_ok=True)
GOOGLE_FLOW_INPUT.mkdir(parents=True, exist_ok=True)
THUMBNAIL_DIR.mkdir(parents=True, exist_ok=True)

CLIENT = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-2.5-flash-image"

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

# ==============================================================================
# 1. PIL TECHNICAL INFOGRAPHICS GENERATION (LAW 9 STRICT COMPLIANCE: 2 CARDS)
# ==============================================================================

def generate_infographic_01_map():
    """Generates ep07_infographic_01_deccan_map_geology.jpg"""
    out_path = IMAGES_DIR / "ep07_infographic_01_deccan_map_geology.jpg"
    img = Image.new("RGB", (WIDTH, HEIGHT), color=(10, 15, 22))
    draw = ImageDraw.Draw(img)
    
    # Border & grid
    draw.rectangle([40, 40, WIDTH-40, HEIGHT-40], outline=(55, 75, 95), width=2)
    draw.rectangle([48, 48, WIDTH-48, HEIGHT-48], outline=(25, 35, 45), width=1)
    
    # Header
    draw.text((70, 65), "DECCAN VOLCANIC CORRIDOR // GEOLOGICAL & EPIGRAPHIC CARTOGRAPHY", fill=(120, 160, 200), font=get_font(20))
    draw.text((WIDTH - 550, 65), "EPISODE 07: THE WAGHUR HORSESHOE CANYON", fill=(210, 160, 80), font=get_font(20))
    draw.line([(70, 95), (WIDTH - 70, 95)], fill=(45, 60, 75), width=1)
    
    # Sub-header Title
    draw.text((70, 120), "REGIONAL VECTOR: ELLORA (CAVE 16) TO AJANTA (WAGHUR GORGE)", fill=(255, 255, 255), font=get_font_bold(32))
    draw.text((70, 165), "Distance: 100 km North-East | Geological Bed: Cretaceous Continental Flood Basalt (Deccan Traps, ~66 Ma)", fill=(170, 185, 200), font=get_font(18))
    
    # Map schematic panel
    draw.rectangle([70, 210, 1100, 980], outline=(40, 60, 80), fill=(14, 20, 28), width=2)
    
    # Grid lines inside map
    for x in range(120, 1050, 100):
        draw.line([(x, 220), (x, 970)], fill=(20, 30, 40), width=1)
    for y in range(250, 950, 100):
        draw.line([(80, y), (1090, y)], fill=(20, 30, 40), width=1)
        
    # Draw geographical features
    # Sahyadri Escarpment Ridge
    draw.line([(150, 850), (350, 600), (600, 450), (900, 300)], fill=(80, 100, 120), width=6)
    draw.text((250, 750), "SAHYADRI ESCARPMENT (CHARANANDRI RIDGE)", fill=(100, 125, 150), font=get_font(16))
    
    # Ellora node
    draw.ellipse([230, 780, 270, 820], fill=(210, 80, 60), outline=(255, 120, 100), width=3)
    draw.text((290, 785), "ELLORA (ELAPURA)\nCave 16 Kailasa (756-773 CE)\nFreestanding Basalt Monolith", fill=(255, 220, 180), font=get_font_bold(18))
    
    # Vector Arrow
    draw.line([(270, 780), (830, 360)], fill=(210, 160, 80), width=3)
    draw.text((480, 530), "100 KM NORTH-EAST\n700-Year Architectural Precedent", fill=(240, 200, 100), font=get_font_bold(18))
    
    # Ajanta node
    draw.ellipse([820, 330, 860, 370], fill=(60, 160, 210), outline=(120, 210, 255), width=3)
    draw.text((880, 330), "AJANTA (WAGHUR CANYON)\n30 Rock-Cut Caves (200 BCE - 480 CE)\nHorseshoe Amphitheater Scarp", fill=(180, 230, 255), font=get_font_bold(18))
    
    # Waghur River curve
    draw.arc([800, 280, 950, 420], start=110, end=340, fill=(40, 140, 200), width=4)
    draw.text((890, 410), "Waghur River Curve (~75m Deep Chasm)", fill=(70, 160, 210), font=get_font(15))
    
    # Right Data Panel
    draw.rectangle([1140, 210, WIDTH-70, 980], outline=(40, 60, 80), fill=(14, 20, 28), width=2)
    draw.text((1170, 240), "STRATIGRAPHIC COMPARISON", fill=(210, 160, 80), font=get_font_bold(22))
    
    stats = [
        ("Feature", "Ajanta Caves", "Ellora (Kailasa)"),
        ("Terrain", "Curved Horseshoe Gorge", "Linear Plateau Scarp"),
        ("Basalt Type", "Dense Microcrystalline", "Tholeiitic Flood Sheets"),
        ("Drop Depth", "75 Meters Vertical", "33 Meters Trench"),
        ("Chronology", "200 BCE – 480 CE", "756 CE – 812 CE"),
        ("Excavation", "Subterranean Chaityas", "Freestanding Monolith"),
        ("Water Mgmt", "Podhi Cistern Relays", "Perimeter Scarp Gutters"),
        ("Discovery", "Lost 1,300 Yrs (1819)", "Never Lost to Memory")
    ]
    
    y_pos = 300
    for i, (col1, col2, col3) in enumerate(stats):
        f_use = get_font_bold(16) if i == 0 else get_font(16)
        color_head = (255, 255, 255) if i == 0 else (170, 190, 210)
        draw.text((1170, y_pos), col1, fill=color_head, font=f_use)
        draw.text((1350, y_pos), col2, fill=(120, 200, 240) if i > 0 else color_head, font=f_use)
        draw.text((1570, y_pos), col3, fill=(240, 180, 120) if i > 0 else color_head, font=f_use)
        draw.line([(1170, y_pos + 26), (WIDTH - 90, y_pos + 26)], fill=(25, 38, 52), width=1)
        y_pos += 45
        
    draw.text((1170, 710), "KEY INSIGHT:", fill=(210, 160, 80), font=get_font_bold(18))
    draw.text((1170, 740), "The top-down subtractive carving technique,\ninward column earthquake bracing, and\nmonolithic water cisterns were engineered at\nAjanta over 7 centuries before Kailasa.", fill=(200, 215, 230), font=get_font(16))
    
    img.save(out_path, quality=95)
    print(f"[OK] Generated Infographic 01: {out_path.name}")
    return out_path

def generate_infographic_02_hydrology():
    """Generates ep07_infographic_02_hydraulic_drainage_cutaway.jpg"""
    out_path = IMAGES_DIR / "ep07_infographic_02_hydraulic_drainage_cutaway.jpg"
    img = Image.new("RGB", (WIDTH, HEIGHT), color=(10, 15, 22))
    draw = ImageDraw.Draw(img)
    
    # Border & grid
    draw.rectangle([40, 40, WIDTH-40, HEIGHT-40], outline=(55, 75, 95), width=2)
    draw.rectangle([48, 48, WIDTH-48, HEIGHT-48], outline=(25, 35, 45), width=1)
    
    # Header
    draw.text((70, 65), "SUBTERRANEAN HYDRAULICS // MONSOON DIVERSION & FILTRATION ARSENAL", fill=(120, 160, 200), font=get_font(20))
    draw.text((WIDTH - 550, 65), "AJANTA CLIFF ENGINEERING // CAVE 10 SECTION", fill=(210, 160, 80), font=get_font(20))
    draw.line([(70, 95), (WIDTH - 70, 95)], fill=(45, 60, 75), width=1)
    
    # Sub-header Title
    draw.text((70, 120), "MONSOON DEFENSE ELEVATION: PLATEAU RUNOFF REDIRECTION & PODHI FILTRATION", fill=(255, 255, 255), font=get_font_bold(30))
    draw.text((70, 165), "Dual-Hazard Mitigation: Preventing Sheet-Flood Erosion while Securing Year-Round Sterile Drinking Water", fill=(170, 185, 200), font=get_font(18))
    
    # Diagram Schematic Box
    draw.rectangle([70, 210, WIDTH-70, 980], outline=(40, 60, 80), fill=(14, 20, 28), width=2)
    
    # Plateau Surface
    draw.polygon([(100, 320), (500, 320), (500, 360), (100, 360)], fill=(40, 50, 60))
    draw.text((120, 280), "UPPER DECCAN PLATEAU BEDROCK (DATUM +75m)", fill=(210, 160, 80), font=get_font_bold(18))
    
    # Torrential rain arrows
    for x in range(150, 480, 50):
        draw.line([(x, 230), (x, 310)], fill=(70, 150, 230), width=2)
        draw.polygon([(x-4, 305), (x+4, 305), (x, 318)], fill=(70, 150, 230))
    draw.text((200, 240), "HEAVY MONSOON TORRENTIAL DOWNPOUR", fill=(140, 200, 255), font=get_font(15))
    
    # Chiseled Gutters
    draw.rectangle([480, 300, 540, 340], fill=(20, 100, 180), outline=(60, 160, 240), width=2)
    draw.text((560, 305), "ROCK-CUT DIVERSION GUTTER (0.8m deep)\nRoutes 85% of surface runoff to side ravines", fill=(120, 210, 255), font=get_font_bold(16))
    
    # Vertical Basalt Cliff Face
    draw.line([(540, 340), (620, 480), (620, 880)], fill=(70, 85, 100), width=8)
    draw.text((640, 420), "VERTICAL BASALT CLIFF DROP (~75 METERS)", fill=(150, 170, 190), font=get_font(16))
    
    # Overhanging drip-ledge
    draw.polygon([(600, 480), (660, 510), (620, 520)], fill=(90, 110, 130))
    draw.text((680, 500), "CANTILEVERED DRIP-LEDGE: Forces runoff to arc past cave facade", fill=(240, 190, 100), font=get_font_bold(16))
    
    # Cave 10 Chaitya Hall Interior Cutaway
    draw.rectangle([620, 530, 1250, 880], fill=(22, 28, 38), outline=(60, 80, 105), width=2)
    draw.arc([620, 530, 820, 730], start=180, end=360, fill=(180, 150, 80), width=3)
    draw.text((650, 560), "HORSESHOE SUN-WINDOW\n& VAULTED CHAITYA NAVE", fill=(255, 230, 170), font=get_font_bold(16))
    
    # Stupa in cave
    draw.arc([1050, 700, 1170, 880], start=180, end=360, fill=(140, 160, 180), width=4)
    draw.text((1060, 760), "MONOLITHIC\nSTUPA", fill=(180, 200, 220), font=get_font(14))
    
    # Natural Basalt Joints / Water Seepage
    for y in range(400, 800, 60):
        draw.line([(450, y), (600, y + 40)], fill=(50, 130, 200), width=2)
    draw.text((220, 580), "NATURAL COOLING JOINTS\nSlow vertical water percolation\nNatural basalt micro-filtration", fill=(100, 180, 240), font=get_font(15))
    
    # Subterranean Podhi Cistern Box
    draw.rectangle([620, 890, 950, 960], fill=(15, 60, 110), outline=(40, 140, 220), width=2)
    draw.text((640, 905), "ROCK-CUT PODHI RESERVOIR (SUBTERRANEAN)", fill=(180, 230, 255), font=get_font_bold(16))
    draw.text((640, 930), "Capacity: 40,000 - 80,000 Liters | Temperature: 18-20°C Constant", fill=(130, 190, 240), font=get_font(14))
    
    # Waghur River Base
    draw.rectangle([1300, 880, WIDTH-100, 960], fill=(10, 45, 75), outline=(20, 90, 150), width=2)
    draw.text((1340, 915), "WAGHUR RIVER BED (DATUM 0.0m)", fill=(100, 180, 230), font=get_font_bold(18))
    
    img.save(out_path, quality=95)
    print(f"[OK] Generated Infographic 02: {out_path.name}")
    return out_path

# ==============================================================================
# 2. GOOGLE FLOW KINETIC ACTION SHOTS & MASTER STILLS PROMPTS
# ==============================================================================

ACTION_SHOTS = [
    {
        "id": "ep07_gf_01",
        "filename": "ep07_gf_01_fpv_canyon_reveal_GENERATE_VIDEO.jpg",
        "spoken_line": "the Waghur River carved a jagged, horseshoe-shaped canyon seventy-five meters deep...",
        "motion_prompt": "FPV drone swooping rapidly down over the sun-drenched Deccan plateau, suddenly plunging over the sheer vertical basalt edge into the mist-veiled, lush green Waghur river horseshoe gorge. Sunlight breaks across the crescent cliff face revealing carved dark cave portals.",
        "camera_movement": "High-speed forward descent transitioning to sweeping slow orbit",
        "duration": "5.5s"
    },
    {
        "id": "ep07_gf_02",
        "filename": "ep07_gf_02_satavahana_monks_cliff_path_GENERATE_VIDEO.jpg",
        "spoken_line": "A band of Buddhist monks and wandering ascetics walked along the trade artery...",
        "motion_prompt": "A line of saffron-robed Buddhist monks walking along a perilous, narrow rock-cut goat trail carved into the sheer vertical basalt cliff high above the rushing Waghur river at dawn. Long walking staffs strike stone; morning mist swirls around their feet.",
        "camera_movement": "Low-angle steady tracking shot following footsteps",
        "duration": "5.5s"
    },
    {
        "id": "ep07_gf_03",
        "filename": "ep07_gf_03_topdown_roofline_excavation_GENERATE_VIDEO.jpg",
        "spoken_line": "early masons entered the cliff at the roofline, establishing the very subtractive top-down technique...",
        "motion_prompt": "Ancient Indian stonemasons chiseled into the rock at the uppermost roofline of Cave 10. Workers in loincloths strike heavy iron pointed picks into dark columnar basalt, chipping away rock benches while orange sparks fly in the raking morning sun.",
        "camera_movement": "Slow push-in over the shoulders of stonecutters",
        "duration": "5.0s"
    },
    {
        "id": "ep07_gf_04",
        "filename": "ep07_gf_04_vaulted_chaitya_ribbing_macro_GENERATE_VIDEO.jpg",
        "spoken_line": "carving soaring vaulted ceilings that mimicked the curved timber rafters...",
        "motion_prompt": "Macro slow-motion tilt along the curved rock ceiling of the early chaitya hall. The chiseled imitation wooden ribs curve overhead in perfect geometry. Dust motes drift through ambient god-rays beaming through the horseshoe arched sun-window.",
        "camera_movement": "Slow cinematic upward tilt with shallow depth of field",
        "duration": "5.0s"
    },
    {
        "id": "ep07_gf_05",
        "filename": "ep07_gf_05_monsoon_plateau_gutter_sheet_GENERATE_VIDEO.jpg",
        "spoken_line": "stonecutters chiseled deep continuous drainage gutters directly into the surface bedrock.",
        "motion_prompt": "A torrential monsoon storm over the Sahyadri plateau. Torrents of rushing rainwater flow rapidly down a wide, rock-cut basalt gutter chiseled above the cave facade, bypassing the portal below and cascading into the canyon like a roaring waterfall.",
        "camera_movement": "Dynamic tracking alongside fast rushing water",
        "duration": "5.5s"
    },
    {
        "id": "ep07_gf_06",
        "filename": "ep07_gf_06_podhi_cistern_water_filtration_GENERATE_VIDEO.jpg",
        "spoken_line": "The water collected in these dark, cold reservoirs, remaining crystal clear...",
        "motion_prompt": "A torchlit subterranean chamber inside a rock-cut podhi cistern. Cool, crystal-clear water slowly drips from an overhead basalt ceiling joint, sending expanding concentric ripples across the mirrored surface of the dark rock pool.",
        "camera_movement": "Macro slow-motion descending crane toward water",
        "duration": "5.0s"
    },
    {
        "id": "ep07_gf_07",
        "filename": "ep07_gf_07_monk_chanting_acoustic_resonance_GENERATE_VIDEO.jpg",
        "spoken_line": "The sound did not merely echo; it vibrated physically through the stone floor and columns...",
        "motion_prompt": "A solitary Buddhist monk sitting in full lotus posture before the monolithic stone stupa inside the darkened Cave 9 chaitya. His mouth moves in resonant deep chanting. The stone floor and octagonal pillars faintly shudder as amber lamp light trembles.",
        "camera_movement": "Slow creeping push-in from wide nave to monk's face",
        "duration": "5.0s"
    },
    {
        "id": "ep07_gf_08",
        "filename": "ep07_gf_08_jungle_overgrowth_dormancy_GENERATE_VIDEO.jpg",
        "spoken_line": "For nearly four hundred uninterrupted years... Ajanta lay dormant.",
        "motion_prompt": "Time-lapse impression of dense teak jungle vines, wild bamboo, and wet silt slowly creeping over the carved stone facade and entrance steps of Cave 10. Seasons shift from dry golden scrub to torrential green monsoon, swallowing the cave entrance into shadow.",
        "camera_movement": "Slow atmospheric pull-back into darkness",
        "duration": "5.5s"
    }
]

def generate_google_flow_prompt_sheet():
    """Generates the clean GOOGLE_FLOW_PROMPT_SHEET.md for user handoff."""
    sheet_path = GOOGLE_FLOW_INPUT / "GOOGLE_FLOW_PROMPT_SHEET.md"
    lines = [
        "# Episode 07: The Secret Canyon of Waghur — Google Flow Action Video Batch Sheet",
        "## Dedicated Image-to-Video (I2V) Prompts for Google Flow / Veo / Runway",
        "",
        "> **Operational Protocol (Law 1 & 2 Gate)**:",
        "> 1. Take each input image from `ajanta-ellora/episode07/google_flow_input_images/`.",
        "> 2. Upload into Google Flow / Veo.",
        "> 3. Paste the corresponding Motion Prompt & Camera Movement.",
        "> 4. Export as 1080p Full HD MP4 and place in `ajanta-ellora/episode07/videos/`.",
        "",
        "| # | Input Image Filename | Spoken Beat / Timestamp | Subject & Camera Motion Prompt (Google Flow / Veo) | Camera Movement | Target Duration |",
        "|---|---|---|---|---|---|"
    ]
    
    for i, item in enumerate(ACTION_SHOTS, 1):
        lines.append(
            f"| **{i:02d}** | `{item['filename']}` | \"{item['spoken_line'][:45]}...\" | {item['motion_prompt']} | {item['camera_movement']} | {item['duration']} |"
        )
        
    lines.extend([
        "",
        "---",
        "### Ingestion Checklist for Assembly:",
        "- [ ] `ep07_gf_01_fpv_canyon_reveal.mp4`",
        "- [ ] `ep07_gf_02_satavahana_monks_cliff_path.mp4`",
        "- [ ] `ep07_gf_03_topdown_roofline_excavation.mp4`",
        "- [ ] `ep07_gf_04_vaulted_chaitya_ribbing_macro.mp4`",
        "- [ ] `ep07_gf_05_monsoon_plateau_gutter_sheet.mp4`",
        "- [ ] `ep07_gf_06_podhi_cistern_water_filtration.mp4`",
        "- [ ] `ep07_gf_07_monk_chanting_acoustic_resonance.mp4`",
        "- [ ] `ep07_gf_08_jungle_overgrowth_dormancy.mp4`",
        ""
    ])
    
    sheet_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"[OK] Generated Google Flow Prompt Sheet: {sheet_path.name}")
    return sheet_path

# ==============================================================================
# 3. GEMINI FLASH IMAGE GENERATOR (BASE STILLS & ACTION BASE IMAGES)
# ==============================================================================

IMAGES_TO_GENERATE = [
    # 8 Google Flow Action Candidates
    {
        "id": "GF-01",
        "filename": "ep07_gf_01_fpv_canyon_reveal_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 16:9 1080p action still. Wide aerial view looking over the dramatic horseshoe-shaped canyon of the Waghur River at dawn. A 75-meter sheer vertical basalt cliff amphitheater, emerald river curving below, ancient cave openings chiseled along the crescent cliff face, warm golden sunlight, National Geographic documentary, 8k"
    },
    {
        "id": "GF-02",
        "filename": "ep07_gf_02_satavahana_monks_cliff_path_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 16:9 1080p action still. A line of ancient Buddhist monks in saffron-ochre robes walking single-file along a precarious, narrow rock-cut path carved into a sheer 75-meter volcanic basalt cliff face. Swirling morning mist in the canyon abyss below, golden dawn light, ultra-realistic textures, 8k"
    },
    {
        "id": "GF-03",
        "filename": "ep07_gf_03_topdown_roofline_excavation_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 16:9 1080p action still. Ancient Indian stonemasons working at the uppermost roofline bench of a rock-cut cave facade. Muscular workers striking carbonized iron picks into dense dark basalt, orange sparks flying, stone dust drifting, raking morning sunbeams, authentic archaeological reconstruction, 8k"
    },
    {
        "id": "GF-04",
        "filename": "ep07_gf_04_vaulted_chaitya_ribbing_macro_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 16:9 1080p action still. Low-angle architectural view looking up at the high vaulted stone ceiling of Cave 10 chaitya. Perfectly carved imitation wooden stone ribs curving across the basalt arch, divine sunbeams streaming through the horseshoe arch sun-window, dust motes in light, 8k"
    },
    {
        "id": "GF-05",
        "filename": "ep07_gf_05_monsoon_plateau_gutter_sheet_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 16:9 1080p action still. Torrential monsoon rain on the Deccan plateau. Fast-flowing sheet runoff rushing down a continuous rock-cut drainage gutter chiseled directly into the basalt bedrock above a cave roof, water splashing in heavy sheets, atmospheric dark monsoon clouds, 8k"
    },
    {
        "id": "GF-06",
        "filename": "ep07_gf_06_podhi_cistern_water_filtration_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 16:9 1080p action still. Atmospheric subterranean chamber of a rock-cut podhi water cistern. Cool crystal-clear water pool illuminated by a warm bronze oil lamp, concentric ripples spreading across the mirror surface, dense volcanic basalt ceiling, subterranean reflection, 8k"
    },
    {
        "id": "GF-07",
        "filename": "ep07_gf_07_monk_chanting_acoustic_resonance_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 16:9 1080p action still. A solitary Buddhist monk in saffron robes meditating in full lotus posture before an austere monolithic stone stupa in the darkened nave of Cave 9. Flickering warm brass butter lamp casting deep shadows on octagonal columns, mystical spiritual atmosphere, 8k"
    },
    {
        "id": "GF-08",
        "filename": "ep07_gf_08_jungle_overgrowth_dormancy_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 16:9 1080p action still. The entrance of Cave 10 partially buried under four feet of dried river silt, tangled wild teak vines, and dense bamboo scrub. Ancient carved rock pillars peeking through wild jungle foliage, melancholic abandoned atmosphere, twilight shadows, 8k"
    },
    # Master Hero Stills
    {
        "id": "HERO-01",
        "filename": "ep07_01_kailasa_chasm_recap_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Looking upward from the deep 100-foot volcanic trench of Kailasa Temple Cave 16, towering dark basalt walls and soaring vimana spire catching morning sun, monumental scale, 8k"
    },
    {
        "id": "HERO-05",
        "filename": "ep07_05_waghur_river_curved_canyon_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Breathtaking panoramic view of the horseshoe curve of the Waghur River gorge. Lush monsoon green vegetation clinging to dark layered volcanic basalt cliffs, emerald river water winding through the canyon floor, 8k"
    },
    {
        "id": "HERO-08",
        "filename": "ep07_08_ajanta_horseshoe_grand_reveal_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Wide majestic panorama showing the entire sweeping crescent curve of all 30 cave portals carved in a continuous arc into the 75-meter vertical cliff face, dramatic morning golden hour lighting, 8k"
    },
    {
        "id": "HERO-14",
        "filename": "ep07_14_monolithic_stupa_cave_10_darkness_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Symmetrical perspective looking down the austere stone nave of Cave 10 toward the solid rock stupa dome. Octagonal columns slanting gently inward, soft diffused daylight from the entrance window, serene spiritual stillness, 8k"
    },
    {
        "id": "HERO-17",
        "filename": "ep07_17_octagonal_inward_slant_pillars_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Close architectural perspective along a row of austere octagonal stone pillars in Cave 10. Noticeable three-degree inward slant mimicking timber earthquake bracing, authentic chisel marks in dark basalt, 8k"
    },
    {
        "id": "HERO-42",
        "filename": "ep07_42_harishena_vakataka_royal_gold_fresco_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Macro detail of an ancient 5th-century Indian mural painting. Royal Vakataka emperor adorned with golden pearl crowns, necklaces, and delicate almond eyes, warm ochre and terracotta skin tones on burnished plaster ground, 8k"
    },
    {
        "id": "HERO-44",
        "filename": "ep07_44_lapis_lazuli_powder_mortar_PAN_ZOOM.jpg",
        "prompt": "Cinematic 16:9 1080p film still. Macro close-up of raw deep blue lapis lazuli mineral crystals and vibrant ultramarine blue pigment powder inside an ancient granite mortar. Raking warm workshop sunlight, fine mineral texture, 8k"
    },
    # Master Thumbnail (16:9)
    {
        "id": "THUMB-01",
        "filename": "ep07_thumbnail_16x9_the_secret_canyon.jpg",
        "prompt": "High-impact YouTube documentary thumbnail (16:9). Dramatic low-angle view of a dark, monumental rock-cut cave portal carved into a sheer volcanic cliff face in a wild canyon, vibrant morning sunbeams slicing through mist, mysterious glowing amber oil lamps inside the portal, photorealistic National Geographic quality, 8k"
    },
    # Companion Short 01 Thumbnail (9:16)
    {
        "id": "SHORT-THUMB-01",
        "filename": "short_01_thumbnail_9x16.jpg",
        "prompt": "High-impact vertical YouTube Short thumbnail (9:16). Extreme vertical perspective of a 75-meter volcanic canyon cliff with ancient monks silhouetted on a narrow rock ledge, dramatic sunbeams piercing morning mist, intense depth, ultra-sharp 8k"
    },
    # Companion Short 02 Thumbnail (9:16)
    {
        "id": "SHORT-THUMB-02",
        "filename": "short_02_thumbnail_9x16.jpg",
        "prompt": "High-impact vertical YouTube Short thumbnail (9:16). Close-up of crystal clear water pouring from a rock-cut drainage channel into a torchlit subterranean reservoir, ancient monk holding a brass lamp, dark volcanic basalt reflections, 8k"
    }
]

def generate_image_item(item: dict) -> bool:
    fname = item["filename"]
    if "thumbnail" in str(fname) or "THUMB" in item["id"]:
        out_path = THUMBNAIL_DIR / fname
    else:
        out_path = IMAGES_DIR / fname

    if out_path.exists() and out_path.stat().st_size > 10000:
        print(f"[{item['id']}] Already exists: {fname}")
        if "GENERATE_VIDEO" in fname:
            gf_target = GOOGLE_FLOW_INPUT / fname
            if not gf_target.exists():
                shutil.copy2(out_path, gf_target)
        return True

    print(f"\n[{item['id']}] Generating {fname}...")
    try:
        resp = CLIENT.models.generate_content(
            model=MODEL,
            contents=item["prompt"]
        )
        if not resp.candidates or not resp.candidates[0].content.parts:
            print("  -> No candidates returned.")
            return False

        saved = False
        for part in resp.candidates[0].content.parts:
            if hasattr(part, "inline_data") and part.inline_data:
                with open(out_path, "wb") as f:
                    f.write(part.inline_data.data)
                print(f"  -> SUCCESS: Saved {out_path.name} ({len(part.inline_data.data):,} bytes)")
                
                if "GENERATE_VIDEO" in fname:
                    gf_target = GOOGLE_FLOW_INPUT / fname
                    shutil.copy2(out_path, gf_target)
                    print(f"  -> ISOLATED for Google Flow: {gf_target.name}")

                saved = True
                break
        if not saved:
            print("  -> No inline image bytes found.")
            return False

        time.sleep(2.0)
        return True
    except Exception as e:
        print(f"  -> ERROR generating {fname}: {e}")
        return False

def add_thumbnail_hook_typography():
    """Adds bold 3-word mobile hook typography to thumbnails obeying Law 5 & 6."""
    thumb_path = THUMBNAIL_DIR / "ep07_thumbnail_16x9_the_secret_canyon.jpg"
    if thumb_path.exists():
        try:
            im = Image.open(thumb_path).convert("RGB")
            draw = ImageDraw.Draw(im)
            f_hook = get_font_bold(88)
            # Mobile 3-Word Hook: "BEFORE KAILASA EXISTED"
            text = "BEFORE KAILASA"
            # Draw shadow
            draw.text((84, 124), text, fill=(0, 0, 0), font=f_hook)
            draw.text((80, 120), text, fill=(255, 215, 0), font=f_hook)
            im.save(thumb_path, quality=92)
            print("[OK] Applied 3-word hook typography to master thumbnail")
        except Exception as e:
            print(f"Warning: typography apply error: {e}")

def main():
    print("=" * 65)
    print("  EPISODE 07 VISUALS & GOOGLE FLOW BATCH GENERATOR")
    print("=" * 65)
    
    # 1. Generate 2 PIL Architectural Infographics (Law 9 compliant)
    generate_infographic_01_map()
    generate_infographic_02_hydrology()
    
    # 2. Generate Google Flow Prompt Sheet Table
    generate_google_flow_prompt_sheet()
    
    # 3. Generate Visual Stills & Google Flow Base Action Images
    success_count = 0
    for item in IMAGES_TO_GENERATE:
        ok = generate_image_item(item)
        if ok:
            success_count += 1
            
    # 4. Add Hook Typography to Thumbnail
    add_thumbnail_hook_typography()
    
    print("\n" + "=" * 65)
    print(f"  GENERATION RUN COMPLETE: {success_count}/{len(IMAGES_TO_GENERATE)} VISUALS READY")
    print(f"  All 8 Google Flow Base Action Stills isolated in: {GOOGLE_FLOW_INPUT}")
    print("=" * 65)

if __name__ == "__main__":
    main()
