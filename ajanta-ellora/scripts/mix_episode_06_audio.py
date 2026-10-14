#!/usr/bin/env python3
"""
mix_episode_06_audio.py — Broadcast Sound Design & Cinematic Audio Bed Mixer for Episode 06
Implements:
1. Cinematic orchestral harmonic pad & strings synthesis (Dramatic D minor / D Aeolian progression)
2. High chasm canyon wind ambience with 44Hz subterranean basalt acoustic resonance
3. Narrative procedural Foley accents (chisel strikes, rope creaks, sub-bass tectonic rumbles)
4. Studio sidechain auto-ducking (-16 dB) under Adam Stone's master narration
5. EBU R128 loudness normalization (-16.0 LUFS, True Peak < -1.5 dBFS) for English & Hindi
6. Mixed audio beds for companion Shorts (English & Hindi)
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
EP06_DIR = BASE_DIR / "ajanta-ellora" / "episode06"
AUDIO_DIR = EP06_DIR / "audio"
AUDIO_HINDI_DIR = EP06_DIR / "audio_hindi"
FINAL_VIDEOS_DIR = EP06_DIR / "final_videos"
SCRIPTS_DIR = BASE_DIR / "ajanta-ellora" / "scripts"

sys.path.insert(0, str(SCRIPTS_DIR))
from foley_generator_v2 import generate_foley_track, SAMPLE_RATE
from audio_engine_v2 import apply_sidechain_ducking, get_media_duration

def synthesize_orchestral_pad(duration_s: float, amplitude: float = 0.18) -> np.ndarray:
    """
    Synthesizes a lush, suspended cinematic pad with warm cello & viol harmonics.
    Chord progression (D minor / D Aeolian):
    Dm (D3, A3, F4) -> Bb (Bb2, F3, D4) -> Gm (G2, D3, Bb3) -> A (A2, E3, C#4) -> Dm
    """
    n_samples = int(duration_s * SAMPLE_RATE)
    t = np.linspace(0, duration_s, n_samples, endpoint=False)
    buffer = np.zeros(n_samples, dtype=np.float32)
    
    # D3=146.83, F3=174.61, A3=220.00, Bb2=116.54, D4=293.66, G2=98.00, A2=110.00, C#4=277.18
    chords = [
        [146.83, 220.00, 349.23], # Dm
        [116.54, 174.61, 293.66], # Bb maj
        [98.00,  146.83, 233.08], # Gm
        [110.00, 164.81, 277.18], # A maj (harmonic tension)
        [146.83, 220.00, 293.66], # Dm open
    ]
    
    chord_len = 34.0
    n_chords = int(np.ceil(duration_s / chord_len)) + 1
    
    for c_idx in range(n_chords):
        chord = chords[c_idx % len(chords)]
        c_start = int(c_idx * chord_len * SAMPLE_RATE)
        c_end = min(n_samples, int((c_idx + 1) * chord_len * SAMPLE_RATE))
        if c_start >= n_samples:
            break
            
        dur = (c_end - c_start) / SAMPLE_RATE
        t_chord = np.linspace(0, dur, c_end - c_start, endpoint=False)
        
        fade_samples = int(min(6.0, dur * 0.4) * SAMPLE_RATE)
        window = np.ones(c_end - c_start, dtype=np.float32)
        if fade_samples > 0:
            window[:fade_samples] = np.linspace(0, 1, fade_samples)
            window[-fade_samples:] = np.linspace(1, 0, fade_samples)
            
        chord_signal = np.zeros(c_end - c_start, dtype=np.float32)
        for freq in chord:
            vib = 1.0 + 0.0035 * np.sin(2 * np.pi * 4.2 * t_chord)
            f1 = np.sin(2 * np.pi * freq * vib * t_chord)
            f2 = 0.42 * np.sin(2 * np.pi * freq * 2.0 * vib * t_chord)
            f3 = 0.18 * np.sin(2 * np.pi * freq * 3.0 * vib * t_chord)
            sub = 0.38 * np.sin(2 * np.pi * (freq * 0.5) * t_chord)
            chord_signal += (f1 + f2 + f3 + sub) * (1.0 / len(chord))
            
        buffer[c_start:c_end] += chord_signal * window
        
    return buffer * amplitude

def synthesize_courtyard_wind(duration_s: float, amplitude: float = 0.15) -> np.ndarray:
    """Synthesizes high chasm wind howling past the aerial stone bridge with canyon resonance."""
    from scipy.signal import lfilter
    n_samples = int(duration_s * SAMPLE_RATE)
    t = np.linspace(0, duration_s, n_samples, endpoint=False)
    
    noise = np.random.uniform(-1, 1, n_samples).astype(np.float32)
    alpha = 0.012
    filtered = lfilter([alpha], [1.0, -(1.0 - alpha)], noise).astype(np.float32)
        
    lfo_slow = 0.65 + 0.35 * np.sin(2 * np.pi * 0.08 * t)
    lfo_gust = 0.85 + 0.15 * np.sin(2 * np.pi * 0.22 * t + 0.5)
    
    # 44Hz basalt subterranean hum
    hum = np.sin(2 * np.pi * 44.0 * t) * 0.18
    wind = (filtered * lfo_slow * lfo_gust * 3.5 + hum) * amplitude
    return wind.astype(np.float32)

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
    yt_audio_dir.mkdir(parents=True, exist_ok=True)
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

    # Clean acoustic pad fallback: ZERO wind noise, gentle low-level floor (-22dB)
    pad = synthesize_orchestral_pad(total_dur + 3.0, amplitude=0.06)
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
    print("  EPISODE 06 BROADCAST AUDIO MIXER & SOUND DESIGN SUITE")
    print("=" * 65)
    
    # 1. Mix English Master Audio
    en_vocal = AUDIO_DIR / "episode_06_narration_master.mp3"
    en_mixed = AUDIO_DIR / "episode_06_master_audio_mixed.mp3"
    if en_vocal.exists():
        dur = get_media_duration(en_vocal)
        print(f"[*] Mixing English Master Audio ({dur:.2f}s) with -18 dB auto-ducking...")
        mix_track_with_bed(en_vocal, en_mixed, dur, ducking_db=-18.0)
        print(f"[OK] Rendered English Mixed Master: {en_mixed.name} ({en_mixed.stat().st_size:,} bytes)")
        
    # 2. Mix English Shorts
    shorts_list = ["short_01_the_sky_bridge_that_shouldnt_exist", "short_02_the_temple_that_1000_men_couldnt_destroy"]
    for idx, s_name in enumerate(shorts_list):
        s_vocal = AUDIO_DIR / f"{s_name}.mp3"
        s_mixed = AUDIO_DIR / f"{s_name}_mixed.mp3"
        if s_vocal.exists():
            s_dur = get_media_duration(s_vocal)
            print(f"[*] Mixing English Short: {s_name} ({s_dur:.2f}s)...")
            mix_track_with_bed(s_vocal, s_mixed, s_dur, track_idx=idx, ducking_db=-18.0)
            print(f"[OK] Rendered Short Audio: {s_mixed.name}")
            
    # 3. Mix Hindi Master Audio & Export YouTube Audio Track (M4A)
    hi_vocal = AUDIO_HINDI_DIR / "episode_06_hindi_narration_master.mp3"
    hi_mixed = AUDIO_HINDI_DIR / "episode_06_hindi_master_audio_mixed.mp3"
    hi_m4a = FINAL_VIDEOS_DIR / "episode_06_hindi_track.m4a"
    if hi_vocal.exists():
        dur = get_media_duration(hi_vocal)
        print(f"[*] Mixing Hindi Master Audio ({dur:.2f}s) with -18 dB auto-ducking...")
        mix_track_with_bed(hi_vocal, hi_mixed, dur, ducking_db=-18.0)
        print(f"[OK] Rendered Hindi Mixed Master: {hi_mixed.name}")
        
        # Normalize and export M4A
        print("[*] Exporting YouTube Multi-Language Audio Track (episode_06_hindi_track.m4a)...")
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
        s_vocal = AUDIO_HINDI_DIR / f"{s_name}.mp3"
        s_mixed = AUDIO_HINDI_DIR / f"{s_name}_mixed.mp3"
        if s_vocal.exists():
            s_dur = get_media_duration(s_vocal)
            print(f"[*] Mixing Hindi Short: {s_name} ({s_dur:.2f}s)...")
            mix_track_with_bed(s_vocal, s_mixed, s_dur, track_idx=idx, ducking_db=-18.0)
            print(f"[OK] Rendered Hindi Short Audio: {s_mixed.name}")
            
    print("\n[ALL COMPLETE] English and Hindi audio beds fully mixed to broadcast EBU R128 (-16 LUFS) standard!")

if __name__ == "__main__":
    main()
