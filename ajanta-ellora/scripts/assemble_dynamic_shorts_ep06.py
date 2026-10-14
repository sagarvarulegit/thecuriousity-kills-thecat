#!/usr/bin/env python3
"""
assemble_dynamic_shorts_ep06.py — High-Retention Multi-Beat Shorts Assembler for Episode 06.
Transforms companion YouTube Shorts into viral, multi-cut vertical masterpieces.
Features:
- Sentence-level micro-beat cuts (cuts every 4 to 7 seconds)
- Splicing of 1080p Google Flow kinetic action video clips + 2D blueprint cards
- 9:16 vertical cinematic center-framing (1080x1920)
- Burned-in high-contrast mobile safe-zone captions (FontSize=56, MarginV=420)
- Muxing with ElevenLabs Adam Stone narration + ducked orchestral music bed
- Enforces Google Flow Video Gate: Checks required videos before rendering.
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
EP06_DIR = BASE_DIR / "ajanta-ellora" / "episode06"
IMAGES_DIR = EP06_DIR / "images"
VIDEOS_DIR = EP06_DIR / "videos"
AUDIO_DIR = EP06_DIR / "audio"
SUB_DIR = EP06_DIR / "subtitles"
OUTPUT_DIR = EP06_DIR / "final_videos"
TEMP_DIR = OUTPUT_DIR / "temp_shorts_cuts_ep06"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# SHORT 01 CONFIGURATION: "The Sky Bridge That Shouldn't Exist" (48.16s / 51.16s mixed)
# ---------------------------------------------------------------------------
SHORT_01_BEATS = [
    {
        "cut_id": "s1_c1",
        "type": "video",
        "asset": "ep06_gf_01_sky_bridge_dawn_mist.mp4",
        "dur": 8.30,
        "desc": "Hook: 3D stress scan shows bridge shouldn't be standing"
    },
    {
        "cut_id": "s1_c2",
        "type": "video",
        "asset": "ep06_gf_02_kokasa_summit_geometry.mp4",
        "dur": 10.00,
        "desc": "Architect Kokasa surveying the abyss: Zero mortar, zero keystones, zero joints"
    },
    {
        "cut_id": "s1_c3",
        "type": "video",
        "asset": "ep06_gf_03_quarrymen_hemp_rope_void.mp4",
        "dur": 7.30,
        "desc": "Quarrymen swinging on hemp ropes hollowing out underbelly"
    },
    {
        "cut_id": "s1_c4",
        "type": "video",
        "asset": "ep06_gf_04_hammer_wedge_sparks_void.mp4",
        "dur": 8.40,
        "desc": "Basalt zero tensile strength: Gravity should have snapped stone"
    },
    {
        "cut_id": "s1_c5",
        "type": "image",
        "asset": "ep06_02_sky_bridge_underside_void_PAN_ZOOM.jpg",
        "dur": 5.20,
        "desc": "Twelve centuries later: Not sagged by a single millimeter"
    },
    {
        "cut_id": "s1_c6",
        "type": "video",
        "asset": "ep06_gf_16_climax_crepuscular_rays_chasm.mp4",
        "dur": 8.96,
        "desc": "Conversion CTA: Secret geological calculation decoded in full documentary below"
    }
]

# ---------------------------------------------------------------------------
# SHORT 02 CONFIGURATION: "The Temple That 1,000 Men Couldn't Destroy" (100% Action Videos)
# ---------------------------------------------------------------------------
SHORT_02_BEATS = [
    {
        "cut_id": "s2_c1",
        "type": "video",
        "asset": "ep06_gf_13_aurangzeb_demolition_siege.mp4",
        "dur": 9.60,
        "desc": "Hook: 1682 Aurangzeb orders 1,000 demolition engineers to destroy temple"
    },
    {
        "cut_id": "s2_c2",
        "type": "video",
        "asset": "ep06_gf_04_hammer_wedge_sparks_void.mp4",
        "dur": 7.70,
        "desc": "Iron sledges & fire: Normal building collapses if 3 pillars fall"
    },
    {
        "cut_id": "s2_c3",
        "type": "video",
        "asset": "ep06_gf_03_quarrymen_hemp_rope_void.mp4",
        "dur": 4.80,
        "desc": "Chisels shattered into scrap metal against solid basalt"
    },
    {
        "cut_id": "s2_c4",
        "type": "video",
        "asset": "ep06_gf_12_ravana_shaking_mountain_torch.mp4",
        "dur": 9.50,
        "desc": "Indestructible: A single uninterrupted 400,000-ton volcanic mountain"
    },
    {
        "cut_id": "s2_c5",
        "type": "video",
        "asset": "ep06_gf_14_torch_priest_stairwell_descent.mp4",
        "dur": 7.00,
        "desc": "Attempted foundation collapse: What they found terrified the Emperor"
    },
    {
        "cut_id": "s2_c6",
        "type": "video",
        "asset": "ep06_gf_16_climax_crepuscular_rays_chasm.mp4",
        "dur": 9.39,
        "desc": "Conversion CTA: Secret geological shield decoded in full film below"
    }
]

def render_vertical_cut(cut_def: dict, out_path: Path) -> Path:
    mtype = cut_def["type"]
    dur = cut_def["dur"]
    fname = cut_def["asset"]
    fps = 30
    
    if mtype == "video":
        src = VIDEOS_DIR / fname
        if not src.exists():
            raise FileNotFoundError(f"Missing video asset: {src}")
            
        # Widescreen-to-Vertical Frosted Backdrop Engine:
        # Background: 1080x1920 fill + heavy Gaussian boxblur + subtle darkness
        # Foreground: 1080x608 uncropped 16:9 full action view centered at (W-w)/2:(H-h)/2
        filter_complex = (
            "[0:v]split[v_bg][v_fg];"
            "[v_bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5,eq=brightness=-0.15[bg];"
            "[v_fg]scale=1080:608:force_original_aspect_ratio=decrease[fg];"
            "[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1[v]"
        )
        cmd = [
            "ffmpeg", "-y",
            "-stream_loop", "-1", "-i", str(src),
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
        src = IMAGES_DIR / fname
        if not src.exists():
            raise FileNotFoundError(f"Missing image asset: {src}")
            
        # Widescreen-to-Vertical Frosted Backdrop Engine for Infographics / Hero Stills:
        # Background: 1080x1920 fill + heavy Gaussian boxblur + subtle darkness
        # Foreground: 1080x608 uncropped 16:9 full view (100% of blueprints & text labels visible)
        filter_complex = (
            "[0:v]split[v_bg][v_fg];"
            "[v_bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5,eq=brightness=-0.15[bg];"
            "[v_fg]scale=1080:608:force_original_aspect_ratio=decrease[fg];"
            "[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1[v]"
        )
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1", "-i", str(src),
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
    return out_path

def assemble_single_short(short_name: str, beats: list, audio_filename: str, srt_filename: str, out_filename: str):
    print(f"\n{'='*60}\nASSEMBLING DYNAMIC SHORT: {short_name}\n{'='*60}")
    
    # 1. Check prerequisites
    missing = []
    for b in beats:
        if b["type"] == "video" and not (VIDEOS_DIR / b["asset"]).exists():
            missing.append(b["asset"])
        elif b["type"] == "image" and not (IMAGES_DIR / b["asset"]).exists():
            missing.append(b["asset"])
            
    if missing:
        print(f"  [GATE NOTICE] {len(missing)} required assets are pending for {short_name}:")
        for m in missing:
            print(f"    - {m}")
        print("  Halting short render until assets are generated.\n")
        return None
        
    # 2. Render subsegments
    sub_files = []
    for idx, b in enumerate(beats):
        cut_out = TEMP_DIR / f"{short_name}_cut_{idx+1:02d}.mp4"
        print(f"  [{idx+1}/{len(beats)}] {b['type'].upper():5s} | {b['asset'][:35]:35s} | {b['dur']:5.2f}s | {b['desc']}")
        render_vertical_cut(b, cut_out)
        sub_files.append(cut_out)
        
    # 3. Concatenate video stream
    concat_txt = TEMP_DIR / f"{short_name}_concat.txt"
    with open(concat_txt, "w", encoding="utf-8") as f:
        for p in sub_files:
            f.write(f"file '{p.as_posix()}'\n")
            
    raw_video = TEMP_DIR / f"{short_name}_raw_video.mp4"
    cmd_concat = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_txt),
        "-c", "copy",
        str(raw_video)
    ]
    subprocess.run(cmd_concat, capture_output=True, check=True)
    
    # 4. Burn-in mobile safe zone subtitles & mux audio
    audio_path = AUDIO_DIR / audio_filename
    srt_path = SUB_DIR / srt_filename
    final_out = OUTPUT_DIR / out_filename
    
    srt_escaped = str(srt_path).replace("\\", "/").replace(":", "\\:")
    sub_filter = f"subtitles='{srt_escaped}':force_style='Fontname=Arial,Bold=1,FontSize=56,Outline=4,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,Alignment=2,MarginV=420'"
    
    print(f"  Muxing audio & burning mobile safe zone subtitles...")
    cmd_final = [
        "ffmpeg", "-y",
        "-i", str(raw_video),
        "-i", str(audio_path),
        "-vf", sub_filter,
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        "-movflags", "+faststart",
        str(final_out)
    ]
    subprocess.run(cmd_final, capture_output=True, check=True)
    print(f"  [SUCCESS] {final_out.name} rendered ({final_out.stat().st_size:,} bytes)!")
    return final_out

def main():
    print("=" * 65)
    print("  HIGH-RETENTION MULTI-CUT SHORTS ENGINE: EPISODE 06")
    print("=" * 65)
    
    # Check if action videos exist
    any_video_missing = False
    all_short_videos = set(b["asset"] for b in SHORT_01_BEATS + SHORT_02_BEATS if b["type"] == "video")
    for v in all_short_videos:
        if not (VIDEOS_DIR / v).exists():
            any_video_missing = True
            break
            
    if any_video_missing:
        print("[*] Google Flow action videos are currently pending for companion shorts.")
        print("[*] Multi-beat cuts are fully configured with exact durations derived from sentence-level SRT cues:")
        print(f"    - Short 01 (The Sky Bridge That Shouldn't Exist): {len(SHORT_01_BEATS)} dynamic micro-cuts")
        print(f"    - Short 02 (The Temple That 1,000 Men Couldn't Destroy): {len(SHORT_02_BEATS)} dynamic micro-cuts")
        print("[*] Halting render until user places video clips in episode06/videos/ per Google Flow Video Gate.")
        return
        
    s1 = assemble_single_short(
        short_name="short_01",
        beats=SHORT_01_BEATS,
        audio_filename="short_01_the_sky_bridge_that_shouldnt_exist_mixed.mp3",
        srt_filename="short_01_the_sky_bridge_that_shouldnt_exist.srt",
        out_filename="short_01_the_sky_bridge_that_shouldnt_exist.mp4"
    )
    
    s2 = assemble_single_short(
        short_name="short_02",
        beats=SHORT_02_BEATS,
        audio_filename="short_02_the_temple_that_1000_men_couldnt_destroy_mixed.mp3",
        srt_filename="short_02_the_temple_that_1000_men_couldnt_destroy.srt",
        out_filename="short_02_the_temple_that_1000_men_couldnt_destroy.mp4"
    )
    
    # Clean up temp cuts if completed
    if s1 and s2:
        shutil.rmtree(TEMP_DIR, ignore_errors=True)
        print("\n[ALL COMPLETE] Companion Dynamic Shorts assembled successfully!")

if __name__ == "__main__":
    main()
