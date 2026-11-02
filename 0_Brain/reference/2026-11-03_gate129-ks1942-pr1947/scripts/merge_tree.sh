#!/bin/bash
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate129-ks1942-pr1947; R=$G/repo; MB=1584c0f0ff808fddf35245bee41b6b5f9231054c
echo "merge-base PR/develop: $(git -C $R merge-base refs/gate/pr1947 refs/gate/develop)"
git -C $R log --oneline $MB..refs/gate/develop
git -C $R diff --name-only $MB refs/gate/develop > $G/logs/dev_moved.txt; echo "develop moved paths: $(wc -l < $G/logs/dev_moved.txt)"
git -C $R diff --name-only $MB refs/gate/pr1947 > $G/logs/pr_paths.txt; echo "PR paths: $(wc -l < $G/logs/pr_paths.txt)"
echo "shared: $(comm -12 <(sort $G/logs/dev_moved.txt) <(sort $G/logs/pr_paths.txt) | wc -l) ; control (moved vs itself): $(comm -12 <(sort $G/logs/dev_moved.txt) <(sort $G/logs/dev_moved.txt) | wc -l)"
T=$(git -C $R merge-tree --write-tree refs/gate/develop refs/gate/pr1947); RC=$?; echo "merge-tree rc=$RC tree=$T"
git -C $R diff --name-only refs/gate/develop $T > $G/logs/merged_vs_develop.txt; echo "merged tree vs develop paths: $(wc -l < $G/logs/merged_vs_develop.txt); equals PR paths: $(cmp -s <(sort $G/logs/merged_vs_develop.txt) <(sort $G/logs/pr_paths.txt) && echo yes || echo NO)"
echo "governance + fragment bytes PR head vs merged tree: $(git -C $R diff --name-only refs/gate/pr1947 $T -- Blockchain/Dev/services/governance 'Projects Documents/fragments/flow/KS-1942-register-binds-the-linked-wallet.html' 'Projects Documents/fragments/cheat/KS-1942-register-binds-the-linked-wallet.html' | wc -l) differing paths"
echo "$T" > $G/logs/merged_tree_id.txt
