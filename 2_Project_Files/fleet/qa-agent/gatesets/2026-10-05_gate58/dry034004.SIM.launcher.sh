#!/bin/bash
# dry034004.SIM.launcher.sh — cross-project QA agent, ONE gate (gate58, round 58) over ONE Secuura/Blockchain PR, FROZEN at ONE:
# #1379 KS-749 (T1, ROUND 1): Seat F 1st's advisory bump — browserslist 4.28.7 in 6 locks (+ data packages below its floors),
# postcss-selector-parser 6.1.4 in the root lock, 3 baseline rows (2026-10-15 fuse) removed. Merger: Seat F 1st (the author). PINNED by repin_and_launch_gate58.sh at 2026-10-05T03:40:39Z from its own ls-remote + PULLS API reads:
# head dd398f2d14db554c47550925fd80761ca9298dfa on feature/ks-749-browserslist-postcss-selector-parser-in-range-f1-1, develop 3ce8cd4026a6e3241413e9c7533d5a84d10c1c79. Shape copied from gate54f's launcher (a NEW COPY, never an edit), one row.
# exit 2:  QA project missing, or this launcher is not in the gateset dir it was filled for (a MOVED KIT).   exit 3-5: pins / prompt / repo missing.
# exit 6:  the head is not at its branch AND refs/pull/<n>/head on origin.   exit 8: thinking directive / kit files named / an unfilled token.
# exit 9:  STALE PIN: the pin is older than G58_MAX_PIN_AGE_S (default 1800 s) — re-pin and re-fill through repin_and_launch_gate58.sh.
# exit 10: the GitHub compare develop...head: merge_base / ahead / behind / files != the pins.   exit 17: origin develop != the pinned develop.
# exit 20: the prompt names the head in full.   exit 7: tier + FROZEN + round + tiering rule.   exit 33: the by-name keyword ladder (as tokens).
# exit 39: the HOLDS + the named exceptions.   exit 34: the six checks C1..C6 by name + the base control + the bite.   exit 26: GO string.
# exit 25: MERGE ADDENDUM + REPORT-HASH-LAST.   exit 23: verdict subject / sender / report dir.   exit 21: the LAUNCH path refuses when stdin
# is not a TTY (`--check` is headless).   exit 16: a launch with a G58_* test override set.
# G58_CUR_DEV / G58_HEAD / G58_PROMPT / G58_PINS / G58_NOW: test overrides (--check only). Opus by the configured default: the exec line carries NO --model.
# Usage: dry034004.SIM.launcher.sh [--check]
set -u
QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
GS='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-05_gate58'
PROMPT_FILE="${G58_PROMPT:-$GS/dry034004.SIM.prompt.txt}"
PINS="${G58_PINS:-$GS/pins_gate58.SIM-dry034004.json}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
PR='1379'
HEAD_SHA='dd398f2d14db554c47550925fd80761ca9298dfa'
BRANCH='refs/heads/feature/ks-749-browserslist-postcss-selector-parser-in-range-f1-1'
DEVELOP_SHA='3ce8cd4026a6e3241413e9c7533d5a84d10c1c79'
PINNED_EPOCH='1791171639'
FILES='Blockchain/Dev/frontend/admin/package-lock.json,Blockchain/Dev/frontend/outlook-addin/package-lock.json,Blockchain/Dev/frontend/verifier/package-lock.json,Blockchain/Dev/package-lock.json,Blockchain/Dev/scripts/audit/audit-baseline.json,Blockchain/Dev/services/governance/package-lock.json,Blockchain/Dev/services/referral/package-lock.json'
[ -d "$QA_DIR" ]      || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
_here="$(dirname "$(/bin/realpath "$0")")"
[ "$_here" = "$GS" ] || { echo "REFUSING: this launcher lives in $_here but was filled for $GS — a MOVED KIT: run repin_and_launch_gate58.sh from its new home" >&2; exit 2; }
[ -s "$PINS" ]        || { echo "pins missing or empty: $PINS" >&2; exit 3; }
[ -s "$PROMPT_FILE" ] || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]        || { echo "repo under test missing: $REPO" >&2; exit 5; }
_age=$(( ${G58_NOW:-$(date +%s)} - PINNED_EPOCH ))
[ "$_age" -le "${G58_MAX_PIN_AGE_S:-1800}" ] || { echo "REFUSING: STALE PIN — pinned ${_age}s ago (max ${G58_MAX_PIN_AGE_S:-1800}s); run repin_and_launch_gate58.sh, which re-pins and re-fills in the same action" >&2; exit 9; }
[ "$(python3 -c 'import json,sys; p=json.load(open(sys.argv[1])); print(p["pr"], p["head"], p["develop"])' "$PINS")" = "$PR $HEAD_SHA $DEVELOP_SHA" ] || { echo "REFUSING: pins_gate58.json and this launcher disagree (a re-fill was interrupted)" >&2; exit 3; }
[ "$(head -n 1 "$PROMPT_FILE")" = "ultrathink" ] || { echo "REFUSING: the prompt does not open with the thinking directive" >&2; exit 8; }
for _f in README.md COMMISSION.md kit.json lib_gate58.py c1_pin_gate58.py c2_lockdiff_gate58.py c3_integrity_gate58.py c4_baseline_gate58.py c5_legs_gate58.py c5_freeze_clock_gate58.cjs c6_scope_gate58.py; do
  [ -s "$GS/$_f" ] && grep -qF "$GS/$_f" "$PROMPT_FILE" || { echo "REFUSING: the kit file $GS/$_f is missing, empty, or not named in the prompt" >&2; exit 8; }
