#!/bin/bash
# run_probe.sh <side: base|head|merged> <outname>
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate159-ks1868-pr1976
side=$1; out=$2
P=$W/wt2_$side/Blockchain/Dev/services/anchoring/src/__tests__/zz_gate159_probe.test.ts
cp "$W/scripts/gate159_probe.test.ts" "$P"
: > "$W/logs/$out.jsonl"
GATE_OUT="$W/logs/$out.jsonl" GATE_SIDE=$side bash "$W/scripts/vt3.sh" "$side" "$out" src/__tests__/zz_gate159_probe.test.ts
wc -l "$W/logs/$out.jsonl"
