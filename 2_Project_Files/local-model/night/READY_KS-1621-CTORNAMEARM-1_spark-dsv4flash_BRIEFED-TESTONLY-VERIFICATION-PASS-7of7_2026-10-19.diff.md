# READY — KS-1621-CTORNAMEARM-1 (Spark (DeepSeek V4 Flash), briefed, test_only (code_patch checker, MODE=test_only), vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1621_apigw/out.md.checker/patch.diff`** (from `ls` at 07:16 2026-10-19; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1621_apigw/out.md.checker/section_1.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden path `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1621_apigw/golden.diff/out.md.checker/patch.diff` does not exist — no identity claim is made.

**Held 07:16 2026-10-19 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1621_apigw/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `83ed01af70fd5ed6cca9ac66f28ddcb8a1034105`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (test-only) touched-file set == { Blockchain/Dev/services/api-gateway/src/__tests__/ks1543-document-types-catch-logs-the-error.test.ts } — the product file is untouched, as the ticket requires`
- Declared set [input.json suggested_test_file; product_file = the TAMPER TARGET, not modified]: `Blockchain/Dev/services/api-gateway/src/__tests__/ks1543-document-types-catch-logs-the-error.test.ts` (test) — equal to numstat.out's set (1 file); `Blockchain/Dev/services/api-gateway/src/routes/verification.ts` (product) untouched, measured above.
- numstat [out.md.checker/numstat.out, verbatim]:
```
12	0	Blockchain/Dev/services/api-gateway/src/__tests__/ks1543-document-types-catch-logs-the-error.test.ts
```
- Test hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (11 line(s)), and no tip line is re-added as a '+' (A3d)` — test section `+` lines 12 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 0.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/api-gateway/src/__tests__/ks1543-document-types-catch-logs-the-error.test.ts byte-exact incl. leading whitespace (apply mode strict): OK 11 line(s) byte-exact incl. leading whitespace (of 11; 12 line(s) added by the apply)` [a3i_indent.out: `OK 11 line(s) byte-exact incl. leading whitespace (of 11; 12 line(s) added by the apply)`]
- **TEST-ONLY (code_patch checker MODE=test_only)** — the product `Blockchain/Dev/services/api-gateway/src/routes/verification.ts` is the TAMPER TARGET and is BYTE-UNCHANGED: the run's `patch.diff` re-applied strictly (`git apply -p1`, scratch tempdir) to the tip content in input.json['files'] leaves it sha256 `bdaf380eaa3f6e2f` = the tip's; numstat.out does not list it; no section names it. [checker.out mode line, verbatim]: `mode: test_only (tamper at Blockchain/Dev/services/api-gateway/src/routes/verification.ts:1580)` · [tamper.out, verbatim]: `tampered /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/spark_secuura_2026-10-19_ks_1621_apigw_065543/clone/Blockchain/Dev/services/api-gateway/src/routes/verification.ts:1580: "      log('error', 'Failed to fetch document types', { error: err instanceof Error ? err.message : typeof err === 'string' ? err : typeof err === 'object' && err !== null ? 'thrown ' + (Object.getPrototypeOf(err)?.constructor?.name ?? 'object') + ' with fields [' + Object.keys(err).join(', ') + ']' : 'thrown ' + typeof err });" -> "      log('error', 'Failed to fetch document types', { error: err instanceof Error ? err.message : typeof err === 'string' ? err : typeof err === 'object' && err !== null ? 'thrown ' + 'Object' + ' with fields [' + Object.keys(err).join(', ') + ']' : 'thrown ' + typeof err });"` · [checker.out, verbatim]: `A4 (test-only): tamper reverted (Blockchain/Dev/services/api-gateway/src/routes/verification.ts back to the tip)` (tamper_revert.out EMPTY) · the tamper's `from` equals the product's tip line 1580. [apply_product.out, verbatim]: `A5 (test-only): no product hunk — the test must be GREEN at the untouched tip`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=1 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/api-gateway/src/__tests__/ks1543-document-types-catch-logs-the-error.test.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1543-document-types-catch-logs-the-error.test.ts fails at the untouched tip (1 failed / 10 run; controls green; assertion reds)` [red_first.json: failed=1 of total=10; red cell(s): ['KS-1619 part 3 - GET /api/document-types describes a thrown non-Error the way fail500 does RED KS-1621 D4 - a thrown instance of a class logs its constructor name and field names, never a value']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1543-document-types-catch-logs-the-error.test.ts passes with the product hunk (10 passed / 10 run)` [green_after.json: failed=0 of total=10, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1195 failed=0 | after: total=1196 failed=0` · `NEW reds: []` [baseline_suite.json total=1195 failed=0; after_suite.json total=1196 failed=0]
- A6 [verbatim]: `PASS A6 whole services/api-gateway suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/api-gateway: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=1 +12/-0 test=src/__tests__/ks1543-document-types-catch-logs-the-error.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** TEST-ONLY — ZERO PRODUCT BYTES: one file, the test `Blockchain/Dev/services/api-gateway/src/__tests__/ks1543-document-types-catch-logs-the-error.test.ts` (+12/-0 per numstat.out); the product `Blockchain/Dev/services/api-gateway/src/routes/verification.ts` is the tamper target and is byte-unchanged (sha256 bdaf380eaa3f6e2f, measured). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict) — at the tip `83ed01af70fd5ed6cca9ac66f28ddcb8a1034105` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: the gate decides (test file only). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1621_apigw/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1621_apigw/checker.out`.

```diff
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1543-document-types-catch-logs-the-error.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1543-document-types-catch-logs-the-error.test.ts
@@ -141,2 +141,14 @@
   });
+
+  it('RED KS-1621 D4 - a thrown instance of a class logs its constructor name and field names, never a value', async () => {
+    class Ks1621Fault {
+      code = 'E_KS1621';
+      detail = 'SECRET-VALUE-ks1621';
+    }
+    getAllDocumentTypes.mockRejectedValue(new Ks1621Fault());
+    const { status, body } = await documentTypes();
+    expect([status, body]).toEqual([500, CONSTANT_BODY]);
+    expect(errorLogs()).toEqual([['Failed to fetch document types', { error: 'thrown Ks1621Fault with fields [code, detail]' }]]);
+    expect(JSON.stringify(log.mock.calls)).not.toContain('SECRET-VALUE-ks1621');
+  });
 });
```
