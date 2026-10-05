#!/bin/bash
# dry042228.SIM.launcher.sh — cross-project QA agent, ONE gate (gate57, round 57) over TWO Secuura/Blockchain PRs, FROZEN at TWO:
# #1380 KS-1333 (T2): a test-only pin of the anchoring blockNumber shape + the two owed one-line doc corrections (Q-27, N-1375-1);
# #1381 KS-1345 (T1, a BEHAVIOUR CHANGE): originate's webhooks list query answers a constant 500 on a DB failure, not 200 [].
# Author and merger: Seat B 60th, one GO per PR, #1380 first; #1381 needs a MERGE-IN after #1380 lands (predicted T2 fb53feacdf1d03e3e949f7cf3a607254e8e5d9c6; Q-M).
# PINNED by repin_and_launch_gate57.sh at 2026-10-05T04:23:03Z from its own ls-remote + PULLS API reads: #1380 ac9f67a661eababfff30a1128f14c853803bd584 on feature/ks-1333-blocknumber-pin-b60-1,
# #1381 7b356195a5e41d530c11f8e9286a6284be55b7c2 on feature/ks-1345-webhooks-list-500-b60-2, develop fe6daca343c143c32b1eb76d681668b4edbe4074 (cut_base 3ce8cd4026a6e3241413e9c7533d5a84d10c1c79, behind 1). A NEW COPY of gate56a's / gate58's launcher.
# exit 2:  QA project missing, or this launcher is not in the gateset dir it was filled for (a MOVED KIT).   exit 3-5: pins / prompt / repo missing.
# exit 6:  a head is not at its branch AND refs/pull/<n>/head on origin.   exit 8: thinking directive / kit files / reports / READY / an unfilled token.
# exit 9:  STALE PIN: older than G57_MAX_PIN_AGE_S (default 1800 s) — re-pin through repin_and_launch_gate57.sh.
# exit 10: a GitHub compare develop...head is not merge_base cut_base / ahead 1 / behind 1 / its own paths.   exit 17: origin develop moved.
# exit 20: the prompt does not name both heads and T2 in full.   exit 7: tiers + FROZEN + round.   exit 33: measurement rules + keyword ladder.
# exit 39: HOLDS + named exceptions.   exit 34: the checks + controls.   exit 26: the two GO strings.   exit 25: MERGE ADDENDUM + REPORT-HASH-LAST.
# exit 23: verdict subject / sender / report dir.   exit 21: the LAUNCH path refuses when stdin is not a TTY.   exit 16: a G57_* override set.
# G57_CUR_DEV / G57_PROMPT / G57_PINS / G57_NOW / G57_COMPARE_FILE / G57_LSREMOTE_FILE: test overrides (--check only; a launch refuses any G57_*).
# Opus by the configured default: the exec line carries NO --model.
# Usage: dry042228.SIM.launcher.sh [--check]
set -u
MODE="${1:-}"
QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
GS='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-05_gate57'
PROMPT_FILE="${G57_PROMPT:-$GS/dry042228.SIM.prompt.txt}"
PINS="${G57_PINS:-$GS/pins_gate57.SIM-dry042228.json}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
PR1='1380'; HEAD1='ac9f67a661eababfff30a1128f14c853803bd584'; BRANCH1='refs/heads/feature/ks-1333-blocknumber-pin-b60-1'; FILES1='Blockchain/Dev/services/anchoring/src/__tests__/ks1333-get-by-id-blocknumber-is-a-number.test.ts,Projects Documents/API_Security_Functional_Testing_Architecture_Flow_Diagrams.html,Projects Documents/QA_Tool_Cheat_Sheet_Secuura_API_Testing.html'; N1='3'
PR2='1381'; HEAD2='7b356195a5e41d530c11f8e9286a6284be55b7c2'; BRANCH2='refs/heads/feature/ks-1345-webhooks-list-500-b60-2'; FILES2='Blockchain/Dev/services/originate/src/__tests__/ks1341a-webhooks-500-never-answers-err-message.test.ts,Blockchain/Dev/services/originate/src/routes/webhooks.ts,Projects Documents/API_Security_Functional_Testing_Architecture_Flow_Diagrams.html,Projects Documents/QA_Tool_Cheat_Sheet_Secuura_API_Testing.html'; N2='4'
DEVELOP_SHA='fe6daca343c143c32b1eb76d681668b4edbe4074'; CUT_BASE='3ce8cd4026a6e3241413e9c7533d5a84d10c1c79'; BEHIND='1'; T2='fb53feacdf1d03e3e949f7cf3a607254e8e5d9c6'
PINNED_EPOCH='1791174183'
[ -d "$QA_DIR" ]      || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
_here="$(dirname "$(/bin/realpath "$0")")"
[ "$_here" = "$GS" ] || { echo "REFUSING: this launcher lives in $_here but was filled for $GS — a MOVED KIT: run repin_and_launch_gate57.sh from its new home" >&2; exit 2; }
[ -s "$PINS" ]        || { echo "pins missing or empty: $PINS" >&2; exit 3; }
[ -s "$PROMPT_FILE" ] || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]        || { echo "repo under test missing: $REPO" >&2; exit 5; }
_age=$(( ${G57_NOW:-$(date +%s)} - PINNED_EPOCH ))
[ "$_age" -le "${G57_MAX_PIN_AGE_S:-1800}" ] || { echo "REFUSING: STALE PIN — pinned ${_age}s ago (max ${G57_MAX_PIN_AGE_S:-1800}s); run repin_and_launch_gate57.sh" >&2; exit 9; }
[ "$(python3 -c 'import json,sys; p=json.load(open(sys.argv[1])); print(p["pr1"], p["head1"], p["pr2"], p["head2"], p["develop"])' "$PINS")" = "$PR1 $HEAD1 $PR2 $HEAD2 $DEVELOP_SHA" ] || { echo "REFUSING: the pins file and this launcher disagree (a re-fill was interrupted)" >&2; exit 3; }
[ "$(head -n 1 "$PROMPT_FILE")" = "ultrathink" ] || { echo "REFUSING: the prompt does not open with the thinking directive" >&2; exit 8; }
for _f in README.md COMMISSION.md kit.json lib_gate57.py c1_pin_gate57.py c2a_ks1333_gate57.py c2b_docfix_gate57.py c3_ks1345_gate57.py c3_probe_ks1345_gate57.test.ts.txt c4_docs_gate57.py c4b_predict_gate57.py c5_preflight_gate57.py c6_scope_gate57.py gh_census_gate57.py; do
  [ -s "$GS/$_f" ] && grep -qF "$GS/$_f" "$PROMPT_FILE" || { echo "REFUSING: the kit file $GS/$_f is missing, empty, or not named in the prompt" >&2; exit 8; }
