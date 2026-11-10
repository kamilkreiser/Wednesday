# READY - KS-2085-KS-2085-O132-P1 (Spark (DeepSeek V4 Flash), briefed, test_only_input) - PASS 9/9 - HELD for QA

> CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_2085_o132_p1_transfer_access_rule_unit_pins_the_executor_on_the_reject_row/out.md.checker/patch.diff` (from `ls` at 15:33 2026-11-10; sha256[:16] 1686aaf8bd14cf93, 1754 B; byte-equal to the out.md fence). Checker A2 (verbatim): `PASS A2 the diff applies at the tip (strict)`; golden comparison [round.json, verbatim]: TREE-IDENTICAL.

**Held 15:33 2026-11-10 by Wednesday after a source read (hold_ready.py, test_only_input path; STRICT-APPLY leg passed first). Every clause below is copied from the run's artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_2085_o132_p1_transfer_access_rule_unit_pins_the_executor_on_the_reject_row/out.md.checker`; product bytes were RE-MEASURED here.** Tip `0e6479d7b6c06b6f8a77aae1cbad167afbdaa089`. Brief: not given (--brief)
- Touched set [patch.diff `+++` headers == input.json test_files, no product or plant file named]: ['Blockchain/Dev/services/transfer/src/__tests__/ks2038-transfer-access-rule-unit.test.ts']; `+` lines 16 (ASCII), `-` lines 0.
- Product bytes UNCHANGED [re-measured: tip index blobs before and after a strict `git apply --cached -p1` of patch.diff]: `Blockchain/Dev/services/transfer/src/services/transferAccess.ts` blob d7e1184bb7a3; plant file(s) also unchanged.
- Red cells [input.json]:
  - `the executor named on a simple transfer may reject it`
  - `the executor named on a sale transfer may reject it`
  - `the executor named on a corporate transfer may reject it`
- Red-first evidence [checker.out, verbatim]: A4 green without plant, A5 red under the plant by assertion.
- Checker legs [checker.out, verbatim]:
  - `PASS A1 output is exactly one fenced ```diff block, nothing outside it`
  - `PASS A2 the diff applies at the tip (strict)`
  - `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=1 ok=1 bad=0 skipped_newfile=0)`
  - `PASS A3 touched set == the brief's declared set (Blockchain/Dev/services/transfer/src/__tests__/ks2038-transfer-access-rule-unit.test.ts)`
  - `PASS A3p the plant applies at the tip (golden_red.diff)`
  - `PASS A4 GREEN WITHOUT PLANT: 3 red cell(s) exist and pass on the unmodified product; declared files 26 cells, 0 red`
  - `PASS A6 WHOLE SUITE no worse: cells 466 -> 471, red 0 -> 0`
  - `PASS A5 RED WITH PLANT: 3 red cell(s) fail by assertion under the plant (Blockchain/Dev/services/transfer/src/services/transferAccess.ts), pass without it`
  - `PASS A7 RESTORE: 2 watched file(s) back at their tip sha256; tracked tree clean`
- RESULT [checker.out]: `RESULT: PASS (tier test_only_input)`

**PR NOTES for the raise seat:** TEST_ONLY_INPUT - test bytes only, zero product bytes. Apply `patch.diff` strictly (`git apply -p1`; proven by the hold's STRICT-APPLY leg). The red proof is the brief's plant (checker clone only), not a change in the PR. No `tsc` leg covers a vitest file; DOES NOT PROVE the plant is the regression that matters or that a cell catches a different one. Wednesday read the cells against the brief before this hold.

```diff
--- a/Blockchain/Dev/services/transfer/src/__tests__/ks2038-transfer-access-rule-unit.test.ts
+++ b/Blockchain/Dev/services/transfer/src/__tests__/ks2038-transfer-access-rule-unit.test.ts
@@ -72,3 +72,19 @@ describe('KS-2038: signedInCaller', () => {
     expect(signedInCaller({ userId: OWNER, ...claims })).toEqual({ userId: OWNER, role: 'unknown' });
   });
 });
+
+// KS-2085 item 1 (gate 229 F6): the executor a transfer names may REFUSE it, whatever its kind. WHO_MAY.reject lists 'executorId' on all
+// four kinds and no cell pinned that, so taking it off the simple, sale or corporate row survived every cell.
+describe('KS-2085 F6: decideTransferAccess, the named executor on the reject door', () => {
+  const EXECUTOR = '00000000-0000-4000-8000-00000000e001';
+  it.each(['simple', 'sale', 'corporate'])('the executor named on a %s transfer may reject it', (transferType) => {
+    expect(decideTransferAccess(EXECUTOR, 'reject', { transferType, currentOwnerId: OWNER, executorId: EXECUTOR })).toEqual({ allow: true });
+  });
+  it('control: the executor named on an inheritance transfer may reject it', () => {
+    expect(decideTransferAccess(EXECUTOR, 'reject', { transferType: 'inheritance', currentOwnerId: OWNER, executorId: EXECUTOR })).toEqual({ allow: true });
+  });
+  it('control: a named executor is a party, so it reads 403 and never 404, where the rule gives it no verb', () => {
+    expect(decideTransferAccess(EXECUTOR, 'approve', { transferType: 'sale', currentOwnerId: OWNER, executorId: EXECUTOR })).toEqual({ allow: false, status: 403 });
+    expect(decideTransferAccess(EXECUTOR, 'execute', { transferType: 'simple', currentOwnerId: OWNER, executorId: EXECUTOR })).toEqual({ allow: false, status: 403 });
+  });
+});
```
