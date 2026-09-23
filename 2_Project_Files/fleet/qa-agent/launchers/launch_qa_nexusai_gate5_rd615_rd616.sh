#!/bin/bash
# launch_qa_nexusai_gate5_rd615_rd616.sh — cross-project QA agent, ONE BATCHED gate (gate 5 of 2026-09-22) on Datasec/NexusAI:
#   TARGET A — RD-615: rd-615-audit-flush-epoch-s77f @ b7fc78f, off main 982a84f; chain 5f99fcb -> 71f2949 -> c60a00d -> b7fc78f. TIER 1.
#   TARGET B — RD-616 + RD-617: rd-616-617-s79h @ f0519fd, off main 982a84f; chain cd6cd55 -> f0519fd. TIER 1.
#   Both heads are KNOWN at drafting — no environment pin.
#
# AUTHORITY: READY FOR QA from S77F (mail-19, RD-615) and S79H (mail-05, RD-616/617). Batching is Kam's standing rule of
# 2026-09-18 (0_Brain/learnings/2026-09-18_minimise-gate-duplication-batch-them.md). Merges after this gate are Tuesday's GO
# under C-127, behind RD-575 and RD-524 (gate 4).
#
# PATTERN: launch_qa_nexusai_gate4_rd575_rd524r2.sh. CHANGES:
#   - no B_HEAD pin (exit 9 removed): both heads are constants below, verified at origin by ls-remote (18).
#   - exit 7/8: each target's base is main (ancestor AND merge-base) and its chain is EXACTLY the commissioned commits.
#   - exit 22/35: each target's file set and counts; exit 50: per-commit file sets (counts-only commits, comment commit).
#   - exit 51: A's dataErasure.js change is COMMENT-ONLY (every changed line is a ` *` docblock line) — with a presence control.
#   - exit 52: B does NOT touch the server entry point, encryptionService.js or jsonStorage.js (the brief's health-field
#     reasoning depends on it) — with presence controls.
#   - exit 38: the brief names all THREE live seats as negative controls (G 57419, H 29254, gate-4 claude 95254).
#   - exit 53: brief and prompt carry the gate-4 DEADLINE / HEARTBEAT rule.
#   - exit 32: SELF-CHECK timestamp and note placeholders stamped by the coordinator before launch (LAST guard, so --check
#     shows every other guard first). Placeholder comparands are BUILT BY CONCATENATION so a sed of the placeholder text
#     cannot reach them.
#   - exit 24 carried: the prompt must not carry the literal server path (RD-591 c.37901).
#
# LAUNCH IT IN A TMUX PANE (cockpit.sh add 'QA/NexusAI-gate5' "bash '<this file>'"), NEVER nohup.
# Identity: exports NexusAI's OWN az/gh dirs; CLAUDE_CONFIG_DIR pinned to Tuesday's project-local store.
# ABSOLUTE PATHS ON PURPOSE. TRACKED in launchers/. Contains a legitimate `cd` (into the QA project, at exec).
# Usage: launch_qa_nexusai_gate5_rd615_rd616.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..53 a guard refused
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
BRIEF="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-22_nexusai-gate5-rd615-rd616.md"
PROMPT_FILE="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-22_nexusai-gate5-rd615-rd616.prompt.txt"
REPO='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files'
NX='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI'
EVID_F="$NX/session-tools/s77f"
EVID_H="$NX/session-tools/s79h"
G2_REPORT="$QA_DIR/projects/nexusai/reports/2026-09-21-gate2-rd495-rd525-rd575/report.md"
G3_FLOOR="$QA_DIR/projects/nexusai/reports/2026-09-22-gate3-rd524-r10i/evidence/qa-floorcount.py"
G4_STALL="$QA_DIR/projects/nexusai/reports/2026-09-22-gate4-rd575-rd524r2/evidence/a3u-stall-evidence.txt"
REPORT="$QA_DIR/projects/nexusai/reports/2026-09-22-gate5-rd615-rd616/report.md"
ID_ROOT="${QA_IDENTITY_ROOT_OVERRIDE:-$NX/4_Credentials}"

