# Music Creation Toolkit

**English** · [简体中文](README.md)

[![CI](https://github.com/Jogzh/music-creation-toolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/Jogzh/music-creation-toolkit/actions/workflows/ci.yml)
[![Code: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE)
[![Audio: mixed licenses](https://img.shields.io/badge/audio-CC0%20%2F%20CC%20BY-green.svg)](docs/assets.md)

**Create your own music with code and reusable sounds.** An open-source music production toolkit for original composition, procedural audio, sound design, game loops and video BGM. Includes Tone.js / Web Audio synthesis, TypeScript arrangement recipes, Python audio DSP, licensed sample libraries, CC0 drum loops, a browser audition player and offline MP3 / WAV export.

The repository contains reusable tools and sound assets. Finished songs, song-specific scores/scripts, source recordings, vocal stems and previous Git history are excluded. The default eight-bar `starter` is an editable exercise. The sample library includes reusable eight-bar loops and short asset previews.

## Quick start

Requires **Node.js >=22.12**, npm and a Web Audio browser. Browser playback and WAV export need no API key, Python or FFmpeg.

Choose **Use this template** on GitHub to start your own repository, or clone:

```sh
git clone https://github.com/Jogzh/music-creation-toolkit.git
cd music-creation-toolkit
npm ci
npm run dev
```

Open the URL printed by Vite:

- `/`: audition your editable arrangement; change BPM, transposition, seed and full / hook / loop versions; download WAV.
- `/palette.html`: browse, search, audition, loop and download sound assets.

Edit [`src/tracks/starter.ts`](src/tracks/starter.ts): `hook` contains melody events, `harmony` contains root notes and chord voicings, and `arrangement` defines sections. Register a new file in [`registry.ts`](src/tracks/registry.ts). See the bilingual [creation guide](docs/getting-started.md).

## Sounds and licenses

**83 audio files** are bundled under [`public/audio/`](public/audio/), with a searchable [JSON catalog](public/audio/catalog.json).

| Library | Files | Contents | Audio license |
| --- | ---: | --- | --- |
| Sound Palette | 43 | Marimba, xylophone, recorded percussion, synthesized electric piano, Sub/Reese bass, pad, transitions, drum/music loops and previews | CC0 1.0 |
| VSCO 2 CE | 25 | Flute, violin section, cello section and harp | CC0 1.0 |
| Salamander | 13 | Grand piano, one recording per sampled pitch | CC BY 3.0 |
| Teropa / DWSD | 2 | Closed and open hi-hats | CC BY; upstream does not specify a version |

**Project-owned code, documentation and starter score: MIT. Audio: each library's own license.** The entire sample library is not CC0. Credit the authors, source and license when using the Salamander or DWSD recordings. See [asset provenance and licensing](docs/assets.md). Choose the license for your own music while respecting the samples you actually use.

The synthesis/arrangement recipes cover electronic pop, cinematic Chinese-inspired music and Chinese-inspired club music. Reusable loops cover Lo-fi Soul, UK Garage / 2-step and Ambient Mallets. These are starting points, not a claim of complete genre coverage. The UI is primarily Chinese; English setup and API notes are provided in these docs.

## Offline MP3 / WAV rendering

The CLI renders with Chromium's real `OfflineAudioContext`:

```sh
npx playwright install chromium
npm run render -- --track starter --version hook --format wav --out artifacts/my-sketch
npm run render -- --track starter --version all --format both --out artifacts/my-work
npm run render -- --help
```

MP3 and loudness mastering require **FFmpeg / FFprobe**; MP3 requires `libmp3lame`. Options support 90–170 BPM, ±12 semitones, uint32 seeds, 44.1/48 kHz, and 16/24-bit WAV. Existing outputs are protected unless `--overwrite` is supplied. See [export options and measurements](docs/mp3-export.md). Keep your finished work in the ignored `artifacts/`, `releases/` or `outputs/` directories.

## Python audio DSP and asset generation

Python **3.11** is recommended. Lightweight processing uses NumPy, SciPy and SoundFile; Torch / Demucs are optional for source separation.

```sh
python3.11 -m venv .venv
.venv/bin/pip install -r scripts/requirements-palette.txt
.venv/bin/python scripts/audio_tools.py --help
.venv/bin/python scripts/audio_tools.py stretch my-recording.wav --speed 1.1 --out artifacts/faster.wav
.venv/bin/python scripts/audio_tools.py pitch-tempo my-voice.wav --semitones=-2 --speed 1.05 --out artifacts/voice-fx.wav
.venv/bin/python scripts/build_sound_palette.py verify
```

Includes pitch-preserving time stretch, separate pitch/tempo control, tape-stop, seeded room reverb, linked compression, mastering and optional source separation. `build_sound_palette.py build` reproduces CC0 recordings from a pinned upstream commit, procedural sounds and style loops. See [Python tools](docs/python-tools.md) and [sound recipes](docs/sound-palette.md).

## Validation and contributions

```sh
npm test
npm run build
npm run test:browser
npm run test:palette
npm run assets:check
.venv/bin/python -m unittest discover -s tests -p 'test_*.py'
```

Tests cover input validation, score cropping, PCM encoding, browser rendering, asset integrity, playback/download and objective audio checks. **Passing tests is not a listening review.** Bundled samples and short loops have not received a human listening review.

Contributions should include author, source URL, a clear redistribution license, pitch/BPM when applicable, and processing notes. Do not commit third-party songs, voices, model weights, credentials or finished music. See [CONTRIBUTING.md](CONTRIBUTING.md).

Derived from reusable parts of [Jogzh/ai-audio](https://github.com/Jogzh/ai-audio), with a fresh Git history and preserved code copyrights/sample credits. It runs independently of that project's local recordings or model cache.
