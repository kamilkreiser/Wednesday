#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate105-ks1868-pr1924
R=$W/repo; RUNS=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs; L=$W/logs/apply_order.log
MB=fcfa5dfdba9b5fe1b4a7c4619403ff3d0e2fe54c
WT=$W/apply_wt
test -e $WT && { echo "worktree path exists"; exit 2; }
git -C $R worktree add -q --detach $WT $MB
{
want(){ case $1 in o69_p1) echo ee6bc738c6664da054833340dfbfde0fb5ea1931ccb50799f0fa4dbda8918f5a;; o69_p2) echo c91f61e7b142cf9aeff065078de58048619fff42d2e42bca0f0f61fc957d9fe2;; o69_p3) echo 0317440f3deb211ece4634364a261360c50f6ea32ea53bf4becf546987ec18ba;; esac; }
for p in o69_p1 o69_p2 o69_p3; do
  D=$(ls -d $RUNS/spark_secuura_2026-11-02_ks_1868_${p}_* | grep -v -- '-control$' | head -1)
  C=$D/out.md.checker
  s=$(shasum -a 256 $C/patch.diff | awk '{print $1}')
  echo "$p patchsha_ok=$([ "$s" = "$(want $p)" ] && echo yes || echo NO)"
  cat $C/section_1.diff $C/section_2.diff | cmp -s - $C/patch.diff && echo "$p sections_concat_equal yes" || echo "$p sections_concat_equal NO"
  grep '^@@' $C/section_1.diff | sed "s/^/$p s1 hunk: /"
  for k in 1 2; do
    f=$C/section_$k.diff
    out=$(git -C $WT apply --check -v -p1 $f 2>&1 | grep -iv "^Checking patch\|cleanly"); rc=$?
    git -C $WT apply --check -p1 $f; echo "$p s$k check rc=$? extra=[$out]"
    git -C $WT apply -v -p1 $f 2>&1 | grep -i "offset\|fuzz\|Hunk"; git -C $WT apply -p1 -R --check $f >/dev/null 2>&1; echo "$p s$k applied (reverse-check rc=$?)"
  done
done
echo DIFF_vs_head:
git -C $WT add -A >/dev/null
git -C $WT diff --cached --stat pr1924 -- Blockchain/Dev | tail -3
git -C $WT diff --cached --quiet pr1924 -- Blockchain/Dev && echo "SERVICE TREE EQUALS PR HEAD" || echo "SERVICE TREE DIFFERS"
git -C $WT diff --cached --quiet $MB -- Blockchain/Dev && echo "control: equals base (BAD)" || echo "control: differs from base (instrument fires)"
} > $L 2>&1
cat $L
git -C $R worktree remove --force $WT; echo wt_removed rc=$?
