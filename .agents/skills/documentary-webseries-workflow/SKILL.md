---
name: documentary-webseries-workflow
description: End-to-end production workflow for creating high-retention documentary web-series, micro-beat storyboards, AI image/video prompts, Google Flow I2V batching, OpenMontage packaging, and companion YouTube Shorts funnels.
---

# Documentary Webseries Production Workflow

Use this skill when designing, scripting, rendering, or packaging long-form YouTube documentary episodes, historical/technical web-series, or educational video storyboards.

## 1. Episode Architecture & Monetization Pacing
- Target runtime: 7 to 10 minutes (optimal for YouTube mid-roll ad placement and completion rate).
- Pacing math: $N = \text{Total Seconds} / \text{Average Cut Duration}$ (typically 5.5s–6.5s per shot).
- 5-Minute Video (~300s): Minimum 50–60 micro-beats.
- 7.5-Minute Video (~450s): Minimum 70–80 micro-beats.
- 10-Minute Video (~600s): Minimum 90–120 micro-beats.

## 2. The Smart Production Pyramid (Budget & API Optimization)
To prevent massive API bills on pay-as-you-go image and video generators:
- **Strict 1080p Resolution Constraint (No 4K)**: Always render and prompt for standard **1080p Full HD (1920x1080)**. Avoid 4K to preserve user generation credits and rendering resources.
- **The Global Zero-Repetition Invariant (Videos & Stills)**: Never repeat the same still image OR the same action video clip multiple times within an episode. To achieve 100% visual variety and high retention at zero extra API cost, combine:
  1. **Master Hero Images (35–45 unique stills)**: Photorealistic 16:9 cinematic stills used once per episode.
  2. **Strict Structural Infographic Ceiling (1–2 cuts max)**: Limit technical infographics to at most 1–2 genuine structural engineering diagrams (e.g., tensile load arch elevation, subterranean void mechanics). Zero text/blueprint dossier cards.
  3. **The Void-Filling Law**: Removing text cards never shortens the video. Video duration is locked to sentence-level cues (0.00ms drift). All void cuts are filled 1:1 with photorealistic stills, Google Flow action captures, or authentic museum historical scans.
  4. **Cross-Episode Archive Reuse & Museum Scans (8–10 cuts)**: Legitimate historical public-domain archive scans (royal copper charters, 19th-century survey plates) and series continuity assets.
  5. **Selective AI Action Videos (7–10 unique clips)**: High-impact kinetic action clips (sparks, steam, fire, smoke, molten wax, water drops), each deployed at its narrative peak.
- **Zero-Cost Motion Graphics & Archival**: 15–20 cuts come from 2D animated blueprints, statistical metric cards ("140 MPa"), historical public domain archival photos, and Google Earth 3D flyovers.
- **Result**: Slashes API costs by ~80–85% while giving the documentary a professional BBC / National Geographic hybrid aesthetic with ZERO visual repetition.

## 3. Google Flow Image-to-Video Workflow
1. **Isolation for Fast Batching**:
   - Copy all images ending in `_GENERATE_VIDEO.jpg` to `assets/episode-XX/google_flow_input_images/`.
   - The user can drag and drop these images in parallel to Google Flow.
2. **Target Moments**:
   - Focus on kinetic physics and particle reactions (e.g., water droplet splashing in basin, volcanic magma flowing from fissure, surveyor striking basalt cliff with mallet, blacksmith striking steel on anvil, surveyors snapping chalk cord on summit, hand stamping seal into molten red wax, sledgehammer striking basalt bedrock).
3. **Ingestion**:
   - Store generated video clips in `assets/episode-XX/google_flow_videos/` (or `videos/`).
   - Match by prefix (e.g., `ep01_05`, `ep01_11`, `ep01_22`).
   - Autonomously normalize platform-downloaded files with timestamp suffixes (e.g., `scene01.mp4_20261006...mp4`) into clean canonical target filenames (`epXX_gf_01_...` or `gf_01_...`) while retaining raw files untouched.
4. **Asset Sanitization & Renaming**:
   - Immediately rename downloaded video clips with clean, descriptive ASCII names (e.g., `gf_03_hammer_chisel.mp4`, `gf_04_bonfire_flames.mp4`) to avoid non-ASCII encoding artifacts (``, `._`) that break build scripts.

