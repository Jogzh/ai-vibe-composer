# 协作约定

- Git commit 的标题与说明使用中文，技术名称、文件名可保留英文。
- 音乐创作需交付可播放音频。区分参考资料、客观音频测量与实际耳听，不把自动检查通过当作听感评价。

## AI 作曲入口 / AI composition entry point

AI Vibe Composer 是面向 AI 编程助手的音乐创作工具箱。助手编写可编辑的乐谱与编曲代码，Tone.js / Web Audio 渲染声音；仓库不内置文本直出音乐模型。

Read [the workflow](docs/ai-composition.md), [score guide](docs/getting-started.md) and [asset licenses](docs/assets.md) before composing. [PROMPTS.md](PROMPTS.md) contains bilingual briefs and revision requests.

1. 根据用户的用途、情绪、BPM、时长与音色写作；未指定时采用合理默认并说明。先做短草稿，再根据实际试听反馈展开。
2. 阅读 `src/music/types.ts`；在 `src/tracks/` 创建 `TrackDefinition` 并加入 `registry.ts`。`starter` 是可替换练习，改变 seed 或标题不等于新旋律。
3. `hook`、`harmony`、`arrangement`、`edits` 必须一致。BPM 当前为 90–170，4/4 拍，MIDI 音高 0–127。`key` 是说明文字，改标签不会改变音符。
4. 实际配方为 `emotional-pop`、`cinematic-guofeng`、`guofeng-club`。新风格需要相应编曲和声音实现。合成中国器乐音色不等于实录；采样文件也不会自动进入混音。
5. 用 `public/audio/catalog.json` 按音色、BPM、根音和许可选择素材，保留来源与署名。只有明确标注的 CC0 素材才是 CC0。
6. 运行 `npm test`、`npm run build`；音频引擎或播放器改动再运行 `npm run test:browser`，资产/素材页改动运行 `npm run assets:check` 和 `npm run test:palette`。
7. 运行 `npm run render -- --track <id> --version hook --format wav --out artifacts/<id>` 交付草稿。首次需 `npx playwright install chromium`；MP3 需 FFmpeg。完整参数见 `docs/mp3-export.md`。
8. 输出到忽略的 `artifacts/`、`outputs/` 或 `releases/`，报告实际文件路径、时长、检查结果与素材署名。没有实际耳听就如实说明，按用户反馈迭代。

This shared template keeps generic tools, licensed assets and the starter exercise. Do not add finished songs or song-specific scores/scripts as template contributions. In a user's own copy, create requested scores locally; keep renders, voices, stems, credentials, caches and model weights out of template commits. See [CONTRIBUTING.md](CONTRIBUTING.md).
