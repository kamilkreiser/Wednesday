#!/bin/bash
# Launch wrapper — Datasec/NexusAI RD-369, branch `rd-369-round2-s47` @ 117931e, TIER 1 (FULL).
#
# Tier 1 because the change alters WHAT SHIPS TO A CUSTOMER (Kam's 2026-09-05 tiering: security
# surfaces get full weight). The builder's headline — shipping carriers 6 -> NONE — rests entirely
# on a NEW instrument it wrote in the same commit (__tests__/helpers/image-manifest.js), so the
# gate's first job is the instrument, not the fix.
#
# Tracked path on purpose — learnings/2026-09-07_a-mechanism-is-recorded-by-its-path-not-its-runtime-id.md.
# Written via the Write tool because it contains a legitimate `cd` (pretooluse_no_cd.sh refuses a
# `cd` inside a Bash tool call).
# Guards match against a NEWLINE-FLATTENED prompt: the 2026-09-07 wrapped-phrase defect showed a
# phrase search over prose that wraps is either wrap-tolerant or it is a check that cannot pass.
#
# Usage: launch_qa_nexusai_rd369.sh [--check]     --check runs every guard, exits 0, launches nothing.
# Exit: 0 launched (or guards pass) · 2..9 a guard refused.
set -u

QA_DIR='/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN'
BRIEF='/Volumes/KK_T9_External_HDD/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-08_nexusai-rd369-round2.md'
PROMPT_FILE='/Volumes/KK_T9_External_HDD/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/qa_nexusai_rd369_round2_prompt.txt'
NEXUS='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files'
HEAD_SHA='c96837d'

[ -d "$QA_DIR" ]      || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]       || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ] || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 5; }
[ -d "$NEXUS" ]       || { echo "NexusAI checkout missing: $NEXUS" >&2; exit 4; }

# THE SUBJECT MUST EXIST AT ORIGIN. Gating a SHA that is not published is gating a ghost —
# ls-remote is a READ verb, safe from Wednesday's seat.
git -C "$NEXUS" ls-remote origin rd-369-round2-s47 2>/dev/null | grep -q "^${HEAD_SHA}" || {
  echo "REFUSING: origin/rd-369-round2-s47 does not resolve to ${HEAD_SHA} — the head moved or the branch is unpushed." >&2
  echo "Re-read the head and re-brief before gating; a gate on the wrong SHA is worse than no gate." >&2
  exit 8
}

PROMPT="$(cat "$PROMPT_FILE")"
PROMPT_FLAT="$(printf '%s' "$PROMPT" | tr '\n' ' ')"

case "$PROMPT" in
  ultrathink*) ;;
  *) echo "prompt does not begin with the thinking directive — refusing to launch" >&2; exit 6 ;;
esac
case "$PROMPT_FLAT" in
  *2026-09-08_nexusai-rd369-round2.md*) ;;
  *) echo "prompt does not name the brief path — refusing to launch a blind agent" >&2; exit 7 ;;
esac
case "$PROMPT_FLAT" in
  *"${HEAD_SHA}"*) ;;
  *) echo "prompt does not name the head ${HEAD_SHA} — refusing to gate the wrong SHA" >&2; exit 8 ;;
esac
case "$PROMPT_FLAT" in
  *"IN BOTH DIRECTIONS"*) ;;
  *) echo "prompt does not carry the both-directions verdict requirement — refusing" >&2; exit 9 ;;
esac
# The instrument is the target. A gate that re-runs the suite green has verified nothing here,
# because the suite's own numbers come from the helper under test.
case "$PROMPT_FLAT" in
  *"INSTRUMENT IS THE THING TO ATTACK"*) ;;
  *) echo "prompt does not carry the attack-the-instrument requirement — refusing" >&2; exit 9 ;;
esac

if [ "${1:-}" = "--check" ]; then
  echo "launch_qa_nexusai_rd369: guards pass (QA dir, brief, prompt, NexusAI checkout, head at origin, directive, brief path, SHA, both-directions, attack-the-instrument)"
  exit 0
fi

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 4; }

exec claude --dangerously-skip-permissions --model claude-opus-5 "$PROMPT"
