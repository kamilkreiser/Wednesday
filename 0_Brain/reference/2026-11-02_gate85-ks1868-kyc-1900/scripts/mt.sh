#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate85-ks1868-kyc-1900; R=$W/repo
git -C /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate85-ks1868-kyc-1900/repo fetch -q origin +refs/heads/develop:refs/gate/develop_now > $W/logs/fetch_develop_now.log 2>&1; echo "fetch rc=$?"
echo "develop at start (refs/gate/develop): $(git -C $R rev-parse refs/gate/develop)"; echo "develop now: $(git -C $R rev-parse refs/gate/develop_now)"
git -C $R diff --name-only refs/gate/pr1900^ refs/gate/pr1900 > $W/logs/pr_files.log
for ref in develop develop_now; do
  echo "### merge-tree onto refs/gate/$ref"
  { git -C $R merge-tree --write-tree refs/gate/$ref refs/gate/pr1900; echo "rc=$?"; } 2>&1
  git -C $R log --oneline 8126b22bd5aa505be194996c9301b6e1ced5583e..refs/gate/$ref 2>&1
  git -C $R diff --name-only 8126b22bd5aa505be194996c9301b6e1ced5583e refs/gate/$ref > $W/logs/develop_since_files_$ref.log 2>&1
  echo "files changed on $ref since 8126b22b: $(wc -l < $W/logs/develop_since_files_$ref.log)"
  echo "overlap with PR files:"; comm -12 <(sort $W/logs/pr_files.log) <(sort $W/logs/develop_since_files_$ref.log); echo "(end overlap)"
  echo "kyc paths touched since: "; grep -i "services/kyc" $W/logs/develop_since_files_$ref.log; echo "(end kyc)"
done
