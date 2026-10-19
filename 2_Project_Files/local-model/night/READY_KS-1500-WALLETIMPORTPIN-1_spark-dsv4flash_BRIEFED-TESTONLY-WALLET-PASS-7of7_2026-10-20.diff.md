# READY — KS-1500-WALLETIMPORTPIN-1 (Spark (DeepSeek V4 Flash), briefed, test_only (code_patch checker, MODE=test_only), vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1500_p1/out.md.checker/patch.diff`** (from `ls` at 01:02 2026-10-20; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1500_p1/out.md.checker/section_1.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; CONTENT-compared against the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1500_p1-control/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1); change lines (`+`/`-`, ordered) IDENTICAL in every file; body lines (context included) identical in every file; hunk headers identical; APPLIED RESULT IDENTICAL: both patches applied strictly (`git apply -p1`, scratch tempdir) to the tip content carried in input.json['files'] yield byte-identical files (ks963-preauth-rethrow.test.ts, sha256 equal).

**Held 01:02 2026-10-20 by Wednesday (overnight 10-20) after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1500_p1/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `a66cd6a4d1726794c816fd4fefec58c728d410e5`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (test-only) touched-file set == { Blockchain/Dev/services/auth/src/__tests__/ks963-preauth-rethrow.test.ts } — the product file is untouched, as the ticket requires`
- Declared set [input.json suggested_test_file; product_file = the TAMPER TARGET, not modified]: `Blockchain/Dev/services/auth/src/__tests__/ks963-preauth-rethrow.test.ts` (test) — equal to numstat.out's set (1 file); `Blockchain/Dev/services/auth/src/routes/wallet.ts` (product) untouched, measured above.
- numstat [out.md.checker/numstat.out, verbatim]:
```
7	0	Blockchain/Dev/services/auth/src/__tests__/ks963-preauth-rethrow.test.ts
```
- Test hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (7 line(s)), and no tip line is re-added as a '+' (A3d)` — test section `+` lines 7 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 0.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/auth/src/__tests__/ks963-preauth-rethrow.test.ts byte-exact incl. leading whitespace (apply mode strict): OK 7 line(s) byte-exact incl. leading whitespace (of 7; 7 line(s) added by the apply)` [a3i_indent.out: `OK 7 line(s) byte-exact incl. leading whitespace (of 7; 7 line(s) added by the apply)`]
- **TEST-ONLY (code_patch checker MODE=test_only)** — the product `Blockchain/Dev/services/auth/src/routes/wallet.ts` is the TAMPER TARGET and is BYTE-UNCHANGED: the run's `patch.diff` re-applied strictly (`git apply -p1`, scratch tempdir) to the tip content in input.json['files'] leaves it sha256 `17cd98c3cad1cb57` = the tip's; numstat.out does not list it; no section names it. [checker.out mode line, verbatim]: `mode: test_only (tamper at Blockchain/Dev/services/auth/src/routes/wallet.ts:34)` · [tamper.out, verbatim]: `tampered /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/spark_secuura_2026-10-20_ks_1500_p1_005137/clone/Blockchain/Dev/services/auth/src/routes/wallet.ts:34: "import { canonicalWalletAddress, syntheticWalletEmail } from '../utils/walletEmail';" -> "import { syntheticWalletEmail } from '../utils/walletEmail'; function canonicalWalletAddress(a: string): string { return a; }"` · [checker.out, verbatim]: `A4 (test-only): tamper reverted (Blockchain/Dev/services/auth/src/routes/wallet.ts back to the tip)` (tamper_revert.out EMPTY) · the tamper's `from` equals the product's tip line 34. [apply_product.out, verbatim]: `A5 (test-only): no product hunk — the test must be GREEN at the untouched tip`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=1 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/auth/src/__tests__/ks963-preauth-rethrow.test.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks963-preauth-rethrow.test.ts fails at the untouched tip (1 failed / 26 run; controls green; assertion reds)` [red_first.json: failed=1 of total=26; red cell(s): ['KS-963 widened — a DB failure no longer burns a single-use token RED KS-1500 m2 - wallet.ts uses the canonicalWalletAddress it IMPORTS from ../utils/walletEmail and declares no binding of that name']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks963-preauth-rethrow.test.ts passes with the product hunk (26 passed / 26 run)` [green_after.json: failed=0 of total=26, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1089 failed=0 | after: total=1090 failed=0` · `NEW reds: []` [baseline_suite.json total=1089 failed=0; after_suite.json total=1090 failed=0]
- A6 [verbatim]: `PASS A6 whole services/auth suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/auth: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=1 +7/-0 test=src/__tests__/ks963-preauth-rethrow.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** TEST-ONLY — ZERO PRODUCT BYTES: one file, the test `Blockchain/Dev/services/auth/src/__tests__/ks963-preauth-rethrow.test.ts` (+7/-0 per numstat.out); the product `Blockchain/Dev/services/auth/src/routes/wallet.ts` is the tamper target and is byte-unchanged (sha256 17cd98c3cad1cb57, measured). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict) — at the tip `a66cd6a4d1726794c816fd4fefec58c728d410e5` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: the gate decides (test file only). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1500_p1/input.json`. Brief (located from the run dir's own name under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1500_p1/KS-1500.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1500_p1/checker.out`.

```diff
--- a/Blockchain/Dev/services/auth/src/__tests__/ks963-preauth-rethrow.test.ts
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks963-preauth-rethrow.test.ts
@@ -415,6 +415,13 @@
     expect(code).not.toMatch(/\bawait\b|\bquery\s*\(|\bfetch\s*\(|\brequire\s*\(|\bimport\s*\(|\bprocess\.|\bfs\b|\bdb\b/);
     expect(code).not.toMatch(/\w\s*=[^=]/); // no assignment other than the signature's own: a pure expression
   });
+  // KS-1500 m2: PURE_BEFORE_LOOKUP matches the NAME canonicalWalletAddress, so a local impure function of that name in wallet.ts would
+  // shadow the pure export and stay green. Pin where the name comes from, and that wallet.ts binds it nowhere itself.
+  it('RED KS-1500 m2 - wallet.ts uses the canonicalWalletAddress it IMPORTS from ../utils/walletEmail and declares no binding of that name', async () => {
+    const src = await readRoute('wallet.ts');
+    expect(src).toMatch(/import\s*\{[^}]*\bcanonicalWalletAddress\b[^}]*\}\s*from\s*'\.\.\/utils\/walletEmail'/);
+    expect(blankCommentsAndStrings(src)).not.toMatch(/\b(?:function|const|let|var|class)\s+canonicalWalletAddress\b/);
+  });
   it('KS-1131 F-C a fire-and-forget write (void query) before the wallet lookup is NOT allowed', () => {
     const src = walletFn("  void query('INSERT INTO users (id) VALUES (1)');");
     expect(() => assertWalletNothingWrittenBeforeLookup(src)).toThrow();
```
