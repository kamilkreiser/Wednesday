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
# SPACING (ledger _ledger_laptop_datasec.md 2026-10-22, w=2 of the 10-21 two-waiters row): B463 and B464 launched 44 s
# apart because this waiter checked load only. Now it also waits until GAP_MIN seconds after the last launch it made.
GAP_MIN="${GAP_MIN:-120}"
STAMP="${LWC_STAMP:-$(cd -P "$(dirname "${BASH_SOURCE[0]}")/../../fleet/state" && pwd)/tuesday_lwc_last_launch}"
spaced() { [ ! -f "$STAMP" ] && return 0; [ $(( $(date +%s) - $(cat "$STAMP") )) -ge "$GAP_MIN" ]; }
START=$(date +%s); OK=0
while :; do
  if cool && spaced; then OK=$((OK+1)); else OK=0; fi
  [ "$OK" -ge 2 ] && break
  [ $(( $(date +%s) - START )) -ge "$MAX_WAIT" ] && { echo "GAVE UP after ${MAX_WAIT}s: load1 $(load1) (max $LOAD_MAX), spaced=$(spaced && echo yes || echo "no, last launch < ${GAP_MIN}s ago"); nothing launched ($NAME)"; exit 4; }
  sleep 20
done
echo "LAUNCHING $NAME at $(date '+%H:%M:%S') load1 $(load1) (waited $(( $(date +%s) - START ))s)"
# PANE SPACE (pickup DELTA 475/476, 2026-10-23 s149): `cockpit.sh add` splits the ACTIVE pane, and tmux refuses with
# "no space for a new pane" when that pane is small (12:5x: M4, M16 and G56 failed rc=1 and this waiter just exited).
# Now: on that refusal, make the coordinator pane active, re-apply the cockpit layout, wait, and retry (RETRIES, default
# 3). Any other failure is not retried. The spacing stamp is written only after a launch that succeeded.
# The add's output goes to one overwritten file beside the stamp (never deleted), then is printed.
RETRIES="${RETRIES:-3}"; SELF_PANE="${LWC_SELF_PANE:-%0}"; OUT="${STAMP}.last_add_output"; TRY=0
while :; do
  TRY=$((TRY+1))
  bash "$COCKPIT" add "$NAME" "$CMD" > "$OUT" 2>&1; RC=$?
  cat "$OUT"
  echo "cockpit.sh add rc=$RC at $(date '+%H:%M:%S'); load1 $(load1) (try $TRY of $((RETRIES+1)))"
  [ "$RC" -eq 0 ] && { date +%s > "$STAMP"; break; }
  if /usr/bin/grep -q -i 'no space for a new pane' "$OUT" && [ "$TRY" -le "$RETRIES" ]; then
    echo "PANE SPACE refusal for $NAME: selecting $SELF_PANE and re-applying the layout, retry in ${LWC_RETRY_SLEEP:-30} s"
    tmux select-pane -t "$SELF_PANE" 2>&1
    bash "$COCKPIT" layout 2>&1 | tail -n 3
    sleep "${LWC_RETRY_SLEEP:-30}"
    continue
  fi
  echo "REFUSED: $NAME NOT launched (rc $RC after $TRY tries). Read the output above; nothing was started."
  break
done
exit $RC
