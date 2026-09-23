#!/bin/bash
# launch_qa_nexusai_gate4_rd575_rd524r2.sh — cross-project QA agent, ONE BATCHED gate (gate 4 of 2026-09-22) on Datasec/NexusAI:
#   TARGET A — RD-575: rd-575-purge-reaches-attachments-s76e @ 6a32426 = forward merge, parents EXACTLY bcb438d (E's head)
#              + main 982a84f. Chain 982a84f..6a32426 = 04253fb -> 4c0fe45 -> 481315f -> bcb438d -> 6a32426. TIER 1.
#   TARGET B — RD-524 (+RD-404 +RD-441) ROUND 2 of 2: rd-524-404-441-s77f @ $B_HEAD = S77F's forward merge of main onto
#              the round-2 fix 3931e2b (test-only, on round 1's f422178). NARROW RE-GATE (gate-3 report §6.5).
#              B_HEAD DID NOT EXIST AT DRAFTING. It is REQUIRED from the environment at launch (exit 9 if unset).
#
# AUTHORITY: merge queue RD-575 -> RD-524, each forward-merged and verified GREEN (C-68 / C-89 / C-57); each merge is
# Tuesday's GO under C-127. Batching is Kam's standing rule of 2026-09-18
# (0_Brain/learnings/2026-09-18_minimise-gate-duplication-batch-them.md). Round cap C-62 for B.
#
# PATTERN: launch_qa_nexusai_gate3_rd524_r10i.sh (gate 3) + gate 2's unpinned-head handling. CHANGES:
#   - B_HEAD comes from the ENVIRONMENT, never a default. PIN IT, immediately before launch, from
#       git -C '<repo>' ls-remote origin rd-524-404-441-s77f
#     never from a mail, then write the same sha into the brief AND the prompt (they carry the placeholder @B_HEAD@):
#       sed -i '' "s/@B_HEAD@/<sha>/g" '<brief>' '<prompt>'
#     and launch:  B_HEAD=<sha> bash '<this file>'
#     The placeholder comparand below is BUILT BY CONCATENATION ('@B''_HEAD@'), so a sed of the placeholder text that
#     reaches this file cannot rewrite the guard (a previous launcher's guard was disarmed exactly that way).
#   - Without --check, an unset B_HEAD refuses FIRST (exit 9), before any other guard. With --check, every guard that does
#     not need B_HEAD runs first and reports, and THEN exit 9 refuses — so a --check before the pin still proves A.
#   - exit 26/27: A is the merge claimed (parents EXACTLY bcb438d + 982a84f); 36/37: the merge-only claim (lane files at
#     A byte-identical to bcb438d) and the revert source (the three product files at 982a84f == 792fda0's).
#   - exit 41-47: B — the fix is one test-only commit on f422178; B_HEAD's shape, files, counts, and its product lines
#     equal round 1's (so gate 3's carried results stay valid).
#   - exit 38: the brief names BOTH live seats as negative controls; 39: gate 3's sequencer (QA_NM form) is on disk.
#   - exit 32: the brief's SELF-CHECK timestamp and note placeholders must be stamped by the coordinator before launch.
#   - exit 24 carried: the prompt must not carry the literal server path (RD-591 c.37901).
#
# LAUNCH IT IN A TMUX PANE (cockpit.sh add 'QA/NexusAI-gate4' "B_HEAD=<sha> bash '<this file>'"), NEVER nohup.
# Identity: exports NexusAI's OWN az/gh dirs; CLAUDE_CONFIG_DIR pinned to Tuesday's project-local store.
# ABSOLUTE PATHS ON PURPOSE. TRACKED in launchers/. Contains a legitimate `cd` (into the QA project, at exec).
# Usage: B_HEAD=<40-hex> launch_qa_nexusai_gate4_rd575_rd524r2.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..47 a guard refused
set -u
CHECK=0
for a in "$@"; do
  case "$a" in
    --check) CHECK=1 ;;
    *) echo "unknown argument: $a" >&2; exit 2 ;;
  esac
done

