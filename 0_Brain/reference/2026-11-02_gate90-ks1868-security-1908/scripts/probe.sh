#!/bin/bash
# usage: probe.sh base|head  (swaps the product file for base, restores). Probe files are moved to a quarantine dir, never deleted.
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate90-ks1868-security-1908
A=$G/repo/Blockchain/Dev/services/security; M=$A/src/index.ts
sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
H1=$(sha $M); Q=$G/logs/_quarantine; mkdir -p $Q
[ "$1" = base ] && cp $G/logs/mergebase_index.ts $M
echo "product sha for $1: $(sha $M)"
for p in p1 p2; do
  cp $G/scripts/probe_$p.test.ts $A/src/__tests__/zz-gate90-probe-$p.test.ts
  : > $G/logs/probe_${p}_$1.jsonl
  PROBE_OUT=$G/logs/probe_${p}_$1.jsonl bash $G/scripts/vt.sh $G/logs/probe_${p}_$1_vitest.log zz-gate90-probe-$p; echo "probe $p $1 rc=$?"
  mv $A/src/__tests__/zz-gate90-probe-$p.test.ts $Q/probe_${p}_$1.test.ts
done
cp $G/logs/head_index.ts $M
[ "$(sha $M)" = "$H1" ] && echo RESTORE_OK || echo RESTORE_FAIL
git -C /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate90-ks1868-security-1908/repo status --short
