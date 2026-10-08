#!/bin/bash
# launch_qa_secuura_gate76.sh — cross-project QA agent, ONE batched gate (gate76, T2 per row) over Secuura/Blockchain #1427 (KS-1274) and
# #1428 (KS-593). Carried from launch_qa_secuura_gate75.sh and re-keyed by the gate76 drafter: TWO rows; the head file carries P x2 / B / D /
# S / C / O (the ruled landing order) / T (the predicted step-2 keep-both tree); TWO GO strings from the ONE merge seat ordinal; the merge seat
# lane is any Secuura/Blockchain-<L> lane whose letter matches the ordinal's (gate75 hard-coded -R; gate76 Q-SEAT76 is a ruling), and is never
# either AUTHOR seat.
# NO PR-SPECIFIC LITERAL lives in this file: heads, branches, base, END_TREEs, develop, merge seat, comparator, order and the step-2 tree come
# from head_at_launch.txt (written by repin_and_launch_gate76.sh from its REQUIRED arguments) and each is compared with kit.json (rc 7).
# Every run (--check included) re-hashes EVERY pinned kit file against kit.json `script_sha256` and re-reads origin by ls-remote.
# exit 2: QA project missing / launcher not in its kit dir (a MOVED KIT).   exit 3: kit.json missing.   exit 4/5: prompt / repo missing.
# exit 30: a REQUIRED kit file is missing, empty, or has no pin.            exit 31: a kit file's sha256 != its pin (BAD PIN).
# exit 7: head_at_launch.txt missing / malformed / a value != kit.json (WRONG VALUE).
# exit 8: comparator UNRULED / merge seat unruled, malformed or an author / thinking directive / kit files named / report dir / an unfilled
#         token / the GO strings (exactly the two, from the merge seat ordinal) / both heads + develop + the step-2 tree in full.
# exit 33: measurement rules + by-name keywords.   exit 39: HOLDS + named exceptions.   exit 25: addendum + REPORT-HASH-LAST + subject + sender.
# exit 6: origin pull/head or branch != a head.  exit 17: origin develop != the rendered develop, or not a descendant of the base.
# exit 21: a LAUNCH (not --check) with stdin not a TTY.   exit 16: a launch with a G76_* test override set.
# Test overrides (--check only): G76_PROMPT, G76_HEADFILE, G76_LS (ls-remote stand-in), G76_KITJSON, G76_FILES_DIR.
# Opus by the configured default: the exec line carries NO --model.   Usage: launch_qa_secuura_gate76.sh [--check]
set -u
MODE="${1:-}"
QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
GS='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-08_gate76'
PROMPT_FILE="${G76_PROMPT:-$GS/prompt_gate76.rendered.txt}"
HEADFILE="${G76_HEADFILE:-$GS/head_at_launch.txt}"
KITJSON="${G76_KITJSON:-$GS/kit.json}"
FILES_DIR="${G76_FILES_DIR:-$GS}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
REQUIRED='lib_gate76.py composee5_copy.py c1_pin_gate76.py c3_redgreen_gate76.py c3_preflight_gate76.py c4_docs_gate76.py gh_gate76.py fixture_body_1427_at_draft.md fixture_body_1428_at_draft.md prompt_gate76.txt launch_qa_secuura_gate76.sh repin_and_launch_gate76.sh'
ROWS='1427 1428'
KJ() { python3 -c 'import json,sys; v=json.load(open(sys.argv[1]))
for k in sys.argv[2].split("."): v=v[int(k)] if isinstance(v,list) else v[k]
print(" ".join(map(str,v)) if isinstance(v,list) else ("" if v is None else v))' "$KITJSON" "$1"; }
[ -d "$QA_DIR" ]      || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
_here="$(dirname "$(/bin/realpath "$0")")"
[ "$_here" = "$GS" ]  || { echo "REFUSING: this launcher lives in $_here but was written for $GS (a MOVED KIT)" >&2; exit 2; }
[ -s "$KITJSON" ]     || { echo "REFUSING: kit.json missing: $KITJSON" >&2; exit 3; }
URL="$(KJ github_url)"; REPORT="$(KJ report_dir_name)"; SEAT="$(KJ merge_seat_ordinal)"; LANE="$(KJ merge_seat)"; AUTHORS="$(KJ author_seats)"; COMP="$(KJ actions_comparator)"

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

# --- the Actions comparator and the merge seat must be RULED (kit.json); the merge seat is never an author ---
[ -n "$COMP" ] || { echo "REFUSING: RULING NEEDED — kit.json actions_comparator is null" >&2; exit 8; }
case "$COMP" in develop|base|union) ;; *) echo "REFUSING: actions_comparator '$COMP' is not develop|base|union" >&2; exit 8;; esac
[ -n "$LANE" ] && [ -n "$SEAT" ] || { echo "REFUSING: RULING NEEDED — kit.json merge_seat / merge_seat_ordinal is null (RULINGS Q-SEAT76)" >&2; exit 8; }
printf '%s' "$LANE" | grep -qE '^Secuura/Blockchain-[A-Z]$' || { echo "REFUSING: kit.json merge_seat '$LANE' is not a Secuura/Blockchain-<L> lane" >&2; exit 8; }
printf '%s' "$SEAT" | grep -qE '^Seat [A-Z] [0-9]+(st|nd|rd|th)$' || { echo "REFUSING: merge_seat_ordinal '$SEAT' is not of the form 'Seat <L> <Nth>'" >&2; exit 8; }
[ "${LANE##*-}" = "$(printf '%s' "$SEAT" | cut -d' ' -f2)" ] || { echo "REFUSING: merge seat lane '$LANE' and ordinal '$SEAT' name different lanes" >&2; exit 8; }
case " $(KJ author_seats | sed 's/Seat /Seat_/g') " in *" $(printf '%s' "$SEAT" | sed 's/Seat /Seat_/') "*) echo "REFUSING: the merge seat may not be an AUTHOR seat ($SEAT)" >&2; exit 8;; esac

