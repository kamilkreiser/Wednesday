# READY — KS-1391-KS-1391 (Spark (DeepSeek V4 Flash), briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-26_ks_1391_p1/out.md.checker/patch.diff`** (from `ls` at 08:48 2026-10-26; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-26_ks_1391_p1/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-26_ks_1391_p1/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden path `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1391_p1/golden.diff/out.md.checker/patch.diff` does not exist — no identity claim is made.

**Held 08:48 2026-10-26 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-26_ks_1391_p1/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `1ae6f17d19a8d973a77714dfe08dee0486b0af65`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/frontend/issuer/package.json , Blockchain/Dev/frontend/issuer/src/__tests__/ks1391-issuer-declares-a-test-script.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/frontend/issuer/package.json` (product) and `Blockchain/Dev/frontend/issuer/src/__tests__/ks1391-issuer-declares-a-test-script.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
1	0	Blockchain/Dev/frontend/issuer/package.json
30	0	Blockchain/Dev/frontend/issuer/src/__tests__/ks1391-issuer-declares-a-test-script.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (1 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 1 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 0.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/frontend/issuer/package.json byte-exact incl. leading whitespace (apply mode strict): OK 1 line(s) byte-exact incl. leading whitespace (of 1; 1 line(s) added by the apply)` [a3i_indent.out: `OK 1 line(s) byte-exact incl. leading whitespace (of 1; 1 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/frontend/issuer/package.json` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/frontend/issuer/src/__tests__/ks1391-issuer-declares-a-test-script.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1391-issuer-declares-a-test-script.test.ts fails at the untouched tip (1 failed / 3 run; controls green; assertion reds)` [red_first.json: failed=1 of total=3; red cell(s): ['KS-1391 - frontend/issuer/package.json reaches its own vitest specs RED KS-1391 R1 the scripts block declares test as vitest run']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1391-issuer-declares-a-test-script.test.ts passes with the product hunk (3 passed / 3 run)` [green_after.json: failed=0 of total=3, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=12 failed=0 | after: total=15 failed=0` · `NEW reds: []` [baseline_suite.json total=12 failed=0; after_suite.json total=15 failed=0]
- A6 [verbatim]: `PASS A6 whole frontend/issuer suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for frontend/issuer: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +31/-0 test=src/__tests__/ks1391-issuer-declares-a-test-script.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/frontend/issuer/package.json` (+1/-0 per numstat.out) and the test file `Blockchain/Dev/frontend/issuer/src/__tests__/ks1391-issuer-declares-a-test-script.test.ts` (+30/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `1ae6f17d19a8d973a77714dfe08dee0486b0af65` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-26_ks_1391_p1/input.json`. Brief (given by --brief; its `# ` heading names KS-1391): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1391_p1/KS-1391.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-26_ks_1391_p1/checker.out`.

```diff
diff --git a/Blockchain/Dev/frontend/issuer/package.json b/Blockchain/Dev/frontend/issuer/package.json
--- a/Blockchain/Dev/frontend/issuer/package.json
+++ b/Blockchain/Dev/frontend/issuer/package.json
@@ -10,2 +10,3 @@
     "lint": "eslint src",
+    "test": "vitest run",
     "check:bundle": "node scripts/check-bundle-size.mjs"
diff --git a/Blockchain/Dev/frontend/issuer/src/__tests__/ks1391-issuer-declares-a-test-script.test.ts b/Blockchain/Dev/frontend/issuer/src/__tests__/ks1391-issuer-declares-a-test-script.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/frontend/issuer/src/__tests__/ks1391-issuer-declares-a-test-script.test.ts
@@ -0,0 +1,30 @@
+/**
+ * KS-1391 - the issuer frontend declares a `test` script, so `npm test -w frontend/issuer` can run its specs.
+ *
+ * Before KS-1391 the scripts block of frontend/issuer/package.json had dev, build, preview, lint and check:bundle but no
+ * `test`, so the specs beside this file could not be reached from any runner. This pins the one line that reaches them.
+ */
+import { describe, it, expect } from 'vitest';
+import { readFileSync } from 'node:fs';
+import { dirname, resolve } from 'node:path';
+import { fileURLToPath } from 'node:url';
+
+const here = dirname(fileURLToPath(import.meta.url));
+const pkg = JSON.parse(readFileSync(resolve(here, '../../package.json'), 'utf8')) as {
+  scripts: Record<string, string>;
+  devDependencies: Record<string, string>;
+};
+
+describe('KS-1391 - frontend/issuer/package.json reaches its own vitest specs', () => {
+  it('RED KS-1391 R1 the scripts block declares test as vitest run', () => {
+    expect(pkg.scripts.test).toBe('vitest run');
+  });
+
+  it('CONTROL KS-1391 C1 the existing scripts are all still declared', () => {
+    expect(Object.keys(pkg.scripts)).toEqual(expect.arrayContaining(['dev', 'build', 'preview', 'lint', 'check:bundle']));
+  });
+
+  it('CONTROL KS-1391 C2 vitest is a declared devDependency, so the script has something to run', () => {
+    expect(pkg.devDependencies.vitest).toBeTruthy();
+  });
+});
```
