#!/bin/zsh
# usage: g1525_run.sh <head|base|asis> <true|false> <tag> [timingN]   (tags must be unique: outputs are never overwritten)
set -u
S=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/f2077cbf-bb12-49ee-8d59-f5f537b335e0/scratchpad
WT=$S/g1525_head; O=$WT/Blockchain/Dev/services/originate; F=$O/src/routes/certifications.ts
L=$S/g1525_logs; mkdir -p $L
[ -e $L/probe_$3.json ] && { echo "tag $3 used"; exit 8; }
HEADSHA=$(git -C $WT show b8393a44ec33984f7380cf5fdfb4f9cd8e87cd74:Blockchain/Dev/services/originate/src/routes/certifications.ts | shasum -a 256 | cut -c1-16)
BASESHA=$(git -C $WT show 69878dc5d1ae4b717834c547c47d8bc036625d2e:Blockchain/Dev/services/originate/src/routes/certifications.ts | shasum -a 256 | cut -c1-16)
if [ "$1" = base ]; then git -C $WT show 69878dc5d1ae4b717834c547c47d8bc036625d2e:Blockchain/Dev/services/originate/src/routes/certifications.ts > $F; WANT=$BASESHA
elif [ "$1" = head ]; then git -C $WT checkout -q -- Blockchain/Dev/services/originate/src/routes/certifications.ts; WANT=$HEADSHA
else WANT=$(shasum -a 256 $F | cut -c1-16); fi
GOT=$(shasum -a 256 $F | cut -c1-16)
[ "$GOT" = "$WANT" ] || { echo "SRC ASSERT FAILED got=$GOT want=$WANT"; exit 9; }
echo "src=$1 certifications.ts sha16=$GOT (head=$HEADSHA base=$BASESHA)"
cp $S/g1525_probe.integration.test.ts $O/src/__tests__/zz-gate1525-probe.integration.test.ts
source $S/g1525_pg/pg.env
export MULTI_TENANCY_ENABLED=$2 PROBE_OUT=$L/probe_$3.json PROBE_TIMING_N=${4:-0}
( builtin cd $O && npx jest --config jest.integration.config.js zz-gate1525-probe > $L/probe_$3.log 2>&1 ); rc=$?
echo "jest rc=$rc"; grep -E "Tests:|✓|✕" $L/probe_$3.log | head -20; cat $PROBE_OUT.cleanup 2>/dev/null
