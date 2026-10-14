"""
populate_ep06_assets.py — Generate all image assets for Episode 06: The Sky Bridges of Kailasa.
Enforces the Upgraded 16-Action Google Flow standard, 3-Pillar Visual Diversity Formula, and zero-repetition invariant.

Generates:
1. 16 Google Flow Action Candidate Stills (isolated in google_flow_input_images/ and copied to images/)
2. 3 Raw Thumbnail Bases in thumbnail/ (1 Master 16:9 + 2 Shorts 9:16)
3. 38 Master Hero Stills (Pillar A) in images/
4. 12 Universe Archive Stills (Pillar C) in images/
Uses Gemini 2.5 Flash Image API with retries and resumes existing files.
"""

import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv
from google import genai

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent # ajanta-ellora
EP06_DIR = BASE_DIR / "episode06"
IMAGES_DIR = EP06_DIR / "images"
GOOGLE_FLOW_DIR = EP06_DIR / "google_flow_input_images"
THUMBNAIL_DIR = EP06_DIR / "thumbnail"

IMAGES_DIR.mkdir(parents=True, exist_ok=True)
GOOGLE_FLOW_DIR.mkdir(parents=True, exist_ok=True)
THUMBNAIL_DIR.mkdir(parents=True, exist_ok=True)

