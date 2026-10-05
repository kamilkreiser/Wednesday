#!/bin/bash
# dry075405.SIM.launcher.sh — cross-project QA agent, ONE gate (gate60, round 60) over ONE Secuura/Blockchain PR, FROZEN at ONE:
# #1384 KS-1210 (T1, ROUND 1): OAuth app scopes closed to the nine, {admin:read, admin:write} platform-only, owner-or-admin 404 on the four
# by-id routes (routes/oauth.ts) + a 24-cell test + two sibling test fixes + its §4 block 18. in both platform-k docs; a SINGLE-PARENT head on
# develop. Merger: Seat E 3rd. PINNED by repin_and_launch_gate60.sh at 2026-10-05T07:55:57Z from its own ls-remote + PULLS API reads: head 852fc927632095fb603583cb543050d5edd66111
# on feature/ks-1210-oauth-app-scopes-and-ownership-e3-1, develop 46c3e20cfbd21acee0c67d544180c33deaa4c8ef. Shape copied from gate59's launcher (a NEW COPY, never an edit).
# exit 2:  QA project missing, or this launcher is not in the gateset dir it was filled for (a MOVED KIT).   exit 3-5: pins / prompt / repo missing.
# exit 6:  the head is not at its branch AND refs/pull/<n>/head on origin.   exit 8: thinking directive / kit files named / an unfilled token.
# exit 9:  STALE PIN: the pin is older than G60_MAX_PIN_AGE_S (default 1800 s) — re-pin and re-fill through repin_and_launch_gate60.sh.
# exit 10: the GitHub compare develop...head: merge_base / ahead / behind / files != the pins.   exit 17: origin develop != the pinned develop.
# exit 20: the prompt names the head in full.   exit 7: tier + FROZEN + round + tiering rule.   exit 33: the by-name keyword ladder (as tokens).
# exit 39: the HOLDS + the named exceptions.   exit 34: the checks C1..C6 + C3b + Q-M by name.   exit 26: GO string.
# exit 25: MERGE ADDENDUM + REPORT-HASH-LAST.   exit 23: verdict subject / sender / report dir.   exit 21: the LAUNCH path refuses when stdin
# is not a TTY (`--check` is headless).   exit 16: a launch with a G60_* test override set.
# G60_CUR_DEV / G60_HEAD / G60_PROMPT / G60_PINS / G60_NOW: test overrides (--check only). Opus by the configured default: the exec line carries NO --model.
# Usage: dry075405.SIM.launcher.sh [--check]
set -u
QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
GS='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-05_gate60'
PROMPT_FILE="${G60_PROMPT:-$GS/dry075405.SIM.prompt.txt}"
PINS="${G60_PINS:-$GS/pins_gate60.SIM-dry075405.json}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
PR='1384'
HEAD_SHA='852fc927632095fb603583cb543050d5edd66111'
BRANCH='refs/heads/feature/ks-1210-oauth-app-scopes-and-ownership-e3-1'
DEVELOP_SHA='46c3e20cfbd21acee0c67d544180c33deaa4c8ef'
PINNED_EPOCH='1791186957'
FILES='Blockchain/Dev/services/auth/src/__tests__/ks1210-oauth-app-scopes-and-ownership.test.ts,Blockchain/Dev/services/auth/src/__tests__/ks431-oauth-app-update.test.ts,Blockchain/Dev/services/auth/src/__tests__/ks451-oauth-app-nul-scope.test.ts,Blockchain/Dev/services/auth/src/routes/oauth.ts,Projects Documents/API_Security_Functional_Testing_Architecture_Flow_Diagrams.html,Projects Documents/QA_Tool_Cheat_Sheet_Secuura_API_Testing.html'
[ -d "$QA_DIR" ]      || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
_here="$(dirname "$(/bin/realpath "$0")")"
[ "$_here" = "$GS" ] || { echo "REFUSING: this launcher lives in $_here but was filled for $GS — a MOVED KIT: run repin_and_launch_gate60.sh from its new home" >&2; exit 2; }
[ -s "$PINS" ]        || { echo "pins missing or empty: $PINS" >&2; exit 3; }
[ -s "$PROMPT_FILE" ] || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]        || { echo "repo under test missing: $REPO" >&2; exit 5; }
_age=$(( ${G60_NOW:-$(date +%s)} - PINNED_EPOCH ))
[ "$_age" -le "${G60_MAX_PIN_AGE_S:-1800}" ] || { echo "REFUSING: STALE PIN — pinned ${_age}s ago (max ${G60_MAX_PIN_AGE_S:-1800}s); run repin_and_launch_gate60.sh, which re-pins and re-fills in the same action" >&2; exit 9; }
[ "$(python3 -c 'import json,sys; p=json.load(open(sys.argv[1])); print(p["pr"], p["head"], p["develop"])' "$PINS")" = "$PR $HEAD_SHA $DEVELOP_SHA" ] || { echo "REFUSING: pins_gate60.json and this launcher disagree (a re-fill was interrupted)" >&2; exit 3; }
[ "$(head -n 1 "$PROMPT_FILE")" = "ultrathink" ] || { echo "REFUSING: the prompt does not open with the thinking directive" >&2; exit 8; }
for _f in README.md COMMISSION.md kit.json lib_gate60.py c1_pin_gate60.py c2_hunk_gate60.py c3_redfirst_gate60.py c3b_probe_gate60.py c3b_probe_ks1210_gate60.test.ts.txt c4_docs_gate60.py c5_prtext_gate60.py c6_notcovered_gate60.py gh_census_gate60.py; do
  [ -s "$GS/$_f" ] && grep -qF "$GS/$_f" "$PROMPT_FILE" || { echo "REFUSING: the kit file $GS/$_f is missing, empty, or not named in the prompt" >&2; exit 8; }
