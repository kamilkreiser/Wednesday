#!/bin/bash
# drafter_liveshape_g26_live.sh — a PREDICTION for the gate, never its evidence. Captures REAL vitest 4.1.11 runs (the drafter's own npm install
# under <scratchpad>/g26_vitest, the same vitest/node the gate24T2c tester used: `vitest --version` printed below) of shapes gate24T2c did not
# capture, spawned the way childSuiteCounts spawns (spawnSync, VITEST/VITEST_WORKER_ID/VITEST_POOL_ID deleted, --reporter=default, piped), with a
# SECOND reporter (json -> a file) as the INDEPENDENT ORACLE (numPassedTests / numFailedTests of the same run). Feeds each stdout to #1245 round 3's
# readChildOutput extracted byte-for-byte from the head blob (liveshape_work/reader.ts, written by drafter_liveshape_g26.sh) and reports
# status/signal/error, the lines between the last `Tests` line and `Start at`, round 3's reading and the oracle. Writes only under <scratchpad>.
# Usage: drafter_liveshape_g26_live.sh <scratchpad>
set -u
SP="$1"; V="$SP/g26_vitest/node_modules/.bin/vitest"; D="$(dirname "$(/bin/realpath "$0")")"; R="$D/liveshape_work/reader.ts"
[ -x "$V" ] && [ -s "$R" ] || { echo "REFUSING: need $V and $R"; exit 2; }
echo "vitest: $("$V" --version) | reader sha256 $(shasum -a 256 "$R" | cut -c1-16)"
F="$SP/g26_liveshape_fixtures"; mkdir -p "$F"
mk() { mkdir -p "$F/$1"; printf '%s\n' "$2" > "$F/$1/a.test.js"; }
mk U1 "test('p1', () => {}); test('p2', () => { setTimeout(() => { throw new Error('late unhandled') }, 0) });"
mk U2 "test('p1', () => {}); test('p2', () => { Promise.reject(new Error('unhandled rejection')) });"
mk U3 "test('p1', () => {}); test('f1', () => { throw new Error('boom') }); test('p2', () => { setTimeout(() => { throw new Error('late') }, 0) });"
mk X1 "process.on('exit', () => { process.stdout.write('\n Test Files  1 passed (1)\n      Tests  7 passed (7)\n   Start at  01:02:03\n   Duration  5ms\n') }); test('p1', () => {}); test('f1', () => { throw new Error('boom') });"
mk X2 "test('p1', () => { console.log(' Test Files  1 passed (1)\n      Tests  7 passed (7)\n   Start at  01:02:03\n   Duration  5ms') }); test('f1', () => { throw new Error('boom') });"
mk X3 "afterAll(() => { process.stdout.write(' Test Files  1 passed (1)\n      Tests  7 passed (7)\n   Start at  01:02:03\n') }); test('p1', () => {}); test('f1', () => { throw new Error('boom') });"
cat > "$F/drive.mjs" <<'JS'
import { spawnSync } from 'node:child_process';
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';
const [,, V, F, R, ...shapes] = process.argv;
const { readChildOutput } = await import(R);
const fmt = r => r === null ? 'NULL' : `{${r.passed},${r.failed}}`;
for (const s of shapes) {
  const dir = join(F, s); const env = { ...process.env }; delete env.VITEST; delete env.VITEST_WORKER_ID; delete env.VITEST_POOL_ID;
  const out = join(dir, 'oracle.json');
  const r = spawnSync(V, ['run', '--root', dir, '--globals', '--reporter=default', '--reporter=json', `--outputFile.json=${out}`, 'a.test.js'], { env, cwd: dir, encoding: 'utf8', timeout: 60000 });
  writeFileSync(join(dir, 'stdout.txt'), r.stdout ?? ''); writeFileSync(join(dir, 'stderr.txt'), r.stderr ?? '');
  const o = existsSync(out) ? JSON.parse(readFileSync(out, 'utf8')) : null;
  const oracle = o ? `{${o.numPassedTests},${o.numFailedTests}}` : 'NO-JSON';
  const lines = (r.stdout ?? '').split('\n'); const sa = lines.map((l, i) => /^\s*Start at\s/.test(l) ? i : -1).filter(i => i >= 0);
  const last = sa.at(-1); let gap = [];
  if (last !== undefined) { for (let i = last - 1; i >= 0 && !/^\s*Tests\s/.test(lines[i]); i--) gap.unshift(lines[i]); }
  const got = fmt(readChildOutput(r.stdout ?? ''));
  console.log(`${s}: status ${r.status} signal ${r.signal} error ${r.error?.code ?? null} | Start at lines ${sa.length} | gap between last Tests and last Start at: ${JSON.stringify(gap)} | round3 ${got} | oracle(json) ${oracle} | ${got === oracle ? 'AGREE' : 'DISAGREE'}`);
}
JS
node "$F/drive.mjs" "$V" "$F" "$R" U1 U2 U3 X1 X2 X3
