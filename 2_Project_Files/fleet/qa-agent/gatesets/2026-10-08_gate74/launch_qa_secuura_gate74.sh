#!/bin/bash
# launch_qa_secuura_gate74.sh — cross-project QA agent, ONE T2 gate (gate74) over Secuura/Blockchain #1423 (KS-1164), with the PREFLIGHT WEIGHT.
# Carried from launch_qa_secuura_gate73.sh and re-keyed by the gate74 drafter: ONE row; the head file carries P x1 / B / D / S / C (C = the
# Actions comparator Wednesday rules, RULINGS Q-SCHEMA74); there are no composed docs (no merge-in is predicted), so no MANIFEST.
# NO PR-SPECIFIC LITERAL lives in this file: head, branch, base, END_TREE, develop, merge seat and comparator come from head_at_launch.txt
# (written by repin_and_launch_gate74.sh from its REQUIRED arguments) and each is compared with kit.json — a wrong value refuses (rc 7).
# Every run (--check included) re-hashes EVERY pinned kit file against kit.json `script_sha256` and re-reads origin by ls-remote.
# exit 2: QA project missing / launcher not in its kit dir (a MOVED KIT).   exit 3: kit.json missing.   exit 4/5: prompt / repo missing.
# exit 30: a REQUIRED kit file is missing, empty, or has no pin.            exit 31: a kit file's sha256 != its pin (BAD PIN).
# exit 7: head_at_launch.txt missing / malformed / a value != kit.json (WRONG VALUE).
# exit 8: comparator UNRULED (kit.json actions_comparator null) / merge seat malformed or an author / thinking directive / kit files
#         named / report dir / an unfilled token / the GO string (exactly one, from the merge seat ordinal) / head + develop in full.
# exit 33: measurement rules + by-name keywords.   exit 39: HOLDS + named exceptions.   exit 25: addendum + REPORT-HASH-LAST + subject + sender.
# exit 6: origin pull/head or branch != the head.  exit 17: origin develop != the rendered develop, or not a descendant of the base.
# exit 21: a LAUNCH (not --check) with stdin not a TTY.   exit 16: a launch with a G74_* test override set.
# Test overrides (--check only): G74_PROMPT, G74_HEADFILE, G74_LS (ls-remote stand-in), G74_KITJSON, G74_FILES_DIR.
# Opus by the configured default: the exec line carries NO --model.   Usage: launch_qa_secuura_gate74.sh [--check]
set -u
MODE="${1:-}"
QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
GS='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-08_gate74'
PROMPT_FILE="${G74_PROMPT:-$GS/prompt_gate74.rendered.txt}"
HEADFILE="${G74_HEADFILE:-$GS/head_at_launch.txt}"
KITJSON="${G74_KITJSON:-$GS/kit.json}"
FILES_DIR="${G74_FILES_DIR:-$GS}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
REQUIRED='lib_gate74.py composee5_copy.py c1_pin_gate74.py c3_suites_gate74.py c4_docs_gate74.py gh_gate74.py t3check_1422.py fixture_body_1423_at_draft.md prompt_gate74.txt launch_qa_secuura_gate74.sh repin_and_launch_gate74.sh'
ROW='1423'
KJ() { python3 -c 'import json,sys; v=json.load(open(sys.argv[1]))
for k in sys.argv[2].split("."): v=v[int(k)] if isinstance(v,list) else v[k]
print(" ".join(map(str,v)) if isinstance(v,list) else ("" if v is None else v))' "$KITJSON" "$1"; }
[ -d "$QA_DIR" ]      || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
_here="$(dirname "$(/bin/realpath "$0")")"
[ "$_here" = "$GS" ]  || { echo "REFUSING: this launcher lives in $_here but was written for $GS (a MOVED KIT)" >&2; exit 2; }
[ -s "$KITJSON" ]     || { echo "REFUSING: kit.json missing: $KITJSON" >&2; exit 3; }
URL="$(KJ github_url)"; REPORT="$(KJ report_dir_name)"; SEAT="$(KJ merge_seat_ordinal)"; LANE="$(KJ merge_seat)"; AUTHOR="$(KJ author_seat)"; COMP="$(KJ actions_comparator)"

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

# --- the Actions comparator must be RULED (Q-SCHEMA74); the merge seat must be well-formed and never the author ---
[ -n "$COMP" ] || { echo "REFUSING: RULING NEEDED — kit.json actions_comparator is null (RULINGS Q-SCHEMA74). Wednesday rules develop|base|union, writes it into kit.json (not a pinned file) and re-runs the repin script, which re-renders." >&2; exit 8; }
case "$COMP" in develop|base|union) ;; *) echo "REFUSING: actions_comparator '$COMP' is not develop|base|union" >&2; exit 8;; esac
[ "$LANE" = "Secuura/Blockchain-R" ] || { echo "REFUSING: kit.json merge_seat '$LANE' is not the R lane (gate73 Q-SEAT: the next R seat)" >&2; exit 8; }
printf '%s' "$SEAT" | grep -qE '^Seat R [0-9]+(st|nd|rd|th)$' || { echo "REFUSING: merge_seat_ordinal '$SEAT' is not of the form 'Seat R <Nth>'" >&2; exit 8; }
[ "$SEAT" != "$AUTHOR" ] || { echo "REFUSING: the merge seat may not be the AUTHOR seat ($SEAT)" >&2; exit 8; }

