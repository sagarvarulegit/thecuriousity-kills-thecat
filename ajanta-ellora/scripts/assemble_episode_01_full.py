"""
Full 22-Master-Image, 92-Micro-Beat Master Assembly Engine for Episode 1 via FFmpeg.
Applies the 1-to-3 Multi-Cam Crop Technique (Wide, 160% Punch-in, Pan Left/Right, Tilt)
for still images, and automatically splices in Google Flow converted .mp4 video clips
with normalized 30fps broadcast-grade encoding and monotonic timestamps.
"""

import os
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMAGES_DIR = BASE_DIR / "assets" / "episode-01" / "images"
AUDIO_DIR = BASE_DIR / "assets" / "episode-01" / "audio_elevenlabs"
if not AUDIO_DIR.exists() or not any(AUDIO_DIR.iterdir()):
    AUDIO_DIR = BASE_DIR / "assets" / "episode-01" / "audio"

SUBTITLES_DIR = BASE_DIR / "assets" / "episode-01" / "subtitles"
GOOGLE_FLOW_DIR = BASE_DIR / "assets" / "episode-01" / "google_flow_videos"
VIDEOS_DIR = BASE_DIR / "assets" / "episode-01" / "videos"
OUTPUT_DIR = BASE_DIR / "output"

GOOGLE_FLOW_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def get_audio_duration(audio_path):
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(audio_path)
    ]
    out = subprocess.run(cmd, capture_output=True, text=True).stdout.strip()
    return float(out)

def resolve_media_source(img_name):
    """
    Resolves whether a Google Flow converted video clip or a still image should be used.
    Extracts prefix e.g. 'ep01_03' from 'ep01_03_queen_vow.jpg'.
    """
    parts = img_name.split("_")
    ep_num = parts[0] if len(parts) >= 1 else "ep01"
    shot_num = parts[1] if len(parts) >= 2 else "01"
    prefix = f"{ep_num}_{shot_num}"

    # 1. Check if a Google Flow video clip exists in google_flow_videos or videos dir
    for vdir in (GOOGLE_FLOW_DIR, VIDEOS_DIR):
        if vdir.exists():
            for vf in os.listdir(vdir):
                if vf.endswith(".mp4"):
                    vf_lower = vf.lower()
                    if (f"{ep_num}_clip_{shot_num}" in vf_lower or 
                        f"_{shot_num}_" in vf_lower or 
                        f"{ep_num}_{shot_num}" in vf_lower or
                        (shot_num == "05" and "water_droplet" in vf_lower) or
                        (shot_num == "11" and "volcanic" in vf_lower) or
                        (shot_num == "13" and "surveyor_striking" in vf_lower) or
                        (shot_num == "19" and "blacksmith" in vf_lower) or
                        (shot_num == "20" and "chalk_cord" in vf_lower) or
                        (shot_num == "21" and "stamping_seal" in vf_lower) or
                        (shot_num == "22" and "sledgehammer" in vf_lower)):
                        return ("video", str(vdir / vf))

    # 2. Check images directory for prefix matching
    for f in os.listdir(IMAGES_DIR):
        if f.startswith(prefix) and f.endswith(".jpg"):
            return ("image", str(IMAGES_DIR / f))

    # 3. Direct match fallback
    direct = IMAGES_DIR / img_name
    if direct.exists():
        return ("image", str(direct))

    # 4. Fallback to any image
    for f in os.listdir(IMAGES_DIR):
        if f.endswith(".jpg"):
            return ("image", str(IMAGES_DIR / f))

    return ("image", str(IMAGES_DIR / "ep01_01_palace_dusk_PAN_ZOOM.jpg"))

