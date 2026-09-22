#!/bin/bash
# Arms for tools/absence_claim_check.sh. Each prints PASS/FAIL; exit 1 if any fail.
C=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/absence_claim_check.sh; F=0
arm(){ # name, text, expect_flag(yes/no)
  err="$(printf '%s' "$2" | bash "$C" 2>&1 >/dev/null)"; rc=$?
  flagged=no; [ -n "$err" ] && flagged=yes
  if [ "$rc" -eq 0 ] && [ "$flagged" = "$3" ]; then echo "PASS  $1  (flag=$flagged rc=$rc)"; else echo "FAIL  $1  (flag=$flagged want=$3 rc=$rc)"; F=1; fi; }
arm "A1 the real #922 claim flags"          "It wasn't waiting on a review, it was waiting on nothing at all." yes
arm "A2 the real TND claim flags"           "Four fixes are merged but not on kintsugi yet."                  yes
arm "A3 a harmless negative flags (advisory)" "Never mind, carry on."                                         yes
arm "A4 a positive claim does NOT flag"      "The gate passed and the pull request merged at 207716440."     no
arm "A5 capitalisation still flags"          "There Is No review on it."                                     yes
arm "A6 empty input exits 0 unflagged"       ""                                                              no
exit $F
