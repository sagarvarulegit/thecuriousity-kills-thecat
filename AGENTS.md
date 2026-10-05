# Multi-Agent Operational Laws & Production Pipeline Rules

## 1. CRITICAL ASSET PREREQUISITE: THE GOOGLE FLOW VIDEO GATE
- **NEVER ASSEMBLE FINAL VIDEOS OR CLAIM "READY FOR PUBLICATION" WITHOUT USER ACTION VIDEOS**:
  - In our production workflow, every episode contains 7–10 high-impact kinetic action shots intended for Image-to-Video generation (via Google Flow / Veo / Runway / Kling).
  - **The user generates these video clips manually.** The agent CANNOT generate them autonomously.
  - **MANDATORY HARD STOP**: The agent MUST generate the 16:9 base images for these action beats, isolate them cleanly into `ajanta-ellora/episodeXX/google_flow_input_images/`, provide the exact camera motion prompts in a clean batch sheet, and **STOP AND WAIT FOR THE USER**.
  - **STRICT PROHIBITION**: NEVER borrow, copy, or rename `.mp4` video files from prior episodes (e.g. copying `episode03/videos/*.mp4` to `episode04/videos/`).
  - **STRICT PROHIBITION**: NEVER render a "final master preview" using borrowed clips or placeholders and claim "production complete" or "ready for publication". Any render prior to user video ingestion is strictly an *Internal Development Draft*, never a final deliverable.

## 2. GOOGLE FLOW WORKFLOW & USER HANDOFF PROTOCOL
When an episode reaches Step 3 (Asset Generation):
1. **Generate All Hero Stills & Video Input Stills**:
   - Master stills with `_PAN_ZOOM.jpg`.
   - Action video candidate stills with `_GENERATE_VIDEO.jpg`.
2. **Isolate Video Input Stills**:
   - Copy all `_GENERATE_VIDEO.jpg` files to `ajanta-ellora/episodeXX/google_flow_input_images/`.
3. **Generate Google Flow Prompt Sheet**:
   - Provide a clean, copy-paste table for the user:
     - Input Image Filename
     - Spoken Beat / Timestamp
     - Subject & Camera Motion Prompt (for Google Flow / Veo)
4. **Pause for User Ingestion**:
   - Tell the user: *"The base action stills are ready in `google_flow_input_images/`. Please generate the video clips in Google Flow and place them in `ajanta-ellora/episodeXX/videos/`. Once you have added them, we will assemble the final master."*
   - **Do NOT proceed to Step 5 (Final Assembly) or Step 6 (Final Sign-off) until the user explicitly confirms the videos are placed in `videos/`.**

## 3. ZERO MEDIA REPETITION INVARIANT (STILLS & VIDEOS)
- Every single cut across the entire video must feature a distinct visual asset (0 duplicates across the episode, 0 duplicates from earlier episodes in the series).
- Python PIL blueprint/infographic cards (Pillar B) must be generated at zero API cost.
- Cross-episode historical archive assets (Pillar C) must represent legitimate universe continuity (e.g. royal copper charters, architect scrolls), not copied scene stills.

## 4. AUDIO INTEGRITY & SUBTITLE SYNCHRONIZATION
- Full narration concatenation drift must strictly remain $\le 10.0\text{ ms}$ (enforce 0.00ms whenever possible).
- All cut durations and start times must be mathematically derived from sentence-level `.srt` cues. No uniform time-slicing.
- Audio loudness must strictly conform to EBU R128 (-16 LUFS $\pm 1$ LUFS, True Peak $< -1.5\text{ dBFS}$).

## 5. YOUTUBE METADATA CEILINGS
- All SEO tag lists across Master videos and Shorts must strictly remain under **500 characters**.
- Thumbnails must strictly remain under **2.0 MB** and obey the Mobile 3-Word Rule.
- Shorts titles must NEVER include episodic labels like `(Ep. 1)` or `Episode 4`.
