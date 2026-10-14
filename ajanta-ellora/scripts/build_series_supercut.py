#!/usr/bin/env python3
"""
The Curiosity Kills The Cat - Automated Series Supercut Engine
Compiles Episodes 01 through 07 into a unified, broadcast-grade feature documentary:
"The Complete Subterranean Megastructures of Kailasa & Ajanta (Remastered 1080p)"

Production Invariants Enforced:
1. Directory Normalization & Validation (ensures episode01..episode07 uniform layout)
2. Outro & Recap Trimming (eliminates repetitive "Subscribe / Previously on" friction)
3. 4-Second Cinematic Chapter Title Cards with Procedural 40Hz Sub-Bass Audio Booms
4. Master Cold Open & Feature Film Epilogue (Passes YouTube YPP "Reused Content" check)
5. Dynamic Cumulative SRT Timestamp Shifter & Merged Chapters Generator
6. Broadcast Audio Normalization (loudnorm=I=-14:TP=-1.5:LRA=11, 48kHz Stereo)
7. Phase 2 Automation: Updates Shorts Publish Kits across all episodes with Related Video hook
"""

import os
import sys
import re
import json
import math
import wave
import struct
import shutil
import argparse
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Workspace Root
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
AJANTA_ELLORA_DIR = WORKSPACE_ROOT / "ajanta-ellora"
OUTPUT_DIR = AJANTA_ELLORA_DIR / "supercut"

# Episode Master Configuration & Trims
EPISODE_CONFIG = [
    {
        "id": 1,
        "name": "episode01",
        "video_filename": "episode_01_master_preview.mp4",
        "part_roman": "PART I",
        "title": "THE IMPOSSIBLE MOUNTAIN",
        "subtitle": "Top-Down Monolithic Excavation & Zero Scaffolding",
        "trim_start": 0.0,
        "trim_end": 14.5,  # Trims "In Episode Two..." outro
    },
    {
        "id": 2,
        "name": "episode02",
        "video_filename": "episode_02_master_preview.mp4",
        "part_roman": "PART II",
        "title": "THE FIRE-QUENCHED BASALT",
        "subtitle": "Thermal Shock Quarrying & 400,000 Tons Excavated",
        "trim_start": 0.0,
        "trim_end": 9.0,   # Trims "In Episode Three..." outro
    },
    {
        "id": 3,
        "name": "episode03",
        "video_filename": "episode_03_master_preview.mp4",
        "part_roman": "PART III",
        "title": "THE FIRST CUT",
        "subtitle": "The Astronomical Spire & Zero-Tolerance Sacred Grid",
        "trim_start": 0.0,
        "trim_end": 9.0,   # Trims "Next week on Episode Four..." outro
    },
    {
        "id": 4,
        "name": "episode04",
        "video_filename": "episode_04_master_preview.mp4",
        "part_roman": "PART IV",
        "title": "THE CHASM OF KAILASA",
        "subtitle": "The Great Spatial Void & Courtyard Isolation",
        "trim_start": 0.0,
        "trim_end": 8.5,   # Trims "That is the next mystery..." outro
    },
    {
        "id": 5,
        "name": "episode05",
        "video_filename": "episode_05_master_preview.mp4",
        "part_roman": "PART V",
        "title": "THE ELEPHANT PLINTH",
        "subtitle": "Monolithic Basalt Compression & High-Relief Mastery",
        "trim_start": 0.0,
        "trim_end": 11.5,  # Trims "That is the next mystery..." outro
    },
    {
        "id": 6,
        "name": "episode06",
        "video_filename": "episode_06_master_preview.mp4",
        "part_roman": "PART VI",
        "title": "THE BRIDGE TO INFINITY",
        "subtitle": "Cantilevered Basalt Sky-Bridges & Sacred Plaster",
        "trim_start": 0.0,
        "trim_end": 0.0,   # Keeps the philosophical conclusion
    },
    {
        "id": 7,
        "name": "episode07",
        "video_filename": "episode_07_the_secret_canyon_of_waghur_master_1080p.mp4",
        "part_roman": "PART VII",
        "title": "THE SECRET CANYON OF WAGHUR",
        "subtitle": "Ajanta's 700-Year Acoustic & Hydraulic Laboratory",
        "trim_start": 0.0,
        "trim_end": 11.5,  # Trims "In our next episode..." outro
    },
]

