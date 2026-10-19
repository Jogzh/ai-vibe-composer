import type { TrackDefinition } from '../music/types.ts';

/** Minimal scale/chord exercise. Replace this data with your own writing. */
export const starter: TrackDefinition = {
  meta: {
    id: 'starter', title: '你的创作起点', subtitle: 'YOUR FIRST SKETCH',
    artist: 'Music Creation Toolkit', bpm: 120, key: 'C major',
    tags: ['EDITABLE TEMPLATE', 'TONE.JS', 'ORIGINAL WORKSPACE'],
    description: '一个可编辑的八小节练习模板：替换音符、和弦与段落，选择音色，再试听和导出你自己的作品。An editable eight-bar sketch for your own music.',
  },
  production: 'emotional-pop', resolveHarmony: 0,
  edits: { hook: { startBar: 2, bars: 4 }, loop: { startBar: 2, bars: 4 } },
  arrangement: [
    { name: '01 / 起步 · Sketch', bars: 2, energy: 'tease' },
    { name: '02 / 练习 · Develop', bars: 4, energy: 'drop' },
    { name: '03 / 收束 · Resolve', bars: 2, energy: 'outro' },
  ],
  // Voicings last two bars in this recipe, so repeat each harmony twice.
  harmony: [
    { root: 36, chord: [52, 55, 59, 62] },
    { root: 36, chord: [52, 55, 59, 62] },
    { root: 33, chord: [48, 52, 55, 59] },
    { root: 33, chord: [48, 52, 55, 59] },
  ],
  hook: [
    [{ offset: 0, note: 72, length: 1, velocity: .65 }],
    [{ offset: 0, note: 74, length: 1, velocity: .65 }],
    [{ offset: 0, note: 76, length: 1, velocity: .65 }],
    [{ offset: 0, note: 79, length: 1, velocity: .65 }],
  ],
};
