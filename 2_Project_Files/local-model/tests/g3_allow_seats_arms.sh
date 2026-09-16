#!/bin/bash
# g3_allow_seats_arms.sh — red-proof for night_run.sh's G3 honouring the SEATS ALLOWANCE (2026-09-16 22:1x).
# Kam 20:40: Claude agents run alongside the local model. G2 honoured night/ALLOW_SEATS; G3 (any live
# `launch_qa_` process) did not, so a live QA gate idled a queued batch. Arms run on an EMPTY scratch
# queue (nothing runs), a scratch NIGHT_LOG_DIR, a tmux socket with NO fleet session (G2 = empty floor),
# and a scratch "QA process" whose argv carries a unique pattern (NIGHT_QA_PGREP override):
#   ARM 1  qa proc live, no allowance      -> G3 REFUSE      (old behaviour kept)
#   ARM 2  qa proc live, future allowance  -> G3 ALLOWED pass
#   ARM 3  qa proc live, expired allowance -> G3 REFUSE      (the override expires on its own)
#   ARM 4  CONTROL: no qa proc, no allowance -> G3 "= 0 ... pass"
# Usage: bash g3_allow_seats_arms.sh [night_run.sh path]   (run it against the OLD runner too: ARM 2 must FAIL)
set -u
HERE="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RUNNER="${1:-$HERE/../night/night_run.sh}"
W="$(mktemp -d "${TMPDIR:-/tmp}/g3allow.XXXXXX")"
PAT="g3armsQA$$"
PASS=0; FAIL=0
: > "$W/queue.md"

run_gates() { # $1 label -> prints the G3 line
  mkdir -p "$W/log_$1"
  NIGHT_TMUX_SOCKET="g3nosock$$" NIGHT_QUEUE="$W/queue.md" NIGHT_LOG_DIR="$W/log_$1" \
  NIGHT_ALLOW_SEATS_FILE="$W/ALLOW_SEATS_$1" NIGHT_QA_PGREP="$PAT" NIGHT_DRY_RUN=1 \
    bash "$RUNNER" > "$W/out_$1.txt" 2>&1
  /usr/bin/grep 'GATE G3' "$W/out_$1.txt" | tail -1
}
check() { case "$2" in *"$3"*) echo "PASS: $1"; PASS=$((PASS+1));; *) echo "FAIL: $1 — got: $2"; FAIL=$((FAIL+1));; esac; }

sh -c "sleep 120; : $PAT" & QAPID=$!
sleep 1

L=$(run_gates a1); check "ARM1 qa live, no allowance -> REFUSE" "$L" "REFUSE"
printf '%s\n%s\n' "$(( $(date +%s) + 3600 ))" "arms: future" > "$W/ALLOW_SEATS_a2"
L=$(run_gates a2); check "ARM2 qa live, future allowance -> ALLOWED pass" "$L" "ALLOWED by"
printf '%s\n%s\n' "$(( $(date +%s) - 60 ))" "arms: expired" > "$W/ALLOW_SEATS_a3"
L=$(run_gates a3); check "ARM3 qa live, expired allowance -> REFUSE" "$L" "REFUSE"

[ -n "${QAPID:-}" ] && [ "$QAPID" != 1 ] && kill "$QAPID" 2>&1
wait "$QAPID" 2>/dev/null
L=$(run_gates a4); check "ARM4 CONTROL no qa proc -> = 0 pass" "$L" "= 0"

echo "arms: $PASS pass, $FAIL fail (work dir $W)"
[ "$FAIL" -eq 0 ]
