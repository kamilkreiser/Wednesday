#!/bin/bash
# runs the gate probe at base product (PR 1913 head webhooks.ts) and at head product; restores head by sha256.
set -u
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate100-ks1933-pr1918
R=$G/repo; A=$R/Blockchain/Dev/services/billing; P=$A/src/routes/webhooks.ts; T=$A/src/__tests__/zz-gate100-probe.test.ts
HEADSHA=$(shasum -a 256 $P | awk '{print $1}')
: > $G/logs/probe_runs.log
cp $G/scripts/probe.test.ts $T
for ver in base head; do
  git -C $R show pr$([ $ver = base ] && echo 1913 || echo 1918):Blockchain/Dev/services/billing/src/routes/webhooks.ts > $P
  echo "$ver product sha256 $(shasum -a 256 $P | awk '{print $1}')" >> $G/logs/probe_runs.log
  mkdir -p $G/logs/_quarantine; [ -f $G/logs/probe_$ver.jsonl ] && mv $G/logs/probe_$ver.jsonl $G/logs/_quarantine/probe_$ver.$(date +%s).jsonl
  PROBE_OUT=$G/logs/probe_$ver.jsonl PROBE_LABEL=$ver bash $G/scripts/vt.sh $G/logs/probe_${ver}_vitest.log zz-gate100-probe
  echo "probe $ver rc=$?" >> $G/logs/probe_runs.log
done
mv $T $G/logs/_quarantine/zz-gate100-probe.test.ts.moved
git -C $R show pr1918:Blockchain/Dev/services/billing/src/routes/webhooks.ts > $P
NOW=$(shasum -a 256 $P | awk '{print $1}')
[ "$NOW" = "$HEADSHA" ] && echo "RESTORE_OK $NOW" >> $G/logs/probe_runs.log || echo "RESTORE_FAIL" >> $G/logs/probe_runs.log
git -C $R status --short >> $G/logs/probe_runs.log