# Act Sequence Mapping:
# list of (image_filename, weight, motion_type)
ACT_IMAGE_MAP = {
    "act_01_the_vow": [
        ("ep01_01_palace_dusk.jpg", 0.10, "pan_right"),
        ("ep01_01_palace_dusk.jpg", 0.10, "punch_center"),
        ("ep01_02_king_sickbed.jpg", 0.10, "zoom_in"),
        ("ep01_03_queen_vow.jpg", 0.10, "pan_left"),
        ("ep01_03_queen_vow.jpg", 0.12, "punch_face"),
        ("ep01_02_king_sickbed.jpg", 0.10, "punch_center"),
        ("ep01_03_queen_vow.jpg", 0.10, "zoom_in_fast"),
        ("ep01_04_architects_council.jpg", 0.10, "pan_right"),
        ("ep01_04_architects_council.jpg", 0.08, "punch_face"),
        ("ep01_05_water_clock.jpg", 0.10, "zoom_in_fast")
    ],
    "act_02_the_heresy": [
        ("ep01_06_kokasa_entrance.jpg", 0.09, "pan_right"),
        ("ep01_06_kokasa_entrance.jpg", 0.08, "punch_face"),
        ("ep01_07_kokasa_scroll.jpg", 0.09, "zoom_in"),
        ("ep01_07_kokasa_scroll.jpg", 0.08, "punch_center"),
        ("ep01_08_blueprint_cutaway.jpg", 0.10, "zoom_in"),
        ("ep01_08_blueprint_cutaway.jpg", 0.09, "pan_left"),
        ("ep01_07_kokasa_scroll.jpg", 0.08, "tilt_down"),
        ("ep01_08_blueprint_cutaway.jpg", 0.09, "punch_center"),
        ("ep01_04_architects_council.jpg", 0.08, "pan_left"),
        ("ep01_06_kokasa_entrance.jpg", 0.07, "zoom_in"),
        ("ep01_09_king_command.jpg", 0.08, "zoom_in_fast"),
        ("ep01_09_king_command.jpg", 0.07, "punch_face")
    ],
    "act_03_geology": [
        ("ep01_10_deccan_riders.jpg", 0.07, "pan_right"),
        ("ep01_10_deccan_riders.jpg", 0.07, "punch_center"),
        ("ep01_11_prehistoric_lava.jpg", 0.08, "zoom_in_fast"),
        ("ep01_11_prehistoric_lava.jpg", 0.08, "pan_left"),
        ("ep01_11_prehistoric_lava.jpg", 0.07, "punch_center"),
        ("ep01_12_charanandri_ridge.jpg", 0.08, "pan_right"),
        ("ep01_12_charanandri_ridge.jpg", 0.07, "tilt_down"),
        ("ep01_10_deccan_riders.jpg", 0.06, "zoom_in"),
        ("ep01_13_testing_basalt.jpg", 0.08, "zoom_in"),
        ("ep01_13_testing_basalt.jpg", 0.07, "punch_center"),
        ("ep01_13_testing_basalt.jpg", 0.07, "pan_left"),
        ("ep01_12_charanandri_ridge.jpg", 0.07, "punch_center"),
        ("ep01_13_testing_basalt.jpg", 0.07, "zoom_in_fast"),
        ("ep01_12_charanandri_ridge.jpg", 0.06, "zoom_in")
    ],
    "act_04_capital": [
        ("ep01_14_treasury_chests.jpg", 0.08, "zoom_in"),
        ("ep01_14_treasury_chests.jpg", 0.08, "punch_center"),
        ("ep01_14_treasury_chests.jpg", 0.07, "pan_left"),
        ("ep01_15_copper_charter.jpg", 0.08, "zoom_in"),
        ("ep01_15_copper_charter.jpg", 0.08, "punch_center"),
        ("ep01_15_copper_charter.jpg", 0.07, "tilt_down"),
        ("ep01_16_agrarian_supply.jpg", 0.08, "pan_right"),
        ("ep01_16_agrarian_supply.jpg", 0.08, "punch_center"),
        ("ep01_16_agrarian_supply.jpg", 0.08, "zoom_in"),
        ("ep01_17_merchant_guild.jpg", 0.08, "pan_left"),
        ("ep01_17_merchant_guild.jpg", 0.07, "punch_face"),
        ("ep01_17_merchant_guild.jpg", 0.07, "zoom_in"),
        ("ep01_14_treasury_chests.jpg", 0.08, "zoom_in_fast")
    ],
    "act_05_guilds": [
        ("ep01_18_artisan_camp.jpg", 0.09, "pan_right"),
        ("ep01_18_artisan_camp.jpg", 0.08, "punch_center"),
        ("ep01_18_artisan_camp.jpg", 0.08, "zoom_in"),
        ("ep01_18_artisan_camp.jpg", 0.08, "pan_left"),
        ("ep01_19_blacksmith_forge.jpg", 0.10, "zoom_in"),
        ("ep01_19_blacksmith_forge.jpg", 0.09, "punch_center"),
        ("ep01_19_blacksmith_forge.jpg", 0.09, "zoom_in_fast"),
        ("ep01_19_blacksmith_forge.jpg", 0.09, "pan_right"),
        ("ep01_19_blacksmith_forge.jpg", 0.08, "tilt_down"),
        ("ep01_19_blacksmith_forge.jpg", 0.08, "punch_face"),
        ("ep01_18_artisan_camp.jpg", 0.07, "zoom_in"),
        ("ep01_18_artisan_camp.jpg", 0.07, "pan_right")
    ],
    "act_06_survey": [
        ("ep01_20_survey_summit.jpg", 0.08, "pan_right"),
        ("ep01_20_survey_summit.jpg", 0.08, "punch_center"),
        ("ep01_20_survey_summit.jpg", 0.07, "zoom_in"),
        ("ep01_20_survey_summit.jpg", 0.07, "tilt_down"),
        ("ep01_20_survey_summit.jpg", 0.07, "pan_left"),
        ("ep01_20_survey_summit.jpg", 0.07, "punch_face"),
        ("ep01_20_survey_summit.jpg", 0.08, "zoom_in_fast"),
        ("ep01_08_blueprint_cutaway.jpg", 0.07, "zoom_in"),
        ("ep01_08_blueprint_cutaway.jpg", 0.07, "punch_center"),
        ("ep01_20_survey_summit.jpg", 0.07, "pan_right"),
        ("ep01_20_survey_summit.jpg", 0.07, "zoom_in"),
        ("ep01_08_blueprint_cutaway.jpg", 0.07, "tilt_down"),
        ("ep01_20_survey_summit.jpg", 0.07, "punch_center"),
        ("ep01_20_survey_summit.jpg", 0.06, "zoom_in_fast")
    ],
    "act_07_council": [
        ("ep01_21_clay_model_seal.jpg", 0.13, "zoom_in"),
        ("ep01_21_clay_model_seal.jpg", 0.13, "punch_center"),
        ("ep01_09_king_command.jpg", 0.13, "pan_left"),
        ("ep01_06_kokasa_entrance.jpg", 0.12, "zoom_in"),
        ("ep01_21_clay_model_seal.jpg", 0.13, "tilt_down"),
        ("ep01_21_clay_model_seal.jpg", 0.13, "punch_face"),
        ("ep01_09_king_command.jpg", 0.12, "zoom_in_fast"),
        ("ep01_21_clay_model_seal.jpg", 0.11, "zoom_in")
    ],
    "act_08_first_strike": [
        ("ep01_20_survey_summit.jpg", 0.11, "pan_right"),
        ("ep01_18_artisan_camp.jpg", 0.11, "zoom_in"),
        ("ep01_22_first_chisel_strike.jpg", 0.11, "pan_left"),
        ("ep01_22_first_chisel_strike.jpg", 0.12, "punch_center"),
        ("ep01_22_first_chisel_strike.jpg", 0.11, "zoom_in"),
        ("ep01_22_first_chisel_strike.jpg", 0.12, "zoom_in_fast"),
        ("ep01_22_first_chisel_strike.jpg", 0.11, "punch_face"),
        ("ep01_19_blacksmith_forge.jpg", 0.10, "punch_center"),
        ("ep01_22_first_chisel_strike.jpg", 0.11, "zoom_in_fast")
    ]
}

