# READY - KS-2123-KS-2123-O106-P1 (Spark (DeepSeek V4 Flash), briefed, test_only_input) - PASS 9/9 - HELD for QA

> CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2123_o106_p1_notification_own_id_rule_pins_every_type_and_the_admin_role/out.md.checker/patch.diff` (from `ls` at 02:23 2026-11-09; sha256[:16] f39d08c9b5c388c4, 1511 B; byte-equal to the out.md fence). Checker A2 (verbatim): `PASS A2 the diff applies at the tip (strict)`; golden comparison [round.json, verbatim]: TREE-IDENTICAL.

**Held 02:23 2026-11-09 by Wednesday after a source read (hold_ready.py, test_only_input path; STRICT-APPLY leg passed first). Every clause below is copied from the run's artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2123_o106_p1_notification_own_id_rule_pins_every_type_and_the_admin_role/out.md.checker`; product bytes were RE-MEASURED here.** Tip `c0e6e744b7b21f3e1aa28105766764775b50ce6d`. Brief: not given (--brief)
- Touched set [patch.diff `+++` headers == input.json test_files, no product or plant file named]: ['Blockchain/Dev/services/api-gateway/src/__tests__/ks1448-notification-create-own-id-only.test.ts']; `+` lines 9 (ASCII), `-` lines 0.
- Product bytes UNCHANGED [re-measured: tip index blobs before and after a strict `git apply --cached -p1` of patch.diff]: `Blockchain/Dev/services/api-gateway/src/routes/notifications.ts` blob 14b31ea57c74; plant file(s) also unchanged.
- Red cells [input.json]:
  - `R1: an admin posting for another user gets 403`
  - `R6: a notification of type`
- Red-first evidence [checker.out, verbatim]: A4 green without plant, A5 red under the plant by assertion.
- Checker legs [checker.out, verbatim]:
  - `PASS A1 output is exactly one fenced ```diff block, nothing outside it`
  - `PASS A2 the diff applies at the tip (strict)`
  - `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=2 ok=2 bad=0 skipped_newfile=0)`
  - `PASS A3 touched set == the brief's declared set (Blockchain/Dev/services/api-gateway/src/__tests__/ks1448-notification-create-own-id-only.test.ts)`
  - `PASS A3p the plant applies at the tip (golden_red.diff)`
  - `PASS A4 GREEN WITHOUT PLANT: 5 red cell(s) exist and pass on the unmodified product; declared files 33 cells, 0 red`
  - `PASS A6 WHOLE SUITE no worse: cells 1869 -> 1874, red 0 -> 0`
  - `PASS A5 RED WITH PLANT: 5 red cell(s) fail by assertion under the plant (Blockchain/Dev/services/api-gateway/src/routes/notifications.ts), pass without it`
  - `PASS A7 RESTORE: 2 watched file(s) back at their tip sha256; tracked tree clean`
- RESULT [checker.out]: `RESULT: PASS (tier test_only_input)`

**PR NOTES for the raise seat:** TEST_ONLY_INPUT - test bytes only, zero product bytes. Apply `patch.diff` strictly (`git apply -p1`; proven by the hold's STRICT-APPLY leg). The red proof is the brief's plant (checker clone only), not a change in the PR. No `tsc` leg covers a vitest file; DOES NOT PROVE the plant is the regression that matters or that a cell catches a different one. Wednesday read the cells against the brief before this hold.

```diff
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1448-notification-create-own-id-only.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1448-notification-create-own-id-only.test.ts
@@ -96,6 +96,7 @@
   ['a verifier', { userId: 'ks1448-verifier', role: 'VERIFIER' }],
   ['an issuer admin', { userId: 'ks1448-issuer', role: 'ISSUER_ADMIN' }],
   ['an org admin', { userId: 'ks1448-org', role: 'ORG_ADMIN' }],
+  ['an admin', { userId: 'ks1448-admin', role: 'ADMIN' }],
   ['a system admin', { userId: 'ks1448-system', role: 'SYSTEM_ADMIN' }],
   ['a super admin in the casing a JWT carries', { userId: 'ks1448-super-lower', role: 'super_admin' }],
   ['a super admin in upper case', { userId: 'ks1448-super-upper', role: 'SUPER_ADMIN' }],
@@ -140,6 +141,14 @@
       expect(res._json).toEqual(REFUSAL);
       expect(await rowsOf(target)).toEqual([]);
     }
+  });
+
+  it.each(['purchase', 'certification', 'verification', 'transfer'])('RED KS-1448 R6: a notification of type %s for another user gets 403 and no row is stored', async (type) => {
+    const target = `ks1448-target-type-${type}`;
+    const res = await post({ userId: 'ks1448-type-caller', role: 'user' }, { type, title: 'T', message: 'M', userId: target });
+    expect(res._status).toBe(403);
+    expect(res._json).toEqual(REFUSAL);
+    expect(await rowsOf(target)).toEqual([]);
   });
 
   it('RED KS-1448 R5: the answer does not depend on whether the target has rows, which is why 403 and not 404', async () => {
```
