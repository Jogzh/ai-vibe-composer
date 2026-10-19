# 从八小节开始 / Create your first sketch

## 1. 运行 / Run

```sh
npm ci
npm run dev
```

浏览器打开终端给出的地址。`/` 是创作试听台；`/palette.html` 是支持中英文音色搜索、试听和下载的素材库。新仓库只内置可替换练习，不依赖任何本地歌曲文件。

Open the printed URL. `/` is the arrangement player, `/palette.html` is the searchable sound library. Edit source files to change the score; the player is not a piano-roll editor.

## 2. 写自己的音符 / Write your own notes

编辑 `src/tracks/starter.ts`：

```ts
hook: [
  [{ offset: 0, note: 72, length: 1, velocity: .65 }],
  [{ offset: 0, note: 74, length: 1, velocity: .65 }],
  [{ offset: 0, note: 76, length: 1, velocity: .65 }],
  [{ offset: 0, note: 79, length: 1, velocity: .65 }],
]
```

- 每个数组是一小节 4/4 拍。`offset` 是小节内起拍，范围 `0 <= offset < 4`。
- `note` 是整数 MIDI 音高（0–127），60 = C4，69 = A4 / 440 Hz。
- `length` 是以拍为单位的时值；`velocity` 为大于 0、至多 1 的力度。
- 建议音符在小节内结束；国风 Club 与旋律发展配置对此有校验。

Each nested array is one 4/4 bar. Time is measured in beats, pitch in MIDI note numbers, and velocity in `(0, 1]`. Replace this exercise with your own writing; changing only the seed does not write a new melody.

`harmony` 的 `root` 决定低音，`chord` 至少含四个合法 MIDI 音高。电子流行配方的和弦/Pad 常持续两小节，相邻两栏应配相同和声，避免低音与长音冲突。元数据 `key` 是说明文字，改变它不会自动移调；页面移调控件与 `transpose` 才会改变音高。

## 3. 安排段落 / Arrange sections

```ts
arrangement: [
  { name: 'Sketch', bars: 2, energy: 'tease' },
  { name: 'Develop', bars: 4, energy: 'drop' },
  { name: 'Resolve', bars: 2, energy: 'outro' },
],
edits: {
  hook: { startBar: 2, bars: 4 },
  loop: { startBar: 2, bars: 4 },
},
```

`startBar` 从 0 开始；短版必须落在完整编曲里。`full` 保留全编曲和尾音；`hook` 取指定段落并保留少量尾音；`loop` 取无额外尾长的循环，渲染预热周期承接空间效果。仍须实际试听循环接缝。

`production` 可选 `emotional-pop`、`cinematic-guofeng`、`guofeng-club`。这是实际编曲和音色配方切换，不是风格标签。后两者以合成器表达中国器乐色彩；仓库没有实录古筝/二胡/笛子库。Club 配方提供独立混音轨，播放器可独奏或移除声部。国风旋律宜使用对应音阶；`key` 标签不做调性检查。

## 4. 新建作品定义 / Add a track definition

复制 `starter.ts` 为新文件，改导出名称、`meta.id`、标题、旋律与和声，然后加入 `src/tracks/registry.ts`：

```ts
import { starter } from './starter.ts';
import { mySketch } from './my-sketch.ts';
export const trackRegistry = [starter, mySketch];
export const defaultTrack = mySketch;
export function findTrack(id: string) {
  return trackRegistry.find(track => track.meta.id === id);
}
```

`meta.id` 用唯一的字母/数字/连字符名称，供 CLI `--track` 和导出文件名使用。切换曲目后页面按定义重置 BPM。`meta` 与其他展示字段应来自可信本地代码。

Register your own `TrackDefinition` and use its `meta.id` with `--track`. The `seed` controls repeatable synthesis/touch variations, not guaranteed cross-browser byte identity.

## 5. 使用声音资产 / Use samples

素材页 WAV / MP3 可直接拖入 DAW 或导入自己的采样器。`public/audio/catalog.json` 索引全部 83 个音频，记录中英文名称、根音（适用时）、循环 BPM、相对路径、许可入口与散列。

```ts
const response = await fetch(`${import.meta.env.BASE_URL}audio/catalog.json`);
const catalog = await response.json();
const flutes = catalog.assets.filter((asset: { family: string }) => asset.family === 'flute');
```

`piano-samples.ts` 和 `acoustic-samples.ts` 也保留在 `src/engine/`。在 `Tone.Offline` 改变全局 context 前完成 `preparePianoSamples()` / `prepareAcousticSamples()`，再调用对应 getter。现有三种合成配方不会因为把采样文件放入目录就自动使用它们；需要在自己的采样器中映射音高、包络和增益。

## 6. 导出与验证 / Export and validate

```sh
npx playwright install chromium
npm run render -- --track starter --version hook --format wav --out artifacts/my-sketch
npm test
npm run build
npm run test:browser
npm run test:palette
npm run assets:check
```

MP3 / 母带见 [导出文档](mp3-export.md)。先试听短段，记录你真正听到的结果，再扩写；峰值、RMS、LUFS 或自动检查不是听感评价。生成的作品与分轨保存在忽略目录，代码与可再分发的通用资产才进入模板仓库。
