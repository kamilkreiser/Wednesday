#!/bin/bash
# launch_qa_nexusai_rd516_fixround_rd604_batch.sh — cross-project QA agent, ONE BATCHED gate on Datasec/NexusAI:
#   TARGET A — RD-516 fix round: rd-516-ai-test-ssrf-s73 @ b966634, range 059f0a8..b966634
#              (ae98c74 RD-585 test-only · b966634 RD-541 server one-limiter). RD-541 TIER 1, RD-585 through-code.
#   TARGET B — RD-604: rd-604-rd423-timer-s76d @ $RD604_SHA, off main aae041a, test-only, one file. Through-code.
#
# AUTHORITY: C-126 (Kam 2026-09-21 18:02:06 — hold RD-516, fix RD-585 + RD-541 first; sequence = one batched gate →
# RD-604 merges first → forward-merge main into RD-516, verify GREEN → Tuesday's GO under C-127). Batching is Kam's
# standing rule of 2026-09-18 (0_Brain/learnings/2026-09-18_minimise-gate-duplication-batch-them.md).
#
# PATTERN: launch_qa_nexusai_rd518_round3_4230d23.sh + launch_qa_nexusai_rd574_round2_7728d69.sh. CHANGES:
#   - TWO targets. Every A guard has a B twin; B's head is the ONE unpinned value (RD604_SHA below) and the launcher
#     REFUSES (exit 9) while it still reads the placeholder. Tuesday pins it from `git ls-remote origin`, never a mail.
#   - exit 27 asserts 059f0a8 is the forward merge it is claimed to be: parents EXACTLY aaffbb9 + aae041a.
#   - exit 22 / 29: A's range is EXACTLY two files; B's delta is EXACTLY one file.
#   - exit 25: backend/services/authEnforcement.js (home of adminGateRefuses, RD-594 excluded) byte-unchanged on A
#     (059f0a8..b966634 AND aae041a..b966634) and on B (aae041a..RD604).
#   - exit 30: the rd423 file is byte-identical at aae041a and b966634 — the claim that A's one red is RD-604's.
#   - exit 32: the brief's SELF-CHECK placeholder must be stamped by the coordinator before launch.
#   - exit 24 carried: the prompt must not carry the literal server path (RD-591 c.37901).
#
# LAUNCH IT IN A TMUX PANE (cockpit.sh add 'QA/NexusAI-RD516fix+604' "bash '<this file>'"), NEVER nohup.
# Identity: exports NexusAI's OWN az/gh dirs; CLAUDE_CONFIG_DIR pinned to Tuesday's project-local store.
# ABSOLUTE PATHS ON PURPOSE. TRACKED in launchers/. Contains a legitimate `cd` (into the QA project, at exec).
# Usage: launch_qa_nexusai_rd516_fixround_rd604_batch.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..32 a guard refused
set -u
ARG1="${1:-}"   # saved: guard 25 reuses the positional parameters

# ─── THE ONE VALUE STILL TO PIN ─────────────────────────────────────────────────────────────────────────────────────
RD604_SHA="${QA_RD604_SHA_OVERRIDE:-172abc8308eeb71d3ffa1a1626ef069559876b98}"
# ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

QA_DIR='/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN'
TUE='/Volumes/KK_T9_External_HDD/TUESDAY'
BRIEF="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-21_nexusai-rd516-fixround-rd604-batch.md"
PROMPT_FILE="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-21_nexusai-rd516-fixround-rd604-batch.prompt.txt"
REPO='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files'
EVID='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/session-tools/s76d'
REPORT="$QA_DIR/projects/nexusai/reports/2026-09-21-rd516-fixround-rd604-batch/report.md"
PRIOR_REPORT="$QA_DIR/projects/nexusai/reports/2026-09-21-rd516-aaffbb9-round2/report.md"
ID_ROOT="${QA_IDENTITY_ROOT_OVERRIDE:-/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/4_Credentials}"

