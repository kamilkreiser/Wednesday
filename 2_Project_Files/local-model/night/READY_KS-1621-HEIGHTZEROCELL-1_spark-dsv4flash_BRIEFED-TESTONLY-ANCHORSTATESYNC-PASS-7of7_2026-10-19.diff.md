# READY — KS-1621-HEIGHTZEROCELL-1 (Spark (DeepSeek V4 Flash), briefed, test_only (code_patch checker, MODE=test_only), jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1621_originate/out.md.checker/patch.diff`** (from `ls` at 07:16 2026-10-19; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1621_originate/out.md.checker/section_1.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden path `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1621_originate/golden.diff/out.md.checker/patch.diff` does not exist — no identity claim is made.

**Held 07:16 2026-10-19 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1621_originate/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `83ed01af70fd5ed6cca9ac66f28ddcb8a1034105`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (test-only) touched-file set == { Blockchain/Dev/services/originate/src/__tests__/ks1333-sync-writers-persist-null-not-zero.test.ts } — the product file is untouched, as the ticket requires`
- Declared set [input.json suggested_test_file; product_file = the TAMPER TARGET, not modified]: `Blockchain/Dev/services/originate/src/__tests__/ks1333-sync-writers-persist-null-not-zero.test.ts` (test) — equal to numstat.out's set (1 file); `Blockchain/Dev/services/originate/src/services/anchorStateSync.ts` (product) untouched, measured above.
- numstat [out.md.checker/numstat.out, verbatim]:
```
5	0	Blockchain/Dev/services/originate/src/__tests__/ks1333-sync-writers-persist-null-not-zero.test.ts
```
- Test hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (4 line(s)), and no tip line is re-added as a '+' (A3d)` — test section `+` lines 5 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 0.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/originate/src/__tests__/ks1333-sync-writers-persist-null-not-zero.test.ts byte-exact incl. leading whitespace (apply mode strict): OK 4 line(s) byte-exact incl. leading whitespace (of 4; 5 line(s) added by the apply)` [a3i_indent.out: `OK 4 line(s) byte-exact incl. leading whitespace (of 4; 5 line(s) added by the apply)`]
- **TEST-ONLY (code_patch checker MODE=test_only)** — the product `Blockchain/Dev/services/originate/src/services/anchorStateSync.ts` is the TAMPER TARGET and is BYTE-UNCHANGED: the run's `patch.diff` re-applied strictly (`git apply -p1`, scratch tempdir) to the tip content in input.json['files'] leaves it sha256 `12ac495e11c92ad7` = the tip's; numstat.out does not list it; no section names it. [checker.out mode line, verbatim]: `mode: test_only (tamper at Blockchain/Dev/services/originate/src/services/anchorStateSync.ts:193)` · [tamper.out, verbatim]: `tampered /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/spark_secuura_2026-10-19_ks_1621_originate_064913/clone/Blockchain/Dev/services/originate/src/services/anchorStateSync.ts:193: '      blockHeight: prior?.blockHeight ?? null,' -> '      blockHeight: prior?.blockHeight || null,'` · [checker.out, verbatim]: `A4 (test-only): tamper reverted (Blockchain/Dev/services/originate/src/services/anchorStateSync.ts back to the tip)` (tamper_revert.out EMPTY) · the tamper's `from` equals the product's tip line 193. [apply_product.out, verbatim]: `A5 (test-only): no product hunk — the test must be GREEN at the untouched tip`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=1 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1333-sync-writers-persist-null-not-zero.test.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1333-sync-writers-persist-null-not-zero.test.ts fails at the untouched tip (1 failed / 15 run; controls green; assertion reds)` [red_first.json: failed=1 of total=15; red cell(s): ['KS-1509 - the failed-anchor writer keeps an unknown block height NULL RED KS-1621 F5 a real prior height of 0 is carried forward as 0, not collapsed to null']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1333-sync-writers-persist-null-not-zero.test.ts passes with the product hunk (15 passed / 15 run)` [green_after.json: failed=0 of total=15, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1405 failed=0 | after: total=1406 failed=0` · `NEW reds: []` [baseline_suite.json total=1405 failed=0; after_suite.json total=1406 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=1 +5/-0 test=src/__tests__/ks1333-sync-writers-persist-null-not-zero.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** TEST-ONLY — ZERO PRODUCT BYTES: one file, the test `Blockchain/Dev/services/originate/src/__tests__/ks1333-sync-writers-persist-null-not-zero.test.ts` (+5/-0 per numstat.out); the product `Blockchain/Dev/services/originate/src/services/anchorStateSync.ts` is the tamper target and is byte-unchanged (sha256 12ac495e11c92ad7, measured). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict) — at the tip `83ed01af70fd5ed6cca9ac66f28ddcb8a1034105` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: the gate decides (test file only). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1621_originate/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1621_originate/checker.out`.

```diff
--- a/Blockchain/Dev/services/originate/src/__tests__/ks1333-sync-writers-persist-null-not-zero.test.ts
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1333-sync-writers-persist-null-not-zero.test.ts
@@ -160,2 +160,7 @@
   });
+
+  it('RED KS-1621 F5 a real prior height of 0 is carried forward as 0, not collapsed to null', async () => {
+    const blob = await failWith({ txHash: null, blockHeight: 0, status: 'submitted', anchorId: 'anchor_1' });
+    expect([blob.status, 'blockHeight' in blob, blob.blockHeight]).toEqual(['anchor_failed', true, 0]);
+  });
 });
```
