#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate162-ks1956-pr1979; R=$W/repo
T=$(git -C $R merge-tree --write-tree 2a827aac1923ac792e0e9b70ad8bf0ade918a579 eeb4ab58d6d110d9bd14119d0c78c0e28e58f2d2); echo "onto 2a827aac rc=$? tree=$T referral=$(git -C $R rev-parse $T:Blockchain/Dev/services/referral)"
echo "shared paths with 2a827aac: $(comm -12 <(git -C $R diff --name-only 66cbe4e52d5afadc9d13ca141200026cc68d5095 2a827aac1923ac792e0e9b70ad8bf0ade918a579 | sort) $W/logs/pr_paths.txt | wc -l)"
