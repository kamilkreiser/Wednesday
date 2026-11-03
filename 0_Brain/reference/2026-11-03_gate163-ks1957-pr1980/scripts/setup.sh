#!/bin/bash
# Gate 163 setup: clone is at pr/1980 (head); base worktree at the PR parent. node_modules cloned (cp -c) from gate 153's clone:
# lockfiles, package.jsons and the packages/shared tree are the SAME blob ids at gate153 HEAD, pr/1980, and develop 0a6575f7f.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate163-ks1957-pr1980
R=$W/repo; D=$R/Blockchain/Dev
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate153-ks1868-pr1969/repo/Blockchain/Dev
git -C $R checkout -q --detach 7d6130ba0d4edb9294dbb81f39c0bcb76268dfa0; echo "head checkout rc=$? $(git -C $R rev-parse HEAD)"
for p in node_modules services/referral/node_modules packages/shared/node_modules; do
  nice -n 10 cp -Rc "$G/$p" "$D/$p"; echo "copied $p rc=$?"
done
Q=$W/_quarantine_$(date +%F); mkdir -p $Q/root $Q/ref
[ -d "$D/node_modules/.vite" ] && mv "$D/node_modules/.vite" $Q/root/
[ -d "$D/services/referral/node_modules/.vite" ] && mv "$D/services/referral/node_modules/.vite" $Q/ref/
nice -n 10 npm run build --prefix $D/packages/shared > $W/logs/shared_build.log 2>&1; echo "shared build rc=$?"
git -C $R worktree add -q --detach $W/wt/base 66cbe4e52d5afadc9d13ca141200026cc68d5095; echo "base wt rc=$? $(git -C $W/wt/base rev-parse HEAD)"
T=$W/wt/base/Blockchain/Dev
ln -s $D/node_modules $T/node_modules
ln -s $D/services/referral/node_modules $T/services/referral/node_modules
ln -s $D/packages/shared/node_modules $T/packages/shared/node_modules
[ -e $T/packages/shared/dist ] && echo "base dist exists, not linking" || ln -s $D/packages/shared/dist $T/packages/shared/dist
git -C $R status --porcelain | head; date