done
grep -qF "2026-10-05-ks1005-1382-g59/report.md" "$PROMPT_FILE" || { echo "REFUSING: the prompt does not name the previous round report (gate59)" >&2; exit 8; }
grep -qF "2026-10-05_seatE3_READY_1384.txt" "$PROMPT_FILE" || { echo "REFUSING: the prompt does not name the seat's READY" >&2; exit 8; }
grep -qE '\{\{[A-Z0-9_]+\}\}' "$PROMPT_FILE" && { echo "REFUSING: the prompt carries an unfilled double-brace fill token" >&2; exit 8; }
grep -qF '<''PR>' "$PROMPT_FILE" && { echo "REFUSING: the prompt carries the unpinned PR placeholder" >&2; exit 8; }   # spelled split so this file carries no placeholder
_LS="$(git -C "$REPO" ls-remote origin refs/heads/develop "$BRANCH" "refs/pull/$PR/head")"   # ONE read of origin
CUR_DEV="${G60_CUR_DEV:-$(printf '%s\n' "$_LS" | awk '$2=="refs/heads/develop"{print $1}')}"
[ "$CUR_DEV" = "$DEVELOP_SHA" ] || { echo "REFUSING: origin develop $CUR_DEV != the pinned develop $DEVELOP_SHA — run repin_and_launch_gate60.sh (a moved develop is a RE-DRAFT for this kit)" >&2; exit 17; }
_h="${G60_HEAD:-$HEAD_SHA}"
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
[ "$COMPARE" = "$DEVELOP_SHA ahead=1 behind=0 files=6 paths=$FILES" ] || { echo "REFUSING: #$PR — the compare is not the pinned merge_base / ahead 1 (the one built commit) / behind 0 / the 6 paths:" >&2; echo "  got  $COMPARE" >&2; echo "  want $DEVELOP_SHA ahead=1 behind=0 files=6 paths=$FILES" >&2; exit 10; }
grep -qwF "$_h" "$PROMPT_FILE" || { echo "REFUSING: the prompt does not name the head $_h in full" >&2; exit 20; }
PROMPT_JOINED="$(python3 -c 'import re,sys; print(re.sub(r"\n\s*", " ", open(sys.argv[1], encoding="utf-8").read()))' "$PROMPT_FILE")"
has() { printf '%s' "$PROMPT_JOINED" | grep -qF -- "$1"; }
has "PR #$PR is KS-1210" && has "#$PR T1" && has 'THE GATE IS FROZEN at ONE PR' && has 'ROUND 1' && has 'round-1 NO GO goes back to the author for round 2' || { echo "REFUSING: the ticket / tier / FROZEN / round / tiering rule" >&2; exit 7; }
has 'MEASURE, not conclude' && has 'RULE WHETHER IT BLOCKS' && has 'NAMES THE TREE' && has 'A check that prints nothing needs a control that prints' && has 'ASSERT THE FILENAME TOO' || { echo "REFUSING: the measurement rules" >&2; exit 33; }
for _w in C1-PIN C2-HUNK C2-CLASS-HUNT C3-RED-FIRST C3-SIBLINGS C3-SUITE C3-TSC C3-OPENAPI C3B-PROBE ROLE-MATRIX SCOPE-ESCALATION LEGACY-APPS TENANT-BOUND C4-DOCS C4-PREDICT Q-M Q-1210 C5-PR-TEXT C6-NOT-COVERED END-TREE NO-TRAILER SUBJECT-EXACT KEYSCAN-OWN-KEY METHOD-STATED PR-BODY-CLAIMS READY-CLAIMS PREFLIGHT-INCOMPLETE KNOWN-CLASS-KS949 COLLISION-CENSUS NOT-TESTED-LIST TIERING DISK-ENOSPC REPORT-HASH-LAST; do   # AS A TOKEN: bounded by a non-[A-Za-z0-9-] character
  printf '%s' "$PROMPT_JOINED" | grep -qE -- "(^|[^A-Za-z0-9-])$_w([^A-Za-z0-9-]|\$)" || { echo "REFUSING: the prompt does not carry the by-name keyword '$_w'" >&2; exit 33; }
