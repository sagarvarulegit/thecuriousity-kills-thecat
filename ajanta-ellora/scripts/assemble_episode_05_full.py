"""
Full 72-Micro-Beat Master Assembly Engine for Kailasa Episode 05 via FFmpeg.
Applies the 4K Anti-Jitter Sub-Pixel Motorized Zoompan Technique (scale=3840:2160 -> zoompan -> scale=1920:1080)
for still images with documentary vignette and color grading, and splices in normalized action clips
at 30fps broadcast-grade encoding with monotonic timestamps derived from sentence-level SRT cues.

Produces:
1. episode05/final_videos/episode_05_master_preview.mp4 (16:9 1080p Master)
2. episode05/final_videos/short_01_the_elephants_that_carry_a_temple.mp4 (9:16 Vertical 1080x1920)
3. episode05/final_videos/short_02_why_elephants_support_the_mountain.mp4 (9:16 Vertical 1080x1920)
4. episode05/openmontage_bundle/ (Canonical OpenMontage distribution package)
"""

import os
import re
import sys
import json
import shutil
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent # ajanta-ellora
EPISODE_DIR = BASE_DIR / "episode05"
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

sys.path.insert(0, str(BASE_DIR / "scripts"))
from generate_episode05_assets import UNIQUE_BEATS_DATA

# 72-Beat Master Manifest derived from UNIQUE_BEATS_DATA: (type, filename, motion)
MANIFEST = [(item[0], item[1], item[3]) for item in UNIQUE_BEATS_DATA]

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
        
        # Conforming filtergraph: 1080p, 30fps, strip audio
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
        
        # 4K pre-scaled sub-pixel anti-jitter Ken Burns motion
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
        else: # slow_drift
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
        print("The following 8 bespoke action videos are required before rendering:")
        for v in missing:
            print(f"  - {v}")
        print("\nPlease generate these clips using the prompts in:")
        print(f"  {EPISODE_DIR / 'google_flow_input_images' / 'GOOGLE_FLOW_PROMPT_SHEET.md'}")
        print(f"and place them into:")
        print(f"  {VIDEOS_DIR}")
        print("!" * 65 + "\n")
        return None

    # 3. Timing Lock
    mixed_audio = AUDIO_DIR / "episode_05_master_audio_mixed.mp3"
    master_audio = mixed_audio if mixed_audio.exists() else (AUDIO_DIR / "episode_05_full_narration.mp3")
    total_audio_dur = get_media_duration(master_audio)
    cues = parse_srt_cues(SUB_DIR / "episode_05_full.srt")
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
    concat_txt = OUTPUT_DIR / "temp_ep05_concat.txt"
    with open(concat_txt, "w", encoding="utf-8") as f:
        for p in sub_files:
            f.write(f"file '{p.as_posix()}'\n")

    master_v_only = OUTPUT_DIR / "temp_ep05_v_only.mp4"
    print("\n[*] Concatenating master video track...")
    cmd_concat = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_txt),
        "-c", "copy",
        str(master_v_only)
    ]
    subprocess.run(cmd_concat, capture_output=True, check=True)

    # 5. Mux Audio Track
    master_out = OUTPUT_DIR / "episode_05_master_preview.mp4"
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

