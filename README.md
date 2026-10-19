# Music Creation Toolkit · 开源音乐创作工具箱

[English](README.en.md) · **简体中文**

[![CI](https://github.com/Jogzh/music-creation-toolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/Jogzh/music-creation-toolkit/actions/workflows/ci.yml)
[![Code: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE)
[![Audio: mixed licenses](https://img.shields.io/badge/audio-CC0%20%2F%20CC%20BY-green.svg)](docs/assets.md)

**用代码和可复用声音资产创作自己的音乐。** 提供 Tone.js / Web Audio 编曲与合成、Python 音频 DSP、采样库、鼓循环、音效、浏览器试听，以及离线 MP3 / WAV 导出。

An open-source music creation toolkit for original composition, procedural audio, sound design and BGM: Tone.js, Web Audio, Python DSP, licensed samples, CC0 loops and offline audio rendering.

## 适合做什么

- 原创音乐、短视频 BGM、游戏循环配乐、音效和编曲实验。
- 用 TypeScript 写旋律、和弦、段落与音色；用 Python 处理自己的录音。
- 用 DAW、Web Audio 采样器或 AI 编程助手复用声音资产与生成脚本。
- 从电子流行、国风交响、国风 Club 配方，或 Lo-fi / UK Garage / Ambient 循环开始写自己的作品。

项目只保留**通用工具与声音资产**。没有已有歌曲的成品、专属谱面、制作脚本、源录音、人声分轨或历史提交。默认 `starter` 是八小节技术练习；声音库里的八小节循环与短试听是可复用素材，许可随目录保留。

## 三分钟开始

需要 **Node.js >=22.12**、npm 与支持 Web Audio 的浏览器。页面试听与 WAV 导出不要求 Python、API Key 或 FFmpeg。

点击 GitHub 的 **Use this template** 创建自己的仓库，或克隆本项目：

```sh
git clone https://github.com/Jogzh/music-creation-toolkit.git
cd music-creation-toolkit
npm ci
npm run dev
```

打开终端显示的网址：

- `/`：可编辑编曲的试听台，支持 BPM、移调、seed、full / hook / loop 和 WAV 下载。
- `/palette.html`：声音素材库，分类试听、循环播放、按名称搜索和下载。

**第一首自己的作品：**修改 [`src/tracks/starter.ts`](src/tracks/starter.ts) 的 `hook` 音符、`harmony` 和弦与 `arrangement` 段落，浏览器更新后试听；复制为新文件时，将其加入 [`registry.ts`](src/tracks/registry.ts)。详见[创作教程](docs/getting-started.md)。

## 声音资产与许可

共 **83 个音频文件**，位于 [`public/audio/`](public/audio/)，有可检索的[机器目录](public/audio/catalog.json)。

| 声音库 | 数量 | 内容 | 音频许可 |
| --- | ---: | --- | --- |
| Sound Palette | 43 | 马林巴、木琴、实录打击乐、合成电钢琴/Sub/Reese/Pad、转场、三组鼓与编曲循环和短试听 | CC0 1.0 |
| VSCO 2 CE | 25 | 长笛、小提琴组、大提琴组、竖琴 | CC0 1.0 |
| Salamander | 13 | 钢琴多音高采样，单条录音/音高 | CC BY 3.0 |
| Teropa / DWSD | 2 | 开/闭踩镲 | CC BY，上游未说明具体版本 |

**代码、文档与练习模板为 MIT；录音按各自许可。** 不把全部采样称为 CC0。使用 Salamander 或 DWSD 录音时保留作者、来源与许可署名；[资产与许可索引](docs/assets.md)包含完整入口。创作者为自己的作品选择许可，同时履行实际使用素材的要求。

## 离线导出 MP3 / WAV

CLI 使用真实 Chromium `OfflineAudioContext`。先安装浏览器：

```sh
npx playwright install chromium
npm run render -- --track starter --version hook --format wav --out artifacts/my-sketch
npm run render -- --track starter --version all --format both --out artifacts/my-work
npm run render -- --help
```

MP3 与响度母带需要 **FFmpeg / FFprobe**，MP3 还需 `libmp3lame`。支持 90–170 BPM、±12 半音、uint32 seed、44.1/48 kHz 和 16/24-bit WAV；同名输出默认拒绝覆盖。[导出指南](docs/mp3-export.md)说明参数和实际文件测量。作品输出到 Git 忽略的 `artifacts/`、`releases/` 或 `outputs/`。

## Python 音频工具与声音生成

推荐 Python **3.11**，轻量 DSP 与声音库生成只需 NumPy、SciPy、SoundFile；Torch / Demucs 仅用于可选的分离功能。

```sh
python3.11 -m venv .venv
.venv/bin/pip install -r scripts/requirements-palette.txt
.venv/bin/python scripts/audio_tools.py --help
.venv/bin/python scripts/audio_tools.py stretch my-recording.wav --speed 1.1 --out artifacts/faster.wav
.venv/bin/python scripts/audio_tools.py pitch-tempo my-voice.wav --semitones=-2 --speed 1.05 --out artifacts/voice-fx.wav
.venv/bin/python scripts/build_sound_palette.py verify
```

通用 DSP 包括保持音高的变速、独立 pitch/tempo、停带、合成房间、联动压缩、MP3/WAV 母带与可选源分离。`build_sound_palette.py build` 从固定上游 commit 复现 CC0 素材、合成音色和风格循环。详见 [Python 工具](docs/python-tools.md)及[声音配方](docs/sound-palette.md)。

## 验证与贡献

```sh
npm test
npm run build
npm run test:browser
npm run test:palette
npm run assets:check
.venv/bin/python -m unittest discover -s tests -p 'test_*.py'
```

自动检查覆盖参数、编曲裁切、PCM 编码、浏览器音频、素材索引、播放、下载与客观测量。**通过测试不代表进行过人工耳听。** 采样与现有短循环尚未经过人工听感审核，欢迎提交具体反馈。

新增声音请附作者、来源 URL、明确的再分发许可、根音/BPM（适用时）及处理记录。不要提交他人歌曲、人声、模型权重、凭证或自己的成品音频。贡献方法见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 项目结构

```text
src/tracks/       你的 TrackDefinition 与八小节练习模板
src/music/        类型、编曲配方、校验、随机源和混音路由
src/engine/       Tone.js 合成器、中国鼓、采样加载与离线渲染
src/audio/        WAV 编码与客观测量
public/audio/     83 个音频文件、目录和来源许可
scripts/          Chromium 导出、Python DSP、资产生成与索引
docs/             创作、采样、Python 与导出指南
tests/            参数、音频编码、DSP 与浏览器检查
```

源自 [Jogzh/ai-audio](https://github.com/Jogzh/ai-audio) 的通用创作能力，独立初始化并保留相关代码版权与第三方采样署名。此仓库用于创作自己的作品；不依赖原项目的本地音频或模型缓存。
