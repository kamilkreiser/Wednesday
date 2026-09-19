# READY — KS-1238-N83-5 (Ornith, briefed, test_only) — PASS 8/8 first sample — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-19_ks1238-ornith35b-night5/out.md.checker/patch.diff`** (from `ls`, 20:12).

**Held 20:12 2026-09-19 by the 18:0x Wednesday seat after a source read** (woken on the verdict by the background waiter). Tip `ba1210afc`. A connector with organizations:register gets 403 on POST /api/platform/tenants with no upstream call (N83-5, KS-1238 (iii) precondition; pins today's 403 only). Test-only: one file under `__tests__/`; every `+`/`-` line = the brief; crossed control (the other round-15 briefs) mostly absent. Source: the #1077-#1083 gate's NOT-PINNED rows. Raise: Refs KS-1238, never Closes; AUTH surface test-only -> tier 1.

**HELD. Not raised.**

---
## Checker verdict (verbatim tail)
PASS T7[TENANTSUNGUARDED] every control green under the tamper
T6 summary: 2/2 tamper(s) red exactly their declared set
T7 summary: controls green under all 2 tamper(s)
T8 summary: all 2 tamper file(s) restored by bytes
SUMMARY test_only file=Blockchain/Dev/services/api-gateway/src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts mode=modify runner=vitest cells=22 tampers=2 apply=strict
RESULT: PASS (8/8)

## Diff
```diff
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts
@@ -344,1 +344,6 @@
+  it('RED KS-1238 (iii): a connector key carrying organizations:register is refused 403 on POST /api/platform/tenants, and neither tenant-provisioning nor refresh-tenants is called', async () => {
+    RAN.add('KS-1238 (iii) tenants refuses a connector');
+    const r = await post(gateway!.url, '/api/platform/tenants', { 'x-api-key': OK_KEY }, { name: 'KS1238 Tenant', slug: 'ks1238-tenant' });
+    expect([r.status, r.code, r.forwarded.map((h) => h.url)]).toEqual([403, 'FORBIDDEN', []]);
+  });
   it('control, register-connector: a JWT-only platform admin still succeeds, and all three upstream calls carry the admin\'s own Bearer', async () => {
@@ -406,1 +411,2 @@
+      'KS-1238 (iii) tenants refuses a connector',
     ];
```
