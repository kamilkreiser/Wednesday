#!/bin/bash
# launch_qa_secuura_gate71.sh — cross-project QA agent, ONE gate (gate71, WIDENED 2026-10-07) over TWO Secuura/Blockchain PRs, in merge order:
#   #1404 (KS-1436, T2: job 06's runner stderr to its own file) — #1398's MERGE CONDITION (ruling Q2), merges FIRST;
#   #1398 (KS-1136, T1, round 1 of 2: a present-but-unparseable security artefact must not read as a clean scan).
# THE HEADS ARE PARAMETERS: repin_and_launch_gate71.sh renders prompt_gate71.txt -> prompt_gate71.rendered.txt and writes head_at_launch.txt
# (`P 1404 <branch> <sha>` + `P 1398 <branch> <sha>` + `D <develop sha>`); this launcher reads ONLY those two files, and re-reads origin itself.
# exit 2: QA project missing / launcher not in its kit dir (a MOVED KIT).   exit 3: kit.json missing.   exit 4/5: prompt / repo missing.
# exit 30: a REQUIRED kit file is missing, empty, or has no pin in kit.json.   exit 31: a kit file's sha256 != its kit.json pin (BAD PIN).
# exit 7: head_at_launch.txt missing or malformed (both P rows and one D row, each exactly once).
# exit 8: thinking directive / kit files named / report dir / an unfilled token / the GO strings (EXACTLY the two R 5th ones) /
#         a GO naming Seat R 3rd (#1398's author) or Seat R 4th (#1404's author, a raise seat) / a head or the develop not named in full.
# exit 33: measurement rules + by-name keywords (as tokens).   exit 39: HOLDS + named exceptions.
# exit 25: MERGE ADDENDUM + REPORT-HASH-LAST + verdict subject + sender.
# exit 6: origin pull/head or branch != a row's head (a MOVED HEAD, named).   exit 17: origin develop != the develop the prompt was rendered for.
# exit 19: a head or the develop is ABSENT from the kit clone's object store (REFUSED BY NAME; run the repin script, it fetches by sha).
# exit 21: a LAUNCH (not --check) with stdin not a TTY.   exit 16: a launch with a G71_* test override set.
# Test overrides (--check only): G71_PROMPT, G71_HEADFILE, G71_LS (an ls-remote stand-in), G71_KITJSON, G71_FILES_DIR, G71_CLONE.
# Opus by the configured default: the exec line carries NO --model.   Usage: launch_qa_secuura_gate71.sh [--check]
set -u
MODE="${1:-}"
QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
GS='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-06_gate71'
PROMPT_FILE="${G71_PROMPT:-$GS/prompt_gate71.rendered.txt}"
HEADFILE="${G71_HEADFILE:-$GS/head_at_launch.txt}"
KITJSON="${G71_KITJSON:-$GS/kit.json}"
FILES_DIR="${G71_FILES_DIR:-$GS}"
CLONE="${G71_CLONE:-$GS/_scratch/clone}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
URL='git@github.com:Secuura/Distributed_Secuura.git'
ROWS='1404 1398'
REPORT='2026-10-06-gate71'
GO_WANT_1404='GO (Seat R 5th): merge 1404 on gate71'
GO_WANT_1398='GO (Seat R 5th): merge 1398 on gate71'
REQUIRED='lib_gate71.py composee5_copy.py recompose_gate71.py c1_pin_gate71.py c2_product_gate71.py c3_suites_gate71.py c4_docs_gate71.py c5_job06_gate71.py gh_gate71.py prompt_gate71.txt launch_qa_secuura_gate71.sh repin_and_launch_gate71.sh'
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

[ -s "$PROMPT_FILE" ] || { echo "prompt file missing or empty: $PROMPT_FILE (render it with repin_and_launch_gate71.sh)" >&2; exit 4; }
[ -d "$REPO" ]        || { echo "repo under test missing: $REPO" >&2; exit 5; }
[ -s "$HEADFILE" ]    || { echo "REFUSING: $HEADFILE missing" >&2; exit 7; }
D_LINE="$(grep '^D ' "$HEADFILE")"; set -- $D_LINE; D_SHA="${2:-}"; set --
printf '%s' "$D_SHA" | grep -qE '^[0-9a-f]{40}$' && [ "$(grep -c '^D ' "$HEADFILE")" = 1 ] && [ "$(grep -c '^P ' "$HEADFILE")" = 2 ] \
  || { echo "REFUSING: head file malformed (want exactly 'P 1404 <branch> <40-hex>', 'P 1398 <branch> <40-hex>' and 'D <40-hex>'): $(tr '\n' '|' < "$HEADFILE")" >&2; exit 7; }
for _r in $ROWS; do
  _l="$(grep "^P $_r " "$HEADFILE")"; set -- $_l
  _sha="${4:-}"; _br="${3:-}"; set --
  [ "$(grep -c "^P $_r " "$HEADFILE")" = 1 ] && printf '%s' "$_sha" | grep -qE '^[0-9a-f]{40}$' && [ -n "$_br" ] \
    || { echo "REFUSING: head file malformed for row $_r: '$_l'" >&2; exit 7; }
  eval "H_$_r=\$_sha; B_$_r=\$_br"
