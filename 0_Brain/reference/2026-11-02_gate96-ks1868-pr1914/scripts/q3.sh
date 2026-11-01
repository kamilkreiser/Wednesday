#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate96-ks1868-pr1914
RR=$W/repo
RUNS=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs
P=Blockchain/Dev/services/analytics/src/routes/analytics.ts
T=$W/logs/q3; mkdir -p $T
BASE=03977e89a343ad7362760e4fb0270602fb6da5ce
git -C $RR show $BASE:$P > $T/base.ts
git -C $RR show refs/qa/pr1914:$P > $T/head.ts
echo base sha $(shasum -a 256 $T/base.ts | cut -c1-16) head sha $(shasum -a 256 $T/head.ts | cut -c1-16)
mkdir -p $T/cum/$(dirname $P); cp $T/base.ts $T/cum/$P
for pass in o61_p1 o61_p2 o60_p1 o61_p3; do
  D=$(ls -d $RUNS/spark_secuura_2026-11-02_ks_1868_${pass}_* | grep -v -- -control)
  echo $pass: $(basename $D | cut -c1-60)
  mkdir -p $T/s_$pass/$(dirname $P); cp $T/base.ts $T/s_$pass/$P
  patch -s -p1 -d $T/s_$pass < $D/out.md.checker/section_1.diff; echo alone_apply_rc=$?
  patch -s -p1 -d $T/cum < $D/out.md.checker/section_1.diff; echo cum_apply_rc=$?
  # hunk -/+ content: PR diff vs this pass alone at U0
  diff <(git diff --no-index -U0 $T/base.ts $T/s_$pass/$P | grep -E '^[-+][^-+]|^[-+]$' ) /dev/null > /dev/null
  git diff --no-index -U0 $T/base.ts $T/s_$pass/$P | grep -E '^[-+]' | grep -vE '^(\+\+\+|---)' | sort > $T/held_$pass.pm
  echo   held lines: $(wc -l < $T/held_$pass.pm)
  # which of those lines are in PR diff (multiset subset check)
done
git diff --no-index -U0 $T/base.ts $T/head.ts | grep -E '^[-+]' | grep -vE '^(\+\+\+|---)' | sort > $T/pr.pm
cat $T/held_*.pm | sort > $T/held_all.pm
echo pr lines $(wc -l < $T/pr.pm) held-all lines $(wc -l < $T/held_all.pm)
diff $T/pr.pm $T/held_all.pm > /dev/null && echo MULTISET_EQUAL || echo MULTISET_DIFF
if cmp -s $T/cum/$P $T/head.ts; then echo CUMULATIVE_BYTE_EQUAL_TO_PR_HEAD_FILE; else echo CUM_DIFFERS; fi
