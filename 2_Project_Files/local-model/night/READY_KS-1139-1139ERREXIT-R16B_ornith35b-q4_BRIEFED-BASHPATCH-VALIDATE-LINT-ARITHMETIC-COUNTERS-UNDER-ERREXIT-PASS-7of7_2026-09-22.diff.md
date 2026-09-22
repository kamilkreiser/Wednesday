# READY — KS-1139-1139ERREXIT-R16B (Ornith, briefed, bash_patch, bash) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1139-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 10:29 2026-09-22; sha256[:16] 2fe125801cd96c6e, 5196 B — a BYTE count; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1139-ornith35b-night/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1139-ornith35b-night/out.md.checker/section_2.diff`). Checker B2 (verbatim from checker.out): `PASS B2 every section applies at the tip (strict)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1139-ornith35b-night/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_feed8-drafter-precheck/ERREXIT/out.md.checker/patch.diff` rc 0, Wednesday (the 07:2x seat)); APPLIED PRODUCT IDENTICAL: the two checkers' own `after.sh` (the script after its hunk) `cmp` rc 0.

**Held 10:29 2026-09-22 by Wednesday (the 07:2x seat) after a source read (hold_ready.py, bash_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1139-ornith35b-night/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `8c2f7b3fd4fde915b2a24542bc32259b24e092a0` (input `bash_patch_1139ERREXIT-R16B.json`).
- Subject [checker.out B0, verbatim]: `PASS B0 subject: clone at 8c2f7b3fd4fde915b2a24542bc32259b24e092a0, systemTest/schemathesis/validate-lint.sh and Blockchain/Dev/scripts/__tests__/docker_build_empty_table.test.sh present`
- Output shape [checker.out B1, verbatim]: `PASS B1 output is exactly one fenced ```diff block` · sections [verbatim]: `sections: ['systemTest/schemathesis/validate-lint.sh', 'Blockchain/Dev/scripts/__tests__/validate_lint_errexit.test.sh']`
- No new-file normalisation line in checker.out (none applied)
- Touched-file set [checker.out B3, verbatim]: `PASS B3 touched-file set == { systemTest/schemathesis/validate-lint.sh , Blockchain/Dev/scripts/__tests__/validate_lint_errexit.test.sh (new) }`
- Declared set [input.json product_file + suggested_test_file]: `systemTest/schemathesis/validate-lint.sh` (script) and `Blockchain/Dev/scripts/__tests__/validate_lint_errexit.test.sh` (NEW file — `--- /dev/null` section) — equal to sections.json's paths (2 files); reference test `Blockchain/Dev/scripts/__tests__/docker_build_empty_table.test.sh` untouched.
- Brief lines [checker.out B3b, verbatim]: `PASS B3b every must_change site is a '-' line; every brief '+' line is in the script hunk; no tip line re-added as '+'` — re-measured from `section_1.diff` + input.json defect_line: every one of the 2 brief `+` line(s) present; script `+` lines 2 ordered-equal (whitespace-stripped) to expected_plus (ASCII); `-` lines 2; must_change sites 2/2 each a `-` line; must_remove 2 (all among the `-` lines).
- No B3c line in checker.out (no stays-site repair)
- Sections [out.md.checker/sections.json + section_<k>.diff.opts + .header_measure.out + .check.out]:
- section 1 `section_1.diff` → `systemTest/schemathesis/validate-lint.sh` (+2/-2 lines counted from the applied section file; git-apply options per `section_1.diff.opts`: `(none — strict)`; `section_1.diff.header_measure.out`: EMPTY (headers consistent); `section_1.diff.check.out` (strict --check): EMPTY (clean))
- section 2 `section_2.diff` → `Blockchain/Dev/scripts/__tests__/validate_lint_errexit.test.sh` (+81/-0 lines counted from the applied section file; git-apply options per `section_2.diff.opts`: `(none — strict)`; `section_2.diff.header_measure.out`: EMPTY (headers consistent); `section_2.diff.check.out` (strict --check): EMPTY (clean))
- RED-FIRST [checker.out B4, verbatim]: `PASS B4 RED-FIRST: Blockchain/Dev/scripts/__tests__/validate_lint_errexit.test.sh fails at the untouched tip (rc=1, 2 FAIL line(s))` · run line [verbatim]: `B4 run at the tip: rc=1 fail_lines=2 pass_lines=1 load_error=0 timeout=0` [red_first.out re-count: 2 FAIL line(s), 1 pass line(s); FAIL lines: ['FAIL validate-lint.sh has NO bare arithmetic-command post-increment/decrement', 'FAIL both counters advance by assignment']]
- Parse [checker.out B5a, verbatim]: `PASS B5a the script parses after the hunk (bash -n)`
- GREEN-AFTER [checker.out B5, verbatim]: `PASS B5 GREEN-AFTER: Blockchain/Dev/scripts/__tests__/validate_lint_errexit.test.sh passes with the script hunk (rc=0, 0 FAIL lines, 3 pass line(s))` · run line [verbatim]: `B5 run after the script hunk: rc=0 fail_lines=0 pass_lines=3 load_error=0 timeout=0` [green_after.out re-count: 0 FAIL line(s), 3 pass line(s)]
- Siblings [checker.out B6, verbatim]: `INFO B6 no sibling suite in Blockchain/Dev/scripts/__tests__ names validate-lint.sh — nothing else drives this script (stated, not counted)`
- Shellcheck [checker.out B7, verbatim]: `INFO B7 shellcheck not installed (informational)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 test=Blockchain/Dev/scripts/__tests__/validate_lint_errexit.test.sh red_first=yes apply_mode=strict`
- RESULT [checker.out, verbatim]: `RESULT: PASS (7/7)`

**PR NOTES for the raise seat:** BASH_PATCH — PRODUCT BYTES CHANGE: `systemTest/schemathesis/validate-lint.sh` (+2/-2 counted from `section_1.diff` by hold_ready — the bash checker writes no numstat.out) and the NEW test `Blockchain/Dev/scripts/__tests__/validate_lint_errexit.test.sh` (+81/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `8c2f7b3fd4fde915b2a24542bc32259b24e092a0` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (script bytes change) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1139-ornith35b-night/input.json`. Brief (located by ticket + ROWID tokens ['1139', 'ERREXIT', 'R16B'] under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1139-R16B-ERREXIT.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1139-ornith35b-night/checker.out`.

```diff
--- a/systemTest/schemathesis/validate-lint.sh
+++ b/systemTest/schemathesis/validate-lint.sh
@@ -31,5 +31,5 @@ run_check() {
     if eval "$cmd" > /dev/null 2>&1; then
         echo -e "${GREEN}✓ PASS${NC}"
-        ((PASS_COUNT++))
+        PASS_COUNT=$((PASS_COUNT + 1))
     else
         echo -e "${RED}✗ FAIL${NC}"
@@ -36,5 +36,5 @@ run_check() {
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
+# TESTS for systemTest/schemathesis/validate-lint.sh - KS-1139 Part B
+# The two bare arithmetic-command post-increments at :33 and :38. Under bash >= 4.1
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
+  echo "FATAL: VALIDATE_LINT_SH is set but EMPTY - refusing to silently grade the shipped script." >&2
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
+# CELL 1 - KS-1139 Part B. The subject has NO bare arithmetic-command
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
+      "instrument cannot fire: the positive control read $arith_control (expected 1) - the cell is not scoring the subject"
+elif [ "$arith_count" -eq 0 ]; then
+  ok "validate-lint.sh has NO bare arithmetic-command post-increment/decrement - ((X++)) exits 1 at 0 and bash >= 4.1 set -e dies on it (control fires: $arith_control)"
+else
+  bad "validate-lint.sh has NO bare arithmetic-command post-increment/decrement" \
+      "count=$arith_count (control=$arith_control): $(printf '%s' "$arith_hits" | sed 's/^\([0-9]*\):[[:space:]]*/:\1 /' | tr '\n' ' ')"
+fi
+
+# ---------------------------------------------------------------------------
+# CELL 2 - KS-1139 Part B. Both counters advance by assignment form
+# `VAR=$((VAR + 1))`. Untouched script: 0 hits -> red. Fixed script: exactly 2.
+# Bracket expressions on purpose - no backslashes in the pattern source.
+# ---------------------------------------------------------------------------
+asg_count="$(grep -cE '^[[:space:]]*(PASS_COUNT|FAIL_COUNT)=[$][(][(](PASS_COUNT|FAIL_COUNT) [+] 1[)][)][[:space:]]*$' "$SUBJ" || true)"
+if [ "$asg_count" = 2 ]; then
+  ok "both counters advance by assignment ($asg_count matches)"
+else
+  bad "both counters advance by assignment" "count=$asg_count (expected 2)"
+fi
+
+# ---------------------------------------------------------------------------
+# CONTROL CELL 3 - The subject parses cleanly under any bash version we run this
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
+  printf '  INCOMPLETE - %d of %d cells ran\n' "$((pass + fail))" "$TOTAL_CELLS"
+  exit 1
+fi
+[ "$fail" -eq 0 ] || exit 1
+exit 0
```
