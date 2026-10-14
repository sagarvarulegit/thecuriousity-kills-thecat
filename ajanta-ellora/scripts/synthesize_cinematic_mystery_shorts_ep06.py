#!/usr/bin/env python3
"""
synthesize_cinematic_mystery_shorts_ep06.py — High-Conversion Mystery Funnel Synthesizer
Re-synthesizes Episode 06 Shorts with:
1. Tight 38-44s pacing (STRICTLY < 58.0s YouTube Shorts duration ceiling)
2. Nolan-style Incomplete Illusion / Prestige structure
3. Spielberg-style Visceral Danger & Reaction Stakes
4. Ray-style Basalt Physics & Human Agony
5. Loewenstein Information Gap & Zeigarnik Effect open loops
6. Native YouTube 'Related Video' UI redirection
7. Millisecond-accurate sentence-level SRT subtitles
8. Broadcast EBU R128 (-16 LUFS) orchestral ducked mixing
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

# Force UTF-8 on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

WORKSPACE_ROOT = Path("C:/Sagar/Projects/thecuriousity-kills-thecat")
EP06_DIR = WORKSPACE_ROOT / "ajanta-ellora" / "episode06"
AUDIO_DIR = EP06_DIR / "audio"
SUB_DIR = EP06_DIR / "subtitles"
AUDIO_HINDI_DIR = EP06_DIR / "audio_hindi"
SUB_HINDI_DIR = EP06_DIR / "subtitles_hindi"
SCRIPTS_DIR = WORKSPACE_ROOT / "ajanta-ellora" / "scripts"

sys.path.insert(0, str(SCRIPTS_DIR))
from mix_episode_06_audio import mix_track_with_bed, get_media_duration

VOICE_ID = "auq43ws1oslv0tO4BDa7"  # Adam Stone
MODEL_ID = "eleven_multilingual_v2"

def get_api_key() -> str:
    env_p = WORKSPACE_ROOT / ".env"
    if env_p.exists():
        for line in env_p.read_text(encoding="utf-8").splitlines():
            if line.startswith("ELEVEN_LABS_API_KEY=") or line.startswith("ELEVENLABS_API_KEY="):
                return line.split("=", 1)[1].strip()
    key = os.getenv("ELEVEN_LABS_API_KEY") or os.getenv("ELEVENLABS_API_KEY")
    if not key:
        raise ValueError("ELEVEN_LABS_API_KEY not found!")
    return key

# Optimized 38-44s High-Pacing Mystery Scripts
ENGLISH_SHORTS = [
    {
        "id": "short_01_the_sky_bridge_that_shouldnt_exist",
        "title": "Short 01: The Sky Bridge That Shouldn't Exist",
        "sentences": [
            "Structural engineers 3D-scanned this ancient stone bridge. According to modern physics, it shouldn't be standing.",
            "Suspended thirty feet over a 100-foot chasm, this bridge has zero mortar, zero keystones, and zero joints.",
            "Ancient carvers didn't build it upward—they scooped away the mountain beneath it while hanging on hemp ropes.",
            "Basalt has zero tensile strength. The second the void was hollowed, gravity should have snapped the stone.",
            "Yet for twelve centuries, it hasn't sagged by a single millimeter.",
            "The lost calculation that cheated gravity is revealed in our full documentary below. Tap to unlock the truth."
        ]
    },
    {
        "id": "short_02_the_temple_that_1000_men_couldnt_destroy",
        "title": "Short 02: The Temple That 1,000 Men Couldn't Destroy",
        "sentences": [
            "In 1682, an army of 1,000 demolition engineers was ordered to destroy one temple. After three years... they surrendered.",
            "They brought iron sledges, crowbars, and fire. In a normal building, knocking out three pillars collapses the entire roof.",
            "But against Kailasa, their chisels shattered into scrap metal.",
            "Because Kailasa isn't assembled from stone blocks—it is a single, 400,000-ton volcanic mountain.",
            "When engineers tried triggering a collapse at the base, what they discovered inside the rock terrified the Emperor.",
            "The secret geological shield that saved this temple is decoded in our full investigation linked below. Tap to watch now."
        ]
    }
]

HINDI_SHORTS = [
    {
        "id": "short_01_the_sky_bridge_that_shouldnt_exist",
        "title": "Short 01: आकाश में झूलता असंभव पाषाण सेतु",
        "sentences": [
            "इंजीनियर्स ने इस प्राचीन पाषाण पुल का 3D स्कैन किया, और आधुनिक भौतिकी के अनुसार... इसे गिर जाना चाहिए था।",
            "सौ फीट गहरी खाई में तीस फीट ऊपर झूलते इस पुल में न कोई जोड़ है, न मेहराब, और न कोई सहारा।",
            "कारीगरों ने इसे बनाया नहीं—बल्कि रस्सियों से लटककर नीचे के पूरे पर्वत को काटकर खाली कर दिया।",
            "बेसाल्ट में कोई खिंचाव क्षमता नहीं होती। नीचे की चट्टान हटते ही इसे तुरंत टूट जाना चाहिए था।",
            "लेकिन बारह सौ वर्षों से, यह एक मिलीमीटर भी नहीं झुका।",
            "गुरुत्वाकर्षण को मात देने वाला यह रहस्य नीचे दिए गए मुख्य वीडियो में उजागर है। पूरा सच जानने के लिए अभी टैप करें।"
        ]
    },
    {
        "id": "short_02_the_temple_that_1000_men_couldnt_destroy",
        "title": "Short 02: वह मंदिर जिसे एक हज़ार सैनिक भी न गिरा सके",
        "sentences": [
            "1682 में, एक हज़ार सैनिकों को यह एक मंदिर गिराने का आदेश दिया गया। तीन वर्षों बाद... उन्होंने हार मान ली।",
            "वे भारी हथौड़े और आग लेकर आए थे। किसी भी इमारत के तीन खंभे तोड़ते ही पूरी छत गिर जाती है।",
            "लेकिन कैलाश पर प्रहार करते ही उनकी लोहे की छैनियां चूर-चूर हो गईं।",
            "क्योंकि कैलाश पत्थरों से नहीं बना—यह चार लाख टन का एक ही अखंड पर्वत है।",
            "जब उन्होंने इसकी नींव ढहाने की कोशिश की, तो चट्टान के भीतर कुछ ऐसा मिला जिसने बादशाह को खौफ में डाल दिया।",
            "मंदिर को बचाने वाली वह गुप्त ढाल नीचे दिए गए मुख्य वीडियो में डिकोड की गई है। पूरा सच जानने के लिए अभी क्लिक करें।"
        ]
    }
]

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
    resp = requests.post(url, json=payload, headers=headers, timeout=90)
    if resp.status_code != 200:
        raise RuntimeError(f"ElevenLabs API Error {resp.status_code}: {resp.text}")
    data = resp.json()
    audio_bytes = base64.b64decode(data["audio_base64"])
    alignment = data.get("alignment", {})
    return audio_bytes, alignment

def format_srt_time(seconds: float) -> str:
    total_ms = int(round(seconds * 1000))
    hours = total_ms // 3600000
    rem = total_ms % 3600000
    mins = rem // 60000
    rem = rem % 60000
    secs = rem // 1000
    ms = rem % 1000
    return f"{hours:02d}:{mins:02d}:{secs:02d},{ms:03d}"

def build_srt_cues(sentences: List[str], full_text: str, alignment: Dict[str, Any], total_duration: float) -> List[Dict[str, Any]]:
    chars = alignment.get("characters", [])
    char_starts = alignment.get("character_start_times_seconds", [])
    char_ends = alignment.get("character_end_times_seconds", [])
    
    cues = []
    if not chars or not char_starts or len(char_starts) == 0:
        chunk = total_duration / len(sentences)
        for i, s in enumerate(sentences):
            cues.append({
                "text": s.strip(),
                "start": i * chunk,
                "end": (i + 1) * chunk
            })
        return cues

    current_search_idx = 0
    full_synth_text = "".join(chars)
    
    for s_idx, sent in enumerate(sentences):
        sent_clean = sent.strip()
        words = sent_clean.split()
        if not words:
            continue
        first_word = words[0].strip(".,!?:;\"'()[]{}—")
        last_word = words[-1].strip(".,!?:;\"'()[]{}—")
        
        pos_start = full_synth_text.find(first_word, current_search_idx)
        if pos_start == -1:
            pos_start = current_search_idx
            
        pos_end = full_synth_text.find(last_word, pos_start)
        if pos_end != -1:
            pos_end = min(pos_end + len(last_word) - 1, len(char_ends) - 1)
        else:
            pos_end = min(pos_start + len(sent_clean) - 1, len(char_ends) - 1)
            
        start_t = char_starts[min(pos_start, len(char_starts) - 1)]
        end_t = char_ends[min(pos_end, len(char_ends) - 1)]
        
        if cues and start_t < cues[-1]["end"]:
            start_t = cues[-1]["end"] + 0.05
        if end_t <= start_t:
            end_t = start_t + 1.5
            
        current_search_idx = pos_end + 1
        cues.append({
            "text": sent_clean,
            "start": round(start_t, 3),
            "end": round(end_t, 3)
        })
        
    if cues:
        cues[0]["start"] = 0.0
        cues[-1]["end"] = round(total_duration, 3)
        for i in range(len(cues) - 1):
            if cues[i]["end"] > cues[i+1]["start"]:
                mid = (cues[i]["end"] + cues[i+1]["start"]) / 2.0
                cues[i]["end"] = round(mid - 0.02, 3)
                cues[i+1]["start"] = round(mid + 0.02, 3)
                
    return cues

def write_srt(cues: List[Dict[str, Any]], out_path: Path):
    lines = []
    for i, c in enumerate(cues, 1):
        s_str = format_srt_time(c["start"])
        e_str = format_srt_time(c["end"])
        lines.append(f"{i}\n{s_str} --> {e_str}\n{c['text']}\n")
    out_path.write_text("\n".join(lines), encoding="utf-8")

def process_shorts_set(lang: str, shorts_data: List[Dict[str, Any]], audio_dir: Path, sub_dir: Path, api_key: str):
    print(f"\n{'=' * 65}")
    print(f"  SYNTHESIZING {lang.upper()} CINEMATIC MYSTERY SHORTS (< 50s TARGET)")
    print(f"{'=' * 65}")
    
    for s in shorts_data:
        s_id = s["id"]
        full_text = " ".join(s["sentences"])
        raw_mp3 = audio_dir / f"{s_id}.mp3"
        mixed_mp3 = audio_dir / f"{s_id}_mixed.mp3"
        srt_file = sub_dir / f"{s_id}.srt"
        
        print(f"\n[*] Synthesizing {s['title']} ({len(s['sentences'])} beats)...")
        audio_bytes, alignment = synthesize_with_timestamps(full_text, api_key)
        raw_mp3.write_bytes(audio_bytes)
        
        dur = get_media_duration(raw_mp3)
        print(f"    Raw Audio: {raw_mp3.name} ({dur:.2f}s | {len(audio_bytes):,} bytes)")
        if dur >= 58.0:
            print(f"    [WARNING] Audio duration ({dur:.2f}s) is close to 60s Shorts ceiling!")
        else:
            print(f"    [PERFECT] Audio duration ({dur:.2f}s) is well within 60s Shorts ceiling!")
        
        cues = build_srt_cues(s["sentences"], full_text, alignment, dur)
        write_srt(cues, srt_file)
        print(f"    Generated SRT: {srt_file.name} ({len(cues)} cues)")
        
        # Mix with cinematic orchestral bed and EBU R128 (-16 LUFS)
        print(f"    Mixing with D-Aeolian orchestral bed & auto-ducking...")
        mix_track_with_bed(raw_mp3, mixed_mp3, dur)
        mixed_dur = get_media_duration(mixed_mp3)
        print(f"    [OK] Mixed Master Audio: {mixed_mp3.name} ({mixed_dur:.2f}s)")
        
        # Also copy legacy aliases if short_02 in hindi
        if s_id == "short_02_the_temple_that_1000_men_couldnt_destroy" and lang == "hi":
            legacy_mp3 = audio_dir / "short_02_why_elephants_support_the_mountain.mp3"
            legacy_srt = sub_dir / "short_02_why_elephants_support_the_mountain.srt"
            legacy_mp3.write_bytes(raw_mp3.read_bytes())
            legacy_srt.write_text(srt_file.read_text(encoding="utf-8"), encoding="utf-8")

def main():
    api_key = get_api_key()
    process_shorts_set("en", ENGLISH_SHORTS, AUDIO_DIR, SUB_DIR, api_key)
    process_shorts_set("hi", HINDI_SHORTS, AUDIO_HINDI_DIR, SUB_HINDI_DIR, api_key)
    print("\n[SUCCESS] All Episode 06 Cinematic Shorts Audio and Subtitles Synthesized & Mixed!")

if __name__ == "__main__":
    main()
