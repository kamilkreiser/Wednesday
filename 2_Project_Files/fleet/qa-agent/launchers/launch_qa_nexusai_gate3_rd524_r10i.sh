#!/bin/bash
# launch_qa_nexusai_gate3_rd524_r10i.sh — cross-project QA agent, ONE BATCHED gate (gate 3 of 2026-09-22) on Datasec/NexusAI:
#   TARGET A — RD-524 + RD-404 + RD-441: rd-524-404-441-s77f @ f422178, chain bdca588..f422178 =
#              faa9cbe (re-implementation of S59 on main) -> 07b9ce6 (fixture W + BACKLOG) -> f422178 (counts 3838/218). TIER 1.
#   TARGET B — RD-516 R10i split + repair: rd-516-ai-test-ssrf-s73, range b966634..91861ae =
#              bef8946 (split + F-5 comment) -> 91861ae (repair: name layer). THROUGH-CODE, test-only.
#              The range end is PINNED at 91861ae; the branch head may move above it (step 2) or merge (step 3).
#
# AUTHORITY: merge queue RD-516 -> RD-495 -> RD-525 -> RD-575 -> RD-524, each forward-merged and verified GREEN
# (C-68 / C-89); each merge is Tuesday's GO under C-127. Batching is Kam's standing rule of 2026-09-18
# (0_Brain/learnings/2026-09-18_minimise-gate-duplication-batch-them.md). Wednesday's ANSWER 2026-09-21T14:28:57Z:
# "step 3 proceeds on 91861ae once step 2 is GREEN; gate 3 reads it after".
#
# PATTERN: launch_qa_nexusai_gate2_rd495_rd525_rd575.sh (gate 2, 2026-09-21). CHANGES:
#   - Both targets fully pinned at drafting: no sha placeholder, no exit 9.
#   - exit 35: the counts file at A reads EXACTLY 3838 tests / 218 suites.
#   - exit 36: the carried tests vs S59's feac318 — helpers byte-identical, test files pure insertions (0 deletions).
#   - exit 40-45: B — range exactly bef8946 -> 91861ae, single-parent; exactly the two test files; 91861ae still reachable
#     at origin (branch head, or an ancestor of it, or of origin main); no collected skip at 91861ae WITH a control that
#     fires at b966634; the parked file sits under the ignored helpers path; C-130 + addendum present in CLARIFICATIONS.
#   - exit 32: the brief's SELF-CHECK timestamp and note placeholders must be stamped by the coordinator before launch.
#     The placeholder comparands are BUILT BY CONCATENATION ('@SELFCHECK''_TS@') so that a global sed of the placeholder
#     text in this file cannot also rewrite the guard (a previous launcher's guard was disarmed exactly that way).
#   - exit 24 carried: the prompt must not carry the literal server path (RD-591 c.37901).
#   - Expected-file variables are NEWLINE-separated; the file guards compare sorted line lists.
#
# LAUNCH IT IN A TMUX PANE (cockpit.sh add 'QA/NexusAI-gate3' "bash '<this file>'"), NEVER nohup.
# Identity: exports NexusAI's OWN az/gh dirs; CLAUDE_CONFIG_DIR pinned to Tuesday's project-local store.
# ABSOLUTE PATHS ON PURPOSE. TRACKED in launchers/. Contains a legitimate `cd` (into the QA project, at exec).
# Usage: launch_qa_nexusai_gate3_rd524_r10i.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..45 a guard refused
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
BRIEF="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-22_nexusai-gate3-rd524-r10i.md"
PROMPT_FILE="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-22_nexusai-gate3-rd524-r10i.prompt.txt"
REPO='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files'
CLARIF='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/1_Project_Definition/CLARIFICATIONS.md'
EVID_F='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/session-tools/s77f'
REPORT="$QA_DIR/projects/nexusai/reports/2026-09-22-gate3-rd524-r10i/report.md"
ID_ROOT="${QA_IDENTITY_ROOT_OVERRIDE:-/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/4_Credentials}"

