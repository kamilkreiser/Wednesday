#!/bin/bash
# launch_qa_nexusai_gate6_rd619_rd607_pr31.sh — cross-project QA agent, ONE BATCHED gate (gate 6 of 2026-09-22) on Datasec/NexusAI:
#   TARGET A — RD-619: rd-619-harness-boot-leak-s79h @ 695ca5a, off 982a84f; chain f26c740 -> 695ca5a. TIER 2 (harness only).
#   TARGET B — RD-607: rd-607-redis-limiter-stores-s79h @ 8fa0791, STACKED on A; 695ca5a..8fa0791 = 80d083b, 9de358e (merge),
#              c7dc9fd (merge), 8fa0791. TIER 1 (rate limiting, a security control).
#   TARGET C — PR #31 = RD-641 (ii): ci-node24-rd641-s79h @ a11eb5f, one commit off main 58bb38c. TIER 2 (three workflow lines).
#   All heads are KNOWN at drafting — no environment pin. Each is re-read by ls-remote right before launch (18).
#
# AUTHORITY: READY FOR QA from S79H (NexusAI-H): RD-619 2026-09-21T23:08:20Z, RD-607 2026-09-22T04:04:23Z, PR #31
# 2026-09-22T04:30:45Z. PR #31's change approved by Kam (C-143). Batching is Kam's standing rule of 2026-09-18
# (0_Brain/learnings/2026-09-18_minimise-gate-duplication-batch-them.md). Merges after this gate are Tuesday's GO (C-127).
#
# PATTERN: launch_qa_nexusai_gate5_rd615_rd616.sh. CHANGES:
#   - three targets; A's and C's base differ (982a84f vs 58bb38c); B's base is A's head.
#   - exit 8: B's chain contains two MERGE commits — every commit's EXACT parent list is asserted, not "single-parent".
#   - exit 18: also refs/pull/31/head == C's head.
#   - exit 54: A touches NO product file (every path under __tests__/ or the counts file) — with a presence control.
#   - exit 55: C's diff is EXACTLY the three approved lines ('20' -> '24' at build.yml:25, deploy.yml:27, npm-audit.yml:25),
#     and deploy.yml at C is workflow_dispatch-only with no secrets / azure login / environment.
#   - exit 56: RD-619's four files are byte-identical at A and B (B does not change the harness).
#   - exit 57: B's server entry point has EXACTLY seven rateLimit( calls, all rateLimit(_rlOpts('<name>'…, seven unique names.
#   - exit 58: brief and prompt forbid claiming Node 24 fixes HS3. exit 59: qa-gate6- lock tag. exit 60: parse-before-red
#     rule. exit 61: tree exclusivity.
#   - exit 38: negative-control seats G 57419, H 29254, Tuesday 63076.
#   - exit 32: SELF-CHECK timestamp and note placeholders stamped by the coordinator before launch (LAST guard, so --check
#     shows every other guard first). Placeholder comparands are BUILT BY CONCATENATION so a sed of the placeholder text
#     cannot reach them.
#   - exit 24 carried: the prompt must not carry the literal server path (RD-591 c.37901).
#
# LAUNCH IT IN A TMUX PANE (cockpit.sh add 'QA/NexusAI-gate6' "bash '<this file>'"), NEVER nohup.
# Identity: exports NexusAI's OWN az/gh dirs (gh is needed READ-ONLY for PR #31's CI run); CLAUDE_CONFIG_DIR pinned to
# Tuesday's project-local store.
# ABSOLUTE PATHS ON PURPOSE. TRACKED in launchers/. Contains a legitimate `cd` (into the QA project, at exec).
# Usage: launch_qa_nexusai_gate6_rd619_rd607_pr31.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..61 a guard refused
set -u
CHECK=0
for a in "$@"; do
  case "$a" in
    --check) CHECK=1 ;;
    *) echo "unknown argument: $a" >&2; exit 2 ;;
  esac
done

# Placeholder comparands, BUILT so that no sed of the placeholder text can reach them.
PH_SCTS='@SELFCHECK''_TS@'
PH_SCNOTE='@SELFCHECK''_NOTE@'