done
grep -qF "2026-10-04-pr0-1373-g54f/report.md" "$PROMPT_FILE" || { echo "REFUSING: the prompt does not name the previous round report (gate54f)" >&2; exit 8; }
grep -qF "2026-10-05_seatF1_READY_1379.txt" "$PROMPT_FILE" || { echo "REFUSING: the prompt does not name the seat's READY" >&2; exit 8; }
grep -qE 'KS-751' "$PROMPT_FILE" && { echo "REFUSING: the prompt writes the ARCHIVED key hyphenated (it must say KS 751)" >&2; exit 8; }
grep -qE '\{\{[A-Z0-9_]+\}\}' "$PROMPT_FILE" && { echo "REFUSING: the prompt carries an unfilled double-brace fill token" >&2; exit 8; }
grep -qF '<''PR>' "$PROMPT_FILE" && { echo "REFUSING: the prompt carries the unpinned PR placeholder" >&2; exit 8; }   # spelled split so this file carries no placeholder
_LS="$(git -C "$REPO" ls-remote origin refs/heads/develop "$BRANCH" "refs/pull/$PR/head")"   # ONE read of origin
CUR_DEV="${G58_CUR_DEV:-$(printf '%s\n' "$_LS" | awk '$2=="refs/heads/develop"{print $1}')}"
[ "$CUR_DEV" = "$DEVELOP_SHA" ] || { echo "REFUSING: origin develop $CUR_DEV != the pinned develop $DEVELOP_SHA — run repin_and_launch_gate58.sh" >&2; exit 17; }
_h="${G58_HEAD:-$HEAD_SHA}"
if [ "$(printf '%s\n' "$_LS" | awk -v h="$_h" -v r="$BRANCH" '$1==h && $2==r' | wc -l | tr -d ' ')" != 1 ] || [ "$(printf '%s\n' "$_LS" | awk -v h="$_h" -v r="refs/pull/$PR/head" '$1==h && $2==r' | wc -l | tr -d ' ')" != 1 ]; then
  echo "REFUSING: #$PR — $_h is not at $BRANCH AND refs/pull/$PR/head on origin — the head moved (or the pin is wrong); a verdict is valid ONLY at its head" >&2
  printf '%s\n' "$_LS" >&2; exit 6
fi
COMPARE="$(set -a; . "$SECUURA_ENV"; set +a   # the token lives only in this subshell, never in the exec'd agent's env
H="$_h" DEV="$CUR_DEV" python3 - <<'PY'
import json, os, urllib.request
t = os.environ.get("GH_TOKEN", "")
try:
    c = json.load(urllib.request.urlopen(urllib.request.Request("https://api.github.com/repos/Secuura/Distributed_Secuura/compare/%s...%s" % (os.environ["DEV"], os.environ["H"]), headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}), timeout=60))
    fs = sorted(x["filename"] for x in (c.get("files") or []))
    print("%s ahead=%d behind=%d files=%d paths=%s" % (c["merge_base_commit"]["sha"], c["ahead_by"], c["behind_by"], len(fs), ",".join(fs)))
