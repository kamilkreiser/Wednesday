#!/bin/bash
# Gate 167 setup: clone at PR 1984 head; base worktree at the PR parent 1e6df0b6.
# node_modules cloned (cp -c) from gate 163's clone: package-lock, package.jsons and the packages/shared TREE are the same
# blob ids at gate163 HEAD 7d6130ba, PR 1984 head and develop 27fe5476 (checked before setup).
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate167-ks1572-pr1984
R=$W/repo; D=$R/Blockchain/Dev
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate163-ks1957-pr1980/repo/Blockchain/Dev
HEAD_SHA=68897dda941066459fcec2e34f667f07d46f9d8d
git -C $R remote set-url --push origin DISABLED
git -C $R checkout -q --detach $HEAD_SHA; echo "head checkout rc=$? $(git -C $R rev-parse HEAD)"
for p in node_modules services/referral/node_modules packages/shared/node_modules; do
  nice -n 10 cp -Rc "$G/$p" "$D/$p"; echo "copied $p rc=$?"
done
mkdir -p $W/scratch/_quarantine/root $W/scratch/_quarantine/ref
[ -d "$D/node_modules/.vite" ] && mv "$D/node_modules/.vite" $W/scratch/_quarantine/root/
[ -d "$D/services/referral/node_modules/.vite" ] && mv "$D/services/referral/node_modules/.vite" $W/scratch/_quarantine/ref/
nice -n 10 npm run build --prefix $D/packages/shared > $W/logs/shared_build.log 2>&1; echo "shared build rc=$?"
mkdir -p $W/scratch/wt
git -C $R worktree add -q --detach $W/scratch/wt/base $HEAD_SHA~1; echo "base wt rc=$? $(git -C $W/scratch/wt/base rev-parse HEAD)"
T=$W/scratch/wt/base/Blockchain/Dev
ln -s $D/node_modules $T/node_modules
ln -s $D/services/referral/node_modules $T/services/referral/node_modules
ln -s $D/packages/shared/node_modules $T/packages/shared/node_modules
ln -s $D/packages/shared/dist $T/packages/shared/dist
git -C $R status --porcelain | head; date -u
