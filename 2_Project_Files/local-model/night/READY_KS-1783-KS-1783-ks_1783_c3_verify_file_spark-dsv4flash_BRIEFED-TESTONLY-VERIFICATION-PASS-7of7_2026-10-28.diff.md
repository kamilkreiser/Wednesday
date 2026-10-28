# READY — KS-1783-KS-1783-ks_1783_c3_verify_file (spark-dsv4flash, briefed, test_only (code_patch checker, MODE=test_only), jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1783_c3_verify_file/out.md.checker/patch.diff`** (from `ls` at 19:23 2026-10-28; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1783_c3_verify_file/out.md.checker/section_1.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; CONTENT-compared against the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1783_c3_verify_file-control/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1); change lines (`+`/`-`, ordered) IDENTICAL in every file; body lines (context included) identical in every file; hunk headers identical; APPLIED RESULT IDENTICAL: both patches applied strictly (`git apply -p1`, scratch tempdir) to the tip content carried in input.json['files'] yield byte-identical files (ks1634-a-simulated-anchor-verified-by-hash.test.ts, sha256 equal).

**Held 19:23 2026-10-28 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1783_c3_verify_file/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `bd6697e079fce41db6b21e094a9eddb3d0e1d08e`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (test-only) touched-file set == { Blockchain/Dev/services/originate/src/__tests__/ks1634-a-simulated-anchor-verified-by-hash.test.ts } — the product file is untouched, as the ticket requires`
- Declared set [input.json suggested_test_file; product_file = the TAMPER TARGET, not modified]: `Blockchain/Dev/services/originate/src/__tests__/ks1634-a-simulated-anchor-verified-by-hash.test.ts` (test) — equal to numstat.out's set (1 file); `Blockchain/Dev/services/originate/src/routes/verification.ts` (product) untouched, measured above.
- numstat [out.md.checker/numstat.out, verbatim]:
```
6	1	Blockchain/Dev/services/originate/src/__tests__/ks1634-a-simulated-anchor-verified-by-hash.test.ts
```
- Test hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (6 line(s)), and no tip line is re-added as a '+' (A3d)` — test section `+` lines 6 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 1.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/originate/src/__tests__/ks1634-a-simulated-anchor-verified-by-hash.test.ts byte-exact incl. leading whitespace (apply mode strict): OK 6 line(s) byte-exact incl. leading whitespace (of 6; 6 line(s) added by the apply)` [a3i_indent.out: `OK 6 line(s) byte-exact incl. leading whitespace (of 6; 6 line(s) added by the apply)`]
- **TEST-ONLY (code_patch checker MODE=test_only)** — the product `Blockchain/Dev/services/originate/src/routes/verification.ts` is the TAMPER TARGET and is BYTE-UNCHANGED: the run's `patch.diff` re-applied strictly (`git apply -p1`, scratch tempdir) to the tip content in input.json['files'] leaves it sha256 `8131c10bac13b44a` = the tip's; numstat.out does not list it; no section names it. [checker.out mode line, verbatim]: `mode: test_only (tamper at Blockchain/Dev/services/originate/src/routes/verification.ts:724)` · [tamper.out, verbatim]: `tampered /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/spark_secuura_2026-10-28_ks_1783_c3_verify_file_192049/clone/Blockchain/Dev/services/originate/src/routes/verification.ts:724: '              simulated: chain.simulated,' -> '              simulated: undefined,'` · [checker.out, verbatim]: `A4 (test-only): tamper reverted (Blockchain/Dev/services/originate/src/routes/verification.ts back to the tip)` (tamper_revert.out EMPTY) · the tamper's `from` equals the product's tip line 724. [apply_product.out, verbatim]: `A5 (test-only): no product hunk — the test must be GREEN at the untouched tip`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=1 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1634-a-simulated-anchor-verified-by-hash.test.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1634-a-simulated-anchor-verified-by-hash.test.ts fails at the untouched tip (2 failed / 6 run; controls green; assertion reds)` [red_first.json: failed=2 of total=6; red cell(s): ['KS-1628 L1 and L6 - the verify-file chain-first fallback RED KS-1628 L6 verify-file: simulated true with a real hash is not on-chain', 'KS-1628 L1 and L6 - the verify-file chain-first fallback RED KS-1628 L6 verify-file: the shape anchoring really sends (simulated true, txHash null) is not on-chain']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1634-a-simulated-anchor-verified-by-hash.test.ts passes with the product hunk (6 passed / 6 run)` [green_after.json: failed=0 of total=6, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1698 failed=0 | after: total=1698 failed=0` · `NEW reds: []` [baseline_suite.json total=1698 failed=0; after_suite.json total=1698 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=1 +6/-1 test=src/__tests__/ks1634-a-simulated-anchor-verified-by-hash.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** TEST-ONLY — ZERO PRODUCT BYTES: one file, the test `Blockchain/Dev/services/originate/src/__tests__/ks1634-a-simulated-anchor-verified-by-hash.test.ts` (+6/-1 per numstat.out); the product `Blockchain/Dev/services/originate/src/routes/verification.ts` is the tamper target and is byte-unchanged (sha256 8131c10bac13b44a, measured). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict) — at the tip `bd6697e079fce41db6b21e094a9eddb3d0e1d08e` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: the gate decides (test file only). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1783_c3_verify_file/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1783_c3_verify_file/checker.out`.

```diff
--- a/Blockchain/Dev/services/originate/src/__tests__/ks1634-a-simulated-anchor-verified-by-hash.test.ts
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1634-a-simulated-anchor-verified-by-hash.test.ts
@@ -44,1 +44,3 @@
+// KS-1783: the shape of a REAL tx hash (as ks1634-v2-chain-only-match-carries-simulated.test.ts:49), held apart from REAL_TX on purpose.
+const REAL_TX_SHAPE = /^[0-9a-f]{64}$/;
 const REAL_TX = '4f1e6a8d2c7b9e3f1a5b7c9d2e4f6a8b1c3d5e7f9a2b4c6d8e0f2a4b6c8d0e2f';
@@ -102,5 +104,8 @@
   it('RED KS-1628 L6 verify-file: simulated true with a real hash is not on-chain', async () => {
-    const body = await callSite(chainReply({ simulated: true }));
+    const reply = chainReply({ simulated: true });
+    // KS-1783: assert the hash this cell sends is real (it was implicit, from chainReply's default). The route's own reply carries txHash null here, so the check is on the reply handed in.
+    expect(reply.txHash).toMatch(REAL_TX_SHAPE);
+    const body = await callSite(reply);
     expect(body.blockchain.simulated).toBe(true);
     expect(body.blockchain.anchored).toBe(false);
     expect(body.blockchain.txHash).toBeNull();
```
