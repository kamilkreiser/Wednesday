#!/bin/zsh
# usage: runprobe.sh <label> <nodeenv>  ; runs the probe against whatever verifier product is in the tree
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate109-ks1868-pr1927
N=$W/repo/Blockchain/Dev/services/nft-certificate
cp $W/scripts/g109_probe.test.ts $N/src/__tests__/g109_probe.test.ts
: > $W/logs/probe_$1_$2.jsonl
IPFS_PROVIDER=pinata PINATA_API_KEY=k PINATA_SECRET_KEY=s NODE_ENV=$2 G109_LABEL=$1 G109_OUT=$W/logs/probe_$1_$2.jsonl $N/node_modules/.bin/vitest run --root $N src/__tests__/g109_probe.test.ts > $W/logs/probe_$1_$2.out 2>&1
echo "$1 $2 rc=$?"
mv $N/src/__tests__/g109_probe.test.ts $W/scripts/_quarantine/g109_probe.$1.$2.moved.ts
