# READY — KS-1364-ANALYTICS-REPORTS-1 (spark-dsv4flash, briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-01_KS-1364-analytics-reports/out.md.checker/patch.diff`** (from `ls` at 10:09 2026-10-01; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-01_KS-1364-analytics-reports/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-01_KS-1364-analytics-reports/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-01_KS-1364-analytics-reports/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1364-analytics-reports/precheck/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 10:09 2026-10-01 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-01_KS-1364-analytics-reports/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `723dc0722b68482a03de8577fdb5eb5b3359e725`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/analytics/src/analytics.openapi.ts , Blockchain/Dev/services/analytics/src/__tests__/ks1364-analytics-reports-body-required.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/analytics/src/analytics.openapi.ts` (product) and `Blockchain/Dev/services/analytics/src/__tests__/ks1364-analytics-reports-body-required.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
1	1	Blockchain/Dev/services/analytics/src/analytics.openapi.ts
40	0	Blockchain/Dev/services/analytics/src/__tests__/ks1364-analytics-reports-body-required.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (1 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 1 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 1.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/analytics/src/analytics.openapi.ts byte-exact incl. leading whitespace (apply mode strict): OK 1 line(s) byte-exact incl. leading whitespace (of 1; 1 line(s) added by the apply)` [a3i_indent.out: `OK 1 line(s) byte-exact incl. leading whitespace (of 1; 1 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/analytics/src/analytics.openapi.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/analytics/src/__tests__/ks1364-analytics-reports-body-required.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1364-analytics-reports-body-required.test.ts fails at the untouched tip (1 failed / 4 run; controls green; assertion reds)` [red_first.json: failed=1 of total=4; red cell(s): ['KS-1364: POST /api/analytics/reports publishes a REQUIRED request body RED KS-1364 AR1: POST /api/analytics/reports marks its request body required']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1364-analytics-reports-body-required.test.ts passes with the product hunk (4 passed / 4 run)` [green_after.json: failed=0 of total=4, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=28 failed=0 | after: total=32 failed=0` · `NEW reds: []` [baseline_suite.json total=28 failed=0; after_suite.json total=32 failed=0]
- A6 [verbatim]: `PASS A6 whole services/analytics suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/analytics: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +41/-1 test=src/__tests__/ks1364-analytics-reports-body-required.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/analytics/src/analytics.openapi.ts` (+1/-1 per numstat.out) and the test file `Blockchain/Dev/services/analytics/src/__tests__/ks1364-analytics-reports-body-required.test.ts` (+40/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `723dc0722b68482a03de8577fdb5eb5b3359e725` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-01_KS-1364-analytics-reports/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-01_KS-1364-analytics-reports/checker.out`.

```diff
--- a/Blockchain/Dev/services/analytics/src/analytics.openapi.ts
+++ b/Blockchain/Dev/services/analytics/src/analytics.openapi.ts
@@ -923,7 +923,7 @@
   summary: 'Generate an analytics report',
   security: [{ bearerAuth: [] }],
   request: {
-    body: { content: { 'application/json': { schema: ReportRequestSchema } } },
+    body: { content: { 'application/json': { schema: ReportRequestSchema } }, required: true },
   },
   responses: {
     // KS-475 (§6): the runtime answers 200 synchronously — the spec's 202
--- /dev/null
+++ b/Blockchain/Dev/services/analytics/src/__tests__/ks1364-analytics-reports-body-required.test.ts
@@ -0,0 +1,40 @@
+// KS-1364 (sweep 4): the published contract for POST /api/analytics/reports did not mark the request body
+// required, so a spec-driven caller (Schemathesis) sent no body at all and the handler (routes/analytics.ts,
+// ReportRequestSchema.parse) answered 400. That zod object requires type and period, so it rejects an absent
+// body, and the spec now says the body is required. This file renders the document the generator publishes,
+// from the shared registry the analytics module populates on import. No server, no database, no network.
+import { describe, it, expect } from 'vitest';
+import { generateOpenApiDocument } from '@secuura/shared';
+import '../analytics.openapi';
+
+type AnyObj = Record<string, any>;
+
+const doc = generateOpenApiDocument({ title: 'analytics (ks1364 reports pin)', version: '0.0.0' }) as AnyObj;
+
+function operation(path: string, method: string): AnyObj | undefined {
+  return doc.paths?.[path]?.[method];
+}
+
+function bodyRef(path: string): string | undefined {
+  return operation(path, 'post')?.requestBody?.content?.['application/json']?.schema?.$ref;
+}
+
+describe('KS-1364: POST /api/analytics/reports publishes a REQUIRED request body', () => {
+  it('RED KS-1364 AR1: POST /api/analytics/reports marks its request body required', () => {
+    expect(operation('/api/analytics/reports', 'post')?.requestBody?.required).toBe(true);
+  });
+
+  it('control KS-1364 AC1: the body keeps its request schema and the operation keeps bearerAuth', () => {
+    expect(bodyRef('/api/analytics/reports')).toBe('#/components/schemas/AnalyticsReportRequest');
+    expect(operation('/api/analytics/reports', 'post')?.security).toEqual([{ bearerAuth: [] }]);
+  });
+
+  it('control KS-1364 AC2: the request component still requires type and period, which is why an absent body is refused', () => {
+    const r = doc.components?.schemas?.AnalyticsReportRequest?.required ?? [];
+    expect([...r].sort()).toEqual(['period', 'type']);
+  });
+
+  it('control KS-1364 AC3: the sibling POST /api/analytics/exports keeps its request body schema', () => {
+    expect(bodyRef('/api/analytics/exports')).toBe('#/components/schemas/AnalyticsExportRequest');
+  });
+});
```

> (Added BY HAND 10:10 2026-10-01 by the brief-writer sub-agent.) **Raise-seat step the model does not do:** the PR also needs the regenerated `Blockchain/Dev/docs/openapi/secuura-api.yaml` — apply `night/briefs/KS-1364-analytics-reports/KS-1364.openapi-yaml.companion.diff` (or run `npm run generate-openapi` in `Blockchain/Dev` and confirm the same `required: true` lines), then `npm run check:openapi` (measured: model files alone -> `generate-openapi --check` rc 1; + companion -> `check:openapi` rc 0). **Scope: refs KS-1364, does NOT close it** (17 operations; the three KS-1364 READYs together close 5). The three READYs + their companions apply strictly in sequence on one tree (measured).
