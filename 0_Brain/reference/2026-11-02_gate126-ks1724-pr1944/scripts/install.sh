#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate126-ks1724-pr1944
D=$W/repo/Blockchain/Dev
node -v > $W/logs/npm_ci.log
nice -n 10 npm ci --ignore-scripts --no-audit --no-fund --prefix $D >> $W/logs/npm_ci.log 2>&1; echo "rc=$?" >> $W/logs/npm_ci.log
nice -n 10 npm run build --prefix $D/packages/shared > $W/logs/shared_build.log 2>&1; echo "rc=$?" >> $W/logs/shared_build.log
date > $W/logs/install.done
