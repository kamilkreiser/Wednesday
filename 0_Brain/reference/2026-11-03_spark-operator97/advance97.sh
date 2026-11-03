#!/bin/bash
# queue the model line for each o97 pass whose CONTROL-PASS row exists (newer than ctlafter_<pN> if that marker exists) and which was not queued yet
S=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model; D=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_spark-operator97
touch $D/queued_models.txt
for d in $S/night/briefs/ks_1868_o97_p*; do
  b=$(basename $d); k=$(echo $b | sed 's/ks_1868_o97_\(p[0-9]*\)_.*/\1/')
  after="0000"; [ -f $D/ctlafter_$k ] && after=$(cat $D/ctlafter_$k)
  cp=$(/usr/bin/grep -F "$b" $S/spark/done.md | /usr/bin/grep 'CONTROL-PASS' | awk -F'|' -v a="$after" '{t=$2; gsub(/^ +| +$/,"",t); if (t>=a) n++} END{print n+0}')
  q=$(/usr/bin/grep -c -x "$k" $D/queued_models.txt)
  echo "$k ctlpass=$cp queued=$q"
  if [ "$cp" -ge 1 ] && [ "$q" -eq 0 ]; then echo "$d" >> $S/spark/queue.md; echo $k >> $D/queued_models.txt; echo "  -> queued model line for $k"; fi
done
