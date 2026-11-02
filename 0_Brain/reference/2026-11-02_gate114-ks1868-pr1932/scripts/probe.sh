#!/bin/bash
# usage: probe.sh <base|head>   runs both probes; product swapped to base for 'base', restored after.
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate114-ks1868-pr1932
R=$G/repo; STAGE=$1
PA=Blockchain/Dev/services/anchoring/src/index.ts; PO=Blockchain/Dev/services/originate/src/routes/anchors.ts
AP=$R/Blockchain/Dev/services/anchoring/src/__tests__/g114_anch_probe.test.ts
OP=$R/Blockchain/Dev/services/originate/src/__tests__/g114_orig_probe.test.ts
SC=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/a974be12-1abe-4d9a-9532-9c46296d28fc/scratchpad/g114cwd; mkdir -p $SC
if [ "$STAGE" = base ]; then git -C $R show cd9c4a7dd3b8:$PA > $R/$PA; git -C $R show cd9c4a7dd3b8:$PO > $R/$PO; fi
cp $G/scripts/g114_anch_probe.test.ts $AP; cp $G/scripts/g114_orig_probe.test.ts $OP
: > $G/logs/probe_anch_$STAGE.jsonl
G114_OUT=$G/logs/probe_anch_$STAGE.jsonl G114_STAGE=$STAGE bash $G/scripts/run.sh anchoring $G/logs/probe_anch_${STAGE}_run src/__tests__/g114_anch_probe.test.ts
for E in test production; do
  : > $G/logs/probe_orig_${STAGE}_$E.jsonl
  G114_OUT=$G/logs/probe_orig_${STAGE}_$E.jsonl G114_STAGE=$STAGE G114_LOGENV=$E G114_CWD=$SC bash $G/scripts/run.sh originate $G/logs/probe_orig_${STAGE}_${E}_run --runTestsByPath $OP
done
mkdir -p $G/logs/_probe_copies; mv $AP $G/logs/_probe_copies/anch_$STAGE.test.ts; mv $OP $G/logs/_probe_copies/orig_$STAGE.test.ts
git -C $R checkout pr/1932 -- $PA $PO
echo "status after: [$(git -C $R status --short | tr '\n' ' ')]"
for f in $PA $PO; do [ "$(git -C $R hash-object $R/$f)" = "$(git -C $R rev-parse pr/1932:$f)" ] && echo "SHA_OK $f" || echo "SHA_BAD $f"; done
wc -l $G/logs/probe_*_$STAGE*.jsonl