# 16 Google Flow Stills
GF_TARGETS = [
    {
        "filename": "ep06_gf_01_sky_bridge_dawn_mist_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 16:9 1080p documentary film still. Low-angle perspective looking up from the 100-foot volcanic basalt rock chasm of Kailasa Cave 16 at Ellora. A monolithic stone bridge spans thirty feet in mid-air between dark rock walls in dense morning mist. An ancient surveyor in saffron robes walks across the suspended stone bridge. Golden dawn rim-lighting, National Geographic style, 8k photorealistic."
    },
    {
        "filename": "ep06_gf_02_kokasa_summit_geometry_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 16:9 1080p historical documentary still. Chief architect Kokasa on the windy mountain cliff summit at sunrise, holding a bronze plumb-bob cord and solar shadow-pole. Red chalk measuring lines snapped across raw volcanic basalt rock. Intense concentration, blowing dust, warm morning sun, 8k photorealistic."
    },
    {
        "filename": "ep06_gf_03_quarrymen_hemp_rope_void_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 16:9 1080p action still. Two muscular ancient Indian stonecutters suspended in thick braided hemp rope harnesses hanging 30 feet in mid-air beneath the underside of a rock bridge. They strike pointed iron picks upward against the basalt ceiling, stone chips raining down into the deep chasm void, dramatic chiaroscuro lighting, 8k."
    },
    {
        "filename": "ep06_gf_04_hammer_wedge_sparks_void_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 16:9 1080p high-speed macro action still. Heavy wooden mallet smashing an iron splitting wedge driven into a natural basalt rock fissure beneath the hanging rock arch. Fiery shower of golden sparks and stone dust bursting against dark stone, 60fps slow-motion capture feel, 8k photorealistic."
    },
    {
        "filename": "ep06_gf_05_water_quench_fissure_check_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 16:9 1080p documentary macro still. Ancient master surveyor pouring clear cold water from a terracotta jug across a freshly carved basalt stone bridge joint. Water sheeting over dark volcanic rock, revealing hairline natural veins under flickering torchlight, 8k archaeological detail."
    },
    {
        "filename": "ep06_gf_06_dhwajasthambha_quarry_reveal_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 16:9 1080p architectural documentary still. Time-lapse quarry impression: A colossal 17-meter tall monolithic stone victory pillar (Dhwajasthambha) emerging standing free from the excavated courtyard rock at Ellora. Dozens of ancient masons clearing basalt rubble around its base, dramatic scale, 8k."
    },
    {
        "filename": "ep06_gf_07_courtyard_elephant_tusk_carve_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 16:9 1080p macro sculpture still. Ancient Indian master sculptor perched on a wooden bench, tapping a steel v-chisel along the curve of a colossal freestanding monolithic elephant's tusk in the Kailasa courtyard. Fine white rock dust drifting in raking golden sunlight, 8k photorealistic."
    },
    {
        "filename": "ep06_gf_08_queen_balcony_seven_days_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 16:9 1080p historical cinematic still. Rashtrakuta royal queen in elegant silks standing on a stone palace balcony at dawn, gazing with awe across misty green Sahyadri hills toward the cliff peak where the newly carved temple shikhara pinnacle catches the first golden beam of sun, 8k masterpiece."
    },
    {
        "filename": "ep06_gf_09_white_chuna_plaster_burnish_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 16:9 1080p macro craftsmanship still. Ancient artisan vigorously rubbing a smooth polished agate river stone against wet white shell-lime plaster (chuna) on a carved temple wall. The dull chalk transforms into a high-gloss porcelain-like mirror finish catching blinding tropical sunlight, 8k photorealistic."
    },
    {
        "filename": "ep06_gf_10_twilight_nandi_oil_lamps_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 16:9 1080p atmospheric dusk still. Interior upper story of the Nandi mandapa pavilion at Kailasa. Bronze oil lamps flickering with warm golden flames in the evening breeze, casting dancing amber shadows across carved stone window grilles and the aerial bridge walkway outside, 8k historical."
    },
    {
        "filename": "ep06_gf_11_ramayana_frieze_chisel_macro_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 16:9 1080p extreme macro photograph. Pointed steel chisel tip carving a miniature galloping war chariot and archer figure on the continuous Ramayana narrative frieze on the volcanic basalt temple plinth. Micro-fractures and sharp stone chips, raking sunlight, 8k ultra-sharp."
    },
    {
        "filename": "ep06_gf_12_ravana_shaking_mountain_torch_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 16:9 1080p dramatic high-relief sculpture still. Atmospheric torchlight sweeping across the massive relief of twenty-armed demon king Ravana trapped beneath the roots of Mount Kailash. Straining muscular stone arms and bulging eyes, deep terrifying chiaroscuro shadow undercuts, 8k documentary."
    },
    {
        "filename": "ep06_gf_13_aurangzeb_demolition_siege_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 16:9 1080p 17th-century historical reconstruction. Demolition workers striking heavy iron sledgehammers against the solid monolithic wall of Kailasa Temple. Iron hammers bouncing off the impenetrable dark volcanic basalt with sparks flying, solid mountain refusing to crumble, 8k gritty realism."
    },
    {
        "filename": "ep06_gf_14_torch_priest_stairwell_descent_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 16:9 1080p atmospheric documentary still. Ancient priest holding a burning torch descending a steep, narrow stone staircase carved directly inside the solid rock wall of Kailasa. Amber torchlight licking dark basalt steps, trailing smoke and deep shadows, 8k cinematic."
    },
    {
        "filename": "ep06_gf_15_kokasa_architect_breakdown_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 16:9 1080p emotional historical portrait. Master architect Kokasa standing on the damp basalt courtyard floor at blue twilight, gazing straight up at the soaring vimana and hanging sky bridges in utter disbelief. He drops his iron calipers, weeping with awe, 8k photorealistic."
    },
    {
        "filename": "ep06_gf_16_climax_crepuscular_rays_chasm_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 16:9 1080p epic documentary climax still. Low-angle wide view looking between the twin 17-meter victory pillars and under the suspended monolithic sky bridge toward the soaring 30-meter temple tower. Divine golden god-rays cutting through morning mist, grand monolithic masterwork, 8k."
    }
]