QA_DIR='/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN'
TUE='/Volumes/KK_T9_External_HDD/TUESDAY'
BRIEF="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-22_nexusai-gate6-rd619-rd607-pr31.md"
PROMPT_FILE="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-22_nexusai-gate6-rd619-rd607-pr31.prompt.txt"
REPO='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files'
NX='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI'
EVID_H="$NX/session-tools/s79h"
G1_REPORT="$QA_DIR/projects/nexusai/reports/2026-09-21-rd516-fixround-rd604-batch/report.md"
G5_REPORT="$QA_DIR/projects/nexusai/reports/2026-09-22-gate5-rd615-rd616/report.md"
G5_FLOOR="$QA_DIR/projects/nexusai/reports/2026-09-22-gate5-rd615-rd616/evidence/qa-floorcount.py"
G5_FLOORLIB="$QA_DIR/projects/nexusai/reports/2026-09-22-gate5-rd615-rd616/evidence/qa-floorlib.sh"
G4_STALL="$QA_DIR/projects/nexusai/reports/2026-09-22-gate4-rd575-rd524r2/evidence/a3u-stall-evidence.txt"
REPORT="$QA_DIR/projects/nexusai/reports/2026-09-22-gate6-rd619-rd607-pr31/report.md"
ID_ROOT="${QA_IDENTITY_ROOT_OVERRIDE:-$NX/4_Credentials}"

CUT_SHA='982a84f2d0c72596a2d389897439e1d8d3425068'    # main when A and B were cut
MAIN_SHA='58bb38c1f49987865782f7fda91477350a8ff303'   # main now; C's base
# Target A
A_BRANCH='rd-619-harness-boot-leak-s79h'
A_HEAD="${QA_A_HEAD_OVERRIDE:-695ca5ac96994f1d1f16e9ad0a8c2d5f6f9b0538}"
A_FIX='f26c740c1a7a8db34c7be18b06e16cf529eac400'
A_CHAIN='695ca5ac96994f1d1f16e9ad0a8c2d5f6f9b0538
f26c740c1a7a8db34c7be18b06e16cf529eac400'
A_EXPECTED_FILES='__tests__/helpers/rd395-server-harness.js
__tests__/helpers/rd619-exits-preload.js
__tests__/helpers/rd619-never-listens-preload.js
__tests__/rd619-harness-boot-failure-stops-child.test.js
scripts/verify-expected-counts.json'
A_FIX_FILES='__tests__/helpers/rd395-server-harness.js
__tests__/helpers/rd619-exits-preload.js
__tests__/helpers/rd619-never-listens-preload.js
__tests__/rd619-harness-boot-failure-stops-child.test.js'
A_EXPECTED_TESTS=3863
A_EXPECTED_SUITES=220
# Target B
B_BRANCH='rd-607-redis-limiter-stores-s79h'
B_HEAD="${QA_B_HEAD_OVERRIDE:-8fa07917092777bc89be0067a67fe01b614532c2}"
B_CHANGE='80d083b0a75284dbe7cb234e2596f5a14d3574d2'
B_MERGE1='9de358e069af8b5b4f8e58cea396ff3b0a9afde9'
B_MERGE2='c7dc9fd5ef364d086ab3027a017c5920696967b4'
B_CHAIN='8fa07917092777bc89be0067a67fe01b614532c2
c7dc9fd5ef364d086ab3027a017c5920696967b4
9de358e069af8b5b4f8e58cea396ff3b0a9afde9
80d083b0a75284dbe7cb234e2596f5a14d3574d2'
# "<commit> <parent1> [<parent2>]" — the EXACT parent list of every commit in B's chain.
B_PARENTS='80d083b0a75284dbe7cb234e2596f5a14d3574d2 982a84f2d0c72596a2d389897439e1d8d3425068
9de358e069af8b5b4f8e58cea396ff3b0a9afde9 80d083b0a75284dbe7cb234e2596f5a14d3574d2 f26c740c1a7a8db34c7be18b06e16cf529eac400
c7dc9fd5ef364d086ab3027a017c5920696967b4 9de358e069af8b5b4f8e58cea396ff3b0a9afde9 695ca5ac96994f1d1f16e9ad0a8c2d5f6f9b0538
8fa07917092777bc89be0067a67fe01b614532c2 c7dc9fd5ef364d086ab3027a017c5920696967b4'
B_EXPECTED_FILES='__tests__/helpers/rd607-fake-redis.js
__tests__/rd607-redis-limiters-keep-their-own-counts.test.js
backend/server.js
scripts/verify-expected-counts.json'
B_CHANGE_FILES='__tests__/helpers/rd607-fake-redis.js
__tests__/rd607-redis-limiters-keep-their-own-counts.test.js
backend/server.js'
B_LIMITER_NAMES='ai
ai-test
auth
csp-report
data-source-test
general
setup'
B_EXPECTED_TESTS=3870
B_EXPECTED_SUITES=221
# Target C
C_BRANCH='ci-node24-rd641-s79h'
C_HEAD="${QA_C_HEAD_OVERRIDE:-a11eb5f1544be745cde315f6273e2a2ef979a0c8}"
C_PR_REF='refs/pull/31/head'
C_EXPECTED_FILES='.github/workflows/build.yml
.github/workflows/deploy.yml
.github/workflows/npm-audit.yml'
C_EXPECTED_HUNKS='@@ -25 +25 @@
@@ -27 +27 @@
@@ -25 +25 @@'
C_EXPECTED_TESTS=3914
C_EXPECTED_SUITES=223
NEG_SEATS='57419 29254 63076'   # NexusAI-G (%36), NexusAI-H (%38), Tuesday (%0) at drafting