def render_act_video(act_key, act_idx):
    audio_path = AUDIO_DIR / f"{act_key}.mp3"
    if not audio_path.exists():
        print(f"Audio not found: {audio_path}")
        return None

    total_dur = get_audio_duration(audio_path)
    cuts = ACT_IMAGE_MAP.get(act_key, [])
    if not cuts:
        return None

    sub_segments = []
    fps = 30

    print(f"  Act {act_idx} duration: {total_dur:.2f}s across {len(cuts)} micro-cuts (~{total_dur/len(cuts):.2f}s/cut)")

    for c_idx, (img_name, weight, motion) in enumerate(cuts):
        media_type, media_path = resolve_media_source(img_name)
        cut_dur = total_dur * weight
        frames = int(cut_dur * fps)
        sub_seg_mp4 = OUTPUT_DIR / f"temp_sub_{act_idx}_{c_idx}.mp4"

        if media_type == "video":
            # Direct video clip from Google Flow - normalized to 1080p 30fps
            cmd = [
                "ffmpeg", "-y",
                "-stream_loop", "-1", "-i", media_path,
                "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30,setpts=PTS-STARTPTS",
                "-r", "30",
                "-c:v", "libx264", "-preset", "fast", "-crf", "18",
                "-pix_fmt", "yuv420p",
                "-an",
                "-t", f"{cut_dur:.3f}",
                str(sub_seg_mp4)
            ]
        else:
            # Dynamic motion filters for 1-to-3 multi-cam crops on still images
            if motion == "zoom_in":
                vf = f"zoompan=z='min(zoom+0.0012,1.25)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1920x1080:fps={fps}"
            elif motion == "zoom_in_fast":
                vf = f"zoompan=z='min(zoom+0.0022,1.35)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1920x1080:fps={fps}"
            elif motion == "pan_right":
                vf = f"zoompan=z=1.18:x='min(x+0.8,iw-iw/zoom)':y='ih/2-(ih/zoom/2)':d={frames}:s=1920x1080:fps={fps}"
            elif motion == "pan_left":
                vf = f"zoompan=z=1.18:x='max(x-0.8,0)':y='ih/2-(ih/zoom/2)':d={frames}:s=1920x1080:fps={fps}"
            elif motion == "tilt_down":
                vf = f"zoompan=z=1.18:x='iw/2-(iw/zoom/2)':y='min(y+0.6,ih-ih/zoom)':d={frames}:s=1920x1080:fps={fps}"
            elif motion == "punch_center":
                vf = f"zoompan=z='min(1.50+0.0010*on,1.75)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1920x1080:fps={fps}"
            elif motion == "punch_face":
                vf = f"zoompan=z='min(1.55+0.0012*on,1.80)':x='iw/2-(iw/zoom/2)':y='max(0,ih/3-(ih/zoom/2))':d={frames}:s=1920x1080:fps={fps}"
            else:
                vf = f"zoompan=z='min(zoom+0.0012,1.25)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1920x1080:fps={fps}"

            cmd = [
                "ffmpeg", "-y",
                "-loop", "1", "-i", media_path,
                "-vf", f"{vf},setsar=1,fps=30,setpts=PTS-STARTPTS",
                "-r", "30",
                "-c:v", "libx264", "-preset", "fast", "-crf", "18",
                "-pix_fmt", "yuv420p",
                "-an",
                "-t", f"{cut_dur:.3f}",
                str(sub_seg_mp4)
            ]

        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        sub_segments.append(sub_seg_mp4)

    # Concat video sub-segments for this act
    concat_txt = OUTPUT_DIR / f"concat_act_{act_idx}.txt"
    with open(concat_txt, "w", encoding="utf-8") as f:
        for s in sub_segments:
            f.write(f"file '{s.as_posix()}'\n")

    act_video_mp4 = OUTPUT_DIR / f"temp_act_video_{act_idx}.mp4"
    subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_txt),
        "-c", "copy",
        "-avoid_negative_ts", "make_zero",
        str(act_video_mp4)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Clean temp sub-segments
    for s in sub_segments:
        try: os.remove(s)
        except: pass
    try: os.remove(concat_txt)
    except: pass

    return act_video_mp4

