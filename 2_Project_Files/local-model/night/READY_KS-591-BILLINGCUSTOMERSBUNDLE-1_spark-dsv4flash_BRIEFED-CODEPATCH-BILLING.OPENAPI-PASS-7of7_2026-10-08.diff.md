# READY — KS-591-BILLINGCUSTOMERSBUNDLE-1 (spark-dsv4flash, briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-591-billing-customers-bundle/out.md.checker/patch.diff`** (from `ls` at 03:25 2026-10-08; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-591-billing-customers-bundle/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-591-billing-customers-bundle/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden not located — no identity claim is made.

**Held 03:25 2026-10-08 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-591-billing-customers-bundle/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `3ce8cd4026a6e3241413e9c7533d5a84d10c1c79`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/billing/src/billing.openapi.ts , Blockchain/Dev/services/billing/src/__tests__/ks591-billing-customers-bundle-body-required.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/billing/src/billing.openapi.ts` (product) and `Blockchain/Dev/services/billing/src/__tests__/ks591-billing-customers-bundle-body-required.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
2	0	Blockchain/Dev/services/billing/src/billing.openapi.ts
60	0	Blockchain/Dev/services/billing/src/__tests__/ks591-billing-customers-bundle-body-required.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (2 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 2 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 0.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/billing/src/billing.openapi.ts byte-exact incl. leading whitespace (apply mode strict): OK 2 line(s) byte-exact incl. leading whitespace (of 2; 2 line(s) added by the apply)` [a3i_indent.out: `OK 2 line(s) byte-exact incl. leading whitespace (of 2; 2 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/billing/src/billing.openapi.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/billing/src/__tests__/ks591-billing-customers-bundle-body-required.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks591-billing-customers-bundle-body-required.test.ts fails at the untouched tip (2 failed / 6 run; controls green; assertion reds)` [red_first.json: failed=2 of total=6; red cell(s): ['KS-591: POST /api/billing/customers and POST /api/billing/checkout/bundle publish a REQUIRED request body RED KS-591 BC1: POST /api/billing/customers marks its request body required', 'KS-591: POST /api/billing/customers and POST /api/billing/checkout/bundle publish a REQUIRED request body RED KS-591 BC2: POST /api/billing/checkout/bundle marks its request body required']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks591-billing-customers-bundle-body-required.test.ts passes with the product hunk (6 passed / 6 run)` [green_after.json: failed=0 of total=6, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=98 failed=0 | after: total=104 failed=0` · `NEW reds: []` [baseline_suite.json total=98 failed=0; after_suite.json total=104 failed=0]
- A6 [verbatim]: `PASS A6 whole services/billing suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/billing: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +62/-0 test=src/__tests__/ks591-billing-customers-bundle-body-required.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/billing/src/billing.openapi.ts` (+2/-0 per numstat.out) and the test file `Blockchain/Dev/services/billing/src/__tests__/ks591-billing-customers-bundle-body-required.test.ts` (+60/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `3ce8cd4026a6e3241413e9c7533d5a84d10c1c79` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-591-billing-customers-bundle/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-591-billing-customers-bundle/checker.out`.

```diff
--- a/Blockchain/Dev/services/billing/src/billing.openapi.ts
+++ b/Blockchain/Dev/services/billing/src/billing.openapi.ts
@@ -579,6 +579,7 @@
   request: {
     body: {
       content: { 'application/json': { schema: CustomerCreateRequestSchema } },
+      required: true,
     },
   },
   responses: {
@@ -711,6 +712,7 @@
   request: {
     body: {
       content: { 'application/json': { schema: CheckoutBundleRequestSchema } },
+      required: true,
     },
   },
   responses: {
--- /dev/null
+++ b/Blockchain/Dev/services/billing/src/__tests__/ks591-billing-customers-bundle-body-required.test.ts
@@ -0,0 +1,60 @@
+// KS-591 (positive_data_acceptance register): the published contracts for POST /api/billing/customers and
+// POST /api/billing/checkout/bundle did not mark the request body required, so a spec-driven caller (Schemathesis)
+// sent no body at all and each handler (routes/billing.ts, CreateCustomerSchema / PurchaseBundleSchema via .parse)
+// answered 400. Those zod objects reject an absent body, so the spec now says the body is required - the KS-1364
+// shape. PUT /api/billing/customers/{id} is the control: its handler accepts an empty body, so its body stays
+// optional. This file renders the document the generator publishes, from the shared registry the billing module
+// populates on import. No server, no database, no network.
+import { describe, it, expect } from 'vitest';
+import { generateOpenApiDocument } from '@secuura/shared';
+import '../billing.openapi';
+
+type AnyObj = Record<string, any>;
+
+const doc = generateOpenApiDocument({ title: 'billing (ks591 customers/bundle pin)', version: '0.0.0' }) as AnyObj;
+
+function operation(path: string, method: string): AnyObj | undefined {
+  return doc.paths?.[path]?.[method];
+}
+
+function bodyRef(path: string, method: string): string | undefined {
+  return operation(path, method)?.requestBody?.content?.['application/json']?.schema?.$ref;
+}
+
+describe('KS-591: POST /api/billing/customers and POST /api/billing/checkout/bundle publish a REQUIRED request body', () => {
+  it('RED KS-591 BC1: POST /api/billing/customers marks its request body required', () => {
+    expect(operation('/api/billing/customers', 'post')?.requestBody?.required).toBe(true);
+  });
+
+  it('RED KS-591 BC2: POST /api/billing/checkout/bundle marks its request body required', () => {
+    expect(operation('/api/billing/checkout/bundle', 'post')?.requestBody?.required).toBe(true);
+  });
+
+  it('control KS-591 BCC1: both bodies keep their request schemas and both operations keep bearerAuth', () => {
+    expect({
+      customers: bodyRef('/api/billing/customers', 'post'),
+      bundle: bodyRef('/api/billing/checkout/bundle', 'post'),
+    }).toEqual({
+      customers: '#/components/schemas/BillingCustomerCreateRequest',
+      bundle: '#/components/schemas/BillingCheckoutBundleRequest',
+    });
+    expect(operation('/api/billing/customers', 'post')?.security).toEqual([{ bearerAuth: [] }]);
+    expect(operation('/api/billing/checkout/bundle', 'post')?.security).toEqual([{ bearerAuth: [] }]);
+  });
+
+  it('control KS-591 BCC2: the request components still list required fields, which is why an absent body is refused', () => {
+    const s: AnyObj = doc.components?.schemas ?? {};
+    expect(s.BillingCustomerCreateRequest?.required).toEqual(expect.arrayContaining(['email', 'userId']));
+    expect(s.BillingCheckoutBundleRequest?.required).toEqual(expect.arrayContaining(['bundleId', 'successUrl', 'cancelUrl']));
+  });
+
+  it('control KS-591 BCC3: PUT /api/billing/customers/{id} keeps an OPTIONAL body (its handler accepts an empty one)', () => {
+    const op = operation('/api/billing/customers/{id}', 'put');
+    expect(op?.requestBody?.content?.['application/json']?.schema?.$ref).toBe('#/components/schemas/BillingCustomerUpdateRequest');
+    expect(op?.requestBody?.required).toBeUndefined();
+  });
+
+  it('control KS-591 BCC4: the KS-1364 sibling POST /api/billing/checkout/custom keeps its required body', () => {
+    expect(operation('/api/billing/checkout/custom', 'post')?.requestBody?.required).toBe(true);
+  });
+});
```

**Appended by Wednesday 03:25 2026-10-08 (not written by hold_ready):** REVIEWED HOLD on 2026-10-05 (`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-591-billing-customers-bundle/REVIEW.md`) but never held until now; classed UNRAISED by `0_Brain/reference/2026-10-08_spark-hold-census/CENSUS.md` (forward strict apply at develop eae08a3f441c, reverse refuses, no open PR). Read the REVIEW body for any raise caveat (the census read only its verdict line). Any YAML companion is in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-591-billing-customers-bundle/`. Raise is blocked until develop is green on pre-push leg 14 (pickup 03:1x).
