#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate138-ks1868-pr1954
A=$W/repo/Blockchain/Dev/services/api-gateway; M=$A/src/routes/admin.ts; V=$W/repo/Blockchain/Dev/node_modules/.bin/vitest
T="ks1868-admin-forward-export-message-coercion ks1868-admin-identity-routes-message-coercion ks1868-admin-identity-seed-message-coercion ks1868-admin-organization-message-coercion"
cmp -s $M $W/logs/admin_head.ts && echo "admin.ts == head"
nice -n 10 $V run --root $A $T --reporter=json --outputFile=$W/logs/pr_tests_head.json > $W/logs/pr_tests_head.out 2>&1; echo "pr tests head rc=$?"
cp $W/logs/admin_base.ts $M
nice -n 10 $V run --root $A $T --reporter=json --outputFile=$W/logs/red_base.json > $W/logs/red_base.out 2>&1; echo "pr tests at BASE admin.ts rc=$?"
cp $W/logs/admin_head.ts $M; cmp -s $M $W/logs/admin_head.ts && echo RESTORE_OK
nice -n 10 $V run --root $A --maxWorkers=3 --reporter=json --outputFile=$W/logs/suite_head.json > $W/logs/suite_head.out 2>&1; echo "suite head rc=$?"
# base suite: base admin.ts, PR tests moved aside
Q=$W/scripts/_quarantine/suite_tests; mkdir -p $Q
cp $W/logs/admin_base.ts $M
for f in $A/src/__tests__/ks1868-admin-*message-coercion-unreadable-throw.test.ts; do mv $f $Q/; done
nice -n 10 $V run --root $A --maxWorkers=3 --reporter=json --outputFile=$W/logs/suite_base.json > $W/logs/suite_base.out 2>&1; echo "suite base rc=$?"
for f in $Q/*.test.ts; do mv $f $A/src/__tests__/; done
cp $W/logs/admin_head.ts $M; cmp -s $M $W/logs/admin_head.ts && echo RESTORE_OK2
git -C $W/repo status --short
python3 - <<'PY'
import json
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate138-ks1868-pr1954/logs/'
for n in ['pr_tests_head','red_base','suite_head','suite_base']:
    d=json.load(open(W+n+'.json')); print(n,'files',d['numTotalTestSuites'] if 0 else len(d['testResults']),'tests',d['numTotalTests'],'passed',d['numPassedTests'],'failed',d['numFailedTests'])
d=json.load(open(W+'red_base.json')); 
import collections
msgs=collections.Counter()
for f in d['testResults']:
    for a in f['assertionResults']:
        if a['status']!='passed': msgs[(a['failureMessages'][0].split('\n')[0][:70])]+=1
print(msgs.most_common(8))
PY
