#!/bin/bash
# usage: cells.sh <label> [c415 | mut:<line>]  runs the 3 PR test files against that product, json out; restores head sha-exact
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate107-ks1868-pr1924-delta
R=$W/repo; A=$R/Blockchain/Dev/services/originate; F=$A/src/routes/certifications.ts
h0=$(shasum -a 256 $F | cut -d' ' -f1); case $h0 in 18e43169e1b2fba8*) ;; *) echo "HEAD SHA MISMATCH $h0"; exit 9;; esac
cp $F $W/logs/_quarantine/cert_head_cells.ts
case "$2" in
  c415) git -C $R show c4159470a859ed9cf0cb7ffc8f1004e4cac9b8e7:Blockchain/Dev/services/originate/src/routes/certifications.ts > $F;;
  mut:*) L=${2#mut:}; python3 - "$F" "$L" <<'PY'
import sys
p,l=sys.argv[1],int(sys.argv[2]); s=open(p).read().split('\n')
new='        reason = String(error instanceof Error ? error.message : error);'
old='        reason = error instanceof Error ? error.message : String(error);'
assert s[l-1]==new, ('placement', s[l-1]); s[l-1]=old; open(p,'w').write('\n'.join(s))
print('mutated line',l)
PY
  ;;
esac
echo "product sha: $(shasum -a 256 $F | cut -c1-16)"
(cd $A && nice -n 10 npx jest --json --outputFile=$W/logs/cells_$1.json ks1868-certifications > $W/logs/cells_$1_jest.log 2>&1); echo "cells $1 rc=$?"
cp $W/logs/_quarantine/cert_head_cells.ts $F; [ "$(shasum -a 256 $F | cut -d' ' -f1)" = "$h0" ] && echo RESTORE_OK
git -C $R status --short
