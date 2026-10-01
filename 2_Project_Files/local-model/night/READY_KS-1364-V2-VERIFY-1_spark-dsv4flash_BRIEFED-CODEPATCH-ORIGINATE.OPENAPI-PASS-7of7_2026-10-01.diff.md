# READY — KS-1364-V2-VERIFY-1 (spark-dsv4flash, briefed, code_patch, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-01_KS-1364-v2-verify/out.md.checker/patch.diff`** (from `ls` at 18:00 2026-10-01; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-01_KS-1364-v2-verify/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-01_KS-1364-v2-verify/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-01_KS-1364-v2-verify/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1364-v2-verify/precheck/out.md.checker/patch.diff` rc 0, Spark brief-writer sub-agent for Wednesday (batch 3)).

**Held 18:00 2026-10-01 by Spark brief-writer sub-agent for Wednesday (batch 3) after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-01_KS-1364-v2-verify/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `0736d8b7849ef6c725c891d7254f2a3e21f42eb6`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/originate/src/originate.openapi.ts , Blockchain/Dev/services/originate/src/__tests__/ks1364-v2-verification-verify-body-required.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/originate.openapi.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1364-v2-verification-verify-body-required.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
1	0	Blockchain/Dev/services/originate/src/originate.openapi.ts
46	0	Blockchain/Dev/services/originate/src/__tests__/ks1364-v2-verification-verify-body-required.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (1 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 1 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 0.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/originate/src/originate.openapi.ts byte-exact incl. leading whitespace (apply mode strict): OK 1 line(s) byte-exact incl. leading whitespace (of 1; 1 line(s) added by the apply)` [a3i_indent.out: `OK 1 line(s) byte-exact incl. leading whitespace (of 1; 1 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/originate.openapi.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1364-v2-verification-verify-body-required.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1364-v2-verification-verify-body-required.test.ts fails at the untouched tip (1 failed / 4 run; controls green; assertion reds)` [red_first.json: failed=1 of total=4; red cell(s): ['KS-1364: POST /api/v2/verification/verify publishes a REQUIRED request body RED KS-1364 VV1: POST /api/v2/verification/verify marks its request body required']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1364-v2-verification-verify-body-required.test.ts passes with the product hunk (4 passed / 4 run)` [green_after.json: failed=0 of total=4, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1058 failed=0 | after: total=1062 failed=0` · `NEW reds: []` [baseline_suite.json total=1058 failed=0; after_suite.json total=1062 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +47/-0 test=src/__tests__/ks1364-v2-verification-verify-body-required.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/originate.openapi.ts` (+1/-0 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1364-v2-verification-verify-body-required.test.ts` (+46/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `0736d8b7849ef6c725c891d7254f2a3e21f42eb6` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-01_KS-1364-v2-verify/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-01_KS-1364-v2-verify/checker.out`.

```diff
--- a/Blockchain/Dev/services/originate/src/originate.openapi.ts
+++ b/Blockchain/Dev/services/originate/src/originate.openapi.ts
@@ -2053,6 +2053,7 @@
   ...sla('read'),
   request: {
     body: {
+      required: true,
       content: {
         'application/json': { schema: V2VerifyRequestSchema },
       },
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1364-v2-verification-verify-body-required.test.ts
@@ -0,0 +1,46 @@
+// KS-1364 (sweep 4): the published contract for POST /api/v2/verification/verify did not mark the request body
+// required, so a spec-driven caller (Schemathesis) sent no body at all and the handler answered 400. The handler
+// (routes/verificationV2.ts) resolves a hash from hash, providedHash, contentHash or documentHash, else uses
+// documentId or documentData, and answers 400 when none is present. An absent body arrives as {} and is refused,
+// so the spec now says the body is required. This file renders the document the generator publishes, from the
+// shared registry the originate module populates on import. No server, no database, no network.
+import { generateOpenApiDocument } from '@secuura/shared';
+import '../originate.openapi';
+
+type AnyObj = Record<string, any>;
+
+const doc = generateOpenApiDocument({ title: 'originate (ks1364 pin)', version: '0.0.0' }) as AnyObj;
+
+const V2 = '/api/v2/verification/verify';
+
+function operation(path: string, method: string): AnyObj | undefined {
+  return doc.paths?.[path]?.[method];
+}
+
+function bodyRef(path: string): string | undefined {
+  return operation(path, 'post')?.requestBody?.content?.['application/json']?.schema?.$ref;
+}
+
+describe('KS-1364: POST /api/v2/verification/verify publishes a REQUIRED request body', () => {
+  it('RED KS-1364 VV1: POST /api/v2/verification/verify marks its request body required', () => {
+    expect(operation(V2, 'post')?.requestBody?.required).toBe(true);
+  });
+
+  it('control KS-1364 VC1: the v2 body keeps its schema and the route stays public (security [])', () => {
+    expect(bodyRef(V2)).toBe('#/components/schemas/V2VerifyRequest');
+    expect(operation(V2, 'post')?.security).toEqual([]);
+  });
+
+  it('control KS-1364 VC2: the v2 request schema keeps every field optional (the handler picks one)', () => {
+    const s = doc.components?.schemas?.V2VerifyRequest;
+    expect(s).toBeDefined();
+    expect(s?.required).toBeUndefined();
+    expect(Object.keys(s?.properties ?? {})).toEqual(
+      expect.arrayContaining(['hash', 'contentHash', 'providedHash', 'documentHash', 'documentId', 'documentData']),
+    );
+  });
+
+  it('control KS-1364 VC3: the v1 POST /api/verification/verify keeps its own request body schema', () => {
+    expect(bodyRef('/api/verification/verify')).toBe('#/components/schemas/VerifyRequest');
+  });
+});
```

> (Added BY HAND 18:02 2026-10-01 by the batch-3 brief-writer sub-agent.) **Raise-seat step the model does not do:** the PR also needs the regenerated `Blockchain/Dev/docs/openapi/secuura-api.yaml` — apply `night/briefs/KS-1364-v2-verify/KS-1364.openapi-yaml.companion.diff` (or run `npm run generate-openapi` and confirm), then `npm run check:openapi` (measured: model files alone -> `generate-openapi --check` rc 1; + companion -> `check:openapi` rc 0). **Scope: refs KS-1364, does NOT close it** (this READY: 1 of 17; with #1365 merged (11) and the other batch-3 READY: 13 of 17). Base develop `0736d8b7`. Measured: both batch-3 goldens + companions apply strictly on top of the HELD KS-1015 envelope golden + companion on one tree, and `check:openapi` is rc 0 there (SCREEN.md, Batch 3).
