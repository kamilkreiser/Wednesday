#!/bin/bash
# usage: probe.sh  -> runs the probe at base product (03977e89a343) and at head product, restores head by sha256.
set -u
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate95-ks1868-pr1913
R=$G/repo
A=$R/Blockchain/Dev/services/billing
P=$A/src/routes/webhooks.ts
T=$A/src/__tests__/zz-gate95-probe.test.ts
HEADSHA=$(shasum -a 256 $P | awk '{print $1}')
cp $G/scripts/probe.test.ts $T
for ver in base head; do
  if [ $ver = base ]; then git -C $R show 03977e89a343:Blockchain/Dev/services/billing/src/routes/webhooks.ts > $P; fi
  if [ $ver = head ]; then git -C $R show pr1913:Blockchain/Dev/services/billing/src/routes/webhooks.ts > $P; fi
  echo "$ver product sha256 $(shasum -a 256 $P | awk '{print $1}')" >> $G/logs/probe_runs.log
  mkdir -p $G/logs/_quarantine; [ -f $G/logs/probe_$ver.jsonl ] && mv $G/logs/probe_$ver.jsonl $G/logs/_quarantine/probe_$ver.$(date +%s).jsonl
  PROBE_OUT=$G/logs/probe_$ver.jsonl PROBE_LABEL=$ver bash $G/scripts/vt.sh $G/logs/probe_${ver}_vitest.log zz-gate95-probe
  echo "probe $ver rc=$?" >> $G/logs/probe_runs.log
done
mkdir -p $G/logs/_quarantine; mv $T $G/logs/_quarantine/zz-gate95-probe.test.ts.moved
git -C $R show pr1913:Blockchain/Dev/services/billing/src/routes/webhooks.ts > $P
NOW=$(shasum -a 256 $P | awk '{print $1}')
[ "$NOW" = "$HEADSHA" ] && echo "RESTORE_OK $NOW" >> $G/logs/probe_runs.log || echo "RESTORE_FAIL" >> $G/logs/probe_runs.log
git -C $R status --short >> $G/logs/probe_runs.log