# Raw Thumbnail Targets
THUMBNAIL_TARGETS = [
    {
        "filename": "ep06_master_thumbnail_raw.jpg",
        "dest_dir": THUMBNAIL_DIR,
        "prompt": "Cinematic 16:9 1080p dramatic documentary still. Extreme low-angle view looking straight up from the deep dark basalt chasm of Kailasa Cave 16 at the monumental monolithic stone bridge suspended 30 feet in mid-air. Golden dawn sunlight streaming through the chasm, ancient surveyor silhouette crossing the floating bridge, 8k National Geographic cover."
    },
    {
        "filename": "short_01_thumbnail_raw_9x16.jpg",
        "dest_dir": THUMBNAIL_DIR,
        "prompt": "Cinematic 9:16 vertical 1080x1920 documentary still. Dramatic vertical framing looking up through the 30-foot void beneath the monolithic sky bridge of Kailasa Temple at Ellora. Saffron-robed surveyor walking across the hanging bridge, dark volcanic basalt walls towering on either side, mobile-optimized high contrast, 8k."
    },
    {
        "filename": "short_02_thumbnail_raw_9x16.jpg",
        "dest_dir": THUMBNAIL_DIR,
        "prompt": "Cinematic 9:16 vertical 1080x1920 documentary still. Vertical framing of an iron sledgehammer striking the impenetrable basalt wall of Kailasa Temple, sparks bursting out against dark stone, with the massive indestructible temple tower rising into a stormy sky, mobile-optimized high contrast, 8k."
    }
]

