#!/bin/bash
# launch_qa_nexusai_gate2_rd495_rd525_rd575.sh — cross-project QA agent, ONE BATCHED gate (gate 2 of 2026-09-21) on Datasec/NexusAI:
#   TARGET A — RD-495 (+RD-498 folded): rd-495-csp-violations-hard-gate-s71 @ 179bf60, chain aae041a..179bf60 =
#              5ce2b62 (S71 hard check) -> dd90e8b (forward merge of main aae041a) -> d0d252c (fix + 12 cells) -> 179bf60 (counts). TIER 1.
#   TARGET B — RD-525: rd-525-export-erasure-coverage-s76e @ $RD525_SHA = E's last push 91f5b73 + NexusAI-D's lane-A commit
#              (the server entry point only: onPurge('audit-buffer')). TIER 1.
#   TARGET C — RD-575 (OPTIONAL, INCLUDE_RD575=1 default): rd-575-purge-reaches-attachments-s76e @ $RD575_SHA, off main aae041a. TIER 1.
#
# AUTHORITY: queued merge sequence RD-604 -> RD-516 -> RD-495 -> RD-525 -> RD-575, each forward-merged and verified GREEN
# (C-68 / C-89); each merge is Tuesday's GO under C-127. Batching is Kam's standing rule of 2026-09-18
# (0_Brain/learnings/2026-09-18_minimise-gate-duplication-batch-them.md).
#
# PATTERN: launch_qa_nexusai_rd516_fixround_rd604_batch.sh (gate 1, same day). CHANGES:
#   - THREE targets, C optional. TWO unpinned values (RD525_SHA, RD575_SHA). Exit 9 refuses while either reads its
#     placeholder. The placeholder is compared against a literal BUILT BY CONCATENATION ('@RD525''_SHA@'), so a global
#     sed of the placeholder in this file cannot also rewrite the guard's comparand (a previous launcher's guard was
#     disarmed exactly that way). Pin both from `git ls-remote origin <branch>`, never from a mail.
#   - INCLUDE_RD575=0 (env) or --without-rd575 drops C from every guard; the brief and the prompt must then carry the
#     NOT-IN-THIS-GATE markers (exit 21), and RD575_SHA may stay unpinned.
#   - exit 27: dd90e8b is the forward merge claimed, parents EXACTLY 5ce2b62 + aae041a.
#   - exit 26/28/29/34: B = E's six commits off aae041a ending at 91f5b73, then EXACTLY B_LANEA_EXPECTED_COMMITS lane-A
#     commit(s) touching EXACTLY B_LANEA_EXPECTED_FILES; the FIRST lane-A commit touches the server entry point ONLY; the
#     onPurge('audit-buffer') registration is present once at B and absent at 91f5b73.
#   - exit 30: the existing-test edit is byte-identical on B and C and differs from main (the claim E made).
#   - exit 32: the brief's SELF-CHECK timestamp and note placeholders must be stamped by the coordinator before launch.
#   - exit 24 carried: the prompt must not carry the literal server path (RD-591 c.37901).
#
# LAUNCH IT IN A TMUX PANE (cockpit.sh add 'QA/NexusAI-gate2' "bash '<this file>'"), NEVER nohup.
# Identity: exports NexusAI's OWN az/gh dirs; CLAUDE_CONFIG_DIR pinned to Tuesday's project-local store.
# ABSOLUTE PATHS ON PURPOSE. TRACKED in launchers/. Contains a legitimate `cd` (into the QA project, at exec).
# Usage: launch_qa_nexusai_gate2_rd495_rd525_rd575.sh [--check] [--without-rd575]
# Exit: 0 launched (or guards passed under --check) · 2..34 a guard refused
set -u
CHECK=0
INCLUDE_RD575="${INCLUDE_RD575:-1}"
for a in "$@"; do
  case "$a" in
    --check) CHECK=1 ;;
    --without-rd575) INCLUDE_RD575=0 ;;
    *) echo "unknown argument: $a" >&2; exit 2 ;;
  esac
done
case "$INCLUDE_RD575" in 0|1) ;; *) echo "REFUSING: INCLUDE_RD575 must be 0 or 1 (got '$INCLUDE_RD575')" >&2; exit 21 ;; esac

