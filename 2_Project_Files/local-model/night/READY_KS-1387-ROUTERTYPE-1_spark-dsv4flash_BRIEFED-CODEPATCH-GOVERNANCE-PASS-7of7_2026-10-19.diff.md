# READY — KS-1387-ROUTERTYPE-1 (Spark (DeepSeek V4 Flash), briefed, code_patch, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1387_p1/out.md.checker/patch.diff`** (from `ls` at 03:01 2026-10-19; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1387_p1/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1387_p1/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; CONTENT-compared against the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1387_p1-control-r2/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1); change lines (`+`/`-`, ordered) IDENTICAL in every file; body lines (context included) DIFFER in governance.ts (run 8 vs golden 11 body lines — context, since the change lines are equal) (identical in ks1387-governance-router-has-an-explicit-type.test.ts); hunk headers identical; APPLIED RESULT not compared (input.json['files'] lacks a touched file's tip content).

**Held 03:01 2026-10-19 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1387_p1/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `385fc288fae831f2ca15b9d091c844f33285b784`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/governance/src/routes/governance.ts , Blockchain/Dev/services/governance/src/__tests__/ks1387-governance-router-has-an-explicit-type.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/governance/src/routes/governance.ts` (product) and `Blockchain/Dev/services/governance/src/__tests__/ks1387-governance-router-has-an-explicit-type.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
3	3	Blockchain/Dev/services/governance/src/routes/governance.ts
34	0	Blockchain/Dev/services/governance/src/__tests__/ks1387-governance-router-has-an-explicit-type.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (1 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 3 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 3.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/governance/src/routes/governance.ts byte-exact incl. leading whitespace (apply mode strict): OK 1 line(s) byte-exact incl. leading whitespace (of 1; 1 line(s) added by the apply)` [a3i_indent.out: `OK 1 line(s) byte-exact incl. leading whitespace (of 1; 1 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/governance/src/routes/governance.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/governance/src/__tests__/ks1387-governance-router-has-an-explicit-type.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1387-governance-router-has-an-explicit-type.test.ts fails at the untouched tip (1 failed / 3 run; controls green; assertion reds)` [red_first.json: failed=1 of total=3; red cell(s): ['KS-1387 - the governance router has an explicit type annotation RED KS-1387 the router declaration carries an explicit Router type annotation']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1387-governance-router-has-an-explicit-type.test.ts passes with the product hunk (3 passed / 3 run)` [green_after.json: failed=0 of total=3, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=116 failed=0 | after: total=119 failed=0` · `NEW reds: []` [baseline_suite.json total=116 failed=0; after_suite.json total=119 failed=0]
- A6 [verbatim]: `PASS A6 whole services/governance suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/governance: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +37/-3 test=src/__tests__/ks1387-governance-router-has-an-explicit-type.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/governance/src/routes/governance.ts` (+3/-3 per numstat.out) and the test file `Blockchain/Dev/services/governance/src/__tests__/ks1387-governance-router-has-an-explicit-type.test.ts` (+34/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `385fc288fae831f2ca15b9d091c844f33285b784` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1387_p1/input.json`. Brief (located from the run dir's own name under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1387_p1/KS-1387.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1387_p1/checker.out`.

```diff
--- a/Blockchain/Dev/services/governance/src/routes/governance.ts
+++ b/Blockchain/Dev/services/governance/src/routes/governance.ts
@@ -17,5 +17,5 @@ import {
 } from '../types/governance.types';
-
-const router = Router();
-
+
+const router: Router = Router();
+
 // =============================================================================
--- /dev/null
+++ b/Blockchain/Dev/services/governance/src/__tests__/ks1387-governance-router-has-an-explicit-type.test.ts
@@ -0,0 +1,34 @@
+/**
+ * =============================================================================
+ * KS-1387 - the governance router is declared with an explicit type
+ * =============================================================================
+ * `const router = Router();` leaves the exported router's type to inference. When @secuura/shared brings its own
+ * @types/express-serve-static-core, the compiler cannot name the inferred type in the declaration file it emits
+ * (`declaration: true` in this service's tsconfig) and `npm run build` stops with TS2742. That broke a clean image build
+ * of the governance service. The usual remedy is an annotation, `const router: Router = Router();`.
+ *
+ * The compiler error only appears on some install layouts, so these cells read the route's own source text (as the
+ * other source-reading tests in this repo do) and pin the annotation itself.
+ * =============================================================================
+ */
+import * as fs from 'fs';
+import * as path from 'path';
+
+const SOURCE = fs.readFileSync(path.resolve(__dirname, '..', 'routes', 'governance.ts'), 'utf8');
+const DECLARATIONS = SOURCE.split('\n').filter((l) => /^(export\s+)?const\s+router\b/.test(l));
+
+describe('KS-1387 - the governance router has an explicit type annotation', () => {
+  it('CONTROL the instrument reads the real route file: one router declaration, imported Router, and routes on it', () => {
+    expect(DECLARATIONS).toHaveLength(1);
+    expect(SOURCE).toContain("import { Router, Request, Response, NextFunction } from 'express';");
+    expect(SOURCE).toContain("router.post('/participants/register'");
+  });
+
+  it('CONTROL the declaration is initialised from Router()', () => {
+    expect(DECLARATIONS[0]).toMatch(/=\s*Router\(\);\s*$/);
+  });
+
+  it('RED KS-1387 the router declaration carries an explicit Router type annotation', () => {
+    expect(DECLARATIONS[0]).toMatch(/^const router:\s*Router\s*=/);
+  });
+});
```
