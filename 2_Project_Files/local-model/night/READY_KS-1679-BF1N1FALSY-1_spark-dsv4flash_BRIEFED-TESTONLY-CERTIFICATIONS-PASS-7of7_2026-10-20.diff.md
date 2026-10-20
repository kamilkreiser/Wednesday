# READY — KS-1679-BF1N1FALSY-1 (Spark (DeepSeek V4 Flash), briefed, test_only (code_patch checker, MODE=test_only), jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1679_p2/out.md.checker/patch.diff`** (from `ls` at 13:48 2026-10-20; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1679_p2/out.md.checker/section_1.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; CONTENT-compared against the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1679_p2-control/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1); change lines (`+`/`-`, ordered) IDENTICAL in every file; body lines (context included) identical in every file; hunk headers identical; APPLIED RESULT IDENTICAL: both patches applied strictly (`git apply -p1`, scratch tempdir) to the tip content carried in input.json['files'] yield byte-identical files (ks1679-the-same-caller-spread-still-overwrites.test.ts, sha256 equal).

**Held 13:48 2026-10-20 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1679_p2/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `f01ba49da56d3d55204caa02ab3348f94d63b9c0`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (test-only) touched-file set == { Blockchain/Dev/services/originate/src/__tests__/ks1679-the-same-caller-spread-still-overwrites.test.ts } — the product file is untouched, as the ticket requires`
- Declared set [input.json suggested_test_file; product_file = the TAMPER TARGET, not modified]: `Blockchain/Dev/services/originate/src/__tests__/ks1679-the-same-caller-spread-still-overwrites.test.ts` (test) — equal to numstat.out's set (1 file); `Blockchain/Dev/services/originate/src/routes/certifications.ts` (product) untouched, measured above.
- numstat [out.md.checker/numstat.out, verbatim]:
```
12	0	Blockchain/Dev/services/originate/src/__tests__/ks1679-the-same-caller-spread-still-overwrites.test.ts
```
- Test hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (12 line(s)), and no tip line is re-added as a '+' (A3d)` — test section `+` lines 12 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 0.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/originate/src/__tests__/ks1679-the-same-caller-spread-still-overwrites.test.ts byte-exact incl. leading whitespace (apply mode strict): OK 12 line(s) byte-exact incl. leading whitespace (of 12; 12 line(s) added by the apply)` [a3i_indent.out: `OK 12 line(s) byte-exact incl. leading whitespace (of 12; 12 line(s) added by the apply)`]
- **TEST-ONLY (code_patch checker MODE=test_only)** — the product `Blockchain/Dev/services/originate/src/routes/certifications.ts` is the TAMPER TARGET and is BYTE-UNCHANGED: the run's `patch.diff` re-applied strictly (`git apply -p1`, scratch tempdir) to the tip content in input.json['files'] leaves it sha256 `6abd05c5ea2f25f1` = the tip's; numstat.out does not list it; no section names it. [checker.out mode line, verbatim]: `mode: test_only (tamper at Blockchain/Dev/services/originate/src/routes/certifications.ts:654)` · [tamper.out, verbatim]: `tampered /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/spark_secuura_2026-10-20_ks_1679_p2_134301/clone/Blockchain/Dev/services/originate/src/routes/certifications.ts:654: '        if (droppedCertificationId !== undefined) {' -> '        if (droppedCertificationId) {'` · [checker.out, verbatim]: `A4 (test-only): tamper reverted (Blockchain/Dev/services/originate/src/routes/certifications.ts back to the tip)` (tamper_revert.out EMPTY) · the tamper's `from` equals the product's tip line 654. [apply_product.out, verbatim]: `A5 (test-only): no product hunk — the test must be GREEN at the untouched tip`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=1 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1679-the-same-caller-spread-still-overwrites.test.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1679-the-same-caller-spread-still-overwrites.test.ts fails at the untouched tip (1 failed / 14 run; controls green; assertion reds)` [red_first.json: failed=1 of total=14; red cell(s): ['KS-1679 the drop is logged without the value RED KS-1679 R6: a FALSY planted value (empty string, null, 0, false) is dropped AND logged for both keys, not only a truthy one']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1679-the-same-caller-spread-still-overwrites.test.ts passes with the product hunk (14 passed / 14 run)` [green_after.json: failed=0 of total=14, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1576 failed=0 | after: total=1577 failed=0` · `NEW reds: []` [baseline_suite.json total=1576 failed=0; after_suite.json total=1577 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=1 +12/-0 test=src/__tests__/ks1679-the-same-caller-spread-still-overwrites.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** TEST-ONLY — ZERO PRODUCT BYTES: one file, the test `Blockchain/Dev/services/originate/src/__tests__/ks1679-the-same-caller-spread-still-overwrites.test.ts` (+12/-0 per numstat.out); the product `Blockchain/Dev/services/originate/src/routes/certifications.ts` is the tamper target and is byte-unchanged (sha256 6abd05c5ea2f25f1, measured). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict) — at the tip `f01ba49da56d3d55204caa02ab3348f94d63b9c0` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: the gate decides (test file only). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1679_p2/input.json`. Brief (located from the run dir's own name under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1679_p2/KS-1679.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1679_p2/checker.out`.

```diff
--- a/Blockchain/Dev/services/originate/src/__tests__/ks1679-the-same-caller-spread-still-overwrites.test.ts
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1679-the-same-caller-spread-still-overwrites.test.ts
@@ -165,6 +165,18 @@ describe('KS-1679 the drop is logged without the value', () => {
     expect(JSON.stringify(logged())).not.toContain(PLANTED_TIME);
     expect(JSON.stringify(named('certifiedAt')[0][1])).toContain(TENANT);
   });
+  // KS-1679 gate BF1 N1: every planted value so far was truthy. The gate is "was a value supplied", not "is it truthy": a falsy plant is dropped from the row
+  // either way, so only the log line can tell the two apart.
+  it('RED KS-1679 R6: a FALSY planted value (empty string, null, 0, false) is dropped AND logged for both keys, not only a truthy one', async () => {
+    for (const planted of ['', null, 0, false]) {
+      for (const key of ['certificationId', 'certifiedAt']) {
+        logger.info.mockClear(); logger.warn.mockClear();
+        const r = await issue(ISSUER, { [key]: planted });
+        expect([key, planted, r.status, r.rec.data[key] === planted]).toEqual([key, planted, 201, false]);
+        expect([key, planted, named(key).length]).toEqual([key, planted, 1]);
+      }
+    }
+  });
   it('CONTROL KS-1679 C3: a derived row that carried neither key logs nothing about them', async () => {
     logger.info.mockClear(); logger.warn.mockClear();
     const r = await issue(ISSUER, {});
```
