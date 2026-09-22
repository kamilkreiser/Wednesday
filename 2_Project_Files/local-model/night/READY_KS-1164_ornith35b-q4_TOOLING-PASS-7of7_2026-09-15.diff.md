# READY — KS-1164 (systemTest/performance `gate/report.ts` writeGateReport: report path derived from directory + scenario, never from the summary's basename — the overwrite of the raw k6 summary closed) — Ornith ornith:35b (Q4_K_M) PASS 7/7 (run night4 20:01; FIRST TOOLING-TIER ticket via the new `tool=` mode; A2 --recount on the test section only)
# Source read by me (Wednesday): the product hunk is the brief's E1 exactly (:325 → path.join(dirname, `${scenario}-gate-report.json`) with the two-line comment; nothing else in the file). The test copies gateMachineShared's driver; 🔴 cell red at the tip (the input overwritten), green after; control (conforming name) green both trees; whole performance unit suite green; tsc green. **Sunday seat: the ticket's DoD also names the `runner/k6_docker.ts:241` sibling (`summaryMount.replace(/-summary\.json$/, '-k6.log')`) — either the same shape or recorded as accepted with the reason; not in this diff (a separate task: the driver is k6Docker.test.ts's spawnSync mock).** The ticket's follow-up (reportFailedGateBreakdown `String(n)` vs `toLocaleString()`) is also NOT in this diff.

```diff
--- a/systemTest/performance/gate/report.ts
+++ b/systemTest/performance/gate/report.ts
@@ -322,7 +322,9 @@ function readMachineShared(summaryPath: string): Record<string, unknown> {
  * @internal
  */
 export function writeGateReport(results: GateResult[], summaryPath: string, scenario: string): void {
-    const reportPath = summaryPath.replace(/-summary\.json$/, '-gate-report.json');
+    // KS-1164: derive from the directory + scenario, never from the summary's basename — a `--summary` path
+    // that does not end in `-summary.json` made reportPath === summaryPath and overwrote the raw k6 summary.
+    const reportPath = path.join(path.dirname(summaryPath), `${scenario}-gate-report.json`);
     const slot = resolveSlot();
     const report = {
         scenario,
--- /dev/null
+++ b/systemTest/performance/tests/unit/gate/ks1164-gate-report-ts-writegatereport-overwrites-the.test.ts
@@ -0,0 +1,62 @@
+/**
+ * KS-1164 regression: when --summary doesn't end in -summary.json, writeGateReport used to overwrite it.
+ */
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
+const RESULTS: GateResult[] = [{ name: 'ci: error rate', passed: true, actual: '0.0000%', limit: '≤ 5.0000%' }];
+
+beforeEach(() => {
+    runDir = fs.mkdtempSync(path.join(os.tmpdir(), 'perf-gate-shared-'));
+});
+afterEach(() => {
+    fs.rmSync(runDir, { recursive: true, force: true });
+});
+
+describe('writeGateReport — input preservation (KS-1164)', () => {
+    it('🔴 KS-1164 — a --summary path that does not end in -summary.json is NOT overwritten; the report lands beside it', () => {
+        const RAW = '{"metrics":{"http_reqs":{"type":"counter","contains":"default","values":{"count":4}}}}';
+        const input = path.join(runDir, 'summary.json');
+        fs.writeFileSync(input, RAW);
+        writeGateReport(RESULTS, input, 'smoke');
+        expect(fs.readFileSync(input, 'utf8')).toBe(RAW);
+        expect(fs.existsSync(path.join(runDir, 'smoke-gate-report.json'))).toBe(true);
+    });
+
+    it('KS-1164 control — the conforming name still writes <scenario>-gate-report.json beside the summary and leaves it intact', () => {
+        const RAW = '{"metrics":{"http_reqs":{"type":"counter","contains":"default","values":{"count":4}}}}';
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

# SUPERSEDED-BY (feed10 drafter, 2026-09-22 11:35:05 AEST): re-briefed at develop 8c2f7b3fd as `night/briefs/KS-1164-R16B-REPORTPATH.md` (golden RESULT: PASS (7/7) through tasks/code_patch/checker.sh in tool mode; the template literal written as concatenation, the test rewritten ASCII with JSON.stringify for the raw summary). This READY is the 2026-09-15 pin; do not raise it.
