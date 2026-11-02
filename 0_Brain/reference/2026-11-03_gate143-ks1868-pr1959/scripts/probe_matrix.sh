#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate143-ks1868-pr1959
T=$W/repo/Blockchain/Dev/node_modules/.bin/tsx
: > $W/logs/probe_matrix.jsonl
for env in development production; do for site in ctor listener; do for v in base head; do
for c in ordinary revokedProxy getterThrows msg42 msgUndefined msgNull msgSymbol msgObjToStringThrows msgObjToString nullValue undefinedValue plainString num42 symbolValue; do
  NODE_ENV=$env $T $W/scripts/probe_child.ts $v $site $c >> $W/logs/probe_matrix.jsonl 2>> $W/logs/probe_stderr.log
done; done; done; done
echo done
