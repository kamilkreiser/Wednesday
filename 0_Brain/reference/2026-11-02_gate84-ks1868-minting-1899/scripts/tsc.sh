#!/bin/bash
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate84-ks1868-minting-1899
A=$G/repo/Blockchain/Dev/services/nft-certificate; T=$G/repo/Blockchain/Dev/node_modules/.bin/tsc
nice -n 10 $T -p $A/tsconfig.json --noEmit > $G/logs/tsc_plain_head.log 2>&1; echo "rc=$?" >> $G/logs/tsc_plain_head.log
nice -n 10 $T -p $G/scripts/tsconfig.tests.json > $G/logs/tsc_tests_head.log 2>&1; echo "rc=$?" >> $G/logs/tsc_tests_head.log
tail -4 $G/logs/tsc_plain_head.log $G/logs/tsc_tests_head.log
