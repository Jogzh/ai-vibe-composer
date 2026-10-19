#!/usr/bin/env python3
"""Audio tools for your own recordings; no song, voice or preset is bundled.

python scripts/audio_tools.py --help
"""
from __future__ import annotations

import argparse
from pathlib import Path
import tempfile

import numpy as np
import soundfile as sf

from audio_dsp import (SR, compressor, fade, master_one, pitch_tempo, read_audio,
                       room, save_json, separate, stretch, tape_stop)


def positive(value):
    result = float(value)
    if not np.isfinite(result) or result <= 0:
        raise argparse.ArgumentTypeError("Must be a finite positive number")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for command in ["stretch", "pitch-tempo", "tape-stop", "room", "compress", "separate", "master"]:
        p = sub.add_parser(command)
        p.add_argument("source", type=Path)
        p.add_argument("--out", type=Path, required=True, help="Output WAV, or directory for master/separate")
        p.add_argument("--overwrite", action="store_true")
        if command in ["stretch", "pitch-tempo"]:
            p.add_argument("--speed", type=positive, default=1.0, help="Playback speed; 1.1 is 10%% faster")
        if command == "pitch-tempo":
            p.add_argument("--semitones", type=float, default=0)
        if command in ["tape-stop", "room"]:
            p.add_argument("--seconds", type=positive, default=1.0)
        if command == "room":
            p.add_argument("--wet", type=float, default=.2)
        if command == "master":
            p.add_argument("--stem", default="my-mix")
            p.add_argument("--title", default="My Music")
        if command == "separate":
            p.add_argument("--model-cache", type=Path, default=Path("artifacts/model-cache"))
    args = parser.parse_args()
    if not args.source.is_file():
        parser.error("Source must be an existing audio file")
    if args.source.resolve() == args.out.resolve():
        parser.error("Output must differ from source")
    directory_output = args.command in ["master", "separate"]
    if directory_output and args.out.exists() and not args.out.is_dir():
        parser.error("This command requires an output directory")
    if args.out.exists() and not args.overwrite and (not directory_output or any(args.out.iterdir())):
        parser.error("Output already exists; choose a new path or pass --overwrite")
    if args.command == "master":
        if not args.stem or Path(args.stem).name != args.stem or args.stem in [".", ".."]:
            parser.error("Stem must be a single filename without directories")
        args.out.mkdir(parents=True, exist_ok=True)
        report = master_one(args.source, args.stem, args.out, args.title)
        save_json(args.out / f"{args.stem}.mastering.json", report)
    elif args.command == "separate":
        separate(args.source, args.out, args.model_cache)
    else:
        if args.out.suffix.lower() != ".wav":
            parser.error("DSP commands write 24-bit PCM .wav files")
        if hasattr(args, "speed") and not .5 <= args.speed <= 2:
            parser.error("Speed must be between 0.5 and 2")
        if args.command == "pitch-tempo" and (not np.isfinite(args.semitones) or not -12 <= args.semitones <= 12):
            parser.error("Semitones must be between -12 and 12")
        if args.command == "room" and (not np.isfinite(args.wet) or not 0 <= args.wet <= 1):
            parser.error("Wet must be between 0 and 1")
        y = read_audio(args.source)
        with tempfile.TemporaryDirectory(prefix="music-toolkit-") as folder:
            work = Path(folder)
            if args.command == "stretch":
                y = stretch(y, args.speed, work)
            elif args.command == "pitch-tempo":
                y, _ = pitch_tempo(y, args.semitones, args.speed, work)
            elif args.command == "tape-stop":
                if args.seconds < .1 or len(y) / SR > args.seconds * 4:
                    parser.error("Tape-stop needs >= 0.1 s output and a short input (<= 4x output duration)")
                y, _ = tape_stop(y, args.seconds)
            elif args.command == "room":
                if args.seconds <= .05:
                    parser.error("Room duration must exceed 0.05 s")
                y = y * (1 - args.wet) + room(y, seconds=args.seconds) * args.wet
            elif args.command == "compress":
                y = compressor(y)
        if not len(y) or not np.isfinite(y).all():
            parser.error("Processing produced empty or nonfinite audio")
        peak = float(np.max(np.abs(y)))
        if peak > .98:
            y *= .98 / peak
        args.out.parent.mkdir(parents=True, exist_ok=True)
        sf.write(args.out, y, SR, subtype="PCM_24")
        print(f"Wrote {args.out}: {len(y)/SR:.3f} s, {SR} Hz, 24-bit PCM")


if __name__ == "__main__":
    main()
