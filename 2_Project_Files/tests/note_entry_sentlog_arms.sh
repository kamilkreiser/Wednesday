#!/bin/bash
# Arms for note_entry.sh's SENT-RECEIPT GUARD (2026-10-08, Tuesday ledger w=6). Scratch note + scratch log only.
set -u
D="$(mktemp -d)"; NE="$(cd "$(dirname "$0")/.." && pwd)/tools/note_entry.sh"
: > "$D/note.md"; printf '2026-10-08T00:00:00Z sent: [Wednesday -> Datasec/NexusAI-M] ANSWER: logged subject here\n' > "$D/log.txt"
export WED_NOTE_OVERRIDE="$D/note.md" SEND_BRIEF_SENT_LOG="$D/log.txt" NOTE_ENTRY_TEST_STAMP=00:01
r(){ echo "$1" | bash "$NE" --stdin >/dev/null 2>&1; echo $?; }
fail=0; chk(){ [ "$2" = "$3" ] && echo "PASS $1" || { echo "FAIL $1 (got $2, want $3)"; fail=1; }; }
chk A1-logged     "$(r 'out "sent: [Wednesday -> Datasec/NexusAI-M] ANSWER: logged subject here"')" 0
chk A2-unlogged   "$(r 'out "sent: [Wednesday -> Datasec/NexusAI-M] ANSWER: never sent"')" 3
chk A3-no-quote   "$(r 'plain line')" 0
chk A4-truncated  "$(r 'out "sent: [Wednesday -> Datasec/NexusAI-M] ANSWER: logged subj"')" 0
chk A5-override   "$(echo 'out "sent: [X -> Y] other seat"' | NOTE_ALLOW_UNLOGGED_SENT=1 bash "$NE" --stdin >/dev/null 2>&1; echo $?)" 0
chk A6-refused-writes-nothing "$(wc -l < "$D/note.md" | tr -d ' ')" 4
exit $fail
