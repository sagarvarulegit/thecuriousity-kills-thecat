#!/usr/bin/env python3
"""
assemble_dynamic_shorts_ep05.py — High-Retention Multi-Beat Shorts Assembler for Episode 05
Transforms the companion YouTube Shorts into viral, multi-cut vertical masterpieces.
Features:
- Sentence-level micro-beat cuts (cuts every 2.5 to 7.5 seconds)
- Splicing of 1080p Google Flow kinetic action video clips + 2D blueprint cards
- 9:16 vertical cinematic center-framing (1080x1920)
- Burned-in high-contrast mobile safe-zone captions (Arial Bold, white text, black border)
- Muxing with ElevenLabs Adam Stone narration + ducked orchestral music bed
"""

import os
import re
import sys
import shutil
import subprocess
from pathlib import Path

# Fix Windows console UTF-8 encoding
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

BASE_DIR = Path("C:/Sagar/Projects/thecuriousity-kills-thecat")
EP05_DIR = BASE_DIR / "ajanta-ellora" / "episode05"
IMAGES_DIR = EP05_DIR / "images"
VIDEOS_DIR = EP05_DIR / "videos"
AUDIO_DIR = EP05_DIR / "audio"
SUB_DIR = EP05_DIR / "subtitles"
OUTPUT_DIR = EP05_DIR / "final_videos"
TEMP_DIR = OUTPUT_DIR / "temp_shorts_cuts"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# SHORT 01 CONFIGURATION: "The Elephants That Carry a Temple" (28.17s)
# ---------------------------------------------------------------------------
SHORT_01_BEATS = [
    {
        "cut_id": "s1_c1",
        "type": "video",
        "asset": "ep05_gf_01_first_encounter_chasm_dawn.mp4",
        "dur": 3.262,
        "desc": "Hook: Elephant head emerging from volcanic basalt at dawn"
    },
    {
        "cut_id": "s1_c2",
        "type": "video",
        "asset": "ep05_gf_03_continuous_ring_elephant_procession.mp4",
        "dur": 4.969,
        "desc": "Continuous ring of marching elephants supporting temple plinth"
    },
    {
        "cut_id": "s1_c3",
        "type": "image",
        "asset": "ep05_infographic_01_plinth_elevation_profile.jpg",
        "dur": 7.222,
        "desc": "Technical Blueprint: Elevation showing relief vs separate columns"
    },
    {
        "cut_id": "s1_c4",
        "type": "video",
        "asset": "ep05_gf_02_life_size_scale_human_silhouette.mp4",
        "dur": 6.653,
        "desc": "Human scale: Monk walking beside giant elephant flank"
    },
    {
        "cut_id": "s1_c5",
        "type": "video",
        "asset": "ep05_gf_06_3d_corner_projection_elephant.mp4",
        "dur": 2.589,
        "desc": "3D corner elephant bursting outward from solid bedrock"
    },
    {
        "cut_id": "s1_c6",
        "type": "video",
        "asset": "ep05_gf_04_dynamic_combat_and_baby_elephant.mp4",
        "dur": 3.475,
        "desc": "Adult elephant in combat & baby elephant clinging to leg"
    }
]

# ---------------------------------------------------------------------------
# SHORT 02 CONFIGURATION: "Why Elephants Support the Mountain" (33.60s)
# ---------------------------------------------------------------------------
SHORT_02_BEATS = [
    {
        "cut_id": "s2_c1",
        "type": "video",
        "asset": "ep05_gf_06_3d_corner_projection_elephant.mp4",
        "dur": 5.155,
        "desc": "Hook Question: 3D corner elephant projecting from bedrock"
    },
    {
        "cut_id": "s2_c2",
        "type": "video",
        "asset": "ep05_gf_03_continuous_ring_elephant_procession.mp4",
        "dur": 6.107,
        "desc": "Procession: Continuous tracking along the plinth elephants"
    },
    {
        "cut_id": "s2_c3",
        "type": "video",
        "asset": "ep05_gf_05_havell_cloud_island_mist.mp4",
        "dur": 7.650,
        "desc": "Havell's Cloud Island: Morning mist making temple float on clouds"
    },
    {
        "cut_id": "s2_c4",
        "type": "image",
        "asset": "ep05_infographic_06_havell_cloud_hypothesis.jpg",
        "dur": 6.723,
        "desc": "Technical Blueprint: Havell's Vedic Cloud Hypothesis comparison"
    },
    {
        "cut_id": "s2_c5",
        "type": "video",
        "asset": "ep05_gf_08_mountain_hoisted_celestial_ascent.mp4",
        "dur": 7.965,
        "desc": "Climax: Upward crane shot hoisting mountain into heavens"
    }
]

