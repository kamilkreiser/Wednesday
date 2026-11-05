#!/bin/bash
# Arms for note_entry.sh's RECEIPT-VERB GUARD (2026-11-05, ledger w=4 note-batching). Scratch note + scratch files only.
# NE_UNDER_TEST=<path> tests a candidate copy before it is installed.
set -u
D="$(mktemp -d)"; NE="${NE_UNDER_TEST:-$(cd "$(dirname "$0")/.." && pwd)/tools/note_entry.sh}"
: > "$D/note.md"; : > "$D/log.txt"
export WED_NOTE_OVERRIDE="$D/note.md" SEND_BRIEF_SENT_LOG="$D/log.txt" NOTE_ENTRY_TEST_STAMP=00:01
printf 'pane_close: detector: prompt empty\nclosed %%9; listeners 1 -> 1\n' > "$D/fresh.out"
printf 'closed %%9\n' > "$D/stale.out"; touch -t 202601010000 "$D/stale.out"
r(){ echo "$2" | bash "$NE" $1 --stdin >/dev/null 2>&1; echo $?; }
fail=0; chk(){ [ "$2" = "$3" ] && echo "PASS $1" || { echo "FAIL $1 (got $2, want $3)"; fail=1; }; }
chk R1-verb-no-receipt     "$(r '' 'pane closed %9 cleanly')" 3
chk R2-verb-fresh-receipt  "$(r "--receipt $D/fresh.out" 'pane closed %9 cleanly')" 0
chk R3-verb-stale-receipt  "$(r "--receipt $D/stale.out" 'pane closed %9 cleanly')" 3
chk R4-answered-no-receipt "$(r '' 'QUESTION answered and tapped')" 3
chk R5-ruled-no-receipt    "$(r '' 'card ruled: x -> a')" 3
chk R6-delivered-case      "$(r '' 'Mark DELIVERED on the card')" 3
chk R7-acked-no-receipt    "$(r '' 'acked %12 idle')" 3
chk R8-plain-line          "$(r '' 'plain progress line, nothing claimed')" 0
chk R9-near-miss-words     "$(r '' 'unanswered question; closed-loop; disclosed %; rule: x')" 0
chk R10-override           "$(echo 'Kam answered on the panel (prose)' | NOTE_ALLOW_RECEIPT_VERB=1 bash "$NE" --stdin >/dev/null 2>&1; echo $?)" 0
chk R11-refused-writes-nothing "$(wc -l < "$D/note.md" | tr -d ' ')" 4
/usr/bin/grep -q 'receipt fresh.out: closed %9; listeners 1 -> 1' "$D/note.md" && echo "PASS R12-receipt-line-copied" || { echo "FAIL R12-receipt-line-copied"; fail=1; }
exit $fail
