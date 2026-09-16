#!/bin/bash
# Run a run's RETRY-ONCE leg once the machine load falls back under the gate.
#
# WHY THIS EXISTS (measured 2026-09-16 15:3x, not assumed):
# KS-1168 failed A3c — a dropped addition, the exact class RETRY-ONCE exists to salvage without
# spending a new brief. The retry then refused: `local_model_task: REFUSING — 1-min load 18.53 >
# LM_MAX_LOAD 14`. The refusal was correct and the mechanism is sound — across every run on disk the
# retry has produced a verdict 15 times and been refused on load exactly ONCE, today.
#
# The load was mine. Two Claude brief-writers, a full-drive unison leg and a vitest suite ran at the
# same time. And the dominant consumer was not unison (99% of one core) but SPOTLIGHT reindexing what
# the sync writes — mds_stores 132%, spotlightknowledged 53%, mds 47%, mdworker_shared 19%, measured
# with `ps -Ao pcpu,pid,comm -r` at 15:37.
#
# So: do NOT weaken the load gate on one instance (2026-09-08_a-new-rule-is-most-dangerous-just-after-
# adoption; go-slow rule 4). Wait for the condition to pass, with a bound, and say so if it does not.
# A wait with no end is a stall wearing a mechanism's clothes — this one exits either way, and its
# exit is the wake (2026-09-07_an-instruction-to-wait-must-name-what-wakes).
#
# Usage: nohup bash retry_when_load_allows.sh <run-dir> <task.md> <clone-dir> [max-wait-min] &
set -u
RUN="${1:?usage: retry_when_load_allows.sh <run-dir> <task.md> <clone-dir> [max-wait-min]}"
TASK="${2:?need the task.md}"
CLONE="${3:?need the clone dir}"
MAXMIN="${4:-90}"
W=/Volumes/DevMASTER/WEDNESDAY
LM="$W/2_Project_Files/local-model"
LOG="$RUN/retry_when_load_allows.log"
GATE="${LM_MAX_LOAD:-14}"
say() { printf '%s %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*" >> "$LOG"; }
panel() { bash "$W/2_Project_Files/tools/chat_reply.sh" "$1" >> "$LOG" 2>&1; }

[ -f "$RUN/retry/input.json" ] || { say "no retry/input.json in $RUN — nothing to retry"; exit 2; }
DEADLINE=$(( $(date +%s) + 60 * MAXMIN ))
say "waiting for the 1-min load to fall to $GATE or below (deadline ${MAXMIN} min)"

while :; do
  L1=$(uptime | sed 's/.*load averages*: *//' | awk '{print $1}' | tr -d ,)
  UNDER=$(python3 -c "import sys; print(1 if float('$L1') <= float('$GATE') else 0)" 2>/dev/null || echo 0)
  [ "$UNDER" = "1" ] && { say "load $L1 <= $GATE — going"; break; }
  if [ "$(date +%s)" -ge "$DEADLINE" ]; then
    say "GAVE UP — load still $L1 after ${MAXMIN} min. Nothing retried; the first verdict stands."
    panel "I could not retry KS-1168 on the local model: the machine's one-minute load has stayed above the safety gate for ${MAXMIN} minutes, sitting at $L1 against a limit of $GATE. The biggest consumer is Spotlight reindexing everything the drive sync writes, not the sync itself. I have not overridden the gate — that limit came from a measurement, not a guess. The ticket keeps its first verdict and I will re-run it when the machine is quiet."
    exit 3
  fi
  sleep 60
done

# The lock GATES the launch — never print and continue (the pickup's trap).
#
# FIXED 2026-09-16 15:4x, on this script's FIRST live fire: the original check ABANDONED (exit 4)
# when a runner held the lock. That is a refusal nobody reads — the retry would simply never happen
# and the log saying so is not a channel. Worse, the check was check-then-act: at 15:40:51 it saw no
# lock and went; at 15:40:55, four seconds later, the night runner took KS-998. Two model calls
# overlapped. It cost nothing (ollama serialises same-model requests — one 23.2 GB instance, 71%
# memory free, measured) but the window is real. So: WAIT for the runner instead of abandoning, and
# re-check inside the same bounded loop rather than once.
while [ -f "$LM/night/log/.night_run.lock/pid" ] && kill -0 "$(cat "$LM/night/log/.night_run.lock/pid" 2>/dev/null)" 2>/dev/null; do
  if [ "$(date +%s)" -ge "$DEADLINE" ]; then
    say "GAVE UP — a night runner has held the lock until the deadline. Nothing retried; the first verdict stands."
    panel "I could not retry KS-1168: the local-model runner was busy with other tickets for the whole window I allowed. Nothing is lost — the ticket keeps its first verdict and goes back in the queue."
    exit 4
  fi
  say "a night runner is live — waiting rather than standing down"
  sleep 60
done

say "running the retry"
LM_MODEL="${NIGHT_MODEL:-ornith:35b}" LM_THINK=0 LM_NUM_CTX=65536 LM_MAX_LOAD="$GATE" \
  bash "$LM/local_model_task.sh" "$TASK" "$RUN/retry/input.json" "$RUN/retry/out.md" >> "$LOG" 2>&1
rrc=$?
say "retry harness rc=$rrc"
if [ "$rrc" -ne 0 ]; then
  panel "The KS-1168 retry ran once the machine went quiet and the model harness still refused it, rc $rrc. I have not worked around it — the log is in the run directory."
  exit 5
fi

bash "$(dirname "$TASK")/checker.sh" "$RUN/retry/input.json" "$RUN/retry/out.md" "$CLONE" > "$RUN/retry/checker.out" 2>&1
RV="$(/usr/bin/grep -m1 '^RESULT:' "$RUN/retry/checker.out")"
say "retry verdict: ${RV:-CHECKER_NO_RESULT}"
case "$RV" in
  *PASS*) panel "KS-1168 passed on the retry once the machine went quiet — ${RV}. I will source-read the applied diff and write the READY before it counts as held." ;;
  *)      panel "KS-1168's retry finished and did not pass — ${RV:-the checker produced no RESULT line}. That is a real verdict, not a machine problem this time; I will read the run and put the fix where it belongs." ;;
esac
