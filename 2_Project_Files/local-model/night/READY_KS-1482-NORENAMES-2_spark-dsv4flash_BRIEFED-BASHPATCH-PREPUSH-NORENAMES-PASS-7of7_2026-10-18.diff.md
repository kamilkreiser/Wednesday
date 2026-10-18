# READY — KS-1482-NORENAMES-2 (Spark (DeepSeek V4 Flash), briefed, bash_patch, bash) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-18_ks_1482_p2/out.md.checker/patch.diff`** (from `ls` at 23:18 2026-10-18; sha256[:16] 67349a6ad605156e, 2133 B — a BYTE count; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-18_ks_1482_p2/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-18_ks_1482_p2/out.md.checker/section_2.diff`). Checker B2 (verbatim from checker.out): `PASS B2 every section applies at the tip (strict)`; CONTEXT-ONLY difference from the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-18_ks_1482_p2-control/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1; run 2133 B vs golden 2413 B): change lines (`+`/`-`, ordered) IDENTICAL in every section (pre-push 2, ks998_pre_push_judges_the_push.test.sh 12); context/empty lines run vs golden: equal counts; hunk headers identical; APPLIED PRODUCT IDENTICAL: the two checkers' own `after.sh` (the script after its hunk) `cmp` rc 0.

**Held 23:18 2026-10-18 by Wednesday after a source read (hold_ready.py, bash_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-18_ks_1482_p2/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `1f73d7ac8cc17add318601c6c572bcace3d5a596`.
- Subject [checker.out B0, verbatim]: `PASS B0 subject: clone at 1f73d7ac8cc17add318601c6c572bcace3d5a596, .githooks/pre-push and Blockchain/Dev/scripts/__tests__/ks998_pre_push_stale_base_hint.test.sh present`
- Output shape [checker.out B1, verbatim]: `PASS B1 output is exactly one fenced ```diff block` · sections [verbatim]: `sections: ['.githooks/pre-push', 'Blockchain/Dev/scripts/__tests__/ks998_pre_push_judges_the_push.test.sh']`
- No new-file normalisation line in checker.out (none applied)
- Touched-file set [checker.out B3, verbatim]: `PASS B3 touched-file set == { .githooks/pre-push , Blockchain/Dev/scripts/__tests__/ks998_pre_push_judges_the_push.test.sh (MODIFIED in place — test_file pinned to an existing suite, 2026-09-16 KS-1163) }`
- Declared set [input.json product_file + suggested_test_file]: `.githooks/pre-push` (script) and `Blockchain/Dev/scripts/__tests__/ks998_pre_push_judges_the_push.test.sh` (MODIFIED in place) — equal to sections.json's paths (2 files); reference test `Blockchain/Dev/scripts/__tests__/ks998_pre_push_stale_base_hint.test.sh` untouched.
- Brief lines [checker.out B3b, verbatim]: `PASS B3b every must_change site is a '-' line; every brief '+' line is in the script hunk; no tip line re-added as '+'` — re-measured from `section_1.diff` + input.json defect_line: every one of the 1 brief `+` line(s) present; script `+` lines 1 ordered-equal (whitespace-stripped) to expected_plus (ASCII); `-` lines 1; must_change sites 1/1 each a `-` line; must_remove 1 (all among the `-` lines).
- No B3c line in checker.out (no stays-site repair)
- Sections [out.md.checker/sections.json + section_<k>.diff.opts + .header_measure.out + .check.out]:
- section 1 `section_1.diff` → `.githooks/pre-push` (+1/-1 lines counted from the applied section file; git-apply options per `section_1.diff.opts`: `(none — strict)`; `section_1.diff.header_measure.out`: EMPTY (headers consistent); `section_1.diff.check.out` (strict --check): EMPTY (clean))
- section 2 `section_2.diff` → `Blockchain/Dev/scripts/__tests__/ks998_pre_push_judges_the_push.test.sh` (+12/-0 lines counted from the applied section file; git-apply options per `section_2.diff.opts`: `(none — strict)`; `section_2.diff.header_measure.out`: EMPTY (headers consistent); `section_2.diff.check.out` (strict --check): EMPTY (clean))
- RED-FIRST [checker.out B4, verbatim]: `PASS B4 RED-FIRST: Blockchain/Dev/scripts/__tests__/ks998_pre_push_judges_the_push.test.sh fails at the untouched tip (rc=1, 1 FAIL line(s))` · run line [verbatim]: `B4 run at the tip: rc=1 fail_lines=1 pass_lines=75 load_error=0 timeout=0` [red_first.out re-count: 1 FAIL line(s), 75 pass line(s); FAIL lines: ['FAIL RED KS-1482 a file renamed out of Blockchain/Dev, pushed as a NEW branch: the preflight runs']]
- Parse [checker.out B5a, verbatim]: `PASS B5a the script parses after the hunk (bash -n)`
- GREEN-AFTER [checker.out B5, verbatim]: `PASS B5 GREEN-AFTER: Blockchain/Dev/scripts/__tests__/ks998_pre_push_judges_the_push.test.sh passes with the script hunk (rc=0, 0 FAIL lines, 76 pass line(s))` · run line [verbatim]: `B5 run after the script hunk: rc=0 fail_lines=0 pass_lines=76 load_error=0 timeout=0` [green_after.out re-count: 0 FAIL line(s), 76 pass line(s)]
- Siblings [checker.out B6, verbatim]: `PASS B6 sibling suite(s) that drive pre-push: no NEW failure after (14 suite(s))` [14 sib<i>_after.out file(s) present]
- Shellcheck [checker.out B7, verbatim]: `INFO B7 shellcheck not installed (informational)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 test=Blockchain/Dev/scripts/__tests__/ks998_pre_push_judges_the_push.test.sh red_first=yes apply_mode=strict`
- RESULT [checker.out, verbatim]: `RESULT: PASS (7/7)`

**PR NOTES for the raise seat:** BASH_PATCH — PRODUCT BYTES CHANGE: `.githooks/pre-push` (+1/-1 counted from `section_1.diff` by hold_ready — the bash checker writes no numstat.out) and the MODIFIED test `Blockchain/Dev/scripts/__tests__/ks998_pre_push_judges_the_push.test.sh` (+12/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `1f73d7ac8cc17add318601c6c572bcace3d5a596` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (script bytes change) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-18_ks_1482_p2/input.json`. Brief (located from the run dir's own name under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1482_p2/KS-1482.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-18_ks_1482_p2/checker.out`.

```diff
--- a/.githooks/pre-push
+++ b/.githooks/pre-push
@@ -250,5 +250,5 @@ if [ -z "$_jr_up" ]; then
         [ "$_b" = "$_head" ] && continue
         _informative=1
-        _files=$(git -c core.quotePath=false diff --name-only "$_b" "$_tip" || true)
+        _files=$(git -c core.quotePath=false diff --no-renames --name-only "$_b" "$_tip" || true)
         # KS-989: keep the union of every ref consulted, for the systemTest gate.
         # The Blockchain/Dev decision on the next lines is byte-for-byte what it
--- a/Blockchain/Dev/scripts/__tests__/ks998_pre_push_judges_the_push.test.sh
+++ b/Blockchain/Dev/scripts/__tests__/ks998_pre_push_judges_the_push.test.sh
@@ -334,4 +334,16 @@ cell "SC17 a HEAD push from a tracking branch that changes Blockchain/Dev is not
   "$rc/$(n_of "$out" '[preflight] ran')/$(n_of "$out" 'REFUSED')/$(remote_has . refs/heads/tracked-up)"
 
+# ---------------------------------------------------------------------------
+# SC22a - KS-1482: a file renamed OUT of Blockchain/Dev, pushed as a NEW branch with no upstream (the merge-base path of
+# _judge_ref). Git's default rename detection lists the move by its NEW path only, so the preflight was skipped.
+# ---------------------------------------------------------------------------
+build_fixture "$WORK/sc22a"; cd "$WORK/sc22a/fresh"
+git checkout -q -b ren1 --no-track origin/develop
+git mv Blockchain/Dev/file.txt docs/moved.txt; git commit -qm "move file.txt out of Blockchain/Dev"
+cell "CONTROL KS-1482 git lists the moved file as a rename (new branch): only docs/moved.txt, never the old Blockchain/Dev path" "0/1" \
+  "$(git diff --name-only HEAD~1 HEAD | grep -c '^Blockchain/Dev/')/$(git diff --name-only HEAD~1 HEAD | grep -c '^docs/moved.txt')"
+out="$(git push origin ren1 2>&1)"; rc=$?
+cell "RED KS-1482 a file renamed out of Blockchain/Dev, pushed as a NEW branch: the preflight runs" "0/1" "$rc/$(n_of "$out" '[preflight] ran')"
+
 # ---------------------------------------------------------------------------
 # SC18 - MINOR 2 (hook half): a package whose name is NOT ASCII. git quotes such a path in `git diff --name-only`
```
