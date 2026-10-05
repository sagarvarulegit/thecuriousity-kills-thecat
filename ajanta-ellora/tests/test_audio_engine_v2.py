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

def test_sidechain_ducking_wav_clean_command(tmp_path, monkeypatch):
    from scripts.audio_engine_v2 import apply_sidechain_ducking
    vocal = tmp_path / "vocal.wav"
    bgm = tmp_path / "bgm.wav"
    out = tmp_path / "mixed.wav"
    create_dummy_wav(vocal, 2.0, 440)
    create_dummy_wav(bgm, 2.0, 220)

    # Track subprocess calls to ensure fallback is NEVER invoked
    calls = []
    orig_run = subprocess.run
    def tracker(cmd, *args, **kwargs):
        calls.append(cmd)
        return orig_run(cmd, *args, **kwargs)
    monkeypatch.setattr(subprocess, "run", tracker)

    res = apply_sidechain_ducking(vocal, bgm, out, ducking_db=-16)
    assert res.exists()
    # Primary call must succeed in 1 call; fallback must NOT be called (calls count == 1)
    assert len(calls) == 1, f"Expected 1 FFmpeg run (primary sidechain), but got {len(calls)} (fallback was invoked!)"

def test_verify_audio_stems_drift(tmp_path):
    from scripts.audio_engine_v2 import verify_audio_stems_drift
    m = tmp_path / "master.wav"
    a1 = tmp_path / "act1.wav"
    a2 = tmp_path / "act2.wav"
    
    # 2.0s master = 1.0s act1 + 1.0s act2 (0ms drift)
    create_dummy_wav(m, 2.0, 440)
    create_dummy_wav(a1, 1.0, 440)
    create_dummy_wav(a2, 1.0, 440)
    
    ok, drift = verify_audio_stems_drift(m, [a1, a2], max_drift_ms=10.0)
    assert ok is True
    assert drift < 10.0

    # Introduce 100ms drift
    a2_mismatch = tmp_path / "act2_mismatch.wav"
    create_dummy_wav(a2_mismatch, 1.10, 440)
    ok2, drift2 = verify_audio_stems_drift(m, [a1, a2_mismatch], max_drift_ms=10.0)
    assert ok2 is False
    assert drift2 >= 10.0
