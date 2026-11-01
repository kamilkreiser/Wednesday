#!/bin/bash
# usage: probe.sh base|head  (swaps product file for base, restores). The probe file is moved to a quarantine dir, never deleted.
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate85-ks1868-kyc-1900
A=$G/repo/Blockchain/Dev/services/kyc; M=$A/src/index.ts
sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
H1=$(sha $M); Q=$G/logs/_quarantine; mkdir -p $Q
[ "$1" = base ] && cp $G/logs/mergebase_index.ts $M
echo "product sha for $1: $(sha $M)"
cp $G/scripts/probe.test.ts $A/src/__tests__/zz-gate85-probe.test.ts
: > $G/logs/probe_$1.jsonl
PROBE_OUT=$G/logs/probe_$1.jsonl bash $G/scripts/vt.sh $G/logs/probe_$1_vitest.log zz-gate85-probe; echo "probe $1 rc=$?"
mv $A/src/__tests__/zz-gate85-probe.test.ts $Q/probe_$1.test.ts
cp $G/logs/head_index.ts $M
[ "$(sha $M)" = "$H1" ] && echo RESTORE_OK || echo RESTORE_FAIL
git -C /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate85-ks1868-kyc-1900/repo status --short
