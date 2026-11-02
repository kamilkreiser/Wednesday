#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate107-ks1868-pr1924-delta
A=$W/repo/Blockchain/Dev/services/originate; L=$W/logs; D=$W/repo/Blockchain/Dev
(cd $A && nice npx jest --json --outputFile=$L/whole_head.json > $L/whole_head.log 2>&1; echo rc=$? >> $L/whole_head.log)
(cd $A && npx tsc -p $W/scripts/tsconfig.tests.json --listFilesOnly > $L/tsc_files.log 2>&1; echo rc=$? >> $L/tsc_files.log)
(cd $A && npx tsc -p $W/scripts/tsconfig.tests.json > $L/tsc_tests.log 2>&1; echo rc=$? >> $L/tsc_tests.log)
(cd $A && npx tsc --noEmit -p tsconfig.json > $L/tsc_plain.log 2>&1; echo rc=$? >> $L/tsc_plain.log)
date > $L/whole.done
