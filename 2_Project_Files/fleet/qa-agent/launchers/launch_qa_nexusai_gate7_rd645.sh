#!/bin/bash
# launch_qa_nexusai_gate7_rd645.sh — cross-project QA agent, ONE gate (gate 7 of 2026-09-22) on Datasec/NexusAI:
#   TARGET — RD-645: rd-645-auth-limiter-mounted-s80i @ 202770e, off aab3bf2 (NOT c0788b1: c0788b1 = aab3bf2 + PR #31's three
#            workflow lines, and is not an ancestor of the head); chain d05ec22 -> 7759591 -> 202770e. TIER 1 (the password
#            sign-in's own rate limit, a security control). The head is KNOWN at drafting — re-read by ls-remote before launch (18).
#
# AUTHORITY: READY FOR QA from S80I (NexusAI-I), 2026-09-22T11:43:09Z (sent copy session-tools/s80i/mail-14-ready645.AQherw).
# Scope ruled by Tuesday as C-146 (login ONLY). Fixes gate 6 F-1. Merges after this gate are Tuesday's GO (C-127).
#
# PATTERN: launch_qa_nexusai_gate6_rd619_rd607_pr31.sh. CHANGES:
#   - one target; base aab3bf2 measured as the merge-base with origin main c0788b1.
#   - exit 8: every commit's EXACT parent list asserted.
#   - exit 62: the server entry point's ONLY non-comment change is the login route line gaining `authLimiter,`.
#   - exit 63: `authLimiter` appears exactly twice at the head (definition + the one mount); its option lines are byte-identical
#     to the base's (windowMs 15 min, max isDev ? 50 : 20); isDev is `=== 'development'`.
#   - exit 64: aab3bf2..c0788b1 is EXACTLY the three workflow files (main's backend = the base's; the positive control on the base
#     stands for main) — advisory NOTE if main moved.
#   - exit 57: seven rateLimit( calls, seven unique _rlOpts names (RD-607 intact at the head).
#   - exit 58: both files carry C-146's scope (login ONLY) and the NAT trade-off; exit 65: both carry the positive control
#     (70 x 401 on the base). exit 66: neither file carries the READY mail's unresolvable abbreviation 202770e472.
#   - exit 59: qa-gate7- lock tag. exit 60: parse-before-red. exit 61: tree exclusivity.
#   - exit 38: negative-control seats G 57419 (%36), I 8360 (%44), Tuesday 45678 (%0) — gate 6's H 29254 / Tuesday 63076 exited.
#   - exit 32: SELF-CHECK timestamp and note placeholders stamped by the coordinator before launch (LAST guard, so --check
#     shows every other guard first). Placeholder comparands are BUILT BY CONCATENATION so a sed of the placeholder text
#     cannot reach them.
#   - exit 24 carried: the prompt must not carry the literal server path (RD-591 c.37901).
#
# LAUNCH IT IN A TMUX PANE (cockpit.sh add 'QA/NexusAI-gate7' "bash '<this file>'"), NEVER nohup.
# Identity: exports NexusAI's OWN az/gh dirs (gh optional and READ-ONLY, for main's CI failing set); CLAUDE_CONFIG_DIR pinned to
# Tuesday's project-local store.
# --check is READ-ONLY: git read verbs (cat-file, log, merge-base, diff, show, rev-parse, ls-remote), grep, ps. No writes.
# ABSOLUTE PATHS ON PURPOSE. TRACKED in launchers/. Contains a legitimate `cd` (into the QA project, at exec).
# Usage: launch_qa_nexusai_gate7_rd645.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..66 a guard refused
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
BAD_ABBREV='202770e''472'

