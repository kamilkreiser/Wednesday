#!/bin/bash
R=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate93-ks1868-pr1911/repo
git -C $R ls-remote origin refs/heads/develop
T=$(git -C $R merge-tree --write-tree refs/gate/develop refs/gate/pr1911); echo "merge-tree rc=$? tree=$T"
git -C $R diff --name-only refs/gate/develop $T
echo "changed paths: $(git -C $R diff --name-only refs/gate/develop $T | wc -l)"
echo "PR paths: $(git -C $R diff --name-only refs/gate/develop...refs/gate/pr1911 | wc -l)"
diff <(git -C $R diff --name-only refs/gate/develop $T) <(git -C $R diff --name-only refs/gate/develop...refs/gate/pr1911) && echo "merged change == PR paths"
echo "merged tree == PR head tree? $( [ "$T" = "$(git -C $R rev-parse refs/gate/pr1911^{tree})" ] && echo yes || echo no)"
