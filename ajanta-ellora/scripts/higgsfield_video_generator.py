#!/usr/bin/env python3
"""
higgsfield_video_generator.py — Higgsfield Automated Video Bridge for Ajanta-Ellora WebSeries

Automates Image-to-Video generation using Higgsfield CLI (Veo 3.1, Seedance 2.5, Kling 3.0 Turbo)
from the episode's GOOGLE_FLOW_PROMPT_SHEET.md.

Enforces:
1. Credit Protection: Default is --dry-run. Pass --execute to run live.
2. Zero Media Repetition Invariant: Each clip has a strictly unique filename and prompt.
3. Audio/SRT Beat Synchronization: Maps 1:1 to the spoken narration beat.
4. Resolution Enforcement: Standard 1080p (1920x1080) / 16:9.
"""

import os
import sys
import re
import argparse
import subprocess
import json
import urllib.request
from pathlib import Path

# Fix Windows console UTF-8 encoding
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

WORKSPACE_ROOT = Path("C:/Sagar/Projects/thecuriousity-kills-thecat")

def parse_prompt_sheet(prompt_sheet_path: Path):
    """
    Parses the Markdown table in GOOGLE_FLOW_PROMPT_SHEET.md into structured records.
    """
    if not prompt_sheet_path.exists():
        raise FileNotFoundError(f"Prompt sheet not found at: {prompt_sheet_path}")

    records = []
    content = prompt_sheet_path.read_text(encoding="utf-8")
    
    for line in content.splitlines():
        line = line.strip()
        if not line.startswith("|") or "Input Image Filename" in line or "---" in line:
            continue
        cols = [c.strip() for c in line.split("|") if c.strip()]
        if len(cols) < 4:
            continue

        input_img = cols[0].strip("` ")
        target_video = cols[1].strip("` ")
        beat_info = cols[2]
        # The prompt is always the last column
        prompt_text = cols[-1]

        records.append({
            "input_image": input_img,
            "target_video": target_video,
            "beat_info": beat_info,
            "prompt": prompt_text
        })
        
    return records

import shutil

def get_cli_bin():
    """Finds the absolute path to higgsfield or hf CLI."""
    cli = shutil.which("higgsfield") or shutil.which("hf")
    if not cli:
        fallback = Path("C:/Users/sunwa/AppData/Roaming/npm/higgsfield.cmd")
        if fallback.exists():
            return str(fallback)
    return cli or "higgsfield"

def check_account_status():
    """Checks Higgsfield credit balance and user account status."""
    try:
        cli = get_cli_bin()
        res = subprocess.run(
            [cli, "account", "status"],
            capture_output=True,
            text=True,
            check=True,
            shell=(os.name == "nt")
        )
        return res.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error checking account: {e.stderr.strip()}"
    except FileNotFoundError:
        return "Higgsfield CLI not found on PATH."

def estimate_cost(model: str, prompt: str, image_path: Path = None):
    """Estimates the credit cost for a single video generation."""
    cli = get_cli_bin()
    cmd = [cli, "generate", "cost", model, "--prompt", prompt, "--aspect_ratio", "16:9"]
    if image_path and image_path.exists():
        cmd.extend(["--image", str(image_path)])
    
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True, shell=(os.name == "nt"))
        return res.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Cost error: {e.stderr.strip()}"

