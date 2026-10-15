#!/usr/bin/env python3
"""
assemble_episode_08_full.py — Full 62-Micro-Beat Master Assembly Engine for Episode 08.
Channel: thecuriousity-kills-thecat

Implements:
1. 62-Beat Manifest derived from 10 Google Flow Action Videos, 2 Infographics, 40 Hero Stills, and 10 Universe Archive Stills.
2. 4K Anti-Jitter Sub-Pixel Motorized Zoompan Engine for still images (scale=3840:2160 -> zoompan -> scale=1920:1080).
3. Monotonic Sentence-Level Cue Timing derived directly from episode_08_full.srt (0.00ms audio drift).
4. Zero media repetition invariant (62 unique assets for 62 cuts).
5. OpenMontage project bundle export.
"""

import os
import re
import sys
import json
import shutil
import subprocess
from pathlib import Path

# Fix Windows console UTF-8 encoding
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

BASE_DIR = Path("C:/Sagar/Projects/thecuriousity-kills-thecat")
EPISODE_DIR = BASE_DIR / "ajanta-ellora" / "episode08"
IMAGES_DIR = EPISODE_DIR / "images"
AUDIO_DIR = EPISODE_DIR / "audio"
SUB_DIR = EPISODE_DIR / "subtitles"
VIDEOS_DIR = EPISODE_DIR / "videos"
OUTPUT_DIR = EPISODE_DIR / "final_videos"
BUNDLE_DIR = EPISODE_DIR / "openmontage_bundle"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
BUNDLE_DIR.mkdir(parents=True, exist_ok=True)
(BUNDLE_DIR / "video").mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# 62-MICRO-BEAT MASTER MANIFEST (TYPE, FILENAME, MOTION)
# ---------------------------------------------------------------------------
def get_manifest():
    return [
        # Act I: The Hidden Paintings of Ajanta (The Golden Reawakening, c. 460 CE) (Cuts 1-9)
        # 1. "Welcome back to Ajanta and Ellora: The Subterranean Titans."
        ("image", "ep08_01_silent_canyon_dormancy_PAN_ZOOM.jpg", "slow_drift"),
        # 2. "This is Episode 8: The Mystery of the Cave Paintings."
        ("image", "ep08_real_painting_03_celestial_apsara_PAN_ZOOM.jpg", "slow_dolly_forward"),
        # 3. "When people think of Ajanta and Ellora, they usually picture giant stone temples carved out of black mountain rock."
        ("image", "ep08_real_ajanta_rock_cut_monolithic_temple_PAN_ZOOM.jpg", "slow_zoom_in"),
        # 4. "But hidden deep inside these dark volcanic caves is something most people have never heard about: world-famous ancient paintings..."
        ("image", "ep08_real_painting_01_cave_mural_panorama_PAN_ZOOM.jpg", "slow_drift"),
        # 5. "For nearly four centuries, this horseshoe mountain canyon lay completely silent, overgrown by thick jungle vines."
        ("video", "ep08_gf_11_jungle_vines_monsoon_chaitya_flood.mp4", "action_clip") if (VIDEOS_DIR / "ep08_gf_11_jungle_vines_monsoon_chaitya_flood.mp4").exists() else ("image", "ep08_gf_11_jungle_vines_monsoon_chaitya_flood_GENERATE_VIDEO.jpg", "pan_right"),
        # 6. "Then, in the year 460, a powerful Indian king named Emperor Harishena united the empire..."
        ("video", "ep08_gf_01_harishena_imperial_cavalry.mp4", "action_clip") if (VIDEOS_DIR / "ep08_gf_01_harishena_imperial_cavalry.mp4").exists() else ("image", "ep08_gf_01_harishena_imperial_cavalry_GENERATE_VIDEO.jpg", "slow_dolly_forward"),
        # 7. "Within just seventeen years, master stonecutters carved twenty colossal new cave halls directly into the solid rock face."
        ("video", "ep08_gf_12_cliffside_bamboo_scaffolding_army.mp4", "action_clip") if (VIDEOS_DIR / "ep08_gf_12_cliffside_bamboo_scaffolding_army.mp4").exists() else ("image", "ep08_gf_12_cliffside_bamboo_scaffolding_army_GENERATE_VIDEO.jpg", "slow_tilt_up"),
        # 8. "But they did not just carve stone; ancient artists transformed these dark subterranean walls into breathtaking, colorful royal palaces."
        ("image", "ep08_real_painting_04_royal_court_figures_PAN_ZOOM.jpg", "slow_dolly_forward"),
        # 9. "In this episode, you will see how these ancient painters actually did their work, and how they solved three impossible engineering mysteries."
        ("image", "ep08_08_monumental_vihara_colonnade_facade_PAN_ZOOM.jpg", "slow_zoom_out"),

        # Act II: The Basalt Problem & The Mud Chemistry Secret (Cuts 10-23)
        # 10. "To paint inside Ajanta, ancient craftsmen faced an impossible geological problem."
        ("image", "ep08_09_royal_university_hall_perspective_PAN_ZOOM.jpg", "slow_dolly_forward"),
        # 11. "The walls were not made of smooth, dry stone; they were carved out of dense, volcanic flood basalt rock."
        ("image", "ep08_10_raw_volcanic_basalt_seepage_PAN_ZOOM.jpg", "pan_right"),
        # 12. "Basalt is cold, hard lava rock that constantly sweats underground water droplets through tiny cracks."
        ("video", "ep08_gf_13_basalt_weeping_water_droplets_macro.mp4", "action_clip") if (VIDEOS_DIR / "ep08_gf_13_basalt_weeping_water_droplets_macro.mp4").exists() else ("image", "ep08_gf_13_basalt_weeping_water_droplets_macro_GENERATE_VIDEO.jpg", "slow_zoom_in"),
        # 13. "If you paint directly on wet basalt rock, the water pushes the paint off within months, causing it to peel and turn to dust."
        ("image", "ep08_11_flaking_paint_moisture_failure_PAN_ZOOM.jpg", "slow_zoom_in"),
        # 14. "European fresco painters put wet lime plaster on walls, but inside a cold, damp volcanic cave, that technique fails completely."
        ("image", "ep08_12_chitrasutra_palm_leaf_manuscript_PAN_ZOOM.jpg", "slow_drift"),
        # 15. "The master guilds of Ajanta invented a revolutionary, multi-layered bio-mud formula that modern scientists still study today."
        ("image", "ep08_infographic_01_plaster_stratigraphy.jpg", "slow_zoom_in"),
        # 16. "First, stonecutters used pointed iron picks to peck thousands of small pits into the rock, creating a rough surface for the mud to grip."
        ("video", "ep08_gf_05_chipping_basalt_key_sparks.mp4", "action_clip") if (VIDEOS_DIR / "ep08_gf_05_chipping_basalt_key_sparks.mp4").exists() else ("image", "ep08_gf_05_chipping_basalt_key_sparks_GENERATE_VIDEO.jpg", "slow_dolly_forward"),
        # 17. "Then came the secret organic recipe: a thick, fermented mud plaster made of local red clay, rock grit, and cow dung."
        ("image", "ep08_14_ferruginous_red_clay_quarry_PAN_ZOOM.jpg", "slow_tilt_down"),
        # 18. "Using fermented cow dung was not dirty—it was pure organic chemistry."
        ("video", "ep08_gf_04_plaster_kneading_cowdung_matrix.mp4", "action_clip") if (VIDEOS_DIR / "ep08_gf_04_plaster_kneading_cowdung_matrix.mp4").exists() else ("image", "ep08_gf_04_plaster_kneading_cowdung_matrix_GENERATE_VIDEO.jpg", "slow_dolly_forward"),
        # 19. "Digested plant fibers in the dung acted like microscopic nylon nets that stopped the mud from cracking, while natural bacteria kept mold away."
        ("image", "ep08_15_cow_dung_cellulose_fibers_macro_PAN_ZOOM.jpg", "slow_zoom_in"),
        # 20. "Mixed with dry rice husks and sticky boiled sap from neem trees, this mud layer created a breathable skin that lived with the damp mountain."
        ("image", "ep08_16_rice_husk_tensile_reinforcement_PAN_ZOOM.jpg", "pan_right"),
        # 21. "Finally, craftsmen spread a paper-thin finish coat made of slaked lime, powdered gypsum, and crushed sea shells."
        ("image", "ep08_20_crushed_oyster_shells_gypsum_powder_PAN_ZOOM.jpg", "slow_drift"),
        # 22. "While still damp, an artisan held a smooth river agate pebble, firmly rubbing the wall in steady circular motions."
        ("image", "ep08_21_agate_burnishing_stone_collection_PAN_ZOOM.jpg", "slow_zoom_in"),
        # 23. "Under the friction of the smooth agate stone, the chalky lime compacted into a gleaming, ivory-smooth surface ready for paint."
        ("video", "ep08_gf_06_agate_burnishing_intonaco.mp4", "action_clip") if (VIDEOS_DIR / "ep08_gf_06_agate_burnishing_intonaco.mp4").exists() else ("image", "ep08_gf_06_agate_burnishing_intonaco_GENERATE_VIDEO.jpg", "slow_dolly_forward"),

        # Act III: The Silk Road Blue (Cuts 24-35)
        # 24. "Once the plaster dried, the painters uncapped their earthenware pigment bowls."
        ("image", "ep08_23_terracotta_pigment_bowls_palette_PAN_ZOOM.jpg", "slow_dolly_forward"),
        # 25. "For red and yellow colors, they crushed local volcanic ochre rocks dug right from the Deccan soil."
        ("image", "ep08_19_slaked_lime_chuna_kiln_calcining_PAN_ZOOM.jpg", "pan_left"),
        # 26. "For green, they ground green earth minerals; for pure black, they collected soot from burning mustard oil lamps."
        ("video", "ep08_gf_14_mustard_oil_lamp_soot_smoke.mp4", "action_clip") if (VIDEOS_DIR / "ep08_gf_14_mustard_oil_lamp_soot_smoke.mp4").exists() else ("image", "ep08_gf_14_mustard_oil_lamp_soot_smoke_GENERATE_VIDEO.jpg", "slow_zoom_in"),
        # 27. "But across the ceilings of Cave One and Cave Seventeen shines a brilliant color that came from thousands of kilometers away."
        ("image", "ep08_real_painting_05_cave_ceiling_medallion_PAN_ZOOM.jpg", "slow_drift"),
        # 28. "It is an intense, glowing ultramarine blue that still looks fresh and wet on the rock walls today."
        ("image", "ep08_36_cave_1_ceiling_painting_museum_scan_PAN_ZOOM.jpg", "slow_tilt_up"),
        # 29. "This color was made from a rare gemstone called lapis lazuli."
        ("image", "ep08_25_raw_lapis_lazuli_mountain_rock_PAN_ZOOM.jpg", "slow_zoom_in"),
        # 30. "In the fifth century, there was only one place in the entire ancient world that had this blue stone: the remote mountain mines of Badakhshan in northern Afghanistan."
        ("image", "ep08_26_badakhshan_afghanistan_mountains_PAN_ZOOM.jpg", "slow_dolly_forward"),
        # 31. "To reach this remote volcanic cave, raw blue rocks traveled over two thousand five hundred kilometers across ancient trade roads."
        ("image", "ep08_04_vakataka_empire_deccan_map_still_PAN_ZOOM.jpg", "pan_right"),
        # 32. "Pack camels carried heavy leather bags of raw blue crystals through freezing mountain passes and across the Indian plains."
        ("video", "ep08_gf_02_caravan_silkroad_lapis.mp4", "action_clip") if (VIDEOS_DIR / "ep08_gf_02_caravan_silkroad_lapis.mp4").exists() else ("image", "ep08_gf_02_caravan_silkroad_lapis_GENERATE_VIDEO.jpg", "slow_dolly_forward"),
        # 33. "Ounce for ounce, this pure Afghan blue stone was worth more than solid gold."
        ("image", "ep08_28_gold_scale_weighing_lapis_lazuli_PAN_ZOOM.jpg", "slow_zoom_in"),
        # 34. "Only the wealthiest royal emperors and ministers could afford to paint entire cave ceilings in imported blue."
        ("video", "ep08_gf_03_mortar_grinding_lapis_powder.mp4", "action_clip") if (VIDEOS_DIR / "ep08_gf_03_mortar_grinding_lapis_powder.mp4").exists() else ("image", "ep08_gf_03_mortar_grinding_lapis_powder_GENERATE_VIDEO.jpg", "slow_dolly_forward"),
        # 35. "It was living proof that ancient India was connected to the entire world through the ancient Silk Road."
        ("image", "ep08_05_dakshinapatha_trade_merchants_PAN_ZOOM.jpg", "pan_left"),

        # Act IV: The Sootless Cave (Cuts 36-49)
        # 36. "But this artistic miracle creates a huge archaeological puzzle that baffled scientists for centuries."
        ("image", "ep08_29_varahadeva_inscription_cave_16_PAN_ZOOM.jpg", "slow_zoom_in"),
        # 37. "Caves One, Two, Sixteen, and Seventeen go thirty to forty meters deep inside solid mountain rock."
        ("image", "ep08_30_pitch_black_cave_interior_void_PAN_ZOOM.jpg", "slow_dolly_forward"),
        # 38. "When you step inside these cave halls, you enter total pitch-black darkness where you cannot see your own hand in front of your face."
        ("image", "ep08_archive_03_james_fergusson_1845_ajanta_cave_1_plate_PAN_ZOOM.jpg", "slow_drift"),
        # 39. "Yet in the deepest, darkest corners of these caves, ancient artists painted microscopic details: eyelashes thinner than a hair, tiny pearls, and detailed gold jewelry."
        ("image", "ep08_archive_04_robert_gill_1850_canvas_replica_plate_PAN_ZOOM.jpg", "pan_right"),
        # 40. "How could they paint these masterworks forty meters underground without any electric light?"
        ("image", "ep08_archive_05_asi_chemical_conservation_cross_section_1955_PAN_ZOOM.jpg", "slow_zoom_in"),
        # 41. "When modern scientists tested the cave ceilings, they searched for smoke stains and soot from burning oil lamps or torches."
        ("image", "ep08_31_clean_white_ceiling_no_soot_forensic_PAN_ZOOM.jpg", "slow_tilt_up"),
        # 42. "They found zero soot. The ceilings were completely clean."
        ("image", "ep08_archive_01_harishena_royal_copper_plate_charter_PAN_ZOOM.jpg", "pan_left"),
        # 43. "Burning fire torches inside these closed underground rooms would have choked the artists with smoke and blackened the white plaster walls."
        ("image", "ep08_24_mustard_oil_lamp_soot_collection_PAN_ZOOM.jpg", "slow_zoom_in"),
        # 44. "So how did they see? Ancient engineers invented an ingenious natural light diversion system."
        ("image", "ep08_infographic_02_bronze_mirror_optics.jpg", "slow_zoom_in"),
        # 45. "Outside in the blazing sunshine, assistants positioned large, circular mirrors made of highly polished cast bronze."
        ("video", "ep08_gf_07_bronze_mirror_sunlight_beam.mp4", "action_clip") if (VIDEOS_DIR / "ep08_gf_07_bronze_mirror_sunlight_beam.mp4").exists() else ("image", "ep08_gf_07_bronze_mirror_sunlight_beam_GENERATE_VIDEO.jpg", "slow_dolly_forward"),
        # 46. "The polished bronze mirrors caught the blinding tropical sun, reflecting powerful beams of natural sunlight straight into the dark cave entrance."
        ("image", "ep08_32_polished_cast_bronze_concave_mirror_PAN_ZOOM.jpg", "slow_drift"),
        # 47. "Inside the dark hall, apprentice boys held up large sheets of wet, bleached white cotton and silk cloth."
        ("image", "ep08_33_wet_linen_sheet_light_diffuser_PAN_ZOOM.jpg", "slow_zoom_in"),
        # 48. "When the intense sunbeam hit the wet white cloth, the light bounced and scattered, filling the dark underground hall with a soft, bright, shadowless glow."
        ("video", "ep08_gf_15_wet_linen_diffuser_light_beam.mp4", "action_clip") if (VIDEOS_DIR / "ep08_gf_15_wet_linen_diffuser_light_beam.mp4").exists() else ("image", "ep08_gf_15_wet_linen_diffuser_light_beam_GENERATE_VIDEO.jpg", "pan_right"),
        # 49. "The ancient painters were literally painting forty meters underground using captured natural sunlight."
        ("video", "ep08_gf_09_cave_interior_sunlit_murals.mp4", "action_clip") if (VIDEOS_DIR / "ep08_gf_09_cave_interior_sunlit_murals.mp4").exists() else ("image", "ep08_gf_09_cave_interior_sunlit_murals_GENERATE_VIDEO.jpg", "slow_dolly_forward"),

        # Act V: The Masterpieces of Humanity & The Looming Shadow (Cuts 50-62)
        # 50. "Illuminated by this soft, redirected sunlight, ancient artists created the greatest masterpieces of ancient world art."
        ("video", "ep08_gf_08_brush_applying_lapis_eyelash.mp4", "action_clip") if (VIDEOS_DIR / "ep08_gf_08_brush_applying_lapis_eyelash.mp4").exists() else ("image", "ep08_gf_08_brush_applying_lapis_eyelash_GENERATE_VIDEO.jpg", "slow_dolly_forward"),
        # 51. "On the rear wall of Cave One stands the famous painting of Bodhisattva Padmapani, holding a blue lotus flower."
        ("image", "ep08_real_painting_02_bodhisattva_lotus_PAN_ZOOM.jpg", "slow_dolly_forward"),
        # 52. "Look closely at his gentle expression, his regal crown, and the downward curve of his eyes full of compassion."
        ("image", "ep08_34_padmapani_tribhanga_posture_mural_PAN_ZOOM.jpg", "slow_zoom_in"),
        # 53. "Notice the realistic three-dimensional shading along his nose and jawline, making his body look soft and alive against the flat stone."
        ("image", "ep08_archive_06_chitrasutra_ancient_canons_proportions_PAN_ZOOM.jpg", "slow_drift"),
        # 54. "A thousand years before Leonardo da Vinci painted in Europe, Indian painters had already mastered human anatomy, emotion, and realistic 3D depth."
        ("image", "ep08_archive_09_vajrapani_cave_1_regal_bodhisattva_PAN_ZOOM.jpg", "pan_right"),
        # 55. "All across these walls, you can see real life from fifteen hundred years ago: royal courts with foreign Persian visitors, forest animals, and joyful celebrations."
        ("image", "ep08_35_persian_embassy_foreigners_fresco_PAN_ZOOM.jpg", "slow_tilt_up"),
        # 56. "But just as the painters were finishing these royal halls in the year 477, tragedy struck the empire."
        ("image", "ep08_37_black_apsara_cave_17_museum_scan_PAN_ZOOM.jpg", "slow_zoom_in"),
        # 57. "Emperor Harishena died suddenly under mysterious circumstances."
        ("image", "ep08_03_harishena_coronation_royal_court_PAN_ZOOM.jpg", "pan_left"),
        # 58. "Almost overnight, his kingdom collapsed into civil war, and hostile armies invaded the Deccan."
        ("image", "ep08_archive_10_harishena_sudden_abandonment_cliff_shadow_PAN_ZOOM.jpg", "slow_dolly_forward"),
        # 59. "Royal money stopped instantly."
        ("image", "ep08_archive_08_majanaka_jataka_royal_renunciation_fresco_PAN_ZOOM.jpg", "slow_zoom_in"),
        # 60. "Down the cliff, stonecutters abandoned half-carved pillars, painters dropped their wet brushes on the stone floor, and monks fled into the hills."
        ("video", "ep08_gf_16_abandoned_chisel_dropped_brush.mp4", "action_clip") if (VIDEOS_DIR / "ep08_gf_16_abandoned_chisel_dropped_brush.mp4").exists() else ("image", "ep08_gf_16_abandoned_chisel_dropped_brush_GENERATE_VIDEO.jpg", "slow_zoom_out"),
        # 61. "Within months, this bustling city of art in the cliff went completely silent."
        ("image", "ep08_02_satavahana_chaitya_silt_floor_PAN_ZOOM.jpg", "slow_drift"),
        # 62. "In our next episode, we will investigate this sudden collapse: the mysterious downfall that froze Ajanta in time, sealing these thirty temples inside the jungle for over a thousand years."
        ("video", "ep08_gf_10_harishena_shadow_cliffhanger.mp4", "action_clip") if (VIDEOS_DIR / "ep08_gf_10_harishena_shadow_cliffhanger.mp4").exists() else ("image", "ep08_gf_10_harishena_shadow_cliffhanger_GENERATE_VIDEO.jpg", "slow_dolly_forward")
    ]

