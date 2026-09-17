#!/bin/bash
# drafter 1025: shared clone by SHA into a fresh mktemp -d; write verbs only here
set -u
R='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
W="$(mktemp -d /private/tmp/claude-501/drafter1025.XXXXXX)"
echo "W=$W"
HEAD=9954a7069a16987da140654337555c9a13268b1f
BASE=efaaa6034f036dd9538ee35b189217b1d08b90a9
git clone --shared --no-checkout "$R" "$W/clone" 2>&1 | tail -2
git -C "$W/clone" cat-file -t $HEAD
git -C "$W/clone" worktree add --detach "$W/base" $BASE 2>&1 | tail -1
git -C "$W/clone" worktree add --detach "$W/head" $HEAD 2>&1 | tail -1
git -C "$W/clone" log --format='%H %P %T %an %s' -1 $HEAD
git -C "$W/clone" log --format='%H %T %s' -1 $BASE
echo "merge-base $(git -C "$W/clone" merge-base $BASE $HEAD)"
echo "rev-list count base..head $(git -C "$W/clone" rev-list --count $BASE..$HEAD)"
git -C "$W/clone" diff --numstat $BASE $HEAD
git -C "$W/clone" diff -w --numstat $BASE $HEAD
git -C "$W/clone" ls-tree $BASE Blockchain/Dev/scripts/audit/ Blockchain/Dev/package-lock.json Blockchain/Dev/package.json
git -C "$W/clone" ls-tree $HEAD Blockchain/Dev/scripts/audit/audit-baseline.json
echo "merge-tree $(git -C "$W/clone" merge-tree --write-tree $BASE $HEAD)"
echo "merge-tree control base x base $(git -C "$W/clone" merge-tree --write-tree $BASE $BASE)"
git -C "$W/clone" log --format='%B' -1 $HEAD
echo "porcelain base $(git -C "$W/base" status --porcelain | wc -l) head $(git -C "$W/head" status --porcelain | wc -l)"
