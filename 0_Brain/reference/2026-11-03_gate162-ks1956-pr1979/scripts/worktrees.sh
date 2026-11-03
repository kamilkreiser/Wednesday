#!/bin/bash
# Gate 162: base and head worktrees of MY clone (repo/), node_modules + shared dist linked to the clone's.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate162-ks1956-pr1979
R=$W/repo
git -C $R worktree add -q --detach $W/wt/base 66cbe4e52d5afadc9d13ca141200026cc68d5095; echo base rc=$?
git -C $R worktree add -q --detach $W/wt/head eeb4ab58d6d110d9bd14119d0c78c0e28e58f2d2; echo head rc=$?
for v in base head; do
  T=$W/wt/$v/Blockchain/Dev
  ln -s $R/Blockchain/Dev/node_modules $T/node_modules
  ln -s $R/Blockchain/Dev/services/referral/node_modules $T/services/referral/node_modules
  rm -rf $T/packages/shared/dist; ln -s $R/Blockchain/Dev/packages/shared/dist $T/packages/shared/dist
  [ -d $R/Blockchain/Dev/packages/shared/node_modules ] && ln -s $R/Blockchain/Dev/packages/shared/node_modules $T/packages/shared/node_modules
  echo "$v $(git -C $W/wt/$v rev-parse HEAD)"
done
mkdir -p $W/logs/child_cwd $W/logs/probe
