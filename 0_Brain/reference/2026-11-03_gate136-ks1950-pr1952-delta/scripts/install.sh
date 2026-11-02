#!/bin/bash
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate136-ks1950-pr1952-delta
D=$G/repo/Blockchain/Dev
node --version > $G/logs/npm_ci.log
nice -n 10 npm ci --ignore-scripts --prefix $D >> $G/logs/npm_ci.log 2>&1; echo "rc=$?" >> $G/logs/npm_ci.log
nice -n 10 npm run build --prefix $D/packages/shared > $G/logs/shared_build.log 2>&1; echo "rc=$?" >> $G/logs/shared_build.log
date > $G/logs/install.done
