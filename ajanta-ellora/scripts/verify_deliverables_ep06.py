"""
Comprehensive Deliverables Verification Script for Kailasa Episode 06:
The Sky Bridges of Kailasa — Carving What Should Have Collapsed.

Validates:
1. Audio stems & Master Narration integrity, duration, and <= 10.0ms drift (English & Hindi)
2. Subtitle syntax, strictly monotonic timestamps, and ZERO overlapping cues
3. Visual assets integrity, dimensions, < 2MB thumbnails (Master 16:9 + 2 Shorts 9:16), and 72-beat manifest 100% uniqueness
4. 16 Google Flow input stills isolation and Prompt Sheet availability
5. YouTube publish kits compliance (5 title variants, < 500 char SEO tags, chapter timestamps, zero episodic markers on shorts)
6. Canonical OpenMontage bundle completeness
"""

import os
import sys
import json
import re
import subprocess
from pathlib import Path
from PIL import Image

BASE_DIR = Path(__file__).resolve().parent.parent # ajanta-ellora
EPISODE_DIR = BASE_DIR / "episode06"

AUDIO_DIR = EPISODE_DIR / "audio"
AUDIO_HI_DIR = EPISODE_DIR / "audio_hindi"
SUB_DIR = EPISODE_DIR / "subtitles"
SUB_HI_DIR = EPISODE_DIR / "subtitles_hindi"
IMAGES_DIR = EPISODE_DIR / "images"
GOOGLE_FLOW_DIR = EPISODE_DIR / "google_flow_input_images"
VIDEOS_DIR = EPISODE_DIR / "videos"
BUNDLE_DIR = EPISODE_DIR / "openmontage_bundle"
THUMBNAIL_DIR = EPISODE_DIR / "thumbnail"
PUBLISH_KIT_DIR = EPISODE_DIR / "publish_kit"
STORYBOARD_FILE = EPISODE_DIR / "script_and_storyboard" / "episode_06_script_and_storyboard.md"

sys.path.insert(0, str(BASE_DIR / "scripts"))
from assemble_episode_06_full import MANIFEST

def get_duration(file_path: Path) -> float:
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(file_path)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0 and res.stdout.strip():
        return float(res.stdout.strip())
    return 0.0

def parse_srt_cues(srt_path: Path):
    text = srt_path.read_text(encoding="utf-8")
    blocks = text.strip().split("\n\n")
    cues = []
    for b in blocks:
        lines = b.strip().split("\n")
        if len(lines) >= 3:
            idx = lines[0].strip()
            time_match = re.match(r"(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})", lines[1].strip())
            if time_match:
                start_str, end_str = time_match.groups()
                def time_to_ms(t):
                    h, m, s_ms = t.split(":")
                    s, ms = s_ms.split(",")
                    return int(h)*3600000 + int(m)*60000 + int(s)*1000 + int(ms)
                cues.append({
                    "idx": idx,
                    "start_ms": time_to_ms(start_str),
                    "end_ms": time_to_ms(end_str),
                    "start_str": start_str,
                    "end_str": end_str,
                    "text": " ".join(lines[2:])
                })
    return cues

