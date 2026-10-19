# MP3 / WAV 导出 / Offline audio export

## 快速用法 / Quick use

```sh
npx playwright install chromium
npm run render -- --track starter --version hook --format wav --out artifacts/my-sketch
npm run render -- --track starter --version all --format both --out artifacts/my-work
npm run render -- --help
```

CLI 自行启动临时 Vite 服务，通过 Chromium 的真实 `OfflineAudioContext` 渲染，并在结束时关闭服务与浏览器。`starter` 是技术练习，换成自己注册的 `meta.id` 即可导出自己的作品。输出默认进入 Git 忽略目录，同名音频、母带报告或 manifest 已存在时拒绝覆盖；选择新 `--out` 或显式 `--overwrite`。

The CLI starts and stops its own Vite server and Chromium browser. Replace `starter` with your registered track ID. Existing files require explicit overwrite. Rendered songs and stems should remain in ignored output directories.

## 参数 / Options

| 参数 / Flag | 取值 / Values |
| --- | --- |
| `--version` | `full` / `hook` / `loop` / `all`（默认 all） |
| `--track` | registry 内的 `meta.id`，默认 starter |
| `--bpm` | 90–170 整数，默认作品定义的 BPM |
| `--transpose` | −12–12 整数半音 |
| `--seed` | 0–4294967295 整数，默认 260713 |
| `--sample-rate` | 44100 / 48000 |
| `--bit-depth` | 16 / 24，用于 WAV |
| `--format` | mp3（默认）/ wav / both |
| `--master` | auto（默认）/ off / loudness |
| `--out` | 相对当前目录或绝对路径 |

MP3 / 显式响度母带需要系统 FFmpeg、FFprobe；MP3 需 `libmp3lame`。`--format wav --master auto` 或 `off` 不需要 FFmpeg。依赖缺失时先失败，不创建无效输出。

`auto` 使用两遍 FFmpeg loudnorm 母带 MP3，保留 WAV 原始 PCM；`loudness` 也母带 WAV；`off` 只编码。Node 导出目标为 −14 LUFS、−1.5 dBTP、LRA 9，属于项目设置而非平台规范；最终实测可能因音频动态与有损编码偏离目标。Python 母带工具具有自己的默认目标，见 [Python 文档](python-tools.md)。

## 测量 / Measurements

使用 FFmpeg 时写出 `.mastering.json`，记录原始与最终输出的 integrated LUFS、true peak 与 LRA。`manifest.json` 记录参数、段落、PCM 统计与输出文件信息。原始 sample peak / RMS 不能当作最终编码的 LUFS / true peak；FFprobe 容器时长可能包含 MP3 padding，PCM 帧数给出内容时长。

Temporary files are cleaned up on success/failure. Tests cover valid PCM, two-pass normalization, final MP3 probing, silent-input failures, dependency failures and overwrite protection. Objective measurements are not a listening review.
