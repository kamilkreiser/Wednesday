#!/bin/bash
# drafter_liveshape_g26.sh — a PREDICTION for the gate, never its evidence. Extracts #1245 ROUND 3's readChildOutput + readSuiteCounts
# (and their constants) BYTE-FOR-BYTE from the head blob (read from the drafter's scratch clone; the head sha is READ from refs/g26/pull/1245
# and asserted equal to the kit's pin), strips nothing by hand (node 24's own type stripping runs the .ts), and feeds it EVERY real stdout
# capture gate24T2c's tester recorded (read-only, from its report's evidence/liveshape and scratch dirs), graded against that tester's own
# independent oracle column (13_L2_table.md: the Tests line before vitest's `Start at`, NULL when none). Then the drafter's SYNTHETIC
# variants (marked SYN — NOT real vitest shapes until the gate captures them live). Writes only under its own dir.
# Usage: drafter_liveshape_g26.sh <scratch clone> <expected #1245 head>
set -u
CL="$1"; WANT="$2"; D="$(dirname "$(/bin/realpath "$0")")/liveshape_work"; mkdir -p "$D"
H="$(git --git-dir "$CL" rev-parse refs/g26/pull/1245)"; [ "$H" = "$WANT" ] || { echo "REFUSING: clone's #1245 $H != pin $WANT"; exit 2; }
F=systemTest/performance/tests/unit/utils/unitSuiteSlotIndependence.test.ts
git --git-dir "$CL" show "$H:$F" > "$D/head_file.ts"
python3 - "$D/head_file.ts" "$D/reader.ts" <<'PY'
import sys, re
t = open(sys.argv[1], encoding='utf-8').read()
a = t.index('const SUMMARY_LABELS = '); b = t.index('function childSuiteCounts(')
b = t.rindex('/**', a, b)          # stop at childSuiteCounts' own docblock
body = t[a:b]
body = 'type SuiteCounts = { passed: number; failed: number };\n' + body
open(sys.argv[2], 'w', encoding='utf-8').write(body)
print('extracted %d bytes (lines %d..%d of the head file)' % (len(body), t[:a].count('\n') + 1, t[:b].count('\n')))
PY
echo "head $H | reader sha256 $(shasum -a 256 "$D/reader.ts" | cut -c1-16) | node $(node --version)"
EV='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-26-batch1245r2-t2c'
cat > "$D/run.mts" <<'JS'
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join, basename } from 'node:path';
const { readChildOutput } = await import(process.argv[2]);
const ev = process.argv[3];
const table = readFileSync(join(ev, 'evidence/liveshape/13_L2_table.md'), 'utf8').split('\n').filter(l => l.startsWith('| ') && !l.startsWith('| shape') );
const oracle = {}; for (const l of table) { const c = l.split('|').map(x => x.trim()); oracle[c[1]] = c[c.length - 4]; }
// ^ the oracle column is read from the ROW'S END: a Tests line carries its own pipes
const files = {};
const walk = d => { for (const n of readdirSync(d)) { const p = join(d, n); const s = statSync(p); if (s.isDirectory()) walk(p); else if (n.endsWith('.stdout')) { const k = basename(n, '.stdout'); if (k in oracle && !(k in files)) files[k] = p; } } };
walk(ev);
const fmt = r => r === null ? 'NULL' : `{${r.passed},${r.failed}}`;
let wrong = 0, n = 0;
for (const k of Object.keys(oracle)) {
  if (!files[k]) { console.log(`${k.padEnd(10)} NO CAPTURE FOUND`); continue; }
  const got = fmt(readChildOutput(readFileSync(files[k], 'utf8'))); n++;
  const ok = got === oracle[k]; if (!ok) wrong++;
  console.log(`${k.padEnd(10)} round3=${got.padEnd(6)} oracle=${oracle[k].padEnd(6)} ${ok ? 'PASS' : 'WRONG'}`);
}
console.log(`REAL CAPTURES: ${n} read, ${wrong} WRONG`);
// SYNTHETIC (drafter-composed; the gate must capture each LIVE before it counts under the rule)
const blk = (p, f, t) => ` Test Files  ${f}\n      Tests  ${t}\n   Start at  04:30:01\n   Duration  130ms (transform 8ms)\n`;
const real = readFileSync(files['S14'], 'utf8');
const syn = {
  'SYN-H1s killed after a lookalike INCLUDING Start at (stdout only; childSuiteCounts refuses on status 143)': '\n RUN  v4.1.11 /x\n\nstdout | a.test.ts > lookalike\n' + blk(0, '1 passed (1)', '7 passed (7)'),
  'SYN-H4s process.on(exit) writes a COMPLETE lookalike AFTER vitest\'s real block (status 1, NOT refused)': real + blk(0, '1 passed (1)', '7 passed (7)'),
  'SYN-H4t exit-hook writes only `   Start at  hh:mm:ss` after the real block': real + '   Start at  04:30:09\n',
  'SYN-ERRLINE an `Errors  1 error` line between Tests and Start at': '\n Test Files  1 passed (1)\n      Tests  2 passed (2)\n     Errors  1 error\n   Start at  04:30:01\n',
  'SYN-TYPEERR a `Type Errors  1 error` line between Tests and Start at': '\n Test Files  1 passed (1)\n      Tests  2 passed (2)\n Type Errors  1 error\n   Start at  04:30:01\n',
  'SYN-CRLF the real S14 block with CRLF line ends': real.replace(/\n/g, '\r\n'),
};
for (const [k, v] of Object.entries(syn)) console.log(`${fmt(readChildOutput(v)).padEnd(6)} ${k}`);
JS
node "$D/run.mts" "$D/reader.ts" "$EV" 2>&1
echo "rc=$?"
