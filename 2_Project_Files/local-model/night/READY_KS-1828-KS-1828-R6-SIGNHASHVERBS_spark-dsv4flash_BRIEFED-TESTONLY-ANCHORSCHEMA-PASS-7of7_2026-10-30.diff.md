# READY — KS-1828-KS-1828-R6-SIGNHASHVERBS (Spark (DeepSeek V4 Flash), briefed, test_only (code_patch checker, MODE=test_only), vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1828_p1_signhash_other_verbs/out.md.checker/patch.diff`** (from `ls` at 01:45 2026-10-30; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1828_p1_signhash_other_verbs/out.md.checker/section_1.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden not located — no identity claim is made.

**Held 01:45 2026-10-30 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1828_p1_signhash_other_verbs/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `5a5c4d2b353fa4091762630df8bfaea26d6b9245`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (test-only) touched-file set == { Blockchain/Dev/services/anchoring/src/__tests__/ks1454-signature-hash-is-accepted-and-anchored-on-the-sign-verb.test.ts } — the product file is untouched, as the ticket requires`
- Declared set [input.json suggested_test_file; product_file = the TAMPER TARGET, not modified]: `Blockchain/Dev/services/anchoring/src/__tests__/ks1454-signature-hash-is-accepted-and-anchored-on-the-sign-verb.test.ts` (test) — equal to numstat.out's set (1 file); `Blockchain/Dev/services/anchoring/src/anchorSchema.ts` (product) untouched, measured above.
- numstat [out.md.checker/numstat.out, verbatim]:
```
16	1	Blockchain/Dev/services/anchoring/src/__tests__/ks1454-signature-hash-is-accepted-and-anchored-on-the-sign-verb.test.ts
```
- Test hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (13 line(s)), and no tip line is re-added as a '+' (A3d)` — test section `+` lines 16 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 1.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/anchoring/src/__tests__/ks1454-signature-hash-is-accepted-and-anchored-on-the-sign-verb.test.ts byte-exact incl. leading whitespace (apply mode strict): OK 13 line(s) byte-exact incl. leading whitespace (of 13; 16 line(s) added by the apply)` [a3i_indent.out: `OK 13 line(s) byte-exact incl. leading whitespace (of 13; 16 line(s) added by the apply)`]
- **TEST-ONLY (code_patch checker MODE=test_only)** — the product `Blockchain/Dev/services/anchoring/src/anchorSchema.ts` is the TAMPER TARGET and is BYTE-UNCHANGED: the run's `patch.diff` re-applied strictly (`git apply -p1`, scratch tempdir) to the tip content in input.json['files'] leaves it sha256 `ca46ef18214bd658` = the tip's; numstat.out does not list it; no section names it. [checker.out mode line, verbatim]: `mode: test_only (tamper at Blockchain/Dev/services/anchoring/src/anchorSchema.ts:301)` · [tamper.out, verbatim]: `tampered /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/spark_secuura_2026-10-30_ks_1828_p1_signhash_other_verbs_012701/clone/Blockchain/Dev/services/anchoring/src/anchorSchema.ts:301: "  if (data.metadata?.signatureHash !== undefined && data.metadata.documentType !== 'sign') {" -> "  if (data.metadata?.signatureHash !== undefined && data.metadata.documentType !== 'sign' && data.metadata.documentType !== 'declare') {"` · [checker.out, verbatim]: `A4 (test-only): tamper reverted (Blockchain/Dev/services/anchoring/src/anchorSchema.ts back to the tip)` (tamper_revert.out EMPTY) · the tamper's `from` equals the product's tip line 301. [apply_product.out, verbatim]: `A5 (test-only): no product hunk — the test must be GREEN at the untouched tip`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=1 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/anchoring/src/__tests__/ks1454-signature-hash-is-accepted-and-anchored-on-the-sign-verb.test.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1454-signature-hash-is-accepted-and-anchored-on-the-sign-verb.test.ts fails at the untouched tip (1 failed / 40 run; controls green; assertion reds)` [red_first.json: failed=1 of total=40; red cell(s): ['KS-1454: metadata.signatureHash on the sign verb RED KS-1828 R6: a signatureHash on the declare verb is refused, not anchored']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1454-signature-hash-is-accepted-and-anchored-on-the-sign-verb.test.ts passes with the product hunk (40 passed / 40 run)` [green_after.json: failed=0 of total=40, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=497 failed=1 | after: total=523 failed=1` · `NEW reds: []` [baseline_suite.json total=497 failed=1; after_suite.json total=523 failed=1]
- A6 [verbatim]: `PASS A6 whole services/anchoring suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/anchoring: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=1 +16/-1 test=src/__tests__/ks1454-signature-hash-is-accepted-and-anchored-on-the-sign-verb.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** TEST-ONLY — ZERO PRODUCT BYTES: one file, the test `Blockchain/Dev/services/anchoring/src/__tests__/ks1454-signature-hash-is-accepted-and-anchored-on-the-sign-verb.test.ts` (+16/-1 per numstat.out); the product `Blockchain/Dev/services/anchoring/src/anchorSchema.ts` is the tamper target and is byte-unchanged (sha256 ca46ef18214bd658, measured). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict) — at the tip `5a5c4d2b353fa4091762630df8bfaea26d6b9245` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: the gate decides (test file only). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1828_p1_signhash_other_verbs/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1828_p1_signhash_other_verbs/checker.out`.

```diff
--- a/Blockchain/Dev/services/anchoring/src/__tests__/ks1454-signature-hash-is-accepted-and-anchored-on-the-sign-verb.test.ts
+++ b/Blockchain/Dev/services/anchoring/src/__tests__/ks1454-signature-hash-is-accepted-and-anchored-on-the-sign-verb.test.ts
@@ -6,2 +6,2 @@
-import { anchorDocumentSchema, buildFlatAnchorMetadataPayload } from '../anchorSchema';
+import { ACCEPTED_LIFECYCLE_VERBS, anchorDocumentSchema, buildFlatAnchorMetadataPayload } from '../anchorSchema';
 import { toCardanoMetadatum } from '../cardano/cardanoMetadatum';
@@ -33,4 +33,19 @@
   it('RED KS-1454 R3: a signatureHash with no documentType is refused', () => {
     const result = anchorDocumentSchema.safeParse({ ...BASE_BODY, metadata: { signatureHash: SIG } });
     expect(result.success).toBe(false);
+  });
+
+  // KS-1828 (gate 18 mutant X8): R2 and R3 pin the sign-only rule for `upload` and for no verb only, so a refinement that also admitted `declare` stayed 23 of 23. Every other accepted verb is driven here.
+  const OTHER_VERBS = ACCEPTED_LIFECYCLE_VERBS.filter((verb) => verb !== 'sign');
+
+  it.each(OTHER_VERBS)('RED KS-1828 R6: a signatureHash on the %s verb is refused, not anchored', (verb) => {
+    const result = anchorDocumentSchema.safeParse({ ...BASE_BODY, metadata: { documentType: verb, signatureHash: SIG } });
+    expect(result.success).toBe(false);
+  });
+
+  it('control KS-1828 C5: the verbs driven by R6 include declare and upload and never sign', () => {
+    expect(OTHER_VERBS).toContain('declare');
+    expect(OTHER_VERBS).toContain('upload');
+    expect(OTHER_VERBS).not.toContain('sign');
+    expect(ACCEPTED_LIFECYCLE_VERBS).toContain('sign');
   });
```
