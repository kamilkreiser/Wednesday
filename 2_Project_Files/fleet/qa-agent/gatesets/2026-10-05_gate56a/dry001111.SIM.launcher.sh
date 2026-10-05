#!/bin/bash
# dry001111.SIM.launcher.sh — cross-project QA agent, ONE gate (gate56a, round 56) over TWO Secuura/Blockchain PRs, FROZEN at TWO:
# #9903 KS-528 (T2): the two react-router baseline rows re-dated to 2026-10-31; #9904 KS-769 (T2): the mobile-tree exclusion re-dated
# to 2027-01-01. Merger: Seat B 59th (the author), one GO per PR. PINNED by repin_and_launch_gate56a.sh at 2026-10-05T00:11:11Z from its own
# ls-remote + PULLS API reads: #9903 fcd8c906a63316b0bc558f9710c6605971daa5bd on feature/ks-528-react-router-rows-redate-b59-3, #9904 44cb8a604f7692dbbeb2c5b3ba85b162e5d6bdfe on feature/ks-769-mobile-exclusion-redate-b59-4, develop 14d40d4455c7da3c31c71d614fc7c4d1d4ffc2fb.
# A NEW COPY of gate55's launcher, re-keyed for two PRs.
# exit 2:  QA project missing, or this launcher is not in the gateset dir it was filled for (a MOVED KIT).   exit 3-5: pins / prompt / repo missing.
# exit 6:  a head is not at its branch AND refs/pull/<n>/head on origin.   exit 8: thinking directive / kit files / charter / an unfilled token.
# exit 9:  STALE PIN: older than G56A_MAX_PIN_AGE_S (default 1800 s) — re-pin through repin_and_launch_gate56a.sh.
# exit 10: a GitHub compare develop...head is not merge_base develop / ahead 1 / behind 0 / its ONE path.   exit 17: origin develop moved.
# exit 20: the prompt does not name both heads in full.   exit 7: tiers + FROZEN + round.   exit 33: the measurement rules + keyword ladder.
# exit 39: the HOLDS + named exceptions.   exit 34: the five checks + controls.   exit 26: the two GO strings.   exit 25: MERGE ADDENDUM +
# REPORT-HASH-LAST.   exit 23: verdict subject / sender / report dir.   exit 21: the LAUNCH path refuses when stdin is not a TTY.
# exit 16: a launch with a G56A_* test override set.
# G56A_CUR_DEV / G56A_PROMPT / G56A_PINS / G56A_NOW / G56A_COMPARE_FILE / G56A_LSREMOTE_FILE: test overrides (--check only; a launch refuses any G56A_*).
# Opus by the configured default: the exec line carries NO --model.
# Usage: dry001111.SIM.launcher.sh [--check]
set -u
QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
GS='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-05_gate56a'
PROMPT_FILE="${G56A_PROMPT:-$GS/dry001111.SIM.prompt.txt}"
PINS="${G56A_PINS:-$GS/pins_gate56a.SIM-dry001111.json}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
PR3='9903'; HEAD3='fcd8c906a63316b0bc558f9710c6605971daa5bd'; BRANCH3='refs/heads/feature/ks-528-react-router-rows-redate-b59-3'; PATH3='Blockchain/Dev/scripts/audit/audit-baseline.json'
PR4='9904'; HEAD4='44cb8a604f7692dbbeb2c5b3ba85b162e5d6bdfe'; BRANCH4='refs/heads/feature/ks-769-mobile-exclusion-redate-b59-4'; PATH4='Blockchain/Dev/scripts/audit/lock-discovery.mjs'
DEVELOP_SHA='14d40d4455c7da3c31c71d614fc7c4d1d4ffc2fb'
PINNED_EPOCH='1791159071'
[ -d "$QA_DIR" ]      || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
_here="$(dirname "$(/bin/realpath "$0")")"
[ "$_here" = "$GS" ] || { echo "REFUSING: this launcher lives in $_here but was filled for $GS — a MOVED KIT: run repin_and_launch_gate56a.sh from its new home" >&2; exit 2; }
[ -s "$PINS" ]        || { echo "pins missing or empty: $PINS" >&2; exit 3; }
[ -s "$PROMPT_FILE" ] || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]        || { echo "repo under test missing: $REPO" >&2; exit 5; }
_age=$(( ${G56A_NOW:-$(date +%s)} - PINNED_EPOCH ))
[ "$_age" -le "${G56A_MAX_PIN_AGE_S:-1800}" ] || { echo "REFUSING: STALE PIN — pinned ${_age}s ago (max ${G56A_MAX_PIN_AGE_S:-1800}s); run repin_and_launch_gate56a.sh" >&2; exit 9; }
[ "$(python3 -c 'import json,sys; p=json.load(open(sys.argv[1])); print(p["pr3"], p["head3"], p["pr4"], p["head4"], p["develop"])' "$PINS")" = "$PR3 $HEAD3 $PR4 $HEAD4 $DEVELOP_SHA" ] || { echo "REFUSING: the pins file and this launcher disagree (a re-fill was interrupted)" >&2; exit 3; }
[ "$(head -n 1 "$PROMPT_FILE")" = "ultrathink" ] || { echo "REFUSING: the prompt does not open with the thinking directive" >&2; exit 8; }
for _f in README.md COMMISSION.md kit.json lib_gate56a.py c1_pin_gate56a.py c2_diffshape_gate56a.py c3_clock_gate56a.py c3_freeze_clock_gate56a.mjs c3_probe_gate56a.mjs c4_security_gate56a.py c5_notcovered_gate56a.py gh_census_gate56a.py; do
  [ -s "$GS/$_f" ] && grep -qF "$GS/$_f" "$PROMPT_FILE" || { echo "REFUSING: the kit file $GS/$_f is missing, empty, or not named in the prompt" >&2; exit 8; }
