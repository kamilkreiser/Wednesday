#!/bin/bash
# Gate 162 merge-tree of PR head onto develop, in MY clone; shared paths; merged referral subtree vs head's.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate162-ks1956-pr1979
R=$W/repo; H=eeb4ab58d6d110d9bd14119d0c78c0e28e58f2d2; B=66cbe4e52d5afadc9d13ca141200026cc68d5095
{ date -u; git -C $R ls-remote origin refs/pull/1979/head refs/heads/develop; } > $W/logs/head_end.log
DEV=$(awk '/refs\/heads\/develop/{print $1}' $W/logs/head_end.log)
git -C $R fetch -q origin +refs/heads/develop:refs/remotes/origin/develop
{
echo "develop=$DEV pinned=2a827aac1923ac792e0e9b70ad8bf0ade918a579"
git -C $R merge-base --is-ancestor $B $DEV; echo "base ancestor of develop rc=$?"
echo "--- develop commits since base:"; git -C $R log --oneline $B..$DEV
git -C $R diff --name-only $B $DEV | sort > $W/logs/dev_paths.txt
git -C $R diff --name-only $B $H | sort > $W/logs/pr_paths.txt
echo "develop paths: $(wc -l < $W/logs/dev_paths.txt)  PR paths: $(wc -l < $W/logs/pr_paths.txt)"
echo "shared: $(comm -12 $W/logs/dev_paths.txt $W/logs/pr_paths.txt | wc -l)"; comm -12 $W/logs/dev_paths.txt $W/logs/pr_paths.txt
echo "control (develop vs itself): $(comm -12 $W/logs/dev_paths.txt $W/logs/dev_paths.txt | wc -l)"
echo "develop paths under services/referral or packages/shared or package-lock: $(grep -cE 'services/referral|packages/shared|package-lock' $W/logs/dev_paths.txt)"
T=$(git -C $R merge-tree --write-tree $DEV $H); echo "merge-tree rc=$? tree=$T"
for p in Blockchain/Dev/services/referral Blockchain/Dev/packages/shared Blockchain/Dev/package-lock.json; do
  echo "$p merged=$(git -C $R rev-parse $T:$p) head=$(git -C $R rev-parse $H:$p)"; done
echo "merged vs develop paths:"; git -C $R diff --name-only $DEV $T
} > $W/logs/merge_tree.log 2>&1
cat $W/logs/merge_tree.log
