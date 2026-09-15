# READY — KS-1139 Part A (sync-secrets.sh: the eight errexit-live `((X++))` sites → `X=$((X + 1))`; Part B = validate-lint.sh's two sites, not yet briefed) — Ornith ornith:35b (Q4_K_M) r1 PASS 7/7 on RE-CHECK (the run's own verdict was FAIL B2: two lines of the NEW test beginning '#' had lost their '+' — restored by the new-file normalisation; the product section needed --recount), BASH_PATCH, tip develop M55 48e65c435 (G6 override verified against origin 0b25f823f), run /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-16_ks1139-ornith35b-night (recheck in /recheck)
# Source read by me (Wednesday): the product diff is exactly eight -/+ pairs, each the brief's line byte-for-byte with its own indent (:186 :192 :198 :204 :216 :221 :227 :232); the ticket's census regex over the APPLIED script = 0 with its positive control = 1 (re-run by Wednesday on recheck/out.md.checker/after.sh), the assignment-form count = 8. The model's suite: three cells in the reference's CELL-4 shape (ok/bad printers verbatim, TOTAL_CELLS=3, the INCOMPLETE guard) — at the tip 2 red for the predicted reason (8 hits; 0 assignments), after 3/3 green; B5a bash -n clean; B6 no sibling suite names the script (stated). One slip in the model's header comment: it lists ':222' among the sites (there are eight, :221 is the one) — a comment, not a cell; the PR seat may correct it.
# PR NOTES for the Sunday raising seat: (1) Part B (validate-lint.sh :33 :38) is a separate Ornith brief or a two-line hand edit — bundle it into the SAME PR if held by Sunday; (2) the ticket's 'durable home' (a rule 8 in check-script-portability.sh) is a Claude seat's, not this PR; (3) the new suite is reached by run-shell-suites.sh's scripts/__tests__ glob — verify with --list; (4) apply the REANCHORED section_1 below (the as-written micro-hunks and the as-written test are kept in the run dir); (5) fix the ':222' typo in the test's header comment when raising.

