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
        "title": "Act I: The Golden Reawakening (The Harishena Renaissance)",
        "sentences": [
            "For nearly four centuries, the horseshoe canyon of Ajanta lay in absolute silence.",
            "The austere stone stupas carved by early Satavahana monks had been swallowed by jungle vines, while monsoon floods silted the dark chaitya floors.",
            "Then—around the year 460 of the common era—a volcanic explosion of royal power transformed the ravine forever.",
            "From the north, Emperor Harishena of the Vakataka dynasty united the Deccan, forging an empire that stretched from the Arabian Sea to the Bay of Bengal.",
            "Wealth from the Silk Road and the ancient Dakshinapatha trade artery poured directly into this secluded mountain.",
            "Harishena’s royal ministers, feudatory kings, and merchant guilds began an unprecedented architectural assault upon the cliff face.",
            "Within just seventeen feverish years, master stonecutters carved twenty colossal new sanctuaries into the sheer basalt.",
            "But these were no longer simple ascetic retreats; they were multi-story rock-cut university palaces with soaring columned courtyards and gilded shrine halls.",
            "And upon their smooth interior walls, ancient painters were about to achieve a visual miracle that would outlast every empire of the ancient world."
        ]
    },
    {
        "id": "act_02_the_basalt_problem_and_mud_chemistry",
        "title": "Act II: The Basalt Problem & The Mud Chemistry Secret",
        "sentences": [
            "To paint inside Ajanta, ancient craftsmen faced an impossible geological reality.",
            "The walls were not made of smooth limestone or dry sandstone; they were carved out of dense, volcanic flood basalt.",
            "Basalt is an igneous rock formed by cooling lava—glassy, non-porous, and constantly weeping subterranean moisture.",
            "If you apply paint directly to raw basalt, the moisture pushes the pigment off within months, causing it to flake and disintegrate into dust.",
            "European fresco painters solved dampness with slaked lime on wet walls, but inside a subterranean volcanic cave, European fresco techniques fail completely.",
            "The master guilds of Ajanta developed a revolutionary, multi-layered bio-composite formula recorded in ancient treatises like the Chitrasutra.",
            "First, laborers took pointed iron picks and rapidly pecked thousands of mechanical dimples directly into the stone, creating a rough key for the plaster to bite.",
            "Then came the secret bio-chemical matrix: a thick, fermented plaster made of local ferruginous red clay, pulverized rock grit, and cow dung.",
            "Fermented cow dung was not crude; it was chemical genius.",
            "Its digested vegetal fibers provided microscopic cellulose netting that prevented shrinkage cracks, while natural bacteria buffered internal cave humidity.",
            "Mixed with fibrous rice husks and boiled sap from neem trees and bel fruit, the mud layer created a natural, mold-resistant living skin that breathed with the mountain.",
            "Finally, artisans applied an ultra-thin finish coat called intonaco—a delicate paste of slaked lime, powdered gypsum, and crushed sea shells.",
            "While still damp, a craftsman knelt before the wall holding a smooth, banded agate river pebble, burnishing the surface with steady circular strokes.",
            "Under the friction of the agate stone, the lime compacted into an ivory-smooth, reflective porcelain surface ready for pigment."
        ]
    },
    {
        "id": "act_03_the_silk_road_blue",
        "title": "Act III: The Silk Road Blue (Lapis Lazuli Alchemy)",
        "sentences": [
            "When the plaster cured, the master painters uncapped their pigment bowls.",
            "For reds and yellows, they crushed local volcanic ochres scooped from Deccan soil.",
            "For forest greens, they ground mineral glauconite; for black, they gathered pure soot from burning mustard oil lamps.",
            "But across the royal ceilings of Cave One and Cave Seventeen glows a color that did not come from the Indian subcontinent.",
            "It is a blinding, celestial ultramarine blue that still burns on the stone walls after fifteen hundred years.",
            "This was lapis lazuli.",
            "In the fifth century, there was only one known source of lapis lazuli in the entire ancient world: the treacherous, high-altitude mines of Badakhshan in northern Afghanistan.",
            "To reach this remote volcanic canyon, raw blue crystals traveled over two thousand five hundred kilometers.",
            "Carried in leather saddlebags on pack camels through the snow-bound passes of the Hindu Kush, the stones crossed the Indus plains and journeyed south along the Dakshinapatha.",
            "Ounce for ounce, pure Badakhshan lapis was worth more than solid gold.",
            "Only the wealthiest royal patrons—like Emperor Harishena’s prime minister Varahadeva—could afford to coat entire ceilings in imported Afghan blue.",
            "It was a physical testament to a globalized world, where Central Asian mineral wealth met the spiritual genius of ancient India."
        ]
    },
    {
        "id": "act_04_the_sootless_cave",
        "title": "Act IV: The Sootless Cave (Subterranean Optical Engineering)",
        "sentences": [
            "Yet this artistic triumph presents a profound archaeological paradox.",
            "Caves One, Two, Sixteen, and Seventeen penetrate thirty to forty meters deep into solid subterranean mountain rock.",
            "Step beyond the entrance portico, and you enter pitch-black darkness where your eyes cannot see your own outstretched hand.",
            "Yet here, in the deepest recess of the cave, artists painted microscopic details: eyelashes a tenth of a millimeter thin, translucent pearls, and gold-embroidered textiles.",
            "How did they paint these masterworks without light?",
            "When Victorian surveyors and modern conservators analyzed the cave ceilings, they searched for the telltale soot and carbon residue left by oil lamps or burning torches.",
            "They found absolutely none.",
            "Burning torches in these enclosed halls would have suffocated the artisans and stained the white lime plaster with thick black smoke.",
            "The solution was an ingenious optical engineering array.",
            "In the searing sunlight outside the veranda, assistants positioned large, circular cast-bronze mirrors.",
            "The highly polished bronze caught the blazing Deccan sun, collimating natural rays into intense, focused beams of light.",
            "These beams were bounced through the cave doorways and intercepted by wet, bleached white cotton and silk sheets held by apprentices.",
            "The wet fabric diffused the harsh solar glare into a soft, ambient glow that illuminated every corner of the subterranean hall without generating a single wisp of soot.",
            "The painters were literally painting with captured sunlight."
        ]
    },
    {
        "id": "act_05_the_masterpieces_of_humanity",
        "title": "Act V: The Masterpieces of Humanity & The Looming Shadow",
        "sentences": [
            "Illuminated by bounced sunlight, the master guilds painted the greatest masterpieces of ancient world art.",
            "Chief among them stands the Bodhisattva Padmapani on the rear wall of Cave One.",
            "Holding a blue lotus in his right hand, his body curves in the gentle tribhanga posture, his heavy-lidded eyes gazing downward with serene compassion.",
            "Notice the subtle three-dimensional shading—known in Sanskrit as vartana—where darker tones along the contours give the illusion of living flesh emerging from the rock.",
            "A thousand years before Leonardo da Vinci developed chiaroscuro in the Italian Renaissance, the painters of Ajanta had already mastered human anatomy, emotional expression, and spatial depth.",
            "Across the walls, narrative Jataka tales come to life: royal courts overflowing with Persian ambassadors in pointed caps, forest ascetics, and celestial dancers floating through clouds.",
            "But as artists applied the final touches of Afghan lapis lazuli around the year 477, a catastrophic shadow fell across the empire.",
            "Emperor Harishena died suddenly under mysterious circumstances.",
            "Almost overnight, the Vakataka dynasty fractured into bitter succession wars, and hostile rival kingdoms converged on the Deccan.",
            "Royal funding vanished in an instant.",
            "In caves down the cliff face, half-finished pillars were abandoned mid-strike, brushes were laid down wet, and terrified monks fled into the hills.",
            "Within months, the golden city in the volcanic cliff went completely silent.",
            "In our next episode, we will investigate the overnight silence: the sudden military collapse that froze Ajanta in time, and sealed thirty temples inside the jungle for thirteen centuries."
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
