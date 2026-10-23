#!/bin/bash
# Tuesday s149 launch queue 2, 2026-10-23: the two MPS lanes whose first launch failed at 12:34 and 12:50 with
# tmux "no space for a new pane" (cockpit window 180x36 full at 11 panes). Three held builders (F3, H2, M1) were
# closed to free room. ONE chain: waits on the G56 waiter's pid ($1) by PID, then M4, then M16, each through
# launch_when_cool.sh (load1 < 7 on two reads, 120 s since the previous launch).
WAIT_PID="${1:-}"
LWC=/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/tools/launch_when_cool.sh
BS=/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/brief_seat.sh
BR=/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs
MP='/Volumes/Laptop-DEV/!CODING/Datasec/Datasec MPS Commercial Calculator'
if [ -n "$WAIT_PID" ]; then
  while kill -0 "$WAIT_PID" 2>/dev/null; do sleep 15; done
  echo "queue2: waiter $WAIT_PID gone at $(date '+%H:%M:%S')"
fi
run() { # name level project brief
  echo "queue2: next $1 at $(date '+%H:%M:%S')"
  WED_USAGE_STOP=100 bash "$LWC" "$1" "BRIEF_SEAT_LEVEL=$2 bash '$BS' '$3' '$BR/$4'"
  echo "queue2: $1 rc=$? at $(date '+%H:%M:%S')"
}
run Datasec/MPS-M4 sonnet "$MP" 2026-10-23_B520_SEAT-M4_mps-source-lifecycle-hardening.md
run Datasec/MPS-M16 sonnet "$MP" 2026-10-23_B522_SEAT-M16_mps-deal-usage-colour-row.md
echo "queue2: done at $(date '+%H:%M:%S')"
