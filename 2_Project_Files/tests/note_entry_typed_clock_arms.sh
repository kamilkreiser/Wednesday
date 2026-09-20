#!/bin/bash
# note_entry_typed_clock_arms.sh — arms for note_entry.sh's TYPED-CLOCK ADVISORY (2026-09-21).
# Why: ledger w>=3 on 2026-09-19 — three typed clocks in one day inside note bodies, each a felt
# near-future time for an act already done. The advisory prints to stderr when a LOCAL HH:MM/HH:Mx
# in the body is later than the line's own stamp; UTC/ISO forms are excluded; never blocking.
# Run: bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tests/note_entry_typed_clock_arms.sh  → 7/7 PASS
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; T="$HERE/../tools/note_entry.sh"
S="$(mktemp -d)"; N="$S/arm_note.md"; printf '# arm\n## Sessions\n' > "$N"
pass=0; fail=0
run(){ printf '%s' "$2" | WED_NOTE_OVERRIDE="$N" NOTE_ENTRY_TEST_STAMP=07:58 bash "$T" --stdin > "$S/out" 2> "$S/err"; rc=$?
  w=$(/usr/bin/grep -c -i 'ADVISORY' "$S/err")
  if [ "$w" = "$3" ] && [ "$rc" = 0 ]; then echo "PASS $1"; pass=$((pass+1)); else echo "FAIL $1: rc=$rc warn=$w expect=$3 :: $(cat "$S/err")"; fail=$((fail+1)); fi; }
run ARM1-typed-future "QUEUED 08:0x by this seat" 1
run ARM2-utc-Z "Seat B STATUS 22:32Z read whole" 0
run ARM3-iso-T "wrap 2026-09-20T22:32 read" 0
run ARM4-earlier "done at 07:03 after a source read" 0
run ARM5-no-time "nothing timed here" 0
run ARM6-expiry-still-warns-advisory "PAUSE_QUEUE re-armed to 10:45 with the reason" 1
run ARM7-clock-with-seconds "sha 12:34:56 style and 7be81d5c9" 0
lines=$(/usr/bin/grep -c '^- ' "$N"); [ "$lines" = 7 ] && echo "PASS control: 7 lines written" || { echo "FAIL control: $lines lines"; fail=$((fail+1)); }
echo "RESULT: $pass pass / $fail fail"; [ "$fail" = 0 ]
