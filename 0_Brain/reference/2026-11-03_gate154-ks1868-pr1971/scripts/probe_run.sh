#!/bin/bash
# usage: probe_run.sh base|head  -> logs/probe_<v>.jsonl ; product file swapped, sha restored
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate154-ks1868-pr1971
M=$W/repo/Blockchain/Dev/services/m365-integration
P=$M/src/oauthState.ts; HEADSHA=7c7c0adcbe5c419a55b75412b451081393b0d32e31d165234fee1c544c612e4f
cp $W/scripts/ks1868-g154-probe.test.ts $M/src/__tests__/ks1868-g154-probe.test.ts
[ "$1" = base ] && cp $W/scripts/oauthState.base.ts $P
: > $W/logs/probe_$1.jsonl
G154_OUT=$W/logs/probe_$1.jsonl $W/repo/Blockchain/Dev/node_modules/.bin/vitest run --root $M src/__tests__/ks1868-g154-probe.test.ts > $W/logs/probe_$1.out 2>&1; echo rc=$? >> $W/logs/probe_$1.out
git -C $W/repo show pr1971:Blockchain/Dev/services/m365-integration/src/oauthState.ts > $P
mv $M/src/__tests__/ks1868-g154-probe.test.ts $W/logs/_probe_copy_$1.ts
[ "$(shasum -a 256 $P | cut -d' ' -f1)" = "7c7c0adcbe5c419a55b75412b451081393b0d32e31d165234fee1c544c612e4f" ] && echo restored OK
tail -6 $W/logs/probe_$1.out; wc -l $W/logs/probe_$1.jsonl
