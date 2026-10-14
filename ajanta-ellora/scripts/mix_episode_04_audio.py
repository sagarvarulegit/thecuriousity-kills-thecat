"""
Cinematic Sound Design & Audio Bed Mixer for Kailasa Episode 04
Implements:
1. Procedural Foley track generation (42Hz sub-bass, 1800Hz stone impacts, whooshes)
2. Open courtyard wind ambient bed synthesis
3. EBU R128 sidechain auto-ducking (-16 dB) under master narration
4. Mathematical audio drift verification (< 10.0 ms)
"""

import sys
import math
import wave
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent # ajanta-ellora
EP04_DIR = BASE_DIR / "episode04"
AUDIO_DIR = EP04_DIR / "audio"

sys.path.insert(0, str(BASE_DIR / "scripts"))
from foley_generator_v2 import generate_foley_track, SAMPLE_RATE
from audio_engine_v2 import apply_sidechain_ducking, get_media_duration, verify_audio_stems_drift

def synthesize_courtyard_wind(duration_s: float, amplitude: float = 0.22) -> np.ndarray:
    """Synthesizes natural, open-air courtyard wind with slow atmospheric modulation."""
    n_samples = int(duration_s * SAMPLE_RATE)
    t = np.linspace(0, duration_s, n_samples, endpoint=False)
    
    # White noise baseline
    noise = np.random.uniform(-1, 1, n_samples)
    
    # Low-pass filter approximation via cumulative moving average / brown noise
    # Simple IIR low-pass filter
    filtered = np.zeros(n_samples, dtype=np.float32)
    alpha = 0.012  # Very soft low cutoff (~120 Hz)
    prev = 0.0
    for i in range(n_samples):
        prev = prev + alpha * (noise[i] - prev)
        filtered[i] = prev
        
    # Slow undulating breeze modulators
    mod1 = 0.65 + 0.35 * np.sin(2 * np.pi * 0.08 * t)
    mod2 = 0.85 + 0.15 * np.sin(2 * np.pi * 0.03 * t + 1.2)
    
    # Add gentle sub-harmonic rumble for high courtyard canyon feeling (Cave 16 scarp walls)
    canyon_drone = 0.25 * np.sin(2 * np.pi * 48.0 * t) * mod1
    
    wind = (filtered * mod1 * mod2 + canyon_drone) * amplitude
    return wind.astype(np.float32)

def build_episode_04_audio_bed():
    print("=" * 65)
    print(" MIXING EPISODE 04 BROADCAST SOUND DESIGN & SIDECHAIN BED")
    print("=" * 65)
    
    master_narration = AUDIO_DIR / "episode_04_full_narration.mp3"
    if not master_narration.exists():
        raise FileNotFoundError(f"Master narration not found: {master_narration}")
        
    total_dur = get_media_duration(master_narration)
    print(f"Master Narration Duration: {total_dur:.2f}s ({total_dur/60:.2f} min)")
    
    # 1. Verify Audio Drift
    act_names = [
        "act_01_the_gap",
        "act_02_a_temple_in_sequence",
        "act_03_the_route",
        "act_04_how_to_leave_a_bridge",
        "act_05_reading_the_stone",
        "act_06_the_missing_span",
        "act_07_architecture_as_procession",
        "act_08_the_mountain_reconnected"
    ]
    act_paths = [AUDIO_DIR / f"{name}.mp3" for name in act_names]
    sync_ok, drift_ms = verify_audio_stems_drift(master_narration, act_paths)
    print(f"Mathematical Audio Drift: {drift_ms:.2f} ms (Sync Status: {'PASS' if sync_ok else 'FAIL'})")
    
    # 2. Build Foley Cues
    # Timestamped cues aligned with narrative moments in Episode 04
    foley_cues = [
        # Act I: The Gap (0 - 45s)
        (0.5, "sub_bass", 3.0),      # First bridge reveal
        (31.5, "sub_bass", 2.5),     # Southern cliff span gone
        (44.0, "whoosh", 0.6),       # Act transition
        
        # Act II: A Temple in Sequence (45 - 98s)
        (46.0, "sub_bass", 2.0),     # Kailasa monolithic island
        (85.0, "stone_strike", 0.25),# Material subtraction
        (97.0, "whoosh", 0.6),       # Act transition
        
        # Act III: The Route Through the Air (98 - 145s)
        (100.0, "sub_bass", 2.0),    # Processional axis
        (144.0, "whoosh", 0.6),      # Act transition
        
        # Act IV: How to Leave a Bridge (145 - 208s)
        (165.0, "stone_strike", 0.25),# Controlled cutting
        (168.0, "stone_strike", 0.25),# Second chisel blow
        (190.0, "stone_strike", 0.25),# Deepening trench
        (207.0, "whoosh", 0.6),       # Act transition
        
        # Act V: Reading the Stone (208 - 263s)
        (210.0, "sub_bass", 2.0),     # Negative evidence
        (235.0, "stone_strike", 0.25),# Chisel fluting marks
        (262.0, "whoosh", 0.6),       # Act transition
        
        # Act VI: The Missing Span (263 - 318s)
        (265.0, "sub_bass", 3.0),     # Southern collapse mystery
        (280.0, "boom", 1.2),         # Ancient collapse gravity
        (317.0, "whoosh", 0.6),       # Act transition
        
        # Act VII: Architecture as Procession (318 - 373s)
        (320.0, "sub_bass", 2.0),     # Sacred path
        (372.0, "whoosh", 0.6),       # Act transition
        
        # Act VIII: The Mountain Reconnected (373 - 425s)
        (375.0, "sub_bass", 3.0),     # The mountain reconnected
        (405.0, "boom", 1.5),         # Elephant plinth reveal
        (418.0, "sub_bass", 3.5),     # Cliffhanger teaser tone
    ]
    
    foley_wav_path = AUDIO_DIR / "_foley_bed_temp.wav"
    generate_foley_track(total_dur + 2.0, foley_cues, foley_wav_path)
    print(f"Generated procedural Foley track: {foley_wav_path.name}")
    
    # 3. Synthesize Courtyard Wind
    print("Synthesizing open courtyard wind bed...")
    wind_samples = synthesize_courtyard_wind(total_dur + 2.0, amplitude=0.20)
    
    # Read foley samples and blend
    with wave.open(str(foley_wav_path), "rb") as wf:
        n_frames = wf.getnframes()
        foley_raw = wf.readframes(n_frames)
        foley_samples = np.frombuffer(foley_raw, dtype=np.int16).astype(np.float32) / 32767.0
        
    min_len = min(len(wind_samples), len(foley_samples))
    blended_bed = (wind_samples[:min_len] * 0.75 + foley_samples[:min_len] * 0.65)
    
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
    print(f"Synthesized full background bed: {bgm_bed_wav.name}")
    
    # 4. Apply Sidechain Compression & EBU R128 Loudness Normalization
    print("Applying -16 dB sidechain auto-ducking under narration...")
    mixed_master_out = AUDIO_DIR / "episode_04_master_audio_mixed.mp3"
    apply_sidechain_ducking(
        vocal_path=master_narration,
        bgm_path=bgm_bed_wav,
        out_path=mixed_master_out,
        ducking_db=-16,
        target_lufs=-16.0
    )
    print(f"[SUCCESS] Mixed broadcast master audio: {mixed_master_out.name} ({get_media_duration(mixed_master_out):.2f}s)")
    
    # Cleanup temp wavs
    if foley_wav_path.exists():
        foley_wav_path.unlink()
    if bgm_bed_wav.exists():
        bgm_bed_wav.unlink()

if __name__ == "__main__":
    build_episode_04_audio_bed()