[ -s "$PROMPT_FILE" ] || { echo "prompt file missing or empty: $PROMPT_FILE (render it with repin_and_launch_gate74.sh)" >&2; exit 4; }
[ -d "$REPO" ]        || { echo "repo under test missing: $REPO" >&2; exit 5; }
[ -s "$HEADFILE" ]    || { echo "REFUSING: $HEADFILE missing" >&2; exit 7; }
# --- the head file: P x1, B, D, S, C; each value compared with kit.json (WRONG VALUE -> rc 7) ---
for _t in P B D S C; do [ "$(grep -c "^$_t " "$HEADFILE")" = 1 ] || { echo "REFUSING: head file must carry exactly one '$_t ' line" >&2; exit 7; }; done
set -- $(grep "^P $ROW " "$HEADFILE"); _br="${3:-}"; _sha="${4:-}"; _tree="${5:-}"; set --
printf '%s' "$_sha$_tree" | grep -qE '^[0-9a-f]{80}$' || { echo "REFUSING: head file P $ROW: head / tree not full 40-hex" >&2; exit 7; }
[ "$_br" = "$(KJ rows.$ROW.branch)" ]          || { echo "REFUSING: WRONG VALUE #$ROW branch '$_br' != kit" >&2; exit 7; }
[ "$_sha" = "$(KJ rows.$ROW.head_expected)" ]   || { echo "REFUSING: WRONG VALUE #$ROW head '$_sha' != kit $(KJ rows.$ROW.head_expected) (re-draft the kit for a moved head)" >&2; exit 7; }
[ "$_tree" = "$(KJ rows.$ROW.end_tree)" ]       || { echo "REFUSING: WRONG VALUE #$ROW END_TREE '$_tree' != kit" >&2; exit 7; }
set -- $(grep '^B ' "$HEADFILE"); B_SHA="${2:-}"; B_N="${3:-}"
set -- $(grep '^D ' "$HEADFILE"); D_SHA="${2:-}"
set -- $(grep '^C ' "$HEADFILE"); C_COMP="${2:-}"; set --
S_SEAT="$(grep '^S ' "$HEADFILE" | cut -c3-)"
[ "$B_SHA" = "$(KJ base)" ] && [ "$B_N" = 1 ] || { echo "REFUSING: WRONG VALUE base '$B_SHA' x'$B_N' != kit $(KJ base) x1" >&2; exit 7; }
printf '%s' "$D_SHA" | grep -qE '^[0-9a-f]{40}$' || { echo "REFUSING: head file develop '$D_SHA' is not full 40-hex" >&2; exit 7; }
[ "$S_SEAT" = "$SEAT" ] || { echo "REFUSING: WRONG VALUE head-file merge seat '$S_SEAT' != kit '$SEAT'" >&2; exit 7; }
[ "$C_COMP" = "$COMP" ] || { echo "REFUSING: WRONG VALUE head-file comparator '$C_COMP' != kit '$COMP'" >&2; exit 7; }

