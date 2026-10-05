"""
OpenMontage Pipeline Integration Engine for Kailasa Documentary Web-Series.
Initializes OpenMontage project workspace, links assets, supports Google Flow I2V clips,
executes video composition, and runs OpenMontage ExportBundle for YouTube publishing.
"""

import os
import sys
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

# Add OpenMontage to sys.path
OPENMONTAGE_ROOT = Path("OpenMontage").resolve()
if str(OPENMONTAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(OPENMONTAGE_ROOT))

from lib.checkpoint import init_project
from tools.publishers.export_bundle import ExportBundle

PROJECT_ID = "kailasa_episode_01"
PROJECT_TITLE = "Kailasa: The Blueprint of the Gods (Episode 1)"
PIPELINE_TYPE = "cinematic"

WORKSPACE_ROOT = Path(".").resolve()
ASSETS_EP1 = WORKSPACE_ROOT / "ajanta-ellora" / "assets" / "episode-01"
OUTPUT_DIR = WORKSPACE_ROOT / "ajanta-ellora" / "output"
GOOGLE_FLOW_DIR = ASSETS_EP1 / "google_flow_videos"
GOOGLE_FLOW_DIR.mkdir(parents=True, exist_ok=True)

def setup_openmontage_project():
    print(f"\n--- Initializing OpenMontage Project: {PROJECT_ID} ---")
    project_dir = init_project(
        project_id=PROJECT_ID,
        title=PROJECT_TITLE,
        pipeline_type=PIPELINE_TYPE
    )
    print(f"OpenMontage Project Directory: {project_dir}")

    # Copy/Symlink master hero images
    om_img_dir = project_dir / "assets" / "images"
    for img in (ASSETS_EP1 / "images").glob("*.jpg"):
        shutil.copy2(img, om_img_dir / img.name)

    # Copy ElevenLabs studio narration audio
    om_audio_dir = project_dir / "assets" / "audio"
    for aud in (ASSETS_EP1 / "audio_elevenlabs").glob("*.mp3"):
        shutil.copy2(aud, om_audio_dir / aud.name)

    # Check for Google Flow converted clips
    om_video_dir = project_dir / "assets" / "video"
    gf_clips = list(GOOGLE_FLOW_DIR.glob("*.mp4"))
    print(f"Detected {len(gf_clips)} Google Flow converted video clips in {GOOGLE_FLOW_DIR}")
    for clip in gf_clips:
        shutil.copy2(clip, om_video_dir / clip.name)

    return project_dir

def create_canonical_artifacts(project_dir: Path):
    print("\n--- Generating OpenMontage Canonical Artifacts ---")
    artifacts_dir = project_dir / "artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    # 1. Scene Plan Artifact
    scene_plan = {
        "version": "1.0",
        "title": PROJECT_TITLE,
        "scenes": [
            {"id": "scene_01", "name": "The Crisis & The Fatal Vow", "duration_seconds": 71.66, "acts": ["Act 1"]},
            {"id": "scene_02", "name": "The Architect's Heresy (Kokasa)", "duration_seconds": 82.06, "acts": ["Act 2"]},
            {"id": "scene_03", "name": "Geology: Deccan Traps Basalt", "duration_seconds": 90.65, "acts": ["Act 3"]},
            {"id": "scene_04", "name": "Imperial Capital & Treasury", "duration_seconds": 86.98, "acts": ["Act 4"]},
            {"id": "scene_05", "name": "Artisan Guilds & The Forge", "duration_seconds": 82.43, "acts": ["Act 5"]},
            {"id": "scene_06", "name": "The Sacred Survey & Geometry", "duration_seconds": 91.21, "acts": ["Act 6"]},
            {"id": "scene_07", "name": "The Royal Charter & Wax Seal", "duration_seconds": 54.20, "acts": ["Act 7"]},
            {"id": "scene_08", "name": "The Historic First Strike", "duration_seconds": 52.11, "acts": ["Act 8"]}
        ],
        "total_duration": 611.3
    }
    with open(artifacts_dir / "scene_plan.json", "w", encoding="utf-8") as f:
        json.dump(scene_plan, f, indent=2)

    # 2. Asset Manifest Artifact
    assets_manifest = {
        "version": "1.0",
        "project_id": PROJECT_ID,
        "visual_assets": [f.name for f in (ASSETS_EP1 / "images").glob("*.jpg")],
        "audio_assets": [f.name for f in (ASSETS_EP1 / "audio_elevenlabs").glob("*.mp3")],
        "google_flow_videos": [f.name for f in GOOGLE_FLOW_DIR.glob("*.mp4")],
        "subtitles": "episode_01_full.srt",
        "thumbnail": "thumbnail_episode_01_master.jpg"
    }
    with open(artifacts_dir / "asset_manifest.json", "w", encoding="utf-8") as f:
        json.dump(assets_manifest, f, indent=2)

    # 3. Edit Decisions Artifact
    edit_decisions = {
        "version": "1.0",
        "render_runtime": "ffmpeg",
        "total_runtime_seconds": 611.55,
        "total_micro_cuts": 92,
        "target_resolution": "1920x1080",
        "target_fps": 30,
        "cuts_pacing_rule": "5.5s-6.5s average cut pace for high YouTube retention",
        "audio_stem": "episode_01_master_audio.mp3"
    }
    with open(artifacts_dir / "edit_decisions.json", "w", encoding="utf-8") as f:
        json.dump(edit_decisions, f, indent=2)

    print("Canonical artifacts generated in artifacts/: scene_plan.json, asset_manifest.json, edit_decisions.json")

