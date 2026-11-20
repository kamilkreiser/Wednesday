#!/bin/bash
# QA-POLICY-MODE-R2: wait for a heavy slot (count < 3, neither earlier check waiting), then run check.sh once at the head.
W=/private/tmp/claude-501/qpm2
P="/Volumes/Laptop-DEV/!CODING/Claude to Claude/coagent/5_Project_History"
LOG=$W/logs/check_wait.log
while :; do
  n=$(bash /Volumes/Laptop-DEV/FRIDAY/2_Project_Files/fleet/heavy_runs.sh 2>/dev/null)
  m1=$(tail -1 "$P/STATUS_QA_RELAY_RECONNECT.md" | grep -ic 'waiting for a heavy slot')
  m2=$(tail -1 "$P/STATUS_QA_WIN_IPC.md" | grep -ic 'waiting for a heavy slot')
  echo "$(date +%T) heavy=$n relay_wait=$m1 winipc_wait=$m2" >> $LOG
  if [ -n "$n" ] && [ "$n" -lt 3 ] && [ "$m1" = 0 ] && [ "$m2" = 0 ]; then break; fi
  sleep 120
done
echo "$(date +%T) START check.sh (heavy=$n)" >> $LOG
START=$(date +%T)
env -C $W/clone COAGENT_TOOLS=$W/tools CARGO_TARGET_DIR=$W/target bash scripts/check.sh > $W/logs/check.log 2>&1
RC=$?
echo "$(date +%T) END check.sh exit=$RC (started $START)" >> $LOG
exit $RC
