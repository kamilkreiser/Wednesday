# READY — KS-1619-MULTICHUNK-1 (Spark (DeepSeek V4 Flash), briefed, test_only (code_patch checker, MODE=test_only), vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-18_ks_1619_p1/out.md.checker/patch.diff`** (from `ls` at 21:11 2026-10-18; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-18_ks_1619_p1/out.md.checker/section_1.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; CONTENT-compared against the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-18_ks_1619_p1-control-r2/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1); change lines (`+`/`-`, ordered) IDENTICAL in every file; body lines (context included) identical in every file; hunk headers identical; APPLIED RESULT IDENTICAL: both patches applied strictly (`git apply -p1`, scratch tempdir) to the tip content carried in input.json['files'] yield byte-identical files (ks1087-workflow-approve-deletes-the-pending-document.test.ts, sha256 equal).

**Held 21:11 2026-10-18 by Wednesday 2026-10-18 (read at source) after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-18_ks_1619_p1/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `d2ec786e6130c7ce13384185c84cc1e7566d77cb`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (test-only) touched-file set == { Blockchain/Dev/services/api-gateway/src/__tests__/ks1087-workflow-approve-deletes-the-pending-document.test.ts } — the product file is untouched, as the ticket requires`
- Declared set [input.json suggested_test_file; product_file = the TAMPER TARGET, not modified]: `Blockchain/Dev/services/api-gateway/src/__tests__/ks1087-workflow-approve-deletes-the-pending-document.test.ts` (test) — equal to numstat.out's set (1 file); `Blockchain/Dev/services/api-gateway/src/routes/verification.ts` (product) untouched, measured above.
- numstat [out.md.checker/numstat.out, verbatim]:
```
27	1	Blockchain/Dev/services/api-gateway/src/__tests__/ks1087-workflow-approve-deletes-the-pending-document.test.ts
```
- Test hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (25 line(s)), and no tip line is re-added as a '+' (A3d)` — test section `+` lines 27 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 1.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/api-gateway/src/__tests__/ks1087-workflow-approve-deletes-the-pending-document.test.ts byte-exact incl. leading whitespace (apply mode strict): OK 25 line(s) byte-exact incl. leading whitespace (of 25; 26 line(s) added by the apply)` [a3i_indent.out: `OK 25 line(s) byte-exact incl. leading whitespace (of 25; 26 line(s) added by the apply)`]
- **TEST-ONLY (code_patch checker MODE=test_only)** — the product `Blockchain/Dev/services/api-gateway/src/routes/verification.ts` is the TAMPER TARGET and is BYTE-UNCHANGED: the run's `patch.diff` re-applied strictly (`git apply -p1`, scratch tempdir) to the tip content in input.json['files'] leaves it sha256 `950a4e445c945c81` = the tip's; numstat.out does not list it; no section names it. [checker.out mode line, verbatim]: `mode: test_only (tamper at Blockchain/Dev/services/api-gateway/src/routes/verification.ts:1068)` · [tamper.out, verbatim]: `tampered /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/spark_secuura_2026-10-18_ks_1619_p1_201659/clone/Blockchain/Dev/services/api-gateway/src/routes/verification.ts:1068: "              proxyRes.on('data', () => { /* drain only: the reply body is not read (KS-1543) */ });" -> "              proxyRes.on('data', () => { proxyRes.pause(); });"` · [checker.out, verbatim]: `A4 (test-only): tamper reverted (Blockchain/Dev/services/api-gateway/src/routes/verification.ts back to the tip)` (tamper_revert.out EMPTY) · the tamper's `from` equals the product's tip line 1068. [apply_product.out, verbatim]: `A5 (test-only): no product hunk — the test must be GREEN at the untouched tip`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=1 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/api-gateway/src/__tests__/ks1087-workflow-approve-deletes-the-pending-document.test.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1087-workflow-approve-deletes-the-pending-document.test.ts fails at the untouched tip (1 failed / 12 run; controls green; assertion reds)` [red_first.json: failed=1 of total=12; red cell(s): ['RED KS-1619 D1 a 201 whose body arrives in several chunks is drained to its end (the forwarded line is logged)']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1087-workflow-approve-deletes-the-pending-document.test.ts passes with the product hunk (12 passed / 12 run)` [green_after.json: failed=0 of total=12, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1165 failed=0 | after: total=1166 failed=0` · `NEW reds: []` [baseline_suite.json total=1165 failed=0; after_suite.json total=1166 failed=0]
- A6 [verbatim]: `PASS A6 whole services/api-gateway suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/api-gateway: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=1 +27/-1 test=src/__tests__/ks1087-workflow-approve-deletes-the-pending-document.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** TEST-ONLY — ZERO PRODUCT BYTES: one file, the test `Blockchain/Dev/services/api-gateway/src/__tests__/ks1087-workflow-approve-deletes-the-pending-document.test.ts` (+27/-1 per numstat.out); the product `Blockchain/Dev/services/api-gateway/src/routes/verification.ts` is the tamper target and is byte-unchanged (sha256 950a4e445c945c81, measured). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict) — at the tip `d2ec786e6130c7ce13384185c84cc1e7566d77cb` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: the gate decides (test file only). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-18_ks_1619_p1/input.json`. Brief (located from the run dir's own name under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1619_p1/KS-1619.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-18_ks_1619_p1/checker.out`.

```diff
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1087-workflow-approve-deletes-the-pending-document.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1087-workflow-approve-deletes-the-pending-document.test.ts
@@ -141,4 +141,30 @@
   res.end(body);
 };
-
+
+// KS-1619 part 1 (gate C LOW-1560-1): the forward's no-op 'data' listener (routes/verification.ts:1068) exists to DRAIN the
+// reply so its 'end' fires. Every other cell answers in ONE chunk, which still ends after a listener that pauses the
+// stream, so the gate's mutant M1c (the listener calls proxyRes.pause()) survived the whole suite. A reply in several
+// chunks, written apart in time, only reaches 'end' if every chunk is read.
+it('RED KS-1619 D1 a 201 whose body arrives in several chunks is drained to its end (the forwarded line is logged)', { timeout: 15_000 }, async () => {
+  const CHUNK = 'x'.repeat(64 * 1024);
+  behave = (_req, res) => {
+    res.writeHead(201, { 'Content-Type': 'application/json' });
+    let sent = 0;
+    const next = (): void => {
+      if (sent === 4) { res.end(); return; }
+      sent++;
+      res.write(CHUNK);
+      setTimeout(next, 25);
+    };
+    next();
+  };
+  const store = freshStore();
+  const log = vi.fn<Log>();
+  const out = await approve(await startGateway(store, undefined, log));
+  expect(out.status).toBe(200);
+  const forwarded = (): boolean => log.mock.calls.some(([, message]) => String(message).endsWith(' document forwarded to originate'));
+  for (let waited = 0; waited < 2_000 && !forwarded(); waited += 50) await new Promise<void>((r) => setTimeout(r, 50));
+  expect(forwarded(), 'the reply was read to its end').toBe(true);
+});
+
 const sleep = (ms: number) => new Promise<void>((r) => setTimeout(r, ms));
```
