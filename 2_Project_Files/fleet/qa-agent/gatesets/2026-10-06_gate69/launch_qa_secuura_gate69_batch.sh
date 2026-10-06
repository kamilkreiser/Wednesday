#!/bin/bash
# launch_qa_secuura_gate69_batch.sh — cross-project QA agent, ONE BATCHED gate (gate69) over Secuura/Blockchain #1395 (KS-1305, T1) and,
# when included, PR B (KS-1256, T1; #1396 at drafting). THE HEADS ARE PARAMETERS: repin_and_launch_gate69.sh renders prompt_gate69.txt ->
# prompt_gate69.rendered.txt and writes head_at_launch.txt (lines `A <pr> <branch> <sha>` and, if included, `B <pr> <branch> <sha>`);
# this launcher reads ONLY those two files. Every run re-reads origin: each PR's refs/pull/<n>/head AND its branch must equal its head (exit 6).
# exit 2: QA project missing / launcher not in its kit dir (a MOVED KIT).   exit 3/4/5: kit / prompt / repo missing.
# exit 7: head_at_launch.txt missing, malformed, or B listed without a PR number.
# exit 8: thinking directive / kit files named / report dir / an unfilled token or [[B]] marker / the GO strings (exactly one per included PR,
#         the pre-ruled seats) / a GO naming a forbidden seat / a head not named in full.
# exit 33: by-name keywords (as tokens) + measurement rules.   exit 39: HOLDS + named exceptions.
# exit 25: MERGE ADDENDUM + REPORT-HASH-LAST + verdict subject + sender.   exit 6: origin pull/head or branch != a head.
# exit 17: origin develop does not descend from 3f9ff4e1e1b9 (both PRs' merge-base).   exit 21: a LAUNCH (not --check) with stdin not a TTY.
# exit 16: a launch with a G69_* test override set.   Test overrides (--check only): G69_PROMPT, G69_HEADFILE, G69_LS.
# Opus by the configured default: the exec line carries NO --model.   Usage: launch_qa_secuura_gate69_batch.sh [--check]
set -u
MODE="${1:-}"   # captured FIRST: the head-file parsing below re-uses the positional parameters
QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
GS='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-06_gate69'
PROMPT_FILE="${G69_PROMPT:-$GS/prompt_gate69.rendered.txt}"
HEADFILE="${G69_HEADFILE:-$GS/head_at_launch.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
BASE_SHA='3f9ff4e1e1b93e2e704918a7825f13a72c9ec76f'
REPORT='2026-10-06-gate69-batch'
[ -d "$QA_DIR" ]      || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
_here="$(dirname "$(/bin/realpath "$0")")"
[ "$_here" = "$GS" ]  || { echo "REFUSING: this launcher lives in $_here but was written for $GS (a MOVED KIT)" >&2; exit 2; }
[ -s "$GS/kit.json" ] || { echo "kit.json missing: $GS" >&2; exit 3; }
[ -s "$PROMPT_FILE" ] || { echo "prompt file missing or empty: $PROMPT_FILE (render it with repin_and_launch_gate69.sh)" >&2; exit 4; }
[ -d "$REPO" ]        || { echo "repo under test missing: $REPO" >&2; exit 5; }
[ -s "$HEADFILE" ]    || { echo "REFUSING: $HEADFILE missing" >&2; exit 7; }
A_LINE="$(grep '^A ' "$HEADFILE")"; B_LINE="$(grep '^B ' "$HEADFILE")"
set -- $A_LINE; A_PR="${2:-}"; A_BR="${3:-}"; A_SHA="${4:-}"
[ "$A_PR" = 1395 ] && printf '%s' "$A_SHA" | grep -qE '^[0-9a-f]{40}$' && [ -n "$A_BR" ] || { echo "REFUSING: head file A line malformed: '$A_LINE'" >&2; exit 7; }
B_IN=0; B_PR=''; B_BR=''; B_SHA=''
if [ -n "$B_LINE" ]; then
  set -- $B_LINE; B_PR="${2:-}"; B_BR="${3:-}"; B_SHA="${4:-}"; B_IN=1
  printf '%s' "$B_PR" | grep -qE '^[0-9]+$' && printf '%s' "$B_SHA" | grep -qE '^[0-9a-f]{40}$' && [ -n "$B_BR" ] || { echo "REFUSING: head file B line malformed (PR number, branch and 40-hex head required): '$B_LINE'" >&2; exit 7; }
fi
set --
[ "$(head -n 1 "$PROMPT_FILE")" = "ultrathink" ] || { echo "REFUSING: the prompt does not open with the thinking directive" >&2; exit 8; }
for _f in README.md kit.json lib_gate69.py composee5_copy.py c1_pin_gate69.py c2_product_gate69.py c3_tests_gate69.py c4_docs_gate69.py gh_gate69.py; do
  [ -s "$GS/$_f" ] && grep -qF "$GS/$_f" "$PROMPT_FILE" || { echo "REFUSING: the kit file $GS/$_f is missing, empty, or not named in the prompt" >&2; exit 8; }
