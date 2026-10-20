# READY — KS-1508-FALSY1508-1 (Spark (DeepSeek V4 Flash), briefed, test_only (code_patch checker, MODE=test_only), jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1508_falsy_p1/out.md.checker/patch.diff`** (from `ls` at 15:40 2026-10-20; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1508_falsy_p1/out.md.checker/section_1.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden not located — no identity claim is made.

**Held 15:40 2026-10-20 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1508_falsy_p1/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `32964477fe8828eb78240150e8ab59bd8179f339`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (test-only) touched-file set == { Blockchain/Dev/services/originate/src/__tests__/ks1508-versionedbyid-is-server-set.test.ts } — the product file is untouched, as the ticket requires`
- Declared set [input.json suggested_test_file; product_file = the TAMPER TARGET, not modified]: `Blockchain/Dev/services/originate/src/__tests__/ks1508-versionedbyid-is-server-set.test.ts` (test) — equal to numstat.out's set (1 file); `Blockchain/Dev/services/originate/src/routes/certifications.ts` (product) untouched, measured above.
- numstat [out.md.checker/numstat.out, verbatim]:
```
11	0	Blockchain/Dev/services/originate/src/__tests__/ks1508-versionedbyid-is-server-set.test.ts
```
- Test hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (11 line(s)), and no tip line is re-added as a '+' (A3d)` — test section `+` lines 11 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 0.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/originate/src/__tests__/ks1508-versionedbyid-is-server-set.test.ts byte-exact incl. leading whitespace (apply mode strict): OK 11 line(s) byte-exact incl. leading whitespace (of 11; 11 line(s) added by the apply)` [a3i_indent.out: `OK 11 line(s) byte-exact incl. leading whitespace (of 11; 11 line(s) added by the apply)`]
- **TEST-ONLY (code_patch checker MODE=test_only)** — the product `Blockchain/Dev/services/originate/src/routes/certifications.ts` is the TAMPER TARGET and is BYTE-UNCHANGED: the run's `patch.diff` re-applied strictly (`git apply -p1`, scratch tempdir) to the tip content in input.json['files'] leaves it sha256 `590288484b463dea` = the tip's; numstat.out does not list it; no section names it. [checker.out mode line, verbatim]: `mode: test_only (tamper at Blockchain/Dev/services/originate/src/routes/certifications.ts:701)` · [tamper.out, verbatim]: `tampered /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/spark_secuura_2026-10-20_ks_1508_falsy_p1_153024/clone/Blockchain/Dev/services/originate/src/routes/certifications.ts:701: '        if (droppedVersionedById !== undefined) {' -> '        if (droppedVersionedById) {'` · [checker.out, verbatim]: `A4 (test-only): tamper reverted (Blockchain/Dev/services/originate/src/routes/certifications.ts back to the tip)` (tamper_revert.out EMPTY) · the tamper's `from` equals the product's tip line 701. [apply_product.out, verbatim]: `A5 (test-only): no product hunk — the test must be GREEN at the untouched tip`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=1 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1508-versionedbyid-is-server-set.test.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1508-versionedbyid-is-server-set.test.ts fails at the untouched tip (4 failed / 50 run; controls green; assertion reds)` [red_first.json: failed=4 of total=50; red cell(s): ['KS-1508 the drop is logged without the value RED KS-1508 F1 - a FALSY planted versionedById "" is dropped from the derived row AND logged once', 'KS-1508 the drop is logged without the value RED KS-1508 F1 - a FALSY planted versionedById null is dropped from the derived row AND logged once', 'KS-1508 the drop is logged without the value RED KS-1508 F1 - a FALSY planted versionedById 0 is dropped from the derived row AND logged once', 'KS-1508 the drop is logged without the value RED KS-1508 F1 - a FALSY planted versionedById false is dropped from the derived row AND logged once']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1508-versionedbyid-is-server-set.test.ts passes with the product hunk (50 passed / 50 run)` [green_after.json: failed=0 of total=50, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1625 failed=0 | after: total=1629 failed=0` · `NEW reds: []` [baseline_suite.json total=1625 failed=0; after_suite.json total=1629 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=1 +11/-0 test=src/__tests__/ks1508-versionedbyid-is-server-set.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** TEST-ONLY — ZERO PRODUCT BYTES: one file, the test `Blockchain/Dev/services/originate/src/__tests__/ks1508-versionedbyid-is-server-set.test.ts` (+11/-0 per numstat.out); the product `Blockchain/Dev/services/originate/src/routes/certifications.ts` is the tamper target and is byte-unchanged (sha256 590288484b463dea, measured). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict) — at the tip `32964477fe8828eb78240150e8ab59bd8179f339` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: the gate decides (test file only). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1508_falsy_p1/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1508_falsy_p1/checker.out`.

```diff
--- a/Blockchain/Dev/services/originate/src/__tests__/ks1508-versionedbyid-is-server-set.test.ts
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1508-versionedbyid-is-server-set.test.ts
@@ -230,6 +230,17 @@
     expect(JSON.stringify(calls)).not.toContain(OTHER_ORG_CONNECTOR);
     expect(JSON.stringify(calls[0][1])).toContain(TENANT);
   });
+  // KS-1508 falsy plants: every planted value in this file is truthy. The gate is "was a value supplied", not "is it truthy": a falsy plant is dropped from
+  // the row either way, so only the log line can tell `!== undefined` from a truthiness test. One it.each row per value, so each is reported on its own.
+  it.each([[''], [null], [0], [false]])('RED KS-1508 F1 - a FALSY planted versionedById %p is dropped from the derived row AND logged once', async (planted) => {
+    const { logger } = jest.requireMock('../utils/logger') as { logger: { info: jest.Mock; warn: jest.Mock } };
+    seedSource();
+    logger.info.mockClear(); logger.warn.mockClear();
+    const r = await send(ISSUER, '/api/certifications/issue', { type: 'DOCUMENT', parentDocumentId: SOURCE_ID, data: { title: 'c', versionedById: planted } });
+    const calls = [...logger.info.mock.calls, ...logger.warn.mock.calls].filter((c) => /versionedById/.test(String(c[0])));
+    expect(['versionedById', planted, r.status, Object.prototype.hasOwnProperty.call(r.rec.data, 'versionedById')]).toEqual(['versionedById', planted, 201, false]);
+    expect(['versionedById', planted, calls.length]).toEqual(['versionedById', planted, 1]);
+  });
   it('control - a certification derived row that did not carry the key logs nothing about it', async () => {
     const { logger } = jest.requireMock('../utils/logger') as { logger: { info: jest.Mock; warn: jest.Mock } };
     seedSource();
```
