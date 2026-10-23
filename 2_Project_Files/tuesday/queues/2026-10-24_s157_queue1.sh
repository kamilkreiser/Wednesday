#!/bin/bash
# s157 queue 1: B574 (MPS #104 fix round, SEAT-M12) launches only AFTER B573's waiter (pid given as $1)
# has exited (it launched M11), then 120 s, then launch_when_cool (load1 < 7). One waiter at a time
# (ledger 2026-10-21 / 10-23 two-waiters rows); waits on a PID, never pgrep -f (ledger 2026-10-22).
P="${1:?usage: queue1.sh <B573 waiter pid>}"
[ "$P" != 1 ] || { echo "refusing pid 1"; exit 2; }
i=0; while kill -0 "$P" 2>/dev/null; do i=$((i+1)); echo "$(date +%H:%M:%S) waiting on B573 waiter pid $P (beat $i)"; sleep 30; done
echo "$(date +%H:%M:%S) B573 waiter $P exited; spacing 120 s"; sleep 120
exec env WED_USAGE_STOP=100 bash /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/tools/launch_when_cool.sh Datasec/MPS-M12 "BRIEF_SEAT_LEVEL=sonnet bash '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/brief_seat.sh' '/Volumes/Laptop-DEV/!CODING/Datasec/Datasec MPS Commercial Calculator' '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-24_B574_SEAT-M12_mps-104-fix-round-2.md'"