except Exception as e: print("ERROR %s" % e)
PY
)"
[ "$COMPARE" = "$DEVELOP_SHA ahead=1 behind=0 files=7 paths=$FILES" ] || { echo "REFUSING: #$PR — the compare is not the pinned merge_base / ahead 1 / behind 0 / the 7 paths:" >&2; echo "  got  $COMPARE" >&2; echo "  want $DEVELOP_SHA ahead=1 behind=0 files=7 paths=$FILES" >&2; exit 10; }
grep -qwF "$_h" "$PROMPT_FILE" || { echo "REFUSING: the prompt does not name the head $_h in full" >&2; exit 20; }
PROMPT_JOINED="$(python3 -c 'import re,sys; print(re.sub(r"\n\s*", " ", open(sys.argv[1], encoding="utf-8").read()))' "$PROMPT_FILE")"
has() { printf '%s' "$PROMPT_JOINED" | grep -qF -- "$1"; }
has "PR #$PR is KS-749" && has "#$PR T1" && has 'THE GATE IS FROZEN at ONE PR' && has 'ROUND 1' && has 'round-1 NO GO goes back to the author for round 2' || { echo "REFUSING: the ticket / tier / FROZEN / round / tiering rule" >&2; exit 7; }
has 'MEASURE, not conclude' && has 'RULE WHETHER IT BLOCKS' && has 'NAMES THE TREE' && has 'A check that prints nothing needs a control that prints' && has 'ASSERT THE FILENAME TOO' || { echo "REFUSING: the measurement rules" >&2; exit 33; }
for _w in C1-PIN C2-LOCKDIFF C3-INTEGRITY C4-BASELINE C5-LEGS C5-FROZEN-CLOCK C5-BASE-CONTROL C5-BITE C5-INSTALL-ROOT C6-NOT-COVERED END-TREE MODES NO-TRAILER KEYSCAN-OWN-KEY NO-ARCHIVED-KEY METHOD-STATED PR-BODY-CLAIMS READY-CLAIMS PREFLIGHT-INCOMPLETE COLLISION-CENSUS NOT-TESTED-LIST TIERING DISK-ENOSPC REPORT-HASH-LAST; do   # AS A TOKEN: bounded by a non-[A-Za-z0-9-] character
  printf '%s' "$PROMPT_JOINED" | grep -qE -- "(^|[^A-Za-z0-9-])$_w([^A-Za-z0-9-]|\$)" || { echo "REFUSING: the prompt does not carry the by-name keyword '$_w'" >&2; exit 33; }
done
has 'BASE CONTROL in YOUR base worktree' && has 'rc 2 is a SKIP' && has 'NEVER a pass' && has 'FROZEN at 2026-10-15T00:01Z' && has 'PROVED BOTH WAYS' && has 'reverting ONE lock to its base blob' && has 'NO-OP CONTROL' && has 'from the COMMITTED root lock' && has 'NEVER in the builder' && has 'SELF-TEST ARM' && has 'NEGATIVE CONTROL' && has 'NOT APPLICABLE / NOT COVERED' && has 'OUT OF GATE SCOPE (KS-769' && has 'PREFLIGHT INCOMPLETE' && has 'CSS build diff' && has 'mobile/secuura-app' && has 'KS 751 is ARCHIVED' || { echo "REFUSING: the six checks / base control / bite / not-covered rules" >&2; exit 34; }
has 'NO MERGE, NO PUSH to any PR branch, NO ticket state change' && has 'NO ticket filed' && has 'NEVER WRITE THE SHARED CHECKOUT. Findings only' && has 'Never `rm`' && has 'No `az` command of any kind' && has 'You NEVER reply to Peter' && has 'No image is built.' && has 'THE NAMED EXCEPTIONS to those holds — these and NO others' && has 'TICKET STATE IS WEDNESDAY' || { echo "REFUSING: the HOLDS" >&2; exit 39; }
has "WEDNESDAY'S signed GO naming the head" && has 'GO (Seat F 1st): merge 1379 on gate58' && has 'The merge seat is Seat F 1st' || { echo "REFUSING: merge authority / the GO string" >&2; exit 26; }
has '## MERGE ADDENDUM' && has 'MG-1 7 over 7 paths' && has 'MG-11 subject <= 92' && has 'NO TRAILER' && has 'EVERY SUBJECT YOU PROPOSE MUST BE TRUE OF THE DIFF' && has 'is the LAST thing you write to report.md' && has 'sha256 report.md = <hex>' || { echo "REFUSING: the MERGE ADDENDUM rules / REPORT-HASH-LAST" >&2; exit 25; }
grep -qF -- '[QA -> Wednesday] GATE58 #1379 (Seat F 1st author and merger; T1 advisory bump KS-749: browserslist 4.28.7 in six locks, postcss-selector-parser 6.1.4 in the root, three 2026-10-15 baseline rows out)' "$PROMPT_FILE" && has 'FROM coagent@agentmail.to' && has 'reports/2026-10-05-ks749-1379-g58/' || { echo "REFUSING: the verdict subject / sender / report dir" >&2; exit 23; }
_ANY_OVR="$(env | grep -c '^G58_')"
NOTE="origin develop $CUR_DEV == the pinned develop | #$PR T1 ${_h:0:12} at branch AND pull/head | compare ok (ahead 1, behind 0, 7 paths) | pin age ${_age}s"
if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  $NOTE"
  echo "  pins, prompt, QA project and repo present; kit at its filled home; thinking directive; every kit file + the gate54f report + the READY named, no hyphenated archived key; no unfilled token, no PR placeholder"
  echo "  the prompt carries 24 by-name keywords (as tokens), the tier lines, the six checks + base control + bite, the holds + named exceptions, the GO string, the addendum + REPORT-HASH-LAST rules, the verdict subject + report dir, the head in full"
  [ "$_ANY_OVR" != 0 ] && echo "  (a G58_* TEST OVERRIDE is set)"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"
  exit 0
fi
[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — run this launcher in a cockpit pane, never inside a Bash tool" >&2; exit 21; }
[ "$_ANY_OVR" = 0 ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions "$(cat "$PROMPT_FILE")"