MAIN_SHA='982a84f2d0c72596a2d389897439e1d8d3425068'
G4_A='6a32426a7aa7b847cd2ec0ab89f0ec3bdc2fe71e'   # RD-575, gate 4, merges first
G4_B='dc8635c50b7fd607f8845f39729f4f2ad5614bcb'   # RD-524 r2, gate 4, merges first
# Target A
A_BRANCH='rd-615-audit-flush-epoch-s77f'
A_HEAD="${QA_A_HEAD_OVERRIDE:-b7fc78f2cb4e3650f4e045596688beed924aeaaa}"
A_FIX='5f99fcb1c1c8178105b0dd3c56715ef44a0bcc04'
A_CMT='71f29496add88164f5331c911dbcd11975bf8815'
A_WAIT='c60a00de2d329d98ea9b575d238850b209d8eaec'
A_CHAIN='b7fc78f2cb4e3650f4e045596688beed924aeaaa
c60a00de2d329d98ea9b575d238850b209d8eaec
71f29496add88164f5331c911dbcd11975bf8815
5f99fcb1c1c8178105b0dd3c56715ef44a0bcc04'
A_EXPECTED_FILES='__tests__/helpers/rd615-slow-audit-flush-preload.js
__tests__/rd615-audit-flush-cannot-resurrect-erased-entries.test.js
backend/dataErasure.js
backend/server.js
scripts/verify-expected-counts.json'
A_FIX_FILES='__tests__/helpers/rd615-slow-audit-flush-preload.js
__tests__/rd615-audit-flush-cannot-resurrect-erased-entries.test.js
backend/server.js'
A_EXPECTED_TESTS=3864
A_EXPECTED_SUITES=220
# Target B
B_BRANCH='rd-616-617-s79h'
B_HEAD="${QA_B_HEAD_OVERRIDE:-f0519fd2390c7d5f2103e72dddac3adc276df639}"
B_CHANGE='cd6cd55735ceac4e931e0f3dea049279ed18bf63'
B_CHAIN='f0519fd2390c7d5f2103e72dddac3adc276df639
cd6cd55735ceac4e931e0f3dea049279ed18bf63'
B_EXPECTED_FILES='__tests__/rd412-smtp-transport.test.js
__tests__/rd616-617-mail-secrets-at-rest-and-export-shapes.test.js
backend/dataExport.js
backend/services/emailService.js
scripts/verify-expected-counts.json'
B_UNTOUCHED='backend/server.js
backend/encryptionService.js
backend/jsonStorage.js'
B_EXPECTED_TESTS=3871
B_EXPECTED_SUITES=220
NEG_SEATS='57419 29254 95254'   # NexusAI-G (%36), NexusAI-H (%38), gate-4 claude (%37) at drafting

AUTH_FILE='backend/services/authEnforcement.js'
COUNTS_FILE='scripts/verify-expected-counts.json'
SUBJECT='[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — gate 5: RD-615 @ b7fc78f (tier 1) + RD-616/617 @ f0519fd (tier 1)'

g() { git --no-optional-locks -C "$REPO" "$@"; }
sorted() { printf '%s\n' "$1" | sed '/^$/d' | sort; }
counts_at() { g show "$1:$COUNTS_FILE" 2>/dev/null | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d["tests"], d["suites"])' 2>/dev/null; }

[ -d "$QA_DIR" ]      || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]       || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ] || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO/.git" ] || [ -f "$REPO/.git" ] || { echo "repo under test missing: $REPO" >&2; exit 5; }

# 6 — every pinned sha is a commit in the object store.
for S in $MAIN_SHA $A_HEAD $A_FIX $A_CMT $A_WAIT $B_HEAD $B_CHANGE $G4_A $G4_B; do
  T="$(g cat-file -t "$S" 2>&1)"
  [ "$T" = "commit" ] || { echo "REFUSING: $S is not a commit in $REPO (got '$T') — this launcher never fetches" >&2; exit 6; }
done

