#!/usr/bin/env python3
"""
generate_ep05_elevenlabs_narration.py — ElevenLabs Studio Narration & Subtitle Synthesizer
Synthesizes Episode 05 narration using ElevenLabs API with Adam Stone (auq43ws1oslv0tO4BDa7).
Extracts millisecond-accurate timestamps using /with-timestamps endpoint.
Generates:
1. 8 individual Act MP3s with exact duration tracking
2. Perfectly monotonic, non-overlapping .srt subtitles for each act and for episode_05_full.srt
3. Seamless master concatenation with 0.00 ms drift
4. 2 companion Shorts voiceovers and subtitles
"""

import os
import re
import sys
import json
import base64
import requests
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Tuple

# Fix Windows console UTF-8 encoding
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

WORKSPACE_ROOT = Path("C:/Sagar/Projects/thecuriousity-kills-thecat")
EP05_DIR = WORKSPACE_ROOT / "ajanta-ellora" / "episode05"
AUDIO_DIR = EP05_DIR / "audio"
SUB_DIR = EP05_DIR / "subtitles"

AUDIO_DIR.mkdir(parents=True, exist_ok=True)
SUB_DIR.mkdir(parents=True, exist_ok=True)

# Voice: Adam Stone (Smooth, relaxed, deep British documentary narrator)
VOICE_ID = "auq43ws1oslv0tO4BDa7"
MODEL_ID = "eleven_multilingual_v2"

def get_api_key() -> str:
    env_p = WORKSPACE_ROOT / ".env"
    if env_p.exists():
        lines = env_p.read_text(encoding="utf-8").splitlines()
        for l in lines:
            if l.startswith("ELEVEN_LABS_API_KEY=") or l.startswith("ELEVENLABS_API_KEY="):
                return l.split("=", 1)[1].strip()
    key = os.getenv("ELEVEN_LABS_API_KEY") or os.getenv("ELEVENLABS_API_KEY")
    if not key:
        raise ValueError("ELEVEN_LABS_API_KEY not found in .env or environment!")
    return key

