# READY — KS-974-974SCOPETRIM-R16B (Ornith, briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks974-ornith35b-night2/out.md.checker/patch.diff`** (from `ls` at 12:18 2026-09-22; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks974-ornith35b-night2/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks974-ornith35b-night2/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip — with an accommodation: [Blockchain/Dev/services/security/src/requestSchemas.ts: --recount --ignore-whitespace needed; miscounted hunks=1; strict rc=128]` — STRICT APPLY NOT CLAIMED: section 1 (Blockchain/Dev/services/security/src/requestSchemas.ts): `error: corrupt patch at line 10` (apply with the options recorded in section_<k>.opts; the raise seat states which); CONTENT-compared against the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_feed10-drafter-precheck/SCOPETRIM/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1); file headers DIFFER (run ['+++ b/Blockchain/Dev/services/security/src/requestSchemas.ts', '+++ b/Blockchain/Dev/services/security/src/__tests__/ks974-published-bound-vs-runtime-bound-on.test.ts'] vs golden ['+++ b/Blockchain/Dev/services/security/src/requestSchemas.ts', '+++ b/Blockchain/Dev/services/security/src/__tests__/ks974-scope-field-bounds-the-trimmed-value.test.ts']); APPLIED RESULT not compared (input.json['files'] lacks a touched file's tip content).

**Held 12:18 2026-09-22 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks974-ornith35b-night2/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `8c2f7b3fd4fde915b2a24542bc32259b24e092a0`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/security/src/requestSchemas.ts , Blockchain/Dev/services/security/src/__tests__/ks974-published-bound-vs-runtime-bound-on.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/security/src/requestSchemas.ts` (product) and `Blockchain/Dev/services/security/src/__tests__/ks974-published-bound-vs-runtime-bound-on.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
1	0	Blockchain/Dev/services/security/src/requestSchemas.ts
30	0	Blockchain/Dev/services/security/src/__tests__/ks974-published-bound-vs-runtime-bound-on.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (1 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 1 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 0.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/security/src/requestSchemas.ts byte-exact incl. leading whitespace (apply mode lenient): OK 1 line(s) byte-exact incl. leading whitespace (of 1; 1 line(s) added by the apply)` [a3i_indent.out: `OK 1 line(s) byte-exact incl. leading whitespace (of 1; 1 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `section 1 Blockchain/Dev/services/security/src/requestSchemas.ts: hunk 1 (@@ -60,6 +60,7 @@ const scopeField = () =>) declared old=6 new=7 but actual old=5 new=6`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/security/src/requestSchemas.ts` (hunks=1, miscount=1; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `--recount --ignore-whitespace`; `apply_check_strict_1.out`: NON-EMPTY: `error: corrupt patch at line 10`)
- section 2 `section_2.diff` → `Blockchain/Dev/services/security/src/__tests__/ks974-published-bound-vs-runtime-bound-on.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks974-published-bound-vs-runtime-bound-on.test.ts fails at the untouched tip (2 failed / 3 run; controls green; assertion reds)` [red_first.json: failed=2 of total=3; red cell(s): ['KS-974 Part B: published bound vs runtime bound on the rate-limit scope fields RED KS-974 B: a tenantId inside the bound after trimming is accepted, and the parsed value is the trimmed one', 'KS-974 Part B: published bound vs runtime bound on the rate-limit scope fields RED KS-974 B: the same for userId, with trailing whitespace']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks974-published-bound-vs-runtime-bound-on.test.ts passes with the product hunk (3 passed / 3 run)` [green_after.json: failed=0 of total=3, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=220 failed=0 | after: total=223 failed=0` · `NEW reds: []` [baseline_suite.json total=220 failed=0; after_suite.json total=223 failed=0]
- A6 [verbatim]: `PASS A6 whole services/security suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/security: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +31/-0 test=src/__tests__/ks974-published-bound-vs-runtime-bound-on.test.ts red_first=yes apply_mode=lenient`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/security/src/requestSchemas.ts` (+1/-0 per numstat.out) and the test file `Blockchain/Dev/services/security/src/__tests__/ks974-published-bound-vs-runtime-bound-on.test.ts` (+30/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1 --recount --ignore-whitespace`; section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `8c2f7b3fd4fde915b2a24542bc32259b24e092a0` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks974-ornith35b-night2/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks974-ornith35b-night2/checker.out`.

```diff
--- a/Blockchain/Dev/services/security/src/requestSchemas.ts
+++ b/Blockchain/Dev/services/security/src/requestSchemas.ts
@@ -60,6 +60,7 @@ const scopeField = () =>
   z
     .string()
+    .trim() // KS-974 item 2: bound and encode the value the runtime USES (rateLimitScope.ts trims)
     .min(1)
     .refine((value) => !hasLoneSurrogate(value), {
       message: 'must not contain an unpaired surrogate',
--- /dev/null
+++ b/Blockchain/Dev/services/security/src/__tests__/ks974-published-bound-vs-runtime-bound-on.test.ts
@@ -0,0 +1,30 @@
+// KS-974 Part B: the published maxLength is measured on the TRIMMED scope value, like the runtime.
+
+import { describe, it, expect } from 'vitest';
+import { resetRateLimitSchema } from '../requestSchemas';
+
+const KEY = 'login:1.2.3.4';
+
+describe('KS-974 Part B: published bound vs runtime bound on the rate-limit scope fields', () => {
+  it('RED KS-974 B: a tenantId inside the bound after trimming is accepted, and the parsed value is the trimmed one', () => {
+    const r = resetRateLimitSchema.safeParse({ key: KEY, tenantId: ' ' + 'a'.repeat(256) });
+    expect(r.success).toBe(true);
+    if (r.success) {
+      expect(r.data.tenantId).toBe('a'.repeat(256));
+    }
+  });
+
+  it('RED KS-974 B: the same for userId, with trailing whitespace', () => {
+    const r = resetRateLimitSchema.safeParse({ key: KEY, userId: 'u'.repeat(256) + '  ' });
+    expect(r.success).toBe(true);
+    if (r.success) {
+      expect(r.data.userId).toBe('u'.repeat(256));
+    }
+  });
+
+  it('control: 257 non-blank characters still refused, a blank scope field still refused, key alone accepted', () => {
+    expect(resetRateLimitSchema.safeParse({ key: KEY, tenantId: 'a'.repeat(257) }).success).toBe(false);
+    expect(resetRateLimitSchema.safeParse({ key: KEY, tenantId: '   ' }).success).toBe(false);
+    expect(resetRateLimitSchema.safeParse({ key: KEY }).success).toBe(true);
+  });
+});
```
