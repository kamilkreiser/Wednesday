# READY — KS-1238-N95-1 (Ornith, briefed, test_only) — PASS 8/8 first sample — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-20_ks1238-ornith35b-night3/out.md.checker/patch.diff`** (from `ls`, 03:25).

**Held 03:25 2026-09-20 by the 18:0x Wednesday seat after a source read** (woken on the verdicts by the background waiter). Tip `c87458bdd`. A connector key alone gets 401 on POST /api/users/admin/create and PATCH /api/users/admin/:id, pinning the admin.ts same-path shadow (N95-1; nothing about O-1). Test-only: 0 `-` lines, one file under `__tests__/`; every `+` line = the brief; crossed control mostly absent. Source: the #1092-#1096 gate's NOT-PINNED rows. Raise: Refs KS-1238, never Closes; AUTH surface test-only -> tier 1.

**HELD. Not raised.**

---
## Checker verdict (verbatim tail)
PASS T7[ADMINSHADOW1428] every control green under the tamper
T6 summary: 2/2 tamper(s) red exactly their declared set
T7 summary: controls green under all 2 tamper(s)
T8 summary: all 2 tamper file(s) restored by bytes
SUMMARY test_only file=Blockchain/Dev/services/api-gateway/src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts mode=modify runner=vitest cells=27 tampers=2 apply=strict
RESULT: PASS (8/8)

## Diff
```diff
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts
@@ -293,1 +293,13 @@
+  it('RED KS-1238: POST /api/users/admin/create with a connector key alone is refused 401 by requireAdmin and nothing is forwarded', async () => {
+    RAN.add('admin create shadow');
+    const ac = await post(gateway!.url, '/api/users/admin/create', { 'x-api-key': OK_KEY }, { email: 'qa-ks1238@secuura.io', role: 'user' });
+    expect([ac.status, ac.code, ac.forwarded.map((h) => h.url)]).toEqual([401, 'UNAUTHORIZED', []]);
+  });
+  it('RED KS-1238: PATCH /api/users/admin/:id with a connector key alone is refused 401 by requireAdmin and nothing is forwarded', async () => {
+    RAN.add('admin patch shadow');
+    const ap0 = hits.length;
+    const ap = await fetch(gateway!.url + '/api/users/admin/u-ks1238', { method: 'PATCH', headers: { 'content-type': 'application/json', 'x-api-key': OK_KEY }, body: JSON.stringify({ role: 'user' }) });
+    const apCode = ((await ap.json().catch(() => ({}))) as any)?.error?.code ?? null; await new Promise((r) => setTimeout(r, 50));
+    expect([ap.status, apCode, hits.slice(ap0).map((h) => h.url)]).toEqual([401, 'UNAUTHORIZED', []]);
+  });
   it('RED KS-1238 (i): a valid key + a REVOKED session JWT under a lower-case or upper-case bearer scheme, exchange refused, reaches the upstream with no Bearer', async () => {
@@ -429,1 +441,2 @@
+      'admin create shadow', 'admin patch shadow',
       'KS-1238 (iii) super-admin tenants',
```
