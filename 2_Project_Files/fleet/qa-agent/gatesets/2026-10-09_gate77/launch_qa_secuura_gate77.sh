#!/bin/bash
# launch_qa_secuura_gate77.sh — cross-project QA agent, ONE batched gate (gate77: #1432 T1, five rows T2) over Secuura/Blockchain #1429 KS-1449,
# #1430 KS-1328, #1431 KS-1355, #1432 KS-1410, #1433 KS-1139, #1434 KS-1171. Carried from launch_qa_secuura_gate76.sh and widened to six rows by
# the gate77 drafter: the head file carries P x6 / B / D / S / C / O (the effective landing order) / T (the predicted FINAL tree) / Q (the #1427
# state); SIX GO strings from the ONE merge seat ordinal; the merge seat is never an AUTHOR seat.
# NO PR-SPECIFIC LITERAL lives in this file: heads, branches, raise_base, END_TREEs, develop, merge seat, comparator, order and the final tree
# come from head_at_launch.txt (written by repin_and_launch_gate77.sh from its REQUIRED arguments) and each is compared with kit.json (rc 7).
# Every run (--check included) re-hashes EVERY pinned kit file against kit.json `script_sha256` and re-reads origin by ls-remote.
# exit 2: QA project missing / launcher not in its kit dir (a MOVED KIT).   exit 3: kit.json missing.   exit 4/5: prompt / repo missing.
# exit 30: a REQUIRED kit file is missing, empty, or has no pin.            exit 31: a kit file's sha256 != its pin (BAD PIN).
# exit 7: head_at_launch.txt missing / malformed / a value != kit.json (WRONG VALUE).
# exit 8: comparator / merge seat unruled, malformed or an author / thinking directive / kit files named / report dir / an unfilled token /
#         the GO strings (exactly the six, from the merge seat ordinal) / six heads + develop + the final tree in full.
# exit 33: measurement rules + by-name keywords.   exit 39: HOLDS + named exceptions.   exit 25: addendum + REPORT-HASH-LAST + subject + sender.
# exit 6: origin pull/head or branch != a head.  exit 17: origin develop != the rendered develop, or not a descendant of the raise_base.
# exit 21: a LAUNCH (not --check) with stdin not a TTY.   exit 16: a launch with a GATE77_* test override set.
# Test overrides (--check only): GATE77_PROMPT, GATE77_HEADFILE, GATE77_LS (ls-remote stand-in), GATE77_KITJSON, GATE77_FILES_DIR.
# Opus by the configured default: the exec line carries NO --model.   Usage: launch_qa_secuura_gate77.sh [--check]
set -u
MODE="${1:-}"
QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
GS='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-09_gate77'
PROMPT_FILE="${GATE77_PROMPT:-$GS/prompt_gate77.rendered.txt}"
HEADFILE="${GATE77_HEADFILE:-$GS/head_at_launch.txt}"
KITJSON="${GATE77_KITJSON:-$GS/kit.json}"
FILES_DIR="${GATE77_FILES_DIR:-$GS}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
REQUIRED='lib_gate77.py composee5_copy.py c1_pin_gate77.py c2_merge_gate77.py c3_tamper_gate77.py gh_gate77.py prompt_gate77.txt launch_qa_secuura_gate77.sh repin_and_launch_gate77.sh'
ROWS='1429 1430 1431 1432 1433 1434'
KJ() { python3 -c 'import json,sys; v=json.load(open(sys.argv[1]))
for k in sys.argv[2].split("."): v=v[int(k)] if isinstance(v,list) else v[k]
print(" ".join(map(str,v)) if isinstance(v,list) else ("" if v is None else v))' "$KITJSON" "$1"; }
[ -d "$QA_DIR" ]      || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
_here="$(dirname "$(/bin/realpath "$0")")"
[ "$_here" = "$GS" ]  || { echo "REFUSING: this launcher lives in $_here but was written for $GS (a MOVED KIT)" >&2; exit 2; }
[ -s "$KITJSON" ]     || { echo "REFUSING: kit.json missing: $KITJSON" >&2; exit 3; }
URL="$(KJ github_url)"; REPORT="$(KJ report_dir_name)"; SEAT="$(KJ merge_seat_ordinal)"; LANE="$(KJ merge_seat)"; COMP="$(KJ actions_comparator)"

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
[ -n "$LANE" ] && [ -n "$SEAT" ] || { echo "REFUSING: RULING NEEDED — kit.json merge_seat / merge_seat_ordinal is null (RULINGS Q-SEAT77)" >&2; exit 8; }
printf '%s' "$LANE" | grep -qE '^Secuura/Blockchain-[A-Z]$' || { echo "REFUSING: kit.json merge_seat '$LANE' is not a Secuura/Blockchain-<L> lane" >&2; exit 8; }
printf '%s' "$SEAT" | grep -qE '^Seat [A-Z] [0-9]+(st|nd|rd|th)$' || { echo "REFUSING: merge_seat_ordinal '$SEAT' is not of the form 'Seat <L> <Nth>'" >&2; exit 8; }
[ "${LANE##*-}" = "$(printf '%s' "$SEAT" | cut -d' ' -f2)" ] || { echo "REFUSING: merge seat lane '$LANE' and ordinal '$SEAT' name different lanes" >&2; exit 8; }
case " $(KJ author_seats | sed 's/Seat \([A-Z]\) /Seat_\1_/g') " in *" $(printf '%s' "$SEAT" | sed 's/Seat \([A-Z]\) /Seat_\1_/') "*) echo "REFUSING: the merge seat may not be an AUTHOR seat ($SEAT)" >&2; exit 8;; esac

