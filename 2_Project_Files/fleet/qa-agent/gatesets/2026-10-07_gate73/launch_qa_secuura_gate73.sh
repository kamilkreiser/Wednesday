#!/bin/bash
# launch_qa_secuura_gate73.sh — cross-project QA agent, ONE BATCHED T2 gate (gate73) over Secuura/Blockchain #1407 #1409 #1408 #1410 on ONE base.
# Carried from launch_qa_secuura_gate72.sh. NO PR-SPECIFIC LITERAL lives in this file: the four heads, branches, base, END_TREEs, develop, the
# landing order and the merge seat come from head_at_launch.txt (written by repin_and_launch_gate73.sh from its REQUIRED arguments) and each
# is compared with kit.json — a wrong value refuses (rc 7).
# Every run (--check included) re-hashes EVERY pinned kit file against kit.json `script_sha256` and re-reads origin by ls-remote.
# exit 2: QA project missing / launcher not in its kit dir (a MOVED KIT).   exit 3: kit.json missing.   exit 4/5: prompt / repo missing.
# exit 30: a REQUIRED kit file is missing, empty, or has no pin.            exit 31: a kit file's sha256 != its pin (BAD PIN).
# exit 7: head_at_launch.txt missing / malformed / a value != kit.json (WRONG VALUE).
# exit 8: merge seat UNRULED (kit.json merge_seat null) / thinking directive / kit files named / report dir / an unfilled token /
#         the GO strings (exactly the four from the ruled merge seat, no author seat) / heads + develop in full.
# exit 33: measurement rules + by-name keywords.   exit 39: HOLDS + named exceptions.   exit 25: addendum + REPORT-HASH-LAST + subject + sender.
# exit 6: an origin pull/head or branch != its head.  exit 17: origin develop != the rendered develop, or not a descendant of the base.
# exit 21: a LAUNCH (not --check) with stdin not a TTY.   exit 16: a launch with a G73_* test override set.
# Test overrides (--check only): G73_PROMPT, G73_HEADFILE, G73_LS (ls-remote stand-in), G73_KITJSON, G73_FILES_DIR.
# Opus by the configured default: the exec line carries NO --model.   Usage: launch_qa_secuura_gate73.sh [--check]
set -u
MODE="${1:-}"
QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
GS='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-07_gate73'
PROMPT_FILE="${G73_PROMPT:-$GS/prompt_gate73.rendered.txt}"
HEADFILE="${G73_HEADFILE:-$GS/head_at_launch.txt}"
KITJSON="${G73_KITJSON:-$GS/kit.json}"
FILES_DIR="${G73_FILES_DIR:-$GS}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
REQUIRED='lib_gate73.py composee5_copy.py c1_pin_gate73.py c2_product_gate73.py c3_suites_gate73.py c4_docs_gate73.py gh_gate73.py prompt_gate73.txt launch_qa_secuura_gate73.sh repin_and_launch_gate73.sh'
ROWS='1407 1409 1408 1410'
KJ() { python3 -c 'import json,sys; v=json.load(open(sys.argv[1]))
for k in sys.argv[2].split("."): v=v[int(k)] if isinstance(v,list) else v[k]
print(" ".join(map(str,v)) if isinstance(v,list) else ("" if v is None else v))' "$KITJSON" "$1"; }
[ -d "$QA_DIR" ]      || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
_here="$(dirname "$(/bin/realpath "$0")")"
[ "$_here" = "$GS" ]  || { echo "REFUSING: this launcher lives in $_here but was written for $GS (a MOVED KIT)" >&2; exit 2; }
[ -s "$KITJSON" ]     || { echo "REFUSING: kit.json missing: $KITJSON" >&2; exit 3; }
URL="$(KJ github_url)"; REPORT="$(KJ report_dir_name)"; SEAT="$(KJ merge_seat)"

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
[ -s "$FILES_DIR/composed_2026-10-07/MANIFEST.txt" ] || { echo "REFUSING: composed_2026-10-07/MANIFEST.txt is MISSING (the merge seat's verbatim docs)" >&2; exit 30; }

# --- the merge seat must be RULED (Q-SEAT) ---
[ -n "$SEAT" ] || { echo "REFUSING: RULING NEEDED — kit.json merge_seat is null (RULINGS Q-SEAT). Wednesday rules the merge seat, writes it into kit.json, re-pins and re-renders." >&2; exit 8; }
printf '%s' "$SEAT" | grep -qE '^Seat [A-Z] [0-9]+(st|nd|rd|th)$' || { echo "REFUSING: merge_seat '$SEAT' is not of the form 'Seat <L> <Nth>'" >&2; exit 8; }
case "$SEAT" in "Seat R 9th"|"Seat E 10th") echo "REFUSING: the merge seat may not be an AUTHOR seat ($SEAT)" >&2; exit 8;; esac