# Placeholder comparands, BUILT so that no sed of the placeholder text can reach them.
PH_BHEAD='@B''_HEAD@'
PH_SCTS='@SELFCHECK''_TS@'
PH_SCNOTE='@SELFCHECK''_NOTE@'

# ─── THE ONE VALUE STILL TO PIN: from the environment only ─────────────────────────────────────────────────────────────
B_HEAD="${B_HEAD:-}"
B_PIN_ERR=''
if [ -z "$B_HEAD" ] || [ "$B_HEAD" = "$PH_BHEAD" ]; then
  B_PIN_ERR="B_HEAD is unset — pin RD-524's forward-merged head from \`git ls-remote origin rd-524-404-441-s77f\` immediately before launch, sed it into the brief and the prompt, and launch with B_HEAD=<sha>"
elif ! printf '%s' "$B_HEAD" | grep -Eq '^[0-9a-f]{40}$'; then
  B_PIN_ERR="B_HEAD '$B_HEAD' is not a full 40-hex sha"
fi
if [ -n "$B_PIN_ERR" ] && [ "$CHECK" = "0" ]; then echo "REFUSING: $B_PIN_ERR" >&2; exit 9; fi
# ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

QA_DIR='/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN'
TUE='/Volumes/KK_T9_External_HDD/TUESDAY'
BRIEF="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-22_nexusai-gate4-rd575-rd524r2.md"
PROMPT_FILE="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-22_nexusai-gate4-rd575-rd524r2.prompt.txt"
REPO='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files'
EVID_E='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/session-tools/s76e'
EVID_F='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/session-tools/s77f'
G3_REPORT="$QA_DIR/projects/nexusai/reports/2026-09-22-gate3-rd524-r10i/report.md"
G3_SEQ="$QA_DIR/projects/nexusai/reports/2026-09-22-gate3-rd524-r10i/evidence/qa-order-sequencer.js"
G2_REPORT="$QA_DIR/projects/nexusai/reports/2026-09-21-gate2-rd495-rd525-rd575/report.md"
REPORT="$QA_DIR/projects/nexusai/reports/2026-09-22-gate4-rd575-rd524r2/report.md"
ID_ROOT="${QA_IDENTITY_ROOT_OVERRIDE:-/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/4_Credentials}"

MAIN_SHA='982a84f2d0c72596a2d389897439e1d8d3425068'
# Target A
A_BRANCH='rd-575-purge-reaches-attachments-s76e'
A_HEAD="${QA_HEAD_SHA_OVERRIDE:-6a32426a7aa7b847cd2ec0ab89f0ec3bdc2fe71e}"
A_E_HEAD='bcb438d1cabb9ef855a024ff93c59048034e6ce8'
RD525_HEAD='792fda0b3dc1884b32f3e04877f18959fbaaae77'
A_CHAIN='6a32426a7aa7b847cd2ec0ab89f0ec3bdc2fe71e
bcb438d1cabb9ef855a024ff93c59048034e6ce8
481315f2f3737d934123037186b5aa82fdbf9b32
4c0fe458342add5110800753b427aee4074da465
04253fbcc0a6fd4135eb674efdbc9942a483ec06'
A_EXPECTED_FILES='__tests__/erasure-reaches-attachments.test.js
__tests__/helpers/zip-entries.js
backend/customerDataFiles.js
backend/dataErasure.js
backend/dataExport.js
scripts/verify-expected-counts.json'
A_LANE_FILES='__tests__/erasure-reaches-attachments.test.js
__tests__/helpers/zip-entries.js
backend/customerDataFiles.js
backend/dataErasure.js
backend/dataExport.js'
A_PRODUCT_FILES='backend/customerDataFiles.js
backend/dataErasure.js
backend/dataExport.js'
A_EXPECTED_TESTS=3868
A_EXPECTED_SUITES=220
# Target B
B_BRANCH='rd-524-404-441-s77f'
B_R1='f42217844bde4fd07952a3d1ec7f165d0957790d'
B_FIX='3931e2b10b4774f8275d08365ece0a032084a604'
B_R1_BASE='bdca588eced9c6a7ee6085b19e48765be3c8c07b'
B_OWN_COMMITS='3931e2b10b4774f8275d08365ece0a032084a604
f42217844bde4fd07952a3d1ec7f165d0957790d
07b9ce6854d036d541d05ba4a3ba97c17e8159c4
faa9cbe445d0cf932c48b784550a4c5383bd4ceb'
B_FIX_FILE='__tests__/rd404-sentinel-first-boot-vs-wipe.test.js'
B_EXPECTED_FILES='BACKLOG.md
__tests__/helpers/persistent-temp-root.js
__tests__/helpers/rd441-banner-render.js
__tests__/rd404-sentinel-first-boot-vs-wipe.test.js
__tests__/rd441-persistence-alarm-reaches-dashboard.test.js
backend/jsonStorage.js
backend/server.js
scripts/verify-expected-counts.json
static/js/index.js'
B_ADD_TESTS=42      # rd404 23 (A3b added) + rd441 19
B_ADD_SUITES=2
NEG_SEATS='94093 57419'   # NexusAI-F (%34) and NexusAI-G (%36) claude pids at drafting

