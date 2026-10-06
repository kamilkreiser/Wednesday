#!/bin/bash
# launch_qa_secuura_gate70.sh — cross-project QA agent, ONE T1 gate (gate70, round 1 of 2) over Secuura/Blockchain #1397 (KS-1425):
# an in-range LOCK-ONLY refresh + 2 baseline rows. THE HEAD IS A PARAMETER: repin_and_launch_gate70.sh renders prompt_gate70.txt ->
# prompt_gate70.rendered.txt and writes head_at_launch.txt (one line `P 1397 <branch> <sha>`); this launcher reads ONLY those two files.
# Every run (--check included) re-hashes EVERY pinned kit file against kit.json `script_sha256` and re-reads origin by ls-remote.
# exit 2: QA project missing / launcher not in its kit dir (a MOVED KIT).   exit 3: kit.json missing.   exit 4/5: prompt / repo missing.
# exit 30: a REQUIRED kit file is missing, empty, or has no pin in kit.json.   exit 31: a kit file's sha256 != its kit.json pin (BAD PIN).
# exit 7: head_at_launch.txt missing or malformed.
# exit 8: thinking directive / kit files named / report dir / an unfilled token / the GO string (exactly the pre-ruled one) /
#         a GO naming the author seat / the head not named in full.
# exit 33: measurement rules + by-name keywords (as tokens).   exit 39: HOLDS + named exceptions.
# exit 25: MERGE ADDENDUM + REPORT-HASH-LAST + verdict subject + sender.   exit 6: origin pull/head or branch != the head.
# exit 17: origin develop does not descend from 4eaf7741a6a4 (the PR's one parent).   exit 21: a LAUNCH (not --check) with stdin not a TTY.
# exit 16: a launch with a G70_* test override set.
# Test overrides (--check only): G70_PROMPT, G70_HEADFILE, G70_LS (an ls-remote stand-in), G70_KITJSON (a kit.json stand-in for the pin
# arms), G70_FILES_DIR (the directory whose files are hashed — a stand-in copy for the missing-file / tampered-file arms).
# Opus by the configured default: the exec line carries NO --model.   Usage: launch_qa_secuura_gate70.sh [--check]
set -u
MODE="${1:-}"
QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
GS='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-06_gate70'
PROMPT_FILE="${G70_PROMPT:-$GS/prompt_gate70.rendered.txt}"
HEADFILE="${G70_HEADFILE:-$GS/head_at_launch.txt}"
KITJSON="${G70_KITJSON:-$GS/kit.json}"
FILES_DIR="${G70_FILES_DIR:-$GS}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
URL='git@github.com:Secuura/Distributed_Secuura.git'
BASE_SHA='4eaf7741a6a4b2c82752d0d94f8bbacb5493aabe'
REPORT='2026-10-06-gate70'
GO_WANT='GO (Seat D 11th): merge 1397 on gate70'
REQUIRED='lib_gate70.py c1_pin_gate70.py c2_locks_gate70.py c3_registry_gate70.py c4_baseline_gate70.py c5_legs_gate70.py gh_gate70.py prompt_gate70.txt launch_qa_secuura_gate70.sh repin_and_launch_gate70.sh'
[ -d "$QA_DIR" ]      || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
_here="$(dirname "$(/bin/realpath "$0")")"
[ "$_here" = "$GS" ]  || { echo "REFUSING: this launcher lives in $_here but was written for $GS (a MOVED KIT)" >&2; exit 2; }
[ -s "$KITJSON" ]     || { echo "REFUSING: kit.json missing: $KITJSON" >&2; exit 3; }

# --- PINS: every REQUIRED file present, non-empty, pinned in kit.json, and hashing to its pin ---
_NPIN=0
for _f in $REQUIRED; do
  _want="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["script_sha256"].get(sys.argv[2],""))' "$KITJSON" "$_f" 2>/dev/null)"
  [ -s "$FILES_DIR/$_f" ] || { echo "REFUSING: the kit file $FILES_DIR/$_f is MISSING or empty" >&2; exit 30; }
  [ -n "$_want" ]         || { echo "REFUSING: the kit file $_f has NO sha256 pin in $KITJSON" >&2; exit 30; }
  _got="$(shasum -a 256 "$FILES_DIR/$_f" | cut -d' ' -f1)"
  [ "$_got" = "$_want" ]  || { echo "REFUSING: BAD PIN — $_f sha256 ${_got:0:16} != kit.json pin ${_want:0:16}" >&2; exit 31; }
  _NPIN=$((_NPIN + 1))
done

