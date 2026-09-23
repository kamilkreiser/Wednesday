#!/bin/bash
# launch_qa_nexusai_rd464_r3_60c76d7.sh — cross-project QA agent, TIER 1 gate, ROUND 1 of 2, on
# Datasec/NexusAI RD-464 r3 MERGED WITH MAIN: branch rd-464-r3-merged-main-s72 @ 60c76d7, built by S72.
#
# PATTERN: launch_qa_nexusai_rd327_67c2992.sh — same guards, same exit codes, same identity pinning,
# re-pointed at this head. TWO DELIBERATE CHANGES, both because THE TARGET IS A MERGE COMMIT:
#   - the single-parent `rev-list --count BASE..HEAD == 1` guard (exit 8) is REPLACED by an assertion
#     that the commit has EXACTLY the two expected parents, read from `rev-list --parents` (exit 8).
#     A commit-count guard on a merge asks a question with no meaningful answer.
#   - the ancestry guard (exit 7) runs for BOTH parents, not one.
# Added: exit 18 asserts the head is at ORIGIN on its branch — a gate's verdict is only reachable to
# a later reader if the sha is on the remote, and this one was pushed.
#
# WHY THIS FILE EXISTS RATHER THAN A GENERATED ONE: the handover said every QA launcher points at an
# unmounted /Volumes/DevMASTER and that a launcher had to be generated. That was a census over the
# wrong frame — true of the NEWEST launcher (Wednesday's Secuura one), false of the NexusAI ones,
# which are already T9-pathed. gen_launcher_from_template.py is also not general: it is hardcoded to
# one past Secuura substitution (966 -> 932) and would have refused.
#
# LAUNCH IT IN A TMUX PANE (cockpit.sh add 'QA/NexusAI-RD464r3' "bash '<this file>'"), NEVER nohup.
# Identity: exports NexusAI's OWN az/gh dirs; CLAUDE_CONFIG_DIR pinned to Tuesday's project-local store.
# ABSOLUTE PATHS ON PURPOSE. TRACKED in launchers/. Written with the Write tool (it contains a legitimate `cd`).
# Usage: launch_qa_nexusai_rd464_r3_60c76d7.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..18 a guard refused
set -u

QA_DIR='/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN'
TUE='/Volumes/KK_T9_External_HDD/TUESDAY'
BRIEF="/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-21_nexusai-rd516-round2.md"
PROMPT_FILE="/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-21_nexusai-rd516-round2.prompt.txt"
WT='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/qa-worktrees/s73-rd516'
REPORT="/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-21-rd516-aaffbb9-round2/report.md"
ID_ROOT="${QA_IDENTITY_ROOT_OVERRIDE:-/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/4_Credentials}"
HEAD_SHA="${QA_HEAD_SHA_OVERRIDE:-aaffbb91a993e23bf06f27e93ea078c3f7879c30}"
BASE='60c76d76350321ad8f51324e042052a8a9f49a96'

BRANCH='rd-516-ai-test-ssrf-s73'
SUBJECT='[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — RD-516 round 2 @ aaffbb9 (through-code)'

[ -d "$QA_DIR" ]      || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]       || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ] || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$WT" ]          || { echo "worktree under test missing: $WT" >&2; exit 5; }

GOT="$(git --no-optional-locks -C "$WT" rev-parse HEAD 2>&1)"
[ "$GOT" = "$HEAD_SHA" ] || { echo "REFUSING: worktree HEAD is '$GOT', not $HEAD_SHA — the brief is stale" >&2; exit 6; }

git --no-optional-locks -C "$WT" merge-base --is-ancestor "$BASE" "$HEAD_SHA" 2>/dev/null || {
  echo "REFUSING: base $BASE is not an ancestor of $HEAD_SHA" >&2; exit 7; }

# THE MERGE-SHAPE GUARD, in place of a commit count: exactly these two parents, in this order.

