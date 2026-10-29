# READY — KS-1817-KS-1817-R4-FALLBACKTEXT (Spark (DeepSeek V4 Flash), briefed, test_only (code_patch checker, MODE=test_only), jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1817_p1_fallback_text/out.md.checker/patch.diff`** (from `ls` at 01:45 2026-10-30; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1817_p1_fallback_text/out.md.checker/section_1.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden not located — no identity claim is made.

**Held 01:45 2026-10-30 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1817_p1_fallback_text/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `5a5c4d2b353fa4091762630df8bfaea26d6b9245`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (test-only) touched-file set == { Blockchain/Dev/services/originate/src/__tests__/ks1802-seed-demo-users-survives-a-hostile-throw-in-the-loop-catch.test.ts } — the product file is untouched, as the ticket requires`
- Declared set [input.json suggested_test_file; product_file = the TAMPER TARGET, not modified]: `Blockchain/Dev/services/originate/src/__tests__/ks1802-seed-demo-users-survives-a-hostile-throw-in-the-loop-catch.test.ts` (test) — equal to numstat.out's set (1 file); `Blockchain/Dev/services/originate/src/routes/adminConfig.ts` (product) untouched, measured above.
- numstat [out.md.checker/numstat.out, verbatim]:
```
15	0	Blockchain/Dev/services/originate/src/__tests__/ks1802-seed-demo-users-survives-a-hostile-throw-in-the-loop-catch.test.ts
```
- Test hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (14 line(s)), and no tip line is re-added as a '+' (A3d)` — test section `+` lines 15 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 0.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/originate/src/__tests__/ks1802-seed-demo-users-survives-a-hostile-throw-in-the-loop-catch.test.ts byte-exact incl. leading whitespace (apply mode strict): OK 14 line(s) byte-exact incl. leading whitespace (of 14; 15 line(s) added by the apply)` [a3i_indent.out: `OK 14 line(s) byte-exact incl. leading whitespace (of 14; 15 line(s) added by the apply)`]
- **TEST-ONLY (code_patch checker MODE=test_only)** — the product `Blockchain/Dev/services/originate/src/routes/adminConfig.ts` is the TAMPER TARGET and is BYTE-UNCHANGED: the run's `patch.diff` re-applied strictly (`git apply -p1`, scratch tempdir) to the tip content in input.json['files'] leaves it sha256 `3775c4092b3c603d` = the tip's; numstat.out does not list it; no section names it. [checker.out mode line, verbatim]: `mode: test_only (tamper at Blockchain/Dev/services/originate/src/routes/adminConfig.ts:154)` · [tamper.out, verbatim]: `tampered /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/spark_secuura_2026-10-30_ks_1817_p1_fallback_text_013108/clone/Blockchain/Dev/services/originate/src/routes/adminConfig.ts:154: "    return 'thrown value that could not be described';" -> '    return undefined;'` · [checker.out, verbatim]: `A4 (test-only): tamper reverted (Blockchain/Dev/services/originate/src/routes/adminConfig.ts back to the tip)` (tamper_revert.out EMPTY) · the tamper's `from` equals the product's tip line 154. [apply_product.out, verbatim]: `A5 (test-only): no product hunk — the test must be GREEN at the untouched tip`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=1 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1802-seed-demo-users-survives-a-hostile-throw-in-the-loop-catch.test.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1802-seed-demo-users-survives-a-hostile-throw-in-the-loop-catch.test.ts fails at the untouched tip (1 failed / 7 run; controls green; assertion reds)` [red_first.json: failed=1 of total=7; red cell(s): ['KS-1802: seed-demo-users keeps going when a user insert throws a hostile value RED KS-1817 R4: every insert rejecting with a revoked Proxy or a throwing message getter logs the fixed fallback text, once per user']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1802-seed-demo-users-survives-a-hostile-throw-in-the-loop-catch.test.ts passes with the product hunk (7 passed / 7 run)` [green_after.json: failed=0 of total=7, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1818 failed=0 | after: total=1819 failed=0` · `NEW reds: []` [baseline_suite.json total=1818 failed=0; after_suite.json total=1819 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=1 +15/-0 test=src/__tests__/ks1802-seed-demo-users-survives-a-hostile-throw-in-the-loop-catch.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** TEST-ONLY — ZERO PRODUCT BYTES: one file, the test `Blockchain/Dev/services/originate/src/__tests__/ks1802-seed-demo-users-survives-a-hostile-throw-in-the-loop-catch.test.ts` (+15/-0 per numstat.out); the product `Blockchain/Dev/services/originate/src/routes/adminConfig.ts` is the tamper target and is byte-unchanged (sha256 3775c4092b3c603d, measured). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict) — at the tip `5a5c4d2b353fa4091762630df8bfaea26d6b9245` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: the gate decides (test file only). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1817_p1_fallback_text/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1817_p1_fallback_text/checker.out`.

```diff
--- a/Blockchain/Dev/services/originate/src/__tests__/ks1802-seed-demo-users-survives-a-hostile-throw-in-the-loop-catch.test.ts
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1802-seed-demo-users-survives-a-hostile-throw-in-the-loop-catch.test.ts
@@ -112,3 +112,18 @@
+  // KS-1817 (gate 17 mutant X3): R1-R3 pin the HTTP report and the counts for a hostile thrown value, but nothing pinned what is LOGGED for it, so the fixed fallback of readableErrorMessage could be
+  // changed or dropped (the catch returning undefined) and every cell stayed green. The fallback text is also the one fail500 and migrate-tenant-data use.
+  it('RED KS-1817 R4: every insert rejecting with a revoked Proxy or a throwing message getter logs the fixed fallback text, once per user', async () => {
+    for (const hostile of [revokedProxy(), throwingMessageGetter()]) {
+      mockLogError.mockReset();
+      mockExecuteRaw.mockReset();
+      mockExecuteRaw.mockRejectedValue(hostile);
+      await seed();
+      const logged = mockLogError.mock.calls.filter((call) => call[0] === 'Demo user seed failed');
+      expect(logged).toHaveLength(USERS);
+      expect(logged[0][1]).toEqual({ email: 'james.wilson@ox.ac.uk', error: 'thrown value that could not be described' });
+      expect(logged.map((call) => (call[1] as { error: unknown }).error)).toEqual(Array(USERS).fill('thrown value that could not be described'));
+    }
+  });
+
   it('control KS-1802 C1: an ordinary Error on every insert is reported as 14 failed and its message is logged', async () => {
     mockExecuteRaw.mockRejectedValue(new Error('ks1802 ordinary'));
     expect(await seed()).toEqual({ status: 200, body: { success: true, seededUsers: 0, created: 0, alreadyPresent: 0, failed: USERS } });
```
