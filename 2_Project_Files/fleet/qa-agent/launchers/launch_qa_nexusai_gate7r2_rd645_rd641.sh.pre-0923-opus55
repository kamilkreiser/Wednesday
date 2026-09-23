#!/bin/bash
# launch_qa_nexusai_gate7r2_rd645_rd641.sh — cross-project QA agent, ONE gate (gate 7 ROUND 2, 2026-09-23) on Datasec/NexusAI,
# TWO coupled targets:
#   A — RD-645 round 2 of 2 (TIER 1): rd-645-auth-limiter-mounted-s80i @ a1b524a, off aab3bf2; chain d05ec22 7759591 202770e
#       823c7fe 1e92f58 a1b524a. Round 2 changes no product file (202770e..a1b524a = cell file + counts).
#   B — RD-641 (i) (TIER 2, harness only): rd-641-harness-wildcard-bind-s80i @ ab54de1, off main c0788b1; chain 1bfc265 d0f04b6 ab54de1.
#   COUPLED: rd645's cells boot through rd395-server-harness, which takes reservePort from the test-server helper B changes (69).
#
# AUTHORITY: READY FOR QA from S80I (NexusAI-I): RD-645 r2 (session-tools/s80i/mail-26-ready645r2.WrFrCF, 01:40 AEST) and RD-641 (i)
# (mail-25-ready641.dhbQRH, 01:21 AEST), batched per Tuesday's 15:23Z mail. Scope C-146 / C-147; cap C-62. Merges: Tuesday's GO (C-127).
#
# PATTERN: launch_qa_nexusai_gate7_rd645.sh. CHANGES:
#   - two heads, both re-pinned by ls-remote (18); both chains + exact parents (8); both deltas (22); four counts (35).
#   - exit 67: 202770e..a1b524a touches no product file (server entry point blob identical).
#   - exit 68: B changes no product file (delta confined to __tests__/ + the counts file; server entry point blob identical).
#   - exit 69: the coupling premise (rd645 cells -> rd395 harness -> ./test-server) AND the counts-conflict premise (both heads
#     rewrite the counts file from the same base blob).
#   - exit 70: package-lock blob identical at base, main, A and B.
#   - exit 71: Tuesday's scoping — brief and prompt carry the NOT TESTED line verbatim; the prompt carries no evasion wording.
#   - exit 72: the drafter's four corrections carried: M-Gib+logout, runs at a1b524a (not 1e92f58), Linux leg --pull never /
#     --network none / offline install at ab54de1, the combined-tree re-run + C-57 regeneration.
#   - exit 38: negative-control seats NexusAI-I 8360 (%44), Vision 1613 (%41), Tuesday 3434 (%0) — round 1's 57419 / 45678 exited.
#   - exit 66 dropped (round 1's bad abbreviation is not in this round).
#   - exit 32: SELF-CHECK stamped by the coordinator — LAST guard. Placeholder comparands BUILT BY CONCATENATION.
#   - exit 24 carried: the prompt must not carry the literal server path (RD-591 c.37901).
#
# LAUNCH IT IN A TMUX PANE (cockpit.sh add 'QA/NexusAI-gate7r2' "bash '<this file>'"), NEVER nohup.
# Identity: exports NexusAI's OWN az/gh dirs (gh optional and READ-ONLY); CLAUDE_CONFIG_DIR pinned to Tuesday's project-local store.
# --check is READ-ONLY: git read verbs (cat-file, log, merge-base, diff, show, rev-parse, ls-remote, grep), grep, ps. No writes.
# ABSOLUTE PATHS ON PURPOSE. TRACKED in launchers/. Contains a legitimate `cd` (into the QA project, at exec).
# Usage: launch_qa_nexusai_gate7r2_rd645_rd641.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..72 a guard refused
set -u
CHECK=0
for a in "$@"; do
  case "$a" in
    --check) CHECK=1 ;;
    *) echo "unknown argument: $a" >&2; exit 2 ;;
  esac
done

PH_SCTS='@SELFCHECK''_TS@'
PH_SCNOTE='@SELFCHECK''_NOTE@'