AUTH_FILE='backend/services/authEnforcement.js'
COUNTS_FILE='scripts/verify-expected-counts.json'
SUBJECT='[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — gate 4: RD-575 @ 6a32426 (tier 1) + RD-524 round 2 (narrow re-gate)'

g() { git --no-optional-locks -C "$REPO" "$@"; }
sorted() { printf '%s\n' "$1" | sed '/^$/d' | sort; }
counts_at() { g show "$1:$COUNTS_FILE" 2>/dev/null | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d["tests"], d["suites"])' 2>/dev/null; }
# the added/removed lines of a diff, as a sorted multiset (hunk positions and context ignored)
change_lines() { g diff -U0 "$1" "$2" -- "$3" 2>/dev/null | grep -E '^[-+]' | grep -vE '^(\+\+\+|---) ' | LC_ALL=C sort; }

[ -d "$QA_DIR" ]      || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]       || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ] || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO/.git" ] || [ -f "$REPO/.git" ] || { echo "repo under test missing: $REPO" >&2; exit 5; }

# 6 — every pinned sha is a commit in the object store.
for S in $MAIN_SHA $A_HEAD $A_E_HEAD $RD525_HEAD $B_R1 $B_FIX $B_R1_BASE; do
  T="$(g cat-file -t "$S" 2>&1)"
  [ "$T" = "commit" ] || { echo "REFUSING: $S is not a commit in $REPO (got '$T')" >&2; exit 6; }
done

# ═════ TARGET A ══════════════════════════════════════════════════════════════════════════════════════════════════════
# 7 / 8 — main is the base (ancestor AND merge-base), and 982a84f..A is EXACTLY the five-commit chain, in order.
g merge-base --is-ancestor "$MAIN_SHA" "$A_HEAD" 2>/dev/null || { echo "REFUSING: main $MAIN_SHA is not an ancestor of A $A_HEAD" >&2; exit 7; }
[ "$(g merge-base "$MAIN_SHA" "$A_HEAD" 2>/dev/null)" = "$MAIN_SHA" ] || { echo "REFUSING: merge-base(main, A) is not $MAIN_SHA" >&2; exit 7; }
GOTC="$(g rev-list "${MAIN_SHA}..${A_HEAD}" 2>&1)"
[ "$GOTC" = "$A_CHAIN" ] || { echo "REFUSING: ${MAIN_SHA:0:7}..A is not exactly 04253fb -> 4c0fe45 -> 481315f -> bcb438d -> 6a32426. Got:" >&2; printf '%s\n' "$GOTC" >&2; exit 8; }

