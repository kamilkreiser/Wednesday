# READY - KS-2169-KS-2169-O163-P1 (Spark (DeepSeek V4 Flash), briefed, test_only_input) - PASS 9/9 - HELD for QA

> CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-12_ks_2169_o163_p1_transfer_cancel_trim_before_max_and_refused_types_pins/out.md.checker/patch.diff` (from `ls` at 10:24 2026-11-12; sha256[:16] d5ade5616ec0902b, 1542 B; byte-equal to the out.md fence). Checker A2 (verbatim): `PASS A2 the diff applies at the tip (strict)`; golden comparison [round.json, verbatim]: TREE-IDENTICAL.

**Held 10:24 2026-11-12 by Wednesday after a source read (hold_ready.py, test_only_input path; STRICT-APPLY leg passed first). Every clause below is copied from the run's artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-12_ks_2169_o163_p1_transfer_cancel_trim_before_max_and_refused_types_pins/out.md.checker`; product bytes were RE-MEASURED here.** Tip `d35f75875275158ce3b20b636b4198a4c8834968`. Brief: not given (--brief)
- Touched set [patch.diff `+++` headers == input.json test_files, no product or plant file named]: ['Blockchain/Dev/services/transfer/src/__tests__/ks2055-transfer-cancel-reason-is-a-string-of-at-most-1000-characters.test.ts']; `+` lines 18 (ASCII), `-` lines 0.
- Product bytes UNCHANGED [re-measured: tip index blobs before and after a strict `git apply --cached -p1` of patch.diff]: `Blockchain/Dev/services/transfer/src/index.ts` blob ed33fda1ad9d; plant file(s) also unchanged.
- Red cells [input.json]:
  - `ks2169 R7 a 1000-character reason padded with spaces`
  - `ks2169 R8 true, false, 0 and an array as the reason`
- Red-first evidence [checker.out, verbatim]: A4 green without plant, A5 red under the plant by assertion.
- Checker legs [checker.out, verbatim]:
  - `PASS A1 output is exactly one fenced ```diff block, nothing outside it`
  - `PASS A2 the diff applies at the tip (strict)`
  - `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=1 ok=1 bad=0 skipped_newfile=0)`
  - `PASS A3 touched set == the brief's declared set (Blockchain/Dev/services/transfer/src/__tests__/ks2055-transfer-cancel-reason-is-a-string-of-at-most-1000-characters.test.ts)`
  - `PASS A3p the plant applies at the tip (1 pinned line(s))`
  - `PASS A4 GREEN WITHOUT PLANT: 2 red cell(s) exist and pass on the unmodified product; declared files 12 cells, 0 red`
  - `PASS A6 WHOLE SUITE no worse: cells 481 -> 483, red 0 -> 0`
  - `PASS A5 RED WITH PLANT: 2 red cell(s) fail by assertion under the plant (Blockchain/Dev/services/transfer/src/index.ts), pass without it`
  - `PASS A7 RESTORE: 2 watched file(s) back at their tip sha256; tracked tree clean`
- RESULT [checker.out]: `RESULT: PASS (tier test_only_input)`

**PR NOTES for the raise seat:** TEST_ONLY_INPUT - test bytes only, zero product bytes. Apply `patch.diff` strictly (`git apply -p1`; proven by the hold's STRICT-APPLY leg). The red proof is the brief's plant (checker clone only), not a change in the PR. No `tsc` leg covers a vitest file; DOES NOT PROVE the plant is the regression that matters or that a cell catches a different one. Wednesday read the cells against the brief before this hold.

```diff
--- a/Blockchain/Dev/services/transfer/src/__tests__/ks2055-transfer-cancel-reason-is-a-string-of-at-most-1000-characters.test.ts
+++ b/Blockchain/Dev/services/transfer/src/__tests__/ks2055-transfer-cancel-reason-is-a-string-of-at-most-1000-characters.test.ts
@@ -169,4 +169,22 @@
     expect(res.status).toBe(200);
     expect((await lastEntry(id)).reason).toBe('Cancelled by user');
   });
+
+  // KS-2169 G312-2182-3 (gate 312, mutant T4): the trim runs BEFORE the 1000 bound, so a 1000-character reason padded with spaces is accepted and recorded trimmed.
+  it('RED ks2169 R7 a 1000-character reason padded with spaces either side is accepted and recorded trimmed', async () => {
+    const id = await makeTransfer();
+    const res = await cancel(id, { reason: `     ${'x'.repeat(1000)}     ` });
+    expect(res.status).toBe(200);
+    expect((await lastEntry(id)).reason).toBe('x'.repeat(1000));
+  });
+
+  // KS-2169 G312-2182-4 (gate 312): beyond a number and an object, a boolean, zero and an array are refused with 400 and write nothing (false and 0 used to fall back to the default text).
+  it('RED ks2169 R8 true, false, 0 and an array as the reason each answer 400 and write nothing', async () => {
+    const id = await makeTransfer();
+    for (const reason of [true, false, 0, ['a']]) {
+      const refused = await cancel(id, { reason });
+      expect([JSON.stringify(reason), refused.status]).toEqual([JSON.stringify(reason), 400]);
+    }
+    expect((await lastEntry(id)).toStatus).not.toBe('cancelled');
+  });
 });
```
