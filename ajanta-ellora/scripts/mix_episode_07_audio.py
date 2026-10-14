#!/usr/bin/env python3
"""
mix_episode_07_audio.py — Broadcast Sound Design & Cinematic Audio Bed Mixer for Episode 07
Implements:
1. YouTube Audio Library Score (Patrick Patrikios: Sands of serenity & Sands of time)
2. 44Hz basalt subterranean acoustic resonance + 110Hz ancient chaitya cave chant overtone
3. Studio sidechain auto-ducking (-18 dB) under Adam Stone's master narration
4. EBU R128 loudness normalization (-16.0 LUFS, True Peak < -1.5 dBFS) for English & Hindi
5. Mixed audio beds for companion Shorts (English & Hindi)
6. YouTube multi-language track export: episode_07_hindi_track.m4a
"""

import sys
import math
import wave
import numpy as np
import subprocess
from pathlib import Path

# Fix Windows console UTF-8 encoding
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

BASE_DIR = Path("C:/Sagar/Projects/thecuriousity-kills-thecat")
EP07_DIR = BASE_DIR / "ajanta-ellora" / "episode07"
AUDIO_DIR = EP07_DIR / "audio"
AUDIO_HINDI_DIR = EP07_DIR / "audio_hindi"
FINAL_VIDEOS_DIR = EP07_DIR / "final_videos"
SCRIPTS_DIR = BASE_DIR / "ajanta-ellora" / "scripts"

FINAL_VIDEOS_DIR.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(SCRIPTS_DIR))
SAMPLE_RATE = 44100
from audio_engine_v2 import apply_sidechain_ducking, get_media_duration

def synthesize_basalt_resonance_pad(duration_s: float, amplitude: float = 0.08) -> np.ndarray:
    """
    Synthesizes a deep subterranean drone mimicking the 44Hz and 110Hz natural basalt
    acoustic resonance of Ajanta Caves 9 and 10.
    """
    n_samples = int(duration_s * SAMPLE_RATE)
    t = np.linspace(0, duration_s, n_samples, endpoint=False)
    
    # 44Hz basal fundamental + 110Hz chaitya chanting formant + subtle 220Hz octave
    f44 = np.sin(2 * np.pi * 44.0 * t) * 0.45
    f110 = np.sin(2 * np.pi * 110.0 * (1.0 + 0.002 * np.sin(2 * np.pi * 0.1 * t)) * t) * 0.35
    f220 = np.sin(2 * np.pi * 220.0 * t) * 0.20
    
    # Organic slow breathing LFO
    lfo = 0.70 + 0.30 * np.sin(2 * np.pi * 0.05 * t)
    
    drone = (f44 + f110 + f220) * lfo * amplitude
    return drone.astype(np.float32)

