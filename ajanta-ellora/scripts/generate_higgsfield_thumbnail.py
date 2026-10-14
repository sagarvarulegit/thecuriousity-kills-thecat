#!/usr/bin/env python3
"""
generate_higgsfield_thumbnail.py — High-CTR YouTube & Shorts Thumbnail Engine via Higgsfield

Generates:
1. Master 16:9 YouTube Thumbnail (1920x1080)
2. Companion Shorts 9:16 Vertical Thumbnails (1080x1920)

Enforces:
- Model default: nano_banana_pro (2 credits per thumbnail)
- Mobile 3-Word Rule typography hooks
- Strict < 2.0 MB file size limit (YouTube metadata ceiling)
- Safe dry-run mode by default
"""

import os
import sys
import argparse
import subprocess
import re
import urllib.request
import shutil
from pathlib import Path
from PIL import Image

# Fix Windows console UTF-8 encoding
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

WORKSPACE_ROOT = Path("C:/Sagar/Projects/thecuriousity-kills-thecat")

EPISODE_THUMBNAIL_CONFIGS = {
    5: {
        "master_16x9": {
            "title": "CARRIED BY ELEPHANTS?",
            "prompt": "Extreme cinematic close-up of a monumental stone elephant sculpted into dark volcanic basalt rock, dramatic warm golden sunrise rim light, intricate stone wrinkles and chisel textures, background of colossal monolithic temple carved from cliff, deep shadows, 8k resolution, viral YouTube documentary thumbnail aesthetic, ultra sharp focus.",
            "aspect_ratio": "16:9",
            "filename": "ep05_master_thumbnail_16x9_higgsfield.jpg"
        },
        "short_01_9x16": {
            "title": "LIFTED BY ELEPHANTS?",
            "prompt": "Vertical 9:16 cinematic shot, low-angle looking up at a row of colossal carved stone elephants supporting the massive monolithic temple plinth of Kailasa, dramatic golden light cutting through mist, epic scale, viral YouTube shorts cover composition.",
            "aspect_ratio": "9:16",
            "filename": "short_01_thumbnail_9x16_higgsfield.jpg"
        },
        "short_02_9x16": {
            "title": "WHY ELEPHANTS BENEATH?",
            "prompt": "Vertical 9:16 macro shot of a weathered stone elephant head emerging directly out of solid rock, ancient chisel marks on volcanic basalt, mystical ambient glow, atmospheric haze, viral YouTube shorts thumbnail framing.",
            "aspect_ratio": "9:16",
            "filename": "short_02_thumbnail_9x16_higgsfield.jpg"
        }
    }
}

def get_cli_bin():
    cli = shutil.which("higgsfield") or shutil.which("hf")
    if not cli:
        fallback = Path("C:/Users/sunwa/AppData/Roaming/npm/higgsfield.cmd")
        if fallback.exists():
            return str(fallback)
    return cli or "higgsfield"

def optimize_thumbnail(image_path: Path, max_bytes: int = 2_000_000):
    """Ensures thumbnail is compressed under the 2.0MB YouTube ceiling."""
    if not image_path.exists():
        return
    
    file_size = image_path.stat().st_size
    if file_size <= max_bytes:
        print(f"   📊 File size: {file_size / (1024*1024):.2f} MB (within <2.0MB ceiling)")
        return

    print(f"   ⚠️ File size {file_size / (1024*1024):.2f} MB exceeds 2.0MB. Compressing...")
    img = Image.open(image_path).convert("RGB")
    quality = 90
    while quality > 40:
        img.save(image_path, "JPEG", quality=quality, optimize=True)
        new_size = image_path.stat().st_size
        if new_size <= max_bytes:
            print(f"   ✅ Compressed to: {new_size / (1024*1024):.2f} MB (quality={quality})")
            return
        quality -= 5

def generate_thumbnail(config: dict, output_dir: Path, model: str = "nano_banana_pro", dry_run: bool = True):
    target_path = output_dir / config["filename"]
    print(f"\n🖼️ Thumbnail: {config['filename']} ({config['aspect_ratio']})")
    print(f"   Hook: \"{config['title']}\"")
    print(f"   Prompt: {config['prompt']}")
    print(f"   Model: {model}")

    cli = get_cli_bin()
    cmd = [
        cli, "generate", "create", model,
        "--prompt", config["prompt"],
        "--aspect_ratio", config["aspect_ratio"],
        "--wait", "--wait-timeout", "10m"
    ]

    cmd_str = " ".join([f'"{c}"' if " " in c else c for c in cmd])
    print(f"   Command: {cmd_str}")

    if dry_run:
        print("   [DRY RUN] Skipped. Pass --execute to submit job to Higgsfield (estimated 2 credits).")
        return True

    print("   🚀 Submitting generation job to Higgsfield...")
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=True, shell=(os.name == "nt"))
        output = proc.stdout.strip()
        print(f"   Output:\n{output}")
        
        urls = re.findall(r'https?://[^\s<>"]+\.(?:jpg|jpeg|png)[^\s<>"]*', output, re.IGNORECASE)
        if not urls:
            urls = re.findall(r'https?://[^\s<>"]+', output)

        if urls:
            download_url = urls[0]
            print(f"   ⬇️ Downloading thumbnail from: {download_url}")
            output_dir.mkdir(parents=True, exist_ok=True)
            urllib.request.urlretrieve(download_url, target_path)
            optimize_thumbnail(target_path)
            print(f"   ✅ Saved to: {target_path}")
            return True
        else:
            print("   ⚠️ No image URL detected in output.")
            return False

    except subprocess.CalledProcessError as e:
        print(f"   ❌ Execution failed: {e.stderr.strip()}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Higgsfield Thumbnail Engine for Ajanta-Ellora WebSeries")
    parser.add_argument("--episode", type=int, default=5, help="Episode number (e.g. 5)")
    parser.add_argument("--type", type=str, choices=["master", "short1", "short2", "all"], default="all", help="Thumbnail variant to generate")
    parser.add_argument("--model", type=str, default="nano_banana_pro", help="Higgsfield image model")
    parser.add_argument("--execute", action="store_true", help="Execute live generation (spends credits)")
    args = parser.parse_args()

    if args.episode not in EPISODE_THUMBNAIL_CONFIGS:
        print(f"❌ No configuration found for Episode {args.episode}")
        return

    ep_config = EPISODE_THUMBNAIL_CONFIGS[args.episode]
    ep_str = f"episode{args.episode:02d}"
    out_dir = WORKSPACE_ROOT / "ajanta-ellora" / ep_str / "thumbnail"

    print(f"Higgsfield Thumbnail Engine — Episode {args.episode:02d}")
    dry_run = not args.execute
    if dry_run:
        print("🛡️ SAFE MODE: Running dry-run simulation. No credits will be spent.")
        print("To submit jobs live, re-run with --execute.")

    targets = []
    if args.type == "master" or args.type == "all":
        targets.append(ep_config["master_16x9"])
    if args.type == "short1" or args.type == "all":
        targets.append(ep_config["short_01_9x16"])
    if args.type == "short2" or args.type == "all":
        targets.append(ep_config["short_02_9x16"])

    success_count = 0
    for cfg in targets:
        if generate_thumbnail(cfg, out_dir, model=args.model, dry_run=dry_run):
            success_count += 1

    print(f"\nProcessed {success_count}/{len(targets)} thumbnail tasks.")

if __name__ == "__main__":
    main()
