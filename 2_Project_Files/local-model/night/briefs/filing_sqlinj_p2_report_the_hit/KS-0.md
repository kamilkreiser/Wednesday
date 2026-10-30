# KS-0 check-no-sql-injection.sh: the failure headline expands two unset variables, so under set -u a real hit aborts the script before the hit list is printed (found by operator 24, no ticket; RUNG 2, bash_patch: one product line spelled, plus a new stub-PATH suite given whole)

DRAFT by Spark operator 24 for Wednesday, 2026-10-30 AEDT. Secuura (Blockchain/Dev/scripts) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: found by operator 24 while testing the exclude-dir filing item (no Linear ticket exists; the raise seat files one on the board account or links the filing). `check-no-sql-injection.sh:35` echoes `::error::SQL injection risk - $queryRawUnsafe / $executeRawUnsafe used ...` inside double quotes and the script runs under `set -euo pipefail`, so the shell aborts with `queryRawUnsafe: unbound variable` (exit 1) before the hit list and the Fix hints are printed: the gate fails but names nothing. The sibling lines 39 and 41 already escape their dollar signs.

File: `Blockchain/Dev/scripts/check-no-sql-injection.sh`  (product, modified in place: 1 hunk)
Test file: `Blockchain/Dev/scripts/__tests__/check_no_sql_injection_reports_the_hit.test.sh`  (NEW, 80 lines)
Tip: `40c06084919d5aff132e82693cd60d513cb40ba7` (develop, read with `git show` in a clone at exactly this sha on 2026-10-30; the script is 51 lines)
Runner: `bash` (bash 3.2, `bash Blockchain/Dev/scripts/__tests__/check_no_sql_injection_reports_the_hit.test.sh` from the repo root; grep is a stub on a private PATH)
Tier: `bash_patch`
Rung: **2** (one product line given byte-exact; the test is copied whole)

## The mode - read this twice

CODE+TEST. Your diff touches EXACTLY 2 files, in this order:
1. `Blockchain/Dev/scripts/check-no-sql-injection.sh` - modified in place, EXACTLY the 1 hunk under "The exact change", byte for byte.
2. `Blockchain/Dev/scripts/__tests__/check_no_sql_injection_reports_the_hit.test.sh` - a NEW file: `--- /dev/null` then `+++ b/Blockchain/Dev/scripts/__tests__/check_no_sql_injection_reports_the_hit.test.sh`, ONE hunk `@@ -0,0 +1,80 @@`, every line `+`.

You never touch any other file. The sibling `check_no_latest_tags.test.sh` is shape reference only - do NOT touch it.

## What is wrong (one paragraph)

At `check-no-sql-injection.sh:35` the headline is `echo "::error::SQL injection risk — $queryRawUnsafe / $executeRawUnsafe used with template-literal interpolation:"`. Both `$queryRawUnsafe` and `$executeRawUnsafe` are meant as literal text but are unset shell variables, and `set -u` makes the expansion fatal. The fix is to escape the two dollar signs with a backslash, exactly as lines 39 and 41 do: `\$queryRawUnsafe / \$executeRawUnsafe`.

## Where

- `:35` - **must change**: the `echo "::error::..."` headline - the two dollar signs before `queryRawUnsafe` and `executeRawUnsafe` each gain a backslash.
- `:28` (the scan grep) and every other line - (correct) stays unchanged; `:36`-`:41` are context.

## The exact change

1 hunk. One line replaced by one.

```diff
@@ -34,5 +34,5 @@
 if [ -n "$hits" ]; then
-  echo "::error::SQL injection risk — $queryRawUnsafe / $executeRawUnsafe used with template-literal interpolation:"
+  echo "::error::SQL injection risk — \$queryRawUnsafe / \$executeRawUnsafe used with template-literal interpolation:"
   echo "$hits" | sed 's/^/  /'
   echo ""
   echo "Fix: pass the SQL as a plain string with positional params:"
```

**Do NOT touch** any other line of the script.

## The test

