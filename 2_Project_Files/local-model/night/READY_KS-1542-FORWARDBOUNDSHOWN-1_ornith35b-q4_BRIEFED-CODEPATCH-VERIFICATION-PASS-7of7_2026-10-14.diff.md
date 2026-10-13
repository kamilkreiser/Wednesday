# READY — KS-1542-FORWARDBOUNDSHOWN-1 (Ornith, briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ✏️ **CORRECTION by Wednesday 07:23 2026-10-14 (tool text below left as written):** the MODEL was **the Spark (DeepSeek V4 Flash via spark/round.sh)**, not Ornith (hold_ready labels every run Ornith; IMPROVEMENTS 2026-10-14). Brief: `local-model/night/briefs/ks_1542_p1/KS-1542.md`. Round 1 of 1, 0 rebriefs; Wednesday diffed the patch body against the golden: identical. Opus QA gate required before merge (api-gateway).

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-14_ks_1542_p1/out.md.checker/patch.diff`** (from `ls` at 07:23 2026-10-14; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-14_ks_1542_p1/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-14_ks_1542_p1/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; CONTENT-compared against the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-14_ks_1542_p1-control-r2/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1); change lines (`+`/`-`, ordered) IDENTICAL in every file; body lines (context included) DIFFER in verification.ts (run 17 vs golden 19 body lines — context, since the change lines are equal) (identical in ks1185-f1-workflow-approve-forward-bound-is-validated.test.ts); hunk headers identical; APPLIED RESULT IDENTICAL: both patches applied strictly (`git apply -p1`, scratch tempdir) to the tip content carried in input.json['files'] yield byte-identical files (ks1185-f1-workflow-approve-forward-bound-is-validated.test.ts/verification.ts, sha256 equal).

**Held 07:23 2026-10-14 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-14_ks_1542_p1/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `3c0a522216258040f32d400ede433e48e683f734`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/api-gateway/src/routes/verification.ts , Blockchain/Dev/services/api-gateway/src/__tests__/ks1185-f1-workflow-approve-forward-bound-is-validated.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/api-gateway/src/routes/verification.ts` (product) and `Blockchain/Dev/services/api-gateway/src/__tests__/ks1185-f1-workflow-approve-forward-bound-is-validated.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
10	1	Blockchain/Dev/services/api-gateway/src/routes/verification.ts
26	0	Blockchain/Dev/services/api-gateway/src/__tests__/ks1185-f1-workflow-approve-forward-bound-is-validated.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (10 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 10 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 1.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/api-gateway/src/routes/verification.ts byte-exact incl. leading whitespace (apply mode strict): OK 10 line(s) byte-exact incl. leading whitespace (of 10; 10 line(s) added by the apply)` [a3i_indent.out: `OK 10 line(s) byte-exact incl. leading whitespace (of 10; 10 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/api-gateway/src/routes/verification.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/api-gateway/src/__tests__/ks1185-f1-workflow-approve-forward-bound-is-validated.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1185-f1-workflow-approve-forward-bound-is-validated.test.ts fails at the untouched tip (6 failed / 25 run; controls green; assertion reds)` [red_first.json: failed=6 of total=25; red cell(s): ['KS-1185 F1 - the approve forward bound override is validated when the routes are built RED KS-1542 - the refused [1] prints as JSON, (got [1]), not as its String() text', 'KS-1185 F1 - the approve forward bound override is validated when the routes are built RED KS-1542 - the refused [] prints as JSON, (got []), not as its String() text', 'KS-1185 F1 - the approve forward bound override is validated when the routes are built RED KS-1542 - the refused {} prints as JSON, (got {}), not as its String() text', 'KS-1185 F1 - the approve forward bound override is validated when the routes are built RED KS-1542 - the refused [1,2] prints as JSON, (got [1,2]), not as its String() text', 'KS-1185 F1 - the approve forward bound override is validated when the routes are built RED KS-1542 - the refused [800] prints as JSON, (got [800]), not as its String() text', 'KS-1185 F1 - the approve forward bound override is validated when the routes are built RED KS-1542 - no refused bound prints the text of an accepted bound (1, 800, 2147483647)']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1185-f1-workflow-approve-forward-bound-is-validated.test.ts passes with the product hunk (25 passed / 25 run)` [green_after.json: failed=0 of total=25, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1146 failed=0 | after: total=1153 failed=0` · `NEW reds: []` [baseline_suite.json total=1146 failed=0; after_suite.json total=1153 failed=0]
- A6 [verbatim]: `PASS A6 whole services/api-gateway suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/api-gateway: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +36/-1 test=src/__tests__/ks1185-f1-workflow-approve-forward-bound-is-validated.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/api-gateway/src/routes/verification.ts` (+10/-1 per numstat.out) and the test file `Blockchain/Dev/services/api-gateway/src/__tests__/ks1185-f1-workflow-approve-forward-bound-is-validated.test.ts` (+26/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `3c0a522216258040f32d400ede433e48e683f734` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-14_ks_1542_p1/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-14_ks_1542_p1/checker.out`.

```diff
--- a/Blockchain/Dev/services/api-gateway/src/routes/verification.ts
+++ b/Blockchain/Dev/services/api-gateway/src/routes/verification.ts
@@ -147,7 +147,16 @@ function resolveOriginateForwardTimeoutMs(value: unknown): number {
   if (value === undefined) return ORIGINATE_FORWARD_TIMEOUT_MS;
   if (Number.isInteger(value) && (value as number) > 0 && (value as number) <= MAX_FORWARD_TIMEOUT_MS) return value as number;
   // String() flattens 1n to "1" and -0 to "0", which read as the valid 1 and the refused 0 (KS-1518): show the type for those two.
-  const shown = typeof value === 'string' ? JSON.stringify(value) : typeof value === 'bigint' ? `${value}n` : Object.is(value, -0) ? '-0' : String(value);
+  // KS-1542: it also flattens [1] to "1" (the valid bound), [] to "" and {} to "[object Object]": an object prints as JSON, or as its
+  // type tag when JSON.stringify throws (a cycle, a BigInt inside).
+  let shown = typeof value === 'string' ? JSON.stringify(value) : typeof value === 'bigint' ? `${value}n` : Object.is(value, -0) ? '-0' : String(value);
+  if (typeof value === 'object' && value !== null) {
+    try {
+      shown = JSON.stringify(value);
+    } catch {
+      shown = Object.prototype.toString.call(value);
+    }
+  }
   throw new Error(
     `originateForwardTimeoutMs must be an integer from 1 to ${MAX_FORWARD_TIMEOUT_MS} milliseconds (got ${shown}); omit it for the ${ORIGINATE_FORWARD_TIMEOUT_MS} ms default`,
   );
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1185-f1-workflow-approve-forward-bound-is-validated.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1185-f1-workflow-approve-forward-bound-is-validated.test.ts
@@ -138,6 +138,32 @@ describe('KS-1185 F1 - the approve forward bound override is validated when the
     expect(collisionsOf([['a', 'x'], ['c', 'y'], ['d', null]])).toEqual([]);
   });
 
+  // KS-1542: String() also flattened an array to its elements and an object to "[object Object]", so a refused [1] printed (got 1), the text
+  // of the VALID bound 1, and [] printed (got ). An object now prints as JSON. No refused bound may print what an accepted bound prints.
+  const ACCEPTED_TEXT = ['1', '800', String(NODE_MAX_TIMER_MS)];
+  const OBJECTS: Array<[string, unknown, string]> = [
+    ['[1]', [1], '[1]'], ['[]', [], '[]'], ['{}', {}, '{}'], ['[1,2]', [1, 2], '[1,2]'], ['[800]', [800], '[800]'],
+  ];
+
+  for (const [label, value, shown] of OBJECTS) {
+    it(`RED KS-1542 - the refused ${label} prints as JSON, (got ${shown}), not as its String() text`, () => {
+      expect(() => build(value)).toThrow(/originateForwardTimeoutMs/);
+      expect(shownIn(value)).toBe(shown);
+    });
+  }
+
+  it('RED KS-1542 - no refused bound prints the text of an accepted bound (1, 800, 2147483647)', () => {
+    const printed = [...DISTINCT.map(([, value]) => value), ...OBJECTS.map(([, value]) => value)].map((value) => shownIn(value));
+    expect(printed.filter((text) => text !== null && ACCEPTED_TEXT.includes(text))).toEqual([]);
+  });
+
+  it('GREEN KS-1542 control - an object JSON cannot print (a cycle) is still refused, and prints its type tag', () => {
+    const cyclic: Record<string, unknown> = {};
+    cyclic.self = cyclic;
+    expect(() => build(cyclic)).toThrow(/originateForwardTimeoutMs/);
+    expect(shownIn(cyclic)).toBe('[object Object]');
+  });
+
   it('GREEN KS-1185 F1 control - no override still builds and means the production default', () => {
     expect(() => build(undefined)).not.toThrow();
   });
```