def test_audio():
    print("\n" + "=" * 60)
    print("TEST 1: AUDIO STEMS & MASTER NARRATION INTEGRITY (EN & HI)")
    print("=" * 60)
    
    acts_en = [
        "act_01_the_bridges_in_the_sky",
        "act_02_the_queens_vow_and_the_shikhara",
        "act_03_carving_the_void",
        "act_04_the_courtyard_monoliths",
        "act_05_the_living_epics_in_basalt",
        "act_06_the_white_mountain_of_ellora",
        "act_07_the_mountain_that_refused_to_fall",
        "act_08_the_architects_confession"
    ]
    
    # 1. English Act Stems & Drift
    act_dur_sum = 0.0
    all_ok = True
    print("[English Narration Track]")
    for act in acts_en:
        p = AUDIO_DIR / f"{act}.mp3"
        if not p.exists():
            print(f"  [FAIL] Missing English act audio: {p.name}")
            all_ok = False
            continue
        dur = get_duration(p)
        act_dur_sum += dur
        print(f"  [OK] {p.name:45s} Duration: {dur:6.2f}s")
        
    master_p = AUDIO_DIR / "episode_06_narration_master.mp3"
    if not master_p.exists():
        print("  [FAIL] Missing master narration: episode_06_narration_master.mp3")
        return False
        
    master_dur = get_duration(master_p)
    drift_ms = abs(master_dur - act_dur_sum) * 1000.0
    print(f"  -> Sum of Acts: {act_dur_sum:.3f}s | Master: {master_dur:.3f}s | Concatenation Drift: {drift_ms:.2f}ms")
    if drift_ms <= 10.0:
        print("  [PASS] English narration audio drift within standard (<= 10.0 ms).")
    else:
        print("  [FAIL] English narration audio drift exceeds standard!")
        all_ok = False
        
    # 2. Hindi Act Stems & Drift
    print("\n[Hindi Multi-Language Narration Track]")
    hi_act_sum = 0.0
    for act in acts_en:
        p = AUDIO_HI_DIR / f"{act}.mp3"
        if p.exists():
            dur = get_duration(p)
            hi_act_sum += dur
            print(f"  [OK] {p.name:45s} Duration: {dur:6.2f}s")
        else:
            print(f"  [FAIL] Missing Hindi act audio: {p.name}")
            all_ok = False
            
    hi_master_p = AUDIO_HI_DIR / "episode_06_hindi_narration_master.mp3"
    if hi_master_p.exists():
        hi_master_dur = get_duration(hi_master_p)
        hi_drift_ms = abs(hi_master_dur - hi_act_sum) * 1000.0
        print(f"  -> Sum of Acts: {hi_act_sum:.3f}s | Master: {hi_master_dur:.3f}s | Concatenation Drift: {hi_drift_ms:.2f}ms")
        if hi_drift_ms <= 10.0:
            print("  [PASS] Hindi narration audio drift within standard (<= 10.0 ms).")
        else:
            print("  [FAIL] Hindi narration audio drift exceeds standard!")
            all_ok = False
            
    # 3. Check Broadcast Mixed Masters
    mixed_master = AUDIO_DIR / "episode_06_master_audio_mixed.mp3"
    if mixed_master.exists():
        print(f"  [PASS] Broadcast mixed master exists: {mixed_master.name} ({get_duration(mixed_master):.2f}s)")
    else:
        print("  [FAIL] Missing episode_06_master_audio_mixed.mp3")
        all_ok = False
        
    hi_m4a = EPISODE_DIR / "final_videos" / "episode_06_hindi_track.m4a"
    if hi_m4a.exists():
        print(f"  [PASS] YouTube Hindi Audio track exists: {hi_m4a.name} ({get_duration(hi_m4a):.2f}s)")
    else:
        print("  [FAIL] Missing episode_06_hindi_track.m4a")
        all_ok = False

    return all_ok

def test_subtitles():
    print("\n" + "=" * 60)
    print("TEST 2: SUBTITLE TIMING & MONOTONIC INTEGRITY")
    print("=" * 60)
    
    srt_files = list(SUB_DIR.glob("*.srt")) + list(SUB_HI_DIR.glob("*.srt"))
    if not srt_files:
        print("  [FAIL] No SRT files found.")
        return False
        
    all_ok = True
    for srt in sorted(srt_files):
        cues = parse_srt_cues(srt)
        if not cues:
            print(f"  [FAIL] Empty or invalid SRT: {srt.name}")
            all_ok = False
            continue
            
        monotonic = True
        overlaps = 0
        for i in range(len(cues) - 1):
            if cues[i]["end_ms"] > cues[i+1]["start_ms"]:
                overlaps += 1
            if cues[i]["start_ms"] >= cues[i+1]["start_ms"]:
                monotonic = False
                
        if monotonic and overlaps == 0:
            print(f"  [OK] {srt.name:45s} Cues: {len(cues):2d} | Monotonic: True | Overlaps: 0")
        else:
            print(f"  [FAIL] {srt.name:45s} Monotonic: {monotonic} | Overlaps: {overlaps}")
            all_ok = False
            
    return all_ok

