#!/bin/bash
# pr9999.SIM.launcher.sh — cross-project QA agent, ONE gate (gateD2, round 54) over ONE Secuura/Blockchain PR, FROZEN at ONE:
# #9999 KS-1404 (T1, ROUND 1): real RFC 3161 verification, node-forge out of timestamping; TWO commits (the second adds the .crt bundle).
# Merger: Seat D 3rd (the author). PINNED by repin_and_launch_gateD2.sh at 2026-10-04T15:02:28Z from its own ls-remote + PULLS API reads:
# head 9884b5588d7ca1061ea424a1782f385da1c36a49 on feature/ks-1404-rfc3161-real-verification-d3-1, develop e6daa806e79a14a580f064db95e797c1fd671dc7. A NEW COPY of gate54f's launcher (itself gate52's guards, one row), re-keyed.
# exit 2:  QA project missing, or this launcher is not in the gateset dir it was filled for (a MOVED KIT).   exit 3-5: pins / prompt / repo missing.
# exit 6:  the head is not at its branch AND refs/pull/<n>/head on origin.   exit 8: thinking directive / kit files / charter named / an unfilled token.
# exit 9:  STALE PIN: the pin is older than GD2_MAX_PIN_AGE_S (default 1800 s) — re-pin and re-fill through repin_and_launch_gateD2.sh.
# exit 10: the GitHub compare develop...head: merge_base / ahead 2 / behind 0 / files != the pins.   exit 17: origin develop != the pinned develop.
# exit 20: the prompt names the head in full.   exit 7: tier + FROZEN + round + tiering rule.   exit 33: the by-name keyword ladder (as tokens).
# exit 39: the HOLDS + the named exceptions.   exit 34: the six checks C1..C6 + the ruling's constraints + the controls.   exit 26: GO string.
# exit 25: MERGE ADDENDUM + REPORT-HASH-LAST.   exit 23: verdict subject / sender / report dir.   exit 21: the LAUNCH path refuses when stdin
# is not a TTY (`--check` is headless).   exit 16: a launch with a GD2_* test override set.
# GD2_CUR_DEV / GD2_HEAD / GD2_PROMPT / GD2_PINS / GD2_NOW: test overrides (--check only). Opus by the configured default: the exec line carries NO --model.
# Usage: pr9999.SIM.launcher.sh [--check]
set -u
QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
GS='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-05_gateD2'
PROMPT_FILE="${GD2_PROMPT:-$GS/pr9999.SIM.prompt.txt}"
PINS="${GD2_PINS:-$GS/pins_gateD2.SIM-pr9999.json}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
PR='9999'
HEAD_SHA='9884b5588d7ca1061ea424a1782f385da1c36a49'
BRANCH='refs/heads/feature/ks-1404-rfc3161-real-verification-d3-1'
DEVELOP_SHA='e6daa806e79a14a580f064db95e797c1fd671dc7'
PINNED_EPOCH='1791126148'
FILES='Blockchain/Dev/package-lock.json,Blockchain/Dev/scripts/audit/audit-baseline.json,Blockchain/Dev/services/timestamping/config/README.md,Blockchain/Dev/services/timestamping/config/tsa-trust-anchors.crt,Blockchain/Dev/services/timestamping/package-lock.json,Blockchain/Dev/services/timestamping/package.json,Blockchain/Dev/services/timestamping/src/__tests__/ks1404-pki.ts,Blockchain/Dev/services/timestamping/src/__tests__/ks1404-verify-rfc3161.test.ts,Blockchain/Dev/services/timestamping/src/tsa/der.ts,Blockchain/Dev/services/timestamping/src/tsa/qualified-tsa.ts,Blockchain/Dev/services/timestamping/src/tsa/rfc3161-client.ts,Blockchain/Dev/services/timestamping/src/tsa/rfc3161-verify.ts,Projects Documents/API_Security_Functional_Testing_Architecture_Flow_Diagrams.html,Projects Documents/QA_Tool_Cheat_Sheet_Secuura_API_Testing.html'
NFILES='14'
[ -d "$QA_DIR" ]      || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
_here="$(dirname "$(/bin/realpath "$0")")"
[ "$_here" = "$GS" ] || { echo "REFUSING: this launcher lives in $_here but was filled for $GS — a MOVED KIT: run repin_and_launch_gateD2.sh from its new home" >&2; exit 2; }
[ -s "$PINS" ]        || { echo "pins missing or empty: $PINS" >&2; exit 3; }
[ -s "$PROMPT_FILE" ] || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]        || { echo "repo under test missing: $REPO" >&2; exit 5; }
_age=$(( ${GD2_NOW:-$(date +%s)} - PINNED_EPOCH ))
[ "$_age" -le "${GD2_MAX_PIN_AGE_S:-1800}" ] || { echo "REFUSING: STALE PIN — pinned ${_age}s ago (max ${GD2_MAX_PIN_AGE_S:-1800}s); run repin_and_launch_gateD2.sh, which re-pins and re-fills in the same action" >&2; exit 9; }
[ "$(python3 -c 'import json,sys; p=json.load(open(sys.argv[1])); print(p["pr"], p["head"], p["develop"])' "$PINS")" = "$PR $HEAD_SHA $DEVELOP_SHA" ] || { echo "REFUSING: the pins file and this launcher disagree (a re-fill was interrupted)" >&2; exit 3; }
[ "$(head -n 1 "$PROMPT_FILE")" = "ultrathink" ] || { echo "REFUSING: the prompt does not open with the thinking directive" >&2; exit 8; }
for _f in README.md COMMISSION.md kit.json lib_gateD2.py c1_pin_gateD2.py c2_lockdiff_gateD2.py c2_integrity_gateD2.py c2_baseline_gateD2.py c2_legs_gateD2.sh c3_cells_gateD2.sh c3_parse_gateD2.py c3_mutate_gateD2.py c3_reqbytes_gateD2.py probe_pki_gateD2.sh probe_ks1404_forgery.test.ts.txt probe_ks1404_mock.test.ts.txt probe_ks1404_reqbytes.test.ts.txt c4_security_gateD2.py c5_docs_gateD2.py c6_notcovered_gateD2.py; do
  [ -s "$GS/$_f" ] && grep -qF "$GS/$_f" "$PROMPT_FILE" || { echo "REFUSING: the kit file $GS/$_f is missing, empty, or not named in the prompt" >&2; exit 8; }
