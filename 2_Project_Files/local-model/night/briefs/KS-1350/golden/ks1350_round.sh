#!/bin/bash
# round.sh — KS-1350 comment_patch Spark round (feed4run chain, comment_patch tier). Scratch clones only; no git write verb outside the scratchpad.
set -uo pipefail
L=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model
SP=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/d0b2ec3e-4b50-4d96-87d2-4a998799b9cd/scratchpad
SRC=$SP/sparkfeed; TIP=94c9c7aa9be7f0c05f4a89cdc532ec6f2fef3812
R=$L/runs/spark_secuura_2026-09-27_KS-1350; W=$SP/ks1350run; C=$W/clone; T=$L/tasks/comment_patch
G=$L/night/briefs/KS-1350/golden/KS-1350.golden.diff
a2a(){ # $1 = out.md ; A2a as KS-789 ran it: sections.json -> the checker's patch.diff
  local REP="$1.checker"
  if [ -f "$REP/patch.diff" ]; then
    printf '[{"n": 1, "path": "%s", "file": "%s"}]' "Blockchain/Dev/services/originate/src/routes/webhooks.ts" "$REP/patch.diff" > "$REP/a2a_sections.json"
    python3 $L/tasks/code_patch/a2a_anchor.py $R/input.json $C "$REP/a2a_sections.json" > "$REP/a2a_anchor.out" 2>&1; echo "A2a rc=$?: $(tr '\n' ' ' < "$REP/a2a_anchor.out")"
  else echo "A2a skipped: no patch.diff"; fi; }
echo "== health: http $(curl -sS -m 10 -o /dev/null -w '%{http_code}' http://127.0.0.1:47788/health)"
H=$(git -C $SRC rev-parse HEAD); P=$(git -C $SRC status --porcelain | wc -l | tr -d ' ')
echo "== source $SRC HEAD=$H porcelain=$P"; [ "$H" = "$TIP" ] && [ "$P" = 0 ] || { echo "SOURCE NOT CLEAN AT TIP — stop"; exit 1; }
[ -d $C ] && { echo "clone exists — stop"; exit 1; }
git clone -q --shared --no-checkout $SRC $C && git -C $C checkout -q --detach $TIP || exit 1
bash $T/prepare_clone.sh $R/input.json $C > $R/prepare_clone.out 2>&1; echo "rc=$?" >> $R/prepare_clone.out; cat $R/prepare_clone.out
# golden probe BEFORE the model round
mkdir -p $R/golden_probe; { echo '```diff'; cat $G; echo '```'; } > $R/golden_probe/out.md
bash $T/checker.sh $R/input.json $R/golden_probe/out.md $C > $R/golden_probe/checker.out 2>&1; echo "golden probe checker rc=$?"; a2a $R/golden_probe/out.md >> $R/golden_probe/checker.out
grep -E '^(PASS|FAIL|INFO|RESULT|A2a)' $R/golden_probe/checker.out
echo "== clone porcelain after probe: $(git -C $C status --porcelain | wc -l | tr -d ' ')"
T0=$(date +%s)
LM_BACKEND=spark SPARK_THINK=0 bash $L/local_model_task.sh $T/task.md $R/input.json $R/out.md > $R/run.log 2>&1; echo "model rc=$? (outer wall $(( $(date +%s)-T0 ))s)"; cat $R/run.log
bash $T/checker.sh $R/input.json $R/out.md $C > $R/checker.out 2>&1; CRC=$?; echo "checker rc=$CRC"; a2a $R/out.md >> $R/checker.out
grep -E '^(PASS|FAIL|INFO|RESULT|A2a)' $R/checker.out
echo "== source porcelain at end: $(git -C $SRC status --porcelain | wc -l | tr -d ' ')"