def generate_synchronized_subtitles(acts):
    """
    Generates perfectly synchronized master subtitles by scaling each act's SRT
    to match the exact duration and offset of the ElevenLabs audio narration.
    """
    print("\n--- Synchronizing Master Subtitles with ElevenLabs Audio ---")
    
    def to_seconds(t_str):
        h, m, rest = t_str.split(':')
        s, ms = rest.split(',')
        return int(h)*3600 + int(m)*60 + int(s) + int(ms)/1000.0

    def to_srt_time(sec):
        h = int(sec // 3600)
        sec %= 3600
        m = int(sec // 60)
        sec %= 60
        s = int(sec)
        ms = int(round((sec - s) * 1000))
        if ms >= 1000:
            s += 1
            ms = 0
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

    current_offset = 0.0
    all_cues = []
    cue_num = 1

    for act in acts:
        audio_path = AUDIO_DIR / f"{act}.mp3"
        dur = get_audio_duration(audio_path)
        srt_path = SUBTITLES_DIR / f"{act}.srt"
        
        if srt_path.exists():
            content = srt_path.read_text(encoding="utf-8")
            blocks = content.strip().split("\n\n")
            times = []
            for b in blocks:
                lines = b.splitlines()
                if len(lines) >= 3 and "-->" in lines[1]:
                    t1, t2 = lines[1].split(" --> ")
                    times.append(to_seconds(t2))
            orig_max = max(times) if times else dur
            scale = dur / orig_max

            for b in blocks:
                lines = b.splitlines()
                if len(lines) >= 3 and "-->" in lines[1]:
                    t1, t2 = lines[1].split(" --> ")
                    new_t1 = to_srt_time(current_offset + to_seconds(t1) * scale)
                    new_t2 = to_srt_time(current_offset + to_seconds(t2) * scale)
                    text = "\n".join(lines[2:])
                    all_cues.append(f"{cue_num}\n{new_t1} --> {new_t2}\n{text}")
                    cue_num += 1

        current_offset += dur

    full_srt_path = SUBTITLES_DIR / "episode_01_full.srt"
    full_srt_path.write_text("\n\n".join(all_cues) + "\n", encoding="utf-8")
    print(f"  -> Aligned {len(all_cues)} cues across {current_offset:.2f}s: {full_srt_path}")
    return full_srt_path

def render_shorts():
    print("\n--- Rendering YouTube Shorts (9:16 Vertical) ---")
    shorts_cfg = [
        ("short_01_the_queen_vow", "ep01_short_01_queen_vow.jpg"),
        ("short_02_billion_dollar_mountain", "ep01_short_02_treasury.jpg")
    ]
    for s_name, img_v in shorts_cfg:
        audio_path = AUDIO_DIR / f"{s_name}.mp3"
        if not audio_path.exists():
            continue
        dur = get_audio_duration(audio_path)
        media_type, media_path = resolve_media_source(img_v)

        out_mp4 = OUTPUT_DIR / f"{s_name}.mp4"
        frames = int(dur * 30)
        vf = f"zoompan=z='min(zoom+0.0014,1.30)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1080x1920:fps=30,setsar=1,fps=30,setpts=PTS-STARTPTS"

        print(f"Rendering {s_name}.mp4 (9:16 vertical, {dur:.1f}s)...")
        subprocess.run([
            "ffmpeg", "-y",
            "-loop", "1", "-i", media_path,
            "-i", str(audio_path),
            "-vf", vf,
            "-r", "30",
            "-c:v", "libx264", "-preset", "fast",
            "-c:a", "aac", "-b:a", "192k", "-pix_fmt", "yuv420p",
            "-t", str(dur),
            "-movflags", "+faststart",
            str(out_mp4)
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"  -> Generated: {out_mp4}")

def main():
    acts = [
        "act_01_the_vow",
        "act_02_the_heresy",
        "act_03_geology",
        "act_04_capital",
        "act_05_guilds",
        "act_06_survey",
        "act_07_council",
        "act_08_first_strike"
    ]

    print("==================================================")
    print("Multi-Scene Master Assembly Engine (Episode 1)")
    print(f"Images Directory: {IMAGES_DIR}")
    print(f"Google Flow Video Clips Directory: {GOOGLE_FLOW_DIR}")
    print(f"Audio Narration Directory: {AUDIO_DIR}")
    print("==================================================")

    act_video_files = []
    for i, act_key in enumerate(acts, 1):
        print(f"\nProcessing Act {i}/8: {act_key}...")
        act_v = render_act_video(act_key, i)
        if act_v and act_v.exists():
            act_video_files.append(act_v)

    # 1. Concat all acts into single Master Video Track (video only, 0 packet errors)
    master_video_concat = OUTPUT_DIR / "master_video_concat.txt"
    with open(master_video_concat, "w", encoding="utf-8") as f:
        for a in act_video_files:
            f.write(f"file '{a.as_posix()}'\n")

    master_video_only = OUTPUT_DIR / "temp_master_video_only.mp4"
    print("\nConcatenating All Acts into Seamless Video Track...")
    subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(master_video_concat),
        "-c", "copy",
        "-avoid_negative_ts", "make_zero",
        str(master_video_only)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 2. Concat all audio stems into single Master Audio Track
    master_audio_concat = OUTPUT_DIR / "master_audio_concat.txt"
    with open(master_audio_concat, "w", encoding="utf-8") as f:
        for act in acts:
            aud = AUDIO_DIR / f"{act}.mp3"
            f.write(f"file '{aud.as_posix()}'\n")

    master_audio_only = OUTPUT_DIR / "temp_master_audio_only.m4a"
    print("Concatenating All Audio Stems into Master Audio Track...")
    subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(master_audio_concat),
        "-c:a", "aac", "-b:a", "192k", "-ar", "44100",
        str(master_audio_only)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 3. Final Mux: Master Video + Master Audio with +faststart
    master_mp4 = OUTPUT_DIR / "episode_01_master_preview.mp4"
    print("Muxing Video & Audio into Final Master Episode 1...")
    subprocess.run([
        "ffmpeg", "-y",
        "-i", str(master_video_only),
        "-i", str(master_audio_only),
        "-c:v", "copy",
        "-c:a", "copy",
        "-movflags", "+faststart",
        str(master_mp4)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Clean intermediate master files
    for a in act_video_files:
        try: os.remove(a)
        except: pass
    for tmp in (master_video_concat, master_video_only, master_audio_concat, master_audio_only):
        try: os.remove(tmp)
        except: pass

    # 4. Synchronize Subtitles with ElevenLabs Audio
    generate_synchronized_subtitles(acts)

    # 5. Render Shorts
    render_shorts()

    print("\n==================================================")
    print(f"FULL PRODUCTION COMPLETE: {master_mp4}")
    print("==================================================")

if __name__ == "__main__":
    main()