done
grep -qE '\{\{[A-Z0-9_]+\}\}|\[\[/?N?O?B\]\]' "$PROMPT_FILE"           && { echo "REFUSING: an unfilled double-brace token or a [[B]] / [[NOB]] marker (render with repin_and_launch_gate69.sh)" >&2; exit 8; }
grep -qF "reports/$REPORT/" "$PROMPT_FILE"                            || { echo "REFUSING: the prompt does not name the report dir $REPORT" >&2; exit 8; }
_GO="$(grep -oE 'GO \(Seat [A-Z] [0-9]+(st|nd|rd|th)\): merge [0-9]+ on gate69' "$PROMPT_FILE" | sort -u)"
_WANT="GO (Seat R 2nd): merge 1395 on gate69"; [ "$B_IN" = 1 ] && _WANT="$(printf '%s\n%s' "GO (Seat E 8th): merge $B_PR on gate69" "$_WANT" | sort -u)"
[ "$_GO" = "$_WANT" ]                                                 || { echo "REFUSING: the GO strings must be exactly the pre-ruled set ($(printf '%s' "$_WANT" | tr '\n' '|')), found: $(printf '%s' "$_GO" | tr '\n' '|')" >&2; exit 8; }
for _x in 'GO (Seat R 1st)' 'GO (Seat E 6th)' 'GO (Seat E 7th)'; do
  grep -qF "$_x" "$PROMPT_FILE" && grep -F "$_x" "$PROMPT_FILE" | grep -qvF 'SUPERSEDED' && { echo "REFUSING: the prompt names a forbidden seat in a GO outside the SUPERSEDED note: $_x" >&2; exit 8; }
done
grep -qwF "$A_SHA" "$PROMPT_FILE"                                     || { echo "REFUSING: the prompt does not name the #1395 head $A_SHA in full" >&2; exit 8; }
if [ "$B_IN" = 1 ]; then grep -qwF "$B_SHA" "$PROMPT_FILE" && grep -qF "#$B_PR" "$PROMPT_FILE" || { echo "REFUSING: the prompt does not name PR B #$B_PR / head $B_SHA in full" >&2; exit 8; }
else grep -qF 'NOT IN THIS GATE' "$PROMPT_FILE" || { echo "REFUSING: an A-only render must say PR B is NOT IN THIS GATE" >&2; exit 8; }; fi
PROMPT_JOINED="$(python3 -c 'import re,sys; print(re.sub(r"\n\s*", " ", open(sys.argv[1], encoding="utf-8").read()))' "$PROMPT_FILE")"
has() { printf '%s' "$PROMPT_JOINED" | grep -qF -- "$1"; }
has 'MEASURE, not conclude' && has 'RULE WHETHER IT BLOCKS' && has 'NAMES THE TREE' && has 'A check that prints nothing needs a control that prints' && has 'ASSERT THE FILENAME TOO' && has 'A SKIP is NEVER a pass' && has 'NOT RUN is never a pass' && has 'A LOAD FAILURE IS NOT A RED' && has 'A LOAD FAILURE IS NEVER "NOT CAUGHT"' && has 'NEWLINE-TOLERANT' && has 'THE HEAD IS A PARAMETER' && has 'THE TAIL RULE' && has 'ONE RED ARM PER CONJUNCT' || { echo "REFUSING: the measurement rules / head-parameter rule / TAIL rule / per-conjunct rule" >&2; exit 33; }
_KW="C1-PIN END-TREE NO-TRAILER NO-COAUTHOR SUBJECT-EXACT NO-NEW-LEG C2-A-PRODUCT TENANT-UNTOUCHED GUARD-CONJUNCTS SECTION-5D C3-RED-FIRST C3-SUITE C3-TSC C3-TYPE-UNCHECKED C3-TAMPER-MATRIX REAL-SHAPE CELL-ORDER C4-DOCS C4-CONTAINMENT H2-TOLERANT C4-MERGE-IN Q-M TAIL-ORDER C5-PR-TEXT CLOSING-WORD KEYSCAN-OWN-KEY PR-BODY-CLAIMS C6-NOT-COVERED ACTIONS-COMPARE MERGEABLE-STATE READY-CLAIMS PREFLIGHT-INCOMPLETE COLLISION-CENSUS NOT-TESTED-LIST TIERING DISK-ENOSPC REPORT-HASH-LAST"
[ "$B_IN" = 1 ] && _KW="$_KW C2-B-PRODUCT AVAILABILITY-BEFORE-READ DOUBLES-SCOPE KS1195-REPOINT DB-RETRY-CLASSIFY"
_NKW=0
for _w in $_KW; do
  _NKW=$((_NKW + 1))
  printf '%s' "$PROMPT_JOINED" | grep -qE -- "(^|[^A-Za-z0-9-])$_w([^A-Za-z0-9-]|\$)" || { echo "REFUSING: the prompt does not carry the by-name keyword '$_w'" >&2; exit 33; }