0. **Pre-Render Manifest, Uniqueness Assertion & Spoken-Word Sync**:
   - **Narration-Visual Spoken Anchor Invariant**: NEVER use uniform time-slicing (`total_dur / N` or equal weights). Parse the sentence-level cues from the corresponding `.srt` file. Every cut's duration and timestamp must align 1:1 with the exact sentence being spoken. Action videos (e.g. fire-setting, water quenching, hammer striking) MUST only appear when those exact words are spoken.
   - **Zero-Repetition Invariant**: Never rely on fuzzy keyword matching in `resolve_media_source()`. Explicitly define `(media_type, filename, weight, motion)` per cut.
   - Programmatically validate that every media item across the episode appears exactly once:
     ```python
     all_media = [item[1] for act in ACT_IMAGE_MAP.values() for item in act]
     duplicates = [x for x in all_media if all_media.count(x) > 1]
     assert not duplicates, f"FATAL ERROR: Duplicate media detected: {set(duplicates)}"
     ```
To guarantee zero stream decoding errors and eliminate non-monotonic DTS timestamp warnings:
1. **Sub-Segment Normalization**:
   - Video clips (Google Flow):
     ```bash
     ffmpeg -y -stream_loop -1 -i clip.mp4 \
       -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30,setpts=PTS-STARTPTS" \
       -r 30 -c:v libx264 -preset fast -crf 18 -pix_fmt yuv420p -an -t <cut_dur> sub.mp4
     ```
     *Note*: When muxing looped video with audio, ALWAYS pass `-t <dur>`. Never rely on `-shortest` with `-stream_loop -1`, which causes indefinite hangs in FFmpeg.
   - Still images (4K Sub-Pixel Smooth Ken Burns - Zero Jitter):
     ```python
     # Continuous mathematical interpolation + 4K pre-scaling
     # Completely eliminates FFmpeg's 1-pixel rounding micro-jitter
     if motion == "zoom_in":
         vf = f"scale=3840:2160,zoompan=z='1.0+0.12*(on/{frames})':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1920x1080:fps={fps},vignette=angle=PI/5,eq=contrast=1.04:saturation=1.06"
     elif motion == "zoom_out":
         vf = f"scale=3840:2160,zoompan=z='1.12-0.12*(on/{frames})':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1920x1080:fps={fps},vignette=angle=PI/5,eq=contrast=1.04:saturation=1.06"
     elif motion == "pan_right":
         vf = f"scale=3840:2160,zoompan=z=1.10:x='(iw-iw/zoom)*(on/{frames})':y='ih/2-(ih/zoom/2)':d={frames}:s=1920x1080:fps={fps},vignette=angle=PI/5,eq=contrast=1.04:saturation=1.06"
     elif motion == "pan_left":
         vf = f"scale=3840:2160,zoompan=z=1.10:x='(iw-iw/zoom)*(1-on/{frames})':y='ih/2-(ih/zoom/2)':d={frames}:s=1920x1080:fps={fps},vignette=angle=PI/5,eq=contrast=1.04:saturation=1.06"
     elif motion == "tilt_down":
         vf = f"scale=3840:2160,zoompan=z=1.10:x='iw/2-(iw/zoom/2)':y='(ih-ih/zoom)*(on/{frames})':d={frames}:s=1920x1080:fps={fps},vignette=angle=PI/5,eq=contrast=1.04:saturation=1.06"
     elif motion == "slow_drift":
         vf = f"scale=3840:2160,zoompan=z='1.0+0.07*(on/{frames})':x='(iw/2-(iw/zoom/2))+(iw*0.02)*(on/{frames})':y='ih/2-(ih/zoom/2)':d={frames}:s=1920x1080:fps={fps},vignette=angle=PI/5,eq=contrast=1.04:saturation=1.06"
     ```
     Run with:
     ```bash
     ffmpeg -y -loop 1 -i image.jpg \
       -vf "<vf>,setsar=1,fps=30,setpts=PTS-STARTPTS" \
       -r 30 -c:v libx264 -preset fast -crf 18 -pix_fmt yuv420p -an -t <cut_dur> sub.mp4
     ```
2. **Independent Track Assembly**:
   - Concatenate all video sub-segments across the episode into a continuous video track (`temp_master_video_only.mp4`) with `-c copy -avoid_negative_ts make_zero`.
   - Concatenate all audio stems into a continuous audio track (`temp_master_audio_only.m4a`) with `-c:a aac -b:a 192k -ar 44100`.
3. **Single-Pass Final Muxing**:
   - Mux video and audio together in one pass:
     ```bash
     ffmpeg -y -i temp_master_video_only.mp4 -i temp_master_audio_only.m4a \
       -c:v copy -c:a copy -movflags +faststart episode_master.mp4
     ```
4. **Subtitle Timeline Scaling**:
   - Scale subtitle cue timestamps to match the exact duration of the final audio stems, ensuring 0ms drift between voice and captions.
