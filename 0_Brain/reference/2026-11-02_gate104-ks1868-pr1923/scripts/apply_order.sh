#!/bin/bash
# Strict sequential apply of the held sections onto the base tree in a throwaway worktree in my own clone; compare with PR head.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate104-ks1868-pr1923
R=$W/repo; RUNS=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs; L=$W/logs/apply_order.log
MB=04ff5262ad526a13c1a0df99480b76860a8d11d1
WT=$W/apply_wt
test -e $WT && { echo "worktree path exists"; exit 2; }
git -C $R worktree add -q --detach $WT $MB
{
want(){ case $1 in o67_p1) echo 3eeaacf1a1165c083711c766daf02eca4fd2827717c4aabfb4431075e5606823;; o67_p2) echo 396d2bf19876d03953604e5a280fdd3f3210d11b8770f28e68f2c75daa34c799;; o67_p3) echo 93a358a59f04d2b30d713213a7253115f8279bf6982c9c8039ca611590ed2081;; o67_p4) echo fcbccaa30d61a7ea99ebf6655024945bf708aa45aa0564eb842dd3bad9fa5325;; o68_p3) echo 37541ea9783b5167ff07c93063d70757ca34eaa76d84da3049a36237b41195c9;; esac; }
for p in o67_p1 o67_p2 o67_p3 o67_p4 o68_p3; do
  D=$(ls -d $RUNS/spark_secuura_2026-11-02_ks_1868_${p}_* | grep -v -- '-control$' | head -1)
  C=$D/out.md.checker
  s=$(shasum -a 256 $C/patch.diff | awk '{print $1}')
  echo "$p dir=$(basename $D) patchsha_ok=$([ "$s" = "$(want $p)" ] && echo yes || echo NO)"
  cat $C/section_1.diff $C/section_2.diff | cmp -s - $C/patch.diff && echo "$p sections_concat_equal yes" || echo "$p sections_concat_equal NO"
  for k in 1 2; do
    f=$C/section_$k.diff
    head -1 $f | sed "s/^/$p s$k: /"
    out=$(git -C $WT apply --check -p1 $f 2>&1); rc=$?
    echo "$p s$k check rc=$rc out=[$out]"
    git -C $WT apply -p1 $f; echo "$p s$k apply rc=$?"
  done
done
echo DIFF_vs_head:
git -C $WT add -A >/dev/null
git -C $WT diff --cached --stat pr1923 -- Blockchain/Dev | tail -3
git -C $WT diff --cached --quiet pr1923 -- Blockchain/Dev && echo "SERVICE TREE EQUALS PR HEAD" || echo "SERVICE TREE DIFFERS"
} > $L 2>&1
cat $L
