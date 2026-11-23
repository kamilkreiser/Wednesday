#!/bin/bash
W=/private/tmp/claude-501/qla2
for i in 1 2 3; do
  s=$(date +%s)
  $W/inrepo.sh $W/clone $W/thead cargo test -p coagent-daemon --locked --lib --test la_bounded --test la_every_decision --test la_mode_as_reported --test la_nothing_kept --test la_nothing_to_peer --test la_source_audit --test la_viewer --test la_wrap > $W/o/la_run$i.log 2>&1
  echo "run $i exit $? $(( $(date +%s)-s ))s" >> $W/o/la_runs.txt
done