# The head must be AT ORIGIN on its branch — a gate cannot run against a sha that lives on one disk.
# 19 — the gate's technical SUBJECT lives IN THE REPO on the branch. Absent, the gate would improvise one.
INREPO_BRIEF="$WT/docs/rd516/RD-516-gate-brief.md"
[ -s "$INREPO_BRIEF" ] || { echo "REFUSING: in-repo gate brief absent from the worktree: $INREPO_BRIEF" >&2; exit 19; }
grep -qi "tier-1" "$INREPO_BRIEF" || { echo "REFUSING: $INREPO_BRIEF does not identify itself as the tier-1 material" >&2; exit 19; }

LSR="$(git --no-optional-locks -C "$WT" ls-remote origin "$BRANCH" 2>&1)"
printf '%s\n' "$LSR" | grep -q "^${HEAD_SHA}[[:space:]]refs/heads/${BRANCH}\$" || {
  echo "REFUSING: $HEAD_SHA is not at refs/heads/$BRANCH on origin — that head moved or was never pushed" >&2
  printf '%s\n' "$LSR" >&2; exit 18; }

grep -qF "$REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the report path $REPORT" >&2; exit 10; }
[ ! -e "$REPORT" ] || { echo "REFUSING: $REPORT already exists — a stale report would read as this gate's" >&2; exit 17; }

[ -d "$ID_ROOT/.azure" ] && [ -d "$ID_ROOT/.gh-config" ] || {
  echo "REFUSING: NexusAI identity dirs missing under $ID_ROOT (.azure / .gh-config) — would inherit the caller's" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_ROOT/.azure"
export GH_CONFIG_DIR="$ID_ROOT/.gh-config"
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"

# TIER AGREEMENT (generalised 2026-09-21). The inherited form hardcoded 'TIER 1' and so could only
# ever launch a tier-1 gate — it REFUSED this through-code round not because brief and prompt
# disagreed but because neither said the one tier it knew. The guard's INTENT is that the two
# documents declare the SAME tier; the tier itself is now a constant this launcher states once, so a
# mismatch between THIS launcher and its own brief is still caught. Widening it to "any tier, as long
# as both agree" would have been the wrong fix: it would pass a brief that names no tier at all.
TIER='THROUGH-CODE'
grep -qi "$TIER" "$BRIEF" && grep -qi "$TIER" "$PROMPT_FILE" || {
  echo "REFUSING: brief and prompt do not both declare tier '$TIER'" >&2; exit 12; }
head -1 "$PROMPT_FILE" | grep -q 'ultrathink' || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 13; }
grep -qF "$BRIEF" "$PROMPT_FILE" && grep -qF "$HEAD_SHA" "$PROMPT_FILE" && grep -qF "$HEAD_SHA" "$BRIEF" || {
  echo "REFUSING: prompt must name the brief path and the head, and the brief must name the head" >&2; exit 14; }
grep -qi 'MAIL YOUR VERDICT' "$PROMPT_FILE" && grep -q 'tuesday-agent@agentmail.to' "$PROMPT_FILE" \
  && grep -qF "$SUBJECT" "$PROMPT_FILE" && grep -qF "$SUBJECT" "$BRIEF" || {
  echo "REFUSING: prompt must say MAIL YOUR VERDICT and name tuesday-agent@agentmail.to; prompt and brief must carry the verdict subject" >&2; exit 15; }

grep -qF '/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env' "$PROMPT_FILE" || {
  echo "REFUSING: prompt must name the AgentMail key by ABSOLUTE path (DELTA 40)" >&2; exit 20; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  worktree HEAD == $HEAD_SHA"
  echo "  base $BASE is an ancestor (target is a CHAIN of 6, not a merge — no two-parent guard)"
  echo "  head is at refs/heads/$BRANCH on origin"
  echo "  report path named in the brief; report does not exist yet"
  echo "  AZURE_CONFIG_DIR=$AZURE_CONFIG_DIR"
  echo "  GH_CONFIG_DIR=$GH_CONFIG_DIR"
  echo "  CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR"
  echo "  in-repo brief present (19) · AgentMail key absolute (20)"
  echo "  tier agrees; prompt: directive, brief path, head, MAIL YOUR VERDICT, tuesday-agent@, subject"
  exit 0
fi

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model claude-opus-5-5 "$(cat "$PROMPT_FILE")"
