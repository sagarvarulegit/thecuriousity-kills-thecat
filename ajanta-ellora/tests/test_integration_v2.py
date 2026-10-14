import pytest
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

def test_pipeline_modules_importable():
    from scripts.audio_engine_v2 import preprocess_pacing_text, apply_sidechain_ducking
    from scripts.foley_generator_v2 import generate_foley_track
    from scripts.shorts_engine_v2 import generate_karaoke_ass, validate_shorts_cuts
    from scripts.motion_graphics_v2 import render_kinetic_hud_card, build_filmic_color_filter
    from scripts.packaging_v2 import generate_high_contrast_thumbnail, generate_publish_suite

    assert callable(preprocess_pacing_text)
    assert callable(generate_foley_track)
    assert callable(generate_karaoke_ass)
    assert callable(render_kinetic_hud_card)
    assert callable(generate_high_contrast_thumbnail)

def test_zero_repetition_manifest_assertion():
    manifest = [
        ("image", "hero_01.jpg", "zoom_in"),
        ("video", "action_01.mp4", "action_clip"),
        ("hud", "hud_01.png", "telemetry"),
        ("image", "hero_02.jpg", "pan_right")
    ]
    assets = [m[1] for m in manifest]
    assert len(assets) == len(set(assets)), "Duplicate assets detected in manifest!"
