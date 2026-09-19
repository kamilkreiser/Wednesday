# READY — KS-1282-N96-1b (Ornith, briefed, test_only) — PASS 8/8 first sample — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-20_ks1282-ornith35b-night3/out.md.checker/patch.diff`** (from `ls`, 03:25).

**Held 03:25 2026-09-20 by the 18:0x Wednesday seat after a source read** (woken on the verdicts by the background waiter). Tip `c87458bdd`. Six requireSuperAdmin guards (767,782,792,806,832,859) (N96-1b; with N96-1a all 11 unpinned guards; KS-1282 completeness is Kam's). Test-only: 0 `-` lines, one file under `__tests__/`; every `+` line = the brief; crossed control mostly absent. Source: the #1092-#1096 gate's NOT-PINNED rows. Raise: Refs KS-1282, never Closes; AUTH surface test-only -> tier 1.

**HELD. Not raised.**

---
## Checker verdict (verbatim tail)
PASS T7[GUARD859UNGUARDED] every control green under the tamper
T6 summary: 6/6 tamper(s) red exactly their declared set
T7 summary: controls green under all 6 tamper(s)
T8 summary: all 6 tamper file(s) restored by bytes
SUMMARY test_only file=Blockchain/Dev/services/api-gateway/src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts mode=modify runner=vitest cells=31 tampers=6 apply=strict
RESULT: PASS (8/8)

## Diff
```diff
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts
@@ -364,1 +364,35 @@
+  it('RED: a connector key is refused 403 on POST /api/platform/tenant-key and nothing is forwarded', async () => {
+    RAN.add('platform POST /api/platform/tenant-key refuses a connector');
+    const k767 = await post(gateway!.url, '/api/platform/tenant-key', { 'x-api-key': OK_KEY }, { tenantId: 'ks1282-t1', key: 'qa-ks1282-key' });
+    expect([k767.status, k767.code, k767.forwarded.map((h) => h.url)]).toEqual([403, 'FORBIDDEN', []]);
+  });
+  it('RED: a connector key is refused 403 on DELETE /api/platform/tenant-key/:tenantId and nothing is forwarded', async () => {
+    RAN.add('platform DELETE /api/platform/tenant-key/:tenantId refuses a connector');
+    const k782n = hits.length;
+    const k782 = await fetch(gateway!.url + '/api/platform/tenant-key/ks1282-t1', { method: 'DELETE', headers: { 'x-api-key': OK_KEY } });
+    const k782code = ((await k782.json().catch(() => ({}))) as any)?.error?.code ?? null; await new Promise((r) => setTimeout(r, 50));
+    expect([k782.status, k782code, hits.slice(k782n).map((h) => h.url)]).toEqual([403, 'FORBIDDEN', []]);
+  });
+  it('RED: a connector key is refused 403 on GET /api/platform/tenant-key/:tenantId/status and nothing is forwarded', async () => {
+    RAN.add('platform GET /api/platform/tenant-key/:tenantId/status refuses a connector');
+    const k792 = await send(gateway!.url, '/api/platform/tenant-key/ks1282-t1/status', { 'x-api-key': OK_KEY });
+    expect([k792.status, k792.code, k792.forwarded.map((h) => h.url)]).toEqual([403, 'FORBIDDEN', []]);
+  });
+  it('RED: a connector key is refused 403 on GET /api/platform/templates/document-types and nothing is forwarded', async () => {
+    RAN.add('platform GET /api/platform/templates/document-types refuses a connector');
+    vi.stubEnv('PLATFORM_DATABASE_URL', 'postgres://ks1282:ks1282@127.0.0.1:1/ks1282_doctypes');
+    const t806 = await send(gateway!.url, '/api/platform/templates/document-types', { 'x-api-key': OK_KEY });
+    expect([t806.status, t806.code, t806.forwarded.map((h) => h.url)]).toEqual([403, 'FORBIDDEN', []]);
+  });
+  it('RED: a connector key is refused 403 on GET /api/platform/templates/workflows and nothing is forwarded', async () => {
+    RAN.add('platform GET /api/platform/templates/workflows refuses a connector');
+    vi.stubEnv('PLATFORM_DATABASE_URL', 'postgres://ks1282:ks1282@127.0.0.1:1/ks1282_workflows');
+    const t832 = await send(gateway!.url, '/api/platform/templates/workflows', { 'x-api-key': OK_KEY });
+    expect([t832.status, t832.code, t832.forwarded.map((h) => h.url)]).toEqual([403, 'FORBIDDEN', []]);
+  });
+  it('RED: a connector key is refused 403 on POST /api/platform/templates/clone-to-tenant and nothing is forwarded', async () => {
+    RAN.add('platform POST /api/platform/templates/clone-to-tenant refuses a connector');
+    const c859 = await post(gateway!.url, '/api/platform/templates/clone-to-tenant', { 'x-api-key': OK_KEY }, { tenantId: 'ks1282-t1' });
+    expect([c859.status, c859.code, c859.forwarded.map((h) => h.url)]).toEqual([403, 'FORBIDDEN', []]);
+  });
   it('control, register-connector: a JWT-only platform admin still succeeds, and all three upstream calls carry the admin\'s own Bearer', async () => {
@@ -424,1 +458,7 @@
+      'platform POST /api/platform/tenant-key refuses a connector',
+      'platform DELETE /api/platform/tenant-key/:tenantId refuses a connector',
+      'platform GET /api/platform/tenant-key/:tenantId/status refuses a connector',
+      'platform GET /api/platform/templates/document-types refuses a connector',
+      'platform GET /api/platform/templates/workflows refuses a connector',
+      'platform POST /api/platform/templates/clone-to-tenant refuses a connector',
       'register live refused',
```
