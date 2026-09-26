# KS-1347 KS732SPACEDPATH — RUNG 4 (strict): ks732's three spec/handler reads take their path through the file-URL decoder, not URL.pathname

File: `Blockchain/Dev/services/auth/src/__tests__/ks732-mfa-disable-proof.test.ts`  (the PRODUCT of this brief — a suite file, modified in place)
Test file: `Blockchain/Dev/services/auth/src/__tests__/ks1347-ks732-spec-paths-survive-a-spaced-checkout.test.ts`  (NEW)
Tip: `3f70224a069b944334480478ad5d16a5ed33eeae`
Runner: `vitest` (`Blockchain/Dev/services/auth/package.json` `"test": "vitest"`, `vitest.config.ts`, globals on, node env)

Written 2026-09-26 21:40:21 AEST (shell `date`) by a Spark brief-writer sub-agent for Wednesday, from develop `3f70224a069b`, read in a `--no-local` scratch clone. `ks732-mfa-disable-proof.test.ts` read WHOLE (326 lines, blob `cd56340e6e73`, last changed `a45204ac9` KS-732 #872, 2026-09-11).

**RUNG 4 (strict).** This brief tells you WHAT is wrong, WHERE (file and line numbers), the behaviour required and the fix shape in PROSE, and names an already-merged example BY PATH. It gives you NO product `+` line, NO product hunk header and NO written-out form of the fixed expression: you compose them. The file's CURRENT lines are in your input's files; copy every `-` line and every context line from there, byte for byte. The TEST is spelled out in full below (copy it byte for byte), so this round measures only the product hunks.

## The mode — read this twice

CODE+TEST, TWO files. File 1 is the product `Blockchain/Dev/services/auth/src/__tests__/ks732-mfa-disable-proof.test.ts`, MODIFIED IN PLACE (`--- a/…` / `+++ b/…` with that exact path). It is a suite file, but here it is the thing being fixed. File 2 is the NEW test in `## The test` (`--- /dev/null` / `+++ b/…`). There is no third file. You never touch `routes/mfa.ts`, `auth.openapi.ts`, `vitest.config.ts`, any other `__tests__` file, or the reference test `ks847-no-raw-control-bytes.test.ts`.

## What is wrong (one paragraph)

ks732's CELL 12 (`:285`) and CELL 13 (`:311`) read two source files as text: each does `await readFile(` on one line, a path argument on the next line, then `);`. The path argument, at `:293`, `:296` and `:316`, is taken from a `new URL(<relative path>, import.meta.url)` by reading its `.pathname` property. A URL pathname is PERCENT-ENCODED: in a checkout whose directory holds a space (the QA gate's own `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/`) the path carries `%20`, `readFile` fails ENOENT, and both cells die before they assert anything. This is KS-1347's second site (the ticket names 4 lines in 2 files; this brief takes the 3 lines in this file; `scripts/openapi-examples/proxy/server.ts:31` is the fourth, and has no runner the checker can drive). Fixed already in the same class: KS-1337's `systemTest/performance/runner/cli.ts` (#1291). `node:url` is not imported in this file today (0 occurrences of `node:url` and of `fileURLToPath`).

## The exact change (RUNG 4 — prose only; you write every product `+` line and every product header)

**The pattern to follow is already merged in this service, and it is in your input's files:** the reference test `Blockchain/Dev/services/auth/src/__tests__/ks847-no-raw-control-bytes.test.ts`. Read its node:url import and its `SRC_ROOT` statement, and the docblock above that statement, which says why a file URL must be decoded rather than read through `.pathname`. Apply the same idiom here.

**Edit 1 — add ONE import line (a pure insertion).** Add a single-line named import of `fileURLToPath` from the built-in module `node:url`, in this file's import style (single quotes, braces with one space inside, semicolon — the same form as `:45`). Put it on its own line BETWEEN `:47` (the `node:net` import) and `:48` (the `express` import), so it sits after the other `node:` imports. Use exactly TWO context lines: `:47` BEFORE your `+` line and `:48` AFTER it. Do NOT use `:49` as context: it is an EMPTY line.

**Edit 2 — CELL 12's two path arguments, `:293` and `:296` (each ONE line out, ONE line in).** In each, keep the six-space indent, the SAME relative path string, the same `import.meta.url` base, and the trailing `, 'utf8',`. Change ONLY how the filesystem path is taken from the URL: pass the `new URL(...)` object itself to the function you imported in Edit 1, instead of reading `.pathname` off it. Each stays ONE physical line, still ending `'utf8',`. Put both in ONE hunk: context `:292` before, `:294`-`:295` between them, `:297` after.

**Edit 3 — CELL 13's path argument, `:316`,** exactly as Edit 2. Its text at the tip is byte-identical to `:293`; the LINE NUMBER is what identifies it. Context `:315` before, `:317` after.

**Header arithmetic is yours.** Edit 1 adds one line above `:48`, so every hunk after it starts one line further down on the NEW side than on the OLD side. Each hunk's old count = its context lines + its `-` lines; new count = its context lines + its `+` lines.

**Do NOT touch:** the `await readFile(` opener lines (`:292`, `:295`, `:315`) and the `);` closers (`:294`, `:297`, `:317`) — the new test finds each path argument as the line after an opener, so the three-line statement shape must stay; every other line, including the `🔴` cell titles (`:285`, `:311`, non-ASCII) and the docblock (`:1`-`:42`); the existing imports `:44`-`:48` (add one line, change none). Add NO comment lines.

## Where (line-keyed — every **must change** line must appear as a '-' line AT ITS NUMBER)

* `:293` — **must change** `      new URL('../auth.openapi.ts', import.meta.url).pathname, 'utf8',`
* `:296` — **must change** `      new URL('../routes/mfa.ts', import.meta.url).pathname, 'utf8',`
* `:316` — **must change** `      new URL('../auth.openapi.ts', import.meta.url).pathname, 'utf8',`
* `:47` — (correct) `import type { AddressInfo } from 'node:net';` — stays (context)
* `:48` — (correct) `import express from 'express';` — stays (context)

## THIS IS VITEST (service `services/auth`)

The new test imports `describe/it/expect/beforeEach/afterEach` from `'vitest'`. NO `vi.mock` is needed. It uses `__dirname` to find ks732 (vitest provides it; merged precedent: `ks622-retired-route-contract.test.ts:50`).

## The test

File: `Blockchain/Dev/services/auth/src/__tests__/ks1347-ks732-spec-paths-survive-a-spaced-checkout.test.ts`

The shape copied is #1291's merged cell `systemTest/performance/tests/unit/runner/ks1337-preSuitePathWithASpace.test.ts`: ks732 is itself a suite, so it cannot be imported. This test reads ks732 as TEXT, takes each line that follows an `await readFile(` opener (the path argument), strips the `, 'utf8',` tail, plants those three expressions in a `probe.mjs` at `<checkout>/services/auth/src/__tests__/` inside a temp dir (next to planted `auth.openapi.ts` and `routes/mfa.ts`), imports the probe for real (so `import.meta.url` is a real, space-containing location), and checks each path is the planted file and exists. The probe imports `node:url` both ways, so the expression works whichever import form it names.

NEW FILE: `--- /dev/null` then `+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1347-ks732-spec-paths-survive-a-spaced-checkout.test.ts`, ONE hunk `@@ -0,0 +1,84 @@` (84 `+` lines; a blank line is a lone `+`). Copy every line byte for byte. (This is the TEST's header; no product header is given anywhere in this brief.)

```
+/**
+ * KS-1347 (ks732 site): ks732-mfa-disable-proof.test.ts reads auth.openapi.ts and routes/mfa.ts
+ * through a path taken off a file URL. A URL pathname is percent-encoded, so a checkout whose
+ * directory holds a space (the QA gate's own Testing Agent MAIN) hands readFile a path carrying
+ * %20 and CELL 12 and CELL 13 die ENOENT before they assert anything. ks732 is itself a suite, so
+ * this one reads it as TEXT, takes each path expression it hands to readFile, plants it in a probe
+ * module inside a temp checkout, imports the probe for real, and checks the path it yields is the
+ * planted file. Same shape as the merged KS-1337 performance cell (#1291).
+ */
+
+import { existsSync, mkdirSync, mkdtempSync, readFileSync, realpathSync, rmSync, writeFileSync } from 'node:fs';
+import { tmpdir } from 'node:os';
+import { join } from 'node:path';
+import { pathToFileURL } from 'node:url';
+
+import { afterEach, beforeEach, describe, expect, it } from 'vitest';
+
+// A newline and a single quote, so no line below needs a backslash or a double-quoted string.
+const NL = String.fromCharCode(10);
+const SQ = String.fromCharCode(39);
+const UTF8_TAIL = ', ' + SQ + 'utf8' + SQ + ',';
+const KS732_LINES = readFileSync(join(__dirname, 'ks732-mfa-disable-proof.test.ts'), 'utf8').split(NL);
+// Every line of ks732 that follows an await readFile( opener is the path argument, then the utf8 tail.
+const PATH_LINES = KS732_LINES.filter((line, i) => i > 0 && KS732_LINES[i - 1].trim().endsWith('await readFile(')).map((line) => line.trim());
+const EXPRESSIONS = PATH_LINES.map((line) => line.slice(0, line.length - UTF8_TAIL.length));
+const TARGETS = ['auth.openapi.ts', 'routes/mfa.ts', 'auth.openapi.ts'];
+
+let root = '';
+
+beforeEach(() => {
+  root = realpathSync(mkdtempSync(join(tmpdir(), 'ks1347-ks732-')));
+});
+afterEach(() => {
+  rmSync(root, { recursive: true, force: true });
+});
+
+/**
+ * Plant checkoutName/services/auth/src/{auth.openapi.ts, routes/mfa.ts, __tests__/probe.mjs}; import the probe.
+ *
+ * @param {string} checkoutName - The checkout directory's name; may contain spaces.
+ * @returns {Promise<{ resolved: string[]; planted: string[] }>} The paths the expressions yield, and the real files.
+ */
+async function pathsFrom(checkoutName: string): Promise<{ resolved: string[]; planted: string[] }> {
+  const src = join(root, checkoutName, 'services', 'auth', 'src');
+  mkdirSync(join(src, 'routes'), { recursive: true });
+  mkdirSync(join(src, '__tests__'), { recursive: true });
+  writeFileSync(join(src, 'auth.openapi.ts'), 'export {};');
+  writeFileSync(join(src, 'routes', 'mfa.ts'), 'export {};');
+  const probe = join(src, '__tests__', 'probe.mjs');
+  writeFileSync(
+    probe,
+    [
+      'import * as url from ' + SQ + 'node:url' + SQ + ';',
+      'import { fileURLToPath } from ' + SQ + 'node:url' + SQ + ';',
+      'export const paths = [' + EXPRESSIONS.join(', ') + '];',
+      'export { url, fileURLToPath };',
+    ].join(NL),
+  );
+  const mod = (await import(pathToFileURL(probe).href)) as { paths: string[] };
+  return { resolved: mod.paths, planted: TARGETS.map((t) => join(src, ...t.split('/'))) };
+}
+
+describe('KS-1347 ks732: the spec and handler paths survive a checkout directory with spaces', () => {
+  it('control KS-1347 A0: ks732 hands readFile three import.meta.url paths, naming the spec, the handler, the spec', () => {
+    expect(PATH_LINES).toHaveLength(3);
+    for (const [i, line] of PATH_LINES.entries()) {
+      expect(line.endsWith(UTF8_TAIL)).toBe(true);
+      expect(line).toContain('import.meta.url');
+      expect(line).toContain(SQ + '../' + TARGETS[i] + SQ);
+    }
+  });
+
+  it('control KS-1347 A1: from a checkout path WITHOUT spaces every path is the real planted file', async () => {
+    const { resolved, planted } = await pathsFrom('TestingAgentMAIN');
+    expect(resolved).toEqual(planted);
+    expect(resolved.map((p) => existsSync(p))).toEqual([true, true, true]);
+  });
+
+  it('RED KS-1347 A2: from a checkout path WITH spaces every path is the real planted file, not a percent-encoded one', async () => {
+    const { resolved, planted } = await pathsFrom('Testing Agent MAIN');
+    expect(resolved).toEqual(planted);
+    expect(resolved.map((p) => existsSync(p))).toEqual([true, true, true]);
+  });
+});
```

**Every test `+` line is ASCII only and carries NO backslash, NO backtick, NO double-quote and NO `$`** (counted: 0 of each). The newline and single quote are `String.fromCharCode(10)` / `(39)` ON PURPOSE. Do not "improve" that; do not rename a cell. The test never names the fixed idiom as a path source: it finds ks732 through `__dirname`.

## Red cells

- RED KS-1347 A2

## Cells and controls

- `control KS-1347 A0: ks732 hands readFile three import.meta.url paths, naming the spec, the handler, the spec` — green before and after (it pins the three-line statement shape the probe relies on, and that each line still ends `, 'utf8',`).
- `control KS-1347 A1: from a checkout path WITHOUT spaces every path is the real planted file` — green before and after (nothing needs encoding).
- `RED KS-1347 A2: from a checkout path WITH spaces every path is the real planted file, not a percent-encoded one` — RED at the tip on its `toEqual` assertion (received paths carry `Testing%20Agent%20MAIN`), GREEN after the fix.

## The failing case (the "tamper")

On the FIXED tree, put `:317` (CELL 13's path argument, one line lower after Edit 1) back to the tip's `:316` text `      new URL('../auth.openapi.ts', import.meta.url).pathname, 'utf8',`. Expected: A2 red on its third element only, A0 and A1 green. **Measured** (below).

## Premises (each one measured, with where)

- `:47`, `:48`, `:292`-`:297`, `:315`-`:317` were read with `git show 3f70224a069b:<path>`; `:293` and `:316` are byte-identical (literal count 2), `:296` once; `.pathname` off an `import.meta.url` URL occurs exactly 3 times in the file; `:49` is empty; non-ASCII is on `:3,:8,:19,:30,:39,:86,:183-:311` cell titles/comments, and on NO line from `:44` to `:48` and NO line from `:292` to `:297` or `:315` to `:317` (`:311`, CELL 13's title, is 4 lines above Edit 3 and outside a one-line context).
- `ks847-no-raw-control-bytes.test.ts` (the reference; merged, 150 lines) imports the decoder at `:41` and uses it at `:60`, with the why at `:44`-`:59`.
- **Golden applies strictly:** `git apply --check` rc 0 and `patch -p1 -F0 --dry-run` rc 0 at `3f70224a` (Edit 1 carries one leading and one trailing context line ON PURPOSE: a trailing-only insertion is refused by macOS `patch -F0`, measured on this file's first draft).
- **RED at tip, EXECUTED** (vitest, the package's own config, node_modules symlink-farmed from the Secuura checkout): ks732 alone `13 passed`; the new test alone `Tests 1 failed | 2 passed (3)` — `RED KS-1347 A2` fails on `toEqual`, received `…/Testing%20Agent%20MAIN/services/auth/src/auth.openapi.ts` (and the other two), both controls green.
- **GREEN after the golden, EXECUTED:** `git apply` strict rc 0 → ks1347 + ks732 `16 passed (16)`; whole auth suite tip `76 files / 832 tests passed` → fixed `77 / 835 passed`, 0 failures.
- **Lint, EXECUTED:** `npm run lint` (`eslint src`) rc 0 (0 errors; warnings only); `eslint --max-warnings 0` on the new test rc 0; on ks732 ONE warning, `disableBlock` unused, which is at `:318` AT THE TIP (pre-existing, not on a changed line); `tsc -p tsconfig.json --noEmit` rc 0 (the service's tsconfig excludes `src/__tests__`).
- **Tamper EXECUTED:** fixed `:317` → the tip's `.pathname` line → exactly `RED KS-1347 A2` red (third element only), A0 + A1 green.
- **Arm EXECUTED:** a string percent-decode of the pathname at all three sites → `3 passed` (see UNMEASURED 1; the arm is in `golden/ks1347_verify.sh`, not here).

## UNMEASURED — stated rather than glossed

1. **An alternative fix also turns A2 green**: percent-decoding the pathname STRING instead of using the node:url decoder (measured GREEN, arm below; the arm's text is kept out of this brief on purpose, so it cannot prime you). The cell tests BEHAVIOUR, not the idiom; the ticket and this brief ask for the node:url decoder, as ks847 does. The checker cannot tell the two apart — Wednesday's line-by-line read of `:294`, `:297`, `:317` must (a PASS without the imported decoder is a brief-compliance FAIL even when green).
2. ks732's own cells are not re-proved from a SPACED checkout end to end (no real clone under a spaced path was run); the probe runs the file's own expressions from a real spaced location through a real ESM import.
3. node_modules come from the real Secuura checkout by symlink farm (`prepare_clone.sh` for the root and shared; `services/auth/node_modules` farmed the same way by hand, because the builder source is the scratch clone), not an install at `3f70224a`.
4. The builder was run against the scratch clone (`NIGHT_SOURCE_CHECKOUT`); `spark_checker.sh` was NOT run on the golden.

## Collision

KS-1347 is **Backlog**, Medium, unassigned, no attachment, **0 rows in night/done.md** (counted `grep -c '^KS-1347'` → 0) and no brief dir before this one. Open PRs read from the GitHub API (24 open): none touches `ks732-mfa-disable-proof.test.ts` or `ks847-no-raw-control-bytes.test.ts`. `git ls-remote` shows one branch naming ks-732 (`seat-b/ks-732-mfa-disable-proof`), the pre-squash head of merged #872. Not in tonight's in-flight set (webhooks.ts, ks1341a/b/c, adminConfig.ts, ks730c, akto preSuiteSetup.ts).

**Surface note (stated, not hidden):** the file lives under `services/auth`, but the change is test-infrastructure path resolution inside a SUITE: no auth product code (`routes/mfa.ts`, `auth.openapi.ts`, any middleware) is read differently or touched, and no mock or assertion of ks732 changes.

## Scope

**Closes 3 of KS-1347's 4 lines (1 of its 2 files); refs KS-1347, does NOT close it** — `scripts/openapi-examples/proxy/server.ts:31` remains (that package has no test script), and the ticket's ks860/ks879 walk decision is untouched.

## Output

Exactly ONE fenced diff block with TWO files: first `--- a/Blockchain/Dev/services/auth/src/__tests__/ks732-mfa-disable-proof.test.ts` / `+++ b/Blockchain/Dev/services/auth/src/__tests__/ks732-mfa-disable-proof.test.ts` (THREE hunks in file order — Edit 1, Edit 2, Edit 3 — headers computed by you), then `--- /dev/null` / `+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1347-ks732-spec-paths-survive-a-spaced-checkout.test.ts` (one hunk `@@ -0,0 +1,84 @@`, every line a `+`). Every `+` line on its own physical line. Every context line keeps its single leading space. Paths exactly as the File: / Test file: lines give them. No prose before or after the block.
