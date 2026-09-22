# KS-1164 R17-SAMEPATH - Wednesday's task for Ornith: `writeGateReport` in `systemTest/performance/gate/report.ts` still overwrites its own input when the `--summary` path IS the gate-report path (`<dir>/smoke-gate-report.json` for scenario `smoke`) - gate 19B's NOT-PINNED row REPORTPATH-SAMEPATH on #1200 (measured: preserved False) - refuse that call (ONE product hunk at `report.ts:327`: five `+` lines, no `-` line) and pin it with ONE NEW vitest file in the shape of #1200's own suite (code_patch, VITEST, the systemTest/performance tooling tier). Tip: `2bc5ccf63b8c40911afb568b03cace066238ffcf`. Written 2026-09-22 19:57:25 AEST by Wednesday's feed17 drafter.

Tip: `2bc5ccf63b8c40911afb568b03cace066238ffcf`
Runner: `vitest`

## Premises (measured by the feed17 drafter in a `git clone --shared` scratchpad clone at the tip; Wednesday re-derives before queueing)
- #1200 (KS-1164, `4d8a5cc4e`) is MERGED at this tip: `report.ts:325-:327` derives `reportPath` from the summary's DIRECTORY plus `scenario + '-gate-report.json'`, so a `--summary` that does not end in `-summary.json` is no longer overwritten. Gate 19B then measured the residual: `writeGateReport(results, '<dir>/smoke-gate-report.json', 'smoke')` derives `reportPath === summaryPath` and `fs.writeFileSync` at `:348` overwrites the input with the verdict (`preserved False`). Proposed by the gate: refuse (or suffix) when `path.resolve(reportPath) === path.resolve(summaryPath)`; cell: the input bytes survive. This brief REFUSES: a verdict written over the file it was asked to read is the exact failure #1200 closed, and a caller that hands the gate its own report is a wiring mistake to surface, not paper over.
- The site at the tip: `:324` `export function writeGateReport(results: GateResult[], summaryPath: string, scenario: string): void {`, `:325-:326` the KS-1164 comment, **`:327` `const reportPath = path.join(path.dirname(summaryPath), scenario + '-gate-report.json');` (leading context)**, **`:328` `const slot = resolveSlot();` (trailing context)**; `path` is imported at `:11` (`import * as path from 'node:path';`). The five `+` lines go between `:327` and `:328`. No other line changes; `:348` still writes `reportPath`.
- The test is a NEW vitest file beside the reference `systemTest/performance/tests/unit/gate/ks1164-write-gate-report-never-overwrites-its-input.test.ts` (#1200's suite, 46 lines, full content in `files[...]`): the same imports, the same `RESULTS` / `RAW` fixtures, the same `mkdtempSync` + `rmSync` lifecycle, a real `writeGateReport` call - no k6, no network, no stack. Red at the tip BY ASSERTION: the call does not throw and the input bytes are replaced by the verdict.
- Every `+` line (product and test) is ASCII-only, backslash-free and carries NO double-quote character (asserted by the writer script); strings are single-quoted; no test title carries an apostrophe. The context line `:327` carries a `+` inside its string concatenation - it is CONTEXT, copied byte for byte with its leading space.
- The tooling tier: `systemTest/performance` is a self-contained package (`package.json`, `vitest.unit.config.ts`, `tests/unit/`); the builder's `tool=systemTest/performance` makes it the repo subdir (the KS-1117 shape, PASS 7/7 on 09-15). `report.ts` was last changed by #1200 (merged) - no open PR and no held READY names it (the builder's own PR gate re-reads at build).

## What is wrong (one paragraph)
`systemTest/performance/gate/report.ts:324-:350` writes the gate verdict to `path.join(path.dirname(summaryPath), scenario + '-gate-report.json')`. When the caller's `--summary` is that very file - `<dir>/smoke-gate-report.json` with scenario `smoke`, the shape gate 19B drove - `reportPath` equals `summaryPath` and `:348` overwrites the input with the verdict computed from it: the raw file is gone and the report now describes a summary that no longer exists. The fix compares the two resolved paths and throws a named error before anything is written; `path` is already imported. Nothing else changes: the derivation at `:327`, `resolveSlot`, `readMachineShared`, the report shape and the console line are untouched.

## The exact change - ONE EDIT in the product file (one hunk; copy the header)
E1 (hunk 1, header `@@ -327,2 +327,7 @@`) - a PURE INSERTION of five `+` lines between the tip's `:327` (leading context, STAYS) and `:328` (trailing context, STAYS): two KS-1164 comment lines and a three-line `if` that throws when the resolved report path equals the resolved summary path. Old side 2 lines, new side 7.
```
@@ -327,2 +327,7 @@
     const reportPath = path.join(path.dirname(summaryPath), scenario + '-gate-report.json');
+    // KS-1164 (gate 19B REPORTPATH-SAMEPATH): a --summary that IS the gate-report path would still be
+    // overwritten by its own verdict - refuse, rather than read a verdict back as a k6 summary.
+    if (path.resolve(reportPath) === path.resolve(summaryPath)) {
+        throw new Error('[ci-gate] KS-1164: summary path ' + summaryPath + ' is the gate report path; refusing to overwrite the input');
+    }
     const slot = resolveSlot();
```
There are exactly 5 `+` lines in the product hunk and NO `-` line; every context line keeps its leading space (`:327` has four spaces at the tip, so its context line has five). Do NOT touch `:325-:326` or `:329-:350` beyond copying `:328` as context. Do NOT change `:348`.