# 27 — A is the forward merge claimed: parents EXACTLY bcb438d + 982a84f; and bcb438d stacks on RD-525 792fda0.
P="$(g rev-list --parents -n 1 "$A_HEAD" 2>/dev/null)"
[ "$P" = "$A_HEAD $A_E_HEAD $MAIN_SHA" ] || { echo "REFUSING: A $A_HEAD parents are not exactly $A_E_HEAD + $MAIN_SHA (got '$P')" >&2; exit 27; }
g merge-base --is-ancestor "$RD525_HEAD" "$A_E_HEAD" 2>/dev/null || { echo "REFUSING: RD-525 $RD525_HEAD is not an ancestor of E's head $A_E_HEAD" >&2; exit 27; }

# 18 — A's head at origin, by ls-remote.
L="$(g ls-remote origin "$A_BRANCH" 2>&1)"
printf '%s\n' "$L" | grep -q "^${A_HEAD}[[:space:]]refs/heads/${A_BRANCH}\$" || {
  echo "REFUSING: $A_HEAD is not at refs/heads/$A_BRANCH on origin — that head moved or was never pushed" >&2; printf '%s\n' "$L" >&2; exit 18; }

# 22 — A: EXACTLY the six commissioned files over main.
GOT="$(g diff --name-only "$MAIN_SHA" "$A_HEAD" 2>/dev/null | sort)"
[ "$GOT" = "$(sorted "$A_EXPECTED_FILES")" ] || { echo "REFUSING: A's delta over main is not exactly the six commissioned files. Got:" >&2; printf '%s\n' "$GOT" >&2; exit 22; }

# 35 — the counts file at A reads EXACTLY the builder's figure.
CT="$(counts_at "$A_HEAD")"
[ "$CT" = "$A_EXPECTED_TESTS $A_EXPECTED_SUITES" ] || { echo "REFUSING: $COUNTS_FILE at A reads '${CT:-unreadable}', not '$A_EXPECTED_TESTS $A_EXPECTED_SUITES'" >&2; exit 35; }

# 36 — the merge-only claim: every lane file at A is byte-identical to E's bcb438d.
while IFS= read -r F; do
  [ -z "$F" ] && continue
  BA="$(g rev-parse "${A_HEAD}:$F" 2>/dev/null)"; BE="$(g rev-parse "${A_E_HEAD}:$F" 2>/dev/null)"
  [ -n "$BA" ] && [ "$BA" = "$BE" ] || { echo "REFUSING: $F differs between A and bcb438d (A '$BA', E '$BE') — the forward merge was not merge-only" >&2; exit 36; }
done <<< "$A_LANE_FILES"

# 37 — the revert source: the three product files at main 982a84f are byte-identical to RD-525's 792fda0 (so REVERTED on
#      A = RD-525 without RD-575, the same revert E used).
while IFS= read -r F; do
  [ -z "$F" ] && continue
  BM="$(g rev-parse "${MAIN_SHA}:$F" 2>/dev/null)"; B5="$(g rev-parse "${RD525_HEAD}:$F" 2>/dev/null)"
  [ -n "$BM" ] && [ "$BM" = "$B5" ] || { echo "REFUSING: $F at main ($BM) is not RD-525's ($B5) — the brief's revert recipe no longer reproduces E's" >&2; exit 37; }
done <<< "$A_PRODUCT_FILES"

# ═════ TARGET B — the fix (always checkable) ═════════════════════════════════════════════════════════════════════════
# 41 — f422178..3931e2b is EXACTLY one single-parent commit touching EXACTLY the rd404 test.
[ "$(g rev-list "${B_R1}..${B_FIX}" 2>&1)" = "$B_FIX" ] || { echo "REFUSING: ${B_R1:0:7}..${B_FIX:0:7} is not exactly one commit" >&2; exit 41; }
[ "$(g rev-list --parents -n 1 "$B_FIX" 2>/dev/null)" = "$B_FIX $B_R1" ] || { echo "REFUSING: $B_FIX is not a single-parent child of $B_R1" >&2; exit 41; }
[ "$(g diff --name-only "$B_R1" "$B_FIX" 2>/dev/null)" = "$B_FIX_FILE" ] || { echo "REFUSING: the round-2 fix touches more than $B_FIX_FILE:" >&2; g diff --name-only "$B_R1" "$B_FIX" >&2; exit 41; }

