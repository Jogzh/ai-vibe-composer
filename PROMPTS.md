# AI 作曲提示词 / AI Music Composition Prompts

[AI 作曲指南 / Workflow](docs/ai-composition.md) · [中文](README.md) · [English](README.en.md)

把下面的请求交给能访问本仓库的 AI 编程助手。替换用途、BPM、音色与曲目 ID；这些是创作指令，不是已完成歌曲。当前配方为无歌词器乐，90–170 BPM、4/4 拍。

Give these briefs to an AI coding agent with repository access. Replace the purpose, tempo, sounds and track ID. These are prompts, not bundled songs. Existing recipes produce instrumental music at 90–170 BPM in 4/4.

## 1. 第一段游戏循环 / First game loop

```text
阅读 AGENTS.md、docs/ai-composition.md 和 src/music/types.ts。
为轻松解谜游戏写原创器乐循环：120 BPM、C 大调、明亮但不喧闹。
先做 8 小节草稿，旋律有清晰短动机、留出空拍，和弦长音避免重叠冲突。
新建 src/tracks/my-loop.ts 并注册，使用 emotional-pop 配方。
保持 hook/loop 裁切在实际编曲范围内，说明实际用了哪些声音与许可。
运行相关检查，导出 artifacts/my-loop-draft 的 WAV；给出实际音频路径，
说明是否真正耳听，再根据我的反馈扩为 16 小节。不要把成品加入模板提交。
```

```text
Read AGENTS.md, docs/ai-composition.md and src/music/types.ts.
Write an original instrumental loop for a relaxed puzzle game: 120 BPM, C major,
bright but unobtrusive. Start with an 8-bar draft, a short motif and deliberate rests;
avoid conflicting sustained chords. Add src/tracks/my-loop.ts and register it using
the emotional-pop recipe. Keep hook/loop edits inside the arrangement.
List the sounds actually used and their licenses. Run relevant checks and render a WAV
under artifacts/my-loop-draft. Report the real file path and whether you listened.
Use my feedback before expanding to 16 bars. Keep finished audio out of template commits.
```

## 2. 国风氛围配乐 / Chinese-inspired cinematic BGM

```text
用本仓库写一段原创国风器乐 BGM：96 BPM、D 小调五声音阶、16 小节，
适合山水游戏场景，前半段疏朗，后半段适度展开，不需要歌词或人声。
从 cinematic-guofeng 配方开始，先读其实际实现，区分合成器与实录采样。
先渲染 8 小节主题供试听，再扩写。新建 my-landscape 曲目并注册，
让旋律、和声、段落和裁切一致。需要额外声音时从 catalog.json 检索，
显式接入采样器并保留署名。导出可播放 WAV，报告具体实现和检查结果。
```

```text
Create original Chinese-inspired instrumental BGM for a landscape game scene:
96 BPM, D minor pentatonic, 16 bars, sparse at first and gently expanding, no vocals.
Start with cinematic-guofeng and read its implementation. Distinguish synthesized
instrument colors from recorded samples. Render an 8-bar theme for feedback first.
Add and register my-landscape; keep melody, harmony, structure and edits consistent.
If extra samples are needed, search catalog.json, integrate them explicitly and retain
credits. Deliver a playable WAV and report the implementation and checks performed.
```

## 3. 按听后反馈修改 / Revise from listening feedback

```text
修改我指定的曲目：[曲目 ID]。我的试听反馈：第 5–8 小节旋律太满，
低音在每句末尾遮盖主旋律，循环接缝有明显收尾感。
保留前 4 小节主题和 BPM，后半句减少音符并增加留白；先检查真实谱面、
音区与包络，再调整和声/低音或循环裁切。不要只改 seed 或调性文字。
新旧版本使用相同参数和长度，分别渲染到忽略目录便于我比较。
报告改动小节、实际音频文件和客观测量；不要把检查通过写成听起来更好。
```

```text
Revise this track: [track ID]. My listening feedback: bars 5–8 are too busy,
the bass masks phrase endings, and the loop feels like a final cadence.
Keep the opening 4-bar motif and tempo. Thin out the response and add rests.
Inspect the actual score, registers and envelopes before changing harmony, bass
or loop edits. Do not just change the seed or key label.
Render before/after versions with equal length and identical render parameters
to separate ignored output paths. Report changed bars, actual files and measurements;
do not present passing checks as a listening judgment.
```

## 4. 导出与交付 / Render and deliver

```text
为已注册曲目 [曲目 ID] 导出 full / hook / loop 的 WAV；如本机有 FFmpeg
及 MP3 编码器，也导出 MP3。先读 docs/mp3-export.md，用独立输出名避免
覆盖已有试听。报告每个实际文件的路径、时长、采样率和技术检查结果，
附实际使用素材的署名说明。音频放在 artifacts/，不加入模板提交。
```

```text
Render full / hook / loop WAV versions of the registered track [track ID].
Also export MP3 if FFmpeg with MP3 encoding is available. Read docs/mp3-export.md;
use separate output names to preserve earlier auditions. Report each actual path,
duration, sample rate and technical checks, plus credits for the samples used.
Keep audio under artifacts/ and out of template commits.
```
