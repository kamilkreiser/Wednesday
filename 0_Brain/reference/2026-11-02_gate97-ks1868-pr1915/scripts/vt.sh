#!/bin/bash
# usage: vt.sh <label> [vitest args...]  (nft-certificate)
P=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate97-ks1868-pr1915
A=$P/repo/Blockchain/Dev/services/nft-certificate
L=$1; shift
nice -n 10 $P/repo/Blockchain/Dev/node_modules/.bin/vitest run --root $A --maxWorkers=2 "$@" > $P/logs/$L.log 2>&1
echo "rc=$?" >> $P/logs/$L.log