File: `Blockchain/Dev/scripts/__tests__/check_no_sql_injection_reports_the_hit.test.sh`
The shape is the sibling suite `Blockchain/Dev/scripts/__tests__/check_no_latest_tags.test.sh` (a fixture root with `scripts/<subject>`, the subject resolving its own root) with a stub `grep` on a private `PATH`.

Emit this text as the new-file hunk `@@ -0,0 +1,80 @@`, every line prefixed `+`, nothing added or dropped (blank lines in it are `+` lines with nothing after the `+`):

```bash
#!/usr/bin/env bash
# =============================================================================
# TESTS for Blockchain/Dev/scripts/check-no-sql-injection.sh - a real hit must be
# REPORTED, not swallowed by `set -u`.
# =============================================================================
# The failure branch echoes "::error::SQL injection risk - $queryRawUnsafe / $executeRawUnsafe ..."
# inside double quotes, so under `set -u` the shell expands two unset variables and
# aborts with "queryRawUnsafe: unbound variable" BEFORE the hit list is printed. The
# gate still fails (exit 1) but names nothing.
# grep is a stub on a private PATH: it answers the scan call with the lines in
# SHIM_HITS and hands the script's own `grep -v` filter call to the real grep. No tree
# is ever walked.
# Usage: bash Blockchain/Dev/scripts/__tests__/check_no_sql_injection_reports_the_hit.test.sh
# =============================================================================

set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SUBJ="${CHECK_NO_SQL_INJECTION_SH:-$HERE/../check-no-sql-injection.sh}"
[[ -r "$SUBJ" ]] || { echo "FATAL: check-no-sql-injection.sh not readable at $SUBJ" >&2; exit 2; }
WORK="$(mktemp -d "${TMPDIR:-/tmp}/sqlhit.XXXXXX")"
trap 'rm -rf "$WORK"' EXIT
PASS=0
FAIL=0
REAL_GREP="$(command -v grep)"

mkdir -p "$WORK/bin" "$WORK/root/scripts" "$WORK/root/services" "$WORK/root/packages"
cp "$SUBJ" "$WORK/root/scripts/check-no-sql-injection.sh"
cat > "$WORK/bin/grep" <<'STUB'
#!/bin/sh
for a in "$@"; do
  [ "$a" = "-v" ] && exec "$REAL_GREP" "$@"
done
[ -n "${SHIM_HITS:-}" ] && printf '%s\n' "$SHIM_HITS"
exit 0
STUB
chmod +x "$WORK/bin/grep"

run_case() {   # $1 = name, $2 = the lines the scan call answers with -> prints rc; output in $WORK/$1.out
  (
    export PATH="$WORK/bin:/usr/bin:/bin" REAL_GREP SHIM_HITS="$2"
    cd "$WORK/root" && bash scripts/check-no-sql-injection.sh
  ) >"$WORK/$1.out" 2>&1
  echo $?
}

RC_CLEAN="$(run_case clean "")"
RC_HIT="$(run_case hit 'services/x/src/repo.ts:3:  db.$queryRawUnsafe(`SELECT 1 WHERE id = ${id}`);')"
RC_DEP="$(run_case dep 'services/x/node_modules/y/index.js:9:  db.$queryRawUnsafe(`SELECT ${id}`);')"

# CELL 1 (RED at the tip) - a hit prints the error headline with both API names.
if "$REAL_GREP" -qF 'SQL injection risk' "$WORK/hit.out" && "$REAL_GREP" -qF '$queryRawUnsafe / $executeRawUnsafe' "$WORK/hit.out"; then
  echo "PASS: a hit prints the error headline naming both Unsafe calls"; PASS=$((PASS+1))
else
  echo "FAIL: the hit output has no error headline naming both Unsafe calls"; FAIL=$((FAIL+1))
fi

# CELL 2 (RED at the tip) - a hit prints the offending line, indented two spaces.
if "$REAL_GREP" -qF '  services/x/src/repo.ts:3:' "$WORK/hit.out"; then
  echo "PASS: a hit prints the offending file and line"; PASS=$((PASS+1))
else
  echo "FAIL: the offending file and line are not printed"; FAIL=$((FAIL+1))
fi

# CELL 3 (GREEN CONTROL, tip AND after) - exit codes: a hit exits 1, a clean scan exits 0 and says OK.
if [[ "$RC_HIT" == "1" && "$RC_CLEAN" == "0" ]] && "$REAL_GREP" -qF 'no string-concatenated SQL found' "$WORK/clean.out"; then
  echo "PASS: CONTROL a hit exits 1 and a clean scan exits 0 with the OK line"; PASS=$((PASS+1))
else
  echo "FAIL: CONTROL exit codes: hit=$RC_HIT clean=$RC_CLEAN"; FAIL=$((FAIL+1))
fi

# CELL 4 (GREEN CONTROL, tip AND after) - a hit under node_modules is still dropped by the script's own filter.
if [[ "$RC_DEP" == "0" ]] && "$REAL_GREP" -qF 'no string-concatenated SQL found' "$WORK/dep.out"; then
  echo "PASS: CONTROL a hit under node_modules is still filtered out"; PASS=$((PASS+1))
else
  echo "FAIL: CONTROL node_modules hit: rc=$RC_DEP $(head -2 "$WORK/dep.out" | tr '\n' ' ')"; FAIL=$((FAIL+1))
fi

echo "check_no_sql_injection_reports_the_hit: $PASS passed, $FAIL failed"
[[ "$FAIL" -eq 0 && "$PASS" -eq 4 ]]
```