QA_DIR='/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN'
TUE='/Volumes/KK_T9_External_HDD/TUESDAY'
BRIEF="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-22_nexusai-gate7-rd645.md"
PROMPT_FILE="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-22_nexusai-gate7-rd645.prompt.txt"
REPO='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files'
NX='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI'
EVID_I="$NX/session-tools/s80i"
G6_DIR="$QA_DIR/projects/nexusai/reports/2026-09-22-gate6-rd619-rd607-pr31"
G6_REPORT="$G6_DIR/report.md"
G6_PROBE="$G6_DIR/evidence/probe-b.js"
G6_FLOOR="$G6_DIR/evidence/qa-floorcount.py"
G6_FLOORLIB="$G6_DIR/evidence/qa-floorlib.sh"
G4_STALL="$QA_DIR/projects/nexusai/reports/2026-09-22-gate4-rd575-rd524r2/evidence/a3u-stall-evidence.txt"
REPORT="$QA_DIR/projects/nexusai/reports/2026-09-22-gate7-rd645/report.md"
ID_ROOT="${QA_IDENTITY_ROOT_OVERRIDE:-$NX/4_Credentials}"

BASE_SHA='aab3bf2dd72659b09713ccb3f0a8e4ad2560d852'   # merge-base; main when RD-645 was cut
MAIN_SHA='c0788b1017a20ea5d2d0b9c0e5837ee233830696'   # origin main at drafting = BASE + PR #31 merge
T_BRANCH='rd-645-auth-limiter-mounted-s80i'
T_HEAD="${QA_T_HEAD_OVERRIDE:-202770e467257a9ca6c5af6432dd72c68dc1210e}"
T_FIX='d05ec2212f8427c17bd9f9a202c46c72d5fee7fe'
T_CELLS='7759591e77e3497b5edde867502c0f516b607582'
T_CHAIN='202770e467257a9ca6c5af6432dd72c68dc1210e
7759591e77e3497b5edde867502c0f516b607582
d05ec2212f8427c17bd9f9a202c46c72d5fee7fe'
# "<commit> <parent>" — the EXACT parent list of every commit in the chain.
T_PARENTS='d05ec2212f8427c17bd9f9a202c46c72d5fee7fe aab3bf2dd72659b09713ccb3f0a8e4ad2560d852
7759591e77e3497b5edde867502c0f516b607582 d05ec2212f8427c17bd9f9a202c46c72d5fee7fe
202770e467257a9ca6c5af6432dd72c68dc1210e 7759591e77e3497b5edde867502c0f516b607582'
CELL_FILE='__tests__/rd645-auth-limiter-mounted.test.js'
SERVER_FILE='backend/server.js'
COUNTS_FILE='scripts/verify-expected-counts.json'
AUTH_FILE='backend/services/authEnforcement.js'
T_EXPECTED_FILES="$CELL_FILE
$SERVER_FILE
$COUNTS_FILE"
T_FIX_FILES="$CELL_FILE
$SERVER_FILE"
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
T_EXPECTED_TESTS=3930
T_EXPECTED_SUITES=226
BASE_EXPECTED_TESTS=3924
BASE_EXPECTED_SUITES=225
NEG_SEATS='57419 8360 45678'   # NexusAI-G (%36), NexusAI-I (%44), Tuesday (%0) at drafting

SUBJECT='[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — gate 7: RD-645 @ 202770e'

g() { git --no-optional-locks -C "$REPO" "$@"; }
sorted() { printf '%s\n' "$1" | sed '/^$/d' | sort; }
counts_at() { g show "$1:$COUNTS_FILE" 2>/dev/null | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d["tests"], d["suites"])' 2>/dev/null; }
files_of() { g diff --name-only "$1^" "$1" 2>/dev/null | sort; }   # vs FIRST parent

[ -d "$QA_DIR" ]      || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]       || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ] || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO/.git" ] || [ -f "$REPO/.git" ] || { echo "repo under test missing: $REPO" >&2; exit 5; }

# 6 — every pinned sha is a commit in the object store.
for S in $BASE_SHA $MAIN_SHA $T_HEAD $T_FIX $T_CELLS; do
  T="$(g cat-file -t "$S" 2>&1)"
  [ "$T" = "commit" ] || { echo "REFUSING: $S is not a commit in $REPO (got '$T') — this launcher never fetches" >&2; exit 6; }
done

