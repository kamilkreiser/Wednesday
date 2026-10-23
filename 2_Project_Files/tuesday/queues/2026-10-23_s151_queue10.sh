#!/bin/bash
# Tuesday s151 queue 10, 2026-10-23 (REPLACES queue9, stopped 15:2x unlaunched): ONE queue; waits for queue8's bash pid
# ($1) to EXIT (kill -0), then launches G63 (B538, Opus tier-1 gate on MPS #102), THEN waits until no
# Datasec/Security-Composer-* pane is live (B537 Step 0 refuses otherwise) and launches D10 (B537, Opus, Composer demo
# deploy). Order = Kam's project priority (HPSM-POC, then the Calculator, then Composer, 2026-10-23 11:13).
PREV="$1"; LWC=/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/tools/launch_when_cool.sh
BS=/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/brief_seat.sh; BR=/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs
MP='/Volumes/Laptop-DEV/!CODING/Datasec/Datasec MPS Commercial Calculator'
CO='/Volumes/Laptop-DEV/!CODING/Datasec/Datasec Security Composer'
while [ -n "$PREV" ] && kill -0 "$PREV" 2>/dev/null; do sleep 20; done
echo "queue10: previous queue pid $PREV gone at $(date '+%H:%M:%S')"
if tmux list-panes -a -F '#{@cockpit_name}' | /usr/bin/grep -q -x -F 'Datasec/MPS-G63'; then echo "queue10: G63 has a pane, skipped"; else
  tmux select-pane -t %0 2>&1
  WED_USAGE_STOP=100 bash "$LWC" Datasec/MPS-G63 "BRIEF_SEAT_LEVEL=opus bash '$BS' '$MP' '$BR/2026-10-23_B538_SEAT-G63_mps-b518-input-hardening-gate-tier1.md'"; echo "queue10: G63 rc=$? at $(date '+%H:%M:%S')"
fi
while tmux list-panes -a -F '#{@cockpit_name}' | /usr/bin/grep -q -E '^Datasec/Security-Composer-'; do sleep 30; done
echo "queue10: no Composer pane live at $(date '+%H:%M:%S')"
tmux select-pane -t %0 2>&1
WED_USAGE_STOP=100 bash "$LWC" Datasec/Security-Composer-D10 "BRIEF_SEAT_LEVEL=opus bash '$BS' '$CO' '$BR/2026-10-23_B537_SEAT-D10_composer-demo-deploy-main.md'"; echo "queue10: D10 rc=$? at $(date '+%H:%M:%S')"
