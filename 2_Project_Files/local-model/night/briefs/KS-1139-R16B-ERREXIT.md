# KS-1139-B R16B-ERREXIT - re-brief at develop 8c2f7b3fd of READY_KS-1139-B_ornith35b-q4_BASHPATCH-NEWFILE-SYNTH-PASS-7of7_2026-09-16.diff.md (written 2026-09-22 09:45:48 AEST by Wednesday's feed8 drafter; the product hunk and the new suite are the old READY's PASS 7/7 output re-anchored at the tip, every '+' line and every suite line made ASCII: the cell glyph is the word RED, em-dashes are hyphens; every context and '-' line asserted byte-exact at the tip at the line numbers below)

File: `Blockchain/Dev/scripts/__tests__/validate_lint_errexit.test.sh`
Tip: 8c2f7b3fd4fde915b2a24542bc32259b24e092a0
Runner: bash (the shell suite runner - `bash <file>` under /bin/bash 3.2; the checker runs the suite alone at the tip, then again after the script hunk)

## What is wrong (one paragraph)
`systemTest/schemathesis/validate-lint.sh` runs under `set -e` (:6) and its `run_check()` counts with a bare arithmetic command —
`((PASS_COUNT++))` at :33 and `((FAIL_COUNT++))` at :38, each in the BODY of an `if`/`else` (not the condition), so errexit applies:
the FIRST increment of each counter (at 0) exits 1 and bash ≥ 4.1 `set -e` exits the script on it, silently; bash 3.2 (macOS) does
not, so the script passes here. **This task: the two sites become the assignment form `X=$((X + 1))` (exit status 0 at every value,
identical effect — the shape Part A used in `sync-secrets.sh` and #977 in `docker-build.sh`), plus one new shell suite pinning the
construct's ABSENCE with the census regex and its positive control (the reference's CELL 4 shape).** NOT in this task: any other line
of the script, Part A's file, `check-script-portability.sh`.

## The exact change - 2 hunk(s) in `systemTest/schemathesis/validate-lint.sh` (2 '-' line(s), 2 '+' line(s), one '+' group per hunk)
Copy the block below BYTE FOR BYTE as the first file of your diff: the two file-header lines, each `@@` header, every context line (a leading space, copied from `files[product_file]`), every `-` line and every `+` line, in this order. Do not add, drop, re-indent or reword a line; do not add a trailing comment; do not mark a context line as `+`. Every `+` line is ASCII - a double quote or a backslash on a `+` line is copied as written, never escaped.
```
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
```

## Where (parsed into the checklist - every **must change** line must appear as a `-` line in your diff)
* `:33` - **must change**: `        ((PASS_COUNT++))`
* `:38` - **must change**: `        ((FAIL_COUNT++))`
* `:31` - (correct) `    if eval "$cmd" > /dev/null 2>&1; then` - stays
* `:32` - (correct) `        echo -e "${GREEN}✓ PASS${NC}"` - stays

## The test - CREATE THE NEW FILE `Blockchain/Dev/scripts/__tests__/validate_lint_errexit.test.sh`

File: `Blockchain/Dev/scripts/__tests__/validate_lint_errexit.test.sh`

bash 3.2. It lives under `Blockchain/Dev/scripts/__tests__/` beside the reference `Blockchain/Dev/scripts/__tests__/docker_build_empty_table.test.sh` (full content in `files[...]`) and locates the subject from `${BASH_SOURCE[0]}` exactly as the block below does. It creates nothing outside `mktemp -d` and never edits the repo's real files.

**Reproduce the file below EXACTLY as written - every line, in order (81 lines).** Do not invent a helper, do not rename a variable, do not reword a message, do not add or drop a cell. Every value a cell reads is assigned above the first cell. **Your diff for this file is a NEW-FILE diff: `--- /dev/null`, `+++ b/Blockchain/Dev/scripts/__tests__/validate_lint_errexit.test.sh`, ONE hunk header `@@ -0,0 +1,81 @@`, then EVERY line with a leading `+` (a blank line is a lone `+`) - no context lines, no `-` lines: you are not diffing the reference.**

