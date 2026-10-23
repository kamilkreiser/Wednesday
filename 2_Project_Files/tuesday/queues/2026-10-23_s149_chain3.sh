#!/bin/bash
# Tuesday s149 restart chain, 2026-10-23. The s149 queues and waiters were background tasks of the s149 session
# and die with its pane at rotation. A successor runs THIS ONE script (as a tracked background task) to finish the
# launches: M16 (B522), G56 (B523, PR #196), G57 (B524, MPS #98), G58 (B525, PRs #197 + #198), in that order,
# ONE at a time through launch_when_cool.sh (load1 < 7 on two reads, 120 s spacing). A seat whose pane already
# exists is SKIPPED (it launched before the rotation). Before each launch the coordinator pane %0 is made active,
# because cockpit.sh add splits the ACTIVE pane (12:53 refusal: the 2-row fleet-monitor was active).
LWC=/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/tools/launch_when_cool.sh
BS=/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/brief_seat.sh
BR=/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs
HP='/Volumes/Laptop-DEV/!CODING/Datasec/HPSM-POC'
MP='/Volumes/Laptop-DEV/!CODING/Datasec/Datasec MPS Commercial Calculator'
SELF="${CHAIN_SELF_PANE:-%0}"
run() { # name level project brief
  if tmux list-panes -a -F '#{@cockpit_name}' | /usr/bin/grep -q -x -F "$1"; then
    echo "chain3: $1 already has a pane, skipped at $(date '+%H:%M:%S')"; return 0
  fi
  echo "chain3: next $1 at $(date '+%H:%M:%S')"
  tmux select-pane -t "$SELF" 2>/dev/null
  WED_USAGE_STOP=100 bash "$LWC" "$1" "BRIEF_SEAT_LEVEL=$2 bash '$BS' '$3' '$BR/$4'"
  echo "chain3: $1 rc=$? at $(date '+%H:%M:%S')"
}
run Datasec/MPS-M16 sonnet "$MP" 2026-10-23_B522_SEAT-M16_mps-deal-usage-colour-row.md
run Datasec/HPSM-POC-G56 sonnet "$HP" 2026-10-23_B523_SEAT-G56_hpsmpoc-b510-gate-tier2.md
run Datasec/MPS-G57 sonnet "$MP" 2026-10-23_B524_SEAT-G57_mps-b517-docs-gate-tier2.md
run Datasec/HPSM-POC-G58 sonnet "$HP" 2026-10-23_B525_SEAT-G58_hpsmpoc-b512-b513-batch-gate-tier2.md
echo "chain3: done at $(date '+%H:%M:%S')"
