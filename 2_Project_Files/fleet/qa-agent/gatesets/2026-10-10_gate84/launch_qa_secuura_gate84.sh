#!/bin/bash
# launch_qa_secuura_gate84.sh — cross-project QA agent, ONE gate (gate84; TIER 2 RE-GATE, round 2) over ONE Secuura/Blockchain PR: #1450 (KS-1426) at bbcbea0e3157, the fix commit for gate83's N-1450-1.
# Carried from launch_qa_secuura_gate83.sh; [g84] the head file's B line carries the BRANCH POINT (kit prs.1450.base = merge-base(develop, head)), NOT the head's parent (the head's ONE parent is the previous head d1d8b91b7c1f);
# the merge SEAT is the fill-at-launch token @MERGE_SEAT@ (an unfilled one refuses rc 8) with the ONE GO string DERIVED from the head file's S line; the keyword set and the holds are re-cut (N-1450-1 re-measure, the scratch-remote push exception).
# [g72] NO PR-SPECIFIC LITERAL lives in this file: the PR, branch, head, base, parent count, END_TREE, develop and seat come from
# head_at_launch.txt (written by repin_and_launch_gate84.sh from its REQUIRED arguments) and each is compared with kit.json — a wrong value refuses (rc 7).
# Every run (--check included) re-hashes EVERY pinned kit file against kit.json `script_sha256` and re-reads origin by ls-remote.
# exit 2: QA project missing / launcher not in its kit dir (a MOVED KIT).   exit 3: kit.json missing.   exit 4/5: prompt / repo missing.
# exit 30: a REQUIRED kit file is missing, empty, or has no pin.            exit 31: a kit file's sha256 != its pin (BAD PIN).
# exit 7: head_at_launch.txt missing / malformed / a value != kit.json (WRONG VALUE).
# exit 8: thinking directive / kit files named / report dir / an unfilled token ({{..}} or @MERGE_SEAT@) / the prepared body named / the GO string (exactly the one derived from the seat) / head, develop and base in full.
# exit 33: measurement rules + by-name keywords.   exit 39: HOLDS + named exceptions.   exit 25: addendum + REPORT-HASH-LAST + subject + sender.
# exit 6: origin pull/head or branch != the head.  exit 17: origin develop != the rendered develop, or not a descendant of the base.
# exit 21: a LAUNCH (not --check) with stdin not a TTY.   exit 16: a launch with a G84_* test override set.
# Test overrides (--check only): G84_PROMPT, G84_HEADFILE, G84_LS (ls-remote stand-in), G84_KITJSON, G84_FILES_DIR.
# MODEL: the exec line carries NO --model (fleet convention): the seat starts on the configured default and Wednesday types
# `/model claude-opus-5-5` at its prompt after launch; the prompt's MODEL-LINE tells the seat so (guarded, rc 33).
# Usage: launch_qa_secuura_gate84.sh [--check]
set -u
MODE="${1:-}"
QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
GS='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-10_gate84'
PROMPT_FILE="${G84_PROMPT:-$GS/prompt_gate84.rendered.txt}"
HEADFILE="${G84_HEADFILE:-$GS/head_at_launch.txt}"
KITJSON="${G84_KITJSON:-$GS/kit.json}"
FILES_DIR="${G84_FILES_DIR:-$GS}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
REQUIRED='lib_gate84.py c1_pin_gate84.py c2_code_gate84.py c3_cells_gate84.py gh_gate84.py prompt_gate84.txt launch_qa_secuura_gate84.sh repin_and_launch_gate84.sh'
KJ() { python3 -c 'import json,sys; v=json.load(open(sys.argv[1]))
for k in sys.argv[2].split("."): v=v[int(k)] if isinstance(v,list) else v[k]
print(" ".join(map(str,v)) if isinstance(v,list) else ("" if v is None else v))' "$KITJSON" "$1"; }
[ -d "$QA_DIR" ]      || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
_here="$(dirname "$(/bin/realpath "$0")")"
[ "$_here" = "$GS" ]  || { echo "REFUSING: this launcher lives in $_here but was written for $GS (a MOVED KIT)" >&2; exit 2; }
[ -s "$KITJSON" ]     || { echo "REFUSING: kit.json missing: $KITJSON" >&2; exit 3; }
URL="$(KJ github_url)"; REPORT="$(KJ report_dir_name)"; GO_TPL="$(KJ go_template)"

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
for _f in KIT_REPORT.md RULINGS_wednesday.md; do [ -s "$FILES_DIR/$_f" ] || { echo "REFUSING: the kit file $FILES_DIR/$_f is MISSING or empty" >&2; exit 30; }; done

[ -s "$PROMPT_FILE" ] || { echo "prompt file missing or empty: $PROMPT_FILE (render it with repin_and_launch_gate84.sh)" >&2; exit 4; }
[ -d "$REPO" ]        || { echo "repo under test missing: $REPO" >&2; exit 5; }
[ -s "$HEADFILE" ]    || { echo "REFUSING: $HEADFILE missing" >&2; exit 7; }
# --- [g72] the head file: P x1, B x1, T x1, D, S — each value compared with kit.json (WRONG VALUE -> rc 7) ---
[ "$(grep -c '^P ' "$HEADFILE")" = 1 ] || { echo "REFUSING: head file must carry exactly one 'P ' line" >&2; exit 7; }
[ "$(grep -c '^B ' "$HEADFILE")" = 1 ] || { echo "REFUSING: head file must carry exactly one 'B ' line" >&2; exit 7; }
for _t in D S; do [ "$(grep -c "^$_t " "$HEADFILE")" = 1 ] || { echo "REFUSING: head file must carry exactly one '$_t ' line" >&2; exit 7; }; done
[ "$(grep -c '^T ' "$HEADFILE")" = 1 ] || { echo "REFUSING: head file must carry exactly one 'T ' line" >&2; exit 7; }
set -- $(grep '^D ' "$HEADFILE"); D_SHA="${2:-}"
SEAT="$(grep '^S ' "$HEADFILE" | cut -d' ' -f2-)"; set --
printf '%s' "$SEAT" | grep -qE '^Seat [A-Z] [0-9]+(st|nd|rd|th)$' || { echo "REFUSING: the head file seat '$SEAT' is not 'Seat X nth'" >&2; exit 7; }
printf '%s' "$D_SHA" | grep -qE '^[0-9a-f]{40}$' || { echo "REFUSING: head file value '$D_SHA' is not a full 40-hex sha" >&2; exit 7; }
BASES=""
for _pr in $(KJ go_prs); do
  set -- $(grep "^P $_pr " "$HEADFILE"); _hp="${2:-}"; _hb="${3:-}"; _hs="${4:-}"
  set -- $(grep -E "^T $_pr " "$HEADFILE"); _ht="${3:-}"
  set -- $(grep -E "^B $_pr " "$HEADFILE"); _bpr="${2:-}"; _bsha="${3:-}"; _bn="${4:-}"; set --
  printf '%s' "$_hs" | grep -qE '^[0-9a-f]{40}$' || { echo "REFUSING: head file head for #$_pr '$_hs' is not a full 40-hex sha" >&2; exit 7; }
  printf '%s' "$_ht" | grep -qE '^[0-9a-f]{40}$' || { echo "REFUSING: head file tree for #$_pr '$_ht' is not a full 40-hex sha" >&2; exit 7; }
  printf '%s' "$_bsha" | grep -qE '^[0-9a-f]{40}$' || { echo "REFUSING: head file base for #$_pr '$_bsha' is not a full 40-hex sha" >&2; exit 7; }
  [ "$_hp" = "$_pr" ]                                  || { echo "REFUSING: head file has no 'P $_pr ' line" >&2; exit 7; }
  [ "$_bpr" = "$_pr" ]                                 || { echo "REFUSING: head file has no 'B $_pr ' line" >&2; exit 7; }
  [ "$_hb" = "$(KJ prs.$_pr.branch)" ]                 || { echo "REFUSING: WRONG VALUE #$_pr branch '$_hb' != kit $(KJ prs.$_pr.branch)" >&2; exit 7; }
  [ "$_hs" = "$(KJ prs.$_pr.head_expected)" ]          || { echo "REFUSING: WRONG VALUE #$_pr head '$_hs' != kit $(KJ prs.$_pr.head_expected) (re-draft the kit for a moved head)" >&2; exit 7; }
  [ "$_ht" = "$(KJ prs.$_pr.end_tree)" ]               || { echo "REFUSING: WRONG VALUE #$_pr end-tree '$_ht' != kit $(KJ prs.$_pr.end_tree)" >&2; exit 7; }
  [ "$_bsha" = "$(KJ prs.$_pr.base)" ]                || { echo "REFUSING: WRONG VALUE #$_pr base '$_bsha' != the kit's BRANCH POINT $(KJ prs.$_pr.base) (merge-base(develop, head); NOT head^)" >&2; exit 7; }
  [ "$_bn" = "$(KJ prs.$_pr.parent_count)" ]           || { echo "REFUSING: WRONG VALUE #$_pr parents-n '$_bn' != kit $(KJ prs.$_pr.parent_count)" >&2; exit 7; }
  eval "HP_$_pr=\$_hs; HB_$_pr=\$_hb; HT_$_pr=\$_ht; HBS_$_pr=\$_bsha"; BASES="$BASES $_bsha"
done
BASES="$(printf '%s\n' $BASES | sort -u)"
GO_WANT="$(for _pr in $(KJ go_prs); do printf '%s\n' "$GO_TPL" | sed "s/{seat}/$SEAT/; s/{pr}/$_pr/"; done | sort -u)"
[ "$(head -n 1 "$PROMPT_FILE")" = "ultrathink" ] || { echo "REFUSING: the prompt does not open with the thinking directive" >&2; exit 8; }
for _f in KIT_REPORT.md RULINGS_wednesday.md kit.json lib_gate84.py c1_pin_gate84.py c2_code_gate84.py c3_cells_gate84.py gh_gate84.py; do
  grep -qF "$GS/$_f" "$PROMPT_FILE" || { echo "REFUSING: the kit file $GS/$_f is not named in the prompt" >&2; exit 8; }
done
grep -qE '\{\{[A-Z0-9_]+\}\}' "$PROMPT_FILE"  && { echo "REFUSING: an unfilled double-brace token (render with repin_and_launch_gate84.sh)" >&2; exit 8; }
grep -qF '@MERGE_SEAT@' "$PROMPT_FILE"  && { echo "REFUSING: the fill-at-launch token @MERGE_SEAT@ is unfilled (the merge seat is a REQUIRED --seat argument of repin_and_launch_gate84.sh)" >&2; exit 8; }
for _pb in prepared_body push_log_head push_log_prev; do grep -qF "$(KJ prs.1450.$_pb)" "$PROMPT_FILE" || { echo "REFUSING: the prompt does not name the $_pb path $(KJ prs.1450.$_pb)" >&2; exit 8; }; done
grep -qF "reports/$REPORT/" "$PROMPT_FILE"    || { echo "REFUSING: the prompt does not name the report dir $REPORT" >&2; exit 8; }
_GO="$(grep -oE 'GO \(Seat [A-Z] [0-9]+(st|nd|rd|th)\): merge [0-9]+ on gate[0-9]+' "$PROMPT_FILE" | sort -u)"
[ "$_GO" = "$GO_WANT" ]                       || { echo "REFUSING: the GO strings must be exactly the one derived from the seat ($(printf '%s' "$GO_WANT" | tr '\n' '|')), found: $(printf '%s' "$_GO" | tr '\n' '|')" >&2; exit 8; }
for _pr in $(KJ go_prs); do
  eval "_h=\$HP_$_pr"; grep -qwF "$_h" "$PROMPT_FILE" || { echo "REFUSING: the prompt does not name the #$_pr head $_h in full" >&2; exit 8; }
done
grep -qwF "$D_SHA" "$PROMPT_FILE"             || { echo "REFUSING: the prompt does not name the develop $D_SHA in full" >&2; exit 8; }
for _b in $BASES; do grep -qwF "$_b" "$PROMPT_FILE" || { echo "REFUSING: the prompt does not name the base $_b in full" >&2; exit 8; }; done
PROMPT_JOINED="$(python3 -c 'import re,sys; print(re.sub(r"\n\s*", " ", open(sys.argv[1], encoding="utf-8").read()))' "$PROMPT_FILE")"
has() { printf '%s' "$PROMPT_JOINED" | grep -qF -- "$1"; }
has 'THE HEADS ARE PARAMETERS' && has 'A check that prints nothing needs a control that prints' && has 'Every zero sits beside a control of the same instrument that fired' && has 'assert the FILENAME too' && has 'ASSERT THE TAMPER LANDED' && has 'A suite that fails to LOAD is never a red' && has 'A SKIP is never a pass' && has 'NOT RUN is never a pass' && has 'CODE-ONLY' && has 'Classify each red by its PATH against comparators' && has 'Opus 5.5 (`claude-opus-5-5`)' || { echo "REFUSING: the measurement rules / head-parameter rule / load-failure rule / code-only census rule / by-path Actions rule / MODEL-LINE" >&2; exit 33; }
_KW="C1-PIN END-TREE NO-TRAILER NO-COAUTHOR SUBJECT-DECLARED KEYS-OWN-ONLY MODES NO-NEW-LEG DEVELOP-OVERLAP CODE-CLAIMS PAYLOAD-EQUALS-PATCH CELLS-BASE-HEAD-PREV SHELL-ARMS N-1450-1-REMEASURE HOOK-PUSH-WORKTREE INHERITED-GIT-DIR EXIT-CODES-12-OF-12 STUB-GIT EMPTY-ARRAY-F2 CWD-Q-CWD1426 SIBLINGS TAMPER-GATE83-T5B-T11 T9-EQUIVALENT-MUTANT DOCS-CLAIM DOCS-COMPOSITION DOCS-PARENT-G83-1 CONFLICT-SET ACTIONS-BY-PATH C5-PR-TEXT PREPARED-BODY ATTRIBUTION LINEAR-STATE COLLISION-CENSUS NOT-TESTED-LIST PLATFORM-SUITES-NOT-RUN TIERING DISK-ENOSPC MODEL-LINE MERGE-SEAT REPORT-HASH-LAST"
_NKW=0
for _w in $_KW; do
  _NKW=$((_NKW + 1))
  printf '%s' "$PROMPT_JOINED" | grep -qE -- "(^|[^A-Za-z0-9-])$_w([^A-Za-z0-9-]|\$)" || { echo "REFUSING: the prompt does not carry the by-name keyword '$_w'" >&2; exit 33; }
done
has 'NO MERGE, NO PUSH to any PR branch, NO ticket state change' && has 'NEVER WRITE THE SHARED CHECKOUT' && has 'Never `rm`' && has 'No `az` command of any kind' && has 'You NEVER reply to Peter' && has 'never `git fetch` into it' && has 'THE NAMED EXCEPTIONS to those holds, these and NO others' && has 'DO NOT start Docker' && has 'NEVER export GIT_SSH_COMMAND' && has 'never comment on GitHub or Linear' && has 'Never create, plant or write ANY path under /Volumes/DevMASTER/!CODING except your report directory' && has '`s-f10-*` is NOT YOURS' && has 'NEVER mail any builder seat' && has 'git push to a scratch BARE remote' && has 'never touch core.hooksPath of the shared checkout' && has 'NEVER run a shell suite that names env.example or bootstrap-env.sh from a directory inside a git repository' && has 'NO `npm ci`, NO `npm install`, NO `npx`' && has 'NEVER run the leg against the real tree' || { echo "REFUSING: the HOLDS" >&2; exit 39; }
has '## MERGE ADDENDUM' && has 'is the LAST thing you write to report.md' && has 'sha256 report.md = <hex>' && has 'EVERY SUBJECT YOU PROPOSE MUST BE TRUE OF THE DIFF' && has 'FROM coagent@agentmail.to' && has 'NOT-TESTED.written-first.md' \
  && grep -qF -- "$(KJ verdict_subject)" "$PROMPT_FILE" || { echo "REFUSING: MERGE ADDENDUM / REPORT-HASH-LAST / verdict subject / sender" >&2; exit 25; }
REFS="refs/heads/develop"; for _pr in $(KJ go_prs); do eval "_b=\$HB_$_pr"; REFS="$REFS refs/pull/$_pr/head refs/heads/$_b"; done
if [ -n "${G84_LS:-}" ]; then _LS="$(cat "$G84_LS")"
else _LS="$(env -u GIT_SSH_COMMAND git -C "$REPO" -c core.sshCommand="$(git -C "$REPO" config --get core.sshCommand)" ls-remote "$URL" $REFS)"; fi
get() { printf '%s\n' "$_LS" | awk -v r="$1" '$2==r{print $1}'; }
CUR_DEV="$(get refs/heads/develop)"
for _pr in $(KJ go_prs); do
  eval "_h=\$HP_$_pr; _b=\$HB_$_pr"
  [ "$(get "refs/pull/$_pr/head")" = "$_h" ] && [ "$(get "refs/heads/$_b")" = "$_h" ] || { echo "REFUSING: #$_pr pull/head '$(get "refs/pull/$_pr/head")' / branch '$(get "refs/heads/$_b")' != $_h — a verdict is valid ONLY at its head" >&2; exit 6; }
done
[ "$CUR_DEV" = "$D_SHA" ] || { echo "REFUSING: origin develop '$CUR_DEV' != the rendered develop $D_SHA (re-run the repin script)" >&2; exit 17; }
if git -C "$REPO" cat-file -t "$CUR_DEV" >/dev/null 2>&1; then
  for _b in $BASES; do git -C "$REPO" merge-base --is-ancestor "$_b" "$CUR_DEV" || { echo "REFUSING: origin develop $CUR_DEV does not descend from the base $_b" >&2; exit 17; }; done
  _DEVNOTE="descends from every base ($(printf '%s' "$BASES" | tr '\n' ' ' | sed 's/\([0-9a-f]\{12\}\)[0-9a-f]*/\1/g'))"
else _DEVNOTE="NOT in the local store: descent NOT checked here (the gate checks it in ITS OWN clone; the repin script checked it in the kit clone)"; fi
_ANY_OVR="$(env | grep -c '^G84_')"
NOTE="#1450 ${HP_1450:0:12} (base ${HBS_1450:0:12}) at pull/head AND branch | END_TREE ${HT_1450:0:12} | origin develop ${CUR_DEV:0:12} == rendered ($_DEVNOTE) | seat $SEAT: $(printf '%s' "$_GO" | tr '\n' '|') | $_NPIN pins EQUAL | prompt sha256 $(shasum -a 256 "$PROMPT_FILE" | cut -c1-16)"
if [ "$MODE" = "--check" ]; then
  echo "all guards pass:"; echo "  $NOTE"
  echo "  QA project, kit at its home, kit.json, $_NPIN pinned kit files hashing to their pins, KIT_REPORT.md + RULINGS_wednesday.md, rendered prompt, head file (1 PR + 1 base + 1 tree + develop + seat == kit), repo; thinking directive; 8 kit files named (+ the prepared body and both raw push logs); report dir; no fill token; the GO string derived from the seat; the head + develop + base in full"
  echo "  the prompt carries the measurement rules, $_NKW by-name keywords (as tokens), the holds + named exceptions, the addendum + REPORT-HASH-LAST rules, the verdict subject + sender"
  [ "$_ANY_OVR" != 0 ] && echo "  (a G84_* TEST OVERRIDE is set)"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"; exit 0
fi
[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — run this launcher in a cockpit pane, never inside a Bash tool" >&2; exit 21; }
[ "$_ANY_OVR" = 0 ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions "$(cat "$PROMPT_FILE")"
