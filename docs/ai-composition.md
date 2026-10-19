# 用 AI 作曲 / Compose music with AI

[中文首页](../README.md) · [English overview](../README.en.md) · [提示词 / Prompts](../PROMPTS.md)

**AI Vibe Composer 的 AI 音乐生成路径是：自然语言需求 → AI 编程助手写谱和编曲 → 本地渲染音频 → 听后迭代。** 旋律与和声保存在 TypeScript，便于具体修改某个音符、段落或音色；音频由 Tone.js / Web Audio 产生。Python 用于可选的 DSP、素材生成与母带处理。

**AI-assisted composition here means prompt → coding agent → editable score → rendered audio → listening feedback.** Bring an assistant that can read/edit files and run commands, or apply its suggested code yourself. The repository supplies music tools and licensed sounds, rather than a bundled neural text-to-music service.

## 1. 准备环境 / Set up

```sh
npm ci
npm run dev
```

在另一个终端为 CLI 导出安装 Chromium：

In another terminal, install Chromium for CLI rendering:

```sh
npx playwright install chromium
```

需要 Node.js >=22.12。浏览器打开 Vite 的地址；`/` 用于试听编曲，`/palette.html` 用于按中英文名称、BPM、调性检索声音。WAV 不需要 FFmpeg；MP3 和响度母带需要 FFmpeg / FFprobe。AI 助手的安装、账户及模型配置由你选择。

Use Node.js >=22.12. The player auditions score code; it is not a chat box or piano-roll editor. WAV rendering needs no external music API. MP3/mastering requires FFmpeg / FFprobe. Your chosen assistant has its own setup requirements.

## 2. 给出创作约束 / Write a brief

告诉助手：用途、情绪、速度、调性、长度、核心音色、是否循环、是否有人声。可从[双语提示词](../PROMPTS.md)复制；没有把握的参数可以留给助手选择并解释。

Describe the use case, mood, BPM, key, length, main instruments, loop requirements and whether vocals are needed. Current recipes generate instrumental audio; a lyric request does not enable singing synthesis.

| 需求 / Brief field | 示例 / Example | 当前边界 / Current constraints |
| --- | --- | --- |
| 用途 / Purpose | 游戏循环 / Game loop; 视频 BGM / Video BGM | 完整、短版、循环 / full, hook, loop |
| 节拍 / Meter, tempo | 120 BPM, 4/4 | 90–170 BPM；现有乐谱为 4/4 / Existing score format uses 4/4 |
| 长度 / Length | 8 小节草稿 → 16 小节 / 8-bar draft → 16 bars | 120 BPM 下 16 小节主体约 32 秒，尾音另计 / About 32 seconds plus tails |
| 声音 / Sounds | 合成 Pad、钢琴、长笛 / Synth pad, piano, flute | 采样需显式接入配方 / Samples require explicit integration |
| 交付 / Delivery | WAV，必要时 MP3 / WAV, optionally MP3 | 输出在忽略目录 / Render to ignored output directories |

## 3. 把想法写成乐谱 / Turn the brief into a score

让助手先读 `AGENTS.md`、`src/music/types.ts` 和[写谱教程](getting-started.md)，从 `src/tracks/starter.ts` 创建自己的定义，再在 `src/tracks/registry.ts` 注册。音乐的可修改入口是：

| 文件或字段 / File or field | 作用 / Purpose |
| --- | --- |
| `src/tracks/<your-id>.ts` | 作品定义 / Your editable `TrackDefinition` |
| `hook` | 每小节的 MIDI 音符、起拍、时值、力度 / Per-bar melody events |
| `harmony` | 低音与和弦配置 / Bass roots and chord voicings |
| `arrangement` | 段落、小节数、能量 / Sections, bars and energy |
| `edits.hook`、`edits.loop` | 从 0 开始的裁切位置和长度 / Zero-based edit ranges |
| `production` | 实际编曲和音色配方 / Actual arrangement/synthesis recipe |
| `public/audio/catalog.json` | 83 项声音的元数据与许可入口 / Sound metadata and license links |

配方为 `emotional-pop`、`cinematic-guofeng`、`guofeng-club`。Lo-fi、Ambient 等素材循环可以复用，但不是任意风格的一键生成开关。`key` 只是文字；改调性要改音符或使用移调参数。`seed` 控制部分演奏/合成变化，不负责创作新的旋律。电子流行配方的和弦长音常持续两小节，和声栏应成对配置，详见写谱教程。

The three production recipes are concrete implementations. Adding a genre name or changing `meta.key` does not alter the musical notes or engine. Changing a seed is not composing a new melody. New sounds must be routed into the arrangement explicitly; placing a sample in a folder is insufficient.

## 4. 检查并渲染 / Check and render

```sh
npm test
npm run build
# Replace my-loop with the meta.id you registered.
npm run render -- --track my-loop --version hook --format wav --out artifacts/my-loop-draft
npm run render -- --track my-loop --version all --format both --out artifacts/my-loop-final
```

最后一条需要 FFmpeg 及 MP3 编码器；只需 WAV 时用 `--format wav`。`--version all` 导出 full / hook / loop。同名文件默认不覆盖；修改后换输出名，或在确实要替换时显式使用 `--overwrite`。参数详见[导出指南](mp3-export.md)。

The final command needs FFmpeg with MP3 encoding. Use `--format wav` for WAV only. Report actual output files and measurements. If the assistant cannot run the renderer, it should provide the command and state that no audio has been generated yet.

## 5. 先听草稿，再扩写 / Listen before expanding

听旋律是否记得住、和声是否冲突、低音是否遮盖主题、循环接缝是否明显，再描述具体修改位置。例如：“第 5–8 小节旋律太满，保留第一句动机、后半句留白；鼓不变，重新导出相同长度做对比。”

Listen for a memorable motif, clashing harmony, masked melody and loop seams. Give bar-specific feedback, such as “thin out bars 5–8, retain the opening motif, leave the drums unchanged, and render an equal-length comparison.” This makes iterations easier to evaluate.

测试和峰值、RMS、LUFS 等测量只能说明相应技术结果，不能代替耳听。助手应分别报告检查结果与实际听过的内容。素材用到 CC BY 时，保留[作者、来源和许可](assets.md)。

Keep listening claims separate from automated checks. Preserve required sample credits. In your own copy, keep your score edits for further work; rendered songs belong in `artifacts/`, `releases/` or `outputs/`. Contributions to this shared template should remain reusable tools, assets or documentation.
