#!/bin/bash
# runprobe.sh base|head test|production
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate113-ks1868-pr1931
D=$W/repo/Blockchain/Dev
bash $W/scripts/swap.sh "$1" > $W/logs/swap_$1_$2.log
cp $W/scripts/g113_probe.test.ts $D/services/auth/src/__tests__/g113_probe.test.ts
G113_OUT=$W/logs/probe_$1_$2.jsonl G113_FMT=$2 $D/node_modules/.bin/vitest run --root $D/services/auth g113_probe > $W/logs/probe_$1_$2.out 2>&1
echo "rc=$? $(wc -l < $W/logs/probe_$1_$2.jsonl) records"
mv $D/services/auth/src/__tests__/g113_probe.test.ts $W/scripts/_probe_copy_last.ts
bash $W/scripts/swap.sh head > /dev/null
