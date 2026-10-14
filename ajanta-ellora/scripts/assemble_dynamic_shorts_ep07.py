#!/usr/bin/env python3
"""
assemble_dynamic_shorts_ep07.py — High-Retention Multi-Beat Shorts Assembler for Episode 07.
Features:
- Sentence-level micro-beat cuts (cuts every 4 to 8 seconds)
- 100% Google Flow kinetic action video clips (0% static images, 0% infographics per Law 10)
- 9:16 vertical cinematic frosted backdrop layout (1080x1920) preserving 100% of 16:9 action
- Burned-in high-contrast mobile safe-zone captions (FontSize=56, MarginV=420)
- Muxing with Adam Stone narration + ducked YouTube Audio Library score
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
EP07_DIR = BASE_DIR / "ajanta-ellora" / "episode07"
VIDEOS_DIR = EP07_DIR / "videos"
AUDIO_DIR = EP07_DIR / "audio"
SUB_DIR = EP07_DIR / "subtitles"
OUTPUT_DIR = EP07_DIR / "final_videos"
TEMP_DIR = OUTPUT_DIR / "temp_shorts_cuts_ep07"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# SHORT 01 CONFIGURATION: "The Horseshoe Canyon Hidden from the World" (34.97s)
# ---------------------------------------------------------------------------
SHORT_01_BEATS = [
    {
        "cut_id": "s1_c1",
        "asset": "ep07_gf_01_fpv_canyon_reveal.mp4",
        "dur": 5.25,
        "desc": "Hook: 30 ancient temples completely lost to human memory"
    },
    {
        "cut_id": "s1_c2",
        "asset": "ep07_gf_16_flash_flood_canyon_river_rush.mp4",
        "dur": 8.10,
        "desc": "Waghur River carved 75-meter volcanic stone fortress"
    },
    {
        "cut_id": "s1_c3",
        "asset": "ep07_gf_02_satavahana_monks_cliff_path.mp4",
        "dur": 7.56,
        "desc": "Buddhist monks hollowing mountain from top down"
    },
    {
        "cut_id": "s1_c4",
        "asset": "ep07_gf_03_topdown_roofline_excavation.mp4",
        "dur": 6.12,
        "desc": "No scaffolding, no mortar, no room for error"
    },
    {
        "cut_id": "s1_c5",
        "asset": "ep07_gf_04_vaulted_chaitya_ribbing_macro.mp4",
        "dur": 7.94,
        "desc": "Secret science of rock carving born here: CTA"
    }
]

# ---------------------------------------------------------------------------
# SHORT 02 CONFIGURATION: "How Ancient Monks Engineered Water" (38.22s)
# ---------------------------------------------------------------------------
SHORT_02_BEATS = [
    {
        "cut_id": "s2_c1",
        "asset": "ep07_gf_13_monsoon_waterfall_clearing_portal.mp4",
        "dur": 4.55,
        "desc": "Hook: How do you keep monsoon from drowning mountain monastery?"
    },
    {
        "cut_id": "s2_c2",
        "asset": "ep07_gf_05_monsoon_plateau_gutter_sheet.mp4",
        "dur": 8.45,
        "desc": "Millions of gallons crashing over cliff edge every summer"
    },
    {
        "cut_id": "s2_c3",
        "asset": "ep07_gf_10_columnar_basalt_quarry_split.mp4",
        "dur": 2.80,
        "desc": "Their solution was pure genius"
    },
    {
        "cut_id": "s2_c4",
        "asset": "ep07_gf_14_torchlit_podhi_descent.mp4",
        "dur": 6.94,
        "desc": "Chiseled massive diversion canals to route floodwaters"
    },
    {
        "cut_id": "s2_c5",
        "asset": "ep07_gf_06_podhi_cistern_water_filtration.mp4",
        "dur": 7.45,
        "desc": "Dug subterranean cisterns trapping percolating rock water"
    },
    {
        "cut_id": "s2_c6",
        "asset": "ep07_gf_07_monk_chanting_acoustic_resonance.mp4",
        "dur": 8.04,
        "desc": "Natural basalt filtration, ice cold water all year round"
    }
]

def render_vertical_cut(asset_name: str, duration: float, out_path: Path):
    """
    Renders 16:9 action video into 9:16 vertical (1080x1920) using frosted blurred backdrop.
    Preserves 100% of the cinematic action video frame.
    """
    src_video = VIDEOS_DIR / asset_name
    if not src_video.exists():
        raise FileNotFoundError(f"Missing required action video: {src_video}")
        
    filter_complex = (
        "[0:v]split[v_bg][v_fg];"
        "[v_bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5,eq=brightness=-0.15[bg];"
        "[v_fg]scale=1080:608:force_original_aspect_ratio=decrease[fg];"
        "[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1[v]"
    )
    
    cmd = [
        "ffmpeg", "-y",
        "-stream_loop", "-1", "-i", str(src_video),
        "-t", f"{duration:.3f}",
        "-filter_complex", filter_complex,
        "-map", "[v]",
        "-r", "30",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-an",
        str(out_path)
    ]
    subprocess.run(cmd, capture_output=True, check=True)

def assemble_short(short_id: str, beats: list, srt_filename: str, audio_filename: str, out_filename: str):
    print(f"\n[*] Assembling {short_id} (9:16 Vertical, {len(beats)} Cuts)...")
    
    cuts_dir = TEMP_DIR / short_id
    cuts_dir.mkdir(parents=True, exist_ok=True)
    
    cut_files = []
    for idx, beat in enumerate(beats):
        cut_out = cuts_dir / f"cut_{idx:02d}_{beat['cut_id']}.mp4"
        print(f"  [{idx+1}/{len(beats)}] {beat['asset']} | {beat['dur']:.2f}s | {beat['desc']}")
        render_vertical_cut(beat["asset"], beat["dur"], cut_out)
        cut_files.append(cut_out)
        
    # Concat video
    concat_txt = cuts_dir / "concat.txt"
    with open(concat_txt, "w", encoding="utf-8") as f:
        for c in cut_files:
            f.write(f"file '{c.as_posix()}'\n")
            
    v_only = cuts_dir / "v_only.mp4"
    cmd_concat = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_txt),
        "-c", "copy",
        str(v_only)
    ]
    subprocess.run(cmd_concat, capture_output=True, check=True)
    
    # Subtitle Burn-in & Audio Muxing
    srt_path = SUB_DIR / srt_filename
    sub_filter_path = str(srt_path).replace("\\", "/").replace(":", "\\:")
    
    # Vertical Safe Zone Subtitles: MarginV=420 to sit above YouTube mobile UI
    vf_sub = (
        f"subtitles='{sub_filter_path}':force_style="
        "'Fontname=Arial,Fontsize=56,PrimaryColour=&H0000FFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=4,Shadow=2,Alignment=2,MarginV=420'"
    )
    
    audio_path = AUDIO_DIR / audio_filename
    final_out = OUTPUT_DIR / out_filename
    
    print(f"[*] Burning mobile safe-zone subtitles and muxing audio -> {final_out.name}...")
    cmd_final = [
        "ffmpeg", "-y",
        "-i", str(v_only),
        "-i", str(audio_path),
        "-vf", vf_sub,
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        "-movflags", "+faststart",
        str(final_out)
    ]
    subprocess.run(cmd_final, capture_output=True, check=True)
    
    # Cleanup temp cuts
    shutil.rmtree(cuts_dir, ignore_errors=True)
    print(f"[OK] Generated Vertical Short: {final_out.name} ({final_out.stat().st_size:,} bytes)")
    return final_out

def main():
    print("=" * 65)
    print("  EPISODE 07 COMPANION SHORTS MULTI-CUT ASSEMBLY")
    print("=" * 65)
    
    # Short 01
    assemble_short(
        short_id="short_01",
        beats=SHORT_01_BEATS,
        srt_filename="short_01_the_horseshoe_canyon_hidden_from_the_world.srt",
        audio_filename="short_01_the_horseshoe_canyon_hidden_from_the_world_mixed.mp3",
        out_filename="short_01_the_horseshoe_canyon_hidden_from_the_world_1080x1920.mp4"
    )
    
    # Short 02
    assemble_short(
        short_id="short_02",
        beats=SHORT_02_BEATS,
        srt_filename="short_02_how_ancient_monks_engineered_water.srt",
        audio_filename="short_02_how_ancient_monks_engineered_water_mixed.mp3",
        out_filename="short_02_how_ancient_monks_engineered_water_1080x1920.mp4"
    )
    
    print("\n" + "=" * 65)
    print("  COMPANION SHORTS ASSEMBLY COMPLETE")
    print("=" * 65)

if __name__ == "__main__":
    main()
