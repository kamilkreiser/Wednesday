#!/bin/bash
# Watches done.md for operator 79's rows: queues a pass's model line once ITS control shows CONTROL-PASS; runs hold79.sh once its model row shows PASS (7/7).
R=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_spark-operator79; S=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model; B=$S/night/briefs
LOG=$R/watch.log
declare -a PASSES=("a2:ISSUE-ANCHORING-CATCH" "a3:ISSUE-RESERVE-SAVE-CHARGE-CATCHES" "a4:ISSUE-HOLDER-AND-LEGACY-UPDATE-CATCHES" "a5:ISSUE-COMPENSATING-DELETE-CATCH" "a6:REPO-LIST-AND-SHARES-CATCHES" "b1:VERIFICATION-VERIFY-HASH-STATUS-COERCE" "b2:VERIFICATION-VERIFY-FILE-COERCE" "b3:VERIFICATION-V2-COERCE" "b4:RETENTION-SCHEDULER-COERCE")
end=$(( $(date +%s) + 7200 ))
while [ $(date +%s) -lt $end ]; do
  alldone=1
  for pl in "${PASSES[@]}"; do
    k=${pl%%:*}; label=${pl#*:}
    [ -f $R/held_$k.flag ] && continue
    alldone=0
    br=$(ls -d $B/ks_*_o79_${k}_*)
    if [ ! -f $R/queued_$k.flag ] && /usr/bin/grep "o79_${k}_" $S/spark/done.md | /usr/bin/grep -q "CONTROL-PASS"; then
      echo "$br" >> $S/spark/queue.md; touch $R/queued_$k.flag; echo "$(date +%T) queued model $k" >> $LOG
    fi
    if [ -f $R/queued_$k.flag ] && /usr/bin/grep "o79_${k}_" $S/spark/done.md | /usr/bin/grep -v -i "CONTROL-" | /usr/bin/grep -q "PASS (7/7)"; then
      bash /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_spark-operator79/gen/hold79.sh $k KS-1868 $label > $R/hold_$k.log 2>&1; touch $R/held_$k.flag; echo "$(date +%T) held $k" >> $LOG
    fi
  done
  [ $alldone -eq 1 ] && break
  sleep 20
done
echo "$(date +%T) watcher exit" >> $LOG
