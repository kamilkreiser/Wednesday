# READY — KS-1525-G1G10CELLS-1 (Spark (DeepSeek V4 Flash), briefed, test_only (code_patch checker, MODE=test_only), vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1525_p1/out.md.checker/patch.diff`** (from `ls` at 09:58 2026-10-19; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1525_p1/out.md.checker/section_1.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; CONTENT-compared against the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1525_p1-control/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1); change lines (`+`/`-`, ordered) IDENTICAL in every file; body lines (context included) identical in every file; hunk headers identical; APPLIED RESULT IDENTICAL: both patches applied strictly (`git apply -p1`, scratch tempdir) to the tip content carried in input.json['files'] yield byte-identical files (row-converters.test.ts, sha256 equal).

**Held 09:58 2026-10-19 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1525_p1/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `78cb3c3939e319332e387ffecb075a169edd4a39`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (test-only) touched-file set == { Blockchain/Dev/services/security/src/__tests__/row-converters.test.ts } — the product file is untouched, as the ticket requires`
- Declared set [input.json suggested_test_file; product_file = the TAMPER TARGET, not modified]: `Blockchain/Dev/services/security/src/__tests__/row-converters.test.ts` (test) — equal to numstat.out's set (1 file); `Blockchain/Dev/services/security/src/converters.ts` (product) untouched, measured above.
- numstat [out.md.checker/numstat.out, verbatim]:
```
12	0	Blockchain/Dev/services/security/src/__tests__/row-converters.test.ts
```
- Test hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (11 line(s)), and no tip line is re-added as a '+' (A3d)` — test section `+` lines 12 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 0.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/security/src/__tests__/row-converters.test.ts byte-exact incl. leading whitespace (apply mode strict): OK 11 line(s) byte-exact incl. leading whitespace (of 11; 12 line(s) added by the apply)` [a3i_indent.out: `OK 11 line(s) byte-exact incl. leading whitespace (of 11; 12 line(s) added by the apply)`]
- **TEST-ONLY (code_patch checker MODE=test_only)** — the product `Blockchain/Dev/services/security/src/converters.ts` is the TAMPER TARGET and is BYTE-UNCHANGED: the run's `patch.diff` re-applied strictly (`git apply -p1`, scratch tempdir) to the tip content in input.json['files'] leaves it sha256 `86d8474669a458c7` = the tip's; numstat.out does not list it; no section names it. [checker.out mode line, verbatim]: `mode: test_only (tamper at Blockchain/Dev/services/security/src/converters.ts:171)` · [tamper.out, verbatim]: `tampered /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/spark_secuura_2026-10-19_ks_1525_p1_095302/clone/Blockchain/Dev/services/security/src/converters.ts:171: '    isActive: Boolean(r.is_active),' -> '    isActive: r.is_active === undefined ? true : Boolean(r.is_active),'` · [checker.out, verbatim]: `A4 (test-only): tamper reverted (Blockchain/Dev/services/security/src/converters.ts back to the tip)` (tamper_revert.out EMPTY) · the tamper's `from` equals the product's tip line 171. [apply_product.out, verbatim]: `A5 (test-only): no product hunk — the test must be GREEN at the untouched tip`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=1 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/security/src/__tests__/row-converters.test.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/row-converters.test.ts fails at the untouched tip (1 failed / 23 run; controls green; assertion reds)` [red_first.json: failed=1 of total=23; red cell(s): ['rowToApiKey() RED KS-1525 G1: a row with NO is_active column reads INACTIVE, never active (an absent column must not un-revoke a key)']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/row-converters.test.ts passes with the product hunk (23 passed / 23 run)` [green_after.json: failed=0 of total=23, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=343 failed=0 | after: total=346 failed=0` · `NEW reds: []` [baseline_suite.json total=343 failed=0; after_suite.json total=346 failed=0]
- A6 [verbatim]: `PASS A6 whole services/security suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/security: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=1 +12/-0 test=src/__tests__/row-converters.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** TEST-ONLY — ZERO PRODUCT BYTES: one file, the test `Blockchain/Dev/services/security/src/__tests__/row-converters.test.ts` (+12/-0 per numstat.out); the product `Blockchain/Dev/services/security/src/converters.ts` is the tamper target and is byte-unchanged (sha256 86d8474669a458c7, measured). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict) — at the tip `78cb3c3939e319332e387ffecb075a169edd4a39` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: the gate decides (test file only). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1525_p1/input.json`. Brief (located from the run dir's own name under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1525_p1/KS-1525.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1525_p1/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/security/src/__tests__/row-converters.test.ts b/Blockchain/Dev/services/security/src/__tests__/row-converters.test.ts
--- a/Blockchain/Dev/services/security/src/__tests__/row-converters.test.ts
+++ b/Blockchain/Dev/services/security/src/__tests__/row-converters.test.ts
@@ -213,4 +213,16 @@ describe('rowToApiKey()', () => {
       expiresAt: new Date('2027-01-01T00:00:00Z'), createdAt: new Date('2026-04-01T00:00:00Z'), connectorId: 'conn_1',
     });
   });
+
+  // KS-1525: the is_active boundary the KS-880 gate's mutants G1 and G10 crossed with the whole suite green.
+  it('RED KS-1525 G1: a row with NO is_active column reads INACTIVE, never active (an absent column must not un-revoke a key)', () => {
+    const { is_active: _a, ...noActive } = KEY_ROW;
+    expect(rowToApiKey(noActive).isActive).toBe(false);
+  });
+  it('CONTROL KS-1525 G1: is_active null reads inactive too', () => {
+    expect(rowToApiKey({ ...KEY_ROW, is_active: null }).isActive).toBe(false);
+  });
+  it('CONTROL KS-1525 G10: the Postgres text form is_active "t" reads active, so tightening Boolean() to === true reds', () => {
+    expect(rowToApiKey({ ...KEY_ROW, is_active: 't' }).isActive).toBe(true);
+  });
 });
```
