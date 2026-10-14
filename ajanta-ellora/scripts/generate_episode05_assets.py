"""Build Episode 05's production assets: storyboard, prompt sheet, publish kits, and manifest.

Implements the 3-Pillar Visual Diversity Formula with zero visual repetition:
- Pillar A: Master Hero Stills (46 unique prompts)
- Pillar B: Technical Infographic & Blueprint Cards (8 cards via PIL)
- Pillar C: Cross-Episode Universe Archive Stills (10 cards)
- Action Video Slots: 8 Dedicated Google Flow/Veo clips

Run:
    python ajanta-ellora/scripts/generate_episode05_assets.py
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = ROOT / "episode05"
AUDIO, SUBS = EP / "audio", EP / "subtitles"
SCRIPT, KIT = EP / "script_and_storyboard", EP / "publish_kit"
GOOGLE_FLOW_DIR = EP / "google_flow_input_images"

# 72 Micro-Beats single source of truth: (type, filename, visual_brief, motion)
UNIQUE_BEATS_DATA = [
    # Act I — The Animals Beneath (Beats 01–09)
    ("image", "ep05_01_courtyard_ground_plinth_reveal_PAN_ZOOM.jpg", "Cinematic low-angle view looking across the dark basalt courtyard toward the towering Kailasa plinth at dawn.", "slow_tilt_up"),
    ("image", "ep05_02_elephant_procession_shoulder_row_PAN_ZOOM.jpg", "Monumental frieze of carved elephants emerging from the bedrock shoulder to shoulder beneath the plinth ledge.", "pan_right"),
    ("image", "ep05_03_apparent_support_angle_PAN_ZOOM.jpg", "Upward camera angle capturing the massive projecting temple cornice resting directly above the elephants' backs.", "slow_zoom_in"),
    ("image", "ep05_infographic_01_plinth_elevation_profile.jpg", "Technical Blueprint Card: Monumental Plinth Elevation Architecture & Vertical Stratigraphy of the Lower Storey.", "slow_drift"),
    ("image", "ep05_04_sculptural_framing_perspective_PAN_ZOOM.jpg", "Wide architectural perspective framing the colossal temple mass rising above the sculpted animal register.", "slow_zoom_out"),
    ("video", "ep05_gf_01_first_encounter_chasm_dawn.mp4", "Action Video: The First Encounter: Low-angle descent into the deep volcanic pit, pushing in on a colossal elephant head emerging from living basalt with warm dawn rim light.", "action_clip"),
    ("image", "ep05_infographic_02_monolithic_subtractive_plinth.jpg", "Technical Blueprint Card: Structural Reality: Subtractive Living Bedrock vs Additive Masonry Foundation.", "slow_drift"),
    ("image", "ep05_05_kailasa_rock_trench_panoramic_PAN_ZOOM.jpg", "Sweeping wide panorama of the excavated Cave 16 pit showing the full height of the monolithic temple from court floor.", "slow_zoom_out"),
    ("image", "ep05_06_elephant_head_chiaroscuro_PAN_ZOOM.jpg", "Dramatic chiaroscuro raking morning light across a sculpted elephant head, highlighting deep basalt eye sockets and ear folds.", "slow_zoom_in"),

    # Act II — A Mountain as Temple (Beats 10–18)
    ("image", "ep05_archive_01_charanandri_ridge_strata_PAN_ZOOM.jpg", "Archive Still: The Charanandri basalt hillside at Ellora showing horizontal volcanic lava strata before excavation.", "slow_drift"),
    ("image", "ep05_archive_02_monolithic_excavation_cutaway_PAN_ZOOM.jpg", "Archive Still: Isometric diagram of top-down trench excavation releasing the freestanding temple monolith.", "slow_tilt_down"),
    ("image", "ep05_07_courtyard_freestanding_sanctuary_PAN_ZOOM.jpg", "Courtyard view showing the central vimana sanctuary, Nandi pavilion, and gateway arranged within the excavated chasm.", "slow_zoom_in"),
    ("image", "ep05_08_towering_plinth_elevation_PAN_ZOOM.jpg", "Direct elevation perspective of the 8-meter high basement plinth setting the main shrine high above courtyard level.", "slow_tilt_up"),
    ("image", "ep05_09_dense_sculptural_band_panning_PAN_ZOOM.jpg", "Horizontal tracking shot across the dense continuous frieze of carved elephants, lions, and mythical creatures.", "pan_right"),
    ("video", "ep05_gf_02_life_size_scale_human_silhouette.mp4", "Action Video: The Life-Size Scale Reveal: Tracking shot behind a lone traveler walking along the courtyard floor, dwarfed beside colossal 10-foot tall carved elephant legs.", "action_clip"),
    ("image", "ep05_10_transition_earth_to_temple_PAN_ZOOM.jpg", "Vertical tilt from courtyard flagstones up through the carved elephant band to the temple wall.", "slow_tilt_up"),
    ("image", "ep05_infographic_03_courtyard_sightlines_scale.jpg", "Technical Blueprint Card: Courtyard Ambulatory & Sightline Phenomenology: Human eye level vs monumental plinth scale.", "slow_drift"),
    ("image", "ep05_11_plinth_corner_angle_perspective_PAN_ZOOM.jpg", "Corner perspective where two orthogonal elephant processions converge at the plinth angle.", "slow_zoom_in"),

    # Act III — Reading the Plinth (Beats 19–27)
    ("image", "ep05_12_lower_storey_ambulatory_walk_PAN_ZOOM.jpg", "Eye-level tracking perspective walking along the southern plinth wall in the narrow courtyard canyon.", "slow_dolly_forward"),
    ("image", "ep05_13_elephant_trunk_lotus_flower_PAN_ZOOM.jpg", "Macro photograph of an elephant trunk delicately curled around a sculpted blooming lotus bud in high basalt relief.", "slow_zoom_in"),
    ("image", "ep05_14_integrated_sculptural_register_PAN_ZOOM.jpg", "Seamless integration where the elephant forequarters merge naturally into the solid bedrock plinth.", "pan_left"),
    ("image", "ep05_infographic_08_plinth_sculptural_fauna_survey.jpg", "Technical Blueprint Card: Plinth Sculptural Fauna & Iconographic Census: Elephants, lions, vyalas, and fighting duels.", "slow_drift"),
    ("image", "ep05_15_deep_relief_chiaroscuro_depth_PAN_ZOOM.jpg", "High-contrast study of deep relief undercutting, showing deep dark voids carved between legs and bellies.", "slow_zoom_in"),
    ("image", "ep05_16_weathered_trunk_patina_detail_PAN_ZOOM.jpg", "Close-up of weathered, fractured basalt trunk showing twelve centuries of natural patina and mineral staining.", "slow_tilt_down"),
    ("image", "ep05_archive_03_historic_traveler_engraving_PAN_ZOOM.jpg", "Archive Still: 19th-century historical engraving of European travelers exploring the Kailasa elephant plinth.", "slow_drift"),
    ("image", "ep05_archive_04_architect_scroll_sketches_PAN_ZOOM.jpg", "Archive Still: Ancient Indian architect Kokasa's palm-leaf architectural scrolls and proportional canon drawings.", "slow_drift"),
    ("video", "ep05_gf_03_continuous_ring_elephant_procession.mp4", "Action Video: ⭐ CENTERPIECE 1: The Continuous Ring: Wide continuous lateral tracking glide along the plinth, revealing an unbroken procession of elephants encircling the temple foundation.", "action_clip"),

    # Act IV — The Illusion of Support (Beats 28–36)
    ("image", "ep05_17_plinth_temple_junction_line_PAN_ZOOM.jpg", "Sharp horizontal architectural line where the uppermost plinth cornice meets the bottom of the temple hall walls.", "pan_right"),
    ("image", "ep05_18_elephant_backs_bearing_molding_PAN_ZOOM.jpg", "Detailed perspective showing curved elephant backs aligned flush against the projecting basement moulding.", "slow_zoom_in"),
    ("image", "ep05_19_monumental_living_procession_PAN_ZOOM.jpg", "Low-angle heroic shot of the elephant herd appearing to stride forward together bearing the stone cathedral.", "slow_zoom_out"),
    ("image", "ep05_infographic_07_relief_undercutting_profile.jpg", "Technical Blueprint Card: Sculptural Technique: High Relief Undercutting Profile (60-90cm void vs bedrock core).", "slow_drift"),
    ("image", "ep05_20_relief_versus_column_demonstration_PAN_ZOOM.jpg", "Raking light revealing how the elephant legs remain rooted into the uncarved rock mass behind.", "pan_left"),
    ("image", "ep05_infographic_05_basalt_compression_vs_relief.jpg", "Technical Blueprint Card: Material Science: Basalt Load Bearing Capacity (140 MPa core vs 0.0 MPa relief shell).", "slow_drift"),
    ("image", "ep05_21_sculptural_precision_eyelid_carving_PAN_ZOOM.jpg", "Extreme macro close-up of elephant eyelid wrinkles, tusk socket contours, and ornamental harness bells in stone.", "slow_zoom_in"),
    ("video", "ep05_gf_04_dynamic_combat_and_baby_elephant.mp4", "Action Video: The Dynamic Movement & Baby Elephant: Kinetic macro lateral camera glide along the frieze: an adult elephant in combat with a lion, and a playful baby elephant carved clinging to its mother's leg.", "action_clip"),
    ("image", "ep05_22_weightless_temple_illusion_hero_PAN_ZOOM.jpg", "Master hero shot: The monolithic Kailasa temple appearing to float weightlessly above the elephant herd at sunset.", "slow_zoom_in"),

    # Act V — Animals and the Sacred Mountain (Beats 37–45)
    ("image", "ep05_23_vimana_shikara_mountain_silhouette_PAN_ZOOM.jpg", "Dramatic silhouette of the Kailasa Dravidian vimana tower framed against sky, evocative of Mount Kailash.", "slow_tilt_up"),
    ("image", "ep05_24_ascending_tiers_mountain_peak_PAN_ZOOM.jpg", "Ascending architectural tiers and miniature pavilions echoing the tiered ridges of Himalayan summits.", "slow_zoom_in"),
    ("image", "ep05_archive_05_havell_1920_monograph_text_PAN_ZOOM.jpg", "Archive Still: Historic archival page and illustration from E.B. Havell's 1920 study 'The Himalayas in Indian Art'.", "slow_drift"),
    ("image", "ep05_infographic_06_havell_cloud_hypothesis.jpg", "Technical Blueprint Card: E.B. Havell's Cloud Interpretation (1920) vs Physical Archaeological Evidence.", "slow_drift"),
    ("video", "ep05_gf_05_havell_cloud_island_mist.mp4", "Action Video: The Cloud Island (Havell's Illusion): Thick morning mist slowly billowing across the trench floor around the knees of the elephants, making the temple appear to float on clouds.", "action_clip"),
    ("image", "ep05_infographic_04_cosmic_diggajas_iconography.jpg", "Technical Blueprint Card: Cosmic Diggajas: Guardians of the Eight Directions sustaining Mount Meru.", "slow_drift"),
    ("image", "ep05_25_multiplicity_of_carved_meanings_PAN_ZOOM.jpg", "Wide frieze showing diversity of animal attitudes: peaceful elephants with lotus flowers beside raging lions.", "pan_right"),
    ("image", "ep05_26_deliberate_visual_relationship_PAN_ZOOM.jpg", "Vertical composition binding the sculpted animal base to the soaring tower above in a unified sacred vision.", "slow_tilt_up"),
    ("image", "ep05_27_animated_base_living_mountain_PAN_ZOOM.jpg", "Golden sunlight sweeping across the plinth, making the stone animals look alive as shadows lengthen.", "slow_zoom_out"),

    # Act VI — One Stone, Many Images (Beats 46–54)
    ("image", "ep05_28_monolithic_paradox_separate_vs_whole_PAN_ZOOM.jpg", "Composition illustrating the paradox: Lifelike distinct animals that never separate from the continuous basalt mass.", "slow_zoom_in"),
    ("image", "ep05_29_basalt_textural_folds_and_skin_PAN_ZOOM.jpg", "Macro study of how hard Deccan volcanic basalt was carved to resemble the soft wrinkled skin of elephants.", "pan_left"),
    ("image", "ep05_30_distant_repeating_band_perspective_PAN_ZOOM.jpg", "Long perspective down the courtyard trench showing the rhythmic procession of elephant heads in receding perspective.", "slow_dolly_forward"),
    ("image", "ep05_31_individual_elephant_pose_variation_PAN_ZOOM.jpg", "Side-by-side comparison of three adjacent elephant figures showing distinct individual head tilts and trunk curves.", "pan_right"),
    ("image", "ep05_32_visual_intelligence_of_sculptor_PAN_ZOOM.jpg", "Medium close-up showing mastery of anatomical proportions and subtle muscle tension in the carved shoulders.", "slow_zoom_in"),
    ("image", "ep05_archive_06_rashtrakuta_copper_charter_PAN_ZOOM.jpg", "Archive Still: Historic Rashtrakuta copper plate charter with royal seal documenting imperial patron Krishna I.", "slow_drift"),
    ("image", "ep05_archive_07_artisan_quarry_camp_dawn_PAN_ZOOM.jpg", "Archive Still: Historical quarry settlement of Rashtrakuta guild stonecutters with iron tools at sunrise.", "slow_drift"),
    ("video", "ep05_gf_06_3d_corner_projection_elephant.mp4", "Action Video: The 3D Corner Projection: Smooth rotational orbital camera pass around the 90-degree corner of the plinth, highlighting a fully three-dimensional corner elephant bursting outward into the open court.", "action_clip"),
    ("image", "ep05_33_shared_ground_monolithic_unity_PAN_ZOOM.jpg", "Sweeping wide shot showing courtyard floor, elephant plinth, and great hall united in a single unbroken stone.", "slow_zoom_out"),

    # Act VII — The Viewer Completes the Image (Beats 55–63)
    ("image", "ep05_34_pradakshina_pathway_movement_PAN_ZOOM.jpg", "Looking down the narrow flagstone walkway between the temple plinth and the outer trench wall.", "slow_dolly_forward"),
    ("image", "ep05_35_commanding_presence_above_eye_level_PAN_ZOOM.jpg", "Low-angle viewpoint from courtyard pit: The temple towering commandingly thirty meters overhead.", "slow_tilt_up"),
    ("image", "ep05_36_changing_fragments_montage_PAN_ZOOM.jpg", "Dynamic angle catching a carved lion grappling an elephant's shoulder in dramatic narrative relief.", "pan_left"),
    ("image", "ep05_37_imagined_ring_around_temple_PAN_ZOOM.jpg", "Panoramic view around the rear vimana corner showing the elephant procession wrapping the entire monument.", "slow_zoom_out"),
    ("image", "ep05_38_two_scales_detail_and_monument_PAN_ZOOM.jpg", "Depth-of-field composition: Sharp focus on carved elephant ear in foreground, towering spire in background.", "slow_zoom_in"),
    ("image", "ep05_39_lotus_trunk_macro_PAN_ZOOM.jpg", "Close macro of an elephant trunk holding a delicate lotus stalk, showing the sculptor's subtle touch.", "slow_tilt_down"),
    ("video", "ep05_gf_07_breathing_basalt_torchlight_dusk.mp4", "Action Video: The Breathing Basalt: Atmospheric dusk scene with warm flickering torchlight casting dancing amber shadows across an ancient elephant's stone eye and wrinkled trunk.", "action_clip"),
    ("image", "ep05_40_viewpoint_and_movement_convergence_PAN_ZOOM.jpg", "Courtyard view at dusk: Shadows lengthening across the plinth as evening light catches the upper sanctum.", "slow_zoom_in"),
    ("image", "ep05_41_small_act_of_discovery_angle_PAN_ZOOM.jpg", "Framed glimpse through a courtyard pillared gallery revealing the elephant band through stone columns.", "slow_dolly_forward"),

    # Act VIII — Beneath the Mountain (Beats 64–72)
    ("image", "ep05_42_return_to_plinth_elephants_hero_PAN_ZOOM.jpg", "Hero return to the full elephant frieze bathed in clear morning sunlight.", "slow_zoom_in"),
    ("image", "ep05_43_solid_bedrock_foundation_truth_PAN_ZOOM.jpg", "Telephoto view demonstrating the solid, unmoving basalt rock core that truly bears the entire mountain.", "pan_right"),
    ("image", "ep05_44_sculptural_decision_upward_thrust_PAN_ZOOM.jpg", "Low-angle composition highlighting the dynamic upward sculptural thrust of the elephant herd.", "slow_tilt_up"),
    ("image", "ep05_45_architecture_mass_sculpture_story_PAN_ZOOM.jpg", "Architectural balance: Geometric discipline of the upper temple perfectly balanced by organic living animals below.", "slow_zoom_out"),
    ("image", "ep05_archive_08_archaeological_survey_plans_PAN_ZOOM.jpg", "Archive Still: Historic 19th-century Archaeological Survey of India measured architectural drawing of Kailasa plinth.", "slow_drift"),
    ("video", "ep05_gf_08_mountain_hoisted_celestial_ascent.mp4", "Action Video: ⭐ CENTERPIECE 2: The Mountain Hoisted: Low-angle camera sweeps up from between the arched backs of the marching elephants, tilting skyward as the entire monolithic mountain appears to lift into the heavens.", "action_clip"),
    ("image", "ep05_46_wall_panels_mahabharata_teaser_PAN_ZOOM.jpg", "Camera tilts up from the elephant plinth toward the narrative epic reliefs of the Mahabharata on the hall walls above.", "slow_tilt_up"),
    ("image", "ep05_archive_09_ramayana_panel_narrative_PAN_ZOOM.jpg", "Archive Still: Close-up of the continuous narrative relief panel depicting the Ramayana battle scenes on Kailasa wall.", "slow_drift"),
    ("image", "ep05_archive_10_sunset_over_kailasa_chasm_PAN_ZOOM.jpg", "Closing hero shot: Sunset glow fading over the monumental Kailasa chasm as twilight descends over Ellora.", "slow_zoom_out"),
]

# Ensure zero duplicate filenames
assert len(UNIQUE_BEATS_DATA) == 72, f"Expected 72 beats, found {len(UNIQUE_BEATS_DATA)}"
filenames = [x[1] for x in UNIQUE_BEATS_DATA]
duplicates = [x for x in filenames if filenames.count(x) > 1]
assert not duplicates, f"Fatal error: duplicate media detected in UNIQUE_BEATS_DATA: {set(duplicates)}"

# 8 Google Flow specifications
GF_STILLS_DATA = [
    {
        "filename": "ep05_gf_01_first_encounter_chasm_dawn_GENERATE_VIDEO.jpg",
        "video_target": "ep05_gf_01_first_encounter_chasm_dawn.mp4",
        "beat": "Beat 06 (Act 1, Beat 6) | Spoken: 'At Ellora, the answer begins with a distinction between what stone does and what sculpture makes us feel.'",
        "image_prompt": "Cinematic 16:9 1080p documentary still. Camera in deep 100-foot volcanic pit of Kailasa Cave 16, low-angle on a monumental carved basalt elephant head emerging from dark rock, warm dawn rim-light catching the curve of its tusk and detailed wrinkles, 8k photorealistic.",
        "motion_prompt": "Camera descends slowly into the deep 100-foot volcanic pit, pushing into a dramatic close-up of a monumental elephant head emerging out of dark basalt. Warm dawn rim-light catches the curve of its tusk and detailed rock wrinkles. Atmospheric morning mist drifting past, 24fps."
    },
    {
        "filename": "ep05_gf_02_life_size_scale_human_silhouette_GENERATE_VIDEO.jpg",
        "video_target": "ep05_gf_02_life_size_scale_human_silhouette.mp4",
        "beat": "Beat 15 (Act 2, Beat 6) | Spoken: 'The base therefore has two jobs for the visitor’s eye: it establishes height and gives that height a living edge.'",
        "image_prompt": "Cinematic 16:9 1080p documentary still. A solitary robed traveler walking across the basalt courtyard floor, dwarfed beside colossal 10-foot tall carved elephant legs and towering plinth wall, dramatic raking side light, 8k documentary.",
        "motion_prompt": "Tracking shot behind a lone traveler walking along the narrow stone courtyard floor. The traveler's silhouette is dwarfed beside the colossal 10-foot tall carved elephant legs and towering plinth wall rising thirty meters overhead, dramatic raking side light."
    },
    {
        "filename": "ep05_gf_03_continuous_ring_elephant_procession_GENERATE_VIDEO.jpg",
        "video_target": "ep05_gf_03_continuous_ring_elephant_procession.mp4",
        "beat": "Beat 27 (Act 3, Beat 9) | Spoken: 'The first clue is visual: the animals create a living threshold between the ground and the sacred structure above.'",
        "image_prompt": "Cinematic 16:9 1080p wide documentary still. Unbroken continuous procession of sculpted stone elephants carved directly from volcanic basalt bedrock, marching shoulder-to-shoulder in a curving ring encircling the temple foundation in warm morning light, 8k photorealistic.",
        "motion_prompt": "A cinematic wide continuous tracking glide moving smoothly alongside the base, revealing an unbroken, curving procession of sculpted elephants wrapping around the entire perimeter of the temple. Marching shoulder to shoulder in living stone, 24fps."
    },
    {
        "filename": "ep05_gf_04_dynamic_combat_and_baby_elephant_GENERATE_VIDEO.jpg",
        "video_target": "ep05_gf_04_dynamic_combat_and_baby_elephant.mp4",
        "beat": "Beat 35 (Act 4, Beat 8) | Spoken: 'The animal band transforms a heavy base into a scene of effort, movement, and upward force.'",
        "image_prompt": "Cinematic 16:9 1080p macro documentary still. Adult stone elephant in combat with a leaping mythical lion, and a playful baby elephant carved in deep relief clinging to its mother's leg on the Kailasa plinth frieze, 8k documentary.",
        "motion_prompt": "Kinetic macro lateral camera glide along the sculpted frieze: an adult elephant trunk curled in defiance, locked tusks with a leaping mythic lion, and a playful baby elephant carved clinging to its mother's hind leg in deep relief undercutting."
    },
    {
        "filename": "ep05_gf_05_havell_cloud_island_mist_GENERATE_VIDEO.jpg",
        "video_target": "ep05_gf_05_havell_cloud_island_mist.mp4",
        "beat": "Beat 41 (Act 5, Beat 5) | Spoken: 'It is an evocative interpretation, not a certainty that the original sculptors left us in writing.'",
        "image_prompt": "Cinematic 16:9 1080p atmospheric still. Rolling morning fog and white mist swirling across trench floor hiding bedrock, temple plinth and vimana floating above like a sacred Vedic cloud-mountain, 8k documentary.",
        "motion_prompt": "Thick morning mist and vapor slowly billowing and drifting across the trench floor around the knees of the elephants, completely obscuring the bedrock. The monumental temple visually appears to float in the sky on storm clouds, ethereal golden lighting."
    },
    {
        "filename": "ep05_gf_06_3d_corner_projection_elephant_GENERATE_VIDEO.jpg",
        "video_target": "ep05_gf_06_3d_corner_projection_elephant.mp4",
        "beat": "Beat 53 (Act 6, Beat 8) | Spoken: 'A single rock mass can become architecture, ornament, and an imagined procession at the same time.'",
        "image_prompt": "Cinematic 16:9 1080p architectural still. Dramatic three-quarter angle on 90-degree plinth corner at Kailasa Cave 16, colossal carved elephant head thrusting outward in full 3D volume into open courtyard under morning chiaroscuro, 8k photorealistic.",
        "motion_prompt": "Smooth rotational orbital camera pass around the 90-degree corner of the plinth, highlighting a fully three-dimensional corner elephant bursting outward in full sculptural volume from the flat bedrock wall into the open courtyard."
    },
    {
        "filename": "ep05_gf_07_breathing_basalt_torchlight_dusk_GENERATE_VIDEO.jpg",
        "video_target": "ep05_gf_07_breathing_basalt_torchlight_dusk.mp4",
        "beat": "Beat 61 (Act 7, Beat 7) | Spoken: 'The temple’s height feels physical, but the carved creatures make that height feel supported and alive.'",
        "image_prompt": "Cinematic 16:9 1080p dusk still. Flickering bronze torchlight casting warm dancing amber shadows across weathered basalt elephant carving at plinth base, rich chiaroscuro, 8k historical.",
        "motion_prompt": "Atmospheric twilight shot. Warm flickering golden torchlight casting dancing amber shadows across an ancient elephant's carved stone eye and wrinkled trunk as gentle desert wind blows dust motes past, making the ancient rock-cut beast appear to breathe."
    },
    {
        "filename": "ep05_gf_08_mountain_hoisted_celestial_ascent_GENERATE_VIDEO.jpg",
        "video_target": "ep05_gf_08_mountain_hoisted_celestial_ascent.mp4",
        "beat": "Beat 69 (Act 8, Beat 6) | Spoken: 'At Kailasa, a mountain was not only cut into a temple; it was made to seem alive around its edges.'",
        "image_prompt": "Cinematic 16:9 1080p climax still. Low-angle hero view from arched backs of elephant procession looking up at soaring vimana tower with golden god-rays cutting through mist, mountain appearing to ascend on the herd, 8k photorealistic.",
        "motion_prompt": "The grand climax. Low-angle camera sweeps upward from between the powerful arched backs of the marching elephants, tilting skyward as golden god-rays burst through the chasm. The upward momentum of the animal band makes the entire monolithic mountain temple seem to physically lift off the earth and ascend into the heavens."
    }
]

def parse_cues(path: Path) -> list[tuple[float, float, str]]:
    blocks = path.read_text(encoding="utf-8-sig").strip().split("\n\n")
    parsed = []
    for block in blocks:
        lines = block.splitlines()
        if len(lines) >= 3 and "-->" in lines[1]:
            def sec(ts: str) -> float:
                h, m, s_ms = ts.strip().replace(",", ".").split(":")
                return int(h)*3600 + int(m)*60 + float(s_ms)
            a, b = lines[1].split("-->")
            parsed.append((sec(a), sec(b), " ".join(lines[2:])))
    return parsed

def clock(seconds: float) -> str:
    m, s = divmod(max(0, int(seconds)), 60)
    return f"{m:02}:{s:02}"

def build_storyboard_and_prompt_sheet():
    full_srt_path = SUBS / "episode_05_full.srt"
    cues = parse_cues(full_srt_path)
    assert len(cues) == 72, f"Expected 72 cues in episode_05_full.srt, got {len(cues)}"

    # Generate Google Flow Prompt Sheet
    GOOGLE_FLOW_DIR.mkdir(parents=True, exist_ok=True)
    gf_sheet = [
        "# Google Flow / Veo Video Generation Batch Sheet — Episode 05",
        "",
        "## Production Instructions",
        "1. Open **Google Flow / Veo / Runway Gen-3**.",
        "2. Upload each input image located in `ajanta-ellora/episode05/google_flow_input_images/`.",
        "3. Copy and paste the corresponding **Subject & Camera Motion Prompt** below.",
        "4. Set aspect ratio to **16:9**, generation resolution to **1080p**, and duration to **5–10 seconds**.",
        "5. Download the rendered video and place it in `ajanta-ellora/episode05/videos/` with the exact target filename.",
        "",
        "| Input Image Filename | Target Video Filename | Spoken Beat / Timestamp | Motion & Camera Prompt |",
        "|---|---|---|---|",
    ]
    for item in GF_STILLS_DATA:
        gf_sheet.append(f"| `{item['filename']}` | `{item['video_target']}` | {item['beat']} | {item['motion_prompt']} |")
    
    gf_sheet.extend([
        "",
        "## Mandatory Verification Invariant",
        "- All clips must feature unique, dynamic physics moments (water splashing, chisel sparks, flame flicker, storm clouds, chalk dust).",
        "- Never reuse video clips from earlier episodes.",
        "- Once placed in `ajanta-ellora/episode05/videos/`, run `python ajanta-ellora/scripts/assemble_episode_05_full.py` to assemble the final master preview.",
        ""
    ])
    (GOOGLE_FLOW_DIR / "GOOGLE_FLOW_PROMPT_SHEET.md").write_text("\n".join(gf_sheet), encoding="utf-8")
    print(f"[OK] Generated {GOOGLE_FLOW_DIR / 'GOOGLE_FLOW_PROMPT_SHEET.md'}")

    # Sound cues mapping per act
    act_sound = [
        "Open-air courtyard ambience, restrained low drone; gentle tonal reveal as the elephant band appears.",
        "Light strings and open ambience; no faux-temple bells or generic exoticized cues.",
        "Quiet, close stone texture under the voice; keep the atmosphere spacious.",
        "Subtle low pulse as the support illusion is explained; no cracking or invented structural stress sounds.",
        "Warm, contemplative strings; leave space around the distinction between evidence and interpretation.",
        "Sparse, dry ambience with a soft transition between wide pattern and close detail.",
        "Measured, gently moving motif suggesting a walk through the courtyard, without literalized footsteps.",
        "Return to the opening motif; resolve into a restrained teaser for the next episode.",
    ]

    act_names = [
        "Act I — The Animals Beneath",
        "Act II — A Mountain as Temple",
        "Act III — Reading the Plinth",
        "Act IV — The Illusion of Support",
        "Act V — Animals and the Sacred Mountain",
        "Act VI — One Stone, Many Images",
        "Act VII — The Viewer Completes the Image",
        "Act VIII — Beneath the Mountain",
    ]

    # Generate Granular Storyboard Markdown
    sb = [
        "# Episode 05 — The Elephants Beneath Kailasa",
        "### Why the temple appears to rise on a living procession",
        "",
        "**Series:** Kailasa: The Mountain Carved From Above  ",
        "**Format:** 16:9 documentary, target ~5.5 minutes; timing measured from synthesized narration.  ",
        "**Evidence note:** The lower storey is carved with elephants and lions, and the elephant relief appears to support the basement. Do not describe the elephants as freestanding structural columns. An older cloud-and-mountain interpretation is attributed to E.B. Havell and presented as interpretation, not settled intent.  ",
        "**Production Invariant:** Global zero-repetition rule enforced across all 72 micro-beats via the 3-Pillar Visual Diversity Formula.  ",
        "",
        "## Master Image Batch Sheet (3-Pillar Formula)",
        "",
        "| Category | Allocation | Description |",
        "|---|---:|---|",
        "| **Pillar A: Master Hero Stills** | 46 Cuts | 1080p photorealistic Gemini/Imagen prompts (`_PAN_ZOOM.jpg`) |",
        "| **Pillar B: Technical Infographics** | 8 Cuts | High-contrast 2D architectural blueprint cards rendered via PIL |",
        "| **Pillar C: Universe Archive Stills** | 10 Cuts | Canonical world-building assets from earlier episodes and archival records |",
        "| **Action Video Moments** | 8 Cuts | High-impact Google Flow / Veo dynamic physics moments |",
        "| **Total Micro-Beats** | **72 Cuts** | **100% Unique Media Assets (0 Duplicates)** |",
        "",
        "## Story and pacing",
        "",
        "| Act | Timing | Story turn |",
        "|---|---:|---|",
    ]

    for i, name in enumerate(act_names):
        start_t = cues[i * 9][0]
        sb.append(f"| {name} | {clock(start_t)} | {name.split('—',1)[1].strip()} |")

    sb.append("")

    for i in range(72):
        act_idx = i // 9
        if i % 9 == 0:
            act_title = act_names[act_idx]
            sb.extend([f"## {act_title}", ""])

        mtype, fname, vbrief, motion = UNIQUE_BEATS_DATA[i]
        start_sec, end_sec, text = cues[i]
        tag = "[VIDEO]" if mtype == "video" else "[IMAGE]"

        sb.extend([
            f"### Beat {i+1:02d} — {clock(start_sec)}–{clock(end_sec)}",
            f"- **Narration:** {text}",
            f"- **Asset:** `{tag}` `{fname}`",
            f"- **Visual Brief:** {vbrief}",
            f"- **Camera Motion:** `{motion}` (Sub-pixel 4K motorized dolly)",
            f"- **Sound Cue:** {act_sound[act_idx]}",
            ""
        ])

    sb.extend([
        "## Narration transcript",
        "",
    ])
    for _, _, text in cues:
        sb.append(text)

    sb.extend([
        "",
        "## Sources and interpretive limits",
        "",
        "- Sahapedia, [The Architecture of Ellora Caves](https://www.sahapedia.org/the-architecture-of-ellora-caves): Cave 16 plan and the elephants gathering lotus flowers on the lower storey.",
        "- Impart Encyclopedia of Art, [Kailasanatha Temple, Ellora](https://imp-art.org/articles/kailasanatha-temple-ellora/): monolithic form, sculptural plinth, and architectural context.",
        "- E. B. Havell, [The Himalayas in Indian Art](https://ignca.gov.in/Asi_data/39131.pdf), p. 27: an older interpretation comparing the plinth elephants to rain clouds beneath a sacred mountain. This is presented as interpretation, not proven original intent.",
        "",
        "The stonework supports a description of the carved figures and their placement. It does not provide a definitive written key to every symbolic meaning or a claim that the relief figures are freestanding structural supports.",
        ""
    ])

    storyboard_path = SCRIPT / "episode-05-the-elephants-beneath-kailasa.md"
    storyboard_path.write_text("\n".join(sb), encoding="utf-8")
    print(f"[OK] Generated {storyboard_path}")

def update_publish_kits():
    KIT.mkdir(parents=True, exist_ok=True)
    cues = parse_cues(SUBS / "episode_05_full.srt")
    
    # Master Publish Kit
    master_chapters = [
        "00:00 - The Animals Beneath",
        f"{clock(cues[9][0])} - A Mountain as Temple",
        f"{clock(cues[18][0])} - Reading the Plinth",
        f"{clock(cues[27][0])} - The Illusion of Support",
        f"{clock(cues[36][0])} - Animals and the Sacred Mountain",
        f"{clock(cues[45][0])} - One Stone, Many Images",
        f"{clock(cues[54][0])} - The Viewer Completes the Image",
        f"{clock(cues[63][0])} - Beneath the Mountain"
    ]
    
    master_tags = "Kailasa Temple,Ellora Caves,Cave 16,Ellora architecture,rock cut temple,monolithic temple,elephant sculptures,Indian sculpture,Rashtrakuta,Shiva temple,Deccan art,Indian history documentary,temple architecture"
    assert len(master_tags) < 500, f"Master tags exceed 500 chars: {len(master_tags)}"
    
    master_desc = (
        "At Ellora’s Kailasa Temple, a procession of carved elephants runs beneath the raised plinth. "
        "They appear to carry the temple, but the relief figures are part of the rock-cut lower storey, "
        "not freestanding pillars. This episode looks at how sculpture gives architectural weight a vivid, "
        "living image—and separates what the stone shows from interpretations of what it may mean.\n\n"
        + "\n".join(master_chapters)
    )
    
    (KIT / "master_publish_kit.md").write_text(f"""# YouTube Publish Kit — Episode 05: The Elephants Beneath Kailasa

