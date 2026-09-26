#!/bin/bash
# drafter_liveshape_g26_r2cmp.sh — a PREDICTION: the same live captures (g26_liveshape_fixtures/*/stdout.txt, written by
# drafter_liveshape_g26_live.sh) read by ROUND 2's readChildOutput (#1245's second commit, the parent of the round-3 head, READ from the clone
# as `<head>^`) beside round 3's, so a round-3 regression is visible as one. Usage: drafter_liveshape_g26_r2cmp.sh <clone> <scratchpad>
set -u
CL="$1"; SP="$2"; D="$(dirname "$(/bin/realpath "$0")")/liveshape_work"; F=systemTest/performance/tests/unit/utils/unitSuiteSlotIndependence.test.ts
H="$(git --git-dir "$CL" rev-parse refs/g26/pull/1245)"; R2="$(git --git-dir "$CL" rev-parse "$H^")"
echo "round 3 head $H | round 2 = its parent $R2 ($(git --git-dir "$CL" log -1 --format=%s "$R2" | cut -c1-80))"
git --git-dir "$CL" show "$R2:$F" > "$D/r2_file.ts"
python3 - "$D/r2_file.ts" "$D/reader_r2.ts" <<'PY'
import sys
t = open(sys.argv[1], encoding='utf-8').read()
a = t.index('const SUMMARY_LABELS = '); b = t.rindex('/**', a, t.index('function childSuiteCounts('))
open(sys.argv[2], 'w', encoding='utf-8').write('type SuiteCounts = { passed: number; failed: number };\n' + t[a:b])
PY
cat > "$D/cmp.mts" <<'JS'
import { readFileSync, readdirSync } from 'node:fs'; import { join } from 'node:path';
const [,, r2, r3, F] = process.argv;
const A = (await import(r2)).readChildOutput, B = (await import(r3)).readChildOutput;
const fmt = r => r === null ? 'NULL' : `{${r.passed},${r.failed}}`;
for (const s of readdirSync(F).filter(x => !x.includes('.')).sort()) {
  const o = JSON.parse(readFileSync(join(F, s, 'oracle.json'), 'utf8')); const out = readFileSync(join(F, s, 'stdout.txt'), 'utf8');
  console.log(`${s}: oracle {${o.numPassedTests},${o.numFailedTests}} | round2 ${fmt(A(out))} | round3 ${fmt(B(out))}`);
}
JS
node "$D/cmp.mts" "$D/reader_r2.ts" "$D/reader.ts" "$SP/g26_liveshape_fixtures"
