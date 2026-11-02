#!/bin/bash
# A second worktree at the PR's merge-base (develop c70f339063ee, which the PR merged in), installed and built the same way.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate126-ks1724-pr1944
[ -e $W/base ] && { echo "base exists"; exit 1; }
git -C $W/repo worktree add -q --detach $W/base c70f339063eedd6ee5d937f4a79274c464091866; echo "worktree rc=$?"
git -C $W/base rev-parse HEAD
D=$W/base/Blockchain/Dev
nice -n 10 npm ci --ignore-scripts --no-audit --no-fund --prefix $D > $W/logs/npm_ci_base.log 2>&1; echo "npm ci rc=$?"
nice -n 10 npm run build --prefix $D/packages/shared > $W/logs/shared_build_base.log 2>&1; echo "build rc=$?"
