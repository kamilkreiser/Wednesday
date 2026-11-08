# READY - KS-2005-KS-2005-O103-P3 (Spark (DeepSeek V4 Flash), briefed, test_only_input) - PASS 9/9 - HELD for QA

> CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-08_ks_2005_o103_p3_seed_demo_users_one_created/out.md.checker/patch.diff` (from `ls` at 23:21 2026-11-08; sha256[:16] 3d51a673ff9cde76, 1193 B; byte-equal to the out.md fence). Checker A2 (verbatim): `PASS A2 the diff applies at the tip (strict)`; golden comparison [round.json, verbatim]: TREE-IDENTICAL.

**Held 23:21 2026-11-08 by Spark operator 103 after a source read (hold_ready.py, test_only_input path; STRICT-APPLY leg passed first). Every clause below is copied from the run's artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-08_ks_2005_o103_p3_seed_demo_users_one_created/out.md.checker`; product bytes were RE-MEASURED here.** Tip `abd044f63a9dd5673f1b9ff7a2b1e42e1c26de82`. Brief: not given (--brief)
- Touched set [patch.diff `+++` headers == input.json test_files, no product or plant file named]: ['Blockchain/Dev/services/originate/src/__tests__/ks1990-seed-demo-users-success-follows-the-counts.test.ts']; `+` lines 10 (ASCII), `-` lines 0.
- Product bytes UNCHANGED [re-measured: tip index blobs before and after a strict `git apply --cached -p1` of patch.diff]: `Blockchain/Dev/services/originate/src/routes/adminConfig.ts` blob 7329f66d0055; plant file(s) also unchanged.
- Red cells [input.json]:
  - `R6: ONE created and 13 failed`
- Red-first evidence [checker.out, verbatim]: A4 green without plant, A5 red under the plant by assertion.
- Checker legs [checker.out, verbatim]:
  - `PASS A1 output is exactly one fenced ```diff block, nothing outside it`
  - `PASS A2 the diff applies at the tip (strict)`
  - `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=1 ok=1 bad=0 skipped_newfile=0)`
  - `PASS A3 touched set == the brief's declared set (Blockchain/Dev/services/originate/src/__tests__/ks1990-seed-demo-users-success-follows-the-counts.test.ts)`
  - `PASS A3p the plant applies at the tip (golden_red.diff)`
  - `PASS A4 GREEN WITHOUT PLANT: 1 red cell(s) exist and pass on the unmodified product; declared files 12 cells, 0 red`
  - `PASS A6 WHOLE SUITE no worse: cells 2563 -> 2564, red 11 -> 11`
  - `PASS A5 RED WITH PLANT: 1 red cell(s) fail by assertion under the plant (Blockchain/Dev/services/originate/src/routes/adminConfig.ts), pass without it`
  - `PASS A7 RESTORE: 2 watched file(s) back at their tip sha256; tracked tree clean`
- RESULT [checker.out]: `RESULT: PASS (tier test_only_input)`

**PR NOTES for the raise seat:** TEST_ONLY_INPUT - test bytes only, zero product bytes. Apply `patch.diff` strictly (`git apply -p1`; proven by the hold's STRICT-APPLY leg). The red proof is the brief's plant (checker clone only), not a change in the PR. No `tsc` leg covers a vitest file; DOES NOT PROVE the plant is the regression that matters or that a cell catches a different one. Wednesday read the cells against the brief before this hold.

```diff
--- a/Blockchain/Dev/services/originate/src/__tests__/ks1990-seed-demo-users-success-follows-the-counts.test.ts
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1990-seed-demo-users-success-follows-the-counts.test.ts
@@ -137,6 +137,16 @@
     expect(outcome(await seed())).toEqual({ status: 500, body: { success: false, seededUsers: 0, created: 0, alreadyPresent: 13, failed: 1 } });
   });
 
+  it('RED KS-1990 R6: ONE created and 13 failed answers 200 with success false (the boundary: any created row keeps the status at 200)', async () => {
+    let calls = 0;
+    mockExecuteRaw.mockImplementation(async () => {
+      calls++;
+      if (calls === 1) return 1;
+      throw new Error('ks1990 insert failed');
+    });
+    expect(outcome(await seed())).toEqual({ status: 200, body: { success: false, seededUsers: 1, created: 1, alreadyPresent: 0, failed: 13 } });
+  });
+
   it('control KS-1990 C1: every insert creating a row stays 200 with success true (14 created)', async () => {
     mockExecuteRaw.mockResolvedValue(1);
     expect(outcome(await seed())).toEqual({ status: 200, body: { success: true, seededUsers: USERS, created: USERS, alreadyPresent: 0, failed: 0 } });
```
