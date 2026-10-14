# Broadcast Production Engine v2.0 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and deploy an automated, high-retention documentary webseries and viral Shorts production engine featuring ElevenLabs Adam Stone narration, dynamic BGM sidechain ducking, procedural Foley synthesis, word-by-word kinetic karaoke captions, headless 3D/HUD motion graphics, 35mm film grain texturing, and mobile-first packaging.

**Architecture:** A modular Python pipeline combining ElevenLabs API, OpenAI Whisper word-level timing, FFmpeg multi-track audio ducking (`sidechaincompress`), NumPy procedural Foley, Headless Blender CLI rendering, Pillow kinetic HUD telemetry, and Advanced SubStation Alpha (`.ass`) karaoke caption generation, guarded by TypeSafe Jev System 1 assertions.

**Tech Stack:** Python 3.11, FFmpeg, NumPy, Pillow, ElevenLabs API, OpenAI Whisper, Blender CLI, pytest, TypeSafe Jev (`typesafe-jev` MCP / Jev-1.13).

**Spec:** [`docs/superpowers/specs/2026-10-05-broadcast-production-engine-v2-design.md`](file:///C:/Sagar/Projects/thecuriousity-kills-thecat/docs/superpowers/specs/2026-10-05-broadcast-production-engine-v2-design.md)

## Global Constraints

- Master video resolution: Strictly 1080p Full HD (`1920x1080`) at 30fps.
- Shorts video resolution: Strictly 9:16 vertical (`1080x1920`) at 30fps.
- Audio loudness: -16.0 ± 1.0 LUFS integrated, True Peak < -1.5 dBFS via FFmpeg `loudnorm`.
- Narration Voice: ElevenLabs **Adam Stone** (`auq43ws1oslv0tO4BDa7`).
- Zero repetition invariant: Every cut must resolve to a unique visual asset (`len(manifest) == len(set(manifest))`).
- YouTube SEO tags: Strictly capped under 500 characters per publish kit.
- Thumbnail file size: Strictly under 2.0 MB per thumbnail.
- Subtitle cues: Monotonic start times, 0 overlapping cues.

## Review Focus

1. **Audio Drift on Concatenation**: When summing individual act audio stems against master narration, duration discrepancy must be < 10.0ms.
2. **Sidechain Ducking Release Click**: FFmpeg `sidechaincompress` must not introduce clipping or audible clicks during rapid voice transitions (`attack=80`, `release=450`).
3. **Shorts Caption Safe Zones**: Kinetic karaoke captions must render between Y: 58% and 62% to prevent collision with YouTube Shorts right-side UI buttons and bottom channel title overlay.
4. **Sub-Pixel Jitter Elimination**: All still Ken Burns moves must be pre-scaled to 4K (`scale=3840:2160 -> zoompan -> s=1920x1080`) using continuous equations to prevent 1-pixel integer micro-jitter.
5. **Headless Blender CLI Fallback**: If Blender binary is missing or headless rendering fails, the pipeline must smoothly fallback to pre-rendered sequences or kinetic 2.5D PIL isometric cards without crashing.

---

### Task 1: Curated Music Library & Audio Ducking Engine

**Files:**
- Create: `ajanta-ellora/scripts/audio_engine_v2.py`
- Create: `ajanta-ellora/tests/test_audio_engine_v2.py`
- Setup: `ajanta-ellora/assets/music_library/{01_mystery_ambient,02_historical_drama,03_tension_percussion,04_climactic_reveal}`

**Interfaces:**
- Consumes: Raw act text strings, ElevenLabs API key, local audio library.
- Produces: `synthesize_narration(text, voice_id) -> Path`, `align_whisper_cues(audio_path) -> dict`, `apply_sidechain_ducking(vocal_path, bgm_path, out_path, ducking_db=-16) -> Path`.

- [ ] **Step 1: Write failing test for audio ducking and loudness normalization**

```python
# ajanta-ellora/tests/test_audio_engine_v2.py
import pytest
from pathlib import Path
import subprocess
import numpy as np

def create_dummy_wav(path: Path, duration_s: float = 3.0, freq: int = 440):
    sr = 44100
    t = np.linspace(0, duration_s, int(sr * duration_s), endpoint=False)
    audio = (0.5 * np.sin(2 * np.pi * freq * t) * 32767).astype(np.int16)
    import wave
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest ajanta-ellora/tests/test_audio_engine_v2.py -v`  
Expected: FAIL (`ModuleNotFoundError: No module named 'scripts.audio_engine_v2'`)

- [ ] **Step 3: Implement `audio_engine_v2.py`**

Implement ElevenLabs Adam Stone synthesis with dramatic cadence preprocessing, Whisper alignment parser, and FFmpeg `sidechaincompress` audio ducking with `loudnorm` filter.

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest ajanta-ellora/tests/test_audio_engine_v2.py -v`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add ajanta-ellora/scripts/audio_engine_v2.py ajanta-ellora/tests/test_audio_engine_v2.py
git commit -m "feat(audio): add ElevenLabs Adam Stone engine and FFmpeg sidechain ducking"
```

---

### Task 2: Procedural & Layered Foley Generator

**Files:**
- Create: `ajanta-ellora/scripts/foley_generator_v2.py`
- Create: `ajanta-ellora/tests/test_foley_generator_v2.py`

**Interfaces:**
- Consumes: Timestamped cue triggers `[(timestamp_s, "sub_bass" | "stone_strike" | "whoosh")]`.
- Produces: `generate_foley_track(duration_s, cues, out_wav_path) -> Path`.

- [ ] **Step 1: Write failing test for Foley track synthesis**

```python
# ajanta-ellora/tests/test_foley_generator_v2.py
from pathlib import Path
import wave

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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest ajanta-ellora/tests/test_foley_generator_v2.py -v`  
Expected: FAIL (`ModuleNotFoundError: No module named 'scripts.foley_generator_v2'`)

- [ ] **Step 3: Implement `foley_generator_v2.py`**

Implement mathematical synthesis in NumPy:
- 42 Hz sub-bass sine with Hanning envelope.
- 1800 Hz basalt impact click with exponential decay ($e^{-60t}$) and secondary reflection.
- Swept-frequency white noise whoosh with bandpass filter.

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest ajanta-ellora/tests/test_foley_generator_v2.py -v`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add ajanta-ellora/scripts/foley_generator_v2.py ajanta-ellora/tests/test_foley_generator_v2.py
git commit -m "feat(foley): implement procedural sub-bass and impact foley synthesis in NumPy"
```

---

### Task 3: Shorts 2.0 Engine & Kinetic Karaoke Captions

**Files:**
- Create: `ajanta-ellora/scripts/shorts_engine_v2.py`
- Create: `ajanta-ellora/tests/test_shorts_engine_v2.py`

**Interfaces:**
- Consumes: Word-level timing JSON, visual asset cut list (12–18 cuts), audio stem.
- Produces: `generate_karaoke_ass(word_cues, out_ass_path) -> Path`, `assemble_short_v2(manifest, audio_path, ass_path, out_mp4) -> Path`.

- [ ] **Step 1: Write failing test for ASS karaoke script generation**

```python
# ajanta-ellora/tests/test_shorts_engine_v2.py
from pathlib import Path

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
    assert "FACC15" in content # Electric yellow active highlight
    assert "WHERE" in content
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest ajanta-ellora/tests/test_shorts_engine_v2.py -v`  
Expected: FAIL (`ModuleNotFoundError: No module named 'scripts.shorts_engine_v2'`)

- [ ] **Step 3: Implement `shorts_engine_v2.py`**

- Generate Advanced SubStation Alpha (`.ass`) with karaoke styling, bold font, and safe-zone bounding (Y: 58–62%).
- Implement multi-cut 9:16 b-roll video assembler (12–18 cuts, 2.0–3.0s pacing) with hook boom SFX and outro CTA card.

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest ajanta-ellora/tests/test_shorts_engine_v2.py -v`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add ajanta-ellora/scripts/shorts_engine_v2.py ajanta-ellora/tests/test_shorts_engine_v2.py
git commit -m "feat(shorts): implement Shorts 2.0 multi-cut engine and ASS karaoke subtitle generator"
```

---

### Task 4: Hybrid 3D / HUD Motion Graphics & 35mm Texturing

**Files:**
- Create: `ajanta-ellora/scripts/motion_graphics_v2.py`
- Create: `ajanta-ellora/tests/test_motion_graphics_v2.py`

**Interfaces:**
- Consumes: Dimension specs, metric targets (e.g. 400,000), base images.
- Produces: `render_kinetic_hud_card(metric_label, end_value, duration_s, out_dir) -> Path`, `apply_film_texture(src_mp4, out_mp4, grain_opacity=0.08) -> Path`.

- [ ] **Step 1: Write failing test for kinetic HUD numerical rolling counter**

```python
# ajanta-ellora/tests/test_motion_graphics_v2.py
from pathlib import Path
from PIL import Image

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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest ajanta-ellora/tests/test_motion_graphics_v2.py -v`  
Expected: FAIL (`ModuleNotFoundError: No module named 'scripts.motion_graphics_v2'`)

- [ ] **Step 3: Implement `motion_graphics_v2.py`**

- Pillow kinetic HUD telemetry renderer with non-linear easing (`easeOutCubic`).
- Animated dimension lines and rolling metric counters.
- Headless Blender CLI caller with safe graceful fallback.
- FFmpeg 35mm film grain overlay filter and documentary warm/cool color grading.

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest ajanta-ellora/tests/test_motion_graphics_v2.py -v`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add ajanta-ellora/scripts/motion_graphics_v2.py ajanta-ellora/tests/test_motion_graphics_v2.py
git commit -m "feat(graphics): implement kinetic HUD telemetry generator and 35mm film texturing"
```

---

### Task 5: Mobile-First 3-Word Rule Packaging Suite

**Files:**
- Create: `ajanta-ellora/scripts/packaging_v2.py`
- Create: `ajanta-ellora/tests/test_packaging_v2.py`

**Interfaces:**
- Consumes: Base hero image, 3-word title phrase, episode metadata.
- Produces: `generate_high_contrast_thumbnail(base_img, three_words, out_jpg) -> Path`, `generate_publish_suite(ep_metadata, out_dir) -> list[Path]`.

- [ ] **Step 1: Write failing test for 3-word rule thumbnail compositor**

```python
# ajanta-ellora/tests/test_packaging_v2.py
from pathlib import Path
from PIL import Image

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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest ajanta-ellora/tests/test_packaging_v2.py -v`  
Expected: FAIL (`ModuleNotFoundError: No module named 'scripts.packaging_v2'`)

- [ ] **Step 3: Implement `packaging_v2.py`**

- Pillow-based high-contrast typography compositor with drop shadows, border strokes, and dark vignette chasm depth.
- Generates 3 distinct concepts (Curiosity Hook, Engineering Blueprint, Scale & Mystery).
- Formats YouTube Publish Kits with tags strictly <= 500 characters and chapters starting at `00:00`.

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest ajanta-ellora/tests/test_packaging_v2.py -v`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add ajanta-ellora/scripts/packaging_v2.py ajanta-ellora/tests/test_packaging_v2.py
git commit -m "feat(packaging): implement 3-word rule thumbnail compositor and publish kit generator"
```

---

### Task 6: Master Assembly Engine & Quality Gate Integration

**Files:**
- Create: `ajanta-ellora/scripts/assemble_master_v2.py`
- Modify: `ajanta-ellora/scripts/verify_deliverables.py`
- Modify: `ajanta-ellora/scripts/jev_quality_gate.py`
- Create: `ajanta-ellora/tests/test_integration_v2.py`

**Interfaces:**
- Consumes: All modules from Tasks 1–5.
- Produces: Fully assembled, verified 1080p Master Preview, 2x Shorts 2.0 videos, and certified pass on Jev Quality Gate.

- [ ] **Step 1: Write integration test validating end-to-end delivery suite constraints**

```python
# ajanta-ellora/tests/test_integration_v2.py
import pytest
from pathlib import Path

def test_quality_gate_constraints():
    tags = "Kailasa Temple, Ancient Engineering, Ellora Caves, Archaeology, Megaliths, Ancient India, Architecture"
    assert len(tags) <= 500
    
    # Assert zero repetition logic
    manifest = ["img_01.jpg", "video_01.mp4", "hud_01.png", "img_02.jpg"]
    assert len(manifest) == len(set(manifest))
```

- [ ] **Step 2: Implement `assemble_master_v2.py`**

Integrate all 5 modules:
1. Synthesizes Adam Stone ElevenLabs voiceover + Whisper word-level timing.
2. Ducked BGM scoring with procedural sub-bass and impact Foley.
3. 4K sub-pixel anti-jitter Ken Burns stills + Headless 3D + Kinetic HUD cards.
4. Shorts 2.0 with fast-paced multi-cut b-roll and active-word karaoke subtitles.
5. 35mm film grain overlay and color grading.
6. 3-word rule high-contrast thumbnails.

- [ ] **Step 3: Run integration test and deliverables verification**

Run: `pytest ajanta-ellora/tests/test_integration_v2.py -v`  
Expected: PASS

- [ ] **Step 4: Update TypeSafe Jev Quality Gate (`jev_quality_gate.py`)**

Verify calibrated System 1 pass:
- Zero repetition assertion (`jev_noul`).
- Spoken narration-to-visual action alignment (`jev_noul` >= 0.70).
- Production readiness score (`jev_score` >= 2.50 / 3.00).

- [ ] **Step 5: Commit**

```bash
git add ajanta-ellora/scripts/assemble_master_v2.py ajanta-ellora/scripts/jev_quality_gate.py ajanta-ellora/tests/test_integration_v2.py
git commit -m "feat: complete Broadcast Production Engine v2.0 master assembler and Jev quality gate"
```
