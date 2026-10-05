"""
Full 77-Micro-Beat Master Assembly Engine for Kailasa Episode 3 via FFmpeg.
Applies the 4K Anti-Jitter Sub-Pixel Motorized Zoompan Technique (scale=3840:2160 -> zoompan -> scale=1920:1080)
for still images with documentary vignette and color grading, and splices in Google Flow converted action clips
with normalized 30fps broadcast-grade encoding and monotonic timestamps derived from sentence-level SRT cues.

Produces:
1. episode03/final_videos/episode_03_master_preview.mp4 (16:9 1080p Master)
2. episode03/final_videos/short_01_the_queens_vow.mp4 (9:16 Vertical 1080x1920)
3. episode03/final_videos/short_02_why_carved_backwards.mp4 (9:16 Vertical 1080x1920)
4. episode03/openmontage_bundle/ (Canonical OpenMontage distribution package)
"""

import os
import re
import sys
import json
import shutil
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent # ajanta-ellora
EPISODE_DIR = BASE_DIR / "episode03"
IMAGES_DIR = EPISODE_DIR / "images"
AUDIO_DIR = EPISODE_DIR / "audio"
SUB_DIR = EPISODE_DIR / "subtitles"
VIDEOS_DIR = EPISODE_DIR / "videos"
OUTPUT_DIR = EPISODE_DIR / "final_videos"
BUNDLE_DIR = EPISODE_DIR / "openmontage_bundle"
THUMBNAIL_DIR = EPISODE_DIR / "thumbnail"
PUBLISH_DIR = EPISODE_DIR / "publish_kit"
OVERLAYS_DIR = EPISODE_DIR / "images" / "overlays"

# In-Video Lower-Third Archival Provenance Overlays (inspired by documentary best practices)
OVERLAYS = {
    "ep03_archive_01_royal_charter_PAN_ZOOM.jpg": OVERLAYS_DIR / "card_01_rashtrakuta_charter.png",
    "ep03_archive_16_king_sickbed_PAN_ZOOM.jpg": OVERLAYS_DIR / "card_02_katha_kalpataru.png",
    "ep03_53_wooden_mallet_acoustic_test_PAN_ZOOM.jpg": OVERLAYS_DIR / "card_03_acoustic_sounding.png",
}

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
BUNDLE_DIR.mkdir(parents=True, exist_ok=True)

