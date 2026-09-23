#!/bin/bash
# launch_qa_nexusai_rd518_round3_4230d23.sh — cross-project QA agent, THROUGH-CODE gate, ROUND 3 (the LAST round
# Kam authorised on this class) on Datasec/NexusAI RD-518: branch rd-518-kv-identity-r2-s75c @ 4230d23, by NexusAI-C.
#
# AUTHORITY: Kam, typed to the Tuesday seat 2026-09-21 15:16 — "authorise round 3 for RD-518" — card rd518-round3 = (a),
# scoped to G-01 (RD-592) + G-02 (RD-593), landed as NexusAI CLARIFICATIONS C-121. RD-594 (adminGateRefuses) is OUT.
#
# PATTERN: launch_qa_nexusai_rd518_round2_9a7bc0c.sh. CHANGES:
#   - BASE is round 2's head 9a7bc0c; EXPECTED_COMMITS 1.
#   - exit 22 is a STRICT BOUNDARY: the delta must be EXACTLY the three files verified at commission. RD-518 touches
#     product code (backend/server.js), so round 1's "zero backend/" guard does not apply; an exact set is the tightest
#     true statement, and any fourth file means the builder pushed again or the brief is stale.
#   - exit 25 is NEW and is Kam's scope, enforced: backend/services/authEnforcement.js — home of adminGateRefuses —
#     must be BYTE-UNCHANGED across the delta. RD-594 is excluded by his ruling; the 6 changed lines that mention the
#     function were checked at commission and are all comments, and this guard makes "no call site changed" a
#     measurement at launch rather than a sentence in a brief.
#   - exit 19 asserts G-01 and G-02 by name; exit 24 (from the RD-574 round-2 launcher) refuses a prompt carrying the
#     literal server path, which would make this agent read as a foreign server to any argv-grep floor count.
#
# LAUNCH IT IN A TMUX PANE (cockpit.sh add 'QA/NexusAI-RD518r3' "bash '<this file>'"), NEVER nohup.
# Identity: exports NexusAI's OWN az/gh dirs; CLAUDE_CONFIG_DIR pinned to Tuesday's project-local store.
# ABSOLUTE PATHS ON PURPOSE. TRACKED in launchers/. Written with the Write tool (it contains a legitimate `cd`).
# Usage: launch_qa_nexusai_rd518_round3_4230d23.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..25 a guard refused
set -u

QA_DIR='/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN'
TUE='/Volumes/KK_T9_External_HDD/TUESDAY'
BRIEF="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-21_nexusai-rd518-round3.md"
PROMPT_FILE="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-21_nexusai-rd518-round3.prompt.txt"
REPO='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files'
REPORT="$QA_DIR/projects/nexusai/reports/2026-09-21-rd518-4230d23-round3/report.md"
ROUND2_REPORT="$QA_DIR/projects/nexusai/reports/2026-09-21-rd518-9a7bc0c-round2/report.md"
ID_ROOT="${QA_IDENTITY_ROOT_OVERRIDE:-/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/4_Credentials}"
HEAD_SHA="${QA_HEAD_SHA_OVERRIDE:-4230d237321a2f252730aeca37c73a950eca0f25}"
BASE_SHA='9a7bc0c'
BRANCH='rd-518-kv-identity-r2-s75c'
EXPECTED_COMMITS=1
EXPECTED_FILES='__tests__/rd518-r3-health-detail-decision.test.js
backend/server.js
scripts/verify-expected-counts.json'
RUNBOOK_BRANCH='rd-518-r2-runbook-fix-s75c'
RUNBOOK_SHA='c54d44cea9f2aea6090015118606cdc48ec6a71b'

SUBJECT='[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — RD-518 round 3 @ 4230d23 (through-code)'

[ -d "$QA_DIR" ]      || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]       || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ] || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO/.git" ] || [ -f "$REPO/.git" ] || { echo "repo under test missing: $REPO" >&2; exit 5; }

T="$(git --no-optional-locks -C "$REPO" cat-file -t "$HEAD_SHA" 2>&1)"
[ "$T" = "commit" ] || { echo "REFUSING: $HEAD_SHA is not a commit in $REPO (got '$T')" >&2; exit 6; }

git --no-optional-locks -C "$REPO" merge-base --is-ancestor "$BASE_SHA" "$HEAD_SHA" 2>/dev/null || {
  echo "REFUSING: $BASE_SHA is not an ancestor of $HEAD_SHA — the base in the brief is wrong" >&2; exit 7; }

N="$(git --no-optional-locks -C "$REPO" rev-list --count "${BASE_SHA}..${HEAD_SHA}" 2>&1)"
[ "$N" = "$EXPECTED_COMMITS" ] || { echo "REFUSING: expected $EXPECTED_COMMITS commit in ${BASE_SHA}..${HEAD_SHA}, found '$N' — the builder pushed again and the brief is stale" >&2; exit 8; }

LSR="$(git --no-optional-locks -C "$REPO" ls-remote origin "$BRANCH" 2>&1)"
printf '%s\n' "$LSR" | grep -q "^${HEAD_SHA}[[:space:]]refs/heads/${BRANCH}\$" || {
  echo "REFUSING: $HEAD_SHA is not at refs/heads/$BRANCH on origin — that head moved or was never pushed" >&2
  printf '%s\n' "$LSR" >&2; exit 18; }

