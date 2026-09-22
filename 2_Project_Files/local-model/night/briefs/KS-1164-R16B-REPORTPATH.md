# KS-1164 R16B-REPORTPATH - Wednesday's task for Ornith, TOOLING tier (`systemTest/performance`, vitest): `writeGateReport` derives the report path from the DIRECTORY + SCENARIO, never from the summary's basename, so a `--summary` path that does not end in `-summary.json` is never overwritten; plus a NEW unit test (code_patch, ONE product hunk in `gate/report.ts`; re-brief of the STALE READY_KS-1164 at develop 8c2f7b3fd, written 11:34:22 AEST on 2026-09-22 by Wednesday's feed10 drafter from the file at the tip - `report.ts` :1-:12 and :318-:349 read; the reference test `tests/unit/gate/gateMachineShared.test.ts` present at the tip)
Tip: `8c2f7b3fd4fde915b2a24542bc32259b24e092a0`
Runner: `vitest`

## Premises (measured by the feed10 drafter in a `--shared --no-checkout` scratchpad clone detached at the tip; Wednesday re-derives before queueing)
- Source READY: `night/READY_KS-1164_ornith35b-q4_TOOLING-PASS-7of7_2026-09-15.diff.md` (Ornith PASS 7/7 at develop 2026-09-15 in tool mode; the FEED 7 census typed it `comment` - it is a code_patch: one product hunk + one NEW test). The old brief `night/briefs/KS-1164.md` is the fix shape's source (the ticket's own: `path.join(path.dirname(summaryPath), <scenario>-gate-report.json)`).
- The product at the tip is UNCHANGED since the READY (offset 0): `:324` `export function writeGateReport(results: GateResult[], summaryPath: string, scenario: string): void {`, `:325` `    const reportPath = summaryPath.replace(/-summary\.json$/, '-gate-report.json');`, `:326` `    const slot = resolveSlot();`, `:327` `    const report = {`, `:328` `        scenario,` - byte-exact at 8c2f7b3fd (the file is 349 lines; `import * as path from 'node:path';` at `:11`). The line `:329` carries an em-dash and is OUTSIDE this hunk; every context line here is ASCII.
- The READY's `+` lines carried a template literal (`${scenario}-gate-report.json`), a backslash (`-summary\.json`) and an em-dash; its test carried double-quoted JSON, `≤` and the red glyph. This brief writes the path by concatenation, the raw summary as `JSON.stringify(...)`, the limit as `<= 5.0000%`, and declares the red cell under `## Red cells`, so every `+` line is ASCII, backslash-free, double-quote-free and `$`-free. Same behaviour, same two cells.
- No file of this brief is on a live seat's list (`systemTest/performance` is neither Seat B's nor Seat C's area; no round-18 PR and no held R15/R16 READY touches it; the STALE `READY_KS-1164-B` is Part B, a different task). Ticket KS-1164: Backlog, not archived, no PR attached (board read at drafting time).
- NOT in this task: the `runner/k6_docker.ts` sibling, `gate/cli.ts`, the `:329-:340` comments.

