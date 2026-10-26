#!/bin/bash
# s187 queue3 (2026-10-27): waits for the live MPS-M38 launch_when_cool (pid given as $1) to exit, then
# launches NexusAI-M16 (B770) through launch_when_cool. ONE launch per queue task (ledger 2026-10-23 w=2:
# a multi-launch queue wakes the coordinator only at its end); last queue of s187.
W="$1"
[ -n "$W" ] || { echo "usage: queue3.sh <pid of the live waiter>" >&2; exit 2; }
i=0
while kill -0 "$W" 2>/dev/null; do i=$((i+1)); echo "queue3: waiting on pid $W, beat $i $(date +%H:%M:%S)"; sleep 20; done
echo "queue3: pid $W gone at $(date +%H:%M:%S); launching M16"
WED_USAGE_STOP=100 bash /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/tools/launch_when_cool.sh Datasec/NexusAI-M16 "BRIEF_SEAT_LEVEL=sonnet bash '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/brief_seat.sh' '/Volumes/Laptop-DEV/!CODING/Datasec/NexusAI' '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-27_B770_SEAT-M16_nexusai-873-codeql-test-reshape.md'"
echo "queue3: launch_when_cool rc=$?"
