#!/bin/bash
# launch_qa_secuura_ks1278_1393r2.sh — cross-project QA agent, ONE gate (gate68) over ONE Secuura/Blockchain PR, FROZEN at ONE:
# #1393 KS-1278 ROUND 2 OF 2 (T1): the guarded revoke UPDATE keyed on the row the read resolved. Author Seat B 65th; merger named at
# launch. Adapted from gate67's launcher. THE HEAD IS A PARAMETER: repin_and_launch_gate68.sh renders prompt_gate68.txt ->
# prompt_gate68.rendered.txt ({{MERGE_SEAT}}, {{HEAD}}) and writes head_at_launch.txt; this launcher reads ONLY those two files.
# Every run re-reads origin: refs/pull/1393/head AND the branch must equal head_at_launch.txt (exit 6).
# exit 2: QA project missing / launcher not in its kit dir (a MOVED KIT).   exit 3/4/5: kit / prompt / repo missing.
# exit 7: head_at_launch.txt missing or not a 40-hex sha.
# exit 8: thinking directive / kit files named / report dir / exactly ONE GO string / a GO naming Seat B 63rd, 64th or 65th / head in full /
#         an unfilled token.   exit 33: by-name keywords (as tokens) + measurement rules.   exit 39: HOLDS + named exceptions.
# exit 25: MERGE ADDENDUM + REPORT-HASH-LAST + verdict subject + sender.   exit 6: origin pull/head or branch != the head.
# exit 17: origin develop does not descend from the branch base 32e058975d4e.   exit 21: a LAUNCH (not --check) with stdin not a TTY.
# exit 16: a launch with a G68_* test override set.   Test overrides (--check only): G68_PROMPT, G68_HEADFILE, G68_LS.
# Opus by the configured default: the exec line carries NO --model.   Usage: launch_qa_secuura_ks1278_1393r2.sh [--check]
set -u
QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
GS='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-06_gate68'
PROMPT_FILE="${G68_PROMPT:-$GS/prompt_gate68.rendered.txt}"
HEADFILE="${G68_HEADFILE:-$GS/head_at_launch.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
PR='1393'
BASE_SHA='32e058975d4e3a9bbabe828f45e7084de4cfa7f0'
BRANCH='refs/heads/feature/ks-1278-revoke-atomic-b63-1'
REPORT='2026-10-06-ks1278-1393r2-g68'
[ -d "$QA_DIR" ]      || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
_here="$(dirname "$(/bin/realpath "$0")")"
[ "$_here" = "$GS" ]  || { echo "REFUSING: this launcher lives in $_here but was written for $GS (a MOVED KIT)" >&2; exit 2; }
[ -s "$GS/kit.json" ] || { echo "kit.json missing: $GS" >&2; exit 3; }
[ -s "$PROMPT_FILE" ] || { echo "prompt file missing or empty: $PROMPT_FILE (render it with repin_and_launch_gate68.sh)" >&2; exit 4; }
[ -d "$REPO" ]        || { echo "repo under test missing: $REPO" >&2; exit 5; }
HEAD_SHA="$(tr -d ' \n' < "$HEADFILE" 2>/dev/null)"
printf '%s' "$HEAD_SHA" | grep -qE '^[0-9a-f]{40}$' || { echo "REFUSING: $HEADFILE missing or not a 40-hex sha (got '$HEAD_SHA')" >&2; exit 7; }
[ "$(head -n 1 "$PROMPT_FILE")" = "ultrathink" ] || { echo "REFUSING: the prompt does not open with the thinking directive" >&2; exit 8; }
for _f in README.md kit.json lib_gate68.py composee5_copy.py c1_pin_gate68.py c2_product_gate68.py c3_tests_gate68.py c3b_pgprobe_gate68.py c4_docs_gate68.py gh_gate68.py; do
  [ -s "$GS/$_f" ] && grep -qF "$GS/$_f" "$PROMPT_FILE" || { echo "REFUSING: the kit file $GS/$_f is missing, empty, or not named in the prompt" >&2; exit 8; }
