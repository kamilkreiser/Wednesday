#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate117-ks1938-pr1935
D=$W/repo/Blockchain/Dev
export TMPDIR=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/0b6f2563-591e-4408-ab3d-78a74ca3c4e8/scratchpad
nice -n 10 npm ci --ignore-scripts --prefix $D > $W/logs/npm_ci.log 2>&1; echo "rc=$?" >> $W/logs/npm_ci.log
nice -n 10 npm run build --prefix $D/packages/shared > $W/logs/shared_build.log 2>&1; echo "rc=$?" >> $W/logs/shared_build.log
date > $W/logs/install.done
