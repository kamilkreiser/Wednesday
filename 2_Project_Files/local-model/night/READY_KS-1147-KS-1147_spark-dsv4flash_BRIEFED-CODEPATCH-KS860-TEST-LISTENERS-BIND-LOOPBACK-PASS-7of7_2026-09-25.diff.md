# READY — KS-1147-KS-1147 (spark-dsv4flash, briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-25_KS-1147/out.md.checker/patch.diff`** (from `ls` at 15:50 2026-09-25; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-25_KS-1147/out.md.checker/section_1.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-25_KS-1147/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-25_KS-1147/golden_probe/out.md.checker/patch.diff` rc 0, Wednesday (Spark builder)).

**Held 15:50 2026-09-25 by Wednesday (Spark builder) after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-25_KS-1147/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `6ab9d5021e96ea1481cb6c6ff2d6d33b414aecb7`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (self-testing) touched-file set == { Blockchain/Dev/packages/shared/src/__tests__/ks860-test-listeners-bind-loopback.test.ts } — one file that is both the product and its test (under Blockchain/Dev/packages/shared/src/__tests__)`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/packages/shared/src/__tests__/ks860-test-listeners-bind-loopback.test.ts` (product) and `Blockchain/Dev/packages/shared/src/__tests__/ks860-test-listeners-bind-loopback.test.ts` (test) — equal to numstat.out's set (1 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
26	1	Blockchain/Dev/packages/shared/src/__tests__/ks860-test-listeners-bind-loopback.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (22 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 26 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 1.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/packages/shared/src/__tests__/ks860-test-listeners-bind-loopback.test.ts byte-exact incl. leading whitespace (apply mode strict): OK 22 line(s) byte-exact incl. leading whitespace (of 22; 26 line(s) added by the apply)` [a3i_indent.out: `OK 22 line(s) byte-exact incl. leading whitespace (of 22; 26 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=1 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/packages/shared/src/__tests__/ks860-test-listeners-bind-loopback.test.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks860-test-listeners-bind-loopback.test.ts fails at the untouched tip (2 failed / 27 run; controls green; assertion reds)` [red_first.json: failed=2 of total=27; red cell(s): ['KS-1147 - a loopback host with ESCAPED quotes inside a string fixture is accepted RED KS-1147 A - a double-quoted fixture whose host is escaped-double-quoted is ACCEPTED', 'KS-1147 - a loopback host with ESCAPED quotes inside a string fixture is accepted RED KS-1147 B - a single-quoted fixture whose host is escaped-single-quoted is ACCEPTED']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks860-test-listeners-bind-loopback.test.ts passes with the product hunk (27 passed / 27 run)` [green_after.json: failed=0 of total=27, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=918 failed=0 | after: total=922 failed=0` · `NEW reds: []` [baseline_suite.json total=918 failed=0; after_suite.json total=922 failed=0]
- A6 [verbatim]: `PASS A6 whole packages/shared suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for packages/shared: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=1 +26/-1 test=src/__tests__/ks860-test-listeners-bind-loopback.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/packages/shared/src/__tests__/ks860-test-listeners-bind-loopback.test.ts` (+26/-1 per numstat.out) — ONE file: it is both the product and its test (self-testing mode; red-first is by HUNK, not by file). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict) — at the tip `6ab9d5021e96ea1481cb6c6ff2d6d33b414aecb7` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-25_KS-1147/input.json`. Brief (given by --brief; its `# ` heading names KS-1147): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/SPARK-KS-1147/KS-1147.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-25_KS-1147/checker.out`.

```diff
--- a/Blockchain/Dev/packages/shared/src/__tests__/ks860-test-listeners-bind-loopback.test.ts
+++ b/Blockchain/Dev/packages/shared/src/__tests__/ks860-test-listeners-bind-loopback.test.ts
@@ -438,5 +438,6 @@
     if (m[1] === ',') {
       // The host, if there is one, is the next non-space token.
-      const host = /^\s*(['"])127\.0\.0\.1\1/.exec(rest);
+      // KS-1147: a host carried inside a string fixture may be spelled with escaped quotes, \"127.0.0.1\".
+      const host = /^\s*\\?(['"])127\.0\.0\.1\\?\1/.exec(rest);
       ok = host !== null;
     }
@@ -782,3 +783,27 @@
     expect(t).toMatch(/block comment/i);
   });
 });
+
+describe('KS-1147 - a loopback host with ESCAPED quotes inside a string fixture is accepted', () => {
+  // The mask keeps string contents, backslashes included, so a listen call carried as a
+  // string fixture spells its host \"127.0.0.1\" (or \'127.0.0.1\'), never a bare quote.
+  it('RED KS-1147 A - a double-quoted fixture whose host is escaped-double-quoted is ACCEPTED', () => {
+    const src = 'const fixture = "const s = app.listen(0, \\"127.0.0.1\\", resolve);";';
+    expect(offendingListenSites(src, 'fixture.test.ts')).toEqual([]);
+  });
+
+  it('RED KS-1147 B - a single-quoted fixture whose host is escaped-single-quoted is ACCEPTED', () => {
+    const src = "const fixture = 'const s = app.listen(0, \\'127.0.0.1\\');';";
+    expect(offendingListenSites(src, 'fixture.test.ts')).toEqual([]);
+  });
+
+  it('CONTROL KS-1147 C - the same fixture with NO host is still exactly one site', () => {
+    const src = 'const fixture = "const s = app.listen(0, () => {});";';
+    expect(sitesOnly(offendingListenSites(src, 'fixture.test.ts'))).toHaveLength(1);
+  });
+
+  it('CONTROL KS-1147 D - escaped quotes around a NON-loopback host are still exactly one site', () => {
+    const src = 'const fixture = "const s = app.listen(0, \\"0.0.0.0\\");";';
+    expect(sitesOnly(offendingListenSites(src, 'fixture.test.ts'))).toHaveLength(1);
+  });
+});
```
