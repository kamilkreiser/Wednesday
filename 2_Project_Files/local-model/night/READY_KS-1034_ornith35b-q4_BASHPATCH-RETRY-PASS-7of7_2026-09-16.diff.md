# READY — KS-1034 (`Blockchain/Dev/scripts/check-stack-safety.sh:34` — in a LINKED worktree git exports GIT_DIR to hooks and `rev-parse --show-toplevel` then answers the wrong directory, so the guard reports every file 'missing — deleted'; the query now clears GIT_DIR/GIT_WORK_TREE)
# Source read by me (Wednesday, 21:20): `diff` of the applied after.sh against `git show 48e65c435:…/check-stack-safety.sh` = EXACTLY line 34 → the comment + `env -u GIT_DIR -u GIT_WORK_TREE git -C "$ROOT" rev-parse --show-toplevel`. Checker PASS 7/7 on the RETRY (20:49; r1 stopped at B3b): B4 red at the tip rc 1 / 2 FAIL, B5 green 5 pass, B6 the sibling suite no new failure. Brief by the 20:07 commission (its set-aside reason measured false; pre-measured 3/5 → 5/5 and a real linked-worktree pre-push rc 1 → rc 0 on git 2.51.0 macOS — other git versions UNMEASURED).
# PR NOTES for the raising seat (raise seat C's partition, `scripts/**`): (1) TWO files: the guard line + the NEW suite `Blockchain/Dev/scripts/__tests__/check_stack_safety_hook_env.test.sh`. (2) The ticket said GIT_DIR reaches hooks in any checkout; measured on git 2.51.0 only in a LINKED worktree — say so. (3) This fixes the class the raise seats' brief flags ('check-stack-safety … is missing — deleted' under a worktree push) — land it EARLY in seat C's queue.

```diff
--- a/Blockchain/Dev/scripts/check-stack-safety.sh
+++ b/Blockchain/Dev/scripts/check-stack-safety.sh
@@ -31,7 +31,9 @@ set -uo pipefail
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
+# TESTS for Blockchain/Dev/scripts/check-stack-safety.sh — repo root inside a
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