# 38 Master Hero Stills
HERO_TARGETS = [
    ("ep06_01_chasm_depth_entry_PAN_ZOOM.jpg", "Cinematic 16:9 1080p documentary film still. Looking down into the 100-foot vertical basalt trench of Kailasa Cave 16, morning light illuminating the sheer excavated rock curtain walls, 8k."),
    ("ep06_02_sky_bridge_underside_void_PAN_ZOOM.jpg", "Cinematic 16:9 1080p low-angle architectural still. Looking directly up at the smooth curved underbelly of the monolithic stone bridge spanning the chasm, clear blue sky visible through the archway, 8k."),
    ("ep06_03_bridge_coping_and_parapet_PAN_ZOOM.jpg", "Cinematic 16:9 1080p architectural medium shot. The carved stone balustrade and decorative lotus frieze running along the top of the suspended monolithic walkway, 8k."),
    ("ep06_04_gopuram_terrace_view_PAN_ZOOM.jpg", "Cinematic 16:9 1080p high perspective shot. Standing on the upper entrance gopuram gateway looking across the monolithic bridge into the second-story Nandi pavilion, 8k."),
    ("ep06_05_basalt_tensile_arch_detail_PAN_ZOOM.jpg", "Cinematic 16:9 1080p macro architectural study. The seamless junction where the horizontal bridge span merges into the vertical cliff rock without mortar joints or seams, 8k."),
    ("ep06_06_courtyard_shadow_play_PAN_ZOOM.jpg", "Cinematic 16:9 1080p atmospheric documentary still. Raking afternoon shadows cast by the suspended sky bridge across the stone courtyard floor 30 feet below, 8k."),
    ("ep06_07_katha_kalpataru_palm_leaf_PAN_ZOOM.jpg", "Cinematic 16:9 museum macro still. Ancient Sanskrit palm-leaf manuscript with Devanagari script detailing the legendary medieval chronicle of the Queen's vow and Kokasa, 8k."),
    ("ep06_08_queen_illness_royal_court_PAN_ZOOM.jpg", "Cinematic 16:9 historical drama still. Ancient Rashtrakuta royal court in stone palace chamber: royal physicians, ministers, and the queen praying for the king's recovery, warm oil lamps, 8k."),
    ("ep06_09_kokasa_presentation_to_king_PAN_ZOOM.jpg", "Cinematic 16:9 historical scene. Master builder Kokasa presenting an architectural plan etched on copper plate before the Rashtrakuta royal throne, promising a 7-day shikhara, 8k."),
    ("ep06_10_cliff_summit_measuring_grid_PAN_ZOOM.jpg", "Cinematic 16:9 wide archaeological still. The flat top of Charanandri hill showing rock-cut grid channels and benchmark datum markers cut into basalt bedrock, 8k."),
    ("ep06_11_shikhara_finial_kalasha_PAN_ZOOM.jpg", "Cinematic 16:9 macro architectural still. The crowning kalasha vase finial of Kailasa shikhara, carved with intricate foliage and ribbed stone moldings, clear morning sky, 8k."),
    ("ep06_12_top_down_stepped_terraces_PAN_ZOOM.jpg", "Cinematic 16:9 aerial perspective illustration. Isometric view of descending rock benches cut into the mountain slope, shikhara finished while lower halls remain solid stone, 8k."),
    ("ep06_13_rope_rigging_anchor_points_PAN_ZOOM.jpg", "Cinematic 16:9 archaeological detail. Deep ancient round drill-holes in the upper basalt parapet used by quarrymen to anchor thick suspension ropes over the chasm, 8k."),
    ("ep06_14_inverted_quarry_technique_PAN_ZOOM.jpg", "Cinematic 16:9 historical reconstruction still. Quarrymen holding iron picks working under the shadow of the bridge arch, chipping away rock fragments into the void, 8k."),
    ("ep06_15_acoustic_sounding_chisel_tap_PAN_ZOOM.jpg", "Cinematic 16:9 macro close-up. Master stone mason holding his ear close to the dark basalt ceiling while gently tapping an iron punch to listen to the stone's pitch, 8k."),
    ("ep06_16_tempered_chisel_arsenal_PAN_ZOOM.jpg", "Cinematic 16:9 still life macro. Row of blackened, fire-tempered iron and steel chisels, punches, and gouges resting on an ancient toolmaker's wooden bench, 8k."),
    ("ep06_17_void_clearance_moment_hero_PAN_ZOOM.jpg", "Cinematic 16:9 dramatic wide still. The moment the final stone block beneath the bridge dropped away, leaving the 30-foot air gap completely clear under morning sun, 8k."),
    ("ep06_18_twin_dhwajasthambha_symmetry_PAN_ZOOM.jpg", "Cinematic 16:9 symmetrical wide shot. Looking west through the courtyard showing both 17-meter fluted victory pillars framing the central Nandi shrine, 8k."),
    ("ep06_19_dhwajasthambha_trident_capital_PAN_ZOOM.jpg", "Cinematic 16:9 low-angle telephoto shot. Crowning capital of the southern victory pillar featuring carved floral swags, fluting, and the sacred trishula finial against clouds, 8k."),
    ("ep06_20_freestanding_elephant_flank_PAN_ZOOM.jpg", "Cinematic 16:9 full-body sculpture portrait. The northern life-size monolithic courtyard elephant standing in proud repose on the stone floor, weathered tusk stubs, 8k."),
    ("ep06_21_elephant_ear_rock_texture_PAN_ZOOM.jpg", "Cinematic 16:9 macro textural still. The sweeping curve of the carved monolithic elephant's ear, showing the fine parallel chisel grooves left by 8th-century tooth chisels, 8k."),
    ("ep06_22_3d_spatial_visualization_still_PAN_ZOOM.jpg", "Cinematic 16:9 documentary still. Diagrammatic lighting tracing the outline of a freestanding elephant inside an uncut square prism of volcanic basalt, 8k."),
    ("ep06_23_ramayana_running_frieze_overview_PAN_ZOOM.jpg", "Cinematic 16:9 panoramic macro still. Continuous horizontal stone band along the south wall of Kailasa showing running narrative panels of the epic Ramayana, 8k."),
    ("ep06_24_battle_of_lanka_warriors_PAN_ZOOM.jpg", "Cinematic 16:9 telephoto macro still. Intricate stone panel of the battle of Lanka: Vanara warriors hurling boulders, war chariots, and archers carved in miniature relief, 8k."),
    ("ep06_25_ravana_anugraha_wide_recess_PAN_ZOOM.jpg", "Cinematic 16:9 dramatic wide still. The deep shaded southern recess of Cave 16 housing the colossal two-story Ravana Shaking Kailasa relief panel, 8k."),
    ("ep06_26_shiva_calm_foot_press_PAN_ZOOM.jpg", "Cinematic 16:9 sculptural close-up. Lord Shiva and goddess Parvati seated peacefully on Mount Kailash, Shiva's right big toe resting lightly on the bedrock, 8k."),
    ("ep06_27_chiaroscuro_relief_depth_PAN_ZOOM.jpg", "Cinematic 16:9 high-contrast photographic still. Raking midday sun creating sharp jet-black shadows inside the 60cm deep undercuts of the epic narrative frieze, 8k."),
    ("ep06_28_ancient_white_plaster_reconstruction_PAN_ZOOM.jpg", "Cinematic 16:9 CGI historical reconstruction still. The entire monolithic Kailasa temple glowing radiant porcelain-white under the Deccan sun, mirroring a snowy Himalayan peak, 8k."),
    ("ep06_29_calcined_river_shells_chuna_PAN_ZOOM.jpg", "Cinematic 16:9 historical macro still. Piles of calcined river freshwater shells, fine white marble dust, and wooden slaking troughs used to prepare imperial chuna plaster, 8k."),
    ("ep06_30_agate_burnishing_stone_macro_PAN_ZOOM.jpg", "Cinematic 16:9 archaeological artifact still. Smooth oval agate and chalcedony river stones used by ancient artisans to burnish plaster surfaces to a mirror finish, 8k."),
    ("ep06_31_surviving_plaster_remnants_cornice_PAN_ZOOM.jpg", "Cinematic 16:9 macro documentary photograph. Actual surviving patches of 1,200-year-old white shell-lime plaster preserved in sheltered ceiling recesses of Cave 16, 8k."),
    ("ep06_32_iceberg_in_black_chasm_hero_PAN_ZOOM.jpg", "Cinematic 16:9 wide historical vision still. How ancient pilgrims saw Elapura from afar: A glistening snow-white mountain temple rising out of a dark volcanic basalt gorge, 8k."),
    ("ep06_33_1682_aurangzeb_royal_camp_PAN_ZOOM.jpg", "Cinematic 16:9 historical wide still. Mughal military encampment with red pavilions and banners pitched on the hills above Ellora in the late 17th century, 8k."),
    ("ep06_34_demolition_taskforce_tools_PAN_ZOOM.jpg", "Cinematic 16:9 historical still. Rows of heavy iron sledgehammers, crowbars, and chisels laid out on stone flags before the temple gateway, 8k."),
    ("ep06_35_failed_demolition_scars_basalt_PAN_ZOOM.jpg", "Cinematic 16:9 documentary photograph. Surface scars and chipped relief moldings on the outer gateway where 17th-century hammers struck the basalt without damaging the monolith, 8k."),
    ("ep06_36_baroda_copper_plate_charter_PAN_ZOOM.jpg", "Cinematic 16:9 museum macro photograph. Close-up of the authentic Baroda copper plate inscription of King Karka II (812 CE) containing the famous architect's lament, 8k."),
    ("ep06_37_celestial_gods_view_downward_PAN_ZOOM.jpg", "Cinematic 16:9 aerial bird's-eye perspective. Looking straight down into the deep rock pit of Cave 16 from high above, capturing the dizzying monolithic layout, 8k."),
    ("ep06_38_architect_katham_akrita_hero_PAN_ZOOM.jpg", "Cinematic 16:9 twilight master portrait. Kailasa Temple soaring in deep blue twilight with golden oil lamps glowing, immortal testament to human impossibility, 8k masterpiece.")
]