# 25 — authEnforcement.js byte-unchanged: A vs main, and the fix vs round 1's base; with presence control.
for PAIR in "$MAIN_SHA $A_HEAD" "$B_R1_BASE $B_FIX"; do
  set -- $PAIR
  ND="$(g diff "$1" "$2" -- "$AUTH_FILE" 2>/dev/null | wc -l | tr -d ' ')"
  [ "$ND" = "0" ] || { echo "REFUSING: $AUTH_FILE changed between $1 and $2 ($ND diff lines) — not commissioned; re-brief" >&2; exit 25; }
  [ "$(g cat-file -t "$2:$AUTH_FILE" 2>/dev/null)" = "blob" ] || { echo "REFUSING: $AUTH_FILE absent at $2 — guard 25 would be vacuous" >&2; exit 25; }
done
set --

# 31 — builder evidence on disk (A: E's red-proof and F's forward merge; B: F's round-2 hold, including the two
#      LEAKFIRST logs the brief warns never ran — the gate is told to read them).
for f in "$EVID_E/rd575-redproof.log" "$EVID_E/expect-rd575-merged.txt" "$EVID_E/rd575-merge-hold.sh" "$EVID_E/rd575-merge-hold.log" \
         "$EVID_E/rd575-dataExport-resolved.diff" "$EVID_E/mail-11-ready-rd575-v2.txt" "$EVID_E/mail-12-addendum.txt" \
         "$EVID_F/mail-14-ready-rd575.txt" "$EVID_F/rd575-fwd-hold.log" "$EVID_F/rd575-fwd-cells.log" "$EVID_F/rd575-fwd-verify.log" \
         "$EVID_F/mail-13-status.txt" "$EVID_F/expect-rd524-r2.txt" "$EVID_F/rd524-r2-hold.sh" "$EVID_F/rd524-r2-hold.log" \
         "$EVID_F/rd524r2-ALONE.log" "$EVID_F/rd524r2-LEAKFIRST.log" "$EVID_F/rd524r2-M-A3-LEAKFIRST.log" "$EVID_F/rd524r2-M-A3-ALONE.log" \
         "$EVID_F/rd524r2-R0.log" "$EVID_F/ordered-sequencer.js" "$G3_REPORT" "$G2_REPORT"; do
  [ -s "$f" ] || { echo "REFUSING: evidence absent: $f" >&2; exit 31; }
done

# 39 — gate 3's sequencer, the method the brief prescribes, is on disk in its QA_NM form.
[ -s "$G3_SEQ" ] && grep -q 'QA_NM' "$G3_SEQ" || { echo "REFUSING: gate 3's sequencer missing or not in its QA_NM form: $G3_SEQ" >&2; exit 39; }

grep -qF "$REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the report path $REPORT" >&2; exit 10; }
[ ! -e "$REPORT" ] || { echo "REFUSING: $REPORT already exists — a stale report would read as this gate's" >&2; exit 17; }

[ -d "$ID_ROOT/.azure" ] && [ -d "$ID_ROOT/.gh-config" ] || {
  echo "REFUSING: NexusAI identity dirs missing under $ID_ROOT (.azure / .gh-config) — would inherit the caller's" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_ROOT/.azure"
export GH_CONFIG_DIR="$ID_ROOT/.gh-config"
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"

grep -qi 'TIER 1' "$BRIEF" && grep -qi 'TIER 1' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt do not both declare A 'TIER 1'" >&2; exit 12; }
grep -q 'NARROW RE-GATE' "$BRIEF" && grep -q 'NARROW RE-GATE' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt do not both declare B a 'NARROW RE-GATE'" >&2; exit 12; }
head -1 "$PROMPT_FILE" | grep -q 'ultrathink' || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 13; }
grep -qF "$BRIEF" "$PROMPT_FILE" || { echo "REFUSING: prompt must name the brief path" >&2; exit 14; }
grep -qF "$G3_REPORT" "$PROMPT_FILE" && grep -qF "$G3_REPORT" "$BRIEF" || { echo "REFUSING: prompt and brief must both name round 1's report path (template: a round-N brief names round N-1's report)" >&2; exit 14; }
for S in $A_HEAD $MAIN_SHA $A_E_HEAD $B_R1 $B_FIX; do
  grep -qF "$S" "$PROMPT_FILE" && grep -qF "$S" "$BRIEF" || { echo "REFUSING: prompt and brief must both name $S" >&2; exit 14; }