# Helper: Probe Media Duration
def probe_duration(filepath: Path) -> float:
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(filepath)
    ]
    res = subprocess.check_output(cmd, text=True).strip()
    return float(res)

# Helper: Subtitle Parsing & Formatting
def parse_srt_time(t_str: str) -> float:
    t_str = t_str.strip().replace(',', '.')
    parts = t_str.split(':')
    return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])

def fmt_srt_time(sec: float) -> str:
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    ms = int(round((sec - int(sec)) * 1000))
    if ms >= 1000:
        s += 1
        ms -= 1000
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

def fmt_chapter_time(sec: float) -> str:
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

# Generator: Procedural 40Hz Sub-Bass Boom WAV
def generate_sub_bass_boom(out_path: Path, duration: float = 4.0, sample_rate: int = 48000):
    num_samples = int(sample_rate * duration)
    samples = []
    for i in range(num_samples):
        t = i / sample_rate
        freq = 45.0 - (17.0 * (t / duration))  # 45Hz -> 28Hz sweep
        if t < 0.02:
            amp = t / 0.02
        else:
            amp = math.exp(-1.4 * (t - 0.02))
        sig = math.sin(2.0 * math.pi * freq * t) * amp
        sig += 0.22 * math.sin(4.0 * math.pi * freq * t) * (amp ** 1.5)  # 2nd harmonic
        val = int(max(-32767, min(32767, sig * 28000)))
        samples.append(struct.pack('<hh', val, val))
    with wave.open(str(out_path), 'wb') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(samples))

# Generator: Theatrical Chapter Title Card Image
def generate_title_card_image(out_path: Path, part_tag: str, main_title: str, subtitle: str):
    w, h = 1920, 1080
    img = Image.new('RGB', (w, h), (10, 10, 12))  # Obsidian
    draw = ImageDraw.Draw(img)

    # Architectural Double Border
    draw.rectangle([(80, 60), (w - 80, h - 60)], outline=(80, 65, 30), width=1)
    draw.rectangle([(90, 70), (w - 90, h - 70)], outline=(140, 115, 50), width=2)

    # Windows Fonts
    try:
        font_tag = ImageFont.truetype('C:/Windows/Fonts/georgiab.ttf', 28)
        font_title = ImageFont.truetype('C:/Windows/Fonts/georgiab.ttf', 60)
        font_sub = ImageFont.truetype('C:/Windows/Fonts/georgia.ttf', 30)
    except Exception:
        font_tag = font_title = font_sub = ImageFont.load_default()

    draw.text((w/2, 420), " ".join(part_tag), font=font_tag, fill=(197, 160, 89), anchor='mm')
    draw.line([(w/2 - 70, 460), (w/2 + 70, 460)], fill=(197, 160, 89), width=2)
    draw.text((w/2, 530), main_title, font=font_title, fill=(247, 231, 206), anchor='mm')
    draw.text((w/2, 610), subtitle, font=font_sub, fill=(176, 168, 152), anchor='mm')

    img.save(str(out_path), quality=95)

# Build Video Title Card MP4 with Sub-Bass Boom
def render_chapter_card_video(img_path: Path, audio_path: Path, out_path: Path, duration: float = 4.0):
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-t", str(duration), "-i", str(img_path),
        "-i", str(audio_path),
        "-vf", f"fade=t=in:st=0:d=0.5,fade=t=out:st={duration-0.5}:d=0.5,format=yuv420p,fps=30",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
        "-shortest", str(out_path)
    ]
    subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Master Cold Open & Epilogue Generation
