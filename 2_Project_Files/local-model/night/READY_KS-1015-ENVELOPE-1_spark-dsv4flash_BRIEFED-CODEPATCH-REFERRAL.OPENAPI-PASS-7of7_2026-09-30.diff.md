# READY — KS-1015-ENVELOPE-1 (spark-dsv4flash, briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-30_KS-1015-envelope/out.md.checker/patch.diff`** (from `ls` at 03:01 2026-09-30; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-30_KS-1015-envelope/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-30_KS-1015-envelope/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-30_KS-1015-envelope/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1015-envelope/precheck/out.md.checker/patch.diff` rc 0, Spark brief-writer sub-agent for Wednesday (ffc4a192)).

> **Added by hand (not by hold_ready.py) — RAISE-SEAT STEP, a THIRD file the model does not write (KS-747 precedent):** the PR must also carry the regenerated `Blockchain/Dev/docs/openapi/secuura-api.yaml`. Apply `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1015-envelope/KS-1015.openapi-yaml.companion.diff` (+30/-1 at `@@ -32163,7 +32163,36 @@`), or run `npm run generate-openapi` in `Blockchain/Dev` and confirm it is byte-identical; then `npm run check:openapi`. Measured at the tip in a scratch clone: the two model files alone → `generate-openapi -- --check` rc 1 (CHECK FAIL); with the companion → `check:openapi` rc 0 (drift PASS, 405 example blocks OK). **Scope: refs KS-1015, does NOT close it** (one pair of a 28+-pair register).

