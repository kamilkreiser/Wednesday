#!/bin/bash
# note_entry_xclock_selftest.sh — fire, quiet and override arms of note_entry.sh's X-DIGIT CLOCK GUARD (2026-11-23).
# Writes only to a scratch note under $TMPDIR (WED_NOTE_OVERRIDE), never to a seat's real note, so it is safe in
# every seat's tree. Exit 0 = every arm as expected; exit 1 = an arm failed (it is named). bash 3.2 safe.
set -u
SELF_DIR="$(cd "$(dirname "$0")" && pwd)"
TOOL="$SELF_DIR/note_entry.sh"
SCR="$(mktemp -d "${TMPDIR:-/tmp}/xclock_selftest.XXXXXX")" || { echo "selftest: cannot make a scratch dir" >&2; exit 1; }
NOTE="$SCR/note.md"; printf '# scratch note\n\n## Sessions\n' > "$NOTE"
FAIL=0
run() {  # run <expected rc> <label> <body> [allow-reason]
  local want="$1" label="$2" body="$3" allow="${4:-}" rc before after
  before="$(wc -c < "$NOTE")"
  if [ -n "$allow" ]; then
    printf '%s\n' "$body" | NOTE_ALLOW_XCLOCK="$allow" WED_NOTE_OVERRIDE="$NOTE" bash "$TOOL" --stdin > "$SCR/out" 2> "$SCR/err"; rc=$?
  else
    printf '%s\n' "$body" | WED_NOTE_OVERRIDE="$NOTE" bash "$TOOL" --stdin > "$SCR/out" 2> "$SCR/err"; rc=$?
  fi
  after="$(wc -c < "$NOTE")"
  if [ "$rc" != "$want" ]; then echo "FAIL [$label]: rc $rc, wanted $want"; sed 's/^/    /' "$SCR/err"; FAIL=1; return; fi
  if [ "$want" = "3" ] && [ "$before" != "$after" ]; then echo "FAIL [$label]: refused but the note grew"; FAIL=1; return; fi
  if [ "$want" = "0" ] && [ "$before" = "$after" ]; then echo "FAIL [$label]: accepted but nothing was written"; FAIL=1; return; fi
  echo "ok   [$label] rc $rc"
}
# FIRE arms: each must be refused (rc 3) and write nothing.
run 3 "fire: 21:5x"            "the statusline read at 21:5x showed forty percent"
run 3 "fire: ~09:3x"           "grant written ~09:3x in the row"
run 3 "fire: 9:0x"             "seen about 9:0x."
run 3 "fire: 12:xx"            "some time after 12:xx"
run 3 "fire: upper case 07:5X" "written 07:5X three times"
run 3 "fire: at line start"    "21:5x was the time"
# QUIET arms: none is a clock with an x digit; each must be written (rc 0).
run 0 "quiet: a real clock"    "the relay listened from 11:22 until it was stopped"
run 0 "quiet: iso stamp"       "stamp 2026-11-23T11:34 in the log"
run 0 "quiet: 5x faster"       "the second build was 5x faster"
run 0 "quiet: hex and x86"     "value 0x1f on x86, id 12ab:5xyz"
run 0 "quiet: plain prose"     "no time in this line at all"
# OVERRIDE arm: quoting is allowed with a reason, and the reason lands in the note.
run 0 "override: quoted row"   "the grant row says 'terminal 2026-10-15 ~12:5x AEDT'" "quoting a grant row"
if ! /usr/bin/grep -q -F '[x-clock quoted, not composed: quoting a grant row]' "$NOTE"; then echo "FAIL [override]: the reason is not in the note"; FAIL=1; else echo "ok   [override reason recorded]"; fi
# The refusal names what it found (a refusal nobody can act on is half a guard).
printf '%s\n' "at 21:5x" | WED_NOTE_OVERRIDE="$NOTE" bash "$TOOL" --stdin > "$SCR/out" 2> "$SCR/err"
if /usr/bin/grep -q -E 'REFUSED.*x digit.*21:5x' "$SCR/err"; then echo "ok   [refusal names the clock]"; else echo "FAIL [refusal text does not name the clock]"; FAIL=1; fi
echo "scratch: $SCR"
[ "$FAIL" = "0" ] && { echo "XCLOCK SELFTEST: ALL ARMS OK"; exit 0; }
echo "XCLOCK SELFTEST: FAILED"; exit 1
