#!/bin/bash
# floor_watch.sh — ONE watcher over every live Datasec seat's STATUS last line.
#
# WHY (ledger 2026-11-10 s262, w=2 of the STOPPED-unwatched row): watchers were armed per seat, by hand,
# only for seats the coordinator LAUNCHED; seats re-tasked by a tap (an addendum, an answer) got none, and
# four sat STOPPED or READY for up to 2 h. This finds every live seat from the panes themselves, so nothing
# depends on remembering.
#
# Usage: floor_watch.sh [--once] [interval-seconds, default 60] [max-minutes, default 240]
#   --once   print the table (pane, B-number, STATUS mtime, last line) and exit 0; writes nothing.
#   default  record each seat's last line at arm, then fire (print + exit 0) when any seat's last line
#            CHANGES to a terminal form: READY / STOPPED / CLOSED / DEPLOYED / RECORDS / ROLLED BACK,
#            or a new seat appears with such a line. A seat whose STATUS is missing is listed, not fired.
# Seat -> STATUS: the B-number is read from the pane's claude/brief_seat command line; the STATUS file is
#   /Volumes/Datasec_DEV/!CODING/Datasec/*/1_Project_Definition/Briefs/*_<Bnnnn>_STATUS.md (newest).
# Read-only: no tap, no file write outside stdout.
set -u
ONCE=0; MARK=0; [ "${1:-}" = "--once" ] && { ONCE=1; shift; }; [ "${1:-}" = "--mark-seen" ] && { MARK=1; shift; }
IV="${1:-60}"; MAXM="${2:-240}"
ROOT='/Volumes/Datasec_DEV/!CODING/Datasec'
TERM_RE='^(READY |STOPPED|CLOSED |DEPLOYED |HANDOVER |DONE: |RECORDS (COMMITTED|PUSHED|DRY RUN|DONE)|ROLLED BACK)'  # DONE: added 2026-11-13 (B1550's final line 'DONE: B1550 ...' was invisible to this watcher)

snapshot() {
  tmux list-panes -a -F '#{pane_id} #{pane_pid} #{@cockpit_name}' 2>/dev/null | while read -r pid_ ppid name; do
    case "$name" in Datasec/*) ;; *) continue ;; esac
    b=""
    for c in $(pgrep -P "$ppid" 2>/dev/null) "$ppid"; do
      b=$(ps -o command= -p "$c" 2>/dev/null | /usr/bin/grep -o -E 'B1[0-9]{3}' | head -1)
      [ -n "$b" ] && break
      for g in $(pgrep -P "$c" 2>/dev/null); do
        b=$(ps -o command= -p "$g" 2>/dev/null | /usr/bin/grep -o -E 'B1[0-9]{3}' | head -1); [ -n "$b" ] && break 2
      done
    done
    [ -z "$b" ] && { echo "$pid_|$name|-|-|no B-number in the pane's commands"; continue; }
    f=$(ls -t "$ROOT"/*/1_Project_Definition/Briefs/*_"${b}"_STATUS.md 2>/dev/null | head -1)
    if [ -z "$f" ]; then echo "$pid_|$name|$b|-|no STATUS file yet"; continue; fi
    m=$(stat -f '%Sm' -t '%H:%M' "$f"); l=$(/usr/bin/grep -v '^[[:space:]]*$' "$f" | tail -1 | cut -c1-160)
    echo "$pid_|$name|$b|$m|$l"
  done
}

STATE=/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/floor_watch_seen.txt
touch "$STATE"
# PERSISTENT SEEN-STATE (Kam 2026-11-10: "fix it so you dont miss agent or chat messages"): the baseline is
# what the coordinator last SAW (seat|terminal line), kept across re-arms, never "now". A seat that reaches a
# terminal line between a fire and the re-arm therefore still fires at the re-arm. --mark-seen records the
# current lines after the coordinator has read them; the watcher marks what it fires on as seen when it exits.
unseen_terminal() {
  snapshot | while IFS='|' read -r p n b m l; do
    printf '%s' "$l" | /usr/bin/grep -q -E "$TERM_RE" || continue
    /usr/bin/grep -q -x -F -- "$n|$l" "$STATE" || echo "$n $b ($m): $l"
  done
}
if [ $ONCE -eq 1 ]; then snapshot; exit 0; fi
if [ "${MARK:-0}" = 1 ]; then snapshot | while IFS='|' read -r p n b m l; do printf '%s' "$l" | /usr/bin/grep -q -E "$TERM_RE" && { /usr/bin/grep -q -x -F -- "$n|$l" "$STATE" || echo "$n|$l" >> "$STATE"; }; done; echo "marked; $(wc -l < "$STATE" | tr -d ' ') keys"; exit 0; fi
mark_fired() { snapshot | while IFS='|' read -r p n b m l; do printf '%s' "$l" | /usr/bin/grep -q -E "$TERM_RE" && { /usr/bin/grep -q -x -F -- "$n|$l" "$STATE" || echo "$n|$l" >> "$STATE"; }; done; }
u=$(unseen_terminal); if [ -n "$u" ]; then echo "FIRED $(date +%H:%M:%S) (unseen at arm):"; printf '%s\n' "$u"; mark_fired; exit 0; fi
echo "ARMED $(date +%H:%M:%S): $(snapshot | wc -l | tr -d ' ') seats, all terminal lines seen"
end=$(( $(date +%s) + MAXM*60 ))
while [ "$(date +%s)" -lt "$end" ]; do
  sleep "$IV"
  u=$(unseen_terminal); if [ -n "$u" ]; then echo "FIRED $(date +%H:%M:%S):"; printf '%s\n' "$u"; mark_fired; exit 0; fi
done
echo "TIMEOUT $(date +%H:%M:%S) after ${MAXM} min, nothing new"
