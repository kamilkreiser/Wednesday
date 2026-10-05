#!/bin/bash
# launch_qa_secuura_ks1401_1383r2.sh — cross-project QA agent, gate61 ROUND 2 over ONE Secuura/Blockchain PR, #1383 (KS-1401, T1), NARROWED to ONE
# commit: 32e8459bc0f5 (the N-1383-1 fix) on round-1 head 7eccb131f2d6. Merger: Seat F 3rd. Shape: gate61's launcher (a NEW file, never an edit),
# with NO pins file: every run re-reads origin itself (the head is pinned in this file; develop is RECORDED, never refused — it is expected to move).
# exit 2: QA project missing, or this launcher is not in its kit dir (a MOVED KIT).  exit 4/5: prompt / repo missing.
# exit 6: the head is not at its exact branch AND refs/pull/1383/head on origin.     exit 11: the head's parent is not the round-1 head.
# exit 8: thinking directive / kit files named / an unfilled token.   exit 20: the prompt names the head in full.
# exit 7: tier + FROZEN + round.   exit 33: the by-name keyword ladder (as tokens) + measurement rules.   exit 39: the HOLDS + named exceptions.
# exit 26: the GO string (with the KS-1404 merge-order clause).   exit 25: MERGE ADDENDUM + REPORT-HASH-LAST.   exit 23: verdict subject / sender / report dir.
# exit 21: a LAUNCH (not --check) refuses when stdin is not a TTY.   exit 16: a launch with a G61R2_* test override set.
# Test overrides (--check only): G61R2_HEAD (pretend head), G61R2_PROMPT (another prompt file). Opus by the configured default: NO --model.
# Usage: launch_qa_secuura_ks1401_1383r2.sh [--check]
set -u
QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
GS='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-05_gate61r2'
PROMPT_FILE="${G61R2_PROMPT:-$GS/2026-10-05_secuura-ks1401-1383r2.prompt.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
PR='1383'
HEAD_SHA='32e8459bc0f51d1af492aae7c0b3d9754f78c9bf'
R1_HEAD='7eccb131f2d627a628d41b2cd537e81ce9e52fc4'
BRANCH='refs/heads/feature/ks-1401-tenant-isolation-after-039-f2-1'
[ -d "$QA_DIR" ] || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
_here="$(dirname "$(/bin/realpath "$0")")"
[ "$_here" = "$GS" ] || { echo "REFUSING: this launcher lives in $_here but belongs to $GS — a MOVED KIT" >&2; exit 2; }
[ -s "$PROMPT_FILE" ] || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]        || { echo "repo under test missing: $REPO" >&2; exit 5; }
[ "$(head -n 1 "$PROMPT_FILE")" = "ultrathink" ] || { echo "REFUSING: the prompt does not open with the thinking directive" >&2; exit 8; }
for _f in README.md COMMISSION.md kit.json r2_check_gate61r2.py qm_gate61r2.sh; do
  [ -s "$GS/$_f" ] && grep -qF "$GS/$_f" "$PROMPT_FILE" || { echo "REFUSING: the kit file $GS/$_f is missing, empty, or not named in the prompt" >&2; exit 8; }
done
grep -qF "2026-10-05-ks1401-1383-g61/report.md" "$PROMPT_FILE" && grep -qF "c1ecb83f16f691823252672340df6961177fc2b20c812ea62d3e78246e354bfd" "$PROMPT_FILE" || { echo "REFUSING: the prompt does not name the round-1 report and its hash" >&2; exit 8; }
grep -qF "2026-10-05_seatF3_successor.md" "$PROMPT_FILE" || { echo "REFUSING: the prompt does not name the seat's brief" >&2; exit 8; }
grep -qE '\{\{[A-Z0-9_]+\}\}' "$PROMPT_FILE" && { echo "REFUSING: the prompt carries an unfilled double-brace fill token" >&2; exit 8; }
_LS="$(git -C "$REPO" ls-remote origin refs/heads/develop "$BRANCH" "refs/pull/$PR/head")"   # ONE read of origin
CUR_DEV="$(printf '%s\n' "$_LS" | awk '$2=="refs/heads/develop"{print $1}')"
_h="${G61R2_HEAD:-$HEAD_SHA}"
if [ "$(printf '%s\n' "$_LS" | awk -v h="$_h" -v r="$BRANCH" '$1==h && $2==r' | wc -l | tr -d ' ')" != 1 ] || [ "$(printf '%s\n' "$_LS" | awk -v h="$_h" -v r="refs/pull/$PR/head" '$1==h && $2==r' | wc -l | tr -d ' ')" != 1 ]; then
  echo "REFUSING: #$PR — $_h is not at $BRANCH AND refs/pull/$PR/head on origin — the head moved (or the pin is wrong); a verdict is valid ONLY at its head" >&2
  printf '%s\n' "$_LS" >&2; exit 6