# Target A
A_BRANCH='rd-516-ai-test-ssrf-s73'
A_HEAD="${QA_HEAD_SHA_OVERRIDE:-b9666342f50646fbe44aefcdeeaa732dea10dccb}"
A_BASE='059f0a880603abb80c9028e2ad1fb98c5adaf41e'
A_MERGE_P1='aaffbb91a993e23bf06f27e93ea078c3f7879c30'
A_EXPECTED_COMMITS=2
A_EXPECTED_FILES='__tests__/rd516-ai-test-ssrf.test.js
backend/server.js'
# Target B
B_BRANCH='rd-604-rd423-timer-s76d'
MAIN_SHA='aae041a0d01113144cadadba3a44f19025b08d85'
B_EXPECTED_COMMITS=1
B_EXPECTED_FILES='__tests__/rd423-test-ai-does-not-crash-server.test.js'

AUTH_FILE='backend/services/authEnforcement.js'
RD423_FILE='__tests__/rd423-test-ai-does-not-crash-server.test.js'
SUBJECT='[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — RD-516 fix round @ b966634 + RD-604 (batched, tier 1/2)'

g() { git --no-optional-locks -C "$REPO" "$@"; }

# 9 — RD-604's head is not pinned yet. Refuse FIRST, before any other guard, so an unpinned launch never gets near claude.
case "$RD604_SHA" in
  @RD604_SHA@|'') echo "REFUSING: RD604_SHA is still the placeholder '@RD604_SHA@' — pin RD-604's head from \`git ls-remote origin $B_BRANCH\` (in this file, the brief and the prompt) before launching" >&2; exit 9 ;;
esac
printf '%s' "$RD604_SHA" | grep -Eq '^[0-9a-f]{40}$' || { echo "REFUSING: RD604_SHA '$RD604_SHA' is not a full 40-hex sha" >&2; exit 9; }

[ -d "$QA_DIR" ]      || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]       || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ] || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO/.git" ] || [ -f "$REPO/.git" ] || { echo "repo under test missing: $REPO" >&2; exit 5; }

# 6 — both heads are commits in the object store.
for S in "$A_HEAD" "$RD604_SHA"; do
  T="$(g cat-file -t "$S" 2>&1)"
  [ "$T" = "commit" ] || { echo "REFUSING: $S is not a commit in $REPO (got '$T')" >&2; exit 6; }
done

# 7 / 8 — A: base ancestor, exactly two commits.
g merge-base --is-ancestor "$A_BASE" "$A_HEAD" 2>/dev/null || { echo "REFUSING: A base $A_BASE is not an ancestor of $A_HEAD" >&2; exit 7; }
N="$(g rev-list --count "${A_BASE}..${A_HEAD}" 2>&1)"
[ "$N" = "$A_EXPECTED_COMMITS" ] || { echo "REFUSING: expected $A_EXPECTED_COMMITS commits in A's range, found '$N' — the builder pushed again and the brief is stale" >&2; exit 8; }

# 27 — 059f0a8 is the forward merge claimed: parents EXACTLY aaffbb9 + aae041a.
P="$(g rev-list --parents -n 1 "$A_BASE" 2>/dev/null)"
[ "$P" = "$A_BASE $A_MERGE_P1 $MAIN_SHA" ] || { echo "REFUSING: $A_BASE parents are not exactly $A_MERGE_P1 + $MAIN_SHA (got '$P')" >&2; exit 27; }

# 26 / 28 — B: parent is main aae041a, exactly one commit.
BP="$(g rev-list --parents -n 1 "$RD604_SHA" 2>/dev/null)"
[ "$BP" = "$RD604_SHA $MAIN_SHA" ] || { echo "REFUSING: RD-604 $RD604_SHA is not a single-parent commit on main $MAIN_SHA (got '$BP')" >&2; exit 26; }
NB="$(g rev-list --count "${MAIN_SHA}..${RD604_SHA}" 2>&1)"
[ "$NB" = "$B_EXPECTED_COMMITS" ] || { echo "REFUSING: expected $B_EXPECTED_COMMITS commit in ${MAIN_SHA}..RD-604, found '$NB'" >&2; exit 28; }

