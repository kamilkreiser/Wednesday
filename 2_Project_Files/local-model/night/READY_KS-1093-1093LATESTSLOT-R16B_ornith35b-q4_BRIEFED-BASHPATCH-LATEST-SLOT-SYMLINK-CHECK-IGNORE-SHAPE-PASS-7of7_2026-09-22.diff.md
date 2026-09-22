# READY — KS-1093-1093LATESTSLOT-R16B (Ornith, briefed, bash_patch, bash) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1093-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 10:29 2026-09-22; sha256[:16] c6f466b8676a44b5, 6778 B — a BYTE count; NOTE — `cat section_*.diff | cmp patch.diff` rc 1, differing by 1 line(s) (all EMPTY — the checker's splitter rstrips each section's trailing empty lines); patch.diff is the model's AS-WRITTEN block, the SECTION FILES are the applied units and the canonical for the raise: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1093-ornith35b-night/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1093-ornith35b-night/out.md.checker/section_2.diff`). Checker B2 (verbatim from checker.out): `PASS B2 every section applies at the tip (strict)`; CONTEXT-ONLY difference from the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_feed8-drafter-precheck/LATESTSLOT/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1; run 6778 B vs golden 6777 B): change lines (`+`/`-`, ordered) IDENTICAL in every section (check-stack-safety.sh 4, check_stack_safety_latest_slot_symlink.test.sh 67); context/empty lines run vs golden: check-stack-safety.sh 13/13 context + 1/0 empty; hunk headers identical; APPLIED PRODUCT IDENTICAL: the two checkers' own `after.sh` (the script after its hunk) `cmp` rc 0; the new test's content IS its `+` lines, so the created file is identical.