done
grep -qE '\{\{[A-Z0-9_]+\}\}' "$PROMPT_FILE"                     && { echo "REFUSING: an unfilled double-brace token (render with repin_and_launch_gate68.sh)" >&2; exit 8; }
grep -qF "reports/$REPORT/" "$PROMPT_FILE"                       || { echo "REFUSING: the prompt does not name the report dir $REPORT" >&2; exit 8; }
_GO="$(grep -oE 'GO \(Seat B [0-9]+(st|nd|rd|th)\): merge 1393 on gate68' "$PROMPT_FILE" | sort -u)"
[ "$(printf '%s\n' "$_GO" | grep -c .)" = 1 ]                    || { echo "REFUSING: the prompt must carry exactly ONE GO string 'GO (Seat B <NNth>): merge 1393 on gate68' (found: $(printf '%s' "$_GO" | tr '\n' '|'))" >&2; exit 8; }
grep -qF 'GO (Seat B 63rd)' "$PROMPT_FILE"                       && { echo "REFUSING: the prompt names Seat B 63rd in a GO" >&2; exit 8; }
grep -qF 'GO (Seat B 64th)' "$PROMPT_FILE"                       && { echo "REFUSING: the prompt names Seat B 64th in a GO" >&2; exit 8; }
grep -qF 'GO (Seat B 65th)' "$PROMPT_FILE"                       && { echo "REFUSING: the prompt names Seat B 65th (the author, wrapping cold) in a GO" >&2; exit 8; }
grep -qwF "$HEAD_SHA" "$PROMPT_FILE"                             || { echo "REFUSING: the prompt does not name the head $HEAD_SHA in full" >&2; exit 8; }
PROMPT_JOINED="$(python3 -c 'import re,sys; print(re.sub(r"\n\s*", " ", open(sys.argv[1], encoding="utf-8").read()))' "$PROMPT_FILE")"
has() { printf '%s' "$PROMPT_JOINED" | grep -qF -- "$1"; }
has 'MEASURE, not conclude' && has 'RULE WHETHER IT BLOCKS' && has 'NAMES THE TREE' && has 'A check that prints nothing needs a control that prints' && has 'ASSERT THE FILENAME TOO' && has 'A SKIP is NEVER a pass' && has 'NOT RUN is never a pass' && has 'A LOAD FAILURE IS NOT A RED' && has 'A LOAD FAILURE IS NEVER "NOT CAUGHT"' && has 'NEWLINE-TOLERANT' && has 'ROUND 2 OF 2' && has 'THE HEAD IS A PARAMETER' || { echo "REFUSING: the measurement rules / round cap / head-parameter rule" >&2; exit 33; }
for _w in C1-PIN END-TREE NO-TRAILER NO-COAUTHOR SUBJECT-EXACT NO-NEW-LEG FOLLOW-UP-SCOPE C2-PRODUCT C2-KEY-SHAPE C2-UUID-CAST C2-N3-BYTE-IDENTICAL C2-CENSUS C2-SECTION-5D C3-RED-FIRST C3-SUITE C3-TSC C3-TYPE-UNCHECKED C3-TAMPER-MATRIX C3-REAL-POSTGRES C4-DOCS C4-CONTAINMENT H2-TOLERANT C4-MERGE-IN Q-M KEY-ANCHORED C5-PR-TEXT CLOSING-WORD KEYSCAN-OWN-KEY PR-BODY-CLAIMS KS1419-CORRECTION KS1424-EXISTS C6-NOT-COVERED ACTIONS-COMPARE MERGEABLE-STATE READY-CLAIMS PREFLIGHT-INCOMPLETE ROUND1-FINDINGS COLLISION-CENSUS NOT-TESTED-LIST TIERING ROUND-CAP DISK-ENOSPC REPORT-HASH-LAST; do
  printf '%s' "$PROMPT_JOINED" | grep -qE -- "(^|[^A-Za-z0-9-])$_w([^A-Za-z0-9-]|\$)" || { echo "REFUSING: the prompt does not carry the by-name keyword '$_w'" >&2; exit 33; }
