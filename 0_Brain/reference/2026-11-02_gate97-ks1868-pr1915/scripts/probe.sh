#!/bin/bash
# usage: probe.sh base|head
P=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate97-ks1868-pr1915
S=$P/repo/Blockchain/Dev/services/nft-certificate
F=$S/src/services/ipfs.service.ts
HSHA=$(shasum -a 256 $F | cut -d' ' -f1)
echo "head sha $HSHA" > $P/logs/probe_$1.sha
cp $P/scripts/probe_route.test.ts $S/src/__tests__/gate97_probe.test.ts
if [ "$1" = base ]; then git -C $P/repo show 03977e89a343:Blockchain/Dev/services/nft-certificate/src/services/ipfs.service.ts > $F; fi
echo "in-use sha $(shasum -a 256 $F | cut -d' ' -f1)" >> $P/logs/probe_$1.sha
PROBE_OUT=$P/logs/probe_$1.json nice -n 10 $P/repo/Blockchain/Dev/node_modules/.bin/vitest run --root $S --maxWorkers=1 src/__tests__/gate97_probe.test.ts > $P/logs/probe_$1.log 2>&1
echo "rc=$?" >> $P/logs/probe_$1.log
git -C $P/repo checkout -q -- Blockchain/Dev/services/nft-certificate/src/services/ipfs.service.ts
mv $S/src/__tests__/gate97_probe.test.ts $P/logs/_quarantine/gate97_probe.$1.test.ts
echo "restored sha $(shasum -a 256 $F | cut -d' ' -f1) (want $HSHA)" >> $P/logs/probe_$1.sha
