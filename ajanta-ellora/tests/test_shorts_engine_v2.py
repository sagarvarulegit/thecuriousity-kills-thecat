import pytest
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

def test_generate_karaoke_ass(tmp_path):
    from scripts.shorts_engine_v2 import generate_karaoke_ass
    words = [
        {"word": "WHERE", "start": 0.0, "end": 0.3},
        {"word": "DID", "start": 0.3, "end": 0.5},
        {"word": "400,000", "start": 0.5, "end": 1.1},
        {"word": "TONS", "start": 1.1, "end": 1.5}
    ]
    out_ass = tmp_path / "subtitles.ass"
    res = generate_karaoke_ass(words, out_ass)
    assert res.exists()
    content = res.read_text(encoding="utf-8")
    assert "[Script Info]" in content
    assert "PlayResY: 1920" in content
    assert "PlayResX: 1080" in content
    assert "FACC15" in content.upper() or "15CCFA" in content.upper() # Yellow active highlight
    assert "WHERE" in content
    assert "400,000" in content

def test_shorts_pacing_validation():
    from scripts.shorts_engine_v2 import validate_shorts_cuts
    # Valid manifest: 14 cuts for 45s (avg ~3.2s)
    manifest = [f"cut_{i:02d}.jpg" for i in range(14)]
    assert validate_shorts_cuts(manifest, duration_s=45.0) is True
    
    # Invalid manifest: only 1 static image
    single_image = ["static.jpg"]
    assert validate_shorts_cuts(single_image, duration_s=45.0) is False
