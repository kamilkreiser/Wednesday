#!/bin/bash
# A third worktree at the PR head, used ONLY for mutants (so mutating it never touches the suite runs).
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate126-ks1724-pr1944
[ -e $W/mut ] && { echo "mut exists"; exit 1; }
git -C $W/repo worktree add -q --detach $W/mut 3b11d11a29880dc8ff5cc8d7331a58cd0ead5e11; echo "worktree rc=$?"
git -C $W/mut rev-parse HEAD
D=$W/mut/Blockchain/Dev
nice -n 10 npm ci --ignore-scripts --no-audit --no-fund --prefix $D > $W/logs/npm_ci_mut.log 2>&1; echo "npm ci rc=$?"
nice -n 10 npm run build --prefix $D/packages/shared > $W/logs/shared_build_mut.log 2>&1; echo "build rc=$?"
