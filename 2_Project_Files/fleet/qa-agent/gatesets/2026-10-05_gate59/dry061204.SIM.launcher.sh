#!/bin/bash
# dry061204.SIM.launcher.sh — cross-project QA agent, ONE gate (gate59, round 59) over ONE Secuura/Blockchain PR, FROZEN at ONE:
# #1382 KS-1005 (T1, ROUND 1): change-password reads the hash it verifies (routes/users.ts, one call site) + a 6-cell test + its §4 block
# in both platform-k docs; a MERGE-IN head (parents built 4346bc7fbdf8 + develop). Merger: Seat E 2nd. PINNED by repin_and_launch_gate59.sh at
# 2026-10-05T06:12:44Z from its own ls-remote + PULLS API reads: head 80bafc849a54a9368810fd0fcd1ee1184fa608bf on feature/ks-1005-change-password-reads-the-hash-it-verifies-e2-1, develop 46c3e20cfbd21acee0c67d544180c33deaa4c8ef. Shape copied from gate58's
# launcher (a NEW COPY, never an edit).
# exit 2:  QA project missing, or this launcher is not in the gateset dir it was filled for (a MOVED KIT).   exit 3-5: pins / prompt / repo missing.
# exit 6:  the head is not at its branch AND refs/pull/<n>/head on origin.   exit 8: thinking directive / kit files named / an unfilled token.
# exit 9:  STALE PIN: the pin is older than G59_MAX_PIN_AGE_S (default 1800 s) — re-pin and re-fill through repin_and_launch_gate59.sh.
# exit 10: the GitHub compare develop...head: merge_base / ahead / behind / files != the pins.   exit 17: origin develop != the pinned develop.
# exit 20: the prompt names the head in full.   exit 7: tier + FROZEN + round + tiering rule.   exit 33: the by-name keyword ladder (as tokens).
# exit 39: the HOLDS + the named exceptions.   exit 34: the checks C1..C6 + C3b + Q-M by name.   exit 26: GO string.
# exit 25: MERGE ADDENDUM + REPORT-HASH-LAST.   exit 23: verdict subject / sender / report dir.   exit 21: the LAUNCH path refuses when stdin
# is not a TTY (`--check` is headless).   exit 16: a launch with a G59_* test override set.
# G59_CUR_DEV / G59_HEAD / G59_PROMPT / G59_PINS / G59_NOW: test overrides (--check only). Opus by the configured default: the exec line carries NO --model.
# Usage: dry061204.SIM.launcher.sh [--check]
set -u
QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
GS='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-05_gate59'
PROMPT_FILE="${G59_PROMPT:-$GS/dry061204.SIM.prompt.txt}"
PINS="${G59_PINS:-$GS/pins_gate59.SIM-dry061204.json}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
PR='1382'
HEAD_SHA='80bafc849a54a9368810fd0fcd1ee1184fa608bf'
BRANCH='refs/heads/feature/ks-1005-change-password-reads-the-hash-it-verifies-e2-1'
DEVELOP_SHA='46c3e20cfbd21acee0c67d544180c33deaa4c8ef'
PINNED_EPOCH='1791180764'
FILES='Blockchain/Dev/services/auth/src/__tests__/ks1005-change-password-reads-the-hash-it-verifies.test.ts,Blockchain/Dev/services/auth/src/routes/users.ts,Projects Documents/API_Security_Functional_Testing_Architecture_Flow_Diagrams.html,Projects Documents/QA_Tool_Cheat_Sheet_Secuura_API_Testing.html'
[ -d "$QA_DIR" ]      || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
_here="$(dirname "$(/bin/realpath "$0")")"
[ "$_here" = "$GS" ] || { echo "REFUSING: this launcher lives in $_here but was filled for $GS — a MOVED KIT: run repin_and_launch_gate59.sh from its new home" >&2; exit 2; }
[ -s "$PINS" ]        || { echo "pins missing or empty: $PINS" >&2; exit 3; }
[ -s "$PROMPT_FILE" ] || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]        || { echo "repo under test missing: $REPO" >&2; exit 5; }
_age=$(( ${G59_NOW:-$(date +%s)} - PINNED_EPOCH ))
[ "$_age" -le "${G59_MAX_PIN_AGE_S:-1800}" ] || { echo "REFUSING: STALE PIN — pinned ${_age}s ago (max ${G59_MAX_PIN_AGE_S:-1800}s); run repin_and_launch_gate59.sh, which re-pins and re-fills in the same action" >&2; exit 9; }
[ "$(python3 -c 'import json,sys; p=json.load(open(sys.argv[1])); print(p["pr"], p["head"], p["develop"])' "$PINS")" = "$PR $HEAD_SHA $DEVELOP_SHA" ] || { echo "REFUSING: pins_gate59.json and this launcher disagree (a re-fill was interrupted)" >&2; exit 3; }
[ "$(head -n 1 "$PROMPT_FILE")" = "ultrathink" ] || { echo "REFUSING: the prompt does not open with the thinking directive" >&2; exit 8; }
for _f in README.md COMMISSION.md kit.json lib_gate59.py c1_pin_gate59.py c2_hunk_gate59.py c3_redfirst_gate59.py c3b_probe_gate59.py c3b_probe_ks1005_gate59.test.ts.txt c4_docs_gate59.py c5_prtext_gate59.py c6_notcovered_gate59.py gh_census_gate59.py; do
  [ -s "$GS/$_f" ] && grep -qF "$GS/$_f" "$PROMPT_FILE" || { echo "REFUSING: the kit file $GS/$_f is missing, empty, or not named in the prompt" >&2; exit 8; }
