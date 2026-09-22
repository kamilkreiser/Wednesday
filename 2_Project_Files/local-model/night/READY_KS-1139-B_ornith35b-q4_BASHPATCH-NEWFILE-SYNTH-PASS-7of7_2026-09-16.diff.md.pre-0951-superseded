# READY — KS-1139 Part B (validate-lint.sh: the two errexit-live `((X++))` sites → `X=$((X + 1))`; Part A = sync-secrets.sh, held separately) — Ornith ornith:35b (Q4_K_M) r2 PASS 7/7 FIRST SAMPLE on the tightened brief (r1's test was a diff of the reference suite — a real model verdict once the harness could reach it), BASH_PATCH, tip develop M55 48e65c435 (G6 override verified against origin 0b25f823f), run /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-16_ks1139-ornith35b-night3
# Source read by me (Wednesday): the product diff is exactly two -/+ pairs at :33 and :38, the brief's lines byte-for-byte (eight-space indent); the ticket's census regex over the APPLIED script = 0 with its positive control = 1, the assignment-form count = 2 (re-run by Wednesday on out.md.checker/after.sh). The model's suite: three cells in the reference's CELL-4 shape with the closing seven lines present; at the tip 2 red for the predicted reason (2 hits named with their line numbers; 0 assignments), after 3/3 green; bash -n clean; no sibling suite names the script (stated). Accommodations named by the verdict: --recount on the product section; the new file's `@@ -0,0 +1,N @@` header synthesised (the model omits it; every body line was a clean `+`).
# PR NOTES for the Sunday raising seat: (1) bundle with Part A as ONE PR (KS-1139 → Done when both land; the check-script-portability rule 8 stays a Claude seat's follow-up); (2) the suite lives under Blockchain/Dev/scripts/__tests__ and reads the subject at systemTest/schemathesis/validate-lint.sh — run-shell-suites.sh's glob reaches it (verify with --list); (3) the ticket says these two sites were 'to be confirmed at the site (a tested context suppresses errexit)' — Wednesday's read: both are in the BODY of an if/else inside run_check(), not the condition, so errexit applies to them when run_check is called from a plain statement; the assignment form is harmless either way.

