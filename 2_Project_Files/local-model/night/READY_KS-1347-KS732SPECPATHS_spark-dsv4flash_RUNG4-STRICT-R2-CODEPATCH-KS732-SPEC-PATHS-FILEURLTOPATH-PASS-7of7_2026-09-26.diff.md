# READY — KS-1347 ks732 spec paths (services/auth TEST file only) — Spark (DeepSeek V4 Flash), STRICT RUNG 4, ROUND 2 (the one rebrief) — PASS 7/7 — HELD for QA

**Held 22:07 2026-09-26 by Wednesday BY HAND** (`hold_ready.py` refuses a rung-4 run: no `PASS A3c` — IMPROVEMENTS row). **Source read by Wednesday:** `out.md.checker/patch.diff` == `night/briefs/KS-1347/golden/*.diff` (`cmp` rc 0, sha1 1ebbb8b57709); strict apply. Round 1 wrote the same code and failed only on hunk-header counts; the round-2 brief named that miss without giving code or headers. **The model derived the fix itself** (the brief quoted no product line): `fileURLToPath(new URL(...))` at the three sites + the `node:url` import.

## Checker verdict (verbatim, round 2)
```
PASS A1 output is exactly one fenced ```diff block, nothing outside it
PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)
PASS A3 touched-file set == { Blockchain/Dev/services/auth/src/__tests__/ks732-mfa-disable-proof.test.ts , Blockchain/Dev/services/auth/src/__tests__/ks1347-ks732-spec-paths-survive-a-spaced-checkout.test.ts }
PASS A3b every must_change site the ticket names is changed by the product hunk (3 site(s); 5 line-keyed site(s), must_change and stays, matched by LINE NUMBER + text; the rest by text)
INFO A3i skipped — the input carries no expected '+' lines (a legacy or brief-less input); indentation not measured
PASS A4 RED-FIRST: src/__tests__/ks1347-ks732-spec-paths-survive-a-spaced-checkout.test.ts fails at the untouched tip (1 failed / 3 run; controls green; assertion reds)
PASS A5 GREEN-AFTER: src/__tests__/ks1347-ks732-spec-paths-survive-a-spaced-checkout.test.ts passes with the product hunk (3 passed / 3 run)
INFO control cell present: 2 cell(s) passed BEFORE and 3 AFTER (the harness reaches the code both times)
PASS A6 whole services/auth suite: no NEW red vs the untouched tip
PASS A7 tsc --noEmit for services/auth: rc 0 after the patch (baseline rc=0)
INFO tsc on the test file alone (--types node,vitest/globals): rc=0 (0 lines; not gated — the runner does not type-check and the service tsconfig excludes __tests__)
SUMMARY files=2 +88/-3 test=src/__tests__/ks1347-ks732-spec-paths-survive-a-spaced-checkout.test.ts red_first=yes apply_mode=strict
RESULT: PASS (7/7)
PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=3 ok=3 bad=0 skipped_newfile=1)
SPARK RESULT: PASS (checker rc 0 + A2a anchor OK)
```

## PR NOTES for the raise seat
- TEST FILE ONLY on an auth service (`services/auth/src/__tests__/ks732-mfa-disable-proof.test.ts`) + a NEW test `ks1347-ks732-spec-paths-survive-a-spaced-checkout.test.ts`. No auth PRODUCT code changes. Refs KS-1347 (this ks732 site; the proxy server.ts site stays open — its package has no test runner). Tier 2 (test-only). Run the auth package's own lint; quote only the gate lines your push printed.
- NOTE for the raise: `prepare_clone.sh` does not farm `services/auth/node_modules` when sourced from a scratch clone — the real checkout is fine.

## Canonical patch (== the model's output == golden)
```diff
--- a/Blockchain/Dev/services/auth/src/__tests__/ks732-mfa-disable-proof.test.ts
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks732-mfa-disable-proof.test.ts
@@ -47,2 +47,3 @@
 import type { AddressInfo } from 'node:net';
+import { fileURLToPath } from 'node:url';
 import express from 'express';
@@ -292,6 +293,6 @@
     const specSrc = await readFile(
-      new URL('../auth.openapi.ts', import.meta.url).pathname, 'utf8',
+      fileURLToPath(new URL('../auth.openapi.ts', import.meta.url)), 'utf8',
     );
     const handlerSrc = await readFile(
-      new URL('../routes/mfa.ts', import.meta.url).pathname, 'utf8',
+      fileURLToPath(new URL('../routes/mfa.ts', import.meta.url)), 'utf8',
     );
@@ -315,3 +316,3 @@
     const specSrc = await readFile(
-      new URL('../auth.openapi.ts', import.meta.url).pathname, 'utf8',
+      fileURLToPath(new URL('../auth.openapi.ts', import.meta.url)), 'utf8',
     );
--- /dev/null
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1347-ks732-spec-paths-survive-a-spaced-checkout.test.ts
@@ -0,0 +1,84 @@
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
