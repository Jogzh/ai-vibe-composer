import assert from 'node:assert/strict';
import test from 'node:test';
import { buildArrangement, validateOptions, validateTrack } from '../src/music/arrange.ts';
import { createRandom } from '../src/music/random.ts';
import { starter } from '../src/tracks/starter.ts';
import { defaultTrack, findTrack, trackRegistry } from '../src/tracks/registry.ts';
import type { RenderOptions, TrackDefinition } from '../src/music/types.ts';

const options: RenderOptions = { version: 'full', bpm: 120, transpose: 0, seed: 261019 };

test('registry exposes an editable sketch without finished compositions', () => {
  assert.equal(defaultTrack, starter);
  assert.deepEqual(trackRegistry, [starter]);
  assert.equal(findTrack('starter'), starter);
  assert.equal(findTrack('missing'), undefined);
  assert.equal(buildArrangement(starter, options).beats, 32);
});

test('invalid parameters and sample rates fail before composition', () => {
  for (const invalid of [
    { bpm: NaN }, { bpm: 89 }, { bpm: 171 }, { bpm: 120.5 },
    { transpose: -13 }, { transpose: 13 }, { transpose: .5 }, { seed: -1 },
    { seed: 2 ** 32 }, { seed: Infinity }, { version: 'other' }, { sampleRate: 96000 },
  ]) assert.throws(() => buildArrangement(starter, { ...options, ...invalid } as RenderOptions));
  for (const sampleRate of [44100, 48000] as const) {
    assert.doesNotThrow(() => validateOptions({ ...options, sampleRate }));
  }
});

test('templates reject invalid pitches, development, harmony, sections and edit ranges', () => {
  const patches = [
    (t: TrackDefinition) => { t.hook[0][0].note = NaN; },
    (t: TrackDefinition) => { t.hook[0][0].offset = 4; },
    (t: TrackDefinition) => { t.hook[0][0].length = 0; },
    (t: TrackDefinition) => { t.harmony[0].chord = [60, 64, 67]; },
    (t: TrackDefinition) => { t.harmony[0].root = -1; },
    (t: TrackDefinition) => { t.arrangement[0].bars = .5; },
    (t: TrackDefinition) => { t.edits!.hook.startBar = 8; },
    (t: TrackDefinition) => { t.resolveHarmony = 100; },
    (t: TrackDefinition) => { t.emotionalPop = { finalHook: [] }; },
    (t: TrackDefinition) => { t.production = 'unknown' as TrackDefinition['production']; },
  ];
  for (const patch of patches) {
    const track = structuredClone(starter);patch(track);
    assert.throws(() => validateTrack(track));
  }
});

test('short versions crop the actual score and retain section endpoints', () => {
  const full = buildArrangement(starter, options);
  for (const version of ['hook', 'loop'] as const) {
    const score = buildArrangement(starter, { ...options, version });
    const edit = starter.edits![version];
    const start = edit.startBar * 4, end = start + edit.bars * 4;
    const expected = full.events.filter(e => e.instrument !== 'texture' && e.beat >= start && e.beat < end)
      .map(e => ({ ...e, beat: e.beat - start, duration: Math.min(e.duration, end - e.beat) }));
    assert.deepEqual(score.events.filter(e => e.instrument !== 'texture'), expected);
    assert.equal(score.beats, edit.bars * 4);
    assert.equal(score.sections[0].start, 0);
    assert.equal(score.sections.at(-1)!.end, score.beats * 60 / options.bpm);
    assert.ok(score.events.every(e => e.beat >= 0 && e.beat + e.duration <= score.beats + 1e-9));
  }
});

test('all recipes accept a four-bar sketch and club development can use its default phrase', () => {
  for (const production of ['emotional-pop', 'cinematic-guofeng', 'guofeng-club'] as const) {
    const track = { ...structuredClone(starter), production };
    track.arrangement = [
      { name: 'Air', bars: 2, energy: 'air' },
      { name: 'Develop', bars: 4, energy: 'drop' },
      { name: 'Resolve', bars: 2, energy: 'outro' },
    ];
    const score = buildArrangement(track, options);
    assert.equal(score.beats, 32);
    assert.ok(score.events.length > 0);
    assert.ok(score.events.every(e => Number.isFinite(e.beat) && e.duration > 0 && Number.isFinite(e.velocity)));
    assert.ok(score.events.every(e => e.notes?.every(Number.isFinite) ?? true));
  }
});

test('seed preserves writing while transposition changes pitches without moving events', () => {
  const full = buildArrangement(starter, options);
  assert.deepEqual(full, buildArrangement(starter, options));
  const changed = buildArrangement(starter, { ...options, seed: 0 });
  assert.notDeepEqual(changed.events, full.events);
  assert.deepEqual(changed.events.filter(e => e.instrument === 'lead'), full.events.filter(e => e.instrument === 'lead'));
  const shifted = buildArrangement(starter, { ...options, transpose: 5 });
  assert.deepEqual(shifted.events, full.events.map(e => e.notes ? { ...e, notes: e.notes.map(n => n + 5) } : e));
  for (const seed of [0, 261019, 0xffffffff]) {
    const a = createRandom(seed), b = createRandom(seed);
    const sequence = Array.from({ length: 100 }, a);
    assert.deepEqual(sequence, Array.from({ length: 100 }, b));
    assert.ok(sequence.every(v => v >= 0 && v < 1));
  }
});
