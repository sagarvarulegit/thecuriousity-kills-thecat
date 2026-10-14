---
description: Enforces micro-beat cut frequency, anti-shaking smooth motion standards, cost-effective asset batching, asset arrival prerequisites, and YouTube title/SEO constraints.
trigger: model_decision
---

# Video Pacing, Micro-Beat & Budget Optimization Requirements

When creating video scripts, storyboards, visual prompt bibles, or rendering pipelines for videos with a target duration:

## 1. The Micro-Beat Cut Frequency (Pacing Math)
- Never provide only high-level macro-scenes for videos longer than 60 seconds.
- Maintain the **5.5 to 6.5 second average cut rule** (essential for high retention on YouTube):
  - 5-Minute Video (~300s): Minimum 50–60 micro-beats.
  - 7.5-Minute Video (~450s): Minimum 70–80 micro-beats.
  - 10-Minute Video (~600s): Minimum 90–120 micro-beats.

## 2. The Smart Production Pyramid (API Budget Optimization)
**70–80 micro-beats does NOT mean 70–80 separate AI image or video API calls.** To prevent massive API cost blowouts:

0. **Strict 1080p Master Resolution & Asset Prerequisite**:
   - All master video renders and video generation prompts must target standard **1080p Full HD (1920x1080)**.
   - Never generate or request 4K video rendering; 1080p conserves generation credits, ensures fast processing, and matches standard YouTube consumption.
   - **CRITICAL ASSET PREREQUISITE**: NEVER assemble or render final preview videos based on still image placeholders when user-provided action videos (Google Flow / Veo / Runway) are pending. Always await actual video clips to avoid wasted tokens, effort, and re-renders.

1. **The Global Zero-Repetition Invariant (Videos & Stills) & 3-Pillar Visual Diversity**:
   - **STRICT ZERO-REPETITION INVARIANT (VIDEOS & STILLS)**: NEVER repeat the same still image OR the same video clip multiple times within the episode. Repeating action video clips breaks immersion immediately; every action clip generated (Google Flow / Runway / Veo) must appear EXACTLY ONCE at its most impactful narrative beat. Every single cut across the entire video must feature a distinct visual asset.
   - **Mandatory Explicit 1:1 Media Manifest**: Assembly scripts must explicitly declare `(media_type, exact_filename, weight, motion)` for every cut. Fuzzy keyword resolution or substring matching at assembly time is strictly forbidden.
   - **Asset Filename Sanitization**: Ingested AI video files must be immediately normalized to clean, standard ASCII identifiers (`gf_01_...`, `gf_02_...`) before assembly to prevent non-ASCII characters or ellipsis artifacts (``, `._`) from breaking pipelines.
   - **Pre-Render Uniqueness Assertion**: Assembly scripts must programmatically assert `len(manifest) == len(set(manifest))` and abort if duplicate media exists before invoking FFmpeg.
   - **The 3-Pillar Visual Diversity Formula (45–55 Unique Scenes at Zero Extra Cost)**:
      - **Pillar A: Master Hero Images (35–45 unique visuals)**: High-production-value photorealistic 16:9 cinematic stills used once per episode.
      - **Pillar B: Strict Structural Infographic Ceiling (1 to 2 cuts max)**: Limit technical infographics to at most 1–2 genuine structural/engineering diagrams (e.g. tensile load-bearing arches, subterranean underbelly excavation mechanics). ABSOLUTE BAN on text-heavy slides, data tables, or bullet-point blueprint dossier cards in final video edits.
      - **Pillar C: Cross-Episode Universe Archive (8–10 cuts)**: Legitimate public-domain historical museum scans (royal copper charters, 19th-century survey plates, colonial sketches) or earlier continuity assets.
    - **The Void-Filling Law**: Removing text cards must NEVER shorten video duration or leave blanks. Video length is mathematically derived from sentence-level `.srt` cues and master audio (0.00ms drift). All void cuts must be filled 1:1 with photorealistic stills, Google Flow action captures, or authentic museum historical scans.
   - **Pacing Calibration**: Hold still shots for a natural **7.0s–9.5s documentary beat** with buttery-smooth 4K sub-pixel motorized dolly motion (`z=1.00 -> 1.12`).
   - **Sub-Pixel Anti-Jitter Mandate**: FFmpeg `zoompan` rounds coordinates to whole integers every frame, creating a severe 30 Hz micro-jitter/shudder if run at 1080p. All still image animations MUST be pre-scaled to 4K (`scale=3840:2160`) before `zoompan`, then downscaled to `s=1920x1080` (or `2160:3840` -> `1080x1920` for Shorts), using continuous `(on/frames)` equations.
   - Use gentle motorized dolly motion (1.00 to 1.12 max zoom factor) with subtle lens vignette (`vignette=angle=PI/5`) and documentary color grading.
   - Name and tag these images explicitly with `_PAN_ZOOM.jpg` in their filename.

