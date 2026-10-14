"""
Setup OpenMontage Distribution Bundle for Episode 06: The Sky Bridges of Kailasa.
Populates metadata, subtitles, and thumbnails directories according to the
OpenMontage package specification.
"""

import json
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent # ajanta-ellora
EP06_DIR = BASE_DIR / "episode06"
BUNDLE_DIR = EP06_DIR / "openmontage_bundle"

META_DIR = BUNDLE_DIR / "metadata"
THUMB_DIR = BUNDLE_DIR / "thumbnails"
VIDEO_DIR = BUNDLE_DIR / "video"

META_DIR.mkdir(parents=True, exist_ok=True)
THUMB_DIR.mkdir(parents=True, exist_ok=True)
VIDEO_DIR.mkdir(parents=True, exist_ok=True)

def setup_bundle():
    print("=" * 65)
    print(" SETTING UP EPISODE 06 OPENMONTAGE BUNDLE")
    print("=" * 65)
    
    # 1. Subtitles (English & Hindi)
    srt_src = EP06_DIR / "subtitles" / "episode_06_full.srt"
    if srt_src.exists():
        shutil.copy2(srt_src, VIDEO_DIR / "subtitles.srt")
        print(f"  [OK] Copied English subtitles.srt to {VIDEO_DIR.name}/")
        
    srt_hi_src = EP06_DIR / "subtitles_hindi" / "episode_06_hindi_full.srt"
    if srt_hi_src.exists():
        shutil.copy2(srt_hi_src, VIDEO_DIR / "subtitles_hindi.srt")
        print(f"  [OK] Copied Hindi subtitles_hindi.srt to {VIDEO_DIR.name}/")
        
    # 2. Thumbnails
    thumb_src = EP06_DIR / "thumbnail" / "ep06_master_thumbnail_16x9.jpg"
    if thumb_src.exists():
        shutil.copy2(thumb_src, THUMB_DIR / "thumbnail.jpg")
        print(f"  [OK] Copied Master thumbnail.jpg to {THUMB_DIR.name}/")
        
    s1_thumb = EP06_DIR / "thumbnail" / "short_01_thumbnail_9x16.jpg"
    if s1_thumb.exists():
        shutil.copy2(s1_thumb, THUMB_DIR / "short_01_thumbnail.jpg")
        print(f"  [OK] Copied Short 01 thumbnail to {THUMB_DIR.name}/")
        
    s2_thumb = EP06_DIR / "thumbnail" / "short_02_thumbnail_9x16.jpg"
    if s2_thumb.exists():
        shutil.copy2(s2_thumb, THUMB_DIR / "short_02_thumbnail.jpg")
        print(f"  [OK] Copied Short 02 thumbnail to {THUMB_DIR.name}/")
        
    # 3. Publish kit copy
    pub_src = EP06_DIR / "publish_kit" / "master_publish_kit.md"
    if pub_src.exists():
        shutil.copy2(pub_src, META_DIR / "youtube_publish_kit.md")
        print(f"  [OK] Copied youtube_publish_kit.md to {META_DIR.name}/")
        
    # 4. Chapters, Description, Tags, JSON
    tags = "Kailasa Temple,Ellora Caves,Cave 16,Sky Bridges,Ellora architecture,rock cut temple,monolithic temple,ancient Indian engineering,Rashtrakuta dynasty,Aurangzeb siege,Kokasa architect,Deccan basalt,ancient Indian history documentary"
    (META_DIR / "tags.txt").write_text(tags, encoding="utf-8")
    
    chapters = """00:00 - The Bridges in the Sky
01:18 - The Queen's Vow & Kokasa's 7-Day Shikhara
02:36 - Carving the Void: Hanging Basalt Mechanics
03:54 - Courtyard Monoliths: Victory Pillars & Living Elephants
05:12 - The Living Epics: Ramayana & Ravana Under Kailash
06:30 - The White Mountain: The Agate-Burnished Chuna Plaster
07:48 - The Mountain That Refused to Fall: Aurangzeb's 1682 Siege
09:06 - The Architect's Confession: Katham-akrita yan-maya"""
    (META_DIR / "chapters.txt").write_text(chapters, encoding="utf-8")
    
    desc = f"""Suspended thirty feet in the open air, a monolithic stone bridge spans the volcanic trench of Cave 16 at Ellora. There are no mortar joints, no structural keystones, and no iron tie-rods holding it together. It was carved out of the solid living mountain from the heavens downward.

In this episode, we investigate how ancient master builders calculated the tensile limits of volcanic basalt, excavated hollow voids beneath suspended ceilings without structural collapse, and created an architectural masterpiece so indestructible that a 1,000-man imperial demolition army couldn't fell it after a full year of siege.

{chapters}

Audio Tracks Available:
- English Narration (Adam Stone - ElevenLabs)
- Hindi Narration (Prem - ElevenLabs Multilingual)
Audio Loudness: EBU R128 (-16.0 LUFS)"""
    (META_DIR / "description.txt").write_text(desc, encoding="utf-8")
    
    meta_json = {
        "title": "The Sky Bridges of Kailasa: Carving What Should Have Collapsed",
        "series": "Kailasa: The Mountain Carved From Above",
        "episode": 6,
        "resolution": "1920x1080",
        "aspect_ratio": "16:9",
        "fps": 30,
        "audio_standard": "EBU R128 (-16.0 LUFS)",
        "audio_tracks": ["English (Default)", "Hindi (Multi-Language Track)"],
        "tags_count": len(tags.split(",")),
        "tags_characters": len(tags),
        "micro_beats": 72,
        "google_flow_kinetic_shots": 16,
        "unique_media_assets": 72
    }
    (META_DIR / "metadata.json").write_text(json.dumps(meta_json, indent=2), encoding="utf-8")
    print(f"  [OK] Wrote chapters.txt, description.txt, tags.txt, metadata.json")
    
    # 5. README in openmontage_bundle
    readme = """# Kailasa Episode 06 — OpenMontage Distribution Bundle

This package conforms to the OpenMontage distribution specification.

## Contents
- `metadata/`: YouTube publish kit, chapter markers, description, tags, and JSON metadata
- `thumbnails/`: Broadcast 16:9 Master thumbnail (< 2.0 MB) & dedicated 9:16 Shorts thumbnails
- `video/`: Subtitles (`subtitles.srt`, `subtitles_hindi.srt`). Master video (`output.mp4`) will be populated upon final assembly.
"""
    (BUNDLE_DIR / "README.md").write_text(readme, encoding="utf-8")
    print(f"  [OK] Generated README.md")
    print("=" * 65)
    print(" OPENMONTAGE BUNDLE SETUP COMPLETE!")
    print("=" * 65)

if __name__ == "__main__":
    setup_bundle()
