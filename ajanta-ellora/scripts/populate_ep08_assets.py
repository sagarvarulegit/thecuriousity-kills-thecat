#!/usr/bin/env python3
"""
populate_ep08_assets.py — Generate all visual image assets for Episode 08: The Silk Road Blue & Mud Chemistry.
Enforces:
  1. The 10-Action Google Flow standard (isolated in google_flow_input_images/ and images/)
  2. 3 Raw Thumbnail Bases (1 Master 16:9 + 2 Shorts 9:16)
  3. 35 Master Hero Stills (Pillar A) in images/
  4. 10 Universe Archive Stills (Pillar C) in images/
  5. Zero duplicate media invariant across the series.
Uses Gemini 2.5 Flash Image API with resumes and exponential retries.
"""

import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv
from google import genai

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent # ajanta-ellora
EP08_DIR = BASE_DIR / "episode08"
IMAGES_DIR = EP08_DIR / "images"
GOOGLE_FLOW_DIR = EP08_DIR / "google_flow_input_images"
THUMBNAIL_DIR = EP08_DIR / "thumbnail"

IMAGES_DIR.mkdir(parents=True, exist_ok=True)
GOOGLE_FLOW_DIR.mkdir(parents=True, exist_ok=True)
THUMBNAIL_DIR.mkdir(parents=True, exist_ok=True)

# 1. 10 GOOGLE FLOW ACTION CANDIDATE STILLS (ISOLATED IN GOOGLE_FLOW_INPUT_IMAGES/)
GF_TARGETS = [
    {
        "filename": "ep08_gf_01_harishena_imperial_cavalry_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 16:9 1080p documentary film still. Ancient Indian Vakataka royal cavalry and armored war elephants draped in gilded copper plate, marching along the rocky Deccan volcanic canyon cliff at sunset. Saffron and deep purple silk banners whip in the warm breeze as golden dust rises from hooves. High contrast, warm golden hour lighting, National Geographic cinematography, 8k photorealistic."
    },
    {
        "filename": "ep08_gf_02_caravan_silkroad_lapis_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 16:9 1080p historical documentary still. A Silk Road merchant caravan of camels and pack bullocks traversing a narrow rocky mountain trail in the Western Ghats. Heavy leather saddlebags tied with thick hemp ropes bulge with rough, unpolished electric-blue lapis lazuli rocks. Dusty atmospheric depth, raking sunlight, 8k."
    },
    {
        "filename": "ep08_gf_03_mortar_grinding_lapis_powder_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 16:9 1080p high-speed macro action still. Weathered craftsman's hand grinding raw crystalline deep-blue lapis lazuli chunks in a heavy black granite mortar using a stone pestle. Bright electric azure mineral dust swirls with clear water into luminous blue paint, micro crystal facets catching light, 8k photorealistic."
    },
    {
        "filename": "ep08_gf_04_plaster_kneading_cowdung_matrix_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 16:9 1080p historical workshop still. Indian artisans in loincloths rhythmically treading and kneading thick organic reddish-brown mud plaster with their bare feet inside a large wooden trough. Golden rice husks, dry straw fibers, and dark fermented clay squishing with organic texture, warm morning workshop light, 8k."
    },
    {
        "filename": "ep08_gf_05_chipping_basalt_key_sparks_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 16:9 1080p action still. Muscular ancient Indian stonecutter striking a pointed iron pick chisel into a dark basalt cave wall. Sharp pointed blows chip away stone fragments at high speed as bright orange sparks ricochet off the dark volcanic rock face in raking lamp light, high-speed shutter, 8k photorealistic."
    },
    {
        "filename": "ep08_gf_06_agate_burnishing_intonaco_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 16:9 1080p macro craftsmanship still. Artisan's fingers firmly gripping a polished, banded brown-and-white agate burnishing river stone, pressing and gliding with rhythmic circular strokes over wet white slaked-lime plaster wall, transforming dull chalk into gleaming mirror-smooth ivory surface, delicate raking light, 8k."
    },
    {
        "filename": "ep08_gf_07_bronze_mirror_sunlight_beam_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 16:9 1080p optical engineering still. Blinding golden midday sunlight reflecting off a massive, highly polished cast-bronze concave circular mirror propped on a wooden tripod outside the cave veranda, casting an intense, collimated beam of golden light cutting through dust motes deep into the dark cave portal, 8k."
    },
    {
        "filename": "ep08_gf_08_brush_applying_lapis_eyelash_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 16:9 1080p microscopic macro still. Ultra-fine squirrel-hair bamboo paintbrush dripping with intense ultramarine blue paint tracing a razor-thin 0.2mm curved contour on the ivory plaster face of Bodhisattva Padmapani, paint settling into dry plaster pores, soft diffused studio-quality light, 8k."
    },
    {
        "filename": "ep08_gf_09_cave_interior_sunlit_murals_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 16:9 1080p sweeping architectural still. Inside the monumental carved rock columns of Cave One at Ajanta; natural reflected sunlight sweeps across the dark basalt ceiling, suddenly igniting intricate turquoise, gold, and terracotta lotus mandalas in brilliant color, deep perspective, 8k."
    },
    {
        "filename": "ep08_gf_10_harishena_shadow_cliffhanger_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 16:9 1080p dramatic climax still. Royal silhouette of an Indian emperor standing motionless at the cave entrance framed against violent purple lightning and black monsoon storm clouds rolling over the volcanic canyon gorge; oil torches flicker violently in cold wind, high contrast, 8k photorealistic."
    }
]

