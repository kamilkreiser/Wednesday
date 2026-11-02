#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate104-ks1868-pr1923; R=$W/repo; RUNS=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs
MB=04ff5262ad526a13c1a0df99480b76860a8d11d1; WT=$W/apply_wt2
{
git -C $W/apply_wt diff --cached --quiet $MB -- Blockchain/Dev && echo "control: forward tree equals BASE (instrument broken)" || echo "control: forward tree differs from base (instrument fires)"
test -e $WT && { echo exists; exit 2; }
git -C $R worktree add -q --detach $WT $MB
for p in o67_p1 o67_p2 o67_p3 o67_p4 o68_p3; do D=$(ls -d $RUNS/spark_secuura_2026-11-02_ks_1868_${p}_* | grep -v -- '-control' | head -1); echo "$p section_1 hunks: $(grep '^@@' $D/out.md.checker/section_1.diff | tr '\n' ' ')"; done
echo "REVERSE ORDER (P2 before P1, P4 before P3), product sections only, verbose:"
for p in o67_p2 o67_p1 o67_p4 o67_p3 o68_p3; do D=$(ls -d $RUNS/spark_secuura_2026-11-02_ks_1868_${p}_* | grep -v -- '-control' | head -1)
  git -C $WT apply -v -p1 $D/out.md.checker/section_1.diff 2>&1 | tr '\n' ' '; echo " $p rc=$?"; done
for f in signatories.ts thirdPartyVerifiers.ts; do cmp -s $WT/Blockchain/Dev/services/originate/src/routes/$f <(git -C $R show pr1923:Blockchain/Dev/services/originate/src/routes/$f) && echo "reverse $f equals head" || echo "reverse $f DIFFERS from head"; done
echo "FORWARD ORDER verbose re-check (offsets) in a fresh tree:"
git -C $R worktree remove --force $WT; git -C $R worktree add -q --detach $WT $MB
for p in o67_p1 o67_p2 o67_p3 o67_p4 o68_p3; do D=$(ls -d $RUNS/spark_secuura_2026-11-02_ks_1868_${p}_* | grep -v -- '-control' | head -1)
  git -C $WT apply -v -p1 $D/out.md.checker/section_1.diff 2>&1 | tr '\n' ' '; echo " $p rc=$?"; done
git -C $R worktree remove --force $WT
} > $W/logs/apply_order2.log 2>&1
cat $W/logs/apply_order2.log
