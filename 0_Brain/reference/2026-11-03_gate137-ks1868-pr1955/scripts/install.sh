#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate137-ks1868-pr1955
D=$W/repo/Blockchain/Dev
export TMPDIR=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/c5199eda-e2e8-42ab-989c-f3882d521117/scratchpad
git -C $W/repo checkout -q -B gate137 pr/1955; echo "checkout rc=$? head=$(git -C $W/repo rev-parse HEAD)" > $W/logs/npm_ci.log
nice -n 10 npm ci --ignore-scripts --prefix $D >> $W/logs/npm_ci.log 2>&1; echo "rc=$?" >> $W/logs/npm_ci.log
nice -n 10 npm run build --prefix $D/packages/shared > $W/logs/shared_build.log 2>&1; echo "rc=$?" >> $W/logs/shared_build.log
date > $W/logs/install.done
