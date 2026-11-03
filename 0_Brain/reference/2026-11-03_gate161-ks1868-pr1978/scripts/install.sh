#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate161-ks1868-pr1978
D=$W/repo/Blockchain/Dev
nice -n 10 npm ci --ignore-scripts --prefix $D > $W/logs/npm_ci.log 2>&1; rc=$?; echo "rc=$rc" >> $W/logs/npm_ci.log
if [ $rc -ne 0 ]; then nice -n 10 npm install --no-package-lock --ignore-scripts --prefix $D > $W/logs/npm_install_nolock.log 2>&1; echo "rc=$?" >> $W/logs/npm_install_nolock.log; fi
nice -n 10 npm run build --prefix $D/packages/shared > $W/logs/shared_build.log 2>&1; echo "rc=$?" >> $W/logs/shared_build.log
date > $W/logs/install.done