[ -s "$PROMPT_FILE" ] || { echo "prompt file missing or empty: $PROMPT_FILE (render it with repin_and_launch_gate70.sh)" >&2; exit 4; }
[ -d "$REPO" ]        || { echo "repo under test missing: $REPO" >&2; exit 5; }
[ -s "$HEADFILE" ]    || { echo "REFUSING: $HEADFILE missing" >&2; exit 7; }
P_LINE="$(grep '^P ' "$HEADFILE")"
set -- $P_LINE; P_PR="${2:-}"; P_BR="${3:-}"; P_SHA="${4:-}"; set --
[ "$P_PR" = 1397 ] && printf '%s' "$P_SHA" | grep -qE '^[0-9a-f]{40}$' && [ -n "$P_BR" ] && [ "$(grep -c '^P ' "$HEADFILE")" = 1 ] \
  || { echo "REFUSING: head file malformed (want exactly one line 'P 1397 <branch> <40-hex>'): '$P_LINE'" >&2; exit 7; }
[ "$(head -n 1 "$PROMPT_FILE")" = "ultrathink" ] || { echo "REFUSING: the prompt does not open with the thinking directive" >&2; exit 8; }
for _f in README.md RULINGS_wednesday.md; do   # unpinned (Wednesday edits them) but required
  [ -s "$FILES_DIR/$_f" ] || { echo "REFUSING: the kit file $FILES_DIR/$_f is MISSING or empty" >&2; exit 30; }
done
for _f in README.md kit.json lib_gate70.py c1_pin_gate70.py c2_locks_gate70.py c3_registry_gate70.py c4_baseline_gate70.py c5_legs_gate70.py gh_gate70.py; do
  grep -qF "$GS/$_f" "$PROMPT_FILE" || { echo "REFUSING: the kit file $GS/$_f is not named in the prompt" >&2; exit 8; }
done
grep -qE '\{\{[A-Z0-9_]+\}\}' "$PROMPT_FILE"                          && { echo "REFUSING: an unfilled double-brace token (render with repin_and_launch_gate70.sh)" >&2; exit 8; }
grep -qF "reports/$REPORT/" "$PROMPT_FILE"                            || { echo "REFUSING: the prompt does not name the report dir $REPORT" >&2; exit 8; }
_GO="$(grep -oE 'GO \(Seat [A-Z] [0-9]+(st|nd|rd|th)\): merge [0-9]+ on gate[0-9]+' "$PROMPT_FILE" | sort -u)"
[ "$_GO" = "$GO_WANT" ]                                               || { echo "REFUSING: the GO strings must be exactly the pre-ruled one ($GO_WANT), found: $(printf '%s' "$_GO" | tr '\n' '|')" >&2; exit 8; }
grep -qF 'GO (Seat D 10th)' "$PROMPT_FILE"                            && { echo "REFUSING: the prompt names the author seat (D 10th) in a GO" >&2; exit 8; }
grep -qwF "$P_SHA" "$PROMPT_FILE"                                     || { echo "REFUSING: the prompt does not name the head $P_SHA in full" >&2; exit 8; }
PROMPT_JOINED="$(python3 -c 'import re,sys; print(re.sub(r"\n\s*", " ", open(sys.argv[1], encoding="utf-8").read()))' "$PROMPT_FILE")"
has() { printf '%s' "$PROMPT_JOINED" | grep -qF -- "$1"; }
has 'MEASURE, not conclude' && has 'RULE WHETHER IT BLOCKS' && has 'NAMES THE TREE' && has 'A check that prints nothing needs a control that prints' && has 'ASSERT THE FILENAME TOO' && has 'ASSERT THE TAMPER LANDED' && has 'A SKIP is NEVER a pass' && has 'NOT RUN is never a pass' && has 'COULD-NOT-CHECK IS A SKIP' && has 'THE HEAD IS A PARAMETER' && has 'derived from the BASE ONLY' || { echo "REFUSING: the measurement rules / head-parameter rule / base-derived plan" >&2; exit 33; }
_KW="C1-PIN END-TREE NO-TRAILER NO-COAUTHOR SUBJECT-EXACT NO-NEW-LEG LOCK-DIFF FIELD-EXACT INDENT-KEPT TARBALL-INTEGRITY PARENT-WALK LEGS-BASE-HEAD AUDIT-CONTRACT CLEANROOM NEGATIVE-CONTROLS BASELINE-ROWS ROW-SHAPE FUSE NO-HIGH-BASELINED PSP7-PARSE MOBILE-UNTOUCHED INSTALL-NPM-CI C5-PR-TEXT CLOSING-WORD KEYSCAN-OWN-KEY PR-BODY-CLAIMS LINEAR-STATE ACTIONS-COMPARE MERGEABLE-STATE READY-CLAIMS PREFLIGHT-INCOMPLETE COLLISION-CENSUS NOT-TESTED-LIST TIERING DISK-ENOSPC REPORT-HASH-LAST"
_NKW=0
for _w in $_KW; do
  _NKW=$((_NKW + 1))
  printf '%s' "$PROMPT_JOINED" | grep -qE -- "(^|[^A-Za-z0-9-])$_w([^A-Za-z0-9-]|\$)" || { echo "REFUSING: the prompt does not carry the by-name keyword '$_w'" >&2; exit 33; }
