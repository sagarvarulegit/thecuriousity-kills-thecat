import pytest
from pathlib import Path
from PIL import Image
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

def test_generate_high_contrast_thumbnail(tmp_path):
    from scripts.packaging_v2 import generate_high_contrast_thumbnail
    base_img = tmp_path / "base.jpg"
    Image.new("RGB", (1920, 1080), (30, 40, 60)).save(base_img)
    out_thumb = tmp_path / "thumb.jpg"
    
    res = generate_high_contrast_thumbnail(
        base_img=base_img,
        three_words="CARVED BACKWARDS?",
        out_jpg=out_thumb,
        concept="curiosity_hook"
    )
    assert res.exists()
    assert res.stat().st_size < 2 * 1024 * 1024 # Strictly < 2MB
    img = Image.open(res)
    assert img.size == (1920, 1080)

def test_three_word_rule_enforcement(tmp_path):
    from scripts.packaging_v2 import generate_high_contrast_thumbnail
    base_img = tmp_path / "base.jpg"
    Image.new("RGB", (1920, 1080), (30, 40, 60)).save(base_img)
    out_thumb = tmp_path / "thumb_err.jpg"
    
    # 5 words should raise ValueError under strict 3-Word Rule
    with pytest.raises(ValueError, match="3-Word Rule"):
        generate_high_contrast_thumbnail(
            base_img=base_img,
            three_words="THIS HAS TOO MANY WORDS HERE",
            out_jpg=out_thumb
        )

def test_publish_kit_tag_limit(tmp_path):
    from scripts.packaging_v2 import generate_publish_suite
    meta = {
        "title": "How Ancient Builders Carved Kailasa",
        "episode": 3,
        "description": "Episode description...",
        "tags": ["Kailasa Temple", "Ancient Engineering", "Ellora Caves", "Archaeology", "Architecture"]
    }
    kit_path = generate_publish_suite(meta, tmp_path)
    assert kit_path.exists()
    content = kit_path.read_text(encoding="utf-8")
    assert "Tags" in content
    # Extract tags block and verify length
    import re
    match = re.search(r"```(?:\w+)?\s*\n(.*?)\n```", content, re.DOTALL)
    if match:
        assert len(match.group(1).strip()) <= 500
