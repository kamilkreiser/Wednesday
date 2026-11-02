#!/bin/bash
# queue the model line for each o89 pass whose CONTROL-PASS row exists and which was not queued yet; print status
S=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model; D=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_spark-operator89
touch $D/queued_models.txt
for d in $S/night/briefs/ks_1868_o89_[pq]*; do
  b=$(basename $d); k=$(echo $b | sed 's/ks_1868_o89_\([pq][0-9]*\)_.*/\1/')
  cp=$(/usr/bin/grep -F "$b" $S/spark/done.md | /usr/bin/grep -c 'CONTROL-PASS')
  cf=$(/usr/bin/grep -F "$b" $S/spark/done.md | /usr/bin/grep -c 'CONTROL-FAIL')
  mr=$(/usr/bin/grep -F "$b" $S/spark/done.md | /usr/bin/grep -v 'CONTROL-' | /usr/bin/grep -c -E '\| (PASS|FAIL)')
  q=$(/usr/bin/grep -c -x "$k" $D/queued_models.txt)
  echo "$k ctlpass=$cp ctlfail=$cf modelrows=$mr queued=$q"
  if [ "$cp" -ge 1 ] && [ "$q" -eq 0 ]; then echo "$d" >> $S/spark/queue.md; echo $k >> $D/queued_models.txt; echo "  -> queued model line for $k"; fi
done
