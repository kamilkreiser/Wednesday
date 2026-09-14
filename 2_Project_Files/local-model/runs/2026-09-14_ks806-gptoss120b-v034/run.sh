#!/bin/bash
# run.sh — gpt-oss:120b on the code_patch task for KS-806 (Kam 2026-09-14 14:54 "Deploy now. Test when it's a quiet time.")
# Same input.json as the Qwen runs (tip f09b62945, pinned) so the scoreboard rows compare like with like.
# Steps: (1) harness → out.md  (2) scratch clone at the pinned tip (SCRATCHPAD only)  (3) prepare_clone  (4) checker.
# Exit code = the checker's (0 = PASS 7/7). Every step's rc is on its own line in run.log.
set -u
L=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model
R="$L/runs/2026-09-14_ks806-gptoss120b-v034"
SCRATCH="${1:?usage: run.sh <session-scratchpad-dir>}"
SRC="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files"
TIP="$(python3 -c "import json;print(json.load(open('$R/input.json'))['repo']['tip'])")"
exec > >(tee -a "$R/run.log") 2>&1
echo "== start $(date '+%F %T %Z') load=$(sysctl -n vm.loadavg) tip=$TIP model=gpt-oss:120b num_ctx=32768"
export OLLAMA_MODELS="$L/models"
LM_MODEL=gpt-oss:120b LM_NUM_CTX=32768 LM_MAX_LOAD=16 bash "$L/local_model_task.sh" "$L/tasks/code_patch/task.md" "$R/input.json" "$R/out.md"
rc=$?; echo "harness rc=$rc $(date '+%T')"
[ $rc -eq 0 ] || { echo "== harness failed; no checker run"; exit 10; }
CLONE="$SCRATCH/clone_gptoss120b-v034_ks806"
if [ ! -d "$CLONE/.git" ]; then
  git clone --shared --no-checkout "$SRC" "$CLONE"; echo "clone rc=$?"
  git -C "$CLONE" checkout --detach "$TIP"; echo "checkout rc=$?"
fi
bash "$L/tasks/code_patch/prepare_clone.sh" "$R/input.json" "$CLONE"; echo "prepare_clone rc=$?"
bash "$L/tasks/code_patch/checker.sh" "$R/input.json" "$R/out.md" "$CLONE" > "$R/checker.out" 2>&1
crc=$?; echo "checker rc=$crc $(date '+%T')"; tail -25 "$R/checker.out"
echo "== end $(date '+%F %T %Z') load=$(sysctl -n vm.loadavg)"
exit $crc
