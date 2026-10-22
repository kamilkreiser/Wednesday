# READY — KS-1705-KS-1705-REQBODY1705-1 (Spark (DeepSeek V4 Flash), briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-23_ks_1705_p1/out.md.checker/patch.diff`** (from `ls` at 06:37 2026-10-23; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-23_ks_1705_p1/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-23_ks_1705_p1/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden path `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1705_p1/golden.diff/out.md.checker/patch.diff` does not exist — no identity claim is made.

**Held 06:37 2026-10-23 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-23_ks_1705_p1/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `f75b52721dadd9539b64de17575e57823b8a936a`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/security/src/security.openapi.ts , Blockchain/Dev/services/security/src/__tests__/ks1705-security-keys-post-and-admin-scopes-put-bodies-are-required.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/security/src/security.openapi.ts` (product) and `Blockchain/Dev/services/security/src/__tests__/ks1705-security-keys-post-and-admin-scopes-put-bodies-are-required.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
2	2	Blockchain/Dev/services/security/src/security.openapi.ts
55	0	Blockchain/Dev/services/security/src/__tests__/ks1705-security-keys-post-and-admin-scopes-put-bodies-are-required.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (2 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 2 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 2.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/security/src/security.openapi.ts byte-exact incl. leading whitespace (apply mode strict): OK 2 line(s) byte-exact incl. leading whitespace (of 2; 2 line(s) added by the apply)` [a3i_indent.out: `OK 2 line(s) byte-exact incl. leading whitespace (of 2; 2 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/security/src/security.openapi.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/security/src/__tests__/ks1705-security-keys-post-and-admin-scopes-put-bodies-are-required.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1705-security-keys-post-and-admin-scopes-put-bodies-are-required.test.ts fails at the untouched tip (2 failed / 5 run; controls green; assertion reds)` [red_first.json: failed=2 of total=5; red cell(s): ['KS-1705: POST /api/security/keys and PUT /api/security/keys/admin-scopes/{userId} publish a REQUIRED request body RED KS-1705 SK1: POST /api/security/keys marks its request body required', 'KS-1705: POST /api/security/keys and PUT /api/security/keys/admin-scopes/{userId} publish a REQUIRED request body RED KS-1705 SK2: PUT /api/security/keys/admin-scopes/{userId} marks its request body required']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1705-security-keys-post-and-admin-scopes-put-bodies-are-required.test.ts passes with the product hunk (5 passed / 5 run)` [green_after.json: failed=0 of total=5, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=361 failed=0 | after: total=366 failed=0` · `NEW reds: []` [baseline_suite.json total=361 failed=0; after_suite.json total=366 failed=0]
- A6 [verbatim]: `PASS A6 whole services/security suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/security: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +57/-2 test=src/__tests__/ks1705-security-keys-post-and-admin-scopes-put-bodies-are-required.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/security/src/security.openapi.ts` (+2/-2 per numstat.out) and the test file `Blockchain/Dev/services/security/src/__tests__/ks1705-security-keys-post-and-admin-scopes-put-bodies-are-required.test.ts` (+55/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `f75b52721dadd9539b64de17575e57823b8a936a` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-23_ks_1705_p1/input.json`. Brief (located from the run dir's own name under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1705_p1/KS-1705.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-23_ks_1705_p1/checker.out`.

```diff
--- a/Blockchain/Dev/services/security/src/security.openapi.ts
+++ b/Blockchain/Dev/services/security/src/security.openapi.ts
@@ -793,7 +793,7 @@
     'only a hash. Caller must persist the plaintext immediately.',
   security: [{ bearerAuth: [] }],
   request: {
-    body: { content: { 'application/json': { schema: ApiKeyCreateRequestSchema } } },
+    body: { content: { 'application/json': { schema: ApiKeyCreateRequestSchema } }, required: true },
   },
   responses: {
     201: {
@@ -892,7 +892,7 @@
   security: [{ bearerAuth: [] }],
   request: {
     params: z.object({ userId: z.string().uuid() }),
-    body: { content: { 'application/json': { schema: AdminScopePutRequestSchema } } },
+    body: { content: { 'application/json': { schema: AdminScopePutRequestSchema } }, required: true },
   },
   responses: {
     200: { description: 'Scope replaced', content: { 'application/json': { schema: AdminScopeResponseSchema } } },
--- /dev/null
+++ b/Blockchain/Dev/services/security/src/__tests__/ks1705-security-keys-post-and-admin-scopes-put-bodies-are-required.test.ts
@@ -0,0 +1,55 @@
+// KS-1705 (the KS-1364 class): the published contract for POST /api/security/keys and PUT
+// /api/security/keys/admin-scopes/{userId} did not mark the request body required, although each body's schema has a
+// non-empty `required` list (ApiKeyCreateRequest: name; AdminScopePutRequest: tenantId, organizationIds) and each
+// handler parses the body with a schema that refuses an absent one (an absent body arrives as {}): index.ts
+// createApiKeySchema.parse and adminScopePutSchema.parse, both answered with a 400. A spec-driven caller such as
+// Schemathesis may therefore send no body and read that 400 as a defect. This file renders the document the generator
+// publishes, from the shared registry the security module populates on import. No server, no database, no network.
+import { describe, it, expect } from 'vitest';
+import { generateOpenApiDocument } from '@secuura/shared';
+import '../security.openapi';
+
+type AnyObj = Record<string, any>;
+
+const doc = generateOpenApiDocument({ title: 'security (ks1705 pin)', version: '0.0.0' }) as AnyObj;
+
+function operation(path: string, method: string): AnyObj | undefined {
+  return doc.paths?.[path]?.[method];
+}
+
+const KEYS = '/api/security/keys';
+const SCOPES = '/api/security/keys/admin-scopes/{userId}';
+
+describe('KS-1705: POST /api/security/keys and PUT /api/security/keys/admin-scopes/{userId} publish a REQUIRED request body', () => {
+  it('RED KS-1705 SK1: POST /api/security/keys marks its request body required', () => {
+    expect(operation(KEYS, 'post')?.requestBody?.required).toBe(true);
+  });
+
+  it('RED KS-1705 SK2: PUT /api/security/keys/admin-scopes/{userId} marks its request body required', () => {
+    expect(operation(SCOPES, 'put')?.requestBody?.required).toBe(true);
+  });
+
+  it('control KS-1705 SKC1: both bodies keep their request schemas and both operations keep bearerAuth', () => {
+    expect(operation(KEYS, 'post')?.requestBody?.content?.['application/json']?.schema?.$ref).toBe(
+      '#/components/schemas/ApiKeyCreateRequest',
+    );
+    expect(operation(SCOPES, 'put')?.requestBody?.content?.['application/json']?.schema?.$ref).toBe(
+      '#/components/schemas/AdminScopePutRequest',
+    );
+    expect(operation(KEYS, 'post')?.security).toEqual([{ bearerAuth: [] }]);
+    expect(operation(SCOPES, 'put')?.security).toEqual([{ bearerAuth: [] }]);
+  });
+
+  it('control KS-1705 SKC2: the two request components still carry their required lists and POST /keys still publishes its fields', () => {
+    const create = doc.components?.schemas?.ApiKeyCreateRequest;
+    const scope = doc.components?.schemas?.AdminScopePutRequest;
+    expect(create?.required ?? []).toEqual(['name']);
+    expect(Object.keys(create?.properties ?? {})).toEqual(expect.arrayContaining(['name', 'organizationId', 'scopes']));
+    expect([...(scope?.required ?? [])].sort()).toEqual(['organizationIds', 'tenantId']);
+  });
+
+  it('control KS-1705 SKC3: the bodiless siblings stay bodiless (GET admin-scopes, DELETE keys/{id})', () => {
+    expect(operation(SCOPES, 'get')?.requestBody).toBeUndefined();
+    expect(operation(`${KEYS}/{id}`, 'delete')?.requestBody).toBeUndefined();
+  });
+});
```