```
#!/usr/bin/env bash
# =============================================================================
# TESTS for systemTest/schemathesis/validate-lint.sh - KS-1139 Part B
# The two bare arithmetic-command post-increments at :33 and :38. Under bash >= 4.1
# `set -e`, each fires with status 1 when its counter is 0 and kills the script
# silently on macOS it does not. This suite pins their ABSENCE statically plus a
# positive control that both trees share.
#
# Usage: bash Blockchain/Dev/scripts/__tests__/validate_lint_errexit.test.sh
# =============================================================================
set -uo pipefail
TOTAL_CELLS=3

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$HERE/../../../.." && pwd)"
if [ "${VALIDATE_LINT_SH+set}" = set ] && [ -z "$VALIDATE_LINT_SH" ]; then
  echo "FATAL: VALIDATE_LINT_SH is set but EMPTY - refusing to silently grade the shipped script." >&2
  exit 2
fi
SUBJ="${VALIDATE_LINT_SH-$REPO_ROOT/systemTest/schemathesis/validate-lint.sh}"
[ -f "$SUBJ" ] || { echo "FATAL: validate-lint.sh not found at $SUBJ" >&2; exit 2; }
[ -r "$SUBJ" ] || { echo "FATAL: VALIDATE_LINT_SH is not readable at $SUBJ" >&2; exit 2; }
printf 'SUBJECT %s\n        sha256 %s\n\n' "$SUBJ" "$(shasum -a 256 "$SUBJ" | cut -d" " -f1)"

pass=0; fail=0
ok()  { printf '  ok   %s\n' "$1"; pass=$((pass + 1)); }
bad() { printf '  FAIL %s\n     %s\n' "$1" "$2"; fail=$((fail + 1)); }

# ---------------------------------------------------------------------------
# CELL 1 - KS-1139 Part B. The subject has NO bare arithmetic-command
# post-increment/decrement (`((X++))` / `((X--))` on a line of its own). Such a
# command exits 1 when its expression evaluates to 0 (post-increment yields the
# OLD value, so `((PASS_COUNT++))` at PASS_COUNT=0 fails) and bash >= 4.1
# `set -e` exits on it. bash 3.2 (macOS) does not. Static pin with a positive
# control inside the cell proving the grep can fire. `[[:space:]]`, not `\s`: BSD grep.
# ---------------------------------------------------------------------------
ARITH_RE='^[[:space:]]*\(\([A-Za-z_][A-Za-z_0-9]*(\+\+|--)\)\)[[:space:]]*$'
arith_control="$(printf '  ((X++))\n' | grep -cE "$ARITH_RE" || true)"
arith_hits="$(grep -nE "$ARITH_RE" "$SUBJ" || true)"
arith_count="$(printf '%s' "$arith_hits" | grep -c . || true)"
if [ "$arith_control" != 1 ]; then
  bad "validate-lint.sh has NO bare arithmetic-command post-increment/decrement" \
      "instrument cannot fire: the positive control read $arith_control (expected 1) - the cell is not scoring the subject"
elif [ "$arith_count" -eq 0 ]; then
  ok "validate-lint.sh has NO bare arithmetic-command post-increment/decrement - ((X++)) exits 1 at 0 and bash >= 4.1 set -e dies on it (control fires: $arith_control)"
else
  bad "validate-lint.sh has NO bare arithmetic-command post-increment/decrement" \
      "count=$arith_count (control=$arith_control): $(printf '%s' "$arith_hits" | sed 's/^\([0-9]*\):[[:space:]]*/:\1 /' | tr '\n' ' ')"
fi

# ---------------------------------------------------------------------------
# CELL 2 - KS-1139 Part B. Both counters advance by assignment form
# `VAR=$((VAR + 1))`. Untouched script: 0 hits -> red. Fixed script: exactly 2.
# Bracket expressions on purpose - no backslashes in the pattern source.
# ---------------------------------------------------------------------------
asg_count="$(grep -cE '^[[:space:]]*(PASS_COUNT|FAIL_COUNT)=[$][(][(](PASS_COUNT|FAIL_COUNT) [+] 1[)][)][[:space:]]*$' "$SUBJ" || true)"
if [ "$asg_count" = 2 ]; then
  ok "both counters advance by assignment ($asg_count matches)"
else
  bad "both counters advance by assignment" "count=$asg_count (expected 2)"
fi

# ---------------------------------------------------------------------------
# CONTROL CELL 3 - The subject parses cleanly under any bash version we run this
# suite against. Green on both trees; without it a broken edit could pass cells 1
# and 2 while producing an unrunnable script.
# ---------------------------------------------------------------------------
if bash -n "$SUBJ"; then
  ok "validate-lint.sh parses (bash -n)"
else
  bad "validate-lint.sh parses (bash -n)" "bash -n exited non-zero on $SUBJ"
fi

printf '\n  %d passed, %d failed (of %d cells)\n' "$pass" "$fail" "$TOTAL_CELLS"
# A cell that never ran is not a pass: the ratio must add up.
if [ "$((pass + fail))" -ne "$TOTAL_CELLS" ]; then
  printf '  INCOMPLETE - %d of %d cells ran\n' "$((pass + fail))" "$TOTAL_CELLS"
  exit 1
fi
[ "$fail" -eq 0 ] || exit 1
exit 0
```

