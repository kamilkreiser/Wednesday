#!/bin/bash
# usage: run.sh <tree: head|dev|prev> <mem|pg> <outname> [harness file name, default gate1521.test.ts]
set -uo pipefail
W=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/f2077cbf-bb12-49ee-8d59-f5f537b335e0/scratchpad/g1521r1
T=$1; M=$2; O=$3; H=${4:-gate1521.test.ts}
S=$W/$T/Blockchain/Dev/services/security
mkdir -p $W/out
cp $W/harness/$H $S/src/__tests__/zz_gate_$H
if [ "$M" = pg ]; then export GATE_DB=1; else unset GATE_DB; fi
export GATE_OUT=$W/out/$O.json
(cd $S && npx vitest run src/__tests__/zz_gate_$H) > $W/out/$O.log 2>&1
rc=$?
mv $S/src/__tests__/zz_gate_$H $W/out/.used_$O.$H
echo "$T $M $O rc=$rc $(grep -E '^\s+Tests ' $W/out/$O.log)"
test -s $GATE_OUT && echo "out written: $(wc -c < $GATE_OUT) bytes" || echo "OUT MISSING"
