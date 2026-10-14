# The Curiosity Kills The Cat 🐾🎬
> **Algorithmic Documentary Web-Series Production Factory**  
> Automated, high-retention cinematic engineering & historical investigation documentaries engineered for YouTube growth and rapid monetization.

---

## 🏛️ Active Series: *The Subterranean Megastructures of Ajanta & Ellora*
An 8-part investigative engineering documentary web-series analyzing the geotechnical, hydraulic, architectural, and acoustic masterworks of 6th–8th century rock-cut India.

- **Episode 01**: *The Impossible Mountain* (The 400,000-Ton Top-Down Basalt Enigma)
- **Episode 02**: *The Fire-Quenched Basalt* (Thermal Shock Quarrying & Gravity-Fed Excavation)
- **Episode 03**: *The First Cut* (Zero-Tolerance Vimana Astronomy & Top-Down Alignment)
- **Episode 04**: *The Chasm of Kailasa* (The Great Spatial Void & Courtyard Isolation)
- **Episode 05**: *The Elephant Plinth* (Monolithic Basalt Compression & High-Relief Mastery)
- **Episode 06**: *The Bridge to Infinity* (Cantilevered Basalt Sky-Bridges & Structural Plaster)
- **Episode 07**: *The Secret Canyon of Waghur* (Ajanta's 700-Year Acoustic & Hydraulic Lab)
- **Episode 08**: *The Awakening of Harishena* (The Golden Age Frescoes & Canyon Dormancy)

---

## 🏗️ Repository Architecture

```text
thecuriousity-kills-thecat/
├── .agents/
│   ├── rules/
│   │   └── video-pacing-microbeats.md       # Micro-beat timing, anti-shaking & SEO invariants
│   └── skills/
│       ├── documentary-webseries-workflow/  # End-to-end production workflow
│       ├── higgsfield-*/                    # Visual brand, thumbnails, AI generation
│       └── hyperframes-*/                   # Programmatic video & animation compositing
├── ajanta-ellora/
│   ├── episode01/ to episode08/             # Self-contained episode production directories
│   │   ├── audio/                           # Narration stems (ElevenLabs Adam Stone, 0.00ms drift)
│   │   ├── final_videos/                    # Rendered 1080p Master + Companion Shorts
│   │   ├── google_flow_input_images/        # Isolated candidate stills for video animation
│   │   ├── images/                          # Master hero stills, infographics & museum archives
│   │   ├── openmontage_bundle/              # Canonical packaging metadata & chapters
│   │   ├── publish_kit/                     # Master & Shorts titles, descriptions, 500-char tags
│   │   ├── script_and_storyboard/           # 8-Act scripts & sentence-level micro-beat storyboards
│   │   ├── subtitles/                       # Sentence-level .srt cue sheets (Master + Shorts)
│   │   ├── thumbnail/                       # Master 16:9 + Companion 9:16 vertical thumbnails (<2MB)
│   │   └── videos/                          # Ingested action video clips (Google Flow / Veo / Runway)
│   └── scripts/                             # Production automation engines & CLI utilities
│       ├── audio_engine_v2.py               # EBU R128 audio synthesis & precision concatenation
│       ├── generate_elevenlabs_narration.py # Subtitle-to-speech synchronization pipeline
│       └── upload_episode07_to_youtube.py   # Resumable YouTube Data API v3 publisher
├── OpenMontage/                             # Submodule video assembly & compositing engine
├── .gitignore                               # Strict binary, raw still & credential exclusion rules
└── README.md                                # This document
```

---

## ⚡ The 6-Step Automated Production Pipeline

### Step 1: Research & 8-Act Micro-Beat Storyboard
Extract peer-reviewed architectural, geological, and historical literature into an 8-act narrative spine with strict 5.5–6.5s micro-beat cut frequency.
```bash
# Storyboard, sentence-level SRT cues, and prompt bible are generated under:
# ajanta-ellora/episodeXX/script_and_storyboard/
# ajanta-ellora/episodeXX/subtitles/
```

### Step 2: Narration Synthesis & Timestamp Alignment
Synthesize multi-act voiceover via ElevenLabs using the channel's canonical voice profile (**Adam Stone**). Word and character timestamps ensure monotonic $\le 10.0\text{ ms}$ concatenation drift.
```bash
python ajanta-ellora/scripts/generate_elevenlabs_narration.py --episode 07
```

### Step 3: Visual Asset Generation & Google Flow Video Gate
Generate 16:9 cinematic hero stills, PIL technical infographics, and isolate 7–10 action candidate stills for Image-to-Video generation.
```bash
python ajanta-ellora/scripts/generate_ep07_google_flow_stills.py
# Action stills are placed in: ajanta-ellora/episodeXX/google_flow_input_images/
# User generates video clips via Google Flow / Veo and places them in: ajanta-ellora/episodeXX/videos/
```

### Step 4: Companion Shorts Extraction (9:16 Vertical Funnel)
Extract 2 high-drama vertical companion Shorts per episode (25–58s), repurposing action video footage with frosted blurred backdrop framing, lower-third safe-zone subtitles, and cliffhanger CTAs.

### Step 5: Full HD Master Preview & Shorts Assembly
Assemble master Full HD 1080p (`1920x1080`) and 9:16 Shorts (`1080x1920`) using 4K anti-jitter sub-pixel zoompan (`scale=3840:2160 -> zoompan -> s=1920x1080`) and EBU R128 audio normalization.
```bash
python ajanta-ellora/scripts/assemble_episode_07_master.py
```

### Step 6: Automated YouTube API Publishing
Publish the full master documentary or companion Shorts to YouTube using OAuth 2.0 and the YouTube Data API v3 with complete SEO metadata, chapters, custom thumbnails, and SRT captions.
```bash
python ajanta-ellora/scripts/upload_episode07_to_youtube.py --privacy unlisted
```

---

## 🛡️ Production & Monetization Invariants

| Invariant | Standard | Enforcement |
| :--- | :--- | :--- |
| **Pacing / Cut Frequency** | 5.5s – 6.5s per cut | Mathematically mapped to sentence-level `.srt` cues. No uniform slicing. |
| **Audio Loudness** | EBU R128 Compliant | Integrated loudness: **-16 LUFS $\pm 1$ LUFS**, True Peak: **$< -1.5\text{ dBFS}$**. |
| **Concatenation Drift** | $\le 10.0\text{ ms}$ | Subtitle-to-audio drift monitored across all 8 acts. |
| **Zero Media Repetition** | 0 duplicate assets | Every single cut in the documentary features a unique visual. |
| **Anti-Shaking Motion** | 4K Sub-Pixel Smooth | Pre-scaled to 4K before integer zoompan to eliminate 30Hz micro-jitter. |
| **SEO Tags Ceiling** | $< 500$ characters | Hard cap enforced on master and Shorts publishing kits. |
| **Thumbnail Optimization** | $< 2.0\text{ MB}$ | High-contrast, Mobile 3-Word Rule hook typography. |
| **Music Clearance** | 100% Content ID Safe | Pre-cleared YouTube Audio Library or bespoke procedural synthesis only. |

---

## 📜 License & Channel Rights
Copyright © 2026 **The Curiosity Kills The Cat**. All rights reserved.  
Unauthorized re-upload or redistribution of generated video masters and original scripts is prohibited.