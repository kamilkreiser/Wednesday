#!/bin/bash
# kam_watch.sh — fires when Kam has posted ANYTHING this seat has not yet marked seen:
# a live/local board message, or a file he uploaded to the board's drawer.
#
# WHY (Kam 2026-11-10 14:3x: "Can you fix it so you dont miss agent or chat messages"):
# the old watcher compared message TIMES ("newer than 14:33"), so a second message in the same
# minute as one already read was invisible, and every re-arm took its baseline from "now", so
# anything that arrived between a fire and the re-arm was swallowed. This one remembers WHAT was
# seen, in a state file, and fires on any message or upload not in it, however close in time.
#
# Usage:
#   kam_watch.sh               watch (60 s poll, 4 h max); prints every UNSEEN item and exits 0 on the first
#   kam_watch.sh --pending     print unseen items now and exit (0 = none, 1 = some); never waits
#   kam_watch.sh --mark-seen   mark everything currently visible as seen (run ONLY after reading it all)
# State: 2_Project_Files/fleet/state/kam_watch_seen.txt (gitignored), one key per line.
# Read-only towards the board: it only reads; marking seen is a local file.
set -u
T=/Volumes/Datasec_DEV/TUESDAY/2_Project_Files
STATE="$T/fleet/state/kam_watch_seen.txt"
PY="$T/dashboard-cloud/.venv/bin/python"
touch "$STATE"

current() {
  # messages: every [live]/[local] row of today, keyed by its whole line plus its occurrence number
  bash "$T/tools/kam_rulings_today.sh" 2>/dev/null | /usr/bin/grep -E '\[(live|local)\]' | awk '{c[$0]++; print "MSG\t" c[$0] "\t" $0}'
  # uploads: files Kam put in the drawer today (id is unique)
  "$PY" "$T/dashboard-cloud/seat/get_files.py" --seat tuesday --client Datasec --limit 500 2>/dev/null \
    | /usr/bin/grep 'by=kam' | /usr/bin/grep "$(date -u +%Y-%m-%d)\|$(date -u -v-1d +%Y-%m-%d)" \
    | sed -E 's/.*id=(f-[0-9a-f]+).* name=(.*) note=.*/FILE\t\1\t\2/'
}
unseen() { current | while IFS= read -r k; do /usr/bin/grep -q -x -F -- "$k" "$STATE" || printf '%s\n' "$k"; done; }

case "${1:-}" in
  --mark-seen) n=0; current | while IFS= read -r k; do /usr/bin/grep -q -x -F -- "$k" "$STATE" || { printf '%s\n' "$k" >> "$STATE"; }; done
               echo "marked; state holds $(wc -l < "$STATE" | tr -d ' ') keys"; exit 0 ;;
  --pending)   u=$(unseen); if [ -n "$u" ]; then echo "UNSEEN:"; printf '%s\n' "$u" | cut -f3-; exit 1; else echo "none unseen"; exit 0; fi ;;
esac

# control: the instrument must see at least one message today, or it is blind.
# 2026-11-13 03:35 (Tuesday s274): after midnight there are 0 rows of TODAY until Kam's first message, so the
# old control refused to arm all night. A board read is proven instead by its FRESHNESS line: 'N live rows
# fetched' with N > 0 (the fetch itself returned rows, whatever their date). Both 0: blind, refuse.
c=$(current | /usr/bin/grep -c '^MSG')
if [ "$c" -eq 0 ]; then
  f=$(bash "$T/tools/kam_rulings_today.sh" 2>/dev/null | /usr/bin/grep -i -o -E '[0-9]+ live rows fetched' | /usr/bin/grep -o -E '^[0-9]+')
  [ -n "$f" ] && [ "$f" -gt 0 ] || { echo "CONTROL FAILED: 0 messages visible and 0 live rows fetched"; exit 3; }
  echo "CONTROL: 0 messages today; board read proven by $f live rows fetched"
fi
u=$(unseen); if [ -n "$u" ]; then echo "FIRED KAM (already unseen at arm):"; printf '%s\n' "$u" | cut -f3-; exit 0; fi
echo "ARMED $(date +%H:%M:%S): $c messages visible, all seen"
for i in $(seq 1 240); do
  sleep 60
  u=$(unseen); if [ -n "$u" ]; then echo "FIRED KAM $(date +%H:%M:%S):"; printf '%s\n' "$u" | cut -f3-; exit 0; fi
done
echo "TIMEOUT 4h, nothing new"
