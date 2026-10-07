# READY — KS-591-PLATFORMTENANTSCREATESTA-1 (spark-dsv4flash, briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-591-platform-tenants-create-status/out.md.checker/patch.diff`** (from `ls` at 03:25 2026-10-08; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-591-platform-tenants-create-status/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-591-platform-tenants-create-status/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden not located — no identity claim is made.

**Held 03:25 2026-10-08 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-591-platform-tenants-create-status/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `3ce8cd4026a6e3241413e9c7533d5a84d10c1c79`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/tenant-provisioning/src/tenant-provisioning.openapi.ts , Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks591-platform-tenants-create-status-body-required.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/tenant-provisioning/src/tenant-provisioning.openapi.ts` (product) and `Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks591-platform-tenants-create-status-body-required.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
2	0	Blockchain/Dev/services/tenant-provisioning/src/tenant-provisioning.openapi.ts
55	0	Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks591-platform-tenants-create-status-body-required.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (2 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 2 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 0.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/tenant-provisioning/src/tenant-provisioning.openapi.ts byte-exact incl. leading whitespace (apply mode strict): OK 2 line(s) byte-exact incl. leading whitespace (of 2; 2 line(s) added by the apply)` [a3i_indent.out: `OK 2 line(s) byte-exact incl. leading whitespace (of 2; 2 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/tenant-provisioning/src/tenant-provisioning.openapi.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks591-platform-tenants-create-status-body-required.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks591-platform-tenants-create-status-body-required.test.ts fails at the untouched tip (2 failed / 5 run; controls green; assertion reds)` [red_first.json: failed=2 of total=5; red cell(s): ['KS-591: POST /api/platform/tenants and PATCH /api/platform/tenants/{id}/status publish a REQUIRED request body RED KS-591 TN1: POST /api/platform/tenants marks its request body required', 'KS-591: POST /api/platform/tenants and PATCH /api/platform/tenants/{id}/status publish a REQUIRED request body RED KS-591 TN2: PATCH /api/platform/tenants/{id}/status marks its request body required']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks591-platform-tenants-create-status-body-required.test.ts passes with the product hunk (5 passed / 5 run)` [green_after.json: failed=0 of total=5, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=17 failed=0 | after: total=22 failed=0` · `NEW reds: []` [baseline_suite.json total=17 failed=0; after_suite.json total=22 failed=0]
- A6 [verbatim]: `PASS A6 whole services/tenant-provisioning suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/tenant-provisioning: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +57/-0 test=src/__tests__/ks591-platform-tenants-create-status-body-required.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/tenant-provisioning/src/tenant-provisioning.openapi.ts` (+2/-0 per numstat.out) and the test file `Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks591-platform-tenants-create-status-body-required.test.ts` (+55/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `3ce8cd4026a6e3241413e9c7533d5a84d10c1c79` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-591-platform-tenants-create-status/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-591-platform-tenants-create-status/checker.out`.

```diff
--- a/Blockchain/Dev/services/tenant-provisioning/src/tenant-provisioning.openapi.ts
+++ b/Blockchain/Dev/services/tenant-provisioning/src/tenant-provisioning.openapi.ts
@@ -360,6 +360,7 @@
       content: {
         'application/json': { schema: TenantCreateRequestSchema },
       },
+      required: true,
     },
   },
   responses: {
@@ -484,6 +485,7 @@
       content: {
         'application/json': { schema: TenantStatusUpdateRequestSchema },
       },
+      required: true,
     },
   },
   responses: {
--- /dev/null
+++ b/Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks591-platform-tenants-create-status-body-required.test.ts
@@ -0,0 +1,55 @@
+// KS-591 (positive_data_acceptance register): the published contracts for POST /api/platform/tenants and
+// PATCH /api/platform/tenants/{id}/status did not mark the request body required, so a spec-driven caller
+// (Schemathesis) sent no body at all and each handler (index.ts) answered 400: create parses the body with
+// createTenantSchema (name and slug required), status refuses anything but active / suspended / archived. An absent
+// body arrives as {} and is refused, so the spec now says the body is required - the KS-1364 shape its sibling
+// PATCH /api/platform/tenants/{id} already has. This file renders the document the generator publishes, from the
+// shared registry the tenant-provisioning module populates on import. No server, no database, no network.
+import { describe, it, expect } from 'vitest';
+import { generateOpenApiDocument } from '@secuura/shared';
+import '../tenant-provisioning.openapi';
+
+type AnyObj = Record<string, any>;
+
+const doc = generateOpenApiDocument({ title: 'tenant-provisioning (ks591 create/status pin)', version: '0.0.0' }) as AnyObj;
+
+function operation(path: string, method: string): AnyObj | undefined {
+  return doc.paths?.[path]?.[method];
+}
+
+function bodyRef(path: string, method: string): string | undefined {
+  return operation(path, method)?.requestBody?.content?.['application/json']?.schema?.$ref;
+}
+
+describe('KS-591: POST /api/platform/tenants and PATCH /api/platform/tenants/{id}/status publish a REQUIRED request body', () => {
+  it('RED KS-591 TN1: POST /api/platform/tenants marks its request body required', () => {
+    expect(operation('/api/platform/tenants', 'post')?.requestBody?.required).toBe(true);
+  });
+
+  it('RED KS-591 TN2: PATCH /api/platform/tenants/{id}/status marks its request body required', () => {
+    expect(operation('/api/platform/tenants/{id}/status', 'patch')?.requestBody?.required).toBe(true);
+  });
+
+  it('control KS-591 TNC1: both bodies keep their request schemas and both operations keep bearerAuth', () => {
+    expect({
+      create: bodyRef('/api/platform/tenants', 'post'),
+      status: bodyRef('/api/platform/tenants/{id}/status', 'patch'),
+    }).toEqual({
+      create: '#/components/schemas/TenantCreateRequest',
+      status: '#/components/schemas/TenantStatusUpdateRequest',
+    });
+    expect(operation('/api/platform/tenants', 'post')?.security).toEqual([{ bearerAuth: [] }]);
+    expect(operation('/api/platform/tenants/{id}/status', 'patch')?.security).toEqual([{ bearerAuth: [] }]);
+  });
+
+  it('control KS-591 TNC2: the request components still list required fields, which is why an absent body is refused', () => {
+    const s: AnyObj = doc.components?.schemas ?? {};
+    expect(s.TenantCreateRequest?.required).toEqual(expect.arrayContaining(['name', 'slug']));
+    expect(s.TenantStatusUpdateRequest?.required).toEqual(['status']);
+  });
+
+  it('control KS-591 TNC3: the KS-1364 sibling PATCH /api/platform/tenants/{id} keeps its required body, and DELETE keeps an optional one', () => {
+    expect(operation('/api/platform/tenants/{id}', 'patch')?.requestBody?.required).toBe(true);
+    expect(operation('/api/platform/tenants/{id}', 'delete')?.requestBody?.required).toBeUndefined();
+  });
+});
```

**Appended by Wednesday 03:25 2026-10-08 (not written by hold_ready):** REVIEWED HOLD on 2026-10-05 (`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-591-platform-tenants-create-status/REVIEW.md`) but never held until now; classed UNRAISED by `0_Brain/reference/2026-10-08_spark-hold-census/CENSUS.md` (forward strict apply at develop eae08a3f441c, reverse refuses, no open PR). Read the REVIEW body for any raise caveat (the census read only its verdict line). Any YAML companion is in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-591-platform-tenants-create-status/`. Raise is blocked until develop is green on pre-push leg 14 (pickup 03:1x).
