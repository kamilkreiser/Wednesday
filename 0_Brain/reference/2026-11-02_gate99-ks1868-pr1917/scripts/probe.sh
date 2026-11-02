#!/bin/bash
# usage: probe.sh base|head. Swaps the product for base, runs the probe, restores head; probe file moved to quarantine.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate99-ks1868-pr1917
A=$W/repo/Blockchain/Dev/services/tenant-provisioning; M=$A/src/index.ts
sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
H1=$(sha $W/logs/head_index.ts); Q=$W/logs/_quarantine; mkdir -p $Q
[ "$1" = base ] && cp $W/logs/base_index.ts $M
echo "product sha for $1: $(sha $M)"
cp $W/scripts/probe.test.ts $A/src/__tests__/zz-gate99-probe.test.ts
: > $W/logs/probe_$1.jsonl
PROBE_OUT=$W/logs/probe_$1.jsonl bash $W/scripts/vt.sh $W/logs/probe_$1_vitest.log zz-gate99-probe; echo "probe $1 rc=$?"
mv $A/src/__tests__/zz-gate99-probe.test.ts $Q/probe_$1.test.ts
cp $W/logs/head_index.ts $M
[ "$(sha $M)" = "$H1" ] && echo RESTORE_OK || echo RESTORE_FAIL
git -C /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate99-ks1868-pr1917/repo status --short
