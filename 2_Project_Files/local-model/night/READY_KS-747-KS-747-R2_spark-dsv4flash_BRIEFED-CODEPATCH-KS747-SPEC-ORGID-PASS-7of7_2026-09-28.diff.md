# READY — KS-747-KS-747-R2 (spark-dsv4flash, briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-28_KS-747-R2/out.md.checker/patch.diff`** (from `ls` at 06:37 2026-09-28; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-28_KS-747-R2/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-28_KS-747-R2/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-28_KS-747-R2/out.md.checker/patch.diff /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/4901153c-5db0-4cfc-bf83-c25726202b34/scratchpad/golden_747/out.md.checker/patch.diff` rc 0, Wednesday morning 4901153c).

**Held 06:37 2026-09-28 by Wednesday morning 4901153c after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-28_KS-747-R2/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `ec32c40e2b1e2698d2e855a916f390d48dad1b45`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/security/src/security.openapi.ts , Blockchain/Dev/services/security/src/__tests__/ks747-keys-list-spec-declares-organizationid.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/security/src/security.openapi.ts` (product) and `Blockchain/Dev/services/security/src/__tests__/ks747-keys-list-spec-declares-organizationid.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
1	0	Blockchain/Dev/services/security/src/security.openapi.ts
50	0	Blockchain/Dev/services/security/src/__tests__/ks747-keys-list-spec-declares-organizationid.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (1 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 1 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 0.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/security/src/security.openapi.ts byte-exact incl. leading whitespace (apply mode strict): OK 1 line(s) byte-exact incl. leading whitespace (of 1; 1 line(s) added by the apply)` [a3i_indent.out: `OK 1 line(s) byte-exact incl. leading whitespace (of 1; 1 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/security/src/security.openapi.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/security/src/__tests__/ks747-keys-list-spec-declares-organizationid.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks747-keys-list-spec-declares-organizationid.test.ts fails at the untouched tip (2 failed / 5 run; controls green; assertion reds)` [red_first.json: failed=2 of total=5; red cell(s): ['KS-747: GET /api/security/keys publishes the organizationId its handler requires RED KS-747 A1: organizationId is declared as a REQUIRED query parameter', 'KS-747: GET /api/security/keys publishes the organizationId its handler requires RED KS-747 A2: the declared organizationId is a uuid-format string']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks747-keys-list-spec-declares-organizationid.test.ts passes with the product hunk (5 passed / 5 run)` [green_after.json: failed=0 of total=5, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=247 failed=0 | after: total=252 failed=0` · `NEW reds: []` [baseline_suite.json total=247 failed=0; after_suite.json total=252 failed=0]
- A6 [verbatim]: `PASS A6 whole services/security suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/security: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +51/-0 test=src/__tests__/ks747-keys-list-spec-declares-organizationid.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/security/src/security.openapi.ts` (+1/-0 per numstat.out) and the test file `Blockchain/Dev/services/security/src/__tests__/ks747-keys-list-spec-declares-organizationid.test.ts` (+50/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `ec32c40e2b1e2698d2e855a916f390d48dad1b45` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-28_KS-747-R2/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-28_KS-747-R2/checker.out`.

```diff
--- a/Blockchain/Dev/services/security/src/security.openapi.ts
+++ b/Blockchain/Dev/services/security/src/security.openapi.ts
@@ -807,6 +807,7 @@
     'Lists metadata only (no plaintext, no hash). Use /api/keys/validate ' +
     'to verify a specific key.',
   security: [{ bearerAuth: [] }],
+  request: { query: z.object({ organizationId: z.string().uuid() }) },
   responses: {
     400: commonErrorResponses[400],
     200: {
--- /dev/null
+++ b/Blockchain/Dev/services/security/src/__tests__/ks747-keys-list-spec-declares-organizationid.test.ts
@@ -0,0 +1,50 @@
+// KS-747: the published contract for GET /api/security/keys declared NO parameters, while the handler
+// (index.ts, the GET /api/keys route) answers 400 organizationId required without the query parameter.
+// Every spec-driven caller, Schemathesis included, was steered into the declared 400 and could never
+// reach the 200 branch. This file renders the document the generator publishes, from the same shared
+// registry the security module populates on import, and pins that the parameter is declared: in the
+// query, required, a uuid-format string. No server, no database, no network.
+import { describe, it, expect } from 'vitest';
+import { generateOpenApiDocument } from '@secuura/shared';
+import '../security.openapi';
+
+type AnyObj = Record<string, any>;
+
+const doc = generateOpenApiDocument({ title: 'security (ks747 pin)', version: '0.0.0' }) as AnyObj;
+
+function operation(path: string, method: string): AnyObj | undefined {
+  return doc.paths?.[path]?.[method];
+}
+
+function param(path: string, method: string, where: string, name: string): AnyObj | undefined {
+  const params: AnyObj[] = operation(path, method)?.parameters ?? [];
+  return params.find((p) => p.in === where && p.name === name);
+}
+
+describe('KS-747: GET /api/security/keys publishes the organizationId its handler requires', () => {
+  it('RED KS-747 A1: organizationId is declared as a REQUIRED query parameter', () => {
+    const p = param('/api/security/keys', 'get', 'query', 'organizationId');
+    expect({ declared: p !== undefined, required: p?.required }).toEqual({ declared: true, required: true });
+  });
+
+  it('RED KS-747 A2: the declared organizationId is a uuid-format string', () => {
+    const p = param('/api/security/keys', 'get', 'query', 'organizationId');
+    expect({ type: p?.schema?.type, format: p?.schema?.format }).toEqual({ type: 'string', format: 'uuid' });
+  });
+
+  it('control KS-747 C1: the GET operation is published, keeps bearerAuth, and still declares its 200 and 400', () => {
+    const op = operation('/api/security/keys', 'get');
+    expect(op).toBeDefined();
+    expect(op?.security).toEqual([{ bearerAuth: [] }]);
+    expect(Object.keys(op?.responses ?? {})).toEqual(expect.arrayContaining(['200', '400']));
+  });
+
+  it('control KS-747 C2: the sibling POST declares no parameters and keeps its request body', () => {
+    const op = operation('/api/security/keys', 'post');
+    expect({ params: (op?.parameters ?? []).length, body: op?.requestBody !== undefined }).toEqual({ params: 0, body: true });
+  });
+
+  it('control KS-747 C3: the sibling DELETE still declares its path parameter id', () => {
+    expect(param('/api/security/keys/{id}', 'delete', 'path', 'id')).toBeDefined();
+  });
+});
```