done
has 'NO MERGE, NO PUSH to any PR branch, NO ticket state change' && has 'NEVER WRITE THE SHARED CHECKOUT' && has 'Never `rm`' && has 'No `az` command of any kind' && has 'You NEVER reply to Peter' && has 'never `git fetch` into the shared checkout' && has 'THE NAMED EXCEPTIONS to those holds — these and NO others' && has 'You never touch GitHub PR #1278 or #1245' && has 'no Docker' && has 'NEVER export GIT_SSH_COMMAND' || { echo "REFUSING: the HOLDS" >&2; exit 39; }
has '## MERGE ADDENDUM' && has 'is the LAST thing you write to report.md' && has 'sha256 report.md = <hex>' && has 'EVERY SUBJECT YOU PROPOSE MUST BE TRUE OF THE DIFF' && has 'FROM coagent@agentmail.to' && has 'NOT-TESTED.written-first.md' \
  && grep -qF -- "$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["verdict_subject"])' "$GS/kit.json")" "$PROMPT_FILE" || { echo "REFUSING: MERGE ADDENDUM / REPORT-HASH-LAST / verdict subject / sender" >&2; exit 25; }
REFS="refs/heads/develop refs/pull/1395/head refs/heads/$A_BR"; [ "$B_IN" = 1 ] && REFS="$REFS refs/pull/$B_PR/head refs/heads/$B_BR"
if [ -n "${G69_LS:-}" ]; then _LS="$(cat "$G69_LS")"; else _LS="$(git -C "$REPO" ls-remote origin $REFS)"; fi
get() { printf '%s\n' "$_LS" | awk -v r="$1" '$2==r{print $1}'; }
CUR_DEV="$(get refs/heads/develop)"
[ "$(get refs/pull/1395/head)" = "$A_SHA" ] && [ "$(get "refs/heads/$A_BR")" = "$A_SHA" ] || { echo "REFUSING: #1395 pull/head '$(get refs/pull/1395/head)' / branch '$(get "refs/heads/$A_BR")' != $A_SHA — a verdict is valid ONLY at its head" >&2; exit 6; }
if [ "$B_IN" = 1 ]; then
  [ "$(get "refs/pull/$B_PR/head")" = "$B_SHA" ] && [ "$(get "refs/heads/$B_BR")" = "$B_SHA" ] || { echo "REFUSING: #$B_PR pull/head '$(get "refs/pull/$B_PR/head")' / branch '$(get "refs/heads/$B_BR")' != $B_SHA" >&2; exit 6; }
fi
if git -C "$REPO" cat-file -t "$CUR_DEV" >/dev/null 2>&1; then
  git -C "$REPO" merge-base --is-ancestor "$BASE_SHA" "$CUR_DEV" || { echo "REFUSING: origin develop $CUR_DEV does not descend from $BASE_SHA" >&2; exit 17; }
  _DEVNOTE="descends from ${BASE_SHA:0:12}"
else
  _DEVNOTE="NOT in the local store: descent NOT checked here (the gate checks it in ITS OWN clone, X7; the repin script checked it in the kit clone)"
fi
_ANY_OVR="$(env | grep -c '^G69_')"
NOTE="#1395 ${A_SHA:0:12}$([ "$B_IN" = 1 ] && echo " + #$B_PR ${B_SHA:0:12}" || echo ' (PR B NOT INCLUDED)') at pull/head AND branch | origin develop ${CUR_DEV:0:12} RECORDED ($_DEVNOTE) | $(printf '%s' "$_GO" | tr '\n' '|') | prompt sha256 $(shasum -a 256 "$PROMPT_FILE" | cut -c1-16)"
if [ "$MODE" = "--check" ]; then
  echo "all guards pass:"; echo "  $NOTE"
  echo "  QA project, kit, rendered prompt, head file, repo present; kit at its home; thinking directive; 9 kit files named; report dir; no fill token / marker; the pre-ruled GO set; no forbidden seat; heads in full"
  echo "  the prompt carries the measurement rules, the head-parameter / TAIL / per-conjunct rules, $_NKW by-name keywords (as tokens), the holds + named exceptions, the addendum + REPORT-HASH-LAST rules, the verdict subject + sender"
  [ "$_ANY_OVR" != 0 ] && echo "  (a G69_* TEST OVERRIDE is set)"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"; exit 0
fi
[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — run this launcher in a cockpit pane, never inside a Bash tool" >&2; exit 21; }
[ "$_ANY_OVR" = 0 ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions "$(cat "$PROMPT_FILE")"
