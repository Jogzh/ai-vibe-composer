#!/usr/bin/env node
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readFile, readdir, writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import { inspectPcmWav } from './lib/audio-export.mjs';

const root = fileURLToPath(new URL('../public/audio/', import.meta.url));
const json = async file => JSON.parse(await readFile(path.join(root, file), 'utf8'));
const palette = await json('palette/manifest.json');
const vsco = await json('vsco/sample-manifest.json');
const drums = await json('teropa-drums/provenance.json');
const names = { flute: '长笛', strings: '小提琴组', cello: '大提琴组', harp: '竖琴' };
const assets = [];

async function add(entry, expectedHash) {
  const bytes = await readFile(path.join(root, entry.file));
  const sha256 = createHash('sha256').update(bytes).digest('hex');
  if (expectedHash) assert.equal(sha256, expectedHash, `${entry.id}: source manifest hash`);
  if (entry.file.endsWith('.wav')) {
    const info = await inspectPcmWav(path.join(root, entry.file));
    entry = { ...entry, sampleRate: info.sampleRate, channels: info.channels,
      frames: Math.round(info.durationSeconds * info.sampleRate), seconds: info.durationSeconds };
  }
  assets.push({ ...entry, bytes: bytes.length, sha256 });
}

for (const asset of palette.assets) {
  await add({ ...asset, id: `palette-${asset.id}`, file: `palette/${asset.file}`,
    nameEn: asset.id.replaceAll('-', ' '), bank: 'palette', licenseFile: 'palette/ATTRIBUTION.md',
    tags: ['sound-design', asset.family, asset.category] }, asset.sha256);
}
for (const asset of vsco.samples) {
  await add({ id: `vsco-${asset.instrument}-${asset.name}`, name: `${names[asset.instrument]} ${asset.name}`,
    nameEn: `${asset.instrument} ${asset.name}`, bank: 'vsco', category: 'orchestral', family: asset.instrument,
    file: `vsco/${asset.file}`, rootMidi: asset.midi, seconds: asset.durationSeconds,
    sampleRate: vsco.sampleRate, channels: vsco.channels, license: 'CC0-1.0',
    licenseFile: 'vsco/ATTRIBUTION.md', tags: ['acoustic', 'orchestral', asset.instrument],
    sourceUrl: `https://github.com/sgossner/VSCO-2-CE/blob/${vsco.commit}/${asset.path.split('/').map(encodeURIComponent).join('/')}` }, asset.assetSha256);
}
for (const [midi, name] of [[45,'A2'],[48,'C3'],[51,'Ds3'],[54,'Fs3'],[57,'A3'],[60,'C4'],[63,'Ds4'],[66,'Fs4'],[69,'A4'],[72,'C5'],[75,'Ds5'],[78,'Fs5'],[81,'A5']]) {
  await add({ id: `salamander-${name}`, name: `钢琴 ${name}`, nameEn: `grand piano ${name}`, bank: 'salamander',
    category: 'piano', family: 'piano', file: `salamander/${name}.mp3`, rootMidi: midi,
    license: 'CC-BY-3.0', licenseFile: 'salamander/ATTRIBUTION.md', tags: ['piano', 'acoustic', '钢琴'],
    sourceUrl: `https://tonejs.github.io/audio/salamander/${name}.mp3` });
}
for (const asset of drums.files) {
  const closed = asset.file === 'hatClosed.wav';
  await add({ id: `teropa-${closed ? 'closed' : 'open'}`, name: closed ? '实录闭镲' : '实录开镲',
    nameEn: closed ? 'closed hi-hat' : 'open hi-hat', bank: 'teropa-drums', category: 'drums', family: 'hi-hat',
    file: `teropa-drums/${asset.file}`, license: 'CC BY (version unspecified)',
    licenseFile: 'teropa-drums/ATTRIBUTION.md', tags: ['hi-hat', 'drums', '踩镲'], sourceUrl: drums.originalCollection }, asset.sha256);
}
const files = (await readdir(root, { recursive: true })).filter(file => /\.(mp3|wav)$/i.test(file)).map(file => file.split(path.sep).join('/')).sort();
assert.deepEqual(assets.map(asset => asset.file).sort(), files, 'Catalog must cover every audio file exactly once');
assert.equal(new Set(assets.map(asset => asset.id)).size, assets.length);
for (const asset of assets) await readFile(path.join(root, asset.licenseFile));
const output = JSON.stringify({ schemaVersion: 1, name: 'AI Vibe Composer audio catalog',
  description: '可复用声音资产 / Reusable sound assets; see per-file licenses', assets }, null, 2) + '\n';
const target = path.join(root, 'catalog.json');
if (process.argv.includes('--check')) {
  assert.equal(await readFile(target, 'utf8'), output, 'Catalog is stale; run npm run assets:catalog');
  console.log(`PASS: ${assets.length} indexed audio files, source hashes, licensing links and catalog freshness.`);
} else {
  await writeFile(target, output);
  console.log(`Indexed ${assets.length} audio files in public/audio/catalog.json`);
}
