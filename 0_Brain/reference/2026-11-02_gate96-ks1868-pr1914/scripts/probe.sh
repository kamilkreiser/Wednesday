#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate96-ks1868-pr1914
RR=$W/repo; A=$RR/Blockchain/Dev/services/analytics
P=Blockchain/Dev/services/analytics/src/routes/analytics.ts
pushd $A >/dev/null
cp $W/scripts/probe.test.ts src/__tests__/zz-gate96-probe.test.ts
git -C $RR show refs/qa/pr1914:$P > src/routes/analytics.ts
PROBE_OUT=$W/logs/probe_head.json npx vitest run src/__tests__/zz-gate96-probe.test.ts > $W/logs/probe_head.log 2>&1; echo head RC=$?
git -C $RR show 03977e89a343:$P > src/routes/analytics.ts
PROBE_OUT=$W/logs/probe_base.json npx vitest run src/__tests__/zz-gate96-probe.test.ts > $W/logs/probe_base.log 2>&1; echo base RC=$?
git -C $RR show refs/qa/pr1914:$P > src/routes/analytics.ts
mkdir -p $W/_quarantine_2026-11-02; mv src/__tests__/zz-gate96-probe.test.ts $W/_quarantine_2026-11-02/
[ "$(shasum -a 256 src/routes/analytics.ts | cut -c1-16)" = d5afff9cd2073371 ] && echo RESTORE_OK