# 7 / 8 — per target: main is ancestor AND merge-base; main..head is EXACTLY the chain, each single-parent.
check_chain() { # label head chain
  local L="$1" H="$2" C="$3" GOTC c P
  g merge-base --is-ancestor "$MAIN_SHA" "$H" 2>/dev/null || { echo "REFUSING: main $MAIN_SHA is not an ancestor of $L $H" >&2; exit 7; }
  [ "$(g merge-base "$MAIN_SHA" "$H" 2>/dev/null)" = "$MAIN_SHA" ] || { echo "REFUSING: merge-base(main, $L) is not $MAIN_SHA" >&2; exit 7; }
  GOTC="$(g rev-list "${MAIN_SHA}..${H}" 2>&1)"
  [ "$GOTC" = "$C" ] || { echo "REFUSING: ${MAIN_SHA:0:7}..$L is not exactly the commissioned chain. Got:" >&2; printf '%s\n' "$GOTC" >&2; exit 8; }
  while IFS= read -r c; do
    [ -z "$c" ] && continue
    P="$(g rev-list --parents -n 1 "$c" 2>/dev/null | wc -w | tr -d ' ')"
    [ "$P" = "2" ] || { echo "REFUSING: $L commit $c is not single-parent" >&2; exit 8; }
  done <<< "$C"
}
check_chain A "$A_HEAD" "$A_CHAIN"
check_chain B "$B_HEAD" "$B_CHAIN"

# 18 — both heads at origin, by ls-remote.
for PAIR in "$A_BRANCH $A_HEAD" "$B_BRANCH $B_HEAD"; do
  BR="${PAIR%% *}"; H="${PAIR##* }"
  L="$(g ls-remote origin "$BR" 2>&1)"
  printf '%s\n' "$L" | grep -q "^${H}[[:space:]]refs/heads/${BR}\$" || {
    echo "REFUSING: $H is not at refs/heads/$BR on origin — that head moved or was never pushed" >&2; printf '%s\n' "$L" >&2; exit 18; }
done

# 22 — each target's delta over main is EXACTLY its commissioned five files.
GOT="$(g diff --name-only "$MAIN_SHA" "$A_HEAD" 2>/dev/null | sort)"
[ "$GOT" = "$(sorted "$A_EXPECTED_FILES")" ] || { echo "REFUSING: A's delta over main is not exactly the five commissioned files. Got:" >&2; printf '%s\n' "$GOT" >&2; exit 22; }
GOT="$(g diff --name-only "$MAIN_SHA" "$B_HEAD" 2>/dev/null | sort)"
[ "$GOT" = "$(sorted "$B_EXPECTED_FILES")" ] || { echo "REFUSING: B's delta over main is not exactly the five commissioned files. Got:" >&2; printf '%s\n' "$GOT" >&2; exit 22; }

# 35 — counts files read EXACTLY the builders' figures.
CT="$(counts_at "$A_HEAD")"
[ "$CT" = "$A_EXPECTED_TESTS $A_EXPECTED_SUITES" ] || { echo "REFUSING: $COUNTS_FILE at A reads '${CT:-unreadable}', not '$A_EXPECTED_TESTS $A_EXPECTED_SUITES'" >&2; exit 35; }
CT="$(counts_at "$B_HEAD")"
[ "$CT" = "$B_EXPECTED_TESTS $B_EXPECTED_SUITES" ] || { echo "REFUSING: $COUNTS_FILE at B reads '${CT:-unreadable}', not '$B_EXPECTED_TESTS $B_EXPECTED_SUITES'" >&2; exit 35; }

# 50 — per-commit file sets: the counts commits touch ONLY the counts file; 71f2949 ONLY dataErasure.js; c60a00d ONLY the
#      rd615 test; 5f99fcb exactly the preload, the rd615 test and the server entry point; cd6cd55 = B minus the counts file.
files_of() { g diff --name-only "$1^" "$1" 2>/dev/null | sort; }
[ "$(files_of "$A_HEAD")" = "$COUNTS_FILE" ] || { echo "REFUSING: ${A_HEAD:0:7} is not counts-only" >&2; exit 50; }
[ "$(files_of "$B_HEAD")" = "$COUNTS_FILE" ] || { echo "REFUSING: ${B_HEAD:0:7} is not counts-only" >&2; exit 50; }
[ "$(files_of "$A_CMT")" = "backend/dataErasure.js" ] || { echo "REFUSING: ${A_CMT:0:7} touches more than backend/dataErasure.js" >&2; exit 50; }
[ "$(files_of "$A_WAIT")" = "__tests__/rd615-audit-flush-cannot-resurrect-erased-entries.test.js" ] || { echo "REFUSING: ${A_WAIT:0:7} touches more than the rd615 test" >&2; exit 50; }
[ "$(files_of "$A_FIX")" = "$(sorted "$A_FIX_FILES")" ] || { echo "REFUSING: ${A_FIX:0:7} file set is not preload + rd615 test + server entry point" >&2; exit 50; }
[ "$(files_of "$B_CHANGE")" = "$(sorted "$(printf '%s\n' "$B_EXPECTED_FILES" | grep -v "^$COUNTS_FILE\$")")" ] || { echo "REFUSING: ${B_CHANGE:0:7} file set is not B's four non-counts files" >&2; exit 50; }