def generate_feature_framing(staging_dir: Path, audio_boom: Path):
    cold_open_img = staging_dir / "master_cold_open.jpg"
    cold_open_mp4 = staging_dir / "master_cold_open.mp4"
    generate_title_card_image(
        cold_open_img,
        "THE CURIOSITY KILLS THE CAT PRESENTS",
        "THE SUBTERRANEAN MEGASTRUCTURES",
        "A 7-Part Investigation into 700 Years of Monolithic Engineering"
    )
    render_chapter_card_video(cold_open_img, audio_boom, cold_open_mp4, duration=5.0)

    epilogue_img = staging_dir / "master_epilogue.jpg"
    epilogue_mp4 = staging_dir / "master_epilogue.mp4"
    generate_title_card_image(
        epilogue_img,
        "EPILOGUE",
        "THE UNFINISHED MONOLITH",
        "Across Seven Centuries, Ancient Builders Did Not Build—They Subtracted Mountains."
    )
    render_chapter_card_video(epilogue_img, audio_boom, epilogue_mp4, duration=5.0)

    return cold_open_mp4, epilogue_mp4

# Step 1: Directory Normalization Check
def verify_directory_structure():
    print("[1/6] Verifying directory structure & episode assets...")
    nested_path = AJANTA_ELLORA_DIR / "ajanta-ellora"
    if nested_path.exists():
        print(f"  [WARN] Found nested {nested_path}. Removing...")
        shutil.rmtree(nested_path, ignore_errors=True)
    
    for ep in EPISODE_CONFIG:
        ep_dir = AJANTA_ELLORA_DIR / ep["name"]
        if not ep_dir.exists():
            raise FileNotFoundError(f"Missing episode directory: {ep_dir}")
        master_video = ep_dir / "final_videos" / ep["video_filename"]
        if not master_video.exists():
            raise FileNotFoundError(f"Missing master video: {master_video}")
        srt_file = ep_dir / "subtitles" / f"episode_{ep['id']:02d}_full.srt"
        if not srt_file.exists():
            raise FileNotFoundError(f"Missing subtitle file: {srt_file}")
        ch_file = ep_dir / "openmontage_bundle" / "metadata" / "chapters.txt"
        if not ch_file.exists():
            raise FileNotFoundError(f"Missing chapters file: {ch_file}")
    print("  [OK] All 7 episode directories and assets verified uniformly.")

# Step 2: Build Chapters, Cold Open & Cards
def prepare_staging_assets(staging_dir: Path):
    print("[2/6] Generating procedural 40Hz sub-bass booms & chapter title cards...")
    staging_dir.mkdir(parents=True, exist_ok=True)
    boom_path = staging_dir / "sub_bass_boom.wav"
    generate_sub_bass_boom(boom_path, duration=4.0)

    card_videos = []
    for ep in EPISODE_CONFIG:
        card_img = staging_dir / f"card_{ep['name']}.jpg"
        card_mp4 = staging_dir / f"card_{ep['name']}.mp4"
        generate_title_card_image(card_img, ep["part_roman"], ep["title"], ep["subtitle"])
        render_chapter_card_video(card_img, boom_path, card_mp4, duration=4.0)
        card_videos.append(card_mp4)

    cold_open_mp4, epilogue_mp4 = generate_feature_framing(staging_dir, boom_path)
    print("  [OK] Chapter cards and master framing videos rendered.")
    return card_videos, cold_open_mp4, epilogue_mp4