AUTH_FILE='backend/services/authEnforcement.js'
SERVER_FILE='backend/server.js'
COUNTS_FILE='scripts/verify-expected-counts.json'
SUBJECT='[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — gate 6: RD-619 @ 695ca5a (tier 2) + RD-607 @ 8fa0791 (tier 1) + PR #31 RD-641 (ii) @ a11eb5f (tier 2)'

g() { git --no-optional-locks -C "$REPO" "$@"; }
sorted() { printf '%s\n' "$1" | sed '/^$/d' | sort; }
counts_at() { g show "$1:$COUNTS_FILE" 2>/dev/null | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d["tests"], d["suites"])' 2>/dev/null; }
files_of() { g diff --name-only "$1^" "$1" 2>/dev/null | sort; }   # vs FIRST parent

[ -d "$QA_DIR" ]      || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]       || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ] || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO/.git" ] || [ -f "$REPO/.git" ] || { echo "repo under test missing: $REPO" >&2; exit 5; }

# 6 — every pinned sha is a commit in the object store.
for S in $CUT_SHA $MAIN_SHA $A_HEAD $A_FIX $B_HEAD $B_CHANGE $B_MERGE1 $B_MERGE2 $C_HEAD; do
  T="$(g cat-file -t "$S" 2>&1)"
  [ "$T" = "commit" ] || { echo "REFUSING: $S is not a commit in $REPO (got '$T') — this launcher never fetches" >&2; exit 6; }
done

# 7 / 8 — per target: its base is ancestor AND merge-base; base..head is EXACTLY the chain; parents exactly as commissioned.
check_chain() { # label base head chain
  local L="$1" BASE="$2" H="$3" C="$4" GOTC
  g merge-base --is-ancestor "$BASE" "$H" 2>/dev/null || { echo "REFUSING: $BASE is not an ancestor of $L $H" >&2; exit 7; }
  [ "$(g merge-base "$BASE" "$H" 2>/dev/null)" = "$BASE" ] || { echo "REFUSING: merge-base($BASE, $L) is not $BASE" >&2; exit 7; }
  GOTC="$(g log --format=%H "${BASE}..${H}" 2>&1)"   # log, not rev-list: same list, reverse-chronological
  [ "$GOTC" = "$C" ] || { echo "REFUSING: ${BASE:0:7}..$L is not exactly the commissioned chain. Got:" >&2; printf '%s\n' "$GOTC" >&2; exit 8; }
}
parents_are() { # commit expected-parents...
  local c="$1"; shift
  local GOT; GOT="$(g log -1 --format='%H %P' "$c" 2>/dev/null)"
  [ "$GOT" = "$c $*" ] || { echo "REFUSING: parents of $c are '${GOT#* }', not '$*'" >&2; exit 8; }
}
check_chain A "$CUT_SHA" "$A_HEAD" "$A_CHAIN"
parents_are "$A_FIX" "$CUT_SHA"
parents_are "$A_HEAD" "$A_FIX"
check_chain B "$A_HEAD" "$B_HEAD" "$B_CHAIN"
while IFS= read -r LINE; do
  [ -z "$LINE" ] && continue
  # shellcheck disable=SC2086
  parents_are $LINE
done <<< "$B_PARENTS"
check_chain C "$MAIN_SHA" "$C_HEAD" "$C_HEAD"
parents_are "$C_HEAD" "$MAIN_SHA"

# 18 — RE-PIN: every head at origin, by ls-remote, read NOW (immediately before launch); and PR #31's head ref.
for PAIR in "$A_BRANCH $A_HEAD" "$B_BRANCH $B_HEAD" "$C_BRANCH $C_HEAD"; do
  BR="${PAIR%% *}"; H="${PAIR##* }"
  L="$(g ls-remote origin "refs/heads/$BR" 2>&1)"
  printf '%s\n' "$L" | grep -q "^${H}[[:space:]]refs/heads/${BR}\$" || {
    echo "REFUSING: $H is not at refs/heads/$BR on origin — that head moved or was never pushed; re-brief" >&2; printf '%s\n' "$L" >&2; exit 18; }
