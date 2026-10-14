import pytest
from pathlib import Path
from PIL import Image
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

def test_render_kinetic_hud_card(tmp_path):
    from scripts.motion_graphics_v2 import render_kinetic_hud_card
    out_dir = tmp_path / "frames"
    frames = render_kinetic_hud_card(
        label="EXCAVATED ROCK",
        end_value=400000,
        unit="TONS",
        duration_s=1.0,
        fps=30,
        out_dir=out_dir
    )
    assert len(frames) == 30
    assert frames[0].exists()
    img = Image.open(frames[-1])
    assert img.size == (1920, 1080)

def test_build_35mm_grain_filter():
    from scripts.motion_graphics_v2 import build_filmic_color_filter
    vf = build_filmic_color_filter(grain_opacity=0.08)
    assert "vignette" in vf
    assert "eq=" in vf
    assert "contrast=" in vf
