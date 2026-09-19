# READY — KS-1282-N99-1 (Ornith, briefed, test_only, AUTH surface) — PASS 8/8 first sample — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-20_ks1282-ornith35b-night4/out.md.checker/patch.diff`** (from `ls` of that dir, 06:13; test_only → patch.diff only).

**Held 06:13 2026-09-20 by the 03:3x Wednesday seat (the morning session) after a source read.** Tip `e47019878`. Pins that a tenant ADMIN JWT is refused 403 on GET /api/platform/tenants with nothing forwarded (the #1097-#1099 gate NOT-PINNED row N99-1; tampers SUPERROLESWIDEN at platform.ts:64 and SUPERADMITSANYUSER at :68 — the subagent corrected the gate's :67). AUTH surface, TEST-ONLY → raise at TIER 1: 0 `-` lines, one file under `__tests__/` (the ks1215 test file; keep `ks1215`/`ks-1215` out of branch, title and subject); every `+` line = the brief (7/7); run input sha256 9eb2da9407b2 = the queued input. Content control: the sibling N96-1a brief (same file) holds 1/7 of these lines. **It pins TODAY's 403 only; KS-1282's scope and completeness are Kam's call.** Raise: Refs KS-1282, never Closes; KS-1282 stays Backlog.

**HELD. Not raised.**

---
## Checker verdict (verbatim tail)
PASS T7[SUPERADMITSANYUSER] every control green under the tamper
T6 summary: 2/2 tamper(s) red exactly their declared set
T7 summary: controls green under all 2 tamper(s)
T8 summary: all 2 tamper file(s) restored by bytes
SUMMARY test_only file=Blockchain/Dev/services/api-gateway/src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts mode=modify runner=vitest cells=39 tampers=2 apply=strict
RESULT: PASS (8/8)

## Diff
```diff
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts
@@ -319,1 +319,7 @@
+  it('RED: a tenant ADMIN JWT is refused 403 on GET /api/platform/tenants and nothing is forwarded', async () => {
+    RAN.add('platform tenants GET refuses a tenant ADMIN');
+    const tok = 'Bearer ' + jwt.sign({ userId: 'u-ks1282-admin', email: 'ks1282-admin@secuura.io', role: 'ADMIN', verificationLevel: 'email', authMethod: 'email', tenantId: TENANT, sessionId: 'ks1215-live' }, PRIV, { algorithm: 'RS256', expiresIn: '10m' });
+    const r = await send(gateway!.url, '/api/platform/tenants', { authorization: tok });
+    expect([r.status, r.code, r.forwarded.map((h) => h.url)]).toEqual([403, 'FORBIDDEN', []]);
+  });
   it('RED: a connector key is refused 403 on GET /api/platform/tenants and nothing is forwarded', async () => {
@@ -514,1 +520,2 @@
+      'platform tenants GET refuses a tenant ADMIN',
       'platform tenants GET refuses a connector',
```