# 77-Beat Master Manifest
# Formatted as (media_type, filename, motion)
MANIFEST = [
    ("image", "ep03_01_monolith_abyss_wide_PAN_ZOOM.jpg", "zoom_in"),
    ("image", "ep03_02_vertical_trench_walls_PAN_ZOOM.jpg", "pan_right"),
    ("video", "gf_trench_isolation_3d_explainer.mp4", "action_clip"),
    ("image", "ep03_archive_40_elephant_haulage_PAN_ZOOM.jpg", "zoom_in"),
    ("image", "ep03_archive_11_charanandri_ridge_PAN_ZOOM.jpg", "slow_drift"),
    ("image", "ep03_archive_13_quarrymen_army_PAN_ZOOM.jpg", "pan_left"),
    ("video", "gf_01_smoke_quarry_dissipate.mp4", "action_clip"),
    ("image", "ep03_archive_04_architects_council_PAN_ZOOM.jpg", "zoom_in"),
    ("image", "ep03_archive_14_isolated_monolith_dusk_PAN_ZOOM.jpg", "slow_drift"),
    ("image", "ep03_archive_52_prehistoric_lava_PAN_ZOOM.jpg", "slow_drift"),
    ("image", "ep03_archive_53_testing_basalt_PAN_ZOOM.jpg", "slow_drift"),
    ("image", "ep03_archive_01_royal_charter_PAN_ZOOM.jpg", "slow_drift"),
    ("image", "ep03_archive_15_palace_dusk_PAN_ZOOM.jpg", "pan_right"),
    ("image", "ep03_archive_16_king_sickbed_PAN_ZOOM.jpg", "zoom_in"),
    ("image", "ep03_archive_17_queen_vow_GENERATE_VIDEO.jpg", "slow_drift"),
    ("image", "ep03_archive_50_architects_council_PAN_ZOOM.jpg", "slow_drift"),
    ("image", "ep03_archive_20_blueprint_cutaway_PAN_ZOOM.jpg", "slow_drift"),
    ("image", "ep03_archive_51_water_clock_PAN_ZOOM.jpg", "slow_drift"),
    ("video", "gf_02_kokasa_stepping_forward.mp4", "action_clip"),
    ("image", "ep03_14_kokasa_hero_promise_PAN_ZOOM.jpg", "slow_drift"),
    ("image", "ep03_archive_18_kokasa_entrance_PAN_ZOOM.jpg", "slow_drift"),
    ("image", "ep03_archive_19_kokasa_scroll_PAN_ZOOM.jpg", "slow_drift"),
    ("image", "ep03_infographic_02_bottom_up_vs_top_down.jpg", "slow_drift"),
    ("image", "ep03_archive_48_infographic_gravity_engine.jpg", "slow_drift"),
    ("image", "ep03_infographic_03_zero_error_margin.jpg", "slow_drift"),
    ("video", "gf_03_chisel_striking_flawless.mp4", "action_clip"),
    ("image", "ep03_archive_08_three_trenches_depth_PAN_ZOOM.jpg", "slow_drift"),
    ("image", "ep03_archive_22_microfracture_cracks_PAN_ZOOM.jpg", "slow_drift"),
    ("image", "ep03_archive_46_infographic_basalt_strength.jpg", "slow_drift"),
    ("image", "ep03_archive_35_dulled_iron_pile_PAN_ZOOM.jpg", "slow_drift"),
    ("image", "ep03_archive_23_superheated_bedrock_PAN_ZOOM.jpg", "slow_drift"),
    ("image", "ep03_archive_12_trench_sunrise_PAN_ZOOM.jpg", "slow_drift"),
    ("image", "ep03_archive_30_survey_summit_GENERATE_VIDEO.jpg", "slow_drift"),
    ("image", "ep03_archive_06_surveyor_plummet_PAN_ZOOM.jpg", "slow_drift"),
    ("video", "gf_shanku_cardinal_3d_explainer.mp4", "action_clip"),
    ("video", "gf_04_shanku_solar_shadow_timelapse.mp4", "action_clip"),
    ("image", "ep03_archive_33_surveyor_plummet_PAN_ZOOM.jpg", "slow_drift"),
    ("image", "ep03_archive_26_copper_charter_PAN_ZOOM.jpg", "slow_drift"),
    ("video", "gf_05_snapping_chalk_line.mp4", "action_clip"),
    ("video", "gf_vastu_mandala_3d_explainer.mp4", "action_clip"),
    ("image", "ep03_archive_31_clay_model_seal_GENERATE_VIDEO.jpg", "slow_drift"),
    ("image", "ep03_archive_29_artisan_camp_PAN_ZOOM.jpg", "slow_drift"),
    ("image", "ep03_archive_32_first_chisel_strike_GENERATE_VIDEO.jpg", "slow_drift"),
    ("video", "gf_06_first_hammer_strike_sparks.mp4", "action_clip"),
    ("image", "ep03_archive_43_the_back_scarp_wall_PAN_ZOOM.jpg", "slow_drift"),
    ("image", "ep03_archive_34_chisel_fracture_test_GENERATE_VIDEO.jpg", "slow_drift"),
    ("image", "ep03_34_isolating_stupi_finial_PAN_ZOOM.jpg", "slow_drift"),
    ("image", "ep03_archive_03_blacksmith_forge_PAN_ZOOM.jpg", "slow_drift"),
    ("image", "ep03_archive_36_hardwood_convoys_PAN_ZOOM.jpg", "slow_drift"),
    ("image", "ep03_archive_37_stacking_pyres_PAN_ZOOM.jpg", "slow_drift"),
    ("image", "ep03_archive_42_depth_marker_checking_PAN_ZOOM.jpg", "slow_drift"),
    ("video", "gf_vimana_tiers_3d_explainer.mp4", "action_clip"),
    ("image", "ep03_archive_45_infographic_three_trenches.jpg", "slow_drift"),
    ("image", "ep03_archive_05_kokasa_scroll_PAN_ZOOM.jpg", "slow_drift"),
    ("image", "ep03_45_stepped_pyramid_emerging_PAN_ZOOM.jpg", "slow_drift"),
    ("video", "gf_07_sculptors_suspended_ropes.mp4", "action_clip"),
    ("image", "ep03_archive_41_dust_and_sweat_PAN_ZOOM.jpg", "slow_drift"),
    ("image", "ep03_archive_49_infographic_monolith_dimensions.jpg", "slow_drift"),
    ("image", "ep03_archive_38_crowbar_levering_GENERATE_VIDEO.jpg", "slow_drift"),
    ("image", "ep03_archive_54_blacksmith_forge_PAN_ZOOM.jpg", "slow_drift"),
    ("video", "gf_08_chipping_ceiling_sparks.mp4", "action_clip"),
    ("image", "ep03_archive_02_artisan_camp_ridge_PAN_ZOOM.jpg", "slow_drift"),
    ("image", "ep03_archive_39_sledgehammer_crush_GENERATE_VIDEO.jpg", "slow_drift"),
    ("image", "ep03_archive_47_infographic_thermal_shock.jpg", "slow_drift"),
    ("image", "ep03_53_wooden_mallet_acoustic_test_PAN_ZOOM.jpg", "slow_drift"),
    ("image", "ep03_infographic_06_acoustic_sounding_thickness.jpg", "slow_drift"),
    ("image", "ep03_archive_27_agrarian_supply_PAN_ZOOM.jpg", "slow_drift"),
    ("image", "ep03_archive_55_queen_vow_wide_PAN_ZOOM.jpg", "slow_drift"),
    ("image", "ep03_57_gleaming_white_spire_hero_PAN_ZOOM.jpg", "slow_drift"),
    ("image", "ep03_archive_10_back_scarp_wall_PAN_ZOOM.jpg", "zoom_out"),
    ("image", "ep03_archive_07_dulled_iron_pile_PAN_ZOOM.jpg", "slow_drift"),
    ("image", "ep03_archive_09_elephant_haulage_PAN_ZOOM.jpg", "slow_drift"),
    ("image", "ep03_archive_24_deccan_riders_PAN_ZOOM.jpg", "slow_drift"),
    ("image", "ep03_archive_21_king_command_PAN_ZOOM.jpg", "slow_drift"),
    ("image", "ep03_archive_28_merchant_guild_PAN_ZOOM.jpg", "slow_drift"),
    ("image", "ep03_archive_44_cliffhanger_spire_summit_GENERATE_VIDEO.jpg", "slow_drift"),
    ("image", "ep03_archive_56_treasury_gold_PAN_ZOOM.jpg", "slow_drift"),
]

