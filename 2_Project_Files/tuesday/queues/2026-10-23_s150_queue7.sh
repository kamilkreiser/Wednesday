#!/bin/bash
# Tuesday s150 queue 7, 2026-10-23: ONE queue at a time; waits for queue6's bash pid ($1) to EXIT (kill -0, never a
# pgrep pattern), then launches G61 (B535, tier-2 Sonnet gate on MPS PR #101) through launch_when_cool.sh.
PREV="$1"; LWC=/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/tools/launch_when_cool.sh
BS=/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/brief_seat.sh; BR=/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs
MP='/Volumes/Laptop-DEV/!CODING/Datasec/Datasec MPS Commercial Calculator'
while [ -n "$PREV" ] && kill -0 "$PREV" 2>/dev/null; do sleep 20; done
echo "queue7: previous queue pid $PREV gone at $(date '+%H:%M:%S')"
if tmux list-panes -a -F '#{@cockpit_name}' | /usr/bin/grep -q -x -F 'Datasec/MPS-G61'; then echo "queue7: G61 has a pane, skipped"; exit 0; fi
tmux select-pane -t %0 2>&1
WED_USAGE_STOP=100 bash "$LWC" Datasec/MPS-G61 "BRIEF_SEAT_LEVEL=sonnet bash '$BS' '$MP' '$BR/2026-10-23_B535_SEAT-G61_mps-b522-deal-usage-colour-row-gate-tier2.md'"; echo "queue7: G61 rc=$? at $(date '+%H:%M:%S')"
