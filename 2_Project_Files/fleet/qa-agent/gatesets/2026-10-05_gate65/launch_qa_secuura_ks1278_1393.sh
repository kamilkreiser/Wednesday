#!/bin/bash
# launch_qa_secuura_ks1278_1393.sh — cross-project QA agent, ONE gate (gate65) over ONE Secuura/Blockchain PR, FROZEN at ONE:
# #1393 KS-1278 (T1, ROUND 1): revoke decides "already revoked" in the UPDATE, not only on the read (audit / integrity path:
# action_provenance + revoke anchor). Author Seat B 63rd (wrapping); merger Seat B 64th. STATIC prompt (no fill step): the head is written
# into the prompt and this launcher; every run re-reads origin, so a moved HEAD refuses. develop is RECORDED, never refused (the head's
# parent is 32e058975d4e, not develop, so the merge always needs Seat B 64th's docs merge-in, judged by Q-M); refused only if it does not
# descend from the base.
# exit 2: QA project missing, or this launcher is not in its kit dir (a MOVED KIT).   exit 3/4/5: kit / prompt / repo missing.
# exit 8: thinking directive / kit files named / report dir / GO string (Seat B 64th) / a GO naming Seat B 63rd / head in full /
#         an unfilled token.   exit 33: the by-name keywords (as tokens) + measurement rules.   exit 39: the HOLDS + named exceptions.
# exit 25: MERGE ADDENDUM + REPORT-HASH-LAST + verdict subject + sender.
# exit 6: origin refs/pull/1393/head or the exact branch is not the pinned head.   exit 17: origin develop does not descend from the base.
# exit 21: a LAUNCH (not --check) refuses when stdin is not a TTY.   exit 16: a launch with a G65_* test override set.
# Test overrides (--check only): G65_PROMPT (another prompt file), G65_LS (a file standing in for the ls-remote output).
# Opus by the configured default: the exec line carries NO --model.   Usage: launch_qa_secuura_ks1278_1393.sh [--check]
set -u
QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
GS='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-05_gate65'
PROMPT_FILE="${G65_PROMPT:-$GS/prompt_gate65.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
PR='1393'
HEAD_SHA='4a1620588819a35c180fb1a4a3d98d35f4814f3f'
BASE_SHA='32e058975d4e3a9bbabe828f45e7084de4cfa7f0'
BRANCH='refs/heads/feature/ks-1278-revoke-atomic-b63-1'
REPORT='2026-10-05-ks1278-1393-g65'
[ -d "$QA_DIR" ]      || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
_here="$(dirname "$(/bin/realpath "$0")")"
[ "$_here" = "$GS" ]  || { echo "REFUSING: this launcher lives in $_here but was written for $GS (a MOVED KIT)" >&2; exit 2; }
[ -s "$GS/kit.json" ] || { echo "kit.json missing: $GS" >&2; exit 3; }
[ -s "$PROMPT_FILE" ] || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]        || { echo "repo under test missing: $REPO" >&2; exit 5; }
[ "$(head -n 1 "$PROMPT_FILE")" = "ultrathink" ] || { echo "REFUSING: the prompt does not open with the thinking directive" >&2; exit 8; }
for _f in README.md kit.json lib_gate65.py c1_pin_gate65.py c2_product_gate65.py c3_tests_gate65.py c3b_security_gate65.py c4_docs_gate65.py c5_prtext_gate65.py gh_census_gate65.py; do
  [ -s "$GS/$_f" ] && grep -qF "$GS/$_f" "$PROMPT_FILE" || { echo "REFUSING: the kit file $GS/$_f is missing, empty, or not named in the prompt" >&2; exit 8; }
done
grep -qF "reports/$REPORT/" "$PROMPT_FILE"                       || { echo "REFUSING: the prompt does not name the report dir $REPORT" >&2; exit 8; }
grep -qF 'GO (Seat B 64th): merge 1393 on gate65' "$PROMPT_FILE" || { echo "REFUSING: the prompt does not carry the GO string (Seat B 64th)" >&2; exit 8; }
grep -qF 'GO (Seat B 63rd)' "$PROMPT_FILE"                       && { echo "REFUSING: the prompt names Seat B 63rd (the wrapping author) in a GO" >&2; exit 8; }
grep -qwF "$HEAD_SHA" "$PROMPT_FILE"                             || { echo "REFUSING: the prompt does not name the head in full" >&2; exit 8; }
grep -qE '\{\{[A-Z0-9_]+\}\}' "$PROMPT_FILE"                     && { echo "REFUSING: an unfilled double-brace token" >&2; exit 8; }
PROMPT_JOINED="$(python3 -c 'import re,sys; print(re.sub(r"\n\s*", " ", open(sys.argv[1], encoding="utf-8").read()))' "$PROMPT_FILE")"
has() { printf '%s' "$PROMPT_JOINED" | grep -qF -- "$1"; }
has 'MEASURE, not conclude' && has 'RULE WHETHER IT BLOCKS' && has 'NAMES THE TREE' && has 'A check that prints nothing needs a control that prints' && has 'ASSERT THE FILENAME TOO' && has 'A SKIP is NEVER a pass' && has 'NOT RUN is never a pass' && has 'A LOAD FAILURE IS NOT A RED' || { echo "REFUSING: the measurement rules" >&2; exit 33; }
for _w in C1-PIN END-TREE NO-TRAILER NO-COAUTHOR SUBJECT-EXACT NO-NEW-LEG C2-PRODUCT C2-PARAMETERISED C2-OPT-IN C2-SECTION-5D C3-RED-FIRST C3-TAMPER C3-BLIND-SPOT C3-SUITE C3-TSC C3B-SECURITY C3B-NULL-MEANINGS C4-DOCS C4-PLACEMENT C4-MERGE-IN Q-M C5-PR-TEXT CLOSING-WORD KEYSCAN-OWN-KEY C5-RESIDUAL C6-NOT-COVERED READY-CLAIMS PR-BODY-CLAIMS PREFLIGHT-INCOMPLETE COLLISION-CENSUS NOT-TESTED-LIST TIERING DISK-ENOSPC REPORT-HASH-LAST KEY-ANCHORED; do
  printf '%s' "$PROMPT_JOINED" | grep -qE -- "(^|[^A-Za-z0-9-])$_w([^A-Za-z0-9-]|\$)" || { echo "REFUSING: the prompt does not carry the by-name keyword '$_w'" >&2; exit 33; }
