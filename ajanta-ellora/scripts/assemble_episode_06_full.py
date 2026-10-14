"""
assemble_episode_06_full.py — Full 72-Micro-Beat Master Assembly Engine for Kailasa Episode 06.
Implements:
1. 72-Beat Manifest derived from 16 Google Flow Action Videos, 6 Infographic Cards, 38 Hero Stills, and 12 Archive Stills.
2. 4K Anti-Jitter Sub-Pixel Motorized Zoompan Engine for still images (scale=3840:2160 -> zoompan -> scale=1920:1080).
3. Monotonic Sentence-Level Cue Timing derived directly from episode_06_full.srt (0.00ms audio drift).
4. Strict Google Flow Video Gate Law: Refuses to render master video without user action videos, while providing dry-run/preview verification.
"""

import os
import re
import sys
import json
import shutil
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent # ajanta-ellora
EPISODE_DIR = BASE_DIR / "episode06"
IMAGES_DIR = EPISODE_DIR / "images"
AUDIO_DIR = EPISODE_DIR / "audio"
SUB_DIR = EPISODE_DIR / "subtitles"
VIDEOS_DIR = EPISODE_DIR / "videos"
OUTPUT_DIR = EPISODE_DIR / "final_videos"
BUNDLE_DIR = EPISODE_DIR / "openmontage_bundle"
THUMBNAIL_DIR = EPISODE_DIR / "thumbnail"
PUBLISH_DIR = EPISODE_DIR / "publish_kit"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
BUNDLE_DIR.mkdir(parents=True, exist_ok=True)
VIDEOS_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# 72-MICRO-BEAT MASTER MANIFEST (TYPE, FILENAME, MOTION)
# ---------------------------------------------------------------------------
MANIFEST = [
    # Act I: The Bridges in the Sky (Cuts 1-9)
    # 1. "When you descend into the deep trench of Cave 16, your eyes are drawn upward by a physical impossibility."
    ("image", "ep06_01_chasm_depth_entry_PAN_ZOOM.jpg", "slow_dolly_forward"),
    # 2. "Suspended thirty feet in the open air, a monolithic stone bridge spans the chasm between the entrance gateway and the inner shrine."
    ("video", "ep06_gf_01_sky_bridge_dawn_mist.mp4", "action_clip"),
    # 3. "There are no mortar joints, no structural keystones, and no iron tie-rods holding this walkway together."
    ("image", "ep06_02_sky_bridge_underside_void_PAN_ZOOM.jpg", "slow_tilt_up"),
    # 4. "It is cut from the living volcanic basalt bedrock, an aerial arch carved out of the mountain interior."
    ("image", "ep06_03_bridge_coping_and_parapet_PAN_ZOOM.jpg", "pan_right"),
    # 5. "To modern structural engineers, an arched bridge is assembled from stone blocks that wedge against each other under compression."
    ("image", "ep06_infographic_01_sky_bridge_structural_elevation.jpg", "slow_zoom_in"),
    # 6. "But at Kailasa, the bridge was never assembled; it was left behind when the empty space below it was hollowed away."
    ("image", "ep06_05_basalt_tensile_arch_detail_PAN_ZOOM.jpg", "slow_zoom_out"),
    # 7. "If a single natural fissure crossed the span, or if a stonecutter struck too deeply, thousands of tons of stone would shear and collapse."
    ("image", "ep06_06_courtyard_shadow_play_PAN_ZOOM.jpg", "pan_left"),
    # 8. "Decades of royal labor and the entire architectural axis of the temple would have been destroyed in seconds."
    ("image", "ep06_archive_01_ellora_ridge_topography_PAN_ZOOM.jpg", "slow_drift"),
    # 9. "Today, we investigate the engineering gamble behind the floating bridges of Ellora."
    ("video", "ep06_gf_14_torch_priest_stairwell_descent.mp4", "action_clip"),

    # Act II: The Queen's Vow & 7-Day Shikhara (Cuts 10-18)
    # 10. "To understand how ancient carvers dared to leave bridges hanging in mid-air, we must look at the legend of its conception."
    ("image", "ep06_07_katha_kalpataru_palm_leaf_PAN_ZOOM.jpg", "slow_zoom_in"),
    # 11. "A medieval chronicle preserved in the Katha-Kalpataru tells of a Rashtrakuta queen whose husband fell critically ill."
    ("image", "ep06_08_queen_illness_royal_court_PAN_ZOOM.jpg", "pan_right"),
    # 12. "She made a sacred vow to fast until she could gaze upon the pinnacle of a magnificent Shiva temple built for his recovery."
    ("image", "ep06_archive_04_ancient_vasthu_shastra_compass_PAN_ZOOM.jpg", "slow_drift"),
    # 13. "Royal architects told the king that building such a monument from the ground up would require decades, condemning the queen to starvation."
    ("image", "ep06_10_cliff_summit_measuring_grid_PAN_ZOOM.jpg", "pan_left"),
    # 14. "Then stepped forward a master builder from the artisan lineage named Kokasa."
    ("image", "ep06_09_kokasa_presentation_to_king_PAN_ZOOM.jpg", "slow_dolly_forward"),
    # 15. "Kokasa promised that the queen would behold the gleaming temple spire in just seven days."
    ("image", "ep06_cinematic_kokasa_top_down_skyline_PAN_ZOOM.jpg", "slow_zoom_in"),
    # 16. "He climbed to the summit of the volcanic cliff, plotted the sacred geometry, and carved the pinnacle downward from the mountain peak."
    ("video", "ep06_gf_02_kokasa_summit_geometry.mp4", "action_clip"),
    # 17. "Within seven days, the soaring shikhara stood fully formed on the mountaintop, allowing the queen to break her fast."
    ("video", "ep06_gf_08_queen_balcony_seven_days.mp4", "action_clip"),
    # 18. "While legendary in detail, the story captures the core engineering truth: Kailasa was conceived from the heavens downward."
    ("image", "ep06_11_shikhara_finial_kalasha_PAN_ZOOM.jpg", "slow_tilt_up"),

    # Act III: Carving the Void (Cuts 19-27)
    # 19. "Carving an aerial bridge from the top down requires solving a terrifying logistical puzzle."
    ("image", "ep06_12_top_down_stepped_terraces_PAN_ZOOM.jpg", "slow_tilt_down"),
    # 20. "The upper walkway of the bridge had to be finished first, while solid bedrock still supported it from below."
    ("image", "ep06_04_gopuram_terrace_view_PAN_ZOOM.jpg", "pan_left"),
    # 21. "Surveyors snapped dyed cords across the surface, marking the exact thickness needed to withstand structural dead loads."
    ("image", "ep06_infographic_03_bridge_underbelly_excavation_mechanics.jpg", "slow_zoom_in"),
    # 22. "Then came the dangerous stage: quarrymen were suspended in hemp rope harnesses over a thirty-foot abyss to hollow out the underbelly."
    ("video", "ep06_gf_03_quarrymen_hemp_rope_void.mp4", "action_clip"),
    # 23. "Working upside down in cramped voids, stonecutters used pointed picks to scoop away the rock beneath the span."
    ("image", "ep06_14_inverted_quarry_technique_PAN_ZOOM.jpg", "pan_right"),
    # 24. "They had to listen to the stone; dull hollow thuds signaled thin basalt, while crisp ringing rings meant solid load-bearing rock."
    ("image", "ep06_15_acoustic_sounding_chisel_tap_PAN_ZOOM.jpg", "slow_dolly_forward"),
    # 25. "Thermal fire-setting could not be used here; intense heat would induce micro-fractures in the hanging ceiling."
    ("video", "ep06_gf_05_water_quench_fissure_check.mp4", "action_clip"),
    # 26. "Every single cubic foot of the void had to be cut through sheer manual percussion with tempered carbon-steel chisels."
    ("video", "ep06_gf_04_hammer_wedge_sparks_void.mp4", "action_clip"),
    # 27. "When the void was cleared, the bridge hung unsupported—a permanent aerial monument suspended between two worlds."
    ("image", "ep06_17_void_clearance_moment_hero_PAN_ZOOM.jpg", "slow_zoom_out"),

    # Act IV: The Courtyard Monoliths (Cuts 28-36)
    # 28. "As quarrymen deepened the courtyard floor past the aerial bridges, they encountered two monumental stone islands."
    ("video", "ep06_gf_10_twilight_nandi_oil_lamps.mp4", "action_clip"),
    # 29. "Rather than clearing the trench into a flat floor, they left two towering columns of living basalt standing fifty feet tall."
    ("video", "ep06_gf_06_dhwajasthambha_quarry_reveal.mp4", "action_clip"),
    # 30. "These became the famous Dhwajasthambhas—the colossal monolithic victory pillars of Kailasa."
    ("image", "ep06_cinematic_dhwajasthambha_quarry_isolation_PAN_ZOOM.jpg", "slow_zoom_in"),
    # 31. "Carved in place from the bedrock, they rise seventeen meters into the sky with intricate fluting, floral bands, and tridents."
    ("image", "ep06_19_dhwajasthambha_trident_capital_PAN_ZOOM.jpg", "slow_zoom_in"),
    # 32. "Flanking the courtyard, two life-size monolithic elephants emerge directly from the courtyard floor."
    ("image", "ep06_20_freestanding_elephant_flank_PAN_ZOOM.jpg", "pan_left"),
    # 33. "Their massive flanks, carved ears, and wrinkled trunks were freed from the surrounding stone without a single joint."
    ("video", "ep06_gf_07_courtyard_elephant_tusk_carve.mp4", "action_clip"),
    # 34. "In ancient Indian rock architecture, creating a freestanding statue inside a quarry requires extreme mathematical precision."
    ("image", "ep06_21_elephant_ear_rock_texture_PAN_ZOOM.jpg", "slow_drift"),
    # 35. "The sculptor must visualize the complete three-dimensional animal inside a dark, uncarved mass of rock before making the first strike."
    ("image", "ep06_22_3d_spatial_visualization_still_PAN_ZOOM.jpg", "slow_zoom_in"),
    # 36. "Once stone is removed, it cannot be replaced; one chipped tusk would ruin twenty years of continuous carving."
    ("image", "ep06_18_twin_dhwajasthambha_symmetry_PAN_ZOOM.jpg", "slow_tilt_up"),

    # Act V: The Living Epics in Basalt (Cuts 37-45)
    # 37. "Along the lower plinth flanking the temple halls, the bedrock transforms from monumental mass into narrative poetry."
    ("image", "ep06_23_ramayana_running_frieze_overview_PAN_ZOOM.jpg", "pan_right"),
    # 38. "Two continuous running friezes depict the great Indian epics—the Ramayana on the south and the Mahabharata on the north."
    ("image", "ep06_archive_06_james_burgess_1883_report_plate_PAN_ZOOM.jpg", "slow_zoom_in"),
    # 39. "Across miniature horizontal tiers, master sculptors chiseled hundreds of dynamic figures into the hard volcanic stone."
    ("video", "ep06_gf_11_ramayana_frieze_chisel_macro.mp4", "action_clip"),
    # 40. "On the southern wall, we see the battle of Lanka, with chariot wheels, galloping war horses, and archers drawing bows."
    ("image", "ep06_24_battle_of_lanka_warriors_PAN_ZOOM.jpg", "slow_dolly_forward"),
    # 41. "Nearby, the dramatic high-relief panel of Ravana Shaking Mount Kailash captures tectonic terror in stone."
    ("image", "ep06_25_ravana_anugraha_wide_recess_PAN_ZOOM.jpg", "slow_tilt_down"),
    # 42. "The demon king exerts all twenty arms against the roots of the mountain, straining with bulging muscles and grimacing fury."
    ("video", "ep06_gf_12_ravana_shaking_mountain_torch.mp4", "action_clip"),
    # 43. "Above, Shiva calmly presses his big toe downward into the bedrock, instantly neutralizing the subterranean earthquake."
    ("image", "ep06_26_shiva_calm_foot_press_PAN_ZOOM.jpg", "slow_zoom_in"),
    # 44. "The depth of the relief creates stark chiaroscuro shadows under the bright Deccan sun, making the figures appear in kinetic motion."
    ("image", "ep06_27_chiaroscuro_relief_depth_PAN_ZOOM.jpg", "slow_zoom_out"),
    # 45. "The living rock ceases to be cold basalt; it becomes a theater of cosmic power and human drama."
    ("image", "ep06_archive_11_stone_mason_guild_emblems_PAN_ZOOM.jpg", "slow_drift"),

    # Act VI: The White Mountain of Ellora (Cuts 46-54)
    # 46. "Today, when visitors enter Kailasa, they see dark, weathered volcanic basalt."
    ("image", "ep06_archive_09_19th_century_collo_type_kailasa_bridge_PAN_ZOOM.jpg", "slow_drift"),
    # 47. "But for centuries after its creation, Kailasa looked completely different."
    ("image", "ep06_archive_08_plaster_microscopic_cross_section_PAN_ZOOM.jpg", "slow_zoom_in"),
    # 48. "The entire monument was coated in a brilliant, luminous white shell-lime plaster known as chuna."
    ("image", "ep06_28_ancient_white_plaster_reconstruction_PAN_ZOOM.jpg", "slow_zoom_out"),
    # 49. "Formulated from calcined river shells, slaked lime, marble dust, and organic plant binders, this coating was burnished with smooth agate stones."
    ("image", "ep06_29_calcined_river_shells_chuna_PAN_ZOOM.jpg", "pan_left"),
    # 50. "Under the blazing tropical sun of Maharashtra, the temple gleamed with a blinding, porcelain-like white radiance."
    ("video", "ep06_gf_09_white_chuna_plaster_burnish.mp4", "action_clip"),
    # 51. "This was the architectural masterstroke of the Rashtrakutas: to recreate Mount Kailash of the snow-covered Himalayas in the volcanic plains of the Deccan."
    ("image", "ep06_cinematic_white_chuna_plaster_layer_PAN_ZOOM.jpg", "slow_zoom_in"),
    # 52. "Travelers approaching Elapura across the dusty plateau saw what appeared to be an iceberg of pure stone rising from a black chasm."
    ("image", "ep06_32_iceberg_in_black_chasm_hero_PAN_ZOOM.jpg", "slow_zoom_out"),
    # 53. "Rain and centuries of monsoon weathering eventually stripped away the white shell, exposing the dark volcanic skeleton beneath."
    ("image", "ep06_30_agate_burnishing_stone_macro_PAN_ZOOM.jpg", "slow_drift"),
    # 54. "Yet in sheltered cornices and ceiling corners, patches of the gleaming white plaster remain intact today."
    ("image", "ep06_31_surviving_plaster_remnants_cornice_PAN_ZOOM.jpg", "slow_dolly_forward"),

    # Act VII: The Mountain That Refused to Fall (Cuts 55-63)
    # 55. "The true test of a building is not just how it was made, but how it withstands the desire to destroy it."
    ("image", "ep06_archive_10_aurangzeb_court_chronicle_manuscript_PAN_ZOOM.jpg", "pan_right"),
    # 56. "In the late seventeenth century, Mughal Emperor Aurangzeb set his camp near Ellora and ordered the temple demolished."
    ("image", "ep06_33_1682_aurangzeb_royal_camp_PAN_ZOOM.jpg", "slow_zoom_in"),
    # 57. "A task force of over one thousand workers equipped with heavy sledgehammers, crowbars, and chisels was dispatched to level Cave 16."
    ("image", "ep06_34_demolition_taskforce_tools_PAN_ZOOM.jpg", "slow_tilt_down"),
    # 58. "For over a year, demolition teams hammered relentlessly against the temple facade, day and night."
    ("video", "ep06_gf_13_aurangzeb_demolition_siege.mp4", "action_clip"),
    # 59. "In conventional stone temples built of mortar and stacked masonry blocks, knocking out a few key pillars causes the roof to cave in."
    ("image", "ep06_13_rope_rigging_anchor_points_PAN_ZOOM.jpg", "slow_drift"),
    # 60. "But Kailasa is not a building; it is a solid mountain peak."
    ("image", "ep06_cinematic_aurangzeb_demolition_quarry_scars_PAN_ZOOM.jpg", "slow_zoom_in"),
    # 61. "The workers broke chisels, chipped away outer statues, and defaced decorative reliefs, but the structural core refused to budge."
    ("image", "ep06_35_failed_demolition_scars_basalt_PAN_ZOOM.jpg", "slow_dolly_forward"),
    # 62. "After months of brutal labor and negligible structural progress, Aurangzeb conceded defeat and abandoned the demolition effort."
    ("image", "ep06_archive_07_rashtrakuta_iron_mine_smelting_PAN_ZOOM.jpg", "slow_drift"),
    # 63. "The living bedrock of the Deccan Traps proved stronger than imperial siege weapons."
    ("image", "ep06_archive_02_kailasa_ground_plan_schematic_PAN_ZOOM.jpg", "slow_zoom_out"),

    # Act VIII: The Architect's Confession (Cuts 64-72)
    # 64. "More than twelve centuries have passed since the last chisel struck the rock of Cave 16."
    ("image", "ep06_archive_12_kailasa_vimana_starry_night_PAN_ZOOM.jpg", "slow_zoom_in"),
    # 65. "In the Baroda copper-plate charter of 812 CE, King Karka the Second recorded the contemporary reaction to the finished sanctuary."
    ("image", "ep06_36_baroda_copper_plate_charter_PAN_ZOOM.jpg", "slow_dolly_forward"),
    # 66. "He wrote that celestial gods flying across the sky in heavenly chariots peered down into the chasm in absolute disbelief."
    ("image", "ep06_37_celestial_gods_view_downward_PAN_ZOOM.jpg", "slow_zoom_out"),
    # 67. "They marveled: 'This temple of Shiva is self-existent; no human skill could have fashioned such a thing.'"
    ("image", "ep06_archive_05_baroda_plates_garuda_seal_PAN_ZOOM.jpg", "slow_zoom_in"),
    # 68. "But the most poignant line in the inscription belongs to the chief architect himself."
    ("image", "ep06_archive_03_top_down_cross_section_elevation_PAN_ZOOM.jpg", "slow_drift"),
    # 69. "Standing on the cleared courtyard floor, looking up at the sky bridges, the victory pillars, and the soaring vimana, he cried out:"
    ("video", "ep06_gf_15_kokasa_architect_breakdown.mp4", "action_clip"),
    # 70. "'Katham-akrita yan-maya' — 'How was it that I could have built it?'"
    ("image", "ep06_38_architect_katham_akrita_hero_PAN_ZOOM.jpg", "slow_dolly_forward"),
    # 71. "Even the mind that conceived the impossible could not believe that mortal hands had brought it into the light."
    ("image", "ep06_16_tempered_chisel_arsenal_PAN_ZOOM.jpg", "slow_drift"),
    # 72. "And that remains the eternal mystery of Kailasa: a monument that surpasses the comprehension of its own creators."
    ("video", "ep06_gf_16_climax_crepuscular_rays_chasm.mp4", "action_clip")
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

def check_video_prerequisites():
    missing = []
    for mtype, fname, _ in MANIFEST:
        if mtype == "video":
            src = VIDEOS_DIR / fname
            if not src.exists() or src.stat().st_size == 0:
                missing.append(fname)
    return missing

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

def assemble_master_preview():
    print("=" * 65)
    print("  ASSEMBLING MASTER PREVIEW (1080P 30FPS, 72 UNIQUE BEATS)")
    print("=" * 65)

    # 1. Assert zero repetition
    fnames = [m[1] for m in MANIFEST]
    assert len(fnames) == len(set(fnames)), f"Duplicate media assets in manifest! {len(fnames)} vs {len(set(fnames))}"
    print(f"[*] Verified Zero-Repetition Invariant: {len(fnames)} unique media assets for {len(MANIFEST)} cuts.")

    # 2. Check Prerequisites
    missing = check_video_prerequisites()
    if missing:
        print("\n" + "!" * 65)
        print("  GOOGLE FLOW VIDEO GATE: ACTION CLIPS PENDING")
        print("!" * 65)
        print(f"The following {len(missing)} bespoke action videos are required before rendering:")
        for v in missing:
            print(f"  - {v}")
        print("\nPlease generate these clips using the prompts in:")
        print(f"  {EPISODE_DIR / 'google_flow_input_images' / 'GOOGLE_FLOW_PROMPT_SHEET.md'}")
        print(f"and place them into:")
        print(f"  {VIDEOS_DIR}")
        print("!" * 65 + "\n")
        return None

    # 3. Timing Lock
    mixed_audio = AUDIO_DIR / "episode_06_master_audio_mixed.mp3"
    master_audio = mixed_audio if mixed_audio.exists() else (AUDIO_DIR / "episode_06_narration_master.mp3")
    total_audio_dur = get_media_duration(master_audio)
    cues = parse_srt_cues(SUB_DIR / "episode_06_full.srt")
    assert len(cues) == len(MANIFEST), f"Cues count ({len(cues)}) != Manifest count ({len(MANIFEST)})"
    durations = derive_cut_durations(cues, total_audio_dur)

    print(f"[*] Master audio track: {master_audio.name} ({total_audio_dur:.3f}s)")
    print(f"[*] Sum of all {len(durations)} cut durations: {sum(durations):.3f}s (0.0ms drift)")

    temp_dir = OUTPUT_DIR / "temp_subsegments"
    temp_dir.mkdir(parents=True, exist_ok=True)

    sub_files = []
    print(f"\n[*] Rendering {len(MANIFEST)} subsegments (video-only, 1080p 30fps)...")
    for idx, ((mtype, fname, motion), dur) in enumerate(zip(MANIFEST, durations)):
        print(f"  [{idx+1:02d}/{len(MANIFEST)}] {mtype.upper():<5} | {fname[:38]:<38} | {dur:4.2f}s | {motion}")
        sub_path = render_subsegment(mtype, fname, motion, dur, idx, len(MANIFEST), temp_dir)
        sub_files.append(sub_path)
    print(f"\n[*] All {len(MANIFEST)} subsegments rendered cleanly!")

    # 4. Concat Video Track
    concat_txt = OUTPUT_DIR / "temp_ep06_concat.txt"
    with open(concat_txt, "w", encoding="utf-8") as f:
        for p in sub_files:
            f.write(f"file '{p.as_posix()}'\n")

    master_v_only = OUTPUT_DIR / "temp_ep06_v_only.mp4"
    print("\n[*] Concatenating master video track...")
    cmd_concat = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_txt),
        "-c", "copy",
        str(master_v_only)
    ]
    subprocess.run(cmd_concat, capture_output=True, check=True)

    # 5. Mux Audio Track (English Default + Multi-language Hindi Track option)
    master_out = OUTPUT_DIR / "episode_06_master_preview.mp4"
    print(f"[*] Muxing master audio ({master_audio.name}) -> {master_out.name}...")
    cmd_mux = [
        "ffmpeg", "-y",
        "-i", str(master_v_only),
        "-i", str(master_audio),
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        "-movflags", "+faststart",
        str(master_out)
    ]
    subprocess.run(cmd_mux, capture_output=True, check=True)

    # Cleanup temp
    if concat_txt.exists():
        concat_txt.unlink()
    if master_v_only.exists():
        master_v_only.unlink()
    shutil.rmtree(temp_dir, ignore_errors=True)

    print(f"[*] Master preview rendered successfully: {master_out.name} ({master_out.stat().st_size:,} bytes)")
    return master_out