MAIN_SHA='bdca588eced9c6a7ee6085b19e48765be3c8c07b'
# Target A
A_BRANCH='rd-524-404-441-s77f'
A_HEAD="${QA_HEAD_SHA_OVERRIDE:-f42217844bde4fd07952a3d1ec7f165d0957790d}"
A_CHAIN='f42217844bde4fd07952a3d1ec7f165d0957790d
07b9ce6854d036d541d05ba4a3ba97c17e8159c4
faa9cbe445d0cf932c48b784550a4c5383bd4ceb'
A_EXPECTED_FILES='BACKLOG.md
__tests__/helpers/persistent-temp-root.js
__tests__/helpers/rd441-banner-render.js
__tests__/rd404-sentinel-first-boot-vs-wipe.test.js
__tests__/rd441-persistence-alarm-reaches-dashboard.test.js
backend/jsonStorage.js
backend/server.js
scripts/verify-expected-counts.json
static/js/index.js'
A_EXPECTED_TESTS=3838
A_EXPECTED_SUITES=218
S59_HEAD='feac3187b83f483545f3f97f30455bb2ab608394'
A_IDENTICAL_TO_S59='__tests__/helpers/persistent-temp-root.js
__tests__/helpers/rd441-banner-render.js'
A_INSERT_ONLY_VS_S59='__tests__/rd404-sentinel-first-boot-vs-wipe.test.js
__tests__/rd441-persistence-alarm-reaches-dashboard.test.js'
# Target B
B_BRANCH='rd-516-ai-test-ssrf-s73'
B_START='b9666342f50646fbe44aefcdeeaa732dea10dccb'
B_END='91861aef2302ef8c8800a28a8977e490c021679a'
B_CHAIN='91861aef2302ef8c8800a28a8977e490c021679a
bef8946d621a41b1a70ee28bb0a12e942be4abda'
B_EXPECTED_FILES='__tests__/helpers/rd583-parked-NOT-RUN/rd516-r10i-scheme-port.test.js
__tests__/rd516-ai-test-ssrf.test.js'
B_PARKED='__tests__/helpers/rd583-parked-NOT-RUN/rd516-r10i-scheme-port.test.js'
SKIP_RE='^[[:space:]]*(test|it|describe)\.skip\(|^[[:space:]]*x(it|test|describe)\('

AUTH_FILE='backend/services/authEnforcement.js'
COUNTS_FILE='scripts/verify-expected-counts.json'
SUBJECT='[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — gate 3: RD-524 @ f422178 + RD-516 R10i split/repair (tier 1 / through-code)'

g() { git --no-optional-locks -C "$REPO" "$@"; }
sorted() { printf '%s\n' "$1" | sed '/^$/d' | sort; }

[ -d "$QA_DIR" ]      || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]       || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ] || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO/.git" ] || [ -f "$REPO/.git" ] || { echo "repo under test missing: $REPO" >&2; exit 5; }

# 6 — every pinned sha is a commit in the object store.
for S in $MAIN_SHA $A_HEAD $S59_HEAD $B_START $B_END; do
  T="$(g cat-file -t "$S" 2>&1)"
  [ "$T" = "commit" ] || { echo "REFUSING: $S is not a commit in $REPO (got '$T')" >&2; exit 6; }
done

# 7 / 8 — A: main is the base (ancestor AND merge-base), and bdca588..A is EXACTLY the three-commit chain, in order.
g merge-base --is-ancestor "$MAIN_SHA" "$A_HEAD" 2>/dev/null || { echo "REFUSING: main $MAIN_SHA is not an ancestor of A $A_HEAD" >&2; exit 7; }
[ "$(g merge-base "$MAIN_SHA" "$A_HEAD" 2>/dev/null)" = "$MAIN_SHA" ] || { echo "REFUSING: merge-base(main, A) is not $MAIN_SHA" >&2; exit 7; }
GOTC="$(g rev-list "${MAIN_SHA}..${A_HEAD}" 2>&1)"
[ "$GOTC" = "$A_CHAIN" ] || { echo "REFUSING: ${MAIN_SHA:0:7}..A is not exactly faa9cbe -> 07b9ce6 -> f422178. Got:" >&2; printf '%s\n' "$GOTC" >&2; exit 8; }
NM="$(g rev-list --merges --count "${MAIN_SHA}..${A_HEAD}" 2>&1)"
[ "$NM" = "0" ] || { echo "REFUSING: A's chain contains $NM merge commit(s) — not the shape commissioned" >&2; exit 8; }

# 18 — A's head at origin, by ls-remote.
L="$(g ls-remote origin "$A_BRANCH" 2>&1)"
printf '%s\n' "$L" | grep -q "^${A_HEAD}[[:space:]]refs/heads/${A_BRANCH}\$" || {
  echo "REFUSING: $A_HEAD is not at refs/heads/$A_BRANCH on origin — that head moved or was never pushed" >&2; printf '%s\n' "$L" >&2; exit 18; }

