# READY — KS-1282-N96-1a (Ornith, briefed, test_only) — PASS 8/8 first sample — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-20_ks1282-ornith35b-night2/out.md.checker/patch.diff`** (from `ls`, 03:25).

**Held 03:25 2026-09-20 by the 18:0x Wednesday seat after a source read** (woken on the verdicts by the background waiter). Tip `c87458bdd`. Five requireSuperAdmin guards (284,301,320,339,362): a connector key is refused 403 and nothing forwarded (N96-1a). Test-only: 0 `-` lines, one file under `__tests__/`; every `+` line = the brief; crossed control mostly absent. Source: the #1092-#1096 gate's NOT-PINNED rows. Raise: Refs KS-1282, never Closes; AUTH surface test-only -> tier 1.

**HELD. Not raised.**

---
## Checker verdict (verbatim tail)
PASS T7[GUARD362UNGUARDED] every control green under the tamper
T6 summary: 5/5 tamper(s) red exactly their declared set
T7 summary: controls green under all 5 tamper(s)
T8 summary: all 5 tamper file(s) restored by bytes
SUMMARY test_only file=Blockchain/Dev/services/api-gateway/src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts mode=modify runner=vitest cells=30 tampers=5 apply=strict
RESULT: PASS (8/8)

## Diff
```diff
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts
@@ -288,1 +288,32 @@
+  it('RED: a connector key is refused 403 on GET /api/platform/tenants/:id and nothing is forwarded', async () => {
+    RAN.add('platform GET /api/platform/tenants/:id refuses a connector');
+    const g284 = await send(gateway!.url, '/api/platform/tenants/ks1282-t1', { 'x-api-key': OK_KEY });
+    expect([g284.status, g284.code, g284.forwarded.map((h) => h.url)]).toEqual([403, 'FORBIDDEN', []]);
+  });
+  it('RED: a connector key is refused 403 on PATCH /api/platform/tenants/:id and nothing is forwarded', async () => {
+    RAN.add('platform PATCH /api/platform/tenants/:id refuses a connector');
+    const p301n = hits.length;
+    const p301 = await fetch(gateway!.url + '/api/platform/tenants/ks1282-t1', { method: 'PATCH', headers: { 'content-type': 'application/json', 'x-api-key': OK_KEY }, body: JSON.stringify({ name: 'KS1282 renamed' }) });
+    const p301code = ((await p301.json().catch(() => ({}))) as any)?.error?.code ?? null; await new Promise((r) => setTimeout(r, 50));
+    expect([p301.status, p301code, hits.slice(p301n).map((h) => h.url)]).toEqual([403, 'FORBIDDEN', []]);
+  });
+  it('RED: a connector key is refused 403 on PATCH /api/platform/tenants/:id/status and nothing is forwarded', async () => {
+    RAN.add('platform PATCH /api/platform/tenants/:id/status refuses a connector');
+    const s320n = hits.length;
+    const s320 = await fetch(gateway!.url + '/api/platform/tenants/ks1282-t1/status', { method: 'PATCH', headers: { 'content-type': 'application/json', 'x-api-key': OK_KEY }, body: JSON.stringify({ status: 'suspended' }) });
+    const s320code = ((await s320.json().catch(() => ({}))) as any)?.error?.code ?? null; await new Promise((r) => setTimeout(r, 50));
+    expect([s320.status, s320code, hits.slice(s320n).map((h) => h.url)]).toEqual([403, 'FORBIDDEN', []]);
+  });
+  it('RED: a connector key is refused 403 on DELETE /api/platform/tenants/:id and nothing is forwarded', async () => {
+    RAN.add('platform DELETE /api/platform/tenants/:id refuses a connector');
+    const d339n = hits.length;
+    const d339 = await fetch(gateway!.url + '/api/platform/tenants/ks1282-t1', { method: 'DELETE', headers: { 'x-api-key': OK_KEY } });
+    const d339code = ((await d339.json().catch(() => ({}))) as any)?.error?.code ?? null; await new Promise((r) => setTimeout(r, 50));
+    expect([d339.status, d339code, hits.slice(d339n).map((h) => h.url)]).toEqual([403, 'FORBIDDEN', []]);
+  });
+  it('RED: a connector key is refused 403 on GET /api/platform/audit-log and nothing is forwarded', async () => {
+    RAN.add('platform GET /api/platform/audit-log refuses a connector');
+    const a362 = await send(gateway!.url, '/api/platform/audit-log', { 'x-api-key': OK_KEY });
+    expect([a362.status, a362.code, a362.forwarded.map((h) => h.url)]).toEqual([403, 'FORBIDDEN', []]);
+  });
   it('RED: a connector key is refused 403 on GET /api/platform/tenants and nothing is forwarded', async () => {
@@ -426,1 +457,6 @@
+      'platform GET /api/platform/tenants/:id refuses a connector',
+      'platform PATCH /api/platform/tenants/:id refuses a connector',
+      'platform PATCH /api/platform/tenants/:id/status refuses a connector',
+      'platform DELETE /api/platform/tenants/:id refuses a connector',
+      'platform GET /api/platform/audit-log refuses a connector',
       'platform tenants GET refuses a connector',
```
