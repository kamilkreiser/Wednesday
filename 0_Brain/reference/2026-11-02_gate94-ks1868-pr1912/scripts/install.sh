#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate94-ks1868-pr1912
D=$W/repo/Blockchain/Dev
cd "$D" || exit 99
nice -n 10 npm ci --ignore-scripts > $W/logs/npm_ci.log 2>&1; echo "rc=$?" >> $W/logs/npm_ci.log
cd "$D/packages/shared" || exit 98
nice -n 10 npm run build > $W/logs/shared_build.log 2>&1; echo "rc=$?" >> $W/logs/shared_build.log
date > $W/logs/install.done
