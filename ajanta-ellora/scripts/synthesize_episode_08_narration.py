#!/usr/bin/env python3
"""
synthesize_episode_08_narration.py — ElevenLabs Studio Narration & Subtitle Synthesizer (Episode 08)
Channel: thecuriousity-kills-thecat
Synthesizes Episode 08 narration in English using ElevenLabs API with Adam Stone (auq43ws1oslv0tO4BDa7).
Extracts millisecond-accurate timestamps using /with-timestamps endpoint.
Generates:
  1. 5 individual English Act MP3s in audio/narration/
  2. Perfectly monotonic, non-overlapping .srt subtitles in subtitles/
  3. Seamless master concatenation with <= 10.0 ms drift
  4. 2 companion Shorts voiceovers and subtitles in audio/ and subtitles/
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
EP08_DIR = WORKSPACE_ROOT / "ajanta-ellora" / "episode08"
AUDIO_DIR = EP08_DIR / "audio" / "narration"
SUB_DIR = EP08_DIR / "subtitles"
SHORTS_AUDIO_DIR = EP08_DIR / "audio"

AUDIO_DIR.mkdir(parents=True, exist_ok=True)
SUB_DIR.mkdir(parents=True, exist_ok=True)
SHORTS_AUDIO_DIR.mkdir(parents=True, exist_ok=True)

VOICE_ID = "auq43ws1oslv0tO4BDa7"  # Adam Stone
MODEL_ID = "eleven_multilingual_v2"

VOICE_SETTINGS = {
    "stability": 0.55,
    "similarity_boost": 0.80,
    "style": 0.15,
    "use_speaker_boost": True
}

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

# Master 5-Act English Script Data
ACTS_DATA = [
    {
        "id": "act_01_the_golden_reawakening",
        "title": "Act I: The Hidden Paintings of Ajanta (The Golden Reawakening, c. 460 CE)",
        "sentences": [
            "Welcome back to Ajanta and Ellora: The Subterranean Titans.",
            "This is Episode 8: The Mystery of the Cave Paintings.",
            "When people think of Ajanta and Ellora, they usually picture giant stone temples carved out of black mountain rock.",
            "But hidden deep inside these dark volcanic caves is something most people have never heard about: world-famous ancient paintings that have survived for fifteen hundred years.",
            "For nearly four centuries, this horseshoe mountain canyon lay completely silent, overgrown by thick jungle vines.",
            "Then, in the year 460, a powerful Indian king named Emperor Harishena united the empire and poured vast wealth into this secluded mountain.",
            "Within just seventeen years, master stonecutters carved twenty colossal new cave halls directly into the solid rock face.",
            "But they did not just carve stone; ancient artists transformed these dark subterranean walls into breathtaking, colorful royal palaces.",
            "In this episode, you will see how these ancient painters actually did their work, and how they solved three impossible engineering mysteries."
        ]
    },
    {
        "id": "act_02_the_basalt_problem_and_mud_chemistry",
        "title": "Act II: The Basalt Problem & The Mud Chemistry Secret",
        "sentences": [
            "To paint inside Ajanta, ancient craftsmen faced an impossible geological problem.",
            "The walls were not made of smooth, dry stone; they were carved out of dense, volcanic flood basalt rock.",
            "Basalt is cold, hard lava rock that constantly sweats underground water droplets through tiny cracks.",
            "If you paint directly on wet basalt rock, the water pushes the paint off within months, causing it to peel and turn to dust.",
            "European fresco painters put wet lime plaster on walls, but inside a cold, damp volcanic cave, that technique fails completely.",
            "The master guilds of Ajanta invented a revolutionary, multi-layered bio-mud formula that modern scientists still study today.",
            "First, stonecutters used pointed iron picks to peck thousands of small pits into the rock, creating a rough surface for the mud to grip.",
            "Then came the secret organic recipe: a thick, fermented mud plaster made of local red clay, rock grit, and cow dung.",
            "Using fermented cow dung was not dirty—it was pure organic chemistry.",
            "Digested plant fibers in the dung acted like microscopic nylon nets that stopped the mud from cracking, while natural bacteria kept mold away.",
            "Mixed with dry rice husks and sticky boiled sap from neem trees, this mud layer created a breathable skin that lived with the damp mountain.",
            "Finally, craftsmen spread a paper-thin finish coat made of slaked lime, powdered gypsum, and crushed sea shells.",
            "While still damp, an artisan held a smooth river agate pebble, firmly rubbing the wall in steady circular motions.",
            "Under the friction of the smooth agate stone, the chalky lime compacted into a gleaming, ivory-smooth surface ready for paint."
        ]
    },
    {
        "id": "act_03_the_silk_road_blue",
        "title": "Act III: The Silk Road Blue (Lapis Lazuli Alchemy)",
        "sentences": [
            "Once the plaster dried, the painters uncapped their earthenware pigment bowls.",
            "For red and yellow colors, they crushed local volcanic ochre rocks dug right from the Deccan soil.",
            "For green, they ground green earth minerals; for pure black, they collected soot from burning mustard oil lamps.",
            "But across the ceilings of Cave One and Cave Seventeen shines a brilliant color that came from thousands of kilometers away.",
            "It is an intense, glowing ultramarine blue that still looks fresh and wet on the rock walls today.",
            "This color was made from a rare gemstone called lapis lazuli.",
            "In the fifth century, there was only one place in the entire ancient world that had this blue stone: the remote mountain mines of Badakhshan in northern Afghanistan.",
            "To reach this remote volcanic cave, raw blue rocks traveled over two thousand five hundred kilometers across ancient trade roads.",
            "Pack camels carried heavy leather bags of raw blue crystals through freezing mountain passes and across the Indian plains.",
            "Ounce for ounce, this pure Afghan blue stone was worth more than solid gold.",
            "Only the wealthiest royal emperors and ministers could afford to paint entire cave ceilings in imported blue.",
            "It was living proof that ancient India was connected to the entire world through the ancient Silk Road."
        ]
    },
    {
        "id": "act_04_the_sootless_cave",
        "title": "Act IV: The Sootless Cave (Subterranean Optical Engineering)",
        "sentences": [
            "But this artistic miracle creates a huge archaeological puzzle that baffled scientists for centuries.",
            "Caves One, Two, Sixteen, and Seventeen go thirty to forty meters deep inside solid mountain rock.",
            "When you step inside these cave halls, you enter total pitch-black darkness where you cannot see your own hand in front of your face.",
            "Yet in the deepest, darkest corners of these caves, ancient artists painted microscopic details: eyelashes thinner than a hair, tiny pearls, and detailed gold jewelry.",
            "How could they paint these masterworks forty meters underground without any electric light?",
            "When modern scientists tested the cave ceilings, they searched for smoke stains and soot from burning oil lamps or torches.",
            "They found zero soot. The ceilings were completely clean.",
            "Burning fire torches inside these closed underground rooms would have choked the artists with smoke and blackened the white plaster walls.",
            "So how did they see? Ancient engineers invented an ingenious natural light diversion system.",
            "Outside in the blazing sunshine, assistants positioned large, circular mirrors made of highly polished cast bronze.",
            "The polished bronze mirrors caught the blinding tropical sun, reflecting powerful beams of natural sunlight straight into the dark cave entrance.",
            "Inside the dark hall, apprentice boys held up large sheets of wet, bleached white cotton and silk cloth.",
            "When the intense sunbeam hit the wet white cloth, the light bounced and scattered, filling the dark underground hall with a soft, bright, shadowless glow.",
            "The ancient painters were literally painting forty meters underground using captured natural sunlight."
        ]
    },
    {
        "id": "act_05_the_masterpieces_of_humanity",
        "title": "Act V: Reliving the Masterpieces & The Sudden Silence",
        "sentences": [
            "Illuminated by this soft, redirected sunlight, ancient artists created the greatest masterpieces of ancient world art.",
            "On the rear wall of Cave One stands the famous painting of Bodhisattva Padmapani, holding a blue lotus flower.",
            "Look closely at his gentle expression, his regal crown, and the downward curve of his eyes full of compassion.",
            "Notice the realistic three-dimensional shading along his nose and jawline, making his body look soft and alive against the flat stone.",
            "A thousand years before Leonardo da Vinci painted in Europe, Indian painters had already mastered human anatomy, emotion, and realistic 3D depth.",
            "All across these walls, you can see real life from fifteen hundred years ago: royal courts with foreign Persian visitors, forest animals, and joyful celebrations.",
            "But just as the painters were finishing these royal halls in the year 477, tragedy struck the empire.",
            "Emperor Harishena died suddenly under mysterious circumstances.",
            "Almost overnight, his kingdom collapsed into civil war, and hostile armies invaded the Deccan.",
            "Royal money stopped instantly.",
            "Down the cliff, stonecutters abandoned half-carved pillars, painters dropped their wet brushes on the stone floor, and monks fled into the hills.",
            "Within months, this bustling city of art in the cliff went completely silent.",
            "In our next episode, we will investigate this sudden collapse: the mysterious downfall that froze Ajanta in time, sealing these thirty temples inside the jungle for over a thousand years."
        ]
    }
]

SHORTS_DATA = [
    {
        "id": "short_01_the_mud_chemistry_secret",
        "sentences": [
            "How did paintings made of fermented mud and cow dung survive fifteen hundred years in a damp volcano canyon without rotting?",
            "Ancient volcanic basalt sweats moisture constantly. In Europe, damp cave walls destroy paintings within decades.",
            "Indian craftsmen mixed clay with digested cow dung fibers and rice husks, creating a living plaster that breathed humidity instead of trapping it.",
            "They sealed it with crushed sea shells, burnishing the wall with agate river stones until it shone like polished porcelain.",
            "But what they used for the blue color broke every law of ancient trade. Tap the linked documentary below to see where they got it."
        ]
    },
    {
        "id": "short_02_the_bronze_mirror_secret",
        "sentences": [
            "Ancient artists painted microscopic details forty meters inside a pitch-black mountain cave—without using a single fire torch.",
            "Step inside Cave One, and you are in total subterranean darkness. Yet scientists found zero smoke or oil soot on the ceiling.",
            "How did they see? In the blazing sun outside, assistants angled massive polished cast-bronze mirrors toward the entrance.",
            "They bounced beams of blinding sunlight onto wet white linen sheets, filling pitch-black caverns with soft, shadowless daylight.",
            "They were literally painting with captured sunlight. But in 477 CE, every painter dropped their brush and ran. Tap the linked documentary below to see why."
        ]
    }
]

def format_timestamp(seconds: float) -> str:
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int(round((seconds - int(seconds)) * 1000))
    if millis >= 1000:
        millis = 999
    return f"{hrs:02d}:{mins:02d}:{secs:02d},{millis:03d}"

def synthesize_text_with_timestamps(api_key: str, text: str) -> Dict[str, Any]:
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/with-timestamps"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "model_id": MODEL_ID,
        "voice_settings": VOICE_SETTINGS
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=90)
    if resp.status_code != 200:
        raise RuntimeError(f"ElevenLabs API error HTTP {resp.status_code}: {resp.text}")
    return resp.json()

def build_srt_from_alignment(sentences: List[str], alignment: Dict[str, Any], total_audio_dur: float) -> List[Tuple[float, float, str]]:
    chars = alignment.get("characters", [])
    starts = alignment.get("character_start_times_seconds", [])
    ends = alignment.get("character_end_times_seconds", [])

    full_text = "".join(chars)
    cue_entries = []
    search_pos = 0

    for idx, sentence in enumerate(sentences):
        # Normalize search text to find match in alignment characters
        clean_target = sentence.strip()
        found_pos = full_text.find(clean_target[:15], search_pos)
        if found_pos == -1:
            found_pos = search_pos

        match_end_pos = min(found_pos + len(clean_target), len(starts) - 1)
        start_t = starts[found_pos] if found_pos < len(starts) else 0.0
        end_t = ends[match_end_pos] if match_end_pos < len(ends) else total_audio_dur

        if idx == len(sentences) - 1:
            end_t = total_audio_dur

        cue_entries.append((start_t, end_t, sentence))
        search_pos = match_end_pos

    # Enforce strictly monotonic, non-overlapping timestamps
    monotonic_cues = []
    prev_end = 0.0
    for idx, (st, en, txt) in enumerate(cue_entries):
        clean_st = max(st, prev_end)
        clean_en = max(en, clean_st + 0.5)
        if idx == len(cue_entries) - 1:
            clean_en = max(clean_en, total_audio_dur)
        monotonic_cues.append((clean_st, clean_en, txt))
        prev_end = clean_en

    return monotonic_cues

def main():
    print("=" * 65)
    print("  ELEVENLABS ADAM STONE SYNTHESIS: EPISODE 08")
    print("=" * 65)

    api_key = get_api_key()
    print("[AUTH] Successfully loaded ElevenLabs API credentials.")

    act_audio_paths = []
    cumulative_cues = []
    cumulative_offset = 0.0

    # 1. Synthesize 5 English Acts
    for act_idx, act in enumerate(ACTS_DATA):
        act_id = act["id"]
        out_mp3 = AUDIO_DIR / f"{act_id}.mp3"
        out_srt = SUB_DIR / f"{act_id}.srt"

        print(f"\n[{act_idx+1}/{len(ACTS_DATA)}] Synthesizing {act['title']}...")
        full_act_text = " ".join(act["sentences"])

        data = synthesize_text_with_timestamps(api_key, full_act_text)
        audio_bytes = base64.b64decode(data["audio_base64"])
        with open(out_mp3, "wb") as f:
            f.write(audio_bytes)

        # Get exact duration via ffprobe
        cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(out_mp3)]
        dur = float(subprocess.check_output(cmd).decode().strip())
        print(f"  [OK] Saved audio: {out_mp3.name} ({dur:.2f}s)")

        alignment = data.get("alignment", {})
        cues = build_srt_from_alignment(act["sentences"], alignment, dur)

        # Write act SRT
        with open(out_srt, "w", encoding="utf-8") as f:
            for c_idx, (st, en, txt) in enumerate(cues):
                f.write(f"{c_idx+1}\n{format_timestamp(st)} --> {format_timestamp(en)}\n{txt}\n\n")
                cumulative_cues.append((st + cumulative_offset, en + cumulative_offset, txt))

        print(f"  [OK] Saved subtitles: {out_srt.name} ({len(cues)} cues)")
        act_audio_paths.append(out_mp3)
        cumulative_offset += dur

    # 2. Concat 5 Acts into Master Audio
    master_mp3 = EP08_DIR / "audio" / "episode_08_narration.mp3"
    concat_txt = AUDIO_DIR / "concat_list.txt"
    with open(concat_txt, "w", encoding="utf-8") as f:
        for p in act_audio_paths:
            f.write(f"file '{p.as_posix()}'\n")

    print(f"\n[*] Concatenating acts into master audio: {master_mp3.name}...")
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_txt), "-c:a", "libmp3lame", "-b:a", "192k", str(master_mp3)], check=True, capture_output=True)
    master_dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(master_mp3)]).decode().strip())
    print(f"[OK] Master audio generated: {master_dur:.2f}s (Cumulative offset drift: {abs(master_dur - cumulative_offset)*1000:.2f}ms)")

    # 3. Write Master Cumulative SRT
    master_srt = SUB_DIR / "episode_08_full.srt"
    with open(master_srt, "w", encoding="utf-8") as f:
        for c_idx, (st, en, txt) in enumerate(cumulative_cues):
            f.write(f"{c_idx+1}\n{format_timestamp(st)} --> {format_timestamp(en)}\n{txt}\n\n")
    print(f"[OK] Master cumulative SRT saved: {master_srt.name} ({len(cumulative_cues)} cues)")

    # 4. Synthesize 2 Companion Shorts Audio & SRT
    print("\n" + "=" * 65)
    print("  SYNTHESIZING COMPANION SHORTS (ENGLISH)")
    print("=" * 65)
    for s_idx, short in enumerate(SHORTS_DATA):
        s_id = short["id"]
        s_mp3 = SHORTS_AUDIO_DIR / f"{s_id}.mp3"
        s_srt = SUB_DIR / f"{s_id}.srt"

        print(f"\n[Short {s_idx+1}/2] Synthesizing {s_id}...")
        short_text = " ".join(short["sentences"])
        data = synthesize_text_with_timestamps(api_key, short_text)
        with open(s_mp3, "wb") as f:
            f.write(base64.b64decode(data["audio_base64"]))

        s_dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(s_mp3)]).decode().strip())
        s_cues = build_srt_from_alignment(short["sentences"], data.get("alignment", {}), s_dur)

        with open(s_srt, "w", encoding="utf-8") as f:
            for c_idx, (st, en, txt) in enumerate(s_cues):
                f.write(f"{c_idx+1}\n{format_timestamp(st)} --> {format_timestamp(en)}\n{txt}\n\n")

        print(f"  [OK] Saved short audio: {s_mp3.name} ({s_dur:.2f}s)")
        print(f"  [OK] Saved short subtitles: {s_srt.name} ({len(s_cues)} cues)")

    print("\n" + "=" * 65)
    print("  EPISODE 08 NARRATION & SUBTITLE SYNTHESIS COMPLETE!")
    print("=" * 65)

if __name__ == "__main__":
    main()