done
grep -qF "2026-10-05-ks1404-1376-gD2/report.md" "$PROMPT_FILE" || { echo "REFUSING: the prompt does not name the previous round report (gateD2)" >&2; exit 8; }
grep -qF "/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md" "$PROMPT_FILE" || { echo "REFUSING: the prompt does not name the QA charter" >&2; exit 8; }
grep -qF "2026-10-05_board-taps-suffice-for-audit-redates.md" "$PROMPT_FILE" || { echo "REFUSING: the prompt does not name Kam's board-tap grant" >&2; exit 8; }
grep -qE '\{\{[A-Z0-9_]+\}\}' "$PROMPT_FILE" && { echo "REFUSING: the prompt carries an unfilled double-brace fill token" >&2; exit 8; }
if [ -n "${G56A_LSREMOTE_FILE:-}" ]; then _LS="$(cat "$G56A_LSREMOTE_FILE")"; else
_LS="$(git -C "$REPO" ls-remote origin refs/heads/develop "$BRANCH3" "refs/pull/$PR3/head" "$BRANCH4" "refs/pull/$PR4/head")"   # ONE read of origin
fi
CUR_DEV="${G56A_CUR_DEV:-$(printf '%s\n' "$_LS" | awk '$2=="refs/heads/develop"{print $1}')}"
[ "$CUR_DEV" = "$DEVELOP_SHA" ] || { echo "REFUSING: origin develop $CUR_DEV != the pinned develop $DEVELOP_SHA — run repin_and_launch_gate56a.sh" >&2; exit 17; }
for _p in "$PR3 $HEAD3 $BRANCH3" "$PR4 $HEAD4 $BRANCH4"; do
  set -- $_p
  if [ "$(printf '%s\n' "$_LS" | awk -v h="$2" -v r="$3" '$1==h && $2==r' | wc -l | tr -d ' ')" != 1 ] || [ "$(printf '%s\n' "$_LS" | awk -v h="$2" -v r="refs/pull/$1/head" '$1==h && $2==r' | wc -l | tr -d ' ')" != 1 ]; then
    echo "REFUSING: #$1 — $2 is not at $3 AND refs/pull/$1/head on origin — the head moved (or the pin is wrong); a verdict is valid ONLY at its head" >&2
    printf '%s\n' "$_LS" >&2; exit 6
  fi