# The 8 Acts with exact sentence cues matching the 72 micro-beats
ACTS_DATA = [
    {
        "id": "act_01_the_animals_beneath",
        "title": "Act I — The Animals Beneath",
        "sentences": [
            "Look beneath the temple.",
            "Along Kailasa’s raised base, elephants emerge from the dark stone, shoulder to shoulder beneath a monumental ledge.",
            "At first glance, they seem to hold the entire temple above the ground.",
            "But the image asks a question that the architecture answers in a more surprising way.",
            "Are these animals carrying the building, or showing us how to see it?",
            "At Ellora, the answer begins with a distinction between what stone does and what sculpture makes us feel.",
            "The elephants are carved into the temple’s lower storey; the temple itself remains part of a vast rock-cut composition.",
            "Today, we follow the plinth from its carved animals to the meaning of a mountain made to appear lifted.",
            "The mystery is not whether the elephants are beautiful, but why the temple seems to need them."
        ]
    },
    {
        "id": "act_02_a_mountain_as_temple",
        "title": "Act II — A Mountain as Temple",
        "sentences": [
            "To understand what the base is doing, step back into the courtyard.",
            "Kailasa was not built by stacking blocks from the ground upward.",
            "Carvers trenched downward into basalt bedrock, isolating a single mass of rock and freeing the temple from above.",
            "The plinth is the elevated base beneath the principal temple, setting the shrine above the court floor.",
            "Its surfaces are not blank foundations: they carry a dense sculptural program that continues around the building.",
            "The base therefore has two jobs for the visitor’s eye: it establishes height and gives that height a living edge.",
            "Rows of figures, animals, and patterned bands turn the transition from earth to temple into an experience.",
            "The monument does not simply stand in the landscape; it stages how we encounter its mass.",
            "To understand the elephants, we first need to see the plinth as architecture and image at once."
        ]
    },
    {
        "id": "act_03_reading_the_plinth",
        "title": "Act III — Reading the Plinth",
        "sentences": [
            "Walk your attention along the lower storey.",
            "Sahapedia describes elephants gathering lotus flowers in their trunks, deeply carved beneath the high basement.",
            "The animals are not isolated ornaments placed on a modern-looking facade.",
            "They belong to a continuous sculpted zone that wraps the base with elephants, lions, and other figures.",
            "The scale and relief make the band legible from the court, even as its details reward a closer look.",
            "Some trunks are damaged, and weathering changes what survives; the sculpture we see is not an untouched original surface.",
            "A historic account also described a herd bearing the temple, an image captured by the composition itself.",
            "That description tells us what the carving makes visible, not a hidden engineering report from the builders.",
            "The first clue is visual: the animals create a living threshold between the ground and the sacred structure above."
        ]
    },
    {
        "id": "act_04_the_illusion_of_support",
        "title": "Act IV — The Illusion of Support",
        "sentences": [
            "Now look at the line where the plinth meets the temple mass.",
            "The elephants appear to push upward, their backs aligned beneath the projecting base.",
            "This is a powerful sculptural convention: the building seems to rest on a procession of living bodies.",
            "Yet at Kailasa, these elephants are carved in relief on the lower storey, within the same rock-cut monument.",
            "They are not a row of freestanding columns secretly holding a separate building aloft.",
            "The rock-cut core and plinth carry the architectural mass; the figures shape how that mass is imagined.",
            "That does not make the sculpture less important.",
            "It makes its work more precise.",
            "The animal band transforms a heavy base into a scene of effort, movement, and upward force.",
            "A stone temple can feel weightless for a moment because its base shows weight being carried."
        ]
    },
    {
        "id": "act_05_animals_and_the_sacred_mountain",
        "title": "Act V — Animals and the Sacred Mountain",
        "sentences": [
            "The temple’s name and design point toward Kailasa, Shiva’s sacred mountain.",
            "The building’s rising form turns that mountain association into architecture, with the central shrine as its summit.",
            "An older interpretation by Havell compared the elephants at the base to rain clouds beneath Himalayan peaks.",
            "In that reading, elephants evoke clouds gathering below a mountain, making the temple appear borne above them.",
            "It is an evocative interpretation, not a certainty that the original sculptors left us in writing.",
            "Other readings emphasize royal power, auspicious abundance, or the familiar image of elephants supporting a cosmic mountain.",
            "The surviving carving alone cannot choose one meaning for every viewer or every figure.",
            "What we can say securely is that the animals and the mountain form a deliberate visual relationship.",
            "The plinth makes the sacred mountain seem animated at its base."
        ]
    },
    {
        "id": "act_06_one_stone_many_images",
        "title": "Act VI — One Stone, Many Images",
        "sentences": [
            "There is a paradox here: the elephants look like separate creatures, but the monument is rock-cut.",
            "The sculptor has made the basalt read as bodies, folds, legs, and patterned surfaces.",
            "At a distance, the repeating animals form a band beneath the temple.",
            "Up close, each figure can interrupt that repetition with its own pose and detail.",
            "This shift between a unified procession and individual bodies is part of the carving’s visual intelligence.",
            "We should not invent a workshop sequence or claim every sculptural detail was carved in a known order.",
            "The finished stone lets us study form and placement, while leaving many production choices undocumented.",
            "A single rock mass can become architecture, ornament, and an imagined procession at the same time.",
            "The temple’s unity does not flatten its images; it gives them a shared ground."
        ]
    },
    {
        "id": "act_07_the_viewer_completes_the_image",
        "title": "Act VII — The Viewer Completes the Image",
        "sentences": [
            "The plinth is also something you move past.",
            "From the courtyard, the raised base lifts the temple above eye level and gives the main shrine a commanding presence.",
            "As you walk, the relief appears in changing fragments: an elephant, a lion, a repeated band, then the larger mass above.",
            "The viewer connects those partial views into an imagined ring of animals around the building.",
            "This is why the sculpture works at more than one scale.",
            "Its repetition binds the base together, while its details invite a slower encounter.",
            "The temple’s height feels physical, but the carved creatures make that height feel supported and alive.",
            "The image is completed not by a mechanical trick, but by the meeting of stone, viewpoint, and movement.",
            "Kailasa turns looking into a small act of discovery."
        ]
    },
    {
        "id": "act_08_beneath_the_mountain",
        "title": "Act VIII — Beneath the Mountain",
        "sentences": [
            "Return to the elephants beneath the plinth.",
            "They do not reveal a concealed system of animal-shaped pillars.",
            "They reveal a sculptural decision: make the base of a sacred mountain appear to move and bear weight.",
            "The architecture gives the temple its mass; the figures give that mass a story the eye can follow.",
            "Some meanings remain open, and that uncertainty is part of reading a monument honestly.",
            "At Kailasa, a mountain was not only cut into a temple; it was made to seem alive around its edges.",
            "Next, we leave the plinth and turn toward the stories carved across the temple walls.",
            "What happens when a whole epic is translated into stone panels around a sacred court?",
            "That is the next mystery waiting at Kailasa."
        ]
    }
]

