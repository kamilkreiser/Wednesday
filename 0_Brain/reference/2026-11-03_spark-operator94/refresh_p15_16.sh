#!/bin/bash
O=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_spark-operator94; S=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model
cat > $O/advance94.sh <<'EOF'
#!/bin/bash
# queue the model line for each o94 pass whose CONTROL-PASS row exists (newer than ctlafter_<pN> if that marker exists) and which was not queued yet
S=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model; D=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_spark-operator94
touch $D/queued_models.txt
for d in $S/night/briefs/ks_1868_o94_p*; do
  b=$(basename $d); k=$(echo $b | sed 's/ks_1868_o94_\(p[0-9]*\)_.*/\1/')
  after="0000"; [ -f $D/ctlafter_$k ] && after=$(cat $D/ctlafter_$k)
  cp=$(/usr/bin/grep -F "$b" $S/spark/done.md | /usr/bin/grep 'CONTROL-PASS' | awk -F'|' -v a="$after" '{t=$2; gsub(/^ +| +$/,"",t); if (t>=a) n++} END{print n+0}')
  q=$(/usr/bin/grep -c -x "$k" $D/queued_models.txt)
  echo "$k ctlpass=$cp queued=$q"
  if [ "$cp" -ge 1 ] && [ "$q" -eq 0 ]; then echo "$d" >> $S/spark/queue.md; echo $k >> $D/queued_models.txt; echo "  -> queued model line for $k"; fi
done
EOF
now=$(date '+%F %T'); for k in p4 p9 p10 p15 p16; do echo "$now" > $O/ctlafter_$k; done
python3 - <<'EOF'
import re
O='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_spark-operator94/'
q=O+'queued_models.txt'; L=[l for l in open(q).read().split() if l not in ('p4','p9','p10','p15','p16')]
open(q,'w').write('\n'.join(L)+'\n')
Q='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/queue.md'
lines=open(Q).read().split('\n'); out=[]
for l in lines:
    if (not l.startswith('#')) and '--control' not in l and re.search(r'_o94_p(15|16)_',l):
        print('removed model line',l[-60:]); continue
    out.append(l)
open(Q,'w').write('\n'.join(out))
EOF
for k in p15 p16; do KEEPBLANK=p4,p9,p10,p15,p16 bash $O/gen/run_mk.sh $k | head -1; bash $O/ld.sh $k | head -1; echo "$S/night/briefs/$(ls $S/night/briefs | /usr/bin/grep o94_${k}_) --control" >> $S/spark/queue.md; git -C /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_spark-operator94/repo apply --check -p1 $S/night/briefs/$(ls $S/night/briefs | /usr/bin/grep o94_${k}_)/golden.diff && echo "$k strict OK"; done
echo "p15/p16 goldens rebuilt with blank context (before their model round ran) $(date +%T)" >> $O/notes.txt
