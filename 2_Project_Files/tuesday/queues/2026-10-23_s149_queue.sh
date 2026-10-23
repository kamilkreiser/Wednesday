#!/bin/bash
# Tuesday s149 launch queue, 2026-10-23: ONE queue (ledger 2026-10-21 two-waiters row).
# Waits for the H4 waiter (pid given as $1) to exit by PID (never a pgrep pattern: ledger 2026-10-22
# self-matching deadlock), then launches each seat in order through launch_when_cool.sh, which waits for
# load1 < 7 on two reads and 120 s since the previous launch. Priority order HPSM-POC -> MPS (Kam 11:13).
WAIT_PID="${1:-}"
LWC=/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/tools/launch_when_cool.sh
BS=/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/brief_seat.sh
BR=/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs
HP='/Volumes/Laptop-DEV/!CODING/Datasec/HPSM-POC'
MP='/Volumes/Laptop-DEV/!CODING/Datasec/Datasec MPS Commercial Calculator'
if [ -n "$WAIT_PID" ]; then
  while kill -0 "$WAIT_PID" 2>/dev/null; do sleep 15; done
  echo "queue: waiter $WAIT_PID gone at $(date '+%H:%M:%S')"
fi
run() { # name level project brief
  echo "queue: next $1 at $(date '+%H:%M:%S')"
  WED_USAGE_STOP=100 bash "$LWC" "$1" "BRIEF_SEAT_LEVEL=$2 bash '$BS' '$3' '$BR/$4'"
  echo "queue: $1 rc=$? at $(date '+%H:%M:%S')"
}
run Datasec/HPSM-POC-H5 sonnet "$HP" 2026-10-23_B516_SEAT-H5_hpsmpoc-n1-lease-lost-flake.md
run Datasec/MPS-M2 sonnet "$MP" 2026-10-23_B518_SEAT-M2_mps-api-input-hardening.md
run Datasec/MPS-M3 opus "$MP" 2026-10-23_B519_SEAT-M3_mps-pricing-policy-leak-tests.md
run Datasec/MPS-M4 sonnet "$MP" 2026-10-23_B520_SEAT-M4_mps-source-lifecycle-hardening.md
run Datasec/MPS-M16 sonnet "$MP" 2026-10-23_B522_SEAT-M16_mps-deal-usage-colour-row.md
echo "queue: done at $(date '+%H:%M:%S')"
