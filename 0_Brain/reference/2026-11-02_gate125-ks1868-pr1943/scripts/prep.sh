#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate125-ks1868-pr1943
R=$W/repo
git -C $R checkout -q pr1943; echo checkout rc=$?; git -C $R rev-parse HEAD
npm ci --ignore-scripts --prefix $R/Blockchain/Dev/services/originate > $W/logs/npm_ci.log 2>&1; echo npm ci rc=$?
