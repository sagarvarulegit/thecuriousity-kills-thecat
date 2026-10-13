#!/usr/bin/env python3
"""
setup_ep07_openmontage_bundle.py — Setup OpenMontage Distribution Bundle for Episode 07:
The Secret Canyon of Waghur — The Lost Predecessors of Kailasa.
"""

import json
import shutil
from pathlib import Path

BASE_DIR = Path("C:/Sagar/Projects/thecuriousity-kills-thecat")
EP07_DIR = BASE_DIR / "ajanta-ellora" / "episode07"
BUNDLE_DIR = EP07_DIR / "openmontage_bundle"

META_DIR = BUNDLE_DIR / "metadata"
THUMB_DIR = BUNDLE_DIR / "thumbnails"
VIDEO_DIR = BUNDLE_DIR / "video"

META_DIR.mkdir(parents=True, exist_ok=True)
THUMB_DIR.mkdir(parents=True, exist_ok=True)
VIDEO_DIR.mkdir(parents=True, exist_ok=True)

def setup_bundle():
    print("=" * 65)
    print(" SETTING UP EPISODE 07 OPENMONTAGE BUNDLE")
    print("=" * 65)
    
    # 1. Subtitles (English & Hindi)
    srt_src = EP07_DIR / "subtitles" / "episode_07_full.srt"
    if srt_src.exists():
        shutil.copy2(srt_src, VIDEO_DIR / "subtitles.srt")
        print(f"  [OK] Copied English subtitles.srt to {VIDEO_DIR.name}/")
        
    srt_hi_src = EP07_DIR / "subtitles_hindi" / "episode_07_hindi_full.srt"
    if srt_hi_src.exists():
        shutil.copy2(srt_hi_src, VIDEO_DIR / "subtitles_hindi.srt")
        print(f"  [OK] Copied Hindi subtitles_hindi.srt to {VIDEO_DIR.name}/")
        
    # 2. Thumbnails
    thumb_src = EP07_DIR / "thumbnail" / "ep07_thumbnail_16x9_the_secret_canyon.jpg"
    if thumb_src.exists():
        shutil.copy2(thumb_src, THUMB_DIR / "thumbnail.jpg")
        print(f"  [OK] Copied Master thumbnail.jpg to {THUMB_DIR.name}/")
        
    s1_thumb = EP07_DIR / "thumbnail" / "short_01_thumbnail_9x16.jpg"
    if s1_thumb.exists():
        shutil.copy2(s1_thumb, THUMB_DIR / "short_01_thumbnail.jpg")
        print(f"  [OK] Copied Short 01 thumbnail to {THUMB_DIR.name}/")
        
    s2_thumb = EP07_DIR / "thumbnail" / "short_02_thumbnail_9x16.jpg"
    if s2_thumb.exists():
        shutil.copy2(s2_thumb, THUMB_DIR / "short_02_thumbnail.jpg")
        print(f"  [OK] Copied Short 02 thumbnail to {THUMB_DIR.name}/")
        
    # 3. Publish kit copy
    pub_src = EP07_DIR / "publish_kit" / "master_publish_kit.md"
    if pub_src.exists():
        shutil.copy2(pub_src, META_DIR / "youtube_publish_kit.md")
        print(f"  [OK] Copied youtube_publish_kit.md to {META_DIR.name}/")
        
    # 4. Chapters, Description, Tags, JSON
    tags = "Ajanta Caves,Waghur River,Kailasa Temple Predecessor,Satavahana dynasty,Ancient Indian Engineering,rock cut architecture,Cave 9,Cave 10,Buddhist monasteries,monsoon engineering,podhi cisterns,acoustic resonance stone,Deccan geology,ancient history documentary"
    (META_DIR / "tags.txt").write_text(tags, encoding="utf-8")
    
    chapters = """00:00 - The Hidden Crescent: The Pivot from Kailasa
01:16 - The First Chisel Strike: The Satavahana Inception
02:30 - Taming the Monsoon: Subterranean Hydrology & Podhi Cisterns
03:45 - The Sound of the Living Stone: Acoustic Architecture & 110Hz Resonance
05:35 - The 400-Year Hibernation: The Forgotten Horizon"""
    (META_DIR / "chapters.txt").write_text(chapters, encoding="utf-8")
    
    desc = f"""Long before Kailasa was carved from the mountain peak at Ellora, master stonecutters perfected the science of top-down basalt excavation 100 kilometers away, hidden inside a wild 75-meter volcanic canyon.

In this inaugural episode of Act II, we investigate the secret origins of Ajanta: how 2nd-century BCE monks engineered subterranean water filtration systems that survived two millennia, tuned solid basalt caves to 110Hz vocal acoustic resonance, and why the entire canyon mysteriously vanished for 400 years.

{chapters}

Audio Tracks Available:
- English Narration (Adam Stone - ElevenLabs)
- Hindi Narration (Prem - ElevenLabs Multilingual)
Audio Loudness: EBU R128 (-16.0 LUFS)"""
    (META_DIR / "description.txt").write_text(desc, encoding="utf-8")
    
    meta_json = {
        "title": "The Secret Canyon of Waghur: The Lost Predecessors of Kailasa",
        "series": "Kailasa & Ajanta: The Underground Giants",
        "episode": 7,
        "act": "Act II: The Lost Predecessor",
        "resolution": "1920x1080",
        "aspect_ratio": "16:9",
        "fps": 30,
        "audio_standard": "EBU R128 (-16.0 LUFS)",
        "audio_tracks": ["English (Default)", "Hindi (Multi-Language Track)"],
        "tags_count": len(tags.split(",")),
        "tags_characters": len(tags),
        "micro_beats": 45,
        "google_flow_kinetic_shots": 15,
        "unique_media_assets": 45
    }
    (META_DIR / "package.json").write_text(json.dumps(meta_json, indent=2), encoding="utf-8")
    print(f"  [OK] Generated OpenMontage package.json")
    print("=" * 65)

if __name__ == "__main__":
    setup_bundle()
