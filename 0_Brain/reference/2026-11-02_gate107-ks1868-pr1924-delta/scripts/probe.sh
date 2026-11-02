#!/bin/bash
# usage: probe.sh c415|head   (runs probe3 against that product; restores head sha-exact)
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate107-ks1868-pr1924-delta
R=$W/repo; A=$R/Blockchain/Dev/services/originate; F=$A/src/routes/certifications.ts
H=18e43169e1b2fba8
h0=$(shasum -a 256 $F | cut -d' ' -f1); case $h0 in $H*) ;; *) echo "HEAD SHA MISMATCH $h0"; exit 9;; esac
cp $F $W/logs/_quarantine/cert_head_probe.ts
if [ "$1" = c415 ]; then git -C $R show c4159470a859ed9cf0cb7ffc8f1004e4cac9b8e7:Blockchain/Dev/services/originate/src/routes/certifications.ts > $F; fi
echo "product sha: $(shasum -a 256 $F | cut -c1-16)"
cp $W/scripts/probe3.test.ts $A/src/__tests__/zz-gate107-probe3.test.ts
: > $W/logs/probe3_$1.jsonl
(cd $A && PROBE_OUT=$W/logs/probe3_$1.jsonl nice -n 10 npx jest zz-gate107-probe3 > $W/logs/probe3_$1_jest.log 2>&1); echo "probe3 $1 rc=$?"
mv $A/src/__tests__/zz-gate107-probe3.test.ts $W/logs/_quarantine/probe3_$1.test.ts
cp $W/logs/_quarantine/cert_head_probe.ts $F; [ "$(shasum -a 256 $F | cut -d' ' -f1)" = "$h0" ] && echo RESTORE_OK
git -C $R status --short