# Step 3: Compute Cumulative SRT & Chapters
def generate_cumulative_srt_and_chapters(cold_open_dur: float, card_dur: float, epilogue_dur: float):
    print("[3/6] Computing cumulative SRT and merged chapters...")
    output_subtitles = OUTPUT_DIR / "subtitles"
    output_metadata = OUTPUT_DIR / "openmontage_bundle" / "metadata"
    output_subtitles.mkdir(parents=True, exist_ok=True)
    output_metadata.mkdir(parents=True, exist_ok=True)

    master_srt_path = output_subtitles / "supercut_master.srt"
    master_chapters_path = output_metadata / "chapters.txt"

    merged_cues = []
    merged_chapters = []
    current_time_sec = 0.0

    # Cold open chapter
    merged_chapters.append(f"{fmt_chapter_time(current_time_sec)} - Master Cold Open: The 700-Year Subterranean Arc")
    current_time_sec += cold_open_dur

    cue_counter = 1
    for ep_idx, ep in enumerate(EPISODE_CONFIG):
        ep_dir = AJANTA_ELLORA_DIR / ep["name"]
        master_video = ep_dir / "final_videos" / ep["video_filename"]
        raw_dur = probe_duration(master_video)
        effective_dur = raw_dur - ep["trim_start"] - ep["trim_end"]

        # Chapter Title Card
        merged_chapters.append(f"{fmt_chapter_time(current_time_sec)} - {ep['part_roman']}: {ep['title']}")
        current_time_sec += card_dur

        # Load & parse SRT
        srt_file = ep_dir / "subtitles" / f"episode_{ep['id']:02d}_full.srt"
        content = srt_file.read_text(encoding="utf-8")
        cues = re.findall(r'(\d+)\n(\d{2}:\d{2}:\d{2}[,\.]\d{3}) --> (\d{2}:\d{2}:\d{2}[,\.]\d{3})\n(.*?)(?=\n\d+\n|\Z)', content, re.DOTALL)

        t_start_cut = ep["trim_start"]
        t_end_cut = raw_dur - ep["trim_end"]

        for _, start_str, end_str, text in cues:
            s_sec = parse_srt_time(start_str)
            e_sec = parse_srt_time(end_str)
            if e_sec <= t_start_cut or s_sec >= t_end_cut:
                continue
            shifted_s = max(0.0, s_sec - t_start_cut) + current_time_sec
            shifted_e = min(effective_dur, e_sec - t_start_cut) + current_time_sec
            merged_cues.append(f"{cue_counter}\n{fmt_srt_time(shifted_s)} --> {fmt_srt_time(shifted_e)}\n{text.strip()}\n")
            cue_counter += 1

        # Load & parse episodic chapters
        ch_file = ep_dir / "openmontage_bundle" / "metadata" / "chapters.txt"
        for line in ch_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line: continue
            m = re.match(r'^([\d:]+)\s*[-:]\s*(.*)$', line)
            if m:
                parts = m.group(1).split(':')
                ch_sec = int(parts[0]) * 60 + float(parts[1]) if len(parts) == 2 else int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
                if ch_sec < t_start_cut or ch_sec >= t_end_cut:
                    continue
                # If chapter is right at start, avoid duplicating the main Chapter Title Card
                if ch_sec - t_start_cut > 10.0:
                    shifted_ch = (ch_sec - t_start_cut) + current_time_sec
                    merged_chapters.append(f"{fmt_chapter_time(shifted_ch)} - {ep['part_roman']}: {m.group(2).strip()}")

        current_time_sec += effective_dur

    # Epilogue chapter
    merged_chapters.append(f"{fmt_chapter_time(current_time_sec)} - Epilogue: The Unfinished Monolith")
    current_time_sec += epilogue_dur

    master_srt_path.write_text("\n".join(merged_cues), encoding="utf-8")
    master_chapters_path.write_text("\n".join(merged_chapters), encoding="utf-8")
    print(f"  [OK] Generated {len(merged_cues)} shifted SRT cues in: {master_srt_path.name}")
    print(f"  [OK] Generated {len(merged_chapters)} merged chapters in: {master_chapters_path.name}")
    print(f"  [OK] Projected Supercut Total Runtime: {fmt_chapter_time(current_time_sec)} ({current_time_sec/60:.2f} mins)")
    return master_srt_path, master_chapters_path