[ -s "$PROMPT_FILE" ] || { echo "prompt file missing or empty: $PROMPT_FILE (render it with repin_and_launch_gate77.sh)" >&2; exit 4; }
[ -d "$REPO" ]        || { echo "repo under test missing: $REPO" >&2; exit 5; }
[ -s "$HEADFILE" ]    || { echo "REFUSING: $HEADFILE missing" >&2; exit 7; }
# --- the head file: P x6, B, D, S, C, O, T, Q; each value compared with kit.json (WRONG VALUE -> rc 7) ---
[ "$(grep -c '^P ' "$HEADFILE")" = 6 ] || { echo "REFUSING: head file must carry exactly six 'P ' lines" >&2; exit 7; }
for _t in B D S C O T Q; do [ "$(grep -c "^$_t " "$HEADFILE")" = 1 ] || { echo "REFUSING: head file must carry exactly one '$_t ' line" >&2; exit 7; }; done
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
[ "$B_SHA" = "$(KJ raise_base)" ] && [ "$B_N" = 1 ] || { echo "REFUSING: WRONG VALUE raise_base '$B_SHA' x'$B_N' != kit $(KJ raise_base) x1" >&2; exit 7; }
printf '%s' "$D_SHA" | grep -qE '^[0-9a-f]{40}$' || { echo "REFUSING: head file develop '$D_SHA' is not full 40-hex" >&2; exit 7; }
printf '%s' "$T_TREE" | grep -qE '^[0-9a-f]{40}$' || { echo "REFUSING: head file final tree '$T_TREE' is not full 40-hex" >&2; exit 7; }
[ "$S_SEAT" = "$SEAT" ] || { echo "REFUSING: WRONG VALUE head-file merge seat '$S_SEAT' != kit '$SEAT'" >&2; exit 7; }
[ "$C_COMP" = "$COMP" ] || { echo "REFUSING: WRONG VALUE head-file comparator '$C_COMP' != kit '$COMP'" >&2; exit 7; }
_ORD="$(KJ merge_order_default | tr ' ' ',')"
[ "$O_ORD" = "$_ORD" ] || [ "$O_ORD" = "1427,$_ORD" ] || { echo "REFUSING: WRONG VALUE head-file order '$O_ORD' != kit merge_order_default ('$_ORD', or '1427,' + it while #1427 is pending)" >&2; exit 7; }