[ -s "$PROMPT_FILE" ] || { echo "prompt file missing or empty: $PROMPT_FILE (render it with repin_and_launch_gate73.sh)" >&2; exit 4; }
[ -d "$REPO" ]        || { echo "repo under test missing: $REPO" >&2; exit 5; }
[ -s "$HEADFILE" ]    || { echo "REFUSING: $HEADFILE missing" >&2; exit 7; }
# --- the head file: P x4, B, D, O, S; each value compared with kit.json (WRONG VALUE -> rc 7) ---
[ "$(grep -c '^P ' "$HEADFILE")" = 4 ] || { echo "REFUSING: head file must carry exactly four 'P ' lines" >&2; exit 7; }
for _t in B D O S; do [ "$(grep -c "^$_t " "$HEADFILE")" = 1 ] || { echo "REFUSING: head file must carry exactly one '$_t ' line" >&2; exit 7; }; done
for _r in $ROWS; do
  set -- $(grep "^P $_r " "$HEADFILE"); _br="${3:-}"; _sha="${4:-}"; _tree="${5:-}"; set --
  printf '%s' "$_sha$_tree" | grep -qE '^[0-9a-f]{80}$' || { echo "REFUSING: head file P $_r: head / tree not full 40-hex" >&2; exit 7; }
  [ "$_br" = "$(KJ rows.$_r.branch)" ]          || { echo "REFUSING: WRONG VALUE #$_r branch '$_br' != kit" >&2; exit 7; }
  [ "$_sha" = "$(KJ rows.$_r.head_expected)" ]   || { echo "REFUSING: WRONG VALUE #$_r head '$_sha' != kit $(KJ rows.$_r.head_expected) (re-draft the kit for a moved head)" >&2; exit 7; }
  [ "$_tree" = "$(KJ rows.$_r.end_tree)" ]       || { echo "REFUSING: WRONG VALUE #$_r END_TREE '$_tree' != kit" >&2; exit 7; }
done
set -- $(grep '^B ' "$HEADFILE"); B_SHA="${2:-}"; B_N="${3:-}"
set -- $(grep '^D ' "$HEADFILE"); D_SHA="${2:-}"
set -- $(grep '^O ' "$HEADFILE"); O_ORD="${2:-}"; set --
S_SEAT="$(grep '^S ' "$HEADFILE" | cut -c3-)"
[ "$B_SHA" = "$(KJ base)" ] && [ "$B_N" = 1 ] || { echo "REFUSING: WRONG VALUE base '$B_SHA' x'$B_N' != kit $(KJ base) x1" >&2; exit 7; }
printf '%s' "$D_SHA" | grep -qE '^[0-9a-f]{40}$' || { echo "REFUSING: head file develop '$D_SHA' is not full 40-hex" >&2; exit 7; }
[ "$(printf '%s' "$O_ORD" | tr ',' '\n' | sort | tr '\n' ' ')" = "1407 1408 1409 1410 " ] || { echo "REFUSING: head file order '$O_ORD' must name each of the four rows exactly once" >&2; exit 7; }
[ "$S_SEAT" = "$SEAT" ] || { echo "REFUSING: WRONG VALUE head-file merge seat '$S_SEAT' != kit '$SEAT'" >&2; exit 7; }

[ "$(head -n 1 "$PROMPT_FILE")" = "ultrathink" ] || { echo "REFUSING: the prompt does not open with the thinking directive" >&2; exit 8; }
for _f in KIT_REPORT.md kit.json lib_gate73.py c1_pin_gate73.py c2_product_gate73.py c3_suites_gate73.py c4_docs_gate73.py gh_gate73.py composed_2026-10-07/MANIFEST.txt; do
  grep -qF "$GS/$_f" "$PROMPT_FILE" || { echo "REFUSING: the kit file $GS/$_f is not named in the prompt" >&2; exit 8; }
