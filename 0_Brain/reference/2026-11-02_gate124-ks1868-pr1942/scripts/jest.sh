#!/bin/bash
# anchored jest runner: jest.sh <json-out> <log> [jest args...]
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate124-ks1868-pr1942; D=$W/repo/Blockchain/Dev; A=$D/services/originate
OUTJ=$1; LOG=$2; shift 2
nice -n 10 $D/node_modules/.bin/jest --config $A/jest.config.js --rootDir $A --forceExit --json --outputFile=$OUTJ "$@" > $LOG 2>&1; echo "rc=$?" >> $LOG