# 2. RAW THUMBNAIL BASES (3 ASSETS)
THUMBNAIL_TARGETS = [
    {
        "filename": "ep08_thumbnail_16x9_the_secret_chemistry.jpg",
        "dest_dir": THUMBNAIL_DIR,
        "prompt": "YouTube documentary thumbnail background 16:9. A solitary ancient Indian master artist holding a golden lamp inside a pitch-black volcanic basalt cave, illuminating the colossal, luminous face of Bodhisattva Padmapani glowing with electric ultramarine blue lapis lazuli and gold leaf. Extreme contrast, dark mystery, cinematic National Geographic lighting, 8k."
    },
    {
        "filename": "short_01_thumbnail_9x16.jpg",
        "dest_dir": THUMBNAIL_DIR,
        "prompt": "Vertical 9:16 mobile thumbnail background. Extreme macro view of ancient Indian hands burnishing wet white plaster with a polished agate stone, revealing a glowing layer of brilliant ultramarine blue paint underneath. High contrast, dramatic raking light, vivid blue and white against dark volcanic rock, 8k."
    },
    {
        "filename": "short_02_thumbnail_9x16.jpg",
        "dest_dir": THUMBNAIL_DIR,
        "prompt": "Vertical 9:16 mobile thumbnail background. A massive polished circular bronze mirror reflecting an intense, blinding beam of sunlight cutting through pitch-black darkness inside an ancient rock-cut cave temple. Volumetric light beam, dust motes, deep black shadows, 8k cinematic."
    }
]