done
set --
compare() {   # $1 head -> "<merge_base> ahead=<n> behind=<n> files=<n> paths=<csv>"
  if [ -n "${G56A_COMPARE_FILE:-}" ]; then grep -F "$1" "$G56A_COMPARE_FILE" | cut -d' ' -f2-; return; fi
  (set -a; . "$SECUURA_ENV"; set +a   # the token lives only in this subshell, never in the exec'd agent's env
  H="$1" DEV="$CUR_DEV" python3 - <<'PY'
import json, os, urllib.request
t = os.environ.get("GH_TOKEN", "")
try:
    c = json.load(urllib.request.urlopen(urllib.request.Request("https://api.github.com/repos/Secuura/Distributed_Secuura/compare/%s...%s" % (os.environ["DEV"], os.environ["H"]), headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}), timeout=60))
    fs = sorted(x["filename"] for x in (c.get("files") or []))
    print("%s ahead=%d behind=%d files=%d paths=%s" % (c["merge_base_commit"]["sha"], c["ahead_by"], c["behind_by"], len(fs), ",".join(fs)))
except Exception as e: print("ERROR %s" % e)
PY
  )
}
for _p in "$PR3 $HEAD3 $PATH3" "$PR4 $HEAD4 $PATH4"; do
  set -- $_p
  _c="$(compare "$2")"
  [ "$_c" = "$DEVELOP_SHA ahead=1 behind=0 files=1 paths=$3" ] || { echo "REFUSING: #$1 — the compare is not develop / ahead 1 / behind 0 / its ONE path:" >&2; echo "  got  $_c" >&2; echo "  want $DEVELOP_SHA ahead=1 behind=0 files=1 paths=$3" >&2; exit 10; }
done
set --
grep -qwF "$HEAD3" "$PROMPT_FILE" && grep -qwF "$HEAD4" "$PROMPT_FILE" || { echo "REFUSING: the prompt does not name both heads in full" >&2; exit 20; }
PROMPT_JOINED="$(python3 -c 'import re,sys; print(re.sub(r"\n\s*", " ", open(sys.argv[1], encoding="utf-8").read()))' "$PROMPT_FILE")"
has() { printf '%s' "$PROMPT_JOINED" | grep -qF -- "$1"; }
has "PR #$PR3 is KS-528" && has "PR #$PR4 is KS-769" && has "#$PR3 T2 and #$PR4 T2" && has 'THE GATE IS FROZEN at TWO PRs' && has 'ROUND 1' && has 'Each PR gets its OWN verdict' && has 'round-1 NO GO goes back to the author for round 2' || { echo "REFUSING: the tickets / tiers / FROZEN / round" >&2; exit 7; }
has 'MEASURE, not conclude' && has 'RULE WHETHER IT BLOCKS' && has 'NAMES THE TREE' && has 'A check that prints nothing needs a control that prints' && has 'ASSERT THE FILENAME TOO' || { echo "REFUSING: the measurement rules" >&2; exit 33; }
for _w in C1-PIN ONE-PATH NO-TRAILER SUBJECT-EXACT KEYSCAN-OWN-KEY END-TREE C2-DIFF-SHAPE C3-FROZEN-CLOCK C3-LAPSE-COMPARISON C3-FUSE-STILL-EXISTS C4-SECURITY C4-NO-WIDENING C5-NOT-COVERED C5-AUTHORITY METHOD-STATED PR-BODY-CLAIMS COLLISION-CENSUS NOT-TESTED-LIST TIERING DISK-ENOSPC REPORT-HASH-LAST; do   # AS A TOKEN: bounded by a non-[A-Za-z0-9-] character
  printf '%s' "$PROMPT_JOINED" | grep -qE -- "(^|[^A-Za-z0-9-])$_w([^A-Za-z0-9-]|\$)" || { echo "REFUSING: the prompt does not carry the by-name keyword '$_w'" >&2; exit 33; }