## What is wrong (one paragraph)
`writeGateReport` (`systemTest/performance/gate/report.ts:324-348`) derives where it writes from the SUMMARY path: `:325` `const reportPath = summaryPath.replace(/-summary\.json$/, '-gate-report.json');`. When the `--summary` path does not end in `-summary.json` (k6's own default basename is `summary.json`; the documented `--summary` override is a free path) the replace is a no-op, `reportPath === summaryPath`, and `:346` `fs.writeFileSync(reportPath, JSON.stringify(report, null, 2));` OVERWRITES the raw k6 summary - the run's only raw record - while `:347` logs success. Fix shape (the ticket's): derive the report path from the DIRECTORY and the SCENARIO - `path.join(path.dirname(summaryPath), scenario + '-gate-report.json')` - so it can never equal the input; `path` is already imported at `:11`. For the conforming names this is byte-identical output (`<dir>/smoke-summary.json`, scenario `smoke` -> `<dir>/smoke-gate-report.json`, which `tests/unit/gate/ciGate.test.ts` and `gateMachineShared.test.ts` read). Plus one NEW vitest unit test: a `summary.json` input is left intact and the report lands beside it (RED at the tip: the input is overwritten), and the conforming name still writes `smoke-gate-report.json` with the scenario and verdict (CONTROL).

## The exact change - ONE EDIT in `systemTest/performance/gate/report.ts` (one hunk, header `@@ -322,7 +322,9 @@`)
E1 - `:325` (the one `-` line) is REPLACED by three lines (two comment lines + the new `const reportPath`); leading context `:322-:324`, trailing context `:326-:328`. Inside the hunk the lines run in exactly ONE sequence: context, then the `-` line, then the three `+` lines, then context. Four-space indent, as the file uses.
```
@@ -322,7 +322,9 @@
  * @internal
  */
 export function writeGateReport(results: GateResult[], summaryPath: string, scenario: string): void {
-    const reportPath = summaryPath.replace(/-summary\.json$/, '-gate-report.json');
+    // KS-1164: derive from the directory + scenario, never from the summary basename - a --summary path
+    // that does not end in -summary.json made reportPath === summaryPath and overwrote the raw k6 summary.
+    const reportPath = path.join(path.dirname(summaryPath), scenario + '-gate-report.json');
     const slot = resolveSlot();
     const report = {
         scenario,
```
Copy every `+` line byte for byte; the `-` line is the tip's `:325` exactly (it carries a backslash and a regex - copy it as it is; it is a `-` line, not a `+` line); every context line keeps its leading space (the two comment-tail context lines are ` * @internal` and ` */` each with the leading space). No blank line anywhere in this hunk. Do not touch any other line of the product file.

## THIS IS VITEST, NOT JEST
`repo.test_runner` begins with `vitest` (the package's `vitest.unit.config.ts`): `afterEach/beforeEach/describe/expect/it` imported from `'vitest'`. No `jest.*`. Import ONLY what the cells use (every import below is used).

## The test - one NEW vitest unit file in the `gateMachineShared.test.ts` shape (in-process, a mkdtemp run dir, no k6, no stack)
File: `systemTest/performance/tests/unit/gate/ks1164-write-gate-report-never-overwrites-its-input.test.ts`
NEW FILE: `--- /dev/null` then `+++ b/systemTest/performance/tests/unit/gate/ks1164-write-gate-report-never-overwrites-its-input.test.ts`, ONE hunk header `@@ -0,0 +1,N @@` where N is the number of `+` lines (count them: 43), every line with a leading `+`. Copy every line byte for byte - single quotes only, no double-quote character, no backslash, no `$`, ASCII only; four-space indent as the sibling tests use.
```
+// KS-1164 regression: when --summary does not end in -summary.json, writeGateReport used to overwrite it.
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
+    runDir = fs.mkdtempSync(path.join(os.tmpdir(), 'perf-gate-ks1164-'));
+});
+afterEach(() => {
+    fs.rmSync(runDir, { recursive: true, force: true });
+});
+
+describe('writeGateReport input preservation (KS-1164)', () => {
+    it('RED KS-1164: a summary path that does not end in -summary.json is NOT overwritten and the report lands beside it', () => {
+        const input = path.join(runDir, 'summary.json');
+        fs.writeFileSync(input, RAW);
+        writeGateReport(RESULTS, input, 'smoke');
+        expect(fs.readFileSync(input, 'utf8')).toBe(RAW);
+        expect(fs.existsSync(path.join(runDir, 'smoke-gate-report.json'))).toBe(true);
+    });
+
+    it('control: the conforming name still writes smoke-gate-report.json beside the summary and leaves it intact', () => {
+        const input = path.join(runDir, 'smoke-summary.json');
+        fs.writeFileSync(input, RAW);
+        writeGateReport(RESULTS, input, 'smoke');
+        expect(fs.readFileSync(input, 'utf8')).toBe(RAW);
+        const report = JSON.parse(fs.readFileSync(path.join(runDir, 'smoke-gate-report.json'), 'utf8')) as Record<string, unknown>;
+        expect(report['scenario']).toBe('smoke');
+        expect(report['passed']).toBe(true);
+    });
+});
```
Cells (every cell RED or CONTROL, nothing optional):
- RED `it('RED KS-1164: a summary path that does not end in -summary.json is NOT overwritten and the report lands beside it')` - at the untouched tip the replace is a no-op, so the report is written OVER `summary.json`: the read-back differs from `RAW` (assertion red) and `smoke-gate-report.json` does not exist; after E1 the input is intact and the report is beside it.
- CONTROL `it('control: the conforming name still writes smoke-gate-report.json beside the summary and leaves it intact')` - `smoke-summary.json` maps to `smoke-gate-report.json` on both trees (the tip's replace and the new join agree), with `scenario` `smoke` and `passed` true.

## Red cells
- RED KS-1164: a summary path that does not end in -summary.json is NOT overwritten and the report lands beside it

## Where (parsed into the checklist - every **must change** line must appear as a `-` line in your diff)
* `:325` - **must change**: `    const reportPath = summaryPath.replace(/-summary\.json$/, '-gate-report.json');`
* `:322` - (correct) ` * @internal` - stays (E1's first leading context line)
* `:323` - (correct) ` */` - stays (leading context)
* `:324` - (correct) `export function writeGateReport(results: GateResult[], summaryPath: string, scenario: string): void {` - stays (leading context)
* `:326` - (correct) `    const slot = resolveSlot();` - stays (trailing context)
* `:327` - (correct) `    const report = {` - stays (trailing context)
* `:328` - (correct) `        scenario,` - stays (trailing context)
* `:11` - (correct) `import * as path from 'node:path';` - stays (the import the new line uses)
* `:346` - (correct) `    fs.writeFileSync(reportPath, JSON.stringify(report, null, 2));` - stays (the write now lands beside the input)

## Output
Exactly ONE ```diff block with TWO files: `--- a/systemTest/performance/gate/report.ts` / `+++ b/systemTest/performance/gate/report.ts` (ONE hunk, header `@@ -322,7 +322,9 @@`, one `-` line, three `+` lines), then `--- /dev/null` / `+++ b/systemTest/performance/tests/unit/gate/ks1164-write-gate-report-never-overwrites-its-input.test.ts` (one `@@ -0,0 +1,43 @@` hunk, all `+`); paths repo-relative; every context line keeps its leading space; no `$`, `\u`, backslash or double-quote character in any `+` line; the cell titles EXACTLY as listed.
