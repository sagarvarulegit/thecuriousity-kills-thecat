#!/usr/bin/env python3
"""
assemble_dynamic_shorts_ep08.py — High-Retention Multi-Beat Shorts Assembler for Episode 08.
Channel: thecuriousity-kills-thecat

Features:
- Multi-cut pacing timed directly to spoken sentence cues (5 cuts per short)
- Repurposes the 10 Google Flow action videos (Zero extra generation cost, Law 7)
- 9:16 vertical cinematic frosted backdrop layout (1080x1920) preserving 100% of 16:9 action
- Mobile safe-zone subtitles (FontSize=56, MarginV=420)
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
EP08_DIR = BASE_DIR / "ajanta-ellora" / "episode08"
VIDEOS_DIR = EP08_DIR / "videos"
IMAGES_DIR = EP08_DIR / "images"
AUDIO_DIR = EP08_DIR / "audio"
SUB_DIR = EP08_DIR / "subtitles"
OUTPUT_DIR = EP08_DIR / "final_videos"
TEMP_DIR = OUTPUT_DIR / "temp_shorts_cuts_ep08"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# SHORT 01 CONFIGURATION: "The Mud Chemistry Secret" (50.90s)
# ---------------------------------------------------------------------------
SHORT_01_BEATS = [
    {
        "cut_id": "s1_c1",
        "video_asset": "ep08_gf_04_plaster_kneading_cowdung_matrix.mp4",
        "still_asset": "ep08_gf_04_plaster_kneading_cowdung_matrix_GENERATE_VIDEO.jpg",
        "dur": 9.54,
        "desc": "Hook: How did fermented mud and cow dung survive 1,500 years?"
    },
    {
        "cut_id": "s1_c2",
        "video_asset": "ep08_gf_05_chipping_basalt_key_sparks.mp4",
        "still_asset": "ep08_gf_05_chipping_basalt_key_sparks_GENERATE_VIDEO.jpg",
        "dur": 9.10,
        "desc": "Chipping mechanical key into cold volcanic basalt wall"
    },
    {
        "cut_id": "s1_c3",
        "video_asset": "ep08_gf_17_artisan_spreading_lime_plaster_finish.mp4",
        "still_asset": "ep08_gf_17_artisan_spreading_lime_plaster_finish_GENERATE_VIDEO.jpg",
        "dur": 12.18,
        "desc": "Spreading living bio-plaster and white lime finish coat"
    },
    {
        "cut_id": "s1_c4",
        "video_asset": "ep08_gf_06_agate_burnishing_intonaco.mp4",
        "still_asset": "ep08_gf_06_agate_burnishing_intonaco_GENERATE_VIDEO.jpg",
        "dur": 9.80,
        "desc": "Agate river stone burnishing lime plaster to porcelain sheen"
    },
    {
        "cut_id": "s1_c5",
        "video_asset": "ep08_gf_03_mortar_grinding_lapis_powder.mp4",
        "still_asset": "ep08_gf_03_mortar_grinding_lapis_powder_GENERATE_VIDEO.jpg",
        "dur": 10.28,
        "desc": "The impossible Afghan blue pigment: Related Video CTA"
    }
]

# ---------------------------------------------------------------------------
# SHORT 02 CONFIGURATION: "The Bronze Mirror Secret" (51.59s)
# ---------------------------------------------------------------------------
SHORT_02_BEATS = [
    {
        "cut_id": "s2_c1",
        "video_asset": "ep08_gf_08_brush_applying_lapis_eyelash.mp4",
        "still_asset": "ep08_gf_08_brush_applying_lapis_eyelash_GENERATE_VIDEO.jpg",
        "dur": 9.11,
        "desc": "Hook: Painting microscopic details in pitch blackness without fire"
    },
    {
        "cut_id": "s2_c2",
        "video_asset": "ep08_gf_14_mustard_oil_lamp_soot_smoke.mp4",
        "still_asset": "ep08_gf_14_mustard_oil_lamp_soot_smoke_GENERATE_VIDEO.jpg",
        "dur": 11.08,
        "desc": "Torches produce thick soot; yet cave ceilings have zero carbon smoke"
    },
    {
        "cut_id": "s2_c3",
        "video_asset": "ep08_gf_07_bronze_mirror_sunlight_beam.mp4",
        "still_asset": "ep08_gf_07_bronze_mirror_sunlight_beam_GENERATE_VIDEO.jpg",
        "dur": 9.21,
        "desc": "Polished cast-bronze mirrors reflecting focused beams of sun"
    },
    {
        "cut_id": "s2_c4",
        "video_asset": "ep08_gf_15_wet_linen_diffuser_light_beam.mp4",
        "still_asset": "ep08_gf_15_wet_linen_diffuser_light_beam_GENERATE_VIDEO.jpg",
        "dur": 9.50,
        "desc": "Wet white linen diffusers filling chambers with shadowless daylight"
    },
    {
        "cut_id": "s2_c5",
        "video_asset": "ep08_gf_16_abandoned_chisel_dropped_brush.mp4",
        "still_asset": "ep08_gf_16_abandoned_chisel_dropped_brush_GENERATE_VIDEO.jpg",
        "dur": 12.69,
        "desc": "477 CE sudden abandonment: Related Video CTA"
    }
]

def render_vertical_cut(beat: dict, out_path: Path):
    """
    Renders 16:9 media into 9:16 vertical (1080x1920) using frosted blurred backdrop.
    Uses video clip if present in VIDEOS_DIR; otherwise uses still asset with zoompan.
    """
    v_src = VIDEOS_DIR / beat["video_asset"]
    dur = beat["dur"]
    
    if v_src.exists():
        filter_complex = (
            "[0:v]split[v_bg][v_fg];"
            "[v_bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5,eq=brightness=-0.15[bg];"
            "[v_fg]scale=1080:608:force_original_aspect_ratio=decrease[fg];"
            "[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1[v]"
        )
        cmd = [
            "ffmpeg", "-y",
            "-stream_loop", "-1", "-i", str(v_src),
            "-t", f"{dur:.3f}",
            "-filter_complex", filter_complex,
            "-map", "[v]",
            "-r", "30",
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-pix_fmt", "yuv420p",
            "-an",
            str(out_path)
        ]
    else:
        # Internal development fallback using still
        s_src = IMAGES_DIR / beat["still_asset"]
        if not s_src.exists():
            raise FileNotFoundError(f"Neither video nor still asset exists: {beat['video_asset']} / {beat['still_asset']}")
            
        filter_complex = (
            "[0:v]split[v_bg][v_fg];"
            "[v_bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5,eq=brightness=-0.15[bg];"
            "[v_fg]scale=1080:608:force_original_aspect_ratio=decrease[fg];"
            "[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1[v]"
        )
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1", "-i", str(s_src),
            "-t", f"{dur:.3f}",
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
        print(f"  [{idx+1}/{len(beats)}] {beat['cut_id']} | {beat['dur']:.2f}s | {beat['desc']}")
        render_vertical_cut(beat, cut_out)
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
    print("  EPISODE 08 COMPANION SHORTS MULTI-CUT ASSEMBLY")
    print("=" * 65)
    
    # Short 01
    assemble_short(
        short_id="short_01",
        beats=SHORT_01_BEATS,
        srt_filename="short_01_the_mud_chemistry_secret.srt",
        audio_filename="short_01_the_mud_chemistry_secret_mixed.mp3",
        out_filename="short_01_the_mud_chemistry_secret_1080x1920.mp4"
    )
    
    # Short 02
    assemble_short(
        short_id="short_02",
        beats=SHORT_02_BEATS,
        srt_filename="short_02_the_bronze_mirror_secret.srt",
        audio_filename="short_02_the_bronze_mirror_secret_mixed.mp3",
        out_filename="short_02_the_bronze_mirror_secret_1080x1920.mp4"
    )
    
    print("\n" + "=" * 65)
    print("  COMPANION SHORTS ASSEMBLY COMPLETE")
    print("=" * 65)

if __name__ == "__main__":
    main()
