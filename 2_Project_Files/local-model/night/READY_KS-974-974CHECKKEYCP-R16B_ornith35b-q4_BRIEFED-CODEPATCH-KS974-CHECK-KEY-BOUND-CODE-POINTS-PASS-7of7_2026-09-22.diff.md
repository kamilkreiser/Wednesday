# READY — KS-974-974CHECKKEYCP-R16B (Ornith, briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks974-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 12:18 2026-09-22; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks974-ornith35b-night/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks974-ornith35b-night/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip — with an accommodation: [services/security/src/index.ts: --recount --ignore-whitespace needed; miscounted hunks=1; strict rc=128]` — STRICT APPLY NOT CLAIMED: section 1 (services/security/src/index.ts): `error: corrupt patch at line 16` (apply with the options recorded in section_<k>.opts; the raise seat states which); CONTENT-compared against the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_feed10-drafter-precheck/CHECKKEYCP/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1); file headers DIFFER (run ['+++ b/services/security/src/index.ts', '+++ b/services/security/src/__tests__/ks974-check-key-bound-code-points.test.ts'] vs golden ['+++ b/Blockchain/Dev/services/security/src/index.ts', '+++ b/Blockchain/Dev/services/security/src/__tests__/ks974-check-key-bound-code-points.test.ts']); APPLIED RESULT not compared (input.json['files'] lacks a touched file's tip content).

**Held 12:18 2026-09-22 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks974-ornith35b-night/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `8c2f7b3fd4fde915b2a24542bc32259b24e092a0`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/security/src/index.ts , Blockchain/Dev/services/security/src/__tests__/ks974-check-key-bound-code-points.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/security/src/index.ts` (product) and `Blockchain/Dev/services/security/src/__tests__/ks974-check-key-bound-code-points.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
6	1	Blockchain/Dev/services/security/src/index.ts
31	0	Blockchain/Dev/services/security/src/__tests__/ks974-check-key-bound-code-points.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (6 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 6 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 1.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/security/src/index.ts byte-exact incl. leading whitespace (apply mode lenient): OK 6 line(s) byte-exact incl. leading whitespace (of 6; 6 line(s) added by the apply)` [a3i_indent.out: `OK 6 line(s) byte-exact incl. leading whitespace (of 6; 6 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `section 1 services/security/src/index.ts: hunk 1 (@@ -597,7 +597,12 @@ export const checkRateLimitSchema = z.object({) declared old=7 new=12 but actual old=6 new=11`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `services/security/src/index.ts` (hunks=1, miscount=1; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `--directory=Blockchain/Dev --recount --ignore-whitespace`; `apply_check_strict_1.out`: NON-EMPTY: `error: corrupt patch at line 16`)
- section 2 `section_2.diff` → `services/security/src/__tests__/ks974-check-key-bound-code-points.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `--directory=Blockchain/Dev`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks974-check-key-bound-code-points.test.ts fails at the untouched tip (2 failed / 3 run; controls green; assertion reds)` [red_first.json: failed=2 of total=3; red cell(s): ['KS-974 Part A: published vs runtime bound on the rate-limit check key RED KS-974 A: 256 astral characters (256 code points, 512 code units) are inside the published bound', 'KS-974 Part A: published vs runtime bound on the rate-limit check key RED KS-974 A: past the bound, the refusal names it in characters, like /reset']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks974-check-key-bound-code-points.test.ts passes with the product hunk (3 passed / 3 run)` [green_after.json: failed=0 of total=3, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=220 failed=0 | after: total=223 failed=0` · `NEW reds: []` [baseline_suite.json total=220 failed=0; after_suite.json total=223 failed=0]
- A6 [verbatim]: `PASS A6 whole services/security suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/security: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +37/-1 test=src/__tests__/ks974-check-key-bound-code-points.test.ts red_first=yes apply_mode=lenient`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/security/src/index.ts` (+6/-1 per numstat.out) and the test file `Blockchain/Dev/services/security/src/__tests__/ks974-check-key-bound-code-points.test.ts` (+31/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1 --directory=Blockchain/Dev --recount --ignore-whitespace`; section 2 `section_2.diff`: `git apply -p1 --directory=Blockchain/Dev` — at the tip `8c2f7b3fd4fde915b2a24542bc32259b24e092a0` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks974-ornith35b-night/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks974-ornith35b-night/checker.out`.

```diff
--- a/services/security/src/index.ts
+++ b/services/security/src/index.ts
@@ -597,7 +597,12 @@ export const checkRateLimitSchema = z.object({
   // KS-952 F10: `min(1)` with no maximum accepted a 100,000-character key and
   // stored it. This bounds one entry; `sweepExpired` bounds the map.
-  key: z.string().min(1).max(RATE_LIMIT_KEY_MAX),
+  // KS-974 item 1: the published maxLength 256 counts CODE POINTS; zod .max() counts UTF-16
+  // code units, so 256 astral characters were refused on the one route anyone can reach.
+  // Same predicate as boundedByCodePoints on /reset (requestSchemas.ts).
+  key: z.string().min(1).refine((value) => [...value].length <= RATE_LIMIT_KEY_MAX, {
+    message: 'must not exceed ' + RATE_LIMIT_KEY_MAX + ' characters',
+  }),
   limit: z.number().int().min(1).default(100),
   // KS-698 fix 1: an UPPER bound. `min` alone let one request poison a key.
   windowMs: z.number().int().min(1000).max(MAX_RATE_LIMIT_WINDOW_MS).default(60000),
--- /dev/null
+++ b/services/security/src/__tests__/ks974-check-key-bound-code-points.test.ts
@@ -0,0 +1,31 @@
+import { describe, it, expect, beforeAll } from 'vitest';
+
+const ASTRAL = String.fromCodePoint(128512);
+
+let checkRateLimitSchema: { safeParse: (v: unknown) => any };
+
+beforeAll(async () => {
+  process.env.SECURITY_DISABLE_BOOT = '1';
+  const mod: any = await import('../index');
+  ({ checkRateLimitSchema } = mod);
+});
+
+describe('KS-974 Part A: published vs runtime bound on the rate-limit check key', () => {
+  it('RED KS-974 A: 256 astral characters (256 code points, 512 code units) are inside the published bound', () => {
+    expect(checkRateLimitSchema.safeParse({ key: ASTRAL.repeat(256) }).success).toBe(true);
+  });
+
+  it('RED KS-974 A: past the bound, the refusal names it in characters, like /reset', () => {
+    const r = checkRateLimitSchema.safeParse({ key: ASTRAL.repeat(257) });
+    expect(r.success).toBe(false);
+    if (!r.success) {
+      expect(r.error.issues[0].message).toBe('must not exceed 256 characters');
+    }
+  });
+
+  it('control: 256 ASCII characters accepted, 257 refused, empty refused', () => {
+    expect(checkRateLimitSchema.safeParse({ key: 'a'.repeat(256) }).success).toBe(true);
+    expect(checkRateLimitSchema.safeParse({ key: 'a'.repeat(257) }).success).toBe(false);
+    expect(checkRateLimitSchema.safeParse({ key: '' }).success).toBe(false);
+  });
+});
```
