"""
Procedural & Layered Foley Generator v2.0
Synthesizes cinema-grade documentary sound effects using NumPy:
- 42 Hz sub-bass seismic rumbles with Hanning envelopes
- 1800 Hz chisel / basalt hammer impacts with exponential decays
- Swept-frequency kinetic whooshes for transitions and camera pans
- 55 Hz pitch-glide boom drops for Shorts 0.0s hooks
Outputs 44.1kHz 16-bit PCM WAV.
"""

import math
import wave
import numpy as np
from pathlib import Path
from typing import List, Tuple, Union

SAMPLE_RATE = 44100

def synthesize_sub_bass(duration_s: float = 2.5, freq: float = 42.0, amplitude: float = 0.40) -> np.ndarray:
    """Synthesizes deep sub-bass seismic rumble with smooth Hanning envelope."""
    n_samples = int(duration_s * SAMPLE_RATE)
    t = np.linspace(0, duration_s, n_samples, endpoint=False)
    # Fundamental + slight sub-harmonic
    wave_data = np.sin(2 * np.pi * freq * t) + 0.35 * np.sin(2 * np.pi * (freq * 0.5) * t)
    # Hanning window envelope for seamless rise and fall
    envelope = np.hanning(n_samples)
    return (amplitude * envelope * wave_data).astype(np.float32)

def synthesize_stone_strike(duration_s: float = 0.20, freq: float = 1800.0, amplitude: float = 0.55) -> np.ndarray:
    """Synthesizes crisp metallic chisel and basalt hammer impact."""
    n_samples = int(duration_s * SAMPLE_RATE)
    t = np.linspace(0, duration_s, n_samples, endpoint=False)
    # Fast exponential decay for initial strike crack
    decay = np.exp(-t * 55)
    # High metallic transient + low stone thud
    strike = np.sin(2 * np.pi * freq * t) + 0.6 * np.sin(2 * np.pi * 520 * t) + 0.3 * np.random.uniform(-1, 1, n_samples)
    return (amplitude * decay * strike).astype(np.float32)

def synthesize_whoosh(duration_s: float = 0.45, amplitude: float = 0.35) -> np.ndarray:
    """Synthesizes swept-frequency aerodynamic air whoosh."""
    n_samples = int(duration_s * SAMPLE_RATE)
    t = np.linspace(0, duration_s, n_samples, endpoint=False)
    envelope = np.sin(np.pi * np.linspace(0, 1, n_samples)) ** 2
    # Swept frequency white noise simulation
    noise = np.random.uniform(-1, 1, n_samples)
    carrier = np.sin(2 * np.pi * (250 + 700 * t / duration_s) * t)
    return (amplitude * envelope * (0.6 * noise + 0.4 * carrier)).astype(np.float32)

def synthesize_boom(duration_s: float = 1.2, start_freq: float = 85.0, end_freq: float = 38.0, amplitude: float = 0.60) -> np.ndarray:
    """Synthesizes cinematic pitch-glide sub-bass boom drop for Shorts hooks."""
    n_samples = int(duration_s * SAMPLE_RATE)
    t = np.linspace(0, duration_s, n_samples, endpoint=False)
    # Linear chirp downward
    instantaneous_freq = start_freq + (end_freq - start_freq) * (t / duration_s)
    phase = 2 * np.pi * np.cumsum(instantaneous_freq) / SAMPLE_RATE
    decay = np.exp(-t * 2.8)
    return (amplitude * decay * np.sin(phase)).astype(np.float32)

def generate_foley_track(
    duration_s: float,
    cues: List[Tuple[float, str, float]],
    out_wav_path: Path
) -> Path:
    """
    Assembles a full timeline Foley track from timestamped cues:
    cues: list of (start_time_s, cue_type, cue_duration_s)
    cue_type: "sub_bass" | "stone_strike" | "whoosh" | "boom"
    """
    total_samples = int(duration_s * SAMPLE_RATE)
    buffer = np.zeros(total_samples, dtype=np.float32)

    for start_s, cue_type, cue_dur in cues:
        start_idx = int(start_s * SAMPLE_RATE)
        if start_idx >= total_samples:
            continue

        if cue_type == "sub_bass":
            sample = synthesize_sub_bass(duration_s=cue_dur)
        elif cue_type == "stone_strike":
            sample = synthesize_stone_strike(duration_s=cue_dur)
        elif cue_type == "whoosh":
            sample = synthesize_whoosh(duration_s=cue_dur)
        elif cue_type == "boom":
            sample = synthesize_boom(duration_s=cue_dur)
        else:
            sample = synthesize_whoosh(duration_s=cue_dur)

        end_idx = min(start_idx + len(sample), total_samples)
        sample_slice = sample[:end_idx - start_idx]
        buffer[start_idx:end_idx] += sample_slice

    # Prevent hard digital clipping
    max_val = np.max(np.abs(buffer))
    if max_val > 0.98:
        buffer = buffer / max_val * 0.98

    # Convert float32 to int16 PCM
    pcm_data = (buffer * 32767).astype(np.int16)

    out_wav_path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(out_wav_path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(pcm_data.tobytes())

    return out_wav_path
