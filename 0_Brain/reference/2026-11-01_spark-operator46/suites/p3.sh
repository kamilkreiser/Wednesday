#!/usr/bin/env bash
# =============================================================================
# TESTS for systemTest/__tests__/manifest_readers_agree.test.sh - a driver that answers nothing must
# say why (KS-1884).
# =============================================================================
# The four driver functions end `2>/dev/null | tail -1`, so a tool that fails to start leaves an empty
# answer and the FAIL line shows only `writer=''`: the reason is thrown away. The fix keeps each
# driver's stderr in a file and prints it under a FAIL line.
# Real bash, env and tail; `npx` and `python3` are STUBS on a private PATH (they print their noise to
# stderr and nothing to stdout), so no tsx, no Python and no stack is needed. Nothing outside the temp
# dir is written.
# Usage: bash systemTest/__tests__/manifest_readers_agree_stderr.test.sh
# =============================================================================

set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SUBJ="${MANIFEST_READERS_AGREE_SH:-$HERE/manifest_readers_agree.test.sh}"
SUPPORT="$HERE/support/slot-expect.sh"
STACK_ENV="$HERE/../../Blockchain/Dev/scripts/stack_env.sh"
for _f in "$SUBJ" "$SUPPORT" "$STACK_ENV"; do
  [[ -r "$_f" ]] || { echo "FATAL: not readable: $_f" >&2; exit 2; }
done
WORK="$(mktemp -d "${TMPDIR:-/tmp}/readers-stderr.XXXXXX")"
trap 'rm -rf "$WORK"' EXIT
PASS=0
FAIL=0
REAL_GREP="$(command -v grep)"

run_case() {   # $1 = case name, $2 = what the stubs print on stdout (may be empty) -> prints the subject's exit code
  local f="$WORK/$1"
  mkdir -p "$f/systemTest/__tests__/support" "$f/systemTest/playwright" "$f/systemTest/performance" \
           "$f/systemTest/schemathesis/tests" "$f/Blockchain/Dev/scripts" "$f/bin"
  cp "$SUBJ" "$f/systemTest/__tests__/manifest_readers_agree.test.sh"
  cp "$SUPPORT" "$f/systemTest/__tests__/support/slot-expect.sh"
  cp "$STACK_ENV" "$f/Blockchain/Dev/scripts/stack_env.sh"
  printf '#!/bin/sh\necho "STUB-NPX-NOISE tsx failed to start" >&2\n[ -n "%s" ] && echo "%s"\nexit 1\n' "$2" "$2" > "$f/bin/npx"
  printf '#!/bin/sh\necho "STUB-PY-NOISE python failed to start" >&2\n[ -n "%s" ] && echo "%s"\nexit 1\n' "$2" "$2" > "$f/bin/python3"
  chmod +x "$f/bin/npx" "$f/bin/python3"
  ( cd "$f" && PATH="$f/bin:$PATH" bash systemTest/__tests__/manifest_readers_agree.test.sh ) >"$WORK/$1.out" 2>&1
  echo $?
}

RC_SILENT="$(run_case silent '')"
RC_ERROR="$(run_case error 'ERROR')"

# CELL 1 (RED at the tip) - the npx stub's stderr appears in the output of a failing run.
if "$REAL_GREP" -qF 'STUB-NPX-NOISE' "$WORK/silent.out"; then
  echo "PASS: a driver's stderr is printed on a FAIL (npx)"; PASS=$((PASS+1))
else
  echo "FAIL: the npx stub's stderr is not in the output of a failing run (rc=$RC_SILENT)"; FAIL=$((FAIL+1))
fi

# CELL 2 (RED at the tip) - the python3 stub's stderr (the schemathesis driver) appears too.
if "$REAL_GREP" -qF 'STUB-PY-NOISE' "$WORK/silent.out"; then
  echo "PASS: a driver's stderr is printed on a FAIL (python3)"; PASS=$((PASS+1))
else
  echo "FAIL: the python3 stub's stderr is not in the output of a failing run (rc=$RC_SILENT)"; FAIL=$((FAIL+1))
fi

# CELL 3 (GREEN CONTROL, tip AND after) - drivers that answer nothing still fail the suite and still say FAIL.
if [[ "$RC_SILENT" != "0" ]] && "$REAL_GREP" -q '^FAIL ' "$WORK/silent.out"; then
  echo "PASS: CONTROL silent drivers still fail the suite with FAIL lines"; PASS=$((PASS+1))
else
  echo "FAIL: CONTROL silent drivers: rc=$RC_SILENT"; FAIL=$((FAIL+1))
fi

# CELL 4 (GREEN CONTROL, tip AND after) - stderr is printed only for a FAIL: no passing case carries it.
if "$REAL_GREP" -q '^ok ' "$WORK/error.out" && ! "$REAL_GREP" '^ok ' "$WORK/error.out" | "$REAL_GREP" -q 'STUB-'; then
  echo "PASS: CONTROL an ok line never carries driver stderr"; PASS=$((PASS+1))
else
  echo "FAIL: CONTROL ok lines: rc=$RC_ERROR, ok lines=$("$REAL_GREP" -c '^ok ' "$WORK/error.out")"; FAIL=$((FAIL+1))
fi

echo ""
echo "Results: $PASS passed, $FAIL failed"
[[ "$FAIL" -eq 0 ]]