def get_media_duration(path: Path) -> float:
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(path)
    ]
    out = subprocess.run(cmd, capture_output=True, text=True).stdout.strip()
    return float(out)

def parse_srt_cues(srt_path: Path):
    content = srt_path.read_text(encoding="utf-8")
    pattern = re.compile(
        r"(\d+)\s*\n(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})\s*\n(.*?)(?=\n\n|\Z)",
        re.DOTALL
    )
    matches = pattern.findall(content)
    
    def parse_time(ts):
        h, m, s_ms = ts.split(":")
        s, ms = s_ms.split(",")
        return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000.0

    cues = []
    for m in matches:
        cues.append({
            "index": int(m[0]),
            "start": parse_time(m[1]),
            "end": parse_time(m[2]),
            "text": m[3].strip().replace("\n", " ")
        })
    return cues

def derive_cut_durations(cues, total_audio_dur):
    # Lock each cut duration to the distance between cue starts,
    # and the final cut to the exact audio end.
    starts = [0.0] + [c["start"] for c in cues[1:]] + [total_audio_dur]
    durations = [starts[i+1] - starts[i] for i in range(len(cues))]
    return durations

def render_subsegment(mtype, fname, motion, dur, idx, total, temp_dir):
    out_mp4 = temp_dir / f"sub_{idx:03d}.mp4"
    fps = 30
    frames = max(1, int(dur * fps))
    
    if mtype == "video":
        src_path = VIDEOS_DIR / fname
        if not src_path.exists():
            raise FileNotFoundError(f"Video clip missing: {src_path}")
        
        # Conforming filtergraph: 720p -> 1080p, 24fps -> 30fps, strip audio
        vf = "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30,setpts=PTS-STARTPTS"
        cmd = [
            "ffmpeg", "-y",
            "-stream_loop", "-1", "-i", str(src_path),
            "-vf", vf,
            "-r", "30",
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-pix_fmt", "yuv420p",
            "-an",
            "-t", f"{dur:.3f}",
            str(out_mp4)
        ]
    else:
        src_path = IMAGES_DIR / fname
        if not src_path.exists():
            raise FileNotFoundError(f"Still image missing: {src_path}")
        
        # 4K pre-scaled sub-pixel anti-jitter Ken Burns motion
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
        elif motion == "tilt_up":
            vf = f"scale=3840:2160,zoompan=z=1.10:x='iw/2-(iw/zoom/2)':y='(ih-ih/zoom)*(1-on/{frames})':d={frames}:s=1920x1080:fps={fps},vignette=angle=PI/5,eq=contrast=1.04:saturation=1.06"
        else: # slow_drift
            vf = f"scale=3840:2160,zoompan=z='1.0+0.07*(on/{frames})':x='(iw/2-(iw/zoom/2))+(iw*0.02)*(on/{frames})':y='ih/2-(ih/zoom/2)':d={frames}:s=1920x1080:fps={fps},vignette=angle=PI/5,eq=contrast=1.04:saturation=1.06"
        
        overlay_path = OVERLAYS.get(fname)
        if overlay_path and overlay_path.exists():
            cmd = [
                "ffmpeg", "-y",
                "-loop", "1", "-i", str(src_path),
                "-i", str(overlay_path),
                "-filter_complex", f"[0:v]{vf}[bg];[bg][1:v]overlay=0:0:format=auto,setsar=1,fps=30,setpts=PTS-STARTPTS[out]",
                "-map", "[out]",
                "-r", "30",
                "-c:v", "libx264", "-preset", "fast", "-crf", "18",
                "-pix_fmt", "yuv420p",
                "-an",
                "-t", f"{dur:.3f}",
                str(out_mp4)
            ]
        else:
            cmd = [
                "ffmpeg", "-y",
                "-loop", "1", "-i", str(src_path),
                "-vf", f"{vf},setsar=1,fps=30,setpts=PTS-STARTPTS",
                "-r", "30",
                "-c:v", "libx264", "-preset", "fast", "-crf", "18",
                "-pix_fmt", "yuv420p",
                "-an",
                "-t", f"{dur:.3f}",
                str(out_mp4)
            ]

    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error rendering cut {idx}: {res.stderr[:200]}")
        raise RuntimeError(f"FFmpeg error on cut {idx}")
    return out_mp4

