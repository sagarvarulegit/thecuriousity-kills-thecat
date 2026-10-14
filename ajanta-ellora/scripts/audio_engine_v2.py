"""
Broadcast Production Engine v2.0 - Audio Suite
Features:
- ElevenLabs Adam Stone synthesis (auq43ws1oslv0tO4BDa7) with dramatic pacing preprocessing
- FFmpeg sidechain auto-ducking (-16 dB) and EBU R128 loudness normalization
- Whisper word-level timing alignment and monotonic cue generation
"""

import os
import re
import sys
import json
import wave
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple

# Default official voice: Adam Stone (British, smooth, relaxed and deep)
ADAM_STONE_VOICE_ID = "auq43ws1oslv0tO4BDa7"

BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets"
MUSIC_DIR = ASSETS_DIR / "music_library"

# Ensure music library directory structure exists
for mood in ["01_mystery_ambient", "02_historical_drama", "03_tension_percussion", "04_climactic_reveal"]:
    (MUSIC_DIR / mood).mkdir(parents=True, exist_ok=True)

def preprocess_pacing_text(text: str) -> str:
    """
    Inserts dramatic breath pauses (...) and cadence separators
    to give ElevenLabs narration authentic documentary gravitas.
    """
    # Replace period before dramatic words, numbers, or questions with an ellipsis pause
    pattern = r'\.\s+([A-Z][a-z]+|\d+|Three|Thirty|One|Two|Four|Five|Look|Now|Yet|Suddenly|Inside|Standing|Archaeologists)\b'
    text = re.sub(pattern, r'... \1', text)
    # Ensure em-dashes have micro-breaths
    text = text.replace("—", " — ")
    return text

def synthesize_narration_elevenlabs(
    text: str,
    out_path: Path,
    voice_id: str = ADAM_STONE_VOICE_ID,
    api_key: Optional[str] = None
) -> Path:
    """
    Synthesizes speech using ElevenLabs API (eleven_multilingual_v2).
    """
    api_key = api_key or os.getenv("ELEVEN_LABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVEN_LABS_API_KEY is not configured in environment!")

    pacing_text = preprocess_pacing_text(text)
    import requests

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "text": pacing_text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.55,
            "similarity_boost": 0.78,
            "style": 0.15,
            "use_speaker_boost": True
        }
    }
    resp = requests.post(url, headers=headers, json=payload)
    if resp.status_code != 200:
        raise RuntimeError(f"ElevenLabs error ({resp.status_code}): {resp.text}")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(resp.content)
    return out_path

def apply_sidechain_ducking(
    vocal_path: Path,
    bgm_path: Path,
    out_path: Path,
    ducking_db: int = -16,
    target_lufs: float = -16.0
) -> Path:
    """
    Applies FFmpeg sidechain compression to duck BGM under speech,
    then applies EBU R128 loudness normalization.
    """
    out_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 1. Check if files exist
    if not vocal_path.exists() or not bgm_path.exists():
        raise FileNotFoundError(f"Input audio files not found: {vocal_path} or {bgm_path}")

    # Sidechain compression filter:
    # [1:a] is vocal, [0:a] is BGM
    # split vocal so it can act as sidechain trigger and final mix
    # sidechaincompress lowers bgm when vocal rises above threshold
    vol_linear = 10 ** (ducking_db / 20.0) if ducking_db < 0 else 0.20
    filter_complex = (
        f"[0:a]volume={vol_linear:.3f}[bgm_base];"
        "[1:a]asplit=2[sc][vox];"
        "[bgm_base][sc]sidechaincompress=threshold=0.08:ratio=4:attack=50:release=350[ducked_bgm];"
        "[vox][ducked_bgm]amix=inputs=2:duration=first:dropout_transition=2[mixed];"
        f"[mixed]loudnorm=I={target_lufs}:TP=-1.5:LRA=11[out]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-i", str(bgm_path),
        "-i", str(vocal_path),
        "-filter_complex", filter_complex,
        "-map", "[out]"
    ]
    if out_path.suffix.lower() == ".wav":
        cmd.extend(["-c:a", "pcm_s16le"])
    elif out_path.suffix.lower() == ".mp3":
        cmd.extend(["-c:a", "libmp3lame", "-b:a", "192k"])
    else:
        cmd.extend(["-c:a", "aac", "-b:a", "192k"])
    cmd.append(str(out_path))
    
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        # Fallback to simple amix if sidechain fails
        cmd_fallback = [
            "ffmpeg", "-y",
            "-i", str(bgm_path),
            "-i", str(vocal_path),
            "-filter_complex", "[0:a]volume=0.25[b];[1:a]volume=1.0[v];[b][v]amix=inputs=2:duration=first[out]",
            "-map", "[out]",
            str(out_path)
        ]
        subprocess.run(cmd_fallback, check=True, capture_output=True)

    return out_path

def get_media_duration(file_path: Path) -> float:
    """Extracts exact media duration in seconds via ffprobe or wave."""
    if not file_path.exists():
        raise FileNotFoundError(f"Media file not found: {file_path}")

    # If WAV file, fast header parse
    if file_path.suffix.lower() == ".wav":
        try:
            with wave.open(str(file_path), "rb") as wf:
                return wf.getnframes() / float(wf.getframerate())
        except Exception:
            pass

    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(file_path)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(res.stdout.strip())

def verify_audio_stems_drift(
    master_audio_path: Path,
    act_audio_paths: List[Path],
    max_drift_ms: float = 10.0
) -> Tuple[bool, float]:
    """
    Mathematically compares the duration of the concatenated master narration
    against the mathematical sum of the individual act audio stems.
    Returns (is_in_sync: bool, drift_ms: float).
    """
    master_dur = get_media_duration(master_audio_path)
    acts_dur = sum(get_media_duration(act_p) for act_p in act_audio_paths)

    drift_ms = abs(master_dur - acts_dur) * 1000.0
    is_in_sync = drift_ms <= max_drift_ms
    return is_in_sync, drift_ms