done
grep -qF "2026-10-04-pr0-1373-g54f/report.md" "$PROMPT_FILE" || { echo "REFUSING: the prompt does not name the previous round report (gate54f)" >&2; exit 8; }
grep -qF "/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md" "$PROMPT_FILE" || { echo "REFUSING: the prompt does not name the QA charter" >&2; exit 8; }
grep -qE '\{\{[A-Z0-9_]+\}\}' "$PROMPT_FILE" && { echo "REFUSING: the prompt carries an unfilled double-brace fill token" >&2; exit 8; }
grep -qF '<''PR>' "$PROMPT_FILE" && { echo "REFUSING: the prompt carries the unpinned PR placeholder" >&2; exit 8; }   # spelled split so this file carries no placeholder
_LS="$(git -C "$REPO" ls-remote origin refs/heads/develop "$BRANCH" "refs/pull/$PR/head")"   # ONE read of origin
CUR_DEV="${GD2_CUR_DEV:-$(printf '%s\n' "$_LS" | awk '$2=="refs/heads/develop"{print $1}')}"
[ "$CUR_DEV" = "$DEVELOP_SHA" ] || { echo "REFUSING: origin develop $CUR_DEV != the pinned develop $DEVELOP_SHA — run repin_and_launch_gateD2.sh" >&2; exit 17; }
_h="${GD2_HEAD:-$HEAD_SHA}"
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
[ "$COMPARE" = "$DEVELOP_SHA ahead=2 behind=0 files=$NFILES paths=$FILES" ] || { echo "REFUSING: #$PR — the compare is not the pinned merge_base / ahead 2 / behind 0 / the $NFILES paths:" >&2; echo "  got  $COMPARE" >&2; echo "  want $DEVELOP_SHA ahead=2 behind=0 files=$NFILES paths=$FILES" >&2; exit 10; }
grep -qwF "$_h" "$PROMPT_FILE" || { echo "REFUSING: the prompt does not name the head $_h in full" >&2; exit 20; }
PROMPT_JOINED="$(python3 -c 'import re,sys; print(re.sub(r"\n\s*", " ", open(sys.argv[1], encoding="utf-8").read()))' "$PROMPT_FILE")"
has() { printf '%s' "$PROMPT_JOINED" | grep -qF -- "$1"; }
has "PR #$PR is KS-1404" && has "#$PR T1" && has 'THE GATE IS FROZEN at ONE PR' && has 'ROUND 1' && has 'round-1 NO GO goes back to the author for round 2' || { echo "REFUSING: the ticket / tier / FROZEN / round / tiering rule" >&2; exit 7; }
has 'MEASURE, not conclude' && has 'RULE WHETHER IT BLOCKS' && has 'NAMES THE TREE' && has 'A check that prints nothing needs a control that prints' && has 'ASSERT THE FILENAME TOO' || { echo "REFUSING: the measurement rules" >&2; exit 33; }
for _w in C1-PIN END-TREE MODES NO-TRAILER KEYSCAN-OWN-KEY PR0-ABSENT PATH-GATE NO-CREDENTIAL C2-LOCKDIFF C2-INTEGRITY C2-BASELINE C2-LEGS C3-CELLS C3-SUITES C3-TSC C3-MUTATION C3-FORGERY C3-MOCK C3-REQBYTES C4-SECURITY C4-BUNDLE C5-DOCS-S4 C5-SHAPE C6-NOT-COVERED METHOD-STATED PR-BODY-CLAIMS COLLISION-CENSUS NOT-TESTED-LIST TIERING DISK-ENOSPC REPORT-HASH-LAST; do   # AS A TOKEN: bounded by a non-[A-Za-z0-9-] character
  printf '%s' "$PROMPT_JOINED" | grep -qE -- "(^|[^A-Za-z0-9-])$_w([^A-Za-z0-9-]|\$)" || { echo "REFUSING: the prompt does not carry the by-name keyword '$_w'" >&2; exit 33; }