# ─── THE VALUES STILL TO PIN (one variable each; the brief and prompt carry the same placeholders) ─────────────────
RD525_SHA="${QA_RD525_SHA_OVERRIDE:-@RD525_SHA@}"
RD575_SHA="${QA_RD575_SHA_OVERRIDE:-@RD575_SHA@}"
# Pin-time shape of B's lane-A tail after 91f5b73 (check with `git log --format='%H %P' 91f5b73..<RD525_SHA>` and
# `git diff --name-only 91f5b73 <RD525_SHA>`): default = D's one commit, the server entry point only. If D also commits
# the regenerated counts (separately or in the same commit), set the count and add scripts/verify-expected-counts.json.
B_LANEA_EXPECTED_COMMITS=1
B_LANEA_EXPECTED_FILES='backend/server.js'
# Pin-time shape of C (WIP at drafting: 1 commit, 6 files). Re-count at pin; if E adds commits or files, set them here.
C_EXPECTED_COMMITS=1
C_EXPECTED_FILES='__tests__/erasure-partial-purge-leaves-a-record.test.js
__tests__/erasure-reaches-attachments.test.js
__tests__/helpers/zip-entries.js
backend/customerDataFiles.js
backend/dataErasure.js
backend/dataExport.js'
# ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

# Placeholder comparands, BUILT so that no sed of the placeholder text can reach them.
PH_525='@RD525''_SHA@'
PH_575='@RD575''_SHA@'
PH_SCTS='@SELFCHECK''_TS@'
PH_SCNOTE='@SELFCHECK''_NOTE@'

QA_DIR='/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN'
TUE='/Volumes/KK_T9_External_HDD/TUESDAY'
BRIEF="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-21_nexusai-gate2-rd495-rd525-rd575.md"
PROMPT_FILE="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-21_nexusai-gate2-rd495-rd525-rd575.prompt.txt"
REPO='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files'
EVID_D='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/session-tools/s76d'
EVID_E='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/session-tools/s76e'
REPORT="$QA_DIR/projects/nexusai/reports/2026-09-21-gate2-rd495-rd525-rd575/report.md"
ID_ROOT="${QA_IDENTITY_ROOT_OVERRIDE:-/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/4_Credentials}"

MAIN_SHA='aae041a0d01113144cadadba3a44f19025b08d85'
# Target A
A_BRANCH='rd-495-csp-violations-hard-gate-s71'
A_HEAD="${QA_HEAD_SHA_OVERRIDE:-179bf603cf563013ac9f89dbc7b1e216e8a9d385}"
A_CHAIN='179bf603cf563013ac9f89dbc7b1e216e8a9d385
d0d252ce595079614ab26cf5c7cc26302e3ea17c
dd90e8bd8289964b9b47a1f2f7882cb16a0396db
5ce2b627b075633a49e629ff8281b9230f48bc44'
A_MERGE='dd90e8bd8289964b9b47a1f2f7882cb16a0396db'
A_MERGE_P1='5ce2b627b075633a49e629ff8281b9230f48bc44'
A_EXPECTED_FILES='__tests__/rd495-admin-routes-behind-the-gate.test.js
backend/server.js
backend/services/cspReport.js
scripts/verify-expected-counts.json'
# Target B
B_BRANCH='rd-525-export-erasure-coverage-s76e'
B_E_LAST='91f5b7338e41ea9717c68495fbdd285bf85618aa'
B_E_EXPECTED_COMMITS=6
B_E_EXPECTED_FILES='__tests__/erasure-partial-purge-leaves-a-record.test.js
__tests__/helpers/rd525-live-store.js
__tests__/helpers/rd525-purge-on-signal-preload.js
__tests__/rd525-export-and-erasure-cover-every-store.test.js
backend/customerDataFiles.js
backend/dataErasure.js
backend/dataExport.js'
# Target C
C_BRANCH='rd-575-purge-reaches-attachments-s76e'

AUTH_FILE='backend/services/authEnforcement.js'
EDITED_TEST='__tests__/erasure-partial-purge-leaves-a-record.test.js'
SUBJECT='[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — gate 2: RD-495 @ 179bf60 + RD-525 + RD-575 (batched, tier 1)'
C_OUT_BRIEF='TARGET C STATUS: NOT IN THIS GATE'
C_IN_BRIEF='TARGET C STATUS: IN THIS GATE'
C_OUT_PROMPT='RD-575 STATUS: NOT IN THIS GATE'
C_IN_PROMPT='RD-575 STATUS: IN THIS GATE'

