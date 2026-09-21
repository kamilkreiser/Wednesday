# READY — KS-910 R15 re-run at the CURRENT tip (Kam RULED option a, 2026-09-16 09:53: keep preflight leg 12 as reachability, correct the comment; close on the comment fix) — `Blockchain/Dev/scripts/__tests__/pre_push_hook_base.test.sh` :49-:51 + the NEW suite `pre_push_hook_base_leg_comment.test.sh` (58 lines)
> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks910-ornith35b-night/out.md.checker/patch.diff`** (sha256[:16] b660b8c4b260f1f5, 4093 B; the fence below is that file byte for byte). Run tip **9f0265eb06ecf24d4de18149ce862ad2330a61ee** (input `night/inputs/bash_patch_910LEGCOMMENT-R15.json`). Checker B2 (verbatim): PASS B2 every section applies at the tip — with an accommodation: section_1.diff: REANCHORED (hunk 1: reanchored at 49 (3 '-' / 3 '+' lines; model header -46,9 +46,9);reanchored 1/1 hunk(s);); — the raise seat applies section_1 REANCHORED (`out.md.checker/section_1.diff.reanchored`, hunk at :49) or applies patch.diff with `--recount`; section_2 (the new file) applies strict.
# Held 00:15 2026-09-22 by Wednesday (the 00:05 post-rotation seat) — HAND-WRITTEN (hold_ready.py has no bash_patch support yet, pickup OWED item 1). Source read: the run's `+`/`-` lines are IDENTICAL to the 2026-09-16 READY's fence (`READY_KS-910_ornith35b-q4_BASHPATCH-REANCHORED-REBRIEF-PASS-7of7_2026-09-16.diff.md`, whose applied file Wednesday cmp'd byte-identical to the hand fix that day): 61 `+` / 3 `-` (64 body lines; the `+++`/`---` headers not counted; 3 comment lines replaced); ONLY the hunk's CONTEXT lines differ (the file moved between the 09-16 tip and 9f0265eb0 — the checker REANCHORED at :49). This READY SUPERSEDES the 09-16 one for the raise pool. Checker verdict verbatim: PASS B0 subject: clone at 9f0265eb06ecf24d4de18149ce862ad2330a61ee, Blockchain/Dev/scripts/__tests__/pre_push_hook_base.test.sh and Blockchain/Dev/scripts/__tests__/pre_push_hook_base.test.sh present | PASS B1 output is exactly one fenced ```diff block | PASS B2 every section applies at the tip — with an accommodation: section_1.diff: REANCHORED (hunk 1: reanchored at 49 (3 '-' / 3 '+' lines; model header -46,9 +46,9);reanchored 1/1 hunk(s);); | PASS B3 touched-file set == { Blockchain/Dev/scripts/__tests__/pre_push_hook_base.test.sh , Blockchain/Dev/scripts/__tests__/pre_push_hook_base_leg_comment.test.sh (new) } | PASS B3b every must_change site is a '-' line; every brief '+' line is in the script hunk; no tip line re-added as '+' | PASS B4 RED-FIRST: Blockchain/Dev/scripts/__tests__/pre_push_hook_base_leg_comment.test.sh fails at the untouched tip (rc=1, 2 FAIL line(s)) | PASS B5a the script parses after the hunk (bash -n) | PASS B5 GREEN-AFTER: Blockchain/Dev/scripts/__tests__/pre_push_hook_base_leg_comment.test.sh passes with the script hunk (rc=0, 0 FAIL lines, 4 pass line(s)) | PASS B6 sibling suite(s) that drive pre_push_hook_base.test.sh: no NEW failure after (1 suite(s)) | RESULT: PASS (7/7)
# PR NOTES for the raising seat: (1) TWO files: the comment run in `pre_push_hook_base.test.sh` + the NEW suite `Blockchain/Dev/scripts/__tests__/pre_push_hook_base_leg_comment.test.sh` (58 lines, 4 cells incl. two CONTROLS and the completeness arm; `HOOK_BASE_SUITE` override for red-proofs). (2) CLOSES KS-910 on merge (Kam's ruling: close on the comment fix). (3) Quote Kam's ruling in the PR body; say the preflight leg numbering was read at develop `48e65c435`.

```diff
--- a/Blockchain/Dev/scripts/__tests__/pre_push_hook_base.test.sh
+++ b/Blockchain/Dev/scripts/__tests__/pre_push_hook_base.test.sh
@@ -46,9 +46,9 @@
 # `$(…)` with stderr discarded; that failed, `base` was empty, `changed` stayed empty, and
 # `[ -z "$changed" ] && exit 0` returned SUCCESS before leg 1. Push rc 0, in
 # seconds, with no `[pre-push]` line at all — no gate, and no signal there was
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
