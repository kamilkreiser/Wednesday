#!/bin/bash
# name_addendum.sh — name a seat ADDENDUM file so its tap cannot be refused by the tap gate.
#
# WHY (Friday ledger, tap-verb rows w=2..w=6, 2026-09-27 → 2026-09-30): Friday delivers an
# addendum to a seat as a FILE plus a bare tap, `New file from Friday: <path>`. The tap gate in
# fleet/cockpit/cockpit.sh (say, the INSTRUCTION-VERB clause) refuses a mail-less tap whose text
# carries a word that authorises work — and the path IS the tap text. Six times an addendum was
# named with such a word (accepted, start, deploy, resume…), the gate refused, and a turn was
# spent renaming. At w=5 the diagnosis was that the author reads a NOUN ("deploy checks") where
# the gate reads a VERB; at w=6 the rule held in memory failed again. So the check moves to the
# moment the name is made.
#
# It does NOT keep its own word list: it reads the gate's regex out of cockpit.sh at run time,
# so the two can never drift (a second implementation disagrees by default — 2026-09-08 rule 7).
# If that line cannot be found, it REFUSES (rc 5) rather than passing everything.
#
# Usage:
#   name_addendum.sh <briefs-dir> <brief-id> <N> <noun-slug>
#       e.g. name_addendum.sh "$HPSM_POC/1_Project_Definition/Briefs" 2026-10-02_B06 1 base-7f6ca4c
#       prints the full path <briefs-dir>/<brief-id>_ADDENDUM-<N>_<noun-slug>.md on stdout (rc 0).
#       It only NAMES the file; it does not create it.
#   name_addendum.sh --check <path>     test an existing path exactly as the tap would carry it.
# Exit: 0 ok · 2 usage · 3 the file already exists (never clobber) · 5 gate regex not found ·
#       6 the name carries a gate word (the word is printed; pick a noun: base-<sha>, records,
#       findings, answers, measurements, state).
# Override for tests only: NAME_ADDENDUM_COCKPIT=<path to a cockpit.sh>.

set -u
SELF_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COCKPIT="${NAME_ADDENDUM_COCKPIT:-$SELF_DIR/../fleet/cockpit/cockpit.sh}"

die() { echo "name_addendum: $*" >&2; exit 2; }

[ -r "$COCKPIT" ] || { echo "name_addendum: REFUSED (rc 5) — cannot read the tap gate at $COCKPIT" >&2; exit 5; }
# The gate's own INSTRUCTION-VERB line is the one carrying authoris(e|ed); take its -qiE pattern.
RE=$(grep -m1 -F 'authoris(e|ed)' "$COCKPIT" | sed -nE "s/.*grep -qiE '([^']+)'.*/\1/p")
[ -n "$RE" ] || { echo "name_addendum: REFUSED (rc 5) — the gate's verb regex was not found in $COCKPIT; refusing rather than passing every name" >&2; exit 5; }

check_path() { # $1 = the full path the tap will carry
  local tap="New file from Friday: $1" hit
  if printf '%s' "$tap" | grep -qiE "$RE"; then
    hit=$(printf '%s' "$tap" | grep -oiE "$RE" | head -1 | sed -E 's/^[^a-zA-Z]+//; s/[^a-zA-Z ]+$//')
    echo "name_addendum: REFUSED (rc 6) — the tap gate would refuse this name: it carries '$hit'." >&2
    echo "  Name the CONTENT with a noun (base-<sha>, records, findings, answers, measurements, state)." >&2
    echo "  Tested text: $tap" >&2
    return 6
  fi
  return 0
}

if [ "${1:-}" = "--check" ]; then
  [ $# -eq 2 ] || die "usage: name_addendum.sh --check <path>"
  check_path "$2" || exit $?
  echo "name_addendum: OK — the tap gate accepts: New file from Friday: $2"
  exit 0
fi

[ $# -eq 4 ] || die "usage: name_addendum.sh <briefs-dir> <brief-id> <N> <noun-slug>   |   --check <path>"
DIR="${1%/}"; ID="$2"; N="$3"; SLUG="$4"
[ -d "$DIR" ] || die "no such briefs directory: $DIR"
case "$N" in ''|*[!0-9]*) die "N must be a number, got '$N'";; esac
case "$SLUG" in *[!A-Za-z0-9._-]*|'') die "noun-slug must be letters, digits, '.', '_' or '-', got '$SLUG'";; esac
P="$DIR/${ID}_ADDENDUM-${N}_${SLUG}.md"
[ -e "$P" ] && { echo "name_addendum: REFUSED (rc 3) — already exists, never clobber: $P" >&2; exit 3; }
check_path "$P" || exit $?
printf '%s\n' "$P"