LSR2="$(git --no-optional-locks -C "$REPO" ls-remote origin "$RUNBOOK_BRANCH" 2>&1)"
printf '%s\n' "$LSR2" | grep -q "^${RUNBOOK_SHA}[[:space:]]refs/heads/${RUNBOOK_BRANCH}\$" || {
  echo "REFUSING: the runbook the gate needs to RUN is not at origin ($RUNBOOK_SHA on $RUNBOOK_BRANCH)" >&2; exit 21; }

# 22 — STRICT BOUNDARY: exactly the three files verified at commission.
GOT_FILES="$(git --no-optional-locks -C "$REPO" diff --name-only "$BASE_SHA" "$HEAD_SHA" 2>/dev/null | sort)"
[ "$GOT_FILES" = "$(printf '%s\n' "$EXPECTED_FILES" | sort)" ] || {
  echo "REFUSING: the delta is not exactly the three files commissioned. Got:" >&2; printf '%s\n' "$GOT_FILES" >&2; exit 22; }

# 25 — KAM'S SCOPE, ENFORCED: adminGateRefuses lives in authEnforcement.js and RD-594 is excluded from this round.
ND="$(git --no-optional-locks -C "$REPO" diff "$BASE_SHA" "$HEAD_SHA" -- backend/services/authEnforcement.js 2>/dev/null | wc -l | tr -d ' ')"
[ "$ND" = "0" ] || { echo "REFUSING: backend/services/authEnforcement.js changed ($ND diff lines) — RD-594 (adminGateRefuses) is OUT of Kam's round-3 scope" >&2; exit 25; }

[ -s "$ROUND2_REPORT" ] || { echo "REFUSING: round-2 report absent: $ROUND2_REPORT — the gate cannot know what not to re-drive" >&2; exit 23; }
grep -qF "$REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the report path $REPORT" >&2; exit 10; }
[ ! -e "$REPORT" ] || { echo "REFUSING: $REPORT already exists — a stale report would read as this gate's" >&2; exit 17; }

[ -d "$ID_ROOT/.azure" ] && [ -d "$ID_ROOT/.gh-config" ] || {
  echo "REFUSING: NexusAI identity dirs missing under $ID_ROOT (.azure / .gh-config) — would inherit the caller's" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_ROOT/.azure"
export GH_CONFIG_DIR="$ID_ROOT/.gh-config"
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"

TIER='THROUGH-CODE'
grep -qi "$TIER" "$BRIEF" && grep -qi "$TIER" "$PROMPT_FILE" || { echo "REFUSING: brief and prompt do not both declare tier '$TIER'" >&2; exit 12; }
head -1 "$PROMPT_FILE" | grep -q 'ultrathink' || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 13; }
grep -qF "$BRIEF" "$PROMPT_FILE" && grep -qF "$HEAD_SHA" "$PROMPT_FILE" && grep -qF "$HEAD_SHA" "$BRIEF" || {
  echo "REFUSING: prompt must name the brief path and the head, and the brief must name the head" >&2; exit 14; }
grep -qi 'MAIL YOUR VERDICT' "$PROMPT_FILE" && grep -q 'tuesday-agent@agentmail.to' "$PROMPT_FILE" \
  && grep -qF "$SUBJECT" "$PROMPT_FILE" && grep -qF "$SUBJECT" "$BRIEF" || {
  echo "REFUSING: prompt must say MAIL YOUR VERDICT and name tuesday-agent@agentmail.to; prompt and brief must carry the verdict subject" >&2; exit 15; }
grep -qF '/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env' "$PROMPT_FILE" || { echo "REFUSING: prompt must name the AgentMail key by ABSOLUTE path" >&2; exit 20; }
for w in G-01 G-02; do grep -q "$w" "$PROMPT_FILE" || { echo "REFUSING: prompt must carry '$w' by name" >&2; exit 19; }; done
if grep -qi 'backend/server\.js' "$PROMPT_FILE"; then
  echo "REFUSING: the prompt contains the literal server path — this agent would read as a FOREIGN SERVER to any argv-grep floor check. Describe it; do not name it." >&2; exit 24
fi

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  $HEAD_SHA is a commit; base $BASE_SHA ancestor; exactly $EXPECTED_COMMITS commit; head at origin"
  echo "  runbook companion at origin (21)"
  echo "  delta is EXACTLY the three commissioned files (22)"
  echo "  authEnforcement.js byte-unchanged — RD-594 out of scope, enforced (25)"
  echo "  round-2 report present (23); this gate's report does not exist yet"
  echo "  AZURE_CONFIG_DIR=$AZURE_CONFIG_DIR  GH_CONFIG_DIR=$GH_CONFIG_DIR  CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR"
  echo "  tier '$TIER'; key absolute (20); G-01/G-02 present (19); prompt free of the server path (24)"
  exit 0
fi

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model claude-opus-5 "$(cat "$PROMPT_FILE")"
