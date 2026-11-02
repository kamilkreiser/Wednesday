#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate122-ks1939-pr1940
WT=$W/wt_apply; R=$W/repo; L=$W/logs; RU=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs
P1=$RU/spark_secuura_2026-11-02_ks_1939_o78_p1_originate_verification_by_id_existence_answer_is_awaited
P2=$RU/spark_secuura_2026-11-02_ks_1939_o78_p2_originate_verification_lookup_catch_unreadable_throw
[ -e $WT ] || git -C $R worktree add -q --detach $WT e2a2426d221d8bd672e97c43c6bbcd6c4027b350
echo "wt HEAD $(git -C $WT rev-parse HEAD)"
for s in $P1/out.md.checker/section_1.diff $P1/out.md.checker/section_2.diff $P2/out.md.checker/section_1.diff $P2/out.md.checker/section_2.diff; do
  echo "apply $(basename $(dirname $(dirname $s)))/$(basename $s)"; git -C $WT apply -v $s 2>&1 | /usr/bin/grep -v '^Checking'; echo rc=${PIPESTATUS[0]}; done
for f in Blockchain/Dev/services/originate/src/routes/verification.ts Blockchain/Dev/services/originate/src/__tests__/ks1939-verification-by-id-existence-answer-throw-is-answered.test.ts Blockchain/Dev/services/originate/src/__tests__/ks1939-verification-lookup-catch-unreadable-throw.test.ts; do
  a=$(git -C $WT hash-object $WT/$f); b=$(git -C $R rev-parse 96208f377d14:$f); echo "$f applied=$a pr=$b $([ $a = $b ] && echo IDENTICAL || echo DIFFERENT)"; done
for p in $P1 $P2; do cmp $p/out.md.checker/patch.diff $p-control/out.md.checker/patch.diff && echo "$(basename $p) control identical"; done
