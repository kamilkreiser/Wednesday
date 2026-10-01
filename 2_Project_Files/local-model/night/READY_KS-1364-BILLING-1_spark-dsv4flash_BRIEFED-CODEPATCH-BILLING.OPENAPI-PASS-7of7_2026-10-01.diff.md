# READY — KS-1364-BILLING-1 (spark-dsv4flash, briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-01_KS-1364-billing/out.md.checker/patch.diff`** (from `ls` at 10:25 2026-10-01; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-01_KS-1364-billing/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-01_KS-1364-billing/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-01_KS-1364-billing/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1364-billing/precheck/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 10:25 2026-10-01 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-01_KS-1364-billing/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `723dc0722b68482a03de8577fdb5eb5b3359e725`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/billing/src/billing.openapi.ts , Blockchain/Dev/services/billing/src/__tests__/ks1364-billing-checkout-custom-default-payment-method-body-required.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/billing/src/billing.openapi.ts` (product) and `Blockchain/Dev/services/billing/src/__tests__/ks1364-billing-checkout-custom-default-payment-method-body-required.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
2	0	Blockchain/Dev/services/billing/src/billing.openapi.ts
53	0	Blockchain/Dev/services/billing/src/__tests__/ks1364-billing-checkout-custom-default-payment-method-body-required.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (2 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 2 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 0.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/billing/src/billing.openapi.ts byte-exact incl. leading whitespace (apply mode strict): OK 2 line(s) byte-exact incl. leading whitespace (of 2; 2 line(s) added by the apply)` [a3i_indent.out: `OK 2 line(s) byte-exact incl. leading whitespace (of 2; 2 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/billing/src/billing.openapi.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/billing/src/__tests__/ks1364-billing-checkout-custom-default-payment-method-body-required.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1364-billing-checkout-custom-default-payment-method-body-required.test.ts fails at the untouched tip (2 failed / 5 run; controls green; assertion reds)` [red_first.json: failed=2 of total=5; red cell(s): ['KS-1364: two billing POSTs publish a REQUIRED request body RED KS-1364 BL1: POST /api/billing/checkout/custom marks its request body required', 'KS-1364: two billing POSTs publish a REQUIRED request body RED KS-1364 BL2: POST default-payment-method marks its request body required']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1364-billing-checkout-custom-default-payment-method-body-required.test.ts passes with the product hunk (5 passed / 5 run)` [green_after.json: failed=0 of total=5, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=93 failed=0 | after: total=98 failed=0` · `NEW reds: []` [baseline_suite.json total=93 failed=0; after_suite.json total=98 failed=0]
- A6 [verbatim]: `PASS A6 whole services/billing suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/billing: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +55/-0 test=src/__tests__/ks1364-billing-checkout-custom-default-payment-method-body-required.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/billing/src/billing.openapi.ts` (+2/-0 per numstat.out) and the test file `Blockchain/Dev/services/billing/src/__tests__/ks1364-billing-checkout-custom-default-payment-method-body-required.test.ts` (+53/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `723dc0722b68482a03de8577fdb5eb5b3359e725` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-01_KS-1364-billing/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-01_KS-1364-billing/checker.out`.

```diff
--- a/Blockchain/Dev/services/billing/src/billing.openapi.ts
+++ b/Blockchain/Dev/services/billing/src/billing.openapi.ts
@@ -738,6 +738,7 @@
   request: {
     body: {
       content: { 'application/json': { schema: CheckoutCustomRequestSchema } },
+      required: true,
     },
   },
   responses: {
@@ -878,6 +879,7 @@
     params: z.object({ customerId: z.string() }),
     body: {
       content: { 'application/json': { schema: SetDefaultPaymentMethodRequestSchema } },
+      required: true,
     },
   },
   responses: {
--- /dev/null
+++ b/Blockchain/Dev/services/billing/src/__tests__/ks1364-billing-checkout-custom-default-payment-method-body-required.test.ts
@@ -0,0 +1,53 @@
+// KS-1364 (sweep 4): the published contracts for POST /api/billing/checkout/custom and
+// POST /api/billing/customers/{customerId}/default-payment-method did not mark the request body required, so a
+// spec-driven caller (Schemathesis) sent no body at all and both handlers answered 400 (routes/billing.ts:
+// PurchaseCustomSchema.parse for checkout/custom; the paymentMethodId string check for default-payment-method).
+// Both reject an absent body, so the spec now says the body is required. This file renders the document the
+// generator publishes, from the shared registry the billing module populates on import. No server, no database,
+// no network, no Stripe.
+import { describe, it, expect } from 'vitest';
+import { generateOpenApiDocument } from '@secuura/shared';
+import '../billing.openapi';
+
+type AnyObj = Record<string, any>;
+
+const doc = generateOpenApiDocument({ title: 'billing (ks1364 pin)', version: '0.0.0' }) as AnyObj;
+
+const CUSTOM = '/api/billing/checkout/custom';
+const DEFAULT_PM = '/api/billing/customers/{customerId}/default-payment-method';
+
+function operation(path: string, method: string): AnyObj | undefined {
+  return doc.paths?.[path]?.[method];
+}
+
+function bodyRef(path: string): string | undefined {
+  return operation(path, 'post')?.requestBody?.content?.['application/json']?.schema?.$ref;
+}
+
+describe('KS-1364: two billing POSTs publish a REQUIRED request body', () => {
+  it('RED KS-1364 BL1: POST /api/billing/checkout/custom marks its request body required', () => {
+    expect(operation(CUSTOM, 'post')?.requestBody?.required).toBe(true);
+  });
+
+  it('RED KS-1364 BL2: POST default-payment-method marks its request body required', () => {
+    expect(operation(DEFAULT_PM, 'post')?.requestBody?.required).toBe(true);
+  });
+
+  it('control KS-1364 BC1: both bodies keep their request schemas and both operations keep bearerAuth', () => {
+    expect({ custom: bodyRef(CUSTOM), pm: bodyRef(DEFAULT_PM) }).toEqual({
+      custom: '#/components/schemas/BillingCheckoutCustomRequest',
+      pm: '#/components/schemas/BillingSetDefaultPaymentMethodRequest',
+    });
+    expect(operation(CUSTOM, 'post')?.security).toEqual([{ bearerAuth: [] }]);
+    expect(operation(DEFAULT_PM, 'post')?.security).toEqual([{ bearerAuth: [] }]);
+  });
+
+  it('control KS-1364 BC2: the custom-checkout component still lists its required fields', () => {
+    const r = doc.components?.schemas?.BillingCheckoutCustomRequest?.required ?? [];
+    expect(r).toEqual(expect.arrayContaining(['quantity', 'successUrl', 'cancelUrl']));
+  });
+
+  it('control KS-1364 BC3: the sibling POST /api/billing/checkout/bundle keeps its request body schema', () => {
+    expect(bodyRef('/api/billing/checkout/bundle')).toBe('#/components/schemas/BillingCheckoutBundleRequest');
+  });
+});
```

> (Added BY HAND 10:28 2026-10-01 by the brief-writer sub-agent.) **Raise-seat step the model does not do:** the PR also needs the regenerated `Blockchain/Dev/docs/openapi/secuura-api.yaml` — apply `night/briefs/KS-1364-billing/KS-1364.openapi-yaml.companion.diff` (or run `npm run generate-openapi` and confirm), then `npm run check:openapi` (measured: model files alone -> `generate-openapi --check` rc 1; + companion -> `check:openapi` rc 0). **Scope: refs KS-1364, does NOT close it** (this READY: 2 of 17; the six KS-1364 READYs together: 11 of 17). All six READYs' product sections + companions apply strictly in sequence on one tree (measured) — they go up as ONE PR.
