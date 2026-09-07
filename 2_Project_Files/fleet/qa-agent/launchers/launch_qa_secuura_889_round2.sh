#!/bin/bash
# Launch wrapper for the cross-project QA agent — Secuura #889 ROUND 2 @ 48ad0354e, TIER 1.
# Round 1 was GO-with-findings with F1 MERGE-BLOCKING; #893 -> develop is held behind this PR.
#
# WHY THIS LIVES HERE AND NOT IN fleet/state/ (2026-09-07 lesson,
# learnings/2026-09-07_a-mechanism-is-recorded-by-its-path-not-its-runtime-id.md):
# fleet/state/ is GITIGNORED. Every QA launch wrapper this fleet has ever used (128 of them)
# is invisible to a git-based search, absent from the repo, and does not travel with a clone —
# which is why a successor spent ~25 minutes reconstructing how a gate is launched and was one
# plausible-looking command away from BYPASSING these guards. State drawers hold state; a tool
# a future seat must find is TOOLING and belongs in a tracked path. New wrappers land here from
# 2026-09-07; moving the 128 historical ones is queued as its own action.
#
# Guards: QA dir, brief, prompt file, thinking directive, brief path, head SHA, and the
# CORRECTED precedent path — because Wednesday's original citation (documents.ts:559) was wrong
# and reached a card Kam ruled on, so a prompt that omits the correction invites the tester to
# re-inherit it from round 1's own verdict.
# Written via the Write tool because it contains a legitimate `cd`.
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
BRIEF='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-07_secuura-ks597-889-bind-round2-tier1.md'
PROMPT_FILE="${QA_PROMPT_FILE_OVERRIDE:-/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/qa_secuura_889_round2_prompt.txt}"

[ -d "$QA_DIR" ]      || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]       || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ] || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 5; }

PROMPT="$(cat "$PROMPT_FILE")"

case "$PROMPT" in
  ultrathink*) ;;
  *) echo "prompt does not begin with the thinking directive — refusing to launch" >&2; exit 6 ;;
esac
case "$PROMPT" in
  *2026-09-07_secuura-ks597-889-bind-round2-tier1.md*) ;;
  *) echo "prompt does not name the brief path — refusing to launch a blind agent" >&2; exit 7 ;;
esac
case "$PROMPT" in
  *48ad0354e*) ;;
  *) echo "prompt does not name the head 48ad0354e — refusing to gate the wrong SHA" >&2; exit 8 ;;
esac
case "$PROMPT" in
  *provenance.ts*) ;;
  *) echo "prompt does not name the CORRECTED precedent (provenance.ts) — refusing: the tester would re-inherit Wednesday's wrong citation" >&2; exit 9 ;;
esac

if [ "${1:-}" = "--check" ]; then
  echo "launch_qa_secuura_889_round2: guards pass (QA dir, brief, prompt file, directive, brief path, head SHA, corrected precedent)"
  exit 0
fi

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 4; }

exec claude --dangerously-skip-permissions --model claude-opus-5 "$PROMPT"