# 51 — A's dataErasure.js change is COMMENT-ONLY: every added/removed line is a docblock ` *` line; and there IS a change.
DL="$(g diff -U0 "$MAIN_SHA" "$A_HEAD" -- backend/dataErasure.js 2>/dev/null | grep -E '^[-+]' | grep -vE '^(\+\+\+|---) ')"
[ -n "$DL" ] || { echo "REFUSING: no dataErasure.js change between main and A — guard 51 would be vacuous" >&2; exit 51; }
NC="$(printf '%s\n' "$DL" | grep -vcE '^[-+][[:space:]]*\*')"
[ "$NC" = "0" ] || { echo "REFUSING: A's dataErasure.js change has $NC non-comment line(s) — the brief calls it comment-only; re-brief" >&2; printf '%s\n' "$DL" | grep -vE '^[-+][[:space:]]*\*' >&2; exit 51; }

# 52 — B does not touch the server entry point, encryptionService.js or jsonStorage.js (each present at B: presence control).
while IFS= read -r F; do
  [ -z "$F" ] && continue
  [ "$(g cat-file -t "$B_HEAD:$F" 2>/dev/null)" = "blob" ] || { echo "REFUSING: $F absent at B — guard 52 would be vacuous" >&2; exit 52; }
  [ "$(g rev-parse "$MAIN_SHA:$F" 2>/dev/null)" = "$(g rev-parse "$B_HEAD:$F" 2>/dev/null)" ] || { echo "REFUSING: B changed $F — the brief says it does not; re-brief" >&2; exit 52; }
done <<< "$B_UNTOUCHED"

# 25 — authEnforcement.js byte-unchanged in both targets; with presence control.
for H in "$A_HEAD" "$B_HEAD"; do
  ND="$(g diff "$MAIN_SHA" "$H" -- "$AUTH_FILE" 2>/dev/null | wc -l | tr -d ' ')"
  [ "$ND" = "0" ] || { echo "REFUSING: $AUTH_FILE changed between main and $H ($ND diff lines) — not commissioned; re-brief" >&2; exit 25; }
  [ "$(g cat-file -t "$H:$AUTH_FILE" 2>/dev/null)" = "blob" ] || { echo "REFUSING: $AUTH_FILE absent at $H — guard 25 would be vacuous" >&2; exit 25; }
done

# 31 — builder evidence and prior-gate evidence on disk.
for f in "$EVID_F/mail-17-rd615-void.txt" "$EVID_F/mail-18-rd627.txt" "$EVID_F/mail-19-ready-rd615.txt" "$EVID_F/expect-rd615.txt" \
         "$EVID_F/rd615-proof-hold.sh" "$EVID_F/rd615-proof-hold.log" "$EVID_F/rd615-proof-hold-run1-VOID-double-sigterm.log" \
         "$EVID_F/rd615-R0.log" "$EVID_F/rd615-M.log" "$EVID_F/rd615-verify.log" "$NX/HANDOVER-S77F.md" \
         "$EVID_H/mail-05-ready-rd616.1ADTXo" "$EVID_H/expect-rd616-617.txt" "$EVID_H/rd616-proof-hold.sh" "$EVID_H/rd616-hold-run1.out" \
         "$EVID_H/rd616-R0.log" "$EVID_H/rd616-M-616.log" "$EVID_H/rd616-M-616d.log" "$EVID_H/rd616-M-617.log" "$EVID_H/rd616-M-413.log" \
         "$EVID_H/rd616-verify.log" "$G2_REPORT" "$G4_STALL"; do
  [ -s "$f" ] || { echo "REFUSING: evidence absent: $f" >&2; exit 31; }
done

# 39 — gate 3's floor instrument, which the brief prescribes, is on disk.
[ -s "$G3_FLOOR" ] || { echo "REFUSING: gate 3's floor instrument missing: $G3_FLOOR" >&2; exit 39; }