done
[ "$(head -n 1 "$PROMPT_FILE")" = "ultrathink" ] || { echo "REFUSING: the prompt does not open with the thinking directive" >&2; exit 8; }
for _f in README.md RULINGS_wednesday.md KIT_REPORT.md; do   # unpinned (Wednesday edits them) but required
  [ -s "$FILES_DIR/$_f" ] || { echo "REFUSING: the kit file $FILES_DIR/$_f is MISSING or empty" >&2; exit 30; }
done
for _f in README.md kit.json lib_gate71.py recompose_gate71.py c1_pin_gate71.py c2_product_gate71.py c3_suites_gate71.py c4_docs_gate71.py c5_job06_gate71.py gh_gate71.py; do
  grep -qF "$GS/$_f" "$PROMPT_FILE" || { echo "REFUSING: the kit file $GS/$_f is not named in the prompt" >&2; exit 8; }
done
grep -qE '\{\{[A-Z0-9_]+\}\}' "$PROMPT_FILE"                          && { echo "REFUSING: an unfilled double-brace token (render with repin_and_launch_gate71.sh)" >&2; exit 8; }
grep -qF "reports/$REPORT/" "$PROMPT_FILE"                            || { echo "REFUSING: the prompt does not name the report dir $REPORT" >&2; exit 8; }
_GO="$(grep -oE 'GO \(Seat [A-Z] [0-9]+(st|nd|rd|th)\): merge [0-9]+ on gate[0-9]+' "$PROMPT_FILE" | sort -u)"
_GO_WANT="$(printf '%s\n%s\n' "$GO_WANT_1398" "$GO_WANT_1404" | sort -u)"
[ "$_GO" = "$_GO_WANT" ]                                              || { echo "REFUSING: the GO strings must be EXACTLY the two ruled ones ($GO_WANT_1404 | $GO_WANT_1398), found: $(printf '%s' "$_GO" | tr '\n' '|')" >&2; exit 8; }
grep -qF 'GO (Seat R 3rd)' "$PROMPT_FILE"                             && { echo "REFUSING: the prompt names Seat R 3rd (#1398's author) in a GO" >&2; exit 8; }
grep -qF 'GO (Seat R 4th)' "$PROMPT_FILE"                             && { echo "REFUSING: the prompt names Seat R 4th (#1404's author, a raise seat that merges nothing) in a GO" >&2; exit 8; }
for _r in $ROWS; do
  eval "_s=\$H_$_r"
  grep -qwF "$_s" "$PROMPT_FILE"                                      || { echo "REFUSING: the prompt does not name the #$_r head $_s in full" >&2; exit 8; }
done
grep -qwF "$D_SHA" "$PROMPT_FILE"                                     || { echo "REFUSING: the prompt does not name the develop $D_SHA in full" >&2; exit 8; }
PROMPT_JOINED="$(python3 -c 'import re,sys; print(re.sub(r"\n\s*", " ", open(sys.argv[1], encoding="utf-8").read()))' "$PROMPT_FILE")"
has() { printf '%s' "$PROMPT_JOINED" | grep -qF -- "$1"; }
has 'MEASURE, not conclude' && has 'RULE WHETHER IT BLOCKS' && has 'NAMES THE TREE' && has 'A check that prints nothing needs a control that prints' && has 'ASSERT THE FILENAME TOO' && has 'ASSERT THE TAMPER LANDED' && has 'A SKIP is NEVER a pass' && has 'NOT RUN is never a pass' && has 'THE HEADS ARE PARAMETERS' || { echo "REFUSING: the measurement rules / head-parameter rule" >&2; exit 33; }
has 'ONE RED ARM PER CONJUNCT' && has 'a genuinely clean scan must still read clean' && has 'MERGE CONDITION' && has 'ascending order is NOT asserted' || { echo "REFUSING: the per-conjunct, clean-stays-clean, merge-condition and doc-order rules" >&2; exit 33; }
_KW="C1-PIN END-TREE PRE-DOCS-TREE NO-TRAILER NO-COAUTHOR SUBJECT-EXACT NO-NEW-LEG GUARD-READ RED-FIRST CONJUNCT-ARMS LEGITIMATE-SHAPES CLEAN-STAYS-CLEAN NO-CLEAN-ON-UNREADABLE CALLERS-ENUMERATED NEGATIVES-REACHED SHELL-SET KS168-CLASS DOCS-ONE-BLOCK NEWLINE-TOLERANT FLOW-UNIQUE-KEYED OWN-KEY-ONLY MERGE-IN-PREDICT RECOMPOSE-GUARD MERGE-TREE C5-PR-TEXT CLOSING-WORD KEYSCAN-OWN-KEY PR-BODY-CLAIMS SQUASH-BODY ACTIONS-BY-LOG-LINE KNOWN-CLASS-PROVED READY-CLAIMS COLLISION-CENSUS NOT-TESTED-LIST TIERING DISK-ENOSPC REPORT-HASH-LAST JOB06-GUARD JOB06-RED-FIRST JOB06-CHAIN FALLBACK-CLEAN LEAK-HIGH TRUNCATED-UNREADABLE STACKED-SHAPES JOB06-REACH MERGE-ORDER SKILL-MUSTS"
_NKW=0
for _w in $_KW; do
  _NKW=$((_NKW + 1))
  printf '%s' "$PROMPT_JOINED" | grep -qE -- "(^|[^A-Za-z0-9-])$_w([^A-Za-z0-9-]|\$)" || { echo "REFUSING: the prompt does not carry the by-name keyword '$_w'" >&2; exit 33; }
