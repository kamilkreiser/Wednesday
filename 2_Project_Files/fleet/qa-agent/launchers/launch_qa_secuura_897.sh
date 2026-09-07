#!/bin/bash
# Launch wrapper for the cross-project QA agent — Secuura #892 ROUND 4 @ 718008cef, TIER 2.
# Kam authorised this round himself after the two-NO-GO cap was already spent once
# (card secuura-892-round3-nogo-blocker-still-open => round4, 2026-09-07 20:55).
# THERE IS NO ROUND 5: a NO GO goes back to Kam, not into a merge and not into another round.
#
# Lives in the TRACKED launchers path, not the gitignored fleet/state/ — see
# learnings/2026-09-07_a-mechanism-is-recorded-by-its-path-not-its-runtime-id.md.
#
# Guards: QA dir, brief, prompt file, thinking directive, brief path, head SHA, Kam's scope
# bound, and THE BINDING CONDITION — because the whole reason this round exists is the
# call-site cell, and a prompt that does not carry it would let the tester re-run round 3's
# pass and call a green function-level suite a closure.
# Written via the Write tool because it contains a legitimate `cd`.
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
BRIEF='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-07_secuura-ks978-897-tier2.md'
PROMPT_FILE="${QA_PROMPT_FILE_OVERRIDE:-/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/qa_secuura_897_prompt.txt}"

[ -d "$QA_DIR" ]      || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]       || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ] || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 5; }

PROMPT="$(cat "$PROMPT_FILE")"
# WRAP-TOLERANT MATCHING (2026-09-07, caught by exercising this very file): every phrase guard
# below matches against a NEWLINE-FLATTENED copy. The first build greppped "IDENTITY OF THE
# FAILING CELL" against the raw prompt, where it wraps across two lines — so the PASS path
# refused with rc 10 and the guard was unsatisfiable by construction. That is the wrapped-phrase
# defect already in the ledger (2026-09-06, w=14): a phrase search over prose that wraps is
# either wrap-tolerant or it is a check that cannot pass.
PROMPT_FLAT="$(printf '%s' "$PROMPT" | tr '\n' ' ')"

case "$PROMPT" in
  ultrathink*) ;;
  *) echo "prompt does not begin with the thinking directive — refusing to launch" >&2; exit 6 ;;
esac
case "$PROMPT_FLAT" in
  *2026-09-07_secuura-ks978-897-tier2.md*) ;;
  *) echo "prompt does not name the brief path — refusing to launch a blind agent" >&2; exit 7 ;;
esac
case "$PROMPT_FLAT" in
  *718008cef*) ;;
  *) echo "prompt does not name the head 718008cef — refusing to gate the wrong SHA" >&2; exit 8 ;;
esac
case "$PROMPT_FLAT" in
  *"IN BOTH DIRECTIONS"*) ;;
  *) echo "prompt does not carry the both-directions verdict requirement — refusing" >&2; exit 9 ;;
esac
# THE BINDING CONDITION. Round 3 got 42/42 green with the defect fully restored because every
# cell pinned the FUNCTION and none pinned the CALL. A prompt without this clause would let the
# tester repeat that pass and read a green function-level suite as a closure.
case "$PROMPT_FLAT" in
  *"IDENTITY OF THE FAILING CELL"*) ;;
  *) echo "prompt does not carry the binding condition (verify the IDENTITY of the failing cell, not just the count) — refusing: this round exists for that cell" >&2; exit 10 ;;
esac
# The builder's own qualifier — a cell that reds by failing to BUILD proves nothing.
case "$PROMPT_FLAT" in
  *"EXECUTED-cell count"*) ;;
  *) echo "prompt does not require the EXECUTED-cell count under each tamper — refusing: a red from a broken build is not a red-proof" >&2; exit 11 ;;
esac

if [ "${1:-}" = "--check" ]; then
  echo "launch_qa_secuura_897: guards pass (QA dir, brief, prompt file, directive, brief path, head SHA, Kam's scope bound, binding condition, executed-cell qualifier)"
  exit 0
fi

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 4; }

exec claude --dangerously-skip-permissions --model claude-opus-5 "$PROMPT"
