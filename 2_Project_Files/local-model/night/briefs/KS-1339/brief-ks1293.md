# KS-1339 CONFIGPINNEDNAMES — RUNG 4 (strict): ks1293's CONFIGPINNED cell asserts its offender list BEFORE its count floor, so a failure names the file

File: `Blockchain/Dev/services/originate/src/__tests__/ks1293-originate-suite-is-hermetic.test.ts`  (the PRODUCT of this brief — a suite file, modified in place)
Test file: `Blockchain/Dev/services/originate/src/__tests__/ks1339-configpinned-names-the-offender-before-the-count.test.ts`  (NEW)
Tip: `3f70224a069b944334480478ad5d16a5ed33eeae`
Runner: `jest` (`Blockchain/Dev/services/originate/package.json` `"test": "jest"`, `jest.config.js` preset ts-jest, node env, globals)

Written 2026-09-26 22:18:02 AEST (shell `date`) by a Spark brief-writer sub-agent for Wednesday, from develop `3f70224a069b`, read in a `--no-local` scratch clone. `ks1293-originate-suite-is-hermetic.test.ts` read WHOLE (303 lines, blob `6689b56555f0`, last changed `e55860c4a` KS-1293 #1261, 2026-09-26).

**RUNG 4 (strict).** This brief tells you WHAT is wrong, WHERE (file and line numbers) and the fix shape in PROSE, and names already-merged examples BY PATH AND LINE. It gives you NO product `+` line and NO product hunk header: you compose them. The file's CURRENT lines are in your input's files; copy every `-` line and every context line from there, byte for byte. The TEST is spelled out in full below (copy it byte for byte), so this round measures only the product hunk.

**Count every hunk's lines exactly** (tonight's round-1 lesson, KS-1347): the old-side start is the real line number of the hunk's FIRST line in the file as given; the old-side count is exactly the number of context + `-` lines you write; the new-side count is exactly the number of context + `+` lines you write. Count the lines you actually emit, not the lines you meant to include.

## The mode — read this twice

CODE+TEST, TWO files. File 1 is the product `Blockchain/Dev/services/originate/src/__tests__/ks1293-originate-suite-is-hermetic.test.ts`, MODIFIED IN PLACE (`--- a/…` / `+++ b/…` with that exact path). It is a suite file, but here it is the thing being fixed. File 2 is the NEW test in `## The test` (`--- /dev/null` / `+++ b/…`). There is no third file. You never touch any SUBJECT file (`ks1213-…`, `ks1228-…`, `ks1264-…`, `ks444-…`, `ks445-…`, `ks520-…`, `ks543-…`), `ks1061-shared-mock-completeness.test.ts`, `jest.config.js`, or the reference test `ks780-org-id-is-the-shared-implementation.test.ts`.

## What is wrong (one paragraph)

ks1293's CONFIGPINNED cell (`:160`-`:165`) scans the nine SUBJECT files (`:161`) and then asserts two things in this order: the count floor `:163` (every subject yields at least one base, so `pinned >= 9`) and THEN the offender list `:164` (must be empty). When a subject stops pinning its base (its env line deleted, nested, or the file renamed), the scan BOTH drops `pinned` to 8 AND records an offender string that names the file. Jest stops at the first failing `expect`, so the floor fires first and the failure prints only `Expected: >= 9 / Received: 8` — it never says WHICH file. The file's own header (`:52`) promises the opposite: "A subject that stops pinning the base is an offender NAMED BY FILE". The ticket (KS-1339, from the KS-1293 gate) measured that 6 of 9 offending subjects are never named at runtime. The verdict is right (red on every real revert); the diagnosis is not.

## The exact change (RUNG 4 — prose only; you write the product hunk and its header)

**The pattern to follow is already merged in THIS file, and it is in your input's files:** the MANIFEST-DRIFT cell's assertion at `:178` and the RS CONTROL cell's assertion at `:221` each put the offender list INTO the thing the failure prints, so a failure there always names what went wrong. Apply the same principle to CONFIGPINNED by ORDER: the offender list must be asserted FIRST, so its failure message (the array of offender strings, each naming a file) is the one Jest prints; the count floor stays, as the SECOND assertion.