# 3. MASTER HERO STILLS (35 ASSETS — PILLAR A)
HERO_TARGETS = [
    ("ep08_01_silent_canyon_dormancy_PAN_ZOOM.jpg", "Cinematic 16:9. Deserted crescent volcanic gorge of Ajanta overgrown with dense teak jungle and morning river mist. Dark cave portals half-hidden in moss, absolute stillness, golden dawn, 8k."),
    ("ep08_02_satavahana_chaitya_silt_floor_PAN_ZOOM.jpg", "Cinematic 16:9. Interior of ancient Cave 10 with river silt and bat guano covering the stone floor; ancient ribbed rafters in dim moody shadows, historical archaeology still, 8k."),
    ("ep08_03_harishena_coronation_royal_court_PAN_ZOOM.jpg", "Cinematic 16:9. Grand coronation court of Vakataka Emperor Harishena; throne room adorned with silk tapestries, brass braziers, and royal advisers examining maps of the Deccan, 8k."),
    ("ep08_04_vakataka_empire_deccan_map_still_PAN_ZOOM.jpg", "Cinematic 16:9. Ancient relief map of 5th century India carved into textured stone tablet; trade routes marked in glowing ochre connecting the Arabian sea to the Bay of Bengal, 8k."),
    ("ep08_05_dakshinapatha_trade_merchants_PAN_ZOOM.jpg", "Cinematic 16:9. Bustling ancient Indian market along the trade route; merchants trading spices, textiles, and gemstones under cloth canopies, warm sunlight, 8k."),
    ("ep08_06_royal_patron_architect_scroll_PAN_ZOOM.jpg", "Cinematic 16:9. Royal minister Varahadeva presenting architectural scrolls to Buddhist elder Buddhabhadra on a veranda overlooking the Ajanta gorge, dramatic composition, 8k."),
    ("ep08_07_canyon_cliff_construction_activity_PAN_ZOOM.jpg", "Cinematic 16:9. Wide view of the Ajanta crescent gorge teeming with activity; hundreds of ancient masons on wooden ramps along the cliff face, smoke from forges, 8k."),
    ("ep08_08_monumental_vihara_colonnade_facade_PAN_ZOOM.jpg", "Cinematic 16:9. Soaring multi-pillared rock-cut facade of Cave 1 at Ajanta; intricate friezes of celestial couples and lion capitals carved into solid basalt cliff, 8k."),
    ("ep08_09_royal_university_hall_perspective_PAN_ZOOM.jpg", "Cinematic 16:9. Colossal central hall of Cave 17; rows of square fluted columns receding in perspective, ancient monks walking in saffron robes, warm oil lamps, 8k."),
    ("ep08_10_raw_volcanic_basalt_seepage_PAN_ZOOM.jpg", "Cinematic 16:9. Macro shot of raw dark Cretaceous basalt rock sweating droplets of cold subterranean water; mineral crystalline glint, damp dark stone texture, 8k."),
    ("ep08_11_flaking_paint_moisture_failure_PAN_ZOOM.jpg", "Cinematic 16:9. Historical scientific demonstration: flaked and peeled pigment on wet basalt demonstrating why European fresco technique fails on volcanic stone, archaeological detail, 8k."),
    ("ep08_12_chitrasutra_palm_leaf_manuscript_PAN_ZOOM.jpg", "Cinematic 16:9. Ancient Sanskrit palm-leaf manuscript of the Chitrasutra text tied with red cord; ink diagrams of painting proportions and pigment chemistry, 8k."),
    ("ep08_13_laborers_pecking_basalt_dimples_PAN_ZOOM.jpg", "Cinematic 16:9. Two ancient laborers using pointed iron hammers to peck thousands of small indentation dimples across a basalt cave wall to create mechanical keying, 8k."),
    ("ep08_14_ferruginous_red_clay_quarry_PAN_ZOOM.jpg", "Cinematic 16:9. Mounds of rich red ferruginous Deccan clay drying in woven baskets under the sun beside the Waghur river; vibrant terracotta tones, 8k."),
    ("ep08_15_cow_dung_cellulose_fibers_macro_PAN_ZOOM.jpg", "Cinematic 16:9. Macro texture of dried and fermented organic cellulose fibers from cow dung and rock grit; fibrous sponge-like microstructure, scientific documentary look, 8k."),
    ("ep08_16_rice_husk_tensile_reinforcement_PAN_ZOOM.jpg", "Cinematic 16:9. Close-up of golden rice husks and vegetable straw being blended into clay paste; rich organic natural building materials, raking light, 8k."),
    ("ep08_17_neem_tree_sap_extraction_vessel_PAN_ZOOM.jpg", "Cinematic 16:9. Terracotta jar collecting viscous amber sap and gum from a thick gnarled neem tree trunk; green foliage, medicinal organic chemistry, 8k."),
    ("ep08_18_wooden_trowel_applying_mud_layer_PAN_ZOOM.jpg", "Cinematic 16:9. Artisan's hand smoothing a thick 10mm layer of organic red mud plaster onto keyed basalt wall with a curved teak wooden float, 8k."),
    ("ep08_19_slaked_lime_chuna_kiln_calcining_PAN_ZOOM.jpg", "Cinematic 16:9. Ancient stone kiln glowing with coals as pure white limestone and sea shells are calcined into slaked lime (chuna); heat haze, white powder, 8k."),
    ("ep08_20_crushed_oyster_shells_gypsum_powder_PAN_ZOOM.jpg", "Cinematic 16:9. Still life of pulverized white mother-of-pearl sea shells and crystalline gypsum powder in stone bowls; iridescent sheen, 8k."),
    ("ep08_21_agate_burnishing_stone_collection_PAN_ZOOM.jpg", "Cinematic 16:9. Array of smooth, water-worn river agates with concentric brown, red, and white bands resting on a wooden workbench beside plastering tools, 8k."),
    ("ep08_22_polished_ivory_smooth_intonaco_sheen_PAN_ZOOM.jpg", "Cinematic 16:9. Raking light catching the mirror-smooth ivory surface of a newly burnished lime plaster wall; reflecting subtle amber light like polished marble, 8k."),
    ("ep08_23_terracotta_pigment_bowls_palette_PAN_ZOOM.jpg", "Cinematic 16:9. Still life of traditional Indian mineral paint bowls: red ochre, yellow ochre, green glauconite, and chalk white beside animal-hair bamboo brushes, 8k."),
    ("ep08_24_mustard_oil_lamp_soot_collection_PAN_ZOOM.jpg", "Cinematic 16:9. Terracotta dish suspended over a smoking mustard oil lamp to collect pure carbon lampblack for eyeliner and contour painting, 8k."),
    ("ep08_25_raw_lapis_lazuli_mountain_rock_PAN_ZOOM.jpg", "Cinematic 16:9. A jagged chunk of raw unpolished deep blue lapis lazuli embedded with sparkling golden pyrite veins, resting on dark slate, 8k."),
    ("ep08_26_badakhshan_afghanistan_mountains_PAN_ZOOM.jpg", "Cinematic 16:9. High-altitude rugged snowy peaks of the Hindu Kush in Badakhshan, Afghanistan; harsh desolate mountain pass under deep azure sky, 8k."),
    ("ep08_27_camels_crossing_hindu_kush_pass_PAN_ZOOM.jpg", "Cinematic 16:9. Silk Road camel train plodding through snowy mountain switchbacks carrying heavy merchant goods toward northern India, dramatic historical landscape, 8k."),
    ("ep08_28_gold_scale_weighing_lapis_lazuli_PAN_ZOOM.jpg", "Cinematic 16:9. Bronze balancing scale weighing raw deep blue lapis lazuli crystals against solid gold coins in an ancient Indian royal treasury, 8k."),
    ("ep08_29_varahadeva_inscription_cave_16_PAN_ZOOM.jpg", "Cinematic 16:9. Ancient Sanskrit Brahmi inscription carved into the basalt veranda wall of Cave 16 commemorating Prime Minister Varahadeva's royal gift, 8k."),
    ("ep08_30_pitch_black_cave_interior_void_PAN_ZOOM.jpg", "Cinematic 16:9. Looking from the sunlit doorway into the pitch-black abyss of Cave 1; dark silhouettes of carved columns disappearing into absolute darkness, 8k."),
    ("ep08_31_clean_white_ceiling_no_soot_forensic_PAN_ZOOM.jpg", "Cinematic 16:9. Scientific macro photography of ancient painted cave ceiling showing vibrant colors and pristine white lime background with zero soot or carbon residue, 8k."),
    ("ep08_32_polished_cast_bronze_concave_mirror_PAN_ZOOM.jpg", "Cinematic 16:9. Close-up of a large circular cast-bronze mirror with decorative beaded rim, its polished golden face catching blinding sun, 8k."),
    ("ep08_33_wet_linen_sheet_light_diffuser_PAN_ZOOM.jpg", "Cinematic 16:9. Apprentices holding a large wet white cotton sheet inside a cave hall; a harsh reflected beam of sunlight hitting the fabric and diffusing into soft ambient light, 8k."),
    ("ep08_34_padmapani_tribhanga_posture_mural_PAN_ZOOM.jpg", "Cinematic 16:9. Frontal masterpiece view of Bodhisattva Padmapani in Cave 1 holding a blue lotus; sublime gentle expression, beaded tiara, soft three-dimensional shading, 8k."),
    ("ep08_35_persian_embassy_foreigners_fresco_PAN_ZOOM.jpg", "Cinematic 16:9. Fresco detail in Cave 1 showing foreign Persian ambassadors in conical caps and belted tunics presenting gifts to the Indian royal court, 8k.")
]