fi
_par="$(git -C "$REPO" rev-list --parents -n 1 "$_h" 2>/dev/null | cut -d' ' -f2-)"
[ "$_par" = "$R1_HEAD" ] || { echo "REFUSING: $_h's parent(s) '$_par' != the round-1 head $R1_HEAD (round 2 is ONE fast-forward commit; anything else is a RE-DRAFT)" >&2; exit 11; }
grep -qwF "$_h" "$PROMPT_FILE" || { echo "REFUSING: the prompt does not name the head $_h in full" >&2; exit 20; }
PROMPT_JOINED="$(python3 -c 'import re,sys; print(re.sub(r"\n\s*", " ", open(sys.argv[1], encoding="utf-8").read()))' "$PROMPT_FILE")"
has() { printf '%s' "$PROMPT_JOINED" | grep -qF -- "$1"; }
has "PR #$PR is KS-1401" && has "#$PR T1" && has 'THE GATE IS FROZEN at ONE PR and ONE commit' && has 'ROUND 2' && has 'Migration-on-live-data: you apply 049 ONLY to throwaway databases you create' || { echo "REFUSING: the ticket / tier / FROZEN / round / live-data line" >&2; exit 7; }
has 'MEASURE, not conclude' && has 'RULE WHETHER IT BLOCKS' && has 'NAMES THE TREE' && has 'A check that prints nothing needs a control that prints' && has 'ASSERT THE FILENAME TOO' && has 'assert the run COMMITTED' || { echo "REFUSING: the measurement rules" >&2; exit 33; }
for _w in C1-PIN FF-ONLY SCOPE-4-PATHS ROUND1-UNCHANGED NO-TRAILER EXEC-BIT C2-DELTA LIVE-SQL-GUARD BYPASS-FIRST IS-LOCAL C3-SUITE-62 RED-FIRST-CELL12 COMMIT-BEFORE-COUNT FALSIFIABLE-60-2 Q-LEAK R2-TAMPERS BYPASS-SCOPE BYPASS-LEAK PRECEDENT-039 RUNNER-TXN C4-BLOCK22-ONLY CLOSE-TAG-UNTOUCHED C4-MERGE-IN Q-M C5-BODY-REREAD CLOSING-WORD-STRICT NEVER-DEMO KEYSCAN-OWN-KEY C6-NOT-COVERED READY-CLAIMS PR-BODY-CLAIMS PREFLIGHT-INCOMPLETE COLLISION-CENSUS NOT-TESTED-LIST TIERING DISK-ENOSPC REPORT-HASH-LAST; do
  printf '%s' "$PROMPT_JOINED" | grep -qE -- "(^|[^A-Za-z0-9-])$_w([^A-Za-z0-9-]|\$)" || { echo "REFUSING: the prompt does not carry the by-name keyword '$_w'" >&2; exit 33; }
done
has 'T-SESSION' && has 'T-NOBYPASS' && has 'KS1401_F049_UNDER_TEST' && has 'KS1401_FLOOR=62' && has 'pool.query(m.sql)' && has 'qm_gate61r2.sh qm' && has 'STRICT predicate' && has '016e2af94abefb59' && has 'PREFLIGHT-INCOMPLETE 12/15' || { echo "REFUSING: the round-2 checks by name" >&2; exit 34; }
has 'NO MERGE, NO PUSH to any PR branch, NO ticket state change' && has 'NEVER WRITE THE SHARED CHECKOUT. Findings only' && has 'Never `rm`' && has 'No `az` command of any kind' && has 'You NEVER reply to Peter' && has 'NEVER apply 049 to any database you did not create' && has 'THE NAMED EXCEPTIONS to those holds — these and NO others' && has 'TICKET STATE IS WEDNESDAY' && has '(X9) a throwaway PostgreSQL 15 keg cluster' || { echo "REFUSING: the HOLDS" >&2; exit 39; }
has "WEDNESDAY'S signed GO naming the head" && has 'GO (Seat F 3rd): merge 1383 on gate61 — merge only after the KS-1404 anchor-wiring PR has merged' && has 'The merge seat is Seat F 3rd' || { echo "REFUSING: merge authority / the GO string" >&2; exit 26; }
has '## MERGE ADDENDUM' && has 'R2 4 over 4 paths' && has 'MG-11 subject <= 92' && has 'NO TRAILER' && has 'EVERY SUBJECT YOU PROPOSE MUST BE TRUE OF THE DIFF' && has 'is the LAST thing you write to report.md' && has 'sha256 report.md = <hex>' || { echo "REFUSING: the MERGE ADDENDUM rules / REPORT-HASH-LAST" >&2; exit 25; }
grep -qF -- '[QA -> Wednesday] GATE61 ROUND 2 #1383 (Seat F 3rd author and merger; T1 KS-1401: N-1383-1 fix, 049 takes the platform bypass for its own backfill; narrowed to 32e8459bc0f5; merge after KS-1404 anchor wiring)' "$PROMPT_FILE" && has 'FROM coagent@agentmail.to' && has 'reports/2026-10-05-ks1401-1383-g61r2/' || { echo "REFUSING: the verdict subject / sender / report dir" >&2; exit 23; }
_ANY_OVR="$(env | grep -c '^G61R2_')"
NOTE="#$PR T1 round 2 ${_h:0:12} at branch AND pull/head, parent ${R1_HEAD:0:12} | origin develop ${CUR_DEV:-UNREAD} (recorded, not refused)"
if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  $NOTE"
  echo "  prompt, QA project and repo present; kit at its home; thinking directive; every kit file + the round-1 report (hash) + the seat brief named; no unfilled token"
  echo "  the prompt carries 37 by-name keywords (as tokens), the round-2 checks, the holds + named exceptions, the GO string with the KS-1404 clause, the addendum + REPORT-HASH-LAST rules, the verdict subject + report dir, the head in full"
  [ "$_ANY_OVR" != 0 ] && echo "  (a G61R2_* TEST OVERRIDE is set)"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"
  exit 0
fi
[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — run this launcher in a cockpit pane, never inside a Bash tool" >&2; exit 21; }
[ "$_ANY_OVR" = 0 ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions "$(cat "$PROMPT_FILE")"
