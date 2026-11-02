#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate121-ks1940-pr1939
G=$W/repo/Blockchain/Dev/services/governance
SVC=$G/src/services/governanceService.ts; RT=$G/src/routes/governance.ts
PROBE=$G/src/__tests__/g121_pg.test.ts
export TMPDIR=$W/tmp G121_DDL=$W/scripts/gov_ddl.sql
cp $W/scripts/g121_pg.test.ts $PROBE
for ver in base head; do
  cp $W/scripts/svc_$ver.ts $SVC; cp $W/scripts/routes_$ver.ts $RT
  out=$W/logs/pg_$ver.jsonl; : > $out
  PROBE_OUT=$out $G/node_modules/.bin/jest --config $G/jest.config.js --rootDir $G --testPathPattern g121_pg --runInBand --forceExit > $W/logs/pg_${ver}_jest.log 2>&1
  echo "$ver rc $? lines $(wc -l < $out)"
done
cp $W/scripts/svc_head.ts $SVC; cp $W/scripts/routes_head.ts $RT
mv $PROBE $W/logs/_quarantine/g121_pg.test.ts.ran
shasum -a 256 $SVC $RT
git -C $W/repo status --short
