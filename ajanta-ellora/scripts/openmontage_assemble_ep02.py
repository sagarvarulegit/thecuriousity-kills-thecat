"""
OpenMontage Pipeline Integration Engine for Kailasa Episode 2.
Initializes OpenMontage project workspace, links assets, supports Google Flow I2V clips,
executes canonical artifacts packaging, and runs OpenMontage ExportBundle for YouTube publishing.
"""

import os
import sys
import json
import shutil
import subprocess
from pathlib import Path

# Add OpenMontage to sys.path
OPENMONTAGE_ROOT = Path("OpenMontage").resolve()
if str(OPENMONTAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(OPENMONTAGE_ROOT))

from lib.checkpoint import init_project
from tools.publishers.export_bundle import ExportBundle

PROJECT_ID = "kailasa_episode_02"
PROJECT_TITLE = "Kailasa: The Inferno in the Trenches (Episode 2)"
PIPELINE_TYPE = "cinematic"

WORKSPACE_ROOT = Path(".").resolve()
ASSETS_EP2 = WORKSPACE_ROOT / "ajanta-ellora" / "assets" / "episode-02"
OUTPUT_DIR = WORKSPACE_ROOT / "ajanta-ellora" / "output"
GOOGLE_FLOW_DIR = ASSETS_EP2 / "google_flow_videos"
GOOGLE_FLOW_DIR.mkdir(parents=True, exist_ok=True)

def setup_openmontage_project():
    print(f"\n--- Initializing OpenMontage Project: {PROJECT_ID} ---")
    project_dir = init_project(
        project_id=PROJECT_ID,
        title=PROJECT_TITLE,
        pipeline_type=PIPELINE_TYPE
    )
    print(f"OpenMontage Project Directory: {project_dir}")

    # Copy master hero images
    om_img_dir = project_dir / "assets" / "images"
    om_img_dir.mkdir(parents=True, exist_ok=True)
    for img in (ASSETS_EP2 / "images").glob("*.jpg"):
        shutil.copy2(img, om_img_dir / img.name)

    # Copy studio narration audio
    om_audio_dir = project_dir / "assets" / "audio"
    om_audio_dir.mkdir(parents=True, exist_ok=True)
    for aud in (ASSETS_EP2 / "audio").glob("*.mp3"):
        shutil.copy2(aud, om_audio_dir / aud.name)

    # Check for action video clips
    om_video_dir = project_dir / "assets" / "video"
    om_video_dir.mkdir(parents=True, exist_ok=True)
    video_clips = list(GOOGLE_FLOW_DIR.glob("*.mp4")) + list((ASSETS_EP2 / "videos").glob("*.mp4"))
    for clip in video_clips:
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
            {"id": "scene_01", "name": "The Sound of War in Stone", "duration_seconds": 52.06, "acts": ["Act 1"]},
            {"id": "scene_02", "name": "The Geometry of the Three Trenches", "duration_seconds": 55.04, "acts": ["Act 2"]},
            {"id": "scene_03", "name": "The Physical Limit of Iron & Steel", "duration_seconds": 54.07, "acts": ["Act 3"]},
            {"id": "scene_04", "name": "Agni-Karma: Ancient Thermal Shock", "duration_seconds": 60.55, "acts": ["Act 4"]},
            {"id": "scene_05", "name": "The Steam Flash: Quenching the Mountain", "duration_seconds": 50.83, "acts": ["Act 5"]},
            {"id": "scene_06", "name": "The Chisel Storm & Lever Crews", "duration_seconds": 37.99, "acts": ["Act 6"]},
            {"id": "scene_07", "name": "Gravity as an Engine: 100,000 Tons Cleared", "duration_seconds": 53.35, "acts": ["Act 7"]},
            {"id": "scene_08", "name": "The Monolithic Island Emerges", "duration_seconds": 56.23, "acts": ["Act 8"]}
        ],
        "total_duration": 420.26
    }
    with open(artifacts_dir / "scene_plan.json", "w", encoding="utf-8") as f:
        json.dump(scene_plan, f, indent=2)

    # 2. Asset Manifest Artifact
    assets_manifest = {
        "version": "1.0",
        "project_id": PROJECT_ID,
        "visual_assets": [f.name for f in (ASSETS_EP2 / "images").glob("*.jpg")],
        "audio_assets": [f.name for f in (ASSETS_EP2 / "audio").glob("*.mp3")],
        "google_flow_videos": [f.name for f in GOOGLE_FLOW_DIR.glob("*.mp4")],
        "subtitles": "episode_02_full.srt",
        "thumbnail": "thumbnail_episode_02_master.jpg"
    }
    with open(artifacts_dir / "asset_manifest.json", "w", encoding="utf-8") as f:
        json.dump(assets_manifest, f, indent=2)

    # 3. Edit Decisions Artifact
    edit_decisions = {
        "version": "1.0",
        "render_runtime": "ffmpeg",
        "total_runtime_seconds": 420.26,
        "total_micro_cuts": 80,
        "target_resolution": "1920x1080",
        "target_fps": 30,
        "cuts_pacing_rule": "5.5s-6.5s average cut pace for high YouTube retention",
        "audio_stem": "episode_02_full_narration.mp3"
    }
    with open(artifacts_dir / "edit_decisions.json", "w", encoding="utf-8") as f:
        json.dump(edit_decisions, f, indent=2)

    print("Canonical artifacts generated in artifacts/: scene_plan.json, asset_manifest.json, edit_decisions.json")

