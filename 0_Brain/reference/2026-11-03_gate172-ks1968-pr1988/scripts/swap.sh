#!/bin/bash
# usage: swap.sh base|head   puts develop's (base) or the PR's (head) product files in the clone; tests stay at head
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate172-ks1968-pr1988; R=$W/repo
[ "$1" = base ] && REV=de8d208a8426747b3a752309e08167fa0de4b2ff || REV=ba973c53ecc3bfa5ff21d71b967c9d4344ad3d52
for f in src/routes/auth.ts src/services/password.ts vitest.setup.ts; do
  git -C $R show $REV:Blockchain/Dev/services/auth/$f > $R/Blockchain/Dev/services/auth/$f
done
echo "swapped to $1 ($REV)"; git -C $R status --porcelain -- Blockchain/Dev/services/auth | grep -v '^??'