done
grep -qF "2026-10-05-ks1015-1375-g55/report.md" "$PROMPT_FILE" && grep -qF "2026-10-05-ks1404-1376-gD2/report.md" "$PROMPT_FILE" || { echo "REFUSING: the prompt does not name both previous round reports (gate55, gateD2)" >&2; exit 8; }
grep -qF "/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md" "$PROMPT_FILE" || { echo "REFUSING: the prompt does not name the QA charter" >&2; exit 8; }
grep -qF "2026-10-05_seatB60_READY_1380_1381.txt" "$PROMPT_FILE" || { echo "REFUSING: the prompt does not name the seat's READY" >&2; exit 8; }
grep -qE '\{\{[A-Z0-9_]+\}\}' "$PROMPT_FILE" && { echo "REFUSING: the prompt carries an unfilled double-brace fill token" >&2; exit 8; }
if [ -n "${G57_LSREMOTE_FILE:-}" ]; then _LS="$(cat "$G57_LSREMOTE_FILE")"; else
_LS="$(git -C "$REPO" ls-remote origin refs/heads/develop "$BRANCH1" "refs/pull/$PR1/head" "$BRANCH2" "refs/pull/$PR2/head")"   # ONE read of origin
fi
CUR_DEV="${G57_CUR_DEV:-$(printf '%s\n' "$_LS" | awk '$2=="refs/heads/develop"{print $1}')}"
[ "$CUR_DEV" = "$DEVELOP_SHA" ] || { echo "REFUSING: origin develop $CUR_DEV != the pinned develop $DEVELOP_SHA — run repin_and_launch_gate57.sh" >&2; exit 17; }
headcheck() {   # $1 PR  $2 head  $3 branch ref
  if [ "$(printf '%s\n' "$_LS" | awk -v h="$2" -v r="$3" '$1==h && $2==r' | wc -l | tr -d ' ')" != 1 ] || [ "$(printf '%s\n' "$_LS" | awk -v h="$2" -v r="refs/pull/$1/head" '$1==h && $2==r' | wc -l | tr -d ' ')" != 1 ]; then
    echo "REFUSING: #$1 — $2 is not at $3 AND refs/pull/$1/head on origin — the head moved (or the pin is wrong); a verdict is valid ONLY at its head" >&2
    printf '%s\n' "$_LS" >&2; exit 6
  fi
}
headcheck "$PR1" "$HEAD1" "$BRANCH1"; headcheck "$PR2" "$HEAD2" "$BRANCH2"
compare() {   # $1 head -> "<merge_base> ahead=<n> behind=<n> files=<n> paths=<csv>"
  if [ -n "${G57_COMPARE_FILE:-}" ]; then grep -F "$1 " "$G57_COMPARE_FILE" | cut -d' ' -f2-; return; fi
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
_c1="$(compare "$HEAD1")"; _w1="$CUT_BASE ahead=1 behind=$BEHIND files=$N1 paths=$FILES1"
[ "$_c1" = "$_w1" ] || { echo "REFUSING: #$PR1 — the compare is not cut_base / ahead 1 / behind $BEHIND / its $N1 paths:" >&2; echo "  got  $_c1" >&2; echo "  want $_w1" >&2; exit 10; }
_c2="$(compare "$HEAD2")"; _w2="$CUT_BASE ahead=1 behind=$BEHIND files=$N2 paths=$FILES2"
[ "$_c2" = "$_w2" ] || { echo "REFUSING: #$PR2 — the compare is not cut_base / ahead 1 / behind $BEHIND / its $N2 paths:" >&2; echo "  got  $_c2" >&2; echo "  want $_w2" >&2; exit 10; }
grep -qwF "$HEAD1" "$PROMPT_FILE" && grep -qwF "$HEAD2" "$PROMPT_FILE" && grep -qwF "$T2" "$PROMPT_FILE" || { echo "REFUSING: the prompt does not name both heads and T2 in full" >&2; exit 20; }
PROMPT_JOINED="$(python3 -c 'import re,sys; print(re.sub(r"\n\s*", " ", open(sys.argv[1], encoding="utf-8").read()))' "$PROMPT_FILE")"
has() { printf '%s' "$PROMPT_JOINED" | grep -qF -- "$1"; }
has "PR #$PR1 is KS-1333" && has "PR #$PR2 is KS-1345" && has "#$PR1 T2 and #$PR2 T1" && has 'THE GATE IS FROZEN at TWO PRs' && has 'ROUND 1' && has 'Each PR gets its OWN verdict' && has 'round-1 NO GO goes back to the author for round 2' || { echo "REFUSING: the tickets / tiers / FROZEN / round" >&2; exit 7; }
has 'MEASURE, not conclude' && has 'RULE WHETHER IT BLOCKS' && has 'NAMES THE TREE' && has 'A check that prints nothing needs a control that prints' && has 'ASSERT THE FILENAME TOO' || { echo "REFUSING: the measurement rules" >&2; exit 33; }
for _w in C1-PIN END-TREE NO-TRAILER SUBJECT-EXACT C2-GOLDEN C2-TAMPER C2-SUITE C2-DOCFIX Q-27 N-1375-1 C3-SHAPE C3-RED-FIRST C3-PROBE C3-SUITE C3-TSC C4-DOCS C4-PREDICT Q-M C5-PREFLIGHT PREFLIGHT-INCOMPLETE C6-SCOPE KEYSCAN-OWN-KEY NOT-COVERED READY-CLAIMS PR-BODY-CLAIMS COLLISION-CENSUS NOT-TESTED-LIST TIERING DISK-ENOSPC REPORT-HASH-LAST; do   # AS A TOKEN: bounded by a non-[A-Za-z0-9-] character
  printf '%s' "$PROMPT_JOINED" | grep -qE -- "(^|[^A-Za-z0-9-])$_w([^A-Za-z0-9-]|\$)" || { echo "REFUSING: the prompt does not carry the by-name keyword '$_w'" >&2; exit 33; }
done
has 'SELF-TEST ARM' && has 'BY TAMPER' && has 'BY ASSERTION' && has 'CHARACTER diff' && has 'non-UUID userId' && has 'POSITIVE CONTROL' && has 'INDEPENDENTLY' && has '12/15 is NOT a pass' && has 'the deliveries half' && has 'wrong-order control' || { echo "REFUSING: the checks / the controls" >&2; exit 34; }
has 'NO MERGE, NO PUSH to any PR branch, NO ticket state change' && has 'NO ticket filed' && has 'NEVER WRITE THE SHARED CHECKOUT. Findings only' && has 'Never `rm`' && has 'No `az` command of any kind' && has 'You NEVER reply to Peter' && has 'No image is built.' && has 'THE NAMED EXCEPTIONS to those holds — these and NO others' && has 'TICKET STATE IS WEDNESDAY' || { echo "REFUSING: the HOLDS" >&2; exit 39; }
has "WEDNESDAY'S signed GO naming the head, one per PR" && has 'GO (Seat B 60th): merge 1380 on gate57' && has 'GO (Seat B 60th): merge 1381 on gate57' && has 'The merge seat is Seat B 60th' || { echo "REFUSING: merge authority / the GO strings" >&2; exit 26; }
has '## MERGE ADDENDUM' && has 'ONE LINE PER PR' && has 'MG-11 subject <= 92' && has 'NO TRAILER' && has 'EVERY SUBJECT YOU PROPOSE MUST BE TRUE OF THE DIFF' && has 'are the LAST thing you write to report.md' && has 'sha256 report.md = <hex>' || { echo "REFUSING: the MERGE ADDENDUM rules / REPORT-HASH-LAST" >&2; exit 25; }
grep -qF -- '[QA -> Wednesday] GATE57 #1380 + #1381 (Seat B 60th author and merger; #1380 T2 KS-1333 blockNumber pin + Q-27 / N-1375-1 doc fixes; #1381 T1 KS-1345 webhooks list 500)' "$PROMPT_FILE" && has 'FROM coagent@agentmail.to' && has 'reports/2026-10-05-ks1333-1345-1380-1381-g57/' && has 'a `MERGE ADDENDUM` line PER PR' || { echo "REFUSING: the verdict subject / sender / report dir" >&2; exit 23; }
_ANY_OVR="$(env | grep -c '^G57_')"
NOTE="origin develop $CUR_DEV == the pinned develop (behind $BEHIND from cut_base) | #$PR1 ${HEAD1:0:12} and #$PR2 ${HEAD2:0:12} at branch AND pull/head | compares ok (ahead 1, their own paths) | pin age ${_age}s"
if [ "$MODE" = "--check" ]; then
  echo "all guards pass:"
  echo "  $NOTE"
  echo "  pins, prompt, QA project and repo present; kit at its filled home; thinking directive; every kit file + both previous reports + the charter + the READY named; no unfilled token"
  echo "  the prompt carries 30 by-name keywords (as tokens), the tier lines, the checks + controls, the holds + named exceptions, both GO strings, the addendum + REPORT-HASH-LAST rules, the verdict subject + report dir, both heads and T2 in full"
  [ "$_ANY_OVR" != 0 ] && echo "  (a G57_* TEST OVERRIDE is set)"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"
  exit 0
fi
[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — run this launcher in a cockpit pane, never inside a Bash tool" >&2; exit 21; }
[ "$_ANY_OVR" = 0 ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions "$(cat "$PROMPT_FILE")"