QA_DIR='/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN'
TUE='/Volumes/KK_T9_External_HDD/TUESDAY'
BRIEF="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-23_nexusai-gate7r2-rd645-rd641.md"
PROMPT_FILE="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-23_nexusai-gate7r2-rd645-rd641.prompt.txt"
REPO='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files'
NX='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI'
EVID_I="$NX/session-tools/s80i"
R1_DIR="$QA_DIR/projects/nexusai/reports/2026-09-22-gate7-rd645"
R1_REPORT="$R1_DIR/report.md"
R1_FLOOR="$R1_DIR/evidence/qa-floorcount.py"
R1_FLOORLIB="$R1_DIR/evidence/qa-floorlib.sh"
G6_PROBE="$QA_DIR/projects/nexusai/reports/2026-09-22-gate6-rd619-rd607-pr31/evidence/probe-b.js"
G4_STALL="$QA_DIR/projects/nexusai/reports/2026-09-22-gate4-rd575-rd524r2/evidence/a3u-stall-evidence.txt"
H_TRACE="$NX/session-tools/s79h/rd641-trace-run.log"
REPORT="$QA_DIR/projects/nexusai/reports/2026-09-23-gate7r2-rd645-rd641/report.md"
ID_ROOT="${QA_IDENTITY_ROOT_OVERRIDE:-$NX/4_Credentials}"

BASE_SHA='aab3bf2dd72659b09713ccb3f0a8e4ad2560d852'   # A's base (merge-base with main)
MAIN_SHA='c0788b1017a20ea5d2d0b9c0e5837ee233830696'   # origin main at drafting; B's base
A_BRANCH='rd-645-auth-limiter-mounted-s80i'
A_HEAD="${QA_A_HEAD_OVERRIDE:-a1b524a9e532f98dd1ffd42f3dd1a3763525f998}"
A_R1='202770e467257a9ca6c5af6432dd72c68dc1210e'       # round 1's gated head
A_PROOF='1e92f58937ae14cba97b1c26bddfd31a4b71d9ce'    # where the builder's proof hold ran
A_CHAIN='a1b524a9e532f98dd1ffd42f3dd1a3763525f998
1e92f58937ae14cba97b1c26bddfd31a4b71d9ce
823c7fe359a9ba0d36ec14b96a991ceeddcdf446
202770e467257a9ca6c5af6432dd72c68dc1210e
7759591e77e3497b5edde867502c0f516b607582
d05ec2212f8427c17bd9f9a202c46c72d5fee7fe'
A_PARENTS='d05ec2212f8427c17bd9f9a202c46c72d5fee7fe aab3bf2dd72659b09713ccb3f0a8e4ad2560d852
7759591e77e3497b5edde867502c0f516b607582 d05ec2212f8427c17bd9f9a202c46c72d5fee7fe
202770e467257a9ca6c5af6432dd72c68dc1210e 7759591e77e3497b5edde867502c0f516b607582
823c7fe359a9ba0d36ec14b96a991ceeddcdf446 202770e467257a9ca6c5af6432dd72c68dc1210e
1e92f58937ae14cba97b1c26bddfd31a4b71d9ce 823c7fe359a9ba0d36ec14b96a991ceeddcdf446
a1b524a9e532f98dd1ffd42f3dd1a3763525f998 1e92f58937ae14cba97b1c26bddfd31a4b71d9ce'
B_BRANCH='rd-641-harness-wildcard-bind-s80i'
B_HEAD="${QA_B_HEAD_OVERRIDE:-ab54de151e3df23fe903aef374bac5691a165a06}"
B_FIX='1bfc265f5d416d773269fb2fbc4faf684b541d22'
B_PROOF='d0f04b6a55809fcff000e58d01267406d3b1a561'
B_CHAIN='ab54de151e3df23fe903aef374bac5691a165a06
d0f04b6a55809fcff000e58d01267406d3b1a561
1bfc265f5d416d773269fb2fbc4faf684b541d22'
B_PARENTS='1bfc265f5d416d773269fb2fbc4faf684b541d22 c0788b1017a20ea5d2d0b9c0e5837ee233830696
d0f04b6a55809fcff000e58d01267406d3b1a561 1bfc265f5d416d773269fb2fbc4faf684b541d22
ab54de151e3df23fe903aef374bac5691a165a06 d0f04b6a55809fcff000e58d01267406d3b1a561'