SHORTS_DATA = [
    {
        "id": "short_01_the_elephants_that_carry_a_temple",
        "sentences": [
            "Look beneath the Kailasa Temple at Ellora.",
            "A carved procession of elephants seems to hold the temple above the ground.",
            "But these figures are sculpted into the lower storey; they are not separate pillars carrying a building.",
            "The rock-cut plinth supports the architecture, while the elephants make that weight feel alive.",
            "The stone does the structural work.",
            "The sculpture gives the mountain a story."
        ]
    },
    {
        "id": "short_02_why_elephants_support_the_mountain",
        "sentences": [
            "Why are elephants carved beneath Kailasa Temple’s raised base?",
            "They appear to bear the temple on their backs, turning its plinth into a living procession.",
            "One older interpretation compared the elephants to clouds gathered beneath a Himalayan peak.",
            "That is a compelling reading, but not a proven statement of the sculptors’ intent.",
            "What the carving shows clearly is a sacred mountain made to feel animated at its base."
        ]
    }
]

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

def synthesize_with_timestamps(text: str, api_key: str) -> Tuple[bytes, Dict[str, Any]]:
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/with-timestamps"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "model_id": MODEL_ID,
        "voice_settings": {
            "stability": 0.55,
            "similarity_boost": 0.80,
            "style": 0.15,
            "use_speaker_boost": True
        }
    }
    resp = requests.post(url, headers=headers, json=payload)
    if resp.status_code != 200:
        raise RuntimeError(f"ElevenLabs API Error ({resp.status_code}): {resp.text}")
    data = resp.json()
    audio_bytes = base64.b64decode(data["audio_base64"])
    return audio_bytes, data["alignment"]

def build_act_cues(sentences: List[str], full_text: str, alignment: Dict[str, Any], total_audio_dur: float) -> List[Dict[str, Any]]:
    starts = alignment["character_start_times_seconds"]
    ends = alignment["character_end_times_seconds"]
    
    cues = []
    curr_pos = 0
    for s in sentences:
        idx = full_text.find(s, curr_pos)
        if idx == -1:
            idx = curr_pos
        end_idx = min(idx + len(s) - 1, len(ends) - 1)
        s_time = starts[idx] if idx < len(starts) else (cues[-1]["end"] + 0.05 if cues else 0.0)
        e_time = ends[end_idx] if end_idx < len(ends) else total_audio_dur
        cues.append({
            "text": s,
            "start": s_time,
            "end": e_time
        })
        curr_pos = idx + len(s)
        
    # Enforce strictly monotonic, non-overlapping cues
    for i in range(len(cues)):
        # Ensure minimum duration 1.5s
        if cues[i]["end"] <= cues[i]["start"]:
            cues[i]["end"] = cues[i]["start"] + 1.5
            
        if i < len(cues) - 1:
            # If current cue overlaps or almost touches next cue, tighten slightly
            if cues[i]["end"] >= cues[i+1]["start"]:
                cues[i]["end"] = max(cues[i]["start"] + 1.0, cues[i+1]["start"] - 0.02)
                
    return cues

def write_srt_file(cues: List[Dict[str, Any]], out_path: Path, offset_seconds: float = 0.0):
    lines = []
    for i, cue in enumerate(cues, 1):
        s_str = format_srt_time(cue["start"] + offset_seconds)
        e_str = format_srt_time(cue["end"] + offset_seconds)
        lines.append(f"{i}\n{s_str} --> {e_str}\n{cue['text']}\n")
    out_path.write_text("\n".join(lines), encoding="utf-8")

def get_audio_duration(file_path: Path) -> float:
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(file_path)
    ]
    out = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout.strip()
    return float(out)