# Step 4: Stitch Master Supercut Video
def stitch_supercut_feature(staging_dir: Path, card_videos, cold_open_mp4, epilogue_mp4):
    print("[4/6] Normalizing segments & stitching master supercut...")
    final_videos_dir = OUTPUT_DIR / "final_videos"
    final_videos_dir.mkdir(parents=True, exist_ok=True)
    master_output = final_videos_dir / "the_complete_megastructures_of_kailasa_and_ajanta_master_1080p.mp4"

    # Normalize each segment (both episode cut and title cards) to uniform intermediate clips
    inter_dir = staging_dir / "intermediates"
    inter_dir.mkdir(exist_ok=True)

    concat_list = []
    
    # 0. Cold Open
    c_open_norm = inter_dir / "00_cold_open.ts"
    cmd = [
        "ffmpeg", "-y", "-i", str(cold_open_mp4),
        "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,format=yuv420p,fps=30",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
        "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "192k",
        "-bsf:v", "h264_mp4toannexb", "-f", "mpegts", str(c_open_norm)
    ]
    subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    concat_list.append(c_open_norm)

    # 1..7 Episodes & Cards
    for idx, ep in enumerate(EPISODE_CONFIG):
        # Card
        card_norm = inter_dir / f"{idx+1:02d}_card.ts"
        cmd = [
            "ffmpeg", "-y", "-i", str(card_videos[idx]),
            "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,format=yuv420p,fps=30",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
            "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "192k",
            "-bsf:v", "h264_mp4toannexb", "-f", "mpegts", str(card_norm)
        ]
        subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        concat_list.append(card_norm)

        # Episode Video with Trims
        ep_norm = inter_dir / f"{idx+1:02d}_ep.ts"
        raw_video = AJANTA_ELLORA_DIR / ep["name"] / "final_videos" / ep["video_filename"]
        raw_dur = probe_duration(raw_video)
        t_start = ep["trim_start"]
        t_duration = raw_dur - ep["trim_start"] - ep["trim_end"]

        cmd = [
            "ffmpeg", "-y",
            "-ss", str(t_start), "-t", str(t_duration), "-i", str(raw_video),
            "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,format=yuv420p,fps=30",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
            "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "192k",
            "-bsf:v", "h264_mp4toannexb", "-f", "mpegts", str(ep_norm)
        ]
        print(f"  Trimming & normalizing {ep['name']} (duration: {t_duration:.1f}s)...")
        subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        concat_list.append(ep_norm)

    # Epilogue
    epilogue_norm = inter_dir / "99_epilogue.ts"
    cmd = [
        "ffmpeg", "-y", "-i", str(epilogue_mp4),
        "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,format=yuv420p,fps=30",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
        "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "192k",
        "-bsf:v", "h264_mp4toannexb", "-f", "mpegts", str(epilogue_norm)
    ]
    subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    concat_list.append(epilogue_norm)

    # Concat file
    concat_txt = staging_dir / "concat_list.txt"
    with open(concat_txt, "w", encoding="utf-8") as f:
        for p in concat_list:
            f.write(f"file '{p.resolve().as_posix()}'\n")

    # Final pass with EBU R128 / loudnorm=I=-14:TP=-1.5:LRA=11
    print("  Applying final audio leveling (loudnorm=I=-14:TP=-1.5:LRA=11) and muxing...")
    final_cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(concat_txt),
        "-af", "loudnorm=I=-14:TP=-1.5:LRA=11",
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "256k", "-ar", "48000",
        "-movflags", "+faststart",
        str(master_output)
    ]
    subprocess.check_call(final_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"  [OK] Master Supercut successfully rendered to: {master_output}")
    return master_output

