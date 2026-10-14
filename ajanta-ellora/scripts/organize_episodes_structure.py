"""
Episode-Wise Organization Script for Ajanta-Ellora Web-Series.
Organizes all assets, scripts, publish kits, subtitles, audios, images, videos,
and rendered final videos into self-contained episode directories:
  - ajanta-ellora/episode01/
  - ajanta-ellora/episode02/
"""

import os
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
WORKSPACE_ROOT = BASE_DIR.parent

def organize_episode_02():
    print("\n--- Organizing Episode 02 into ajanta-ellora/episode02/ ---")
    ep2_dir = BASE_DIR / "episode02"
    ep2_dir.mkdir(parents=True, exist_ok=True)

    # Subfolders
    subdirs = {
        "final_videos": ep2_dir / "final_videos",
        "publish_kit": ep2_dir / "publish_kit",
        "script_and_storyboard": ep2_dir / "script_and_storyboard",
        "subtitles": ep2_dir / "subtitles",
        "audio": ep2_dir / "audio",
        "images": ep2_dir / "images",
        "videos": ep2_dir / "videos",
        "openmontage_bundle": ep2_dir / "openmontage_bundle",
    }
    for p in subdirs.values():
        p.mkdir(parents=True, exist_ok=True)

    # 1. Final Videos
    src_out = BASE_DIR / "output"
    videos_to_copy = [
        ("episode_02_master_preview.mp4", "episode_02_master_preview.mp4"),
        ("short_01_the_fire_secret.mp4", "short_01_the_fire_secret.mp4"),
        ("short_02_where_did_400k_tons_go.mp4", "short_02_where_did_400k_tons_go.mp4"),
    ]
    for src_name, dst_name in videos_to_copy:
        src = src_out / src_name
        if src.exists():
            shutil.copy2(src, subdirs["final_videos"] / dst_name)
            print(f"  [final_videos] {dst_name} ({src.stat().st_size:,} bytes)")

    # 2. Publish Kits
    src_ep = BASE_DIR / "episodes"
    publish_kits = [
        "episode-02-youtube-publish-kit.md",
        "short-01-the-fire-secret-youtube-publish-kit.md",
        "short-02-where-did-400k-tons-go-youtube-publish-kit.md",
    ]
    for pk in publish_kits:
        src = src_ep / pk
        if src.exists():
            shutil.copy2(src, subdirs["publish_kit"] / pk)
            print(f"  [publish_kit] {pk}")

    # 3. Script and Storyboard
    storyboards = [
        "episode-02-the-inferno-in-the-trenches.md",
    ]
    for sb in storyboards:
        src = src_ep / sb
        if src.exists():
            shutil.copy2(src, subdirs["script_and_storyboard"] / sb)
            print(f"  [script_and_storyboard] {sb}")

    # 4. Subtitles
    src_subs = BASE_DIR / "assets" / "episode-02" / "subtitles"
    if src_subs.exists():
        for srt in src_subs.glob("*.srt"):
            shutil.copy2(srt, subdirs["subtitles"] / srt.name)
            print(f"  [subtitles] {srt.name}")

    # 5. Audio
    src_aud = BASE_DIR / "assets" / "episode-02" / "audio"
    if src_aud.exists():
        for aud in src_aud.glob("*.mp3"):
            shutil.copy2(aud, subdirs["audio"] / aud.name)
            print(f"  [audio] {aud.name}")

    # 6. Images, Thumbnails & Google Flow Input Images
    src_img = BASE_DIR / "assets" / "episode-02" / "images"
    if src_img.exists():
        for img in src_img.glob("*.jpg"):
            shutil.copy2(img, subdirs["images"] / img.name)
            print(f"  [images] {img.name}")

    src_thumb = BASE_DIR / "assets" / "episode-02" / "thumbnail"
    thumb_dir = ep2_dir / "thumbnail"
    thumb_dir.mkdir(parents=True, exist_ok=True)
    if src_thumb.exists():
        for thumb in src_thumb.glob("*.jpg"):
            shutil.copy2(thumb, thumb_dir / thumb.name)
            print(f"  [thumbnail] {thumb.name}")

    src_gf = BASE_DIR / "assets" / "episode-02" / "google_flow_input_images"
    gf_dir = ep2_dir / "google_flow_input_images"
    gf_dir.mkdir(parents=True, exist_ok=True)
    if src_gf.exists():
        for gf in src_gf.glob("*.jpg"):
            shutil.copy2(gf, gf_dir / gf.name)
            print(f"  [google_flow_input_images] {gf.name}")

    # 7. Videos (Action clips)
    src_vids = BASE_DIR / "assets" / "episode-02" / "videos"
    if src_vids.exists():
        for vid in src_vids.glob("*.mp4"):
            shutil.copy2(vid, subdirs["videos"] / vid.name)
            print(f"  [videos] {vid.name}")

    # 8. OpenMontage Bundle
    src_om = WORKSPACE_ROOT / "OpenMontage" / "projects" / "kailasa_episode_02" / "exports"
    if src_om.exists():
        for item in src_om.glob("**/*"):
            if item.is_file():
                rel = item.relative_to(src_om)
                target = subdirs["openmontage_bundle"] / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, target)
        print(f"  [openmontage_bundle] Copied export bundle")

    print("--- Episode 02 Organization Complete! ---")

