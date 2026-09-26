# READY — KS-1337 akto site (systemTest/akto/tests/preSuiteSetup.ts:36) — Spark (DeepSeek V4 Flash), RUNG 4 brief, code_patch, vitest — PASS 7/7 — HELD for QA

**Held 21:31 2026-09-26 by Wednesday BY HAND:** `hold_ready.py` REFUSED rc 2 (no `PASS A3c` line — a rung-4 brief gives no expected `+` lines, so the checker skipped A3c/A3i). Tooling gap owned on Wednesday's side (IMPROVEMENTS row). Every verdict line below is COPIED from `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-26_KS-1337-akto/checker.out`. **Wednesday's source read:** the model's diff (`out.md.checker/patch.diff`) is BYTE-IDENTICAL to `night/briefs/KS-1337/golden/KS-1337-akto.golden.diff` (sha1 27033ab4); the only product `-` line is the `.pathname` line; product `+` lines: `import { fileURLToPath } from 'node:url';` and the `fileURLToPath(new URL('../../fixtures/pre-suite.ts', import.meta.url))` line — the ticket's idiom.

**Rung-4 caveat (recorded, not hidden):** the brief quoted #1291's whole product expression and both hunk headers, so this measures ADAPTING a quoted pattern, not deriving the fix. It is not yet a clean rung-4 result.

## Checker verdict (verbatim)
```
PASS A1 output is exactly one fenced ```diff block, nothing outside it
PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)
PASS A3 touched-file set == { systemTest/akto/tests/preSuiteSetup.ts , systemTest/akto/tests/unit/setup/ks1337-preSuiteSetupPathWithASpace.test.ts }
PASS A3b every must_change site the ticket names is changed by the product hunk (1 site(s))
INFO A3i skipped — the input carries no expected '+' lines (a legacy or brief-less input); indentation not measured
PASS A4 RED-FIRST: tests/unit/setup/ks1337-preSuiteSetupPathWithASpace.test.ts fails at the untouched tip (1 failed / 3 run; controls green; assertion reds)
PASS A5 GREEN-AFTER: tests/unit/setup/ks1337-preSuiteSetupPathWithASpace.test.ts passes with the product hunk (3 passed / 3 run)
PASS A6 whole . suite: no NEW red vs the untouched tip
PASS A7 tsc --noEmit for .: rc 0 after the patch (baseline rc=0)
SUMMARY files=2 +81/-1 test=tests/unit/setup/ks1337-preSuiteSetupPathWithASpace.test.ts red_first=yes apply_mode=strict
RESULT: PASS (7/7)
PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=2 ok=2 bad=0 skipped_newfile=1)
SPARK RESULT: PASS (checker rc 0 + A2a anchor OK)
```

## PR NOTES for the raise seat
- CODE_PATCH, tool package `systemTest/akto`: `tests/preSuiteSetup.ts` (+2/-1) + the new test cell (see diff). Refs KS-1337 (site 2 of 3; KS-1337 stays In Progress — the playwright site remains, its runner is not vitest). Tier 2 (tooling). Run the akto package's own lint + format:check before pushing; quote only the gate lines the push prints.
- Base: develop 3f70224a069b.

## Canonical patch (== the model's output == golden)
```diff
--- a/systemTest/akto/tests/preSuiteSetup.ts
+++ b/systemTest/akto/tests/preSuiteSetup.ts
@@ -12,1 +12,2 @@
+import { fileURLToPath } from 'node:url';
 import { spawnSync } from 'node:child_process';