done
L="$(g ls-remote origin "$C_PR_REF" 2>&1)"
printf '%s\n' "$L" | grep -q "^${C_HEAD}[[:space:]]${C_PR_REF}\$" || {
  echo "REFUSING: $C_PR_REF is not $C_HEAD on origin — PR #31 moved; re-brief" >&2; printf '%s\n' "$L" >&2; exit 18; }

# 22 — each target's delta over its base is EXACTLY its commissioned file set.
GOT="$(g diff --name-only "$CUT_SHA" "$A_HEAD" 2>/dev/null | sort)"
[ "$GOT" = "$(sorted "$A_EXPECTED_FILES")" ] || { echo "REFUSING: A's delta over ${CUT_SHA:0:7} is not exactly the five commissioned files. Got:" >&2; printf '%s\n' "$GOT" >&2; exit 22; }
GOT="$(g diff --name-only "$A_HEAD" "$B_HEAD" 2>/dev/null | sort)"
[ "$GOT" = "$(sorted "$B_EXPECTED_FILES")" ] || { echo "REFUSING: B's delta over A is not exactly the four commissioned files. Got:" >&2; printf '%s\n' "$GOT" >&2; exit 22; }
GOT="$(g diff --name-only "$MAIN_SHA" "$C_HEAD" 2>/dev/null | sort)"
[ "$GOT" = "$(sorted "$C_EXPECTED_FILES")" ] || { echo "REFUSING: C's delta over main is not exactly the three workflow files. Got:" >&2; printf '%s\n' "$GOT" >&2; exit 22; }

# 35 — counts files read EXACTLY the builders' figures (C = main's: it changes no test).
for T in "A $A_HEAD $A_EXPECTED_TESTS $A_EXPECTED_SUITES" "B $B_HEAD $B_EXPECTED_TESTS $B_EXPECTED_SUITES" "C $C_HEAD $C_EXPECTED_TESTS $C_EXPECTED_SUITES"; do
  set -- $T
  CT="$(counts_at "$2")"
  [ "$CT" = "$3 $4" ] || { echo "REFUSING: $COUNTS_FILE at $1 reads '${CT:-unreadable}', not '$3 $4'" >&2; exit 35; }
done

# 50 — per-commit file sets (vs FIRST parent): counts-only commits; the fix commits; B's two merges.
[ "$(files_of "$A_HEAD")" = "$COUNTS_FILE" ] || { echo "REFUSING: ${A_HEAD:0:7} is not counts-only" >&2; exit 50; }
[ "$(files_of "$A_FIX")" = "$(sorted "$A_FIX_FILES")" ] || { echo "REFUSING: ${A_FIX:0:7} file set is not RD-619's four non-counts files" >&2; exit 50; }
[ "$(files_of "$B_HEAD")" = "$COUNTS_FILE" ] || { echo "REFUSING: ${B_HEAD:0:7} is not counts-only" >&2; exit 50; }
[ "$(files_of "$B_MERGE2")" = "$COUNTS_FILE" ] || { echo "REFUSING: merge ${B_MERGE2:0:7} changes more than the counts file over its first parent" >&2; exit 50; }
[ "$(files_of "$B_MERGE1")" = "$(sorted "$A_FIX_FILES")" ] || { echo "REFUSING: merge ${B_MERGE1:0:7} brings more than RD-619's four files over its first parent" >&2; exit 50; }
[ "$(files_of "$B_CHANGE")" = "$(sorted "$B_CHANGE_FILES")" ] || { echo "REFUSING: ${B_CHANGE:0:7} file set is not fake-redis + rd607 test + the server entry point" >&2; exit 50; }

# 54 — A touches NO product file: every path is under __tests__/ or is the counts file; presence control on the harness.
NP="$(g diff --name-only "$CUT_SHA" "$A_HEAD" 2>/dev/null | grep -v -E '^__tests__/' | grep -v -x -F "$COUNTS_FILE")"
[ -z "$NP" ] || { echo "REFUSING: A touches a non-test path — it is not tier 2 as briefed; re-tier:" >&2; printf '%s\n' "$NP" >&2; exit 54; }
[ "$(g cat-file -t "$A_HEAD:__tests__/helpers/rd395-server-harness.js" 2>/dev/null)" = "blob" ] || { echo "REFUSING: harness absent at A — guard 54 would be vacuous" >&2; exit 54; }