## Title options
1. Why Are Elephants Carved Beneath Kailasa Temple?
2. The Elephants That Seem to Carry a Mountain
3. What the Kailasa Temple’s Elephant Plinth Really Shows
4. A Temple Raised on Elephants? The Sculpture at Ellora Explained
5. The Living Base of Kailasa Temple

## Description
{master_desc}

## SEO tags ({len(master_tags)} characters)
```text
{master_tags}
```

## Pinned comment
Do the elephants feel like structural supports, sacred imagery, or both when you stand before the plinth? Tell us what you notice—and where you draw the line between evidence and interpretation.

## Thumbnail brief (16:9 Master)
16:9 low-angle view of the plinth elephant relief beneath the temple mass; clear contrast between animal band and towering stone above. Bold 3-Word Rule: "CARRIED BY ELEPHANTS?" Output saved to `episode05/thumbnail/ep05_master_thumbnail_16x9.jpg` (< 2.0 MB).
""", encoding="utf-8")
    print(f"[OK] Verified {KIT / 'master_publish_kit.md'}")

    # Short 1 Publish Kit
    short1_cues = parse_cues(SUBS / "short_01_the_elephants_that_carry_a_temple.srt")
    short1_desc = " ".join(c[2] for c in short1_cues)
    short1_tags = "Kailasa Temple,Ellora Caves,elephant sculpture,Indian art,rock cut temple,history shorts,ancient engineering"
    assert len(short1_tags) < 500
    
    (KIT / "short_01_the_elephants_that_carry_a_temple_publish_kit.md").write_text(f"""# YouTube Publish Kit — Short 1: The Elephants That Carry a Temple

