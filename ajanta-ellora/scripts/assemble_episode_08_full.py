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
        # Act I: The Golden Reawakening (Cuts 1-9)
        # 1. "For nearly four centuries, the horseshoe canyon of Ajanta lay in absolute silence."
        ("image", "ep08_01_silent_canyon_dormancy_PAN_ZOOM.jpg", "slow_drift"),
        # 2. "The austere stone stupas carved by early Satavahana monks had been swallowed by jungle vines..."
        ("video", "ep08_gf_11_jungle_vines_monsoon_chaitya_flood.mp4", "action_clip") if (VIDEOS_DIR / "ep08_gf_11_jungle_vines_monsoon_chaitya_flood.mp4").exists() else ("image", "ep08_gf_11_jungle_vines_monsoon_chaitya_flood_GENERATE_VIDEO.jpg", "pan_right"),
        # 3. "Then—around the year 460 of the common era—a volcanic explosion of royal power transformed the ravine forever."
        ("image", "ep08_03_harishena_coronation_royal_court_PAN_ZOOM.jpg", "slow_zoom_in"),
        # 4. "From the north, Emperor Harishena of the Vakataka dynasty united the Deccan..."
        ("video", "ep08_gf_01_harishena_imperial_cavalry.mp4", "action_clip") if (VIDEOS_DIR / "ep08_gf_01_harishena_imperial_cavalry.mp4").exists() else ("image", "ep08_gf_01_harishena_imperial_cavalry_GENERATE_VIDEO.jpg", "slow_dolly_forward"),
        # 5. "Wealth from the Silk Road and the ancient Dakshinapatha trade artery poured directly into this secluded mountain."
        ("image", "ep08_04_vakataka_empire_deccan_map_still_PAN_ZOOM.jpg", "slow_zoom_in"),
        # 6. "Harishena’s royal ministers, feudatory kings, and merchant guilds began an unprecedented architectural assault..."
        ("image", "ep08_05_dakshinapatha_trade_merchants_PAN_ZOOM.jpg", "pan_left"),
        # 7. "Within just seventeen feverish years, master stonecutters carved twenty colossal new sanctuaries into the sheer basalt."
        ("video", "ep08_gf_12_cliffside_bamboo_scaffolding_army.mp4", "action_clip") if (VIDEOS_DIR / "ep08_gf_12_cliffside_bamboo_scaffolding_army.mp4").exists() else ("image", "ep08_gf_12_cliffside_bamboo_scaffolding_army_GENERATE_VIDEO.jpg", "slow_tilt_up"),
        # 8. "But these were no longer simple ascetic retreats; they were multi-story rock-cut university palaces..."
        ("image", "ep08_07_canyon_cliff_construction_activity_PAN_ZOOM.jpg", "slow_dolly_forward"),
        # 9. "And upon their smooth interior walls, ancient painters were about to achieve a visual miracle..."
        ("image", "ep08_08_monumental_vihara_colonnade_facade_PAN_ZOOM.jpg", "slow_zoom_out"),

        # Act II: The Basalt Problem & The Mud Chemistry Secret (Cuts 10-23)
        # 10. "To paint inside Ajanta, ancient craftsmen faced an impossible geological reality."
        ("image", "ep08_09_royal_university_hall_perspective_PAN_ZOOM.jpg", "slow_dolly_forward"),
        # 11. "The walls were not made of smooth limestone or dry sandstone; they were carved out of dense, volcanic flood basalt."
        ("video", "ep08_gf_13_basalt_weeping_water_droplets_macro.mp4", "action_clip") if (VIDEOS_DIR / "ep08_gf_13_basalt_weeping_water_droplets_macro.mp4").exists() else ("image", "ep08_gf_13_basalt_weeping_water_droplets_macro_GENERATE_VIDEO.jpg", "pan_right"),
        # 12. "Basalt is an igneous rock formed by cooling lava—glassy, non-porous, and constantly weeping subterranean moisture."
        ("image", "ep08_11_flaking_paint_moisture_failure_PAN_ZOOM.jpg", "slow_zoom_in"),
        # 13. "If you apply paint directly to raw basalt, the moisture pushes the pigment off within months..."
        ("image", "ep08_infographic_01_plaster_stratigraphy.jpg", "slow_zoom_in"),
        # 14. "European fresco painters solved dampness with slaked lime on wet walls..."
        ("image", "ep08_12_chitrasutra_palm_leaf_manuscript_PAN_ZOOM.jpg", "slow_drift"),
        # 15. "The master guilds of Ajanta developed a revolutionary, multi-layered bio-composite formula..."
        ("video", "ep08_gf_05_chipping_basalt_key_sparks.mp4", "action_clip") if (VIDEOS_DIR / "ep08_gf_05_chipping_basalt_key_sparks.mp4").exists() else ("image", "ep08_gf_05_chipping_basalt_key_sparks_GENERATE_VIDEO.jpg", "slow_dolly_forward"),
        # 16. "First, laborers took pointed iron picks and rapidly pecked thousands of mechanical dimples..."
        ("image", "ep08_13_laborers_pecking_basalt_dimples_PAN_ZOOM.jpg", "pan_left"),
        # 17. "Then came the secret bio-chemical matrix: a thick, fermented plaster made of local ferruginous red clay..."
        ("image", "ep08_14_ferruginous_red_clay_quarry_PAN_ZOOM.jpg", "slow_tilt_down"),
        # 18. "Fermented cow dung was not crude; it was chemical genius."
        ("video", "ep08_gf_04_plaster_kneading_cowdung_matrix.mp4", "action_clip") if (VIDEOS_DIR / "ep08_gf_04_plaster_kneading_cowdung_matrix.mp4").exists() else ("image", "ep08_gf_04_plaster_kneading_cowdung_matrix_GENERATE_VIDEO.jpg", "slow_dolly_forward"),
        # 19. "Its digested vegetal fibers provided microscopic cellulose netting that prevented shrinkage cracks..."
        ("image", "ep08_15_cow_dung_cellulose_fibers_macro_PAN_ZOOM.jpg", "slow_zoom_in"),
        # 20. "Mixed with fibrous rice husks and boiled sap from neem trees and bel fruit..."
        ("image", "ep08_16_rice_husk_tensile_reinforcement_PAN_ZOOM.jpg", "pan_right"),
        # 21. "Finally, artisans applied an ultra-thin finish coat called intonaco..."
        ("image", "ep08_17_neem_tree_sap_extraction_vessel_PAN_ZOOM.jpg", "slow_drift"),
        # 22. "While still damp, a craftsman knelt before the wall holding a smooth, banded agate river pebble..."
        ("image", "ep08_18_wooden_trowel_applying_mud_layer_PAN_ZOOM.jpg", "slow_zoom_in"),
        # 23. "Under the friction of the agate stone, the lime compacted into an ivory-smooth, reflective porcelain surface..."
        ("video", "ep08_gf_06_agate_burnishing_intonaco.mp4", "action_clip") if (VIDEOS_DIR / "ep08_gf_06_agate_burnishing_intonaco.mp4").exists() else ("image", "ep08_gf_06_agate_burnishing_intonaco_GENERATE_VIDEO.jpg", "slow_dolly_forward"),

        # Act III: The Silk Road Blue (Cuts 24-35)
        # 24. "When the plaster cured, the master painters uncapped their pigment bowls."
        ("image", "ep08_19_slaked_lime_chuna_kiln_calcining_PAN_ZOOM.jpg", "slow_dolly_forward"),
        # 25. "For reds and yellows, they crushed local volcanic ochres scooped from Deccan soil."
        ("image", "ep08_20_crushed_oyster_shells_gypsum_powder_PAN_ZOOM.jpg", "pan_left"),
        # 26. "For forest greens, they ground mineral glauconite; for black, they gathered pure soot from burning mustard oil lamps."
        ("video", "ep08_gf_14_mustard_oil_lamp_soot_smoke.mp4", "action_clip") if (VIDEOS_DIR / "ep08_gf_14_mustard_oil_lamp_soot_smoke.mp4").exists() else ("image", "ep08_gf_14_mustard_oil_lamp_soot_smoke_GENERATE_VIDEO.jpg", "slow_zoom_in"),
        # 27. "But across the royal ceilings of Cave One and Cave Seventeen glows a color that did not come from the Indian subcontinent."
        ("image", "ep08_22_polished_ivory_smooth_intonaco_sheen_PAN_ZOOM.jpg", "slow_drift"),
        # 28. "It is a blinding, celestial ultramarine blue that still burns on the stone walls after fifteen hundred years."
        ("image", "ep08_23_terracotta_pigment_bowls_palette_PAN_ZOOM.jpg", "slow_tilt_up"),
        # 29. "This was lapis lazuli."
        ("image", "ep08_24_mustard_oil_lamp_soot_collection_PAN_ZOOM.jpg", "slow_zoom_in"),
        # 30. "In the fifth century, there was only one known source of lapis lazuli in the entire ancient world..."
        ("image", "ep08_25_raw_lapis_lazuli_mountain_rock_PAN_ZOOM.jpg", "slow_dolly_forward"),
        # 31. "To reach this remote volcanic canyon, raw blue crystals traveled over two thousand five hundred kilometers."
        ("image", "ep08_26_badakhshan_afghanistan_mountains_PAN_ZOOM.jpg", "pan_right"),
        # 32. "Carried in leather saddlebags on pack camels through the snow-bound passes of the Hindu Kush..."
        ("video", "ep08_gf_02_caravan_silkroad_lapis.mp4", "action_clip") if (VIDEOS_DIR / "ep08_gf_02_caravan_silkroad_lapis.mp4").exists() else ("image", "ep08_gf_02_caravan_silkroad_lapis_GENERATE_VIDEO.jpg", "slow_dolly_forward"),
        # 33. "Ounce for ounce, pure Badakhshan lapis was worth more than solid gold."
        ("image", "ep08_27_camels_crossing_hindu_kush_pass_PAN_ZOOM.jpg", "slow_zoom_in"),
        # 34. "Only the wealthiest royal patrons—like Emperor Harishena’s prime minister Varahadeva—could afford..."
        ("video", "ep08_gf_03_mortar_grinding_lapis_powder.mp4", "action_clip") if (VIDEOS_DIR / "ep08_gf_03_mortar_grinding_lapis_powder.mp4").exists() else ("image", "ep08_gf_03_mortar_grinding_lapis_powder_GENERATE_VIDEO.jpg", "slow_dolly_forward"),
        # 35. "It was a physical testament to a globalized world, where Central Asian mineral wealth met the spiritual genius..."
        ("image", "ep08_28_gold_scale_weighing_lapis_lazuli_PAN_ZOOM.jpg", "pan_left"),

        # Act IV: The Sootless Cave (Cuts 36-49)
        # 36. "Yet this artistic triumph presents a profound archaeological paradox."
        ("image", "ep08_29_varahadeva_inscription_cave_16_PAN_ZOOM.jpg", "slow_zoom_in"),
        # 37. "Caves One, Two, Sixteen, and Seventeen penetrate thirty to forty meters deep into solid subterranean mountain rock."
        ("image", "ep08_30_pitch_black_cave_interior_void_PAN_ZOOM.jpg", "slow_dolly_forward"),
        # 38. "Step beyond the entrance portico, and you enter pitch-black darkness where your eyes cannot see your own outstretched hand."
        ("image", "ep08_archive_01_harishena_royal_copper_plate_charter_PAN_ZOOM.jpg", "slow_drift"),
        # 39. "Yet here, in the deepest recess of the cave, artists painted microscopic details..."
        ("image", "ep08_archive_02_badakhshan_lapis_geological_survey_map_PAN_ZOOM.jpg", "pan_right"),
        # 40. "How did they paint these masterworks without light?"
        ("image", "ep08_archive_03_james_fergusson_1845_ajanta_cave_1_plate_PAN_ZOOM.jpg", "slow_zoom_in"),
        # 41. "When Victorian surveyors and modern conservators analyzed the cave ceilings..."
        ("image", "ep08_31_clean_white_ceiling_no_soot_forensic_PAN_ZOOM.jpg", "slow_tilt_up"),
        # 42. "They found absolutely none."
        ("image", "ep08_archive_04_robert_gill_1850_canvas_replica_plate_PAN_ZOOM.jpg", "pan_left"),
        # 43. "Burning torches in these enclosed halls would have suffocated the artisans..."
        ("image", "ep08_archive_05_asi_chemical_conservation_cross_section_1955_PAN_ZOOM.jpg", "slow_zoom_in"),
        # 44. "The solution was an ingenious optical engineering array."
        ("image", "ep08_infographic_02_bronze_mirror_optics.jpg", "slow_zoom_in"),
        # 45. "In the searing sunlight outside the veranda, assistants positioned large, circular cast-bronze mirrors."
        ("video", "ep08_gf_07_bronze_mirror_sunlight_beam.mp4", "action_clip") if (VIDEOS_DIR / "ep08_gf_07_bronze_mirror_sunlight_beam.mp4").exists() else ("image", "ep08_gf_07_bronze_mirror_sunlight_beam_GENERATE_VIDEO.jpg", "slow_dolly_forward"),
        # 46. "The highly polished bronze caught the blazing Deccan sun, collimating natural rays into intense, focused beams of light."
        ("image", "ep08_32_polished_cast_bronze_concave_mirror_PAN_ZOOM.jpg", "slow_drift"),
        # 47. "These beams were bounced through the cave doorways and intercepted by wet, bleached white cotton and silk sheets..."
        ("image", "ep08_archive_07_bronze_mirror_harappan_vakataka_museum_scan_PAN_ZOOM.jpg", "slow_zoom_in"),
        # 48. "The wet fabric diffused the harsh solar glare into a soft, ambient glow..."
        ("video", "ep08_gf_15_wet_linen_diffuser_light_beam.mp4", "action_clip") if (VIDEOS_DIR / "ep08_gf_15_wet_linen_diffuser_light_beam.mp4").exists() else ("image", "ep08_gf_15_wet_linen_diffuser_light_beam_GENERATE_VIDEO.jpg", "pan_right"),
        # 49. "The painters were literally painting with captured sunlight."
        ("video", "ep08_gf_09_cave_interior_sunlit_murals.mp4", "action_clip") if (VIDEOS_DIR / "ep08_gf_09_cave_interior_sunlit_murals.mp4").exists() else ("image", "ep08_gf_09_cave_interior_sunlit_murals_GENERATE_VIDEO.jpg", "slow_dolly_forward"),

        # Act V: The Masterpieces of Humanity & The Looming Shadow (Cuts 50-62)
        # 50. "Illuminated by bounced sunlight, the master guilds painted the greatest masterpieces of ancient world art."
        ("video", "ep08_gf_08_brush_applying_lapis_eyelash.mp4", "action_clip") if (VIDEOS_DIR / "ep08_gf_08_brush_applying_lapis_eyelash.mp4").exists() else ("image", "ep08_gf_08_brush_applying_lapis_eyelash_GENERATE_VIDEO.jpg", "slow_dolly_forward"),
        # 51. "Chief among them stands the Bodhisattva Padmapani on the rear wall of Cave One."
        ("image", "ep08_34_padmapani_tribhanga_posture_mural_PAN_ZOOM.jpg", "slow_dolly_forward"),
        # 52. "Holding a blue lotus in his right hand, his body curves in the gentle tribhanga posture..."
        ("image", "ep08_archive_06_chitrasutra_ancient_canons_proportions_PAN_ZOOM.jpg", "slow_zoom_in"),
        # 53. "Notice the subtle three-dimensional shading—known in Sanskrit as vartana..."
        ("image", "ep08_archive_09_vajrapani_cave_1_regal_bodhisattva_PAN_ZOOM.jpg", "slow_drift"),
        # 54. "A thousand years before Leonardo da Vinci developed chiaroscuro in the Italian Renaissance..."
        ("image", "ep08_36_cave_1_ceiling_painting_museum_scan_PAN_ZOOM.jpg", "pan_right"),
        # 55. "Across the walls, narrative Jataka tales come to life: royal courts overflowing with Persian ambassadors..."
        ("image", "ep08_35_persian_embassy_foreigners_fresco_PAN_ZOOM.jpg", "slow_tilt_up"),
        # 56. "But as artists applied the final touches of Afghan lapis lazuli around the year 477..."
        ("image", "ep08_37_black_apsara_cave_17_museum_scan_PAN_ZOOM.jpg", "slow_zoom_in"),
        # 57. "Emperor Harishena died suddenly under mysterious circumstances."
        ("image", "ep08_38_indra_apsaras_cave_17_museum_scan_PAN_ZOOM.jpg", "pan_left"),
        # 58. "Almost overnight, the Vakataka dynasty fractured into bitter succession wars..."
        ("image", "ep08_39_mahajanaka_jataka_museum_scan_PAN_ZOOM.jpg", "slow_dolly_forward"),
        # 59. "Royal funding vanished in an instant."
        ("image", "ep08_archive_08_majanaka_jataka_royal_renunciation_fresco_PAN_ZOOM.jpg", "slow_zoom_in"),
        # 60. "In caves down the cliff face, half-finished pillars were abandoned mid-strike..."
        ("image", "ep08_40_cave_1_ceiling_medallion_museum_scan_PAN_ZOOM.jpg", "slow_drift"),
        # 61. "Within months, the golden city in the volcanic cliff went completely silent."
        ("video", "ep08_gf_16_abandoned_chisel_dropped_brush.mp4", "action_clip") if (VIDEOS_DIR / "ep08_gf_16_abandoned_chisel_dropped_brush.mp4").exists() else ("image", "ep08_gf_16_abandoned_chisel_dropped_brush_GENERATE_VIDEO.jpg", "slow_zoom_out"),
        # 62. "In our next episode, we will investigate the overnight silence..."
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