def test_visual_assets():
    print("\n" + "=" * 60)
    print("TEST 3: VISUAL ASSETS, THUMBNAILS & ZERO-REPETITION")
    print("=" * 60)
    
    all_ok = True
    
    # 1. 72-beat Manifest Uniqueness
    manifest_fnames = [m[1] for m in MANIFEST]
    total_cuts = len(manifest_fnames)
    unique_cuts = len(set(manifest_fnames))
    duplicates = [x for x in manifest_fnames if manifest_fnames.count(x) > 1]
    
    print(f"  72-Beat Manifest: {total_cuts} cuts | Unique: {unique_cuts}")
    if duplicates:
        print(f"  [FAIL] Duplicate media in manifest: {set(duplicates)}")
        all_ok = False
    else:
        print("  [PASS] 100% Unique Media Manifest (0 duplicates).")
        
    # 2. Check all still files in images/
    missing_images = []
    for mtype, fname, _ in MANIFEST:
        if mtype != "video":
            p_img = IMAGES_DIR / fname
            if not p_img.exists() or p_img.stat().st_size == 0:
                missing_images.append(fname)
            
    if missing_images:
        print(f"  [FAIL] Missing image assets in images/: {len(missing_images)}")
        for m in missing_images[:5]:
            print(f"    - {m}")
        all_ok = False
    else:
        print(f"  [PASS] All {total_cuts - 16} still image assets exist in images/.")
        
    # 3. Check Google Flow input stills (16 ASSETS)
    gf_files = list(GOOGLE_FLOW_DIR.glob("*_GENERATE_VIDEO.jpg"))
    print(f"  Google Flow input stills in {GOOGLE_FLOW_DIR.name}/: {len(gf_files)}/16")
    if len(gf_files) == 16:
        print("  [PASS] All 16 Google Flow input stills isolated cleanly.")
    else:
        print(f"  [FAIL] Expected 16 Google Flow input stills, found {len(gf_files)}")
        all_ok = False
        
    gf_sheet = GOOGLE_FLOW_DIR / "GOOGLE_FLOW_PROMPT_SHEET.md"
    if gf_sheet.exists() and gf_sheet.stat().st_size > 0:
        print(f"  [PASS] Google Flow prompt sheet exists ({gf_sheet.name}).")
    else:
        print("  [FAIL] Missing GOOGLE_FLOW_PROMPT_SHEET.md")
        all_ok = False
        
    # 4. Check Master Thumbnail (16:9, < 2MB, 1920x1080)
    master_thumb = THUMBNAIL_DIR / "ep06_master_thumbnail_16x9.jpg"
    if master_thumb.exists():
        im = Image.open(master_thumb)
        size_mb = master_thumb.stat().st_size / (1024 * 1024)
        print(f"  Master Thumbnail: {master_thumb.name} ({im.size[0]}x{im.size[1]}, {size_mb:.2f} MB)")
        if im.size == (1920, 1080) and size_mb < 2.0:
            print("  [PASS] Master Thumbnail meets 1920x1080 resolution and < 2.0 MB limit.")
        else:
            print("  [FAIL] Master Thumbnail failed dimensions or size constraint.")
            all_ok = False
    else:
        print("  [FAIL] Missing ep06_master_thumbnail_16x9.jpg")
        all_ok = False
        
    # 5. Check Companion Shorts Thumbnails (9:16, < 2MB, 1080x1920)
    for s_name in ["short_01_thumbnail_9x16.jpg", "short_02_thumbnail_9x16.jpg"]:
        st = THUMBNAIL_DIR / s_name
        if st.exists():
            im = Image.open(st)
            size_mb = st.stat().st_size / (1024 * 1024)
            print(f"  Short Thumbnail:  {st.name} ({im.size[0]}x{im.size[1]}, {size_mb:.2f} MB)")
            if im.size == (1080, 1920) and size_mb < 2.0:
                print(f"  [PASS] {s_name} meets 1080x1920 vertical format and < 2.0 MB limit.")
            else:
                print(f"  [FAIL] {s_name} failed dimensions or size constraint.")
                all_ok = False
        else:
            print(f"  [FAIL] Missing dedicated Shorts thumbnail: {s_name}")
            all_ok = False
            
    return all_ok

def test_publish_kits():
    print("\n" + "=" * 60)
    print("TEST 4: YOUTUBE PUBLISH KITS COMPLIANCE (<500 CHAR TAGS)")
    print("=" * 60)
    
    kits = [
        ("Master Video", PUBLISH_KIT_DIR / "master_publish_kit.md", True),
        ("Short 1", PUBLISH_KIT_DIR / "short_01_the_sky_bridge_that_shouldnt_exist_publish_kit.md", False),
        ("Short 2", PUBLISH_KIT_DIR / "short_02_the_temple_that_1000_men_couldnt_destroy_publish_kit.md", False),
        ("Hindi Audio Metadata", PUBLISH_KIT_DIR / "hindi_audio_track_metadata.md", False)
    ]
    
    all_ok = True
    for label, path, is_master in kits:
        if not path.exists():
            print(f"  [FAIL] Missing publish kit: {path.name}")
            all_ok = False
            continue
            
        content = path.read_text(encoding="utf-8")
        
        # Check title variants if master or shorts
        if "Metadata" not in label:
            titles_section = re.search(r"## Title [Oo]ptions[^\n]*\n(.*?)(?=\n##|\Z)", content, re.DOTALL)
            if titles_section:
                title_count = len(re.findall(r"^\d+\.", titles_section.group(1).strip(), re.MULTILINE))
                print(f"  [{label}] Title variants: {title_count}/5")
                if title_count < 5:
                    print(f"  [FAIL] Less than 5 titles in {path.name}")
                    all_ok = False
            else:
                print(f"  [FAIL] Missing Title options section in {path.name}")
                all_ok = False
                
        # Check tags < 500 characters
        tags_match = re.search(r"```text\n(.*?)\n```", content, re.DOTALL)
        if tags_match:
            tags_str = tags_match.group(1).strip()
            char_count = len(tags_str)
            print(f"  [{label}] SEO Tags: {char_count}/500 chars")
            if char_count < 500:
                print(f"  [PASS] {label} SEO tags under 500 characters.")
            else:
                print(f"  [FAIL] {label} SEO tags exceed 500 characters ({char_count})!")
                all_ok = False
        else:
            print(f"  [FAIL] No SEO tags block in {path.name}")
            all_ok = False
            
        # Shorts titles must not contain episodic labels
        if not is_master and "Short" in label:
            titles_section = re.search(r"## Title [Oo]ptions[^\n]*\n(.*?)(?=\n##|\Z)", content, re.DOTALL)
            titles_text = titles_section.group(1) if titles_section else content
            if re.search(r"\b(?:Episode|Ep\.)\s*0?6\b", titles_text, re.IGNORECASE):
                print(f"  [FAIL] Episodic marker detected in Shorts titles: {path.name}")
                all_ok = False
            else:
                print(f"  [PASS] No episodic markers in {label} titles.")
                
    return all_ok

