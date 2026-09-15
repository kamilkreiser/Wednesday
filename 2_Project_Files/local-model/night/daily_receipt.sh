#!/bin/bash
# daily_receipt.sh [YYYY-MM-DD] [--post] — ONE panel line for Kam from the night runner's own records, so that
# "know progress continues through the week" (Kam 2026-09-15 18:19) is a mechanism, not a seat remembering.
# Reads: night/done.md (verdicts, by date), night/READY_* (held pins/tickets, from filenames), IMPROVEMENTS.md (rows
# dated today), usage_wednesday.json (the 7d gauge). Prints the line; --post mirrors it via chat_reply.sh (first person,
# no typed clock — the panel stamps it). Every number is COUNTED here, never carried from a note (ledger w=5, 08-14).
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"; LM="$(cd "$HERE/.." && pwd)"; W="$(cd "$LM/../.." && pwd)"
# 2026-09-15 23:1x: the date is the FIRST argument that LOOKS like a date, in any position — `daily_receipt.sh --post`
# (the launchd job's shape) used to read DAY="--post" and would have posted a garbage line (caught at the render arm).
# RECEIPT_DRY=1 prints the line that WOULD be posted, without posting (the test seam).
DAY=""; POST=0
for a in "$@"; do
  case "$a" in
    --post) POST=1 ;;
    [0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]) DAY="$a" ;;
    *) echo "daily_receipt: unknown argument '$a' (usage: daily_receipt.sh [YYYY-MM-DD] [--post])" >&2; exit 2 ;;
  esac
done
[ -n "$DAY" ] || DAY="$(date +%F)"
DONE="$HERE/done.md"
pass=$(/usr/bin/grep -i "| done $DAY " "$DONE" 2>/dev/null | /usr/bin/grep -ci 'RESULT: PASS')
fail=$(/usr/bin/grep -i "| done $DAY " "$DONE" 2>/dev/null | /usr/bin/grep -ci 'RESULT: FAIL')
# 2026-09-16 07:4x: "fails" counted VERDICT LINES — on 09-16 the 06:45 line said "10 fails" when every one was a harness/brief
# round later held (a representation read as a result). UNRESOLVED = tickets with a FAIL row today and NO READY_<id>* file.
rounds=$(/usr/bin/grep -i "| done $DAY " "$DONE" 2>/dev/null | /usr/bin/grep -vci "DRY-RUN ROW")
unresolved=$(/usr/bin/grep -i "| done $DAY " "$DONE" 2>/dev/null | /usr/bin/grep -i 'RESULT: FAIL' | sed -E 's/^(KS-[0-9]+).*/\1/' | sort -u | while IFS= read -r id; do [ -n "$id" ] || continue; held=0; for f in "$HERE"/READY_"$id"_* "$HERE"/READY_"$id"-*; do [ -e "$f" ] && held=1; done; [ "$held" = 1 ] || echo "$id"; done | tr '\n' ' ' | sed 's/ $//')
unresolved_n=$(printf '%s' "$unresolved" | wc -w | tr -d ' ')
refused=$(/usr/bin/grep -i "| done $DAY " "$DONE" 2>/dev/null | /usr/bin/grep -ci 'BUILD_REFUSED')
retracted=$(/usr/bin/grep -ci "^# RETRACTED by Wednesday" "$DONE" 2>/dev/null)
files=$(ls "$HERE"/READY_* 2>/dev/null | wc -l | tr -d ' ')
pins=$(ls "$HERE"/READY_* 2>/dev/null | sed -E 's|.*/READY_(KS-[0-9]+(-[A-Za-z0-9]+)?)_.*|\1|' | sort -u | wc -l | tr -d ' ')
tickets=$(ls "$HERE"/READY_* 2>/dev/null | sed -E 's|.*/READY_(KS-[0-9]+).*|\1|' | sort -u | wc -l | tr -d ' ')
newtoday=$(ls "$HERE"/READY_*_"$DAY".diff.md 2>/dev/null | sed -E 's|.*/READY_(KS-[0-9]+(-[A-Za-z0-9]+)?)_.*|\1|' | sort -u | wc -l | tr -d ' ')
rows=$(/usr/bin/grep -c "^| $DAY " "$LM/IMPROVEMENTS.md" 2>/dev/null)
gauge=$(python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); print(d.get("pct","?"))' "$W/0_Brain/dashboard/data/usage_wednesday.json" 2>/dev/null || echo "?")
lock="$HERE/log/.night_run.lock/pid"; running="idle"; [ -f "$lock" ] && kill -0 "$(cat "$lock")" 2>/dev/null && running="running"
LINE="Ornith daily receipt for $DAY: $rounds model rounds — $pass passes, $fail fail rounds (harness/brief rounds included), $unresolved_n ticket(s) still unresolved${unresolved:+ ($unresolved)}, $refused build-refusals; $newtoday new pins held today; $pins pins across $tickets tickets held for Sunday in total ($files files); $rows harness improvement rows written today; the model is $running now; Claude allowance at ${gauge}%."
[ "$retracted" -gt 0 ] && LINE="$LINE $retracted verdict(s) stand retracted in done.md."
echo "$LINE"
if [ "$POST" = 1 ]; then if [ "${RECEIPT_DRY:-0}" = 1 ]; then echo "DRY (would post): $LINE"; else bash "$W/2_Project_Files/tools/chat_reply.sh" "$LINE" > /dev/null 2>&1 && echo "posted to the panel" || echo "post FAILED" >&2; fi; fi
