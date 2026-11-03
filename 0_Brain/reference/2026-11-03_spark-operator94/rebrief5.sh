#!/bin/bash
O=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_spark-operator94; S=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model
now=$(date '+%F %T')
for k in p4 p9 p10 p15 p16; do
  echo "$now" > $O/ctlafter_$k
  unset KEEPBLANK; bash $O/gen/run_mk.sh $k | head -1
  bash $O/ld.sh $k | head -1
  d=$S/night/briefs/$(ls $S/night/briefs | /usr/bin/grep o94_${k}_)
  git -C /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_spark-operator94/repo apply --check -p1 $d/golden.diff && echo "$k strict OK"
  echo "$d --control" >> $S/spark/queue.md
done
python3 - <<'EOF'
q='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_spark-operator94/queued_models.txt'
L=[l for l in open(q).read().split() if l not in ('p4','p9','p10','p15','p16')]
open(q,'w').write('\n'.join(L)+'\n')
EOF