# 12 Universe Archive Stills
ARCHIVE_TARGETS = [
    ("ep06_archive_01_ellora_ridge_topography_PAN_ZOOM.jpg", "Cinematic 16:9 geological survey still. Overview of the Charanandri hill range showing horizontal lava basalt traps and natural escarpments, 8k."),
    ("ep06_archive_02_kailasa_ground_plan_schematic_PAN_ZOOM.jpg", "Cinematic 16:9 architectural blueprint still. Detailed measured ground plan of Cave 16 showing the gopuram, Nandi shrine, sabha mandapa, and vimana, 8k."),
    ("ep06_archive_03_top_down_cross_section_elevation_PAN_ZOOM.jpg", "Cinematic 16:9 architectural cross-section drawing. 19th-century Archaeological Survey of India plate showing the longitudinal section of Cave 16 with sky bridge, 8k."),
    ("ep06_archive_04_ancient_vasthu_shastra_compass_PAN_ZOOM.jpg", "Cinematic 16:9 macro still. Ancient Indian brass gnomon sundial and geometric calculation instruments on parchment, 8k."),
    ("ep06_archive_05_baroda_plates_garuda_seal_PAN_ZOOM.jpg", "Cinematic 16:9 museum macro photograph. The heavy cast-bronze Garuda seal ring joining the Baroda copper plates of 812 CE, 8k."),
    ("ep06_archive_06_james_burgess_1883_report_plate_PAN_ZOOM.jpg", "Cinematic 16:9 vintage archival still. Open 1883 Archaeological Survey volume by James Burgess featuring photographic plates of Kailasa bridges, 8k."),
    ("ep06_archive_07_rashtrakuta_iron_mine_smelting_PAN_ZOOM.jpg", "Cinematic 16:9 historical reconstruction. 8th-century bloomeries and bellows smelting high-carbon wootz steel for stoneworking tools, 8k."),
    ("ep06_archive_08_plaster_microscopic_cross_section_PAN_ZOOM.jpg", "Cinematic 16:9 scientific polarized light microscope still. Thin section of ancient shell-lime plaster showing calcined shell fragments and calcite crystals, 8k."),
    ("ep06_archive_09_19th_century_collo_type_kailasa_bridge_PAN_ZOOM.jpg", "Cinematic 16:9 vintage collotype photograph from 1870. The upper monolithic bridge and Nandi mandapa of Cave 16 in sepia albumen tones, 8k."),
    ("ep06_archive_10_aurangzeb_court_chronicle_manuscript_PAN_ZOOM.jpg", "Cinematic 16:9 historical manuscript still. Persian court chronicle Maasir-i-Alamgiri describing the Mughal campaigns in the Deccan near Daulatabad, 8k."),
    ("ep06_archive_11_stone_mason_guild_emblems_PAN_ZOOM.jpg", "Cinematic 16:9 macro archaeological still. Ancient artisan guild masons' marks chiseled into rock flags at Ellora, 8k."),
    ("ep06_archive_12_kailasa_vimana_starry_night_PAN_ZOOM.jpg", "Cinematic 16:9 astrophotography documentary still. The towering 30-meter stone spire of Kailasa silhouetted against the Milky Way core over Ellora, 8k.")
]

