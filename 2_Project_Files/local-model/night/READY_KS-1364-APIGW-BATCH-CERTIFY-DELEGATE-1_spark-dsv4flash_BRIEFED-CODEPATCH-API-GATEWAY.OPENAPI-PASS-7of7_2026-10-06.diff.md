# READY — KS-1364-APIGW-BATCH-CERTIFY-DELEGATE-1 (spark-dsv4flash, briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-06_KS-1364-apigw-batch-certify-delegate/out.md.checker/patch.diff`** (from `ls` at 10:48 2026-10-06; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-06_KS-1364-apigw-batch-certify-delegate/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-06_KS-1364-apigw-batch-certify-delegate/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden not located — no identity claim is made.

**Held 10:48 2026-10-06 by Spark review agent after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-06_KS-1364-apigw-batch-certify-delegate/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `3f9ff4e1e1b93e2e704918a7825f13a72c9ec76f`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/api-gateway/src/api-gateway.openapi.ts , Blockchain/Dev/services/api-gateway/src/__tests__/ks1364-batch-certifications-delegations-body-required.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/api-gateway/src/api-gateway.openapi.ts` (product) and `Blockchain/Dev/services/api-gateway/src/__tests__/ks1364-batch-certifications-delegations-body-required.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
2	0	Blockchain/Dev/services/api-gateway/src/api-gateway.openapi.ts
51	0	Blockchain/Dev/services/api-gateway/src/__tests__/ks1364-batch-certifications-delegations-body-required.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (2 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 2 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 0.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/api-gateway/src/api-gateway.openapi.ts byte-exact incl. leading whitespace (apply mode strict): OK 2 line(s) byte-exact incl. leading whitespace (of 2; 2 line(s) added by the apply)` [a3i_indent.out: `OK 2 line(s) byte-exact incl. leading whitespace (of 2; 2 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/api-gateway/src/api-gateway.openapi.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/api-gateway/src/__tests__/ks1364-batch-certifications-delegations-body-required.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1364-batch-certifications-delegations-body-required.test.ts fails at the untouched tip (2 failed / 5 run; controls green; assertion reds)` [red_first.json: failed=2 of total=5; red cell(s): ['KS-1364: POST /api/batch/certifications and /api/batch/delegations publish a REQUIRED request body RED KS-1364 BA1: POST /api/batch/certifications marks its request body required', 'KS-1364: POST /api/batch/certifications and /api/batch/delegations publish a REQUIRED request body RED KS-1364 BA2: POST /api/batch/delegations marks its request body required']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1364-batch-certifications-delegations-body-required.test.ts passes with the product hunk (5 passed / 5 run)` [green_after.json: failed=0 of total=5, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=812 failed=0 | after: total=817 failed=0` · `NEW reds: []` [baseline_suite.json total=812 failed=0; after_suite.json total=817 failed=0]
- A6 [verbatim]: `PASS A6 whole services/api-gateway suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/api-gateway: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +53/-0 test=src/__tests__/ks1364-batch-certifications-delegations-body-required.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/api-gateway/src/api-gateway.openapi.ts` (+2/-0 per numstat.out) and the test file `Blockchain/Dev/services/api-gateway/src/__tests__/ks1364-batch-certifications-delegations-body-required.test.ts` (+51/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `3f9ff4e1e1b93e2e704918a7825f13a72c9ec76f` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-06_KS-1364-apigw-batch-certify-delegate/input.json`. Brief (given by --brief; its `# ` heading names KS-1364): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1364-apigw-batch-certify-delegate/KS-1364.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-06_KS-1364-apigw-batch-certify-delegate/checker.out`.

```diff
--- a/Blockchain/Dev/services/api-gateway/src/api-gateway.openapi.ts
+++ b/Blockchain/Dev/services/api-gateway/src/api-gateway.openapi.ts
@@ -350,6 +350,7 @@
   security: [{ bearerAuth: [] }],
   request: {
     body: {
+      required: true,
       content: {
         'application/json': { schema: BatchCertifyRequestSchema },
       },
@@ -404,6 +405,7 @@
   security: [{ bearerAuth: [] }],
   request: {
     body: {
+      required: true,
       content: {
         'application/json': { schema: BatchDelegationsRequestSchema },
       },
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1364-batch-certifications-delegations-body-required.test.ts
@@ -0,0 +1,51 @@
+// KS-1364 (85 request bodies not marked required): the published contract for POST /api/batch/certifications and
+// POST /api/batch/delegations did not mark the request body required, although each body's schema has a non-empty
+// `required` list (BatchCertifyRequest: documentIds; BatchDelegationsRequest: documentIds, delegateUserId) - the
+// ticket's spec-lint rule. The handlers (routes/batch.ts validateBatchCertify / validateBatchDelegate) answer 400
+// for an absent or empty body. POST /api/batch/verify is the control: every field of its schema is optional, so
+// its body stays optional here. This file renders the document the generator publishes, from the shared registry
+// the gateway module populates on import. No server, no database, no network.
+import { describe, it, expect } from 'vitest';
+import { generateOpenApiDocument } from '@secuura/shared';
+import '../api-gateway.openapi';
+
+type AnyObj = Record<string, any>;
+
+const doc = generateOpenApiDocument({ title: 'api-gateway (ks1364 batch pin)', version: '0.0.0' }) as AnyObj;
+
+function operation(path: string, method: string): AnyObj | undefined {
+  return doc.paths?.[path]?.[method];
+}
+
+describe('KS-1364: POST /api/batch/certifications and /api/batch/delegations publish a REQUIRED request body', () => {
+  it('RED KS-1364 BA1: POST /api/batch/certifications marks its request body required', () => {
+    expect(operation('/api/batch/certifications', 'post')?.requestBody?.required).toBe(true);
+  });
+
+  it('RED KS-1364 BA2: POST /api/batch/delegations marks its request body required', () => {
+    expect(operation('/api/batch/delegations', 'post')?.requestBody?.required).toBe(true);
+  });
+
+  it('control KS-1364 BAC1: both bodies keep their request schemas and both operations keep bearerAuth', () => {
+    expect(operation('/api/batch/certifications', 'post')?.requestBody?.content?.['application/json']?.schema?.$ref).toBe(
+      '#/components/schemas/BatchCertifyRequest',
+    );
+    expect(operation('/api/batch/delegations', 'post')?.requestBody?.content?.['application/json']?.schema?.$ref).toBe(
+      '#/components/schemas/BatchDelegationsRequest',
+    );
+    expect(operation('/api/batch/certifications', 'post')?.security).toEqual([{ bearerAuth: [] }]);
+    expect(operation('/api/batch/delegations', 'post')?.security).toEqual([{ bearerAuth: [] }]);
+  });
+
+  it('control KS-1364 BAC2: the two request components still carry their required lists', () => {
+    const certify = doc.components?.schemas?.BatchCertifyRequest?.required ?? [];
+    const delegate = doc.components?.schemas?.BatchDelegationsRequest?.required ?? [];
+    expect([...certify].sort()).toEqual(['documentIds']);
+    expect([...delegate].sort()).toEqual(['delegateUserId', 'documentIds']);
+  });
+
+  it('control KS-1364 BAC3: POST /api/batch/verify (every field optional) keeps an OPTIONAL body', () => {
+    expect(operation('/api/batch/verify', 'post')?.requestBody?.required).toBeUndefined();
+    expect(doc.components?.schemas?.BatchVerifyRequest?.required ?? []).toEqual([]);
+  });
+});
```