grep -qF "$REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the report path $REPORT" >&2; exit 10; }
[ ! -e "$REPORT" ] || { echo "REFUSING: $REPORT already exists — a stale report would read as this gate's" >&2; exit 17; }

[ -d "$ID_ROOT/.azure" ] && [ -d "$ID_ROOT/.gh-config" ] || {
  echo "REFUSING: NexusAI identity dirs missing under $ID_ROOT (.azure / .gh-config) — would inherit the caller's" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_ROOT/.azure"
export GH_CONFIG_DIR="$ID_ROOT/.gh-config"
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"

# 12 — both targets declared TIER 1 in both files.
grep -q 'A (RD-615) is TIER 1' "$BRIEF" && grep -q 'B (RD-616 + RD-617) is TIER 1' "$BRIEF" \
  && grep -q 'TARGET A — RD-615 (TIER 1)' "$PROMPT_FILE" && grep -q 'TARGET B — RD-616 + RD-617 (TIER 1)' "$PROMPT_FILE" || {
  echo "REFUSING: brief and prompt do not both declare A and B 'TIER 1'" >&2; exit 12; }
head -1 "$PROMPT_FILE" | grep -q 'ultrathink' || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 13; }
grep -qF "$BRIEF" "$PROMPT_FILE" || { echo "REFUSING: prompt must name the brief path" >&2; exit 14; }
grep -qF "$G2_REPORT" "$BRIEF" || { echo "REFUSING: brief must name gate 2's report path (where both defects were found)" >&2; exit 14; }
for S in $A_HEAD $B_HEAD $MAIN_SHA $A_FIX $B_CHANGE; do
  grep -qF "$S" "$PROMPT_FILE" && grep -qF "$S" "$BRIEF" || { echo "REFUSING: prompt and brief must both name $S" >&2; exit 14; }
done
if grep -qF "$PH_SCTS" "$PROMPT_FILE" || grep -qF "$PH_SCNOTE" "$PROMPT_FILE"; then echo "REFUSING: the prompt carries a self-check placeholder — it belongs in the brief only" >&2; exit 14; fi
grep -qi 'MAIL YOUR VERDICT' "$PROMPT_FILE" && grep -q 'tuesday-agent@agentmail.to' "$PROMPT_FILE" \
  && grep -qF "$SUBJECT" "$PROMPT_FILE" && grep -qF "$SUBJECT" "$BRIEF" || {
  echo "REFUSING: prompt must say MAIL YOUR VERDICT and name tuesday-agent@agentmail.to; prompt and brief must carry the verdict subject" >&2; exit 15; }
grep -qF '/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env' "$PROMPT_FILE" || { echo "REFUSING: prompt must name the AgentMail key by ABSOLUTE path" >&2; exit 20; }
grep -q 'QUESTION: <topic>' "$PROMPT_FILE" && grep -qi 'no inbox routing line' "$PROMPT_FILE" || { echo "REFUSING: prompt must say QA/Datasec-NexusAI has no inbox routing line and how to ask (QUESTION: <topic>, proceed on the safest reading)" >&2; exit 20; }
WORDS="RD-615 RD-616 RD-617 RD-627 RD-413 M-413 M-616 M-616d M-617 W1 W2 audit-buffer.json.tmp machine-id includeSecrets feedback-attachments unknown%shape option%B stored%form /api/setup/mail-config merge-tree C-68 C-97 LEGITIMATE%SHAPES NOT%TESTED SEPARATELY%PER%TARGET QUEUE,%NEVER%TAKE%OVER"
for w in $WORDS; do
  w="${w//%/ }"
  grep -q -- "$w" "$PROMPT_FILE" || { echo "REFUSING: prompt must carry '$w'" >&2; exit 19; }
done
grep -q 'RULED BY KAM, NOT YET IN AN ARTEFACT' "$BRIEF" || { echo "REFUSING: brief lacks the RULED BY KAM section" >&2; exit 19; }
grep -q '^## PRIOR ROUND' "$BRIEF" || { echo "REFUSING: brief lacks the PRIOR ROUND section" >&2; exit 19; }
grep -q '^## 2a. LEGITIMATE SHAPES' "$BRIEF" || { echo "REFUSING: brief lacks §2a LEGITIMATE SHAPES (RD-617's refusal is a checker)" >&2; exit 19; }
if grep -qi 'backend/server\.js' "$PROMPT_FILE"; then
  echo "REFUSING: the prompt contains the literal server path — this agent would read as a FOREIGN SERVER to any argv-grep floor check (RD-591 c.37901). Describe it; do not name it." >&2; exit 24