def generate_one_image(client, model_name, prompt, target_paths):
    all_exist = all(p.exists() and p.stat().st_size > 10000 for p in target_paths)
    if all_exist:
        print(f"  [EXISTS] Skipping {target_paths[0].name}")
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
    print(f"  EPISODE 06 IMAGE ASSETS PIPELINE ({total} TOTAL ASSETS)")
    print(f"  Including 16 Google Flow Action Stills (Upgraded Standard)")
    print("=" * 65)

    count = 0

    # 1. Google Flow Action Stills (16 ASSETS)
    print("\n--- PHASE 1: GOOGLE FLOW ACTION CANDIDATE STILLS (16 ASSETS) ---")
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

    # 3. Master Hero Stills (38 ASSETS)
    print("\n--- PHASE 3: MASTER HERO STILLS (38 ASSETS) ---")
    for fname, prompt in HERO_TARGETS:
        count += 1
        print(f"[{count:02d}/{total:02d}] Generating {fname}...")
        p_hero = IMAGES_DIR / fname
        generate_one_image(client, model_name, prompt, [p_hero])
        time.sleep(1.0)

    # 4. Universe Archive Stills (12 ASSETS)
    print("\n--- PHASE 4: UNIVERSE ARCHIVE STILLS (12 ASSETS) ---")
    for fname, prompt in ARCHIVE_TARGETS:
        count += 1
        print(f"[{count:02d}/{total:02d}] Generating {fname}...")
        p_arch = IMAGES_DIR / fname
        generate_one_image(client, model_name, prompt, [p_arch])
        time.sleep(1.0)

    print(f"\n[ALL COMPLETE] Finished processing {total} Episode 06 visual assets!")

if __name__ == "__main__":
    main()
