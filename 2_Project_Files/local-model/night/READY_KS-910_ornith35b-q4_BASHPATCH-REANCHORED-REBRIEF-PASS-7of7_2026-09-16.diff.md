# READY — KS-910 (Kam RULED option a, 2026-09-16 09:53: keep preflight leg 12 as reachability, correct the comment; close on the comment fix) — `Blockchain/Dev/scripts/__tests__/pre_push_hook_base.test.sh` :49-:51, the comment that credited leg 12 with RUNNING this suite now says leg 12 proves it REACHABLE and leg 14 RUNS it
# Source read by me (Wednesday, 20:46): the applied file is BYTE-IDENTICAL (`cmp` rc 0) to Wednesday's hand fix from the pre-measure (the three-line run :49-:51 replaced, re-wrapped, nothing else). r2 = the ONE rebrief under Kam's counter (r1 + retry FAILED B3b: the wrapped-run dialect). Checker PASS 7/7 (20:45, q4): B2 REANCHORED 3 '-' / 3 '+'; B3b all three must_change sites '-', no tip line re-added; B4 RED at the tip rc 1 / 2 FAIL; B5 GREEN 4/4; B6 the sibling suite driving the file: no new failure. Premises measured at the tip: `preflight.sh:521` leg 12 = `run-shell-suites.sh --check-unreached` (exits before the run block); `:544`/`:631` leg 14 runs `run-shell-suites.sh` with no argument.
# PR NOTES for the raising seat: (1) TWO files: the comment run in `pre_push_hook_base.test.sh` + the NEW suite `Blockchain/Dev/scripts/__tests__/pre_push_hook_base_leg_comment.test.sh` (58 lines, 4 cells incl. two CONTROLS and the completeness arm; `HOOK_BASE_SUITE` override for red-proofs). (2) CLOSES KS-910 on merge (Kam's ruling: close on the comment fix). (3) Quote Kam's ruling in the PR body; say the preflight leg numbering was read at develop `48e65c435`.

```diff
--- a/Blockchain/Dev/scripts/__tests__/pre_push_hook_base.test.sh
+++ b/Blockchain/Dev/scripts/__tests__/pre_push_hook_base.test.sh
@@ -46,9 +46,9 @@
 # VACUOUS in the same run — its commit failed too, so the push it asserts on
 # carried no docs change at all. A green cell there meant nothing.
 #
-# Leg 12 of the preflight now reaches this suite on every gated push, so anyone
-# who signs their commits gets that red, pointing at the hook rather than at
-# their own config.
+# Leg 12 of the preflight only proves this suite is REACHABLE (it runs no
+# cell); leg 14 RUNS it on every gated push, so anyone who signs their commits
+# gets that red, pointing at the hook rather than at their own config.
 export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null
 
 HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
--- /dev/null
+++ b/Blockchain/Dev/scripts/__tests__/pre_push_hook_base_leg_comment.test.sh
@@ -0,0 +1,58 @@
+#!/usr/bin/env bash
+# =============================================================================
+# TESTS for the leg-12 comment in pre_push_hook_base.test.sh (KS-910)
+# =============================================================================
+# Preflight leg 12 runs `run-shell-suites.sh --check-unreached`: it proves every
+# suite is REACHABLE and executes no cell. Leg 14 is the leg that RUNS them. The
+# KS-883 comment said leg 12 "reaches" the suite on every gated push, crediting
+# the red to a leg that never runs it. Kam ruled (2026-09-16 09:53): keep leg 12
+# as reachability, correct the comment. These cells pin the corrected wording.
+#
+# Usage: bash Blockchain/Dev/scripts/__tests__/pre_push_hook_base_leg_comment.test.sh
+#        HOOK_BASE_SUITE=/path/to/other/copy bash ...   (red-proof)
+# =============================================================================
+set -uo pipefail
+TOTAL_CELLS=4
+
+HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
+REPO_ROOT="$(cd "$HERE/../../../.." && pwd)"
+if [ "${HOOK_BASE_SUITE+set}" = set ] && [ -z "$HOOK_BASE_SUITE" ]; then
+  echo "FATAL: HOOK_BASE_SUITE is set but EMPTY - refusing to silently grade the shipped file." >&2
+  exit 2
+fi
+SUBJ="${HOOK_BASE_SUITE-$REPO_ROOT/Blockchain/Dev/scripts/__tests__/pre_push_hook_base.test.sh}"
+[ -f "$SUBJ" ] || { echo "FATAL: pre_push_hook_base.test.sh not found at $SUBJ" >&2; exit 2; }
+[ -r "$SUBJ" ] || { echo "FATAL: HOOK_BASE_SUITE is not readable at $SUBJ" >&2; exit 2; }
+
+pass=0; fail=0
+ok()  { echo "  ok   $1"; pass=$((pass + 1)); }
+bad() { echo "  FAIL $1"; echo "     $2"; fail=$((fail + 1)); }
+
+stale_hits="$(grep -c -F 'Leg 12 of the preflight now reaches this suite' "$SUBJ" || true)"
+fix_hits="$(grep -c -F 'leg 14 RUNS it on every gated push' "$SUBJ" || true)"
+anchor_hits="$(grep -c -F 'carried no docs change at all. A green cell there meant nothing.' "$SUBJ" || true)"
+
+# CELL 1 - red at the tip
+if [ "$stale_hits" -eq 0 ]; then ok "the false claim that leg 12 reaches this suite on every gated push is gone"
+else bad "the false leg-12 claim is still present" "hits=$stale_hits"; fi
+
+# CELL 2 - red at the tip
+if [ "$fix_hits" -eq 1 ]; then ok "the comment names leg 14 as the leg that runs this suite"
+else bad "the corrected leg-14 wording is not present exactly once" "hits=$fix_hits"; fi
+
+# CONTROL CELL 3 - green on both trees
+if [ "$anchor_hits" -eq 1 ]; then ok "CONTROL the untouched line above the edited run is still there"
+else bad "CONTROL the untouched line above the edited run moved or vanished" "hits=$anchor_hits"; fi
+
+# CONTROL CELL 4 - green on both trees
+if bash -n "$SUBJ"; then ok "CONTROL pre_push_hook_base.test.sh parses (bash -n)"
+else bad "CONTROL pre_push_hook_base.test.sh does not parse" "bash -n failed"; fi
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