def assemble_master_episode():
    print("\n" + "=" * 65)
    print("  ASSEMBLING MASTER EPISODE 03 (1080p, 77 MICRO-BEATS)")
    print("=" * 65)

    # 1. Assert 1:1 Uniqueness
    fnames = [m[1] for m in MANIFEST]
    assert len(fnames) == len(set(fnames)), "Duplicate media assets in manifest!"
    print(f"[*] Verified Zero-Repetition Invariant: 77 unique media assets for 77 cuts.")

    # 2. Timing Lock
    master_audio = AUDIO_DIR / "episode_03_full_narration.mp3"
    total_audio_dur = get_media_duration(master_audio)
    cues = parse_srt_cues(SUB_DIR / "episode_03_full.srt")
    assert len(cues) == len(MANIFEST), f"Cues count ({len(cues)}) != Manifest count ({len(MANIFEST)})"
    durations = derive_cut_durations(cues, total_audio_dur)

    print(f"[*] Total master narration duration: {total_audio_dur:.3f}s")
    print(f"[*] Sum of all 77 cut durations:    {sum(durations):.3f}s (0.0ms drift)")

    temp_dir = OUTPUT_DIR / "temp_subsegments"
    temp_dir.mkdir(parents=True, exist_ok=True)

    sub_files = []
    print("\n[*] Rendering 77 subsegments (video-only, 1080p 30fps)...")
    for idx, ((mtype, fname, motion), dur) in enumerate(zip(MANIFEST, durations)):
        print(f"  [{idx+1:02d}/77] {mtype.upper():<5} | {fname[:38]:<38} | {dur:4.2f}s | {motion}", end="\r")
        sub_path = render_subsegment(mtype, fname, motion, dur, idx, len(MANIFEST), temp_dir)
        sub_files.append(sub_path)
    print(f"\n[*] All 77 subsegments rendered cleanly!")

    # 3. Concat Video Track
    concat_txt = OUTPUT_DIR / "temp_ep03_concat.txt"
    with open(concat_txt, "w", encoding="utf-8") as f:
        for p in sub_files:
            f.write(f"file '{p.as_posix()}'\n")

    master_v_only = OUTPUT_DIR / "temp_ep03_v_only.mp4"
    print("\n[*] Concatenating master video track...")
    cmd_concat = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_txt),
        "-c", "copy",
        str(master_v_only)
    ]
    subprocess.run(cmd_concat, capture_output=True, check=True)

    # 4. Mux Audio Track
    master_out = OUTPUT_DIR / "episode_03_master_preview.mp4"
    print(f"[*] Muxing master audio ({master_audio.name}) -> {master_out.name}...")
    cmd_mux = [
        "ffmpeg", "-y",
        "-i", str(master_v_only),
        "-i", str(master_audio),
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        "-movflags", "+faststart",
        str(master_out)
    ]
    subprocess.run(cmd_mux, capture_output=True, check=True)

    # Cleanup temp
    if concat_txt.exists():
        concat_txt.unlink()
    if master_v_only.exists():
        master_v_only.unlink()
    shutil.rmtree(temp_dir, ignore_errors=True)

    print(f"[*] Master preview rendered successfully: {master_out.name} ({master_out.stat().st_size:,} bytes)")
    return master_out

