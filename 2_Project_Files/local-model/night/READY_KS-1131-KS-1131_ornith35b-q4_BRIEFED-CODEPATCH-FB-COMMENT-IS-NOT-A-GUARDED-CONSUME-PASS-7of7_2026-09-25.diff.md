# READY — KS-1131-KS-1131 (Ornith, briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-25_ks1131-ornith35b-night4/out.md.checker/patch.diff`** (from `ls` at 10:13 2026-09-25; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-25_ks1131-ornith35b-night4/out.md.checker/section_1.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip — with an accommodation: [Blockchain/Dev/services/auth/src/__tests__/ks963-preauth-rethrow.test.ts: --recount --ignore-whitespace needed; miscounted hunks=1; strict rc=128]` — STRICT APPLY NOT CLAIMED: section 1 (Blockchain/Dev/services/auth/src/__tests__/ks963-preauth-rethrow.test.ts): `error: patch fragment without header at line 10: @@ -223,3 +224,29 @@ describe('KS-963 widened — a DB failure no longer burns a single-use token', ()` (apply with the options recorded in section_<k>.opts; the raise seat states which); golden not located — no identity claim is made.

**Held 10:13 2026-09-25 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-25_ks1131-ornith35b-night4/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `6ab9d5021e96ea1481cb6c6ff2d6d33b414aecb7`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (self-testing) touched-file set == { Blockchain/Dev/services/auth/src/__tests__/ks963-preauth-rethrow.test.ts } — one file that is both the product and its test (under Blockchain/Dev/services/auth/src/__tests__)`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/auth/src/__tests__/ks963-preauth-rethrow.test.ts` (product) and `Blockchain/Dev/services/auth/src/__tests__/ks963-preauth-rethrow.test.ts` (test) — equal to numstat.out's set (1 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
27	0	Blockchain/Dev/services/auth/src/__tests__/ks963-preauth-rethrow.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (27 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 27 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 0.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/auth/src/__tests__/ks963-preauth-rethrow.test.ts byte-exact incl. leading whitespace (apply mode lenient): OK 27 line(s) byte-exact incl. leading whitespace (of 27; 27 line(s) added by the apply)` [a3i_indent.out: `OK 27 line(s) byte-exact incl. leading whitespace (of 27; 27 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `section 1 Blockchain/Dev/services/auth/src/__tests__/ks963-preauth-rethrow.test.ts: hunk 1 (@@ -203,4 +203,5 @@ function assertConsumeIsGuarded(src: string, consumeFn: string, lookupFrom: num) declared old=4 new=5 but actual old=5 new=6`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/auth/src/__tests__/ks963-preauth-rethrow.test.ts` (hunks=2, miscount=1; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `--recount --ignore-whitespace`; `apply_check_strict_1.out`: NON-EMPTY: `error: patch fragment without header at line 10: @@ -223,3 +224,29 @@ describe('KS-963 widened — a DB failure no longer burns a single-use token', ()`)
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks963-preauth-rethrow.test.ts fails at the untouched tip (1 failed / 15 run; controls green; assertion reds)` [red_first.json: failed=1 of total=15; red cell(s): ['KS-963 widened — a DB failure no longer burns a single-use token KS-1131 F-B a comment naming the consume inside the !user block is NOT a guarded consume']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks963-preauth-rethrow.test.ts passes with the product hunk (15 passed / 15 run)` [green_after.json: failed=0 of total=15, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=828 failed=0 | after: total=830 failed=0` · `NEW reds: []` [baseline_suite.json total=828 failed=0; after_suite.json total=830 failed=0]
- A6 [verbatim]: `PASS A6 whole services/auth suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/auth: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=1 +27/-0 test=src/__tests__/ks963-preauth-rethrow.test.ts red_first=yes apply_mode=lenient`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/auth/src/__tests__/ks963-preauth-rethrow.test.ts` (+27/-0 per numstat.out) — ONE file: it is both the product and its test (self-testing mode; red-first is by HUNK, not by file). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1 --recount --ignore-whitespace` — at the tip `6ab9d5021e96ea1481cb6c6ff2d6d33b414aecb7` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-25_ks1131-ornith35b-night4/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-25_ks1131-ornith35b-night4/checker.out`.

```diff
--- a/Blockchain/Dev/services/auth/src/__tests__/ks963-preauth-rethrow.test.ts
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks963-preauth-rethrow.test.ts
@@ -203,4 +203,5 @@ function assertConsumeIsGuarded(src: string, consumeFn: string, lookupFrom: num
   // somewhere after it. A sibling occurrence cannot satisfy this.
   const guardBody = braceBlock(src, guard);
   expect(guardBody).not.toBe('');
+  expect(guardBody).toContain(consumeFn + '(');
   expect(guardBody).toContain(consumeFn);
 
@@ -223,3 +224,29 @@ describe('KS-963 widened — a DB failure no longer burns a single-use token', ()
+  // KS-1131 F-B: a comment naming the consume inside the !user block is not a consume.
+  const LF = String.fromCharCode(10);
+  const guardedHandler = (guardLine: string) =>
+    [
+      'router.post(PATH, async (req, res) => {',
+      '  const stored = await userRepo.getResetToken(tokenHash);',
+      '  if (new Date() > stored.expiresAt) {',
+      '    await userRepo.consumeResetToken(tokenHash);',
+      '    return res.status(400).json({ error: 1 });',
+      '  }',
+      '  const user = await userRepo.getUserByIdPreAuth(stored.userId);',
+      '  if (!user) {',
+      guardLine,
+      '    return res.status(404).json({ error: 2 });',
+      '  }',
+      '  await userRepo.consumeResetToken(tokenHash);',
+      '});',
+    ].join(LF);
+  it('KS-1131 F-B a comment naming the consume inside the !user block is NOT a guarded consume', () => {
+    const src = guardedHandler('    // consumeResetToken deliberately not called here any more');
+    expect(() => assertConsumeIsGuarded(src, 'consumeResetToken', 0)).toThrow();
+  });
+  it('KS-1131 F-B CONTROL a real consume inside the !user block still satisfies the helper', () => {
+    const src = guardedHandler('    await userRepo.consumeResetToken(tokenHash);');
+    expect(() => assertConsumeIsGuarded(src, 'consumeResetToken', 0)).not.toThrow();
+  });
   it('the reset-token consume is INSIDE the !user branch, so a throw precedes it', async () => {
     const src = await readRoute('auth.ts');
     assertConsumeIsGuarded(src, 'consumeResetToken', 0);
```