done
grep -qE '\{\{[A-Z0-9_]+\}\}' "$PROMPT_FILE"  && { echo "REFUSING: an unfilled double-brace token (render with repin_and_launch_gate73.sh)" >&2; exit 8; }
grep -qF "reports/$REPORT/" "$PROMPT_FILE"    || { echo "REFUSING: the prompt does not name the report dir $REPORT" >&2; exit 8; }
_GO="$(grep -oE 'GO \(Seat [A-Z] [0-9]+(st|nd|rd|th)\): merge [0-9]+ on gate[0-9]+' "$PROMPT_FILE" | sort -u | tr '\n' '|')"
_GO_WANT="$(for _r in $ROWS; do echo "GO ($SEAT): merge $_r on gate73"; done | sort -u | tr '\n' '|')"
[ "$_GO" = "$_GO_WANT" ]                      || { echo "REFUSING: the GO strings must be exactly the four from the ruled seat ($_GO_WANT), found: $_GO" >&2; exit 8; }
for _r in $ROWS; do grep -qwF "$(KJ rows.$_r.head_expected)" "$PROMPT_FILE" || { echo "REFUSING: the prompt does not name #$_r's head in full" >&2; exit 8; }; done
grep -qwF "$D_SHA" "$PROMPT_FILE"             || { echo "REFUSING: the prompt does not name the develop $D_SHA in full" >&2; exit 8; }
PROMPT_JOINED="$(python3 -c 'import re,sys; print(re.sub(r"\n\s*", " ", open(sys.argv[1], encoding="utf-8").read()))' "$PROMPT_FILE")"
has() { printf '%s' "$PROMPT_JOINED" | grep -qF -- "$1"; }
has 'MEASURE, not conclude' && has 'RULE WHETHER IT BLOCKS' && has 'NAMES THE TREE' && has 'A check that prints nothing needs a control that prints' && has 'ASSERT THE FILENAME TOO' && has 'ASSERT THE TAMPER LANDED' && has 'A SKIP is NEVER a pass' && has 'NOT RUN is never a pass' && has 'COULD-NOT-CHECK IS A SKIP' && has 'THE HEAD IS A PARAMETER' && has 'ONE PARSER FOR BEFORE AND AFTER' && has 'SUBSET, never equality' && has 'VERBATIM' || { echo "REFUSING: the measurement rules / head-parameter rule / one parser / subset predicate / verbatim docs" >&2; exit 33; }
_KW="C1-PIN END-TREE NO-TRAILER NO-COAUTHOR SUBJECT-EXACT KEYS-OWN-ONLY NO-NEW-LEG DISJOINT PREEXISTING-MISMATCH PRODUCT-READ SKILL-5D CONTRACT-ONLY CLASS-AUDIT RED-FIRST LABEL-MATRIX NOANCHOR-GAP DRIVE-1435 NULL-SIGNATURE OPENAPI-CHECK SUITES-OWN SHELL-SET PERF-SUBSET DOCS-ONE-BLOCK FLOW-UNIQUE-KEYED OWN-KEY-ONLY TAG-BALANCE CALIBRATE MERGE-IN-CHAIN MERGE-ORDER UNION-HAZARD QM-READBACK C5-PR-TEXT LIVE-SWEEP PLATFORM-SUITES-UNMEASURED ACTIONS-SUBSET ADVISORY-FREEZE READY-CLAIMS COLLISION-CENSUS NOT-TESTED-LIST TIERING SKILL-MUSTS DISK-ENOSPC REPORT-HASH-LAST"
_NKW=0
for _w in $_KW; do
  _NKW=$((_NKW + 1))
  printf '%s' "$PROMPT_JOINED" | grep -qE -- "(^|[^A-Za-z0-9-])$_w([^A-Za-z0-9-]|\$)" || { echo "REFUSING: the prompt does not carry the by-name keyword '$_w'" >&2; exit 33; }
