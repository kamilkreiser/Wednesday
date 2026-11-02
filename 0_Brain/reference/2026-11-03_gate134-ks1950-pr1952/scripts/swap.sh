#!/bin/bash
# usage: swap.sh base|head|status  — the two product .ts files only; head restore asserted by sha256
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate134-ks1950-pr1952
R=$G/repo; S=Blockchain/Dev/services/governance/src; MB=8150eeb3802bd9cfe5242ffbc49278c1a3739a84
P="services/governanceService.ts governance.openapi.ts"
mkdir -p $G/logs/prod/base $G/logs/prod/head
for f in $P; do n=$(echo $f | tr / _)
  [ -f $G/logs/prod/head/$n ] || git -C $R show refs/gate/pr1952:$S/$f > $G/logs/prod/head/$n
  [ -f $G/logs/prod/base/$n ] || git -C $R show $MB:$S/$f > $G/logs/prod/base/$n
  case "$1" in base) cp $G/logs/prod/base/$n $R/$S/$f;; head) cp $G/logs/prod/head/$n $R/$S/$f;; esac
  echo "$f $(shasum -a 256 $R/$S/$f | cut -c1-12) head=$(shasum -a 256 $G/logs/prod/head/$n | cut -c1-12) base=$(shasum -a 256 $G/logs/prod/base/$n | cut -c1-12)"
done