[ -s "$PROMPT_FILE" ] || { echo "prompt file missing or empty: $PROMPT_FILE (render it with repin_and_launch_gate76.sh)" >&2; exit 4; }
[ -d "$REPO" ]        || { echo "repo under test missing: $REPO" >&2; exit 5; }
[ -s "$HEADFILE" ]    || { echo "REFUSING: $HEADFILE missing" >&2; exit 7; }
# --- the head file: P x2, B, D, S, C, O, T; each value compared with kit.json (WRONG VALUE -> rc 7) ---
[ "$(grep -c '^P ' "$HEADFILE")" = 2 ] || { echo "REFUSING: head file must carry exactly two 'P ' lines" >&2; exit 7; }
for _t in B D S C O T; do [ "$(grep -c "^$_t " "$HEADFILE")" = 1 ] || { echo "REFUSING: head file must carry exactly one '$_t ' line" >&2; exit 7; }; done
for ROW in $ROWS; do
  set -- $(grep "^P $ROW " "$HEADFILE"); _br="${3:-}"; _sha="${4:-}"; _tree="${5:-}"; set --
  printf '%s' "$_sha$_tree" | grep -qE '^[0-9a-f]{80}$' || { echo "REFUSING: head file P $ROW: head / tree not full 40-hex" >&2; exit 7; }
  [ "$_br" = "$(KJ rows.$ROW.branch)" ]          || { echo "REFUSING: WRONG VALUE #$ROW branch '$_br' != kit" >&2; exit 7; }
  [ "$_sha" = "$(KJ rows.$ROW.head_expected)" ]   || { echo "REFUSING: WRONG VALUE #$ROW head '$_sha' != kit $(KJ rows.$ROW.head_expected) (re-draft the kit for a moved head)" >&2; exit 7; }
  [ "$_tree" = "$(KJ rows.$ROW.end_tree)" ]       || { echo "REFUSING: WRONG VALUE #$ROW END_TREE '$_tree' != kit" >&2; exit 7; }