done
grep -qF "2026-10-05-ks1333-1345-1380-1381-g57/report.md" "$PROMPT_FILE" || { echo "REFUSING: the prompt does not name the previous round report (gate57)" >&2; exit 8; }
grep -qF "2026-10-05_seatE2_READY_1382.txt" "$PROMPT_FILE" || { echo "REFUSING: the prompt does not name the seat's READY" >&2; exit 8; }
grep -qE '\{\{[A-Z0-9_]+\}\}' "$PROMPT_FILE" && { echo "REFUSING: the prompt carries an unfilled double-brace fill token" >&2; exit 8; }
grep -qF '<''PR>' "$PROMPT_FILE" && { echo "REFUSING: the prompt carries the unpinned PR placeholder" >&2; exit 8; }   # spelled split so this file carries no placeholder
_LS="$(git -C "$REPO" ls-remote origin refs/heads/develop "$BRANCH" "refs/pull/$PR/head")"   # ONE read of origin
CUR_DEV="${G59_CUR_DEV:-$(printf '%s\n' "$_LS" | awk '$2=="refs/heads/develop"{print $1}')}"
[ "$CUR_DEV" = "$DEVELOP_SHA" ] || { echo "REFUSING: origin develop $CUR_DEV != the pinned develop $DEVELOP_SHA — run repin_and_launch_gate59.sh (a moved develop is a RE-DRAFT for this kit)" >&2; exit 17; }
_h="${G59_HEAD:-$HEAD_SHA}"
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
[ "$COMPARE" = "$DEVELOP_SHA ahead=2 behind=0 files=4 paths=$FILES" ] || { echo "REFUSING: #$PR — the compare is not the pinned merge_base / ahead 2 (the merge-in + the built commit) / behind 0 / the 4 paths:" >&2; echo "  got  $COMPARE" >&2; echo "  want $DEVELOP_SHA ahead=2 behind=0 files=4 paths=$FILES" >&2; exit 10; }
grep -qwF "$_h" "$PROMPT_FILE" || { echo "REFUSING: the prompt does not name the head $_h in full" >&2; exit 20; }
PROMPT_JOINED="$(python3 -c 'import re,sys; print(re.sub(r"\n\s*", " ", open(sys.argv[1], encoding="utf-8").read()))' "$PROMPT_FILE")"
has() { printf '%s' "$PROMPT_JOINED" | grep -qF -- "$1"; }
has "PR #$PR is KS-1005" && has "#$PR T1" && has 'THE GATE IS FROZEN at ONE PR' && has 'ROUND 1' && has 'round-1 NO GO goes back to the author for round 2' || { echo "REFUSING: the ticket / tier / FROZEN / round / tiering rule" >&2; exit 7; }
has 'MEASURE, not conclude' && has 'RULE WHETHER IT BLOCKS' && has 'NAMES THE TREE' && has 'A check that prints nothing needs a control that prints' && has 'ASSERT THE FILENAME TOO' || { echo "REFUSING: the measurement rules" >&2; exit 33; }
for _w in C1-PIN C2-HUNK C2-SAME-HASH C3-RED-FIRST C3-SUITE C3-TSC C3B-PROBE C4-DOCS C4-MERGE-IN Q-M Q-1005 C5-PR-TEXT C6-NOT-COVERED END-TREE NO-TRAILER SUBJECT-EXACT KEYSCAN-OWN-KEY METHOD-STATED PR-BODY-CLAIMS READY-CLAIMS PREFLIGHT-INCOMPLETE KNOWN-CLASS-KS949 COLLISION-CENSUS NOT-TESTED-LIST TIERING DISK-ENOSPC REPORT-HASH-LAST; do   # AS A TOKEN: bounded by a non-[A-Za-z0-9-] character
  printf '%s' "$PROMPT_JOINED" | grep -qE -- "(^|[^A-Za-z0-9-])$_w([^A-Za-z0-9-]|\$)" || { echo "REFUSING: the prompt does not carry the by-name keyword '$_w'" >&2; exit 33; }