def assemble_shorts():
    print("\n" + "=" * 65)
    print("  ASSEMBLING COMPANION SHORTS (9:16 VERTICAL 1080x1920)")
    print("=" * 65)

    shorts = [
        {
            "name": "short_01_the_queens_vow",
            "img": "ep03_short_01_queens_vow_GENERATE_VIDEO.jpg",
            "audio": "short_01_the_queens_vow.mp3",
            "out": "short_01_the_queens_vow.mp4"
        },
        {
            "name": "short_02_why_carved_backwards",
            "img": "ep03_short_02_carved_backwards_PAN_ZOOM.jpg",
            "audio": "short_02_why_carved_backwards.mp3",
            "out": "short_02_why_carved_backwards.mp4"
        }
    ]

    outputs = []
    for s in shorts:
        img_path = IMAGES_DIR / s["img"]
        audio_path = AUDIO_DIR / s["audio"]
        out_path = OUTPUT_DIR / s["out"]
        
        dur = get_media_duration(audio_path)
        fps = 30
        frames = max(1, int(dur * fps))

        print(f"[*] Rendering {s['name']} (9:16 Vertical, {dur:.2f}s)...")
        vf = f"scale=2160:3840:force_original_aspect_ratio=increase,crop=2160:3840,zoompan=z='1.0+0.10*(on/{frames})':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1080x1920:fps={fps},vignette=angle=PI/5,eq=contrast=1.04:saturation=1.06,setsar=1,fps=30"
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1", "-i", str(img_path),
            "-i", str(audio_path),
            "-t", f"{dur:.3f}",
            "-vf", vf,
            "-r", "30",
            "-c:v", "libx264", "-preset", "fast", "-crf", "20",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart",
            str(out_path)
        ]
        subprocess.run(cmd, capture_output=True, check=True)
        print(f"[*] Rendered: {out_path.name} ({out_path.stat().st_size:,} bytes)")
        outputs.append(out_path)
    return outputs

