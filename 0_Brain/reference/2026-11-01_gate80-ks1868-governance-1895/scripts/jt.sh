#!/bin/bash
# usage: jt.sh <head|base> <log> [jest args...]
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate80-ks1868-governance-1895
T=$1; LOG=$2; shift 2
GOV=$W/wt_$T/Blockchain/Dev/services/governance
L1=$(uptime | sed 's/.*averages: *//' | awk '{print $1}' | tr -d ,)
echo "start $(date +%T) load1=$L1 tree=$T" > $LOG
nice -n 10 $W/wt_head/Blockchain/Dev/node_modules/.bin/jest --config $GOV/jest.config.js --rootDir $GOV --maxWorkers=2 "$@" >> $LOG 2>&1
echo "rc=$?" >> $LOG
