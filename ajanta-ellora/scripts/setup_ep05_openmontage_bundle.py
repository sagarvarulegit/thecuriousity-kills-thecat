"""
Setup OpenMontage Distribution Bundle for Episode 05.
Populates metadata, subtitles, and thumbnails directories according to the
OpenMontage package specification.
"""

import json
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent # ajanta-ellora
EP05_DIR = BASE_DIR / "episode05"
BUNDLE_DIR = EP05_DIR / "openmontage_bundle"

META_DIR = BUNDLE_DIR / "metadata"
THUMB_DIR = BUNDLE_DIR / "thumbnails"
VIDEO_DIR = BUNDLE_DIR / "video"

META_DIR.mkdir(parents=True, exist_ok=True)
THUMB_DIR.mkdir(parents=True, exist_ok=True)
VIDEO_DIR.mkdir(parents=True, exist_ok=True)

def setup_bundle():
    print("=" * 65)
    print(" SETTING UP EPISODE 05 OPENMONTAGE BUNDLE")
    print("=" * 65)
    
    # 1. Subtitles
    srt_src = EP05_DIR / "subtitles" / "episode_05_full.srt"
    if srt_src.exists():
        shutil.copy2(srt_src, VIDEO_DIR / "subtitles.srt")
        print(f"  [OK] Copied subtitles.srt to {VIDEO_DIR.name}/")
        
    # 2. Thumbnail
    thumb_src = EP05_DIR / "thumbnail" / "ep05_master_thumbnail_16x9.jpg"
    if thumb_src.exists():
        shutil.copy2(thumb_src, THUMB_DIR / "thumbnail.jpg")
        print(f"  [OK] Copied thumbnail.jpg to {THUMB_DIR.name}/")
        
    # 3. Publish kit copy
    pub_src = EP05_DIR / "publish_kit" / "master_publish_kit.md"
    if pub_src.exists():
        shutil.copy2(pub_src, META_DIR / "youtube_publish_kit.md")
        print(f"  [OK] Copied youtube_publish_kit.md to {META_DIR.name}/")
        
    # 4. Chapters, Description, Tags, JSON
    tags = "Kailasa Temple,Ellora Caves,Cave 16,Ellora architecture,rock cut temple,monolithic temple,elephant sculptures,Indian sculpture,Rashtrakuta,Shiva temple,Deccan art,Indian history documentary,temple architecture"
    (META_DIR / "tags.txt").write_text(tags, encoding="utf-8")
    
    chapters = """00:00 - The Animals Beneath
00:50 - A Mountain as Temple
01:40 - Reading the Plinth
02:30 - The Illusion of Support
03:20 - Animals and the Sacred Mountain
04:10 - One Stone, Many Images
05:00 - The Viewer Completes the Image
05:50 - Beneath the Mountain"""
    (META_DIR / "chapters.txt").write_text(chapters, encoding="utf-8")
    
    desc = f"""At Ellora’s Kailasa Temple, a procession of carved elephants runs beneath the raised plinth. They appear to carry the temple, but the relief figures are part of the rock-cut lower storey, not freestanding pillars. This episode looks at how sculpture gives architectural weight a vivid, living image—and separates what the stone shows from interpretations of what it may mean.

{chapters}"""
    (META_DIR / "description.txt").write_text(desc, encoding="utf-8")
    
    meta_json = {
        "title": "Why Are Elephants Carved Beneath Kailasa Temple?",
        "series": "Kailasa: The Mountain Carved From Above",
        "episode": 5,
        "resolution": "1920x1080",
        "aspect_ratio": "16:9",
        "fps": 30,
        "audio": "EBU R128 (-16 LUFS)",
        "tags_count": len(tags.split(",")),
        "tags_characters": len(tags),
        "micro_beats": 72,
        "unique_media_assets": 72
    }
    (META_DIR / "metadata.json").write_text(json.dumps(meta_json, indent=2), encoding="utf-8")
    print(f"  [OK] Wrote chapters.txt, description.txt, tags.txt, metadata.json")
    
    # 5. README in openmontage_bundle
    readme = """# Kailasa Episode 05 — OpenMontage Distribution Bundle

This package conforms to the OpenMontage distribution specification.

## Contents
- `metadata/`: YouTube publish kit, chapter markers, description, tags, and JSON metadata
- `thumbnails/`: Broadcast 16:9 Master thumbnail (< 2.0 MB)
- `video/`: Subtitles (`subtitles.srt`). Master video (`output.mp4`) will be populated upon final assembly.
"""
    (BUNDLE_DIR / "README.md").write_text(readme, encoding="utf-8")
    print(f"  [OK] Generated README.md")
    print("=" * 65)
    print(" OPENMONTAGE BUNDLE SETUP COMPLETE!")
    print("=" * 65)

if __name__ == "__main__":
    setup_bundle()
