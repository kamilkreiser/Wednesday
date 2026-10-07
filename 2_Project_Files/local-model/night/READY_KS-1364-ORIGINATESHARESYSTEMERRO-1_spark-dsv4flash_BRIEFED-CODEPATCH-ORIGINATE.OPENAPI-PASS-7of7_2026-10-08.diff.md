# READY — KS-1364-ORIGINATESHARESYSTEMERRO-1 (spark-dsv4flash, briefed, code_patch, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-1364-originate-share-system-errors/out.md.checker/patch.diff`** (from `ls` at 03:25 2026-10-08; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-1364-originate-share-system-errors/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-1364-originate-share-system-errors/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden not located — no identity claim is made.

**Held 03:25 2026-10-08 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-1364-originate-share-system-errors/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `46c3e20cfbd21acee0c67d544180c33deaa4c8ef`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/originate/src/originate.openapi.ts , Blockchain/Dev/services/originate/src/__tests__/ks1364-share-system-errors-body-required.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/originate.openapi.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1364-share-system-errors-body-required.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
3	0	Blockchain/Dev/services/originate/src/originate.openapi.ts
64	0	Blockchain/Dev/services/originate/src/__tests__/ks1364-share-system-errors-body-required.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (3 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 3 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 0.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/originate/src/originate.openapi.ts byte-exact incl. leading whitespace (apply mode strict): OK 3 line(s) byte-exact incl. leading whitespace (of 3; 3 line(s) added by the apply)` [a3i_indent.out: `OK 3 line(s) byte-exact incl. leading whitespace (of 3; 3 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/originate.openapi.ts` (hunks=3, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1364-share-system-errors-body-required.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1364-share-system-errors-body-required.test.ts fails at the untouched tip (3 failed / 6 run; controls green; assertion reds)` [red_first.json: failed=3 of total=6; red cell(s): ['KS-1364: three originate POSTs publish a REQUIRED request body RED KS-1364 OB1: POST /api/documents/{id}/share marks its request body required', 'KS-1364: three originate POSTs publish a REQUIRED request body RED KS-1364 OB2: POST /api/system-errors/ingest marks its request body required', 'KS-1364: three originate POSTs publish a REQUIRED request body RED KS-1364 OB3: POST /api/system-errors/resolve-by-service marks its request body required']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1364-share-system-errors-body-required.test.ts passes with the product hunk (6 passed / 6 run)` [green_after.json: failed=0 of total=6, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1062 failed=0 | after: total=1068 failed=0` · `NEW reds: []` [baseline_suite.json total=1062 failed=0; after_suite.json total=1068 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +67/-0 test=src/__tests__/ks1364-share-system-errors-body-required.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/originate.openapi.ts` (+3/-0 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1364-share-system-errors-body-required.test.ts` (+64/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `46c3e20cfbd21acee0c67d544180c33deaa4c8ef` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-1364-originate-share-system-errors/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-1364-originate-share-system-errors/checker.out`.

```diff
--- a/Blockchain/Dev/services/originate/src/originate.openapi.ts
+++ b/Blockchain/Dev/services/originate/src/originate.openapi.ts
@@ -1601,6 +1601,7 @@
   request: {
     params: documentIdPathParams,
     body: {
+      required: true,
       content: { 'application/json': { schema: DocumentShareRequestSchema } },
     },
   },
@@ -3763,6 +3764,7 @@
     'it here for centralised tracking + admin dashboarding.',
   request: {
     body: {
+      required: true,
       content: {
         'application/json': { schema: SystemErrorIngestRequestSchema },
       },
@@ -3911,6 +3913,7 @@
   security: [{ bearerAuth: [] }],
   request: {
     body: {
+      required: true,
       content: {
         'application/json': { schema: SystemErrorResolveByServiceRequestSchema },
       },
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1364-share-system-errors-body-required.test.ts
@@ -0,0 +1,64 @@
+// KS-1364 (85 request bodies not marked required): the published contracts for POST /api/documents/{id}/share,
+// POST /api/system-errors/ingest and POST /api/system-errors/resolve-by-service did not mark the request body
+// required, so a spec-driven caller (Schemathesis) may send no body at all. Each handler refuses an absent body
+// (it arrives as {}) with 400: share's express-validator chain requires a non-empty recipients array
+// (routes/documents.ts), ingest requires service and message and resolve-by-service requires service
+// (routes/systemErrors.ts zod objects). The spec now says each body is required. POST /api/system-errors/client-errors
+// declares every field optional and its handler accepts {}, so its body stays OPTIONAL. This file renders the
+// document the generator publishes, from the shared registry the originate module populates on import. No server,
+// no database, no network.
+import { generateOpenApiDocument } from '@secuura/shared';
+import '../originate.openapi';
+
+type AnyObj = Record<string, any>;
+
+const doc = generateOpenApiDocument({ title: 'originate (ks1364 share/system-errors pin)', version: '0.0.0' }) as AnyObj;
+
+const SHARE = '/api/documents/{id}/share';
+const INGEST = '/api/system-errors/ingest';
+const RESOLVE = '/api/system-errors/resolve-by-service';
+
+function operation(path: string, method: string): AnyObj | undefined {
+  return doc.paths?.[path]?.[method];
+}
+
+function bodyRef(path: string): string | undefined {
+  return operation(path, 'post')?.requestBody?.content?.['application/json']?.schema?.$ref;
+}
+
+describe('KS-1364: three originate POSTs publish a REQUIRED request body', () => {
+  it('RED KS-1364 OB1: POST /api/documents/{id}/share marks its request body required', () => {
+    expect(operation(SHARE, 'post')?.requestBody?.required).toBe(true);
+  });
+
+  it('RED KS-1364 OB2: POST /api/system-errors/ingest marks its request body required', () => {
+    expect(operation(INGEST, 'post')?.requestBody?.required).toBe(true);
+  });
+
+  it('RED KS-1364 OB3: POST /api/system-errors/resolve-by-service marks its request body required', () => {
+    expect(operation(RESOLVE, 'post')?.requestBody?.required).toBe(true);
+  });
+
+  it('control KS-1364 OBC1: the three bodies keep their request schemas and their bearerAuth', () => {
+    expect({ share: bodyRef(SHARE), ingest: bodyRef(INGEST), resolve: bodyRef(RESOLVE) }).toEqual({
+      share: '#/components/schemas/DocumentShareRequest',
+      ingest: '#/components/schemas/SystemErrorIngestRequest',
+      resolve: '#/components/schemas/SystemErrorResolveByServiceRequest',
+    });
+    for (const p of [SHARE, INGEST, RESOLVE]) {
+      expect(operation(p, 'post')?.security).toEqual([{ bearerAuth: [] }]);
+    }
+  });
+
+  it('control KS-1364 OBC2: the request components still list their required fields', () => {
+    const s: AnyObj = doc.components?.schemas ?? {};
+    expect(s.DocumentShareRequest?.required).toEqual(expect.arrayContaining(['recipients']));
+    expect(s.SystemErrorIngestRequest?.required).toEqual(expect.arrayContaining(['service', 'message']));
+    expect(s.SystemErrorResolveByServiceRequest?.required).toEqual(['service']);
+  });
+
+  it('control KS-1364 OBC3: client-errors (every field optional, {} accepted) keeps an OPTIONAL body, and the landed v2 verify carve keeps its required one', () => {
+    expect(operation('/api/system-errors/client-errors', 'post')?.requestBody?.required).toBeUndefined();
+    expect(operation('/api/v2/verification/verify', 'post')?.requestBody?.required).toBe(true);
+  });
+});
```

**Appended by Wednesday 03:25 2026-10-08 (not written by hold_ready):** REVIEWED HOLD on 2026-10-05 (`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-1364-originate-share-system-errors/REVIEW.md`) but never held until now; classed UNRAISED by `0_Brain/reference/2026-10-08_spark-hold-census/CENSUS.md` (forward strict apply at develop eae08a3f441c, reverse refuses, no open PR). Read the REVIEW body for any raise caveat (the census read only its verdict line). Any YAML companion is in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1364-originate-share-system-errors/`. Raise is blocked until develop is green on pre-push leg 14 (pickup 03:1x).