# Step 5: Generate Publish Kit & 3-Way A/B/C Thumbnails
def generate_publish_kit_and_thumbnails():
    print("[5/6] Generating 3-Way A/B/C Thumbnails & YouTube Publish Kit...")
    thumb_dir = OUTPUT_DIR / "thumbnail"
    pk_dir = OUTPUT_DIR / "publish_kit"
    thumb_dir.mkdir(parents=True, exist_ok=True)
    pk_dir.mkdir(parents=True, exist_ok=True)

    # 3-Way Thumbnails:
    # 1. Variant A (Scale Contrast)
    var_a = thumb_dir / "thumbnail_variant_a_scale_contrast.jpg"
    shutil.copy2(AJANTA_ELLORA_DIR / "episode04" / "thumbnail" / "ep04_master_thumbnail_16x9.jpg", var_a)

    # 2. Variant B (Impossible Blueprint)
    var_b = thumb_dir / "thumbnail_variant_b_impossible_blueprint.jpg"
    shutil.copy2(AJANTA_ELLORA_DIR / "episode02" / "images" / "ep02_infographic_01_three_trenches.jpg", var_b)

    # 3. Variant C (Curiosity Gap / Forbidden Chamber)
    var_c = thumb_dir / "thumbnail_variant_c_forbidden_chamber.jpg"
    shutil.copy2(AJANTA_ELLORA_DIR / "episode07" / "thumbnail" / "ep07_thumbnail_16x9_the_secret_canyon.jpg", var_c)

    # Master Publish Kit
    pk_content = """# Master YouTube Publish Kit: The Complete Megastructures of Kailasa & Ajanta
## 7-Part Master Engineering Documentary (Director's Cut Remastered)

**Master Video**: `the_complete_megastructures_of_kailasa_and_ajanta_master_1080p.mp4`  
**Runtime**: ~60 Minutes (Theatrical Feature)  
**Format**: 16:9 Full HD (1920x1080, 30 fps, EBU -14 LUFS)  
**Primary Distribution Target**: Living Room TVs / Connected TVs & High-Retention Search

---

## 1. High-CTR Living Room & Search Titles (A/B/C Test Options)

| # | Title Option | Angle / Target Audience |
| :--- | :--- | :--- |
| **A** | **The Impossible Subterranean Megastructures of Ancient India (Full Documentary)** *(Recommended)* | High-RPM Search & Living Room TV |
| **B** | **How Ancient Architects Carved a 400,000-Ton Mountain From The Top Down | Kailasa & Ajanta** | Technical Curiosity & Feat |
| **C** | **700 Years of Forbidden Underground Engineering: The Complete Kailasa Mystery** | Mystery & Historical Drama |
| **D** | **Ancient Megastructures: Kailasa & Ajanta (All 7 Episodes Remastered)** | Binge / Complete Collection |
| **E** | **They Subtracted an Entire Mountain: The Subterranean Wonders of India** | Philosophical Scale Contrast |

---

## 2. YouTube Master Description (Studio Paste Ready)

```markdown
Over 700 years before modern civil engineering, ancient Indian stonecutters achieved what modern geologists still struggle to explain: they excavated over 400,000 tons of solid volcanic basalt—not by building from the foundation up, but by carving directly downward from the mountain summit.

This complete, uninterrupted 7-part master documentary presents the full investigative arc of Kailasa Temple (Cave 16) and the mysterious crescent canyon of Ajanta. Remastered with theatrical broadcast audio and continuous chapter navigation, this feature reveals the thermal shock quarrying mechanics, zero-tolerance astronomy, subterranean hydraulic defense networks, and acoustic resonance chambers that turned living rock into an architectural miracle.

TIMESTAMPS / CHAPTERS:
See pinned comment and video player for all 25+ detailed architectural chapters.

🔔 Subscribe to @thecuriousity-kills-thecat for deep-dive historical engineering documentaries.

#KailasaTemple #AjantaCaves #AncientEngineering #FullDocumentary #AncientIndia #ElloraCaves #Megaliths #HistoryDocumentary
```

---

## 3. SEO Tags (<500 Characters Strictly Compliant)

```text
Kailasa Temple,Ajanta Caves,Full Documentary,Ancient Megastructures,Ellora Caves,How Kailasa Was Built,Ancient Engineering,Top Down Temple,Rock Cut Architecture,Ancient India,Archaeology Documentary,Ellora Cave 16,Architect Kokasa,Rashtrakuta Dynasty,Vakataka Dynasty,Ancient Technology,Megaliths,Indian History,Ancient Builders,Thermal Shock Quarrying,Geotechnical Engineering,Waghur River,Ancient Mysteries,Complete Series
```

*(Tag character count: 424 characters — strictly compliant with YouTube's 500-character ceiling).*

---

## 4. 3-Way A/B/C Thumbnail Test & Compare Strategy

1. **Variant A (`thumbnail_variant_a_scale_contrast.jpg`)**: Tiny surveyor figure standing in the colossal 100-foot Kailasa trench (Human Scale vs. Basalt Monolith).
2. **Variant B (`thumbnail_variant_b_impossible_blueprint.jpg`)**: Three-Trench structural blueprint elevation with cyan/amber dimension arrows and "NO FOUNDATION" hook.
3. **Variant C (`thumbnail_variant_c_forbidden_chamber.jpg`)**: Solitary torchlit beam cutting through the ancient volcanic canyon of Ajanta.
"""
    pk_file = pk_dir / "master_publish_kit.md"
    pk_file.write_text(pk_content, encoding="utf-8")
    print(f"  [OK] Publish kit and 3-Way thumbnails created in: {pk_dir}")