done
has 'NO MERGE, NO PUSH to any PR branch, NO ticket state change' && has 'NEVER WRITE THE SHARED CHECKOUT' && has 'Never `rm`' && has 'No `az` command of any kind' && has 'You NEVER reply to Peter' && has 'never `git fetch` into the shared checkout' && has 'THE NAMED EXCEPTIONS to those holds — these and NO others' && has 'TICKET STATE IS WEDNESDAY' && has 'You never touch GitHub PR #1278 or #1245' || { echo "REFUSING: the HOLDS" >&2; exit 39; }
has '## MERGE ADDENDUM' && has 'is the LAST thing you write to report.md' && has 'sha256 report.md = <hex>' && has 'EVERY SUBJECT YOU PROPOSE MUST BE TRUE OF THE DIFF' && has 'FROM coagent@agentmail.to' && has 'NOT-TESTED.written-first.md' \
  && grep -qF -- "$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["verdict_subject"])' "$GS/kit.json")" "$PROMPT_FILE" || { echo "REFUSING: MERGE ADDENDUM / REPORT-HASH-LAST / verdict subject / sender" >&2; exit 25; }
if [ -n "${G65_LS:-}" ]; then _LS="$(cat "$G65_LS")"; else _LS="$(git -C "$REPO" ls-remote origin refs/heads/develop "$BRANCH" "refs/pull/$PR/head")"; fi
CUR_DEV="$(printf '%s\n' "$_LS" | awk '$2=="refs/heads/develop"{print $1}')"
_PH="$(printf '%s\n' "$_LS" | awk -v r="refs/pull/$PR/head" '$2==r{print $1}')"; _BH="$(printf '%s\n' "$_LS" | awk -v r="$BRANCH" '$2==r{print $1}')"
[ "$_PH" = "$HEAD_SHA" ] && [ "$_BH" = "$HEAD_SHA" ] || { echo "REFUSING: #$PR pull/head '$_PH' / branch '$_BH' != the pinned head $HEAD_SHA — a verdict is valid ONLY at its head (RE-DRAFT, README section 8)" >&2; exit 6; }
if git -C "$REPO" cat-file -t "$CUR_DEV" >/dev/null 2>&1; then
  git -C "$REPO" merge-base --is-ancestor "$BASE_SHA" "$CUR_DEV" || { echo "REFUSING: origin develop $CUR_DEV does not descend from the base $BASE_SHA (history rewritten?)" >&2; exit 17; }
  _DEVNOTE="descends from the base ${BASE_SHA:0:12}"
else
  _DEVNOTE="NOT in the local store: descent NOT checked here (the repin script uses the compare API when develop MOVED; the gate checks P2 in ITS OWN clone, X7)"
fi
_ANY_OVR="$(env | grep -c '^G65_')"
NOTE="#$PR T1 ${HEAD_SHA:0:12} at branch AND pull/head | origin develop ${CUR_DEV:0:12} RECORDED ($_DEVNOTE) | prompt sha256 $(shasum -a 256 "$PROMPT_FILE" | cut -c1-16)"
if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"; echo "  $NOTE"
  echo "  QA project, kit, prompt, repo present; kit at its home; thinking directive; 10 kit files named; report dir; GO string (Seat B 64th); no GO naming Seat B 63rd; head in full; no fill token"
  echo "  the prompt carries the measurement rules, 36 by-name keywords (as tokens), the holds + named exceptions, the addendum + REPORT-HASH-LAST rules, the verdict subject + sender"
  [ "$_ANY_OVR" != 0 ] && echo "  (a G65_* TEST OVERRIDE is set)"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"; exit 0
fi
[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — run this launcher in a cockpit pane, never inside a Bash tool" >&2; exit 21; }
[ "$_ANY_OVR" = 0 ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions "$(cat "$PROMPT_FILE")"
