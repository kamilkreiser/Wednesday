# READY — KS-1364-M365-1 (spark-dsv4flash, briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-01_KS-1364-m365/out.md.checker/patch.diff`** (from `ls` at 10:27 2026-10-01; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-01_KS-1364-m365/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-01_KS-1364-m365/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-01_KS-1364-m365/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1364-m365/precheck/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 10:27 2026-10-01 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-01_KS-1364-m365/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `723dc0722b68482a03de8577fdb5eb5b3359e725`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/m365-integration/src/m365-integration.openapi.ts , Blockchain/Dev/services/m365-integration/src/__tests__/ks1364-m365-sites-sync-verifyhash-body-required.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/m365-integration/src/m365-integration.openapi.ts` (product) and `Blockchain/Dev/services/m365-integration/src/__tests__/ks1364-m365-sites-sync-verifyhash-body-required.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
3	3	Blockchain/Dev/services/m365-integration/src/m365-integration.openapi.ts
58	0	Blockchain/Dev/services/m365-integration/src/__tests__/ks1364-m365-sites-sync-verifyhash-body-required.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (3 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 3 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 3.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/m365-integration/src/m365-integration.openapi.ts byte-exact incl. leading whitespace (apply mode strict): OK 3 line(s) byte-exact incl. leading whitespace (of 3; 3 line(s) added by the apply)` [a3i_indent.out: `OK 3 line(s) byte-exact incl. leading whitespace (of 3; 3 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/m365-integration/src/m365-integration.openapi.ts` (hunks=3, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/m365-integration/src/__tests__/ks1364-m365-sites-sync-verifyhash-body-required.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1364-m365-sites-sync-verifyhash-body-required.test.ts fails at the untouched tip (3 failed / 6 run; controls green; assertion reds)` [red_first.json: failed=3 of total=6; red cell(s): ['KS-1364: three m365 POSTs publish a REQUIRED request body RED KS-1364 MS1: POST /api/m365/sites marks its request body required', 'KS-1364: three m365 POSTs publish a REQUIRED request body RED KS-1364 MS2: POST /api/m365/documents/sync marks its request body required', 'KS-1364: three m365 POSTs publish a REQUIRED request body RED KS-1364 MS3: POST /api/m365/outlook/verify-hash marks its request body required']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1364-m365-sites-sync-verifyhash-body-required.test.ts passes with the product hunk (6 passed / 6 run)` [green_after.json: failed=0 of total=6, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=47 failed=0 | after: total=53 failed=0` · `NEW reds: []` [baseline_suite.json total=47 failed=0; after_suite.json total=53 failed=0]
- A6 [verbatim]: `PASS A6 whole services/m365-integration suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/m365-integration: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +61/-3 test=src/__tests__/ks1364-m365-sites-sync-verifyhash-body-required.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/m365-integration/src/m365-integration.openapi.ts` (+3/-3 per numstat.out) and the test file `Blockchain/Dev/services/m365-integration/src/__tests__/ks1364-m365-sites-sync-verifyhash-body-required.test.ts` (+58/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `723dc0722b68482a03de8577fdb5eb5b3359e725` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-01_KS-1364-m365/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-01_KS-1364-m365/checker.out`.

```diff
--- a/Blockchain/Dev/services/m365-integration/src/m365-integration.openapi.ts
+++ b/Blockchain/Dev/services/m365-integration/src/m365-integration.openapi.ts
@@ -598,7 +598,7 @@
   summary: 'Add a SharePoint site to a connection',
   security: [{ bearerAuth: [] }],
   request: {
-    body: { content: { 'application/json': { schema: M365AddSiteRequestSchema } } },
+    body: { content: { 'application/json': { schema: M365AddSiteRequestSchema } }, required: true },
   },
   responses: {
     201: {
@@ -703,7 +703,7 @@
   summary: 'Sync a SharePoint drive item into the platform',
   security: [{ bearerAuth: [] }],
   request: {
-    body: { content: { 'application/json': { schema: M365SyncDocumentRequestSchema } } },
+    body: { content: { 'application/json': { schema: M365SyncDocumentRequestSchema } }, required: true },
   },
   responses: {
     200: {
@@ -1016,7 +1016,7 @@
   tags: ['M365', 'Outlook'],
   summary: 'Verify a content hash via the Outlook add-in',
   request: {
-    body: { content: { 'application/json': { schema: M365VerifyHashRequestSchema } } },
+    body: { content: { 'application/json': { schema: M365VerifyHashRequestSchema } }, required: true },
   },
   responses: {
     200: {
--- /dev/null
+++ b/Blockchain/Dev/services/m365-integration/src/__tests__/ks1364-m365-sites-sync-verifyhash-body-required.test.ts
@@ -0,0 +1,58 @@
+// KS-1364 (sweep 4): the published contracts for POST /api/m365/sites, POST /api/m365/documents/sync and
+// POST /api/m365/outlook/verify-hash did not mark the request body required, so a spec-driven caller
+// (Schemathesis) sent no body at all and all three handlers answered 400 (index.ts: addSiteSchema.parse,
+// syncDocumentSchema.parse, and an inline zod object for verify-hash). Each rejects an absent body, so the spec now
+// says the body is required. verify-hash stays public (KS-442). This file renders the document the generator
+// publishes, from the shared registry the m365-integration module populates on import. No server, no database,
+// no network.
+import { describe, it, expect } from 'vitest';
+import { generateOpenApiDocument } from '@secuura/shared';
+import '../m365-integration.openapi';
+
+type AnyObj = Record<string, any>;
+
+const doc = generateOpenApiDocument({ title: 'm365-integration (ks1364 pin)', version: '0.0.0' }) as AnyObj;
+
+function operation(path: string, method: string): AnyObj | undefined {
+  return doc.paths?.[path]?.[method];
+}
+
+function bodyRef(path: string): string | undefined {
+  return operation(path, 'post')?.requestBody?.content?.['application/json']?.schema?.$ref;
+}
+
+describe('KS-1364: three m365 POSTs publish a REQUIRED request body', () => {
+  it('RED KS-1364 MS1: POST /api/m365/sites marks its request body required', () => {
+    expect(operation('/api/m365/sites', 'post')?.requestBody?.required).toBe(true);
+  });
+
+  it('RED KS-1364 MS2: POST /api/m365/documents/sync marks its request body required', () => {
+    expect(operation('/api/m365/documents/sync', 'post')?.requestBody?.required).toBe(true);
+  });
+
+  it('RED KS-1364 MS3: POST /api/m365/outlook/verify-hash marks its request body required', () => {
+    expect(operation('/api/m365/outlook/verify-hash', 'post')?.requestBody?.required).toBe(true);
+  });
+
+  it('control KS-1364 MC1: the three bodies keep their request schemas', () => {
+    expect({
+      sites: bodyRef('/api/m365/sites'),
+      sync: bodyRef('/api/m365/documents/sync'),
+      hash: bodyRef('/api/m365/outlook/verify-hash'),
+    }).toEqual({
+      sites: '#/components/schemas/M365AddSiteRequest',
+      sync: '#/components/schemas/M365SyncDocumentRequest',
+      hash: '#/components/schemas/M365VerifyHashRequest',
+    });
+  });
+
+  it('control KS-1364 MC2: sites and sync keep bearerAuth, and verify-hash stays public', () => {
+    expect(operation('/api/m365/sites', 'post')?.security).toEqual([{ bearerAuth: [] }]);
+    expect(operation('/api/m365/documents/sync', 'post')?.security).toEqual([{ bearerAuth: [] }]);
+    expect(operation('/api/m365/outlook/verify-hash', 'post')?.security).toEqual([]);
+  });
+
+  it('control KS-1364 MC3: the sibling POST /api/teams/notify keeps its request body schema', () => {
+    expect(bodyRef('/api/teams/notify')).toBe('#/components/schemas/M365TeamsNotifyRequest');
+  });
+});
```

> (Added BY HAND 10:28 2026-10-01 by the brief-writer sub-agent.) **Raise-seat step the model does not do:** the PR also needs the regenerated `Blockchain/Dev/docs/openapi/secuura-api.yaml` — apply `night/briefs/KS-1364-m365/KS-1364.openapi-yaml.companion.diff` (or run `npm run generate-openapi` and confirm), then `npm run check:openapi` (measured: model files alone -> `generate-openapi --check` rc 1; + companion -> `check:openapi` rc 0). **Scope: refs KS-1364, does NOT close it** (this READY: 3 of 17; the six KS-1364 READYs together: 11 of 17). All six READYs' product sections + companions apply strictly in sequence on one tree (measured) — they go up as ONE PR.
