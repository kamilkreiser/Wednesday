# READY — KS-591-KS-591-TENANT-1 (Spark DeepSeek V4 Flash, briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-07_KS-591-platform-tenant-id-uuid/out.md.checker/patch.diff`** (from `ls` at 11:57 2026-10-07; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-07_KS-591-platform-tenant-id-uuid/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-07_KS-591-platform-tenant-id-uuid/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-07_KS-591-platform-tenant-id-uuid/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-07_KS-591-platform-tenant-id-uuid-control-r3/out.md.checker/patch.diff` rc 0, Wednesday late-morning seat).

**Held 11:57 2026-10-07 by Wednesday late-morning seat after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-07_KS-591-platform-tenant-id-uuid/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `69f2045af2a4f5f0b83b2f76c62514512abdc7b5`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/tenant-provisioning/src/tenant-provisioning.openapi.ts , Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks591-platform-tenant-id-path-is-a-uuid.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/tenant-provisioning/src/tenant-provisioning.openapi.ts` (product) and `Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks591-platform-tenant-id-path-is-a-uuid.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
3	3	Blockchain/Dev/services/tenant-provisioning/src/tenant-provisioning.openapi.ts
50	0	Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks591-platform-tenant-id-path-is-a-uuid.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (3 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 3 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 3.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/tenant-provisioning/src/tenant-provisioning.openapi.ts byte-exact incl. leading whitespace (apply mode strict): OK 3 line(s) byte-exact incl. leading whitespace (of 3; 3 line(s) added by the apply)` [a3i_indent.out: `OK 3 line(s) byte-exact incl. leading whitespace (of 3; 3 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/tenant-provisioning/src/tenant-provisioning.openapi.ts` (hunks=3, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks591-platform-tenant-id-path-is-a-uuid.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks591-platform-tenant-id-path-is-a-uuid.test.ts fails at the untouched tip (3 failed / 5 run; controls green; assertion reds)` [red_first.json: failed=3 of total=5; red cell(s): ['KS-591: the tenant {id} path parameter is published as a UUID, as the service enforces RED KS-591 TID1: PATCH /api/platform/tenants/{id}/status publishes {id} with format uuid', 'KS-591: the tenant {id} path parameter is published as a UUID, as the service enforces RED KS-591 TID2: GET /api/platform/tenants/{id} publishes {id} with format uuid', 'KS-591: the tenant {id} path parameter is published as a UUID, as the service enforces RED KS-591 TID3: PATCH /api/platform/tenants/{id} publishes {id} with format uuid']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks591-platform-tenant-id-path-is-a-uuid.test.ts passes with the product hunk (5 passed / 5 run)` [green_after.json: failed=0 of total=5, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=17 failed=0 | after: total=22 failed=0` · `NEW reds: []` [baseline_suite.json total=17 failed=0; after_suite.json total=22 failed=0]
- A6 [verbatim]: `PASS A6 whole services/tenant-provisioning suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/tenant-provisioning: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +53/-3 test=src/__tests__/ks591-platform-tenant-id-path-is-a-uuid.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/tenant-provisioning/src/tenant-provisioning.openapi.ts` (+3/-3 per numstat.out) and the test file `Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks591-platform-tenant-id-path-is-a-uuid.test.ts` (+50/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `69f2045af2a4f5f0b83b2f76c62514512abdc7b5` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-07_KS-591-platform-tenant-id-uuid/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-07_KS-591-platform-tenant-id-uuid/checker.out`.

```diff
--- a/Blockchain/Dev/services/tenant-provisioning/src/tenant-provisioning.openapi.ts
+++ b/Blockchain/Dev/services/tenant-provisioning/src/tenant-provisioning.openapi.ts
@@ -454,3 +454,3 @@
   request: {
-    params: z.object({ id: z.string().openapi({ example: FX.tenant.id }) }),
+    params: z.object({ id: z.string().uuid().openapi({ example: FX.tenant.id }) }),
   },
@@ -481,3 +481,3 @@
   request: {
-    params: z.object({ id: z.string().openapi({ example: FX.tenant.id }) }),
+    params: z.object({ id: z.string().uuid().openapi({ example: FX.tenant.id }) }),
     body: {
@@ -521,3 +521,3 @@
   request: {
-    params: z.object({ id: z.string().openapi({ example: FX.tenant.id }) }),
+    params: z.object({ id: z.string().uuid().openapi({ example: FX.tenant.id }) }),
     body: {
--- /dev/null
+++ b/Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks591-platform-tenant-id-path-is-a-uuid.test.ts
@@ -0,0 +1,50 @@
+// KS-591 / KS-565 (2026-10-06 sweep addendum): PATCH /api/platform/tenants/{id}/status published its {id} path
+// parameter as a bare `type: string`, but the service refuses any non-UUID :id with 400 "Tenant id must be a UUID"
+// (index.ts app.param('id', tenantIdParamGuard), KS-497) - so Schemathesis sent a spec-valid 300-character id and
+// the 400 failed positive_data_acceptance. The same guard covers GET and PATCH /api/platform/tenants/{id}. This
+// file renders the document the generator publishes, from the shared registry the tenant-provisioning module
+// populates on import, and reads each operation's {id} parameter. No server, no database, no network.
+import { describe, it, expect } from 'vitest';
+import { generateOpenApiDocument } from '@secuura/shared';
+import '../tenant-provisioning.openapi';
+
+type AnyObj = Record<string, any>;
+
+const doc = generateOpenApiDocument({ title: 'tenant-provisioning (ks591 id pin)', version: '0.0.0' }) as AnyObj;
+
+const TENANT = '/api/platform/tenants/{id}';
+
+function idParam(path: string, method: string): AnyObj | undefined {
+  const params: AnyObj[] = doc.paths?.[path]?.[method]?.parameters ?? [];
+  return params.find((p) => p.in === 'path' && p.name === 'id');
+}
+
+describe('KS-591: the tenant {id} path parameter is published as a UUID, as the service enforces', () => {
+  it('RED KS-591 TID1: PATCH /api/platform/tenants/{id}/status publishes {id} with format uuid', () => {
+    expect(idParam(TENANT + '/status', 'patch')?.schema?.format).toBe('uuid');
+  });
+
+  it('RED KS-591 TID2: GET /api/platform/tenants/{id} publishes {id} with format uuid', () => {
+    expect(idParam(TENANT, 'get')?.schema?.format).toBe('uuid');
+  });
+
+  it('RED KS-591 TID3: PATCH /api/platform/tenants/{id} publishes {id} with format uuid', () => {
+    expect(idParam(TENANT, 'patch')?.schema?.format).toBe('uuid');
+  });
+
+  it('control KS-591 TIDC1: each {id} stays a required string path parameter with its UUID example', () => {
+    for (const [path, method] of [[TENANT + '/status', 'patch'], [TENANT, 'get'], [TENANT, 'patch']]) {
+      const p = idParam(path, method);
+      expect({ required: p?.required, type: p?.schema?.type }).toEqual({ required: true, type: 'string' });
+      expect(p?.schema?.example ?? p?.example).toBe('00000000-0000-4000-8000-000000000001');
+    }
+  });
+
+  it('control KS-591 TIDC2: the three operations keep bearerAuth and their request bodies', () => {
+    expect(doc.paths?.[TENANT + '/status']?.patch?.security).toEqual([{ bearerAuth: [] }]);
+    expect(doc.paths?.[TENANT]?.get?.security).toEqual([{ bearerAuth: [] }]);
+    expect(doc.paths?.[TENANT]?.patch?.requestBody?.content?.['application/json']?.schema?.$ref).toBe(
+      '#/components/schemas/TenantUpdateRequest',
+    );
+  });
+});
```
