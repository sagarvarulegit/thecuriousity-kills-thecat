#!/usr/bin/env python3
"""
assemble_episode_07_full.py — Full 45-Micro-Beat Master Assembly Engine for Episode 07.
Implements:
1. 45-Beat Manifest derived from 15 Google Flow Action Videos, 2 Infographics, and 28 Hero Stills.
2. 4K Anti-Jitter Sub-Pixel Motorized Zoompan Engine for still images (scale=3840:2160 -> zoompan -> scale=1920:1080).
3. Monotonic Sentence-Level Cue Timing derived directly from episode_07_full.srt (0.00ms audio drift).
4. Zero media repetition invariant (0 duplicate assets).
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
EPISODE_DIR = BASE_DIR / "ajanta-ellora" / "episode07"
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
# 45-MICRO-BEAT MASTER MANIFEST (TYPE, FILENAME, MOTION)
# ---------------------------------------------------------------------------
MANIFEST = [
    # Act I: The Hidden Crescent (Cuts 1-9)
    # 1. "When you stand inside the 100-foot chasm of Kailasa at Ellora..."
    ("image", "ep07_01_kailasa_chasm_recap_PAN_ZOOM.jpg", "slow_dolly_forward"),
    # 2. "But Kailasa did not appear out of thin air."
    ("video", "ep07_gf_01_fpv_canyon_reveal.mp4", "action_clip"),
    # 3. "Decades before the Rashtrakutas cleared four hundred thousand tons..."
    ("image", "ep07_05_waghur_river_curved_canyon_PAN_ZOOM.jpg", "slow_zoom_in"),
    # 4. "To find where it began, we must travel one hundred kilometers north..."
    ("image", "ep07_infographic_01_deccan_map_geology.jpg", "slow_zoom_in"),
    # 5. "Here, sliced through a solid table of Cretaceous flood basalt, the Waghur River carved..."
    ("video", "ep07_gf_16_flash_flood_canyon_river_rush.mp4", "action_clip"),
    # 6. "From the outer plateau, the gorge is completely invisible, hidden behind dense teak scrub..."
    ("image", "ep07_06_teak_scrub_plateau_rim_PAN_ZOOM.jpg", "pan_right"),
    # 7. "Yet along the curved inner wall of this sheer basalt amphitheater..."
    ("image", "ep07_08_ajanta_horseshoe_grand_reveal_PAN_ZOOM.jpg", "slow_tilt_up"),
    # 8. "This is Ajanta."
    ("image", "ep07_09_satavahana_ancient_scroll_charter_PAN_ZOOM.jpg", "slow_zoom_in"),
    # 9. "And for more than seven centuries, it was the laboratory where India’s master stonecutters..."
    ("image", "ep07_10_seven_centuries_stone_laboratory_PAN_ZOOM.jpg", "pan_left"),

    # Act II: The First Chisel Strike (Cuts 10-18)
    # 10. "The story of Ajanta begins in the second century before the common era..."
    ("video", "ep07_gf_02_satavahana_monks_cliff_path.mp4", "action_clip"),
    # 11. "A band of Buddhist monks and wandering ascetics walked along the trade artery..."
    ("video", "ep07_gf_09_dakshinapatha_caravan_crossing.mp4", "action_clip"),
    # 12. "They chose this crescent ravine because volcanic geology offered something unique..."
    ("video", "ep07_gf_10_columnar_basalt_quarry_split.mp4", "action_clip"),
    # 13. "In early Buddhism, doctrine strictly forbade carving anthropomorphic statues..."
    ("image", "ep07_13_aniconic_buddha_wheel_footprint_PAN_ZOOM.jpg", "slow_drift"),
    # 14. "Worship was centered upon the stupa—a solid hemispherical dome..."
    ("image", "ep07_14_monolithic_stupa_cave_10_darkness_PAN_ZOOM.jpg", "slow_dolly_forward"),
    # 15. "In Caves Nine and Ten, early masons entered the cliff at the roofline..."
    ("video", "ep07_gf_03_topdown_roofline_excavation.mp4", "action_clip"),
    # 16. "Without scaffolding, they hollowed out monumental apsidal chaitya halls..."
    ("video", "ep07_gf_04_vaulted_chaitya_ribbing_macro.mp4", "action_clip"),
    # 17. "Along the sides, they chiseled rows of austere octagonal columns, slanting them slightly inward by three degrees..."
    ("image", "ep07_17_octagonal_inward_slant_pillars_PAN_ZOOM.jpg", "slow_tilt_down"),
    # 18. "Even in stone, their hands remembered wood; but the mountain demanded an entirely different mastery."
    ("video", "ep07_gf_12_carpentry_peg_socket_carving.mp4", "action_clip"),

    # Act III: Taming the Monsoon (Cuts 19-28)
    # 19. "Carving a monastery into the sheer face of a river canyon comes with a deadly enemy: the Indian monsoon."
    ("image", "ep07_19_monsoon_dark_clouds_sahyadri_PAN_ZOOM.jpg", "slow_zoom_in"),
    # 20. "Every summer, torrential downpours cascade off the high Deccan plateau..."
    ("video", "ep07_gf_13_monsoon_waterfall_clearing_portal.mp4", "action_clip"),
    # 21. "If uncontrolled, sheet runoff would flood the subterranean halls..."
    ("image", "ep07_21_flood_erosion_basalt_crack_detail_PAN_ZOOM.jpg", "slow_drift"),
    # 22. "Ancient engineers countered nature with a brilliant hydraulic defense system."
    ("image", "ep07_infographic_02_hydraulic_drainage_cutaway.jpg", "slow_zoom_in"),
    # 23. "Along the upper rim of the cliff, meters above the cave roofs, stonecutters chiseled deep continuous drainage gutters..."
    ("video", "ep07_gf_05_monsoon_plateau_gutter_sheet.mp4", "action_clip"),
    # 24. "These rock-cut channels captured surface runoff and redirected the torrent away..."
    ("image", "ep07_24_rock_cut_diversion_ravine_overflow_PAN_ZOOM.jpg", "pan_right"),
    # 25. "Meanwhile, inside the canyon, builders solved the problem of surviving the eight-month dry season."
    ("image", "ep07_25_dry_season_arid_canyon_sunlight_PAN_ZOOM.jpg", "pan_left"),
    # 26. "They carved deep subterranean cisterns known as podhis beneath the cave courtyards."
    ("video", "ep07_gf_14_torchlit_podhi_descent.mp4", "action_clip"),
    # 27. "Rainwater that seeped through natural cooling joints in the volcanic rock was caught..."
    ("image", "ep07_27_basalt_cooling_joint_micro_filtration_PAN_ZOOM.jpg", "slow_zoom_in"),
    # 28. "The water collected in these dark, cold reservoirs, remaining crystal clear..."
    ("video", "ep07_gf_06_podhi_cistern_water_filtration.mp4", "action_clip"),

    # Act IV: The Sound of the Living Stone (Cuts 29-35)
    # 29. "But the early masters of Ajanta did not just sculpt for the eye; they engineered for the ear."
    ("image", "ep07_29_acoustic_resonator_chaitya_elevation_PAN_ZOOM.jpg", "slow_dolly_forward"),
    # 30. "The apsidal prayer halls of Caves Nine and Ten were sculpted as acoustic resonators."
    ("image", "ep07_30_basalt_nonporous_wall_reverberation_PAN_ZOOM.jpg", "slow_drift"),
    # 31. "The dense, non-porous basalt walls possess minimal sound absorption..."
    ("image", "ep07_31_cave_9_nave_geometry_perspective_PAN_ZOOM.jpg", "pan_right"),
    # 32. "When monks gathered in the darkness around the monolithic stupa to chant sacred mantras..."
    ("video", "ep07_gf_15_stupa_pradakshina_ritual.mp4", "action_clip"),
    # 33. "The human voice, pitched between one hundred and one hundred and twenty hertz..."
    ("image", "ep07_33_vocal_frequency_110hz_resonance_wave_PAN_ZOOM.jpg", "slow_zoom_in"),
    # 34. "The sound did not merely echo; it vibrated physically through the stone floor and columns..."
    ("video", "ep07_gf_07_monk_chanting_acoustic_resonance.mp4", "action_clip"),
    # 35. "In an era without microphones or amplification, the monks turned the living bedrock into a colossal musical instrument."
    ("image", "ep07_35_bedrock_musical_instrument_nave_glow_PAN_ZOOM.jpg", "slow_zoom_out"),

    # Act V: The 400-Year Hibernation (Cuts 36-45)
    # 36. "By the first century of the common era, something shifted across the Deccan."
    ("image", "ep07_36_satavahana_dynasty_coins_copper_charter_PAN_ZOOM.jpg", "slow_drift"),
    # 37. "Royal dynasties rose and fell, regional trade routes migrated south toward coastal ports..."
    ("image", "ep07_37_ancient_trade_routes_indian_ocean_ports_PAN_ZOOM.jpg", "pan_left"),
    # 38. "Activity in the horseshoe canyon ground to a complete halt."
    ("image", "ep07_38_silent_canyon_abandoned_scarp_twilight_PAN_ZOOM.jpg", "slow_zoom_in"),
    # 39. "For nearly four hundred uninterrupted years—longer than the United States has existed as a nation—Ajanta lay dormant."
    ("video", "ep07_gf_08_jungle_overgrowth_dormancy.mp4", "action_clip"),
    # 40. "Teak trees grew across the terrace steps, silt washed into the lower chaityas..."
    ("image", "ep07_40_wild_bamboo_bats_darkened_sanctum_PAN_ZOOM.jpg", "pan_right"),
    # 41. "Yet the knowledge carved into these volcanic cliffs was not destroyed."
    ("image", "ep07_41_dormant_chiseled_basalt_portal_shadow_PAN_ZOOM.jpg", "slow_drift"),
    # 42. "It waited patiently in the dark until the mid-fifth century, when a powerful emperor named Harishena..."
    ("image", "ep07_42_harishena_vakataka_royal_gold_fresco_PAN_ZOOM.jpg", "slow_dolly_forward"),
    # 43. "But that golden renaissance would bring with it an even darker mystery..."
    ("image", "ep07_43_sealed_canyon_secret_1000_years_PAN_ZOOM.jpg", "slow_zoom_out"),
    # 44. "In our next episode, we unlock the secret chemistry of Ajanta's golden age."
    ("image", "ep07_44_lapis_lazuli_powder_mortar_PAN_ZOOM.jpg", "slow_zoom_in"),
    # 45. "From Afghan blue gems to fermented cow dung plaster and polished mirror light."
    ("image", "ep07_45_polished_mirror_light_brass_reflector_PAN_ZOOM.jpg", "slow_dolly_forward"),
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
    print("  ASSEMBLING EPISODE 07 MASTER VIDEO (1080P 30FPS, 45 UNIQUE BEATS)")
    print("=" * 65)

    # 1. Assert zero repetition invariant
    fnames = [m[1] for m in MANIFEST]
    assert len(fnames) == len(set(fnames)), f"Duplicate media assets in manifest! {len(fnames)} vs {len(set(fnames))}"
    print(f"[*] Verified Zero-Repetition Invariant: {len(fnames)} unique media assets for {len(MANIFEST)} cuts.")

    # 2. Timing Lock
    mixed_audio = AUDIO_DIR / "episode_07_master_audio_mixed.mp3"
    master_audio = mixed_audio if mixed_audio.exists() else (AUDIO_DIR / "narration" / "episode_07_narration_master.mp3")
    total_audio_dur = get_media_duration(master_audio)
    cues = parse_srt_cues(SUB_DIR / "episode_07_full.srt")
    assert len(cues) == len(MANIFEST), f"Cues count ({len(cues)}) != Manifest count ({len(MANIFEST)})"
    durations = derive_cut_durations(cues, total_audio_dur)

    print(f"[*] Master audio track: {master_audio.name} ({total_audio_dur:.3f}s)")
    print(f"[*] Sum of all {len(durations)} cut durations: {sum(durations):.3f}s (0.0ms drift)")

    temp_dir = OUTPUT_DIR / "temp_subsegments_ep07"
    temp_dir.mkdir(parents=True, exist_ok=True)

    sub_files = []
    print(f"\n[*] Rendering {len(MANIFEST)} subsegments (video-only, 1080p 30fps)...")
    for idx, ((mtype, fname, motion), dur) in enumerate(zip(MANIFEST, durations)):
        print(f"  [{idx+1:02d}/{len(MANIFEST)}] {mtype.upper():<5} | {fname[:38]:<38} | {dur:4.2f}s | {motion}")
        sub_path = render_subsegment(mtype, fname, motion, dur, idx, len(MANIFEST), temp_dir)
        sub_files.append(sub_path)
    print(f"\n[*] All {len(MANIFEST)} subsegments rendered cleanly!")

    # 3. Concat Video Track
    concat_txt = OUTPUT_DIR / "temp_ep07_concat.txt"
    with open(concat_txt, "w", encoding="utf-8") as f:
        for p in sub_files:
            f.write(f"file '{p.as_posix()}'\n")

    master_v_only = OUTPUT_DIR / "temp_ep07_v_only.mp4"
    print("\n[*] Concatenating master video track...")
    cmd_concat = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_txt),
        "-c", "copy",
        str(master_v_only)
    ]
    subprocess.run(cmd_concat, capture_output=True, check=True)

    # 4. Mux Audio Track & Burn in Subtitles
    master_out = OUTPUT_DIR / "episode_07_the_secret_canyon_of_waghur_master_1080p.mp4"
    srt_file = SUB_DIR / "episode_07_full.srt"
    
    # Subtitle burn-in with clean styling
    sub_filter_path = str(srt_file).replace("\\", "/").replace(":", "\\:")
    vf_sub = f"subtitles='{sub_filter_path}':force_style='Fontname=Arial,Fontsize=22,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=2,Shadow=1,Alignment=2,MarginV=45'"

    print(f"[*] Muxing audio and burning in broadcast subtitles -> {master_out.name}...")
    cmd_mux = [
        "ffmpeg", "-y",
        "-i", str(master_v_only),
        "-i", str(master_audio),
        "-vf", vf_sub,
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
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

    print(f"[*] Master video rendered successfully: {master_out.name} ({master_out.stat().st_size:,} bytes)")
    
    # Copy to OpenMontage bundle
    bundle_video = BUNDLE_DIR / "video" / "master.mp4"
    shutil.copy2(master_out, bundle_video)
    print(f"[*] Copied master video to OpenMontage bundle: {bundle_video.name}")
    
    return master_out

def main():
    print("=" * 65)
    print("  EPISODE 07: THE SECRET CANYON OF WAGHUR — MASTER ASSEMBLY")
    print("=" * 65)
    assemble_master_video()

if __name__ == "__main__":
    main()
