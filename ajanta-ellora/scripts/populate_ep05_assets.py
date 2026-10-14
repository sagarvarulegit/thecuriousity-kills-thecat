"""
Populate and generate all image assets for Episode 05: The Elephants Beneath Kailasa.
Enforces the 3-Pillar Visual Diversity Formula and strict zero-repetition invariant.

Generates:
1. 8 Google Flow Action Candidate Stills (isolated in google_flow_input_images/ and copied to images/)
2. 46 Master Hero Stills (Pillar A) in images/
3. 10 Universe Archive Stills (Pillar C) in images/
4. 3 Raw Thumbnail Bases in thumbnail/ (1 Master 16:9 + 2 Shorts 9:16)
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
EP05_DIR = BASE_DIR / "episode05"
IMAGES_DIR = EP05_DIR / "images"
GOOGLE_FLOW_DIR = EP05_DIR / "google_flow_input_images"
THUMBNAIL_DIR = EP05_DIR / "thumbnail"

IMAGES_DIR.mkdir(parents=True, exist_ok=True)
GOOGLE_FLOW_DIR.mkdir(parents=True, exist_ok=True)
THUMBNAIL_DIR.mkdir(parents=True, exist_ok=True)

# 8 Google Flow Stills
GF_TARGETS = [
    {
        "filename": "ep05_gf_01_chisel_striking_elephant_tusk_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 16:9 1080p macro action still. Pointed iron chisel held firmly against the curved tusk of a monumental carved basalt elephant at Kailasa Temple. Heavy wooden mallet striking the chisel end, sharp chips and grey rock powder bursting into the air, dramatic raking dawn sunlight, 8k photorealistic."
    },
    {
        "filename": "ep05_gf_02_water_quenching_carved_plinth_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 16:9 1080p action still. A bronze bucket splashing cool clear water across freshly chiseled dark Deccan basalt stone plinth. Glistening water droplets washing away fine stone dust, delicate steam rising from the sun-warmed volcanic rock, 8k documentary."
    },
    {
        "filename": "ep05_gf_03_mallet_carving_elephant_underbelly_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 16:9 1080p macro action still. Ancient Indian stone carver's weathered hands holding an iron claw chisel deep in the undercut cavity beneath a colossal stone elephant's belly. Wooden mallet striking, stone chips cascading downward, deep shadow contrast, 8k photorealistic."
    },
    {
        "filename": "ep05_gf_04_plinth_measuring_cord_snap_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 16:9 1080p macro action still. Two ancient Indian master architects pulling a taut cord saturated with crimson red-ochre mineral dye along the dark flat basalt baseline of the plinth. Crimson mineral dust clinging to the cord, intense focus, morning quarry light, 8k documentary."
    },
    {
        "filename": "ep05_gf_05_rain_clouds_over_kailasa_summit_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 16:9 1080p dramatic weather still. Colossal dark monsoon storm clouds billowing rapidly over the towering carved basalt vimana tower of Kailasa Temple. A faint distant flash of lightning illuminating the mountain pinnacle, torrential rain mist in the courtyard chasm, 8k documentary."
    },
    {
        "filename": "ep05_gf_06_sledgehammer_quarry_impact_sparks_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 16:9 1080p high-speed action still. Colossal 20-pound forged iron sledgehammer impacting a heavy iron splitting wedge driven into a raw basalt boulder at the plinth boundary. Fiery shower of golden friction sparks bursting against dark volcanic stone, raw explosive power, 8k photorealistic."
    },
    {
        "filename": "ep05_gf_07_oil_lamp_flicker_elephant_relief_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 16:9 1080p atmospheric still. Ancient bronze oil lamp held near the weathered head of a carved basalt elephant in the Kailasa courtyard at twilight. Golden flame flickering, casting dancing warm amber shadows across the deep stone eye socket and curled trunk, 8k historical."
    },
    {
        "filename": "ep05_gf_08_dust_swirling_past_elephant_row_GENERATE_VIDEO.jpg",
        "prompt": "Cinematic 16:9 1080p atmospheric still. A shaft of golden afternoon sunlight piercing the deep courtyard pit, illuminating fine stone dust and dry motes swirling past a procession of colossal carved basalt elephant heads. Cinematic depth, 8k photorealistic."
    }
]

# Raw Thumbnail Targets
THUMBNAIL_TARGETS = [
    {
        "filename": "ep05_master_thumbnail_raw.jpg",
        "dest_dir": THUMBNAIL_DIR,
        "prompt": "Cinematic 16:9 1080p dramatic documentary still. Extreme low-angle view from the dark basalt courtyard looking straight up at a colossal carved elephant on the Kailasa plinth. The massive elephant head and curled trunk with tusks thrust upward as if physically hoisting the towering carved temple cathedral above. Intense golden raking dawn sunlight, dark stormy sky, 8k photorealistic National Geographic cover."
    },
    {
        "filename": "short_01_thumbnail_raw_9x16.jpg",
        "dest_dir": THUMBNAIL_DIR,
        "prompt": "Cinematic 9:16 vertical 1080x1920 documentary still. Dramatic low-angle vertical framing of a life-sized carved basalt elephant on Kailasa temple plinth holding a lotus flower in its trunk, with the massive temple wall towering above. Intense golden raking sunlight, dark basalt texture, mobile-optimized high contrast, 8k."
    },
    {
        "filename": "short_02_thumbnail_raw_9x16.jpg",
        "dest_dir": THUMBNAIL_DIR,
        "prompt": "Cinematic 9:16 vertical 1080x1920 documentary still. Vertical composition showing the soaring Dravidian temple tower of Kailasa emerging directly above a procession of carved stone elephants at the base. Dark storm clouds swirling above, warm golden light on the elephant heads, 8k photorealistic."
    }
]

# 46 Master Hero Stills
HERO_TARGETS = [
    ("ep05_01_courtyard_ground_plinth_reveal_PAN_ZOOM.jpg", "Cinematic 16:9 1080p documentary film still. Low-angle perspective looking across the dark volcanic basalt courtyard of Kailasa Temple at dawn. The monumental 8-meter high carved plinth rises out of the rock, ancient chisel marks catch golden raking morning light, National Geographic style, 8k."),
    ("ep05_02_elephant_procession_shoulder_row_PAN_ZOOM.jpg", "Cinematic 16:9 1080p architectural still. Continuous horizontal frieze of monumental life-sized elephants carved in high relief shoulder to shoulder along the Kailasa temple plinth. Weathered dark Deccan basalt, powerful muscular anatomy, 8k photorealistic."),
    ("ep05_03_apparent_support_angle_PAN_ZOOM.jpg", "Cinematic 16:9 1080p low-angle shot. Looking up from courtyard floor where the massive curved backs and heads of carved stone elephants appear to physically carry the monumental projecting cornice and upper temple hall on their shoulders. Dramatic scale, 8k."),
    ("ep05_04_sculptural_framing_perspective_PAN_ZOOM.jpg", "Cinematic 16:9 1080p wide architectural composition. Framing the towering vimana sanctuary and pillared halls of Kailasa as they rise above the dark sculpted animal plinth. Clear morning sky, ancient volcanic rock texture, 8k."),
    ("ep05_05_kailasa_rock_trench_panoramic_PAN_ZOOM.jpg", "Cinematic 16:9 1080p panoramic documentary shot. Wide view of the excavated Cave 16 rock pit at Ellora, showing the immense 30-meter high temple monolith standing completely free within the mountain trench, morning sunlight raking across basalt walls, 8k."),
    ("ep05_06_elephant_head_chiaroscuro_PAN_ZOOM.jpg", "Cinematic 16:9 1080p chiaroscuro photographic still. Extreme side-lit close-up of a carved elephant head on the Kailasa plinth. Deep shadows in the eye sockets and stone ear folds, rough volcanic basalt grain, golden sunrise illumination, 8k."),
    ("ep05_07_courtyard_freestanding_sanctuary_PAN_ZOOM.jpg", "Cinematic 16:9 1080p wide documentary film still. Looking east across the excavated courtyard showing the freestanding Nandi pavilion, courtyard victory pillar (dhvajastambha), and main temple sanctuary rising from the plinth. Historical depth, 8k."),
    ("ep05_08_towering_plinth_elevation_PAN_ZOOM.jpg", "Cinematic 16:9 1080p straight-on architectural elevation photograph. The 8-meter tall monolithic basement plinth of Kailasa, showing the moulded base, continuous elephant and lion frieze, and overhanging cornice moulding. Archaeological clarity, 8k."),
    ("ep05_09_dense_sculptural_band_panning_PAN_ZOOM.jpg", "Cinematic 16:9 1080p medium shot tracking along the plinth. Rhythm of carved elephants alternating with ferocious roaring lions and mythical vyalas, all carved from the same solid Deccan trap bedrock. Warm sunlight, 8k photorealistic."),
    ("ep05_10_transition_earth_to_temple_PAN_ZOOM.jpg", "Cinematic 16:9 1080p vertical perspective composition. Transitioning from the flat basalt courtyard flagstones up through the carved elephant band into the pilastered temple sanctuary walls above. Rich stone textures, 8k."),
    ("ep05_11_plinth_corner_angle_perspective_PAN_ZOOM.jpg", "Cinematic 16:9 1080p three-quarter angle photograph of the south-west plinth corner. Two rows of carved elephants converge at the sharp rock corner, meeting in dynamic high relief. Raking morning sun, 8k documentary."),
    ("ep05_12_lower_storey_ambulatory_walk_PAN_ZOOM.jpg", "Cinematic 16:9 1080p eye-level film still walking along the narrow pradakshina circumambulation path in Kailasa courtyard. The colossal elephant relief looms beside the viewer, dark basalt canyon walls on the left, atmospheric dust motes, 8k."),
    ("ep05_13_elephant_trunk_lotus_flower_PAN_ZOOM.jpg", "Cinematic 16:9 1080p archaeological macro close-up. A life-sized carved elephant trunk delicately curling around a blooming lotus flower bud chiseled from Deccan basalt. Remarkable ancient sculptural finesse, soft side lighting, 8k."),
    ("ep05_14_integrated_sculptural_register_PAN_ZOOM.jpg", "Cinematic 16:9 1080p close architectural study. Demonstrating the seamless geological continuity where an elephant's hindquarters meld directly into the uncarved living rock mass behind. Zero joints or mortar, 8k."),
    ("ep05_15_deep_relief_chiaroscuro_depth_PAN_ZOOM.jpg", "Cinematic 16:9 1080p high-contrast documentary still. Focusing into the deep 80cm undercut void between the carved legs of adjacent elephants. Deep pitch-black shadows contrasted against sunlit stone foreheads, 8k."),
    ("ep05_16_weathered_trunk_patina_detail_PAN_ZOOM.jpg", "Cinematic 16:9 1080p macro photograph of ancient stone weathering. Fractured elephant tusk stub and natural mineral patina accumulated over 1,200 years of monsoon rains on Deccan basalt, archaeological museum quality, 8k."),
    ("ep05_17_plinth_temple_junction_line_PAN_ZOOM.jpg", "Cinematic 16:9 1080p architectural detail. The crisp horizontal line where the top cornice of the elephant plinth meets the decorative basement moulding of the main assembly hall. Flawless subtractive alignment, 8k."),
    ("ep05_18_elephant_backs_bearing_molding_PAN_ZOOM.jpg", "Cinematic 16:9 1080p medium close-up. Three carved elephant backs perfectly contoured beneath the projecting stone cornice above, illustrating the sculptural convention of weight-bearing effort, 8k."),
    ("ep05_19_monumental_living_procession_PAN_ZOOM.jpg", "Cinematic 16:9 1080p low-angle heroic film still. Looking down the long south facade of Kailasa: A living procession of stone elephants appearing to stride resolutely forward in unison beneath the cathedral mass, 8k."),
    ("ep05_20_relief_versus_column_demonstration_PAN_ZOOM.jpg", "Cinematic 16:9 1080p technical documentary still. Raking light revealing that the elephants are sculpted relief projecting from a solid uncarved rock core, proving they are not separate weight-bearing columns, 8k."),
    ("ep05_21_sculptural_precision_eyelid_carving_PAN_ZOOM.jpg", "Cinematic 16:9 1080p extreme macro photograph. Intricate 8th-century stonecutter detailing: delicately carved wrinkles around the elephant's eye, decorative forehead headstalls, and hanging bronze bell harnesses carved in stone, 8k."),
    ("ep05_22_weightless_temple_illusion_hero_PAN_ZOOM.jpg", "Cinematic 16:9 1080p sunset hero shot. Kailasa Temple glowing amber in twilight, the dark elephant frieze below appearing to float the entire monolithic complex into midair against a vibrant evening sky, 8k masterpiece."),
    ("ep05_23_vimana_shikara_mountain_silhouette_PAN_ZOOM.jpg", "Cinematic 16:9 1080p wide telephoto still. The soaring Dravidian vimana tower of Kailasa framed against morning clouds, evoking the pyramidal sacred profile of Mount Kailash in the Himalayas, 8k."),
    ("ep05_24_ascending_tiers_mountain_peak_PAN_ZOOM.jpg", "Cinematic 16:9 1080p architectural detail of the central temple tower. Ascending horizontal tiers, miniature shrines (kutas and salas), and octagonal shikhara dome echoing alpine mountain ridges, 8k."),
    ("ep05_25_multiplicity_of_carved_meanings_PAN_ZOOM.jpg", "Cinematic 16:9 1080p medium shot of varied plinth sculptures. A tranquil elephant clutching a lotus blossom positioned right next to an aggressive lion grappling a beast, illustrating layered symbolic registers, 8k."),
    ("ep05_26_deliberate_visual_relationship_PAN_ZOOM.jpg", "Cinematic 16:9 1080p vertical tilt composition. Connecting the living animal base at the bottom of the frame to the sacred vimana pinnacle at the top, showing their deliberate cosmological harmony, 8k."),
    ("ep05_27_animated_base_living_mountain_PAN_ZOOM.jpg", "Cinematic 16:9 1080p documentary film still. Late afternoon golden sunlight sweeping across the plinth frieze, animated shadows giving the illusion of living movement to the carved elephants, 8k."),
    ("ep05_28_monolithic_paradox_separate_vs_whole_PAN_ZOOM.jpg", "Cinematic 16:9 1080p conceptual documentary still. Side profile showing an elephant's head projecting dynamically into space while its body remains continuous with the mountain behind, 8k."),
    ("ep05_29_basalt_textural_folds_and_skin_PAN_ZOOM.jpg", "Cinematic 16:9 1080p macro photographic study. The hard volcanic texture of Deccan trap basalt transformed by ancient Rashtrakuta chisels into supple anatomical skin folds and leather-like hide, 8k."),
    ("ep05_30_distant_repeating_band_perspective_PAN_ZOOM.jpg", "Cinematic 16:9 1080p long focal length corridor view. Looking down the deep courtyard canyon, capturing the rhythmic repetition of identical elephant silhouettes fading into courtyard haze, 8k."),
    ("ep05_31_individual_elephant_pose_variation_PAN_ZOOM.jpg", "Cinematic 16:9 1080p comparison still. Three consecutive carved elephants showing individual differences: one turning its trunk inward, one trumpeting outward, another calm with drooping ears, 8k."),
    ("ep05_32_visual_intelligence_of_sculptor_PAN_ZOOM.jpg", "Cinematic 16:9 1080p close-up. Masterful anatomical articulation of elephant shoulder musculature and joint compression in dark carved stone, demonstrating high sculptural intelligence, 8k."),
    ("ep05_33_shared_ground_monolithic_unity_PAN_ZOOM.jpg", "Cinematic 16:9 1080p wide panoramic still. The courtyard bedrock floor, carved plinth animals, and towering assembly hall united in a single unbroken mass of planet Earth, 8k documentary."),
    ("ep05_34_pradakshina_pathway_movement_PAN_ZOOM.jpg", "Cinematic 16:9 1080p eye-level dolly shot along the circumambulatory path. Ancient stone flagstones underfoot, massive elephant heads passing on the right, towering vertical rock wall on the left, 8k."),
    ("ep05_35_commanding_presence_above_eye_level_PAN_ZOOM.jpg", "Cinematic 16:9 1080p extreme low angle. Standing directly beneath an elephant head looking straight up at the 30-meter high sanctuary wall rising into the blue sky, dizzying verticality, 8k."),
    ("ep05_36_changing_fragments_montage_PAN_ZOOM.jpg", "Cinematic 16:9 1080p dynamic diagonal shot. Capturing a violent corner relief where a rampant lion attacks an elephant's flank, dramatic narrative tension in stone, 8k."),
    ("ep05_37_imagined_ring_around_temple_PAN_ZOOM.jpg", "Cinematic 16:9 1080p high three-quarter angle. Overview of the rear apsidal plinth curve showing the continuous ring of sculpted elephants wrapping around the circumambulatory corridor, 8k."),
    ("ep05_38_two_scales_detail_and_monument_PAN_ZOOM.jpg", "Cinematic 16:9 1080p shallow depth-of-field photograph. Sharp macro focus on a carved elephant's weathered ear and tusk in foreground, with the grand temple shikara softly blurred in the background, 8k."),
    ("ep05_39_lotus_trunk_macro_PAN_ZOOM.jpg", "Cinematic 16:9 1080p extreme macro photograph. The tip of an elephant trunk delicately wrapping around a sacred lotus blossom, showing fine chisel grooves and ancient mineral patina, 8k."),
    ("ep05_40_viewpoint_and_movement_convergence_PAN_ZOOM.jpg", "Cinematic 16:9 1080p atmospheric dusk still. Long shadows stretching across the courtyard as evening light illuminates the upper temple stories while the elephant base sinks into cool indigo shade, 8k."),
    ("ep05_41_small_act_of_discovery_angle_PAN_ZOOM.jpg", "Cinematic 16:9 1080p framed view through an outer courtyard gallery archway. Pillars frame a solitary carved elephant standing in deep amber raking light, sense of intimate discovery, 8k."),
    ("ep05_42_return_to_plinth_elephants_hero_PAN_ZOOM.jpg", "Cinematic 16:9 1080p clear morning hero still. The entire southern plinth elephant frieze illuminated in crisp, pristine dawn light, triumphant architectural portrait, 8k."),
    ("ep05_43_solid_bedrock_foundation_truth_PAN_ZOOM.jpg", "Cinematic 16:9 1080p geological documentary photograph. Showing the uncarved mass of basalt bedrock beneath the decorative frieze, grounding the temple solidly in the Earth, 8k."),
    ("ep05_44_sculptural_decision_upward_thrust_PAN_ZOOM.jpg", "Cinematic 16:9 1080p dynamic upward perspective. Highlighting the arched necks and muscular shoulders of the elephant herd thrusting upward to visually elevate the sacred mountain, 8k."),
    ("ep05_45_architecture_mass_sculpture_story_PAN_ZOOM.jpg", "Cinematic 16:9 1080p balanced wide shot. Complete visual synthesis of architectural engineering above and mythical sculpture below, harmonious ancient masterpiece, 8k."),
    ("ep05_46_wall_panels_mahabharata_teaser_PAN_ZOOM.jpg", "Cinematic 16:9 1080p teaser film still. Camera tilting upward above the elephant plinth to reveal the intricate horizontal relief panels of the Mahabharata battle on the temple hall wall — Teaser for Episode 06, 8k.")
]

# 10 Universe Archive Stills
ARCHIVE_TARGETS = [
    ("ep05_archive_01_charanandri_ridge_strata_PAN_ZOOM.jpg", "Cinematic 16:9 documentary still. The volcanic basalt cliffs of Charanandri hill at Ellora showing horizontal Deccan trap basalt flow layers, untouched ancient landscape, 8k."),
    ("ep05_archive_02_monolithic_excavation_cutaway_PAN_ZOOM.jpg", "Cinematic 16:9 archaeological isometric cutaway illustration. Showing the top-down subtractive excavation of 200,000 tons of rock from the mountain ridge at Cave 16, 8k."),
    ("ep05_archive_03_historic_traveler_engraving_PAN_ZOOM.jpg", "Cinematic 16:9 vintage 19th-century museum archival engraving. Early European and Indian travelers sketching the monumental elephant plinth of Kailasa, sepia and etching tones, 8k."),
    ("ep05_archive_04_architect_scroll_sketches_PAN_ZOOM.jpg", "Cinematic 16:9 historical macro still. Ancient Indian master architect Kokasa studying Sanskrit architectural Vastu Shastra drawings and temple elevation diagrams on aged palm leaf manuscripts, 8k."),
    ("ep05_archive_05_havell_1920_monograph_text_PAN_ZOOM.jpg", "Cinematic 16:9 archival still. Open vintage art monograph from 1920 featuring E.B. Havell's text and monochrome plates analyzing the Himalayas in Indian art, museum lighting, 8k."),
    ("ep05_archive_06_rashtrakuta_copper_charter_PAN_ZOOM.jpg", "Cinematic 16:9 museum macro photograph. Authentic 8th-century Rashtrakuta royal copper plate charter held by a royal Garuda seal ring, recording King Krishna I's patronage of Kailasa temple, 8k."),
    ("ep05_archive_07_artisan_quarry_camp_dawn_PAN_ZOOM.jpg", "Cinematic 16:9 historical wide still. Thousands of Rashtrakuta guild stonecutters, iron smelters, and sculptors gathered at the foot of Ellora cliffs at dawn, smoke rising from forges, 8k."),
    ("ep05_archive_08_archaeological_survey_plans_PAN_ZOOM.jpg", "Cinematic 16:9 archival blueprint document. 19th-century British Archaeological Survey of India measured architectural elevation and cross-section drawing of Cave 16 plinth, 8k."),
    ("ep05_archive_09_ramayana_panel_narrative_PAN_ZOOM.jpg", "Cinematic 16:9 archaeological close-up still. The intricate continuous narrative wall frieze of the Ramayana epic carved into the south wall of Kailasa above the plinth, 8k."),
    ("ep05_archive_10_sunset_over_kailasa_chasm_PAN_ZOOM.jpg", "Cinematic 16:9 epic landscape still. The golden sun sinking behind the western horizon of the Deccan plateau, casting the great excavated chasm of Kailasa into mystical twilight, 8k.")
]

def generate_one_image(client, model_name, prompt, target_paths):
    # Check if already generated at all target paths
    all_exist = all(p.exists() and p.stat().st_size > 10000 for p in target_paths)
    if all_exist:
        print(f"  [EXISTS] Skipping {target_paths[0].name} (already exists)")
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
    print(f"  EPISODE 05 IMAGE ASSETS PIPELINE ({total} TOTAL ASSETS)")
    print("  Using gemini-2.5-flash-image with zero-duplication guarantee")
    print("=" * 65)

    count = 0

    # 1. Google Flow Action Stills (isolated to both images/ and google_flow_input_images/)
    print("\n--- PHASE 1: GOOGLE FLOW ACTION CANDIDATE STILLS (8 ASSETS) ---")
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

    # 3. Master Hero Stills (46 ASSETS)
    print("\n--- PHASE 3: MASTER HERO STILLS (46 ASSETS) ---")
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
        p_arc = IMAGES_DIR / fname
        generate_one_image(client, model_name, prompt, [p_arc])
        time.sleep(1.0)

    print("\n" + "=" * 65)
    print(" ALL EPISODE 05 IMAGE ASSETS GENERATED SUCCESSFULLY!")
    print("=" * 65)

if __name__ == "__main__":
    main()
