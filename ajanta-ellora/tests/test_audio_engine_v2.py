import pytest
from pathlib import Path
import subprocess
import numpy as np
import wave
import sys

# Ensure ajanta-ellora is on path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

def create_dummy_wav(path: Path, duration_s: float = 3.0, freq: int = 440):
    sr = 44100
    t = np.linspace(0, duration_s, int(sr * duration_s), endpoint=False)
    audio = (0.5 * np.sin(2 * np.pi * freq * t) * 32767).astype(np.int16)
    with wave.open(str(path), 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(audio.tobytes())

def test_apply_sidechain_ducking(tmp_path):
    from scripts.audio_engine_v2 import apply_sidechain_ducking
    vocal = tmp_path / "vocal.wav"
    bgm = tmp_path / "bgm.wav"
    out = tmp_path / "mixed.wav"
    create_dummy_wav(vocal, 3.0, 440)
    create_dummy_wav(bgm, 3.0, 220)
    
    res = apply_sidechain_ducking(vocal, bgm, out, ducking_db=-16)
    assert res.exists()
    assert res.stat().st_size > 0

def test_preprocess_pacing_text():
    from scripts.audio_engine_v2 import preprocess_pacing_text
    raw = "Look down into the abyss. Three colossal trenches have severed the living rock."
    processed = preprocess_pacing_text(raw)
    assert "..." in processed or "—" in processed or "," in processed
