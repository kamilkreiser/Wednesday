#!/bin/bash
# Tuesday s150 queue 4, 2026-10-23. ONE queue at a time (ledger 2026-10-21 two-waiters row): waits for the s149 chain3
# process (pid passed as $1) to EXIT by pid (never a pgrep pattern: ledger 2026-10-22 self-matching wait), then launches
# each seat in order through launch_when_cool.sh (load1 < 7 twice, 120 s spacing, pane-space retry).
CHAIN_PID="$1"; LWC=/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/tools/launch_when_cool.sh
BS=/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/brief_seat.sh; BR=/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs
CO='/Volumes/Laptop-DEV/!CODING/Datasec/Datasec Security Composer'
while [ -n "$CHAIN_PID" ] && kill -0 "$CHAIN_PID" 2>/dev/null; do sleep 20; done
echo "queue4: chain pid $CHAIN_PID gone at $(date '+%H:%M:%S')"
run() { # name level project brief
  if tmux list-panes -a -F '#{@cockpit_name}' | /usr/bin/grep -q -x -F "$1"; then echo "queue4: $1 has a pane, skipped"; return 0; fi
  tmux select-pane -t %0 2>&1
  WED_USAGE_STOP=100 bash "$LWC" "$1" "BRIEF_SEAT_LEVEL=$2 bash '$BS' '$3' '$BR/$4'"; echo "queue4: $1 rc=$? at $(date '+%H:%M:%S')"
}
run Datasec/Security-Composer-R24 sonnet "$CO" 2026-10-23_B532_SEAT-R24_composer-records-fold-approval.md
echo "queue4: done at $(date '+%H:%M:%S')"
