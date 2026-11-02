#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate128-ks1868-pr1946
R=$W/repo
git -C $R checkout -q pr1946; echo checkout rc=$?; git -C $R rev-parse HEAD
npm ci --ignore-scripts --prefix $R/Blockchain/Dev/services/originate > $W/logs/npmci.log 2>&1; echo npm ci rc=$?
tail -3 $W/logs/npmci.log | cut -c1-200