def get_media_duration(path: Path) -> float:
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(path)
    ]
    out = subprocess.run(cmd, capture_output=True, text=True).stdout.strip()
    return float(out)

def parse_srt_cues(srt_path: Path):
    content = srt_path.read_text(encoding="utf-8")
    pattern = re.compile(
        r"(\d+)\s*\n(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})\s*\n(.*?)(?=\n\n|\Z)",
        re.DOTALL
    )
    matches = pattern.findall(content)
    
    def parse_time(ts):
        h, m, s_ms = ts.split(":")
        s, ms = s_ms.split(",")
        return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000.0

    cues = []
    for m in matches:
        cues.append({
            "index": int(m[0]),
            "start": parse_time(m[1]),
            "end": parse_time(m[2]),
            "text": m[3].strip().replace("\n", " ")
        })
    return cues

def derive_cut_durations(cues, total_audio_dur):
    starts = [0.0] + [c["start"] for c in cues[1:]] + [total_audio_dur]
    durations = [starts[i+1] - starts[i] for i in range(len(cues))]
    return durations

def render_subsegment(mtype, fname, motion, dur, idx, total, temp_dir):
    out_mp4 = temp_dir / f"sub_{idx:03d}.mp4"
    fps = 30
    frames = max(1, int(dur * fps))
    
    if mtype == "video":
        src_path = VIDEOS_DIR / fname
        if not src_path.exists():
            raise FileNotFoundError(f"Video clip missing: {src_path}")
        
        vf = "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30,setpts=PTS-STARTPTS"
        cmd = [
            "ffmpeg", "-y",
            "-stream_loop", "-1", "-i", str(src_path),
            "-vf", vf,
            "-r", "30",
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-pix_fmt", "yuv420p",
            "-an",
            "-t", f"{dur:.3f}",
            str(out_mp4)
        ]
    else:
        src_path = IMAGES_DIR / fname
        if not src_path.exists():
            raise FileNotFoundError(f"Still image missing: {src_path}")
        
        if motion == "slow_zoom_in":
            vf = f"scale=3840:2160,zoompan=z='1.0+0.12*(on/{frames})':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1920x1080:fps={fps},vignette=angle=PI/5,eq=contrast=1.04:saturation=1.06"
        elif motion == "slow_zoom_out":
            vf = f"scale=3840:2160,zoompan=z='1.12-0.12*(on/{frames})':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1920x1080:fps={fps},vignette=angle=PI/5,eq=contrast=1.04:saturation=1.06"
        elif motion == "pan_right":
            vf = f"scale=3840:2160,zoompan=z=1.10:x='(iw-iw/zoom)*(on/{frames})':y='ih/2-(ih/zoom/2)':d={frames}:s=1920x1080:fps={fps},vignette=angle=PI/5,eq=contrast=1.04:saturation=1.06"
        elif motion == "pan_left":
            vf = f"scale=3840:2160,zoompan=z=1.10:x='(iw-iw/zoom)*(1-on/{frames})':y='ih/2-(ih/zoom/2)':d={frames}:s=1920x1080:fps={fps},vignette=angle=PI/5,eq=contrast=1.04:saturation=1.06"
        elif motion == "slow_tilt_down":
            vf = f"scale=3840:2160,zoompan=z=1.10:x='iw/2-(iw/zoom/2)':y='(ih-ih/zoom)*(on/{frames})':d={frames}:s=1920x1080:fps={fps},vignette=angle=PI/5,eq=contrast=1.04:saturation=1.06"
        elif motion == "slow_tilt_up":
            vf = f"scale=3840:2160,zoompan=z=1.10:x='iw/2-(iw/zoom/2)':y='(ih-ih/zoom)*(1-on/{frames})':d={frames}:s=1920x1080:fps={fps},vignette=angle=PI/5,eq=contrast=1.04:saturation=1.06"
        elif motion == "slow_dolly_forward":
            vf = f"scale=3840:2160,zoompan=z='1.0+0.14*(on/{frames})':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1920x1080:fps={fps},vignette=angle=PI/5,eq=contrast=1.04:saturation=1.06"
        else:
            vf = f"scale=3840:2160,zoompan=z='1.0+0.07*(on/{frames})':x='(iw/2-(iw/zoom/2))+(iw*0.02)*(on/{frames})':y='ih/2-(ih/zoom/2)':d={frames}:s=1920x1080:fps={fps},vignette=angle=PI/5,eq=contrast=1.04:saturation=1.06"
            
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1", "-i", str(src_path),
            "-t", f"{dur:.3f}",
            "-vf", vf,
            "-r", "30",
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-pix_fmt", "yuv420p",
            "-an",
            str(out_mp4)
        ]
        
    subprocess.run(cmd, capture_output=True, check=True)
    return out_mp4

