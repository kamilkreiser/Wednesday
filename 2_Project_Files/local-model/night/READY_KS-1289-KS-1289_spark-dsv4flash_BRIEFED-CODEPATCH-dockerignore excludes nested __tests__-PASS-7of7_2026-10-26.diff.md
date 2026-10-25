# READY — KS-1289-KS-1289 (Spark (DeepSeek V4 Flash), briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-26_ks_1289_p1/out.md.checker/patch.diff`** (from `ls` at 08:50 2026-10-26; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-26_ks_1289_p1/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-26_ks_1289_p1/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden path `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1289_p1/golden.diff/out.md.checker/patch.diff` does not exist — no identity claim is made.

**Held 08:50 2026-10-26 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-26_ks_1289_p1/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `1ae6f17d19a8d973a77714dfe08dee0486b0af65`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/.dockerignore , Blockchain/Dev/packages/shared/src/__tests__/ks1289-dockerignore-excludes-nested-tests.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/.dockerignore` (product) and `Blockchain/Dev/packages/shared/src/__tests__/ks1289-dockerignore-excludes-nested-tests.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
1	0	Blockchain/Dev/.dockerignore
34	0	Blockchain/Dev/packages/shared/src/__tests__/ks1289-dockerignore-excludes-nested-tests.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (1 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 1 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 0.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/.dockerignore byte-exact incl. leading whitespace (apply mode strict): OK 1 line(s) byte-exact incl. leading whitespace (of 1; 1 line(s) added by the apply)` [a3i_indent.out: `OK 1 line(s) byte-exact incl. leading whitespace (of 1; 1 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/.dockerignore` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/packages/shared/src/__tests__/ks1289-dockerignore-excludes-nested-tests.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1289-dockerignore-excludes-nested-tests.test.ts fails at the untouched tip (1 failed / 4 run; controls green; assertion reds)` [red_first.json: failed=1 of total=4; red cell(s): ['KS-1289 - Blockchain/Dev/.dockerignore excludes nested __tests__ directories RED KS-1289 R1 a line excludes __tests__ at any depth']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1289-dockerignore-excludes-nested-tests.test.ts passes with the product hunk (4 passed / 4 run)` [green_after.json: failed=0 of total=4, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=994 failed=2 | after: total=998 failed=1` · `NEW reds: []` [baseline_suite.json total=994 failed=2; after_suite.json total=998 failed=1]
- A6 [verbatim]: `PASS A6 whole packages/shared suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for packages/shared: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +35/-0 test=src/__tests__/ks1289-dockerignore-excludes-nested-tests.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/.dockerignore` (+1/-0 per numstat.out) and the test file `Blockchain/Dev/packages/shared/src/__tests__/ks1289-dockerignore-excludes-nested-tests.test.ts` (+34/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `1ae6f17d19a8d973a77714dfe08dee0486b0af65` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-26_ks_1289_p1/input.json`. Brief (given by --brief; its `# ` heading names KS-1289): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1289_p1/KS-1289.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-26_ks_1289_p1/checker.out`.

```diff
diff --git a/Blockchain/Dev/.dockerignore b/Blockchain/Dev/.dockerignore
--- a/Blockchain/Dev/.dockerignore
+++ b/Blockchain/Dev/.dockerignore
@@ -13,2 +13,3 @@
 tests
+**/__tests__
 contracts/secuura/build
diff --git a/Blockchain/Dev/packages/shared/src/__tests__/ks1289-dockerignore-excludes-nested-tests.test.ts b/Blockchain/Dev/packages/shared/src/__tests__/ks1289-dockerignore-excludes-nested-tests.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/packages/shared/src/__tests__/ks1289-dockerignore-excludes-nested-tests.test.ts
@@ -0,0 +1,34 @@
+/**
+ * KS-1289 - Blockchain/Dev/.dockerignore keeps every nested __tests__ directory out of the build context.
+ *
+ * A .dockerignore pattern is matched from the build-context root, not at any depth (unlike .gitignore). The line `tests`
+ * therefore matches only a top-level tests/ directory, and every services/<name>/src/__tests__/ directory stayed in the
+ * context: test sources shipped into runtime images, and a change to one shared test file invalidated the cache of services
+ * whose runtime code had not changed. `**` + `/__tests__` is the pattern that matches at any depth.
+ */
+import { describe, it, expect } from 'vitest';
+import { readFileSync } from 'node:fs';
+import { dirname, resolve } from 'node:path';
+import { fileURLToPath } from 'node:url';
+
+const here = dirname(fileURLToPath(import.meta.url));
+// packages/shared/src/__tests__ -> four levels up is Blockchain/Dev, the build-context root
+const lines = readFileSync(resolve(here, '../../../../.dockerignore'), 'utf8').split('\n');
+
+describe('KS-1289 - Blockchain/Dev/.dockerignore excludes nested __tests__ directories', () => {
+  it('RED KS-1289 R1 a line excludes __tests__ at any depth', () => {
+    expect(lines).toContain('**/__tests__');
+  });
+
+  it('CONTROL KS-1289 C1 the original top-level tests line is still there', () => {
+    expect(lines).toContain('tests');
+  });
+
+  it('CONTROL KS-1289 C2 the whatsapp-bot re-include is still there, so its build keeps its sources', () => {
+    expect(lines).toContain('!connectors/whatsapp-bot');
+  });
+
+  it('CONTROL KS-1289 C3 the docs/openapi re-include is still there', () => {
+    expect(lines).toContain('!docs/openapi');
+  });
+});
```
