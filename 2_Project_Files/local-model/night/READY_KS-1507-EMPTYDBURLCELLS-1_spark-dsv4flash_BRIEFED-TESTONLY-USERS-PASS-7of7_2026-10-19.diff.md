# READY — KS-1507-EMPTYDBURLCELLS-1 (Spark (DeepSeek V4 Flash), briefed, test_only (code_patch checker, MODE=test_only), vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1507_p1/out.md.checker/patch.diff`** (from `ls` at 10:44 2026-10-19; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1507_p1/out.md.checker/section_1.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1507_p1/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1507_p1-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 10:44 2026-10-19 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1507_p1/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `78cb3c3939e319332e387ffecb075a169edd4a39`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (test-only) touched-file set == { Blockchain/Dev/services/auth/src/__tests__/ks1477-the-verification-store-is-memory-only-only-when-no-database-is-configured.test.ts } — the product file is untouched, as the ticket requires`
- Declared set [input.json suggested_test_file; product_file = the TAMPER TARGET, not modified]: `Blockchain/Dev/services/auth/src/__tests__/ks1477-the-verification-store-is-memory-only-only-when-no-database-is-configured.test.ts` (test) — equal to numstat.out's set (1 file); `Blockchain/Dev/services/auth/src/routes/users.ts` (product) untouched, measured above.
- numstat [out.md.checker/numstat.out, verbatim]:
```
21	1	Blockchain/Dev/services/auth/src/__tests__/ks1477-the-verification-store-is-memory-only-only-when-no-database-is-configured.test.ts
```
- Test hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (18 line(s)), and no tip line is re-added as a '+' (A3d)` — test section `+` lines 21 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 1.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/auth/src/__tests__/ks1477-the-verification-store-is-memory-only-only-when-no-database-is-configured.test.ts byte-exact incl. leading whitespace (apply mode strict): OK 18 line(s) byte-exact incl. leading whitespace (of 18; 20 line(s) added by the apply)` [a3i_indent.out: `OK 18 line(s) byte-exact incl. leading whitespace (of 18; 20 line(s) added by the apply)`]
- **TEST-ONLY (code_patch checker MODE=test_only)** — the product `Blockchain/Dev/services/auth/src/routes/users.ts` is the TAMPER TARGET and is BYTE-UNCHANGED: the run's `patch.diff` re-applied strictly (`git apply -p1`, scratch tempdir) to the tip content in input.json['files'] leaves it sha256 `7cdf68ac37c460f1` = the tip's; numstat.out does not list it; no section names it. [checker.out mode line, verbatim]: `mode: test_only (tamper at Blockchain/Dev/services/auth/src/routes/users.ts:1197)` · [tamper.out, verbatim]: `tampered /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/spark_secuura_2026-10-19_ks_1507_p1_103857/clone/Blockchain/Dev/services/auth/src/routes/users.ts:1197: '  return !process.env.DATABASE_URL;' -> '  return !process.env.DATABASE_URL?.trim();'` · [checker.out, verbatim]: `A4 (test-only): tamper reverted (Blockchain/Dev/services/auth/src/routes/users.ts back to the tip)` (tamper_revert.out EMPTY) · the tamper's `from` equals the product's tip line 1197. [apply_product.out, verbatim]: `A5 (test-only): no product hunk — the test must be GREEN at the untouched tip`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=1 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/auth/src/__tests__/ks1477-the-verification-store-is-memory-only-only-when-no-database-is-configured.test.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1477-the-verification-store-is-memory-only-only-when-no-database-is-configured.test.ts fails at the untouched tip (1 failed / 14 run; controls green; assertion reds)` [red_first.json: failed=1 of total=14; red cell(s): ['KS-1477 - a CONFIGURED database that is not reachable refuses; it never falls back to the process-local map RED KS-1507 note 3 whitespace - a whitespace-only DATABASE_URL counts as CONFIGURED: the boot window answers 503 and files nothing']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1477-the-verification-store-is-memory-only-only-when-no-database-is-configured.test.ts passes with the product hunk (14 passed / 14 run)` [green_after.json: failed=0 of total=14, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1061 failed=0 | after: total=1063 failed=0` · `NEW reds: []` [baseline_suite.json total=1061 failed=0; after_suite.json total=1063 failed=0]
- A6 [verbatim]: `PASS A6 whole services/auth suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/auth: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=1 +21/-1 test=src/__tests__/ks1477-the-verification-store-is-memory-only-only-when-no-database-is-configured.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** TEST-ONLY — ZERO PRODUCT BYTES: one file, the test `Blockchain/Dev/services/auth/src/__tests__/ks1477-the-verification-store-is-memory-only-only-when-no-database-is-configured.test.ts` (+21/-1 per numstat.out); the product `Blockchain/Dev/services/auth/src/routes/users.ts` is the tamper target and is byte-unchanged (sha256 7cdf68ac37c460f1, measured). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict) — at the tip `78cb3c3939e319332e387ffecb075a169edd4a39` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: the gate decides (test file only). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1507_p1/input.json`. Brief (located from the run dir's own name under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1507_p1/KS-1507.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1507_p1/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/auth/src/__tests__/ks1477-the-verification-store-is-memory-only-only-when-no-database-is-configured.test.ts b/Blockchain/Dev/services/auth/src/__tests__/ks1477-the-verification-store-is-memory-only-only-when-no-database-is-configured.test.ts
index 08257baca..253dc75cc 100644
--- a/Blockchain/Dev/services/auth/src/__tests__/ks1477-the-verification-store-is-memory-only-only-when-no-database-is-configured.test.ts
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1477-the-verification-store-is-memory-only-only-when-no-database-is-configured.test.ts
@@ -187,3 +187,23 @@
   });
-
+
+  // KS-1507 note 3: "configured" is `!process.env.DATABASE_URL` (db.ts getPool/initDb read it the same way), so an EMPTY string is memory-only
+  // and a whitespace-only value is CONFIGURED (it fails closed with a 503 for as long as the probe fails). The next two cells fix that
+  // meaning in place; a predicate that trimmed the value would flip the whitespace cell.
+  it('RED KS-1507 note 3 whitespace - a whitespace-only DATABASE_URL counts as CONFIGURED: the boot window answers 503 and files nothing', async () => {
+    process.env.DATABASE_URL = '   ';
+    asUser('ks1507-blank');
+    state.dbAvailable = false;
+    const r = await submit();
+    expect([r.status, code(r)]).toEqual([503, 'SERVICE_UNAVAILABLE']);
+    expect(state.inserts).toBe(0);
+  });
+
+  it('CONTROL KS-1507 note 3 empty - an EMPTY DATABASE_URL is memory-only, exactly as an unset one: the request is accepted into memory', async () => {
+    process.env.DATABASE_URL = '';
+    asUser('ks1507-empty');
+    state.dbAvailable = false;
+    const r = await submit();
+    expect([r.status, r.json.data?.status, state.inserts]).toEqual([200, 'PENDING', 0]);
+  });
+
   it('CONTROL KS-1477 - a read that SUCCEEDS with no row answers 404 (the map is empty here by construction, so this passes on the base too; the orphan cell below is the one that can tell)', async () => {
```