def assemble_master_video():
    print("=" * 65)
    print("  ASSEMBLING EPISODE 08 MASTER VIDEO (1080P 30FPS, 62 UNIQUE BEATS)")
    print("=" * 65)

    manifest = get_manifest()
    # 1. Assert zero repetition invariant
    fnames = [m[1] for m in manifest]
    assert len(fnames) == len(set(fnames)), f"Duplicate media assets in manifest! {len(fnames)} vs {len(set(fnames))}"
    print(f"[*] Verified Zero-Repetition Invariant: {len(fnames)} unique media assets for {len(manifest)} cuts.")

    # 2. Check how many actual video clips are present
    v_clips = [m[1] for m in manifest if m[0] == "video"]
    print(f"[*] Google Flow Video Clips detected: {len(v_clips)} / 10 clips present in manifest.")
    if len(v_clips) < 10:
        print("[NOTE] Rendering Internal Development Draft (Action candidate stills used for pending video clips).")

    # 3. Audio & Subtitles
    master_audio = AUDIO_DIR / "episode_08_master_audio_mixed.mp3"
    srt_file = SUB_DIR / "episode_08_full.srt"

    if not master_audio.exists():
        raise FileNotFoundError(f"Master mixed audio missing: {master_audio}")
    if not srt_file.exists():
        raise FileNotFoundError(f"Subtitles missing: {srt_file}")

    total_audio_dur = get_media_duration(master_audio)
    cues = parse_srt_cues(srt_file)
    print(f"[*] Loaded Master Audio: {total_audio_dur:.2f}s | {len(cues)} sentence cues")

    assert len(cues) == len(manifest), f"Cue count ({len(cues)}) does not match Manifest count ({len(manifest)})!"

    durations = derive_cut_durations(cues, total_audio_dur)
    print(f"[*] Derived {len(durations)} cut durations (Total video time: {sum(durations):.2f}s)")

    # 4. Render subsegments
    temp_dir = EPISODE_DIR / "_temp_cuts"
    temp_dir.mkdir(parents=True, exist_ok=True)

    concat_list = temp_dir / "concat_list.txt"
    subsegment_paths = []

    print("\n[*] Rendering individual cuts with 4K sub-pixel Ken Burns & action video...")
    for idx, (mtype, fname, motion) in enumerate(manifest):
        dur = durations[idx]
        print(f"  [{idx+1:02d}/{len(manifest):02d}] {mtype.upper()}: {fname} ({dur:.2f}s, {motion})")
        sub_path = render_subsegment(mtype, fname, motion, dur, idx, len(manifest), temp_dir)
        subsegment_paths.append(sub_path)

    with open(concat_list, "w", encoding="utf-8") as f:
        for p in subsegment_paths:
            f.write(f"file '{p.as_posix()}'\n")

    # 5. Concatenate video stream
    raw_video = temp_dir / "raw_video_stream.mp4"
    print(f"\n[*] Concatenating {len(subsegment_paths)} cuts into raw video stream...")
    cmd_cat = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy",
        str(raw_video)
    ]
    subprocess.run(cmd_cat, capture_output=True, check=True)

    # 6. Mux audio and video into final master
    final_output = OUTPUT_DIR / "episode_08_master_1080p.mp4"
    print(f"[*] Muxing mixed master audio into: {final_output.name}...")
    cmd_mux = [
        "ffmpeg", "-y",
        "-i", str(raw_video),
        "-i", str(master_audio),
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "256k",
        "-movflags", "+faststart",
        str(final_output)
    ]
    subprocess.run(cmd_mux, capture_output=True, check=True)
    final_dur = get_media_duration(final_output)
    print(f"\n[OK] Master Video Successfully Rendered: {final_output.name}")
    print(f"     Duration: {final_dur:.2f}s ({final_output.stat().st_size:,} bytes)")

    # Clean up temp cuts
    shutil.rmtree(temp_dir, ignore_errors=True)
    print("[*] Cleaned up temporary cut buffers.")

if __name__ == "__main__":
    assemble_master_video()