done
if grep -qF "$PH_SCTS" "$PROMPT_FILE" || grep -qF "$PH_SCNOTE" "$PROMPT_FILE"; then echo "REFUSING: the prompt carries a self-check placeholder — it belongs in the brief only" >&2; exit 14; fi
grep -qi 'MAIL YOUR VERDICT' "$PROMPT_FILE" && grep -q 'tuesday-agent@agentmail.to' "$PROMPT_FILE" \
  && grep -qF "$SUBJECT" "$PROMPT_FILE" && grep -qF "$SUBJECT" "$BRIEF" || {
  echo "REFUSING: prompt must say MAIL YOUR VERDICT and name tuesday-agent@agentmail.to; prompt and brief must carry the verdict subject" >&2; exit 15; }
grep -qF '/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env' "$PROMPT_FILE" || { echo "REFUSING: prompt must name the AgentMail key by ABSOLUTE path" >&2; exit 20; }
grep -q 'QUESTION: <topic>' "$PROMPT_FILE" && grep -qi 'no inbox routing line' "$PROMPT_FILE" || { echo "REFUSING: prompt must say QA/Datasec-NexusAI has no inbox routing line and how to ask (QUESTION: <topic>, proceed on the safest reading)" >&2; exit 20; }
WORDS="RD-575 RD-524 RD-404 RD-441 A3 A3b C1b CTRL-1 CTRL-2 E1-R E2-LIVE S2-CTL AB0 P-2 P-6 coexist symlink merge-tree C-68 C-62 QA_NM LEAKER%FIRST NOT%TESTED SEPARATELY%PER%TARGET QUEUE,%NEVER%TAKE%OVER"
for w in $WORDS; do
  w="${w//%/ }"
  grep -q -- "$w" "$PROMPT_FILE" || { echo "REFUSING: prompt must carry '$w'" >&2; exit 19; }
done
grep -q 'RULED BY KAM, NOT YET IN AN ARTEFACT' "$BRIEF" || { echo "REFUSING: brief lacks the RULED BY KAM section" >&2; exit 19; }
grep -q '^PRIOR ROUND\|^## PRIOR ROUND' "$BRIEF" || { echo "REFUSING: brief lacks the PRIOR ROUND section" >&2; exit 19; }
if grep -qi 'backend/server\.js' "$PROMPT_FILE"; then
  echo "REFUSING: the prompt contains the literal server path — this agent would read as a FOREIGN SERVER to any argv-grep floor check (RD-591 c.37901). Describe it; do not name it." >&2; exit 24
fi

# 38 — the brief names BOTH live seats as negative controls; advisory if either is no longer running.
for P in $NEG_SEATS; do
  grep -q "\`$P\`" "$BRIEF" || { echo "REFUSING: brief does not name seat pid $P as a negative control" >&2; exit 38; }
  [ "$(ps -o comm= -p "$P" 2>/dev/null | sed 's#.*/##')" = "claude" ] || echo "NOTE: negative-control seat $P is not a running claude now — re-read the seats and update the brief's §7 before launch" >&2
done

# Advisory only (not a guard): main moving is expected while the queue drains; A is defined against 982a84f.
M_ORIGIN="$(g ls-remote origin main 2>/dev/null | awk '{print $1}')"
[ "$M_ORIGIN" = "$MAIN_SHA" ] || echo "NOTE: origin main is now ${M_ORIGIN:-unreadable}, not ${MAIN_SHA:0:7} — A is still defined against ${MAIN_SHA:0:7}; if RD-575 already merged, this gate is late: re-read before launching" >&2

