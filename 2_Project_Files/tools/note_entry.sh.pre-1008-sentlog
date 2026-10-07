#!/bin/bash
# note_entry.sh — append a bullet to TODAY's daily note with a GENERATED timestamp.
# WHY (consolidation 2026-08-30; ledger w=17/20/22/24/34/46 — six composed timestamps in
# ten days, the last one after a nine-hour gap, all self-consistent and wrong): a timestamp
# typed by hand is composed from narrative; the clock is read only if the WRITER reads it.
# This script reads it. Usage:
#   note_entry.sh --stdin <<'EOF'   → "- HH:MM — text" appended under the LAST heading of the note
#   note_entry.sh --h3 --stdin <<'EOF' → "### HH:MM — title" appended (a new block)
#   note_entry.sh --where              → print the note path this call WOULD write; writes nothing
#   (bare-argument forms RETIRED 2026-09-02, ledger w=5 — see the refusal below)
# Refuses empty text. Never discards stderr. The note must already exist (created at boot).
# SEAT NOTES (2026-09-16, Tuesday's census 20:23): the default note is the SEAT's own —
# WEDNESDAY tree -> 0_Brain/daily/, TUESDAY tree -> 0_Brain/daily_tuesday/ — via the ONE mapping in
# tools/seat_note.sh. Unrecognised tree, or WED_AGENT disagreeing with the tree: REFUSED, exit 2.
# WED_NOTE_OVERRIDE is a pure path seam and still wins outright (no seat resolution at all).
set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; PROJECT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
if [ -n "${WED_NOTE_OVERRIDE:-}" ]; then
  NOTE="$WED_NOTE_OVERRIDE"
else
  # shellcheck disable=SC1091
  . "$SCRIPT_DIR/seat_note.sh" || { echo "note_entry: REFUSED — cannot load $SCRIPT_DIR/seat_note.sh" >&2; exit 2; }
  seat_note_dir "$PROJECT_DIR" note_entry || exit 2
  NOTE="$SEAT_NOTE_DIR/$(date +%F).md"
fi
[ "${1:-}" = "--where" ] && { echo "$NOTE"; exit 0; }
[ -n "${WED_NOTE_OVERRIDE:-}" ] || mkdir -p "$SEAT_NOTE_DIR" || { echo "note_entry: cannot create $SEAT_NOTE_DIR" >&2; exit 2; }
[ -f "$NOTE" ] || { echo "note_entry: no note at $NOTE — create it from _template.md first" >&2; exit 2; }
# --stdin (added 2026-09-01, ledger w=4 in the unquoted-heredoc/backtick family): text passed as an
# ARGUMENT goes through the calling shell first — a backtick or $(…) inside a double-quoted
# argument is EXECUTED before this script runs (tonight: `git ls-remote --heads` ran and a
# handover line landed with a hole). With --stdin the caller writes  note_entry.sh --stdin <<'EOF'
# and nothing in the body can expand. This is the path Wednesday uses for ANY text containing
# a backtick, a dollar sign or a command; the argument form stays for one-line plain prose.
MODE=line; [ "${1:-}" = "--h3" ] && { MODE=h3; shift; }   # --h3 also takes its title via --stdin (2026-09-02: no argument path anywhere)
if [ "${1:-}" = "--stdin" ]; then
  TEXT="$(cat)"; TEXT="${TEXT%$'\n'}"
else
  # ARGUMENT FORM RETIRED 2026-09-02 (ledger w=5 in the unquoted-heredoc/backtick family): the
  # w=4 rule kept it "for one-line plain prose" and the very next backtick arrived inside prose
  # that felt plain — the shell executed `[]` and blanked the phrase. The writer cannot see the
  # backtick it is about to type, so the unsafe path must not exist. Use:  note_entry.sh --stdin <<'EOF'
  echo "note_entry: REFUSED — the bare-argument form is retired (ledger w=5, 2026-09-02). Use --stdin with a quoted heredoc (or --h3 for a heading)." >&2
  exit 2
fi
[ -n "$TEXT" ] || { echo "note_entry: refusing empty text" >&2; exit 2; }
STAMP="${NOTE_ENTRY_TEST_STAMP:-$(date +%H:%M)}"   # the test seam exists only for the arms below
# TYPED-CLOCK ADVISORY (2026-09-21; ledger w>=3 on 2026-09-19 — three typed clocks in one day, all
# "felt near-future" times for acts already done, written into bodies this script stamps but does
# not read). Any LOCAL HH:MM or HH:Mx in the body that is LATER than this line's own stamp is
# printed to stderr. Advisory, never blocking: an expiry or a schedule is a legitimate future time.
# Excluded on purpose: ISO/UTC forms (…T22:32, 22:32Z) — the fleet's mail clocks are UTC and
# routinely "later" than the local stamp without being typed clocks.
python3 - "$STAMP" "$TEXT" <<'PYCLK' >&2
import re, sys
stamp, text = sys.argv[1], sys.argv[2]
sh, sm = map(int, stamp.split(':'))
later = []
for m in re.finditer(r'(?<![\dT:])([01]\d|2[0-3]):([0-5](?:\d|x))(?![\dZ:])', text):
    h = int(m.group(1)); mm = m.group(2); mi = int(mm.replace('x', '0'))
    if (h, mi) > (sh, sm) and (h - sh) < 12:
        later.append(m.group(0))
if later:
    print("note_entry ADVISORY: body carries a time LATER than this line's stamp %s: %s — an expiry or a schedule is fine; a clock for an act already done is a typed clock (write 'just before this line' or copy the artefact's own stamp)." % (stamp, ", ".join(later)))
PYCLK
case $MODE in
  line) printf -- '- %s — %s\n' "$STAMP" "$TEXT" >> "$NOTE" ;;
  h3)   printf -- '### %s — %s\n' "$STAMP" "$TEXT" >> "$NOTE" ;;
esac
echo "note_entry: $STAMP → $NOTE"
