# READY — KS-1131-KS-1131 (Ornith, briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-25_ks1131-ornith35b-night3/out.md.checker/patch.diff`** (from `ls` at 10:01 2026-09-25; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-25_ks1131-ornith35b-night3/out.md.checker/section_1.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip — with an accommodation: [Blockchain/Dev/services/auth/src/__tests__/ks963-preauth-rethrow.test.ts: --recount --ignore-whitespace needed; miscounted hunks=2; strict rc=128]` — STRICT APPLY NOT CLAIMED: section 1 (Blockchain/Dev/services/auth/src/__tests__/ks963-preauth-rethrow.test.ts): `error: patch fragment without header at line 12: @@ -262,4 +262,31 @@ describe('KS-963 widened — a DB failure no longer burns a single-use token', ()` (apply with the options recorded in section_<k>.opts; the raise seat states which); golden not located — no identity claim is made.

**Held 10:01 2026-09-25 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-25_ks1131-ornith35b-night3/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `6ab9d5021e96ea1481cb6c6ff2d6d33b414aecb7`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (self-testing) touched-file set == { Blockchain/Dev/services/auth/src/__tests__/ks963-preauth-rethrow.test.ts } — one file that is both the product and its test (under Blockchain/Dev/services/auth/src/__tests__)`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/auth/src/__tests__/ks963-preauth-rethrow.test.ts` (product) and `Blockchain/Dev/services/auth/src/__tests__/ks963-preauth-rethrow.test.ts` (test) — equal to numstat.out's set (1 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
28	1	Blockchain/Dev/services/auth/src/__tests__/ks963-preauth-rethrow.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (28 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 28 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 1.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/auth/src/__tests__/ks963-preauth-rethrow.test.ts byte-exact incl. leading whitespace (apply mode lenient): OK 28 line(s) byte-exact incl. leading whitespace (of 28; 28 line(s) added by the apply)` [a3i_indent.out: `OK 28 line(s) byte-exact incl. leading whitespace (of 28; 28 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `section 1 Blockchain/Dev/services/auth/src/__tests__/ks963-preauth-rethrow.test.ts: hunk 1 (@@ -216,5 +216,5 @@ function assertConsumeIsGuarded(src: string, consumeFn: string, lookupFrom: numbe) declared old=5 new=5 but actual old=7 new=7`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/auth/src/__tests__/ks963-preauth-rethrow.test.ts` (hunks=2, miscount=2; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `--recount --ignore-whitespace`; `apply_check_strict_1.out`: NON-EMPTY: `error: patch fragment without header at line 12: @@ -262,4 +262,31 @@ describe('KS-963 widened — a DB failure no longer burns a single-use token', ()`)
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks963-preauth-rethrow.test.ts fails at the untouched tip (1 failed / 15 run; controls green; assertion reds)` [red_first.json: failed=1 of total=15; red cell(s): ['KS-963 widened — a DB failure no longer burns a single-use token KS-1131 F-A a comment naming the consume in the gap is NOT a hoisted consume']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks963-preauth-rethrow.test.ts passes with the product hunk (15 passed / 15 run)` [green_after.json: failed=0 of total=15, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=828 failed=0 | after: total=830 failed=0` · `NEW reds: []` [baseline_suite.json total=828 failed=0; after_suite.json total=830 failed=0]
- A6 [verbatim]: `PASS A6 whole services/auth suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/auth: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=1 +28/-1 test=src/__tests__/ks963-preauth-rethrow.test.ts red_first=yes apply_mode=lenient`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/auth/src/__tests__/ks963-preauth-rethrow.test.ts` (+28/-1 per numstat.out) — ONE file: it is both the product and its test (self-testing mode; red-first is by HUNK, not by file). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1 --recount --ignore-whitespace` — at the tip `6ab9d5021e96ea1481cb6c6ff2d6d33b414aecb7` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-25_ks1131-ornith35b-night3/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-25_ks1131-ornith35b-night3/checker.out`.

```diff
--- a/Blockchain/Dev/services/auth/src/__tests__/ks963-preauth-rethrow.test.ts
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks963-preauth-rethrow.test.ts
@@ -216,5 +216,5 @@ function assertConsumeIsGuarded(src: string, consumeFn: string, lookupFrom: numbe
   expect(expiryGuard).toBeLessThan(lookup);
   const expiryBody = braceBlock(src, expiryGuard);
   expect(count(expiryBody, consumeFn)).toBe(1);
-  expect(count(src.slice(expiryGuard, lookup), consumeFn)).toBe(1);
+  expect(count(src.slice(expiryGuard, lookup), consumeFn + '(')).toBe(1);
 }
 
 describe('KS-963 widened — a DB failure no longer burns a single-use token', () => {
@@ -262,4 +262,31 @@ describe('KS-963 widened — a DB failure no longer burns a single-use token', ()
     // rather than to its name.
     expect(body.slice(0, lookup)).toContain('SELECT * FROM auth_find_user_by_wallet');
   });
+  // KS-1131 F-A: a MENTION of the consume in the gap before the lookup is not a hoisted call.
+  const NL = String.fromCharCode(10);
+  const resetHandler = (gap: string) =>
+    [
+      'router.post(PATH, async (req, res) => {',
+      '  const stored = await userRepo.getResetToken(tokenHash);',
+      '  if (new Date() > stored.expiresAt) {',
+      '    await userRepo.consumeResetToken(tokenHash);',
+      '    return res.status(400).json({ error: 1 });',
+      '  }',
+      gap,
+      '  const user = await userRepo.getUserByIdPreAuth(stored.userId);',
+      '  if (!user) {',
+      '    await userRepo.consumeResetToken(tokenHash);',
+      '    return res.status(404).json({ error: 2 });',
+      '  }',
+      '  await userRepo.consumeResetToken(tokenHash);',
+      '});',
+    ].join(NL);
+  it('KS-1131 F-A a comment naming the consume in the gap is NOT a hoisted consume', () => {
+    const src = resetHandler('  // NOTE: consumeResetToken runs in the two branches around this line');
+    expect(() => assertConsumeIsGuarded(src, 'consumeResetToken', 0)).not.toThrow();
+  });
+  it('KS-1131 CONTROL a real consume hoisted into the gap still reds property 2', () => {
+    const src = resetHandler('  await userRepo.consumeResetToken(tokenHash);');
+    expect(() => assertConsumeIsGuarded(src, 'consumeResetToken', 0)).toThrow();
+  });
 });
 
 /**
```
