# READY — KS-1815-KS-1815-P4 (Spark (DeepSeek V4 Flash), briefed, test_only (code_patch checker, MODE=test_only), vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1815_p4_real_node_reply_not_retried/out.md.checker/patch.diff`** (from `ls` at 13:55 2026-10-30; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1815_p4_real_node_reply_not_retried/out.md.checker/section_1.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; CONTENT-compared against the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1815_p4_real_node_reply_not_retried-control/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1); change lines (`+`/`-`, ordered) IDENTICAL in every file; body lines (context included) identical in every file; hunk headers identical; APPLIED RESULT IDENTICAL: both patches applied strictly (`git apply -p1`, scratch tempdir) to the tip content carried in input.json['files'] yield byte-identical files (ks726-write-ahead-tx-hash.test.ts, sha256 equal).

**Held 13:55 2026-10-30 by Spark operator 24 (Wednesday) after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1815_p4_real_node_reply_not_retried/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `85cd24d81cb97e30e08fdc054d1ba4b65ea8b558`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (test-only) touched-file set == { Blockchain/Dev/services/anchoring/src/__tests__/ks726-write-ahead-tx-hash.test.ts } — the product file is untouched, as the ticket requires`
- Declared set [input.json suggested_test_file; product_file = the TAMPER TARGET, not modified]: `Blockchain/Dev/services/anchoring/src/__tests__/ks726-write-ahead-tx-hash.test.ts` (test) — equal to numstat.out's set (1 file); `Blockchain/Dev/services/anchoring/src/anchorSubmission.ts` (product) untouched, measured above.
- numstat [out.md.checker/numstat.out, verbatim]:
```
35	0	Blockchain/Dev/services/anchoring/src/__tests__/ks726-write-ahead-tx-hash.test.ts
```
- Test hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (30 line(s)), and no tip line is re-added as a '+' (A3d)` — test section `+` lines 35 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 0.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/anchoring/src/__tests__/ks726-write-ahead-tx-hash.test.ts byte-exact incl. leading whitespace (apply mode strict): OK 30 line(s) byte-exact incl. leading whitespace (of 30; 35 line(s) added by the apply)` [a3i_indent.out: `OK 30 line(s) byte-exact incl. leading whitespace (of 30; 35 line(s) added by the apply)`]
- **TEST-ONLY (code_patch checker MODE=test_only)** — the product `Blockchain/Dev/services/anchoring/src/anchorSubmission.ts` is the TAMPER TARGET and is BYTE-UNCHANGED: the run's `patch.diff` re-applied strictly (`git apply -p1`, scratch tempdir) to the tip content in input.json['files'] leaves it sha256 `738a8374de43738e` = the tip's; numstat.out does not list it; no section names it. [checker.out mode line, verbatim]: `mode: test_only (tamper at Blockchain/Dev/services/anchoring/src/anchorSubmission.ts:640)` · [tamper.out, verbatim]: `tampered /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/spark_secuura_2026-10-30_ks_1815_p4_real_node_reply_not_retried_135335/clone/Blockchain/Dev/services/anchoring/src/anchorSubmission.ts:640: "            !ALREADY_INCLUDED_REPLY.test(message ?? '');" -> '            true;'` · [checker.out, verbatim]: `A4 (test-only): tamper reverted (Blockchain/Dev/services/anchoring/src/anchorSubmission.ts back to the tip)` (tamper_revert.out EMPTY) · the tamper's `from` equals the product's tip line 640. [apply_product.out, verbatim]: `A5 (test-only): no product hunk — the test must be GREEN at the untouched tip`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=1 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/anchoring/src/__tests__/ks726-write-ahead-tx-hash.test.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks726-write-ahead-tx-hash.test.ts fails at the untouched tip (1 failed / 16 run; controls green; assertion reds)` [red_first.json: failed=1 of total=16; red cell(s): ['KS-726 — a DEFINITIVE node rejection keeps the ordinary retry; only a LOST reply rests in submitting (#805 review, ruled 2026-09-14) RED KS-1815 R1 the node REAL reply ("... already been included ...") after onSigned, with a DEFINITIVE absent re-poll, is NOT retried: the row rests in submitting']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks726-write-ahead-tx-hash.test.ts passes with the product hunk (16 passed / 16 run)` [green_after.json: failed=0 of total=16, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=550 failed=1 | after: total=552 failed=1` · `NEW reds: []` [baseline_suite.json total=550 failed=1; after_suite.json total=552 failed=1]
- A6 [verbatim]: `PASS A6 whole services/anchoring suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/anchoring: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=1 +35/-0 test=src/__tests__/ks726-write-ahead-tx-hash.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** TEST-ONLY — ZERO PRODUCT BYTES: one file, the test `Blockchain/Dev/services/anchoring/src/__tests__/ks726-write-ahead-tx-hash.test.ts` (+35/-0 per numstat.out); the product `Blockchain/Dev/services/anchoring/src/anchorSubmission.ts` is the tamper target and is byte-unchanged (sha256 738a8374de43738e, measured). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict) — at the tip `85cd24d81cb97e30e08fdc054d1ba4b65ea8b558` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: the gate decides (test file only). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1815_p4_real_node_reply_not_retried/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1815_p4_real_node_reply_not_retried/checker.out`.

```diff
--- a/Blockchain/Dev/services/anchoring/src/__tests__/ks726-write-ahead-tx-hash.test.ts
+++ b/Blockchain/Dev/services/anchoring/src/__tests__/ks726-write-ahead-tx-hash.test.ts
@@ -452,3 +452,38 @@
+  // KS-1815: the cell above feeds the guard a PARAPHRASE of the node's reply ("All inputs are spent"). The node's real text (stored in
+  // ks705-submission-idempotency.test.ts) also says "already been included", and the ALREADY_INCLUDED_REPLY clause of `refusedAndAbsent`
+  // turns the ruled retry OFF for any text that contains it. These cells pin that clause with the real text.
+  const REAL_NODE_REPLY =
+    'Transaction submission failed: ConwayMempoolFailure "All inputs are spent. ' +
+    'Transaction has probably already been included in a successfully applied block."';
+  const definitiveAbsent = () =>
+    vi.fn(async () => ({
+      confirmed: false,
+      polled: ABSENT_MIN_ANSWERED_POLLS,
+      errored: 0,
+      lastAnsweredAttempt: ABSENT_MIN_ANSWERED_POLLS,
+      lastAnsweredElapsedMs: ABSENT_MIN_LAST_ANSWER_MS + 1_000,
+    }));
+
+  it('RED KS-1815 R1 the node REAL reply ("... already been included ...") after onSigned, with a DEFINITIVE absent re-poll, is NOT retried: the row rests in submitting', async () => {
+    const h = makeHarness({ over: { submit: throwingSubmit(refused(REAL_NODE_REPLY)), confirm: definitiveAbsent() } });
+    await createAnchorSubmitter(h.deps)(ANCHOR_ID);
+
+    expect(h.deps.confirm).toHaveBeenCalledTimes(1);
+    expect(h.deps.scheduleRetry).toHaveBeenCalledTimes(0);
+    expect(h.row.status).toBe('submitting');
+  });
+
+  it('control KS-1815 C1 the same DEFINITIVE absent re-poll with the paraphrase "All inputs are spent" (no "already been included") IS retried', async () => {
+    const h = makeHarness({
+      over: { submit: throwingSubmit(refused('Transaction submission failed: ConwayMempoolFailure "All inputs are spent"')), confirm: definitiveAbsent() },
+    });
+    await createAnchorSubmitter(h.deps)(ANCHOR_ID);
+
+    expect(h.deps.confirm).toHaveBeenCalledTimes(1);
+    expect(h.deps.scheduleRetry).toHaveBeenCalledTimes(1);
+    expect(h.row.status).not.toBe('submitting');
+  });
+
   it('CONTROL — a 400 "already been included" after onSigned → re-polled and confirmed, scheduleRetry NOT called (the hash IS on chain)', async () => {
     const h = makeHarness({ over: { submit: throwingSubmit(refused('Transaction submission failed: this transaction has already been included')) } });
     await createAnchorSubmitter(h.deps)(ANCHOR_ID);
```

> OPERATOR 24 SCOPE NOTE: touches the anchoring service (not index.ts, not KS-1384, no open PR file overlaps at 2026-10-30). Operator 19 had treated the whole anchoring service as out; Wednesday to confirm before a raise.