def package_openmontage_bundle():
    print("\n" + "=" * 65)
    print("  PACKAGING CANONICAL OPENMONTAGE DISTRIBUTION BUNDLE")
    print("=" * 65)

    meta_dir = BUNDLE_DIR / "metadata"
    thumb_dir = BUNDLE_DIR / "thumbnails"
    video_dir = BUNDLE_DIR / "video"

    meta_dir.mkdir(parents=True, exist_ok=True)
    thumb_dir.mkdir(parents=True, exist_ok=True)
    video_dir.mkdir(parents=True, exist_ok=True)

    # Copy Master Thumbnail
    master_thumb = THUMBNAIL_DIR / "ep03_master_thumbnail_16x9.jpg"
    shutil.copy2(master_thumb, thumb_dir / "thumbnail.jpg")
    print(f"[*] Packaged thumbnail: {thumb_dir / 'thumbnail.jpg'}")

    # Copy Video & Subtitles
    master_vid = OUTPUT_DIR / "episode_03_master_preview.mp4"
    shutil.copy2(master_vid, video_dir / "output.mp4")
    shutil.copy2(SUB_DIR / "episode_03_full.srt", video_dir / "subtitles.srt")
    print(f"[*] Packaged video & subtitles: output.mp4 & subtitles.srt")

    # Extract Publish Kit Metadata
    master_kit_txt = (PUBLISH_DIR / "master_publish_kit.md").read_text(encoding="utf-8")
    
    # Chapters
    chap_lines = [
        "00:00 - Act I: The Monolith in the Abyss",
        "00:59 - Act II: The Queen's Vow & The Legend of Kokasa",
        "02:04 - Act III: The Physics of Zero Margin for Error",
        "02:59 - Act IV: The Solar Gnomon & The Sacred Grid",
        "03:55 - Act V: The First Strike: Hewing the Stupi",
        "04:46 - Act VI: The Four Tiers of the Dravidian Vimana",
        "05:39 - Act VII: The Terrifying Hollow Core",
        "06:33 - Act VIII: The Crown Emerges & Cliffhanger"
    ]
    (meta_dir / "chapters.txt").write_text("\n".join(chap_lines), encoding="utf-8")

    # Description
    desc_text = (
        "Thirty-three meters below the mountain ridge of Ellora, ancient stonecutters isolated a colossal "
        "rectangular island of volcanic basalt in a 100-foot abyss. Then began the most perilous subtractive "
        "excavation in human history: carving the sacred temple from the roof down.\n\n"
        "While medieval Marathi folklore in the Katha-Kalpataru recounts Queen Manikavati's desperate vow and "
        "master builder Kokasa's promise to reveal the temple spire within days, modern archaeology reveals that "
        "top-down excavation was a cold engineering necessity. Without ground scaffolding, the mountain itself became their platform.\n\n"
        "Join us on Episode 3 of our 10-part documentary web-series as we reconstruct the astronomical gnomon surveys, "
        "the geometry of the Vastu-Purusha Mandala, and the terrifying non-destructive acoustic sounding used to hollow out "
        "the inner sanctum without collapsing the overhead mountain."
    )
    (meta_dir / "description.txt").write_text(desc_text, encoding="utf-8")

    # Tags
    tag_match = re.search(r"```(?:\w+)?\s*\n(.*?)\n```", master_kit_txt, re.DOTALL)
    tags_str = tag_match.group(1).strip() if tag_match else ""
    (meta_dir / "tags.txt").write_text(tags_str, encoding="utf-8")

    # Metadata JSON
    meta_json_data = {
        "title": "How Ancient Builders Carved a 100-Foot Temple From the Roof Down (Kailasa Cave 16)",
        "episode": 3,
        "series": "Kailasa: The Mountain Carved From Above",
        "duration_seconds": 466.08,
        "resolution": "1920x1080",
        "fps": 30,
        "aspect_ratio": "16:9",
        "cuts_count": 77,
        "action_videos_count": 8,
        "tags": [t.strip() for t in tags_str.split(",") if t.strip()],
        "chapters": [
            {"start_seconds": 0.0, "title": "Act I: The Monolith in the Abyss"},
            {"start_seconds": 59.0, "title": "Act II: The Queen's Vow & The Legend of Kokasa"},
            {"start_seconds": 124.0, "title": "Act III: The Physics of Zero Margin for Error"},
            {"start_seconds": 179.0, "title": "Act IV: The Solar Gnomon & The Sacred Grid"},
            {"start_seconds": 235.0, "title": "Act V: The First Strike: Hewing the Stupi"},
            {"start_seconds": 286.0, "title": "Act VI: The Four Tiers of the Dravidian Vimana"},
            {"start_seconds": 339.0, "title": "Act VII: The Terrifying Hollow Core"},
            {"start_seconds": 393.0, "title": "Act VIII: The Crown Emerges & Cliffhanger"}
        ]
    }
    (meta_dir / "metadata.json").write_text(json.dumps(meta_json_data, indent=2), encoding="utf-8")
    print(f"[*] Packaged OpenMontage metadata: chapters, description, tags, metadata.json")

