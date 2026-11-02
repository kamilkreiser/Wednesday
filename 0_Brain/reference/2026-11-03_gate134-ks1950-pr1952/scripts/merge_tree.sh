#!/bin/bash
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate134-ks1950-pr1952; R=$G/repo
echo "develop ancestor of PR head: $(git -C $R merge-base --is-ancestor refs/gate/develop_end refs/gate/pr1952_end && echo yes || echo no)"
T=$(git -C $R merge-tree --write-tree refs/gate/develop_end refs/gate/pr1952_end); echo "merge-tree rc=$? tree=$T head tree=$(git -C $R rev-parse refs/gate/pr1952_end^{tree})"
git -C $R diff --name-only refs/gate/develop_end $T > $G/logs/merged_vs_develop.txt; git -C $R diff --name-only refs/gate/develop_end...refs/gate/pr1952_end > $G/logs/pr_paths.txt
echo "merged vs develop: $(wc -l < $G/logs/merged_vs_develop.txt) paths; PR paths $(wc -l < $G/logs/pr_paths.txt); equal: $(cmp -s <(sort $G/logs/merged_vs_develop.txt) <(sort $G/logs/pr_paths.txt) && echo yes || echo NO)"
git -C $R log --oneline refs/gate/develop_end..refs/gate/pr1952_end --no-merges