def run_export_bundle(project_dir: Path):
    print("\n--- Running OpenMontage ExportBundle Publisher ---")
    master_video = OUTPUT_DIR / "episode_02_master_preview.mp4"
    if not master_video.exists():
        print(f"Error: Master video not found at {master_video}")
        return None

    # Copy master render to OpenMontage renders/
    om_renders = project_dir / "renders"
    om_renders.mkdir(parents=True, exist_ok=True)
    target_render = om_renders / "episode_02_master.mp4"
    shutil.copy2(master_video, target_render)

    subtitles_path = ASSETS_EP2 / "subtitles" / "episode_02_full.srt"
    thumbnail_path = ASSETS_EP2 / "thumbnail" / "thumbnail_episode_02_master.jpg"

    chapters = [
        {"start_seconds": 0.0, "title": "The Sound of War in Stone: Mobilizing 10,000 Quarrymen"},
        {"start_seconds": 52.06, "title": "The Geometry of the Three Trenches (33-Meter Vertical Abyss)"},
        {"start_seconds": 107.10, "title": "The Physical Limit of Iron: Why Steel Chisels Bounced"},
        {"start_seconds": 161.17, "title": "Agni-Karma: The Ancient Science of Thermal Shock"},
        {"start_seconds": 221.72, "title": "The Steam Flash: Quenching 600°C Basalt with Mountain Water"},
        {"start_seconds": 272.55, "title": "The Chisel Storm: Levering 2-Ton Basalt Slabs in Minutes"},
        {"start_seconds": 310.54, "title": "Gravity as an Engine: Timber Chutes & 100,000 Tons Cleared"},
        {"start_seconds": 363.89, "title": "The Monolithic Island Emerges (The Spire Cliffhanger)"}
    ]

    description = (
        "Before ancient builders could carve a single statue of Shiva, they had to remove 400,000 tons of the hardest rock on Earth.\n\n"
        "When iron chisels shattered against 140 MPa tholeiitic basalt, master architect Kokasa deployed an ancient weapon recorded in the Shilpa Shastras: Agni-Karma—the science of thermal shock.\n\n"
        "This is Episode 2 of our 10-part documentary web-series on the construction of the Kailasa Temple (Ellora Cave 16)."
    )

    tags = [
        "Kailasa Temple", "Ellora Caves", "Kailasanatha Temple", "How Kailasa temple was built",
        "Ancient Indian Architecture", "Ellora Cave 16", "ancient engineering mysteries",
        "thermal shock ancient quarrying", "Agni Karma fire setting", "ancient India documentary",
        "King Krishna I", "Rashtrakuta dynasty", "top down rock cut temple", "Kokasa architect",
        "Deccan basalt", "400000 tons rock", "how ancient temples were carved", "monolithic architecture",
        "ancient technology", "Kailasa excavation", "gravity chutes ancient", "Ellora caves history", "megaliths"
    ]

    hashtags = ["#KailasaTemple", "#ElloraCaves", "#AncientEngineering", "#AncientIndia", "#Documentary", "#Archaeology"]

    inputs = {
        "video_path": str(target_render),
        "title": "How Ancient Indians Broke a Mountain with Fire and Water",
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
    project_dir = setup_openmontage_project()
    create_canonical_artifacts(project_dir)
    run_export_bundle(project_dir)

if __name__ == "__main__":
    main()