done
has 'NO MERGE, NO PUSH to any PR branch, NO ticket state change' && has 'NEVER WRITE THE SHARED CHECKOUT' && has 'Never `rm`' && has 'No `az` command of any kind' && has 'You NEVER reply to Peter' && has 'never `git fetch` into the shared checkout' && has 'THE NAMED EXCEPTIONS to those holds — these and NO others' && has 'You never touch GitHub PR #1278 or #1245' && has 'no Docker' && has 'NEVER export GIT_SSH_COMMAND' && has 'you never run run-internal-audit.sh' || { echo "REFUSING: the HOLDS" >&2; exit 39; }
has '## MERGE ADDENDUM' && has 'is the LAST thing you write to report.md' && has 'sha256 report.md = <hex>' && has 'EVERY SUBJECT YOU PROPOSE MUST BE TRUE OF THE DIFF' && has 'FROM coagent@agentmail.to' && has 'NOT-TESTED.written-first.md' \
  && grep -qF -- "$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["verdict_subject"])' "$KITJSON")" "$PROMPT_FILE" || { echo "REFUSING: MERGE ADDENDUM / REPORT-HASH-LAST / verdict subject / sender" >&2; exit 25; }
REFS="refs/heads/develop refs/pull/1404/head refs/heads/$B_1404 refs/pull/1398/head refs/heads/$B_1398"
if [ -n "${G71_LS:-}" ]; then _LS="$(cat "$G71_LS")"
else _LS="$(env -u GIT_SSH_COMMAND git -C "$REPO" -c core.sshCommand="$(git -C "$REPO" config --get core.sshCommand)" ls-remote "$URL" $REFS)"; fi
get() { printf '%s\n' "$_LS" | awk -v r="$1" '$2==r{print $1}'; }
CUR_DEV="$(get refs/heads/develop)"
for _r in $ROWS; do
  eval "_s=\$H_$_r; _b=\$B_$_r"
  [ "$(get refs/pull/$_r/head)" = "$_s" ] && [ "$(get "refs/heads/$_b")" = "$_s" ] || { echo "REFUSING: #$_r pull/head '$(get refs/pull/$_r/head)' / branch '$(get "refs/heads/$_b")' != $_s — the #$_r HEAD MOVED; a verdict is valid ONLY at its head (re-draft)" >&2; exit 6; }
done
[ -n "$CUR_DEV" ] || { echo "REFUSING: ls-remote returned no develop" >&2; exit 6; }
[ "$CUR_DEV" = "$D_SHA" ] || { echo "REFUSING: origin develop $CUR_DEV != the develop the prompt was rendered for ($D_SHA) — DEVELOP MOVED since the render: re-run repin_and_launch_gate71.sh" >&2; exit 17; }
for _pair in "head 1404:$H_1404" "head 1398:$H_1398" "develop:$CUR_DEV"; do
  _n="${_pair%%:*}"; _s="${_pair#*:}"
  git -C "$CLONE" cat-file -e "$_s^{commit}" 2>/dev/null || { echo "REFUSING BY NAME: the $_n $_s is ABSENT from the kit clone $CLONE (run repin_and_launch_gate71.sh: it fetches by sha)" >&2; exit 19; }
done
_ANY_OVR="$(env | grep -c '^G71_')"
NOTE="#1404 ${H_1404:0:12} + #1398 ${H_1398:0:12} at pull/head AND branch | origin develop ${CUR_DEV:0:12} == rendered | heads + develop PRESENT in the kit clone | $(printf '%s' "$_GO" | tr '\n' '|') | $_NPIN pins EQUAL | prompt sha256 $(shasum -a 256 "$PROMPT_FILE" | cut -c1-16)"
if [ "$MODE" = "--check" ]; then
  echo "all guards pass:"; echo "  $NOTE"
  echo "  QA project, kit at its home, kit.json, $_NPIN pinned kit files present and hashing to their pins, rendered prompt, head file (2 P + D), repo; thinking directive; 10 kit files named; report dir; no fill token; EXACTLY the two R 5th GO strings; no R 3rd / R 4th GO; both heads and develop in full"
  echo "  the prompt carries the measurement rules, $_NKW by-name keywords (as tokens), the holds + named exceptions, the addendum + REPORT-HASH-LAST rules, the verdict subject + sender"
  [ "$_ANY_OVR" != 0 ] && echo "  (a G71_* TEST OVERRIDE is set)"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"; exit 0
fi
[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — run this launcher in a cockpit pane, never inside a Bash tool" >&2; exit 21; }
[ "$_ANY_OVR" = 0 ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions "$(cat "$PROMPT_FILE")"
