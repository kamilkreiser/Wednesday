# READY — KS-1364-ONEDRIVE-1 (spark-dsv4flash, briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-01_KS-1364-onedrive/out.md.checker/patch.diff`** (from `ls` at 10:28 2026-10-01; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-01_KS-1364-onedrive/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-01_KS-1364-onedrive/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-01_KS-1364-onedrive/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1364-onedrive/precheck/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 10:28 2026-10-01 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-01_KS-1364-onedrive/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `723dc0722b68482a03de8577fdb5eb5b3359e725`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/m365-integration/src/m365-integration.openapi.ts , Blockchain/Dev/services/m365-integration/src/__tests__/ks1364-onedrive-file-sync-body-required.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/m365-integration/src/m365-integration.openapi.ts` (product) and `Blockchain/Dev/services/m365-integration/src/__tests__/ks1364-onedrive-file-sync-body-required.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
1	0	Blockchain/Dev/services/m365-integration/src/m365-integration.openapi.ts
43	0	Blockchain/Dev/services/m365-integration/src/__tests__/ks1364-onedrive-file-sync-body-required.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (1 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 1 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 0.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/m365-integration/src/m365-integration.openapi.ts byte-exact incl. leading whitespace (apply mode strict): OK 1 line(s) byte-exact incl. leading whitespace (of 1; 1 line(s) added by the apply)` [a3i_indent.out: `OK 1 line(s) byte-exact incl. leading whitespace (of 1; 1 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/m365-integration/src/m365-integration.openapi.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/m365-integration/src/__tests__/ks1364-onedrive-file-sync-body-required.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1364-onedrive-file-sync-body-required.test.ts fails at the untouched tip (1 failed / 4 run; controls green; assertion reds)` [red_first.json: failed=1 of total=4; red cell(s): ['KS-1364: POST /api/onedrive/files/{id}/sync publishes a REQUIRED request body RED KS-1364 OD1: POST /api/onedrive/files/{id}/sync marks its request body required']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1364-onedrive-file-sync-body-required.test.ts passes with the product hunk (4 passed / 4 run)` [green_after.json: failed=0 of total=4, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=47 failed=0 | after: total=51 failed=0` · `NEW reds: []` [baseline_suite.json total=47 failed=0; after_suite.json total=51 failed=0]
- A6 [verbatim]: `PASS A6 whole services/m365-integration suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/m365-integration: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +44/-0 test=src/__tests__/ks1364-onedrive-file-sync-body-required.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/m365-integration/src/m365-integration.openapi.ts` (+1/-0 per numstat.out) and the test file `Blockchain/Dev/services/m365-integration/src/__tests__/ks1364-onedrive-file-sync-body-required.test.ts` (+43/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `723dc0722b68482a03de8577fdb5eb5b3359e725` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-01_KS-1364-onedrive/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-01_KS-1364-onedrive/checker.out`.

```diff
--- a/Blockchain/Dev/services/m365-integration/src/m365-integration.openapi.ts
+++ b/Blockchain/Dev/services/m365-integration/src/m365-integration.openapi.ts
@@ -831,6 +831,7 @@
             .passthrough(),
         },
       },
+      required: true,
     },
   },
   responses: {
--- /dev/null
+++ b/Blockchain/Dev/services/m365-integration/src/__tests__/ks1364-onedrive-file-sync-body-required.test.ts
@@ -0,0 +1,43 @@
+// KS-1364 (sweep 4): the published contract for POST /api/onedrive/files/{id}/sync did not mark the request body
+// required, so a spec-driven caller (Schemathesis) sent no body at all and the handler (index.ts, the
+// connectionId truthy check) answered 400. The handler rejects an absent body, so the spec now says the body is
+// required. This file renders the document the generator publishes, from the shared registry the m365-integration
+// module populates on import. No server, no database, no network.
+import { describe, it, expect } from 'vitest';
+import { generateOpenApiDocument } from '@secuura/shared';
+import '../m365-integration.openapi';
+
+type AnyObj = Record<string, any>;
+
+const doc = generateOpenApiDocument({ title: 'm365-integration (ks1364 onedrive pin)', version: '0.0.0' }) as AnyObj;
+
+const SYNC = '/api/onedrive/files/{id}/sync';
+
+function operation(path: string, method: string): AnyObj | undefined {
+  return doc.paths?.[path]?.[method];
+}
+
+describe('KS-1364: POST /api/onedrive/files/{id}/sync publishes a REQUIRED request body', () => {
+  it('RED KS-1364 OD1: POST /api/onedrive/files/{id}/sync marks its request body required', () => {
+    expect(operation(SYNC, 'post')?.requestBody?.required).toBe(true);
+  });
+
+  it('control KS-1364 OC1: the inline body schema still requires a non-empty connectionId', () => {
+    const s = operation(SYNC, 'post')?.requestBody?.content?.['application/json']?.schema;
+    expect({ required: s?.required, minLength: s?.properties?.connectionId?.minLength }).toEqual({
+      required: ['connectionId'],
+      minLength: 1,
+    });
+  });
+
+  it('control KS-1364 OC2: the operation keeps bearerAuth and its path parameter id', () => {
+    const op = operation(SYNC, 'post');
+    expect(op?.security).toEqual([{ bearerAuth: [] }]);
+    expect((op?.parameters ?? []).map((q: AnyObj) => q.in + ':' + q.name)).toEqual(['path:id']);
+  });
+
+  it('control KS-1364 OC3: the sibling POST /api/teams/notify keeps its request body schema', () => {
+    const ref = operation('/api/teams/notify', 'post')?.requestBody?.content?.['application/json']?.schema?.$ref;
+    expect(ref).toBe('#/components/schemas/M365TeamsNotifyRequest');
+  });
+});
```

> (Added BY HAND 10:28 2026-10-01 by the brief-writer sub-agent.) **Raise-seat step the model does not do:** the PR also needs the regenerated `Blockchain/Dev/docs/openapi/secuura-api.yaml` — apply `night/briefs/KS-1364-onedrive/KS-1364.openapi-yaml.companion.diff` (or run `npm run generate-openapi` and confirm), then `npm run check:openapi` (measured: model files alone -> `generate-openapi --check` rc 1; + companion -> `check:openapi` rc 0). **Scope: refs KS-1364, does NOT close it** (this READY: 1 of 17; the six KS-1364 READYs together: 11 of 17). All six READYs' product sections + companions apply strictly in sequence on one tree (measured) — they go up as ONE PR.
