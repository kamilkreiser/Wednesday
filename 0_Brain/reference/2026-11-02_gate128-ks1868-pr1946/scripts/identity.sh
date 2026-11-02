#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate128-ks1868-pr1946
R=$W/repo
P=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o79_b4_originate_retention_scheduler_guard_coerces_message/out.md.checker
S=$W/scratch_base; test ! -e $S || { echo scratch exists; exit 1; }; mkdir -p $S
git -C $R archive e2a2426d221d | tar -x -C $S
cat $P/section_1.diff $P/section_2.diff | cmp - $P/patch.diff; echo cmp_rc=$?
grep '^+++' $P/section_1.diff $P/section_2.diff
for s in section_1 section_2; do (cd $S && patch -p1 --dry-run < $P/$s.diff >/dev/null; echo dry_$s=$?; patch -p1 < $P/$s.diff >/dev/null; echo apply_$s=$?); done
T=Blockchain/Dev/services/originate/src
for f in services/retentionScheduler.ts __tests__/ks1868-retention-scheduler-guard-coerces-message-o79b4.test.ts; do
 echo "$f held: $(shasum -a 256 $S/$T/$f|cut -c1-16)"
 echo "$f c1  : $(git -C $R show 5bc7b5f5bce4:$T/$f|shasum -a 256|cut -c1-16)"
 echo "$f head: $(git -C $R show pr1946:$T/$f|shasum -a 256|cut -c1-16)"
done
git -C $R diff --stat 5bc7b5f5bce4 pr1946
for k in cheat flow; do f="Projects Documents/fragments/$k/KS-1868-originate-retention-scheduler-guard-coerces-message.html"; echo "$k c1: $(git -C $R show 5bc7b5f5bce4:"$f" | shasum -a 256|cut -c1-16) pr: $(git -C $R show pr1946:"$f" | shasum -a 256|cut -c1-16)"; done
git -C $R diff --name-only 5bc7b5f5bce4~1 5bc7b5f5bce4
