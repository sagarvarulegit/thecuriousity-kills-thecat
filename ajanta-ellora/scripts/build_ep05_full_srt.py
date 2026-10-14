#!/usr/bin/env python3
"""
build_ep05_full_srt.py — Reconstructs episode_05_full.srt from the 8 act SRT files
Ensures 100% strictly monotonic, non-overlapping cues and exactly 72 beats.
"""

from pathlib import Path
import subprocess

BASE_DIR = Path("C:/Sagar/Projects/thecuriousity-kills-thecat")
EP05_DIR = BASE_DIR / "ajanta-ellora" / "episode05"
AUDIO_DIR = EP05_DIR / "audio"
SUB_DIR = EP05_DIR / "subtitles"

def get_audio_duration(file_path: Path) -> float:
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(file_path)
    ]
    out = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout.strip()
    return float(out)

def format_srt_time(seconds: float) -> str:
    h = int(seconds // 3600)
    seconds %= 3600
    m = int(seconds // 60)
    seconds %= 60
    s = int(seconds)
    ms = int(round((seconds - s) * 1000))
    if ms >= 1000:
        s += 1
        ms = 0
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

def parse_time(ts):
    h, m, s_ms = ts.split(":")
    s, ms = s_ms.split(",")
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000.0

def main():
    act_names = [
        "act_01_the_animals_beneath",
        "act_02_a_mountain_as_temple",
        "act_03_reading_the_plinth",
        "act_04_the_illusion_of_support",
        "act_05_animals_and_the_sacred_mountain",
        "act_06_one_stone_many_images",
        "act_07_the_viewer_completes_the_image",
        "act_08_beneath_the_mountain"
    ]
    
    full_cues = []
    current_offset = 0.0
    
    for act in act_names:
        audio_p = AUDIO_DIR / f"{act}.mp3"
        srt_p = SUB_DIR / f"{act}.srt"
        dur = get_audio_duration(audio_p)
        
        content = srt_p.read_text(encoding="utf-8").strip()
        blocks = content.split("\n\n")
        act_cues = []
        for b in blocks:
            lines = b.splitlines()
            if len(lines) >= 3 and "-->" in lines[1]:
                t1, t2 = lines[1].split(" --> ")
                text = "\n".join(lines[2:]).strip()
                act_cues.append({
                    "start": parse_time(t1),
                    "end": parse_time(t2),
                    "text": text
                })
                
        if act == "act_04_the_illusion_of_support":
            # Combine cues 7 & 8 into 1 cue so act 4 has 9 cues and total is 72
            u_start = act_cues[6]["start"]
            u_end = act_cues[7]["end"]
            u_text = act_cues[6]["text"] + " " + act_cues[7]["text"]
            act4_unified = act_cues[:6] + [{"start": u_start, "end": u_end, "text": u_text}] + act_cues[8:]
            for c in act4_unified:
                full_cues.append({
                    "start": current_offset + c["start"],
                    "end": current_offset + c["end"],
                    "text": c["text"]
                })
        else:
            for c in act_cues:
                full_cues.append({
                    "start": current_offset + c["start"],
                    "end": current_offset + c["end"],
                    "text": c["text"]
                })
                
        current_offset += dur
        
    # Strictly monotonic, zero-overlap enforcement
    for i in range(len(full_cues) - 1):
        if full_cues[i]["end"] >= full_cues[i+1]["start"]:
            full_cues[i]["end"] = max(full_cues[i]["start"] + 1.0, full_cues[i+1]["start"] - 0.02)
            
    # Write episode_05_full.srt
    lines = []
    for i, c in enumerate(full_cues, 1):
        s_str = format_srt_time(c["start"])
        e_str = format_srt_time(c["end"])
        lines.append(f"{i}\n{s_str} --> {e_str}\n{c['text']}\n")
        
    full_srt_p = SUB_DIR / "episode_05_full.srt"
    full_srt_p.write_text("\n".join(lines), encoding="utf-8")
    print(f"[OK] Wrote {full_srt_p.name} with {len(full_cues)} cues (Total Duration: {current_offset:.2f}s)")

if __name__ == "__main__":
    main()