# 7 / 8 — base is ancestor AND merge-base (with the head, and with main); base..head is EXACTLY the chain; parents exact.
g merge-base --is-ancestor "$BASE_SHA" "$T_HEAD" 2>/dev/null || { echo "REFUSING: $BASE_SHA is not an ancestor of $T_HEAD" >&2; exit 7; }
[ "$(g merge-base "$MAIN_SHA" "$T_HEAD" 2>/dev/null)" = "$BASE_SHA" ] || { echo "REFUSING: merge-base(main ${MAIN_SHA:0:7}, head) is not ${BASE_SHA:0:7} — the brief's base is wrong" >&2; exit 7; }
GOTC="$(g log --format=%H "${BASE_SHA}..${T_HEAD}" 2>&1)"
[ "$GOTC" = "$T_CHAIN" ] || { echo "REFUSING: ${BASE_SHA:0:7}..head is not exactly the commissioned chain. Got:" >&2; printf '%s\n' "$GOTC" >&2; exit 8; }
while IFS= read -r LINE; do
  [ -z "$LINE" ] && continue
  c="${LINE%% *}"; p="${LINE#* }"
  GOT="$(g log -1 --format='%H %P' "$c" 2>/dev/null)"
  [ "$GOT" = "$c $p" ] || { echo "REFUSING: parents of $c are '${GOT#* }', not '$p'" >&2; exit 8; }
done <<< "$T_PARENTS"

# 18 — RE-PIN: the head at origin, by ls-remote, read NOW (immediately before launch).
L="$(g ls-remote origin "refs/heads/$T_BRANCH" 2>&1)"
printf '%s\n' "$L" | grep -q "^${T_HEAD}[[:space:]]refs/heads/${T_BRANCH}\$" || {
  echo "REFUSING: $T_HEAD is not at refs/heads/$T_BRANCH on origin — that head moved or was never pushed; re-brief" >&2; printf '%s\n' "$L" >&2; exit 18; }

# 22 — the delta over the base is EXACTLY the commissioned file set.
GOT="$(g diff --name-only "$BASE_SHA" "$T_HEAD" 2>/dev/null | sort)"
[ "$GOT" = "$(sorted "$T_EXPECTED_FILES")" ] || { echo "REFUSING: the delta over ${BASE_SHA:0:7} is not exactly the three commissioned files. Got:" >&2; printf '%s\n' "$GOT" >&2; exit 22; }

# 35 — counts read EXACTLY the builder's figures at the head and the base's at the base.
CT="$(counts_at "$T_HEAD")"
[ "$CT" = "$T_EXPECTED_TESTS $T_EXPECTED_SUITES" ] || { echo "REFUSING: $COUNTS_FILE at head reads '${CT:-unreadable}', not '$T_EXPECTED_TESTS $T_EXPECTED_SUITES'" >&2; exit 35; }
CT="$(counts_at "$BASE_SHA")"
[ "$CT" = "$BASE_EXPECTED_TESTS $BASE_EXPECTED_SUITES" ] || { echo "REFUSING: $COUNTS_FILE at base reads '${CT:-unreadable}', not '$BASE_EXPECTED_TESTS $BASE_EXPECTED_SUITES'" >&2; exit 35; }

# 50 — per-commit file sets (vs FIRST parent).
[ "$(files_of "$T_FIX")" = "$(sorted "$T_FIX_FILES")" ] || { echo "REFUSING: ${T_FIX:0:7} file set is not the cell file + the server entry point" >&2; exit 50; }
[ "$(files_of "$T_CELLS")" = "$CELL_FILE" ] || { echo "REFUSING: ${T_CELLS:0:7} changes more than the cell file" >&2; exit 50; }
[ "$(files_of "$T_HEAD")" = "$COUNTS_FILE" ] || { echo "REFUSING: ${T_HEAD:0:7} is not counts-only" >&2; exit 50; }

