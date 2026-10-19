# AI Vibe Composer · AI Music Composition Toolkit

**English** · [简体中文](README.md)

[![CI](https://github.com/Jogzh/ai-vibe-composer/actions/workflows/ci.yml/badge.svg)](https://github.com/Jogzh/ai-vibe-composer/actions/workflows/ci.yml)
[![Code: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE)
[![Audio: mixed licenses](https://img.shields.io/badge/audio-CC0%20%2F%20CC%20BY-green.svg)](docs/assets.md)

**Describe your music, let an AI coding agent write the score, then listen and export WAV / MP3.** An open-source toolkit for AI-assisted music composition, AI music generation through code, vibe coding, game soundtracks and video BGM. Melodies, chords and arrangements remain editable TypeScript; Tone.js / Web Audio renders the audio, with licensed sounds and optional Python DSP.

[AI composition workflow](docs/ai-composition.md) · [Copyable prompts](PROMPTS.md) · [Score guide](docs/getting-started.md) · [Sounds and licenses](docs/assets.md)

The workflow is **prompt → AI-written score and arrangement code → local audio rendering → listening and revision**. Bring your own coding assistant or LLM. This repository does not bundle a neural text-to-music model. Playback and WAV rendering run locally; your chosen AI assistant has its own setup and requirements.

## Start composing with AI

After setup, give an assistant that can edit this repository and run commands this prompt:

```text
Read AGENTS.md and docs/ai-composition.md. Create an original instrumental game loop:
bright, 120 BPM, C major, 16 bars, with space between melodic phrases.
Render an 8-bar draft for feedback before expanding. Add src/tracks/my-loop.ts and register it.
Keep melody, harmony, sections and hook/loop edits consistent. Use supported production recipes
and licensed sounds; implement any new timbres explicitly. Run the relevant checks and export
a playable WAV under artifacts/my-loop. Report the output path, sample credits and measurements.
State whether you actually listened, then use my listening feedback to revise.
```

MP3 export additionally needs FFmpeg. If your assistant only provides code, apply it and run the [export commands](docs/mp3-export.md) yourself. See [bilingual prompts](PROMPTS.md) for composition, arrangement revision and delivery.

The repository contains reusable tools and sound assets. Finished songs, song-specific scores/scripts, source recordings, vocal stems and previous Git history are excluded. The default eight-bar `starter` is an editable exercise. The sample library includes reusable eight-bar loops and short asset previews.

## Quick start

Requires **Node.js >=22.12**, npm and a Web Audio browser. Browser playback and WAV export need no API key, Python or FFmpeg.

Choose **Use this template** on GitHub to start your own repository, or clone:

```sh
git clone https://github.com/Jogzh/ai-vibe-composer.git
cd ai-vibe-composer
npm ci
npm run dev
```

Open the URL printed by Vite:

- `/`: audition your editable arrangement; change BPM, transposition, seed and full / hook / loop versions; download WAV.
- `/palette.html`: browse, search, audition, loop and download sound assets.

Use the AI prompt above, or edit [`src/tracks/starter.ts`](src/tracks/starter.ts) manually: `hook` contains melody events, `harmony` contains root notes and chord voicings, and `arrangement` defines sections. Register a new file in [`registry.ts`](src/tracks/registry.ts). See the bilingual [AI workflow](docs/ai-composition.md) and [score guide](docs/getting-started.md).

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