[ "$(head -n 1 "$PROMPT_FILE")" = "ultrathink" ] || { echo "REFUSING: the prompt does not open with the thinking directive" >&2; exit 8; }
for _f in KIT_REPORT.md kit.json lib_gate74.py c1_pin_gate74.py c3_suites_gate74.py c4_docs_gate74.py gh_gate74.py; do
  grep -qF "$GS/$_f" "$PROMPT_FILE" || { echo "REFUSING: the kit file $GS/$_f is not named in the prompt" >&2; exit 8; }
done
grep -qE '\{\{[A-Z0-9_]+\}\}' "$PROMPT_FILE"  && { echo "REFUSING: an unfilled double-brace token (render with repin_and_launch_gate74.sh)" >&2; exit 8; }
grep -qF "reports/$REPORT/" "$PROMPT_FILE"    || { echo "REFUSING: the prompt does not name the report dir $REPORT" >&2; exit 8; }
_GO="$(grep -oE 'GO \(Seat [A-Z] [0-9]+(st|nd|rd|th)\): merge [0-9]+ on gate[0-9]+' "$PROMPT_FILE" | sort -u | tr '\n' '|')"
_GO_WANT="GO ($SEAT): merge $ROW on gate74|"
[ "$_GO" = "$_GO_WANT" ]                      || { echo "REFUSING: the GO string must be exactly '$_GO_WANT', found: $_GO" >&2; exit 8; }
grep -qwF "$(KJ rows.$ROW.head_expected)" "$PROMPT_FILE" || { echo "REFUSING: the prompt does not name #$ROW's head in full" >&2; exit 8; }
grep -qwF "$D_SHA" "$PROMPT_FILE"             || { echo "REFUSING: the prompt does not name the develop $D_SHA in full" >&2; exit 8; }
PROMPT_JOINED="$(python3 -c 'import re,sys; print(re.sub(r"\n\s*", " ", open(sys.argv[1], encoding="utf-8").read()))' "$PROMPT_FILE")"
has() { printf '%s' "$PROMPT_JOINED" | grep -qF -- "$1"; }
has 'MEASURE, not conclude' && has 'RULE WHETHER IT BLOCKS' && has 'NAMES THE TREE' && has 'A check that prints nothing needs a control that prints' && has 'ASSERT THE FILENAME TOO' && has 'ASSERT THE TAMPER LANDED' && has 'A SKIP is NEVER a pass' && has 'NOT RUN is never a pass' && has 'COULD-NOT-CHECK IS A SKIP' && has 'THE HEAD IS A PARAMETER' && has 'ONE PARSER FOR BEFORE AND AFTER' && has 'SUBSET, never equality' && has 'THE PREFLIGHT WEIGHT' && has 'NEVER a bare `vitest run`' && has 'is NOT tag-balance evidence' || { echo "REFUSING: the measurement rules / head-parameter rule / one parser / subset predicate / the preflight weight / the runner trap / tag balance" >&2; exit 33; }
_KW="C1-PIN END-TREE NO-TRAILER NO-COAUTHOR SUBJECT-EXACT KEYS-OWN-ONLY NO-NEW-LEG DISJOINT PREEXISTING-MISMATCH TEST-ONLY PRODUCT-READ SKILL-5D RED-FIRST TAMPER-ARMS PREFLIGHT-WEIGHT LEG-14 SHELL-SET PERF-SUBSET PERF-OWN-SCRIPT FORMAT-GATE TSC DOCS-ONE-BLOCK FLOW-UNIQUE-KEYED OWN-KEY-ONLY TAG-BALANCE MERGE-IN-NEED LEG14-EXPOSURE KEEP-BOTH-BYTES UNKEYED-BASE-STATE C5-PR-TEXT SQUASH-SUBJECT LIVE-SWEEP PLATFORM-SUITES-UNMEASURED ACTIONS-SUBSET ADVISORY-FREEZE SCHEMATHESIS-FLIP READY-CLAIMS COLLISION-CENSUS NOT-TESTED-LIST TIERING SKILL-MUSTS DISK-ENOSPC REPORT-HASH-LAST"
_NKW=0
for _w in $_KW; do
  _NKW=$((_NKW + 1))
  printf '%s' "$PROMPT_JOINED" | grep -qE -- "(^|[^A-Za-z0-9-])$_w([^A-Za-z0-9-]|\$)" || { echo "REFUSING: the prompt does not carry the by-name keyword '$_w'" >&2; exit 33; }