# 4. UNIVERSE ARCHIVE STILLS (10 ASSETS — PILLAR C)
ARCHIVE_TARGETS = [
    ("ep08_archive_01_harishena_royal_copper_plate_charter_PAN_ZOOM.jpg", "Historical archive scan 16:9. 5th-century Vakataka royal copper plate charter bound by a bronze ring with royal bull crest; Sanskrit Brahmi script engraved, museum plate, 8k."),
    ("ep08_archive_02_badakhshan_lapis_geological_survey_map_PAN_ZOOM.jpg", "Historical archive scan 16:9. Antique 19th-century geological survey map of Badakhshan Afghanistan showing historic Sar-e-Sang lapis lazuli vein locations, hand-tinted cartography, 8k."),
    ("ep08_archive_03_james_fergusson_1845_ajanta_cave_1_plate_PAN_ZOOM.jpg", "Historical archive scan 16:9. Tinted lithograph from James Fergusson's 1845 Illustrations of the Rock-Cut Temples of India showing Cave 1 interior in soft lighting, 8k."),
    ("ep08_archive_04_robert_gill_1850_canvas_replica_plate_PAN_ZOOM.jpg", "Historical archive scan 16:9. Archival Victorian plate of Major Robert Gill painting oil reproductions of Ajanta murals in his tent camp at the base of the gorge, 8k."),
    ("ep08_archive_05_asi_chemical_conservation_cross_section_1955_PAN_ZOOM.jpg", "Historical archive scan 16:9. 1955 Archaeological Survey of India chemical conservation report plate showing microscopic thin-section of Ajanta plaster layers with annotations, 8k."),
    ("ep08_archive_06_chitrasutra_ancient_canons_proportions_PAN_ZOOM.jpg", "Historical archive scan 16:9. Ancient Sanskrit treatise plate illustrating traditional facial measurement grids (Talamana) for Bodhisattva eyes and hands, museum archive, 8k."),
    ("ep08_archive_07_bronze_mirror_harappan_vakataka_museum_scan_PAN_ZOOM.jpg", "Historical archive scan 16:9. High-resolution museum scan of ancient Indian polished bronze mirror with ornate carved handle, National Museum New Delhi plate, 8k."),
    ("ep08_archive_08_majanaka_jataka_royal_renunciation_fresco_PAN_ZOOM.jpg", "Historical archive scan 16:9. High-resolution museum restoration plate of the Mahajanaka Jataka mural in Cave 1 showing royal palace scene with gold and lapis pigments, 8k."),
    ("ep08_archive_09_vajrapani_cave_1_regal_bodhisattva_PAN_ZOOM.jpg", "Historical archive scan 16:9. Museum conservation photograph of Bodhisattva Vajrapani in Cave 1; crowned in jewels, holding a diamond thunderbolt sceptre, warm ambient light, 8k."),
    ("ep08_archive_10_harishena_sudden_abandonment_cliff_shadow_PAN_ZOOM.jpg", "Historical archive scan 16:9. 19th-century monochrome survey plate of unfinished Cave 24 showing half-carved rock columns and abandoned chisel marks in dramatic shadow, 8k.")
]

