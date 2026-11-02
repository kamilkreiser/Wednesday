#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate137-ks1868-pr1955; R=$W/repo
export TMPDIR=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/c5199eda-e2e8-42ab-989c-f3882d521117/scratchpad
T=$(cat $W/logs/mt_tree_pair.txt)
C=$(git -C $R commit-tree $T -p pr/1953 -p pr/1955 -m "g137 local pair merge (never pushed)"); echo "pair commit $C tree $T"
test -e $W/merged && echo "merged dir EXISTS" && exit 1
git -C $R worktree add --detach $W/merged $C; echo "worktree rc=$?"
echo "worktree HEAD tree $(git -C $W/merged rev-parse HEAD^{tree})"
nice -n 10 npm ci --ignore-scripts --prefix $W/merged/Blockchain/Dev > $W/logs/pair_npm_ci.log 2>&1; echo "npm ci rc=$?"
nice -n 10 npm run build --prefix $W/merged/Blockchain/Dev/packages/shared > $W/logs/pair_shared_build.log 2>&1; echo "shared build rc=$?"
grep -m1 '"version"' $W/merged/Blockchain/Dev/node_modules/zod/package.json
