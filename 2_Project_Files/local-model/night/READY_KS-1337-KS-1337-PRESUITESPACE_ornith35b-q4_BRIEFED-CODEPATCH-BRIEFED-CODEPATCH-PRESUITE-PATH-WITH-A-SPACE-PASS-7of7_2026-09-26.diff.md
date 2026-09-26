# READY — KS-1337-KS-1337-PRESUITESPACE (Ornith, briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-26_ks1337-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 18:46 2026-09-26; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-26_ks1337-ornith35b-night/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-26_ks1337-ornith35b-night/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden path `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1337.golden/KS-1337.golden.diff/out.md.checker/patch.diff` does not exist — no identity claim is made.

**Held 18:46 2026-09-26 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-26_ks1337-ornith35b-night/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `179a4f32ec0643689b55a8d7207e63f6ec3d3831`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { systemTest/performance/runner/cli.ts , systemTest/performance/tests/unit/runner/ks1337-preSuitePathWithASpace.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `systemTest/performance/runner/cli.ts` (product) and `systemTest/performance/tests/unit/runner/ks1337-preSuitePathWithASpace.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
4	1	systemTest/performance/runner/cli.ts
69	0	systemTest/performance/tests/unit/runner/ks1337-preSuitePathWithASpace.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (4 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 4 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 1.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied systemTest/performance/runner/cli.ts byte-exact incl. leading whitespace (apply mode strict): OK 4 line(s) byte-exact incl. leading whitespace (of 4; 4 line(s) added by the apply)` [a3i_indent.out: `OK 4 line(s) byte-exact incl. leading whitespace (of 4; 4 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `systemTest/performance/runner/cli.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `systemTest/performance/tests/unit/runner/ks1337-preSuitePathWithASpace.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: tests/unit/runner/ks1337-preSuitePathWithASpace.test.ts fails at the untouched tip (1 failed / 3 run; controls green; assertion reds)` [red_first.json: failed=1 of total=3; red cell(s): ['KS-1337: the pre-suite step path survives a checkout directory with spaces RED KS-1337: from a checkout path WITH spaces the step is the real pre-suite file, not a percent-encoded one']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: tests/unit/runner/ks1337-preSuitePathWithASpace.test.ts passes with the product hunk (3 passed / 3 run)` [green_after.json: failed=0 of total=3, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1114 failed=1 | after: total=1117 failed=1` · `NEW reds: []` [baseline_suite.json total=1114 failed=1; after_suite.json total=1117 failed=1]
- A6 [verbatim]: `PASS A6 whole . suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for .: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +73/-1 test=tests/unit/runner/ks1337-preSuitePathWithASpace.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `systemTest/performance/runner/cli.ts` (+4/-1 per numstat.out) and the test file `systemTest/performance/tests/unit/runner/ks1337-preSuitePathWithASpace.test.ts` (+69/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `179a4f32ec0643689b55a8d7207e63f6ec3d3831` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-26_ks1337-ornith35b-night/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-26_ks1337-ornith35b-night/checker.out`.

```diff
--- a/systemTest/performance/runner/cli.ts
+++ b/systemTest/performance/runner/cli.ts
@@ -28,2 +28,3 @@
 import * as path from 'node:path';
+import { fileURLToPath } from 'node:url';
 import { spawnSync } from 'node:child_process';
@@ -159,5 +160,7 @@
         process.exit(2);
     }
 }
-const preSuiteStep = new URL('../../fixtures/pre-suite.ts', import.meta.url).pathname;
+// KS-1337: fileURLToPath, not .pathname - a URL pathname is percent-encoded, so a checkout directory
+// with a space in its name handed tsx a path with %20 in it and the step died ERR_MODULE_NOT_FOUND.
+const preSuiteStep = fileURLToPath(new URL('../../fixtures/pre-suite.ts', import.meta.url));
 // KS-1016 (exploratory testing, 2026-09-11): hand the step THIS run's target, as Playwright's
--- /dev/null
+++ b/systemTest/performance/tests/unit/runner/ks1337-preSuitePathWithASpace.test.ts
@@ -0,0 +1,69 @@
+/**
+ * KS-1337: runner/cli.ts resolved the pre-suite step with new URL(...).pathname. A URL pathname is
+ * percent-encoded, so a checkout whose directory holds a space (the QA gate's own Testing Agent MAIN)
+ * handed tsx a path carrying %20 and the step died with ERR_MODULE_NOT_FOUND. cli.ts runs its whole
+ * flow at import, so this suite copies cli.ts's own preSuiteStep statement into a probe module planted
+ * at runner/ inside a temp checkout, imports it for real, and checks the path it yields is the file.
+ *
+ * @module tests/unit/runner/ks1337-preSuitePathWithASpace.test
+ */
+
+import { existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
+import { tmpdir } from 'node:os';
+import { join } from 'node:path';
+import { fileURLToPath, pathToFileURL } from 'node:url';
+
+import { afterEach, beforeEach, describe, expect, it } from 'vitest';
+
+// A newline and a single quote, so no line below needs a backslash or a double-quoted string.
+const NL = String.fromCharCode(10);
+const SQ = String.fromCharCode(39);
+const CLI_LINES = readFileSync(fileURLToPath(new URL('../../../runner/cli.ts', import.meta.url)), 'utf8').split(NL);
+const STATEMENT = CLI_LINES.find((line) => line.startsWith('const preSuiteStep = '));
+
+let root = '';
+
+beforeEach(() => {
+    root = mkdtempSync(join(tmpdir(), 'ks1337-'));
+});
+afterEach(() => {
+    rmSync(root, { recursive: true, force: true });
+});
+
+/** Plant checkoutName/systemTest/{fixtures/pre-suite.ts, performance/runner/probe.mjs}; import the probe. */
+async function preSuiteStepFrom(checkoutName: string): Promise<{ resolved: string; preSuite: string }> {
+    const systemTest = join(root, checkoutName, 'systemTest');
+    mkdirSync(join(systemTest, 'fixtures'), { recursive: true });
+    mkdirSync(join(systemTest, 'performance', 'runner'), { recursive: true });
+    const preSuite = join(systemTest, 'fixtures', 'pre-suite.ts');
+    writeFileSync(preSuite, 'export {};');
+    const probe = join(systemTest, 'performance', 'runner', 'probe.mjs');
+    writeFileSync(probe, [
+        'import * as url from ' + SQ + 'node:url' + SQ + ';',
+        'import { fileURLToPath } from ' + SQ + 'node:url' + SQ + ';',
+        String(STATEMENT),
+        'export { preSuiteStep, url, fileURLToPath };',
+    ].join(NL));
+    const mod = (await import(pathToFileURL(probe).href)) as { preSuiteStep: string };
+    return { resolved: mod.preSuiteStep, preSuite };
+}
+
+describe('KS-1337: the pre-suite step path survives a checkout directory with spaces', () => {
+    it('control KS-1337: cli.ts has one preSuiteStep statement and it names fixtures/pre-suite.ts', () => {
+        expect(CLI_LINES.filter((line) => line.startsWith('const preSuiteStep = '))).toHaveLength(1);
+        expect(STATEMENT).toContain('../../fixtures/pre-suite.ts');
+        expect(STATEMENT).toContain('import.meta.url');
+    });
+
+    it('control KS-1337: from a checkout path WITHOUT spaces the step is the real pre-suite file', async () => {
+        const { resolved, preSuite } = await preSuiteStepFrom('TestingAgentMAIN');
+        expect(resolved).toBe(preSuite);
+        expect(existsSync(resolved)).toBe(true);
+    });
+
+    it('RED KS-1337: from a checkout path WITH spaces the step is the real pre-suite file, not a percent-encoded one', async () => {
+        const { resolved, preSuite } = await preSuiteStepFrom('Testing Agent MAIN');
+        expect(resolved).toBe(preSuite);
+        expect(existsSync(resolved)).toBe(true);
+    });
+});
```
