#!/bin/bash
# Tuesday s151 queue 11, 2026-10-23: ONE queue at a time; waits for queue10's bash pid ($1) to EXIT (kill -0, never a
# pgrep pattern), then launches M3R (B539, Opus, MPS #99 fix round for round 2) through launch_when_cool.sh.
PREV="$1"; LWC=/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/tools/launch_when_cool.sh
BS=/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/brief_seat.sh; BR=/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs
MP='/Volumes/Laptop-DEV/!CODING/Datasec/Datasec MPS Commercial Calculator'
while [ -n "$PREV" ] && kill -0 "$PREV" 2>/dev/null; do sleep 20; done
echo "queue11: previous queue pid $PREV gone at $(date '+%H:%M:%S')"
if tmux list-panes -a -F '#{@cockpit_name}' | /usr/bin/grep -q -x -F 'Datasec/MPS-M3R'; then echo "queue11: M3R has a pane, skipped"; exit 0; fi
tmux select-pane -t %0 2>&1
WED_USAGE_STOP=100 bash "$LWC" Datasec/MPS-M3R "BRIEF_SEAT_LEVEL=opus bash '$BS' '$MP' '$BR/2026-10-23_B539_SEAT-M3R_mps-b519-fix-round-2.md'"; echo "queue11: M3R rc=$? at $(date '+%H:%M:%S')"