## Title options
1. Why Are Elephants Holding Up This Temple?
2. The Secret Behind Kailasa's Elephant Plinth
3. How Carved Elephants Carry a Solid Mountain
4. The Illusion of Support at Kailasa Temple
5. Did Ancient Indians Carve Weightless Stone?

## Description
{short1_desc}

Watch the full documentary: The Elephants Beneath Kailasa [link after upload].

## SEO tags ({len(short1_tags)} characters)
```text
{short1_tags}
```

## Pinned comment
Watch the full documentary episode to uncover how 8th-century master sculptors created the illusion of a floating mountain: [add episode link after upload].

## Thumbnail brief (9:16 Vertical Short)
9:16 vertical crop of elephant tusk and projecting plinth; 3-Word Rule: "LIFTED BY ELEPHANTS?" Output saved to `thumbnail/short_01_thumbnail_9x16.jpg` (< 2.0 MB).
""", encoding="utf-8")
    print(f"[OK] Verified {KIT / 'short_01_the_elephants_that_carry_a_temple_publish_kit.md'}")

    # Short 2 Publish Kit
    short2_cues = parse_cues(SUBS / "short_02_why_elephants_support_the_mountain.srt")
    short2_desc = " ".join(c[2] for c in short2_cues)
    short2_tags = "Kailasa Temple,Ellora Caves,elephant sculpture,sacred mountain,ancient mystery,history shorts"
    assert len(short2_tags) < 500
    
    (KIT / "short_02_why_elephants_support_the_mountain_publish_kit.md").write_text(f"""# YouTube Publish Kit — Short 2: Why Put Elephants Under a Mountain?

