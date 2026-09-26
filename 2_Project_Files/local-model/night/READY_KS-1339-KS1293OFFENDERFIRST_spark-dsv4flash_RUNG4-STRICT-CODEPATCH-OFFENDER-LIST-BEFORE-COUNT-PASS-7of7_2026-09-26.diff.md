# READY — KS-1339 ks1293 offender list before the count (originate TEST file) — Spark, STRICT RUNG 4 (a moved line), round 1 — PASS 7/7 — HELD for QA

**Held 22:24 2026-09-26 by Wednesday BY HAND** (hold_ready.py refuses rung-4 runs: no `PASS A3c`). Source read: `patch.diff` == `night/briefs/KS-1339/golden/KS-1339.golden.diff` (`cmp` rc 0, sha1 50e1f31ebf43); strict apply; the move is in the direction the brief asks (:164 above :162). Caveat: a moved line's `+` equals its `-`, so this measured hunk construction, not code derivation.

## Checker verdict (verbatim)
```
PASS A1 output is exactly one fenced ```diff block, nothing outside it
PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)
PASS A3 touched-file set == { Blockchain/Dev/services/originate/src/__tests__/ks1293-originate-suite-is-hermetic.test.ts , Blockchain/Dev/services/originate/src/__tests__/ks1339-configpinned-names-the-offender-before-the-count.test.ts }
PASS A3b every must_change site the ticket names is changed by the product hunk (1 site(s); 5 line-keyed site(s), must_change and stays, matched by LINE NUMBER + text; the rest by text)
INFO A3i skipped — the input carries no expected '+' lines (a legacy or brief-less input); indentation not measured
PASS A4 RED-FIRST: src/__tests__/ks1339-configpinned-names-the-offender-before-the-count.test.ts fails at the untouched tip (1 failed / 4 run; controls green; assertion reds)
PASS A5 GREEN-AFTER: src/__tests__/ks1339-configpinned-names-the-offender-before-the-count.test.ts passes with the product hunk (4 passed / 4 run)
INFO control cell present: 3 cell(s) passed BEFORE and 4 AFTER (the harness reaches the code both times)
PASS A6 whole services/originate suite: no NEW red vs the untouched tip
PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)
INFO tsc on the test file alone (--types node,jest): rc=0 (0 lines; not gated — the runner does not type-check and the service tsconfig excludes __tests__)
SUMMARY files=2 +65/-1 test=src/__tests__/ks1339-configpinned-names-the-offender-before-the-count.test.ts red_first=yes apply_mode=strict
RESULT: PASS (7/7)
PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=1 ok=1 bad=0 skipped_newfile=1)
SPARK RESULT: PASS (checker rc 0 + A2a anchor OK)
```

## PR NOTES
- TEST FILES ONLY (originate): `ks1293-originate-suite-is-hermetic.test.ts` edited in place + NEW `ks1339-configpinned-names-the-offender-before-the-count.test.ts`. Refs KS-1339. Tier 2. Originate lint; quote only the gate lines your push printed.

## Canonical patch (== model == golden)
```diff
--- a/Blockchain/Dev/services/originate/src/__tests__/ks1293-originate-suite-is-hermetic.test.ts
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1293-originate-suite-is-hermetic.test.ts
@@ -161,5 +161,5 @@
     const { offenders, pinned } = scanHermeticity(TESTS_DIR, SUBJECTS);
+    expect(offenders).toEqual([]);
     // Non-vacuity: the manifest is 9 files and each must yield at least one base.
     expect(pinned).toBeGreaterThanOrEqual(SUBJECTS.length);
-    expect(offenders).toEqual([]);
   });
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1339-configpinned-names-the-offender-before-the-count.test.ts
@@ -0,0 +1,64 @@
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
