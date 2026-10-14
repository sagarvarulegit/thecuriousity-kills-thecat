"""
Episode 1 Video Assembly Engine via FFmpeg
Renders the full 16:9 episode preview and the two 9:16 vertical YouTube Shorts.
"""

import os
import subprocess
import glob

IMAGES_DIR = "ajanta-ellora/assets/episode-01/images"
# Prefer ElevenLabs studio audio if generated, otherwise fall back to neural edge-tts
if os.path.exists("ajanta-ellora/assets/episode-01/audio_elevenlabs") and os.listdir("ajanta-ellora/assets/episode-01/audio_elevenlabs"):
    AUDIO_DIR = "ajanta-ellora/assets/episode-01/audio_elevenlabs"
else:
    AUDIO_DIR = "ajanta-ellora/assets/episode-01/audio"

SUBS_DIR = "ajanta-ellora/assets/episode-01/subtitles"
OUTPUT_DIR = "ajanta-ellora/output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_audio_duration(audio_path):
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        audio_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return float(result.stdout.strip())

def render_short_01():
    print("Rendering Short 1: The 7-Day Royal Vow (9:16)...")
    img_path = os.path.join(IMAGES_DIR, "ep01_03_queen_vow.jpg")
    audio_path = os.path.join(AUDIO_DIR, "short_01_the_queen_vow.mp3")
    out_mp4 = os.path.join(OUTPUT_DIR, "short_01_the_queen_vow.mp4")

    if not os.path.exists(img_path) or not os.path.exists(audio_path):
        print("Missing assets for Short 1")
        return

    duration = get_audio_duration(audio_path) + 0.5
    # 9:16 1080x1920 with subtle Ken Burns zoom
    vf = (
        f"zoompan=z='min(zoom+0.0015,1.25)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
        f"d={int(duration*30)}:s=1080x1920:fps=30"
    )

    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", img_path,
        "-i", audio_path,
        "-vf", vf,
        "-c:v", "libx264", "-tune", "stillimage",
        "-c:a", "aac", "-b:a", "192k", "-pix_fmt", "yuv420p",
        "-t", str(duration),
        out_mp4
    ]
    subprocess.run(cmd, check=True)
    print(f"Generated: {out_mp4}")

def render_short_02():
    print("Rendering Short 2: Billion-Dollar Mountain (9:16)...")
    img_path = os.path.join(IMAGES_DIR, "ep01_01_palace_dusk.jpg")
    audio_path = os.path.join(AUDIO_DIR, "short_02_billion_dollar_mountain.mp3")
    out_mp4 = os.path.join(OUTPUT_DIR, "short_02_billion_dollar_mountain.mp4")

    if not os.path.exists(img_path) or not os.path.exists(audio_path):
        print("Missing assets for Short 2")
        return

    duration = get_audio_duration(audio_path) + 0.5
    # 9:16 with subtle pan
    vf = (
        f"zoompan=z='min(zoom+0.0012,1.20)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
        f"d={int(duration*30)}:s=1080x1920:fps=30"
    )

    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", img_path,
        "-i", audio_path,
        "-vf", vf,
        "-c:v", "libx264", "-tune", "stillimage",
        "-c:a", "aac", "-b:a", "192k", "-pix_fmt", "yuv420p",
        "-t", str(duration),
        out_mp4
    ]
    subprocess.run(cmd, check=True)
    print(f"Generated: {out_mp4}")

def render_episode_01_preview():
    print("Rendering Episode 1 Master 16:9 Preview...")
    # Map generated images across the 8 acts
    acts_map = [
        ("act_01_the_vow.mp3", "ep01_03_queen_vow.jpg", "zoom_in"),
        ("act_02_the_heresy.mp3", "ep01_07_kokasa_scroll.jpg", "pan_right"),
        ("act_03_geology.mp3", "ep01_13_testing_basalt.jpg", "zoom_in"),
        ("act_04_capital.mp3", "ep01_01_palace_dusk.jpg", "pan_left"),
        ("act_05_guilds.mp3", "ep01_07_kokasa_scroll.jpg", "zoom_in"),
        ("act_06_survey.mp3", "ep01_13_testing_basalt.jpg", "pan_right"),
        ("act_07_council.mp3", "ep01_07_kokasa_scroll.jpg", "zoom_in"),
        ("act_08_first_strike.mp3", "ep01_13_testing_basalt.jpg", "zoom_in_fast"),
    ]

    segment_files = []

    for i, (audio_file, img_file, motion) in enumerate(acts_map):
        audio_path = os.path.join(AUDIO_DIR, audio_file)
        img_path = os.path.join(IMAGES_DIR, img_file)
        seg_mp4 = os.path.join(OUTPUT_DIR, f"seg_{i:02d}.mp4")

        if not os.path.exists(audio_path) or not os.path.exists(img_path):
            print(f"Missing {audio_path} or {img_path}")
            continue

        dur = get_audio_duration(audio_path)
        fps = 30
        frames = int(dur * fps)

        if motion == "zoom_in":
            vf = f"zoompan=z='min(zoom+0.0010,1.25)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1920x1080:fps={fps}"
        elif motion == "zoom_in_fast":
            vf = f"zoompan=z='min(zoom+0.0020,1.35)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1920x1080:fps={fps}"
        elif motion == "pan_right":
            vf = f"zoompan=z=1.15:x='min(x+0.5,iw-iw/zoom)':y='ih/2-(ih/zoom/2)':d={frames}:s=1920x1080:fps={fps}"
        else:
            vf = f"zoompan=z=1.15:x='max(x-0.5,0)':y='ih/2-(ih/zoom/2)':d={frames}:s=1920x1080:fps={fps}"

        cmd = [
            "ffmpeg", "-y",
            "-loop", "1", "-i", img_path,
            "-i", audio_path,
            "-vf", vf,
            "-c:v", "libx264", "-preset", "fast",
            "-c:a", "aac", "-b:a", "192k", "-pix_fmt", "yuv420p",
            "-t", str(dur),
            seg_mp4
        ]
        subprocess.run(cmd, check=True)
        segment_files.append(seg_mp4)

    # Concat all segments into master video
    concat_list = os.path.join(OUTPUT_DIR, "concat_list.txt")
    with open(concat_list, "w", encoding="utf-8") as f:
        for seg in segment_files:
            abs_path = os.path.abspath(seg).replace("\\", "/")
            f.write(f"file '{abs_path}'\n")

    master_mp4 = os.path.join(OUTPUT_DIR, "episode_01_master_preview.mp4")
    cmd_concat = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", concat_list,
        "-c", "copy",
        master_mp4
    ]
    subprocess.run(cmd_concat, check=True)
    print(f"\n==========================================")
    print(f"MASTER EPISODE 1 RENDERED: {master_mp4}")
    print(f"==========================================")

    # Clean up temp segments
    for seg in segment_files:
        try:
            os.remove(seg)
        except:
            pass
    try:
        os.remove(concat_list)
    except:
        pass

if __name__ == "__main__":
    render_short_01()
    render_short_02()
    render_episode_01_preview()
