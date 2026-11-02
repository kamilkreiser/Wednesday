#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate127-ks1943-pr1945
D=$W/repo/Blockchain/Dev
export TMPDIR=/tmp/g127
echo "node $(node -v) load $(sysctl -n vm.loadavg)" > $W/logs/npm_ci.log
nice -n 10 npm ci --ignore-scripts --prefix $D >> $W/logs/npm_ci.log 2>&1; echo "rc=$?" >> $W/logs/npm_ci.log
nice -n 10 npm run build --prefix $D/packages/shared > $W/logs/shared_build.log 2>&1; echo "rc=$?" >> $W/logs/shared_build.log
nice -n 10 node $D/scripts/prisma-generate.cjs > $W/logs/prisma_generate.log 2>&1; echo "rc=$?" >> $W/logs/prisma_generate.log
date > $W/logs/install.done
