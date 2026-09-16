#!/bin/bash
# Wait for a brief to appear, then build its input, queue it and run the model — unattended.
#
# Why: "a seat may END ITS TURN only with the model RUNNING or a batch QUEUED" (Kam 2026-09-15 18:19,
# sharpened 2026-09-16 09:53). When the brief is being written by a subagent, the gap between "brief
# lands" and "model starts" is a human step, and a human step is exactly what an unattended week
# cannot have. This closes it: the wait has a WAKE, and the wake is the file appearing
# (2026-09-07_an-instruction-to-wait-must-name-what-wakes).
#
# It is also the shape the unattended-week loop needs, exercised on a real ticket rather than designed
# on paper.
#
# Usage: autostart_on_brief.sh [--tier bash|vitest] <KS-id> <product path> <ref> [pins…]
#        (run detached: nohup bash autostart_on_brief.sh ... &)
#
# TIER, added 2026-09-16 14:4x before this ever fired on a TypeScript ticket: the two tiers have
# DIFFERENT builders and DIFFERENT task files, and this script hardcoded the bash one. Armed for
# KS-953 (`api-gateway/src/index.ts`) it would have built a bash_patch input for a vitest ticket and
# the failure would have arrived as a confusing checker verdict rather than as "wrong tier".
# Default is bash because that is the tier it was written against; --tier vitest selects
# `night/build_input.sh` + `tasks/code_patch/task.md`. Caught by reading the tool before arming it,
# which is the only reason it is a comment here and not an incident.
# Gives up after NIGHT_AUTOSTART_WAIT_MIN minutes (default 30) and says so — a wait with no end is a
# stall wearing a mechanism's clothes.
set -u
LM="$(cd -P "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TIER=bash
if [ "${1:-}" = "--tier" ]; then TIER="${2:?--tier needs bash or vitest}"; shift 2; fi
case "$TIER" in
  bash)   BUILDER="$LM/tasks/bash_patch/build_bash_input.sh"; TASKMD="$LM/tasks/bash_patch/task.md" ;;
  vitest) BUILDER="$LM/night/build_input.sh";                 TASKMD="$LM/tasks/code_patch/task.md" ;;
  *) echo "REFUSED — --tier must be bash or vitest, got '$TIER'" >&2; exit 2 ;;
esac
[ -f "$BUILDER" ] || { echo "REFUSED — no builder for tier '$TIER' at $BUILDER" >&2; exit 2; }
[ -f "$TASKMD" ]  || { echo "REFUSED — no task file for tier '$TIER' at $TASKMD" >&2; exit 2; }
ID="${1:?usage: autostart_on_brief.sh [--tier bash|vitest] <KS-id> <product> <ref> [pins...]}"
PRODUCT="${2:?product path required}"
REF="${3:?reference *.test.sh required}"
shift 3
BRIEF="$LM/night/briefs/$ID.md"
# The input's NAME carries its tier — `bash_1031.json`, `doc_1049.json`. Hardcoding `bash_` here
# would have written a vitest input under a bash name, which reads as the wrong thing to every
# later reader and to the re-check path (2026-09-07: a mechanism is recorded by what it IS).
case "$TIER" in bash) PFX=bash ;; vitest) PFX=code ;; *) PFX="$TIER" ;; esac
INPUT="$LM/night/inputs/${PFX}_${ID#KS-}.json"
LOG="$LM/night/log/autostart_${ID}_$(date +%H%M).log"
DEADLINE=$(( $(date +%s) + 60 * ${NIGHT_AUTOSTART_WAIT_MIN:-30} ))

say() { echo "$(date '+%F %T') $*" | tee -a "$LOG"; }
say "tier=$TIER builder=$(basename "$BUILDER"); waiting for $BRIEF (deadline $(date -r $DEADLINE '+%H:%M'))"

while [ ! -s "$BRIEF" ]; do
  if [ "$(date +%s)" -ge "$DEADLINE" ]; then
    say "GAVE UP — no brief at $BRIEF after ${NIGHT_AUTOSTART_WAIT_MIN:-30} min. Nothing queued, model still idle."
    bash "$LM/../tools/chat_reply.sh" "The $ID brief never arrived, so the local model is still idle — the autostart gave up after ${NIGHT_AUTOSTART_WAIT_MIN:-30} minutes rather than waiting silently." > /dev/null 2>&1
    exit 4
  fi
  sleep 20
done
# A file can exist before it is finished being written. Require it to stop growing for two reads.
A=$(wc -c < "$BRIEF"); sleep 10; B=$(wc -c < "$BRIEF")
while [ "$A" != "$B" ]; do A=$B; sleep 10; B=$(wc -c < "$BRIEF"); done
say "brief present and settled ($B bytes)"

if ! bash "$BUILDER" "$ID" "$INPUT" "$BRIEF" \
     product="$PRODUCT" ref="$REF" "$@" >> "$LOG" 2>&1; then
  say "BUILD REFUSED — see $LOG. Nothing queued; the brief needs a fix (this is the usual first failure)."
  bash "$LM/../tools/chat_reply.sh" "The $ID brief was written but the input builder refused it, so nothing is queued — I will read the refusal and fix the brief." > /dev/null 2>&1
  exit 2
fi
say "input built: $INPUT"

printf '%s\n' "# $(date +%H:%M) — $ID queued by autostart_on_brief.sh the moment its brief landed." >> "$LM/night/queue.md"
# 2026-09-16 14:38, FIRST REAL USE, FIRST EXCEPTION: this line was a `for`+`case` INSIDE a
# command substitution. Bash parses the `)` that closes a case pattern as the end of the
# substitution, so it died with "syntax error near unexpected token" AFTER building the input
# and BEFORE writing the queue line — the model sat idle and the give-up path could not fire,
# because the wait had already succeeded. `bash -n` passed on it, exactly as it did for the
# 2026-09-02 launcher-quote defect: a parse that is only wrong INSIDE a substitution.
# Build the pin in a plain loop first; never put `case` inside `$( )`.
CTX_PIN=""
for a in "$@"; do
  case "$a" in ctx=*) CTX_PIN="$a" ;; esac
done
printf '%s\n' "$ID input=$INPUT task=$TASKMD $CTX_PIN" >> "$LM/night/queue.md"
say "queued"

# The lock GATES the launch — never print-and-continue (the pickup's trap).
if [ -f "$LM/night/log/.night_run.lock/pid" ]; then
  P="$(cat "$LM/night/log/.night_run.lock/pid" 2>/dev/null)"
  if [ -n "$P" ] && [ "$P" != 1 ] && kill -0 "$P" 2>/dev/null; then
    say "a runner is already live (pid $P) — it will take the queued line; not launching a second."
    exit 0
  fi
fi
say "launching night_run"
bash "$LM/night/night_run.sh" >> "$LOG" 2>&1
say "night_run exited rc=$?"
