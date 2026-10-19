# 声音资产与许可 / Audio assets and licensing

共 83 个音频文件；机器目录 [`public/audio/catalog.json`](../public/audio/catalog.json) 包含 `id`、中文 `name`、`nameEn`、`family`、`bank`、`category`、`file`、`license`、`licenseFile`、`tags`、`sha256` 和文件大小。适用时提供 `rootMidi`、`bpm`、`bars`、`loop`、采样率/声道与时长；未测得的字段不伪造值，浏览器播放时可读取真实媒体时长。

The JSON catalog indexes 83 audio files. Paths are relative to `public/audio/`. Not all files are CC0. Read each entry's `licenseFile`, preserve sample credits, and choose the license of your own writing separately.

| 库 / Bank | 文件 / Files | 许可 / License | 作者、来源与处理 / Provenance |
| --- | ---: | --- | --- |
| Sound Palette | 43 | CC0 1.0 Universal | [录音、原创合成与循环说明](../public/audio/palette/ATTRIBUTION.md)；[原 CC0 全文](../public/audio/palette/sources/LICENSE) |
| VSCO 2 Community Edition | 25 | CC0 1.0 Universal | [Sam Gossner / Versilian Studios、Simon Dalzell / Ivy Audio、Elan Hickler / Soundemote](../public/audio/vsco/ATTRIBUTION.md) |
| Salamander Grand Piano v3 | 13 | CC BY 3.0 Unported | [Alexander Holm；Tone.js MP3 分发](../public/audio/salamander/ATTRIBUTION.md) |
| Teropa / DWSD hi-hats | 2 | CC BY，版本未由上游说明 | [DWSD、Freesound、teropa/drumkit](../public/audio/teropa-drums/ATTRIBUTION.md) |

本库没有歌手录音、商业歌曲或拆分人声。CC0 的短风格试听是可复用资产预览；WAV 编曲循环为 8 小节。MP3 预览带淡出，拼接循环使用对应 WAV。不要把合成中国器乐配方描述为实录民族乐器。

## 可复用署名 / Suggested attribution

使用 Salamander 时可采用以下格式，并注明对采样进行的变调、包络或混音等处理：

> Piano recordings: Alexander Holm, Salamander Grand Piano v3, CC BY 3.0. Source: https://archive.org/details/SalamanderGrandPianoV3 ; MP3 distribution: https://tonejs.github.io/audio/salamander/ . Modified through pitch playback, envelopes and mixing.

使用 DWSD 踩镲时保留：

> Hi-hat recordings: DWSD, Deep House Drum kit, Creative Commons Attribution (version unspecified by upstream). Distributed via @teropa/drumkit 1.1.0. Source: https://freesound.org/people/DWSD/packs/11575/ . Converted from MP3 to 24-bit / 44.1 kHz WAV.

具体使用方式的授权以原许可为准。代码的 MIT 不会重新授权录音；公开仓库也不会自动改变作者许可。CC0 免署名，仍欢迎保留原作者与来源。

## 索引与验证 / Catalog and integrity

```sh
npm run assets:catalog
npm run assets:check
npm run test:palette
python scripts/build_sound_palette.py verify
```

`assets:catalog` 根据各库 manifest 与本地文件生成统一目录；`assets:check` 核对文件散列、许可路径、全量覆盖与目录新鲜度，不访问网络、不依赖 FFmpeg。修改或重建素材后重新生成目录。`verify` 对 Palette 做解码、电平、准确循环帧数和边界检查；需要 Python 依赖及 FFmpeg。

Piano sample hashes are computed from the bundled files for integrity, not evidence of an independent upstream comparison. VSCO / Palette / Teropa entries are also checked against their respective existing manifests. Pitches use scientific MIDI mapping; some upstream WAV names use a different octave convention. No automatic checks substitute for a human listening review.
