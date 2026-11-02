#!/bin/bash
# usage: probe.sh base|head
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate134-ks1950-pr1952
A=$G/repo/Blockchain/Dev/services/governance; Q=$G/logs/_quarantine; mkdir -p $Q
bash $G/scripts/swap.sh $1
cp $G/scripts/probe.test.ts $A/src/__tests__/zz-gate134-probe.test.ts
: > $G/logs/probe_$1.jsonl
PROBE_OUT=$G/logs/probe_$1.jsonl RACE_N=${RACE_N:-150} bash $G/scripts/jt.sh $G/logs/probe_$1_jest.log zz-gate134-probe; echo "probe $1 rc=$?"
mv $A/src/__tests__/zz-gate134-probe.test.ts $Q/probe_$1_$(date +%H%M%S).test.ts
bash $G/scripts/swap.sh head
git -C $G/repo status --short
