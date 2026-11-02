#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate143-ks1868-pr1959; R=$W/repo; L=$W/logs
git -C $R fetch origin develop > $L/fetch3.log 2>&1; echo fetch rc=$?
D=$(git -C $R rev-parse origin/develop); echo develop=$D
git -C $R log --oneline cc33e702..$D
git -C $R diff --name-only cc33e702 $D > $L/develop_since_cc33.log; cat $L/develop_since_cc33.log | head -30
git -C $R merge-tree --write-tree --name-only $D pr1959 > $L/mergetree2.out 2>&1; echo merge-tree rc=$?; cat $L/mergetree2.out
T=$(head -1 $L/mergetree2.out); git -C $R diff --name-status $D $T | tee $L/mergetree2_paths.log
git -C $R diff --name-status $D...pr1959 | diff - $L/mergetree2_paths.log && echo paths-equal
git -C $R rev-parse $T:Blockchain/Dev/services/auth/src/events.ts pr1959:Blockchain/Dev/services/auth/src/events.ts
git -C $R show $D:Blockchain/Dev/services/auth/src/events.ts | shasum -a 256; git -C $R show 2d3b3bb3:Blockchain/Dev/services/auth/src/events.ts | shasum -a 256
git -C $R grep -n "initEventBus" $D -- Blockchain/Dev/services/auth/src/index.ts
git -C $R diff cc33e702~1 cc33e702 -- Blockchain/Dev/services/auth/src/index.ts
grep -n "^import" $R/Blockchain/Dev/services/auth/src/events.ts