done
has 'NO MERGE, NO PUSH to any PR branch, NO ticket state change' && has 'NEVER WRITE THE SHARED CHECKOUT' && has 'Never `rm`' && has 'No `az` command of any kind' && has 'You NEVER reply to Peter' && has 'never `git fetch` into the shared checkout' && has 'THE NAMED EXCEPTIONS to those holds — these and NO others' && has 'You never touch GitHub PR #1278 or #1245' && has 'no Docker' && has 'NEVER export GIT_SSH_COMMAND' || { echo "REFUSING: the HOLDS" >&2; exit 39; }
has '## MERGE ADDENDUM' && has 'is the LAST thing you write to report.md' && has 'sha256 report.md = <hex>' && has 'EVERY SUBJECT YOU PROPOSE MUST BE TRUE OF THE DIFF' && has 'FROM coagent@agentmail.to' && has 'NOT-TESTED.written-first.md' \
  && grep -qF -- "$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["verdict_subject"])' "$KITJSON")" "$PROMPT_FILE" || { echo "REFUSING: MERGE ADDENDUM / REPORT-HASH-LAST / verdict subject / sender" >&2; exit 25; }
REFS="refs/heads/develop refs/pull/1397/head refs/heads/$P_BR"
if [ -n "${G70_LS:-}" ]; then _LS="$(cat "$G70_LS")"
else _LS="$(env -u GIT_SSH_COMMAND git -C "$REPO" -c core.sshCommand="$(git -C "$REPO" config --get core.sshCommand)" ls-remote "$URL" $REFS)"; fi
get() { printf '%s\n' "$_LS" | awk -v r="$1" '$2==r{print $1}'; }
CUR_DEV="$(get refs/heads/develop)"
[ "$(get refs/pull/1397/head)" = "$P_SHA" ] && [ "$(get "refs/heads/$P_BR")" = "$P_SHA" ] || { echo "REFUSING: #1397 pull/head '$(get refs/pull/1397/head)' / branch '$(get "refs/heads/$P_BR")' != $P_SHA — a verdict is valid ONLY at its head" >&2; exit 6; }
[ -n "$CUR_DEV" ] || { echo "REFUSING: ls-remote returned no develop" >&2; exit 6; }
if git -C "$REPO" cat-file -t "$CUR_DEV" >/dev/null 2>&1; then
  git -C "$REPO" merge-base --is-ancestor "$BASE_SHA" "$CUR_DEV" || { echo "REFUSING: origin develop $CUR_DEV does not descend from $BASE_SHA" >&2; exit 17; }
  _DEVNOTE="descends from ${BASE_SHA:0:12}"
else
  _DEVNOTE="NOT in the local store: descent NOT checked here (the gate checks it in ITS OWN clone, X7; the repin script checked it in the kit clone)"
fi
_ANY_OVR="$(env | grep -c '^G70_')"
NOTE="#1397 ${P_SHA:0:12} at pull/head AND branch | origin develop ${CUR_DEV:0:12} RECORDED ($_DEVNOTE) | $_GO | $_NPIN pins EQUAL | prompt sha256 $(shasum -a 256 "$PROMPT_FILE" | cut -c1-16)"
if [ "$MODE" = "--check" ]; then
  echo "all guards pass:"; echo "  $NOTE"
  echo "  QA project, kit at its home, kit.json, $_NPIN pinned kit files present and hashing to their pins, rendered prompt, head file, repo; thinking directive; 9 kit files named; report dir; no fill token; the pre-ruled GO; no author-seat GO; head in full"
  echo "  the prompt carries the measurement rules, $_NKW by-name keywords (as tokens), the holds + named exceptions, the addendum + REPORT-HASH-LAST rules, the verdict subject + sender"
  [ "$_ANY_OVR" != 0 ] && echo "  (a G70_* TEST OVERRIDE is set)"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"; exit 0
fi
[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — run this launcher in a cockpit pane, never inside a Bash tool" >&2; exit 21; }
[ "$_ANY_OVR" = 0 ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions "$(cat "$PROMPT_FILE")"
