#!/bin/bash
# addendum_name_check.sh <file name or path> — refuse a brief/addendum FILE NAME that `cockpit.sh say` would refuse to
# carry in an un-mailed pointer tap.
#
# WHY (ledger _ledger_laptop_datasec.md, REGRESSION w=4 on 2026-10-26: B639 'resume', B650 'accepted', B742
# 'accepted'): a pointer tap quotes the addendum's file name, and cockpit.sh:334 refuses any un-mailed tap matching
# its authorisation-verb list. Each time the word came from the RULING being relayed (an option label), so the file
# was named after the decision's verb. The rule: an addendum name ends in _ruling / _answer / _correction and carries
# only NOUNS from the subject. This tool is the check in the path: run it BEFORE writing the file.
#
# The regex is READ FROM cockpit.sh at run time (the line holding `grep -qiE '(^|[^a-z])(proceed`), never copied, so
# the two cannot drift. If that line cannot be found, this REFUSES (rc 2): a check whose pattern is missing is not a
# check (learnings/2026-08-07_a-check-that-cannot-fail).
#
# rc 0 = clean · rc 3 = a refused word is in the name (printed) · rc 2 = usage error or regex not found.
# Arms: tests/addendum_name_check_arms.sh
set -u
[ $# -eq 1 ] || { echo "usage: addendum_name_check.sh <file name or path>" >&2; exit 2; }
SELF_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COCKPIT="${ADDENDUM_COCKPIT:-$SELF_DIR/../../fleet/cockpit/cockpit.sh}"
[ -r "$COCKPIT" ] || { echo "addendum_name_check: REFUSED — cannot read $COCKPIT" >&2; exit 2; }
LINE="$(/usr/bin/grep -F "grep -qiE '(^|[^a-z])(proceed" "$COCKPIT" | head -1)"
RE="$(printf '%s' "$LINE" | sed -n "s/.*grep -qiE '\([^']*\)'.*/\1/p")"
[ -n "$RE" ] || { echo "addendum_name_check: REFUSED — the tap verb regex was not found in $COCKPIT" >&2; exit 2; }
NAME="$(basename "$1")"
# Separators in a file name (_ - .) are non-letters, exactly as the tap text sees them.
HIT="$(printf '%s' "$NAME" | /usr/bin/grep -oiE "$RE" | head -1)"
if [ -n "$HIT" ]; then
  echo "addendum_name_check: REFUSED (rc 3) — '$NAME' carries a word cockpit.sh say refuses un-mailed:${HIT}" >&2
  echo "  rename it with NOUNS from the subject, ending _ruling / _answer / _correction" >&2
  exit 3
fi
echo "addendum_name_check: clean — $NAME"
exit 0
