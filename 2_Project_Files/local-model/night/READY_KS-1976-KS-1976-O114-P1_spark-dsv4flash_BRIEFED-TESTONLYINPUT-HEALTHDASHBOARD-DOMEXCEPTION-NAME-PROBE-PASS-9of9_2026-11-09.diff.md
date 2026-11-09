# READY - KS-1976-KS-1976-O114-P1 (Spark (DeepSeek V4 Flash), briefed, test_only_input) - PASS 9/9 - HELD for QA

> CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_1976_o114_p1_health_dashboard_domexception_name_probe/out.md.checker/patch.diff` (from `ls` at 16:33 2026-11-09; sha256[:16] 1fb719e4c919d754, 1259 B; byte-equal to the out.md fence). Checker A2 (verbatim): `PASS A2 the diff applies at the tip (strict)`; golden comparison [round.json, verbatim]: TREE-IDENTICAL.

**Held 16:33 2026-11-09 by Wednesday after a source read (hold_ready.py, test_only_input path; STRICT-APPLY leg passed first). Every clause below is copied from the run's artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_1976_o114_p1_health_dashboard_domexception_name_probe/out.md.checker`; product bytes were RE-MEASURED here.** Tip `204e62acdc351e664f9a1ca49a058275e9b3e907`. Brief: not given (--brief)
- Touched set [patch.diff `+++` headers == input.json test_files, no product or plant file named]: ['Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-health-dashboard-check-service-catch-unreadable-throw.test.ts']; `+` lines 13 (ASCII), `-` lines 0.
- Product bytes UNCHANGED [re-measured: tip index blobs before and after a strict `git apply --cached -p1` of patch.diff]: `Blockchain/Dev/services/api-gateway/src/routes/health-dashboard.ts` blob 1b6df6244f09; plant file(s) also unchanged.
- Red cells [input.json]:
  - `ks1976 N1 a DOMException named AbortError reports the service down as a timeout with no latency`
  - `ks1976 N2 a DOMException whose name getter throws reports the service down with a constant reason`
- Red-first evidence [checker.out, verbatim]: A4 green without plant, A5 red under the plant by assertion.
- Checker legs [checker.out, verbatim]:
  - `PASS A1 output is exactly one fenced ```diff block, nothing outside it`
  - `PASS A2 the diff applies at the tip (strict)`
  - `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=1 ok=1 bad=0 skipped_newfile=0)`
  - `PASS A3 touched set == the brief's declared set (Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-health-dashboard-check-service-catch-unreadable-throw.test.ts)`
  - `PASS A3p the plant applies at the tip (2 pinned line(s))`
  - `PASS A4 GREEN WITHOUT PLANT: 2 red cell(s) exist and pass on the unmodified product; declared files 6 cells, 0 red`
  - `PASS A6 WHOLE SUITE no worse: cells 1880 -> 1882, red 0 -> 0`
  - `PASS A5 RED WITH PLANT: 2 red cell(s) fail by assertion under the plant (Blockchain/Dev/services/api-gateway/src/routes/health-dashboard.ts, Blockchain/Dev/services/api-gateway/src/routes/health-dashboard.ts), pass without it`
  - `PASS A7 RESTORE: 2 watched file(s) back at their tip sha256; tracked tree clean`
- RESULT [checker.out]: `RESULT: PASS (tier test_only_input)`

**PR NOTES for the raise seat:** TEST_ONLY_INPUT - test bytes only, zero product bytes. Apply `patch.diff` strictly (`git apply -p1`; proven by the hold's STRICT-APPLY leg). The red proof is the brief's plant (checker clone only), not a change in the PR. No `tsc` leg covers a vitest file; DOES NOT PROVE the plant is the regression that matters or that a cell catches a different one. Wednesday read the cells against the brief before this hold.

```diff
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-health-dashboard-check-service-catch-unreadable-throw.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-health-dashboard-check-service-catch-unreadable-throw.test.ts
@@ -85,4 +85,17 @@
     const out = await dashboard(getterThrows());
     expect(out.body?.services?.svc).toEqual(down('unreadable thrown value'));
   });
+
+  // KS-1976 (gate 177 mutant H5): the DOMException name probe in checkService is pinned by no cell.
+  it('ks1976 N1 a DOMException named AbortError reports the service down as a timeout with no latency', async () => {
+    const out = await dashboard(new DOMException('aborted', 'AbortError'));
+    expect(out.body?.services?.svc).toEqual({ status: 'down', latencyMs: null, url: 'https://svc.example.test', error: 'timeout' });
+  });
+
+  it('ks1976 N2 a DOMException whose name getter throws reports the service down with a constant reason', async () => {
+    const thrown = new DOMException('aborted', 'AbortError');
+    Object.defineProperty(thrown, 'name', { get: () => { throw new Error('name boom'); } });
+    const out = await dashboard(thrown);
+    expect(out.body?.services?.svc).toEqual(down('unreadable thrown value'));
+  });
 });
```