@@ -35,3 +36,3 @@
 function runPreSuiteStep(label: string): void {
-    const step = new URL('../../fixtures/pre-suite.ts', import.meta.url).pathname;
+    const step = fileURLToPath(new URL('../../fixtures/pre-suite.ts', import.meta.url));
     const res = spawnSync('npx', ['tsx', step, label], { stdio: 'inherit' });
--- /dev/null
+++ b/systemTest/akto/tests/unit/setup/ks1337-preSuiteSetupPathWithASpace.test.ts
@@ -0,0 +1,79 @@
+/**
+ * KS-1337 (akto site): tests/preSuiteSetup.ts resolved the shared pre-suite step with
+ * new URL(...).pathname. A URL pathname is percent-encoded, so a checkout whose directory holds a
+ * space (the QA gate's own Testing Agent MAIN) handed tsx a path carrying %20 and the step died with
+ * ERR_MODULE_NOT_FOUND. preSuiteSetup.ts spawns npx at setup(), so this suite copies its own
+ * const step statement into a probe module planted at tests/ inside a temp checkout, imports the
+ * probe for real, and checks the path it yields is the file. Same shape as the performance
+ * runner's merged KS-1337 cell (#1291).
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
+const SETUP_LINES = readFileSync(fileURLToPath(new URL('../../preSuiteSetup.ts', import.meta.url)), 'utf8').split(NL);
+const STEP_LINES = SETUP_LINES.filter((line) => line.trim().startsWith('const step = '));
+const STATEMENT = String(STEP_LINES[0]).trim();
+
+let root = '';
+
+beforeEach(() => {
+    root = mkdtempSync(join(tmpdir(), 'ks1337-akto-'));
+});
+afterEach(() => {
+    rmSync(root, { recursive: true, force: true });
+});
+
+/**
+ * Plant checkoutName/systemTest/{fixtures/pre-suite.ts, akto/tests/probe.mjs}; import the probe.
+ *
+ * @param {string} checkoutName - The checkout directory's name; may contain spaces.
+ * @returns {Promise<{ resolved: string; preSuite: string }>} The path the statement yields, and the real file.
+ */
+async function stepFrom(checkoutName: string): Promise<{ resolved: string; preSuite: string }> {
+    const systemTest = join(root, checkoutName, 'systemTest');
+    mkdirSync(join(systemTest, 'fixtures'), { recursive: true });
+    mkdirSync(join(systemTest, 'akto', 'tests'), { recursive: true });
+    const preSuite = join(systemTest, 'fixtures', 'pre-suite.ts');
+    writeFileSync(preSuite, 'export {};');
+    const probe = join(systemTest, 'akto', 'tests', 'probe.mjs');
+    writeFileSync(
+        probe,
+        [
+            'import * as url from ' + SQ + 'node:url' + SQ + ';',
+            'import { fileURLToPath } from ' + SQ + 'node:url' + SQ + ';',
+            STATEMENT,
+            'export { step, url, fileURLToPath };',
+        ].join(NL),
+    );
+    const mod = (await import(pathToFileURL(probe).href)) as { step: string };
+    return { resolved: mod.step, preSuite };
+}
+
+describe('KS-1337 akto: the pre-suite step path survives a checkout directory with spaces', () => {
+    it('control KS-1337 akto: preSuiteSetup.ts has one step statement and it names fixtures/pre-suite.ts', () => {
+        expect(STEP_LINES).toHaveLength(1);
+        expect(STATEMENT).toContain('../../fixtures/pre-suite.ts');
+        expect(STATEMENT).toContain('import.meta.url');
+        expect(STATEMENT.endsWith(';')).toBe(true);
+    });
+
+    it('control KS-1337 akto: from a checkout path WITHOUT spaces the step is the real pre-suite file', async () => {
+        const { resolved, preSuite } = await stepFrom('TestingAgentMAIN');
+        expect(resolved).toBe(preSuite);
+        expect(existsSync(resolved)).toBe(true);
+    });
+
+    it('RED KS-1337 akto: from a checkout path WITH spaces the step is the real pre-suite file, not a percent-encoded one', async () => {
+        const { resolved, preSuite } = await stepFrom('Testing Agent MAIN');
+        expect(resolved).toBe(preSuite);
+        expect(existsSync(resolved)).toBe(true);
+    });
+});
```
