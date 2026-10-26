#!/bin/bash
# s187 queue2 (2026-10-27): waits for the live MPS-M38 launch_when_cool (pid given as $1) to exit, then
# launches HPSM-POC-H40 (B768) through launch_when_cool. ONE launch per queue task (ledger 2026-10-23 w=2:
# a multi-launch queue wakes the coordinator only at its end); B770 (NexusAI-M16) gets its own queue after this exits.
W="$1"
[ -n "$W" ] || { echo "usage: queue2.sh <pid of the live waiter>" >&2; exit 2; }
i=0
while kill -0 "$W" 2>/dev/null; do i=$((i+1)); echo "queue2: waiting on pid $W, beat $i $(date +%H:%M:%S)"; sleep 20; done
echo "queue2: pid $W gone at $(date +%H:%M:%S); launching H40"
WED_USAGE_STOP=100 bash /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/tools/launch_when_cool.sh Datasec/HPSM-POC-H40 "BRIEF_SEAT_LEVEL=sonnet bash '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/brief_seat.sh' '/Volumes/Laptop-DEV/!CODING/Datasec/HPSM-POC' '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-27_B768_SEAT-H40_hpsmpoc-356-228-infra-test-rows.md'"
echo "queue2: launch_when_cool rc=$?"
