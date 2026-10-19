#!/usr/bin/env node
import assert from 'node:assert/strict';
import { fileURLToPath } from 'node:url';
import { chromium } from 'playwright';
import { createServer } from 'vite';

const root = fileURLToPath(new URL('../', import.meta.url));
let server;
let browser;
try {
  server = await createServer({ root, server: { host: '127.0.0.1', port: 0, open: false }, logLevel: 'error' });
  await server.listen();
  const baseUrl = `http://127.0.0.1:${server.httpServer.address().port}`;
  browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ acceptDownloads: true });
  const pageErrors = [];
  page.on('pageerror', error => pageErrors.push(error.message));
  await page.goto(`${baseUrl}/?track=starter&version=hook`);
  await page.locator('#play').waitFor();
  assert.equal(await page.locator('#track-select').inputValue(), 'starter');
  assert.equal(await page.locator('#track-select option').count(), 1);
  assert.equal(await page.locator('#render-badge').textContent(), '等待合成');

  const checks = await page.evaluate(async () => {
    const { getTailSeconds, renderTrack } = await import('/src/engine/render.ts');
    const { starter } = await import('/src/tracks/starter.ts');
    const { defaultTrack, trackRegistry } = await import('/src/tracks/registry.ts');
    const { encodeWav, measureAudio } = await import('/src/audio/wav.ts');
    const options = { version: 'hook', bpm: starter.meta.bpm, transpose: 0, seed: 261013 };
    const finite = buffer => Array.from({ length: buffer.numberOfChannels }, (_, channel) => buffer.getChannelData(channel).every(Number.isFinite)).every(Boolean);
    const hook = await renderTrack(starter, options);
    const full = await renderTrack(starter, { ...options, version: 'full' });
    const loop = await renderTrack(starter, { ...options, version: 'loop' });
    const otherRecipes = [];
    for (const production of ['cinematic-guofeng', 'guofeng-club']) {
      const audio = await renderTrack({ ...structuredClone(starter), production }, options);
      otherRecipes.push({ production, stats: audio.stats, finite: finite(audio.buffer) });
    }
    const invalid = structuredClone(starter);
    invalid.hook[0][0].note = NaN;
    let invalidHandled = false;
    try { await renderTrack(invalid, options); } catch { invalidHandled = true; }
    return {
      registry: { defaultId: defaultTrack.meta.id, ids: trackRegistry.map(track => track.meta.id) },
      hook: { duration: hook.duration, stats: hook.stats, finite: finite(hook.buffer), channels: hook.buffer.numberOfChannels, rate: hook.buffer.sampleRate },
      full: { duration: full.duration, stats: full.stats, finite: finite(full.buffer), channels: full.buffer.numberOfChannels, rate: full.buffer.sampleRate, sections: full.sections.length },
      loop: { duration: loop.duration, stats: loop.stats, finite: finite(loop.buffer), channels: loop.buffer.numberOfChannels, rate: loop.buffer.sampleRate, frames: loop.buffer.length },
      expectedHook: starter.edits.hook.bars * 4 * 60 / options.bpm + getTailSeconds(starter, 'hook'),
      expectedLoop: starter.edits.loop.bars * 4 * 60 / options.bpm,
      wavSize: encodeWav(hook.buffer).byteLength,
      expectedWavSize: 44 + hook.buffer.length * hook.buffer.numberOfChannels * 2,
      invalidHandled,
      sourceStats: measureAudio(hook.buffer),
      otherRecipes,
    };
  });

  assert.deepEqual(checks.registry.ids, ['starter']);
  assert.equal(checks.registry.defaultId, 'starter');
  for (const rendered of [checks.hook, checks.full, checks.loop]) {
    assert.equal(rendered.channels, 2);
    assert.ok([44100, 48000].includes(rendered.rate));
    assert.equal(rendered.finite, true);
    assert.ok(rendered.stats.peak > 0.05 && rendered.stats.rms > 0.001, 'audio must be non-silent');
    assert.equal(rendered.stats.clippedSamples, 0);
  }
  assert.ok(Math.abs(checks.hook.duration - checks.expectedHook) < 1 / checks.hook.rate);
  assert.ok(Math.abs(checks.loop.duration - checks.expectedLoop) < 1 / checks.loop.rate);
  assert.equal(checks.wavSize, checks.expectedWavSize);
  assert.equal(checks.invalidHandled, true);
  for (const recipe of checks.otherRecipes) {
    assert.equal(recipe.finite, true, recipe.production);
    assert.ok(recipe.stats.peak > .05 && recipe.stats.rms > .001, recipe.production);
    assert.equal(recipe.stats.clippedSamples, 0, recipe.production);
  }
  await page.locator('#play').click();
  await page.locator('#render-badge').waitFor({ state: 'visible', timeout: 300000 });
  await page.waitForFunction(() => document.querySelector('#render-badge')?.textContent === '合成完成', undefined, { timeout: 300000 });
  assert.equal(pageErrors.length, 0, pageErrors.join('; '));
  console.log('PASS: starter-only registry, browser render, WAV export, validation and playback UI');
} finally {
  await browser?.close();
  await server?.close();
}
