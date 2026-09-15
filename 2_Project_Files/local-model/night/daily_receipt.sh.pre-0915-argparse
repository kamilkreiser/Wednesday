#!/bin/bash
# daily_receipt.sh [YYYY-MM-DD] [--post] — ONE panel line for Kam from the night runner's own records, so that
# "know progress continues through the week" (Kam 2026-09-15 18:19) is a mechanism, not a seat remembering.
# Reads: night/done.md (verdicts, by date), night/READY_* (held pins/tickets, from filenames), IMPROVEMENTS.md (rows
# dated today), usage_wednesday.json (the 7d gauge). Prints the line; --post mirrors it via chat_reply.sh (first person,
# no typed clock — the panel stamps it). Every number is COUNTED here, never carried from a note (ledger w=5, 08-14).
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"; LM="$(cd "$HERE/.." && pwd)"; W="$(cd "$LM/../.." && pwd)"
DAY="${1:-$(date +%F)}"; POST=0; for a in "$@"; do [ "$a" = "--post" ] && POST=1; done
DONE="$HERE/done.md"
pass=$(/usr/bin/grep -i "| done $DAY " "$DONE" 2>/dev/null | /usr/bin/grep -ci 'RESULT: PASS')
fail=$(/usr/bin/grep -i "| done $DAY " "$DONE" 2>/dev/null | /usr/bin/grep -ci 'RESULT: FAIL')
refused=$(/usr/bin/grep -i "| done $DAY " "$DONE" 2>/dev/null | /usr/bin/grep -ci 'BUILD_REFUSED')
retracted=$(/usr/bin/grep -ci "^# RETRACTED by Wednesday" "$DONE" 2>/dev/null)
files=$(ls "$HERE"/READY_* 2>/dev/null | wc -l | tr -d ' ')
pins=$(ls "$HERE"/READY_* 2>/dev/null | sed -E 's|.*/READY_(KS-[0-9]+(-[A-Za-z0-9]+)?)_.*|\1|' | sort -u | wc -l | tr -d ' ')
tickets=$(ls "$HERE"/READY_* 2>/dev/null | sed -E 's|.*/READY_(KS-[0-9]+).*|\1|' | sort -u | wc -l | tr -d ' ')
newtoday=$(ls "$HERE"/READY_*_"$DAY".diff.md 2>/dev/null | sed -E 's|.*/READY_(KS-[0-9]+(-[A-Za-z0-9]+)?)_.*|\1|' | sort -u | wc -l | tr -d ' ')
rows=$(/usr/bin/grep -c "^| $DAY " "$LM/IMPROVEMENTS.md" 2>/dev/null)
gauge=$(python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); print(d.get("pct","?"))' "$W/0_Brain/dashboard/data/usage_wednesday.json" 2>/dev/null || echo "?")
lock="$HERE/log/.night_run.lock/pid"; running="idle"; [ -f "$lock" ] && kill -0 "$(cat "$lock")" 2>/dev/null && running="running"
LINE="Ornith daily receipt for $DAY: $pass passes, $fail fails, $refused build-refusals in the runner's log today; $newtoday new pins held today; $pins pins across $tickets tickets held for Sunday in total ($files files); $rows harness improvement rows written today; the model is $running now; Claude allowance at ${gauge}%."
[ "$retracted" -gt 0 ] && LINE="$LINE $retracted verdict(s) stand retracted in done.md."
echo "$LINE"
if [ "$POST" = 1 ]; then bash "$W/2_Project_Files/tools/chat_reply.sh" "$LINE" > /dev/null 2>&1 && echo "posted to the panel" || echo "post FAILED" >&2; fi