def main():
    print("=" * 65)
    print("  KAILASA EPISODE 06 MASTER ASSEMBLY SUITE")
    print("=" * 65)
    
    missing = check_video_prerequisites()
    if missing:
        print(f"[*] Action videos pending ({len(missing)} clips).")
        print("[*] Checking asset manifest and timing integrity...")
        fnames = [m[1] for m in MANIFEST]
        assert len(fnames) == len(set(fnames)), "Duplicate media assets in manifest!"
        print(f"[*] PASS: 100% Unique Media Manifest ({len(fnames)} cuts, 0 duplicates).")
        
        cues = parse_srt_cues(SUB_DIR / "episode_06_full.srt")
        assert len(cues) == len(MANIFEST), "SRT cue count does not match manifest cut count!"
        print(f"[*] PASS: 1:1 Narration-to-Visual Spoken Anchor ({len(cues)} cues).")
        
        print("\nPrerequisites status:")
        print(f"  - Images in images/: {len(list(IMAGES_DIR.glob('*.jpg')))} (Expected: 72)")
        print(f"  - Google Flow input stills: {len(list(EPISODE_DIR.joinpath('google_flow_input_images').glob('*_GENERATE_VIDEO.jpg')))} (Expected: 16)")
        print(f"  - Action videos in videos/: {16 - len(missing)}/16 present")
        print("\nHalting before video render per Google Flow Video Gate Law and user explicit directive.")
        return
        
    master = assemble_master_preview()
    if master and master.exists():
        bundle_video = BUNDLE_DIR / "video" / "master.mp4"
        shutil.copy2(master, bundle_video)
        print(f"[*] Copied master video to OpenMontage bundle: {bundle_video.name}")

if __name__ == "__main__":
    main()
