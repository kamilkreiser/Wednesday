#!/bin/bash
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate136-ks1950-pr1952-delta; R=$G/repo
echo "develop_end $(git -C $R rev-parse refs/gate/develop_end) pr1952_end $(git -C $R rev-parse refs/gate/pr1952_end)"
echo "develop_end ancestor of PR head: $(git -C $R merge-base --is-ancestor refs/gate/develop_end refs/gate/pr1952_end && echo yes || echo no); merge-base $(git -C $R merge-base refs/gate/develop_end refs/gate/pr1952_end)"
T=$(git -C $R merge-tree --write-tree refs/gate/develop_end refs/gate/pr1952_end); echo "merge-tree rc=$? tree=$T"
git -C $R diff --name-only refs/gate/develop_end $T | sort > $G/logs/merged_vs_develop.txt; git -C $R diff --name-only refs/gate/develop_end...refs/gate/pr1952_end | sort > $G/logs/pr_paths.txt
echo "merged vs develop_end: $(wc -l < $G/logs/merged_vs_develop.txt) paths; PR three-dot paths $(wc -l < $G/logs/pr_paths.txt); equal: $(cmp -s $G/logs/merged_vs_develop.txt $G/logs/pr_paths.txt && echo yes || echo NO)"
echo "PR paths' blobs in merged tree equal PR head: $(for p in $(cat $G/logs/pr_paths.txt | tr ' ' '?'); do :; done; git -C $R diff --quiet refs/gate/pr1952_end $T -- $(sed 's/^/:(literal)/' $G/logs/pr_paths.txt | tr '\n' ' ') 2>/dev/null && echo yes || echo CHECK)"
git -C $R diff --stat refs/gate/develop_end...refs/gate/pr1952_end | tail -1
echo "-- pair with open PR 1953 (head $(git -C $R rev-parse refs/gate/pr1953_end | cut -c1-12))"
git -C $R merge-tree --write-tree refs/gate/pr1952_end refs/gate/pr1953_end > $G/logs/merge_tree_1953.out; echo "merge-tree 1952 x 1953 rc=$? tree=$(head -1 $G/logs/merge_tree_1953.out)"
git -C $R diff --name-only refs/gate/develop_end...refs/gate/pr1953_end | sort > $G/logs/pr1953_paths.txt; echo "shared paths with 1953: $(comm -12 $G/logs/pr_paths.txt $G/logs/pr1953_paths.txt | tr '\n' ' ')"
