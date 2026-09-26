# KS-1337 AKTOPRESUITE — RUNG 4 (fix shape in PROSE): the akto pre-suite hook takes its step path through fileURLToPath, not URL.pathname

File: `systemTest/akto/tests/preSuiteSetup.ts`
Tip: `3f70224a069b944334480478ad5d16a5ed33eeae`
Runner: `vitest` (`npx vitest run --config vitest.unit.config.ts <file>` from `systemTest/akto`)

Written 2026-09-26 21:14:42 AEST (shell `date`) by a Spark brief-writer sub-agent for Wednesday, from develop `3f70224a069b` (#1291 merged), file read whole (58 lines, blob `9e74cdd8fad9`, last changed `3af1d37b9` KS-687, 2026-09-11).

**THIS IS A DELIBERATE RUNG-4 BRIEF (Kam's ladder experiment, 2026-09-26).** The product change is stated in PROSE plus the pattern to follow; the two product `+` lines and the hunk headers are NOT given — you write them. The file's CURRENT lines are quoted byte-exact so you copy the `-` line and every context line from the file, never from this prose. The test file IS spelled out in full (copy it byte for byte), so that the only thing this round measures is the product hunk. It was chosen as the SIMPLEST open site of the class (two edit points, one of them a one-line import) so a failure is informative, not noise.

## The mode — read this twice

CODE_PATCH, TWO files. File 1 is the product `systemTest/akto/tests/preSuiteSetup.ts`, MODIFIED IN PLACE (`--- a/systemTest/akto/tests/preSuiteSetup.ts` / `+++ b/systemTest/akto/tests/preSuiteSetup.ts`), exactly TWO hunks. File 2 is a NEW vitest file (`--- /dev/null` / `+++ b/systemTest/akto/tests/unit/setup/ks1337-preSuiteSetupPathWithASpace.test.ts`), ONE hunk `@@ -0,0 +1,79 @@`. There is no third file. You never touch `systemTest/performance/**` (already fixed by #1291), `systemTest/playwright/global-setup.ts` (another package, another runner), `vitest.config.ts`, or the reference test.

## What is wrong (one paragraph)

`preSuiteSetup.ts:36` builds the shared pre-suite step's path with `new URL('../../fixtures/pre-suite.ts', import.meta.url).pathname`. A URL pathname is **percent-encoded**, so when the checkout directory holds a space (the QA gate's own `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/`) the path handed to `npx tsx` at `:37` carries `%20`, and every akto run (this file is the vitest `globalSetup` every akto suite passes through, `:56-:58`) dies `ERR_MODULE_NOT_FOUND` before a test starts. The same defect was fixed in `systemTest/performance/runner/cli.ts` by #1291 (squash `3f70224a069b`, KS-1337's first site); this is the second of the three sites the ticket's sweep names. The fix is the idiom #1291 merged: `fileURLToPath(new URL(...))`. `preSuiteSetup.ts` imports nothing from `node:url` today (0 occurrences of `node:url` and of `fileURLToPath` in the file), so the import is added.

## The exact change (RUNG 4 — prose only; you write the `+` lines and the headers)

**Edit 1 — add the import (a pure insertion, ONE new line).** Add a named import of `fileURLToPath` from the built-in module `'node:url'`, on its OWN line, as a single-line ES import statement in the file's style (single quotes, semicolon, braces with one space inside: the same form as `:12`). Place it IMMEDIATELY ABOVE `:12`. `:12` is then the ONE context line and it comes AFTER your `+` line (trailing context — a pure insertion with trailing context is the shape that applies strictly). Do NOT use `:11` or `:13` as context: both are EMPTY lines.
The current text at `:12` (copy it as your context line, byte for byte, with its leading space in the diff):
`import { spawnSync } from 'node:child_process';`

**Edit 2 — replace `:36` (ONE line out, ONE line in).** Keep the statement's shape — 4 spaces of indent, `const step = `, the SAME relative path string `'../../fixtures/pre-suite.ts'`, the same `import.meta.url` base, the semicolon — and change ONLY how the path is taken from the URL: instead of reading `.pathname` off the `new URL(...)`, pass the `new URL(...)` itself to `fileURLToPath(...)`. That is exactly the change #1291 made to `runner/cli.ts`, whose merged line at develop reads (a DIFFERENT file and variable — adapt, do not paste):
`const preSuiteStep = fileURLToPath(new URL('../../fixtures/pre-suite.ts', import.meta.url));`
Use `:35` and `:37` as the context (one line before, one after — both non-empty). Their current text, and the `-` line, byte for byte:
- `:35` `function runPreSuiteStep(label: string): void {`
- `:36` (the `-` line) `    const step = new URL('../../fixtures/pre-suite.ts', import.meta.url).pathname;`
- `:37` `    const res = spawnSync('npx', ['tsx', step, label], { stdio: 'inherit' });`

**Header arithmetic is yours.** Edit 1 adds one line above `:12`, so every line after it is one further down on the NEW side: hunk 2's old-start is `35`, its new-start is `36`. Each hunk's old count = its context + `-` lines; new count = its context + `+` lines.

**Do NOT touch:** `:37-:40` (the spawn and its refusal — the exit code IS the contract), `:56-:58` (`setup`, the vitest globalSetup export — do not rename), the docblocks (`:1-:10`, `:14-:34`, `:43-:55`, several carry non-ASCII dashes), the variable name `step`. Add NO comment lines (#1291 added two; this brief does not ask for them — two `+` lines in the product file, no more).

## Where (parsed into the checklist — every **must change** line must appear as a `-` line in your diff)

* `:36` — **must change**: `    const step = new URL('../../fixtures/pre-suite.ts', import.meta.url).pathname;`
* `:12` — (correct) `import { spawnSync } from 'node:child_process';` — stays (context)
* `:37` — (correct) `    const res = spawnSync('npx', ['tsx', step, label], { stdio: 'inherit' });` — stays (context)

## THIS IS VITEST (tool package `systemTest/akto`)

`systemTest/akto/package.json` `"test:unit": "vitest run --config vitest.unit.config.ts"` (include `tests/unit/**/*.test.ts`, globals on, node env, NO globalSetup — so running the unit config never calls the hook this file is). Import `describe/it/expect/beforeEach/afterEach` from `'vitest'`. NO `jest.*`, no `vi.mock` needed.

## The test

File: `systemTest/akto/tests/unit/setup/ks1337-preSuiteSetupPathWithASpace.test.ts`

The shape copied is #1291's merged cell `systemTest/performance/tests/unit/runner/ks1337-preSuitePathWithASpace.test.ts` (read at develop, 72 lines): `preSuiteSetup.ts` spawns `npx` at `setup()`, so it cannot be imported by a test. The suite reads the product as TEXT (as the input's reference test `tests/unit/bin/loadTemplatesGuard.test.ts:29-32` reads `bin/load-templates.ts`), takes its OWN `const step = ...;` line, plants it in a `probe.mjs` at `<checkout>/systemTest/akto/tests/` inside a temp dir, imports the probe for real (so `import.meta.url` is a real, space-containing location), and checks the path is the planted `<checkout>/systemTest/fixtures/pre-suite.ts` and exists. The probe imports both `url` and `fileURLToPath` from `node:url`, so either idiom works in it. **Your fixed `:36` must stay ONE physical line** — the probe copies one line.

NEW FILE: `--- /dev/null` then `+++ b/systemTest/akto/tests/unit/setup/ks1337-preSuiteSetupPathWithASpace.test.ts`, ONE hunk header `@@ -0,0 +1,79 @@` (79 `+` lines; a blank line is a lone `+`). Copy every line byte for byte.

```
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

**Every test `+` line is ASCII only and carries NO backslash, NO backtick, NO double-quote and NO `$`** (counted: 0 of each). The newline and single quote the probe needs are `String.fromCharCode(10)` / `(39)` ON PURPOSE. Do not "improve" that; do not rename a cell.

## Cells and controls

- `control KS-1337 akto: preSuiteSetup.ts has one step statement and it names fixtures/pre-suite.ts` — green before and after (the probe copies a real, single line).
- `control KS-1337 akto: from a checkout path WITHOUT spaces the step is the real pre-suite file` — green before and after (the probe resolves correctly when nothing needs encoding).
- `RED KS-1337 akto: from a checkout path WITH spaces the step is the real pre-suite file, not a percent-encoded one` — RED at the tip on its `toBe` assertion (`Received: …/Testing%20Agent%20MAIN/…`), GREEN after the fix.

## Red cells

- RED KS-1337 akto: from a checkout path WITH spaces

## The failing case (the "tamper")

On the FIXED tree, put `:37` (the fixed statement's line after Edit 1) back to the tip's `:36` text `    const step = new URL('../../fixtures/pre-suite.ts', import.meta.url).pathname;`. The fixed line occurs exactly ONCE in the fixed file (counted: 1). Expected: the RED cell goes red on assertion, both controls stay green. **Measured** (below).

## Premises (each one measured, with where)

- `:12`, `:35-:37` quoted above were read with `git show 3f70224a069b:systemTest/akto/tests/preSuiteSetup.ts` in a `--no-local` scratch clone with develop fetched; `:11` and `:13` are empty; non-ASCII is on `:3,:7,:19,:23,:30,:44` only (none in either hunk).
- `node:url` / `fileURLToPath` occur 0 times in the file; `.pathname` once (`:36`).
- Sweep at `3f70224a069b`, `git grep 'import.meta.url).pathname'` over the whole repo: 5 lines — `systemTest/akto/tests/preSuiteSetup.ts:36` (this brief), `systemTest/playwright/global-setup.ts:42` (KS-1337's third site, NOT briefable here: that package's runner is Playwright/`node --test`, which the checker cannot run), and the 3 KS-1347 lines under `Blockchain/Dev`. `systemTest/performance/runner/cli.ts` is already fixed.
- **RED at the tip, EXECUTED** (vitest v4.1.11, the package's own node_modules farmed from the Secuura checkout, unit config): `Tests 1 failed | 2 passed (3)`, the RED failing on `toBe` (`Expected …/Testing Agent MAIN/systemTest/fixtures/pre-suite.ts`, `Received …/Testing%20Agent%20MAIN/…`).
- **GREEN after the reference fix, EXECUTED**: the reference diff (Edit 1 `@@ -12,1 +12,2 @@` trailing-context insertion, Edit 2 `@@ -35,3 +36,3 @@`, plus this test) applied with `git apply` (strict, no `--recount`) rc 0 → `Tests 3 passed (3)`; whole akto unit suite on the fixed tree `70 files / 1236 tests passed`; `tsc -p tsconfig.json --noEmit` rc 0; `eslint --max-warnings 0` on both files rc 0; `prettier --check` on both files OK.
- **Tamper EXECUTED**: fixed line → `.pathname` again (count 1) → exactly the RED cell red, 2 green.

## UNMEASURED — stated rather than glossed

1. **An alternative fix also turns the cell green**: `decodeURIComponent(new URL(...).pathname)` was measured GREEN (arm run on the fixed tree). The cell tests BEHAVIOUR, not the idiom; the ticket and this brief ask for `fileURLToPath`. The checker cannot tell the two apart — Wednesday's line-by-line source read must (a PASS whose `:36` is not `fileURLToPath(new URL(...))` is a brief-compliance FAIL even when green).
2. `patch -p1 -F0` (macOS patch 2.0-12u11) REFUSES Edit 1's trailing-only-context insertion (`Hunk #1 failed at 12`: BSD patch anchors an asymmetric-context hunk to the file start); `git apply` strict accepts it. The checker's A2 is `git apply`. Measured, not a model issue — do not score a `patch -F0` refusal of hunk 1 against the model.
3. The ticket's Done-means 2 ("run the CLI from a spaced copy of the tree and see the step spawn") is approximated, as #1291's was: the cell runs the file's own statement from a real spaced location through a real ESM import; no `npx tsx` spawn, no akto stack.
4. The builder was run against the scratch clone (`NIGHT_SOURCE_CHECKOUT`), not the real checkout; the checker (`spark_checker.sh`) was NOT run on the golden.

## Collision

KS-1337 is **In Progress** (its first site merged as #1291, PR merged, no open PR). No seat holds the akto site (the ticket names it open; no branch or PR touches `systemTest/akto/tests/preSuiteSetup.ts` — `git log` at develop: last change `3af1d37b9`, 2026-09-11). This site has had **0 model rounds**; `started_ok` is required for the builder. The playwright site stays open.

## Scope

**Closes 2 of KS-1337's 3 sites (with #1291); refs KS-1337, does NOT close it** — `systemTest/playwright/global-setup.ts:42` remains.

## Output

Exactly ONE ```diff block with TWO files: first `--- a/systemTest/akto/tests/preSuiteSetup.ts` / `+++ b/systemTest/akto/tests/preSuiteSetup.ts` (two hunks, in file order, headers computed by you as above), then `--- /dev/null` / `+++ b/systemTest/akto/tests/unit/setup/ks1337-preSuiteSetupPathWithASpace.test.ts` (one hunk `@@ -0,0 +1,79 @@`, every line a `+`). Every `+` line on its own physical line. Every context line keeps its single leading space. Paths are repo-rooted (they start `systemTest/`). No prose before or after the block.