[ "$(head -n 1 "$PROMPT_FILE")" = "ultrathink" ] || { echo "REFUSING: the prompt does not open with the thinking directive" >&2; exit 8; }
for _f in KIT_REPORT.md RULINGS_wednesday.md kit.json lib_gate77.py c1_pin_gate77.py c2_merge_gate77.py c3_tamper_gate77.py gh_gate77.py; do
  grep -qF "$GS/$_f" "$PROMPT_FILE" || { echo "REFUSING: the kit file $GS/$_f is not named in the prompt" >&2; exit 8; }
done
grep -qE '\{\{[A-Z0-9_]+\}\}' "$PROMPT_FILE"  && { echo "REFUSING: an unfilled double-brace token (render with repin_and_launch_gate77.sh)" >&2; exit 8; }
grep -qF "reports/$REPORT/" "$PROMPT_FILE"    || { echo "REFUSING: the prompt does not name the report dir $REPORT" >&2; exit 8; }
_GO="$(grep -oE 'GO \(Seat [A-Z] [0-9]+(st|nd|rd|th)\): merge [0-9]+ on gate[0-9]+' "$PROMPT_FILE" | sort -u | tr '\n' '|')"
_GO_WANT="$(for ROW in $ROWS; do printf 'GO (%s): merge %s on gate77\n' "$SEAT" "$ROW"; done | sort -u | tr '\n' '|')"
[ "$_GO" = "$_GO_WANT" ]                      || { echo "REFUSING: the GO strings must be exactly '$_GO_WANT', found: $_GO" >&2; exit 8; }
for ROW in $ROWS; do grep -qwF "$(KJ rows.$ROW.head_expected)" "$PROMPT_FILE" || { echo "REFUSING: the prompt does not name #$ROW's head in full" >&2; exit 8; }; done
grep -qwF "$D_SHA" "$PROMPT_FILE"             || { echo "REFUSING: the prompt does not name the develop $D_SHA in full" >&2; exit 8; }
grep -qwF "$T_TREE" "$PROMPT_FILE"            || { echo "REFUSING: the prompt does not name the final tree $T_TREE in full" >&2; exit 8; }
PROMPT_JOINED="$(python3 -c 'import re,sys; print(re.sub(r"\n\s*", " ", open(sys.argv[1], encoding="utf-8").read()))' "$PROMPT_FILE")"
has() { printf '%s' "$PROMPT_JOINED" | grep -qF -- "$1"; }
has 'MEASURE, not conclude' && has 'RULE WHETHER IT BLOCKS' && has 'NAMES THE TREE' && has 'A check that prints nothing needs a control that prints' && has 'ASSERT THE FILENAME TOO' && has 'ASSERT THE TAMPER LANDED' && has 'A SKIP is NEVER a pass' && has 'NOT RUN is never a pass' && has 'COULD-NOT-CHECK IS A SKIP' && has 'THE HEAD IS A PARAMETER' && has 'ONE PARSER FOR BEFORE AND AFTER' && has 'SUBSET, never equality' && has 'RESTORE TO THE HEAD STATE' && has 'is NOT tag-balance evidence' && has 'a red from the WRONG CELL is not the arm' && has 'VERBATIM' && has 'NEVER `git merge-file --union`' && has 'the discriminator is the diff, not the SHA' && has 'NEVER `npm test` in services/api-gateway' || { echo "REFUSING: the measurement rules / head-parameter rule / one parser / subset / restore-to-head / tag balance / wrong-cell / keep-both verbatim / union hazard / diff-not-sha / api-gateway watch trap" >&2; exit 33; }
_KW="C1-PIN END-TREE BRANCH-TRAILER KEYS-ATTACH CLOSE-RESIDUE MERGE-CLEAN THROUGH-CODE TICKET-CLAIM SECURITY-SURFACE DECISION-INVARIANT SERVED-SPEC BASH-41 RED-PROOF REDGREEN-RERUN RESTORE-HEAD-STATE FULL-SUITE OWN-ARM PREFLIGHT-BY-HAND SIM-FINAL DOCS-PARITY TAG-BALANCE KEEP-BOTH UNION-HAZARD CHAIN-PREDICT COLLISION-TABLE C5-PR-TEXT SQUASH-SUBJECT SQUASH-BODY ATTRIBUTION BODY-CORRECTION ACTIONS-SUBSET ADVISORY-FREEZE CI-CORROBORATION READY-CLAIMS COLLISION-CENSUS NOT-TESTED-LIST TIERING SKILL-MUSTS LIVE-SWEEP-OWED REPIN DISK-ENOSPC REPORT-HASH-LAST"
_NKW=0
for _w in $_KW; do
  _NKW=$((_NKW + 1))
  printf '%s' "$PROMPT_JOINED" | grep -qE -- "(^|[^A-Za-z0-9-])$_w([^A-Za-z0-9-]|\$)" || { echo "REFUSING: the prompt does not carry the by-name keyword '$_w'" >&2; exit 33; }
