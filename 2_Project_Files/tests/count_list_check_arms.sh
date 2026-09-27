#!/bin/bash
# Arms for tools/count_list_check.sh. Each prints PASS/FAIL, then a total; exit 1 if any fail.
# (Resolved from this file's own folder, not a drive path, so the arms run on the laptop tree and the DevMASTER tree alike.)
C="$(cd -P "$(dirname "${BASH_SOURCE[0]}")/../tools" && pwd)/count_list_check.sh"; F=0; P=0; N=0
arm(){ # name, text, expect_flag(yes/no)
  err="$(printf '%s' "$2" | bash "$C" 2>&1 >/dev/null)"; rc=$?
  flagged=no; [ -n "$err" ] && flagged=yes; N=$((N+1))
  if [ "$rc" -eq 0 ] && [ "$flagged" = "$3" ]; then echo "PASS  $1  (flag=$flagged rc=$rc)"; P=$((P+1)); else echo "FAIL  $1  (flag=$flagged want=$3 rc=$rc)"; F=1; fi
  [ -n "$err" ] && echo "      $err"; }
arm "a the real 2026-09-27 card (five vs six ids) flags"   "Five tickets depend on this answer (HPSM-12/19/25/32/35/41)."  yes
arm "b 'Four High findings' over three flags"             "Four High findings: HPSMPOC-73, HPSMPOC-74, HPSMPOC-75."        yes
arm "c a correct pair is silent"                          "Three findings: A, B and C."                                    no
arm "d a count with no list is silent"                    "Five tickets closed today."                                     no
arm "e a number that is not a count is silent"            "PR #49 merged at 17:20; main CI green."                          no
# (f) the exit code is 0 even when it flags — checked directly, not through arm(), so a flag cannot mask it.
N=$((N+1)); out="$(printf '%s' "Five tickets depend on this answer (HPSM-12/19/25/32/35/41)." | bash "$C" 2>&1)"; rc=$?
if [ "$rc" -eq 0 ] && [ -n "$out" ]; then echo "PASS  f exit code is 0 while flagging  (rc=$rc, flagged)"; P=$((P+1)); else echo "FAIL  f exit code is 0 while flagging  (rc=$rc, out='$out')"; F=1; fi
arm "g Oxford comma + nested aside counts right (silent)"  "Three fixes: A (merged), B, and C."                           no
arm "h id/PR pairs are two items, not four (silent)"       "Two finished fixes (#730/KS-570, #726/KS-667)."               no
arm "i digit count mismatch flags"                         "2 blockers (Peter's review / the CI flake / DNS)."            yes
arm "j empty input exits 0 unflagged"                      ""                                                            no
echo "TOTAL: $P/$N passed"
exit $F