# 62 — the server entry point's ONLY non-comment change is the login route line gaining authLimiter.
SD="$(g diff -U0 "$BASE_SHA" "$T_HEAD" -- "$SERVER_FILE" 2>/dev/null)"
[ -n "$SD" ] || { echo "REFUSING: no diff in the server entry point — guard 62 would be vacuous" >&2; exit 62; }
MINUS="$(printf '%s\n' "$SD" | grep -E '^-[^-]' | sed 's/^-//' | grep -v -E '^[[:space:]]*//' | sed '/^[[:space:]]*$/d')"
PLUS="$(printf '%s\n' "$SD" | grep -E '^\+[^+]' | sed 's/^+//' | grep -v -E '^[[:space:]]*//' | sed '/^[[:space:]]*$/d')"
[ "$MINUS" = "$ROUTE_OLD" ] && [ "$PLUS" = "$ROUTE_NEW" ] || {
  echo "REFUSING: the server entry point's non-comment change is not exactly the login route gaining authLimiter. Got -[$MINUS] +[$PLUS]" >&2; exit 62; }

# 63 — authLimiter: exactly the definition + the one mount at the head; options byte-identical to the base; isDev === 'development'.
SRC="$(g show "$T_HEAD:$SERVER_FILE" 2>/dev/null)"
BSRC="$(g show "$BASE_SHA:$SERVER_FILE" 2>/dev/null)"
[ -n "$SRC" ] && [ -n "$BSRC" ] || { echo "REFUSING: server entry point unreadable — guard 63 would be vacuous" >&2; exit 63; }
NAL="$(printf '%s\n' "$SRC" | grep -v -E '^[[:space:]]*//' | grep -c -w 'authLimiter')"
[ "$NAL" = "2" ] || { echo "REFUSING: authLimiter appears on $NAL non-comment lines at the head, not 2 (definition + the one mount)" >&2; exit 63; }
opts() { printf '%s\n' "$1" | awk '/^const authLimiter = rateLimit\(_rlOpts\(.auth., \{/{f=1} f{print} f&&/^\}\)\);/{exit}'; }
OH="$(opts "$SRC")"; OB="$(opts "$BSRC")"
[ -n "$OH" ] && [ "$OH" = "$OB" ] || { echo "REFUSING: authLimiter's option block differs between base and head (or is unreadable) — the brief says unchanged" >&2; exit 63; }
printf '%s\n' "$OH" | grep -q 'windowMs: 15 \* 60 \* 1000' && printf '%s\n' "$OH" | grep -q 'max: isDev ? 50 : 20' || {
  echo "REFUSING: authLimiter is not windowMs 15 min / max isDev ? 50 : 20 as briefed" >&2; exit 63; }
printf '%s\n' "$SRC" | grep -q "^const isDev = process.env.NODE_ENV === 'development';" || { echo "REFUSING: isDev is not NODE_ENV === 'development' at the head — the brief's cap table is wrong" >&2; exit 63; }

# 64 — main = base + the three workflow files only (so the base control stands for main's backend).
GOT="$(g diff --name-only "$BASE_SHA" "$MAIN_SHA" 2>/dev/null | sort)"
[ "$GOT" = "$(sorted "$MAIN_DELTA_FILES")" ] || { echo "REFUSING: ${BASE_SHA:0:7}..${MAIN_SHA:0:7} is not exactly the three workflow files. Got:" >&2; printf '%s\n' "$GOT" >&2; exit 64; }