CELL_FILE='__tests__/rd645-auth-limiter-mounted.test.js'
SERVER_FILE='backend/server.js'
COUNTS_FILE='scripts/verify-expected-counts.json'
AUTH_FILE='backend/services/authEnforcement.js'
HELPER='__tests__/helpers/test-server.js'
HARNESS='__tests__/helpers/rd395-server-harness.js'
B_CELL='__tests__/rd641-reserved-port-binds-on-every-address.test.js'
A_EXPECTED_FILES="$CELL_FILE
$SERVER_FILE
$COUNTS_FILE"
B_EXPECTED_FILES="$HELPER
$B_CELL
$COUNTS_FILE"
MAIN_DELTA_FILES='.github/workflows/build.yml
.github/workflows/deploy.yml
.github/workflows/npm-audit.yml'
LIMITER_NAMES='ai
ai-test
auth
csp-report
data-source-test
general
setup'
ROUTE_OLD="app.post('/api/auth/login', async (req, res) => {"
ROUTE_NEW="app.post('/api/auth/login', authLimiter, async (req, res) => {"
LOCK_BLOB='906476350431e2ecb3c21070a25c64b1702c1aa8'
NEG_SEATS='8360 1613 3434'   # NexusAI-I (%44), Vision (%41), Tuesday (%0) at drafting 2026-09-23 01:52
SCOPE_LINE="Limiter-evasion via request headers: not run this round by the coordinator's scoping; the trust-proxy exposure is ticketed as RD-651."

SUBJECT='[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — gate 7 r2: RD-645 @ a1b524a + RD-641 @ ab54de1'

g() { git --no-optional-locks -C "$REPO" "$@"; }
sorted() { printf '%s\n' "$1" | sed '/^$/d' | sort; }
counts_at() { g show "$1:$COUNTS_FILE" 2>/dev/null | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d["tests"], d["suites"])' 2>/dev/null; }
files_of() { g diff --name-only "$1^" "$1" 2>/dev/null | sort; }   # vs FIRST parent
blob() { g rev-parse "$1:$2" 2>/dev/null; }

[ -d "$QA_DIR" ]      || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]       || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ] || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO/.git" ] || [ -f "$REPO/.git" ] || { echo "repo under test missing: $REPO" >&2; exit 5; }

# 6 — every pinned sha is a commit in the object store.
for S in $BASE_SHA $MAIN_SHA $A_CHAIN $B_CHAIN; do
  T="$(g cat-file -t "$S" 2>&1)"
  [ "$T" = "commit" ] || { echo "REFUSING: $S is not a commit in $REPO (got '$T') — this launcher never fetches" >&2; exit 6; }
done

# 7 — A: base is ancestor AND merge-base with main. B: main is its merge-base.
g merge-base --is-ancestor "$BASE_SHA" "$A_HEAD" 2>/dev/null || { echo "REFUSING: $BASE_SHA is not an ancestor of A $A_HEAD" >&2; exit 7; }
[ "$(g merge-base "$MAIN_SHA" "$A_HEAD" 2>/dev/null)" = "$BASE_SHA" ] || { echo "REFUSING: merge-base(main, A) is not ${BASE_SHA:0:7}" >&2; exit 7; }
[ "$(g merge-base "$MAIN_SHA" "$B_HEAD" 2>/dev/null)" = "$MAIN_SHA" ] || { echo "REFUSING: main ${MAIN_SHA:0:7} is not B's base (merge-base)" >&2; exit 7; }

# 8 — each chain exact; every parent list exact.
GOTC="$(g log --format=%H "${BASE_SHA}..${A_HEAD}" 2>&1)"
[ "$GOTC" = "$A_CHAIN" ] || { echo "REFUSING: ${BASE_SHA:0:7}..A is not exactly the commissioned chain. Got:" >&2; printf '%s\n' "$GOTC" >&2; exit 8; }
GOTC="$(g log --format=%H "${MAIN_SHA}..${B_HEAD}" 2>&1)"
[ "$GOTC" = "$B_CHAIN" ] || { echo "REFUSING: ${MAIN_SHA:0:7}..B is not exactly the commissioned chain. Got:" >&2; printf '%s\n' "$GOTC" >&2; exit 8; }
while IFS= read -r LINE; do
  [ -z "$LINE" ] && continue
  c="${LINE%% *}"; p="${LINE#* }"
  GOT="$(g log -1 --format='%H %P' "$c" 2>/dev/null)"
  [ "$GOT" = "$c $p" ] || { echo "REFUSING: parents of $c are '${GOT#* }', not '$p'" >&2; exit 8; }
done <<< "$A_PARENTS
$B_PARENTS"

# 18 — RE-PIN: both heads at origin, by ls-remote, read NOW.
for PAIR in "$A_BRANCH $A_HEAD" "$B_BRANCH $B_HEAD"; do
  BR="${PAIR%% *}"; H="${PAIR#* }"
  L="$(g ls-remote origin "refs/heads/$BR" 2>&1)"
  printf '%s\n' "$L" | grep -q "^${H}[[:space:]]refs/heads/${BR}\$" || {
    echo "REFUSING: $H is not at refs/heads/$BR on origin — that head moved or was never pushed; re-brief" >&2; printf '%s\n' "$L" >&2; exit 18; }