5. **Null Sink Integrity Audit**:
   - Always run `ffmpeg -v error -i <video> -f null -` across all deliverables to confirm **0 packet errors** before declaring completion.
6. **Zero Media Repetition Verification Audit**:
   - Programmatically verify that every media item (video clips and still images) across all acts in the episode has an occurrence count of exactly 1, confirming 0 duplicate video clips and 0 duplicate stills.

## 5. Episode-Wise Folder Architecture & Complete Deliverable Suites
All production outputs must be structured strictly within self-contained episode folders (`ajanta-ellora/episode0X/`):
- `final_videos/`: Master preview (`episode_XX_master_preview.mp4`) + Short 1 + Short 2.
- `publish_kit/`: Master YouTube publish kit + Short 1 kit + Short 2 kit.
- `thumbnail/`: Master 16:9 thumbnail (<2 MB) + dedicated 9:16 vertical thumbnails for all companion Shorts (<2 MB each, mandatory from Episode 05 onward).
- `script_and_storyboard/`: Full episode script, acts breakdown, micro-beat storyboard.
- `audio/`: Full concatenated narration stem + individual act stems + shorts audio.
- `subtitles/`: Full `.srt` (sentence-level) + individual act `.srt` + shorts `.srt`.
- `images/`: Master hero stills, custom technical infographics, archive stills.
- `videos/`: Normalized action video clips (Google Flow / Runway).
- `google_flow_input_images/`: Clean, isolated image prompt files for video generation.
- `openmontage_bundle/`: Canonical OpenMontage export package (`video/output.mp4`, `metadata/`, `subtitles/`, `thumbnails/`).

## 6. YouTube Publishing Suites & SEO Limits (Master + 2 Shorts)
Every episode requires **3 distinct publish kits** in `publish_kit/`:
1. `episode-XX-youtube-publish-kit.md`
2. `short-01-...-youtube-publish-kit.md`
3. `short-02-...-youtube-publish-kit.md`

Each publish kit must contain:
- **5 High-CTR A/B Test Titles** (Curiosity, Scale, Documentary, Tech, Mobile-Optimized).
- **Comprehensive Video Description** with formatted chapter timestamps starting at `00:00` and companion video links.
- **YouTube SEO Tags (Studio Paste Ready)**: A comma-separated tag block verified to be **strictly under 500 characters** (YouTube's hard upload ceiling).
- **Strategic Pinned Comment**: Engaging community debate question or conversion funnel CTA.
- **Standalone Shorts Titles**: NEVER use episodic markers like `(Ep. 1)` or `Episode 2` in Shorts titles to protect viral algorithmic distribution.
- **Dedicated 9:16 Shorts Thumbnails (Mandatory from Episode 05 Onward)**:
  - Every companion Short must have a custom 9:16 vertical thumbnail (`1080x1920`, `< 2.0 MB`).
  - Follow the Mobile 3-Word Rule with bold, high-contrast hook typography.
  - File naming: `short_01_thumbnail_9x16.jpg`, `short_02_thumbnail_9x16.jpg` in `thumbnail/`.

## 7. Automated Deliverables Verification Gate (`verify_deliverables_ep0X.py`)
Never consider an episode complete until an automated audit script asserts 100% PASS on:
1. Audio stems & sync (drift < 100ms)
2. Subtitles monotonic timing & syntax
3. Visual assets presence (Master hero stills + technical infographics + Google Flow inputs)
   - Verify all companion Shorts 9:16 thumbnails exist, measure 1080x1920, and remain under 2.0 MB (from Episode 05 onward).
4. YouTube publish kits compliance (all 3 kits present with tags < 500 characters)
5. Video stream decoding integrity (0 packet decoding errors across Master and Shorts)
6. Zero media repetition invariant (every cut features an asset with occurrence count == 1)

## 8. TypeSafe Jev System 1 Quality Gate (`jev_quality_gate.py`)
Every episode must pass the calibrated **TypeSafe Jev System 1** decision engine audit:
1. **Zero Repetition Proposition (`jev_noul`)**: Micro-sanity assertion verifying 100% unique visual assets across the entire cut manifest.
2. **Narration-to-Visual Spoken Alignment (`jev_noul`)**: Calibrated check asserting that every action video cut matches the physical action spoken in the corresponding SRT subtitle line (probability >= 0.70).
3. **YouTube Tag Compliance (`jev_noul`)**: Verifying that tag blocks are strictly <= 500 characters.
4. **Production Readiness Score (`jev_score`)**: Ordinal tier evaluation (`unusable`, `needs_rework`, `acceptable`, `production_ready`) requiring >= 2.50 / 3.00 and high probability of `production_ready`.
