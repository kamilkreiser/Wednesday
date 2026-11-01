#!/bin/bash
P=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate97-ks1868-pr1915
S=$P/repo/Blockchain/Dev/services/nft-certificate
T=src/__tests__/ks1868-ipfs-fetch-unreadable-throw.test.ts
G="git -C $P/repo"
$G status --short > $P/logs/status_pre.log
bash $P/scripts/vt.sh whole_head
$G show 03977e89a343:Blockchain/Dev/services/nft-certificate/src/services/ipfs.service.ts > $S/src/services/ipfs.service.ts
bash $P/scripts/vt.sh red_base $T
mv $S/$T $P/logs/_quarantine/newtest.ts
bash $P/scripts/vt.sh whole_base
$G checkout -q -- Blockchain/Dev/services/nft-certificate
$G status --short > $P/logs/status_post.log
shasum -a 256 $S/src/services/ipfs.service.ts $S/$T > $P/logs/suite_sha.log
