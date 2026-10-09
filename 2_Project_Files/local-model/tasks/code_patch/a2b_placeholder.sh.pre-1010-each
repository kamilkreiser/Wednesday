#!/bin/bash
# a2b_placeholder.sh <section.diff> — the A2b PLACEHOLDER predicate, factored out of checker.sh on 2026-09-16 00:3x so
# it can be ARMED on real artefacts (KS-887 r1+retry: a modify-in-place hunk with no new cell was refused twice).
# A NEW test file (`--- /dev/null`) is a stub when it adds no `it(`/`test(`. An EXISTING file (`--- a/…`) is a stub
# only when it REMOVES more cells than it adds — rewriting assertions inside a cell the tip already has is legitimate.
# Prints a one-line reason and exits 1 when it is a placeholder; prints nothing and exits 0 otherwise. bash 3.2.
set -u
pf="${1:-}"; [ -n "$pf" ] && [ -f "$pf" ] || { echo "usage: a2b_placeholder.sh <section.diff>" >&2; exit 2; }
nplus="$(/usr/bin/grep -c -E "^\+\s*(it|test)\(" "$pf")"; nminus="$(/usr/bin/grep -c -E "^-\s*(it|test)\(" "$pf")"
if /usr/bin/grep -q -E '^--- (a/|"a/)' "$pf"; then
  if [ "$nminus" -gt "$nplus" ]; then echo "existing file: $nminus cell(s) removed, $nplus added"; exit 1; fi
else
  if [ "$nplus" -eq 0 ]; then echo "$(/usr/bin/grep -c '^+' "$pf") lines, 0 cells"; exit 1; fi
fi
exit 0
