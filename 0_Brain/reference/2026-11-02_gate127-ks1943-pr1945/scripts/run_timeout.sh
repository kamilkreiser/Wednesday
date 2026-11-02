#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate127-ks1943-pr1945
D=$W/repo/Blockchain/Dev
export TMPDIR=/tmp/g127
set -a; . /tmp/g127/pg/env; set +a
export G127_PG_PORT=$(docker port g127-pg 5432 | sed 's/.*://')
echo "node $(node -v) load $(sysctl -n vm.loadavg) $(date -u +%T)"
for v in ${VERSIONS:-head base}; do
  bash $W/scripts/swap.sh $v || exit 9
  for m in st mt; do
    nice -n 10 $D/node_modules/.bin/tsx $W/scripts/pgtimeout_g127.mts ${TAG:-}$v $m $W/logs/pgto_${TAG:-}${v}_$m.json ${HOLD:-9000} > $W/logs/pgto_${TAG:-}${v}_$m.txt 2>&1; echo "$v $m rc=$?"
  done
done
bash $W/scripts/swap.sh head