# 22 — A: EXACTLY the nine commissioned files across bdca588..A.
GOT="$(g diff --name-only "$MAIN_SHA" "$A_HEAD" 2>/dev/null | sort)"
[ "$GOT" = "$(sorted "$A_EXPECTED_FILES")" ] || { echo "REFUSING: A's range is not exactly the nine commissioned files. Got:" >&2; printf '%s\n' "$GOT" >&2; exit 22; }

# 25 — authEnforcement.js byte-unchanged on A and across B's range, with presence control.
for PAIR in "$MAIN_SHA $A_HEAD" "$B_START $B_END"; do
  set -- $PAIR
  ND="$(g diff "$1" "$2" -- "$AUTH_FILE" 2>/dev/null | wc -l | tr -d ' ')"
  [ "$ND" = "0" ] || { echo "REFUSING: $AUTH_FILE changed between $1 and $2 ($ND diff lines) — not commissioned; re-brief" >&2; exit 25; }
  [ "$(g cat-file -t "$2:$AUTH_FILE" 2>/dev/null)" = "blob" ] || { echo "REFUSING: $AUTH_FILE absent at $2 — guard 25 would be vacuous" >&2; exit 25; }
done
set --

# 35 — the counts file at A reads EXACTLY the builder's figure.
CJ="$(g show "${A_HEAD}:${COUNTS_FILE}" 2>/dev/null)"
CT="$(printf '%s' "$CJ" | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d["tests"], d["suites"])' 2>/dev/null)"
[ "$CT" = "$A_EXPECTED_TESTS $A_EXPECTED_SUITES" ] || { echo "REFUSING: $COUNTS_FILE at A reads '${CT:-unreadable}', not '$A_EXPECTED_TESTS $A_EXPECTED_SUITES'" >&2; exit 35; }

# 36 — the carried tests vs S59's feac318: helpers byte-identical; test files are pure insertions.
while IFS= read -r P; do
  [ -z "$P" ] && continue
  BA="$(g rev-parse "${A_HEAD}:$P" 2>/dev/null)"; BS="$(g rev-parse "${S59_HEAD}:$P" 2>/dev/null)"
  [ -n "$BA" ] && [ "$BA" = "$BS" ] || { echo "REFUSING: $P is not byte-identical to S59's feac318 (A '$BA', S59 '$BS')" >&2; exit 36; }
done <<< "$A_IDENTICAL_TO_S59"
while IFS= read -r P; do
  [ -z "$P" ] && continue
  NS="$(g diff --numstat "$S59_HEAD" "$A_HEAD" -- "$P" 2>/dev/null)"
  ADDS="$(printf '%s' "$NS" | awk '{print $1}')"; DELS="$(printf '%s' "$NS" | awk '{print $2}')"
  [ -n "$ADDS" ] && [ "$ADDS" -gt 0 ] 2>/dev/null && [ "$DELS" = "0" ] || { echo "REFUSING: $P vs feac318 is not a pure insertion (numstat '$NS')" >&2; exit 36; }
done <<< "$A_INSERT_ONLY_VS_S59"

# 40 — B's range end is still reachable at origin: the branch head IS 91861ae, or 91861ae is an ancestor of the branch
#      head (step 2 pushed a forward merge) or of origin main (step 3 merged). The launcher never fetches: if origin's
#      head is not in the local object store, it refuses rather than guess.
B_ORIGIN="$(g ls-remote origin "$B_BRANCH" 2>/dev/null | awk '{print $1}')"
M_ORIGIN="$(g ls-remote origin main 2>/dev/null | awk '{print $1}')"
B_STATE=''
if [ "$B_ORIGIN" = "$B_END" ]; then
  B_STATE="branch head IS ${B_END:0:7}"
elif [ -n "$B_ORIGIN" ] && [ "$(g cat-file -t "$B_ORIGIN" 2>/dev/null)" = "commit" ] && g merge-base --is-ancestor "$B_END" "$B_ORIGIN" 2>/dev/null; then
  B_STATE="branch head ${B_ORIGIN:0:7} is ABOVE ${B_END:0:7} (forward merge pushed) — the gate still reads ${B_END:0:7}"
elif [ -n "$M_ORIGIN" ] && [ "$(g cat-file -t "$M_ORIGIN" 2>/dev/null)" = "commit" ] && g merge-base --is-ancestor "$B_END" "$M_ORIGIN" 2>/dev/null; then
  B_STATE="${B_END:0:7} is MERGED into origin main ${M_ORIGIN:0:7} (branch head '${B_ORIGIN:-deleted}') — the gate still reads ${B_END:0:7}"