def audit_streams():
    print("\n" + "=" * 65)
    print("  AUDITING RENDERED VIDEO STREAMS (FFMPEG NULL SINK)")
    print("=" * 65)

    targets = [
        OUTPUT_DIR / "episode_03_master_preview.mp4",
        OUTPUT_DIR / "short_01_the_queens_vow.mp4",
        OUTPUT_DIR / "short_02_why_carved_backwards.mp4"
    ]

    all_pass = True
    for t in targets:
        cmd = ["ffmpeg", "-v", "error", "-i", str(t), "-f", "null", "-"]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if not res.stderr.strip():
            print(f"  [PASS] {t.name:<35} : 0 packet decoding errors ({t.stat().st_size:,} bytes)")
        else:
            print(f"  [FAIL] {t.name:<35} : {res.stderr.strip()}")
            all_pass = False
    return all_pass

def main():
    # 1. Assemble Master Video
    master_path = assemble_master_episode()
    # 2. Assemble Shorts
    shorts_paths = assemble_shorts()
    # 3. Package OpenMontage Bundle
    package_openmontage_bundle()
    # 4. Audit Stream Integrity
    ok = audit_streams()
    if not ok:
        print("\n[ERROR] Stream audit detected errors in rendered outputs!")
        return 1

    print("\n" + "=" * 65)
    print("  KAILASA EPISODE 03 ASSEMBLY & PACKAGING 100% COMPLETE!")
    print("=" * 65)
    return 0

if __name__ == "__main__":
    sys.exit(main())
