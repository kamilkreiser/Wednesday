#!/bin/bash
# QA-VIEWER-NEXT: cargo fetch --locked, then plain workspace builds of main (m -> tm) and head (h -> th) from EMPTY target dirs.
W=/private/tmp/claude-501/qvx; O=$W/out/build; mkdir -p $O
for t in m h; do
  s=$(date +%s); bash $W/s/inrepo.sh $W/$t $W/t$t cargo fetch --locked > $O/fetch_$t.log 2>&1; echo "fetch $t exit $? $(( $(date +%s)-s ))s" >> $O/runs.txt
done
for t in m h; do
  [ -e $W/t$t ] && { echo "t$t exists, not empty-start" >> $O/runs.txt; continue; }
  s=$(date +%s); bash $W/s/inrepo.sh $W/$t $W/t$t cargo build --workspace --locked > $O/build_$t.log 2>&1; echo "build $t exit $? $(( $(date +%s)-s ))s compiled=$(grep -c '^ *Compiling' $O/build_$t.log)" >> $O/runs.txt
done
echo DONE >> $O/runs.txt
