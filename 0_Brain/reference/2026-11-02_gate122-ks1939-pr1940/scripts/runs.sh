#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate122-ks1939-pr1940
R=$W/repo; D=$R/Blockchain/Dev; A=$D/services/originate; L=$W/logs; J="$D/node_modules/.bin/jest --config $A/jest.config.js --rootDir $A --forceExit"
F=src/routes/verification.ts; MB=e2a2426d221d8bd672e97c43c6bbcd6c4027b350; sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
NEW="ks1939-verification"
mkdir -p $L/head_copy; cp $A/$F $L/head_copy/verification.ts; h0=$(sha $A/$F)
git -C $R show $MB:Blockchain/Dev/services/originate/$F > $A/$F; echo "base product $(sha $A/$F)"
nice $J --json --outputFile=$L/red_base.json $NEW > $L/red_base_new.log 2>&1; echo "red rc=$?"
nice $J --json --outputFile=$L/whole_base.json --testPathIgnorePatterns '/node_modules/' '\.integration\.test\.ts$' 'ks1939-verification' > $L/whole_base.log 2>&1; echo "whole base rc=$?"
cp $L/head_copy/verification.ts $A/$F; [ "$(sha $A/$F)" = "$h0" ] && echo RESTORE_OK
nice $J --json --outputFile=$L/head_new.json $NEW > $L/head_new_tests.log 2>&1; echo "green rc=$?"
nice $J --json --outputFile=$L/whole_head.json > $L/whole_head.log 2>&1; echo "whole head rc=$?"
git -C $R status --short
