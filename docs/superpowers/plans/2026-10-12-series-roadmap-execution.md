# Series Roadmap Execution & Episode 07 Production Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Launch full production for Episode 07 (*The Secret Canyon of Waghur*) as the inaugural episode of Act II (The Lost Predecessor), enforcing the Google Flow video gate, 0 duplicate media invariant, and Content ID immunity. (Note: Episodes 01–05 are completed and published on YouTube; Episode 06 is fully assembled and audited).

**Architecture:** A multi-stage production pipeline adhering to `AGENTS.md` laws: Episode 07 script/storyboard generation, ElevenLabs Adam Stone narration synthesis (drift $\le 10$ ms), Google Flow prompt isolation, internal sound design bed mix, and companion Shorts metadata packaging.

**Tech Stack:** Python 3.11, FFmpeg, ElevenLabs API (`eleven_multilingual_v2`), YouTube Audio Library (Patrick Patrikios), OpenMontage, Pillow.

**Spec:** [`docs/superpowers/specs/2026-10-12-definitive-series-roadmap-design.md`](file:///C:/Sagar/Projects/thecuriousity-kills-thecat/docs/superpowers/specs/2026-10-12-definitive-series-roadmap-design.md)

## Global Constraints

- **Law 1 & 2 (Google Flow Video Gate)**: Mandatory hard stop after isolating 7–10 base action stills in `google_flow_input_images/`. Never render final master or claim complete without user video clips.
- **Law 3 (Zero Media Repetition Invariant)**: 0 duplicate visual cuts across Episode 07; 0 duplicate cuts from earlier episodes.
- **Law 4 & 8 (Audio Integrity & ElevenLabs Voice Profile)**: Voice ID `auq43ws1oslv0tO4BDa7` (Adam Stone), concatenation drift $\le 10.0\text{ ms}$, EBU R128 (-16 LUFS $\pm 1$ LUFS, True Peak $< -1.5\text{ dBFS}$).
- **Law 9 (Strict Infographic Ceiling)**: Max 1–2 structural engineering diagrams; 0% text dossier slides or bullet lists.
- **Law 11 (Zero Content ID Claim Invariant)**: Only YouTube Audio Library tracks (Patrick Patrikios) or bespoke procedural synthesis. 0% third-party stock audio.
- **Law 5 (YouTube Metadata Ceilings)**: SEO tags strictly $< 500$ characters. Thumbnails $< 2.0\text{ MB}$ with 3-word hook typography.

## Review Focus

1. **Narration Concatenation Drift**: Verify full concatenation drift remains $\le 10.0\text{ ms}$ against `.srt` cues.
2. **Audio Bed Ducking & Content ID**: Background music must be strictly from YouTube Audio Library, ducked by $\ge -16\text{ dB}$ under narration with zero sidechain fluttering.
3. **Google Flow Isolation**: All video candidate stills must exist exclusively in `episode07/google_flow_input_images/` with corresponding camera motion prompt sheet before halting.
4. **Shorts Safe Zone Subtitles**: Vertical subtitles must specify `PlayResX=1080,PlayResY=1920,FontSize=56,Outline=4,Alignment=2,MarginV=420`.
5. **No Visual Duplicates**: Verification script must confirm 0 asset hash collisions across the episode.

---

### Task 1: Scaffold Episode 07 Script & Micro-Beat Storyboard

**Files:**
- Create: `ajanta-ellora/episode07/script_and_storyboard/episode-07-the-secret-canyon-of-waghur.md`
- Test: `ajanta-ellora/tests/test_storyboard_structure.py`

**Interfaces:**
- Consumes: Historical research from `ajanta-ellora/ajanta-ellora-comprehensive-research.md` (Satavahana origins, Waghur gorge, podhi water cisterns)
- Produces: 55–65 micro-beats with timed duration, spoken narration, visual subject, and camera motion instructions.

- [x] **Step 1: Draft the 5-Act narrative script for Episode 07**
  Incorporate the Ep 07 Pivot Hook (*"Kailasa was not the beginning..."*), early Satavahana Theravada caves, basalt hydrology, and acoustic resonance.
- [x] **Step 2: Assign visual types per beat obeying Law 9**
  Ensure max 1–2 technical diagrams (hydraulic runoff gutter elevation), 0 text dossier cards, and 7–10 action video beats.
- [x] **Step 3: Validate micro-beat pacing**
  Verify cut durations range between 2.5s and 8.0s, matching sentence-level cadence.
- [x] **Step 4: Commit script and storyboard**
  Run: `git add ajanta-ellora/episode07/script_and_storyboard/; git commit -m "feat(ep07): Create Episode 07 script and micro-beat storyboard"`

---

### Task 2: Synthesize Episode 07 Narration & Generate Synchronized SRT

**Files:**
- Create: `ajanta-ellora/scripts/synthesize_episode_07_narration.py`
- Test: `ajanta-ellora/episode07/audio/narration/episode_07_full.srt`

**Interfaces:**
- Consumes: Spoken script from `episode-07-the-secret-canyon-of-waghur.md`, ElevenLabs API Key
- Produces: Character-aligned `.srt` cues and concatenated `episode_07_full_narration.wav`

- [ ] **Step 1: Write narration synthesis script**
  Use ElevenLabs profile Adam Stone (`auq43ws1oslv0tO4BDa7`, `eleven_multilingual_v2`, `stability=0.55`).
- [ ] **Step 2: Execute synthesis and generate sentence SRT**
  Run: `python ajanta-ellora/scripts/synthesize_episode_07_narration.py`
  Expected: Sentence cues generated with 0.00ms overlap.
- [ ] **Step 3: Verify concatenation drift**
  Confirm total concatenated audio drift $\le 10.0\text{ ms}$ relative to subtitle timestamps.
- [ ] **Step 4: Commit audio assets**
  Run: `git add ajanta-ellora/scripts/synthesize_episode_07_narration.py ajanta-ellora/episode07/audio/narration/episode_07_full.srt; git commit -m "feat(ep07): Synthesize official Adam Stone narration and generate SRT"`

---

### Task 3: Generate Episode 07 Base Visual Stills & Isolate Google Flow Inputs (Law 1 & 2 Gate)

**Files:**
- Create: `ajanta-ellora/scripts/generate_episode_07_visuals.py`
- Create: `ajanta-ellora/episode07/google_flow_input_images/GOOGLE_FLOW_PROMPT_SHEET.md`

**Interfaces:**
- Consumes: Storyboard asset requirements (7–10 action candidate stills, 50–55 master stills)
- Produces: Base 16:9 stills, isolated images in `google_flow_input_images/`, and copy-paste prompt table.

- [ ] **Step 1: Write visual asset prompt generator**
  Generate prompts for Waghur gorge landscape, early chaitya cave portals, water cisterns, and drone fly-throughs.
- [ ] **Step 2: Generate 16:9 stills and copy action candidates to `google_flow_input_images/`**
  Isolate 7–10 candidate files (`ep07_gf_01` to `ep07_gf_10`) into `ajanta-ellora/episode07/google_flow_input_images/`.
- [ ] **Step 3: Generate clean Google Flow prompt markdown sheet**
  Create a markdown table with filename, spoken timestamp, camera motion prompt, and duration.
- [ ] **Step 4: Mandatory Hard Stop (Law 1 Gate)**
  Announce to user that action stills are ready in `google_flow_input_images/` and wait for user video generation.
- [ ] **Step 5: Commit prompt sheet and generation script**
  Run: `git add ajanta-ellora/scripts/generate_episode_07_visuals.py ajanta-ellora/episode07/google_flow_input_images/; git commit -m "feat(ep07): Isolate Google Flow base stills and generate prompt sheet"`

---

### Task 4: Package Episode 07 YouTube Publish Kit & Companion Shorts Funnel

**Files:**
- Create: `ajanta-ellora/episode07/publish_kit/master_publish_kit.md`
- Create: `ajanta-ellora/episode07/publish_kit/short_01_the_horseshoe_canyon_publish_kit.md`
- Create: `ajanta-ellora/episode07/publish_kit/short_02_ancient_water_engineering_publish_kit.md`

**Interfaces:**
- Consumes: Episode 07 metadata, virality hooks, SEO keywords
- Produces: Titles, descriptions, pinned comments, tag lists (< 500 chars), and thumbnail specs.

- [ ] **Step 1: Write master documentary publish kit**
  Include 3-Word hook thumbnail concept, description, and SEO tags verified $< 500$ chars.
- [ ] **Step 2: Write Companion Short 01 publish kit**
  Repurpose Google Flow drone gorge footage; vertical subtitle cues and $< 500$ char tags.
- [ ] **Step 3: Write Companion Short 02 publish kit**
  Focus on ancient monsoon hydraulic engineering; vertical subtitle cues and $< 500$ char tags.
- [ ] **Step 4: Commit publish kits**
  Run: `git add ajanta-ellora/episode07/publish_kit/; git commit -m "docs(ep07): Create YouTube publish kit and companion shorts metadata"`
