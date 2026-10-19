# AI 作曲项目检索信息 / AI music project discovery

项目名称：**AI Vibe Composer · Vibe 作曲**。仓库：[`Jogzh/ai-vibe-composer`](https://github.com/Jogzh/ai-vibe-composer)。此前名称为 Music Creation Toolkit，内容持续作为可复用创作工具与声音资产维护。

## 定位 / Positioning

中文：**面向 AI 编程助手的开源作曲工具箱**。用自然语言描述音乐，让助手写 TypeScript 旋律、和弦与编曲，用 Tone.js / Web Audio 在本地渲染可播放 WAV / MP3；提供声音素材与 Python 音频处理。

English: **An open-source AI music composition toolkit for coding agents.** Vibe compose with an LLM: prompt, write editable melodies and arrangements, render audio locally, listen and revise. Includes licensed sounds, Tone.js / Web Audio, Python DSP and WAV / MP3 export.

AI 音乐生成在这里指代码驱动的 AI 辅助创作。仓库不内置神经网络文本转音乐模型，也不提供演唱合成。

## 检索词与入口 / Search terms and entry points

| 用户可能搜索 / Search intent | 对应内容 / Relevant entry point |
| --- | --- |
| AI 作曲、AI 编曲、AI 音乐生成、Vibe 作曲 | [中文首页](../README.md)、[工作流](ai-composition.md) |
| AI music composition, AI music generation, AI composer | [English README](../README.en.md) |
| Vibe coding music, vibe composing, LLM music, coding agents | [双语提示词 / Bilingual prompts](../PROMPTS.md)、[AGENTS.md](../AGENTS.md) |
| Algorithmic composition, generative music, Tone.js, Web Audio | [写谱与编曲 / Score and arrangement guide](getting-started.md) |
| Game BGM, sound library, CC0 samples, Python audio DSP | [声音 / Assets](assets.md)、[Python 工具 / Tools](python-tools.md) |

仓库名、中英文 About、GitHub topics、README 首段与 package metadata 使用一致定位。公开模板方便创作者通过 **Use this template** 开始自己的作品；中英文文档互链，提示词链接到真实文件与命令。

The repository name, bilingual About description, GitHub topics, README introductions and package metadata describe the same implemented workflow. Topics should reflect actual AI-assisted composition, code-driven music generation and the audio stack. Keep documentation links and clone URLs aligned with the repository name.

声音目录的中英文名称、音色族、MIDI 根音、BPM、调性与 tags 供本地检索和助手处理；SHA-256 和许可链接用于核查。新增素材后运行 `npm run assets:catalog`，并以 `npm run assets:check` 检查目录一致性。

The sound catalog supports local/agent discovery with bilingual names, families, pitch, tempo, key, tags, hashes and license links. These metadata describe available sounds; they do not imply every sound is already routed into a production recipe. Search ranking and indexing are controlled by external platforms.
