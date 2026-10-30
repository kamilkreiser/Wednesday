# READY — KS-1534-KS-1534-P1 (Spark (DeepSeek V4 Flash), briefed, test_only (code_patch checker, MODE=test_only), vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1534_p1_guard_same_code/out.md.checker/patch.diff`** (from `ls` at 12:16 2026-10-30; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1534_p1_guard_same_code/out.md.checker/section_1.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1534_p1_guard_same_code/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1534_p1_guard_same_code-control/out.md.checker/patch.diff` rc 0, Spark operator 20).

**Held 12:16 2026-10-30 by Spark operator 20 after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1534_p1_guard_same_code/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `530f091120d5da749edf972e8e0089e44cfc5589`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (test-only) touched-file set == { Blockchain/Dev/services/api-gateway/src/__tests__/ks1534-allow-list-guards-are-the-same-executable-code.test.ts } — the product file is untouched, as the ticket requires`
- Declared set [input.json suggested_test_file; product_file = the TAMPER TARGET, not modified]: `Blockchain/Dev/services/api-gateway/src/__tests__/ks1534-allow-list-guards-are-the-same-executable-code.test.ts` (test) — equal to numstat.out's set (1 file); `Blockchain/Dev/services/api-gateway/src/services/health.ts` (product) untouched, measured above.
- numstat [out.md.checker/numstat.out, verbatim]:
```
57	0	Blockchain/Dev/services/api-gateway/src/__tests__/ks1534-allow-list-guards-are-the-same-executable-code.test.ts
```
- Test hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (47 line(s)), and no tip line is re-added as a '+' (A3d)` — test section `+` lines 57 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 0.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/api-gateway/src/__tests__/ks1534-allow-list-guards-are-the-same-executable-code.test.ts byte-exact incl. leading whitespace (apply mode strict): OK 47 line(s) byte-exact incl. leading whitespace (of 47; 58 line(s) added by the apply)` [a3i_indent.out: `OK 47 line(s) byte-exact incl. leading whitespace (of 47; 58 line(s) added by the apply)`]
- **TEST-ONLY (code_patch checker MODE=test_only)** — the product `Blockchain/Dev/services/api-gateway/src/services/health.ts` is the TAMPER TARGET and is BYTE-UNCHANGED: the run's `patch.diff` re-applied strictly (`git apply -p1`, scratch tempdir) to the tip content in input.json['files'] leaves it sha256 `1838f6baa7887ce4` = the tip's; numstat.out does not list it; no section names it. [checker.out mode line, verbatim]: `mode: test_only (tamper at Blockchain/Dev/services/api-gateway/src/services/health.ts:98)` · [tamper.out, verbatim]: `tampered /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/spark_secuura_2026-10-30_ks_1534_p1_guard_same_code_121405/clone/Blockchain/Dev/services/api-gateway/src/services/health.ts:98: '    if (rawAllowedTypes !== undefined && rawAllowedTypes !== null && !Array.isArray(rawAllowedTypes)) {' -> '    if (rawAllowedTypes !== undefined && rawAllowedTypes !== null) {'` · [checker.out, verbatim]: `A4 (test-only): tamper reverted (Blockchain/Dev/services/api-gateway/src/services/health.ts back to the tip)` (tamper_revert.out EMPTY) · the tamper's `from` equals the product's tip line 98. [apply_product.out, verbatim]: `A5 (test-only): no product hunk — the test must be GREEN at the untouched tip`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=1 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/api-gateway/src/__tests__/ks1534-allow-list-guards-are-the-same-executable-code.test.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1534-allow-list-guards-are-the-same-executable-code.test.ts fails at the untouched tip (2 failed / 5 run; controls green; assertion reds)` [red_first.json: failed=2 of total=5; red cell(s): ['KS-1534 (a): the info reader and the create path carry the same allow-list guard RED KS-1534 G1 the info reader (health.ts) has exactly one executable guard and it is the canonical condition', 'KS-1534 (a): the info reader and the create path carry the same allow-list guard RED KS-1534 G2 the two files carry the same guard condition, compared as executable code']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1534-allow-list-guards-are-the-same-executable-code.test.ts passes with the product hunk (5 passed / 5 run)` [green_after.json: failed=0 of total=5, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1321 failed=0 | after: total=1326 failed=0` · `NEW reds: []` [baseline_suite.json total=1321 failed=0; after_suite.json total=1326 failed=0]
- A6 [verbatim]: `PASS A6 whole services/api-gateway suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/api-gateway: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=1 +57/-0 test=src/__tests__/ks1534-allow-list-guards-are-the-same-executable-code.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** TEST-ONLY — ZERO PRODUCT BYTES: one file, the test `Blockchain/Dev/services/api-gateway/src/__tests__/ks1534-allow-list-guards-are-the-same-executable-code.test.ts` (+57/-0 per numstat.out); the product `Blockchain/Dev/services/api-gateway/src/services/health.ts` is the tamper target and is byte-unchanged (sha256 1838f6baa7887ce4, measured). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict) — at the tip `530f091120d5da749edf972e8e0089e44cfc5589` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: the gate decides (test file only). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1534_p1_guard_same_code/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1534_p1_guard_same_code/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1534-allow-list-guards-are-the-same-executable-code.test.ts b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1534-allow-list-guards-are-the-same-executable-code.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1534-allow-list-guards-are-the-same-executable-code.test.ts
@@ -0,0 +1,57 @@
+// KS-1534 (a) (the Sonnet gate on PR 1517, Minor 1): GET /api/connector/info (services/health.ts) refuses a PRESENT allow-list that is
+// not an array with the SAME guard as the create path (routes/verification.ts, KS-1204):
+//     if (X !== undefined && X !== null && !Array.isArray(X)) {
+// The two copies are duplicated, not shared. The behavioural AGREEMENT cell in ks1232-info-reader-refuses-a-non-array-allow-list.test.ts
+// catches a drift in what each route DOES; this file pins the other half the ticket asks for: that the two guards stay the same
+// EXECUTABLE code. It reads both sources as text, drops every comment line first (a guard that survives only in a comment is not a guard,
+// the KS-1319 class), and compares the guard condition with the variable name normalised. Nothing is started.
+import { describe, it, expect } from 'vitest';
+import { readFileSync } from 'fs';
+import { join } from 'path';
+
+const SRC = join(__dirname, '..');
+const HEALTH = readFileSync(join(SRC, 'services', 'health.ts'), 'utf8');
+const VERIFICATION = readFileSync(join(SRC, 'routes', 'verification.ts'), 'utf8');
+
+const GUARD = /^\s*if \((\w+) !== undefined && \1 !== null && !Array\.isArray\(\1\)\) \{\s*$/;
+
+/** The source with every whole-line comment (// ..., /* ..., * ...) removed. */
+function executableLines(src: string): string[] {
+  return src.split('\n').filter((l) => !/^\s*(\/\/|\/\*|\*)/.test(l));
+}
+
+/** Every line that is the allow-list guard, with the variable name replaced by X. */
+function guardLines(src: string): string[] {
+  return executableLines(src)
+    .map((l) => GUARD.exec(l))
+    .filter((m): m is RegExpExecArray => m !== null)
+    .map((m) => m[0].trim().split(m[1]).join('X'));
+}
+
+const CANONICAL = 'if (X !== undefined && X !== null && !Array.isArray(X)) {';
+
+describe('KS-1534 (a): the info reader and the create path carry the same allow-list guard', () => {
+  it('RED KS-1534 G1 the info reader (health.ts) has exactly one executable guard and it is the canonical condition', () => {
+    expect(guardLines(HEALTH)).toEqual([CANONICAL]);
+  });
+
+  it('RED KS-1534 G2 the two files carry the same guard condition, compared as executable code', () => {
+    expect(guardLines(HEALTH)).toEqual(guardLines(VERIFICATION));
+  });
+
+  it('CONTROL KS-1534 G3 the create path (verification.ts) has exactly one executable guard and it is the canonical condition', () => {
+    expect(guardLines(VERIFICATION)).toEqual([CANONICAL]);
+  });
+
+  it('CONTROL KS-1534 G4 a guard that survives only in a comment is not counted', () => {
+    const planted = '    // if (rawAllowedTypes !== undefined && rawAllowedTypes !== null && !Array.isArray(rawAllowedTypes)) {\n    const kept = 1;\n';
+    expect(guardLines(planted)).toEqual([]);
+  });
+
+  it('CONTROL KS-1534 G5 the scan can fail: a guard with the array test dropped is not the canonical condition', () => {
+    const planted = '    if (rawAllowedTypes !== undefined && rawAllowedTypes !== null) {\n';
+    expect(guardLines(planted)).toEqual([]);
+    expect(guardLines(HEALTH + planted)).toEqual(guardLines(HEALTH));
+    expect(guardLines('    if (rawAllowedTypes !== undefined && rawAllowedTypes !== null && !Array.isArray(rawAllowedTypes)) {\n')).toEqual([CANONICAL]);
+  });
+});
```
