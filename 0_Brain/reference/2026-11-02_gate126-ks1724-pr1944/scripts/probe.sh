#!/bin/bash
# usage: probe.sh <repo|base> <service> ; copies the probe + helper into the service's src/__tests__, runs, moves them to quarantine.
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate126-ks1724-pr1944
T=$1; S=$2; A=$G/$T/Blockchain/Dev/services/$S/src/__tests__; Q=$G/logs/_quarantine; mkdir -p $Q
cp $G/scripts/probes/common.ts $A/zz-gate126-common.ts
cp $G/scripts/probes/$S.probe.ts $A/zz-gate126-probe.test.ts
: > $G/logs/probe_${S}_$T.jsonl
PROBE_TREE=$T PROBE_OUT=$G/logs/probe_${S}_$T.jsonl bash $G/scripts/vt.sh $T services/$S $G/logs/probe_${S}_${T}_vitest.log zz-gate126-probe; echo "probe $S $T rc=$?"
mv $A/zz-gate126-common.ts $Q/${S}_${T}_common.ts; mv $A/zz-gate126-probe.test.ts $Q/${S}_${T}_probe.test.ts
git -C $G/$T status --short