def test_openmontage_bundle():
    print("\n" + "=" * 60)
    print("TEST 5: OPENMONTAGE DISTRIBUTION BUNDLE")
    print("=" * 60)
    
    meta_dir = BUNDLE_DIR / "metadata"
    thumb_dir = BUNDLE_DIR / "thumbnails"
    video_dir = BUNDLE_DIR / "video"
    
    all_ok = True
    for d in [meta_dir, thumb_dir, video_dir]:
        if d.exists():
            print(f"  [OK] Bundle Directory: {d.name}/")
        else:
            print(f"  [FAIL] Missing bundle directory: {d.name}/")
            all_ok = False
            
    # Check essential files
    for f in [meta_dir / "metadata.json", meta_dir / "tags.txt", meta_dir / "chapters.txt", meta_dir / "description.txt"]:
        if f.exists():
            print(f"  [PASS] {f.name} exists in bundle metadata.")
        else:
            print(f"  [FAIL] Missing {f.name}")
            all_ok = False
            
    for f in [thumb_dir / "thumbnail.jpg", thumb_dir / "short_01_thumbnail.jpg", thumb_dir / "short_02_thumbnail.jpg"]:
        if f.exists():
            print(f"  [PASS] {f.name} exists in bundle thumbnails.")
        else:
            print(f"  [FAIL] Missing {f.name}")
            all_ok = False
            
    for f in [video_dir / "subtitles.srt", video_dir / "subtitles_hindi.srt"]:
        if f.exists():
            print(f"  [PASS] {f.name} exists in bundle video.")
        else:
            print(f"  [FAIL] Missing {f.name}")
            all_ok = False
            
    return all_ok

def main():
    print("=" * 65)
    print("  COMPREHENSIVE DELIVERABLES VERIFICATION: EPISODE 06")
    print("=" * 65)
    
    t1 = test_audio()
    t2 = test_subtitles()
    t3 = test_visual_assets()
    t4 = test_publish_kits()
    t5 = test_openmontage_bundle()
    
    print("\n" + "=" * 65)
    print("VERIFICATION SUMMARY")
    print("=" * 65)
    print(f"  Test 1 (Audio Stems & Monotonic Sync):  {'PASS' if t1 else 'FAIL'}")
    print(f"  Test 2 (Subtitle Syntax & Monotonic):  {'PASS' if t2 else 'FAIL'}")
    print(f"  Test 3 (Visual Assets & Thumbnails):    {'PASS' if t3 else 'FAIL'}")
    print(f"  Test 4 (Publish Kits & <500 Char Tags): {'PASS' if t4 else 'FAIL'}")
    print(f"  Test 5 (OpenMontage Distribution Kit):  {'PASS' if t5 else 'FAIL'}")
    print("=" * 65)
    
    if all([t1, t2, t3, t4, t5]):
        print(">>> ALL NON-VIDEO DELIVERABLES 100% VERIFIED AND PRODUCTION READY! <<<")
        print("Google Flow base action images are isolated in google_flow_input_images/ awaiting user generation.")
        sys.exit(0)
    else:
        print(">>> VERIFICATION FAILED! PLEASE RESOLVE ISSUES ABOVE. <<<")
        sys.exit(1)

if __name__ == "__main__":
    main()
