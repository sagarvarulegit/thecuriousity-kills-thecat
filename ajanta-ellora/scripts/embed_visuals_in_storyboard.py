#!/usr/bin/env python3
"""
embed_visuals_in_storyboard.py — Embeds all 62 corresponding image stills directly into the script & storyboard.
Channel: thecuriousity-kills-thecat
"""

import sys
import re
from pathlib import Path

# Add scripts directory
WORKSPACE_ROOT = Path("C:/Sagar/Projects/thecuriousity-kills-thecat")
sys.path.append(str(WORKSPACE_ROOT / "ajanta-ellora" / "scripts"))
import assemble_episode_08_full as a

manifest = a.get_manifest()

md_path = WORKSPACE_ROOT / "ajanta-ellora" / "episode08" / "script_and_storyboard" / "episode-08-the-silk-road-blue-and-mud-chemistry.md"
lines = md_path.read_text(encoding="utf-8").splitlines()

new_lines = []
cut_idx = 0

for line in lines:
    match = re.match(r'^(\d+)\.\s+(.*)', line.strip())
    # Only match lines 1 to 62 from the 5 acts (not Part 3)
    if match and cut_idx < 62:
        num = int(match.group(1))
        sentence = match.group(2)
        media_type, filename, motion = manifest[cut_idx]
        
        # Determine classification badge
        if "GENERATE_VIDEO" in filename or "ep08_gf_" in filename:
            badge = "🎬 **Google Flow Action Video Candidate Still**"
        elif "infographic" in filename:
            badge = "📊 **Structural Engineering Diagram**"
        elif "museum_scan" in filename or "archive" in filename:
            badge = "🏛️ **Authentic Museum Scan / Historical Archive**"
        else:
            badge = "🖼️ **Hero Still (4K Zoompan)**"
            
        new_lines.append(f"{num}. **{sentence}**")
        new_lines.append("")
        new_lines.append(f"   <div class=\"storyboard-card\" style=\"background:#131b2e; border:1px solid #2a3754; border-radius:8px; padding:12px; margin:10px 0 16px 0; max-width:760px;\">")
        new_lines.append(f"     <img src=\"../images/{filename}\" alt=\"{filename}\" style=\"width:100%; border-radius:6px; aspect-ratio:16/9; object-fit:cover; display:block; border:1px solid #1e293b;\" />")
        new_lines.append(f"     <div style=\"font-size:0.82rem; color:#94a3b8; font-family:monospace; margin-top:8px;\">{badge}: <code>{filename}</code> | Motion: <em>{motion}</em></div>")
        new_lines.append(f"   </div>")
        new_lines.append("")
        cut_idx += 1
    else:
        new_lines.append(line)

md_path.write_text("\n".join(new_lines), encoding="utf-8")
print(f"[OK] Successfully embedded visual stills for {cut_idx} cuts into {md_path.name}")