done
has 'RED-FIRST BY ASSERTION at DEVELOP' && has 'POSITIVE CONTROL a planted TS2322' && has "the GATE's OWN cells" && has 'pass-the-hash' && has 'TIMING / ENUMERATION NOTE' && has 'an INDEPENDENT number-order resolution' && has 'remerge-diff' && has 'SECTION-BOUNDED' && has 'SELF-TEST ARM' && has 'BASELINE' && has 'SESSION REVOCATION' && has 'PREFLIGHT-INCOMPLETE 12/15' || { echo "REFUSING: the checks C1..C6 / C3b / Q-M by name" >&2; exit 34; }
has 'NO MERGE, NO PUSH to any PR branch, NO ticket state change' && has 'NO ticket filed' && has 'NEVER WRITE THE SHARED CHECKOUT. Findings only' && has 'Never `rm`' && has 'No `az` command of any kind' && has 'You NEVER reply to Peter' && has 'No image is built.' && has 'THE NAMED EXCEPTIONS to those holds — these and NO others' && has 'TICKET STATE IS WEDNESDAY' && has '(X8) ONE read-only Linear GraphQL' || { echo "REFUSING: the HOLDS" >&2; exit 39; }
has "WEDNESDAY'S signed GO naming the head" && has 'GO (Seat E 2nd): merge 1382 on gate59' && has 'The merge seat is Seat E 2nd' || { echo "REFUSING: merge authority / the GO string" >&2; exit 26; }
has '## MERGE ADDENDUM' && has 'MG-1 4 over 4 paths' && has 'MG-11 subject <= 92' && has 'NO TRAILER' && has 'EVERY SUBJECT YOU PROPOSE MUST BE TRUE OF THE DIFF' && has 'is the LAST thing you write to report.md' && has 'sha256 report.md = <hex>' || { echo "REFUSING: the MERGE ADDENDUM rules / REPORT-HASH-LAST" >&2; exit 25; }
grep -qF -- '[QA -> Wednesday] GATE59 #1382 (Seat E 2nd author and merger; T1 KS-1005: change-password reads the hash it verifies; merge-in head, Q-M M1-M4)' "$PROMPT_FILE" && has 'FROM coagent@agentmail.to' && has 'reports/2026-10-05-ks1005-1382-g59/' || { echo "REFUSING: the verdict subject / sender / report dir" >&2; exit 23; }
_ANY_OVR="$(env | grep -c '^G59_')"
NOTE="origin develop $CUR_DEV == the pinned develop | #$PR T1 ${_h:0:12} at branch AND pull/head | compare ok (ahead 2, behind 0, 4 paths) | pin age ${_age}s"
if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  $NOTE"
  echo "  pins, prompt, QA project and repo present; kit at its filled home; thinking directive; every kit file + the gate57 report + the READY named; no unfilled token, no PR placeholder"
  echo "  the prompt carries 27 by-name keywords (as tokens), the tier lines, the checks C1..C6 + C3b + Q-M, the holds + named exceptions, the GO string, the addendum + REPORT-HASH-LAST rules, the verdict subject + report dir, the head in full"
  [ "$_ANY_OVR" != 0 ] && echo "  (a G59_* TEST OVERRIDE is set)"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"
  exit 0
fi
[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — run this launcher in a cockpit pane, never inside a Bash tool" >&2; exit 21; }
[ "$_ANY_OVR" = 0 ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions "$(cat "$PROMPT_FILE")"