```diff
--- a/Blockchain/Dev/deployment/azure/sync-secrets.sh
+++ b/Blockchain/Dev/deployment/azure/sync-secrets.sh
@@ -183,7 +183,7 @@ for ENTRY in "${SECRETS[@]}"; do
 
     if [ -n "$EXISTING" ]; then
       log_info "Skipping '${NAME}' — already set (auto-generated type: ${GEN_TYPE})"
-      ((SKIPPED++))
+      SKIPPED=$((SKIPPED + 1))
       continue
     fi
 
@@ -189,19 +189,19 @@ for ENTRY in "${SECRETS[@]}"; do
     VALUE=$(generate_value "$GEN_TYPE")
     set_secret "$NAME" "$VALUE" "$DESCRIPTION"
-    ((GENERATED++))
+    GENERATED=$((GENERATED + 1))
 
   elif [[ "$VALUE" == "<manual>"* ]]; then
     # Requires manual input
     if [ -n "$EXISTING" ]; then
       log_info "Skipping '${NAME}' — already set"
-      ((SKIPPED++))
+      SKIPPED=$((SKIPPED + 1))
       continue
     fi
 
     if [ "$NON_INTERACTIVE" = true ]; then
       log_warn "Skipping '${NAME}' — requires manual input (use interactive mode)"
-      ((SKIPPED++))
+      SKIPPED=$((SKIPPED + 1))
       continue
     fi
 
@@ -213,12 +213,12 @@ for ENTRY in "${SECRETS[@]}"; do
 
     if [ -z "$MANUAL_VALUE" ]; then
       log_warn "Skipping '${NAME}' — empty value"
-      ((SKIPPED++))
+      SKIPPED=$((SKIPPED + 1))
       continue
     fi
 
     set_secret "$NAME" "$MANUAL_VALUE" "$DESCRIPTION"
-    ((UPDATED++))
+    UPDATED=$((UPDATED + 1))
 
   else
     # Static value
@@ -226,13 +226,13 @@ for ENTRY in "${SECRETS[@]}"; do
     if [ "$EXISTING" = "$VALUE" ]; then
       log_info "Skipping '${NAME}' — already correct"
-      ((SKIPPED++))
+      SKIPPED=$((SKIPPED + 1))
       continue
     fi
 
     set_secret "$NAME" "$VALUE" "$DESCRIPTION"
-    ((UPDATED++))
+    UPDATED=$((UPDATED + 1))
   fi
 done
--- /dev/null
+++ b/Blockchain/Dev/scripts/__tests__/sync_secrets_errexit.test.sh
@@ -0,0 +1,88 @@
+#!/usr/bin/env bash
+# =============================================================================
+# TESTS for Blockchain/Dev/deployment/azure/sync-secrets.sh — the eight errexit-live arithmetic-command sites (KS-1139)
+# =============================================================================
+# The defect: `((X++))` exits 1 when X is 0 under bash >= 4.1 `set -e`. This
+# script uses that form at exactly 8 sites (:186 :192 :198 :204 :216 :221 :222
+# :227 :232). On macOS (bash 3.2) it passes silently; on Linux CI it dies.
+#
+# These cells pin the ABSENCE of the bare arithmetic command and prove the fix
+# does not break parsing. No temp dir needed — only read access to the subject.
+#
+# Usage: bash Blockchain/Dev/scripts/__tests__/sync_secrets_errexit.test.sh
+#        SYNC_SECRETS_SH=/path/to/other/sync-secrets.sh bash …
+# =============================================================================
+set -uo pipefail
+TOTAL_CELLS=3
+
+HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
+REPO_ROOT="$(cd "$HERE/../../../.." && pwd)"
+if [ "${SYNC_SECRETS_SH+set}" = set ] && [ -z "$SYNC_SECRETS_SH" ]; then
+  echo "FATAL: SYNC_SECRETS_SH is set but EMPTY — refusing to silently grade the shipped script." >&2
+  exit 2
+fi
+SUBJ="${SYNC_SECRETS_SH-$REPO_ROOT/Blockchain/Dev/deployment/azure/sync-secrets.sh}"
+[ -f "$SUBJ" ] || { echo "FATAL: sync-secrets.sh not found at $SUBJ" >&2; exit 2; }
+[ -r "$SUBJ" ] || { echo "FATAL: SYNC_SECRETS_SH is not readable at $SUBJ" >&2; exit 2; }
+printf 'SUBJECT %s\n        sha256 %s\n\n' "$SUBJ" "$(shasum -a 256 "$SUBJ" | cut -d" " -f1)"
+
+pass=0; fail=0
+ok()  { printf '  ok   %s\n' "$1"; pass=$((pass + 1)); }
+bad() { printf '  FAIL %s\n     %s\n' "$1" "$2"; fail=$((fail + 1)); }
+
+# ---------------------------------------------------------------------------
+# CELL 1 — KS-1139. The subject has NO bare arithmetic-command post-increment/
+# decrement (`((X++))` / `((X--))` on a line of its own). Such a command exits
+# 1 when its expression evaluates to 0 — a post-increment yields the OLD value,
+# so `((SKIPPED++))` at SKIPPED=0 "fails" — and bash >= 4.1 `set -e` exits on
+# it (bash COMPAT item 45). bash 3.2 does not, which is why this passes here
+# and REDS on CI's ubuntu. This is a STATIC pin, honest about being one. The
+# positive control inside the cell proves the grep can fire (a here-string
+# holding `((X++))` -> 1). `[[:space:]]`, not `\s`: BSD grep.
+# ---------------------------------------------------------------------------
+ARITH_RE='^[[:space:]]*\(\([A-Za-z_][A-Za-z_0-9]*(\+\+|--)\)\)[[:space:]]*$'
+arith_control="$(printf '  ((X++))\n' | grep -cE "$ARITH_RE" || true)"
+arith_hits="$(grep -nE "$ARITH_RE" "$SUBJ" || true)"
+arith_count="$(printf '%s' "$arith_hits" | grep -c . || true)"
+if [ "$arith_control" != 1 ]; then
+  bad "sync-secrets.sh has NO bare arithmetic-command post-increment/decrement" \
+      "instrument cannot fire: the positive control read $arith_control (expected 1) — the cell is not scoring the subject"
+elif [ "$arith_count" -eq 0 ]; then
+  ok "sync-secrets.sh has NO bare arithmetic-command post-increment/decrement — ((X++)) exits 1 at 0 and bash >= 4.1 set -e dies on it (control fires: $arith_control)"
+else
+  bad "sync-secrets.sh has NO bare arithmetic-command post-increment/decrement" \
+      "count=$arith_count (control=$arith_control): $(printf '%s' "$arith_hits" | sed 's/^\([0-9]*\):[[:space:]]*/:\1 /' | tr '\n' ' ')"
+fi
+
+# ---------------------------------------------------------------------------
+# CELL 2 — KS-1139 round 2. The three counters advance by assignment form
+# X=$((X + 1)) at all 8 sites. Asserted via grep count of the exact pattern.
+# Untouched script: 0 hits → FAIL. Fixed script: 8 hits → PASS.
+# ---------------------------------------------------------------------------
+asg_re='^[[:space:]]*(SKIPPED|GENERATED|UPDATED)=[$][(][(](SKIPPED|GENERATED|UPDATED) [+] 1[)][)][[:space:]]*$'
+asg_count="$(grep -cE "$asg_re" "$SUBJ" || true)"
+if [ "$asg_count" = 8 ]; then
+  ok "the three counters advance by assignment at all 8 sites ($asg_count matches)"
+else
+  bad "the three counters advance by assignment at all 8 sites" \
+      "found $asg_count expected 8 — the fix did not land everywhere"
+fi
+
+# ---------------------------------------------------------------------------
+# CELL 3 — CONTROL. The subject parses under `bash -n`. Green on both trees.
+# ---------------------------------------------------------------------------
+if bash -n "$SUBJ"; then
+  ok "sync-secrets.sh parses (bash -n)"
+else
+  bad "sync-secrets.sh parses (bash -n)" \
+      "`bash -n` exited non-zero — syntax error in the shipped script"
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
