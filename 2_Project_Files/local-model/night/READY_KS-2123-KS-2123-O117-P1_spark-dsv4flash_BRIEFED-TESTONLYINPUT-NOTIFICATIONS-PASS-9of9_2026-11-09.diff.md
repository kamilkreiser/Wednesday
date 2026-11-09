# READY - KS-2123-KS-2123-O117-P1 (Spark (DeepSeek V4 Flash), briefed, test_only_input) - PASS 9/9 - HELD for QA

> CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2123_o117_p1_ks1448_notification_own_id_type_and_admin_cells/out.md.checker/patch.diff` (from `ls` at 17:59 2026-11-09; sha256[:16] 5ed5b7613764ec26, 1620 B; byte-equal to the out.md fence). Checker A2 (verbatim): `PASS A2 the diff applies at the tip (strict)`; golden comparison [round.json, verbatim]: TREE-IDENTICAL.

**Held 17:59 2026-11-09 by Wednesday after a source read (hold_ready.py, test_only_input path; STRICT-APPLY leg passed first). Every clause below is copied from the run's artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2123_o117_p1_ks1448_notification_own_id_type_and_admin_cells/out.md.checker`; product bytes were RE-MEASURED here.** Tip `e8d23ce366e292ed6ca13f296cc2cfb2a3796496`. Brief: not given (--brief)
- Touched set [patch.diff `+++` headers == input.json test_files, no product or plant file named]: ['Blockchain/Dev/services/api-gateway/src/__tests__/ks1448-notification-create-own-id-only.test.ts']; `+` lines 9 (ASCII), `-` lines 0.
- Product bytes UNCHANGED [re-measured: tip index blobs before and after a strict `git apply --cached -p1` of patch.diff]: `Blockchain/Dev/services/api-gateway/src/routes/notifications.ts` blob 14b31ea57c74; plant file(s) also unchanged.
- Red cells [input.json]:
  - `KS-1448 R1: an ADMIN role`
  - `KS-2123 R6: type purchase`
  - `KS-2123 R6: type certification`
  - `KS-2123 R6: type verification`
  - `KS-2123 R6: type transfer`
- Red-first evidence [checker.out, verbatim]: A4 green without plant, A5 red under the plant by assertion.
- Checker legs [checker.out, verbatim]:
  - `PASS A1 output is exactly one fenced ```diff block, nothing outside it`
  - `PASS A2 the diff applies at the tip (strict)`
  - `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=2 ok=2 bad=0 skipped_newfile=0)`
  - `PASS A3 touched set == the brief's declared set (Blockchain/Dev/services/api-gateway/src/__tests__/ks1448-notification-create-own-id-only.test.ts)`
  - `PASS A3p the plant applies at the tip (1 pinned line(s))`
  - `PASS A4 GREEN WITHOUT PLANT: 5 red cell(s) exist and pass on the unmodified product; declared files 33 cells, 0 red`
  - `PASS A6 WHOLE SUITE no worse: cells 1880 -> 1885, red 0 -> 0`
  - `PASS A5 RED WITH PLANT: 5 red cell(s) fail by assertion under the plant (Blockchain/Dev/services/api-gateway/src/routes/notifications.ts), pass without it`
  - `PASS A7 RESTORE: 2 watched file(s) back at their tip sha256; tracked tree clean`
- RESULT [checker.out]: `RESULT: PASS (tier test_only_input)`

**PR NOTES for the raise seat:** TEST_ONLY_INPUT - test bytes only, zero product bytes. Apply `patch.diff` strictly (`git apply -p1`; proven by the hold's STRICT-APPLY leg). The red proof is the brief's plant (checker clone only), not a change in the PR. No `tsc` leg covers a vitest file; DOES NOT PROVE the plant is the regression that matters or that a cell catches a different one. Wednesday read the cells against the brief before this hold.

```diff
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1448-notification-create-own-id-only.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1448-notification-create-own-id-only.test.ts
@@ -100,6 +100,7 @@
   ['a super admin in the casing a JWT carries', { userId: 'ks1448-super-lower', role: 'super_admin' }],
   ['a super admin in upper case', { userId: 'ks1448-super-upper', role: 'SUPER_ADMIN' }],
   ['a platform_admin role', { userId: 'ks1448-platform', role: 'platform_admin' }],
+  ['an ADMIN role', { userId: 'ks1448-admin', role: 'ADMIN' }],
   // The shape authenticateToken attaches for a valid sk_ key (middleware/auth.ts).
   ['a connector key', { userId: 'connector:ks1448-conn', role: 'connector', connectorId: 'ks1448-conn', authMethod: 'api_key' }],
 ];
@@ -115,6 +116,14 @@
     expect(await rowsOf(target)).toEqual([]);
     expect(mockLoggerError).not.toHaveBeenCalled();
   });
+
+  // KS-2123 (gate 246 G246-F2): the refusal must hold for every notification type, not only security and system.
+  it.each(['purchase', 'certification', 'verification', 'transfer'])('RED KS-2123 R6: type %s posting for another user gets 403 and no row is stored', async (type) => {
+    const target = `ks1448-target-type-${type}`;
+    const res = await post({ userId: 'ks1448-typed', role: 'user' }, { ...BODY, type, userId: target });
+    expect(res._status).toBe(403);
+    expect(await rowsOf(target)).toEqual([]);
+  });
 
   it('RED KS-1448 R2: the phishing shape, type security with an actionUrl, stores nothing for the target', async () => {
     const target = 'ks1448-target-phish';
```