fi

# 53 — the gate-4 lesson: per-step DEADLINE, HEARTBEAT every 2 minutes, abort at 5 minutes silent, server killed in a finally.
for FL in "$BRIEF" "$PROMPT_FILE"; do
  grep -q 'DEADLINE' "$FL" && grep -q 'HEARTBEAT' "$FL" && grep -q '2 minutes' "$FL" && grep -q '5 minutes' "$FL" && grep -q 'finally' "$FL" || {
    echo "REFUSING: $FL lacks the DEADLINE / HEARTBEAT rule (2 minutes, 5 minutes, finally) — gate 4 stalled ~70 min holding the lock" >&2; exit 53; }
done

# 38 — the brief names ALL THREE live seats as negative controls; advisory if one is no longer running.
for P in $NEG_SEATS; do
  grep -q "\`$P\`" "$BRIEF" || { echo "REFUSING: brief does not name seat pid $P as a negative control" >&2; exit 38; }
  [ "$(ps -o comm= -p "$P" 2>/dev/null | sed 's#.*/##')" = "claude" ] || echo "NOTE: negative-control seat $P is not a running claude now — re-read the seats and update the brief's §7 before launch" >&2
done

# Advisory only: main moving is expected while the queue drains; both targets are defined against 982a84f.
M_ORIGIN="$(g ls-remote origin main 2>/dev/null | awk '{print $1}')"
[ "$M_ORIGIN" = "$MAIN_SHA" ] || echo "NOTE: origin main is now ${M_ORIGIN:-unreadable}, not ${MAIN_SHA:0:7} — if RD-575/RD-524 merged, §6's merge-tree table is stale: re-measure before launch" >&2

# 32 — the coordinator stamps the self-check (timestamp AND note) before launch. LAST, so --check shows every other guard.
if grep -qF "$PH_SCTS" "$BRIEF" || grep -qF "$PH_SCNOTE" "$BRIEF" \
   || ! grep -q '^SELF-CHECK: re-read end-to-end for contradictions | ' "$BRIEF" || ! grep -q '^Self-check note: ' "$BRIEF"; then
  echo "guards pass (6 7 8 18 22 35 50 51 52 25 31 39 10 17 11 12 13 14 15 20 19 24 53 38); self-check NOT stamped." >&2
  echo "REFUSING: the brief's SELF-CHECK line or Self-check note is unstamped — the coordinator re-reads end-to-end and stamps both before launch" >&2; exit 32
fi

if [ "$CHECK" = "1" ]; then
  echo "all guards pass:"
  echo "  A $A_HEAD at origin (18); base ${MAIN_SHA:0:7} (7); chain 5f99fcb 71f2949 c60a00d b7fc78f, single-parent (8); five files (22); counts $A_EXPECTED_TESTS/$A_EXPECTED_SUITES (35)"
  echo "  B $B_HEAD at origin (18); base ${MAIN_SHA:0:7} (7); chain cd6cd55 f0519fd, single-parent (8); five files (22); counts $B_EXPECTED_TESTS/$B_EXPECTED_SUITES (35)"
  echo "  per-commit file sets (50); dataErasure.js comment-only (51); B leaves server entry point / encryptionService / jsonStorage alone (52); $AUTH_FILE unchanged (25)"
  echo "  evidence present (31); gate-3 floor instrument (39); report does not exist yet (17); seats $NEG_SEATS named (38)"
  echo "  AZURE_CONFIG_DIR=$AZURE_CONFIG_DIR  GH_CONFIG_DIR=$GH_CONFIG_DIR  CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR"
  echo "  tier (12); directive (13); brief+shas+gate-2 report named (14); mail (15); key absolute + question route (20); names (19); no server path (24); deadline/heartbeat (53); self-check stamped (32)"
  exit 0
fi

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model claude-opus-5-5 "$(cat "$PROMPT_FILE")"