done
has 'THE POINT OF THIS GATE' && has 'return expires <= today;' && has 'THE FUSE STILL EXISTS' && has 'ACCEPTED RISK EXTENDED, NOT FIXED' && has 'APPENDED note' && has 'SIBLING-ADVANCE' && has 'SELF-TEST ARM' && has 'NEGATIVE CONTROL' && has 'a FAKE `npm` printing a canned report' && has '2027-01-01 valid through 2026-12-31' && has '2026-10-31 valid through 2026-10-30' || { echo "REFUSING: the five checks / the controls" >&2; exit 34; }
has 'NO MERGE, NO PUSH to any PR branch, NO ticket state change' && has 'NO ticket filed' && has 'NEVER WRITE THE SHARED CHECKOUT. Findings only' && has 'Never `rm`' && has 'No `az` command of any kind' && has 'You NEVER reply to Peter' && has 'No image is built.' && has 'THE NAMED EXCEPTIONS to those holds — these and NO others' && has 'TICKET STATE IS WEDNESDAY' || { echo "REFUSING: the HOLDS" >&2; exit 39; }
has "WEDNESDAY'S signed GO naming the head, one per PR" && has 'GO (Seat B 59th): merge 9903 on gate56a' && has 'GO (Seat B 59th): merge 9904 on gate56a' && has 'The merge seat is Seat B 59th' || { echo "REFUSING: merge authority / the GO strings" >&2; exit 26; }
has '## MERGE ADDENDUM' && has 'ONE LINE PER PR' && has 'MG-1 1 over 1 path' && has 'MG-11 subject <= 92' && has 'NO TRAILER' && has 'EVERY SUBJECT YOU PROPOSE MUST BE TRUE OF THE DIFF' && has 'are the LAST thing you write to report.md' && has 'sha256 report.md = <hex>' || { echo "REFUSING: the MERGE ADDENDUM rules / REPORT-HASH-LAST" >&2; exit 25; }
grep -qF -- '[QA -> Wednesday] GATE56A #9903 + #9904 (Seat B59 author and merger; T2 date-only: KS 528 react-router rows to 2026-10-31, KS 769 mobile-tree exclusion to 2027-01-01)' "$PROMPT_FILE" && has 'FROM coagent@agentmail.to' && has 'reports/2026-10-05-ks528-769-g56a/' && has 'a `MERGE ADDENDUM` line PER PR' || { echo "REFUSING: the verdict subject / sender / report dir" >&2; exit 23; }
_ANY_OVR="$(env | grep -c '^G56A_')"
NOTE="origin develop $CUR_DEV == the pinned develop | #$PR3 ${HEAD3:0:12} and #$PR4 ${HEAD4:0:12} at branch AND pull/head | compares ok (ahead 1, behind 0, 1 path each) | pin age ${_age}s"
if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  $NOTE"
  echo "  pins, prompt, QA project and repo present; kit at its filled home; thinking directive; every kit file + gateD2 report + the charter + the grant named; no unfilled token"
  echo "  the prompt carries 21 by-name keywords (as tokens), the tier lines, the five checks + the controls, the holds + named exceptions, both GO strings, the addendum + REPORT-HASH-LAST rules, the verdict subject + report dir, both heads in full"
  [ "$_ANY_OVR" != 0 ] && echo "  (a G56A_* TEST OVERRIDE is set)"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"
  exit 0
fi
[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — run this launcher in a cockpit pane, never inside a Bash tool" >&2; exit 21; }
[ "$_ANY_OVR" = 0 ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions "$(cat "$PROMPT_FILE")"
