# READY — KS-1269-N71-2 (Ornith, briefed, test_only, runner PINNED vitest, FIRST MULTI-LINE BLOCK TAMPERS) — PASS 8/8 first sample — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-19_ks1269-ornith35b-night4/out.md.checker/patch.diff`** (from `ls`, 18:50).

**Held 18:50 2026-09-19 by the 18:0x Wednesday seat after a source read.** Tip `f9c28a8b8`. Two ordering cells in the ks1269 revoke test pinning the /revoke index guard's position (the #1070-#1076 gate's REVOKEGUARDAFTER404 + REVOKEGUARDBELOWREASON NOT-PINNED rows): a bad index on an UNKNOWN credential is 400 before the 404; a bad index with a bad reason answers the index error. Test-only: 0 `-` lines, one file under `__tests__/`. Source read: 10/10 `+` lines = the brief; crossed control (the N71-1 brief) 7/10 absent (shared scaffolding). Declared deviation (in the brief): AFTER404 reds BOTH new cells — moving the guard below the 404 also moves it below the reason check. Collision with held READY_KS-1269-N71-1: hunks :63 vs :82, same blob in either order (the brief's proof). Raise with KS-1269-N71-1 (same file) — Refs KS-1269, never Closes; pins nothing about -1.

**HELD. Not raised.**

---
## Checker verdict (verbatim tail)
PASS T6[REVOKEGUARDBELOWREASON] red set == declared exactly: {KS-1269 N71-2 ordering: on /revoke, a bad index with a bad r}, every red an assertion failure
PASS T7[REVOKEGUARDBELOWREASON] every control green under the tamper
T6 summary: 2/2 tamper(s) red exactly their declared set
T7 summary: controls green under all 2 tamper(s)
T8 summary: all 2 tamper file(s) restored by bytes
SUMMARY test_only file=Blockchain/Dev/services/vc-issuer/src/__tests__/ks1269-status-revoke-refuses-a-non-integer-index.test.ts mode=modify runner=vitest cells=8 tampers=2 apply=strict
RESULT: PASS (8/8)

## Diff
```diff
--- a/Blockchain/Dev/services/vc-issuer/src/__tests__/ks1269-status-revoke-refuses-a-non-integer-index.test.ts
+++ b/Blockchain/Dev/services/vc-issuer/src/__tests__/ks1269-status-revoke-refuses-a-non-integer-index.test.ts
@@ -63,1 +63,11 @@
+  it('KS-1269 N71-2 ordering: on /revoke, a bad index on an UNKNOWN credential is 400, before the 404', async () => {
+    const r = await dispatch('POST', '/default/revoke', { credentialId: 'urn:uuid:ks1269-never-allocated', index: {} });
+    expect([r.status, r.body?.error?.message]).toEqual([400, 'index must be an integer']);
+  });
+  it('KS-1269 N71-2 ordering: on /revoke, a bad index with a bad reason answers the index error', async () => {
+    const c = 'urn:uuid:ks1269-both-bad';
+    await dispatch('POST', '/default/allocate', { credentialId: c });
+    const r = await dispatch('POST', '/default/revoke', { credentialId: c, index: {}, reason: {} });
+    expect([r.status, r.body?.error?.message]).toEqual([400, 'index must be an integer']);
+  });
   it('control: an integer index still revokes, 200', async () => {
```
