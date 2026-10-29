# READY — KS-1827-KS-1827-B6-BYIDSPREAD (Spark (DeepSeek V4 Flash), briefed, test_only (code_patch checker, MODE=test_only), vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1827_p1_byid_spread_live/out.md.checker/patch.diff`** (from `ls` at 01:45 2026-10-30; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1827_p1_byid_spread_live/out.md.checker/section_1.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden not located — no identity claim is made.

**Held 01:45 2026-10-30 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1827_p1_byid_spread_live/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `5a5c4d2b353fa4091762630df8bfaea26d6b9245`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (test-only) touched-file set == { Blockchain/Dev/services/anchoring/src/__tests__/ks1454-signature-hash-is-read-back-on-the-verify-and-by-id-reads.test.ts } — the product file is untouched, as the ticket requires`
- Declared set [input.json suggested_test_file; product_file = the TAMPER TARGET, not modified]: `Blockchain/Dev/services/anchoring/src/__tests__/ks1454-signature-hash-is-read-back-on-the-verify-and-by-id-reads.test.ts` (test) — equal to numstat.out's set (1 file); `Blockchain/Dev/services/anchoring/src/index.ts` (product) untouched, measured above.
- numstat [out.md.checker/numstat.out, verbatim]:
```
14	0	Blockchain/Dev/services/anchoring/src/__tests__/ks1454-signature-hash-is-read-back-on-the-verify-and-by-id-reads.test.ts
```
- Test hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (12 line(s)), and no tip line is re-added as a '+' (A3d)` — test section `+` lines 14 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 0.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/anchoring/src/__tests__/ks1454-signature-hash-is-read-back-on-the-verify-and-by-id-reads.test.ts byte-exact incl. leading whitespace (apply mode strict): OK 12 line(s) byte-exact incl. leading whitespace (of 12; 14 line(s) added by the apply)` [a3i_indent.out: `OK 12 line(s) byte-exact incl. leading whitespace (of 12; 14 line(s) added by the apply)`]
- **TEST-ONLY (code_patch checker MODE=test_only)** — the product `Blockchain/Dev/services/anchoring/src/index.ts` is the TAMPER TARGET and is BYTE-UNCHANGED: the run's `patch.diff` re-applied strictly (`git apply -p1`, scratch tempdir) to the tip content in input.json['files'] leaves it sha256 `e84c76b01e75e70b` = the tip's; numstat.out does not list it; no section names it. [checker.out mode line, verbatim]: `mode: test_only (tamper at Blockchain/Dev/services/anchoring/src/index.ts:960)` · [tamper.out, verbatim]: `tampered /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/spark_secuura_2026-10-30_ks_1827_p1_byid_spread_live_012417/clone/Blockchain/Dev/services/anchoring/src/index.ts:960: '    ...anchorSignatureHashView((anchor.metadataPayload as any)?.secuura),' -> '    // ...anchorSignatureHashView((anchor.metadataPayload as any)?.secuura),'` · [checker.out, verbatim]: `A4 (test-only): tamper reverted (Blockchain/Dev/services/anchoring/src/index.ts back to the tip)` (tamper_revert.out EMPTY) · the tamper's `from` equals the product's tip line 960. [apply_product.out, verbatim]: `A5 (test-only): no product hunk — the test must be GREEN at the untouched tip`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=1 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/anchoring/src/__tests__/ks1454-signature-hash-is-read-back-on-the-verify-and-by-id-reads.test.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1454-signature-hash-is-read-back-on-the-verify-and-by-id-reads.test.ts fails at the untouched tip (1 failed / 11 run; controls green; assertion reds)` [red_first.json: failed=1 of total=11; red cell(s): ['KS-1454: the anchored signatureHash is read back RED KS-1827 B6: the by-id spread of anchorSignatureHashView is live code in the handler, not commented out']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1454-signature-hash-is-read-back-on-the-verify-and-by-id-reads.test.ts passes with the product hunk (11 passed / 11 run)` [green_after.json: failed=0 of total=11, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=497 failed=1 | after: total=499 failed=1` · `NEW reds: []` [baseline_suite.json total=497 failed=1; after_suite.json total=499 failed=1]
- A6 [verbatim]: `PASS A6 whole services/anchoring suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/anchoring: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=1 +14/-0 test=src/__tests__/ks1454-signature-hash-is-read-back-on-the-verify-and-by-id-reads.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** TEST-ONLY — ZERO PRODUCT BYTES: one file, the test `Blockchain/Dev/services/anchoring/src/__tests__/ks1454-signature-hash-is-read-back-on-the-verify-and-by-id-reads.test.ts` (+14/-0 per numstat.out); the product `Blockchain/Dev/services/anchoring/src/index.ts` is the tamper target and is byte-unchanged (sha256 e84c76b01e75e70b, measured). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict) — at the tip `5a5c4d2b353fa4091762630df8bfaea26d6b9245` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: the gate decides (test file only). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1827_p1_byid_spread_live/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1827_p1_byid_spread_live/checker.out`.

```diff
--- a/Blockchain/Dev/services/anchoring/src/__tests__/ks1454-signature-hash-is-read-back-on-the-verify-and-by-id-reads.test.ts
+++ b/Blockchain/Dev/services/anchoring/src/__tests__/ks1454-signature-hash-is-read-back-on-the-verify-and-by-id-reads.test.ts
@@ -61,3 +61,17 @@
+  // KS-1827 (gate 18 mutant X16): B5 matches the spread by source TEXT, and a commented-out spread keeps that text in the file, so the mutant passed 23 of 23 while the route stopped returning the hash.
+  // B6 reads the handler slice with its comments removed (whole `//` lines and `/* */` blocks), so only live code can satisfy the match.
+  it('RED KS-1827 B6: the by-id spread of anchorSignatureHashView is live code in the handler, not commented out', () => {
+    const live = GET_BY_ID.replace(/\/\*[\s\S]*?\*\//g, '').split('\n').filter((line) => !line.trim().startsWith('//')).join('\n');
+    expect(live.includes('...anchorSignatureHashView((anchor.metadataPayload as any)?.secuura),')).toBe(true);
+  });
+
+  it('control KS-1827 B7: the comment-stripping read still sees the live identity spread beside it and drops the KS-1454 comment line', () => {
+    const live = GET_BY_ID.replace(/\/\*[\s\S]*?\*\//g, '').split('\n').filter((line) => !line.trim().startsWith('//')).join('\n');
+    expect(live.includes('...anchorIdentityView((anchor.metadataPayload as any)?.secuura),')).toBe(true);
+    expect(live.includes('KS-1454: the SHA-256 of the detached')).toBe(false);
+    expect(GET_BY_ID.includes('KS-1454: the SHA-256 of the detached')).toBe(true);
+  });
+
   it('control KS-1454 C1: an anchor with no signatureHash reads null (the key is never invented), on both reads', () => {
     expect(RB.anchorSignatureHashView?.(PLAIN.secuura) ?? { signatureHash: null }).toEqual({ signatureHash: null });
     expect((RB.buildVerifyResponse('db', PLAIN, ROW, CTX) as any).metadata.signatureHash ?? null).toBeNull();
```
