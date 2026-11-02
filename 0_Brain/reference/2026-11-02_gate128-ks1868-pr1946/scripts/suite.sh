#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate128-ks1868-pr1946
O=$W/repo/Blockchain/Dev/services/originate
PF=$O/src/services/retentionScheduler.ts
J="$O/node_modules/.bin/jest --config $O/jest.config.js --rootDir $O --maxWorkers=2 --silent"
SAVE=$(shasum -a 256 $PF|cut -d' ' -f1)
echo load=$(uptime|sed 's/.*load averages: //')

git -C $W/repo show e2a2426d221d:Blockchain/Dev/services/originate/src/services/retentionScheduler.ts > $PF
$J --testPathIgnorePatterns 'o79b4' '/node_modules/' '[.]integration[.]test[.]ts$' --json --outputFile=$W/logs/suite_base.json > $W/logs/suite_base.log 2>&1; echo base_rc=$?
git -C $W/repo checkout -q -- Blockchain/Dev/services/originate/src/services/retentionScheduler.ts
echo restore=$([ "$(shasum -a 256 $PF|cut -d' ' -f1)" = "$SAVE" ] && echo OK || echo BAD)
echo load=$(uptime|sed 's/.*load averages: //')
python3 -I -c "
import json
for v in ('head','base'):
    d=json.load(open('$W/logs/suite_%s.json'%v)); print(v,'suites',d['numTotalTestSuites'],'tests',d['numPassedTests'],'/',d['numTotalTests'],'failed',d['numFailedTests'],'failedSuites',d['numFailedTestSuites'])
"