# ═════ TARGET B — B_HEAD (needs the pin) ═════════════════════════════════════════════════════════════════════════════
# 9 — the pin. Under --check this is reached only after every guard above has passed.
if [ -n "$B_PIN_ERR" ]; then
  echo "A-side and fix-side guards pass (6 7 8 27 18 22 35 36 37 41 25 31 39 10 17 11 12 13 14 15 20 19 24 38); B_HEAD guards NOT run." >&2
  echo "REFUSING: $B_PIN_ERR" >&2; exit 9
fi

T="$(g cat-file -t "$B_HEAD" 2>&1)"
[ "$T" = "commit" ] || { echo "REFUSING: B_HEAD $B_HEAD is not a commit in $REPO (got '$T') — this launcher never fetches; wait for the local object store to have it" >&2; exit 6; }

# 18 — B_HEAD at origin, by ls-remote.
L="$(g ls-remote origin "$B_BRANCH" 2>&1)"
printf '%s\n' "$L" | grep -q "^${B_HEAD}[[:space:]]refs/heads/${B_BRANCH}\$" || {
  echo "REFUSING: $B_HEAD is not at refs/heads/$B_BRANCH on origin — re-pin from ls-remote" >&2; printf '%s\n' "$L" >&2; exit 18; }

# 42 — the brief and prompt name B_HEAD, and neither still carries the placeholder.
grep -qF "$B_HEAD" "$PROMPT_FILE" && grep -qF "$B_HEAD" "$BRIEF" || { echo "REFUSING: prompt and brief must both name B_HEAD $B_HEAD (sed the placeholder)" >&2; exit 42; }
if grep -qF "$PH_BHEAD" "$PROMPT_FILE" "$BRIEF"; then echo "REFUSING: the brief or prompt still carries the B_HEAD placeholder" >&2; exit 42; fi

# 43 — shape: a two-parent merge; first parent descends from the fix; second parent (B_MAIN) is 982a84f or a later main.
PB="$(g rev-list --parents -n 1 "$B_HEAD" 2>/dev/null)"
set -- $PB
[ "$#" = "3" ] || { echo "REFUSING: B_HEAD is not a two-parent merge (got '$PB')" >&2; exit 43; }
B_P1="$2"; B_MAIN="$3"
set --
g merge-base --is-ancestor "$B_FIX" "$B_P1" 2>/dev/null || { echo "REFUSING: B_HEAD's first parent $B_P1 does not descend from the fix $B_FIX" >&2; exit 43; }
g merge-base --is-ancestor "$MAIN_SHA" "$B_MAIN" 2>/dev/null || { echo "REFUSING: B_HEAD's second parent $B_MAIN is not main $MAIN_SHA or later" >&2; exit 43; }
if [ -n "$M_ORIGIN" ] && [ "$(g cat-file -t "$M_ORIGIN" 2>/dev/null)" = "commit" ]; then
  g merge-base --is-ancestor "$B_MAIN" "$M_ORIGIN" 2>/dev/null || { echo "REFUSING: B_HEAD's second parent $B_MAIN is not on origin main $M_ORIGIN" >&2; exit 43; }
else
  echo "NOTE: origin main ${M_ORIGIN:-unreadable} is not in the local object store — cannot confirm $B_MAIN is on it (this launcher never fetches)" >&2
fi

# 44 — no non-merge commit in B_HEAD beyond RD-524's own four that B_MAIN lacks.
GOTN="$(g rev-list --no-merges "$B_HEAD" "^$B_MAIN" 2>&1 | sort)"
[ "$GOTN" = "$(sorted "$B_OWN_COMMITS")" ] || { echo "REFUSING: B_HEAD carries non-merge commits beyond faa9cbe 07b9ce6 f422178 3931e2b. Got:" >&2; printf '%s\n' "$GOTN" >&2; exit 44; }

# 45 — B_HEAD over its main: EXACTLY round 1's nine files.
GOTBF="$(g diff --name-only "$B_MAIN" "$B_HEAD" 2>/dev/null | sort)"
[ "$GOTBF" = "$(sorted "$B_EXPECTED_FILES")" ] || { echo "REFUSING: B_HEAD's delta over $B_MAIN is not exactly round 1's nine files. Got:" >&2; printf '%s\n' "$GOTBF" >&2; exit 45; }

