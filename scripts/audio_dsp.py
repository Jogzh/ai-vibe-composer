"""Reusable audio DSP: decoding, EQ, dynamics, room, tempo, speech FX and mastering.

All processing uses a 44.1 kHz stereo float array unless documented otherwise.
Demucs / Torch are imported only when separate() is requested.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import re
import subprocess
from pathlib import Path

import numpy as np
import soundfile as sf
from scipy import signal

SR = 44100



def run(args):
    result = subprocess.run([str(a) for a in args], capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(result.stderr[-3000:])
    return result


def save_json(path, data):
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def read_audio(path):
    # Decode through FFmpeg to support AAC/MP3 and normalize sample layout.
    raw = subprocess.run([
        "ffmpeg", "-v", "error", "-i", str(path), "-ar", str(SR), "-ac", "2",
        "-f", "f32le", "pipe:1",
    ], check=True, capture_output=True).stdout
    return np.frombuffer(raw, dtype="<f4").reshape(-1, 2).copy()


def filt(y, hz, kind="lowpass", order=2):
    return signal.sosfilt(signal.butter(order, hz, kind, fs=SR, output="sos"), y, axis=0).astype(np.float32)


def fade(y, attack=.006, release=.018):
    y = y.copy()
    a, r = min(round(attack * SR), len(y)), min(round(release * SR), len(y))
    if a:
        y[:a] *= np.linspace(0, 1, a).reshape((-1,) + (1,) * (y.ndim - 1))
    if r:
        y[-r:] *= np.linspace(1, 0, r).reshape((-1,) + (1,) * (y.ndim - 1))
    return y


def stereo(y, pan=0):
    if y.ndim == 2:
        return y
    return np.column_stack([y * math.sqrt(1 - pan), y * math.sqrt(1 + pan)])


def stretch(y, factor, directory):
    # FFmpeg atempo changes duration while preserving pitch; no resampling trick.
    key = hashlib.sha256(y.tobytes() + str(factor).encode()).hexdigest()[:16]
    target = directory / f"stretch-{key}.wav"
    if not target.exists():
        source = directory / f"input-{key}.wav"
        sf.write(source, y, SR, subtype="FLOAT")
        run(["ffmpeg", "-v", "error", "-y", "-i", source, "-af", f"atempo={factor:.12f}",
             "-c:a", "pcm_f32le", target])
        source.unlink()
    return sf.read(target, dtype="float32", always_2d=True)[0]


def separate(source, destination, model_cache):
    import torch
    from demucs.apply import apply_model
    from demucs.pretrained import get_model

    destination.mkdir(parents=True, exist_ok=True)
    torch.hub.set_dir(str(model_cache.resolve()))
    torch.manual_seed(261015)
    torch.set_num_threads(min(6, os.cpu_count() or 4))
    y = read_audio(source)
    sf.write(destination / "preview.wav", y, SR, subtype="FLOAT")
    model = get_model("htdemucs").eval()
    wave = torch.from_numpy(y.T.copy())
    reference = wave.mean(0)
    mean, deviation = reference.mean(), reference.std()
    if deviation < 1e-6:
        raise ValueError("Source is silent")
    with torch.no_grad():
        stems = apply_model(model, ((wave - mean) / deviation)[None], device="cpu",
                            shifts=1, split=True, overlap=.25, progress=True)[0]
        stems = stems * deviation + mean
    for name, audio in zip(model.sources, stems):
        sf.write(destination / f"{name}.wav", audio.T.numpy(), SR, subtype="FLOAT")
    save_json(destination / "separation.json", {
        "model": "htdemucs", "seed": 261015, "sampleRate": SR,
        "source": str(source), "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "duration": len(y) / SR, "sources": model.sources,
        "note": "Machine-separated stems; these are not original studio multitracks.",
    })


def measure(path):
    result = run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af",
                  "loudnorm=I=-13:TP=-1.7:LRA=9:print_format=json", "-f", "null", "-"])
    blocks = re.findall(r'\{\s*"input_i"[\s\S]*?\}', result.stderr)
    if not blocks:
        raise RuntimeError("No loudness measurement returned")
    raw = json.loads(blocks[-1])
    if not all(math.isfinite(float(raw[k])) for k in ["input_i", "input_tp", "input_lra"]):
        raise ValueError("Invalid/silent audio")
    return raw


def master_one(source, stem, output, title="My Audio Export"):
    before = measure(source)
    filtstr = ("loudnorm=I=-13:TP=-1.7:LRA=9:"
               f"measured_I={before['input_i']}:measured_TP={before['input_tp']}:"
               f"measured_LRA={before['input_lra']}:measured_thresh={before['input_thresh']}:"
               f"offset={before['target_offset']}:linear=true:print_format=json")
    wav, mp3 = output / f"{stem}.wav", output / f"{stem}.mp3"
    run(["ffmpeg", "-v", "info", "-nostats", "-y", "-i", source, "-af", filtstr,
         "-ar", SR, "-c:a", "pcm_s24le", wav])
    corrections = []

    def attenuate(decibels):
        safe = output / f"{stem}.peak-safe.wav"
        run(["ffmpeg", "-v", "error", "-y", "-i", wav, "-af", f"volume={decibels:.6f}dB",
             "-c:a", "pcm_s24le", safe])
        safe.replace(wav)
        corrections.append(decibels)

    # Loudnorm and MP3 encoding can overshoot their nominal true-peak setting.
    # Measure the actual files and preserve headroom with gain, not extra clipping.
    wav_peak = float(measure(wav)["input_tp"])
    if wav_peak > -1.9:
        attenuate(-1.95 - wav_peak)
    for attempt in range(3):
        run(["ffmpeg", "-v", "error", "-y", "-i", wav, "-c:a", "libmp3lame", "-b:a", "320k",
             "-metadata", f"title={title}", "-metadata", "artist=Independent creator",
             "-write_xing", "1", mp3])
        mp3_peak = float(measure(mp3)["input_tp"])
        if mp3_peak <= -1.5:
            break
        attenuate(-1.6 - mp3_peak)
    files = []
    for path in [wav, mp3]:
        m = measure(path)
        pcm = read_audio(path)
        files.append({"filename": path.name, "bytes": path.stat().st_size,
                      "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                      "audioDurationSeconds": len(pcm) / SR, "sampleRate": SR, "channels": 2,
                      "integratedLufs": float(m["input_i"]), "truePeakDbtp": float(m["input_tp"]),
                      "loudnessRangeLu": float(m["input_lra"]),
                      "clippedSamples": int(np.count_nonzero(np.abs(pcm) >= 1)),
                      "finite": bool(np.isfinite(pcm).all()),
                      "stereoCorrelation": float(np.corrcoef(pcm.T)[0, 1])})
        if files[-1]["clippedSamples"] or files[-1]["truePeakDbtp"] > -1.5:
            raise ValueError(f"Final-file peak check failed: {path}")
    return {"before": before, "postMasterGainCorrectionsDb": corrections, "files": files}


def compressor(y, threshold=.17, ratio=3., makeup=1., release=.09):
    """Linked channels, 1 ms peak envelope, smooth attack and release."""
    hop = 44
    pad = (-len(y)) % hop
    blocks = np.pad(np.max(np.abs(y), axis=1), (0, pad)).reshape(-1, hop).max(axis=1)
    env, state = np.zeros(len(blocks)), 0.
    attack_c, release_c = np.exp(-hop / SR / .003), np.exp(-hop / SR / release)
    for i, value in enumerate(blocks):
        c = attack_c if value > state else release_c
        state = c * state + (1 - c) * value
        env[i] = state
    gain = np.minimum(1, (np.maximum(env, 1e-8) / threshold) ** (1 / ratio - 1)) * makeup
    curve = np.interp(np.arange(len(y)), np.arange(len(gain)) * hop, gain)
    return (y * curve[:, None]).astype(np.float32)


def room(y, seconds=.65, predelay=.018, seed=1):
    """Small, decorrelated room; the dry signal is routed separately."""
    rng = np.random.default_rng(seed)
    t = np.arange(round(seconds * SR)) / SR
    ir = rng.normal(0, 1, (len(t), 2)).astype(np.float32)
    ir = filt(filt(ir, 430, "highpass"), 6500)
    ir *= np.exp(-t * 7 / seconds)[:, None]
    ir[:round(predelay * SR)] = 0
    ir /= np.sqrt(np.sum(ir ** 2, axis=0))
    return np.column_stack([signal.fftconvolve(y[:, c], ir[:, c])[:len(y)] for c in range(2)]).astype(np.float32)


def pitch_tempo(y, semitones, speed, directory):
    """Resample the voice/formants, then independently set its delivery speed.

    Both operations act on samples. Save the pre-EQ result for independent QA;
    changing event metadata alone cannot produce a passing audio measurement.
    """
    if not -12 <= semitones <= 12 or not .5 <= speed <= 2:
        raise ValueError("Voice pitch/speed is outside this project's range")
    rate = round(SR * 2 ** (semitones / 12))
    ratio = rate / SR
    key = hashlib.sha256(y.tobytes() + f"{rate}/{speed:.12f}".encode()).hexdigest()[:16]
    output = directory / f"pitch-tempo-{key}.wav"
    if not output.exists():
        source = directory / f"dry-{key}.wav"
        sf.write(source, y, SR, subtype="FLOAT")
        run(["ffmpeg", "-v", "error", "-y", "-i", source, "-af",
             f"asetrate={rate},aresample={SR},atempo={speed / ratio:.12f}",
             "-ar", SR, "-c:a", "pcm_f32le", output])
        source.unlink()
    return sf.read(output, dtype="float32", always_2d=True)[0], output


def tape_stop(y, seconds, end_rate=.10):
    """Continuous varispeed slowdown, with no segment joins or repeated grains."""
    n = round(seconds * SR)
    u = np.linspace(0, 1, n)
    # Choose the starting rate so the complete input fits the slowdown curve.
    shape = (1 - u) ** 1.45
    start_rate = (len(y) / n - end_rate) / shape.mean() + end_rate
    rates = end_rate + (start_rate - end_rate) * shape
    positions = np.cumsum(rates) - rates[0]
    result = np.column_stack([np.interp(positions, np.arange(len(y)), y[:, c], right=0)
                              for c in range(2)]).astype(np.float32)
    return fade(result, .012, .045), float(start_rate)