```diff
--- a/systemTest/schemathesis/validate-lint.sh
+++ b/systemTest/schemathesis/validate-lint.sh
@@ -30,12 +30,12 @@ run_check() {
     if eval "$cmd" > /dev/null 2>&1; then
         echo -e "${GREEN}✓ PASS${NC}"
-        ((PASS_COUNT++))
+        PASS_COUNT=$((PASS_COUNT + 1))
     else
         echo -e "${RED}✗ FAIL${NC}"
         echo "  Running: $cmd"
         eval "$cmd"
-        ((FAIL_COUNT++))
+        FAIL_COUNT=$((FAIL_COUNT + 1))
     fi
 }
--- /dev/null
+++ b/Blockchain/Dev/scripts/__tests__/validate_lint_errexit.test.sh
@@ -0,0 +1,81 @@
+#!/usr/bin/env bash
+# =============================================================================
+# TESTS for systemTest/schemathesis/validate-lint.sh — KS-1139 Part B
+# The two bare arithmetic-command post-increments at :33 and :38. Under bash ≥ 4.1
+# `set -e`, each fires with status 1 when its counter is 0 and kills the script
+# silently on macOS it does not. This suite pins their ABSENCE statically plus a
+# positive control that both trees share.
+#
+# Usage: bash Blockchain/Dev/scripts/__tests__/validate_lint_errexit.test.sh
+# =============================================================================
+set -uo pipefail
+TOTAL_CELLS=3
+
+HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
+REPO_ROOT="$(cd "$HERE/../../../.." && pwd)"
+if [ "${VALIDATE_LINT_SH+set}" = set ] && [ -z "$VALIDATE_LINT_SH" ]; then
+  echo "FATAL: VALIDATE_LINT_SH is set but EMPTY — refusing to silently grade the shipped script." >&2
+  exit 2
+fi
+SUBJ="${VALIDATE_LINT_SH-$REPO_ROOT/systemTest/schemathesis/validate-lint.sh}"
+[ -f "$SUBJ" ] || { echo "FATAL: validate-lint.sh not found at $SUBJ" >&2; exit 2; }
+[ -r "$SUBJ" ] || { echo "FATAL: VALIDATE_LINT_SH is not readable at $SUBJ" >&2; exit 2; }
+printf 'SUBJECT %s\n        sha256 %s\n\n' "$SUBJ" "$(shasum -a 256 "$SUBJ" | cut -d" " -f1)"
+
+pass=0; fail=0
+ok()  { printf '  ok   %s\n' "$1"; pass=$((pass + 1)); }
+bad() { printf '  FAIL %s\n     %s\n' "$1" "$2"; fail=$((fail + 1)); }
+
+# ---------------------------------------------------------------------------
+# CELL 1 — KS-1139 Part B. The subject has NO bare arithmetic-command
+# post-increment/decrement (`((X++))` / `((X--))` on a line of its own). Such a
+# command exits 1 when its expression evaluates to 0 (post-increment yields the
+# OLD value, so `((PASS_COUNT++))` at PASS_COUNT=0 fails) and bash >= 4.1
+# `set -e` exits on it. bash 3.2 (macOS) does not. Static pin with a positive
+# control inside the cell proving the grep can fire. `[[:space:]]`, not `\s`: BSD grep.
+# ---------------------------------------------------------------------------
+ARITH_RE='^[[:space:]]*\(\([A-Za-z_][A-Za-z_0-9]*(\+\+|--)\)\)[[:space:]]*$'
+arith_control="$(printf '  ((X++))\n' | grep -cE "$ARITH_RE" || true)"
+arith_hits="$(grep -nE "$ARITH_RE" "$SUBJ" || true)"
+arith_count="$(printf '%s' "$arith_hits" | grep -c . || true)"
+if [ "$arith_control" != 1 ]; then
+  bad "validate-lint.sh has NO bare arithmetic-command post-increment/decrement" \
+      "instrument cannot fire: the positive control read $arith_control (expected 1) — the cell is not scoring the subject"
+elif [ "$arith_count" -eq 0 ]; then
+  ok "validate-lint.sh has NO bare arithmetic-command post-increment/decrement — ((X++)) exits 1 at 0 and bash >= 4.1 set -e dies on it (control fires: $arith_control)"
+else
+  bad "validate-lint.sh has NO bare arithmetic-command post-increment/decrement" \
+      "count=$arith_count (control=$arith_control): $(printf '%s' "$arith_hits" | sed 's/^\([0-9]*\):[[:space:]]*/:\1 /' | tr '\n' ' ')"
+fi
+
+# ---------------------------------------------------------------------------
+# CELL 2 — KS-1139 Part B. Both counters advance by assignment form
+# `VAR=$((VAR + 1))`. Untouched script: 0 hits → red. Fixed script: exactly 2.
+# Bracket expressions on purpose — no backslashes in the pattern source.
+# ---------------------------------------------------------------------------
+asg_count="$(grep -cE '^[[:space:]]*(PASS_COUNT|FAIL_COUNT)=[$][(][(](PASS_COUNT|FAIL_COUNT) [+] 1[)][)][[:space:]]*$' "$SUBJ" || true)"
+if [ "$asg_count" = 2 ]; then
+  ok "both counters advance by assignment ($asg_count matches)"
+else
+  bad "both counters advance by assignment" "count=$asg_count (expected 2)"
+fi
+
+# ---------------------------------------------------------------------------
+# CONTROL CELL 3 — The subject parses cleanly under any bash version we run this
+# suite against. Green on both trees; without it a broken edit could pass cells 1
+# and 2 while producing an unrunnable script.
+# ---------------------------------------------------------------------------
+if bash -n "$SUBJ"; then
+  ok "validate-lint.sh parses (bash -n)"
+else
+  bad "validate-lint.sh parses (bash -n)" "bash -n exited non-zero on $SUBJ"
+fi
+
+printf '\n  %d passed, %d failed (of %d cells)\n' "$pass" "$fail" "$TOTAL_CELLS"
+# A cell that never ran is not a pass: the ratio must add up.
+if [ "$((pass + fail))" -ne "$TOTAL_CELLS" ]; then
+  printf '  INCOMPLETE — %d of %d cells ran\n' "$((pass + fail))" "$TOTAL_CELLS"
+  exit 1
+fi
+[ "$fail" -eq 0 ] || exit 1
+exit 0
```
