#!/bin/bash
# Arms for tuesday/tools/addendum_name_check.sh. Each arm states its expected rc first.
# Real refusals of 25-26 Oct are the fire arms; today's real clean names are the quiet arms.
set -u
SELF_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
T="$SELF_DIR/../tools/addendum_name_check.sh"
pass=0; fail=0
arm() { # expected_rc name [env]
  local exp="$1" name="$2"; shift 2
  env "$@" bash "$T" "$name" >/dev/null 2>&1; local rc=$?
  if [ "$rc" = "$exp" ]; then pass=$((pass+1)); echo "PASS rc=$rc  $name"; else fail=$((fail+1)); echo "FAIL rc=$rc (want $exp)  $name"; fi
}
# fire: the B742 and B650 names are the refused originals as the ledger rows quote them (both since renamed on disk);
# the B639 name is CONSTRUCTED in the shape of its 'resume' instance (its original name is not recorded anywhere)
arm 3 2026-10-26_B742_ADDENDUM-2_lost-cells-accepted-ruling.md
arm 3 2026-10-25_B650_ADDENDUM-1_b650-1-linear-cost-accepted.md
arm 3 2026-10-25_B639_ADDENDUM-1_resume-after-stop.md
# fire: a full path, and an upper-case word
arm 3 /Volumes/x/briefs/2026-10-26_B999_ADDENDUM-1_DEPLOY-window_answer.md
# quiet: real clean names from 26 Oct, and a word that only CONTAINS a verb (pushback / restart are not words on the list)
arm 0 2026-10-26_B742_ADDENDUM-2_lost-cells-ruling.md
arm 0 2026-10-26_B752_ADDENDUM-1_docs-sentence-ruling.md
arm 0 2026-10-26_B753_ADDENDUM-1_nonascii-line-ruling.md
arm 0 2026-10-26_B999_ADDENDUM-1_pushback-restart_answer.md
# fail-closed: the regex cannot be found -> rc 2
TMPC="$(mktemp)"; echo '#!/bin/bash' > "$TMPC"
arm 2 2026-10-26_B999_ADDENDUM-1_any_ruling.md ADDENDUM_COCKPIT="$TMPC"
rm -f "$TMPC"
# body clock (2026-10-30 w=2): an existing file whose body holds an HH:Mx placeholder -> rc 4; a real clock, a ratio -> 0
TMPD="$(mktemp -d)"
printf 'Tuesday read it read-only after 18:2x AEDT\n' > "$TMPD/2026-10-30_B999_ADDENDUM-1_clock-red_answer.md"
printf 'finished at 18:23 AEDT; contrast 3:1; B959\n' > "$TMPD/2026-10-30_B999_ADDENDUM-1_clock-green_answer.md"
arm 4 "$TMPD/2026-10-30_B999_ADDENDUM-1_clock-red_answer.md"
arm 0 "$TMPD/2026-10-30_B999_ADDENDUM-1_clock-green_answer.md"
mv "$TMPD" "$TMPD.done" 2>/dev/null
# usage
env bash "$T" >/dev/null 2>&1; rc=$?; if [ "$rc" = 2 ]; then pass=$((pass+1)); echo "PASS rc=2  (no argument)"; else fail=$((fail+1)); echo "FAIL rc=$rc (want 2)  (no argument)"; fi
echo "arms: $pass pass, $fail fail"
[ "$fail" = 0 ]