Cells, in file order (a RED cell FAILS at the untouched tip by assertion and PASSES after the script hunk; a CONTROL cell passes on both trees):
- `# CELL 1 - KS-1139 Part B. The subject has NO bare arithmetic-command`
- `ok "validate-lint.sh has NO bare arithmetic-command post-increment/decrement - ((X++)) exits 1 at 0 and bash >= 4.1 set -e dies on it (control fires: `
- `# CELL 2 - KS-1139 Part B. Both counters advance by assignment form`
- `ok "both counters advance by assignment ($asg_count matches)"`
- `# CONTROL CELL 3 - The subject parses cleanly under any bash version we run this`
- `ok "validate-lint.sh parses (bash -n)"`

## Output
Exactly ONE ```diff block with TWO files: `--- a/systemTest/schemathesis/validate-lint.sh` / `+++ b/systemTest/schemathesis/validate-lint.sh` (2 hunk(s), copied from `## The exact change`), then `--- /dev/null` / `+++ b/Blockchain/Dev/scripts/__tests__/validate_lint_errexit.test.sh` (one hunk, `@@ -0,0 +1,81 @@`, every line a `+`). No prose before or after the block.

## Premises (measured at develop 8c2f7b3fd4fde915b2a24542bc32259b24e092a0 by the feed8 drafter, scratchpad `--shared --no-checkout` clone, 2026-09-22 09:45:48 AEST)
- `systemTest/schemathesis/validate-lint.sh` at the tip carries every context and `-` line of the hunk(s) above BYTE FOR BYTE at the line numbers in `## Where` (asserted by rebrief.py against `git show 8c2f7b3fd:systemTest/schemathesis/validate-lint.sh`); the rebuilt product section applies STRICT (`git apply --check -p1` rc 0 in the clone).
- The new suite `Blockchain/Dev/scripts/__tests__/validate_lint_errexit.test.sh` is ABSENT at the tip (`git cat-file -e` rc 1). The reference suite `Blockchain/Dev/scripts/__tests__/docker_build_empty_table.test.sh` is present.
- Every `+` line of the product hunk(s) and every line of the suite is ASCII (non-ASCII 0, asserted); the FEED 8 ruling (Wednesday, 2026-09-22 09:3x) WAIVES the `"` 0 / `\` 0 rule for bash_patch - the guard is the checker's B3b (every brief `+` line present in the script hunk, whitespace-stripped) and B4/B5 (RED at the tip, GREEN after).
- Golden precheck through the real `tasks/bash_patch/checker.sh` in the clone: see `runs/2026-09-22_feed8-drafter-precheck/ERREXIT/checker.log` (the verdict is quoted on the queue line, never here by hand).
- Ticket KS-1139 on the Secuura board at 2026-09-22 09:45:48 AEST: Backlog, not archived (`board_states.log`). The product file is on neither 18th seat's GROUPING list (Seat B: shared/anchoring/auth/originate; Seat C: api-gateway).