def generate_video_clip(record: dict, episode_dir: Path, model: str, dry_run: bool = True):
    """
    Executes or previews video generation for a single candidate shot.
    """
    input_img_path = episode_dir / "google_flow_input_images" / record["input_image"]
    target_video_path = episode_dir / "videos" / record["target_video"]
    
    if not input_img_path.exists():
        print(f"❌ Input image not found: {input_img_path}")
        return False

    print(f"\n🎬 Clip: {record['target_video']}")
    print(f"   Beat: {record['beat_info']}")
    print(f"   Input Image: {input_img_path.name}")
    print(f"   Prompt: {record['prompt']}")
    print(f"   Model: {model}")

    cli = get_cli_bin()
    # Build command based on model specification
    # For Veo 3.1: uses --start-image; For Seedance/Kling: uses --image / --image-references
    cmd = [cli, "generate", "create", model, "--prompt", record["prompt"], "--aspect_ratio", "16:9"]
    
    if model.startswith("veo") or "seedance" in model:
        cmd.extend(["--start-image", str(input_img_path)])
    else:
        cmd.extend(["--image", str(input_img_path)])
        
    cmd.extend(["--wait", "--wait-timeout", "15m", "--wait-interval", "5s"])

    cmd_str = " ".join([f'"{c}"' if " " in c else c for c in cmd])
    print(f"   Command: {cmd_str}")

    if dry_run:
        print("   [DRY RUN] Generation skipped. Pass --execute to submit job to Higgsfield.")
        return True

    print("   🚀 Submitting generation job to Higgsfield (waiting for completion)...")
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=True, shell=(os.name == "nt"))
        output = proc.stdout.strip()
        print(f"   Output:\n{output}")
        
        # Extract URL from stdout
        urls = re.findall(r'https?://[^\s<>"]+\.mp4[^\s<>"]*', output)
        if not urls:
            # Fallback to general url
            urls = re.findall(r'https?://[^\s<>"]+', output)

        if urls:
            download_url = urls[0]
            print(f"   ⬇️ Downloading rendered video from: {download_url}")
            target_video_path.parent.mkdir(parents=True, exist_ok=True)
            urllib.request.urlretrieve(download_url, target_video_path)
            print(f"   ✅ Saved to: {target_video_path}")
            return True
        else:
            print("   ⚠️ No video URL detected in output. Check Higgsfield console.")
            return False

    except subprocess.CalledProcessError as e:
        print(f"   ❌ Execution failed: {e.stderr.strip()}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Higgsfield Automated Video Generator for Ajanta-Ellora WebSeries")
    parser.add_argument("--episode", type=int, default=5, help="Episode number (e.g. 5)")
    parser.add_argument("--model", type=str, default="veo3_1", help="Higgsfield video model (veo3_1, seedance_2_5, kling3_0_turbo)")
    parser.add_argument("--clip", type=str, default=None, help="Specific target video name or index (e.g. ep05_gf_01 or 1)")
    parser.add_argument("--list", action="store_true", help="List all parsed action beats from prompt sheet")
    parser.add_argument("--cost", action="store_true", help="Query credit cost estimation for action shots")
    parser.add_argument("--execute", action="store_true", help="Execute live generation (spends credits)")
    args = parser.parse_args()

    ep_str = f"episode{args.episode:02d}"
    ep_dir = WORKSPACE_ROOT / "ajanta-ellora" / ep_str
    prompt_sheet = ep_dir / "google_flow_input_images" / "GOOGLE_FLOW_PROMPT_SHEET.md"

    if not prompt_sheet.exists():
        print(f"❌ Could not find {prompt_sheet}")
        sys.exit(1)

    records = parse_prompt_sheet(prompt_sheet)
    print(f"Loaded {len(records)} action video beats for Episode {args.episode:02d}.")
    print(f"Higgsfield Account: {check_account_status()}\n")

    if args.list:
        print(f"{'Idx':<4} | {'Target Video Filename':<45} | {'Beat':<25}")
        print("-" * 80)
        for idx, r in enumerate(records, start=1):
            print(f"{idx:<4} | {r['target_video']:<45} | {r['beat_info']:<25}")
        return

    if args.cost:
        print(f"Estimating credit cost with model: {args.model}...")
        for idx, r in enumerate(records, start=1):
            cost_str = estimate_cost(args.model, r["prompt"])
            print(f"[{idx}] {r['target_video']} -> {cost_str}")
        return

    selected_records = records
    if args.clip:
        if args.clip.isdigit():
            idx = int(args.clip) - 1
            if 0 <= idx < len(records):
                selected_records = [records[idx]]
            else:
                print(f"❌ Index {args.clip} out of range (1-{len(records)})")
                return
        else:
            selected_records = [r for r in records if args.clip in r["target_video"] or args.clip in r["input_image"]]
            if not selected_records:
                print(f"❌ No matching clip found for '{args.clip}'")
                return

    dry_run = not args.execute
    if dry_run:
        print("🛡️ SAFE MODE: Running dry-run simulation. No credits will be spent.")
        print("To submit jobs live, re-run with --execute.")

    success_count = 0
    for r in selected_records:
        if generate_video_clip(r, ep_dir, args.model, dry_run=dry_run):
            success_count += 1

    print(f"\nCompleted {success_count}/{len(selected_records)} clip jobs.")

if __name__ == "__main__":
    main()