done
has 'NO MERGE, NO PUSH to any PR branch, NO ticket state change' && has 'NEVER WRITE THE SHARED CHECKOUT' && has 'Never `rm`' && has 'No `az` command of any kind' && has 'You NEVER reply to Peter' && has 'never `git fetch` into the shared checkout' && has 'THE NAMED EXCEPTIONS to those holds — these and NO others' && has 'Do NOT start Docker' && has 'NEVER export GIT_SSH_COMMAND' && has 'NO comment on GitHub or Linear' && has 'Never `--no-verify`' || { echo "REFUSING: the HOLDS" >&2; exit 39; }
has '## MERGE ADDENDUM' && has 'is the LAST thing you write to report.md' && has 'sha256 report.md = <hex>' && has 'EVERY SUBJECT YOU PROPOSE MUST BE TRUE OF THE DIFF' && has 'FROM coagent@agentmail.to' && has 'NOT-TESTED.written-first.md' && has 'subjects land as written' \
  && grep -qF -- "$(KJ verdict_subject)" "$PROMPT_FILE" || { echo "REFUSING: MERGE ADDENDUM / REPORT-HASH-LAST / no-suffix subjects / verdict subject / sender" >&2; exit 25; }
REFS="refs/heads/develop"; for ROW in $ROWS; do REFS="$REFS refs/pull/$ROW/head refs/heads/$(KJ rows.$ROW.branch)"; done
if [ -n "${GATE77_LS:-}" ]; then _LS="$(cat "$GATE77_LS")"
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
else _DEVNOTE="NOT in the local store: descent NOT checked here (the repin checked it in the kit clone; the gate checks it in ITS OWN clone)"; fi
_ANY_OVR="$(env | grep -c '^GATE77_')"
NOTE="six rows at pull/head AND branch | raise_base ${B_SHA:0:12} x1 | origin develop ${CUR_DEV:0:12} == rendered ($_DEVNOTE) | order $O_ORD, final tree ${T_TREE:0:12} | merge seat $SEAT ($LANE) | comparator $COMP | $_NPIN pins EQUAL | prompt sha256 $(shasum -a 256 "$PROMPT_FILE" | cut -c1-16)"
if [ "$MODE" = "--check" ]; then
  echo "all guards pass:"; echo "  $NOTE"
  echo "  QA project, kit at its home, kit.json, $_NPIN pinned kit files hashing to their pins, KIT_REPORT.md, rendered prompt, head file (P x6 + B + D + S + C + O + T + Q == kit), repo; thinking directive; 8 kit files named; report dir; no fill token; the SIX GO strings from the merge seat ordinal; six heads + develop + the final tree in full"
  echo "  the prompt carries the measurement rules, $_NKW by-name keywords (as tokens), the holds + named exceptions, the addendum + REPORT-HASH-LAST rules, the verdict subject + sender"
  [ "$_ANY_OVR" != 0 ] && echo "  (a GATE77_* TEST OVERRIDE is set)"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"; exit 0
fi
[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — run this launcher in a cockpit pane, never inside a Bash tool" >&2; exit 21; }
[ "$_ANY_OVR" = 0 ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions "$(cat "$PROMPT_FILE")"
