# READY — KS-1238-N83-6 (Ornith, briefed, test_only) — PASS 8/8 first sample — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-20_ks1238-ornith35b-night2/out.md.checker/patch.diff`** (from `ls`, 00:06).

**Held 00:06 2026-09-20 by the 18:0x Wednesday seat after a source read** (woken on the verdicts by the background waiter). Tip `4273adfac`. register-connector with a LIVE JWT on a REFUSED exchange sends no caller Bearer (N83-6, KS-1238 (iv)). Test-only: 0 `-` lines, one file under `__tests__/`; every `+` line = the brief; crossed control mostly absent. Both-order collision proofs against held N90-1 (ks1238 file) / N91-1 (ks1215 file) are in the brief. Source: the #1084-#1091 gate's NOT-PINNED rows. Raise: Refs KS-1238, never Closes; AUTH surface test-only -> tier 1.

**HELD. Not raised.**

---
## Checker verdict (verbatim tail)
PASS T7[IV_REGLIVEONLY] every control green under the tamper
T6 summary: 1/1 tamper(s) red exactly their declared set
T7 summary: controls green under all 1 tamper(s)
T8 summary: all 1 tamper file(s) restored by bytes
SUMMARY test_only file=Blockchain/Dev/services/api-gateway/src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts mode=modify runner=vitest cells=23 tampers=1 apply=strict
RESULT: PASS (8/8)

## Diff
```diff
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts
@@ -344,1 +344,6 @@
+  it('RED register-connector: a valid key + a LIVE user\'s JWT, exchange REFUSED, sends no caller Bearer to /api/tenants, /api/keys or /api/audit', async () => {
+    RAN.add('register live refused');
+    const liveRefused = await post(gateway!.url, PATH, { 'x-api-key': REFUSED_KEY, authorization: userJwt('ks1215-live') }, registerBody());
+    expect(JSON.stringify([liveRefused.status, registerBearers(liveRefused)])).toBe(JSON.stringify([201, allThree('none')]));
+  });
   it('RED KS-1238 (iii): a connector key carrying organizations:register is refused 403 on POST /api/platform/tenants, and neither tenant-provisioning nor refresh-tenants is called', async () => {
@@ -409,1 +414,2 @@
+      'register live refused',
       'register revoked', 'register live', 'register admin control', 'register key-only control',
```
