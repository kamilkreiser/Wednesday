#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate142-ks1868-pr1958
R=$W/repo/Blockchain/Dev
npm --prefix $R ci --ignore-scripts > $W/logs/npm_ci.log 2>&1; echo ci RC=$? >> $W/logs/npm_ci.log
npm --prefix $R run build --workspace=packages/shared > $W/logs/build_shared.log 2>&1; echo build RC=$? >> $W/logs/build_shared.log
