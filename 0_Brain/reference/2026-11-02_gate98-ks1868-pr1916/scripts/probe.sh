#!/bin/bash
# usage: probe.sh base|head
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate98-ks1868-pr1916
A=$G/repo/Blockchain/Dev/services/api-gateway; M=$A/src/routes/admin.ts
sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
H1=$(sha $M); Q=$G/logs/_quarantine; mkdir -p $Q
[ "$1" = base ] && cp $G/logs/admin_base.ts $M
echo "product sha for $1: $(sha $M)"
cp $G/scripts/probe2.test.ts $A/src/__tests__/zz-gate98-probe.test.ts
PROBE_OUT=$G/logs/probe_$1.jsonl bash $G/scripts/vt.sh $G/logs/probe_$1_vitest.log zz-gate98-probe; echo "probe $1 rc=$?"
mv $A/src/__tests__/zz-gate98-probe.test.ts $Q/probe_$1.test.ts
cp $G/logs/admin_head.ts $M
[ "$(sha $M)" = "$H1" ] && echo RESTORE_OK || echo RESTORE_FAIL