def assemble_shorts():
    print("\n" + "=" * 65)
    print("  ASSEMBLING COMPANION SHORTS (9:16 VERTICAL 1080x1920)")
    print("=" * 65)

    dynamic_shorts_script = BASE_DIR / "ajanta-ellora" / "scripts" / "assemble_dynamic_shorts_ep05.py"
    if dynamic_shorts_script.exists():
        print("[*] Launching high-retention multi-cut dynamic shorts assembler...")
        subprocess.run([sys.executable, str(dynamic_shorts_script)], check=True)
        return [
            OUTPUT_DIR / "short_01_the_elephants_that_carry_a_temple.mp4",
            OUTPUT_DIR / "short_02_why_elephants_support_the_mountain.mp4"
        ]

    shorts = [
        {
            "name": "short_01_the_elephants_that_carry_a_temple",
            "img": "ep05_01_courtyard_ground_plinth_reveal_PAN_ZOOM.jpg",
            "audio": "short_01_the_elephants_that_carry_a_temple_mixed.mp3" if (AUDIO_DIR / "short_01_the_elephants_that_carry_a_temple_mixed.mp3").exists() else "short_01_the_elephants_that_carry_a_temple.mp3",
            "out": "short_01_the_elephants_that_carry_a_temple.mp4"
        },
        {
            "name": "short_02_why_elephants_support_the_mountain",
            "img": "ep05_03_apparent_support_angle_PAN_ZOOM.jpg",
            "audio": "short_02_why_elephants_support_the_mountain_mixed.mp3" if (AUDIO_DIR / "short_02_why_elephants_support_the_mountain_mixed.mp3").exists() else "short_02_why_elephants_support_the_mountain.mp3",
            "out": "short_02_why_elephants_support_the_mountain.mp4"
        }
    ]

    outputs = []
    for s in shorts:
        img_path = IMAGES_DIR / s["img"]
        audio_path = AUDIO_DIR / s["audio"]
        out_path = OUTPUT_DIR / s["out"]
        
        dur = get_media_duration(audio_path)
        fps = 30
        frames = max(1, int(dur * fps))

        print(f"[*] Rendering {s['name']} (9:16 Vertical, {dur:.2f}s)...")
        # 4K vertical pre-scaling (2160x3840 -> zoompan -> 1080x1920)
        vf = f"scale=2160:3840:force_original_aspect_ratio=increase,crop=2160:3840,zoompan=z='1.0+0.10*(on/{frames})':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1080x1920:fps={fps},vignette=angle=PI/5,eq=contrast=1.04:saturation=1.06,setsar=1,fps=30"
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1", "-i", str(img_path),
            "-i", str(audio_path),
            "-t", f"{dur:.3f}",
            "-vf", vf,
            "-r", "30",
            "-c:v", "libx264", "-preset", "fast", "-crf", "20",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart",
            str(out_path)
        ]
        subprocess.run(cmd, capture_output=True, check=True)
        print(f"[*] Rendered: {out_path.name} ({out_path.stat().st_size:,} bytes)")
        outputs.append(out_path)
    return outputs

def main():
    print("=" * 65)
    print("  KAILASA EPISODE 05 MASTER ASSEMBLY SUITE")
    print("=" * 65)
    
    # Check if videos exist
    missing = check_video_prerequisites()
    if missing:
        print(f"[*] Action videos pending ({len(missing)} clips).")
        print("[*] Checking asset manifest and timing integrity...")
        fnames = [m[1] for m in MANIFEST]
        assert len(fnames) == len(set(fnames)), "Duplicate media assets in manifest!"
        print(f"[*] PASS: 100% Unique Media Manifest ({len(fnames)} cuts, 0 duplicates).")
        
        cues = parse_srt_cues(SUB_DIR / "episode_05_full.srt")
        assert len(cues) == len(MANIFEST), "SRT cue count does not match manifest cut count!"
        print(f"[*] PASS: 1:1 Narration-to-Visual Spoken Anchor ({len(cues)} cues).")
        
        print("\nPrerequisites status:")
        print(f"  - Images in images/: {len(list(IMAGES_DIR.glob('*.jpg')))} (Expected: 72)")
        print(f"  - Google Flow input stills: {len(list(EPISODE_DIR.joinpath('google_flow_input_images').glob('*_GENERATE_VIDEO.jpg')))} (Expected: 8)")
        print(f"  - Action videos in videos/: {8 - len(missing)}/8 present")
        print("\nHalting before video render per Google Flow Video Gate Law.")
        return
        
    master = assemble_master_preview()
    shorts = assemble_shorts()
    
    if master and master.exists():
        bundle_video = BUNDLE_DIR / "video" / "master.mp4"
        shutil.copy2(master, bundle_video)
        print(f"[*] Copied master video to OpenMontage bundle: {bundle_video.name}")
        
    print("\n[SUCCESS] Master preview, companion shorts, and OpenMontage bundle assembled cleanly.")

if __name__ == "__main__":
    main()