g() { git --no-optional-locks -C "$REPO" "$@"; }

# 9 — unpinned heads. Refuse FIRST, before any other guard, so an unpinned launch never gets near claude.
if [ "$RD525_SHA" = "$PH_525" ] || [ -z "$RD525_SHA" ]; then
  echo "REFUSING: RD525_SHA is still the placeholder — pin RD-525's head from \`git ls-remote origin $B_BRANCH\` (in this file, the brief and the prompt) before launching" >&2; exit 9
fi
printf '%s' "$RD525_SHA" | grep -Eq '^[0-9a-f]{40}$' || { echo "REFUSING: RD525_SHA '$RD525_SHA' is not a full 40-hex sha" >&2; exit 9; }
if [ "$INCLUDE_RD575" = "1" ]; then
  if [ "$RD575_SHA" = "$PH_575" ] || [ -z "$RD575_SHA" ]; then
    echo "REFUSING: RD575_SHA is still the placeholder — pin it from \`git ls-remote origin $C_BRANCH\`, or drop C with INCLUDE_RD575=0 / --without-rd575 (and switch the markers in the brief and prompt)" >&2; exit 9
  fi
  printf '%s' "$RD575_SHA" | grep -Eq '^[0-9a-f]{40}$' || { echo "REFUSING: RD575_SHA '$RD575_SHA' is not a full 40-hex sha" >&2; exit 9; }
fi

[ -d "$QA_DIR" ]      || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]       || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ] || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO/.git" ] || [ -f "$REPO/.git" ] || { echo "repo under test missing: $REPO" >&2; exit 5; }

# 21 — INCLUDE_RD575 agrees with the markers in the brief and the prompt.
if [ "$INCLUDE_RD575" = "1" ]; then
  grep -qF "$C_IN_BRIEF" "$BRIEF" && grep -qF "$C_IN_PROMPT" "$PROMPT_FILE" || { echo "REFUSING: INCLUDE_RD575=1 but the brief/prompt do not carry '$C_IN_BRIEF' / '$C_IN_PROMPT'" >&2; exit 21; }
  if grep -qF "$C_OUT_BRIEF" "$BRIEF" || grep -qF "$C_OUT_PROMPT" "$PROMPT_FILE"; then echo "REFUSING: INCLUDE_RD575=1 but a NOT-IN-THIS-GATE marker is present" >&2; exit 21; fi
else
  grep -qF "$C_OUT_BRIEF" "$BRIEF" && grep -qF "$C_OUT_PROMPT" "$PROMPT_FILE" || { echo "REFUSING: INCLUDE_RD575=0 but the brief/prompt do not carry '$C_OUT_BRIEF' / '$C_OUT_PROMPT'" >&2; exit 21; }
  if grep -qF "$C_IN_BRIEF" "$BRIEF" || grep -qF "$C_IN_PROMPT" "$PROMPT_FILE"; then echo "REFUSING: INCLUDE_RD575=0 but an IN-THIS-GATE marker is still present" >&2; exit 21; fi
fi

HEADS="$A_HEAD $B_E_LAST $RD525_SHA"; [ "$INCLUDE_RD575" = "1" ] && HEADS="$HEADS $RD575_SHA"

# 6 — every head is a commit in the object store.
for S in $HEADS; do
  T="$(g cat-file -t "$S" 2>&1)"
  [ "$T" = "commit" ] || { echo "REFUSING: $S is not a commit in $REPO (got '$T')" >&2; exit 6; }
done

# 7 / 8 — A: main is an ancestor, and aae041a..A is EXACTLY the four-commit chain claimed, in order.
g merge-base --is-ancestor "$MAIN_SHA" "$A_HEAD" 2>/dev/null || { echo "REFUSING: main $MAIN_SHA is not an ancestor of A $A_HEAD" >&2; exit 7; }
GOTC="$(g rev-list "${MAIN_SHA}..${A_HEAD}" 2>&1)"
[ "$GOTC" = "$A_CHAIN" ] || { echo "REFUSING: ${MAIN_SHA:0:7}..A is not exactly 5ce2b62 -> dd90e8b -> d0d252c -> 179bf60. Got:" >&2; printf '%s\n' "$GOTC" >&2; exit 8; }