# 55 — C is EXACTLY the three approved lines, and deploy.yml at C deploys nothing.
NS="$(g diff --numstat "$MAIN_SHA" "$C_HEAD" 2>/dev/null | awk '{print $1" "$2}' | sort -u)"
[ "$NS" = "1 1" ] || { echo "REFUSING: C's numstat is not 1/1 on every file (got: $NS)" >&2; exit 55; }
HK="$(g diff -U0 "$MAIN_SHA" "$C_HEAD" 2>/dev/null | grep '^@@' | sed 's/ jobs:$//')"
[ "$HK" = "$C_EXPECTED_HUNKS" ] || { echo "REFUSING: C's hunks are not at build.yml:25, deploy.yml:27, npm-audit.yml:25. Got:" >&2; printf '%s\n' "$HK" >&2; exit 55; }
MINUS="$(g diff -U0 "$MAIN_SHA" "$C_HEAD" 2>/dev/null | grep -E '^-[^-]' | sed 's/^-[[:space:]]*//' | sort -u)"
PLUS="$(g diff -U0 "$MAIN_SHA" "$C_HEAD" 2>/dev/null | grep -E '^\+[^+]' | sed 's/^+[[:space:]]*//' | sort -u)"
[ "$MINUS" = "node-version: '20'" ] && [ "$PLUS" = "node-version: '24'" ] || { echo "REFUSING: C's changed lines are not exactly node-version '20' -> '24' (got -[$MINUS] +[$PLUS])" >&2; exit 55; }
DY="$(g show "$C_HEAD:.github/workflows/deploy.yml" 2>/dev/null)"
[ -n "$DY" ] || { echo "REFUSING: deploy.yml unreadable at C — guard 55 would be vacuous" >&2; exit 55; }
printf '%s\n' "$DY" | grep -q '^  workflow_dispatch:' || { echo "REFUSING: deploy.yml at C has no workflow_dispatch trigger — not the file the brief describes" >&2; exit 55; }
if printf '%s\n' "$DY" | grep -q -E '^  (push|pull_request|pull_request_target|schedule|workflow_run|release):' \
   || printf '%s\n' "$DY" | grep -q -E 'secrets\.|azure/login|^[[:space:]]+environment:'; then
  echo "REFUSING: deploy.yml at C has a push/schedule trigger, a secret, an Azure login or an environment — the brief says it deploys nothing; re-brief" >&2; exit 55
fi

# 56 — RD-619's four files are byte-identical at A and at B.
while IFS= read -r F; do
  [ -z "$F" ] && continue
  BA="$(g rev-parse "$A_HEAD:$F" 2>/dev/null)"; BB="$(g rev-parse "$B_HEAD:$F" 2>/dev/null)"
  [ -n "$BA" ] && [ "$BA" = "$BB" ] || { echo "REFUSING: $F differs between A and B (or is absent) — B changes RD-619's files; re-brief" >&2; exit 56; }
done <<< "$A_FIX_FILES"

