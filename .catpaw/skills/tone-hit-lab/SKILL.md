---
name: tone-hit-lab
description: 使用 Music Creation Toolkit 的声音资产、Tone.js 编曲配方和 Python DSP，帮助创作者写自己的音乐、试听并导出 MP3/WAV。
---

# 音乐创作工作流

1. 先读根目录 AGENTS.md、README.md、docs/getting-started.md 和 docs/assets.md。
2. 用途、情绪、BPM、长度与核心音色决定编曲。默认 starter 是可替换练习，不是既有成品。
3. 在 src/tracks/ 新建 TrackDefinition 并加入 registry；hook、harmony、arrangement、edits 必须一致。
4. 选用 emotional-pop、cinematic-guofeng 或 guofeng-club 的实际声音配方。增加风格需同步类型、校验、编曲、音源和测试，不能只改标签。
5. public/audio/ 保留署名与许可。MIDI 根音以 manifest / 原 SFZ 为准；合成器与单力度采样不能称为真实多力度录音。
6. 音乐创作交付可播放音频，输出到忽略的 artifacts/、releases/ 或 outputs/。不自动提交作品、人声、源录音、分轨、模型权重或凭证。
7. npm test、npm run build、npm run test:browser、npm run test:palette；音频检查只说明客观测量，不代表实际耳听。
8. 导出参数与许可见 docs/mp3-export.md、docs/assets.md；外部发布和 Git 操作按当前会话授权处理。

Python 工具：scripts/audio_tools.py，提供变速、pitch/tempo、停带、空间、压缩、可选人声分离与母带。脚本不下载歌曲或捆绑人声。声音资产生成见 scripts/build_sound_palette.py。