done
has 'RED-FIRST BY ASSERTION at DEVELOP' && has 'POSITIVE CONTROL a planted TS2322' && has "the GATE's OWN cells" && has 'the six-role bypass' && has 'existing apps' && has 'an INDEPENDENT number-order resolution' && has 'remerge-diff' && has 'SECTION-BOUNDED' && has 'SELF-TEST ARM' && has 'BASELINE' && has 'CONFLICTED toplevel tree' && has 'PREFLIGHT-INCOMPLETE 12/15' || { echo "REFUSING: the checks C1..C6 / C3b / Q-M by name" >&2; exit 34; }
has 'NO MERGE, NO PUSH to any PR branch, NO ticket state change' && has 'NO ticket filed' && has 'NEVER WRITE THE SHARED CHECKOUT. Findings only' && has 'Never `rm`' && has 'No `az` command of any kind' && has 'You NEVER reply to Peter' && has 'No image is built.' && has 'THE NAMED EXCEPTIONS to those holds — these and NO others' && has 'TICKET STATE IS WEDNESDAY' && has '(X8) ONE read-only Linear GraphQL' || { echo "REFUSING: the HOLDS" >&2; exit 39; }
has "WEDNESDAY'S signed GO naming the head" && has 'GO (Seat E 3rd): merge 1384 on gate60' && has 'The merge seat is Seat E 3rd' || { echo "REFUSING: merge authority / the GO string" >&2; exit 26; }
has '## MERGE ADDENDUM' && has 'MG-1 6 over 6 paths' && has 'MG-11 subject <= 92' && has 'NO TRAILER' && has 'EVERY SUBJECT YOU PROPOSE MUST BE TRUE OF THE DIFF' && has 'is the LAST thing you write to report.md' && has 'sha256 report.md = <hex>' || { echo "REFUSING: the MERGE ADDENDUM rules / REPORT-HASH-LAST" >&2; exit 25; }
grep -qF -- '[QA -> Wednesday] GATE60 #1384 (Seat E 3rd author and merger; T1 KS-1210: OAuth app scopes closed to the nine, admin pair platform-only, owner-or-admin 404; single-parent head, Q-M for the later merge-ins)' "$PROMPT_FILE" && has 'FROM coagent@agentmail.to' && has 'reports/2026-10-05-ks1210-1384-g60/' || { echo "REFUSING: the verdict subject / sender / report dir" >&2; exit 23; }
_ANY_OVR="$(env | grep -c '^G60_')"
NOTE="origin develop $CUR_DEV == the pinned develop | #$PR T1 ${_h:0:12} at branch AND pull/head | compare ok (ahead 1, behind 0, 6 paths) | pin age ${_age}s"
if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  $NOTE"
  echo "  pins, prompt, QA project and repo present; kit at its filled home; thinking directive; every kit file + the gate59 report + the READY named; no unfilled token, no PR placeholder"
  echo "  the prompt carries 33 by-name keywords (as tokens), the tier lines, the checks C1..C6 + C3b + Q-M, the holds + named exceptions, the GO string, the addendum + REPORT-HASH-LAST rules, the verdict subject + report dir, the head in full"
  [ "$_ANY_OVR" != 0 ] && echo "  (a G60_* TEST OVERRIDE is set)"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"
  exit 0
fi
[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — run this launcher in a cockpit pane, never inside a Bash tool" >&2; exit 21; }
[ "$_ANY_OVR" = 0 ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions "$(cat "$PROMPT_FILE")"