else
  echo "REFUSING: $B_END is not origin's $B_BRANCH head, not an ancestor of it ('${B_ORIGIN:-absent}'), and not an ancestor of origin main ('${M_ORIGIN:-unreadable}') — or origin's head is not in the local object store (this launcher never fetches). Re-read before launching." >&2; exit 40
fi

# 41 — B: range EXACTLY bef8946 -> 91861ae, no merges, each single-parent.
GOTB="$(g rev-list "${B_START}..${B_END}" 2>&1)"
[ "$GOTB" = "$B_CHAIN" ] || { echo "REFUSING: ${B_START:0:7}..${B_END:0:7} is not exactly bef8946 -> 91861ae. Got:" >&2; printf '%s\n' "$GOTB" >&2; exit 41; }
[ "$(g rev-list --merges --count "${B_START}..${B_END}" 2>&1)" = "0" ] || { echo "REFUSING: B's range contains a merge commit" >&2; exit 41; }

# 42 — B: EXACTLY the two test files; no product, static or scripts file.
GOTBF="$(g diff --name-only "$B_START" "$B_END" 2>/dev/null | sort)"
[ "$GOTBF" = "$(sorted "$B_EXPECTED_FILES")" ] || { echo "REFUSING: B's range is not exactly the two commissioned test files. Got:" >&2; printf '%s\n' "$GOTBF" >&2; exit 42; }

# 43 — no collected skip at 91861ae, with a control that must fire at b966634 (the skip the split removed).
N_END="$(g grep -nE "$SKIP_RE" "$B_END" -- __tests__ ':(exclude)__tests__/helpers' 2>/dev/null | wc -l | tr -d ' ')"
N_CTL="$(g grep -nE "$SKIP_RE" "$B_START" -- __tests__ ':(exclude)__tests__/helpers' 2>/dev/null | wc -l | tr -d ' ')"
[ "$N_CTL" -ge 1 ] 2>/dev/null || { echo "REFUSING: the skip search found nothing at $B_START, where R10i's test.skip is known to be — the instrument is blind (guard 43 would be vacuous)" >&2; exit 43; }
[ "$N_END" = "0" ] || { echo "REFUSING: $N_END collected skip form(s) at $B_END — the split claimed none" >&2; g grep -nE "$SKIP_RE" "$B_END" -- __tests__ ':(exclude)__tests__/helpers' >&2; exit 43; }

# 44 — the parked file exists at 91861ae under the helpers path, and jest's config ignores that path.
[ "$(g cat-file -t "${B_END}:${B_PARKED}" 2>/dev/null)" = "blob" ] || { echo "REFUSING: parked file absent at $B_END: $B_PARKED" >&2; exit 44; }
IGN="$(g show "${B_END}:package.json" 2>/dev/null | python3 -c 'import json,sys; print("\n".join(json.load(sys.stdin).get("jest",{}).get("testPathIgnorePatterns",[])))' 2>/dev/null)"
printf '%s\n' "$IGN" | grep -qxF '/__tests__/helpers/' || { echo "REFUSING: package.json jest.testPathIgnorePatterns at $B_END does not contain '/__tests__/helpers/' — the parked file may be collected" >&2; exit 44; }

# 45 — C-130 and its addendum are in the NexusAI clarifications file (read-only).
[ -s "$CLARIF" ] || { echo "REFUSING: CLARIFICATIONS.md missing: $CLARIF" >&2; exit 45; }
grep -qF '**C-130. ' "$CLARIF" && grep -qF 'ADDENDUM 2026-09-21 (S77F) — C-130' "$CLARIF" || { echo "REFUSING: C-130 or its S77F addendum not found in $CLARIF" >&2; exit 45; }

# 31 — builder evidence on disk.
for f in "$EVID_F/mail-07-ready-rd524.txt" "$EVID_F/expect-rd524.txt" "$EVID_F/rd524-proof-hold.sh" "$EVID_F/rd524-proof-hold.log" \
         "$EVID_F/rd524-R0.log" "$EVID_F/rd524-M1.log" "$EVID_F/rd524-M2.log" "$EVID_F/rd524-full-verify.log" \
         "$EVID_F/mail-05-status.txt" "$EVID_F/mail-06-question.txt" "$EVID_F/expect-rd516-split.txt" "$EVID_F/rd516-split-hold.sh" \
         "$EVID_F/rd516-split-hold-run1-bef8946.log" "$EVID_F/rd516-split-hold.log"; do
  [ -s "$f" ] || { echo "REFUSING: builder evidence absent: $f" >&2; exit 31; }
done

