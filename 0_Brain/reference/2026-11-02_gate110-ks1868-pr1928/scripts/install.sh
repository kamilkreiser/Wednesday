#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate110-ks1868-pr1928
nice -n 10 npm ci --ignore-scripts --prefix $W/repo/Blockchain/Dev > $W/logs/npm_ci.log 2>&1; echo "rc=$?" >> $W/logs/npm_ci.log
nice -n 10 npm run build --prefix $W/repo/Blockchain/Dev/packages/shared > $W/logs/shared_build.log 2>&1; echo "rc=$?" >> $W/logs/shared_build.log
date > $W/logs/install.done