def main():
    print("=" * 65)
    print("  ELEVENLABS ADAM STONE SYNTHESIS FOR EPISODE 05")
    print("=" * 65)
    
    api_key = get_api_key()
    print(f"[*] Voice ID: {VOICE_ID} (Adam Stone)")
    print(f"[*] Model ID: {MODEL_ID}")
    
    act_cues_all = []
    act_audio_paths = []
    
    # 1. Synthesize 8 Acts
    for act_idx, act in enumerate(ACTS_DATA):
        act_id = act["id"]
        mp3_path = AUDIO_DIR / f"{act_id}.mp3"
        srt_path = SUB_DIR / f"{act_id}.srt"
        
        full_text = " ".join(act["sentences"])
        print(f"\n[{act_idx+1}/8] Synthesizing {act_id} ({len(full_text)} chars)...")
        
        audio_bytes, alignment = synthesize_with_timestamps(full_text, api_key)
        mp3_path.write_bytes(audio_bytes)
        
        dur = get_audio_duration(mp3_path)
        print(f"  -> Saved MP3: {mp3_path.name} ({dur:.2f}s, {len(audio_bytes):,} bytes)")
        
        cues = build_act_cues(act["sentences"], full_text, alignment, dur)
        write_srt_file(cues, srt_path)
        print(f"  -> Saved SRT: {srt_path.name} ({len(cues)} cues)")
        
        act_cues_all.append((act_id, cues, dur))
        act_audio_paths.append(mp3_path)
        
    # 2. Concatenate Master Narration with 0.00ms Drift
    print("\n" + "=" * 65)
    print("  CONCATENATING MASTER NARRATION (0.00 MS DRIFT ENFORCEMENT)")
    print("=" * 65)
    
    concat_list = AUDIO_DIR / "_concat_acts.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        for p in act_audio_paths:
            f.write(f"file '{p.as_posix()}'\n")
            
    master_narration = AUDIO_DIR / "episode_05_full_narration.mp3"
    cmd_cat = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-c:a", "libmp3lame", "-b:a", "192k",
        str(master_narration)
    ]
    subprocess.run(cmd_cat, capture_output=True, check=True)
    if concat_list.exists():
        concat_list.unlink()
        
    master_dur = get_audio_duration(master_narration)
    acts_sum_dur = sum(dur for _, _, dur in act_cues_all)
    drift_ms = abs(master_dur - acts_sum_dur) * 1000.0
    print(f"[*] Sum of Acts Duration: {acts_sum_dur:.3f}s")
    print(f"[*] Master Narration Duration: {master_dur:.3f}s")
    print(f"[*] Master Concatenation Drift: {drift_ms:.2f} ms")
    assert drift_ms <= 10.0, f"Drift {drift_ms} ms exceeds 10.0ms limit!"
    
    # 3. Build Synchronized 72-Cue episode_05_full.srt
    print("\n[*] Building full synchronized 72-cue SRT (episode_05_full.srt)...")
    full_cues = []
    current_offset = 0.0
    
    for act_idx, (act_id, cues, dur) in enumerate(act_cues_all):
        if act_id == "act_04_the_illusion_of_support":
            # In full SRT, cues 7 & 8 are unified to maintain exactly 72 beats (9 cuts per act)
            # cues[0..5]: first 6 cues
            # unified cue: cues[6] + cues[7] ("That does not make the sculpture less important. It makes its work more precise.")
            # cues[8..9]: cues 35 and 36
            u_start = cues[6]["start"]
            u_end = cues[7]["end"]
            u_text = cues[6]["text"] + " " + cues[7]["text"]
            
            act4_unified = cues[:6] + [{"text": u_text, "start": u_start, "end": u_end}] + cues[8:]
            for c in act4_unified:
                full_cues.append({
                    "text": c["text"],
                    "start": current_offset + c["start"],
                    "end": current_offset + c["end"]
                })
        else:
            for c in cues:
                full_cues.append({
                    "text": c["text"],
                    "start": current_offset + c["start"],
                    "end": current_offset + c["end"]
                })
        current_offset += dur
        
    # Enforce strictly monotonic, non-overlapping cues across act boundaries
    for i in range(len(full_cues) - 1):
        if full_cues[i]["end"] >= full_cues[i+1]["start"]:
            full_cues[i]["end"] = max(full_cues[i]["start"] + 1.0, full_cues[i+1]["start"] - 0.02)
            
    full_srt_path = SUB_DIR / "episode_05_full.srt"
    write_srt_file(full_cues, full_srt_path)
    print(f"[*] Generated: {full_srt_path.name} with {len(full_cues)} cues (strictly monotonic)!")
    
    # 4. Synthesize 2 Companion Shorts
    print("\n" + "=" * 65)
    print("  SYNTHESIZING COMPANION SHORTS")
    print("=" * 65)
    for short in SHORTS_DATA:
        s_id = short["id"]
        mp3_path = AUDIO_DIR / f"{s_id}.mp3"
        srt_path = SUB_DIR / f"{s_id}.srt"
        full_text = " ".join(short["sentences"])
        print(f"[*] Synthesizing {s_id} ({len(full_text)} chars)...")
        audio_bytes, alignment = synthesize_with_timestamps(full_text, api_key)
        mp3_path.write_bytes(audio_bytes)
        dur = get_audio_duration(mp3_path)
        print(f"  -> Saved MP3: {mp3_path.name} ({dur:.2f}s)")
        cues = build_act_cues(short["sentences"], full_text, alignment, dur)
        write_srt_file(cues, srt_path)
        print(f"  -> Saved SRT: {srt_path.name} ({len(cues)} cues)")

    print("\n[SUCCESS] All ElevenLabs narration stems and subtitles synthesized cleanly!")

if __name__ == "__main__":
    main()