**Held 03:01 2026-09-30 by Spark brief-writer sub-agent for Wednesday (ffc4a192) after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-30_KS-1015-envelope/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `37205947ddd2775a72a417beb5b7ac8e3240fbf3`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/referral/src/referral.openapi.ts , Blockchain/Dev/services/referral/src/__tests__/ks1015-referral-lookup-spec-declares-envelope.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/referral/src/referral.openapi.ts` (product) and `Blockchain/Dev/services/referral/src/__tests__/ks1015-referral-lookup-spec-declares-envelope.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
21	1	Blockchain/Dev/services/referral/src/referral.openapi.ts
76	0	Blockchain/Dev/services/referral/src/__tests__/ks1015-referral-lookup-spec-declares-envelope.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (21 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 21 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 1.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/referral/src/referral.openapi.ts byte-exact incl. leading whitespace (apply mode strict): OK 21 line(s) byte-exact incl. leading whitespace (of 21; 21 line(s) added by the apply)` [a3i_indent.out: `OK 21 line(s) byte-exact incl. leading whitespace (of 21; 21 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/referral/src/referral.openapi.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/referral/src/__tests__/ks1015-referral-lookup-spec-declares-envelope.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1015-referral-lookup-spec-declares-envelope.test.ts fails at the untouched tip (3 failed / 6 run; controls green; assertion reds)` [red_first.json: failed=3 of total=6; red cell(s): ['KS-1015: GET /api/referrals/{code} publishes the envelope its handler returns RED KS-1015 A1: the 200 body is the success/data envelope, not the flat ReferralCode record', 'KS-1015: GET /api/referrals/{code} publishes the envelope its handler returns RED KS-1015 A2: data declares the six fields the handler sends, customLabel optional, no id or ownerUserId', 'KS-1015: GET /api/referrals/{code} publishes the envelope its handler returns RED KS-1015 A3: the data fields carry the runtime types']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1015-referral-lookup-spec-declares-envelope.test.ts passes with the product hunk (6 passed / 6 run)` [green_after.json: failed=0 of total=6, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=28 failed=0 | after: total=34 failed=0` · `NEW reds: []` [baseline_suite.json total=28 failed=0; after_suite.json total=34 failed=0]
- A6 [verbatim]: `PASS A6 whole services/referral suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/referral: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +97/-1 test=src/__tests__/ks1015-referral-lookup-spec-declares-envelope.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/referral/src/referral.openapi.ts` (+21/-1 per numstat.out) and the test file `Blockchain/Dev/services/referral/src/__tests__/ks1015-referral-lookup-spec-declares-envelope.test.ts` (+76/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `37205947ddd2775a72a417beb5b7ac8e3240fbf3` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-30_KS-1015-envelope/input.json`. Brief (given by --brief; its `# ` heading names KS-1015): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1015-envelope/KS-1015.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-30_KS-1015-envelope/checker.out`.

```diff
--- a/Blockchain/Dev/services/referral/src/referral.openapi.ts
+++ b/Blockchain/Dev/services/referral/src/referral.openapi.ts
@@ -477,7 +477,27 @@
     400: commonErrorResponses[400],
     200: {
       description: 'Code',
-      content: { 'application/json': { schema: ReferralCodeSchema } },
+      // KS-1015: the handler (routes/referrals.ts, GET /:code) returns a success/data envelope
+      // with a public projection: code, isActive, isExpired, referredReward and referrerReward
+      // always, customLabel only when set. It leaves out id and ownerUserId on purpose (a public
+      // lookup), so the spec follows the runtime. ReferralCodeSchema stays for the owner list.
+      content: {
+        'application/json': {
+          schema: z.object({
+            success: z.literal(true),
+            data: z
+              .object({
+                code: z.string(),
+                isActive: z.boolean(),
+                isExpired: z.boolean(),
+                customLabel: z.string().optional(),
+                referredReward: z.string(),
+                referrerReward: z.string(),
+              })
+              .passthrough(),
+          }),
+        },
+      },
     },
     404: { ...commonErrorResponses[404], description: 'Code not found / inactive' },
     429: commonErrorResponses[429],
--- /dev/null
+++ b/Blockchain/Dev/services/referral/src/__tests__/ks1015-referral-lookup-spec-declares-envelope.test.ts
@@ -0,0 +1,76 @@
+// KS-1015 (sweep 2026-09-29): the published contract for GET /api/referrals/{code} declared the flat
+// ReferralCode record (id, code, ownerUserId, uses, ...) as its 200 body, while the handler (routes/referrals.ts,
+// GET /:code) answers { success, data: { code, isActive, isExpired, customLabel, referredReward, referrerReward } }.
+// Schemathesis flagged the 200 as response_schema_conformance. The handler leaves out id and ownerUserId on
+// purpose (a public lookup), so the spec follows the runtime. This file renders the document the generator
+// publishes, from the shared registry the referral module populates on import. No server, no database, no network.
+import { describe, it, expect } from 'vitest';
+import { generateOpenApiDocument } from '@secuura/shared';
+import '../referral.openapi';
+
+type AnyObj = Record<string, any>;
+
+const doc = generateOpenApiDocument({ title: 'referral (ks1015 pin)', version: '0.0.0' }) as AnyObj;
+
+function operation(path: string, method: string): AnyObj | undefined {
+  return doc.paths?.[path]?.[method];
+}
+
+function body(path: string, method: string, status: string): AnyObj | undefined {
+  return operation(path, method)?.responses?.[status]?.content?.['application/json']?.schema;
+}
+
+describe('KS-1015: GET /api/referrals/{code} publishes the envelope its handler returns', () => {
+  it('RED KS-1015 A1: the 200 body is the success/data envelope, not the flat ReferralCode record', () => {
+    const s = body('/api/referrals/{code}', 'get', '200');
+    expect({ ref: s?.$ref, required: s?.required, success: s?.properties?.success }).toEqual({
+      ref: undefined,
+      required: ['success', 'data'],
+      success: { type: 'boolean', enum: [true] },
+    });
+  });
+
+  it('RED KS-1015 A2: data declares the six fields the handler sends, customLabel optional, no id or ownerUserId', () => {
+    const d = body('/api/referrals/{code}', 'get', '200')?.properties?.data;
+    expect({
+      fields: Object.keys(d?.properties ?? {}).sort(),
+      required: [...(d?.required ?? [])].sort(),
+    }).toEqual({
+      fields: ['code', 'customLabel', 'isActive', 'isExpired', 'referredReward', 'referrerReward'],
+      required: ['code', 'isActive', 'isExpired', 'referredReward', 'referrerReward'],
+    });
+  });
+
+  it('RED KS-1015 A3: the data fields carry the runtime types', () => {
+    const p: AnyObj = body('/api/referrals/{code}', 'get', '200')?.properties?.data?.properties ?? {};
+    const types = Object.fromEntries(Object.entries(p).map(([k, v]) => [k, (v as AnyObj).type]));
+    expect(types).toEqual({
+      code: 'string',
+      isActive: 'boolean',
+      isExpired: 'boolean',
+      customLabel: 'string',
+      referredReward: 'string',
+      referrerReward: 'string',
+    });
+  });
+
+  it('control KS-1015 C1: the GET operation keeps bearerAuth, its path parameter code, and its 404', () => {
+    const op = operation('/api/referrals/{code}', 'get');
+    expect(op?.security).toEqual([{ bearerAuth: [] }]);
+    expect((op?.parameters ?? []).map((q: AnyObj) => q.in + ':' + q.name + ':' + q.required)).toEqual(['path:code:true']);
+    expect(Object.keys(op?.responses ?? {})).toEqual(expect.arrayContaining(['200', '404']));
+  });
+
+  it('control KS-1015 C2: the ReferralCode component stays published and the owner list still returns it', () => {
+    expect(doc.components?.schemas?.ReferralCode).toBeDefined();
+    expect(body('/api/referrals/user/{userId}', 'get', '200')?.properties?.codes?.items?.$ref).toBe('#/components/schemas/ReferralCode');
+  });
+
+  it('control KS-1015 C3: the sibling POST /generate keeps its own 201 envelope', () => {
+    const s = body('/api/referrals/generate', 'post', '201');
+    expect({ required: s?.required, shareUrl: s?.properties?.data?.properties?.shareUrl?.type }).toEqual({
+      required: ['success', 'data'],
+      shareUrl: 'string',
+    });
+  });
+});
```
