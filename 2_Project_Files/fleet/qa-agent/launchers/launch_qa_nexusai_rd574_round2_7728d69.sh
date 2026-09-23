#!/bin/bash
# launch_qa_nexusai_rd574_round2_7728d69.sh — cross-project QA agent, THROUGH-CODE gate, ROUND 2 of 2, on
# Datasec/NexusAI RD-574 seam-dependent cells: branch rd-574-seam-cells-s74 @ 7728d69, built by S74.
#
# WHY THROUGH-CODE: round 1 (tier 1, launch_qa_nexusai_rd574_6ec3606.sh) returned NO-GO with two Majors —
# F-1, the "refusing" port was the server's own port; F-2, RD-590 measured, the key-release check lost its only
# protection (V2 stayed green across the whole suite). Everything else round 1 measured HELD. This round carries
# the two repairs and what they disturbed; the tier-1 weight is not spent again.
#
# PATTERN: the round-1 RD-574 launcher. FOUR DELIBERATE CHANGES:
#   - BASE is round 1's head 6ec3606 and EXPECTED_COMMITS is 1: the delta is the repair commit alone.
#   - exit 22 is STRICTER than round 1's. Round 1 asserted zero backend/ files. Round 2 legitimately adds one
#     non-test path (scripts/verify-expected-counts.json: the suite grew by the guard cell round 1 asked for), so
#     the guard now asserts the WHOLE branch touches nothing outside __tests__/ except exactly that file. A
#     looser "no backend/" would silently admit any other product path.
#   - exit 19 asserts the round-2 must-work by name: F-1, F-2, V2, V3.
#   - exit 24 is NEW and STRUCTURAL: the PROMPT must not contain the literal server path. Measured today by S74
#     (RD-591 comment 37901): the floor rule's foreign-server count, a grep over whole command lines, matches QA
#     agents whose PROMPT in argv mentions the path — naive count 3, real server processes 0. Tuesday's own gate
#     prompts were putting it there. Writing the corrected rule into the brief fixes this gate; refusing a prompt
#     that carries the string fixes every later one, whether or not its author remembers why.
#
# Shape verified at commission, from the object store: 7728d69 parents [6ec3606], 1 commit; the round-2 delta is
# 4 files under __tests__/ + scripts/verify-expected-counts.json; zero backend/ across the whole branch.
#
# LAUNCH IT IN A TMUX PANE (cockpit.sh add 'QA/NexusAI-RD574r2' "bash '<this file>'"), NEVER nohup.
# Identity: exports NexusAI's OWN az/gh dirs; CLAUDE_CONFIG_DIR pinned to Tuesday's project-local store.
# ABSOLUTE PATHS ON PURPOSE. TRACKED in launchers/. Written with the Write tool (it contains a legitimate `cd`).
# Usage: launch_qa_nexusai_rd574_round2_7728d69.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..24 a guard refused
set -u

QA_DIR='/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN'
TUE='/Volumes/KK_T9_External_HDD/TUESDAY'
BRIEF="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-21_nexusai-rd574-round2.md"
PROMPT_FILE="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-21_nexusai-rd574-round2.prompt.txt"
REPO='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files'
REPORT="$QA_DIR/projects/nexusai/reports/2026-09-21-rd574-7728d69-round2/report.md"
ROUND1_REPORT="$QA_DIR/projects/nexusai/reports/2026-09-21-rd574-6ec3606-tier1/report.md"
ID_ROOT="${QA_IDENTITY_ROOT_OVERRIDE:-/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/4_Credentials}"
HEAD_SHA="${QA_HEAD_SHA_OVERRIDE:-7728d692f1561fe537960efc5431940e45722cf5}"
BASE_SHA='6ec3606'
MAIN_SHA='60c76d7'
BRANCH='rd-574-seam-cells-s74'
EXPECTED_COMMITS=1
ALLOWED_NONTEST='scripts/verify-expected-counts.json'

SUBJECT='[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — RD-574 round 2 @ 7728d69 (through-code)'

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

# 22 — THE BOUNDARY, stricter than round 1: over the WHOLE branch from main, nothing outside __tests__/ except
# exactly the counts file. Measured, never trusted.
OUT="$(git --no-optional-locks -C "$REPO" diff --name-only "$MAIN_SHA" "$HEAD_SHA" 2>/dev/null | grep -v '^__tests__/' | grep -vxF "$ALLOWED_NONTEST")"
[ -z "$OUT" ] || { echo "REFUSING: the branch touches paths outside __tests__/ beyond $ALLOWED_NONTEST:" >&2; printf '%s\n' "$OUT" >&2; exit 22; }

# 23 — round 1's report must be on disk: the brief tells the gate to read it first and not re-drive what it proved.
[ -s "$ROUND1_REPORT" ] || { echo "REFUSING: round-1 report absent: $ROUND1_REPORT — the gate cannot know what not to re-drive" >&2; exit 23; }

grep -qF "$REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the report path $REPORT" >&2; exit 10; }
[ ! -e "$REPORT" ] || { echo "REFUSING: $REPORT already exists — a stale report would read as this gate's" >&2; exit 17; }

[ -d "$ID_ROOT/.azure" ] && [ -d "$ID_ROOT/.gh-config" ] || {
  echo "REFUSING: NexusAI identity dirs missing under $ID_ROOT (.azure / .gh-config) — would inherit the caller's" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_ROOT/.azure"
export GH_CONFIG_DIR="$ID_ROOT/.gh-config"
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"

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

# 19 — the round-2 must-work, by name.
for w in F-1 F-2 V2 V3; do grep -q "$w" "$PROMPT_FILE" || { echo "REFUSING: prompt must carry '$w' by name" >&2; exit 19; }; done

# 24 — THE PROMPT MUST NOT CARRY THE LITERAL SERVER PATH. The prompt becomes this agent's argv, and a grep-based
# foreign-server count reads argv: a gate whose prompt names the path is counted as a foreign server by every
# seat still using that count (RD-591 comment 37901: naive 3, real 0). Case-insensitive, with a positive control
# proved at commission (the round-1 prompt carries it once).
if grep -qi 'backend/server\.js' "$PROMPT_FILE"; then
  echo "REFUSING: the prompt contains the literal server path — this agent would read as a FOREIGN SERVER to any argv-grep floor check (RD-591 c.37901). Describe it; do not name it." >&2; exit 24
fi

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  $HEAD_SHA is a commit in the object store"
  echo "  base $BASE_SHA is an ancestor; range is exactly $EXPECTED_COMMITS commit (the repair alone)"
  echo "  head is at refs/heads/$BRANCH on origin"
  echo "  whole branch from $MAIN_SHA: nothing outside __tests__/ except $ALLOWED_NONTEST (22)"
  echo "  round-1 report present (23)"
  echo "  report path named in the brief; report does not exist yet"
  echo "  AZURE_CONFIG_DIR=$AZURE_CONFIG_DIR"
  echo "  GH_CONFIG_DIR=$GH_CONFIG_DIR"
  echo "  CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR"
  echo "  tier '$TIER' agrees; AgentMail key absolute (20); F-1/F-2/V2/V3 present (19)"
  echo "  prompt does NOT carry the literal server path (24)"
  echo "  prompt: directive, brief path, head, MAIL YOUR VERDICT, tuesday-agent@, subject"
  exit 0
fi

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model claude-opus-5-5 "$(cat "$PROMPT_FILE")"
