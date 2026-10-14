# Broadcast Production Engine v2.0 Design Specification
**Channel**: [Curiosity Kills the Cat](https://www.youtube.com/@TheCuriosityKillsTheCat) (`@TheCuriosityKillsTheCat`)  
**Date**: 2026-10-05  
**Status**: APPROVED DESIGN SPECIFICATION  

---

## 1. Executive Summary & Goals

### 1.1 Context
*Curiosity Kills the Cat* produces long-form historical and archaeological engineering documentaries and companion YouTube Shorts. Recent analysis of channel performance revealed a key finding: a companion Short (*"Where Did 400,000 Tons of Basalt Rock Disappear?"*) achieved **1,020+ organic views**, demonstrating strong audience appetite for ancient engineering mysteries. However, long-form episodes (Episodes 01–03) and companion Shorts have suffered from low retention and view-through rates due to five core production bottlenecks:
1. **Robotic Voiceover**: Using free Edge-TTS (`en-US-ChristopherNeural`) without natural cadence or emotional range.
2. **Missing Audio Bed**: Long-form videos lacked background music (BGM) and sound effects (Foley), creating an immersion-breaking dry lecture feel.
3. **Static Shorts**: Previous Shorts utilized a single static image pan-zoomed for 45–58 seconds with zero subtitles, zero cuts, and zero sound effects.
4. **"Slideshow" Visuals**: Long-form episodes relied on ~85–90% still images with Ken Burns motion, lacking kinetic energy, animated telemetry, or high-impact motion graphics.
5. **AI Plastic Aesthetic**: Raw Imagen 3 / Midjourney stills exhibited a smooth digital sheen without organic film texture or unified color grading.

### 1.2 Objective
Build and deploy the **Broadcast Production Engine v2.0**, an end-to-end automated production suite that elevates channel releases to **BBC / Lemmino / Vox** caliber.

### 1.3 Key Metrics & Success Criteria
* **Audio Quality**: 100% ElevenLabs voiceover (**Adam Stone**), broadcast loudness normalized (-16 LUFS, -1.5 dBFS True Peak), dynamic music ducking (-16 dB under speech), and procedural Foley (0 ms desync).
* **Shorts Retention**: Shorts transformed from 1 static image into fast-paced 12–18 micro-cut videos (2.0–3.0s cut frequency) with word-by-word kinetic karaoke subtitles and hook impact SFX.
* **Visual Polish**: 3D spatial cutaways via headless Blender scripts, kinetic HUD dimension cards with smooth easing curves, and an organic 35mm film grain overlay.
* **Mobile CTR**: High-contrast thumbnail generator adhering to the "3-Word Rule", rim-lit focal subjects, and automated A/B/C testing packages.
* **Automated Quality Gate**: 100% pass rate on TypeSafe Jev System 1 assertions (`jev_noul` and `jev_score` >= 2.50 / 3.00).

---

## 2. System Architecture & Subsystems

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        BROADCAST PRODUCTION PIPELINE v2.0                              │
└───────────────────────────────────┬────────────────────────────────────────────────────┘
                                    │
    ┌───────────────────────────────┴───────────────────────────────┐
    ▼                                                               ▼
┌──────────────────────────────────────────────┐  ┌──────────────────────────────────────┐
│          1. NARRATION & SOUND SUITE          │  │       2. VISUALS & 3D MOTION         │
├──────────────────────────────────────────────┤  ├──────────────────────────────────────┤
│ • ElevenLabs: Adam Stone (British, smooth)   │  │ • Pillar A: Master Hero Stills       │
│ • Whisper: Word-level timestamp extraction   │  │   (4K Ken Burns sub-pixel anti-jitter)│
│ • Music Library: Act-based BGM scoring       │  │ • Pillar B: Headless Blender 3D cuts │
│ • FFmpeg Sidechain: Auto-ducking (-16 dB)    │  │ • Pillar C: Kinetic PIL HUD Overlays  │
│ • Foley Generator: Procedural sub-bass rumble│  │ • Google Flow: High-impact video clips│
│   and stone/metal impact cues                │  │ • Cinematic 35mm film grain overlay   │
└──────────────────────┬───────────────────────┘  └──────────────────┬───────────────────┘
                       │                                             │
                       └──────────────────────┬──────────────────────┘
                                              │
                                              ▼
                             ┌──────────────────────────────────┐
                             │    3. MULTI-TRACK MASTER MUX     │
                             │ (FFmpeg Broadcast Conformance)   │
                             └────────────────┬─────────────────┘
                                              │
                    ┌─────────────────────────┴─────────────────────────┐
                    ▼                                                   ▼
┌──────────────────────────────────────────────┐  ┌──────────────────────────────────────┐
│            MASTER 16:9 DOCUMENTARY           │  │          SHORTS 2.0 ENGINE           │
├──────────────────────────────────────────────┤  ├──────────────────────────────────────┤
│ • Full 7–10 min narrative episode            │  │ • 50–58s vertical format (1080x1920) │
│ • 0.0ms audio-visual synchrony               │  │ • Fast 2.0–3.0s cut frequency         │
│ • Monotonic SRT subtitle cues                │  │ • Word-by-word highlighted karaoke    │
│ • Lower-third historical overlays            │  │   subtitles with pop animations       │
│ • High-contrast 3-word rule thumbnail        │  │ • Whoosh / boom Foley on hooks        │
│ • YouTube Publish Kit (Tags < 500 chars)     │  │ • Conversion CTA to Master Video      │
└──────────────────────────────────────────────┘  └──────────────────────────────────────┘
```

---

## 3. Detailed Component Specifications

### 3.1 Cinematic Audio Suite & Foley Compositor (`audio_engine_v2.py`)
1. **Narration Synthesis**:
   - **Provider**: ElevenLabs API (`eleven_multilingual_v2`).
   - **Voice**: Adam Stone (Voice ID: `auq43ws1oslv0tO4BDa7`), British accent, smooth and deep documentary resonance.
   - **Settings**: Stability = `0.55`, Similarity Boost = `0.78`, Style = `0.15`, Speaker Boost = `True`.
   - **Pacing Engine**: Automatic pre-processing of script sentences to insert strategic pause tags (`...`, em-dashes) for natural breathing room before dramatic reveals.
2. **Word-Level Whisper Synchronization**:
   - Transcribes generated audio via OpenAI Whisper to generate both:
     - Sentence-level `.srt` cues for long-form video timing.
     - Word-level timing arrays `[{"word": str, "start": float, "end": float}]` for kinetic karaoke subtitle rendering and exact Foley alignment.
3. **Curated Music Scoring & Auto-Ducking**:
   - **Library Hierarchy** (`assets/music_library/`):
     - `01_mystery_ambient/`: Eerie low drones and resonant singing bowls.
     - `02_historical_drama/`: Sparse ancient strings and medieval drone textures.
     - `03_tension_percussion/`: Rhythmic clock pulses and rising sub-bass pressure.
     - `04_climactic_reveal/`: Sweeping orchestral pads and reverberant bells.
   - **FFmpeg Sidechain Compression**:
     ```bash
     -filter_complex "[1:a]asplit=2[sc][vox];[0:a][sc]sidechaincompress=threshold=0.08:ratio=6:attack=80:release=450[ducked_bgm];[ducked_bgm][vox]amix=inputs=2:weights=1.0 1.0"
     ```
     BGM automatically ducks by -16 dB whenever Adam Stone speaks, smoothly swelling back to baseline (-18 dB to -22 dB) during pauses.
4. **Procedural & Layered Foley Generator**:
   - **Sub-Bass Seismic Rumble**: 40–50 Hz analog sine wave with Hanning window envelope timed to deep abyss camera plunges and tectonic trench cutaways.
   - **Impact Transients**: Metallic and basalt stone strikes (1.4–2.2 kHz) with rapid 60ms exponential decays timed to chisel hits, iron sledges, and rock falls.
   - **Kinetic Whooshes**: Low-frequency noise sweeps on rapid camera moves, scene transitions, and telemetry card reveals.
5. **Loudness Standards**:
   - Conforms audio to YouTube's broadcast delivery benchmark (-16 LUFS integrated loudness, -1.5 dBFS True Peak) via FFmpeg `loudnorm`.

---

### 3.2 Shorts 2.0 Engine (`shorts_engine_v2.py`)
1. **Dynamic B-Roll Pacing (12–18 Cuts per Short)**:
   - Eliminates single-image shorts. Enforces an average shot duration of **2.0s to 3.0s**.
   - **Asset Mix**:
     - 0.0s–2.0s: Immediate scroll-stopping hook with rapid motorized zoom punch-in (`z=1.00 -> 1.28`).
     - 6–8 Hero AI Stills with alternating directional pans and zooms.
     - 3–4 High-impact action video clips (fire bursts, quenching steam, chisel strikes).
     - 2–3 Kinetic blueprint telemetry cards (dimension brackets, metric gauges).
     - 1 Outro conversion card directing viewers to the master documentary.
2. **Word-by-Word Kinetic Karaoke Captions**:
   - **Format**: Advanced SubStation Alpha (`.ass`) with karaoke timing (`{\k}`) rendered directly into 1080x1920 video.
   - **Typography**: Ultra-bold sans-serif (`Montserrat Black` or `Segoe UI Bold`) in all caps.
   - **Position**: Vertical center (Y: 58%–62%), strictly adhering to YouTube Shorts UI safe zones (avoiding right-side icons and bottom title overlays).
   - **Highlighting**: 2–3 words displayed at once in crisp white with a 3px black stroke; active spoken word dynamically pops in **Electric Yellow (`#FACC15`)** with a 1.12x scale pulse.
3. **Sound Design Bed**:
   - 0.0s Sub-bass boom drop on the initial hook line.
   - Transition whooshes on every cut.
   - High-tempo documentary pulse (110–120 BPM) ducked cleanly under narration.
4. **Conversion Bridge**:
   - Last 4 seconds explicitly funnel viewers to the full episode.
   - Automated generation of YouTube Studio "Related Video" deep link and pinned comment copy.

---

### 3.3 Hybrid 3D / HUD Motion Graphics & Texturing (`motion_graphics_v2.py`)
1. **Headless Blender 3D Engine**:
   - Automates spatial scenes via headless Blender CLI (`blender -b -P script.py`):
     - **Trench Plunge**: Orbiting camera diving into the 33-meter perimeter chasm.
     - **Isometric Wireframe Cutaway**: Architectural model isolating the temple block from the mountain.
     - **Vimana Tier Progression**: Top-down reveals showing roof-first excavation stages.
   - Renders 1080p 30fps frames with PBR basalt textures and Freestyle wireframe edges.
2. **Kinetic PIL HUD Overlays & Telemetry**:
   - Non-linear easing curves (`easeOutCubic`, `easeInOutQuad`):
     - **Dimension Brackets**: Animated laser lines tracing length, width, and depth.
     - **Metric Counters**: Numerical values rapidly rolling up from 0 to 400,000 Tons with tactile click sound effects.
     - **Archival Glass Cards**: Lower-third provenance pills distinguishing verified Rashtrakuta royal charters from medieval *Katha-Kalpataru* folklore.
3. **35mm Film Grain Overlay & Color Grading**:
   - Applies an authentic 35mm organic film grain loop (`blend=all_mode=overlay:all_opacity=0.08`) over all stills and AI videos to eliminate the plastic AI look.
   - Cinematic documentary color grade: subtle vignette (`vignette=angle=PI/5`), warm amber stone highlights, and deep cool teal trench shadows.

---

### 3.4 Packaging & Mobile-First CTR Suite (`packaging_v2.py`)
1. **The 3-Word Rule Thumbnails**:
   - Restricts text overlay to 3–4 punchy, high-curiosity words (e.g., `"CARVED BACKWARDS?"`, `"NO SCAFFOLDING"`, `"400,000 TONS GONE"`).
2. **High-Contrast Subject Isolation**:
   - Automated cutout of the hero focal subject (monolithic stupi or master architect silhouette) with rim lighting and dark chasm background separation.
3. **Automated 3-Concept Generation**:
   - Concept A: *Curiosity / Drama* (Architect on sheer cliff overlooking glowing abyss).
   - Concept B: *Engineering Blueprint* (High-contrast 3D isometric cutaway with measurement lines).
   - Concept C: *Scale & Mystery* (Massive mountain comparison with bold typography).
4. **YouTube Publish Kits**:
   - 5 A/B title options per kit.
   - Studio-ready tag blocks strictly under **500 characters**.
   - Formatted chapter markers starting at `00:00`.

---

## 4. Error Handling & Quality Gate Assertions

### 4.1 Programmatic Acceptance Matrix
| Verification Check | Threshold / Target | Enforcement Mechanism |
| :--- | :--- | :--- |
| **Audio Drift** | < 10.0 ms | Mathematical comparison between master narration and sum of acts |
| **Audio Loudness** | -16.0 ± 1.0 LUFS, < -1.5 dBFS TP | FFmpeg `ebur128` filter audit |
| **Stream Integrity** | 0 decoding errors | FFmpeg null sink audit (`ffmpeg -v error -i ... -f null -`) |
| **Visual Uniqueness** | 100% unique assets (0 duplicate cuts) | Programmatic assertion `len(manifest) == len(set(manifest))` |
| **SRT Monotonicity** | 0 overlapping cues, monotonic start times | `verify_deliverables.py` parser |
| **YouTube Tag Ceiling** | Strictly <= 500 characters | String length assertion |
| **Thumbnail File Size** | Strictly < 2.0 MB | File size check |

### 4.2 TypeSafe Jev System 1 Quality Gate (`jev_quality_gate.py`)
- `jev_noul` assertion for 100% unique visual assets across the entire cut manifest.
- `jev_noul` assertion verifying that every action video cut coincides with the exact physical action spoken in the SRT line (probability >= 0.70).
- `jev_noul` assertion for YouTube tag limits.
- `jev_score` evaluation verifying overall Production Readiness >= 2.50 / 3.00.

---

## 5. File & Directory Structure

```
C:/Sagar/Projects/thecuriousity-kills-thecat/
├── ajanta-ellora/
│   ├── assets/
│   │   └── music_library/
│   │       ├── 01_mystery_ambient/
│   │       ├── 02_historical_drama/
│   │       ├── 03_tension_percussion/
│   │       └── 04_climactic_reveal/
│   ├── episode0X/
│   │   ├── audio/              # ElevenLabs Adam Stone stems + mixed tracks
│   │   ├── final_videos/       # Master 16:9 + 2x Shorts 2.0
│   │   ├── images/             # Hero stills, HUD overlays, textures
│   │   ├── explainers_3d/      # Blender 3D rendered sequences
│   │   ├── publish_kit/        # Master + Shorts publish kits
│   │   ├── subtitles/          # Sentence & word-level .srt / .ass
│   │   ├── thumbnail/          # 3-word rule high-contrast thumbnails
│   │   └── videos/             # Action clips (Google Flow / Runway)
│   └── scripts/
│       ├── audio_engine_v2.py
│       ├── shorts_engine_v2.py
│       ├── motion_graphics_v2.py
│       ├── packaging_v2.py
│       ├── assemble_master_v2.py
│       ├── verify_deliverables_v2.py
│       └── jev_quality_gate.py
```
