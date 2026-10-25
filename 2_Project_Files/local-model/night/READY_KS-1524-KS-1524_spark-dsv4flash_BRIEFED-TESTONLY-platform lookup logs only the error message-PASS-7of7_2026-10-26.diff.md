# READY — KS-1524-KS-1524 (Spark (DeepSeek V4 Flash), briefed, test_only (code_patch checker, MODE=test_only), vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-26_ks_1524_p1/out.md.checker/patch.diff`** (from `ls` at 09:20 2026-10-26; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-26_ks_1524_p1/out.md.checker/section_1.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden path `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1524_p1/golden.diff/out.md.checker/patch.diff` does not exist — no identity claim is made.

**Held 09:20 2026-10-26 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-26_ks_1524_p1/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `1ae6f17d19a8d973a77714dfe08dee0486b0af65`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (test-only) touched-file set == { Blockchain/Dev/services/api-gateway/src/__tests__/ks1510-document-lookup-logs-the-thrown-error.test.ts } — the product file is untouched, as the ticket requires`
- Declared set [input.json suggested_test_file; product_file = the TAMPER TARGET, not modified]: `Blockchain/Dev/services/api-gateway/src/__tests__/ks1510-document-lookup-logs-the-thrown-error.test.ts` (test) — equal to numstat.out's set (1 file); `Blockchain/Dev/services/api-gateway/src/routes/platform.ts` (product) untouched, measured above.
- numstat [out.md.checker/numstat.out, verbatim]:
```
9	1	Blockchain/Dev/services/api-gateway/src/__tests__/ks1510-document-lookup-logs-the-thrown-error.test.ts
```
- Test hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (7 line(s)), and no tip line is re-added as a '+' (A3d)` — test section `+` lines 9 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 1.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/api-gateway/src/__tests__/ks1510-document-lookup-logs-the-thrown-error.test.ts byte-exact incl. leading whitespace (apply mode strict): OK 7 line(s) byte-exact incl. leading whitespace (of 7; 8 line(s) added by the apply)` [a3i_indent.out: `OK 7 line(s) byte-exact incl. leading whitespace (of 7; 8 line(s) added by the apply)`]
- **TEST-ONLY (code_patch checker MODE=test_only)** — the product `Blockchain/Dev/services/api-gateway/src/routes/platform.ts` is the TAMPER TARGET and is BYTE-UNCHANGED: the run's `patch.diff` re-applied strictly (`git apply -p1`, scratch tempdir) to the tip content in input.json['files'] leaves it sha256 `a175b25d6f3f225b` = the tip's; numstat.out does not list it; no section names it. [checker.out mode line, verbatim]: `mode: test_only (tamper at Blockchain/Dev/services/api-gateway/src/routes/platform.ts:1143)` · [tamper.out, verbatim]: `tampered /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/spark_secuura_2026-10-26_ks_1524_p1_090611/clone/Blockchain/Dev/services/api-gateway/src/routes/platform.ts:1143: "        logger.error('Document lookup failed (GET /api/platform/document-lookup)', { error: err instanceof Error ? err.message : typeof err === 'string' ? err : typeof err === 'object' && err !== null ? 'thrown ' + (Object.getPrototypeOf(err)?.constructor?.name ?? 'object') + ' with fields [' + Object.keys(err).join(', ') + ']' : 'thrown ' + typeof err });" -> "        logger.error('Document lookup failed (GET /api/platform/document-lookup)', { error: err instanceof Error ? err.stack : typeof err === 'string' ? err : typeof err === 'object' && err !== null ? 'thrown ' + (Object.getPrototypeOf(err)?.constructor?.name ?? 'object') + ' with fields [' + Object.keys(err).join(', ') + ']' : 'thrown ' + typeof err });"` · [checker.out, verbatim]: `A4 (test-only): tamper reverted (Blockchain/Dev/services/api-gateway/src/routes/platform.ts back to the tip)` (tamper_revert.out EMPTY) · the tamper's `from` equals the product's tip line 1143. [apply_product.out, verbatim]: `A5 (test-only): no product hunk — the test must be GREEN at the untouched tip`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=1 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/api-gateway/src/__tests__/ks1510-document-lookup-logs-the-thrown-error.test.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1510-document-lookup-logs-the-thrown-error.test.ts fails at the untouched tip (1 failed / 9 run; controls green; assertion reds)` [red_first.json: failed=1 of total=9; red cell(s): ['KS-1510 document-lookup logs the thrown error RED KS-1510 L5 - a thrown Error logs exactly its message, not its stack and not String(err)']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1510-document-lookup-logs-the-thrown-error.test.ts passes with the product hunk (9 passed / 9 run)` [green_after.json: failed=0 of total=9, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1175 failed=0 | after: total=1176 failed=0` · `NEW reds: []` [baseline_suite.json total=1175 failed=0; after_suite.json total=1176 failed=0]
- A6 [verbatim]: `PASS A6 whole services/api-gateway suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/api-gateway: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=1 +9/-1 test=src/__tests__/ks1510-document-lookup-logs-the-thrown-error.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** TEST-ONLY — ZERO PRODUCT BYTES: one file, the test `Blockchain/Dev/services/api-gateway/src/__tests__/ks1510-document-lookup-logs-the-thrown-error.test.ts` (+9/-1 per numstat.out); the product `Blockchain/Dev/services/api-gateway/src/routes/platform.ts` is the tamper target and is byte-unchanged (sha256 a175b25d6f3f225b, measured). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict) — at the tip `1ae6f17d19a8d973a77714dfe08dee0486b0af65` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: the gate decides (test file only). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-26_ks_1524_p1/input.json`. Brief (given by --brief; its `# ` heading names KS-1524): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1524_p1/KS-1524.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-26_ks_1524_p1/checker.out`.

```diff
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1510-document-lookup-logs-the-thrown-error.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1510-document-lookup-logs-the-thrown-error.test.ts
@@ -92,7 +92,15 @@
     expect([r.status, r.body]).toEqual([500, CONSTANT_BODY]);
     expect(logged()).toEqual([[CONTEXT, { error: 'platform registry exploded' }]]);
   });
-
+
+  // KS-1524 (b): an Error logs its message and ONLY its message. L1 asserts just that the text contains ECONNREFUSED, so logging err.stack or String(err) stays green there.
+  it('RED KS-1510 L5 - a thrown Error logs exactly its message, not its stack and not String(err)', async () => {
+    stubQueryRejecting(new Error('platform registry exploded'));
+    const r = await lookup('?hash=abc');
+    expect([r.status, r.body]).toEqual([500, CONSTANT_BODY]);
+    expect(logged()).toEqual([[CONTEXT, { error: 'platform registry exploded' }]]);
+  });
+
   it('RED KS-1510 L3 - a thrown object logs its TYPE and FIELD NAMES, never its values', async () => {
     stubQueryRejecting({ code: '57P01', detail: 'SECRET-DETAIL-VALUE' });
     const r = await lookup('?documentId=d1');
```