# 27 — dd90e8b is the forward merge claimed: parents EXACTLY 5ce2b62 + aae041a.
P="$(g rev-list --parents -n 1 "$A_MERGE" 2>/dev/null)"
[ "$P" = "$A_MERGE $A_MERGE_P1 $MAIN_SHA" ] || { echo "REFUSING: $A_MERGE parents are not exactly $A_MERGE_P1 + $MAIN_SHA (got '$P')" >&2; exit 27; }

# 26 — B: E's part is EXACTLY six commits off main ending at 91f5b73, and 91f5b73 is an ancestor of B's head.
[ "$(g merge-base "$MAIN_SHA" "$B_E_LAST" 2>/dev/null)" = "$MAIN_SHA" ] || { echo "REFUSING: 91f5b73 is not built on main $MAIN_SHA" >&2; exit 26; }
NE="$(g rev-list --count "${MAIN_SHA}..${B_E_LAST}" 2>&1)"
[ "$NE" = "$B_E_EXPECTED_COMMITS" ] || { echo "REFUSING: expected $B_E_EXPECTED_COMMITS commits in ${MAIN_SHA:0:7}..91f5b73, found '$NE'" >&2; exit 26; }
g merge-base --is-ancestor "$B_E_LAST" "$RD525_SHA" 2>/dev/null || { echo "REFUSING: E's last push 91f5b73 is not an ancestor of RD-525 $RD525_SHA" >&2; exit 26; }
g merge-base --is-ancestor "$MAIN_SHA" "$RD525_SHA" 2>/dev/null || { echo "REFUSING: main is not an ancestor of RD-525 $RD525_SHA" >&2; exit 26; }

# 28 — B's lane-A tail: EXACTLY B_LANEA_EXPECTED_COMMITS single-parent commits; the FIRST touches the server entry point ONLY.
NL="$(g rev-list --count "${B_E_LAST}..${RD525_SHA}" 2>&1)"
[ "$NL" = "$B_LANEA_EXPECTED_COMMITS" ] || { echo "REFUSING: expected $B_LANEA_EXPECTED_COMMITS lane-A commit(s) in 91f5b73..RD-525, found '$NL' — re-read the tail and set B_LANEA_* at pin time" >&2; exit 28; }
NM="$(g rev-list --merges --count "${B_E_LAST}..${RD525_SHA}" 2>&1)"
[ "$NM" = "0" ] || { echo "REFUSING: the lane-A tail contains $NM merge commit(s) — not the shape commissioned" >&2; exit 28; }
FIRST_LA="$(g rev-list --reverse "${B_E_LAST}..${RD525_SHA}" 2>/dev/null | head -1)"
[ "$(g rev-list --parents -n 1 "$FIRST_LA" 2>/dev/null)" = "$FIRST_LA $B_E_LAST" ] || { echo "REFUSING: the first lane-A commit $FIRST_LA is not a single-parent child of 91f5b73" >&2; exit 28; }
[ "$(g diff-tree --no-commit-id -r --name-only "$FIRST_LA" 2>/dev/null)" = "backend/server.js" ] || { echo "REFUSING: the first lane-A commit $FIRST_LA touches more than the server entry point" >&2; exit 28; }

# 18 — heads at origin, by ls-remote.
chk_remote() {  # $1 sha  $2 branch
  local L; L="$(g ls-remote origin "$2" 2>&1)"
  printf '%s\n' "$L" | grep -q "^${1}[[:space:]]refs/heads/${2}\$" || {
    echo "REFUSING: $1 is not at refs/heads/$2 on origin — that head moved or was never pushed" >&2; printf '%s\n' "$L" >&2; exit 18; }
}
chk_remote "$A_HEAD" "$A_BRANCH"
chk_remote "$RD525_SHA" "$B_BRANCH"
[ "$INCLUDE_RD575" = "1" ] && chk_remote "$RD575_SHA" "$C_BRANCH"

