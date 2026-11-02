#!/bin/bash
# usage: probe.sh base|head <probe-name>   (swaps product for base, restores by sha). Probe file moved to quarantine.
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate103-ks1868-pr1921
A=$G/repo/Blockchain/Dev/services/kyc; M=$A/src/index.ts
sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
H1=$(sha $G/logs/head_index.ts); Q=$G/logs/_quarantine; mkdir -p $Q
[ "$(sha $M)" = "$H1" ] || { echo "PRODUCT NOT HEAD AT START"; exit 9; }
[ "$1" = base ] && cp $G/logs/mergebase_index.ts $M
echo "product sha for $1: $(sha $M)"
cp $G/scripts/probe_$2.test.ts $A/src/__tests__/zz-gate103-probe-$2.test.ts
: > $G/logs/probe_$2_$1.jsonl
PROBE_OUT=$G/logs/probe_$2_$1.jsonl bash $G/scripts/vt.sh $G/logs/probe_$2_$1_vitest.log zz-gate103-probe-$2; echo "probe $2 $1 rc=$?"
mv $A/src/__tests__/zz-gate103-probe-$2.test.ts $Q/probe_$2_$1.test.ts
cp $G/logs/head_index.ts $M
[ "$(sha $M)" = "$H1" ] && echo RESTORE_OK || echo RESTORE_FAIL
git -C /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate103-ks1868-pr1921/repo status --short