done

# 22 — each delta is EXACTLY the commissioned file set.
GOT="$(g diff --name-only "$BASE_SHA" "$A_HEAD" 2>/dev/null | sort)"
[ "$GOT" = "$(sorted "$A_EXPECTED_FILES")" ] || { echo "REFUSING: A's delta over ${BASE_SHA:0:7} is not the three commissioned files. Got:" >&2; printf '%s\n' "$GOT" >&2; exit 22; }
GOT="$(g diff --name-only "$MAIN_SHA" "$B_HEAD" 2>/dev/null | sort)"
[ "$GOT" = "$(sorted "$B_EXPECTED_FILES")" ] || { echo "REFUSING: B's delta over ${MAIN_SHA:0:7} is not the three commissioned files. Got:" >&2; printf '%s\n' "$GOT" >&2; exit 22; }

# 35 — counts: base/main 3924 225; A 3934 226; B 3927 226.
for PAIR in "$BASE_SHA 3924 225" "$MAIN_SHA 3924 225" "$A_HEAD 3934 226" "$B_HEAD 3927 226"; do
  S="${PAIR%% *}"; WANT="${PAIR#* }"
  CT="$(counts_at "$S")"
  [ "$CT" = "$WANT" ] || { echo "REFUSING: $COUNTS_FILE at ${S:0:7} reads '${CT:-unreadable}', not '$WANT'" >&2; exit 35; }
done

# 50 — per-commit file sets for the round-2 and B commits (vs FIRST parent).
[ "$(files_of 823c7fe359a9ba0d36ec14b96a991ceeddcdf446)" = "$CELL_FILE" ] || { echo "REFUSING: 823c7fe changes more than the cell file" >&2; exit 50; }
[ "$(files_of "$A_PROOF")" = "$CELL_FILE" ] || { echo "REFUSING: 1e92f58 changes more than the cell file" >&2; exit 50; }
[ "$(files_of "$A_HEAD")" = "$COUNTS_FILE" ] || { echo "REFUSING: A head is not counts-only" >&2; exit 50; }
[ "$(files_of "$B_FIX")" = "$(sorted "$HELPER
$B_CELL")" ] || { echo "REFUSING: 1bfc265 is not the helper + the new cell file" >&2; exit 50; }
[ "$(files_of "$B_PROOF")" = "$B_CELL" ] || { echo "REFUSING: d0f04b6 changes more than the rd641 cell file" >&2; exit 50; }
[ "$(files_of "$B_HEAD")" = "$COUNTS_FILE" ] || { echo "REFUSING: B head is not counts-only" >&2; exit 50; }

# 67 — round 2 changes no product file.
GOT="$(g diff --name-only "$A_R1" "$A_HEAD" 2>/dev/null | sort)"
[ "$GOT" = "$(sorted "$CELL_FILE
$COUNTS_FILE")" ] || { echo "REFUSING: 202770e..A is not the cell file + counts only. Got:" >&2; printf '%s\n' "$GOT" >&2; exit 67; }
[ -n "$(blob "$A_R1" "$SERVER_FILE")" ] && [ "$(blob "$A_R1" "$SERVER_FILE")" = "$(blob "$A_HEAD" "$SERVER_FILE")" ] || { echo "REFUSING: server entry point differs between 202770e and A" >&2; exit 67; }

# 68 — B changes no product file.
[ -n "$(blob "$MAIN_SHA" "$SERVER_FILE")" ] && [ "$(blob "$MAIN_SHA" "$SERVER_FILE")" = "$(blob "$B_HEAD" "$SERVER_FILE")" ] || { echo "REFUSING: server entry point differs between main and B" >&2; exit 68; }
if g diff --name-only "$MAIN_SHA" "$B_HEAD" 2>/dev/null | grep -v -E '^__tests__/' | grep -v -x -F "$COUNTS_FILE" | grep -q .; then
  echo "REFUSING: B touches a file outside __tests__/ and the counts file" >&2; exit 68; fi

# 62 / 63 / 57 / 25 — A's product change, carried from round 1, at the A head.
SD="$(g diff -U0 "$BASE_SHA" "$A_HEAD" -- "$SERVER_FILE" 2>/dev/null)"
[ -n "$SD" ] || { echo "REFUSING: no diff in the server entry point — guard 62 would be vacuous" >&2; exit 62; }
MINUS="$(printf '%s\n' "$SD" | grep -E '^-[^-]' | sed 's/^-//' | grep -v -E '^[[:space:]]*//' | sed '/^[[:space:]]*$/d')"
PLUS="$(printf '%s\n' "$SD" | grep -E '^\+[^+]' | sed 's/^+//' | grep -v -E '^[[:space:]]*//' | sed '/^[[:space:]]*$/d')"
[ "$MINUS" = "$ROUTE_OLD" ] && [ "$PLUS" = "$ROUTE_NEW" ] || {
  echo "REFUSING: the server entry point's non-comment change is not exactly the login route gaining authLimiter. Got -[$MINUS] +[$PLUS]" >&2; exit 62; }
