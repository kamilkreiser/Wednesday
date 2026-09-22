# READY — KS-1164-1164REPORTPATH-R16B (Ornith, briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1164-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 12:18 2026-09-22; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1164-ornith35b-night/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1164-ornith35b-night/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1164-ornith35b-night/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_feed10-drafter-precheck/REPORTPATH/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 12:18 2026-09-22 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1164-ornith35b-night/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `8c2f7b3fd4fde915b2a24542bc32259b24e092a0`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { systemTest/performance/gate/report.ts , systemTest/performance/tests/unit/gate/ks1164-write-gate-report-never-overwrites-its-input.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `systemTest/performance/gate/report.ts` (product) and `systemTest/performance/tests/unit/gate/ks1164-write-gate-report-never-overwrites-its-input.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
3	1	systemTest/performance/gate/report.ts
43	0	systemTest/performance/tests/unit/gate/ks1164-write-gate-report-never-overwrites-its-input.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (3 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 3 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 1.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied systemTest/performance/gate/report.ts byte-exact incl. leading whitespace (apply mode strict): OK 3 line(s) byte-exact incl. leading whitespace (of 3; 3 line(s) added by the apply)` [a3i_indent.out: `OK 3 line(s) byte-exact incl. leading whitespace (of 3; 3 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `systemTest/performance/gate/report.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `systemTest/performance/tests/unit/gate/ks1164-write-gate-report-never-overwrites-its-input.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: tests/unit/gate/ks1164-write-gate-report-never-overwrites-its-input.test.ts fails at the untouched tip (1 failed / 2 run; controls green; assertion reds)` [red_first.json: failed=1 of total=2; red cell(s): ['writeGateReport input preservation (KS-1164) RED KS-1164: a summary path that does not end in -summary.json is NOT overwritten and the report lands beside it']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: tests/unit/gate/ks1164-write-gate-report-never-overwrites-its-input.test.ts passes with the product hunk (2 passed / 2 run)` [green_after.json: failed=0 of total=2, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1083 failed=1 | after: total=1085 failed=1` · `NEW reds: []` [baseline_suite.json total=1083 failed=1; after_suite.json total=1085 failed=1]
- A6 [verbatim]: `PASS A6 whole . suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for .: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +46/-1 test=tests/unit/gate/ks1164-write-gate-report-never-overwrites-its-input.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `systemTest/performance/gate/report.ts` (+3/-1 per numstat.out) and the test file `systemTest/performance/tests/unit/gate/ks1164-write-gate-report-never-overwrites-its-input.test.ts` (+43/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `8c2f7b3fd4fde915b2a24542bc32259b24e092a0` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1164-ornith35b-night/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1164-ornith35b-night/checker.out`.

```diff
--- a/systemTest/performance/gate/report.ts
+++ b/systemTest/performance/gate/report.ts
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
--- /dev/null
+++ b/systemTest/performance/tests/unit/gate/ks1164-write-gate-report-never-overwrites-its-input.test.ts
@@ -0,0 +1,43 @@
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
