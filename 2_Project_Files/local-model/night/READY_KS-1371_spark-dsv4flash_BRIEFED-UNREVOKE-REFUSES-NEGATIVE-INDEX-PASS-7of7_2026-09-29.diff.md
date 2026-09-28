# READY — KS-1371 unrevoke refuses a negative index (spark-dsv4flash, briefed, first valid round) — PASS 7/7 — HELD for QA

> **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-29_KS-1371-b/out.md.checker/patch.diff`**. **BYTE-IDENTICAL to the screen drafter's golden** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1371/KS-1371.golden.diff` (`cmp` rc 0; a mutated-golden control rc 1), measured by Wednesday.

**Held BY HAND at 06:33 2026-09-29 by Wednesday morning seat 407373b1** (hold_ready.py's owed defect; same shape as the overnight holds). Source develop **215cc6875e2b** (ls-remote against GitHub in the round's source clone).

- **Why:** vc-issuer `POST /api/status/:id/unrevoke` accepted `index: -1` and answered 200. The fix refuses a negative index with 400 `'index must be a non-negative integer'` at `status.ts:328-:329`; `/revoke` is untouched and still admits `-1` (the KS-662 ruling). Four cells appended to the existing KS-1269 unrevoke test file.
- **A choice the brief made, for the raise seat to state in the PR body:** the ticket offers "validate against the declared bounds, or widen the ruling". This takes the first, which is what KS-662 and the schema's `nonnegative()` already say. If Kam wants the ruling widened instead, this READY is not raised.
- **Round record:** a first attempt (`runs/spark_secuura_2026-09-29_KS-1371`) was VOID, a HARNESS fault and not a model round: the scratch source clone's `origin` was the local Blockchain checkout, whose develop ref is stale (3bad652), so build_input pinned the wrong tip and prepare_clone refused. Fixed by pointing that clone's origin at GitHub; this is round 1 of the counter.
- **Tier:** briefed for Ornith; run on the Spark because Ornith's G2 gate refuses while a Secuura seat pane is live.
- Checker verdict [checker.out, verbatim]:
  - `PASS A1 output is exactly one fenced ```diff block, nothing outside it`
  - `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`
  - `PASS A3 touched-file set == { Blockchain/Dev/services/vc-issuer/src/routes/status.ts , Blockchain/Dev/services/vc-issuer/src/__tests__/ks1269-status-unrevoke-refuses-a-non-integer-index.test.ts }`
  - `PASS A3c every '+' line the brief adds is in the product hunk (17 line(s)), and no tip line is re-added as a '+' (A3d)`
  - `PASS A4 RED-FIRST: src/__tests__/ks1269-status-unrevoke-refuses-a-non-integer-index.test.ts fails at the untouched tip (2 failed / 9 run; controls green; assertion reds)`
  - `PASS A5 GREEN-AFTER: src/__tests__/ks1269-status-unrevoke-refuses-a-non-integer-index.test.ts passes with the product hunk (9 passed / 9 run)`
  - `PASS A6 whole services/vc-issuer suite: no NEW red vs the untouched tip`
  - `PASS A7 tsc --noEmit for services/vc-issuer: rc 0 after the patch (baseline rc=0)`
  - `SUMMARY files=2 +21/-2 test=src/__tests__/ks1269-status-unrevoke-refuses-a-non-integer-index.test.ts red_first=yes apply_mode=strict`
  - `RESULT: PASS (7/7)`
  - `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=2 ok=2 bad=0 skipped_newfile=0)`
  - `SPARK RESULT: PASS (checker rc 0 + A2a anchor OK)`

```diff
--- a/Blockchain/Dev/services/vc-issuer/src/routes/status.ts
+++ b/Blockchain/Dev/services/vc-issuer/src/routes/status.ts
@@ -327,4 +327,5 @@
     // KS-1269: index is optional and not read here, but a present index must be an integer.
-    if (req.body.index !== undefined && !Number.isInteger(req.body.index)) {
-      throw new AppError('index must be an integer', 400);
+    // KS-1371: and not below the declared minimum 0 (KS-662 tolerates index -1 on revoke only).
+    if (req.body.index !== undefined && (!Number.isInteger(req.body.index) || req.body.index < 0)) {
+      throw new AppError('index must be a non-negative integer', 400);
     }
--- a/Blockchain/Dev/services/vc-issuer/src/__tests__/ks1269-status-unrevoke-refuses-a-non-integer-index.test.ts
+++ b/Blockchain/Dev/services/vc-issuer/src/__tests__/ks1269-status-unrevoke-refuses-a-non-integer-index.test.ts
@@ -77,3 +77,21 @@
     expect(await unrevokeWith('urn:uuid:ks1269u-fraction', { index: 1.5 })).toEqual([400, 'BAD_REQUEST', true]);
   });
+
+  it('control KS-1371: index 0 still unrevokes, 200', async () => {
+    expect(await unrevokeWith('urn:uuid:ks1371-zero', { index: 0 })).toEqual([200, null, false]);
+  });
+
+  it('control KS-1371: revoke still admits index -1 (the KS-662 ruling), 200', async () => {
+    await dispatch('POST', '/default/allocate', { credentialId: 'urn:uuid:ks1371-revoke' });
+    const r = await dispatch('POST', '/default/revoke', { credentialId: 'urn:uuid:ks1371-revoke', index: -1 });
+    expect([r.status, r.body?.revoked]).toEqual([200, true]);
+  });
+
+  it('RED KS-1371 U1: index -1 is refused 400 and the credential stays revoked', async () => {
+    expect(await unrevokeWith('urn:uuid:ks1371-minus-one', { index: -1 })).toEqual([400, 'BAD_REQUEST', true]);
+  });
+
+  it('RED KS-1371 U2: index -7 is refused 400 and the credential stays revoked', async () => {
+    expect(await unrevokeWith('urn:uuid:ks1371-minus-seven', { index: -7 })).toEqual([400, 'BAD_REQUEST', true]);
+  });
 });
```