done
set -- $(grep '^B ' "$HEADFILE"); B_SHA="${2:-}"; B_N="${3:-}"
set -- $(grep '^D ' "$HEADFILE"); D_SHA="${2:-}"
set -- $(grep '^C ' "$HEADFILE"); C_COMP="${2:-}"
set -- $(grep '^O ' "$HEADFILE"); O_ORD="${2:-}"
set -- $(grep '^T ' "$HEADFILE"); T_TREE="${2:-}"; set --
S_SEAT="$(grep '^S ' "$HEADFILE" | cut -c3-)"
[ "$B_SHA" = "$(KJ base)" ] && [ "$B_N" = 1 ] || { echo "REFUSING: WRONG VALUE base '$B_SHA' x'$B_N' != kit $(KJ base) x1" >&2; exit 7; }
printf '%s' "$D_SHA" | grep -qE '^[0-9a-f]{40}$' || { echo "REFUSING: head file develop '$D_SHA' is not full 40-hex" >&2; exit 7; }
printf '%s' "$T_TREE" | grep -qE '^[0-9a-f]{40}$' || { echo "REFUSING: head file step-2 tree '$T_TREE' is not full 40-hex" >&2; exit 7; }
[ "$S_SEAT" = "$SEAT" ] || { echo "REFUSING: WRONG VALUE head-file merge seat '$S_SEAT' != kit '$SEAT'" >&2; exit 7; }
[ "$C_COMP" = "$COMP" ] || { echo "REFUSING: WRONG VALUE head-file comparator '$C_COMP' != kit '$COMP'" >&2; exit 7; }
[ "$O_ORD" = "$(KJ merge_order_default | tr ' ' ',')" ] || { echo "REFUSING: WRONG VALUE head-file order '$O_ORD' != kit merge_order_default" >&2; exit 7; }

[ "$(head -n 1 "$PROMPT_FILE")" = "ultrathink" ] || { echo "REFUSING: the prompt does not open with the thinking directive" >&2; exit 8; }
for _f in KIT_REPORT.md kit.json lib_gate76.py c1_pin_gate76.py c3_redgreen_gate76.py c3_preflight_gate76.py c4_docs_gate76.py gh_gate76.py; do
  grep -qF "$GS/$_f" "$PROMPT_FILE" || { echo "REFUSING: the kit file $GS/$_f is not named in the prompt" >&2; exit 8; }
