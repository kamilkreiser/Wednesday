# READY — KS-1143-GUARDMENTION-SELFTEST-1 (Ornith, briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-23_ks1143-ornith35b-night2/out.md.checker/patch.diff`** (from `ls` at 18:21 2026-09-23; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-23_ks1143-ornith35b-night2/out.md.checker/section_1.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; CONTENT-compared against the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-23_ks1143-R19-golden-selftest-arm-C1/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1); change lines (`+`/`-`, ordered) IDENTICAL in every file; body lines (context included) identical in every file; hunk headers differ (ks781-p3-3-body-parser-order.test.ts: golden `@@ -2324,7 +2324,7 @@` vs run `@@ -2324,7 +2324,7 @@ function routerParserAnalysis(source: string, fileName: string): RouterParserSite`; ks781-p3-3-body-parser-order.test.ts: golden `@@ -2549,3 +2549,7 @@` vs run `@@ -2549,3 +2549,7 @@ describe('KS-828 — LEG F sees the guard LEAVE a wrapped router (the wrapper body`); APPLIED RESULT IDENTICAL: both patches applied strictly (`git apply -p1`, scratch tempdir) to the tip content carried in input.json['files'] yield byte-identical files (ks781-p3-3-body-parser-order.test.ts, sha256 equal).

**Held 18:21 2026-09-23 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-23_ks1143-ornith35b-night2/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `2bc5ccf63b8c40911afb568b03cace066238ffcf`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (self-testing) touched-file set == { Blockchain/Dev/packages/shared/src/__tests__/ks781-p3-3-body-parser-order.test.ts } — one file that is both the product and its test (under Blockchain/Dev/packages/shared/src/__tests__)`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/packages/shared/src/__tests__/ks781-p3-3-body-parser-order.test.ts` (product) and `Blockchain/Dev/packages/shared/src/__tests__/ks781-p3-3-body-parser-order.test.ts` (test) — equal to numstat.out's set (1 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
5	1	Blockchain/Dev/packages/shared/src/__tests__/ks781-p3-3-body-parser-order.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (5 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 5 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 1.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/packages/shared/src/__tests__/ks781-p3-3-body-parser-order.test.ts byte-exact incl. leading whitespace (apply mode strict): OK 5 line(s) byte-exact incl. leading whitespace (of 5; 5 line(s) added by the apply)` [a3i_indent.out: `OK 5 line(s) byte-exact incl. leading whitespace (of 5; 5 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=1 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/packages/shared/src/__tests__/ks781-p3-3-body-parser-order.test.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks781-p3-3-body-parser-order.test.ts fails at the untouched tip (1 failed / 232 run; controls green; assertion reds)` [red_first.json: failed=1 of total=232; red cell(s): ['KS-828 — LEG F sees the guard LEAVE a wrapped router (the wrapper body must reach a guard call) W6 KS-1143 GF-1 - a MENTION of a guard-bound local inside the wrapper is NOT a mount']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks781-p3-3-body-parser-order.test.ts passes with the product hunk (232 passed / 232 run)` [green_after.json: failed=0 of total=232, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=917 failed=0 | after: total=918 failed=0` · `NEW reds: []` [baseline_suite.json total=917 failed=0; after_suite.json total=918 failed=0]
- A6 [verbatim]: `PASS A6 whole packages/shared suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for packages/shared: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=1 +5/-1 test=src/__tests__/ks781-p3-3-body-parser-order.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/packages/shared/src/__tests__/ks781-p3-3-body-parser-order.test.ts` (+5/-1 per numstat.out) — ONE file: it is both the product and its test (self-testing mode; red-first is by HUNK, not by file). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict) — at the tip `2bc5ccf63b8c40911afb568b03cace066238ffcf` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-23_ks1143-ornith35b-night2/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-23_ks1143-ornith35b-night2/checker.out`.

```diff
--- a/Blockchain/Dev/packages/shared/src/__tests__/ks781-p3-3-body-parser-order.test.ts
+++ b/Blockchain/Dev/packages/shared/src/__tests__/ks781-p3-3-body-parser-order.test.ts
@@ -2324,7 +2324,7 @@ function routerParserAnalysis(source: string, fileName: string): RouterParserSite
       const walk = (m: ts.Node): void => {
         if (hit) return;
         if (guardCallName(m, b)) { hit = true; return; }
-        if (ts.isIdentifier(m) && (guardSyms.has(m.text) || guardedWrappers.has(m.text))) { hit = true; return; }
+        if (ts.isCallExpression(m) && ts.isIdentifier(m.expression) && (guardSyms.has(m.expression.text) || guardedWrappers.has(m.expression.text))) { hit = true; return; }
         ts.forEachChild(m, walk);
       };
       walk(body);
@@ -2549,3 +2549,7 @@ describe('KS-828 — LEG F sees the guard LEAVE a wrapped router (the wrapper body
     expect(routerParserSites(src, 'x.ts')).toEqual({ routes: 1, guarded: 'none' });
   });
+  it('W6 KS-1143 GF-1 - a MENTION of a guard-bound local inside the wrapper is NOT a mount', () => {
+    const src = wrapperModule('      void g; next();', '  const g = rejectControlBytes();');
+    expect(routerParserSites(src, 'x.ts')).toEqual({ routes: 2, guarded: false });
+  });
 });
```
