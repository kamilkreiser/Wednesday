#!/bin/bash
R=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate99-ks1868-pr1917/repo; L=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate99-ks1868-pr1917/logs
git -C /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate99-ks1868-pr1917/repo fetch origin develop:refs/remotes/origin/develop > $L/fetch_end.log 2>&1
{ git -C $R rev-parse origin/develop; git -C $R log --oneline bd8785796118..origin/develop; git -C $R diff --name-only bd8785796118 origin/develop; echo merge-tree:
T=$(git -C /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate99-ks1868-pr1917/repo merge-tree --write-tree origin/develop pr/1917); echo "rc=$? tree=$T"
echo "merged vs develop:"; git -C $R diff --stat origin/develop $T | tail -1
echo shared:; comm -12 <(git -C $R diff --name-only 03977e89a343 origin/develop | sort) <(git -C $R diff --name-only 03977e89a343 pr/1917 | sort) | wc -l
echo "index.ts blob develop:"; git -C $R rev-parse origin/develop:Blockchain/Dev/services/tenant-provisioning/src/index.ts; } > $L/merge_tree_end.log 2>&1
