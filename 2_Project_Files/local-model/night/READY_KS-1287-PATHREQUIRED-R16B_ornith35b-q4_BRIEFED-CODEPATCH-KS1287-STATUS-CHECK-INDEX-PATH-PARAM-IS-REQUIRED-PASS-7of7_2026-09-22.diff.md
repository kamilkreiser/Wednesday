# READY — KS-1287-PATHREQUIRED-R16B (Ornith, briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `2_Project_Files/local-model/runs/2026-09-22_ks1287-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 15:52 2026-09-22; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1287-ornith35b-night/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1287-ornith35b-night/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; CONTENT-compared against the drafter's golden `2_Project_Files/local-model/runs/2026-09-22_feed14-drafter-precheck/PATHREQUIRED/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1); change lines (`+`/`-`, ordered) IDENTICAL in every file; body lines (context included) identical in every file; hunk headers differ (vc-issuer.openapi.ts: golden `@@ -1493,7 +1493,8 @@` vs run `@@ -1493,7 +1493,8 @@ sharedRegistry.registerPath({`); APPLIED RESULT not compared (input.json['files'] lacks a touched file's tip content).

**Held 15:52 2026-09-22 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `2_Project_Files/local-model/runs/2026-09-22_ks1287-ornith35b-night/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `3bad652d17cf111c1e2e1bed1ae7686894637487`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/vc-issuer/src/vc-issuer.openapi.ts , Blockchain/Dev/services/vc-issuer/src/__tests__/ks1287-status-check-index-path-param-is-required.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/vc-issuer/src/vc-issuer.openapi.ts` (product) and `Blockchain/Dev/services/vc-issuer/src/__tests__/ks1287-status-check-index-path-param-is-required.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
2	1	Blockchain/Dev/services/vc-issuer/src/vc-issuer.openapi.ts
55	0	Blockchain/Dev/services/vc-issuer/src/__tests__/ks1287-status-check-index-path-param-is-required.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (2 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 2 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 1.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/vc-issuer/src/vc-issuer.openapi.ts byte-exact incl. leading whitespace (apply mode strict): OK 2 line(s) byte-exact incl. leading whitespace (of 2; 2 line(s) added by the apply)` [a3i_indent.out: `OK 2 line(s) byte-exact incl. leading whitespace (of 2; 2 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/vc-issuer/src/vc-issuer.openapi.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/vc-issuer/src/__tests__/ks1287-status-check-index-path-param-is-required.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1287-status-check-index-path-param-is-required.test.ts fails at the untouched tip (2 failed / 4 run; controls green; assertion reds)` [red_first.json: failed=2 of total=4; red cell(s): ['KS-1287: the index path parameter of GET /api/status/{id}/check/{index} is published required RED KS-1287 A: the index path parameter renders required: true', 'KS-1287: the index path parameter of GET /api/status/{id}/check/{index} is published required RED KS-1287 B: no vc-issuer operation publishes an optional in: path parameter']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1287-status-check-index-path-param-is-required.test.ts passes with the product hunk (4 passed / 4 run)` [green_after.json: failed=0 of total=4, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=123 failed=0 | after: total=127 failed=0` · `NEW reds: []` [baseline_suite.json total=123 failed=0; after_suite.json total=127 failed=0]
- A6 [verbatim]: `PASS A6 whole services/vc-issuer suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/vc-issuer: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +57/-1 test=src/__tests__/ks1287-status-check-index-path-param-is-required.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/vc-issuer/src/vc-issuer.openapi.ts` (+2/-1 per numstat.out) and the test file `Blockchain/Dev/services/vc-issuer/src/__tests__/ks1287-status-check-index-path-param-is-required.test.ts` (+55/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `3bad652d17cf111c1e2e1bed1ae7686894637487` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `2_Project_Files/local-model/runs/2026-09-22_ks1287-ornith35b-night/input.json`. Brief (located by ticket + ROWID tokens under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1287-R16B-PATHREQUIRED.md`. Verdict source: `2_Project_Files/local-model/runs/2026-09-22_ks1287-ornith35b-night/checker.out`.

```diff
--- a/Blockchain/Dev/services/vc-issuer/src/vc-issuer.openapi.ts
+++ b/Blockchain/Dev/services/vc-issuer/src/vc-issuer.openapi.ts
@@ -1493,7 +1493,8 @@ sharedRegistry.registerPath({
     params: z.object({
       id: z.string(),
       // KS-423: pin the emitted type (coerce+nonnegative renders [integer, "null"]).
-      index: z.coerce.number().int().nonnegative().openapi({ type: 'integer', minimum: 0 }),
+      // KS-1287: coerce parses null as 0, so the lib reads the param as nullable and publishes required: false - pin it.
+      index: z.coerce.number().int().nonnegative().openapi({ type: 'integer', minimum: 0, param: { required: true } }),
     }),
   },
   responses: {
--- /dev/null
+++ b/Blockchain/Dev/services/vc-issuer/src/__tests__/ks1287-status-check-index-path-param-is-required.test.ts
@@ -0,0 +1,55 @@
+/**
+ * KS-1287: GET /api/status/{id}/check/{index} published its path parameter index as required: false - the only
+ * optional path parameter in the spec (OpenAPI 3 requires required: true on every in: path parameter; Schemathesis
+ * 4.27.5 reports it as a Schema Error). Mechanism, measured in-process: zod-to-openapi v7 computes required as
+ * not-isOptional and not-isNullable, and z.coerce.number() parses null as 0, so the coerce wrapper reads as
+ * nullable. The one-site fix pins required: true through the param metadata. This suite generates the document
+ * in-process from vc-issuer.openapi.ts the way scripts/generate-openapi.ts does.
+ */
+import { describe, it, expect } from 'vitest';
+import '../vc-issuer.openapi';
+import { generateOpenApiDocument } from '@secuura/shared';
+
+type Param = { name: string; in: string; required?: boolean; schema?: { type?: string; minimum?: number } };
+type Operation = { operationId?: string; parameters?: Param[] };
+
+const doc = generateOpenApiDocument({ title: 'ks1287', version: '0.0.0' }) as unknown as {
+  paths: Record<string, Record<string, Operation>>;
+};
+const op = doc.paths['/api/status/{id}/check/{index}'].get;
+const params = op.parameters ?? [];
+const indexParam = params.find((p) => p.name === 'index');
+const idParam = params.find((p) => p.name === 'id');
+
+function optionalPathParams(): string[] {
+  const out: string[] = [];
+  for (const [routePath, item] of Object.entries(doc.paths)) {
+    for (const [method, operation] of Object.entries(item)) {
+      for (const p of operation.parameters ?? []) {
+        if (p.in === 'path' && p.required !== true) out.push(method + ' ' + routePath + ' ' + p.name);
+      }
+    }
+  }
+  return out;
+}
+
+describe('KS-1287: the index path parameter of GET /api/status/{id}/check/{index} is published required', () => {
+  it('RED KS-1287 A: the index path parameter renders required: true', () => {
+    expect(indexParam?.required).toBe(true);
+  });
+
+  it('RED KS-1287 B: no vc-issuer operation publishes an optional in: path parameter', () => {
+    expect(optionalPathParams()).toEqual([]);
+  });
+
+  it('control: the operation and its two path parameters are registered', () => {
+    expect(op.operationId).toBe('getStatusByIdCheckByIndex');
+    expect(params.filter((p) => p.in === 'path').map((p) => p.name)).toEqual(['id', 'index']);
+  });
+
+  it('control: the id sibling renders required: true and index keeps its pinned integer schema', () => {
+    expect(idParam?.required).toBe(true);
+    expect(indexParam?.schema?.type).toBe('integer');
+    expect(indexParam?.schema?.minimum).toBe(0);
+  });
+});
```
