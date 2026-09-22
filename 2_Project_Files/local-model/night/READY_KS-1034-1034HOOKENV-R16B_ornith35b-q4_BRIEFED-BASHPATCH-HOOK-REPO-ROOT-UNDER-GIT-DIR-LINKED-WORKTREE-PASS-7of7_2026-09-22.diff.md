# READY — KS-1034-1034HOOKENV-R16B (Ornith, briefed, bash_patch, bash) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1034-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 10:29 2026-09-22; sha256[:16] f5032db802b5c29c, 4659 B — a BYTE count; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1034-ornith35b-night/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1034-ornith35b-night/out.md.checker/section_2.diff`). Checker B2 (verbatim from checker.out): `PASS B2 every section applies at the tip (strict)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1034-ornith35b-night/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_feed8-drafter-precheck/HOOKENV/out.md.checker/patch.diff` rc 0, Wednesday (the 07:2x seat)); APPLIED PRODUCT IDENTICAL: the two checkers' own `after.sh` (the script after its hunk) `cmp` rc 0.

**Held 10:29 2026-09-22 by Wednesday (the 07:2x seat) after a source read (hold_ready.py, bash_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1034-ornith35b-night/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `8c2f7b3fd4fde915b2a24542bc32259b24e092a0` (input `bash_patch_1034HOOKENV-R16B.json`).
- Subject [checker.out B0, verbatim]: `PASS B0 subject: clone at 8c2f7b3fd4fde915b2a24542bc32259b24e092a0, Blockchain/Dev/scripts/check-stack-safety.sh and Blockchain/Dev/scripts/__tests__/docker_build_empty_table.test.sh present`
- Output shape [checker.out B1, verbatim]: `PASS B1 output is exactly one fenced ```diff block` · sections [verbatim]: `sections: ['Blockchain/Dev/scripts/check-stack-safety.sh', 'Blockchain/Dev/scripts/__tests__/check_stack_safety_hook_env.test.sh']`
- No new-file normalisation line in checker.out (none applied)
- Touched-file set [checker.out B3, verbatim]: `PASS B3 touched-file set == { Blockchain/Dev/scripts/check-stack-safety.sh , Blockchain/Dev/scripts/__tests__/check_stack_safety_hook_env.test.sh (new) }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/scripts/check-stack-safety.sh` (script) and `Blockchain/Dev/scripts/__tests__/check_stack_safety_hook_env.test.sh` (NEW file — `--- /dev/null` section) — equal to sections.json's paths (2 files); reference test `Blockchain/Dev/scripts/__tests__/docker_build_empty_table.test.sh` untouched.
- Brief lines [checker.out B3b, verbatim]: `PASS B3b every must_change site is a '-' line; every brief '+' line is in the script hunk; no tip line re-added as '+'` — re-measured from `section_1.diff` + input.json defect_line: every one of the 2 brief `+` line(s) present; script `+` lines 2 ordered-equal (whitespace-stripped) to expected_plus (ASCII); `-` lines 1; must_change sites 1/1 each a `-` line; must_remove 1 (all among the `-` lines).
- No B3c line in checker.out (no stays-site repair)
- Sections [out.md.checker/sections.json + section_<k>.diff.opts + .header_measure.out + .check.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/scripts/check-stack-safety.sh` (+2/-1 lines counted from the applied section file; git-apply options per `section_1.diff.opts`: `(none — strict)`; `section_1.diff.header_measure.out`: EMPTY (headers consistent); `section_1.diff.check.out` (strict --check): EMPTY (clean))
- section 2 `section_2.diff` → `Blockchain/Dev/scripts/__tests__/check_stack_safety_hook_env.test.sh` (+71/-0 lines counted from the applied section file; git-apply options per `section_2.diff.opts`: `(none — strict)`; `section_2.diff.header_measure.out`: EMPTY (headers consistent); `section_2.diff.check.out` (strict --check): EMPTY (clean))
- RED-FIRST [checker.out B4, verbatim]: `PASS B4 RED-FIRST: Blockchain/Dev/scripts/__tests__/check_stack_safety_hook_env.test.sh fails at the untouched tip (rc=1, 2 FAIL line(s))` · run line [verbatim]: `B4 run at the tip: rc=1 fail_lines=2 pass_lines=3 load_error=0 timeout=0` [red_first.out re-count: 2 FAIL line(s), 3 pass line(s); FAIL lines: ["FAIL the guard fails when a hook's GIT_DIR is set", 'FAIL files reported missing under GIT_DIR']]
- Parse [checker.out B5a, verbatim]: `PASS B5a the script parses after the hunk (bash -n)`
- GREEN-AFTER [checker.out B5, verbatim]: `PASS B5 GREEN-AFTER: Blockchain/Dev/scripts/__tests__/check_stack_safety_hook_env.test.sh passes with the script hunk (rc=0, 0 FAIL lines, 5 pass line(s))` · run line [verbatim]: `B5 run after the script hunk: rc=0 fail_lines=0 pass_lines=5 load_error=0 timeout=0` [green_after.out re-count: 0 FAIL line(s), 5 pass line(s)]
- Siblings [checker.out B6, verbatim]: `PASS B6 sibling suite(s) that drive check-stack-safety.sh: no NEW failure after (1 suite(s))` [1 sib<i>_after.out file(s) present]
- Shellcheck [checker.out B7, verbatim]: `INFO B7 shellcheck not installed (informational)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 test=Blockchain/Dev/scripts/__tests__/check_stack_safety_hook_env.test.sh red_first=yes apply_mode=strict`
- RESULT [checker.out, verbatim]: `RESULT: PASS (7/7)`

**PR NOTES for the raise seat:** BASH_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/scripts/check-stack-safety.sh` (+2/-1 counted from `section_1.diff` by hold_ready — the bash checker writes no numstat.out) and the NEW test `Blockchain/Dev/scripts/__tests__/check_stack_safety_hook_env.test.sh` (+71/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `8c2f7b3fd4fde915b2a24542bc32259b24e092a0` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (script bytes change) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1034-ornith35b-night/input.json`. Brief (located by ticket + ROWID tokens ['1034', 'HOOKENV', 'R16B'] under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1034-R16B-HOOKENV.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1034-ornith35b-night/checker.out`.

```diff
--- a/Blockchain/Dev/scripts/check-stack-safety.sh
+++ b/Blockchain/Dev/scripts/check-stack-safety.sh
@@ -32,6 +32,7 @@ set -uo pipefail
 # succeeds, because && binds to the result of the whole `a || cd b` list — which
 # concatenated both paths into REPO and broke every path built from it.
-REPO="$(git -C "$ROOT" rev-parse --show-toplevel 2>/dev/null || (cd "$ROOT/../.." && pwd))"
+# KS-1034: in a linked worktree git exports GIT_DIR to hooks, and under it --show-toplevel answers the directory asked from, so clear it for this one query.
+REPO="$(env -u GIT_DIR -u GIT_WORK_TREE git -C "$ROOT" rev-parse --show-toplevel 2>/dev/null || (cd "$ROOT/../.." && pwd))"
 
 EXIT=0
 CHECKS=0
--- /dev/null
+++ b/Blockchain/Dev/scripts/__tests__/check_stack_safety_hook_env.test.sh
@@ -0,0 +1,71 @@
+#!/usr/bin/env bash
+# =============================================================================
+# TESTS for Blockchain/Dev/scripts/check-stack-safety.sh - repo root inside a
+# git hook (KS-1034)
+# =============================================================================
+# The defect: git exports GIT_DIR to hooks run in a linked worktree, and under
+# GIT_DIR the query `git -C Blockchain/Dev rev-parse --show-toplevel` answers
+# Blockchain/Dev instead of the repository root. The guard built every repo-root path one
+# level too deep and reported present files as "missing". run-code-guards.sh
+# shields the guard by unsetting the git env; a direct call from a hook was
+# still exposed. The guard now clears GIT_DIR for that one query.
+#
+# The cells run the REAL guard against this checkout: once with GIT_DIR set the
+# way a hook sets it, once without. It reads files only.
+#
+# Usage: bash Blockchain/Dev/scripts/__tests__/check_stack_safety_hook_env.test.sh
+#        STACK_SAFETY_SH=/path/to/other/copy bash ...   (red-proof)
+# =============================================================================
+set -uo pipefail
+TOTAL_CELLS=5
+
+HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
+REPO_ROOT="$(cd "$HERE/../../../.." && pwd)"
+if [ "${STACK_SAFETY_SH+set}" = set ] && [ -z "$STACK_SAFETY_SH" ]; then
+  echo "FATAL: STACK_SAFETY_SH is set but EMPTY - refusing to silently grade the shipped script." >&2
+  exit 2
+fi
+SUBJ="${STACK_SAFETY_SH-$REPO_ROOT/Blockchain/Dev/scripts/check-stack-safety.sh}"
+[ -f "$SUBJ" ] || { echo "FATAL: check-stack-safety.sh not found at $SUBJ" >&2; exit 2; }
+GD="$(env -u GIT_DIR -u GIT_WORK_TREE git -C "$REPO_ROOT" rev-parse --absolute-git-dir 2>/dev/null)"
+[ -n "$GD" ] || { echo "FATAL: $REPO_ROOT is not a git checkout - this suite needs one to set GIT_DIR" >&2; exit 2; }
+
+pass=0; fail=0
+ok()  { echo "  ok   $1"; pass=$((pass + 1)); }
+bad() { echo "  FAIL $1"; echo "     $2"; fail=$((fail + 1)); }
+
+rc_hook=0; out_hook="$(env -u GIT_WORK_TREE GIT_DIR="$GD" bash "$SUBJ" 2>&1)" || rc_hook=$?
+rc_plain=0; out_plain="$(env -u GIT_DIR -u GIT_WORK_TREE bash "$SUBJ" 2>&1)" || rc_plain=$?
+errors_hook="$(printf '%s' "$out_hook" | grep -c -F '::error::' || true)"
+top_hook="$(env -u GIT_WORK_TREE GIT_DIR="$GD" git -C "$REPO_ROOT/Blockchain/Dev" rev-parse --show-toplevel 2>/dev/null)"
+
+# CELL 1 - red at the tip
+if [ "$rc_hook" -eq 0 ]; then ok "the guard passes when a hook's GIT_DIR is set"
+else bad "the guard fails when a hook's GIT_DIR is set" "rc=$rc_hook"; fi
+
+# CELL 2 - red at the tip
+if [ "$errors_hook" -eq 0 ]; then ok "no present file is reported missing under GIT_DIR"
+else bad "files reported missing under GIT_DIR" "$errors_hook error line(s), first: $(printf '%s' "$out_hook" | grep -m1 -F '::error::')"; fi
+
+# CONTROL CELL 3 - green on both trees
+if [ "$rc_plain" -eq 0 ] && printf '%s' "$out_plain" | grep -qF 'shared-stack safety invariants hold'; then ok "CONTROL the guard passes on this tree without GIT_DIR"
+else bad "CONTROL the guard fails on this tree even without GIT_DIR" "rc=$rc_plain"; fi
+
+# CONTROL CELL 4 - green on both trees
+case "$top_hook" in
+  */Blockchain/Dev) ok "CONTROL under GIT_DIR git itself answers Blockchain/Dev as the top level" ;;
+  *) bad "CONTROL git no longer answers Blockchain/Dev under GIT_DIR - this suite cannot see the hook defect" "top=$top_hook" ;;
+esac
+
+# CONTROL CELL 5 - green on both trees
+if bash -n "$SUBJ"; then ok "CONTROL check-stack-safety.sh parses (bash -n)"
+else bad "CONTROL check-stack-safety.sh does not parse" "bash -n failed"; fi
+
+echo ""
+echo "  $pass passed, $fail failed (of $TOTAL_CELLS cells)"
+if [ "$((pass + fail))" -ne "$TOTAL_CELLS" ]; then
+  echo "  INCOMPLETE - $((pass + fail)) of $TOTAL_CELLS cells ran"
+  exit 1
+fi
+[ "$fail" -eq 0 ] || exit 1
+exit 0
```