done
has 'mock tokens verify ONLY through the DB-row branch' && has 'BER indefinite length refused' && has 'isQualified dropped' && has 'fail CLOSED on an empty / unset anchor bundle' && has 'byte-identical to the old forge encoder' && has 'config/tsa-trust-anchors.crt (NOT .pem' && has 'a load failure is NEVER a red' && has 'SELF-TEST ARM' && has 'NEGATIVE CONTROL' && has 'MUST-HIT' && has 'EACH RECOMPUTED BY YOU' && has '4D:24:80:7B:9C:AD:51:10:F4:0E:D7:9D:93:43:46:D7:C9:B0:29:04:31:DC:9B:11:A4:0B:BB:86:FC:F2:AE:F6' && has '3E:90:99:B5:01:5E:8F:48:6C:00:BC:EA:9D:11:1E:E7:21:FA:BA:35:5A:89:BC:F1:DF:69:56:1E:3D:C6:32:5C' && has 'NOT COVERED: KS-1404 stays In Progress' && has 'NEVER guess a new base' || { echo "REFUSING: the six checks / the rulings / the controls" >&2; exit 34; }
has 'NO MERGE, NO PUSH to any PR branch, NO ticket state change' && has 'NO ticket filed' && has 'NEVER WRITE THE SHARED CHECKOUT. Findings only' && has 'Never `rm`' && has 'No `az` command of any kind' && has 'You NEVER reply to Peter' && has 'No image is built.' && has 'NO CALL TO ANY REAL TSA' && has 'THE NAMED EXCEPTIONS to those holds — these and NO others' && has 'TICKET STATE IS WEDNESDAY' || { echo "REFUSING: the HOLDS" >&2; exit 39; }
has "WEDNESDAY'S signed GO naming the head" && has 'GO (Seat D 3rd): merge 9999 on gateD2' && has 'The merge seat is Seat D 3rd' || { echo "REFUSING: merge authority / the GO string" >&2; exit 26; }
has '## MERGE ADDENDUM' && has 'MG-1 14 over 14 paths, 2 commits' && has 'MG-11 subject <= 92' && has 'NO TRAILER' && has 'EVERY SUBJECT YOU PROPOSE MUST BE TRUE OF THE DIFF' && has 'is the LAST thing you write to report.md' && has 'sha256 report.md = <hex>' || { echo "REFUSING: the MERGE ADDENDUM rules / REPORT-HASH-LAST" >&2; exit 25; }
grep -qF -- '[QA -> Wednesday] GATED2 #9999 (Seat D3 author and merger; T1 security: real RFC 3161 verification, node-forge out of timestamping, KS-1404)' "$PROMPT_FILE" && has 'FROM coagent@agentmail.to' && has 'reports/2026-10-05-ks1404-9999-gD2/' || { echo "REFUSING: the verdict subject / sender / report dir" >&2; exit 23; }
_ANY_OVR="$(env | grep -c '^GD2_')"
NOTE="origin develop $CUR_DEV == the pinned develop | #$PR T1 ${_h:0:12} at branch AND pull/head | compare ok (ahead 2, behind 0, $NFILES paths) | pin age ${_age}s"
if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  $NOTE"
  echo "  pins, prompt, QA project and repo present; kit at its filled home; thinking directive; every kit file + gate54f report + the charter named; no unfilled token, no PR placeholder"
  echo "  the prompt carries 31 by-name keywords (as tokens), the tier lines, the six checks + the ruling's constraints + the controls, the holds + named exceptions, the GO string, the addendum + REPORT-HASH-LAST rules, the verdict subject + report dir, the head in full"
  [ "$_ANY_OVR" != 0 ] && echo "  (a GD2_* TEST OVERRIDE is set)"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"
  exit 0
fi
[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — run this launcher in a cockpit pane, never inside a Bash tool" >&2; exit 21; }
[ "$_ANY_OVR" = 0 ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions "$(cat "$PROMPT_FILE")"