# 57 — B's server entry point: EXACTLY seven rateLimit( calls, all through _rlOpts('<name>', seven unique names as briefed.
SRC="$(g show "$B_HEAD:$SERVER_FILE" 2>/dev/null)"
[ -n "$SRC" ] || { echo "REFUSING: server entry point unreadable at B — guard 57 would be vacuous" >&2; exit 57; }
NCALL="$(printf '%s\n' "$SRC" | grep -o 'rateLimit(' | wc -l | tr -d ' ')"
NAMES="$(printf '%s\n' "$SRC" | grep -o -E "rateLimit\(_rlOpts\('[a-z][a-z0-9-]*'" | sed -E "s/.*'([a-z0-9-]+)'/\1/" | sort)"
[ "$NCALL" = "7" ] && [ "$NAMES" = "$(sorted "$B_LIMITER_NAMES")" ] || {
  echo "REFUSING: B's server entry point has $NCALL rateLimit( calls / names [$(printf '%s' "$NAMES" | tr '\n' ' ')] — the brief says seven: $(printf '%s' "$B_LIMITER_NAMES" | tr '\n' ' ')" >&2; exit 57; }

# 25 — authEnforcement.js byte-unchanged by A, B and C; with presence control.
for PAIR in "$CUT_SHA $A_HEAD" "$A_HEAD $B_HEAD" "$MAIN_SHA $C_HEAD"; do
  BASE="${PAIR%% *}"; H="${PAIR##* }"
  ND="$(g diff "$BASE" "$H" -- "$AUTH_FILE" 2>/dev/null | wc -l | tr -d ' ')"
  [ "$ND" = "0" ] || { echo "REFUSING: $AUTH_FILE changed between $BASE and $H ($ND diff lines) — not commissioned; re-brief" >&2; exit 25; }
  [ "$(g cat-file -t "$H:$AUTH_FILE" 2>/dev/null)" = "blob" ] || { echo "REFUSING: $AUTH_FILE absent at $H — guard 25 would be vacuous" >&2; exit 25; }
done

# 31 — builder evidence and prior-gate evidence on disk.
for f in "$EVID_H/mail-09-ready-rd619.7jslsO" "$EVID_H/expect-rd619.txt" "$EVID_H/rd619-proof-hold.sh" "$EVID_H/rd619-hold-run1.out" \
         "$EVID_H/rd619-R0.log" "$EVID_H/rd619-M-619.log" "$EVID_H/rd619-C68.log" "$EVID_H/rd619-verify.log" \
         "$EVID_H/mail-32-ready607.QYVHTx" "$EVID_H/expect-rd607.txt" "$EVID_H/rd607-proof-hold.sh" "$EVID_H/rd607-hold-run5.out" \
         "$EVID_H/rd607-R0.log" "$EVID_H/rd607-M-607.log" "$EVID_H/rd607-M-dup.log" "$EVID_H/rd607-verify.log" \
         "$EVID_H/mail-34-ready-pr31.IzmaCR" "$EVID_H/mail-33-ci615.7rctbl" "$EVID_H/rd641-known-failing-set-982a84f.txt" \
         "$EVID_H/rd641-failing-set-pr31.txt" "$EVID_H/rd641-failing-set-58bb38c.txt" "$NX/HANDOVER-S79H.md" \
         "$G1_REPORT" "$G5_REPORT" "$G4_STALL"; do
  [ -s "$f" ] || { echo "REFUSING: evidence absent: $f" >&2; exit 31; }
done

# 39 — gate 5's floor instrument, which the brief prescribes, is on disk.
[ -s "$G5_FLOOR" ] && [ -s "$G5_FLOORLIB" ] || { echo "REFUSING: gate 5's floor instrument missing: $G5_FLOOR / $G5_FLOORLIB" >&2; exit 39; }
grep -qF "$G5_FLOOR" "$BRIEF" || { echo "REFUSING: brief does not name the floor instrument $G5_FLOOR" >&2; exit 39; }

grep -qF "$REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the report path $REPORT" >&2; exit 10; }
grep -qF "$REPORT" "$PROMPT_FILE" || { echo "REFUSING: prompt does not name the report path $REPORT" >&2; exit 10; }
[ ! -e "$REPORT" ] || { echo "REFUSING: $REPORT already exists — a stale report would read as this gate's" >&2; exit 17; }

[ -d "$ID_ROOT/.azure" ] && [ -d "$ID_ROOT/.gh-config" ] || {
  echo "REFUSING: NexusAI identity dirs missing under $ID_ROOT (.azure / .gh-config) — would inherit the caller's" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_ROOT/.azure"
export GH_CONFIG_DIR="$ID_ROOT/.gh-config"
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"

# 12 — tiers declared in both files: A TIER 2, B TIER 1, C TIER 2.
grep -q 'A (RD-619) is TIER 2' "$BRIEF" && grep -q 'B (RD-607) is TIER 1' "$BRIEF" && grep -q 'C (PR #31, RD-641 (ii)) is TIER 2' "$BRIEF" \
  && grep -q 'TARGET A — RD-619 (TIER 2' "$PROMPT_FILE" && grep -q 'TARGET B — RD-607 (TIER 1' "$PROMPT_FILE" \
  && grep -q 'TARGET C — PR #31, RD-641 (ii) (TIER 2' "$PROMPT_FILE" || {
  echo "REFUSING: brief and prompt do not both declare A 'TIER 2', B 'TIER 1', C 'TIER 2'" >&2; exit 12; }
head -1 "$PROMPT_FILE" | grep -q 'ultrathink' || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 13; }
grep -qF "$BRIEF" "$PROMPT_FILE" || { echo "REFUSING: prompt must name the brief path" >&2; exit 14; }
grep -qF "$G1_REPORT" "$BRIEF" || { echo "REFUSING: brief must name gate 1's report path (where RD-607's defect was found)" >&2; exit 14; }
grep -qF "$G5_REPORT" "$BRIEF" || { echo "REFUSING: brief must name gate 5's report path (the order-dependent verify)" >&2; exit 14; }
for S in $A_HEAD $B_HEAD $C_HEAD $MAIN_SHA $CUT_SHA $A_FIX $B_CHANGE; do
  grep -qF "$S" "$PROMPT_FILE" && grep -qF "$S" "$BRIEF" || { echo "REFUSING: prompt and brief must both name $S" >&2; exit 14; }
done
if grep -qF "$PH_SCTS" "$PROMPT_FILE" || grep -qF "$PH_SCNOTE" "$PROMPT_FILE"; then echo "REFUSING: the prompt carries a self-check placeholder — it belongs in the brief only" >&2; exit 14; fi
grep -qi 'MAIL YOUR VERDICT' "$PROMPT_FILE" && grep -q 'tuesday-agent@agentmail.to' "$PROMPT_FILE" \
  && grep -qF "$SUBJECT" "$PROMPT_FILE" && grep -qF "$SUBJECT" "$BRIEF" || {
  echo "REFUSING: prompt must say MAIL YOUR VERDICT and name tuesday-agent@agentmail.to; prompt and brief must carry the verdict subject" >&2; exit 15; }
grep -qF '/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env' "$PROMPT_FILE" || { echo "REFUSING: prompt must name the AgentMail key by ABSOLUTE path" >&2; exit 20; }
grep -q 'QUESTION: <topic>' "$PROMPT_FILE" && grep -qi 'no inbox routing line' "$PROMPT_FILE" || { echo "REFUSING: prompt must say QA/Datasec-NexusAI has no inbox routing line and how to ask (QUESTION: <topic>, proceed on the safest reading)" >&2; exit 20; }
WORDS="RD-619 RD-607 RD-641 PR%#31 M-619 M-607 M-dup N1 X1 S1 SIGKILL redis:7.4-alpine docker%lock csp-report data-source-test ai-test fail%open 35685088456 35683749970 rd641-known-failing-set-982a84f.txt NEW%must%be%none HS3 deploy.yml workflow_dispatch C-68 C-142 C-143 C-122 C-141 C-110 C-28 LEGITIMATE%SHAPES NOT%TESTED SEPARATELY%PER%TARGET QUEUE,%NEVER%TAKE%OVER merge-tree"
for w in $WORDS; do
  w="${w//%/ }"
  grep -q -- "$w" "$PROMPT_FILE" || { echo "REFUSING: prompt must carry '$w'" >&2; exit 19; }
done
grep -q 'RULED BY KAM, NOT YET IN AN ARTEFACT' "$BRIEF" || { echo "REFUSING: brief lacks the RULED BY KAM section" >&2; exit 19; }
grep -q '^## PRIOR ROUND' "$BRIEF" || { echo "REFUSING: brief lacks the PRIOR ROUND section" >&2; exit 19; }
grep -q '^## 2a. LEGITIMATE SHAPES' "$BRIEF" || { echo "REFUSING: brief lacks §2a LEGITIMATE SHAPES (RD-607's name check is a checker)" >&2; exit 19; }
if grep -qi 'backend/server\.js' "$PROMPT_FILE"; then
  echo "REFUSING: the prompt contains the literal server path — this agent would read as a FOREIGN SERVER to any argv-grep floor check (RD-591 c.37901). Describe it; do not name it." >&2; exit 24
fi

# 53 — the gate-4 lesson: per-step DEADLINE, HEARTBEAT every 2 minutes, abort at 5 minutes silent, server killed in a finally.
for FL in "$BRIEF" "$PROMPT_FILE"; do
  grep -q 'DEADLINE' "$FL" && grep -q 'HEARTBEAT' "$FL" && grep -q '2 minutes' "$FL" && grep -q '5 minutes' "$FL" && grep -q 'finally' "$FL" || {
    echo "REFUSING: $FL lacks the DEADLINE / HEARTBEAT rule (2 minutes, 5 minutes, finally) — gate 4 stalled ~70 min holding the lock" >&2; exit 53; }
done

# 58 — neither file may let the gate claim Node 24 fixes HS3 (the rate is unmeasured).
for FL in "$BRIEF" "$PROMPT_FILE"; do
  grep -q 'NOT claim that Node 24 fixes HS3' "$FL" || { echo "REFUSING: $FL lacks 'NOT claim that Node 24 fixes HS3'" >&2; exit 58; }
done
# 59 — gate-class lock tag (C-141), in both files.
for FL in "$BRIEF" "$PROMPT_FILE"; do
  grep -q 'qa-gate6-' "$FL" || { echo "REFUSING: $FL does not give the gate-class lock tag prefix qa-gate6- (C-141)" >&2; exit 59; }
done
# 60 — a red arm counts only if the mutant still parses, in both files.
for FL in "$BRIEF" "$PROMPT_FILE"; do
  grep -q 'node --check' "$FL" && grep -qi 'VOID' "$FL" || { echo "REFUSING: $FL lacks the parse-before-red rule (node --check; a non-parsing mutant is VOID)" >&2; exit 60; }
done
# 61 — the gate's trees are EXCLUSIVE to it, in both files.
for FL in "$BRIEF" "$PROMPT_FILE"; do
  grep -q 'EXCLUSIVE' "$FL" || { echo "REFUSING: $FL lacks the tree-exclusivity rule" >&2; exit 61; }
done

# 38 — the brief names ALL THREE negative-control seats; advisory if one is no longer running.
for P in $NEG_SEATS; do
  grep -q "\`$P\`" "$BRIEF" || { echo "REFUSING: brief does not name seat pid $P as a negative control" >&2; exit 38; }
  [ "$(ps -o comm= -p "$P" 2>/dev/null | sed 's#.*/##')" = "claude" ] || echo "NOTE: negative-control seat $P is not a running claude now — re-read the seats and update the brief's §7 before launch" >&2
done

# Advisory only: main moving changes C's merge ref and §6's forward-merge pairs.
M_ORIGIN="$(g ls-remote origin refs/heads/main 2>/dev/null | awk '{print $1}')"
[ "$M_ORIGIN" = "$MAIN_SHA" ] || echo "NOTE: origin main is now ${M_ORIGIN:-unreadable}, not ${MAIN_SHA:0:7} — C's PR CI ran against ${MAIN_SHA:0:7} and §6's pairs name it: re-measure / re-brief before launch" >&2

# 32 — the coordinator stamps the self-check (timestamp AND note) before launch. LAST, so --check shows every other guard.
if grep -qF "$PH_SCTS" "$BRIEF" || grep -qF "$PH_SCNOTE" "$BRIEF" \
   || ! grep -q '^SELF-CHECK: re-read end-to-end for contradictions | ' "$BRIEF" || ! grep -q '^Self-check note: ' "$BRIEF"; then
  echo "guards pass (6 7 8 18 22 35 50 54 55 56 57 25 31 39 10 17 11 12 13 14 15 20 19 24 53 58 59 60 61 38); self-check NOT stamped." >&2
  echo "REFUSING: the brief's SELF-CHECK line or Self-check note is unstamped — the coordinator re-reads end-to-end and stamps both before launch" >&2; exit 32
fi

if [ "$CHECK" = "1" ]; then
  echo "all guards pass:"
  echo "  A $A_HEAD at origin (18); base ${CUT_SHA:0:7} (7); chain f26c740 695ca5a, parents exact (8); five files, no product file (22, 54); counts $A_EXPECTED_TESTS/$A_EXPECTED_SUITES (35)"
  echo "  B $B_HEAD at origin (18); base A (7); chain 80d083b 9de358e c7dc9fd 8fa0791, parents exact incl. two merges (8); four files (22); counts $B_EXPECTED_TESTS/$B_EXPECTED_SUITES (35); harness identical to A (56); seven named limiters (57)"
  echo "  C $C_HEAD at origin and $C_PR_REF (18); base ${MAIN_SHA:0:7} (7, 8); three files, three '20'->'24' lines at 25/27/25 (22, 55); deploy.yml dispatch-only, no secrets (55); counts $C_EXPECTED_TESTS/$C_EXPECTED_SUITES (35)"
  echo "  per-commit file sets (50); $AUTH_FILE unchanged (25); evidence present (31); gate-5 floor instrument (39); report does not exist yet (17); seats $NEG_SEATS named (38)"
  echo "  AZURE_CONFIG_DIR=$AZURE_CONFIG_DIR  GH_CONFIG_DIR=$GH_CONFIG_DIR  CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR"
  echo "  tier (12); directive (13); brief+shas+gate-1/5 reports named (14); mail (15); key absolute + question route (20); names (19); no server path (24); deadline/heartbeat (53); no HS3 claim (58); qa-gate6- tag (59); parse-before-red (60); exclusive trees (61); self-check stamped (32)"
  exit 0
fi

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model claude-opus-5-5 "$(cat "$PROMPT_FILE")"
