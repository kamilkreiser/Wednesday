#!/bin/bash
# launch_qa_secuura_push_protocol_d2a53096.sh — cross-project QA agent, TIER 2 (through code) gate ROUND 1
# on Secuura's push-protocol verifier 5_Project_History/push-protocol/push_protocol.py @ sha256 d2a53096.
#
# Adapted from launch_qa_secuura_ks1086_953_round2.sh. The subject is a FILE outside the repo, not a PR
# head, so the "head moved" guard becomes a sha256 guard on the file, and the round-N pointer guard
# becomes a pointer to the author's handover (the QA agent has no inbox, so a carry-forward with no
# path is unanswerable). The merge-base guard does not apply and is removed.
#
# Test hook (for the red-proof only): QA_LAUNCH_ROOT overrides WHERE the brief and prompt are read
# from. It never changes the subject, the QA project or the launch command.
#
# Written with the Write tool because it contains a legitimate `cd`.
#
# Usage: launch_qa_secuura_push_protocol_d2a53096.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..18 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
ROOT="${QA_LAUNCH_ROOT:-$WED/2_Project_Files/fleet/qa-agent/briefs}"
BRIEF_CANON="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-11_secuura-push-protocol-d2a53096-tier2.md"
BRIEF="$ROOT/2026-09-11_secuura-push-protocol-d2a53096-tier2.md"
PROMPT_FILE="$ROOT/2026-09-11_secuura-push-protocol-d2a53096-tier2.prompt.txt"
HANDOVER='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-s179-tier2-predicate.md'
SUBJECT='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/push-protocol/push_protocol.py'
SUBJECT_SHA="${QA_LAUNCH_SUBJECT_SHA:-d2a5309661d5f9617a12df445b9f91fee4886481d4f21a152924cc730a68a4f9}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'

[ -d "$QA_DIR" ]       || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]        || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ]  || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]         || { echo "repo missing: $REPO" >&2; exit 5; }
[ -s "$HANDOVER" ]     || { echo "author's handover missing: $HANDOVER" >&2; exit 14; }
[ -s "$SUBJECT" ]      || { echo "subject missing: $SUBJECT" >&2; exit 18; }

ACTUAL_SHA="$(shasum -a 256 "$SUBJECT" | awk '{print $1}')"
[ "$ACTUAL_SHA" = "$SUBJECT_SHA" ] || { echo "REFUSING: subject sha256 is '$ACTUAL_SHA', brief gates '$SUBJECT_SHA' — the file changed" >&2; exit 6; }

grep -q 'TIER 2' "$BRIEF" && grep -q 'TIER 2' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the tier" >&2; exit 7; }
grep -q 'ROUND 1' "$BRIEF" && grep -q 'ROUND 1' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the round" >&2; exit 15; }
head -1 "$PROMPT_FILE" | grep -q 'ultrathink' || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 8; }
grep -qF "$BRIEF_CANON" "$PROMPT_FILE" || { echo "REFUSING: prompt does not name the brief path" >&2; exit 9; }
grep -qF "$HANDOVER" "$PROMPT_FILE" || { echo "REFUSING: prompt does not name the author's handover — the agent has no inbox to ask" >&2; exit 17; }
grep -qi 'MAIL YOUR VERDICT' "$PROMPT_FILE" || { echo "REFUSING: prompt does not tell the agent to MAIL its verdict" >&2; exit 12; }
grep -qi 'NEVER run a push, the real pre-push hook, or preflight.sh inside the Secuura checkout' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid pushing / running the hook in the real checkout" >&2; exit 11; }
grep -qi 'Never write into 5_Project_History' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid writing into the subject's folder" >&2; exit 13; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  subject sha256 $SUBJECT_SHA"
  echo "  brief, prompt, handover, subject, QA project and repo all present"
  echo "  brief and prompt agree on TIER 2 and ROUND 1"
  echo "  prompt opens with the thinking directive, names the brief AND the author's handover"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing / the real hook / preflight in the checkout, and writing into 5_Project_History"
  exit 0
fi

[ -z "${QA_LAUNCH_ROOT:-}" ] && [ -z "${QA_LAUNCH_SUBJECT_SHA:-}" ] || { echo "REFUSING to launch with a test override set" >&2; exit 16; }
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
