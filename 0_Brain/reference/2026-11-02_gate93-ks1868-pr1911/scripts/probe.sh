#!/bin/bash
# usage: probe.sh base|head <probe-name>  (swaps auth.ts for base, restores to head; probe file moved to quarantine after)
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate93-ks1868-pr1911
A=$G/repo/Blockchain/Dev/services/auth; M=$A/src/routes/auth.ts
sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
H1=$(sha $G/logs/head_auth.ts); Q=$G/logs/_quarantine; mkdir -p $Q
[ "$(sha $M)" = "$H1" ] || { echo "product not at head before run"; exit 3; }
[ "$1" = base ] && cp $G/logs/base_auth.ts $M
echo "product sha for $1: $(sha $M)"
cp $G/scripts/$2.test.ts $A/src/__tests__/zz-gate93-$2.test.ts
: > $G/logs/$2_$1.jsonl
PROBE_OUT=$G/logs/$2_$1.jsonl bash $G/scripts/vt.sh $G/logs/$2_$1_vitest.log zz-gate93-$2; echo "probe $2 $1 rc=$?"
mv $A/src/__tests__/zz-gate93-$2.test.ts $Q/$2_$1.test.ts
cp $G/logs/head_auth.ts $M
[ "$(sha $M)" = "$H1" ] && echo RESTORE_OK || echo RESTORE_FAIL
git -C /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate93-ks1868-pr1911/repo status --short
