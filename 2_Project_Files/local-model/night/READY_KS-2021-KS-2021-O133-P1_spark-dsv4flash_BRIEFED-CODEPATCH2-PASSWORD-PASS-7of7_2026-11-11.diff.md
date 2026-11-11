# READY — KS-2021-KS-2021-O133-P1 (Spark (DeepSeek V4 Flash), briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_2021_o133_p1_auth_hibp_range_match_ignores_the_count/out.md.checker/patch.diff`** (from `ls` at 10:38 2026-11-11; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_2021_o133_p1_auth_hibp_range_match_ignores_the_count/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_2021_o133_p1_auth_hibp_range_match_ignores_the_count/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_2021_o133_p1_auth_hibp_range_match_ignores_the_count/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_2021_o133_p1_auth_hibp_range_match_ignores_the_count-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 10:38 2026-11-11 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_2021_o133_p1_auth_hibp_range_match_ignores_the_count/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `0b55401ad5dcb748f9dc47189f9896209567eb75`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/auth/src/services/password.ts } + { Blockchain/Dev/services/auth/src/__tests__/ks2021-hibp-range-match-needs-a-count-above-zero.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/auth/src/services/password.ts` (product) and `Blockchain/Dev/services/auth/src/__tests__/ks2021-hibp-range-match-needs-a-count-above-zero.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
3	2	Blockchain/Dev/services/auth/src/services/password.ts
65	0	Blockchain/Dev/services/auth/src/__tests__/ks2021-hibp-range-match-needs-a-count-above-zero.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (3 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: password.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/auth/src/services/password.ts`; test(s): `Blockchain/Dev/services/auth/src/__tests__/ks2021-hibp-range-match-needs-a-count-above-zero.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/auth/src/services/password.ts 3 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/auth/src/__tests__/ks2021-hibp-range-match-needs-a-count-above-zero.test.ts 65 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/auth/src/services/password.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/auth/src/__tests__/ks2021-hibp-range-match-needs-a-count-above-zero.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (2 failed / 5 run; controls green; assertion reds)` [red_first.json: failed=2 of total=5; red cell(s): ['KS-2021 the breach check matches a range row only when its count is above 0 RED ks2021 R1 a padding row (count 0) carrying the password suffix does not make it breached', 'KS-2021 the breach check matches a range row only when its count is above 0 RED ks2021 R2 a padding row with count 0 in the middle of real rows does not make it breached']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (5 passed / 5 run)` [green_after.json: failed=0 of total=5, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1839 failed=0 | after: total=1844 failed=0` · `NEW reds: []` [baseline_suite.json total=1839 failed=0; after_suite.json total=1844 failed=0]
- A6 [verbatim]: `PASS A6 whole services/auth suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/auth: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/auth/src/services/password.ts` (+3/-2 per numstat.out) and the test file `Blockchain/Dev/services/auth/src/__tests__/ks2021-hibp-range-match-needs-a-count-above-zero.test.ts` (+65/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/auth/src/services/password.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `0b55401ad5dcb748f9dc47189f9896209567eb75` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_2021_o133_p1_auth_hibp_range_match_ignores_the_count/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_2021_o133_p1_auth_hibp_range_match_ignores_the_count/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/auth/src/services/password.ts b/Blockchain/Dev/services/auth/src/services/password.ts
--- a/Blockchain/Dev/services/auth/src/services/password.ts
+++ b/Blockchain/Dev/services/auth/src/services/password.ts
@@ -175,4 +175,5 @@
     for (const line of body.split('\n')) {
-      const [hashSuffix] = line.trim().split(':');
-      if (hashSuffix === suffix) return true;
+      const [hashSuffix, countText] = line.trim().split(':');
+      // KS-2021: a padding row (request header Add-Padding) carries count 0 and is no breach record; only a count above 0 matches.
+      if (hashSuffix === suffix && Number(countText) > 0) return true;
     }
diff --git a/Blockchain/Dev/services/auth/src/__tests__/ks2021-hibp-range-match-needs-a-count-above-zero.test.ts b/Blockchain/Dev/services/auth/src/__tests__/ks2021-hibp-range-match-needs-a-count-above-zero.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks2021-hibp-range-match-needs-a-count-above-zero.test.ts
@@ -0,0 +1,65 @@
+import { describe, it, expect, beforeAll, beforeEach, afterAll, vi } from 'vitest';
+import { createHash } from 'crypto';
+
+// KS-2021: isPasswordBreached (services/password.ts) compared only the SUFFIX of each line of the Pwned Passwords range body and
+// ignored the count after the colon. The request sends `Add-Padding: true`, and a padding row carries count 0: it is not a breach
+// record, so a padding row that carried the user's own suffix refused a clean password as breached. Only a count above 0 matches now.
+// Harness: the real module; the logger is a stand-in and the global fetch answers a plain body (no network).
+vi.mock('../utils/logger', () => {
+  const noop = () => undefined;
+  const logger = { debug: noop, info: noop, warn: noop, error: noop, log: noop };
+  return { logger, createLogger: () => logger, validateEnv: () => undefined };
+});
+
+const h = vi.hoisted(() => ({ body: '' }));
+const PW = 'ks2021-Unlisted-pass-phrase-9Q';
+const SUFFIX = createHash('sha1').update(PW).digest('hex').toUpperCase().slice(5);
+const FILLER = '0000000000000000000000000000000000A:7';
+
+type Pw = typeof import('../services/password');
+let mod: Pw;
+const realFetch = globalThis.fetch;
+const savedHibp = process.env.HIBP_ENABLED;
+beforeAll(async () => {
+  mod = await import('../services/password');
+});
+afterAll(() => {
+  globalThis.fetch = realFetch;
+  if (savedHibp === undefined) delete process.env.HIBP_ENABLED;
+  else process.env.HIBP_ENABLED = savedHibp;
+});
+beforeEach(() => {
+  delete process.env.HIBP_ENABLED;
+  globalThis.fetch = (async () => new Response(h.body, { status: 200 })) as unknown as typeof fetch;
+});
+
+const answer = (lines: string[]) => {
+  h.body = lines.join('\r\n');
+};
+
+describe('KS-2021 the breach check matches a range row only when its count is above 0', () => {
+  it('RED ks2021 R1 a padding row (count 0) carrying the password suffix does not make it breached', async () => {
+    answer([FILLER, `${SUFFIX}:0`]);
+    expect(await mod.isPasswordBreached(PW)).toBe(false);
+  });
+
+  it('RED ks2021 R2 a padding row with count 0 in the middle of real rows does not make it breached', async () => {
+    answer([FILLER, `${SUFFIX}:0`, '1111111111111111111111111111111111B:3']);
+    expect(await mod.isPasswordBreached(PW)).toBe(false);
+  });
+
+  it('control ks2021 C1 a row carrying the suffix with a count of 3861493 is breached', async () => {
+    answer([FILLER, `${SUFFIX}:3861493`]);
+    expect(await mod.isPasswordBreached(PW)).toBe(true);
+  });
+
+  it('control ks2021 C2 a row carrying the suffix with the smallest real count, 1, is breached', async () => {
+    answer([`${SUFFIX}:1`, FILLER]);
+    expect(await mod.isPasswordBreached(PW)).toBe(true);
+  });
+
+  it('control ks2021 C3 a body without the suffix is not breached', async () => {
+    answer([FILLER, '1111111111111111111111111111111111B:3']);
+    expect(await mod.isPasswordBreached(PW)).toBe(false);
+  });
+});
```