done
has 'NO MERGE, NO PUSH to any PR branch, NO ticket state change' && has 'NEVER WRITE THE SHARED CHECKOUT' && has 'Never `rm`' && has 'No `az` command of any kind' && has 'You NEVER reply to Peter' && has 'never `git fetch` into the shared checkout' && has 'THE NAMED EXCEPTIONS to those holds — these and NO others' && has 'TICKET STATE IS WEDNESDAY' && has 'You never touch GitHub PR #1278 or #1245' && has 'no Docker' && has 'NEVER export GIT_SSH_COMMAND' || { echo "REFUSING: the HOLDS" >&2; exit 39; }
has '## MERGE ADDENDUM' && has 'is the LAST thing you write to report.md' && has 'sha256 report.md = <hex>' && has 'EVERY SUBJECT YOU PROPOSE MUST BE TRUE OF THE DIFF' && has 'FROM coagent@agentmail.to' && has 'NOT-TESTED.written-first.md' \
  && grep -qF -- "$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["verdict_subject"])' "$GS/kit.json")" "$PROMPT_FILE" || { echo "REFUSING: MERGE ADDENDUM / REPORT-HASH-LAST / verdict subject / sender" >&2; exit 25; }
if [ -n "${G68_LS:-}" ]; then _LS="$(cat "$G68_LS")"; else _LS="$(git -C "$REPO" ls-remote origin refs/heads/develop "$BRANCH" "refs/pull/$PR/head")"; fi
CUR_DEV="$(printf '%s\n' "$_LS" | awk '$2=="refs/heads/develop"{print $1}')"
_PH="$(printf '%s\n' "$_LS" | awk -v r="refs/pull/$PR/head" '$2==r{print $1}')"; _BH="$(printf '%s\n' "$_LS" | awk -v r="$BRANCH" '$2==r{print $1}')"
[ "$_PH" = "$HEAD_SHA" ] && [ "$_BH" = "$HEAD_SHA" ] || { echo "REFUSING: #$PR pull/head '$_PH' / branch '$_BH' != the head $HEAD_SHA (head_at_launch.txt) — a verdict is valid ONLY at its head" >&2; exit 6; }
if git -C "$REPO" cat-file -t "$CUR_DEV" >/dev/null 2>&1; then
  git -C "$REPO" merge-base --is-ancestor "$BASE_SHA" "$CUR_DEV" || { echo "REFUSING: origin develop $CUR_DEV does not descend from the branch base $BASE_SHA" >&2; exit 17; }
  _DEVNOTE="descends from the branch base ${BASE_SHA:0:12}"
else
  _DEVNOTE="NOT in the local store: descent NOT checked here (the gate checks P2 in ITS OWN clone, X7)"
fi
_ANY_OVR="$(env | grep -c '^G68_')"
NOTE="#$PR T1 ROUND 2 ${HEAD_SHA:0:12} at branch AND pull/head | origin develop ${CUR_DEV:0:12} RECORDED ($_DEVNOTE) | $_GO | prompt sha256 $(shasum -a 256 "$PROMPT_FILE" | cut -c1-16)"
if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"; echo "  $NOTE"
  echo "  QA project, kit, rendered prompt, head file, repo present; kit at its home; thinking directive; 10 kit files named; report dir; ONE GO string; no GO naming Seat B 63rd / 64th / 65th; head in full; no fill token"
  echo "  the prompt carries the measurement rules, the round cap, the head-parameter rule, 43 by-name keywords (as tokens), the holds + named exceptions, the addendum + REPORT-HASH-LAST rules, the verdict subject + sender"
  [ "$_ANY_OVR" != 0 ] && echo "  (a G68_* TEST OVERRIDE is set)"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"; exit 0
fi
[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — run this launcher in a cockpit pane, never inside a Bash tool" >&2; exit 21; }
[ "$_ANY_OVR" = 0 ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions "$(cat "$PROMPT_FILE")"