# 22 — A: EXACTLY the four commissioned files across aae041a..A.
GOT="$(g diff --name-only "$MAIN_SHA" "$A_HEAD" 2>/dev/null | sort)"
[ "$GOT" = "$(printf '%s\n' "$A_EXPECTED_FILES" | sort)" ] || { echo "REFUSING: A's range is not exactly the four commissioned files. Got:" >&2; printf '%s\n' "$GOT" >&2; exit 22; }

# 29 — B: E's range EXACTLY the seven files; the lane-A tail EXACTLY B_LANEA_EXPECTED_FILES; the whole range their union.
GOTE="$(g diff --name-only "$MAIN_SHA" "$B_E_LAST" 2>/dev/null | sort)"
[ "$GOTE" = "$(printf '%s\n' "$B_E_EXPECTED_FILES" | sort)" ] || { echo "REFUSING: E's range aae041a..91f5b73 is not exactly the seven commissioned files. Got:" >&2; printf '%s\n' "$GOTE" >&2; exit 29; }
GOTL="$(g diff --name-only "$B_E_LAST" "$RD525_SHA" 2>/dev/null | sort)"
[ "$GOTL" = "$(printf '%s\n' "$B_LANEA_EXPECTED_FILES" | sort)" ] || { echo "REFUSING: the lane-A tail 91f5b73..RD-525 is not exactly: $B_LANEA_EXPECTED_FILES. Got:" >&2; printf '%s\n' "$GOTL" >&2; exit 29; }
GOTB="$(g diff --name-only "$MAIN_SHA" "$RD525_SHA" 2>/dev/null | sort)"
[ "$GOTB" = "$(printf '%s\n%s\n' "$B_E_EXPECTED_FILES" "$B_LANEA_EXPECTED_FILES" | sort -u)" ] || { echo "REFUSING: B's whole range is not E's seven files plus the lane-A files. Got:" >&2; printf '%s\n' "$GOTB" >&2; exit 29; }

