#!/bin/bash
# Launch wrapper for the cross-project QA agent — Secuura #892 ROUND 3 @ 34a48abc6, TIER 2.
# The two-NO-GO cap was SPENT; Kam authorised this round himself
# (card secuura-892-cap-spent-blocker-open => round3-narrow, 2026-09-07 19:56). No round 4
# without his word: a NO GO here goes back to Kam, it does not ship under the cap.
#
# WHY THIS LIVES HERE AND NOT IN fleet/state/ — see the sibling wrapper
# launch_qa_secuura_889_round2.sh and
# learnings/2026-09-07_a-mechanism-is-recorded-by-its-path-not-its-runtime-id.md.
#
# Guards: QA dir, brief, prompt file, thinking directive, brief path, head SHA, and the SCOPE
# CLAUSE — because the round Kam authorised is F1 and F2 only, and a prompt that does not carry
# that bound invites a tester to gate work he did not authorise.
# Written via the Write tool because it contains a legitimate `cd`.
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
BRIEF='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-07_secuura-ks969-892-round3-tier2.md'
PROMPT_FILE="${QA_PROMPT_FILE_OVERRIDE:-/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/qa_secuura_892_round3_prompt.txt}"

[ -d "$QA_DIR" ]      || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]       || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ] || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 5; }

PROMPT="$(cat "$PROMPT_FILE")"

case "$PROMPT" in
  ultrathink*) ;;
  *) echo "prompt does not begin with the thinking directive — refusing to launch" >&2; exit 6 ;;
esac
case "$PROMPT" in
  *2026-09-07_secuura-ks969-892-round3-tier2.md*) ;;
  *) echo "prompt does not name the brief path — refusing to launch a blind agent" >&2; exit 7 ;;
esac
case "$PROMPT" in
  *34a48abc6*) ;;
  *) echo "prompt does not name the head 34a48abc6 — refusing to gate the wrong SHA" >&2; exit 8 ;;
esac
case "$PROMPT" in
  *"F1 and F2 ONLY"*) ;;
  *) echo "prompt does not carry the scope bound Kam authorised (F1 and F2 ONLY) — refusing" >&2; exit 9 ;;
esac

if [ "${1:-}" = "--check" ]; then
  echo "launch_qa_secuura_892_round3: guards pass (QA dir, brief, prompt file, directive, brief path, head SHA, Kam's scope bound)"
  exit 0
fi

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 4; }

exec claude --dangerously-skip-permissions --model claude-opus-5 "$PROMPT"
