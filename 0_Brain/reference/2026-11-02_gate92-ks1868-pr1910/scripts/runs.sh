#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate92-ks1868-pr1910
R=$W/repo; M=$R/Blockchain/Dev/services/mcp-server; L=$W/logs
P=$M/src/http-server.ts
v() { (cd $M && npx vitest run "$@"); }
sha256sum() { shasum -a 256 "$@"; }
v > $L/head_suite.log 2>&1; echo head_suite rc=$? >> $L/summary.log; tail -6 $L/head_suite.log >> $L/summary.log
v src/__tests__/ks1410 src/__tests__/ks1901 src/__tests__/ks1868-hash src/__tests__/ks1893 src/__tests__/ks1232 > $L/head_pins.log 2>&1; echo pins rc=$? >> $L/summary.log; tail -6 $L/head_pins.log >> $L/summary.log
cp $P $W/http-server.head.ts
# base product, new tests present
git -C $R show origin/develop:Blockchain/Dev/services/mcp-server/src/http-server.ts > $P
v > $L/base_with_new.log 2>&1; echo base_with_new rc=$? >> $L/summary.log; tail -6 $L/base_with_new.log >> $L/summary.log
v src/__tests__/ks1410 src/__tests__/ks1901 > $L/base_pins.log 2>&1; echo base_pins rc=$? >> $L/summary.log; tail -6 $L/base_pins.log >> $L/summary.log
cp $W/http-server.head.ts $P
shasum -a 256 $P $W/http-server.head.ts >> $L/summary.log
