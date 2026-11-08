# READY - KS-2121-KS-2121-O106-P1 (Spark (DeepSeek V4 Flash), briefed, test_only_input) - PASS 9/9 - HELD for QA

> CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2121_o106_p1_transfer_doors_one_refusal_fingerprint_across_six_doors/out.md.checker/patch.diff` (from `ls` at 02:23 2026-11-09; sha256[:16] 27cffb845beb8281, 908 B; byte-equal to the out.md fence). Checker A2 (verbatim): `PASS A2 the diff applies at the tip (strict)`; golden comparison [round.json, verbatim]: TREE-IDENTICAL.

**Held 02:23 2026-11-09 by Wednesday after a source read (hold_ready.py, test_only_input path; STRICT-APPLY leg passed first). Every clause below is copied from the run's artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2121_o106_p1_transfer_doors_one_refusal_fingerprint_across_six_doors/out.md.checker`; product bytes were RE-MEASURED here.** Tip `c0e6e744b7b21f3e1aa28105766764775b50ce6d`. Brief: not given (--brief)
- Touched set [patch.diff `+++` headers == input.json test_files, no product or plant file named]: ['Blockchain/Dev/services/transfer/src/__tests__/ks2081-transfer-doors-refuse-non-user-principals.test.ts']; `+` lines 15 (ASCII), `-` lines 0.
- Product bytes UNCHANGED [re-measured: tip index blobs before and after a strict `git apply --cached -p1` of patch.diff]: `Blockchain/Dev/services/transfer/src/index.ts` blob ac33dcb90b8e; plant file(s) also unchanged.
- Red cells [input.json]:
  - `reads one and the same refusal, headers included`
- Red-first evidence [checker.out, verbatim]: A4 green without plant, A5 red under the plant by assertion.
- Checker legs [checker.out, verbatim]:
  - `PASS A1 output is exactly one fenced ```diff block, nothing outside it`
  - `PASS A2 the diff applies at the tip (strict)`
  - `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=1 ok=1 bad=0 skipped_newfile=0)`
  - `PASS A3 touched set == the brief's declared set (Blockchain/Dev/services/transfer/src/__tests__/ks2081-transfer-doors-refuse-non-user-principals.test.ts)`
  - `PASS A3p the plant applies at the tip (golden_red.diff)`
  - `PASS A4 GREEN WITHOUT PLANT: 1 red cell(s) exist and pass on the unmodified product; declared files 108 cells, 0 red`
  - `PASS A6 WHOLE SUITE no worse: cells 460 -> 461, red 0 -> 0`
  - `PASS A5 RED WITH PLANT: 1 red cell(s) fail by assertion under the plant (Blockchain/Dev/services/transfer/src/index.ts), pass without it`
  - `PASS A7 RESTORE: 2 watched file(s) back at their tip sha256; tracked tree clean`
- RESULT [checker.out]: `RESULT: PASS (tier test_only_input)`

**PR NOTES for the raise seat:** TEST_ONLY_INPUT - test bytes only, zero product bytes. Apply `patch.diff` strictly (`git apply -p1`; proven by the hold's STRICT-APPLY leg). The red proof is the brief's plant (checker clone only), not a change in the PR. No `tsc` leg covers a vitest file; DOES NOT PROVE the plant is the regression that matters or that a cell catches a different one. Wednesday read the cells against the brief before this hold.

```diff
--- a/Blockchain/Dev/services/transfer/src/__tests__/ks2081-transfer-doors-refuse-non-user-principals.test.ts
+++ b/Blockchain/Dev/services/transfer/src/__tests__/ks2081-transfer-doors-refuse-non-user-principals.test.ts
@@ -471,3 +471,18 @@
     expect(await statusOf(own)).toBe('pending_approval');
   });
 });
+
+describe('KS-2121: the refusal is one answer across the six write doors', () => {
+  it('RED KS-2121 F1: a key reads one and the same refusal, headers included, at all six write doors', async () => {
+    const id = await open();
+    const token = key(null, TENANT_A);
+    const prints = new Set<string>();
+    for (const d of DOORS) {
+      const res = await call(token, 'POST', d.path(id), d.body());
+      expect([d.name, res.status]).toEqual([d.name, 403]);
+      prints.add(fingerprint(res));
+    }
+    expect(DOORS).toHaveLength(6);
+    expect(prints.size).toBe(1);
+  });
+});
```