def generate_one_image(client, model_name: str, prompt: str, target_paths: list) -> bool:
    if target_paths[0].exists() and target_paths[0].stat().st_size > 50000:
        print(f"  [EXISTS] Skipping {target_paths[0].name}")
        for p in target_paths[1:]:
            if not p.exists() or p.stat().st_size < 50000:
                with open(target_paths[0], "rb") as src, open(p, "wb") as dst:
                    dst.write(src.read())
        return True

    for attempt in range(3):
        try:
            resp = client.models.generate_content(
                model=model_name,
                contents=prompt
            )
            if resp.candidates and resp.candidates[0].content.parts:
                for part in resp.candidates[0].content.parts:
                    if hasattr(part, "inline_data") and part.inline_data:
                        data = part.inline_data.data
                        for p in target_paths:
                            with open(p, "wb") as f:
                                f.write(data)
                        print(f"  [OK] Saved {target_paths[0].name} ({len(data)} bytes)")
                        return True
            print(f"  [WARN] No inline image data on attempt {attempt+1}")
        except Exception as e:
            print(f"  [RETRY] Attempt {attempt+1} failed: {e}")
            time.sleep(2.0 * (attempt + 1))
    return False

def main():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("[ERROR] GEMINI_API_KEY not found in environment.")
        sys.exit(1)

    client = genai.Client(api_key=api_key)
    model_name = "gemini-2.5-flash-image"

    total = len(GF_TARGETS) + len(THUMBNAIL_TARGETS) + len(HERO_TARGETS) + len(ARCHIVE_TARGETS)
    print("=" * 65)
    print(f"  EPISODE 08 IMAGE ASSETS PIPELINE ({total} TOTAL ASSETS)")
    print(f"  Including 10 Google Flow Action Stills (Isolated in google_flow_input_images/)")
    print("=" * 65)

    count = 0

    # 1. Google Flow Action Stills (10 ASSETS)
    print("\n--- PHASE 1: GOOGLE FLOW ACTION CANDIDATE STILLS (10 ASSETS) ---")
    for item in GF_TARGETS:
        count += 1
        print(f"[{count:02d}/{total:02d}] Generating {item['filename']}...")
        p_img = IMAGES_DIR / item["filename"]
        p_gf = GOOGLE_FLOW_DIR / item["filename"]
        generate_one_image(client, model_name, item["prompt"], [p_img, p_gf])
        time.sleep(1.0)

    # 2. Raw Thumbnail Bases (3 ASSETS)
    print("\n--- PHASE 2: RAW THUMBNAIL BASES (3 ASSETS) ---")
    for item in THUMBNAIL_TARGETS:
        count += 1
        print(f"[{count:02d}/{total:02d}] Generating {item['filename']}...")
        p_thumb = item["dest_dir"] / item["filename"]
        generate_one_image(client, model_name, item["prompt"], [p_thumb])
        time.sleep(1.0)

    # 3. Master Hero Stills (35 ASSETS)
    print("\n--- PHASE 3: MASTER HERO STILLS (35 ASSETS) ---")
    for fname, prompt in HERO_TARGETS:
        count += 1
        print(f"[{count:02d}/{total:02d}] Generating {fname}...")
        p_hero = IMAGES_DIR / fname
        generate_one_image(client, model_name, prompt, [p_hero])
        time.sleep(1.0)

    # 4. Universe Archive Stills (10 ASSETS)
    print("\n--- PHASE 4: UNIVERSE ARCHIVE STILLS (10 ASSETS) ---")
    for fname, prompt in ARCHIVE_TARGETS:
        count += 1
        print(f"[{count:02d}/{total:02d}] Generating {fname}...")
        p_arch = IMAGES_DIR / fname
        generate_one_image(client, model_name, prompt, [p_arch])
        time.sleep(1.0)

    print(f"\n[ALL COMPLETE] Finished processing {total} Episode 08 visual assets!")

if __name__ == "__main__":
    main()