def load_audio_as_float32(path: Path) -> np.ndarray:
    """Reads audio file into numpy float32 stereo array via ffmpeg."""
    cmd = [
        "ffmpeg", "-v", "error",
        "-i", str(path),
        "-f", "f32le",
        "-ac", "2",
        "-ar", str(SAMPLE_RATE),
        "pipe:1"
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    raw, _ = proc.communicate()
    arr = np.frombuffer(raw, dtype=np.float32).reshape(-1, 2)
    return arr

def build_continuous_bgm(target_dur: float, out_wav: Path, yt_tracks: list) -> Path:
    """
    Seamlessly chains and crossfades YouTube Audio Library tracks to cover target duration.
    Balances levels, applies 4-second crossfades, and a 3.5s smooth outro fade.
    """
    if len(yt_tracks) == 1:
        t1 = load_audio_as_float32(yt_tracks[0])
        playlist = [t1] * (int(target_dur / (len(t1) / SAMPLE_RATE)) + 2)
    else:
        t1 = load_audio_as_float32(yt_tracks[0])
        t2 = load_audio_as_float32(yt_tracks[1])
        rms1 = np.sqrt(np.mean(t1**2))
        rms2 = np.sqrt(np.mean(t2**2))
        if rms2 > 0:
            t2 = t2 * (rms1 / rms2)
        playlist = [t1, t2, t1, t2, t1, t2, t1, t2]

    fade_len = int(4.0 * SAMPLE_RATE)
    t_fade = np.linspace(0, 1, fade_len)
    fade_out = np.cos(t_fade * (np.pi / 2))[:, None]
    fade_in = np.sin(t_fade * (np.pi / 2))[:, None]

    current_audio = playlist[0]
    for next_track in playlist[1:]:
        if len(current_audio) / SAMPLE_RATE >= target_dur + 5.0:
            break
        overlap_a = current_audio[-fade_len:] * fade_out
        overlap_b = next_track[:fade_len] * fade_in
        crossfaded = overlap_a + overlap_b
        current_audio = np.vstack([
            current_audio[:-fade_len],
            crossfaded,
            next_track[fade_len:]
        ])

    target_samples = int(target_dur * SAMPLE_RATE)
    final_bed = current_audio[:target_samples].copy()

    # Add subtle basalt acoustic resonance drone
    drone = synthesize_basalt_resonance_pad(target_dur, amplitude=0.04)
    drone_stereo = np.column_stack([drone, drone])
    final_bed = final_bed * 0.90 + drone_stereo * 0.10

    # 3.5s smooth outro fadeout
    out_fade_len = min(int(3.5 * SAMPLE_RATE), len(final_bed))
    out_t = np.linspace(1, 0, out_fade_len)[:, None]
    final_bed[-out_fade_len:] *= out_t

    # Peak normalization to safe headroom
    peak = np.max(np.abs(final_bed))
    if peak > 0:
        final_bed = final_bed / peak * 0.70

    int16_data = (np.clip(final_bed, -1.0, 1.0) * 32767).astype(np.int16)
    with wave.open(str(out_wav), "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(int16_data.tobytes())

    return out_wav

def mix_track_with_bed(vocal_path: Path, out_path: Path, total_dur: float, track_idx: int = 0, ducking_db: float = -18.0, target_lufs: float = -16.0):
    yt_audio_dir = AUDIO_DIR / "youtube_audio_library"
    yt_tracks = sorted(list(yt_audio_dir.glob("*.mp3")) + list(yt_audio_dir.glob("*.wav")))
    
    if yt_tracks:
        temp_bed_wav = None
        if total_dur > 120.0:
            temp_bed_wav = vocal_path.parent / f"_temp_yt_bed_{vocal_path.stem}.wav"
            print(f"[*] Assembling continuous YouTube Audio Library score ({total_dur:.2f}s) across {len(yt_tracks)} tracks...")
            build_continuous_bgm(total_dur, temp_bed_wav, yt_tracks)
            bgm_src = temp_bed_wav
        else:
            bgm_src = yt_tracks[track_idx % len(yt_tracks)]
            print(f"[*] Using YouTube Audio Library Track for Short: {bgm_src.name}")

        apply_sidechain_ducking(
            vocal_path=vocal_path,
            bgm_path=bgm_src,
            out_path=out_path,
            ducking_db=ducking_db,
            target_lufs=target_lufs
        )
        if temp_bed_wav and temp_bed_wav.exists():
            temp_bed_wav.unlink()
        return

    # Fallback to pure procedural basalt resonance pad
    pad = synthesize_basalt_resonance_pad(total_dur + 3.0, amplitude=0.08)
    peak = np.max(np.abs(pad))
    if peak > 0.95:
        pad = pad / peak * 0.95
        
    temp_bed_wav = vocal_path.parent / f"_temp_bed_{vocal_path.stem}.wav"
    with wave.open(str(temp_bed_wav), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes((pad * 32767).astype(np.int16).tobytes())
        
    apply_sidechain_ducking(
        vocal_path=vocal_path,
        bgm_path=temp_bed_wav,
        out_path=out_path,
        ducking_db=-22,
        target_lufs=target_lufs
    )
    
    if temp_bed_wav.exists():
        temp_bed_wav.unlink()

def main():
    print("=" * 65)
    print("  EPISODE 07 BROADCAST AUDIO MIXER & SOUND DESIGN SUITE")
    print("=" * 65)
    
    # 1. Mix English Master Audio
    en_vocal = AUDIO_DIR / "narration" / "episode_07_narration_master.mp3"
    en_mixed = AUDIO_DIR / "episode_07_master_audio_mixed.mp3"
    if en_vocal.exists():
        dur = get_media_duration(en_vocal)
        print(f"[*] Mixing English Master Audio ({dur:.2f}s) with -18 dB auto-ducking...")
        mix_track_with_bed(en_vocal, en_mixed, dur, ducking_db=-18.0)
        print(f"[OK] Rendered English Mixed Master: {en_mixed.name} ({en_mixed.stat().st_size:,} bytes)")
    else:
        print(f"[ERROR] English master vocal not found: {en_vocal}")
        
    # 2. Mix English Shorts
    shorts_list = [
        "short_01_the_horseshoe_canyon_hidden_from_the_world",
        "short_02_how_ancient_monks_engineered_water"
    ]
    for idx, s_name in enumerate(shorts_list):
        s_vocal = AUDIO_DIR / "narration" / f"{s_name}.mp3"
        s_mixed = AUDIO_DIR / f"{s_name}_mixed.mp3"
        if s_vocal.exists():
            s_dur = get_media_duration(s_vocal)
            print(f"[*] Mixing English Short: {s_name} ({s_dur:.2f}s)...")
            mix_track_with_bed(s_vocal, s_mixed, s_dur, track_idx=idx, ducking_db=-18.0)
            print(f"[OK] Rendered Short Audio: {s_mixed.name}")
            
    # 3. Mix Hindi Master Audio & Export YouTube Audio Track (M4A)
    hi_vocal = AUDIO_HINDI_DIR / "narration" / "episode_07_hindi_narration_master.mp3"
    hi_mixed = AUDIO_HINDI_DIR / "episode_07_hindi_master_audio_mixed.mp3"
    hi_m4a = FINAL_VIDEOS_DIR / "episode_07_hindi_track.m4a"
    if hi_vocal.exists():
        dur = get_media_duration(hi_vocal)
        print(f"[*] Mixing Hindi Master Audio ({dur:.2f}s) with -18 dB auto-ducking...")
        mix_track_with_bed(hi_vocal, hi_mixed, dur, ducking_db=-18.0)
        print(f"[OK] Rendered Hindi Mixed Master: {hi_mixed.name}")
        
        # Normalize and export M4A
        print("[*] Exporting YouTube Multi-Language Audio Track (episode_07_hindi_track.m4a)...")
        cmd_m4a = [
            "ffmpeg", "-y",
            "-i", str(hi_mixed),
            "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
            "-c:a", "aac", "-b:a", "256k",
            str(hi_m4a)
        ]
        subprocess.run(cmd_m4a, capture_output=True, check=True)
        print(f"[OK] Exported YouTube Audio Track: {hi_m4a.name} ({hi_m4a.stat().st_size:,} bytes)")
        
    # 4. Mix Hindi Shorts
    for idx, s_name in enumerate(shorts_list):
        s_vocal = AUDIO_HINDI_DIR / "narration" / f"{s_name}.mp3"
        s_mixed = AUDIO_HINDI_DIR / f"{s_name}_mixed.mp3"
        if s_vocal.exists():
            s_dur = get_media_duration(s_vocal)
            print(f"[*] Mixing Hindi Short: {s_name} ({s_dur:.2f}s)...")
            mix_track_with_bed(s_vocal, s_mixed, s_dur, track_idx=idx, ducking_db=-18.0)
            print(f"[OK] Rendered Hindi Short Audio: {s_mixed.name}")
            
    print("\n" + "=" * 65)
    print("  AUDIO MIXING & LOUDNESS NORMALIZATION COMPLETE")
    print("=" * 65)

if __name__ == "__main__":
    main()