## Red cells
- a hit prints the error headline naming both Unsafe calls
- a hit prints the offending file and line

## Cells and controls

- RED CELL 1 `a hit prints the error headline naming both Unsafe calls` - red at the tip (the script aborts at the headline with an unbound variable), green with the product hunk.
- RED CELL 2 `a hit prints the offending file and line` - red at the tip for the same reason.
- green CELL 3 `CONTROL a hit exits 1 and a clean scan exits 0 with the OK line` - the exit codes are untouched.
- green CELL 4 `CONTROL a hit under node_modules is still filtered out` - the script's own `grep -v` filter stays.

## The failing case (the "tamper")

Product fix, no tamper. Measured in a scratch tree (the tip's script written out with `git show`, the suite pointed at it with `CHECK_NO_SQL_INJECTION_SH=`), bash 3.2: the suite at the tip is `2 passed, 2 failed` (the two FAILs are CELL 1 and CELL 2) and with the edited script `4 passed, 0 failed`.

## Premises (each one measured, with where)

- `Blockchain/Dev/scripts/check-no-sql-injection.sh` at `40c06084919d`: the script runs under `set -euo pipefail`; line 35 is the headline quoted above; lines 39 and 41 escape their dollar signs (`\$executeRawUnsafe`, `\$queryRaw`).
- Measured in the scratch tree: with a planted hit the tip prints only `scripts/check-no-sql-injection.sh: line 35: queryRawUnsafe: unbound variable` and exits 1.
- The suite resolves the subject through `CHECK_NO_SQL_INJECTION_SH` (default: the script beside `__tests__/`); nothing in it touches the real tree. A sibling brief (filing_sqlinj_p1) edits line 28 of the same script: disjoint hunks.

## UNMEASURED - stated rather than glossed

- The drafter ran the suite by hand against the tip and the edited script (results above) but did NOT run `round.sh --dry-run`/`--control` before this text was written; that run is the proof.
- Whether the script's stdout is read by anything that parses it is not measured.

## Scope

**Refs the filing list item (no ticket); never a close-word.** The headline escaping at `:35` only; the scan at `:28` is the sibling brief's.

## Output

Exactly ONE fenced ```diff block, nothing outside it:
1. the product file (`--- a/Blockchain/Dev/scripts/check-no-sql-injection.sh` / `+++ b/Blockchain/Dev/scripts/check-no-sql-injection.sh`) with the single hunk given under "The exact change";
2. the new test file (`--- /dev/null` / `+++ b/Blockchain/Dev/scripts/__tests__/check_no_sql_injection_reports_the_hit.test.sh`, `@@ -0,0 +1,80 @@`), every line `+`.
Every `+` line on its own physical line. Every context line keeps its leading space.