done
grep -qE '\{\{[A-Z0-9_]+\}\}' "$PROMPT_FILE"  && { echo "REFUSING: an unfilled double-brace token (render with repin_and_launch_gate76.sh)" >&2; exit 8; }
grep -qF "reports/$REPORT/" "$PROMPT_FILE"    || { echo "REFUSING: the prompt does not name the report dir $REPORT" >&2; exit 8; }
_GO="$(grep -oE 'GO \(Seat [A-Z] [0-9]+(st|nd|rd|th)\): merge [0-9]+ on gate[0-9]+' "$PROMPT_FILE" | sort -u | tr '\n' '|')"
_GO_WANT="$(printf 'GO (%s): merge 1427 on gate76\nGO (%s): merge 1428 on gate76\n' "$SEAT" "$SEAT" | sort -u | tr '\n' '|')"
[ "$_GO" = "$_GO_WANT" ]                      || { echo "REFUSING: the GO strings must be exactly '$_GO_WANT', found: $_GO" >&2; exit 8; }
for ROW in $ROWS; do grep -qwF "$(KJ rows.$ROW.head_expected)" "$PROMPT_FILE" || { echo "REFUSING: the prompt does not name #$ROW's head in full" >&2; exit 8; }; done
grep -qwF "$D_SHA" "$PROMPT_FILE"             || { echo "REFUSING: the prompt does not name the develop $D_SHA in full" >&2; exit 8; }
grep -qwF "$T_TREE" "$PROMPT_FILE"            || { echo "REFUSING: the prompt does not name the step-2 tree $T_TREE in full" >&2; exit 8; }
PROMPT_JOINED="$(python3 -c 'import re,sys; print(re.sub(r"\n\s*", " ", open(sys.argv[1], encoding="utf-8").read()))' "$PROMPT_FILE")"
has() { printf '%s' "$PROMPT_JOINED" | grep -qF -- "$1"; }
has 'MEASURE, not conclude' && has 'RULE WHETHER IT BLOCKS' && has 'NAMES THE TREE' && has 'A check that prints nothing needs a control that prints' && has 'ASSERT THE FILENAME TOO' && has 'ASSERT THE TAMPER LANDED' && has 'A SKIP is NEVER a pass' && has 'NOT RUN is never a pass' && has 'COULD-NOT-CHECK IS A SKIP' && has 'THE HEAD IS A PARAMETER' && has 'ONE PARSER FOR BEFORE AND AFTER' && has 'SUBSET, never equality' && has 'THE RED-PROOF IS YOURS, NOT THE SEATS' && has 'RESTORE TO THE HEAD STATE, NEVER THE BASE' && has 'is NOT tag-balance evidence' && has 'a red from the WRONG CELL is not the arm' && has 'composed docs VERBATIM' && has 'NEVER `git merge-file --union`' || { echo "REFUSING: the measurement rules / head-parameter rule / one parser / subset predicate / the red-proof / restore-to-head / tag balance / wrong-cell rule / keep-both verbatim / union hazard" >&2; exit 33; }
_KW="C1-PIN END-TREE BRANCH-TRAILER KEYS-ATTACH CLOSE-RESIDUE SCOPE-DISJOINT NO-NEW-LEG FIX-INVARIANTS PREEXISTING-MISMATCH THROUGH-CODE TICKET-CLAIM SECURITY-ADJACENT AUTHZ-ORDER RED-PROOF REDGREEN-RERUN RESTORE-HEAD-STATE TRIVY-ARMS NULL-RESULTS-GAP ORIGINATE-RED FULL-SUITE OWN-ARM PREFLIGHT-BY-HAND SIM-FINAL DOCS-PARITY INSERTION-ONLY TAG-BALANCE KEEP-BOTH UNION-HAZARD CHAIN-PREDICT MERGE-IN-NEED C5-PR-TEXT SQUASH-SUBJECT SQUASH-BODY ATTRIBUTION ACTIONS-SUBSET ADVISORY-FREEZE CI-CORROBORATION READY-CLAIMS COLLISION-CENSUS NOT-TESTED-LIST TIERING SKILL-MUSTS LIVE-SWEEP-OWED DISK-ENOSPC REPORT-HASH-LAST"
_NKW=0
for _w in $_KW; do
  _NKW=$((_NKW + 1))
  printf '%s' "$PROMPT_JOINED" | grep -qE -- "(^|[^A-Za-z0-9-])$_w([^A-Za-z0-9-]|\$)" || { echo "REFUSING: the prompt does not carry the by-name keyword '$_w'" >&2; exit 33; }
done
has 'NO MERGE, NO PUSH to any PR branch, NO ticket state change' && has 'NEVER WRITE THE SHARED CHECKOUT' && has 'Never `rm`' && has 'No `az` command of any kind' && has 'You NEVER reply to Peter' && has 'never `git fetch` into the shared checkout' && has 'THE NAMED EXCEPTIONS to those holds — these and NO others' && has 'Do NOT start Docker' && has 'NEVER export GIT_SSH_COMMAND' && has 'NO comment on GitHub or Linear' && has 'Never `--no-verify`' || { echo "REFUSING: the HOLDS" >&2; exit 39; }
has '## MERGE ADDENDUM' && has 'is the LAST thing you write to report.md' && has 'sha256 report.md = <hex>' && has 'EVERY SUBJECT YOU PROPOSE MUST BE TRUE OF THE DIFF' && has 'FROM coagent@agentmail.to' && has 'NOT-TESTED.written-first.md' \
  && grep -qF -- "$(KJ verdict_subject)" "$PROMPT_FILE" || { echo "REFUSING: MERGE ADDENDUM / REPORT-HASH-LAST / verdict subject / sender" >&2; exit 25; }
