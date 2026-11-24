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
#   kam_watch.sh --mark-seen   mark ONLY the keys the last --pending print listed. REFUSES (rc 4) if no --pending print
#                              in the last 120 s, or (rc 5) if the board now shows an unseen key that print did not list
#                              (a row that landed after the read). Run `--pending` first, read it, then `--mark-seen`.
# State: 2_Project_Files/fleet/state/kam_watch_seen.txt (gitignored), one key per line.
# Read-only towards the board: it only reads; marking seen is a local file.
set -u
T=/Volumes/Datasec_DEV/TUESDAY/2_Project_Files
# KAM_WATCH_STATE_DIR / KAM_WATCH_FIXTURE: test overrides only (fixture = a file of "current" key lines used instead of the board).
SD="${KAM_WATCH_STATE_DIR:-$T/fleet/state}"
STATE="$SD/kam_watch_seen.txt"
PENDING="$SD/kam_watch_pending.txt"   # line 1: epoch of the last --pending print; then the keys that print listed
MAXAGE="${KAM_WATCH_MAXAGE:-120}"
PY="$T/dashboard-cloud/.venv/bin/python"
mkdir -p "$SD"; touch "$STATE"

current() {
  if [ -n "${KAM_WATCH_FIXTURE:-}" ]; then cat "$KAM_WATCH_FIXTURE"; return; fi
  # messages: every [live]/[local] row of today, keyed by its whole line plus its occurrence number
  bash "$T/tools/kam_rulings_today.sh" 2>/dev/null | /usr/bin/grep -E '\[(live|local)\]' | awk '{c[$0]++; print "MSG\t" c[$0] "\t" $0}'
  # uploads: files Kam put in the drawer today (id is unique)
  "$PY" "$T/dashboard-cloud/seat/get_files.py" --seat tuesday --client Datasec --limit 500 2>/dev/null \
    | /usr/bin/grep 'by=kam' | /usr/bin/grep "$(date -u +%Y-%m-%d)\|$(date -u -v-1d +%Y-%m-%d)" \
    | sed -E 's/.*id=(f-[0-9a-f]+).* name=(.*) note=.*/FILE\t\1\t\2/'
}
unseen() { current | while IFS= read -r k; do /usr/bin/grep -q -x -F -- "$k" "$STATE" || printf '%s\n' "$k"; done; }

case "${1:-}" in
  --mark-seen) if [ ! -f "$PENDING" ]; then echo "REFUSED: no --pending print on record. Run: bash $0 --pending, read it, then --mark-seen." >&2; exit 4; fi
               pe=$(head -1 "$PENDING" | tr -d ' '); now=$(date +%s)
               case "$pe" in ''|*[!0-9]*) echo "REFUSED: pending record unreadable. Run: bash $0 --pending" >&2; exit 4;; esac
               age=$((now - pe))
               if [ "$age" -gt "$MAXAGE" ] || [ "$age" -lt 0 ]; then echo "REFUSED: last --pending print was ${age}s ago (limit ${MAXAGE}s). Run: bash $0 --pending, read it, then --mark-seen." >&2; exit 4; fi
               extra=$(unseen | while IFS= read -r k; do tail -n +2 "$PENDING" | /usr/bin/grep -q -x -F -- "$k" || printf '%s\n' "$k"; done)
               if [ -n "$extra" ]; then echo "REFUSED: the board now shows unseen row(s) the last --pending print did not list (landed after your read):" >&2; printf '%s\n' "$extra" | cut -f3- >&2; echo "Run: bash $0 --pending, read it, then --mark-seen." >&2; exit 5; fi
               tail -n +2 "$PENDING" | while IFS= read -r k; do /usr/bin/grep -q -x -F -- "$k" "$STATE" || printf '%s\n' "$k" >> "$STATE"; done
               : > "$PENDING"
               echo "marked only the keys the --pending print listed; state holds $(wc -l < "$STATE" | tr -d ' ') keys"; exit 0 ;;
  --pending)   u=$(unseen); { date +%s; [ -n "$u" ] && printf '%s\n' "$u"; } > "$PENDING.tmp" && mv "$PENDING.tmp" "$PENDING"
               if [ -n "$u" ]; then echo "UNSEEN:"; printf '%s\n' "$u" | cut -f3-; exit 1; else echo "none unseen"; exit 0; fi ;;
esac

# control: the instrument must see at least one message today, or it is blind.
# 2026-11-13 03:35 (Tuesday s274): after midnight there are 0 rows of TODAY until Kam's first message, so the
# old control refused to arm all night. A board read is proven instead by its FRESHNESS line: 'N live rows
# fetched' with N > 0 (the fetch itself returned rows, whatever their date). Both 0: blind, refuse.
c=$(current | /usr/bin/grep -c '^MSG')
if [ "$c" -eq 0 ]; then
  f=$(bash "$T/tools/kam_rulings_today.sh" 2>/dev/null | /usr/bin/grep -i -o -E '[0-9]+ live rows fetched' | /usr/bin/grep -o -E '^[0-9]+')
  # 2026-11-15 02:44 (Tuesday s275): today's live fetch can ALSO be empty when Kam has been quiet since
  # yesterday morning (the window holds only today's rows). Fall back to YESTERDAY's live read as the proof
  # the same instrument can reach the board; both empty = blind, refuse.
  w="today"
  if [ -z "$f" ] || [ "$f" -eq 0 ]; then
    f=$(bash "$T/tools/kam_rulings_today.sh" "$(date -v-1d +%Y-%m-%d)" 2>/dev/null | /usr/bin/grep -i -o -E '[0-9]+ live rows fetched' | /usr/bin/grep -o -E '^[0-9]+'); w="yesterday"
  fi
  [ -n "$f" ] && [ "$f" -gt 0 ] || { echo "CONTROL FAILED: 0 messages visible and 0 live rows fetched (today and yesterday)"; exit 3; }
  echo "CONTROL: 0 messages today; board read proven by $f live rows fetched ($w's window)"
fi
u=$(unseen); if [ -n "$u" ]; then echo "FIRED KAM (already unseen at arm):"; printf '%s\n' "$u" | cut -f3-; exit 0; fi
echo "ARMED $(date +%H:%M:%S): $c messages visible, all seen"
for i in $(seq 1 240); do
  sleep 60
  u=$(unseen); if [ -n "$u" ]; then echo "FIRED KAM $(date +%H:%M:%S):"; printf '%s\n' "$u" | cut -f3-; exit 0; fi
done
echo "TIMEOUT 4h, nothing new"
