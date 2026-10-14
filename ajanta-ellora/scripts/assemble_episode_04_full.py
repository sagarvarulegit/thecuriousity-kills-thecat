"""
Full 72-Micro-Beat Master Assembly Engine for Kailasa Episode 04 via FFmpeg.
Applies the 4K Anti-Jitter Sub-Pixel Motorized Zoompan Technique (scale=3840:2160 -> zoompan -> scale=1920:1080)
for still images with documentary vignette and color grading, and splices in normalized action clips
at 30fps broadcast-grade encoding with monotonic timestamps derived from sentence-level SRT cues.

Produces:
1. episode04/final_videos/episode_04_master_preview.mp4 (16:9 1080p Master)
2. episode04/final_videos/short_01_the_bridge_in_midair.mp4 (9:16 Vertical 1080x1920)
3. episode04/final_videos/short_02_the_bridge_that_fell.mp4 (9:16 Vertical 1080x1920)
4. episode04/openmontage_bundle/ (Canonical OpenMontage distribution package)
"""

import os
import re
import sys
import json
import shutil
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent # ajanta-ellora
EPISODE_DIR = BASE_DIR / "episode04"
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

sys.path.insert(0, str(BASE_DIR / "scripts"))
from generate_episode04_assets import UNIQUE_BEATS_DATA

# 72-Beat Master Manifest derived from UNIQUE_BEATS_DATA
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

    # 2. Timing Lock
    # Prefer mixed master audio if generated, else fallback to full narration
    master_audio = AUDIO_DIR / "episode_04_master_audio_mixed.mp3"
    if not master_audio.exists():
        master_audio = AUDIO_DIR / "episode_04_full_narration.mp3"
        
    total_audio_dur = get_media_duration(master_audio)
    cues = parse_srt_cues(SUB_DIR / "episode_04_full.srt")
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

    # 3. Concat Video Track
    concat_txt = OUTPUT_DIR / "temp_ep04_concat.txt"
    with open(concat_txt, "w", encoding="utf-8") as f:
        for p in sub_files:
            f.write(f"file '{p.as_posix()}'\n")

    master_v_only = OUTPUT_DIR / "temp_ep04_v_only.mp4"
    print("\n[*] Concatenating master video track...")
    cmd_concat = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_txt),
        "-c", "copy",
        str(master_v_only)
    ]
    subprocess.run(cmd_concat, capture_output=True, check=True)

    # 4. Mux Audio Track
    master_out = OUTPUT_DIR / "episode_04_master_preview.mp4"
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

    shorts = [
        {
            "name": "short_01_the_bridge_in_midair",
            "img": "ep04_01_courtyard_ground_upward_PAN_ZOOM.jpg",
            "audio": "short_01_the_bridge_in_midair.mp3",
            "out": "short_01_the_bridge_in_midair.mp4"
        },
        {
            "name": "short_02_the_bridge_that_fell",
            "img": "ep04_06_southern_cliff_broken_scar_PAN_ZOOM.jpg",
            "audio": "short_02_the_bridge_that_fell.mp3",
            "out": "short_02_the_bridge_that_fell.mp4"
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

def package_openmontage_bundle():
    print("\n" + "=" * 65)
    print("  PACKAGING CANONICAL OPENMONTAGE DISTRIBUTION BUNDLE")
    print("=" * 65)

    meta_dir = BUNDLE_DIR / "metadata"
    thumb_dir = BUNDLE_DIR / "thumbnails"
    video_dir = BUNDLE_DIR / "video"

    meta_dir.mkdir(parents=True, exist_ok=True)
    thumb_dir.mkdir(parents=True, exist_ok=True)
    video_dir.mkdir(parents=True, exist_ok=True)

    # 1. Copy Master Thumbnail
    thumb_src = THUMBNAIL_DIR / "ep04_master_thumbnail_16x9.jpg"
    if not thumb_src.exists():
        thumb_src = THUMBNAIL_DIR / "ep04_master_thumbnail_raw.jpg"
    if thumb_src.exists():
        shutil.copy2(thumb_src, thumb_dir / "thumbnail.jpg")
        print(f"[*] Packaged thumbnail: {thumb_dir / 'thumbnail.jpg'}")

    # 2. Copy Video & Subtitles
    master_vid = OUTPUT_DIR / "episode_04_master_preview.mp4"
    if master_vid.exists():
        shutil.copy2(master_vid, video_dir / "output.mp4")
        print(f"[*] Packaged video: {video_dir / 'output.mp4'}")
        
    master_srt = SUB_DIR / "episode_04_full.srt"
    if master_srt.exists():
        shutil.copy2(master_srt, video_dir / "subtitles.srt")
        print(f"[*] Packaged subtitles: {video_dir / 'subtitles.srt'}")

    # 3. Build OpenMontage Metadata Files
    pub_kit_path = PUBLISH_DIR / "master_publish_kit.md"
    if pub_kit_path.exists():
        content = pub_kit_path.read_text(encoding="utf-8")
        shutil.copy2(pub_kit_path, meta_dir / "youtube_publish_kit.md")

        # Extract Chapters
        chap_match = re.search(r"(\d{2}:\d{2}\s*-\s*[^\n]+(?:\n\d{2}:\d{2}\s*-\s*[^\n]+)+)", content)
        if chap_match:
            (meta_dir / "chapters.txt").write_text(chap_match.group(1).strip() + "\n", encoding="utf-8")
            print(f"[*] Packaged chapters.txt")

        # Extract Tags
        tags_match = re.search(r"## SEO tags[^\n]*\n```(?:text)?\n(.*?)\n```", content, re.DOTALL)
        if tags_match:
            (meta_dir / "tags.txt").write_text(tags_match.group(1).strip() + "\n", encoding="utf-8")
            print(f"[*] Packaged tags.txt")

        # Extract Description
        desc_match = re.search(r"## Description\n(.*?)(?=\n##|\Z)", content, re.DOTALL)
        if desc_match:
            (meta_dir / "description.txt").write_text(desc_match.group(1).strip() + "\n", encoding="utf-8")
            print(f"[*] Packaged description.txt")

    meta_json = {
        "title": "The Floating Bridges of Kailasa",
        "episode": 4,
        "series": "Kailasa: The Mountain Carved From Above",
        "dimensions": {"width": 1920, "height": 1080},
        "fps": 30,
        "format": "16:9",
        "audio": "EBU R128 (-16 LUFS)",
        "cuts_count": len(MANIFEST),
        "zero_repetition_verified": True
    }
    (meta_dir / "metadata.json").write_text(json.dumps(meta_json, indent=2), encoding="utf-8")
    print(f"[*] Packaged metadata.json")
    print("\n[SUCCESS] Canonical OpenMontage bundle ready in:", BUNDLE_DIR)

def main():
    print("=" * 65)
    print(" FULL EPISODE 04 MASTER BROADCAST PRODUCTION SUITE")
    print("=" * 65)
    assemble_master_preview()
    assemble_shorts()
    package_openmontage_bundle()
    print("\n[COMPLETE] Episode 04 Master, Shorts, and OpenMontage Bundle Assembled.")

if __name__ == "__main__":
    main()
