#!/bin/bash
D=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate116-ks1413-pr1934; R=$D/repo
git -C $R worktree add -f $D/wt_base 8f313815f415 >/dev/null 2>&1
git -C $R worktree add -f $D/wt_head pr1934 >/dev/null 2>&1
SIB=$(git -C $D/wt_head grep -lE 'start-secuura\.sh|start-local\.sh' -- 'Blockchain/Dev/scripts/__tests__/*.test.sh' 'Start_Up/*.test.sh' 'Start_Up/**/*.test.sh')
echo "$SIB" > $D/logs/siblings.txt; echo "siblings: $(echo "$SIB" | wc -l)"
for T in base head; do
  W=$D/wt_$T; : > $D/logs/suites_$T.log
  for f in $SIB; do
    [ -f $W/$f ] || { echo "MISSING $f" >> $D/logs/suites_$T.log; continue; }
    out=$(bash $W/$f 2>&1); rc=$?
    echo "rc=$rc $f :: $(echo "$out" | grep -E 'passed|PASS|FAIL' | tail -1)" >> $D/logs/suites_$T.log
  done
done
echo "--- new suite at head"; bash $D/wt_head/Blockchain/Dev/scripts/__tests__/ks1413_start_banners_print_no_demo_password.test.sh > $D/logs/new_head.log 2>&1; echo rc=$?
echo "--- new suite at base"
cp $D/wt_head/Blockchain/Dev/scripts/__tests__/ks1413_start_banners_print_no_demo_password.test.sh $D/wt_base/Blockchain/Dev/scripts/__tests__/
bash $D/wt_base/Blockchain/Dev/scripts/__tests__/ks1413_start_banners_print_no_demo_password.test.sh > $D/logs/new_base.log 2>&1; echo rc=$?