def render_vertical_cut(cut_def: dict, out_path: Path) -> Path:
    mtype = cut_def["type"]
    dur = cut_def["dur"]
    fname = cut_def["asset"]
    fps = 30
    frames = max(1, int(dur * fps))
    
    if mtype == "video":
        src = VIDEOS_DIR / fname
        if not src.exists():
            raise FileNotFoundError(f"Missing video asset: {src}")
            
        # 9:16 center-crop + scale to 1080x1920
        vf = "scale=1920:1080,crop=ih*9/16:ih:(iw-ow)/2:0,scale=1080:1920,setsar=1,fps=30,setpts=PTS-STARTPTS"
        cmd = [
            "ffmpeg", "-y",
            "-stream_loop", "-1", "-i", str(src),
            "-vf", vf,
            "-r", "30",
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-pix_fmt", "yuv420p",
            "-an",
            "-t", f"{dur:.3f}",
            str(out_path)
        ]
    else: # Image / Infographic
        src = IMAGES_DIR / fname
        if not src.exists():
            raise FileNotFoundError(f"Missing image asset: {src}")
            
        # 4K vertical pre-scaling with subtle motorized zoompan
        vf = f"scale=2160:3840:force_original_aspect_ratio=increase,crop=2160:3840,zoompan=z='1.0+0.12*(on/{frames})':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1080x1920:fps=30,vignette=angle=PI/5,eq=contrast=1.04:saturation=1.06,setsar=1,fps=30"
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1", "-i", str(src),
            "-vf", vf,
            "-r", "30",
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-pix_fmt", "yuv420p",
            "-an",
            "-t", f"{dur:.3f}",
            str(out_path)
        ]
        
    subprocess.run(cmd, check=True, capture_output=True)
    return out_path

def assemble_single_short(short_name: str, beats: list, audio_filename: str, srt_filename: str, out_filename: str):
    print("\n" + "=" * 65)
    print(f"  ASSEMBLING DYNAMIC SHORT: {short_name}")
    print(f"  ({len(beats)} micro-beat cuts | Target Audio: {audio_filename})")
    print("=" * 65)
    
    sub_files = []
    for idx, beat in enumerate(beats):
        cut_out = TEMP_DIR / f"{short_name}_cut_{idx:02d}.mp4"
        print(f"  [{idx+1}/{len(beats)}] {beat['type'].upper():<5} | {beat['asset'][:36]:<36} | {beat['dur']:4.2f}s | {beat['desc']}")
        render_vertical_cut(beat, cut_out)
        sub_files.append(cut_out)
        
    # Concat video track
    concat_txt = TEMP_DIR / f"{short_name}_concat.txt"
    with open(concat_txt, "w", encoding="utf-8") as f:
        for p in sub_files:
            f.write(f"file '{p.as_posix()}'\n")
            
    v_only = TEMP_DIR / f"{short_name}_v_only.mp4"
    cmd_concat = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_txt),
        "-c", "copy",
        str(v_only)
    ]
    subprocess.run(cmd_concat, check=True, capture_output=True)
    
    # Mux Audio and Burn Subtitles
    audio_path = AUDIO_DIR / audio_filename
    srt_path = SUB_DIR / srt_filename
    final_out = OUTPUT_DIR / out_filename
    
    # Subtitle styling in mobile safe-zone (PlayRes 1080x1920, MarginV=420 above bottom UI)
    # Forward slashes for subtitle path, escaped colon for drive letter
    srt_clean = srt_path.resolve().as_posix().replace(":", "\\:")
    style = "PlayResX=1080,PlayResY=1920,FontName=Arial,FontSize=56,Bold=1,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=4,Shadow=2,Alignment=2,MarginV=420"
    sub_filter = f"subtitles='{srt_clean}':force_style='{style}'"
    
    print(f"[*] Muxing audio ({audio_path.name}) & burning mobile captions ({srt_path.name})...")
    cmd_mux = [
        "ffmpeg", "-y",
        "-i", str(v_only),
        "-i", str(audio_path),
        "-vf", sub_filter,
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        "-movflags", "+faststart",
        str(final_out)
    ]
    
    try:
        subprocess.run(cmd_mux, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        print(f"Subtitle burn failed, falling back to clean mux: {e}")
        cmd_mux_fallback = [
            "ffmpeg", "-y",
            "-i", str(v_only),
            "-i", str(audio_path),
            "-c:v", "copy",
            "-c:a", "aac", "-b:a", "192k",
            "-shortest",
            "-movflags", "+faststart",
            str(final_out)
        ]
        subprocess.run(cmd_mux_fallback, check=True, capture_output=True)
        
    print(f"[SUCCESS] Rendered dynamic short: {final_out.name} ({final_out.stat().st_size:,} bytes)")
    return final_out

def main():
    print("=" * 65)
    print("  KAILASA EPISODE 05 DYNAMIC MULTI-CUT SHORTS ENGINE")
    print("=" * 65)
    
    # Short 01
    s1_out = assemble_single_short(
        short_name="short_01",
        beats=SHORT_01_BEATS,
        audio_filename="short_01_the_elephants_that_carry_a_temple_mixed.mp3",
        srt_filename="short_01_the_elephants_that_carry_a_temple.srt",
        out_filename="short_01_the_elephants_that_carry_a_temple.mp4"
    )
    
    # Short 02
    s2_out = assemble_single_short(
        short_name="short_02",
        beats=SHORT_02_BEATS,
        audio_filename="short_02_why_elephants_support_the_mountain_mixed.mp3",
        srt_filename="short_02_why_elephants_support_the_mountain.srt",
        out_filename="short_02_why_elephants_support_the_mountain.mp4"
    )
    
    # Clean temp files
    shutil.rmtree(TEMP_DIR, ignore_errors=True)
    print("\n[ALL COMPLETE] Both companion Shorts upgraded to high-retention multi-cut cinematic edits!")

if __name__ == "__main__":
    main()