REFS="refs/heads/develop"; for ROW in $ROWS; do REFS="$REFS refs/pull/$ROW/head refs/heads/$(KJ rows.$ROW.branch)"; done
if [ -n "${G76_LS:-}" ]; then _LS="$(cat "$G76_LS")"
else _LS="$(env -u GIT_SSH_COMMAND git -C "$REPO" -c core.sshCommand="$(git -C "$REPO" config --get core.sshCommand)" ls-remote "$URL" $REFS)"; fi
get() { printf '%s\n' "$_LS" | awk -v r="$1" '$2==r{print $1}'; }
CUR_DEV="$(get refs/heads/develop)"
for ROW in $ROWS; do
  _h="$(KJ rows.$ROW.head_expected)"; _b="$(KJ rows.$ROW.branch)"
  [ "$(get "refs/pull/$ROW/head")" = "$_h" ] && [ "$(get "refs/heads/$_b")" = "$_h" ] || { echo "REFUSING: #$ROW pull/head '$(get "refs/pull/$ROW/head")' / branch '$(get "refs/heads/$_b")' != $_h — a verdict is valid ONLY at its head" >&2; exit 6; }
done
[ -n "$CUR_DEV" ] && [ "$CUR_DEV" = "$D_SHA" ] || { echo "REFUSING: origin develop '$CUR_DEV' != the rendered develop $D_SHA (re-run the repin script)" >&2; exit 17; }
if git -C "$REPO" cat-file -e "$CUR_DEV^{commit}" 2>/dev/null; then
  git -C "$REPO" merge-base --is-ancestor "$B_SHA" "$CUR_DEV" || { echo "REFUSING: origin develop $CUR_DEV does not descend from $B_SHA" >&2; exit 17; }
  _DEVNOTE="descends from ${B_SHA:0:12}"
else _DEVNOTE="NOT in the local store: descent NOT checked here (the gate checks it in ITS OWN clone; the repin script checked it in the kit clone)"; fi
_ANY_OVR="$(env | grep -c '^G76_')"
NOTE="#1427 + #1428 at pull/head AND branch | base ${B_SHA:0:12} x1 | origin develop ${CUR_DEV:0:12} == rendered ($_DEVNOTE) | order $O_ORD, step-2 tree ${T_TREE:0:12} | merge seat $SEAT ($LANE) | comparator $COMP | $_NPIN pins EQUAL | prompt sha256 $(shasum -a 256 "$PROMPT_FILE" | cut -c1-16)"
if [ "$MODE" = "--check" ]; then
  echo "all guards pass:"; echo "  $NOTE"
  echo "  QA project, kit at its home, kit.json, $_NPIN pinned kit files hashing to their pins, KIT_REPORT.md, rendered prompt, head file (P x2 + B + D + S + C + O + T == kit), repo; thinking directive; 8 kit files named; report dir; no fill token; the TWO GO strings from the merge seat ordinal; both heads + develop + the step-2 tree in full"
  echo "  the prompt carries the measurement rules, $_NKW by-name keywords (as tokens), the holds + named exceptions, the addendum + REPORT-HASH-LAST rules, the verdict subject + sender"
  [ "$_ANY_OVR" != 0 ] && echo "  (a G76_* TEST OVERRIDE is set)"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"; exit 0
fi
[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — run this launcher in a cockpit pane, never inside a Bash tool" >&2; exit 21; }
[ "$_ANY_OVR" = 0 ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions "$(cat "$PROMPT_FILE")"