done
has 'NO MERGE, NO PUSH to any PR branch, NO ticket state change' && has 'NEVER WRITE THE SHARED CHECKOUT' && has 'Never `rm`' && has 'No `az` command of any kind' && has 'You NEVER reply to Peter' && has 'never `git fetch` into the shared checkout' && has 'THE NAMED EXCEPTIONS to those holds — these and NO others' && has 'Do NOT start Docker' && has 'NEVER export GIT_SSH_COMMAND' && has 'NO comment on GitHub or Linear' && has 'Never `--no-verify`' || { echo "REFUSING: the HOLDS" >&2; exit 39; }
has '## MERGE ADDENDUM' && has 'is the LAST thing you write to report.md' && has 'sha256 report.md = <hex>' && has 'EVERY SUBJECT YOU PROPOSE MUST BE TRUE OF THE DIFF' && has 'FROM coagent@agentmail.to' && has 'NOT-TESTED.written-first.md' \
  && grep -qF -- "$(KJ verdict_subject)" "$PROMPT_FILE" || { echo "REFUSING: MERGE ADDENDUM / REPORT-HASH-LAST / verdict subject / sender" >&2; exit 25; }
REFS="refs/heads/develop refs/pull/$ROW/head refs/heads/$(KJ rows.$ROW.branch)"
if [ -n "${G74_LS:-}" ]; then _LS="$(cat "$G74_LS")"
else _LS="$(env -u GIT_SSH_COMMAND git -C "$REPO" -c core.sshCommand="$(git -C "$REPO" config --get core.sshCommand)" ls-remote "$URL" $REFS)"; fi
get() { printf '%s\n' "$_LS" | awk -v r="$1" '$2==r{print $1}'; }
CUR_DEV="$(get refs/heads/develop)"
_h="$(KJ rows.$ROW.head_expected)"; _b="$(KJ rows.$ROW.branch)"
[ "$(get "refs/pull/$ROW/head")" = "$_h" ] && [ "$(get "refs/heads/$_b")" = "$_h" ] || { echo "REFUSING: #$ROW pull/head '$(get "refs/pull/$ROW/head")' / branch '$(get "refs/heads/$_b")' != $_h — a verdict is valid ONLY at its head" >&2; exit 6; }
[ -n "$CUR_DEV" ] && [ "$CUR_DEV" = "$D_SHA" ] || { echo "REFUSING: origin develop '$CUR_DEV' != the rendered develop $D_SHA (re-run the repin script)" >&2; exit 17; }
if git -C "$REPO" cat-file -t "$CUR_DEV" >/dev/null 2>&1; then
  git -C "$REPO" merge-base --is-ancestor "$B_SHA" "$CUR_DEV" || { echo "REFUSING: origin develop $CUR_DEV does not descend from $B_SHA" >&2; exit 17; }
  _DEVNOTE="descends from ${B_SHA:0:12}"
else _DEVNOTE="NOT in the local store: descent NOT checked here (the gate checks it in ITS OWN clone; the repin script checked it in the kit clone)"; fi
_ANY_OVR="$(env | grep -c '^G74_')"
NOTE="#$ROW at pull/head AND branch | base ${B_SHA:0:12} x1 | origin develop ${CUR_DEV:0:12} == rendered ($_DEVNOTE) | merge seat $SEAT ($LANE) | comparator $COMP | $_NPIN pins EQUAL | prompt sha256 $(shasum -a 256 "$PROMPT_FILE" | cut -c1-16)"
if [ "$MODE" = "--check" ]; then
  echo "all guards pass:"; echo "  $NOTE"
  echo "  QA project, kit at its home, kit.json, $_NPIN pinned kit files hashing to their pins, KIT_REPORT.md, rendered prompt, head file (P + B + D + S + C == kit), repo; thinking directive; 7 kit files named; report dir; no fill token; the ONE GO string from the merge seat ordinal; head + develop in full"
  echo "  the prompt carries the measurement rules, $_NKW by-name keywords (as tokens), the holds + named exceptions, the addendum + REPORT-HASH-LAST rules, the verdict subject + sender"
  [ "$_ANY_OVR" != 0 ] && echo "  (a G74_* TEST OVERRIDE is set)"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"; exit 0
fi
[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — run this launcher in a cockpit pane, never inside a Bash tool" >&2; exit 21; }
[ "$_ANY_OVR" = 0 ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions "$(cat "$PROMPT_FILE")"