def run_export_bundle(project_dir: Path):
    print("\n--- Running OpenMontage ExportBundle Publisher ---")
    master_video = OUTPUT_DIR / "episode_01_master_preview.mp4"
    if not master_video.exists():
        print(f"Error: Master video not found at {master_video}")
        return None

    # Copy master render to OpenMontage renders/
    om_renders = project_dir / "renders"
    om_renders.mkdir(parents=True, exist_ok=True)
    target_render = om_renders / "episode_01_master.mp4"
    shutil.copy2(master_video, target_render)

    subtitles_path = ASSETS_EP1 / "subtitles" / "episode_01_full.srt"
    thumbnail_path = ASSETS_EP1 / "thumbnail" / "thumbnail_episode_01_master.jpg"

    chapters = [
        {"start_seconds": 0.0, "title": "The Crisis & The Queen's Fatal Fast"},
        {"start_seconds": 71.66, "title": "The Architect's Heresy (Kokasa's Top-Down Plan)"},
        {"start_seconds": 153.72, "title": "The Deccan Traps: Scouting 66-Million-Year-Old Basalt"},
        {"start_seconds": 244.37, "title": "Imperial Capital: Mobilizing Gold & Trade Guilds"},
        {"start_seconds": 331.35, "title": "The Industrial Army: 10,000 Artisans & The Steel Forge"},
        {"start_seconds": 413.78, "title": "Sacred Geometry: Snapping the Red Chalk Baseline"},
        {"start_seconds": 504.99, "title": "The Royal Charter: Sealed in Molten Wax"},
        {"start_seconds": 559.19, "title": "The First Strike: The Downward Journey Begins"}
    ]

    description = (
        "They didn't build this temple with stones. They took an entire volcanic mountain—and carved away 400,000 tons of solid basalt until a multi-tiered cathedral was left standing in the sun.\n\n"
        "In the year 756 CE, an impossible royal crisis struck the Rashtrakuta Empire. A dying king, a queen's fatal vow, and an unknown architect named Kokasa who proposed a radical, dangerous idea: cut from the top down.\n\n"
        "This is Episode 1 of our 10-part documentary web-series on the construction of Kailasa Temple (Ellora Cave 16) and the Ajanta caves."
    )

    tags = [
        "Kailasa Temple", "Ellora Caves", "Ancient Indian Architecture", "How Kailasa temple was built",
        "Ajanta and Ellora caves", "Ellora Cave 16", "Ancient engineering mysteries", "King Krishna I",
        "Rashtrakuta dynasty", "top down rock cut temple", "Kokasa architect", "Deccan traps basalt",
        "Baroda copper plate inscription", "megalithic architecture", "ancient India documentary",
        "Katha Kalpataru", "lost ancient technology", "monolithic architecture", "history documentary"
    ]

    hashtags = ["#KailasaTemple", "#AncientEngineering", "#ElloraCaves", "#Documentary", "#IncredibleIndia"]

    inputs = {
        "video_path": str(target_render),
        "title": "They Carved a Mountain From the Top Down (Nobody Knows How)",
        "project_name": PROJECT_ID,
        "export_dir": str(project_dir / "exports"),
        "description": description,
        "tags": tags,
        "hashtags": hashtags,
        "chapters": chapters,
        "subtitles_path": str(subtitles_path) if subtitles_path.exists() else None,
        "thumbnail_path": str(thumbnail_path) if thumbnail_path.exists() else None,
        "platform": "youtube",
        "visibility": "public"
    }

    bundler = ExportBundle()
    res = bundler.execute(inputs)
    if res.success:
        print(f"SUCCESS: ExportBundle completed successfully!")
        print(f"Export directory: {res.data['export_path']}")
        print("Files created in bundle:")
        for f in res.data["files_written"]:
            print(f"  - {f}")
        return res.data
    else:
        print(f"ExportBundle Error: {res.error}")
        return None

def main():
    print("==================================================")
    print("OpenMontage Pipeline Integration: Kailasa Ep. 1")
    print("==================================================")
    project_dir = setup_openmontage_project()
    create_canonical_artifacts(project_dir)
    res = run_export_bundle(project_dir)
    print("\n==================================================")
    print("OpenMontage Assembly & Publish Suite Complete!")
    print("==================================================")

if __name__ == "__main__":
    main()
