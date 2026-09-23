#!/bin/bash
# Launch wrapper — Secuura #892 ROUND 5 @ d2aa11fd1, TIER 2 (through-code).
# Kam authorised this round himself (panel 2026-09-08 07:08:30): "ONE more narrow round — F-1 and
# F-2 only, F-2 first." THERE IS NO ROUND 6: a NO GO goes back to Kam, not into a merge and not
# into another round. The two-NO-GO cap on this class was already spent once (round 3 NO GO).
#
# Tracked path on purpose — learnings/2026-09-07_a-mechanism-is-recorded-by-its-path-not-its-runtime-id.md.
# Written via the Write tool because it contains a legitimate `cd` (same reason as the 897 wrapper).
# Guards match against a NEWLINE-FLATTENED prompt: the 2026-09-07 wrapped-phrase defect showed that
# a phrase search over prose that wraps is either wrap-tolerant or it is a check that cannot pass.
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
BRIEF='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-08_secuura-892-round5-tier2.md'
PROMPT_FILE="${QA_PROMPT_FILE_OVERRIDE:-/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/qa_secuura_892_round5_prompt.txt}"

[ -d "$QA_DIR" ]      || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]       || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ] || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 5; }

PROMPT="$(cat "$PROMPT_FILE")"
PROMPT_FLAT="$(printf '%s' "$PROMPT" | tr '\n' ' ')"

case "$PROMPT" in
  ultrathink*) ;;
  *) echo "prompt does not begin with the thinking directive — refusing to launch" >&2; exit 6 ;;
esac
case "$PROMPT_FLAT" in
  *2026-09-08_secuura-892-round5-tier2.md*) ;;
  *) echo "prompt does not name the brief path — refusing to launch a blind agent" >&2; exit 7 ;;
esac
case "$PROMPT_FLAT" in
  *d2aa11fd1*) ;;
  *) echo "prompt does not name the head d2aa11fd1 — refusing to gate the wrong SHA" >&2; exit 8 ;;
esac
case "$PROMPT_FLAT" in
  *"IN BOTH DIRECTIONS"*) ;;
  *) echo "prompt does not carry the both-directions verdict requirement — refusing" >&2; exit 9 ;;
esac
# F-2's binding condition: the suite's report is provably BLIND to the defect. A gate that only
# re-runs the suite green has verified nothing — which is exactly how round 3 passed 42/42 with the
# defect fully restored.
case "$PROMPT_FLAT" in
  *"BLIND to the"*) ;;
  *) echo "prompt does not carry F-2's binding condition (show the suite's report is BLIND) — refusing" >&2; exit 10 ;;
esac
# The CORRECTED discriminator. Wednesday's round-4 brief said a cell that reds by failing to BUILD
# proves nothing, and told the builder to plant a syntax error. The builder MEASURED that bash runs
# on regardless: all cells still executed and the trailer still printed a clean pass. A prompt
# carrying the old rule would have the gate read rc and conclude nothing.
case "$PROMPT_FLAT" in
  *"TRAILER'S FAILED NUMBER"*) ;;
  *) echo "prompt does not carry the corrected bash discriminator (read the trailer's FAILED number, not rc) — refusing" >&2; exit 11 ;;
esac
# A number in a brief is not a fixture — Wednesday said 24 cells, it is 29.
case "$PROMPT_FLAT" in
  *"NOT A FIXTURE"*) ;;
  *) echo "prompt does not warn that a briefed number is not a fixture — refusing" >&2; exit 12 ;;
esac

if [ "${1:-}" = "--check" ]; then
  echo "launch_qa_secuura_892_round5: guards pass (QA dir, brief, prompt file, directive, brief path, head SHA, both-directions, F-2 blindness, bash discriminator, number-not-fixture)"
  exit 0
fi

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 4; }

exec claude --dangerously-skip-permissions --model claude-opus-5 "$PROMPT"