2. **Selective AI Video Generation (Google Flow / Runway Gen-3 / Kling)**:
   - Animate only **7 to 10 high-impact action/physics moments** per episode (e.g., hammer impact sparks, water quenching steam, molten wax dripping, fire explosions, windblown smoke).
   - Do NOT animate talking characters or static rooms.
   - Name and tag these images explicitly with `_GENERATE_VIDEO.jpg` in their filename, and isolate them into a dedicated `google_flow_input_images/` folder for rapid parallel batch upload.

3. **Zero-Cost Visual Assets (15 to 20 Cuts)**:
   - Include kinetic motion graphics, 2D blueprint schematics, statistical callouts ("140 MPa", "400,000 Tons"), and public domain archival/satellite footage (Google Earth 3D, ASI archives, British Library sketches).

## 3. The Narration-to-Visual Spoken Anchor Law (Zero-Desync Invariant)
- **STRICT PROHIBITION OF UNIFORM TIME-SLICING**: Never divide acts or scenes into uniform time slices (`duration / N` or equal weights). Uniform slicing is the root cause of narration-visual desync.
- **SRT Sentence-Level Cue Binding**:
  - Every cut's duration and timestamp range MUST be mathematically derived from the sentence-level subtitle cues (`.srt`).
  - Action visuals (e.g. fire-setting, water quenching, chisel striking, sledgehammer swinging) MUST coincide with the exact second that specific action or concept is spoken in the narration.
  - Generic ambient shots must be relegated to purely contextual or transitional spoken lines.
- **Verification Rule**: Before rendering, verify that every visual asset's subject matches the narration sentence occurring in that time slice.

## 4. Episode-Wise Self-Contained Folder Architecture
Every episode must reside entirely within its dedicated self-contained folder (`ajanta-ellora/episode0X/`) with these exact standardized subfolders:
- `final_videos/`: Master preview (`episode_XX_master_preview.mp4`) + Short 1 + Short 2.
- `publish_kit/`: Master YouTube publish kit + Short 1 kit + Short 2 kit.
- `thumbnail/`: Master 16:9 thumbnail (<2 MB) + dedicated 9:16 vertical thumbnails for all companion Shorts (<2 MB each, mandatory from Episode 05 onward).
- `script_and_storyboard/`: Full episode script, acts breakdown, micro-beat storyboard.
- `audio/`: Full concatenated narration stem + individual act stems + shorts audio.
- `subtitles/`: Full `.srt` (sentence-level) + individual act `.srt` + shorts `.srt`.
- `images/`: Master hero stills, custom technical infographics, archive stills.
- `videos/`: Normalized action video clips (Google Flow / Runway).
- `google_flow_input_images/`: Clean, isolated image prompt files for video generation.
- `openmontage_bundle/`: Canonical OpenMontage export package.

## 5. Micro-Beat Output Standard & Complete Deliverables Gate
Every episode production bible must provide:
- **Master Image Batch Sheet**: A concise table mapping the 20–25 Master AI prompts directly to the micro-beats they satisfy.
- **Granular Micro-Beats**:
  - `Beat #` & `Timestamp Range` (derived from SRT cue)
  - `Shot Classification` (Wide, Medium, Close-Up, Macro, Drone, Tracking)
  - `Exact Narration Sentence` timed to that cut
  - `Visual Image Prompt` (16:9 for Midjourney v6 / Flux / Gemini Imagen 3 with style anchor)
  - `Motion Video Prompt` (Camera and subject movement)
  - `SFX / BGM Cue`