SRC="$(g show "$A_HEAD:$SERVER_FILE" 2>/dev/null)"
BSRC="$(g show "$BASE_SHA:$SERVER_FILE" 2>/dev/null)"
[ -n "$SRC" ] && [ -n "$BSRC" ] || { echo "REFUSING: server entry point unreadable — guard 63 would be vacuous" >&2; exit 63; }
NAL="$(printf '%s\n' "$SRC" | grep -v -E '^[[:space:]]*//' | grep -c -w 'authLimiter')"
[ "$NAL" = "2" ] || { echo "REFUSING: authLimiter on $NAL non-comment lines at A, not 2" >&2; exit 63; }
opts() { printf '%s\n' "$1" | awk '/^const authLimiter = rateLimit\(_rlOpts\(.auth., \{/{f=1} f{print} f&&/^\}\)\);/{exit}'; }
OH="$(opts "$SRC")"; OB="$(opts "$BSRC")"
[ -n "$OH" ] && [ "$OH" = "$OB" ] || { echo "REFUSING: authLimiter's option block differs between base and A (or is unreadable)" >&2; exit 63; }
printf '%s\n' "$OH" | grep -q 'windowMs: 15 \* 60 \* 1000' && printf '%s\n' "$OH" | grep -q 'max: isDev ? 50 : 20' || {
  echo "REFUSING: authLimiter is not windowMs 15 min / max isDev ? 50 : 20 as briefed" >&2; exit 63; }