# 57 — RD-607 intact at the head: seven rateLimit( calls, all through _rlOpts('<name>', seven unique names.
NCALL="$(printf '%s\n' "$SRC" | grep -o 'rateLimit(' | wc -l | tr -d ' ')"
NAMES="$(printf '%s\n' "$SRC" | grep -o -E "rateLimit\(_rlOpts\('[a-z][a-z0-9-]*'" | sed -E "s/.*'([a-z0-9-]+)'/\1/" | sort)"
[ "$NCALL" = "7" ] && [ "$NAMES" = "$(sorted "$LIMITER_NAMES")" ] || {
  echo "REFUSING: the head's server entry point has $NCALL rateLimit( calls / names [$(printf '%s' "$NAMES" | tr '\n' ' ')] — expected seven: $(printf '%s' "$LIMITER_NAMES" | tr '\n' ' ')" >&2; exit 57; }

# 25 — authEnforcement.js byte-unchanged; with presence control.
ND="$(g diff "$BASE_SHA" "$T_HEAD" -- "$AUTH_FILE" 2>/dev/null | wc -l | tr -d ' ')"
[ "$ND" = "0" ] || { echo "REFUSING: $AUTH_FILE changed ($ND diff lines) — not commissioned; re-brief" >&2; exit 25; }
[ "$(g cat-file -t "$T_HEAD:$AUTH_FILE" 2>/dev/null)" = "blob" ] || { echo "REFUSING: $AUTH_FILE absent at head — guard 25 would be vacuous" >&2; exit 25; }

# 31 — builder evidence and prior-gate evidence on disk.
for f in "$EVID_I/mail-14-ready645.AQherw" "$EVID_I/expect-rd645.txt" "$EVID_I/rd645-proof-hold.sh" "$EVID_I/rd645-hold-run2.out" \
         "$EVID_I/rd645-clean1.log" "$EVID_I/rd645-m645.log" "$EVID_I/rd645-clean2.log" "$EVID_I/rd645-related.log" \
         "$EVID_I/rd645-verify.log" "$EVID_I/jc-rd645-prior.HditR9" \
         "$G6_REPORT" "$G6_PROBE" "$G4_STALL"; do
  [ -s "$f" ] || { echo "REFUSING: evidence absent: $f" >&2; exit 31; }
done

# 39 — gate 6's floor instrument, which the brief prescribes, is on disk and named.
[ -s "$G6_FLOOR" ] && [ -s "$G6_FLOORLIB" ] || { echo "REFUSING: gate 6's floor instrument missing: $G6_FLOOR / $G6_FLOORLIB" >&2; exit 39; }
grep -qF "$G6_FLOOR" "$BRIEF" || { echo "REFUSING: brief does not name the floor instrument $G6_FLOOR" >&2; exit 39; }

grep -qF "$REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the report path $REPORT" >&2; exit 10; }
grep -qF "$REPORT" "$PROMPT_FILE" || { echo "REFUSING: prompt does not name the report path $REPORT" >&2; exit 10; }
[ ! -e "$REPORT" ] || { echo "REFUSING: $REPORT already exists — a stale report would read as this gate's" >&2; exit 17; }

[ -d "$ID_ROOT/.azure" ] && [ -d "$ID_ROOT/.gh-config" ] || {
  echo "REFUSING: NexusAI identity dirs missing under $ID_ROOT (.azure / .gh-config) — would inherit the caller's" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_ROOT/.azure"
export GH_CONFIG_DIR="$ID_ROOT/.gh-config"
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"

# 12 — TIER 1 declared in both files.
grep -q 'RD-645 is TIER 1' "$BRIEF" && grep -q 'TARGET — RD-645 (TIER 1' "$PROMPT_FILE" || {
  echo "REFUSING: brief and prompt do not both declare RD-645 TIER 1" >&2; exit 12; }
head -1 "$PROMPT_FILE" | grep -q 'ultrathink' || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 13; }
grep -qF "$BRIEF" "$PROMPT_FILE" || { echo "REFUSING: prompt must name the brief path" >&2; exit 14; }
grep -qF "$G6_REPORT" "$BRIEF" || { echo "REFUSING: brief must name gate 6's report path (where F-1 was found)" >&2; exit 14; }
for S in $T_HEAD $BASE_SHA $MAIN_SHA $T_FIX $T_CELLS; do
  grep -qF "$S" "$PROMPT_FILE" && grep -qF "$S" "$BRIEF" || { echo "REFUSING: prompt and brief must both name $S" >&2; exit 14; }
done
if grep -qF "$PH_SCTS" "$PROMPT_FILE" || grep -qF "$PH_SCNOTE" "$PROMPT_FILE"; then echo "REFUSING: the prompt carries a self-check placeholder — it belongs in the brief only" >&2; exit 14; fi
grep -qi 'MAIL YOUR VERDICT' "$PROMPT_FILE" && grep -q 'tuesday-agent@agentmail.to' "$PROMPT_FILE" \
  && grep -qF "$SUBJECT" "$PROMPT_FILE" && grep -qF "$SUBJECT" "$BRIEF" || {
  echo "REFUSING: prompt must say MAIL YOUR VERDICT and name tuesday-agent@agentmail.to; prompt and brief must carry the verdict subject" >&2; exit 15; }
grep -qF '/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env' "$PROMPT_FILE" || { echo "REFUSING: prompt must name the AgentMail key by ABSOLUTE path" >&2; exit 20; }
grep -q 'QUESTION: <topic>' "$PROMPT_FILE" && grep -qi 'no inbox routing line' "$PROMPT_FILE" || { echo "REFUSING: prompt must say QA/Datasec-NexusAI has no inbox routing line and how to ask (QUESTION: <topic>, proceed on the safest reading)" >&2; exit 20; }
WORDS="RD-645 C-146 M-645 A1 A5 CTRL POSITIVE%CONTROL 70%x%401 authLimiter X-Forwarded-For trust%proxy%1 IPv6 parallel enforce entra-config verify-group microsoft%callback RD-607 redis:7.4-alpine docker%lock NAT%TRADE-OFF 20%password-login%attempts%per%15%minutes C-68 C-142 C-145 C-141 C-110 C-28 C-122 CI%NOT%RUN NOT%TESTED merge-tree QUEUE,%NEVER%TAKE%OVER"
for w in $WORDS; do
  w="${w//%/ }"
  grep -q -- "$w" "$PROMPT_FILE" || { echo "REFUSING: prompt must carry '$w'" >&2; exit 19; }
done
grep -q 'RULED BY KAM, NOT YET IN AN ARTEFACT' "$BRIEF" || { echo "REFUSING: brief lacks the RULED BY KAM section" >&2; exit 19; }
grep -q '^## PRIOR ROUND' "$BRIEF" || { echo "REFUSING: brief lacks the PRIOR ROUND section" >&2; exit 19; }
grep -q '^## 2a. LEGITIMATE SHAPES' "$BRIEF" || { echo "REFUSING: brief lacks §2a LEGITIMATE SHAPES (authLimiter is a checker)" >&2; exit 19; }
if grep -qi 'backend/server\.js' "$PROMPT_FILE"; then
  echo "REFUSING: the prompt contains the literal server path — this agent would read as a FOREIGN SERVER to any argv-grep floor check (RD-591 c.37901). Describe it; do not name it." >&2; exit 24
fi

# 53 — the gate-4 lesson: per-step DEADLINE, HEARTBEAT every 2 minutes, abort at 5 minutes silent, server killed in a finally.
for FL in "$BRIEF" "$PROMPT_FILE"; do
  grep -q 'DEADLINE' "$FL" && grep -q 'HEARTBEAT' "$FL" && grep -q '2 minutes' "$FL" && grep -q '5 minutes' "$FL" && grep -q 'finally' "$FL" || {
    echo "REFUSING: $FL lacks the DEADLINE / HEARTBEAT rule (2 minutes, 5 minutes, finally) — gate 4 stalled ~70 min holding the lock" >&2; exit 53; }
done

# 58 — C-146's scope (login ONLY) and the NAT trade-off, in both files.
for FL in "$BRIEF" "$PROMPT_FILE"; do
  grep -q 'POST /api/auth/login ONLY' "$FL" && grep -q 'NAT TRADE-OFF' "$FL" || {
    echo "REFUSING: $FL lacks C-146's scope ('POST /api/auth/login ONLY') or the NAT TRADE-OFF" >&2; exit 58; }
done
# 65 — the positive control on the base (gate 6's 70 x 401), in both files.
grep -q 'POSITIVE CONTROL FIRST' "$BRIEF" && grep -q '70 × 401' "$BRIEF" && grep -q 'POSITIVE CONTROL FIRST' "$PROMPT_FILE" && grep -q '70 x 401' "$PROMPT_FILE" || {
  echo "REFUSING: brief and prompt must both require the positive control first (70 x 401 on the base)" >&2; exit 65; }
# 66 — neither file pins the READY mail's unresolvable abbreviation (it is quoted in the brief only as an error, prefixed).
if grep -qF "$BAD_ABBREV" "$PROMPT_FILE"; then
  grep -q 'does not resolve' "$PROMPT_FILE" || { echo "REFUSING: the prompt carries $BAD_ABBREV without saying it does not resolve" >&2; exit 66; }
fi
if grep -qF "$BAD_ABBREV" "$BRIEF"; then
  grep -q 'That abbreviation does not resolve' "$BRIEF" || { echo "REFUSING: the brief carries $BAD_ABBREV without saying it does not resolve" >&2; exit 66; }
fi
# 59 — gate-class lock tag (C-141), in both files.
for FL in "$BRIEF" "$PROMPT_FILE"; do
  grep -q 'qa-gate7-' "$FL" || { echo "REFUSING: $FL does not give the gate-class lock tag prefix qa-gate7- (C-141)" >&2; exit 59; }
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
  [ "$(ps -o comm= -p "$P" 2>/dev/null | sed 's#.*/##')" = "claude" ] || echo "NOTE: negative-control seat $P is not a running claude now — re-read the seats and update the brief's §5 before launch" >&2
done

# Advisory only: main moving changes §4's merge pair and guard 64's premise.
M_ORIGIN="$(g ls-remote origin refs/heads/main 2>/dev/null | awk '{print $1}')"
[ "$M_ORIGIN" = "$MAIN_SHA" ] || echo "NOTE: origin main is now ${M_ORIGIN:-unreadable}, not ${MAIN_SHA:0:7} — §4's merge pair names it: re-measure / re-brief before launch" >&2

# 32 — the coordinator stamps the self-check (timestamp AND note) before launch. LAST, so --check shows every other guard.
if grep -qF "$PH_SCTS" "$BRIEF" || grep -qF "$PH_SCNOTE" "$BRIEF" \
   || ! grep -q '^SELF-CHECK: re-read end-to-end for contradictions | ' "$BRIEF" || ! grep -q '^Self-check note: ' "$BRIEF"; then
  echo "guards pass (6 7 8 18 22 35 50 62 63 64 57 25 31 39 10 17 11 12 13 14 15 20 19 24 53 58 65 66 59 60 61 38); self-check NOT stamped." >&2
  echo "REFUSING: the brief's SELF-CHECK line or Self-check note is unstamped — the coordinator re-reads end-to-end and stamps both before launch" >&2; exit 32
fi

if [ "$CHECK" = "1" ]; then
  echo "all guards pass:"
  echo "  RD-645 $T_HEAD at origin (18); base ${BASE_SHA:0:7} = merge-base with main ${MAIN_SHA:0:7} (7); chain d05ec22 7759591 202770e, parents exact (8)"
  echo "  three files (22); per-commit sets (50); counts $T_EXPECTED_TESTS/$T_EXPECTED_SUITES at head, $BASE_EXPECTED_TESTS/$BASE_EXPECTED_SUITES at base (35)"
  echo "  only non-comment change = login route gains authLimiter (62); authLimiter def + one mount, options unchanged, isDev === 'development' (63)"
  echo "  main = base + three workflow files (64); seven named limiters (57); $AUTH_FILE unchanged (25); evidence present (31); gate-6 floor instrument (39)"
  echo "  report does not exist yet (17); seats $NEG_SEATS named (38)"
  echo "  AZURE_CONFIG_DIR=$AZURE_CONFIG_DIR  GH_CONFIG_DIR=$GH_CONFIG_DIR  CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR"
  echo "  tier (12); directive (13); brief+shas+gate-6 report named (14); mail (15); key absolute + question route (20); names (19); no server path (24); deadline/heartbeat (53); C-146 + NAT (58); positive control (65); no bad abbrev (66); qa-gate7- tag (59); parse-before-red (60); exclusive trees (61); self-check stamped (32)"
  exit 0
fi

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model claude-opus-5-5 "$(cat "$PROMPT_FILE")"