# 18 — both heads at origin, by ls-remote.
LSR="$(g ls-remote origin "$A_BRANCH" 2>&1)"
printf '%s\n' "$LSR" | grep -q "^${A_HEAD}[[:space:]]refs/heads/${A_BRANCH}\$" || {
  echo "REFUSING: $A_HEAD is not at refs/heads/$A_BRANCH on origin — that head moved or was never pushed" >&2; printf '%s\n' "$LSR" >&2; exit 18; }
LSRB="$(g ls-remote origin "$B_BRANCH" 2>&1)"
printf '%s\n' "$LSRB" | grep -q "^${RD604_SHA}[[:space:]]refs/heads/${B_BRANCH}\$" || {
  echo "REFUSING: $RD604_SHA is not at refs/heads/$B_BRANCH on origin — RD-604 moved or was never pushed" >&2; printf '%s\n' "$LSRB" >&2; exit 18; }

# 22 — A: EXACTLY the two commissioned files.
GOT="$(g diff --name-only "$A_BASE" "$A_HEAD" 2>/dev/null | sort)"
[ "$GOT" = "$(printf '%s\n' "$A_EXPECTED_FILES" | sort)" ] || { echo "REFUSING: A's range is not exactly the two commissioned files. Got:" >&2; printf '%s\n' "$GOT" >&2; exit 22; }
# 29 — B: EXACTLY the one commissioned file.
GOTB="$(g diff --name-only "$MAIN_SHA" "$RD604_SHA" 2>/dev/null | sort)"
[ "$GOTB" = "$B_EXPECTED_FILES" ] || { echo "REFUSING: RD-604's delta is not exactly the one commissioned file. Got:" >&2; printf '%s\n' "$GOTB" >&2; exit 29; }

# 25 — RD-594 exclusion: authEnforcement.js byte-unchanged on both targets.
for R in "$A_BASE $A_HEAD" "$MAIN_SHA $A_HEAD" "$MAIN_SHA $RD604_SHA"; do
  set -- $R
  ND="$(g diff "$1" "$2" -- "$AUTH_FILE" 2>/dev/null | wc -l | tr -d ' ')"
  [ "$ND" = "0" ] || { echo "REFUSING: $AUTH_FILE changed between $1 and $2 ($ND diff lines) — RD-594 (adminGateRefuses) is excluded" >&2; exit 25; }
done
set --
# positive control for 25: the path exists at every sha, so a 0 above is a measurement, not a missing file.
for S in "$A_HEAD" "$MAIN_SHA" "$RD604_SHA"; do
  [ "$(g cat-file -t "$S:$AUTH_FILE" 2>/dev/null)" = "blob" ] || { echo "REFUSING: $AUTH_FILE absent at $S — guard 25 would be vacuous" >&2; exit 25; }
done

# 30 — A's one red is RD-604's: the rd423 file is byte-identical on A's head and on main.
[ "$(g rev-parse "$A_HEAD:$RD423_FILE" 2>/dev/null)" = "$(g rev-parse "$MAIN_SHA:$RD423_FILE" 2>/dev/null)" ] || {
  echo "REFUSING: $RD423_FILE differs between A's head and main — the 'one red is RD-604' claim no longer holds" >&2; exit 30; }

# 23 / 31 — prior report and builder evidence on disk.
[ -s "$PRIOR_REPORT" ] || { echo "REFUSING: round-2 report absent: $PRIOR_REPORT" >&2; exit 23; }
for f in rd585-rd541-PROOFS.txt rd585-r7-response.json rd604-PROOFS.txt; do
  [ -s "$EVID/$f" ] || { echo "REFUSING: builder evidence absent: $EVID/$f" >&2; exit 31; }
done

grep -qF "$REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the report path $REPORT" >&2; exit 10; }
[ ! -e "$REPORT" ] || { echo "REFUSING: $REPORT already exists — a stale report would read as this gate's" >&2; exit 17; }

