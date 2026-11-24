#!/bin/bash
W=/private/tmp/claude-501/qvn2; mkdir -p $W/out/la
for i in 1 2; do
  s=$(date +%s)
  $W/s/inrepo2.sh $W/h $W/th cargo test -p coagent-daemon --locked --lib --test la_bounded --test la_every_decision --test la_mode_as_reported --test la_nothing_kept --test la_nothing_to_peer --test la_source_audit --test la_viewer --test la_wrap > $W/out/la/la_run$i.log 2>&1
  echo "run $i exit $? $(( $(date +%s)-s ))s" >> $W/out/la/la_runs.txt
done
