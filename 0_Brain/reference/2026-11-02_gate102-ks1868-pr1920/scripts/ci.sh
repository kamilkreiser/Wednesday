#!/bin/bash
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate102-ks1868-pr1920
S=$G/repo/Blockchain/Dev/services/analytics
cd "$S" && npm ci --ignore-scripts > $G/logs/npm_ci2.log 2>&1
echo "rc=$?" >> $G/logs/npm_ci2.log
tail -5 $G/logs/npm_ci2.log
ls node_modules | wc -l; ls node_modules/.bin | grep -c .