done
has 'NO MERGE, NO PUSH to any PR branch, NO ticket state change' && has 'NEVER WRITE THE SHARED CHECKOUT' && has 'Never `rm`' && has 'No `az` command of any kind' && has 'You NEVER reply to Peter' && has 'never `git fetch` into the shared checkout' && has 'THE NAMED EXCEPTIONS to those holds — these and NO others' && has 'Do NOT start Docker' && has 'NEVER export GIT_SSH_COMMAND' && has 'NO comment on GitHub or Linear' || { echo "REFUSING: the HOLDS" >&2; exit 39; }
has '## MERGE ADDENDUM' && has 'is the LAST thing you write to report.md' && has 'sha256 report.md = <hex>' && has 'EVERY SUBJECT YOU PROPOSE MUST BE TRUE OF THE DIFF' && has 'FROM coagent@agentmail.to' && has 'NOT-TESTED.written-first.md' \
  && grep -qF -- "$(KJ verdict_subject)" "$PROMPT_FILE" || { echo "REFUSING: MERGE ADDENDUM / REPORT-HASH-LAST / verdict subject / sender" >&2; exit 25; }
REFS="refs/heads/develop"
for _r in $ROWS; do REFS="$REFS refs/pull/$_r/head refs/heads/$(KJ rows.$_r.branch)"; done
if [ -n "${G73_LS:-}" ]; then _LS="$(cat "$G73_LS")"
else _LS="$(env -u GIT_SSH_COMMAND git -C "$REPO" -c core.sshCommand="$(git -C "$REPO" config --get core.sshCommand)" ls-remote "$URL" $REFS)"; fi
get() { printf '%s\n' "$_LS" | awk -v r="$1" '$2==r{print $1}'; }
CUR_DEV="$(get refs/heads/develop)"
for _r in $ROWS; do
  _h="$(KJ rows.$_r.head_expected)"; _b="$(KJ rows.$_r.branch)"
  [ "$(get "refs/pull/$_r/head")" = "$_h" ] && [ "$(get "refs/heads/$_b")" = "$_h" ] || { echo "REFUSING: #$_r pull/head '$(get "refs/pull/$_r/head")' / branch '$(get "refs/heads/$_b")' != $_h — a verdict is valid ONLY at its head" >&2; exit 6; }
done
[ -n "$CUR_DEV" ] && [ "$CUR_DEV" = "$D_SHA" ] || { echo "REFUSING: origin develop '$CUR_DEV' != the rendered develop $D_SHA (re-run the repin script)" >&2; exit 17; }
if git -C "$REPO" cat-file -t "$CUR_DEV" >/dev/null 2>&1; then
  git -C "$REPO" merge-base --is-ancestor "$B_SHA" "$CUR_DEV" || { echo "REFUSING: origin develop $CUR_DEV does not descend from $B_SHA" >&2; exit 17; }
  _DEVNOTE="descends from ${B_SHA:0:12}"
else _DEVNOTE="NOT in the local store: descent NOT checked here (the gate checks it in ITS OWN clone; the repin script checked it in the kit clone)"; fi
_ANY_OVR="$(env | grep -c '^G73_')"
NOTE="#1407 #1409 #1408 #1410 at pull/head AND branch | base ${B_SHA:0:12} x1 | origin develop ${CUR_DEV:0:12} == rendered ($_DEVNOTE) | order $O_ORD | merge seat $SEAT | $_NPIN pins EQUAL | prompt sha256 $(shasum -a 256 "$PROMPT_FILE" | cut -c1-16)"
if [ "$MODE" = "--check" ]; then
  echo "all guards pass:"; echo "  $NOTE"
  echo "  QA project, kit at its home, kit.json, $_NPIN pinned kit files hashing to their pins, KIT_REPORT.md, the composed MANIFEST, rendered prompt, head file (4 P + B + D + O + S == kit), repo; thinking directive; 9 kit files named; report dir; no fill token; the four GO strings from the ruled seat; four heads + develop in full"
  echo "  the prompt carries the measurement rules, $_NKW by-name keywords (as tokens), the holds + named exceptions, the addendum + REPORT-HASH-LAST rules, the verdict subject + sender"
  [ "$_ANY_OVR" != 0 ] && echo "  (a G73_* TEST OVERRIDE is set)"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"; exit 0
fi
[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — run this launcher in a cockpit pane, never inside a Bash tool" >&2; exit 21; }
[ "$_ANY_OVR" = 0 ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions "$(cat "$PROMPT_FILE")"