grep -qF "$REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the report path $REPORT" >&2; exit 10; }
[ ! -e "$REPORT" ] || { echo "REFUSING: $REPORT already exists — a stale report would read as this gate's" >&2; exit 17; }

[ -d "$ID_ROOT/.azure" ] && [ -d "$ID_ROOT/.gh-config" ] || {
  echo "REFUSING: NexusAI identity dirs missing under $ID_ROOT (.azure / .gh-config) — would inherit the caller's" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_ROOT/.azure"
export GH_CONFIG_DIR="$ID_ROOT/.gh-config"
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"

grep -qi 'TIER 1' "$BRIEF" && grep -qi 'TIER 1' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt do not both declare 'TIER 1'" >&2; exit 12; }
grep -q 'THROUGH-CODE' "$BRIEF" && grep -q 'THROUGH-CODE' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt do not both declare B 'THROUGH-CODE'" >&2; exit 12; }
head -1 "$PROMPT_FILE" | grep -q 'ultrathink' || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 13; }
grep -qF "$BRIEF" "$PROMPT_FILE" || { echo "REFUSING: prompt must name the brief path" >&2; exit 14; }
for S in $A_HEAD $MAIN_SHA $B_START $B_END; do
  grep -qF "$S" "$PROMPT_FILE" && grep -qF "$S" "$BRIEF" || { echo "REFUSING: prompt and brief must both name $S" >&2; exit 14; }
done
if grep -qF "$PH_SCTS" "$PROMPT_FILE" || grep -qF "$PH_SCNOTE" "$PROMPT_FILE"; then echo "REFUSING: the prompt carries a self-check placeholder — it belongs in the brief only" >&2; exit 14; fi
grep -qi 'MAIL YOUR VERDICT' "$PROMPT_FILE" && grep -q 'tuesday-agent@agentmail.to' "$PROMPT_FILE" \
  && grep -qF "$SUBJECT" "$PROMPT_FILE" && grep -qF "$SUBJECT" "$BRIEF" || {
  echo "REFUSING: prompt must say MAIL YOUR VERDICT and name tuesday-agent@agentmail.to; prompt and brief must carry the verdict subject" >&2; exit 15; }
grep -qF '/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env' "$PROMPT_FILE" || { echo "REFUSING: prompt must name the AgentMail key by ABSOLUTE path" >&2; exit 20; }
WORDS="RD-524 RD-404 RD-441 RD-516 R10i B7 F4 M1 M2 M-a M-b checkEndpointName collectPriorStateEvidence /api/status/persistence RD-612 C-130 merge-tree NOT%TESTED SEPARATELY%PER%TARGET"
for w in $WORDS; do
  w="${w//%/ }"
  grep -q -- "$w" "$PROMPT_FILE" || { echo "REFUSING: prompt must carry '$w'" >&2; exit 19; }
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

# Advisory only (not a guard): main moving is expected while the queue drains; A is defined against bdca588.
[ "$M_ORIGIN" = "$MAIN_SHA" ] || echo "NOTE: origin main is now ${M_ORIGIN:-unreadable}, not ${MAIN_SHA:0:7} — A's range is still against ${MAIN_SHA:0:7}; the gate reports main three times and merge-trees A against the new main" >&2

if [ "$CHECK" = "1" ]; then
  echo "all guards pass:"
  echo "  A $A_HEAD at origin (18); base ${MAIN_SHA:0:7} ancestor + merge-base (7); chain exactly faa9cbe 07b9ce6 f422178, no merges (8); nine files (22)"
  echo "  A counts $A_EXPECTED_TESTS/$A_EXPECTED_SUITES (35); carried tests vs feac318: helpers identical, tests insert-only (36)"
  echo "  B ${B_START:0:7}..${B_END:0:7} exactly bef8946 91861ae (41); two test files (42); $B_STATE (40)"
  echo "  B collected skips 0 at ${B_END:0:7}, control $N_CTL at ${B_START:0:7} (43); parked file under ignored helpers path (44); C-130 + addendum present (45)"
  echo "  $AUTH_FILE byte-unchanged on A and across B, with presence control (25)"
  echo "  builder evidence present (31); this gate's report does not exist yet (17)"
  echo "  AZURE_CONFIG_DIR=$AZURE_CONFIG_DIR  GH_CONFIG_DIR=$GH_CONFIG_DIR  CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR"
  echo "  tier (12); directive (13); brief+shas named, no placeholder in prompt (14); mail (15); key absolute (20); names (19); no server path (24); self-check stamped (32)"
  exit 0
fi

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model claude-opus-5-5 "$(cat "$PROMPT_FILE")"