[ -d "$ID_ROOT/.azure" ] && [ -d "$ID_ROOT/.gh-config" ] || {
  echo "REFUSING: NexusAI identity dirs missing under $ID_ROOT (.azure / .gh-config) — would inherit the caller's" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_ROOT/.azure"
export GH_CONFIG_DIR="$ID_ROOT/.gh-config"
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"

for TIER in 'TIER 1' 'THROUGH-CODE'; do
  grep -qi "$TIER" "$BRIEF" && grep -qi "$TIER" "$PROMPT_FILE" || { echo "REFUSING: brief and prompt do not both declare '$TIER'" >&2; exit 12; }
done
head -1 "$PROMPT_FILE" | grep -q 'ultrathink' || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 13; }
grep -qF "$BRIEF" "$PROMPT_FILE" || { echo "REFUSING: prompt must name the brief path" >&2; exit 14; }
for S in "$A_HEAD" "$RD604_SHA"; do
  grep -qF "$S" "$PROMPT_FILE" && grep -qF "$S" "$BRIEF" || { echo "REFUSING: prompt and brief must both name $S" >&2; exit 14; }
done
if grep -qF '@RD604_SHA@' "$PROMPT_FILE" "$BRIEF"; then echo "REFUSING: the brief or prompt still carries '@RD604_SHA@'" >&2; exit 14; fi
grep -qi 'MAIL YOUR VERDICT' "$PROMPT_FILE" && grep -q 'tuesday-agent@agentmail.to' "$PROMPT_FILE" \
  && grep -qF "$SUBJECT" "$PROMPT_FILE" && grep -qF "$SUBJECT" "$BRIEF" || {
  echo "REFUSING: prompt must say MAIL YOUR VERDICT and name tuesday-agent@agentmail.to; prompt and brief must carry the verdict subject" >&2; exit 15; }
grep -qF '/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env' "$PROMPT_FILE" || { echo "REFUSING: prompt must name the AgentMail key by ABSOLUTE path" >&2; exit 20; }
for w in RD-585 RD-541 RD-604 R7 R8 rd545 'SEPARATELY PER TARGET'; do
  grep -q "$w" "$PROMPT_FILE" || { echo "REFUSING: prompt must carry '$w'" >&2; exit 19; }
done
grep -q 'RULED BY KAM, NOT YET IN AN ARTEFACT' "$BRIEF" || { echo "REFUSING: brief lacks the RULED BY KAM section" >&2; exit 19; }
if grep -qi 'backend/server\.js' "$PROMPT_FILE"; then
  echo "REFUSING: the prompt contains the literal server path — this agent would read as a FOREIGN SERVER to any argv-grep floor check (RD-591 c.37901). Describe it; do not name it." >&2; exit 24
fi
# 32 — the coordinator stamps the self-check before launch.
if grep -qF 'SELF-CHECK: @SELFCHECK@' "$BRIEF" || ! grep -q '^SELF-CHECK: ' "$BRIEF"; then
  echo "REFUSING: the brief's SELF-CHECK line is unstamped — the coordinator stamps it before launch" >&2; exit 32
fi

if [ "$ARG1" = "--check" ]; then
  echo "all guards pass:"
  echo "  A $A_HEAD at origin; base ${A_BASE:0:7} ancestor; exactly $A_EXPECTED_COMMITS commits; merge parents aaffbb9+aae041a (27)"
  echo "  B $RD604_SHA at origin; single parent main ${MAIN_SHA:0:7}; exactly $B_EXPECTED_COMMITS commit (26/28)"
  echo "  A range EXACTLY two files (22); B EXACTLY one file (29)"
  echo "  $AUTH_FILE byte-unchanged on A and B, with presence control (25)"
  echo "  rd423 byte-identical on A head and main (30)"
  echo "  prior report (23) + builder evidence (31) present; this gate's report does not exist yet"
  echo "  AZURE_CONFIG_DIR=$AZURE_CONFIG_DIR  GH_CONFIG_DIR=$GH_CONFIG_DIR  CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR"
  echo "  tiers declared (12); directive (13); brief+both heads named (14); key absolute (20); names (19); no server path (24); self-check stamped (32)"
  exit 0
fi

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model claude-opus-5 "$(cat "$PROMPT_FILE")"