# Step 6: Phase 2 Automation: Update All Shorts Publish Kits
def update_shorts_publish_kits():
    print("[6/6] Updating Shorts Publish Kits across Episodes 01–07 with 'Related Video' Hook...")
    related_video_directive = """
> [!IMPORTANT]
> **NATIVE 'RELATED VIDEO' CLIFFHANGER HOOK**:
> In YouTube Studio mobile packaging:
> 1. Set **'Related video'** to: **The Impossible Subterranean Megastructures of Ancient India (Full Documentary)**
> 2. Ensure the final 3 seconds of the Short points viewers directly to the pill above the title.
"""
    count = 0
    for ep in range(1, 8):
        pk_dir = AJANTA_ELLORA_DIR / f"episode{ep:02d}" / "publish_kit"
        if not pk_dir.exists(): continue
        for md_file in pk_dir.glob("short*.md"):
            content = md_file.read_text(encoding="utf-8")
            if "NATIVE 'RELATED VIDEO' CLIFFHANGER HOOK" not in content:
                # Insert directive after header
                lines = content.splitlines()
                insert_idx = 8
                for idx, line in enumerate(lines):
                    if line.startswith("## 1."):
                        insert_idx = idx
                        break
                new_content = "\n".join(lines[:insert_idx]) + "\n" + related_video_directive + "\n" + "\n".join(lines[insert_idx:])
                md_file.write_text(new_content, encoding="utf-8")
                count += 1
    print(f"  [OK] Updated {count} Shorts publish kits with native 'Related Video' directives.")

def main():
    parser = argparse.ArgumentParser(description="Automated Series Supercut Production Engine")
    parser.add_argument("--dry-run", action="store_true", help="Generate metadata, title cards and staging assets without full video stitch")
    args = parser.parse_args()

    print("===================================================================")
    print("  THE CURIOSITY KILLS THE CAT: MASTER SERIES SUPERCUT ENGINE")
    print("===================================================================")

    verify_directory_structure()
    staging_dir = OUTPUT_DIR / "staging"
    card_videos, cold_open_mp4, epilogue_mp4 = prepare_staging_assets(staging_dir)

    cold_open_dur = probe_duration(cold_open_mp4)
    card_dur = probe_duration(card_videos[0])
    epilogue_dur = probe_duration(epilogue_mp4)

    generate_cumulative_srt_and_chapters(cold_open_dur, card_dur, epilogue_dur)
    generate_publish_kit_and_thumbnails()
    update_shorts_publish_kits()

    if args.dry_run:
        print("\n[DRY RUN COMPLETE] Metadata, cards, subtitles, and publish kits are ready.")
        print(f"To render the master 1080p supercut, run without --dry-run.")
    else:
        stitch_supercut_feature(staging_dir, card_videos, cold_open_mp4, epilogue_mp4)
        print("\n===================================================================")
        print("  MASTER SUPERCUT PRODUCTION & PUBLISHING PACKAGE COMPLETE!")
        print("===================================================================")

if __name__ == "__main__":
    main()
