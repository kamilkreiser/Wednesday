#!/bin/bash
# Tuesday s151 queue 8, 2026-10-23: ONE queue at a time; waits for queue7's bash pid ($1) to EXIT (kill -0, never a
# pgrep pattern), then launches G62 (B536, tier-2 Sonnet batched gate on HPSM-POC PRs #200 + #201) through launch_when_cool.sh.
PREV="$1"; LWC=/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/tools/launch_when_cool.sh
BS=/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/brief_seat.sh; BR=/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs
HP='/Volumes/Laptop-DEV/!CODING/Datasec/HPSM-POC'
while [ -n "$PREV" ] && kill -0 "$PREV" 2>/dev/null; do sleep 20; done
echo "queue8: previous queue pid $PREV gone at $(date '+%H:%M:%S')"
if tmux list-panes -a -F '#{@cockpit_name}' | /usr/bin/grep -q -x -F 'Datasec/HPSM-POC-G62'; then echo "queue8: G62 has a pane, skipped"; exit 0; fi
tmux select-pane -t %0 2>&1
WED_USAGE_STOP=100 bash "$LWC" Datasec/HPSM-POC-G62 "BRIEF_SEAT_LEVEL=sonnet bash '$BS' '$HP' '$BR/2026-10-23_B536_SEAT-G62_hpsmpoc-b515-b516-batch-gate-tier2.md'"; echo "queue8: G62 rc=$? at $(date '+%H:%M:%S')"
