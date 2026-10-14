import pytest
from pathlib import Path
import wave
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

def test_generate_foley_track(tmp_path):
    from scripts.foley_generator_v2 import generate_foley_track
    out_wav = tmp_path / "foley.wav"
    cues = [
        (0.5, "sub_bass", 2.0),
        (2.0, "stone_strike", 0.1),
        (3.5, "whoosh", 0.4)
    ]
    res = generate_foley_track(duration_s=5.0, cues=cues, out_wav_path=out_wav)
    assert res.exists()
    with wave.open(str(res), 'rb') as wf:
        assert wf.getframerate() == 44100
        assert wf.getnchannels() == 1
        assert wf.getnframes() == int(5.0 * 44100)
