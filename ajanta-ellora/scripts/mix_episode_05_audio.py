#!/usr/bin/env python3
"""
mix_episode_05_audio.py — Broadcast Sound Design & Cinematic Audio Bed Mixer for Episode 05
Implements:
1. Cinematic orchestral harmonic pad & strings synthesis (Warm modal D minor / D Dorian progression)
2. Open courtyard canyon wind ambience with 48Hz subterranean basalt resonance
3. Narrative procedural Foley accents (sub-bass seismic rumbles, soft stone clicks, swept whooshes)
4. Studio sidechain auto-ducking (-16 dB) under Adam Stone's ElevenLabs master narration
5. EBU R128 loudness normalization (-16.0 LUFS, True Peak < -1.5 dBFS)
6. Mixed audio beds for companion Shorts
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
EP05_DIR = BASE_DIR / "ajanta-ellora" / "episode05"
AUDIO_DIR = EP05_DIR / "audio"
SCRIPTS_DIR = BASE_DIR / "ajanta-ellora" / "scripts"

sys.path.insert(0, str(SCRIPTS_DIR))
from foley_generator_v2 import generate_foley_track, SAMPLE_RATE
from audio_engine_v2 import apply_sidechain_ducking, get_media_duration, verify_audio_stems_drift

def synthesize_orchestral_pad(duration_s: float, amplitude: float = 0.18) -> np.ndarray:
    """
    Synthesizes a lush, contemplative cinematic drone/pad with warm cello & viol harmonics.
    Chord progression (D minor / D Dorian):
    Dm (D3, A3, F4) -> F (F3, C4, A4) -> C (C3, G3, E4) -> Dm (D3, A3, D4)
    """
    n_samples = int(duration_s * SAMPLE_RATE)
    t = np.linspace(0, duration_s, n_samples, endpoint=False)
    buffer = np.zeros(n_samples, dtype=np.float32)
    
    # Chord frequencies
    # D3=146.83, F3=174.61, A3=220.00, C4=261.63, E4=329.63, F4=349.23, G3=196.00, D4=293.66
    chords = [
        [146.83, 220.00, 349.23], # Dm
        [174.61, 261.63, 440.00], # F major
        [130.81, 196.00, 329.63], # C major
        [146.83, 220.00, 293.66], # Dm9 / open
    ]
    
    chord_len = 36.0 # seconds per chord
    n_chords = int(np.ceil(duration_s / chord_len)) + 1
    
    for c_idx in range(n_chords):
        chord = chords[c_idx % len(chords)]
        c_start = int(c_idx * chord_len * SAMPLE_RATE)
        c_end = min(n_samples, int((c_idx + 1) * chord_len * SAMPLE_RATE))
        if c_start >= n_samples:
            break
            
        dur = (c_end - c_start) / SAMPLE_RATE
        t_chord = np.linspace(0, dur, c_end - c_start, endpoint=False)
        
        # Crossfade window
        fade_samples = int(min(6.0, dur * 0.4) * SAMPLE_RATE)
        window = np.ones(c_end - c_start, dtype=np.float32)
        if fade_samples > 0:
            window[:fade_samples] = np.linspace(0, 1, fade_samples)
            window[-fade_samples:] = np.linspace(1, 0, fade_samples)
            
        chord_signal = np.zeros(c_end - c_start, dtype=np.float32)
        for freq in chord:
            # Vibrato
            vib = 1.0 + 0.004 * np.sin(2 * np.pi * 4.5 * t_chord)
            # Fundamental + soft harmonics
            f1 = np.sin(2 * np.pi * freq * vib * t_chord)
            f2 = 0.45 * np.sin(2 * np.pi * freq * 2.0 * vib * t_chord)
            f3 = 0.20 * np.sin(2 * np.pi * freq * 3.0 * vib * t_chord)
            sub = 0.35 * np.sin(2 * np.pi * (freq * 0.5) * t_chord)
            chord_signal += (f1 + f2 + f3 + sub) * (1.0 / len(chord))
            
        buffer[c_start:c_end] += chord_signal * window
        
    return buffer * amplitude

def synthesize_courtyard_wind(duration_s: float, amplitude: float = 0.16) -> np.ndarray:
    """Synthesizes natural, open-air courtyard wind with canyon resonance."""
    n_samples = int(duration_s * SAMPLE_RATE)
    t = np.linspace(0, duration_s, n_samples, endpoint=False)
    
    # White noise baseline
    noise = np.random.uniform(-1, 1, n_samples)
    
    # Low-pass filter (brown noise approximation)
    filtered = np.zeros(n_samples, dtype=np.float32)
    alpha = 0.010
    prev = 0.0
    for i in range(n_samples):
        prev = prev + alpha * (noise[i] - prev)
        filtered[i] = prev
        
    # Undulating breeze modulators
    mod1 = 0.70 + 0.30 * np.sin(2 * np.pi * 0.06 * t)
    mod2 = 0.85 + 0.15 * np.sin(2 * np.pi * 0.025 * t + 1.5)
    
    # Sub-harmonic basalt trench rumble (44 Hz)
    canyon_drone = 0.20 * np.sin(2 * np.pi * 44.0 * t) * mod1
    
    wind = (filtered * mod1 * mod2 + canyon_drone) * amplitude
    return wind.astype(np.float32)

def mix_master_audio():
    print("=" * 65)
    print("  MIXING EPISODE 05 BROADCAST SOUND DESIGN & SIDECHAIN BED")
    print("=" * 65)
    
    master_narration = AUDIO_DIR / "episode_05_full_narration.mp3"
    if not master_narration.exists():
        raise FileNotFoundError(f"Master narration not found: {master_narration}")
        
    total_dur = get_media_duration(master_narration)
    print(f"[*] Master Narration Duration: {total_dur:.2f}s ({total_dur/60:.2f} min)")
    
    # 1. Verify Audio Drift across Acts
    act_names = [
        "act_01_the_animals_beneath",
        "act_02_a_mountain_as_temple",
        "act_03_reading_the_plinth",
        "act_04_the_illusion_of_support",
        "act_05_animals_and_the_sacred_mountain",
        "act_06_one_stone_many_images",
        "act_07_the_viewer_completes_the_image",
        "act_08_beneath_the_mountain"
    ]
    act_paths = [AUDIO_DIR / f"{name}.mp3" for name in act_names]
    sync_ok, drift_ms = verify_audio_stems_drift(master_narration, act_paths)
    print(f"[*] Mathematical Audio Drift: {drift_ms:.2f} ms (Sync Status: {'PASS' if sync_ok else 'FAIL'})")
    
    # 2. Build Foley Cues aligned with narrative acts
    foley_cues = [
        # Act I: The Animals Beneath (0 - 55s)
        (0.5, "sub_bass", 3.0),       # First reveal beneath the temple
        (25.0, "stone_strike", 0.25), # Chasm encounter
        (50.0, "whoosh", 0.6),        # Act transition
        
        # Act II: A Mountain as Temple (55 - 120s)
        (58.0, "sub_bass", 2.5),      # Top-down excavation perspective
        (115.0, "whoosh", 0.6),       # Act transition
        
        # Act III: Reading the Plinth (120 - 180s)
        (122.0, "sub_bass", 2.0),     # Continuous plinth band
        (178.0, "whoosh", 0.6),       # Act transition
        
        # Act IV: The Illusion of Support (180 - 235s)
        (182.0, "sub_bass", 3.0),     # The weight-bearing illusion
        (232.0, "whoosh", 0.6),       # Act transition
        
        # Act V: Animals and Sacred Mountain (235 - 300s)
        (240.0, "sub_bass", 2.5),     # Havell cloud island mist
        (295.0, "whoosh", 0.6),       # Act transition
        
        # Act VI: One Stone, Many Images (300 - 360s)
        (305.0, "sub_bass", 2.0),     # 3D corner projection
        (355.0, "whoosh", 0.6),       # Act transition
        
        # Act VII: The Viewer Completes the Image (360 - 415s)
        (365.0, "sub_bass", 2.5),     # Breathing basalt dusk
        (410.0, "whoosh", 0.6),       # Act transition
        
        # Act VIII: Beneath the Mountain (415 - 465s)
        (420.0, "sub_bass", 3.5),     # Climax: The mountain hoisted
        (450.0, "boom", 1.8),         # Final teaser into temple wall epics
    ]
    
    foley_wav_path = AUDIO_DIR / "_foley_bed_temp.wav"
    generate_foley_track(total_dur + 3.0, foley_cues, foley_wav_path)
    print(f"[*] Generated procedural Foley track: {foley_wav_path.name}")
    
    # 3. Synthesize Music & Ambience
    print("[*] Synthesizing orchestral ambient strings & canyon wind bed...")
    pad_samples = synthesize_orchestral_pad(total_dur + 3.0, amplitude=0.18)
    wind_samples = synthesize_courtyard_wind(total_dur + 3.0, amplitude=0.14)
    
    with wave.open(str(foley_wav_path), "rb") as wf:
        n_frames = wf.getnframes()
        foley_raw = wf.readframes(n_frames)
        foley_samples = np.frombuffer(foley_raw, dtype=np.int16).astype(np.float32) / 32767.0
        
    min_len = min(len(pad_samples), len(wind_samples), len(foley_samples))
    blended_bed = (pad_samples[:min_len] * 0.85 + wind_samples[:min_len] * 0.65 + foley_samples[:min_len] * 0.60)
    
    # Master limiter
    peak = np.max(np.abs(blended_bed))
    if peak > 0.95:
        blended_bed = blended_bed / peak * 0.95
        
    bgm_bed_wav = AUDIO_DIR / "_bgm_bed_final.wav"
    pcm_out = (blended_bed * 32767).astype(np.int16)
    with wave.open(str(bgm_bed_wav), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(pcm_out.tobytes())
    print(f"[*] Synthesized full background bed: {bgm_bed_wav.name}")
    
    # 4. Apply Sidechain Compression (-16 dB) & EBU R128 Loudness Normalization
    print("[*] Applying -16 dB sidechain auto-ducking under Adam Stone narration...")
    mixed_master_out = AUDIO_DIR / "episode_05_master_audio_mixed.mp3"
    apply_sidechain_ducking(
        vocal_path=master_narration,
        bgm_path=bgm_bed_wav,
        out_path=mixed_master_out,
        ducking_db=-16,
        target_lufs=-16.0
    )
    print(f"[SUCCESS] Mixed broadcast master audio: {mixed_master_out.name} ({get_media_duration(mixed_master_out):.2f}s)")
    
    # 5. Mix Shorts Audio Beds
    for short_name in ["short_01_the_elephants_that_carry_a_temple", "short_02_why_elephants_support_the_mountain"]:
        s_vocal = AUDIO_DIR / f"{short_name}.mp3"
        if s_vocal.exists():
            s_dur = get_media_duration(s_vocal)
            s_pad = synthesize_orchestral_pad(s_dur + 1.0, amplitude=0.20)
            s_wind = synthesize_courtyard_wind(s_dur + 1.0, amplitude=0.15)
            s_len = min(len(s_pad), len(s_wind))
            s_bed = (s_pad[:s_len] * 0.85 + s_wind[:s_len] * 0.65)
            s_peak = np.max(np.abs(s_bed))
            if s_peak > 0.95:
                s_bed = s_bed / s_peak * 0.95
            s_bed_wav = AUDIO_DIR / f"_{short_name}_bed.wav"
            with wave.open(str(s_bed_wav), "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(SAMPLE_RATE)
                wf.writeframes((s_bed * 32767).astype(np.int16).tobytes())
                
            s_mixed = AUDIO_DIR / f"{short_name}_mixed.mp3"
            apply_sidechain_ducking(
                vocal_path=s_vocal,
                bgm_path=s_bed_wav,
                out_path=s_mixed,
                ducking_db=-16,
                target_lufs=-16.0
            )
            print(f"[*] Mixed Short Audio: {s_mixed.name} ({get_media_duration(s_mixed):.2f}s)")
            if s_bed_wav.exists():
                s_bed_wav.unlink()

    # Cleanup temp wavs
    if foley_wav_path.exists():
        foley_wav_path.unlink()
    if bgm_bed_wav.exists():
        bgm_bed_wav.unlink()

if __name__ == "__main__":
    mix_master_audio()
