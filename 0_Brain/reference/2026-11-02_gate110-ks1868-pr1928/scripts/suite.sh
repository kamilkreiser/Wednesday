#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate110-ks1868-pr1928
A=$W/repo/Blockchain/Dev/services/api-gateway; M=$A/src/routes/admin.ts; V=$W/repo/Blockchain/Dev/node_modules/.bin/vitest
Q=$W/scripts/_quarantine/suite_tests; mkdir -p $Q
nice -n 10 $V run --root $A --maxWorkers=3 --reporter=json --outputFile=$W/logs/suite_head.json > $W/logs/suite_head.out 2>&1; echo "head rc=$?" > $W/logs/suite.status
cp $W/logs/admin_base.ts $M
for f in ks1868-admin-organization-route-catches-unreadable-throw ks1868-admin-forward-and-export-catches-unreadable-throw ks1868-admin-identity-seed-catch-unreadable-throw; do mv $A/src/__tests__/$f.test.ts $Q/; done
nice -n 10 $V run --root $A --maxWorkers=3 --reporter=json --outputFile=$W/logs/suite_base.json > $W/logs/suite_base.out 2>&1; echo "base rc=$?" >> $W/logs/suite.status
for f in $Q/*.test.ts; do mv $f $A/src/__tests__/; done
cp $W/logs/admin_head.ts $M
git -C $W/repo status --short >> $W/logs/suite.status; echo done >> $W/logs/suite.status