# 46 — counts at B_HEAD = counts at B_MAIN + 42 tests / 2 suites.
CM="$(counts_at "$B_MAIN")"; CB="$(counts_at "$B_HEAD")"
set -- $CM
WANT="$(( ${1:-0} + B_ADD_TESTS )) $(( ${2:-0} + B_ADD_SUITES ))"
set --
[ -n "$CM" ] && [ "$CB" = "$WANT" ] || { echo "REFUSING: counts at B_HEAD read '${CB:-unreadable}', want '$WANT' (B_MAIN '${CM:-unreadable}' + $B_ADD_TESTS/$B_ADD_SUITES)" >&2; exit 46; }

# 47 — NARROW: for every file but the counts file, B_HEAD's added/removed lines over B_MAIN equal 3931e2b's over bdca588.
while IFS= read -r F; do
  [ -z "$F" ] || [ "$F" = "$COUNTS_FILE" ] && continue
  if [ "$(change_lines "$B_MAIN" "$B_HEAD" "$F")" != "$(change_lines "$B_R1_BASE" "$B_FIX" "$F")" ]; then
    echo "REFUSING: $F does not arrive line-for-line: its change lines over $B_MAIN differ from ${B_FIX:0:7}'s over ${B_R1_BASE:0:7} — the round is not narrow; re-brief" >&2; exit 47
  fi
done <<< "$B_EXPECTED_FILES"
ND="$(g diff "$B_MAIN" "$B_HEAD" -- "$AUTH_FILE" 2>/dev/null | wc -l | tr -d ' ')"
[ "$ND" = "0" ] || { echo "REFUSING: $AUTH_FILE changed between B_MAIN and B_HEAD" >&2; exit 25; }

# 32 — the coordinator stamps the self-check (timestamp AND note) before launch. LAST, so --check shows every other guard.
if grep -qF "$PH_SCTS" "$BRIEF" || grep -qF "$PH_SCNOTE" "$BRIEF" \
   || ! grep -q '^SELF-CHECK: re-read end-to-end for contradictions | ' "$BRIEF" || ! grep -q '^Self-check note: ' "$BRIEF"; then
  echo "REFUSING: the brief's SELF-CHECK line or Self-check note is unstamped — the coordinator re-reads end-to-end and stamps both before launch" >&2; exit 32
fi

if [ "$CHECK" = "1" ]; then
  echo "all guards pass:"
  echo "  A $A_HEAD at origin (18); base ${MAIN_SHA:0:7} ancestor + merge-base (7); chain exactly 04253fb 4c0fe45 481315f bcb438d 6a32426 (8); parents bcb438d+982a84f (27); six files (22)"
  echo "  A counts $A_EXPECTED_TESTS/$A_EXPECTED_SUITES (35); lane files identical to bcb438d (36); product files at main == 792fda0's (37)"
  echo "  fix ${B_FIX:0:7}: one commit on ${B_R1:0:7}, rd404 test only (41); $AUTH_FILE unchanged (25)"
  echo "  B_HEAD $B_HEAD at origin (18); named, no placeholder (42); merge of ${B_P1:0:7} + main ${B_MAIN:0:7} (43); own commits only (44); nine files (45); counts $CB (46); line-for-line narrow (47)"
  echo "  evidence present (31); gate-3 sequencer QA_NM form (39); report does not exist yet (17); seats $NEG_SEATS named (38)"
  echo "  AZURE_CONFIG_DIR=$AZURE_CONFIG_DIR  GH_CONFIG_DIR=$GH_CONFIG_DIR  CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR"
  echo "  tier (12); directive (13); brief+shas+round-1 report named (14); mail (15); key absolute + question route (20); names (19); no server path (24); self-check stamped (32)"
  exit 0
fi

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model claude-opus-5 "$(cat "$PROMPT_FILE")"