printf '%s\n' "$SRC" | grep -q "^const isDev = process.env.NODE_ENV === 'development';" || { echo "REFUSING: isDev is not NODE_ENV === 'development' at A" >&2; exit 63; }
NCALL="$(printf '%s\n' "$SRC" | grep -o 'rateLimit(' | wc -l | tr -d ' ')"
NAMES="$(printf '%s\n' "$SRC" | grep -o -E "rateLimit\(_rlOpts\('[a-z][a-z0-9-]*'" | sed -E "s/.*'([a-z0-9-]+)'/\1/" | sort)"
[ "$NCALL" = "7" ] && [ "$NAMES" = "$(sorted "$LIMITER_NAMES")" ] || { echo "REFUSING: A has $NCALL rateLimit( calls / names [$(printf '%s' "$NAMES" | tr '\n' ' ')] — expected seven" >&2; exit 57; }
ND="$(g diff "$BASE_SHA" "$A_HEAD" -- "$AUTH_FILE" 2>/dev/null | wc -l | tr -d ' ')"
[ "$ND" = "0" ] && [ "$(g cat-file -t "$A_HEAD:$AUTH_FILE" 2>/dev/null)" = "blob" ] || { echo "REFUSING: $AUTH_FILE changed or absent at A" >&2; exit 25; }

# 64 — main = base + the three workflow files only (the base control stands for main's backend).
GOT="$(g diff --name-only "$BASE_SHA" "$MAIN_SHA" 2>/dev/null | sort)"
[ "$GOT" = "$(sorted "$MAIN_DELTA_FILES")" ] || { echo "REFUSING: ${BASE_SHA:0:7}..${MAIN_SHA:0:7} is not exactly the three workflow files" >&2; exit 64; }

# 69 — the coupling premise and the counts-conflict premise.
g grep -q -F "require('./helpers/rd395-server-harness')" "$A_HEAD" -- "$CELL_FILE" 2>/dev/null || { echo "REFUSING: rd645 cells no longer boot through the rd395 harness — §5's coupling premise is gone; re-brief" >&2; exit 69; }
g grep -q -F "require('./test-server')" "$B_HEAD" -- "$HARNESS" 2>/dev/null || { echo "REFUSING: the rd395 harness no longer takes its port from ./test-server at B — re-brief §5" >&2; exit 69; }
[ "$(blob "$A_HEAD" "$HELPER")" = "$(blob "$MAIN_SHA" "$HELPER")" ] && [ "$(blob "$B_HEAD" "$HELPER")" != "$(blob "$MAIN_SHA" "$HELPER")" ] || { echo "REFUSING: helper blobs do not match the coupling premise (A = main's, B changed)" >&2; exit 69; }
[ "$(blob "$BASE_SHA" "$COUNTS_FILE")" = "$(blob "$MAIN_SHA" "$COUNTS_FILE")" ] && [ "$(blob "$A_HEAD" "$COUNTS_FILE")" != "$(blob "$B_HEAD" "$COUNTS_FILE")" ] || { echo "REFUSING: counts-conflict premise false (bases differ or heads agree)" >&2; exit 69; }

# 70 — package-lock identical everywhere (one node_modules serves every tree).
for S in $BASE_SHA $MAIN_SHA $A_HEAD $B_HEAD; do
  [ "$(blob "$S" package-lock.json)" = "$LOCK_BLOB" ] || { echo "REFUSING: package-lock at ${S:0:7} is not ${LOCK_BLOB:0:7}" >&2; exit 70; }
done

# 31 — builder evidence and prior-gate evidence on disk.
for f in "$EVID_I/mail-26-ready645r2.WrFrCF" "$EVID_I/mail-25-ready641.dhbQRH" "$EVID_I/expect-rd645-r2.txt" "$EVID_I/expect-rd641.txt" \
         "$EVID_I/rd645-r2-hold.sh" "$EVID_I/rd645r2-hold-run2.out" "$EVID_I/rd645r2-M-Gib.log" "$EVID_I/rd645r2-redis.json" \
         "$EVID_I/rd645r2-related.log" "$EVID_I/rd645r2-verify.log" "$EVID_I/rd641-hold-run3.out" "$EVID_I/rd641-linux-arms.sh" \
         "$EVID_I/rd641-linux-old.log" "$EVID_I/rd641-linux-container.log" "$EVID_I/rd641-verify.log" \
         "$EVID_I/rd641-failing-set-c0788b1.tests.txt" "$H_TRACE" "$R1_REPORT" "$G6_PROBE" "$G4_STALL"; do
  [ -s "$f" ] || { echo "REFUSING: evidence absent: $f" >&2; exit 31; }
done

# 39 — round 1's floor instrument, which the brief prescribes, is on disk and named.
[ -s "$R1_FLOOR" ] && [ -s "$R1_FLOORLIB" ] || { echo "REFUSING: round 1's floor instrument missing" >&2; exit 39; }
grep -qF "$R1_FLOOR" "$BRIEF" || { echo "REFUSING: brief does not name the floor instrument $R1_FLOOR" >&2; exit 39; }

grep -qF "$REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the report path $REPORT" >&2; exit 10; }
grep -qF "$REPORT" "$PROMPT_FILE" || { echo "REFUSING: prompt does not name the report path $REPORT" >&2; exit 10; }
[ ! -e "$REPORT" ] || { echo "REFUSING: $REPORT already exists — a stale report would read as this gate's" >&2; exit 17; }

[ -d "$ID_ROOT/.azure" ] && [ -d "$ID_ROOT/.gh-config" ] || {
  echo "REFUSING: NexusAI identity dirs missing under $ID_ROOT (.azure / .gh-config) — would inherit the caller's" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_ROOT/.azure"
export GH_CONFIG_DIR="$ID_ROOT/.gh-config"
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"

# 12 — tiers declared in both files.
grep -q 'RD-645 is TIER 1' "$BRIEF" && grep -q 'RD-641 (i) is TIER 2' "$BRIEF" \
  && grep -q 'TARGET A — RD-645 (TIER 1' "$PROMPT_FILE" && grep -q 'TARGET B — RD-641 (i) (TIER 2' "$PROMPT_FILE" || {
  echo "REFUSING: brief and prompt do not both declare RD-645 TIER 1 and RD-641 (i) TIER 2" >&2; exit 12; }
head -1 "$PROMPT_FILE" | grep -q 'ultrathink' || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 13; }
grep -qF "$BRIEF" "$PROMPT_FILE" || { echo "REFUSING: prompt must name the brief path" >&2; exit 14; }
grep -qF "$R1_REPORT" "$BRIEF" || { echo "REFUSING: brief must name round 1's report" >&2; exit 14; }
for S in $A_HEAD $BASE_SHA $MAIN_SHA $B_HEAD $A_PROOF $B_PROOF $B_FIX; do
  grep -qF "$S" "$PROMPT_FILE" && grep -qF "$S" "$BRIEF" || { echo "REFUSING: prompt and brief must both name $S" >&2; exit 14; }
done
if grep -qF "$PH_SCTS" "$PROMPT_FILE" || grep -qF "$PH_SCNOTE" "$PROMPT_FILE"; then echo "REFUSING: the prompt carries a self-check placeholder" >&2; exit 14; fi
grep -qi 'MAIL YOUR VERDICT' "$PROMPT_FILE" && grep -q 'tuesday-agent@agentmail.to' "$PROMPT_FILE" \
  && grep -qF "$SUBJECT" "$PROMPT_FILE" && grep -qF "$SUBJECT" "$BRIEF" || {
  echo "REFUSING: prompt must say MAIL YOUR VERDICT and name tuesday-agent@agentmail.to; both files must carry the verdict subject" >&2; exit 15; }
grep -qF '/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env' "$PROMPT_FILE" || { echo "REFUSING: prompt must name the AgentMail key by ABSOLUTE path" >&2; exit 20; }
grep -q 'QUESTION: <topic>' "$PROMPT_FILE" && grep -qi 'no inbox routing line' "$PROMPT_FILE" || { echo "REFUSING: prompt must carry the question route" >&2; exit 20; }
WORDS="RD-645 RD-641 C-146 C-147 C-62 M-645 M-Gib+logout G-1 G-2 G-3 G-4 SESSION_SECRET POSITIVE%CONTROL 70%x%401 authLimiter enforce entra-config verify-group microsoft%callback logout RD-607 redis:7.4-alpine node:24-alpine --pull%never --network%none OFFLINE docker%lock NAT%TRADE-OFF 20%password-login%attempts%per%15%minutes C-68 C-57 C-142 C-145 C-141 C-110 C-28 C-122 CI%NOT%RUN NOT%TESTED merge-tree COMBINED RD-651 QUEUE,%NEVER%TAKE%OVER"
for w in $WORDS; do
  w="${w//%/ }"
  grep -q -- "$w" "$PROMPT_FILE" || { echo "REFUSING: prompt must carry '$w'" >&2; exit 19; }
done
grep -q 'RULED BY KAM, NOT YET IN AN ARTEFACT' "$BRIEF" || { echo "REFUSING: brief lacks the RULED BY KAM section" >&2; exit 19; }
grep -q '^## PRIOR ROUND' "$BRIEF" || { echo "REFUSING: brief lacks the PRIOR ROUND section" >&2; exit 19; }
grep -q '^## 2a. LEGITIMATE SHAPES' "$BRIEF" || { echo "REFUSING: brief lacks §2a LEGITIMATE SHAPES" >&2; exit 19; }
grep -q '^## 5. THE COUPLING' "$BRIEF" || { echo "REFUSING: brief lacks §5 THE COUPLING" >&2; exit 19; }
if grep -qi 'backend/server\.js' "$PROMPT_FILE"; then
  echo "REFUSING: the prompt contains the literal server path (RD-591 c.37901). Describe it; do not name it." >&2; exit 24
fi

# 53 — DEADLINE / HEARTBEAT, both files.
for FL in "$BRIEF" "$PROMPT_FILE"; do
  grep -q 'DEADLINE' "$FL" && grep -q 'HEARTBEAT' "$FL" && grep -q '2 minutes' "$FL" && grep -q '5 minutes' "$FL" && grep -q 'finally' "$FL" || {
    echo "REFUSING: $FL lacks the DEADLINE / HEARTBEAT rule" >&2; exit 53; }
done
# 58 — C-146's scope and the NAT trade-off, both files.
for FL in "$BRIEF" "$PROMPT_FILE"; do
  grep -q 'POST /api/auth/login ONLY' "$FL" && grep -q 'NAT TRADE-OFF' "$FL" || { echo "REFUSING: $FL lacks C-146's scope or the NAT TRADE-OFF" >&2; exit 58; }
done
# 65 — the positive control, both files.
grep -q 'POSITIVE CONTROL FIRST' "$BRIEF" && grep -q '70 × 401' "$BRIEF" && grep -q 'POSITIVE CONTROL FIRST' "$PROMPT_FILE" && grep -q '70 x 401' "$PROMPT_FILE" || {
  echo "REFUSING: brief and prompt must both require the positive control first" >&2; exit 65; }
# 59 / 60 / 61 — lock tag, parse-before-red, exclusive trees.
for FL in "$BRIEF" "$PROMPT_FILE"; do
  grep -q 'qa-gate7r2-' "$FL" || { echo "REFUSING: $FL lacks the lock tag prefix qa-gate7r2-" >&2; exit 59; }
  grep -q 'node --check' "$FL" && grep -qi 'VOID' "$FL" || { echo "REFUSING: $FL lacks parse-before-red" >&2; exit 60; }
  grep -q 'EXCLUSIVE' "$FL" || { echo "REFUSING: $FL lacks tree exclusivity" >&2; exit 61; }
done

# 71 — Tuesday's scoping: the NOT TESTED line verbatim in both; no evasion wording in the prompt.
grep -qF "$SCOPE_LINE" "$BRIEF" && grep -qF "$SCOPE_LINE" "$PROMPT_FILE" || { echo "REFUSING: brief and prompt must both carry the scoping line verbatim" >&2; exit 71; }
grep -q "TUESDAY'S RULING" "$BRIEF" && grep -q 'supersedes' "$BRIEF" || { echo "REFUSING: brief must state Tuesday's ruling superseding the PRIOR ROUND's bypass item" >&2; exit 71; }
if grep -qi -E 'bypass|forwarded|spoof|forg' "$PROMPT_FILE"; then echo "REFUSING: the prompt carries evasion wording — out of scope this round" >&2; exit 71; fi

# 72 — the drafter's four corrections carried.
grep -q 'M-Gib+logout' "$BRIEF" && grep -q 'REQUIRED to redden' "$BRIEF" || { echo "REFUSING: brief lacks the required M-Gib+logout arm" >&2; exit 72; }
grep -q 'YOUR runs are at `a1b524a`' "$BRIEF" && grep -q 'YOUR runs are at `ab54de1`' "$BRIEF" || { echo "REFUSING: brief must put the gate's runs at the gated heads" >&2; exit 72; }
grep -q -- '--pull never --network none' "$BRIEF" && grep -q 'OFFLINE' "$BRIEF" || { echo "REFUSING: brief lacks the Linux leg's --pull never / --network none / offline install" >&2; exit 72; }
grep -q 'COMBINED' "$BRIEF" && grep -q 'C-57' "$BRIEF" && grep -q 'CONFLICT' "$BRIEF" || { echo "REFUSING: brief lacks the combined-tree run / predicted counts conflict / C-57" >&2; exit 72; }

# 38 — the brief names ALL negative-control seats; advisory if one is no longer running.
for P in $NEG_SEATS; do
  grep -q "\`$P\`" "$BRIEF" || { echo "REFUSING: brief does not name seat pid $P as a negative control" >&2; exit 38; }
  [ "$(ps -o comm= -p "$P" 2>/dev/null | sed 's#.*/##')" = "claude" ] || echo "NOTE: negative-control seat $P is not a running claude now — re-read the seats and update the brief's §7 before launch" >&2
done

M_ORIGIN="$(g ls-remote origin refs/heads/main 2>/dev/null | awk '{print $1}')"
[ "$M_ORIGIN" = "$MAIN_SHA" ] || echo "NOTE: origin main is now ${M_ORIGIN:-unreadable}, not ${MAIN_SHA:0:7} — §5's merge pair names it: re-brief before launch" >&2

# 32 — the coordinator stamps the self-check. LAST.
if grep -qF "$PH_SCTS" "$BRIEF" || grep -qF "$PH_SCNOTE" "$BRIEF" \
   || ! grep -q '^SELF-CHECK: re-read end-to-end for contradictions | ' "$BRIEF" || ! grep -q '^Self-check note: ' "$BRIEF"; then
  echo "guards pass (6 7 8 18 22 35 50 67 68 62 63 57 25 64 69 70 31 39 10 17 11 12 13 14 15 20 19 24 53 58 65 59 60 61 71 72 38); self-check NOT stamped." >&2
  echo "REFUSING: the brief's SELF-CHECK line or Self-check note is unstamped — the coordinator re-reads end-to-end and stamps both before launch" >&2; exit 32
fi

if [ "$CHECK" = "1" ]; then
  echo "all guards pass:"
  echo "  A RD-645 $A_HEAD and B RD-641 $B_HEAD at origin (18); chains + parents exact (8); deltas (22); counts (35); per-commit sets (50)"
  echo "  round 2 + B change no product file (67 68); A's product change as round 1 (62 63 57 25); main = base + workflows (64)"
  echo "  coupling + counts-conflict premises (69); package-lock ${LOCK_BLOB:0:7} everywhere (70); evidence (31); round-1 floor instrument (39)"
  echo "  report absent (17); scoping line (71); four corrections (72); seats $NEG_SEATS named (38)"
  echo "  AZURE_CONFIG_DIR=$AZURE_CONFIG_DIR  GH_CONFIG_DIR=$GH_CONFIG_DIR  CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR"
  exit 0
fi

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model claude-opus-5 "$(cat "$PROMPT_FILE")"
