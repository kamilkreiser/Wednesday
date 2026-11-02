#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate125-ks1868-pr1943
S=$W/repo/Blockchain/Dev/services/originate
echo "load $(uptime)" > $W/logs/suite_$1.log
$S/node_modules/.bin/jest --rootDir $S -c $S/jest.config.js --silent >> $W/logs/suite_$1.log 2>&1; echo "jest rc=$?" >> $W/logs/suite_$1.log
