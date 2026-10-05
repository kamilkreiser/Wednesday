#!/bin/bash
# launch_qa_secuura_ks1388_1387.sh — cross-project QA agent, ONE gate (gate62) over ONE Secuura/Blockchain PR, FROZEN at ONE:
# #1387 KS-1388 s1 (T2, ROUND 1): both observability env examples point the nginx status URI at :80. Author Seat B 61st (WRAPPED);
# merger <B successor> (Wednesday names it). STATIC prompt (no fill step): the head and develop are written into the prompt and this
# launcher, and the launcher RE-READS origin before every launch, so a moved head or develop REFUSES instead of launching stale.
# exit 2: QA project missing, or this launcher is not in the kit dir it was written for (a MOVED KIT).   exit 3/4/5: kit / prompt / repo missing.
# exit 8: thinking directive / kit files / report dir / GO placeholder / head-in-full / a stray fill token.
# exit 6: origin pull/1387/head or the branch is not the pinned head.   exit 17: origin develop != the pinned develop.
# exit 21: the LAUNCH path refuses when stdin is not a TTY (`--check` is headless).   exit 16: a launch with a G62_* test override set.
# G62_PROMPT / G62_LS (a file standing in for the ls-remote output): test overrides, --check only.
# Opus by the configured default: the exec line carries NO --model.   Usage: launch_qa_secuura_ks1388_1387.sh [--check]
set -u
QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
GS='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-05_gate62'
PROMPT_FILE="${G62_PROMPT:-$GS/prompt_gate62.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
PR='1387'
HEAD_SHA='67324c7604fd871637b197395139841da9913122'
BRANCH='refs/heads/feature/ks-1388-observability-env-examples-status-uri-80-b61-1'
DEVELOP_SHA='f01c1da5717fdcb80a5e1aeeaa8ff9f0f00edd80'
REPORT='2026-10-05-ks1388-1387-g62'
[ -d "$QA_DIR" ]      || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
_here="$(dirname "$(/bin/realpath "$0")")"
[ "$_here" = "$GS" ]  || { echo "REFUSING: this launcher lives in $_here but was written for $GS (a MOVED KIT)" >&2; exit 2; }
[ -s "$GS/kit.json" ] || { echo "kit.json missing: $GS" >&2; exit 3; }
[ -s "$PROMPT_FILE" ] || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]        || { echo "repo under test missing: $REPO" >&2; exit 5; }
[ "$(head -n 1 "$PROMPT_FILE")" = "ultrathink" ] || { echo "REFUSING: the prompt does not open with the thinking directive" >&2; exit 8; }
for _f in README.md kit.json lib_gate62.py c1_pin_gate62.py c2_held_gate62.py c4_docs_gate62.py c5_prtext_gate62.py gh_census_gate62.py; do
  [ -s "$GS/$_f" ] && grep -qF "$GS/$_f" "$PROMPT_FILE" || { echo "REFUSING: the kit file $GS/$_f is missing, empty, or not named in the prompt" >&2; exit 8; }
done
grep -qF "reports/$REPORT/" "$PROMPT_FILE"              || { echo "REFUSING: the prompt does not name the report dir $REPORT" >&2; exit 8; }
grep -qF 'GO (Seat <B successor>): merge 1387 on gate62' "$PROMPT_FILE" || { echo "REFUSING: the prompt does not carry the GO string with its placeholder" >&2; exit 8; }
grep -qF 'GO (Seat B 61st)' "$PROMPT_FILE"              && { echo "REFUSING: the prompt names the WRAPPED seat in a GO" >&2; exit 8; }
grep -qwF "$HEAD_SHA" "$PROMPT_FILE"                    || { echo "REFUSING: the prompt does not name the head in full" >&2; exit 8; }
grep -qF 'never use 0c0f8e5e' "$PROMPT_FILE"            || { echo "REFUSING: the prompt does not forbid the fabricated tree" >&2; exit 8; }
grep -qF 'NOT-TESTED.written-first.md' "$PROMPT_FILE" && grep -qF 'REPORT-HASH-LAST' "$PROMPT_FILE" && grep -qF 'FROM coagent@agentmail.to' "$PROMPT_FILE" \
                                                        || { echo "REFUSING: NOT-TESTED-first / REPORT-HASH-LAST / sender missing" >&2; exit 8; }
grep -qE '\{\{[A-Z0-9_]+\}\}' "$PROMPT_FILE"            && { echo "REFUSING: an unfilled double-brace token" >&2; exit 8; }
if [ -n "${G62_LS:-}" ]; then _LS="$(cat "$G62_LS")"; else _LS="$(git -C "$REPO" ls-remote origin refs/heads/develop "$BRANCH" "refs/pull/$PR/head")"; fi
CUR_DEV="$(printf '%s\n' "$_LS" | awk '$2=="refs/heads/develop"{print $1}')"
[ "$CUR_DEV" = "$DEVELOP_SHA" ] || { echo "REFUSING: origin develop '$CUR_DEV' != the pinned develop $DEVELOP_SHA — a docs-only merge-in (new head) or a RE-DRAFT first (README section 6)" >&2; exit 17; }
_PH="$(printf '%s\n' "$_LS" | awk -v r="refs/pull/$PR/head" '$2==r{print $1}')"; _BH="$(printf '%s\n' "$_LS" | awk -v r="$BRANCH" '$2==r{print $1}')"
[ "$_PH" = "$HEAD_SHA" ] && [ "$_BH" = "$HEAD_SHA" ] || { echo "REFUSING: #$PR pull/head '$_PH' / branch '$_BH' != the pinned head $HEAD_SHA — a verdict is valid ONLY at its head (RE-DRAFT)" >&2; exit 6; }
_ANY_OVR="$(env | grep -c '^G62_')"
NOTE="origin develop ${CUR_DEV:0:12} == pinned | #$PR ${HEAD_SHA:0:12} at branch AND pull/head | prompt sha256 $(shasum -a 256 "$PROMPT_FILE" | cut -c1-16)"
if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"; echo "  $NOTE"
  echo "  QA project, kit, prompt, repo present; kit at its home; thinking directive; 8 kit files named; report dir; GO placeholder; no wrapped seat in a GO; head in full; fabricated tree forbidden; no fill token"
  [ "$_ANY_OVR" != 0 ] && echo "  (a G62_* TEST OVERRIDE is set)"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"; exit 0
fi
[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — run this launcher in a cockpit pane, never inside a Bash tool" >&2; exit 21; }
[ "$_ANY_OVR" = 0 ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions "$(cat "$PROMPT_FILE")"
