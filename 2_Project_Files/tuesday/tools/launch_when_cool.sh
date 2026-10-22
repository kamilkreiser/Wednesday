#!/bin/bash
# launch_when_cool.sh <cockpit name> <command string for cockpit.sh add>
#
# Waits until the machine's 1-minute load is below LOAD_MAX (default 7) on TWO consecutive reads 20 s apart,
# then runs `cockpit.sh add <name> "<command>"` ONCE, prints the result and exits. Run it as a tracked
# background task (run_in_background), never disowned: its exit is the wake to verify the launch at rung 5.
#
# WHY (ledger _ledger_laptop_datasec.md 2026-10-21, w=3 load-in-same-command + the 09:32 two-waiters row): a load read
# printed beside the launch can stop nothing, and two independent waiters fire together in one dip. So: ONE waiter at a
# time (the seat starts the next only after this one exits and the launch is verified), the load read is inside the
# waiter, and two consecutive reads are required so a single dip does not count.
# Bounded: gives up after MAX_WAIT seconds (default 3600) with rc 4 and launches nothing.
NAME="$1"; CMD="$2"
[ -n "$NAME" ] && [ -n "$CMD" ] || { echo "usage: launch_when_cool.sh <cockpit name> <command>" >&2; exit 2; }
LOAD_MAX="${LOAD_MAX:-7}"; MAX_WAIT="${MAX_WAIT:-3600}"
COCKPIT="${LWC_COCKPIT:-$(cd -P "$(dirname "${BASH_SOURCE[0]}")/../../fleet/cockpit" && pwd)/cockpit.sh}"   # LWC_COCKPIT: test stub only
[ -x "$COCKPIT" ] || [ -f "$COCKPIT" ] || { echo "REFUSED: cockpit.sh not found at $COCKPIT" >&2; exit 3; }
load1() { sysctl -n vm.loadavg | awk '{print $2}'; }
cool() { awk -v l="$(load1)" -v m="$LOAD_MAX" 'BEGIN{exit !(l < m)}'; }
START=$(date +%s); OK=0
while :; do
  if cool; then OK=$((OK+1)); else OK=0; fi
  [ "$OK" -ge 2 ] && break
  [ $(( $(date +%s) - START )) -ge "$MAX_WAIT" ] && { echo "GAVE UP: load1 $(load1) still >= $LOAD_MAX after ${MAX_WAIT}s; nothing launched ($NAME)"; exit 4; }
  sleep 20
done
echo "LAUNCHING $NAME at $(date '+%H:%M:%S') load1 $(load1) (waited $(( $(date +%s) - START ))s)"
bash "$COCKPIT" add "$NAME" "$CMD"; RC=$?
echo "cockpit.sh add rc=$RC at $(date '+%H:%M:%S'); load1 $(load1)"
exit $RC
