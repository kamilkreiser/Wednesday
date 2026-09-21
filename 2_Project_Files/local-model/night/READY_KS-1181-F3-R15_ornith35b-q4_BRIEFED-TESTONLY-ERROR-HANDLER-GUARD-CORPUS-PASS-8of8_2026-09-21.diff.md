# READY — KS-1181-F3-R15 (Ornith, briefed, test_only, new · vitest) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1181-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 21:43 2026-09-21). Checker T3 (verbatim from checker.out): `PASS T3 diff applies at the tip — with an accommodation: --recount (miscounted header: hunk @@ -0,0 +1,74 @@ declared old=0 new=74 actual old=0 new=75 ); every line byte-exact`; golden not located — no byte-identity claim is made.

**Held 21:43 2026-09-21 by Wednesday (the 20:1x seat) after a source read (hold_ready.py — every clause below is built from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1181-ornith35b-night/out.md.checker`, not typed).** Tip `9f0265eb06ecf24d4de18149ce862ad2330a61ee`. Touches ONE file: `Blockchain/Dev/packages/shared/src/__tests__/ks1181-ks-727-error-handler-guard-corpus.test.ts` (new). `+` lines 75 ordered-equal to the brief's `expected_plus` (ASCII); `-` lines 0 == `must_remove`. Green at the tip: 3/3 cells. Tampers (1), each red exactly its declared set with controls green and the product file restored by bytes (T6/T7/T8):
- `F3` → red exactly ['RED KS-1181 F3 - every count in the guard header equals the ']

**PR NOTES for the raise seat:** TEST-ONLY — zero product bytes; one file, apply `patch.diff` strictly at the tip (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` and state it). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1181-ornith35b-night/input.json`. Brief: `night/briefs/KS-1181-F3-R15.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1181-ornith35b-night/checker.out`.

```diff
--- /dev/null
+++ b/Blockchain/Dev/packages/shared/src/__tests__/ks1181-ks-727-error-handler-guard-corpus.test.ts
@@ -0,0 +1,74 @@
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
+describe('KS-1181 F3 - the KS-727 guard header counts are asserted against its exact sets', () => {
+  it('GREEN KS-1181 control - each header count phrase and each exact-set declaration occurs once in the guard', () => {
+    expect(matchCount(GUARD_SOURCE, CORPUS_ONE_COUNTS), 'corpus 1 count phrase').toBe(1);
+    expect(matchCount(GUARD_SOURCE, FILTER_COUNTS), 'filter count phrase').toBe(1);
+    expect(matchCount(GUARD_SOURCE, CORPUS_TWO_COUNTS), 'corpus 2 count phrase').toBe(1);
+    for (const opening of [CORPUS_OPENING, HANDLERS_OPENING, FORWARDING_OPENING, INLINE_OPENING]) {
+      expect(GUARD_SOURCE.split(opening).length, opening).toBe(2);
+    }
+  });
+
+  it('GREEN KS-1181 control - the readers see a wrong count in a known fixture', () => {
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
+  it('RED KS-1181 F3 - every count in the guard header equals the exact set the guard asserts', () => {
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
