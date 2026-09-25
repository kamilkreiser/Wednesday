# READY — KS-1140-GF1-OFFENDERSUNDER-HANDED-LIST (Ornith, briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-25_ks1140-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 12:51 2026-09-25; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-25_ks1140-ornith35b-night/out.md.checker/section_1.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip — with an accommodation: [Blockchain/Dev/packages/shared/src/__tests__/ks879-no-raw-control-bytes-repo-wide.test.ts: --recount --ignore-whitespace needed; miscounted hunks=2; strict rc=128]` — STRICT APPLY NOT CLAIMED: section 1 (Blockchain/Dev/packages/shared/src/__tests__/ks879-no-raw-control-bytes-repo-wide.test.ts): `error: patch fragment without header at line 16: @@ -148,3 +148,3 @@ describe('KS-879 — no raw control byte anywhere under Blockchain/Dev', () => {` (apply with the options recorded in section_<k>.opts; the raise seat states which); golden not located — no identity claim is made.

**Held 12:51 2026-09-25 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-25_ks1140-ornith35b-night/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `6ab9d5021e96ea1481cb6c6ff2d6d33b414aecb7`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (self-testing) touched-file set == { Blockchain/Dev/packages/shared/src/__tests__/ks879-no-raw-control-bytes-repo-wide.test.ts } — one file that is both the product and its test (under Blockchain/Dev/packages/shared/src/__tests__)`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/packages/shared/src/__tests__/ks879-no-raw-control-bytes-repo-wide.test.ts` (product) and `Blockchain/Dev/packages/shared/src/__tests__/ks879-no-raw-control-bytes-repo-wide.test.ts` (test) — equal to numstat.out's set (1 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
33	3	Blockchain/Dev/packages/shared/src/__tests__/ks879-no-raw-control-bytes-repo-wide.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (33 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 33 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 3.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/packages/shared/src/__tests__/ks879-no-raw-control-bytes-repo-wide.test.ts byte-exact incl. leading whitespace (apply mode lenient): OK 33 line(s) byte-exact incl. leading whitespace (of 33; 33 line(s) added by the apply)` [a3i_indent.out: `OK 33 line(s) byte-exact incl. leading whitespace (of 33; 33 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `section 1 Blockchain/Dev/packages/shared/src/__tests__/ks879-no-raw-control-bytes-repo-wide.test.ts: hunk 1 (@@ -120,9 +120,9 @@ const EXTS = ['.ts', '.tsx', '.js', '.mjs', '.cjs'];) declared old=9 new=9 but actual old=10 new=10`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/packages/shared/src/__tests__/ks879-no-raw-control-bytes-repo-wide.test.ts` (hunks=3, miscount=2; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `--recount --ignore-whitespace`; `apply_check_strict_1.out`: NON-EMPTY: `error: patch fragment without header at line 16: @@ -148,3 +148,3 @@ describe('KS-879 — no raw control byte anywhere under Blockchain/Dev', () => {`)
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks879-no-raw-control-bytes-repo-wide.test.ts fails at the untouched tip (1 failed / 10 run; controls green; assertion reds)` [red_first.json: failed=1 of total=10; red cell(s): ['KS-886 — the walk is repo-wide, as the name and the docblock say KS-1140 GF-1 offendersUnder judges the list it is handed, and the red cell hands it WALKED']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks879-no-raw-control-bytes-repo-wide.test.ts passes with the product hunk (10 passed / 10 run)` [green_after.json: failed=0 of total=10, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=918 failed=0 | after: total=920 failed=0` · `NEW reds: []` [baseline_suite.json total=918 failed=0; after_suite.json total=920 failed=0]
- A6 [verbatim]: `PASS A6 whole packages/shared suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for packages/shared: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=1 +33/-3 test=src/__tests__/ks879-no-raw-control-bytes-repo-wide.test.ts red_first=yes apply_mode=lenient`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/packages/shared/src/__tests__/ks879-no-raw-control-bytes-repo-wide.test.ts` (+33/-3 per numstat.out) — ONE file: it is both the product and its test (self-testing mode; red-first is by HUNK, not by file). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1 --recount --ignore-whitespace` — at the tip `6ab9d5021e96ea1481cb6c6ff2d6d33b414aecb7` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-25_ks1140-ornith35b-night/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-25_ks1140-ornith35b-night/checker.out`.

```diff
--- a/Blockchain/Dev/packages/shared/src/__tests__/ks879-no-raw-control-bytes-repo-wide.test.ts
+++ b/Blockchain/Dev/packages/shared/src/__tests__/ks879-no-raw-control-bytes-repo-wide.test.ts
@@ -120,9 +120,9 @@ const EXTS = ['.ts', '.tsx', '.js', '.mjs', '.cjs'];
  * the SAME function over a scratch tree with a planted NUL, so the walk and
  * the predicate the guard actually uses are what the regression exercises.
  */
-export function offendersUnder(root: string): string[] {
+export function offendersUnder(root: string, files: readonly string[] = sourceFiles(root)): string[] {
   // Bytes, not a string: reading as utf8 goes through a decoder that can
   // normalise or replace, and the claim is about what is ON DISK.
   const out: string[] = [];
-  for (const f of sourceFiles(root)) {
+  for (const f of files) {
     for (const { offset, byte } of rawControlBytes(readFileSync(f))) {
       out.push(`${relative(root, f)}: 0x${byte.toString(16).padStart(2, '0')} at byte ${offset}`);
@@ -148,3 +148,3 @@ describe('KS-879 — no raw control byte anywhere under Blockchain/Dev', () => {
-    const offenders = offendersUnder(DEV_ROOT);
+    const offenders = offendersUnder(DEV_ROOT, WALKED);
     expect(
       offenders,
       'A raw control byte reached a committed file. grep will now skip that whole file ' +
@@ -281,4 +281,34 @@ describe('KS-886 — the walk is repo-wide, as the name and the docblock say', () => {
       rmSync(scratch, { recursive: true, force: true });
     }
   });
+  it('KS-1140 GF-1 offendersUnder judges the list it is handed, and the red cell hands it WALKED', () => {
+    // KS-1140 GF-1: the red cell must judge the SAME array the walk CONTROL and F1 vouch for.
+    const scratch = mkdtempSync(join(tmpdir(), 'ks1140-'));
+    try {
+      const dir = join(scratch, 'tests');
+      mkdirSync(dir, { recursive: true });
+      const clean = join(dir, 'clean.spec.ts');
+      writeFileSync(clean, 'export const ok = 1;');
+      writeFileSync(join(dir, 'planted.spec.ts'), Buffer.from([0x61, 0x00, 0x62]));
+      expect(offendersUnder(scratch, [clean]), 'only the handed list is judged').toEqual([]);
+    } finally {
+      rmSync(scratch, { recursive: true, force: true });
+    }
+    const self = readFileSync(
+      join(DEV_ROOT, 'packages', 'shared', 'src', '__tests__', 'ks879-no-raw-control-bytes-repo-wide.test.ts'),
+      'utf8',
+    );
+    const call = ['offendersUnder(DEV_ROOT', 'WALKED)'].join(', ');
+    expect(self.split(call).length - 1, 'the red cell judges WALKED, the array the controls pin').toBe(1);
+  });
+  it('KS-1140 GF-1 CONTROL a handed list holding the planted file still names its byte', () => {
+    const scratch = mkdtempSync(join(tmpdir(), 'ks1140c-'));
+    try {
+      const planted = join(scratch, 'planted.spec.ts');
+      writeFileSync(planted, Buffer.from([0x61, 0x00, 0x62]));
+      expect(offendersUnder(scratch, [planted])).toEqual(['planted.spec.ts: 0x00 at byte 1']);
+    } finally {
+      rmSync(scratch, { recursive: true, force: true });
+    }
+  });
 });
```
