# READY — KS-591-KS-591-CUSTODY-1 (Spark DeepSeek V4 Flash, briefed, code_patch, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-07_KS-591-transfer-custody-holder-id-uuid/out.md.checker/patch.diff`** (from `ls` at 11:57 2026-10-07; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-07_KS-591-transfer-custody-holder-id-uuid/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-07_KS-591-transfer-custody-holder-id-uuid/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-07_KS-591-transfer-custody-holder-id-uuid/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-07_KS-591-transfer-custody-holder-id-uuid-control/out.md.checker/patch.diff` rc 0, Wednesday late-morning seat).

**Held 11:57 2026-10-07 by Wednesday late-morning seat after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-07_KS-591-transfer-custody-holder-id-uuid/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `69f2045af2a4f5f0b83b2f76c62514512abdc7b5`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/originate/src/originate.openapi.ts , Blockchain/Dev/services/originate/src/__tests__/ks591-transfer-custody-new-holder-id-is-a-uuid.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/originate.openapi.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks591-transfer-custody-new-holder-id-is-a-uuid.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
1	1	Blockchain/Dev/services/originate/src/originate.openapi.ts
39	0	Blockchain/Dev/services/originate/src/__tests__/ks591-transfer-custody-new-holder-id-is-a-uuid.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (1 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 1 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 1.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/originate/src/originate.openapi.ts byte-exact incl. leading whitespace (apply mode strict): OK 1 line(s) byte-exact incl. leading whitespace (of 1; 1 line(s) added by the apply)` [a3i_indent.out: `OK 1 line(s) byte-exact incl. leading whitespace (of 1; 1 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/originate.openapi.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks591-transfer-custody-new-holder-id-is-a-uuid.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks591-transfer-custody-new-holder-id-is-a-uuid.test.ts fails at the untouched tip (1 failed / 3 run; controls green; assertion reds)` [red_first.json: failed=1 of total=3; red cell(s): ['KS-591: TransferCustodyRequest publishes newHolderId as a UUID, as the handler enforces RED KS-591 TC1: TransferCustodyRequest.newHolderId carries format uuid']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks591-transfer-custody-new-holder-id-is-a-uuid.test.ts passes with the product hunk (3 passed / 3 run)` [green_after.json: failed=0 of total=3, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1074 failed=0 | after: total=1077 failed=0` · `NEW reds: []` [baseline_suite.json total=1074 failed=0; after_suite.json total=1077 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +40/-1 test=src/__tests__/ks591-transfer-custody-new-holder-id-is-a-uuid.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/originate.openapi.ts` (+1/-1 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks591-transfer-custody-new-holder-id-is-a-uuid.test.ts` (+39/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `69f2045af2a4f5f0b83b2f76c62514512abdc7b5` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-07_KS-591-transfer-custody-holder-id-uuid/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-07_KS-591-transfer-custody-holder-id-uuid/checker.out`.

```diff
--- a/Blockchain/Dev/services/originate/src/originate.openapi.ts
+++ b/Blockchain/Dev/services/originate/src/originate.openapi.ts
@@ -1629,3 +1629,3 @@
     .object({
-      newHolderId: z.string().optional().openapi({ description: 'Resolved new rights-holder user id.' }),
+      newHolderId: z.string().uuid().optional().openapi({ description: 'Resolved new rights-holder user id.' }),
       newHolderEmail: z.string().optional().openapi({
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks591-transfer-custody-new-holder-id-is-a-uuid.test.ts
@@ -0,0 +1,39 @@
+// KS-591 (2026-10-06 addendum, sweep full-ks-571-2026-10-06T10-09-50Z-slot4): POST /api/documents/{id}/transfer-custody
+// refuses a non-UUID newHolderId with 400 "newHolderId must be a valid UUID" (routes/documents.ts, the KS-697 guard
+// before the ::uuid cast), but the published TransferCustodyRequest declared newHolderId as a bare string - so a
+// spec-valid body was refused (6 positive_data_acceptance cases). The spec now says format: uuid, as the handler
+// enforces. This file renders the document the generator publishes, from the shared registry the originate module
+// populates on import. No server, no database, no network.
+import { generateOpenApiDocument } from '@secuura/shared';
+import '../originate.openapi';
+
+type AnyObj = Record<string, any>;
+
+const doc = generateOpenApiDocument({ title: 'originate (ks591 custody pin)', version: '0.0.0' }) as AnyObj;
+
+const CUSTODY = '/api/documents/{id}/transfer-custody';
+
+function custodySchema(): AnyObj | undefined {
+  return doc.components?.schemas?.TransferCustodyRequest;
+}
+
+describe('KS-591: TransferCustodyRequest publishes newHolderId as a UUID, as the handler enforces', () => {
+  it('RED KS-591 TC1: TransferCustodyRequest.newHolderId carries format uuid', () => {
+    expect(custodySchema()?.properties?.newHolderId?.format).toBe('uuid');
+  });
+
+  it('control KS-591 TCC1: newHolderId stays an optional string, and newHolderEmail is unchanged', () => {
+    const s = custodySchema();
+    expect(s?.properties?.newHolderId?.type).toBe('string');
+    expect(s?.required ?? []).not.toContain('newHolderId');
+    expect(s?.properties?.newHolderEmail?.type).toBe('string');
+    expect(s?.properties?.newHolderEmail?.format).toBeUndefined();
+  });
+
+  it('control KS-591 TCC2: the operation still posts a TransferCustodyRequest and the example still pins only the email', () => {
+    expect(doc.paths?.[CUSTODY]?.post?.requestBody?.content?.['application/json']?.schema?.$ref).toBe(
+      '#/components/schemas/TransferCustodyRequest',
+    );
+    expect(Object.keys(custodySchema()?.example ?? {}).sort()).toEqual(['effectiveAt', 'newHolderEmail', 'reason']);
+  });
+});
```
