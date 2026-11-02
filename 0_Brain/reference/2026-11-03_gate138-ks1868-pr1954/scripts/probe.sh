#!/bin/bash
# usage: probe.sh base|head
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate138-ks1868-pr1954
A=$W/repo/Blockchain/Dev/services/api-gateway; M=$A/src/routes/admin.ts
sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
git -C $W/repo show pr1954:Blockchain/Dev/services/api-gateway/src/routes/admin.ts > $W/logs/admin_head.ts
git -C $W/repo show 9a9bf86967e3:Blockchain/Dev/services/api-gateway/src/routes/admin.ts > $W/logs/admin_base.ts
[ "$1" = base ] && cp $W/logs/admin_base.ts $M || cp $W/logs/admin_head.ts $M
echo "product sha for $1: $(sha $M)"
cp $W/scripts/g138_probe.test.ts $A/src/__tests__/zz-g138-probe.test.ts
PROBE_REAL_CONSOLE=${RC_ON:-} PROBE_OUT=$W/logs/probe_${1}${SUF:-}.jsonl nice -n 10 $W/repo/Blockchain/Dev/node_modules/.bin/vitest run --root $A --maxWorkers=2 zz-g138-probe > $W/logs/probe_${1}${SUF:-}_vitest.log 2>&1; echo "probe $1 rc=$?"
mv $A/src/__tests__/zz-g138-probe.test.ts $W/scripts/_quarantine/probe_$1.test.ts
cp $W/logs/admin_head.ts $M
[ "$(sha $M)" = "$(sha $W/logs/admin_head.ts)" ] && echo RESTORE_OK || echo RESTORE_FAIL
