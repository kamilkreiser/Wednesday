# READY — KS-1181 F3 PARTIAL ("parse the header counts": NEW test ks1181-ks-727-error-handler-guard-corpus.test.ts reads the KS-727 guard's header counts and asserts each equals the exact set the guard asserts) — Ornith ornith:35b (Q4_K_M) PASS 7/7 FIRST SAMPLE (04:46:59). Held by Wednesday at 04:50 AEST. Run /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-17_ks1181-ornith35b-night
# Source read by me (Wednesday): the model's 75 lines IDENTICAL to the brief's test block (python compare; a mutated-copy control unequal); one new file, the 946-line guard untouched; apply STRICT; A4 under the #1006 gate's G7 (:32 → 8 modules / 9 handlers) 1 red by assertion / 3 run, controls green; A6 packages/shared no NEW red.
# NOT GRADED BY THE CHECKER (brief P6): the Of-those / FILTER / inline-site / inline-file / set-growth header tampers and the reword row (a control reds by design) — graded in the writer's pre-measure.
# PR NOTES: "Refs KS-1181 (F3)" — F2 (canary hit witness inside driveThroughRoute) and F3's wording stay open. Test-only → tier 2 (the writer wrote "tier 1"; the raise seat decides). packages/shared __tests__ — partition-clear at 04:19 (0 open PRs touch the guard or a ks1181 file).

```diff
--- /dev/null
+++ b/Blockchain/Dev/packages/shared/src/__tests__/ks1181-ks-727-error-handler-guard-corpus.test.ts
@@ -0,0 +1,75 @@
+// KS-1181 F3 (KS-844 gate): the KS-727 guard header says that if a count in it is wrong, a test is red.
+// Its counts are comments and no cell read them: the gate reverted them to 8/9 and all 851 cells stayed green.
+// This file reads the guard source itself: each header count, and the size of the exact set the guard asserts.
+import { describe, it, expect } from 'vitest';
+import { readFileSync } from 'node:fs';
+import { join } from 'node:path';
+
+const GUARD_SOURCE = readFileSync(join(__dirname, 'ks727-errorhandler-class-guard.test.ts'), 'utf8');
+
+const CORPUS_ONE_COUNTS = /Count today: ([0-9]+) modules contributing ([0-9]+) handlers[.]/g;
+const FILTER_COUNTS = /Of those ([0-9]+), exactly ([0-9]+) is a FILTER/g;
+const CORPUS_TWO_COUNTS = /Count today: ([0-9]+) inline sites, across ([0-9]+) files/g;
+
+const CORPUS_OPENING = 'const EXPECTED_CORPUS = [';
+const HANDLERS_OPENING = 'const EXPECTED_HANDLERS = [';
+const FORWARDING_OPENING = 'const FORWARDING_HANDLERS = new Set([';
+const INLINE_OPENING = 'const EXPECTED_INLINE_SITES: string[] = [';
+
+function matchCount(source: string, pattern: RegExp): number {
+  return [...source.matchAll(pattern)].length;
+}
+
+function headerNumber(source: string, pattern: RegExp, group: number): number {
+  const found = [...source.matchAll(pattern)];
+  return found.length === 1 ? Number(found[0][group]) : Number.NaN;
+}
+
+function setEntries(source: string, opening: string): string[] {
+  const start = source.indexOf(opening);
+  if (start < 0) return ['<no declaration found>'];
+  const end = source.indexOf(']', start + opening.length);
+  const body = source.slice(start + opening.length, end);
+  return (body.match(/'[^']+'/g) ?? []).map((quoted) => quoted.slice(1, -1));
+}
+
+function distinctFiles(sites: string[]): number {
+  return new Set(sites.map((site) => site.replace(/:[0-9]+$/, ''))).size;
+}
+
+describe('KS-1181 F3 — the KS-727 guard header counts are asserted against its exact sets', () => {
+  it('🟢 KS-1181 control — each header count phrase and each exact-set declaration occurs once in the guard', () => {
+    expect(matchCount(GUARD_SOURCE, CORPUS_ONE_COUNTS), 'corpus 1 count phrase').toBe(1);
+    expect(matchCount(GUARD_SOURCE, FILTER_COUNTS), 'filter count phrase').toBe(1);
+    expect(matchCount(GUARD_SOURCE, CORPUS_TWO_COUNTS), 'corpus 2 count phrase').toBe(1);
+    for (const opening of [CORPUS_OPENING, HANDLERS_OPENING, FORWARDING_OPENING, INLINE_OPENING]) {
+      expect(GUARD_SOURCE.split(opening).length, opening).toBe(2);
+    }
+  });
+
+  it('🟢 KS-1181 control — the readers see a wrong count in a known fixture', () => {
+    const fixture = [
+      '//   Count today: 2 modules contributing 3 handlers. Both are exact sets',
+      "const EXPECTED_CORPUS = [ 'a.ts', 'b.ts', 'c.ts', ];",
+      "const EXPECTED_INLINE_SITES: string[] = [ 'services/x/src/index.ts:12', 'services/x/src/index.ts:40' ];",
+    ].join(' ');
+    expect(headerNumber(fixture, CORPUS_ONE_COUNTS, 1)).toBe(2);
+    expect(setEntries(fixture, CORPUS_OPENING)).toEqual(['a.ts', 'b.ts', 'c.ts']);
+    expect(headerNumber(fixture, CORPUS_ONE_COUNTS, 1)).not.toBe(setEntries(fixture, CORPUS_OPENING).length);
+    expect(distinctFiles(setEntries(fixture, INLINE_OPENING))).toBe(1);
+    expect(setEntries(fixture, HANDLERS_OPENING)).toEqual(['<no declaration found>']);
+  });
+
+  it('🔴 KS-1181 F3 — every count in the guard header equals the exact set the guard asserts', () => {
+    const corpus = setEntries(GUARD_SOURCE, CORPUS_OPENING);
+    const handlers = setEntries(GUARD_SOURCE, HANDLERS_OPENING);
+    const forwarding = setEntries(GUARD_SOURCE, FORWARDING_OPENING);
+    const inlineSites = setEntries(GUARD_SOURCE, INLINE_OPENING);
+    expect(headerNumber(GUARD_SOURCE, CORPUS_ONE_COUNTS, 1), 'header modules vs EXPECTED_CORPUS').toBe(corpus.length);
+    expect(headerNumber(GUARD_SOURCE, CORPUS_ONE_COUNTS, 2), 'header handlers vs EXPECTED_HANDLERS').toBe(handlers.length);
+    expect(headerNumber(GUARD_SOURCE, FILTER_COUNTS, 1), 'header Of those N vs EXPECTED_HANDLERS').toBe(handlers.length);
+    expect(headerNumber(GUARD_SOURCE, FILTER_COUNTS, 2), 'header FILTER count vs FORWARDING_HANDLERS').toBe(forwarding.length);
+    expect(headerNumber(GUARD_SOURCE, CORPUS_TWO_COUNTS, 1), 'header inline sites vs EXPECTED_INLINE_SITES').toBe(inlineSites.length);
+    expect(headerNumber(GUARD_SOURCE, CORPUS_TWO_COUNTS, 2), 'header inline files vs EXPECTED_INLINE_SITES').toBe(distinctFiles(inlineSites));
+  });
+});
```
