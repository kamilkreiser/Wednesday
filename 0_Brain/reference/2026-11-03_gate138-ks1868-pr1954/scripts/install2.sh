#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate138-ks1868-pr1954
git -C $W/repo checkout -q pr1954 > $W/logs/checkout.log 2>&1; git -C $W/repo rev-parse HEAD >> $W/logs/checkout.log
nice -n 10 npm ci --ignore-scripts --prefix $W/repo/Blockchain/Dev > $W/logs/npm_ci.log 2>&1; echo "rc=$?" >> $W/logs/npm_ci.log
nice -n 10 npm run build --prefix $W/repo/Blockchain/Dev/packages/shared > $W/logs/shared_build.log 2>&1; echo "rc=$?" >> $W/logs/shared_build.log
date > $W/logs/install.done
