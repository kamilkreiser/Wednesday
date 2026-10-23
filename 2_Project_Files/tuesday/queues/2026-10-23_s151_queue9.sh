#!/bin/bash
# Tuesday s151 queue 9, 2026-10-23: ONE queue at a time; waits for queue8's bash pid ($1) to EXIT (kill -0, never a
# pgrep pattern), THEN for the Composer records seat's pane (Datasec/Security-Composer-R24) to be gone (B537's Step 0
# refuses while another Composer pane is live), then launches D10 (B537, Opus, Composer demo deploy) via launch_when_cool.sh.
PREV="$1"; LWC=/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/tools/launch_when_cool.sh
BS=/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/brief_seat.sh; BR=/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs
CO='/Volumes/Laptop-DEV/!CODING/Datasec/Datasec Security Composer'
while [ -n "$PREV" ] && kill -0 "$PREV" 2>/dev/null; do sleep 20; done
echo "queue9: previous queue pid $PREV gone at $(date '+%H:%M:%S')"
while tmux list-panes -a -F '#{@cockpit_name}' | /usr/bin/grep -q -E '^Datasec/Security-Composer-'; do sleep 30; done
echo "queue9: no Composer pane live at $(date '+%H:%M:%S')"
tmux select-pane -t %0 2>&1
WED_USAGE_STOP=100 bash "$LWC" Datasec/Security-Composer-D10 "BRIEF_SEAT_LEVEL=opus bash '$BS' '$CO' '$BR/2026-10-23_B537_SEAT-D10_composer-demo-deploy-main.md'"; echo "queue9: D10 rc=$? at $(date '+%H:%M:%S')"
