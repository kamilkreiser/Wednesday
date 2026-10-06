#!/bin/bash
# launch_qa_secuura_gate72.sh — cross-project QA agent, ONE T1 gate (gate72) over Secuura/Blockchain #1406 (KS-1437): an in-range LOCK-ONLY
# refresh of 5 locks, 0 baseline rows. Carried from launch_qa_secuura_gate70.sh. [g72] NO PR-SPECIFIC LITERAL lives in this file: the PR,
# branch, head, base, parent count, END_TREE and develop come from head_at_launch.txt (written by repin_and_launch_gate72.sh from its
# REQUIRED arguments) and each is compared with kit.json — a wrong value refuses (rc 7).
# Every run (--check included) re-hashes EVERY pinned kit file against kit.json `script_sha256` and re-reads origin by ls-remote.
# exit 2: QA project missing / launcher not in its kit dir (a MOVED KIT).   exit 3: kit.json missing.   exit 4/5: prompt / repo missing.
# exit 30: a REQUIRED kit file is missing, empty, or has no pin.            exit 31: a kit file's sha256 != its pin (BAD PIN).
# exit 7: head_at_launch.txt missing / malformed / a value != kit.json (WRONG VALUE).
# exit 8: thinking directive / kit files named / report dir / an unfilled token / the GO string (exactly the pre-ruled one) / head in full.
# exit 33: measurement rules + by-name keywords.   exit 39: HOLDS + named exceptions.   exit 25: addendum + REPORT-HASH-LAST + subject + sender.
# exit 6: origin pull/head or branch != the head.  exit 17: origin develop != the rendered develop, or not a descendant of the base.
# exit 21: a LAUNCH (not --check) with stdin not a TTY.   exit 16: a launch with a G72_* test override set.
# Test overrides (--check only): G72_PROMPT, G72_HEADFILE, G72_LS (ls-remote stand-in), G72_KITJSON, G72_FILES_DIR.
# Opus by the configured default: the exec line carries NO --model.   Usage: launch_qa_secuura_gate72.sh [--check]
set -u
MODE="${1:-}"
QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
GS='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-07_gate72'
PROMPT_FILE="${G72_PROMPT:-$GS/prompt_gate72.rendered.txt}"
HEADFILE="${G72_HEADFILE:-$GS/head_at_launch.txt}"
KITJSON="${G72_KITJSON:-$GS/kit.json}"
FILES_DIR="${G72_FILES_DIR:-$GS}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
REQUIRED='lib_gate72.py c1_pin_gate72.py c2_locks_gate72.py c3_registry_gate72.py c5_legs_gate72.py c6_reach_gate72.py gh_gate72.py prompt_gate72.txt launch_qa_secuura_gate72.sh repin_and_launch_gate72.sh'
KJ() { python3 -c 'import json,sys; v=json.load(open(sys.argv[1]))
for k in sys.argv[2].split("."): v=v[int(k)] if isinstance(v,list) else v[k]
print(" ".join(map(str,v)) if isinstance(v,list) else ("" if v is None else v))' "$KITJSON" "$1"; }
[ -d "$QA_DIR" ]      || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
_here="$(dirname "$(/bin/realpath "$0")")"
[ "$_here" = "$GS" ]  || { echo "REFUSING: this launcher lives in $_here but was written for $GS (a MOVED KIT)" >&2; exit 2; }
[ -s "$KITJSON" ]     || { echo "REFUSING: kit.json missing: $KITJSON" >&2; exit 3; }
URL="$(KJ github_url)"; REPORT="$(KJ report_dir_name)"; GO_WANT="$(KJ go_string)"

# --- PINS ---
_NPIN=0
for _f in $REQUIRED; do
  _want="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["script_sha256"].get(sys.argv[2],""))' "$KITJSON" "$_f" 2>/dev/null)"
  [ -s "$FILES_DIR/$_f" ] || { echo "REFUSING: the kit file $FILES_DIR/$_f is MISSING or empty" >&2; exit 30; }
  [ -n "$_want" ]         || { echo "REFUSING: the kit file $_f has NO sha256 pin in $KITJSON" >&2; exit 30; }
  _got="$(shasum -a 256 "$FILES_DIR/$_f" | cut -d' ' -f1)"
  [ "$_got" = "$_want" ]  || { echo "REFUSING: BAD PIN — $_f sha256 ${_got:0:16} != kit.json pin ${_want:0:16}" >&2; exit 31; }
  _NPIN=$((_NPIN + 1))
done
[ -s "$FILES_DIR/KIT_REPORT.md" ] || { echo "REFUSING: the kit file $FILES_DIR/KIT_REPORT.md is MISSING or empty" >&2; exit 30; }

[ -s "$PROMPT_FILE" ] || { echo "prompt file missing or empty: $PROMPT_FILE (render it with repin_and_launch_gate72.sh)" >&2; exit 4; }
[ -d "$REPO" ]        || { echo "repo under test missing: $REPO" >&2; exit 5; }
[ -s "$HEADFILE" ]    || { echo "REFUSING: $HEADFILE missing" >&2; exit 7; }
# --- [g72] the head file: four lines, each value compared with kit.json (WRONG VALUE -> rc 7) ---
for _t in P B T D; do [ "$(grep -c "^$_t " "$HEADFILE")" = 1 ] || { echo "REFUSING: head file must carry exactly one '$_t ' line" >&2; exit 7; }; done
set -- $(grep '^P ' "$HEADFILE"); P_PR="${2:-}"; P_BR="${3:-}"; P_SHA="${4:-}"
set -- $(grep '^B ' "$HEADFILE"); B_SHA="${2:-}"; B_N="${3:-}"
set -- $(grep '^T ' "$HEADFILE"); T_SHA="${2:-}"
set -- $(grep '^D ' "$HEADFILE"); D_SHA="${2:-}"; set --
for _v in "$P_SHA" "$B_SHA" "$T_SHA" "$D_SHA"; do printf '%s' "$_v" | grep -qE '^[0-9a-f]{40}$' || { echo "REFUSING: head file value '$_v' is not a full 40-hex sha" >&2; exit 7; }; done
[ "$P_PR" = "$(KJ pr.pr)" ]             || { echo "REFUSING: WRONG VALUE pr '$P_PR' != kit $(KJ pr.pr)" >&2; exit 7; }
[ "$P_BR" = "$(KJ pr.branch)" ]         || { echo "REFUSING: WRONG VALUE branch '$P_BR' != kit $(KJ pr.branch)" >&2; exit 7; }
[ "$P_SHA" = "$(KJ pr.head_expected)" ] || { echo "REFUSING: WRONG VALUE head '$P_SHA' != kit $(KJ pr.head_expected) (re-draft the kit for a moved head)" >&2; exit 7; }
[ "$B_SHA" = "$(KJ pr.parents.0)" ]     || { echo "REFUSING: WRONG VALUE base '$B_SHA' != kit $(KJ pr.parents.0)" >&2; exit 7; }
[ "$B_N" = "$(KJ pr.parent_count)" ]    || { echo "REFUSING: WRONG VALUE parents-n '$B_N' != kit $(KJ pr.parent_count)" >&2; exit 7; }
[ "$T_SHA" = "$(KJ pr.end_tree)" ]      || { echo "REFUSING: WRONG VALUE end-tree '$T_SHA' != kit $(KJ pr.end_tree)" >&2; exit 7; }
[ "$(head -n 1 "$PROMPT_FILE")" = "ultrathink" ] || { echo "REFUSING: the prompt does not open with the thinking directive" >&2; exit 8; }
for _f in KIT_REPORT.md kit.json lib_gate72.py c1_pin_gate72.py c2_locks_gate72.py c3_registry_gate72.py c5_legs_gate72.py c6_reach_gate72.py gh_gate72.py; do
  grep -qF "$GS/$_f" "$PROMPT_FILE" || { echo "REFUSING: the kit file $GS/$_f is not named in the prompt" >&2; exit 8; }
done
grep -qE '\{\{[A-Z0-9_]+\}\}' "$PROMPT_FILE"  && { echo "REFUSING: an unfilled double-brace token (render with repin_and_launch_gate72.sh)" >&2; exit 8; }
grep -qF "reports/$REPORT/" "$PROMPT_FILE"    || { echo "REFUSING: the prompt does not name the report dir $REPORT" >&2; exit 8; }
_GO="$(grep -oE 'GO \(Seat [A-Z] [0-9]+(st|nd|rd|th)\): merge [0-9]+ on gate[0-9]+' "$PROMPT_FILE" | sort -u)"
[ "$_GO" = "$GO_WANT" ]                       || { echo "REFUSING: the GO strings must be exactly the pre-ruled one ($GO_WANT), found: $(printf '%s' "$_GO" | tr '\n' '|')" >&2; exit 8; }
grep -qwF "$P_SHA" "$PROMPT_FILE"             || { echo "REFUSING: the prompt does not name the head $P_SHA in full" >&2; exit 8; }
grep -qwF "$D_SHA" "$PROMPT_FILE"             || { echo "REFUSING: the prompt does not name the develop $D_SHA in full" >&2; exit 8; }
PROMPT_JOINED="$(python3 -c 'import re,sys; print(re.sub(r"\n\s*", " ", open(sys.argv[1], encoding="utf-8").read()))' "$PROMPT_FILE")"
has() { printf '%s' "$PROMPT_JOINED" | grep -qF -- "$1"; }
has 'MEASURE, not conclude' && has 'RULE WHETHER IT BLOCKS' && has 'NAMES THE TREE' && has 'A check that prints nothing needs a control that prints' && has 'ASSERT THE FILENAME TOO' && has 'ASSERT THE TAMPER LANDED' && has 'A SKIP is NEVER a pass' && has 'NOT RUN is never a pass' && has 'COULD-NOT-CHECK IS A SKIP' && has 'THE HEAD IS A PARAMETER' && has 'derived from the BASE + THE REGISTRY' && has 'different instruments' || { echo "REFUSING: the measurement rules / head-parameter rule / base-derived plan / instrument distinction" >&2; exit 33; }
_KW="C1-PIN END-TREE NO-TRAILER NO-COAUTHOR SUBJECT-EXACT KEYS-OWN-ONLY NO-NEW-LEG BASELINE-UNTOUCHED MOBILE-UNTOUCHED LOCK-DIFF FIELD-EXACT LINE-DIFF INDENT-KEPT TARBALL-INTEGRITY ADVISORIES-CLEARED IN-RANGE NO-CASCADE LEGS-BASE-HEAD AUDIT-CONTRACT CLEANROOM NEGATIVE-CONTROLS INSTALL-ISOLATED INSTALL-ROOT SUITES KNOWN-FAILURE RUNTIME-REACH BUNDLE C5-PR-TEXT TICKET-COMMENT LINEAR-STATE ACTIONS-PREEXISTING MERGEABLE-STATE READY-CLAIMS COLLISION-CENSUS NOT-TESTED-LIST PLATFORM-SUITES-NOT-RUN TIERING DISK-ENOSPC REPORT-HASH-LAST"
_NKW=0
for _w in $_KW; do
  _NKW=$((_NKW + 1))
  printf '%s' "$PROMPT_JOINED" | grep -qE -- "(^|[^A-Za-z0-9-])$_w([^A-Za-z0-9-]|\$)" || { echo "REFUSING: the prompt does not carry the by-name keyword '$_w'" >&2; exit 33; }
done
has 'NO MERGE, NO PUSH to any PR branch, NO ticket state change' && has 'NEVER WRITE THE SHARED CHECKOUT' && has 'Never `rm`' && has 'No `az` command of any kind' && has 'You NEVER reply to Peter' && has 'never `git fetch` into the shared checkout' && has 'THE NAMED EXCEPTIONS to those holds — these and NO others' && has 'Do NOT start Docker' && has 'NEVER export GIT_SSH_COMMAND' && has 'never comment' || { echo "REFUSING: the HOLDS" >&2; exit 39; }
has '## MERGE ADDENDUM' && has 'is the LAST thing you write to report.md' && has 'sha256 report.md = <hex>' && has 'EVERY SUBJECT YOU PROPOSE MUST BE TRUE OF THE DIFF' && has 'FROM coagent@agentmail.to' && has 'NOT-TESTED.written-first.md' \
  && grep -qF -- "$(KJ verdict_subject)" "$PROMPT_FILE" || { echo "REFUSING: MERGE ADDENDUM / REPORT-HASH-LAST / verdict subject / sender" >&2; exit 25; }
REFS="refs/heads/develop refs/pull/$P_PR/head refs/heads/$P_BR"
if [ -n "${G72_LS:-}" ]; then _LS="$(cat "$G72_LS")"
else _LS="$(env -u GIT_SSH_COMMAND git -C "$REPO" -c core.sshCommand="$(git -C "$REPO" config --get core.sshCommand)" ls-remote "$URL" $REFS)"; fi
get() { printf '%s\n' "$_LS" | awk -v r="$1" '$2==r{print $1}'; }
CUR_DEV="$(get refs/heads/develop)"
[ "$(get "refs/pull/$P_PR/head")" = "$P_SHA" ] && [ "$(get "refs/heads/$P_BR")" = "$P_SHA" ] || { echo "REFUSING: #$P_PR pull/head '$(get "refs/pull/$P_PR/head")' / branch '$(get "refs/heads/$P_BR")' != $P_SHA — a verdict is valid ONLY at its head" >&2; exit 6; }
[ "$CUR_DEV" = "$D_SHA" ] || { echo "REFUSING: origin develop '$CUR_DEV' != the rendered develop $D_SHA (re-run the repin script)" >&2; exit 17; }
if git -C "$REPO" cat-file -t "$CUR_DEV" >/dev/null 2>&1; then
  git -C "$REPO" merge-base --is-ancestor "$B_SHA" "$CUR_DEV" || { echo "REFUSING: origin develop $CUR_DEV does not descend from $B_SHA" >&2; exit 17; }
  _DEVNOTE="descends from ${B_SHA:0:12}"
else _DEVNOTE="NOT in the local store: descent NOT checked here (the gate checks it in ITS OWN clone, X7; the repin script checked it in the kit clone)"; fi
_ANY_OVR="$(env | grep -c '^G72_')"
NOTE="#$P_PR ${P_SHA:0:12} at pull/head AND branch | base ${B_SHA:0:12} x$B_N | END_TREE ${T_SHA:0:12} | origin develop ${CUR_DEV:0:12} == rendered ($_DEVNOTE) | $_GO | $_NPIN pins EQUAL | prompt sha256 $(shasum -a 256 "$PROMPT_FILE" | cut -c1-16)"
if [ "$MODE" = "--check" ]; then
  echo "all guards pass:"; echo "  $NOTE"
  echo "  QA project, kit at its home, kit.json, $_NPIN pinned kit files hashing to their pins, KIT_REPORT.md, rendered prompt, head file (4 values == kit), repo; thinking directive; 9 kit files named; report dir; no fill token; the pre-ruled GO; head + develop in full"
  echo "  the prompt carries the measurement rules, $_NKW by-name keywords (as tokens), the holds + named exceptions, the addendum + REPORT-HASH-LAST rules, the verdict subject + sender"
  [ "$_ANY_OVR" != 0 ] && echo "  (a G72_* TEST OVERRIDE is set)"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"; exit 0
fi
[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — run this launcher in a cockpit pane, never inside a Bash tool" >&2; exit 21; }
[ "$_ANY_OVR" = 0 ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions "$(cat "$PROMPT_FILE")"
