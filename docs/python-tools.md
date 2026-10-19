# Python 音频工具 / Python audio tools

## 安装 / Setup

轻量工具推荐 Python 3.11：

```sh
python3.11 -m venv .venv
.venv/bin/pip install -r scripts/requirements-palette.txt
.venv/bin/python scripts/audio_tools.py --help
```

FFmpeg 负责音频解码、保留音高的 `atempo` 和编码；母带另需 libmp3lame。没有内置歌曲、声音克隆模型或歌手录音。输入音源由使用者提供。

Lightweight tools use NumPy, SciPy and SoundFile. Install FFmpeg separately. Supply your own audio. Default DSP layout is 44.1 kHz stereo float; CLI DSP outputs are 24-bit WAV and avoid sample clipping with gain reduction when necessary.

## 命令 / Commands

```sh
# 变速但保留音高 / Pitch-preserving stretch
.venv/bin/python scripts/audio_tools.py stretch input.wav --speed 1.1 --out artifacts/faster.wav

# 独立调音高和速度；不是保持共振峰的人声算法
# Separate pitch and speed; formants are not preserved
.venv/bin/python scripts/audio_tools.py pitch-tempo input.wav --semitones=-2 --speed 1.05 --out artifacts/pitched.wav

# 对短片段做停带 / Tape-stop on a short clip
.venv/bin/python scripts/audio_tools.py tape-stop short.wav --seconds 2 --out artifacts/stopped.wav

# 混合程序生成房间空间 / Seeded synthetic room
.venv/bin/python scripts/audio_tools.py room input.wav --seconds .8 --wet .2 --out artifacts/room.wav

# 双声道联动压缩 / Linked stereo compression
.venv/bin/python scripts/audio_tools.py compress input.wav --out artifacts/compressed.wav

# 双遍响度母带和最终文件检查 / Mastering and final-file measurements
.venv/bin/python scripts/audio_tools.py master input.wav --out artifacts/master --stem my-mix --title 'My Music'
```

`--out` 不能与源文件相同。文件或非空输出目录已存在时默认拒绝，替换需 `--overwrite`。`--speed` 为 0.5–2，半音范围 ±12。`master` 输出 WAV、320 kbps MP3 和 `.mastering.json`，项目目标与 CLI 的 Node 导出配置不同：Python 该工具使用 −13 LUFS，正常化 true peak 为 −1.7 dBTP，并检查最终编码结果，可能再减增益；不要把目标值写作实测。

`audio_dsp.py` 可直接导入 `read_audio`、`filt`、`fade`、`stereo`、`stretch`、`compressor`、`room`、`pitch_tempo`、`tape_stop`、`measure`、`master_one`。无歌曲专属类、预设或硬编码输入片段。

## 可选分离 / Optional source separation

只有分离功能需要较大的 Torch / Demucs 依赖与模型下载：

```sh
.venv/bin/pip install -r scripts/requirements-dj.txt
.venv/bin/python scripts/audio_tools.py separate input.wav --out artifacts/stems
```

该命令会通过 Demucs 获取 `htdemucs` 模型并在 CPU 上运行；权重缓存位于 `artifacts/model-cache/`，不入 Git。机器分离结果不是原录音室分轨，不会转移输入作品的版权。此可选功能不在默认 CI 下载模型运行；轻量 DSP 使用生成信号做集成验证。

## 素材生成 / Asset generation

```sh
.venv/bin/python scripts/build_sound_palette.py build
npm run assets:catalog
.venv/bin/python scripts/build_sound_palette.py verify
npm run assets:check
```

第一次 build 从固定 commit 下载 CC0 源录音；下载缓存位于忽略目录。生成器内含基础合成配方，风格谱面位于 `scripts/presets/sound-palette.json`，不包含已完成歌曲。细节见 [声音素材说明](sound-palette.md)。