-- **Companion Shorts Funnels**:
  - 2 companion 9:16 vertical Shorts scripts (30–42s) with dedicated hooks, visual prompts, and cliffhanger CTAs pointing directly to YouTube's native "Related Video" button.
  - **0.5-SECOND CONFLICT HOOK INVARIANT**: The opening frame and very first spoken line (0:00–0:01) must present active human conflict, physical catastrophe, or a survival paradox (e.g., "1,000 Men Tried to Destroy This Temple", "Monsoon Floods Tried to Drown This Monastery"). Never open with passive or academic narration ("This canyon holds 30 temples...").
  - **SUB-48S DURATION CEILING**: Shorts must target 30–42 seconds and terminate strictly before 48 seconds to eliminate the steep 46–50s drop-off cliff revealed by YouTube Studio retention analytics.
  - **SHORTS-TO-LONGFORM RELATED VIDEO CLIFFHANGER (LAW 12)**: The final 3.0 seconds of every Short must NOT be a generic outro or sign-off. It must terminate on an unresolved cognitive cliffhanger with on-screen directive graphics and spoken prompt explicitly pointing to the native "Related Video" pill linking the full documentary episode.
  - **DYNAMIC MULTI-BEAT EDITING (0% INFOGRAPHICS)**: Every Short must contain 5–7 micro-beat cuts (every 2.5s to 7.5s), splicing 100% Google Flow action video clips and cinematic visuals. Never loop a single static image, and NEVER use technical infographic cards or text slides in Shorts.
  - **FROSTED BACKDROP FRAMING FOR 16:9 MEDIA IN SHORTS**: When repurposing 16:9 action footage into 9:16 vertical Shorts, NEVER center-crop if it cuts off key focal action. Use the frosted blurred backdrop layout (blurred 1080x1920 background with sharp 1080x608 foreground overlay) to preserve 100% of the cinematic frame.
  - **MOBILE SUBTITLE SAFE-ZONE PROTOCOL**: Subtitle styling in FFmpeg must explicitly declare `PlayResX=1080,PlayResY=1920,MarginV=420,FontSize=56,Outline=4` to anchor in the lower safe area above platform UI buttons without clipping.
  - **NO EPISODIC LABELS**: Never include `(Ep. 1)`, `(Ep. 2)`, or `Episode X` in Shorts titles. Frame each Short as a self-contained, shocking question or mystery to protect the 70%+ retention breakout threshold.
  - **MANDATORY DEDICATED 9:16 THUMBNAILS (EPISODE 05 ONWARD)**: Generate dedicated 9:16 vertical thumbnails (`short_01_thumbnail_9x16.jpg`, `short_02_thumbnail_9x16.jpg`) at 1080x1920 with high-contrast text hooks obeying the Mobile 3-Word Rule (<2.0 MB).
- **YouTube Publish Kit Constraints (Master + 2 Shorts)**:
  - **3-Way A/B/C Thumbnail Hook Testing**: Master publish kits must generate 3 distinct psychological thumbnail variants (Scale Contrast, Impossible Engineering Blueprint, and Extreme Curiosity Gap) ready for YouTube's native "Test & Compare" feature.
  - Title: 5 high-CTR A/B options per kit.
  - SEO Tags: Full comma-separated tag list strictly capped under **500 characters** (YouTube limit) for Master, Short 1, and Short 2.
  - Chapter Timestamps: Formatted starting at `00:00`.
- **Automated Verification & Jev Quality Gate Assertion Before Handoff**:
  - Run the automated deliverables audit script (`verify_deliverables_ep0X.py`) ensuring 100% pass across audio stems, SRT monotonic timing, stream integrity (0 packet errors), zero media repetition (45-55 cuts with 0 duplicates), and YouTube publish kit constraints.
  - Run the TypeSafe Jev System 1 Quality Gate (`jev_quality_gate.py`) ensuring calibrated verification on zero repetition (`jev_noul`), spoken narration-to-visual action alignment (`jev_noul` >= 0.70 across all action cuts), YouTube SEO tag compliance, and production readiness score (`jev_score` >= 2.50 / 3.00).

## 6. Series Supercut Compilation Standards (Anti-Reused Content YPP Defense)
When assembling multi-episode documentary feature films (e.g. 50–90+ minute series supercuts):
1. **Recap & Outro Stripping**: Programmatically trim intermediate Act 01 recap hooks and Act 08 cliffhanger outros between episodes. Insert 4-second Chapter Title Bumpers with deep sub-bass acoustic booms.
2. **Transformative Framing**: Prepend a 60–90s Master Cold Open and append an Epilogue Synthesis to ensure the feature is classified as a transformative Director's Cut documentary under YouTube's Partner Program policies.
3. **Cumulative Millisecond Timing**: Dynamically read exact trimmed durations via `ffprobe` to shift subtitle timestamps and chapter markers with 0.00ms drift.
4. **Theatrical Leveling**: Normalize full feature audio with FFmpeg `loudnorm=I=-14:TP=-1.5:LRA=11`.