## Where (parsed into the checklist - every **must change** line must appear as a `-` line in your diff; there is none here, the change is an insertion)
* `:327` - (correct) `    const reportPath = path.join(path.dirname(summaryPath), scenario + '-gate-report.json');` - stays (leading context; the five `+` lines go directly below it)
* `:328` - (correct) `    const slot = resolveSlot();` - stays (trailing context)

## THIS IS VITEST
`repo.test_runner` begins with `vitest`. `describe/it/expect/beforeEach/afterEach` are imported from `'vitest'`; NO `jest.*`; the config is `vitest.unit.config.ts` (the package's `npm run test:unit`).

## The test - one NEW vitest file that drives the real writeGateReport (the ks1164 shape)
File: `systemTest/performance/tests/unit/gate/ks1164-write-gate-report-refuses-its-own-report-path.test.ts`
NEW FILE: `--- /dev/null` then `+++ b/systemTest/performance/tests/unit/gate/ks1164-write-gate-report-refuses-its-own-report-path.test.ts`, ONE hunk header `@@ -0,0 +1,N @@` where N is the number of `+` lines (count them: 46), every line with a leading `+` (a blank line is a lone `+`). Copy every line byte for byte - single quotes only, no double-quote character, no backslash, ASCII only.
```
+// KS-1164 residual (gate 19B REPORTPATH-SAMEPATH): when --summary IS the gate-report path, writeGateReport
+// derived reportPath === summaryPath and overwrote its input with the verdict. It now refuses.
+
+import * as fs from 'node:fs';
+import * as os from 'node:os';
+import * as path from 'node:path';
+
+import { afterEach, beforeEach, describe, expect, it } from 'vitest';
+
+import { writeGateReport } from '../../../gate/report.ts';
+import type { GateResult } from '../../../gate/evaluate.ts';
+
+let runDir: string;
+
+const RESULTS: GateResult[] = [{ name: 'ci: error rate', passed: true, actual: '0.0000%', limit: '<= 5.0000%' }];
+
+const RAW = JSON.stringify({ metrics: { http_reqs: { type: 'counter', contains: 'default', values: { count: 4 } } } });
+
+beforeEach(() => {
+    runDir = fs.mkdtempSync(path.join(os.tmpdir(), 'perf-gate-ks1164-samepath-'));
+});
+afterEach(() => {
+    fs.rmSync(runDir, { recursive: true, force: true });
+});
+
+describe('writeGateReport refuses its own report path (KS-1164 residual)', () => {
+    it('RED KS-1164: a summary path equal to the derived gate-report path is refused and its bytes survive', () => {
+        const input = path.join(runDir, 'smoke-gate-report.json');
+        fs.writeFileSync(input, RAW);
+        expect(() => writeGateReport(RESULTS, input, 'smoke')).toThrow(/KS-1164/);
+        expect(fs.readFileSync(input, 'utf8')).toBe(RAW);
+    });
+
+    it('control: the conforming name still writes smoke-gate-report.json beside the summary and leaves it intact', () => {
+        const input = path.join(runDir, 'smoke-summary.json');
+        fs.writeFileSync(input, RAW);
+        writeGateReport(RESULTS, input, 'smoke');
+        expect(fs.readFileSync(input, 'utf8')).toBe(RAW);
+        const report = JSON.parse(fs.readFileSync(path.join(runDir, 'smoke-gate-report.json'), 'utf8')) as Record<
+            string,
+            unknown
+        >;
+        expect(report['scenario']).toBe('smoke');
+        expect(report['passed']).toBe(true);
+    });
+});
```
Cells: `RED KS-1164: a summary path equal to the derived gate-report path is refused and its bytes survive` (RED at the tip: no throw, and the file now holds the verdict, not `RAW`; GREEN after: throws `/KS-1164/`, bytes intact) and `control: the conforming name still writes smoke-gate-report.json beside the summary and leaves it intact` (passes on both trees).

## Red cells
- RED KS-1164: a summary path equal to the derived gate-report path is refused and its bytes survive

## Output
Exactly ONE ```diff block with TWO files: `--- a/systemTest/performance/gate/report.ts` / `+++ b/systemTest/performance/gate/report.ts` (1 hunk, copied from `## The exact change`), then `--- /dev/null` / `+++ b/systemTest/performance/tests/unit/gate/ks1164-write-gate-report-refuses-its-own-report-path.test.ts` (one hunk, `@@ -0,0 +1,46 @@`, every line a `+`). No prose before or after the block.

## Notes for the raise (not for the model)
- The gate offered "refuse (or suffix)"; this brief refuses. If the reviewer prefers a suffix, the same cell shape pins it (assert the input bytes survive and a suffixed report exists) - a different `+` block, same anchor. **Refs KS-1164, does not close it** (the ticket's item is closed by #1200; this is the gate's residual).
- Tooling tier (`systemTest/performance`): no service image, no hook legs (#1200's gate: "No hook legs (systemTest-only)"). HELD and GATED like every Ornith output.
