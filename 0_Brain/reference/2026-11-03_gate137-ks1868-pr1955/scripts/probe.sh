#!/bin/bash
# usage: probe.sh <base|head>; product swapped to base for 'base', restored after.
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate137-ks1868-pr1955
R=$G/repo; STAGE=$1; BASE=9a9bf86967e31166ed4aba863e4c1fc4b763bfe8
PA=Blockchain/Dev/services/anchoring/src/index.ts; PO=Blockchain/Dev/services/originate/src/routes/anchors.ts
AP=$R/Blockchain/Dev/services/anchoring/src/__tests__/g137_anch_probe.test.ts
OP=$R/Blockchain/Dev/services/originate/src/__tests__/g137_orig_probe.test.ts
SC=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/c5199eda-e2e8-42ab-989c-f3882d521117/scratchpad/g137cwd; mkdir -p $SC
if [ "$STAGE" = base ]; then git -C $R show $BASE:$PA > $R/$PA; git -C $R show $BASE:$PO > $R/$PO; fi
cp $G/scripts/g137_anch_probe.test.ts $AP; cp $G/scripts/g137_orig_probe.test.ts $OP
: > $G/logs/probe_anch_$STAGE.jsonl
G137_OUT=$G/logs/probe_anch_$STAGE.jsonl G137_STAGE=$STAGE bash $G/scripts/run.sh anchoring $G/logs/probe_anch_${STAGE}_run src/__tests__/g137_anch_probe.test.ts
for E in development production; do
  : > $G/logs/probe_orig_${STAGE}_$E.jsonl
  G137_OUT=$G/logs/probe_orig_${STAGE}_$E.jsonl G137_STAGE=$STAGE G137_LOGENV=$E G137_CWD=$SC bash $G/scripts/run.sh originate $G/logs/probe_orig_${STAGE}_${E}_run --runTestsByPath $OP
done
mkdir -p $G/logs/_probe_copies; mv $AP $G/logs/_probe_copies/anch_$STAGE.test.ts; mv $OP $G/logs/_probe_copies/orig_$STAGE.test.ts
git -C $R checkout gate137 -- $PA $PO
echo "status after: [$(git -C $R status --short | tr '\n' ' ')]"
for f in $PA $PO; do [ "$(git -C $R hash-object $R/$f)" = "$(git -C $R rev-parse pr/1955:$f)" ] && echo "SHA_OK $f" || echo "SHA_BAD $f"; done
wc -l $G/logs/probe_*_$STAGE*.jsonl
