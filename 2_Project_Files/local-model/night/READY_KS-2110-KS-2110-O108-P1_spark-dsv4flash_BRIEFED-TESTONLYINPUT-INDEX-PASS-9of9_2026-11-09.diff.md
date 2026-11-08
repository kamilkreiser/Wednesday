# READY - KS-2110-KS-2110-O108-P1 (Spark (DeepSeek V4 Flash), briefed, test_only_input) - PASS 9/9 - HELD for QA

> CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2110_o108_p1_requireplatformrole_undefined_role_row_and_per_route_pin/out.md.checker/patch.diff` (from `ls` at 04:24 2026-11-09; sha256[:16] ecdb68e3b3c65447, 1263 B; byte-equal to the out.md fence). Checker A2 (verbatim): `PASS A2 the diff applies at the tip (strict)`; golden comparison [round.json, verbatim]: TREE-IDENTICAL.

**Held 04:24 2026-11-09 by Wednesday after a source read (hold_ready.py, test_only_input path; STRICT-APPLY leg passed first). Every clause below is copied from the run's artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2110_o108_p1_requireplatformrole_undefined_role_row_and_per_route_pin/out.md.checker`; product bytes were RE-MEASURED here.** Tip `2935f723109756a60cadc5521977c7a036ec322d`. Brief: not given (--brief)
- Touched set [patch.diff `+++` headers == input.json test_files, no product or plant file named]: ['Blockchain/Dev/packages/shared/src/__tests__/ks1536-one-role-vocabulary.test.ts']; `+` lines 7 (ASCII), `-` lines 0.
- Product bytes UNCHANGED [re-measured: tip index blobs before and after a strict `git apply --cached -p1` of patch.diff]: `Blockchain/Dev/packages/shared/src/middleware/index.ts` blob ccde0ce9ebf2; plant file(s) also unchanged.
- Red cells [input.json]:
  - `M4 a user with no role is ForbiddenError`
  - `G5b tokenisation puts requirePlatformRole on each key route itself`
- Red-first evidence [checker.out, verbatim]: A4 green without plant, A5 red under the plant by assertion.
- Checker legs [checker.out, verbatim]:
  - `PASS A1 output is exactly one fenced ```diff block, nothing outside it`
  - `PASS A2 the diff applies at the tip (strict)`
  - `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=2 ok=2 bad=0 skipped_newfile=0)`
  - `PASS A3 touched set == the brief's declared set (Blockchain/Dev/packages/shared/src/__tests__/ks1536-one-role-vocabulary.test.ts)`
  - `PASS A3p the plant applies at the tip (golden_red.diff)`
  - `PASS A4 GREEN WITHOUT PLANT: 2 red cell(s) exist and pass on the unmodified product; declared files 99 cells, 0 red`
  - `PASS A6 WHOLE SUITE no worse: cells 1592 -> 1594, red 1 -> 1`
  - `PASS A5 RED WITH PLANT: 2 red cell(s) fail by assertion under the plant (Blockchain/Dev/packages/shared/src/middleware/index.ts, Blockchain/Dev/services/tokenisation/src/index.ts), pass without it`
  - `PASS A7 RESTORE: 3 watched file(s) back at their tip sha256; tracked tree clean`
- RESULT [checker.out]: `RESULT: PASS (tier test_only_input)`

**PR NOTES for the raise seat:** TEST_ONLY_INPUT - test bytes only, zero product bytes. Apply `patch.diff` strictly (`git apply -p1`; proven by the hold's STRICT-APPLY leg). The red proof is the brief's plant (checker clone only), not a change in the PR. No `tsc` leg covers a vitest file; DOES NOT PROVE the plant is the regression that matters or that a cell catches a different one. Wednesday read the cells against the brief before this hold.

```diff
--- a/Blockchain/Dev/packages/shared/src/__tests__/ks1536-one-role-vocabulary.test.ts
+++ b/Blockchain/Dev/packages/shared/src/__tests__/ks1536-one-role-vocabulary.test.ts
@@ -82,6 +82,7 @@
     expect(await run({ role })).toBe('ForbiddenError');
   });
   it('RED ks1536 M3 no user is UnauthorizedError', async () => { expect(await run(undefined)).toBe('UnauthorizedError'); });
+  it('RED ks1536 M4 a user with no role is ForbiddenError', async () => { expect(await run({})).toBe('ForbiddenError'); });
 });
 
 // ---- the guard
@@ -172,6 +173,12 @@
     expect(t).not.toContain('PLATFORM_ADMIN_ROLES');
   });
 
+  it('RED ks1536 G5b tokenisation puts requirePlatformRole on each key route itself, not only twice somewhere', () => {
+    const t = readFileSync(join(DEV, 'services/tokenisation/src/index.ts'), 'utf8');
+    expect(t).toContain("app.post('/api/generate-key', requirePlatformRole(),");
+    expect(t).toContain("app.post('/api/rotate-key', requirePlatformRole(),");
+  });
+
   it('RED ks1536 G6 originate adminConfig resolves tenants by the shared predicate and keeps no list of its own', () => {
     const t = readFileSync(join(DEV, 'services/originate/src/routes/adminConfig.ts'), 'utf8');
     expect(t).not.toContain('SUPER_ADMIN_ROLES');
```