# 34 — the lane-A registration is present exactly once at B and absent at 91f5b73.
N1="$(g grep -c "onPurge('audit-buffer'" "$RD525_SHA" -- backend/server.js 2>/dev/null | awk -F: '{print $NF}')"
N0="$(g grep -c "onPurge('audit-buffer'" "$B_E_LAST" -- backend/server.js 2>/dev/null | awk -F: '{print $NF}')"
[ "${N1:-0}" = "1" ] && [ "${N0:-0}" = "0" ] || { echo "REFUSING: onPurge('audit-buffer') count is '${N1:-0}' at RD-525 (want 1) and '${N0:-0}' at 91f5b73 (want 0)" >&2; exit 34; }

# 33 — C: built on main, EXACTLY C_EXPECTED_COMMITS commits, EXACTLY the commissioned files.
if [ "$INCLUDE_RD575" = "1" ]; then
  [ "$(g merge-base "$MAIN_SHA" "$RD575_SHA" 2>/dev/null)" = "$MAIN_SHA" ] || { echo "REFUSING: RD-575 $RD575_SHA is not built on main $MAIN_SHA" >&2; exit 33; }
  NC="$(g rev-list --count "${MAIN_SHA}..${RD575_SHA}" 2>&1)"
  [ "$NC" = "$C_EXPECTED_COMMITS" ] || { echo "REFUSING: expected $C_EXPECTED_COMMITS commit(s) in ${MAIN_SHA:0:7}..RD-575, found '$NC' — re-read and set C_EXPECTED_* at pin time" >&2; exit 33; }
  GOTCF="$(g diff --name-only "$MAIN_SHA" "$RD575_SHA" 2>/dev/null | sort)"
  [ "$GOTCF" = "$(printf '%s\n' "$C_EXPECTED_FILES" | sort)" ] || { echo "REFUSING: RD-575's range is not exactly the commissioned files. Got:" >&2; printf '%s\n' "$GOTCF" >&2; exit 33; }
fi

# 30 — the existing-test edit: changed from main on B (and on C, byte-identical to B's).
BE="$(g rev-parse "$RD525_SHA:$EDITED_TEST" 2>/dev/null)"; ME="$(g rev-parse "$MAIN_SHA:$EDITED_TEST" 2>/dev/null)"
[ -n "$BE" ] && [ -n "$ME" ] && [ "$BE" != "$ME" ] || { echo "REFUSING: $EDITED_TEST is absent or unchanged on RD-525 — the approved edit is not where the brief says" >&2; exit 30; }
if [ "$INCLUDE_RD575" = "1" ]; then
  [ "$(g rev-parse "$RD575_SHA:$EDITED_TEST" 2>/dev/null)" = "$BE" ] || { echo "REFUSING: $EDITED_TEST differs between RD-525 and RD-575 — the 'byte-identical edit' claim no longer holds" >&2; exit 30; }
fi

# 25 — authEnforcement.js (adminGateRefuses; RD-594 excluded) byte-unchanged on every target, with presence control.
for S in $HEADS; do
  ND="$(g diff "$MAIN_SHA" "$S" -- "$AUTH_FILE" 2>/dev/null | wc -l | tr -d ' ')"
  [ "$ND" = "0" ] || { echo "REFUSING: $AUTH_FILE changed between main and $S ($ND diff lines) — RD-594 (adminGateRefuses) is excluded" >&2; exit 25; }
  [ "$(g cat-file -t "$S:$AUTH_FILE" 2>/dev/null)" = "blob" ] || { echo "REFUSING: $AUTH_FILE absent at $S — guard 25 would be vacuous" >&2; exit 25; }
done

# 31 — builder evidence on disk.
for f in "$EVID_D/rd495-PROOFS.txt" "$EVID_D/rd495-M2-recheck.txt" "$EVID_D/rd495-proofs.sh" "$EVID_D/rd525-laneA-PROOFS.txt" \
         "$EVID_E/mail-07-ready-rd525.txt" "$EVID_E/rd525-redproof2.log" "$EVID_E/rd525-m1-verify.log" "$EVID_E/expect-redproof-468b9a1.txt" \
         "$EVID_E/laneA-server-js.diff" "$EVID_E/existing-test-edit.diff"; do
  [ -s "$f" ] || { echo "REFUSING: builder evidence absent: $f" >&2; exit 31; }
done
if [ "$INCLUDE_RD575" = "1" ]; then
  for f in "$EVID_E/mail-08-rd575-status.txt" "$EVID_E/rd575-redproof.log"; do
    [ -s "$f" ] || { echo "REFUSING: builder evidence absent: $f" >&2; exit 31; }
  done
fi

grep -qF "$REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the report path $REPORT" >&2; exit 10; }
[ ! -e "$REPORT" ] || { echo "REFUSING: $REPORT already exists — a stale report would read as this gate's" >&2; exit 17; }

[ -d "$ID_ROOT/.azure" ] && [ -d "$ID_ROOT/.gh-config" ] || {
  echo "REFUSING: NexusAI identity dirs missing under $ID_ROOT (.azure / .gh-config) — would inherit the caller's" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_ROOT/.azure"
export GH_CONFIG_DIR="$ID_ROOT/.gh-config"
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"

grep -qi 'TIER 1' "$BRIEF" && grep -qi 'TIER 1' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt do not both declare 'TIER 1'" >&2; exit 12; }
head -1 "$PROMPT_FILE" | grep -q 'ultrathink' || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 13; }
grep -qF "$BRIEF" "$PROMPT_FILE" || { echo "REFUSING: prompt must name the brief path" >&2; exit 14; }
NAMED="$A_HEAD $RD525_SHA"; [ "$INCLUDE_RD575" = "1" ] && NAMED="$NAMED $RD575_SHA"
for S in $NAMED; do
  grep -qF "$S" "$PROMPT_FILE" && grep -qF "$S" "$BRIEF" || { echo "REFUSING: prompt and brief must both name $S" >&2; exit 14; }
done
if grep -qF "$PH_525" "$PROMPT_FILE" "$BRIEF"; then echo "REFUSING: the brief or prompt still carries the RD-525 placeholder" >&2; exit 14; fi
if [ "$INCLUDE_RD575" = "1" ] && grep -qF "$PH_575" "$PROMPT_FILE" "$BRIEF"; then echo "REFUSING: the brief or prompt still carries the RD-575 placeholder" >&2; exit 14; fi
grep -qi 'MAIL YOUR VERDICT' "$PROMPT_FILE" && grep -q 'tuesday-agent@agentmail.to' "$PROMPT_FILE" \
  && grep -qF "$SUBJECT" "$PROMPT_FILE" && grep -qF "$SUBJECT" "$BRIEF" || {
  echo "REFUSING: prompt must say MAIL YOUR VERDICT and name tuesday-agent@agentmail.to; prompt and brief must carry the verdict subject" >&2; exit 15; }
grep -qF '/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env' "$PROMPT_FILE" || { echo "REFUSING: prompt must name the AgentMail key by ABSOLUTE path" >&2; exit 20; }
WORDS="RD-495 RD-498 RD-525 M1 M2 M3 M4 AB1 AB2 S2-CTL onPurge merge-tree C-129 SEPARATELY%PER%TARGET"
[ "$INCLUDE_RD575" = "1" ] && WORDS="$WORDS RD-575 C-98 symlink"
for w in $WORDS; do
  w="${w//%/ }"
  grep -q "$w" "$PROMPT_FILE" || { echo "REFUSING: prompt must carry '$w'" >&2; exit 19; }
done
grep -q 'RULED BY KAM, NOT YET IN AN ARTEFACT' "$BRIEF" || { echo "REFUSING: brief lacks the RULED BY KAM section" >&2; exit 19; }
if grep -qi 'backend/server\.js' "$PROMPT_FILE"; then
  echo "REFUSING: the prompt contains the literal server path — this agent would read as a FOREIGN SERVER to any argv-grep floor check (RD-591 c.37901). Describe it; do not name it." >&2; exit 24
fi
# 32 — the coordinator stamps the self-check (timestamp AND note) before launch.
if grep -qF "$PH_SCTS" "$BRIEF" || grep -qF "$PH_SCNOTE" "$BRIEF" \
   || ! grep -q '^SELF-CHECK: re-read end-to-end for contradictions | ' "$BRIEF" || ! grep -q '^Self-check note: ' "$BRIEF"; then
  echo "REFUSING: the brief's SELF-CHECK line or Self-check note is unstamped — the coordinator re-reads end-to-end and stamps both before launch" >&2; exit 32
fi

# Advisory only (not a guard): main moving is expected while the queue drains; the targets are defined against aae041a.
ML="$(g ls-remote origin main 2>/dev/null | awk '{print $1}')"
[ "$ML" = "$MAIN_SHA" ] || echo "NOTE: origin main is now ${ML:-unreadable}, not ${MAIN_SHA:0:7} — the brief's ranges are still against ${MAIN_SHA:0:7}; the gate reports main three times" >&2

if [ "$CHECK" = "1" ]; then
  echo "all guards pass (INCLUDE_RD575=$INCLUDE_RD575):"
  echo "  A $A_HEAD at origin; chain aae041a..A exactly 5ce2b62 dd90e8b d0d252c 179bf60 (7/8); dd90e8b parents 5ce2b62+aae041a (27); four files (22)"
  echo "  B $RD525_SHA at origin; E's 6 commits to 91f5b73 off main (26); lane-A tail $B_LANEA_EXPECTED_COMMITS commit(s), first = server entry point only (28)"
  echo "  B files: E's seven + [$B_LANEA_EXPECTED_FILES] (29); onPurge('audit-buffer') 1 at B, 0 at 91f5b73 (34)"
  if [ "$INCLUDE_RD575" = "1" ]; then
    echo "  C $RD575_SHA at origin; off main; $C_EXPECTED_COMMITS commit(s); commissioned files (33); existing-test edit identical to B's (30)"
  else
    echo "  C NOT IN THIS GATE — markers present in brief and prompt (21)"
  fi
  echo "  $AUTH_FILE byte-unchanged on every target, with presence control (25)"
  echo "  builder evidence present (31); this gate's report does not exist yet (17)"
  echo "  AZURE_CONFIG_DIR=$AZURE_CONFIG_DIR  GH_CONFIG_DIR=$GH_CONFIG_DIR  CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR"
  echo "  tier (12); directive (13); brief+heads named, no placeholder (14); mail (15); key absolute (20); names (19); no server path (24); self-check stamped (32)"
  exit 0
fi

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model claude-opus-5 "$(cat "$PROMPT_FILE")"