**Held 10:29 2026-09-22 by Wednesday (the 07:2x seat) after a source read (hold_ready.py, bash_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1093-ornith35b-night/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `8c2f7b3fd4fde915b2a24542bc32259b24e092a0` (input `bash_patch_1093LATESTSLOT-R16B.json`).
- Subject [checker.out B0, verbatim]: `PASS B0 subject: clone at 8c2f7b3fd4fde915b2a24542bc32259b24e092a0, Blockchain/Dev/scripts/check-stack-safety.sh and Blockchain/Dev/scripts/__tests__/docker_build_empty_table.test.sh present`
- Output shape [checker.out B1, verbatim]: `PASS B1 output is exactly one fenced ```diff block` · sections [verbatim]: `sections: ['Blockchain/Dev/scripts/check-stack-safety.sh', 'Blockchain/Dev/scripts/__tests__/check_stack_safety_latest_slot_symlink.test.sh']`
- No new-file normalisation line in checker.out (none applied)
- Touched-file set [checker.out B3, verbatim]: `PASS B3 touched-file set == { Blockchain/Dev/scripts/check-stack-safety.sh , Blockchain/Dev/scripts/__tests__/check_stack_safety_latest_slot_symlink.test.sh (new) }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/scripts/check-stack-safety.sh` (script) and `Blockchain/Dev/scripts/__tests__/check_stack_safety_latest_slot_symlink.test.sh` (NEW file — `--- /dev/null` section) — equal to sections.json's paths (2 files); reference test `Blockchain/Dev/scripts/__tests__/docker_build_empty_table.test.sh` untouched.
- Brief lines [checker.out B3b, verbatim]: `PASS B3b every must_change site is a '-' line; every brief '+' line is in the script hunk; no tip line re-added as '+'` — re-measured from `section_1.diff` + input.json defect_line: every one of the 3 brief `+` line(s) present; script `+` lines 3 ordered-equal (whitespace-stripped) to expected_plus (ASCII); `-` lines 1; must_change sites 1/1 each a `-` line; must_remove 1 (all among the `-` lines).
- No B3c line in checker.out (no stays-site repair)
- Sections [out.md.checker/sections.json + section_<k>.diff.opts + .header_measure.out + .check.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/scripts/check-stack-safety.sh` (+3/-1 lines counted from the applied section file; git-apply options per `section_1.diff.opts`: `(none — strict)`; `section_1.diff.header_measure.out`: EMPTY (headers consistent); `section_1.diff.check.out` (strict --check): EMPTY (clean))
- section 2 `section_2.diff` → `Blockchain/Dev/scripts/__tests__/check_stack_safety_latest_slot_symlink.test.sh` (+67/-0 lines counted from the applied section file; git-apply options per `section_2.diff.opts`: `(none — strict)`; `section_2.diff.header_measure.out`: EMPTY (headers consistent); `section_2.diff.check.out` (strict --check): EMPTY (clean))
- RED-FIRST [checker.out B4, verbatim]: `PASS B4 RED-FIRST: Blockchain/Dev/scripts/__tests__/check_stack_safety_latest_slot_symlink.test.sh fails at the untouched tip (rc=1, 3 FAIL line(s))` · run line [verbatim]: `B4 run at the tip: rc=1 fail_lines=3 pass_lines=3 load_error=0 timeout=0` [red_first.out re-count: 3 FAIL line(s), 3 pass line(s); FAIL lines: ['FAIL the probe no longer reads THROUGH the latest-slot symlink (index.html)', 'FAIL the probe names the latest-slot symlink ITSELF', 'FAIL with a latest-slot4 symlink present the gate exits 0 and names no latest-slot error']]
- Parse [checker.out B5a, verbatim]: `PASS B5a the script parses after the hunk (bash -n)`
- GREEN-AFTER [checker.out B5, verbatim]: `PASS B5 GREEN-AFTER: Blockchain/Dev/scripts/__tests__/check_stack_safety_latest_slot_symlink.test.sh passes with the script hunk (rc=0, 0 FAIL lines, 6 pass line(s))` · run line [verbatim]: `B5 run after the script hunk: rc=0 fail_lines=0 pass_lines=6 load_error=0 timeout=0` [green_after.out re-count: 0 FAIL line(s), 6 pass line(s)]
- Siblings [checker.out B6, verbatim]: `PASS B6 sibling suite(s) that drive check-stack-safety.sh: no NEW failure after (1 suite(s))` [1 sib<i>_after.out file(s) present]
- Shellcheck [checker.out B7, verbatim]: `INFO B7 shellcheck not installed (informational)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 test=Blockchain/Dev/scripts/__tests__/check_stack_safety_latest_slot_symlink.test.sh red_first=yes apply_mode=strict`
- RESULT [checker.out, verbatim]: `RESULT: PASS (7/7)`

**PR NOTES for the raise seat:** BASH_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/scripts/check-stack-safety.sh` (+3/-1 counted from `section_1.diff` by hold_ready — the bash checker writes no numstat.out) and the NEW test `Blockchain/Dev/scripts/__tests__/check_stack_safety_latest_slot_symlink.test.sh` (+67/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `8c2f7b3fd4fde915b2a24542bc32259b24e092a0` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (script bytes change) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1093-ornith35b-night/input.json`. Brief (located by ticket + ROWID tokens ['1093', 'LATESTSLOT', 'R16B'] under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1093-R16B-LATESTSLOT.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1093-ornith35b-night/checker.out`.

```diff
--- a/Blockchain/Dev/scripts/check-stack-safety.sh
+++ b/Blockchain/Dev/scripts/check-stack-safety.sh
@@ -318,7 +318,9 @@ PW_STAMP="2026-01-01T00-00-00-000Z"
 # Honest limit, measured on #803 review: `systemTest/playwright/.gitignore` carries a blanket
 # `results/`, so every `results/...` probe passes by that line alone — they prove the blanket
 # holds, not the suffix. The `.auth-*/` probe is the one that tests a suffix pattern, and it is the
 # one holding a bearer token, which is why it is here for every slot and not just slot 3.
+# KS-1093: `latest-slot<N>` is a SYMLINK once a run exists, and `git check-ignore` refuses any path
+# beyond a symlink (fatal, rc 128 - read as "not ignored"). Probe the symlink ITSELF, never through it.
 PW_STAMP="2026-01-01T00-00-00-000Z"
 for slot in 1 2 3 4; do
   for artifact in \
@@ -325,7 +327,7 @@ PW_STAMP="2026-01-01T00-00-00-000Z"
     "$REPO/systemTest/playwright/results/playwright-report-ks-682-${PW_STAMP}-slot${slot}/index.html" \
     "$REPO/systemTest/playwright/results/test-results-ks-682-${PW_STAMP}-slot${slot}/.last-run.json" \
     "$REPO/systemTest/playwright/results/har-ks-682-${PW_STAMP}-slot${slot}/1.har" \
-    "$REPO/systemTest/playwright/results/latest-slot${slot}/index.html" \
+    "$REPO/systemTest/playwright/results/latest-slot${slot}" \
     "$REPO/systemTest/playwright/.auth-ks-682-slot${slot}/token.json" \
     "$REPO/systemTest/playwright/.auth-ks-682-slot${slot}/state.json"; do
     if git -C "$REPO" check-ignore -q "$artifact" 2>/dev/null; then ok; else

--- /dev/null
+++ b/Blockchain/Dev/scripts/__tests__/check_stack_safety_latest_slot_symlink.test.sh
@@ -0,0 +1,67 @@
+#!/usr/bin/env bash
+# =============================================================================
+# TESTS for Blockchain/Dev/scripts/check-stack-safety.sh - latest-slot symlinks (KS-1093)
+# =============================================================================
+# The defect: with `systemTest/playwright/results/latest-slot4` a symlink,
+# the gate prints `::error::latest-slot4/index.html is NOT gitignored on slot 4 (KS-682).`
+# and exits 1 because `git check-ignore` refuses paths beyond a symbolic link.
+# This suite proves E1+E2 fix that without weakening what is proven.
+#
+# Usage: bash Blockchain/Dev/scripts/__tests__/check_stack_safety_latest_slot_symlink.test.sh
+# =============================================================================
+set -uo pipefail
+TOTAL_CELLS=6
+
+HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
+REPO_ROOT="$(cd "$HERE/../../../.." && pwd)"
+SUBJ="${CHECK_STACK_SAFETY_SH-$REPO_ROOT/Blockchain/Dev/scripts/check-stack-safety.sh}"
+[ -f "$SUBJ" ] || { echo "FATAL: check-stack-safety.sh not found at $SUBJ" >&2; exit 2; }
+[ -r "$SUBJ" ] || { echo "FATAL: CHECK_STACK_SAFETY_SH is not readable at $SUBJ" >&2; exit 2; }
+printf 'SUBJECT %s\n        sha256 %s\n\n' "$SUBJ" "$(shasum -a 256 "$SUBJ" | cut -d" " -f1)"
+
+WORK="$(mktemp -d "${TMPDIR:-/tmp}/ks1093.XXXXXX")"
+trap 'rm -rf "$WORK"' EXIT
+
+pass=0; fail=0
+ok()  { printf '  ok   %s\n' "$1"; pass=$((pass + 1)); }
+bad() { printf '  FAIL %s\n     %s\n' "$1" "$2"; fail=$((fail + 1)); }
+RES="$REPO_ROOT/systemTest/playwright/results"
+
+# CELL 1 - RED at the tip: the through-symlink probe is gone.
+through_hits="$(grep -c 'results/latest-slot${slot}/index.html' "$SUBJ" || true)"
+if [ "$through_hits" -eq 0 ]; then ok "the probe no longer reads THROUGH the latest-slot symlink (index.html)"; else bad "the probe no longer reads THROUGH the latest-slot symlink (index.html)" "count=$through_hits (expected 0)"; fi
+# CELL 2 - RED at the tip: the probe of the symlink itself is present.
+self_hits="$(grep -c 'results/latest-slot${slot}"' "$SUBJ" || true)"
+if [ "$self_hits" -eq 1 ]; then ok "the probe names the latest-slot symlink ITSELF"; else bad "the probe names the latest-slot symlink ITSELF" "count=$self_hits (expected 1)"; fi
+# CELL 3 - CONTROL on a clean checkout: the gate exits 0 on this tree as found (nothing created yet).
+bash "$SUBJ" > "$WORK/clean.out" 2>&1; rc_clean=$?
+if [ "$rc_clean" -eq 0 ]; then ok "the gate exits 0 on this tree as found"; else bad "the gate exits 0 on this tree as found" "rc=$rc_clean: $(grep '::error::' "$WORK/clean.out" | head -2 | tr '\n' ' ')"; fi
+# CELL 4 - RED at the tip: with a latest-slot4 SYMLINK present the gate still exits 0 and names no latest-slot error.
+made_results=0; made_link=0
+[ -d "$RES" ] || { mkdir -p "$RES"; made_results=1; }
+if [ ! -e "$RES/latest-slot4" ] && [ ! -L "$RES/latest-slot4" ]; then
+  mkdir -p "$RES/playwright-report-ks-1093-slot4"; : > "$RES/playwright-report-ks-1093-slot4/index.html"
+  ln -s playwright-report-ks-1093-slot4 "$RES/latest-slot4"; made_link=1
+fi
+bash "$SUBJ" > "$WORK/symlink.out" 2>&1; rc_link=$?
+link_errors="$(grep -c '::error::latest-slot' "$WORK/symlink.out" || true)"
+if [ "$made_link" -eq 1 ]; then rm "$RES/latest-slot4"; rm "$RES/playwright-report-ks-1093-slot4/index.html"; rmdir "$RES/playwright-report-ks-1093-slot4"; fi
+if [ "$made_results" -eq 1 ]; then rmdir "$RES" 2>/dev/null || true; fi
+if [ "$rc_link" -eq 0 ] && [ "$link_errors" -eq 0 ]; then ok "with a latest-slot4 symlink present the gate exits 0 and names no latest-slot error"; else bad "with a latest-slot4 symlink present the gate exits 0 and names no latest-slot error" "rc=$rc_link latest-slot errors=$link_errors"; fi
+# CELL 5 - CONTROL: the git mechanism the fix rests on, in a throwaway repo (through the symlink: rc 128; the symlink itself: rc 0).
+git -C "$WORK" init -q; printf 'results/\n' > "$WORK/.gitignore"
+mkdir -p "$WORK/results/playwright-report-x-slot4"; ln -s playwright-report-x-slot4 "$WORK/results/latest-slot4"
+git -C "$WORK" check-ignore -q results/latest-slot4/index.html 2>/dev/null; rc_through=$?
+git -C "$WORK" check-ignore -q results/latest-slot4 2>/dev/null; rc_self=$?
+if [ "$rc_through" -eq 128 ] && [ "$rc_self" -eq 0 ]; then ok "git check-ignore refuses a path beyond a symlink (rc 128) and accepts the symlink itself (rc 0)"; else bad "git check-ignore refuses a path beyond a symlink (rc 128) and accepts the symlink itself (rc 0)" "through=$rc_through self=$rc_self"; fi
+# CELL 6 - CONTROL: the subject parses.
+if bash -n "$SUBJ" >/dev/null 2>&1; then ok "check-stack-safety.sh parses (bash -n)"; else bad "check-stack-safety.sh parses (bash -n)" "$(bash -n "$SUBJ" 2>&1 | head -5 | tr '\n' ' ')"; fi
+
+printf '\n  %d passed, %d failed (of %d cells)\n' "$pass" "$fail" "$TOTAL_CELLS"
+# A cell that never ran is not a pass (KS-1093 round 2): the ratio must add up.
+if [ "$((pass + fail))" -ne "$TOTAL_CELLS" ]; then
+  printf '  INCOMPLETE - %d of %d cells ran\n' "$((pass + fail))" "$TOTAL_CELLS"
+  exit 1
+fi
+[ "$fail" -eq 0 ] || exit 1
+exit 0
```
