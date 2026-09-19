# READY — KS-1282-N91-2 (Ornith, briefed, test_only) — PASS 8/8 first sample — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-20_ks1282-ornith35b-night/out.md.checker/patch.diff`** (from `ls`, 00:06).

**Held 00:06 2026-09-20 by the 18:0x Wednesday seat after a source read** (woken on the verdicts by the background waiter). Tip `4273adfac`. A connector key is refused 403 on GET /api/platform/tenants and nothing is forwarded (N91-2; pins the :222 guard only). Test-only: 0 `-` lines, one file under `__tests__/`; every `+` line = the brief; crossed control mostly absent. Both-order collision proofs against held N90-1 (ks1238 file) / N91-1 (ks1215 file) are in the brief. Source: the #1084-#1091 gate's NOT-PINNED rows. Raise: Refs KS-1282, never Closes; AUTH surface test-only -> tier 1.

**HELD. Not raised.**

---
## Checker verdict (verbatim tail)
PASS T7[TENANTSGETUNGUARDED] every control green under the tamper
T6 summary: 1/1 tamper(s) red exactly their declared set
T7 summary: controls green under all 1 tamper(s)
T8 summary: all 1 tamper file(s) restored by bytes
SUMMARY test_only file=Blockchain/Dev/services/api-gateway/src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts mode=modify runner=vitest cells=23 tampers=1 apply=strict
RESULT: PASS (8/8)

## Diff
```diff
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts
@@ -288,1 +288,6 @@
+  it('RED: a connector key is refused 403 on GET /api/platform/tenants and nothing is forwarded', async () => {
+    RAN.add('platform tenants GET refuses a connector');
+    const tg = await send(gateway!.url, '/api/platform/tenants', { 'x-api-key': OK_KEY });
+    expect([tg.status, tg.code, tg.forwarded.map((h) => h.url)]).toEqual([403, 'FORBIDDEN', []]);
+  });
   it('RED KS-1238 (i): a valid key + a REVOKED session JWT under a lower-case or upper-case bearer scheme, exchange refused, reaches the upstream with no Bearer', async () => {
@@ -410,1 +415,2 @@
+      'platform tenants GET refuses a connector',
       'KS-1238 (i) bearer scheme case',
```
