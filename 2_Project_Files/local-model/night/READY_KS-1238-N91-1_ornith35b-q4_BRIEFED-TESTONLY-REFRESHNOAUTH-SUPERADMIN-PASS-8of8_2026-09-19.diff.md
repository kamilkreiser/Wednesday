# READY — KS-1238-N91-1 (Ornith, briefed, test_only) — PASS 8/8 first sample — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-19_ks1238-ornith35b-night6/out.md.checker/patch.diff`** (from `ls`, 23:51).

**Held 23:51 2026-09-19 by the 18:0x Wednesday seat after a source read** (woken on the verdicts by the background waiter). Tip `4273adfac`. The F-1 super-admin cell: POST /api/platform/tenants forwards its own post-auth Bearer to refresh-tenants (N91-1; presumes :254 kept). Test-only: 0 `-` lines, one file under `__tests__/`; every `+` line = the brief; crossed control (the other round-16 briefs) mostly absent. Source: the #1084-#1091 gate's NOT-PINNED rows. Raise: Refs KS-1238, never Closes; AUTH surface test-only -> tier 1.

**HELD. Not raised.**

---
## Checker verdict (verbatim tail)
PASS T7[REFRESHNOAUTH] every control green under the tamper
T6 summary: 1/1 tamper(s) red exactly their declared set
T7 summary: controls green under all 1 tamper(s)
T8 summary: all 1 tamper file(s) restored by bytes
SUMMARY test_only file=Blockchain/Dev/services/api-gateway/src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts mode=modify runner=vitest cells=23 tampers=1 apply=strict
RESULT: PASS (8/8)

## Diff
```diff
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts
@@ -349,1 +349,6 @@
+  it('RED KS-1238 (iii): a super-admin JWT on POST /api/platform/tenants reaches tenant-provisioning and refresh-tenants with its own post-auth Bearer', async () => {
+    RAN.add('KS-1238 (iii) super-admin tenants');
+    const sa = await post(gateway!.url, '/api/platform/tenants', { authorization: adminJwt('ks1215-live') }, { name: 'KS1238 SA Tenant', slug: 'ks1238-sa-tenant' });
+    expect([sa.status, sa.forwarded.map((h) => [h.url, h.bearer])]).toEqual([200, [['/api/tenants', 'user:ks1215-live'], ['/api/admin/refresh-tenants', 'user:ks1215-live']]]);
+  });
   it('control, register-connector: a JWT-only platform admin still succeeds, and all three upstream calls carry the admin\'s own Bearer', async () => {
@@ -412,1 +417,2 @@
+      'KS-1238 (iii) super-admin tenants',
     ];
```