**Edit 1 — the only edit: MOVE ONE LINE, one hunk.** Move the offender-list assertion at `:164` so that it sits directly AFTER the scan line `:161` and BEFORE the `// Non-vacuity` comment `:162`. Its text does not change at all (same four-space indent, same statement, same semicolon). The comment `:162` and the count floor `:163` stay exactly as they are, still together, still in that order — the comment belongs to the floor. In the diff this is ONE hunk carrying the moved statement TWICE: once as a `+` line after `:161`, and once as a `-` line AT `:164`. Use exactly these context lines: `:161` before the `+` line; `:162` and `:163` between the `+` line and the `-` line; `:165` (the cell's closing `  });`) after the `-` line. Do NOT use `:166` as context: it is an EMPTY line. Do NOT express the move the other way round (removing `:162`-`:163` and re-adding them below `:164`): `:164` is the line that must appear as a `-` line.

**Header arithmetic is yours.** This is a move inside one hunk, so the hunk's old count and new count are equal; the file's length does not change. Old count = context lines + `-` lines; new count = context lines + `+` lines; the old-side start is the number of the hunk's first line.

**Do NOT touch:** the scan line `:161`, the `// Non-vacuity` comment `:162` or the count floor `:163` (their text; they only shift down by the move); the cell title `:160`; the `describe` line `:159`; every other cell (MANIFEST-DRIFT `:167`-, RS1/RS2/RS3a, RS CONTROL, RS3a MECHANISM, NODNS), including the non-ASCII `🔴` title at `:206`; the docblock (`:1`-`:25`, `:42`-`:56`); `SUBJECTS`, `importScopeBases`, `scanHermeticity`, `BAD_PORTS`. Add NO comment lines and NO new assertion; delete nothing but the moved line's old position.

## Where (line-keyed — every **must change** line must appear as a '-' line AT ITS NUMBER)

* `:164` — **must change** `    expect(offenders).toEqual([]);`
* `:161` — (correct) `    const { offenders, pinned } = scanHermeticity(TESTS_DIR, SUBJECTS);` — stays (context)
* `:162` — (correct) `    // Non-vacuity: the manifest is 9 files and each must yield at least one base.` — stays (context)
* `:163` — (correct) `    expect(pinned).toBeGreaterThanOrEqual(SUBJECTS.length);` — stays (context)
* `:165` — (correct) `  });` — stays (context)

## THIS IS JEST (service `services/originate`, ts-jest)

`describe`/`it`/`expect` are jest GLOBALS here (no import; the product file uses them the same way). The new test uses `__dirname` to find ks1293 (CommonJS under ts-jest; merged precedent: the reference `ks780-org-id-is-the-shared-implementation.test.ts:35`).

## The test

File: `Blockchain/Dev/services/originate/src/__tests__/ks1339-configpinned-names-the-offender-before-the-count.test.ts`

The shape copied is the reference `ks780-org-id-is-the-shared-implementation.test.ts` I2 (`:34`-`:42`): read a source file as TEXT through `readFileSync(join(__dirname, …))` and assert on it. ks1293 is itself a suite (importing it would register its cells inside this file), so this test reads it as TEXT, takes the CONFIGPINNED statements that follow its scan line up to the cell's `  });`, compiles them with `new Function` taking `expect, offenders, pinned, SUBJECTS`, runs them against a chosen scan result, and returns the FIRST failure's message. It never names the key the MANIFEST-DRIFT cell looks for, so it does not become an undeclared subject.

NEW FILE: `--- /dev/null` then `+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1339-configpinned-names-the-offender-before-the-count.test.ts`, ONE hunk `@@ -0,0 +1,64 @@` (64 `+` lines; a blank line is a lone `+`). Copy every line byte for byte. (This is the TEST's header; no product header is given anywhere in this brief.)

```
+/**
+ * KS-1339: ks1293's CONFIGPINNED cell asserts its count floor BEFORE its offender list. When a
+ * SUBJECT stops pinning the base, the scan both drops the pinned count by one and records an
+ * offender that names the file, but the floor fires first, so the failure prints only a count
+ * comparison and never names the file. The file's own header claims the opposite: an offender is
+ * NAMED BY FILE. ks1293 is itself a suite, so it cannot be imported here. This test reads it as
+ * TEXT, takes the statements of the CONFIGPINNED cell that follow its scan, runs them against a
+ * scan result, and checks which failure comes FIRST.
+ */
+
+import { readFileSync } from 'fs';
+import { join } from 'path';
+
+// A newline and a single quote, so no line below needs a backslash or a double-quoted string.
+const NL = String.fromCharCode(10);
+const SQ = String.fromCharCode(39);
+const LINES = readFileSync(join(__dirname, 'ks1293-originate-suite-is-hermetic.test.ts'), 'utf-8').split(NL);
+const START = LINES.findIndex((line) => line.trim().startsWith('it(' + SQ + 'CONFIGPINNED:'));
+const END = LINES.findIndex((line, i) => i > START && line === '  });');
+const SCAN_AT = LINES.findIndex((line, i) => i > START && i < END && line.includes('scanHermeticity(TESTS_DIR, SUBJECTS)'));
+// The CONFIGPINNED statements after its scan, in the order the file writes them.
+const ASSERTIONS = LINES.slice(SCAN_AT + 1, END).join(NL);
+
+const SUBJECTS = Array.from({ length: 9 }, (_, i) => 'subject-' + String(i) + '.test.ts');
+const OFFENDER = 'ks1228-a-refused-request-writes-no-provenance-row.test.ts sets no IMPORT-SCOPE base';
+
+/**
+ * Run the CONFIGPINNED assertions on one scan result.
+ *
+ * @param {string[]} offenders - The scan's offender list.
+ * @param {number} pinned - The scan's pinned-base count.
+ * @returns {string} The FIRST failure's message, or an empty string when every assertion holds.
+ */
+function firstFailure(offenders: string[], pinned: number): string {
+  const cell = new Function('expect', 'offenders', 'pinned', 'SUBJECTS', ASSERTIONS) as (...args: unknown[]) => void;
+  try {
+    cell(expect, offenders, pinned, SUBJECTS);
+    return '';
+  } catch (err) {
+    return err instanceof Error ? err.message : String(err);
+  }
+}
+
+describe('KS-1339 ks1293 CONFIGPINNED: a failure names the offending file, not only a count', () => {
+  it('control KS-1339 A0: the CONFIGPINNED cell asserts both the offender list and the count floor after its scan', () => {
+    expect(START).toBeGreaterThan(-1);
+    expect(SCAN_AT).toBeGreaterThan(START);
+    expect(END).toBeGreaterThan(SCAN_AT);
+    expect(ASSERTIONS).toContain('expect(offenders).toEqual([]);');
+    expect(ASSERTIONS).toContain('expect(pinned).toBeGreaterThanOrEqual(SUBJECTS.length);');
+  });
+
+  it('control KS-1339 A1: a clean scan with every subject pinned passes', () => {
+    expect(firstFailure([], 9)).toBe('');
+  });
+
+  it('control KS-1339 A2: a scan one base short with no offender still fails, so the floor is kept', () => {
+    expect(firstFailure([], 8)).not.toBe('');
+  });
+
+  it('RED KS-1339 A3: a scan with one offender and one base short fails FIRST on the offender list, naming the file', () => {
+    expect(firstFailure([OFFENDER], 8)).toContain('ks1228-a-refused-request-writes-no-provenance-row.test.ts');
+  });
+});
```

**Every test `+` line is ASCII only and carries NO backslash, NO backtick, NO double-quote and NO `$`** (counted: 0 of each). The newline and single quote are `String.fromCharCode(10)` / `(39)` ON PURPOSE. Do not "improve" that; do not rename a cell.

## Red cells

- RED KS-1339 A3

## Cells and controls

- `control KS-1339 A0: the CONFIGPINNED cell asserts both the offender list and the count floor after its scan` — green before and after (pins that the fix MOVES the offender assertion and keeps the floor; a "fix" that deletes either reds here).
- `control KS-1339 A1: a clean scan with every subject pinned passes` — green before and after.
- `control KS-1339 A2: a scan one base short with no offender still fails, so the floor is kept` — green before and after.
- `RED KS-1339 A3: a scan with one offender and one base short fails FIRST on the offender list, naming the file` — RED at the tip on its `toContain` assertion (received `expect(received).toBeGreaterThanOrEqual(expected) … Expected: >= 9 Received: 8`), GREEN after the fix.

## The failing case (the "tamper")

On the FIXED tree, move the offender assertion (now `:162`) back to below the count floor (`:164`). Expected: exactly `RED KS-1339 A3` red; A0, A1, A2 green; ks1293's own 10 cells green. **Measured** (below).

## Premises (each one measured, with where)

- `:159`-`:166` read with `git show 3f70224a069b:<path>`: `:161` the scan, `:162` the comment, `:163` the floor, `:164` the offender assertion, `:165` `  });`, `:166` EMPTY. `expect(offenders).toEqual([]);` occurs ONCE in the file (literal count 1), `expect(pinned).toBeGreaterThanOrEqual(SUBJECTS.length);` once. Non-ASCII lines in the file: `:2,:5,:8,:12,:16,:29,:42,:49,:70,:75,:120,:125,:138,:142,:181,:190,:206,:247,:267,:298` — NONE from `:159` to `:166`.
- `:178` (MANIFEST-DRIFT) and `:221` (RS CONTROL) are the merged cells whose failures print the list (read at the tip). No merged cell anywhere in the repo asserts an offender list directly before a count floor (searched every tracked `*.test.ts`: 0), so the in-file cells are the nearest merged precedent — stated rather than dressed up.
- **Golden applies strictly:** `git apply --check` rc 0 and `patch -p1 -F0 --dry-run` rc 0 against a `git archive` of `3f70224a` (one leading and one trailing context line, no blank context line). The golden result is byte-identical (`cmp`) to the hand-edited tree the tests ran on.
- **RED at tip, EXECUTED** (`npx jest` on the new test + ks1293, the package's own config, node_modules symlink-farmed from the Secuura checkout): `Tests: 1 failed, 13 passed, 14 total` — `RED KS-1339 A3` fails on `toContain`, received the floor's message; A0/A1/A2 and all 10 ks1293 cells green (the new file does not trip MANIFEST-DRIFT).
- **GREEN after the golden, EXECUTED:** the same two files `14 passed (14)`; whole originate suite tip `82 suites / 962 tests passed` → fixed `83 / 966 passed`, 0 failures.
- **Lint + types, EXECUTED:** `eslint --max-warnings 0` on the new test AND ks1293 rc 0; `npm run lint` rc 0 (0 errors, 22 pre-existing warnings); `tsc -p tsconfig.json --noEmit` rc 0 (the service tsconfig EXCLUDES `src/__tests__`, so the new test was also type-checked alone, `--strict --types jest,node`: rc 0).
- **Tamper EXECUTED:** fixed tree, offender line moved back below the floor → exactly `RED KS-1339 A3` red, 13 green.
- **Arms EXECUTED:** (1) a wrong fix that deletes the floor instead → A0 and A2 red. (2) A REAL subject revert (ks1228's import-scope env line removed): on the FIXED tree CONFIGPINNED now fails with the offender-array diff; on the TIP ordering it fails `Expected: >= 9 / Received: 8` (the ticket's defect, reproduced on real files).

## UNMEASURED — stated rather than glossed

1. **For a move, the `+` text equals the `-` text.** The `-` line must be quoted in `## Where` (the checker's A3b needs it), so this rung-4 round measures hunk COMPOSITION and HEADER ARITHMETIC for a move-inside-one-hunk (a `+` and a `-` of the same statement separated by context), not derivation of a new expression. That is the honest size of this rung-4.
2. The new test executes ks1293's CONFIGPINNED statements through `new Function`, not through ks1293's own `it`; it proves the ORDER of the file's real statements against a chosen scan result. Arm 2 covers the real-file path once, by hand.
3. node_modules come from the real Secuura checkout by symlink farm (the scratch clone's `services/originate/node_modules` farmed the same way as KS-1346's), not an install at `3f70224a`.
4. The builder was run against the scratch clone (`NIGHT_SOURCE_CHECKOUT`); `spark_checker.sh` was NOT run on the golden.

## Collision

KS-1339 is **Backlog**, unassigned-to-Peter/Stuart (kamil.kreiser@secuura.ai), no attachment, **0 rows in night/done.md** (`grep -c '^KS-1339'` → 0; control `^KS-1227` → 3) and no brief dir before this one. Open PRs read from the GitHub API (24 open): none touches `ks1293-originate-suite-is-hermetic.test.ts` or `ks780-…` (originate files in open PRs: `index.ts`, `utils/gatewayProvenance.ts`, `ks741-emitter-marker-strip.test.ts`, `package.json` only). Not in tonight's in-flight set (webhooks.ts, adminConfig.ts, systemErrors.ts, gdpr.ts, ks1341a/b/c, ks730a/b/c, akto preSuiteSetup.ts, ks732). Not an auth/credential product surface: a test-infrastructure guard in originate's suite.

## Scope

**Closes KS-1339** (its one-line fix shape: offender list before the count floor; the floor stays as the secondary assertion).

## Output

Exactly ONE fenced diff block with TWO files: first `--- a/Blockchain/Dev/services/originate/src/__tests__/ks1293-originate-suite-is-hermetic.test.ts` / `+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1293-originate-suite-is-hermetic.test.ts` (ONE hunk, header computed by you), then `--- /dev/null` / `+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1339-configpinned-names-the-offender-before-the-count.test.ts` (one hunk `@@ -0,0 +1,64 @@`, every line a `+`). Every `+` line on its own physical line. Every context line keeps its single leading space. Paths exactly as the File: / Test file: lines give them. No prose before or after the block.
