#!/bin/bash
# usage: probe.sh base|head. Swaps the two product files for base, restores by sha. Probe file is moved to quarantine.
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate133-ks1868-pr1951
A=$G/repo/Blockchain/Dev/services/nft-certificate; S=$A/src/services
sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
Q=$G/logs/_quarantine; mkdir -p $Q
if [ "$1" = base ]; then cp $G/logs/base_ipfs.service.ts $S/ipfs.service.ts; cp $G/logs/base_blockchain-verifier.service.ts $S/blockchain-verifier.service.ts; fi
echo "product sha for $1: $(sha $S/ipfs.service.ts) $(sha $S/blockchain-verifier.service.ts)"
cp $G/scripts/probe.test.ts $A/src/__tests__/zz-gate133-probe.test.ts
: > $G/logs/probe_$1.jsonl
PROBE_VERSION=$1 PROBE_OUT=$G/logs/probe_$1.jsonl bash $G/scripts/vt.sh $G/logs/probe_$1_vitest.log zz-gate133-probe; echo "probe $1 rc=$?"
mv $A/src/__tests__/zz-gate133-probe.test.ts $Q/probe_$1.$(date +%s).test.ts
cp $G/logs/head_ipfs.service.ts $S/ipfs.service.ts; cp $G/logs/head_blockchain-verifier.service.ts $S/blockchain-verifier.service.ts
[ "$(sha $S/ipfs.service.ts)" = 27e149641d0bc2794afe0a1b9db44b603fb29019645d3ce8f7a8625e13c71b64 ] && [ "$(sha $S/blockchain-verifier.service.ts)" = 9b03deadb7dcf8eaaf1fa863373e32725ee624f7c95c0190c3b6b2bb21ce95ec ] && echo RESTORE_OK || echo RESTORE_FAIL
git -C /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate133-ks1868-pr1951/repo status --short