def organize_episode_01():
    print("\n--- Organizing Episode 01 into ajanta-ellora/episode01/ ---")
    ep1_dir = BASE_DIR / "episode01"
    ep1_dir.mkdir(parents=True, exist_ok=True)

    subdirs = {
        "final_videos": ep1_dir / "final_videos",
        "publish_kit": ep1_dir / "publish_kit",
        "script_and_storyboard": ep1_dir / "script_and_storyboard",
        "subtitles": ep1_dir / "subtitles",
        "audio": ep1_dir / "audio",
        "images": ep1_dir / "images",
        "openmontage_bundle": ep1_dir / "openmontage_bundle",
    }
    for p in subdirs.values():
        p.mkdir(parents=True, exist_ok=True)

    # 1. Final Videos
    src_out = BASE_DIR / "output"
    videos_to_copy = [
        ("episode_01_master_preview.mp4", "episode_01_master_preview.mp4"),
        ("short_01_the_queen_vow.mp4", "short_01_the_queen_vow.mp4"),
        ("short_02_billion_dollar_mountain.mp4", "short_02_billion_dollar_mountain.mp4"),
    ]
    for src_name, dst_name in videos_to_copy:
        src = src_out / src_name
        if src.exists():
            shutil.copy2(src, subdirs["final_videos"] / dst_name)
            print(f"  [final_videos] {dst_name} ({src.stat().st_size:,} bytes)")

    # 2. Publish Kits
    src_ep = BASE_DIR / "episodes"
    publish_kits = [
        "episode-01-youtube-publish-kit.md",
        "short-01-the-queen-vow-youtube-publish-kit.md",
        "short-02-billion-dollar-mountain-youtube-publish-kit.md",
    ]
    for pk in publish_kits:
        src = src_ep / pk
        if src.exists():
            shutil.copy2(src, subdirs["publish_kit"] / pk)
            print(f"  [publish_kit] {pk}")

    # 3. Script and Storyboard
    storyboards = [
        "episode-01-the-queen-vow.md",
    ]
    for sb in storyboards:
        src = src_ep / sb
        if src.exists():
            shutil.copy2(src, subdirs["script_and_storyboard"] / sb)
            print(f"  [script_and_storyboard] {sb}")

    # 4. Subtitles
    src_subs = BASE_DIR / "assets" / "episode-01" / "subtitles"
    if src_subs.exists():
        for srt in src_subs.glob("*.srt"):
            shutil.copy2(srt, subdirs["subtitles"] / srt.name)
            print(f"  [subtitles] {srt.name}")

    # 5. Audio
    src_aud = BASE_DIR / "assets" / "episode-01" / "audio"
    if src_aud.exists():
        for aud in src_aud.glob("*.mp3"):
            shutil.copy2(aud, subdirs["audio"] / aud.name)
            print(f"  [audio] {aud.name}")

    # 6. Images & Thumbnails
    src_img = BASE_DIR / "assets" / "episode-01" / "images"
    if src_img.exists():
        for img in src_img.glob("*.jpg"):
            shutil.copy2(img, subdirs["images"] / img.name)
            print(f"  [images] {img.name}")
    src_thumb = BASE_DIR / "assets" / "episode-01" / "thumbnail"
    if src_thumb.exists():
        for thumb in src_thumb.glob("*.jpg"):
            shutil.copy2(thumb, subdirs["images"] / thumb.name)
            print(f"  [images/thumbnail] {thumb.name}")

    # 7. OpenMontage Bundle
    src_om = WORKSPACE_ROOT / "OpenMontage" / "projects" / "kailasa_episode_01" / "exports"
    if src_om.exists():
        for item in src_om.glob("**/*"):
            if item.is_file():
                rel = item.relative_to(src_om)
                target = subdirs["openmontage_bundle"] / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, target)
        print(f"  [openmontage_bundle] Copied export bundle")

    print("--- Episode 01 Organization Complete! ---")

if __name__ == "__main__":
    organize_episode_01()
    organize_episode_02()
