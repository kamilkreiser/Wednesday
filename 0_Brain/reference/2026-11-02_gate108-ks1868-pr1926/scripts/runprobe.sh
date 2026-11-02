#!/bin/zsh
# usage: runprobe.sh <label> ; run the probe for 3 providers against whatever product is checked out
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate108-ks1868-pr1926
N=$W/repo/Blockchain/Dev/services/nft-certificate
cp $W/scripts/g108_probe.test.ts $N/src/__tests__/g108_probe.test.ts
for P in pinata infura web3storage; do
  : > $W/logs/probe_$1_$P.jsonl
  G108_PROVIDER=$P G108_OUT=$W/logs/probe_$1_$P.jsonl $N/node_modules/.bin/vitest run --root $N src/__tests__/g108_probe.test.ts > $W/logs/probe_$1_$P.out 2>&1
  echo "$P rc=$?"
done
mv $N/src/__tests__/g108_probe.test.ts $W/scripts/_quarantine/g108_probe.$1.moved.ts