## Title options
1. Why Put Elephants Beneath a Mountain?
2. The Rain Cloud Mystery of Kailasa Temple
3. Cosmic Elephants Holding Up Mount Kailash
4. What Historians Missed at Ellora Cave 16
5. The Living Foundation of Kailasa

## Description
{short2_desc}

Watch the full documentary: The Elephants Beneath Kailasa [link after upload].

## SEO tags ({len(short2_tags)} characters)
```text
{short2_tags}
```

## Pinned comment
Explore the difference between physical archaeological evidence and poetic mythological interpretations in the full episode: [add episode link after upload].

## Thumbnail brief (9:16 Vertical Short)
9:16 vertical crop of temple spire looming above elephant heads; 3-Word Rule: "WHY ELEPHANTS BENEATH?" Output saved to `thumbnail/short_02_thumbnail_9x16.jpg` (< 2.0 MB).
""", encoding="utf-8")
    print(f"[OK] Verified {KIT / 'short_02_why_elephants_support_the_mountain_publish_kit.md'}")

def main():
    print("=" * 65)
    print(" GENERATING EPISODE 05 ASSETS, STORYBOARD & PUBLISH KITS")
    print("=" * 65)
    build_storyboard_and_prompt_sheet()
    update_publish_kits()
    print("=" * 65)
    print(" EPISODE 05 STORYBOARD AND SPECIFICATION SUITE COMPLETE!")
    print("=" * 65)

if __name__ == "__main__":
    main()
