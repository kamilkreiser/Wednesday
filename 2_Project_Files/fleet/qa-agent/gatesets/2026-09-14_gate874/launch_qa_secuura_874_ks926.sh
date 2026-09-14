#!/bin/bash
# launch_qa_secuura_874_ks926.sh — cross-project QA agent, TIER 2 (a docs READ gate — ONE markdown family
# record under Blockchain/Dev/docs/, no code, no config, no runtime, no route, no schema, no migration)
# gate ROUND 1 on Secuura/Blockchain PR #874 (KS-926 campaign document), lane L8, seat s229, pane
# Secuura/Blockchain-B.
#
# THE PIN. Head b244f4913c948b6d763a6abcf018dac301232345 — 5 commits: the four 09-06 authoring commits
# (5e83eb28f -> fe5225f31 -> bea418b02 -> 6f7885602) + a --no-ff merge of develop M38 0e78c7270 (the
# document is byte-unchanged by the merge-in — blob e31f85cda both before and after). Base: origin
# develop M38 0e78c7270188ac45c1c29f927bdf90728f10215d (unmoved at drafting time). ONE file, +355 (new).
#
# THE ARCHIVED-TICKET EXCEPTION. KS-926 is Done and ARCHIVED (2026-09-14T02:17:17Z, after #918 landed as
# M22) — an archived ticket refuses commentCreate ("Entity not found"). This gate posts NOTHING to KS-926
# (or any other ticket) — findings go only into the report and the verdict mail, per BOUNDS.
#
# The develop pin is judged BY CONTENT against the one PR file (a single exact path, not a prefix): a
# develop move that does not touch it is DISJOINT and the gate proceeds; a move that touches it is
# GUARDED (exit 18) unless CONTENT-JUDGED into DEV_CONTENT_ALLOWED by blob (exit 0, ALLOWED) or the move
# lands the file at the head's own blob (exit 19, moot — the PR already merged).
#
# Refuses when stdin is not a TTY (exit 22) unless run with --check.
#
# Usage: launch_qa_secuura_874_ks926.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..22 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QA874_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gate874/2026-09-14_secuura-874-ks926-tier2.md}"
PROMPT_FILE="${QA874_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gate874/2026-09-14_secuura-874-ks926-tier2.prompt.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
BRANCH='refs/heads/kamilkreiser/ks-926-checks-that-cannot-fail'
HEAD_SHA="${QA874_HEAD:-b244f4913c948b6d763a6abcf018dac301232345}"
BASE_SHA='0e78c7270188ac45c1c29f927bdf90728f10215d'
DEVELOP_SHA='0e78c7270188ac45c1c29f927bdf90728f10215d'
AHEAD_WANT=5
FILES_WANT=1
REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gate874/2026-09-14_secuura-874-ks926-tier2.md"

DOC_FILE='Blockchain/Dev/docs/KS-926-CHECKS-THAT-CANNOT-FAIL.md'
DOC_HEAD_BLOB='e31f85cda8dfadf1d57f3cc975ad7f219b8966f8'

[ -d "$QA_DIR" ]      || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]       || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ] || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]        || { echo "repo under test missing: $REPO" >&2; exit 5; }

# The head must still be at its branch on origin (the verdict is per PR, on this SHA).
LSR="$(git -C "$REPO" ls-remote origin "$BRANCH")"
if ! printf '%s\n' "$LSR" | grep -q "^${HEAD_SHA}[[:space:]]${BRANCH}\$"; then
  echo "REFUSING: $HEAD_SHA is not at $BRANCH on origin — the head moved; re-pin HEAD_SHA (one line) and FILES_WANT if the file count changed" >&2
  printf '%s\n' "$LSR" >&2
  exit 6
fi

# The compare: base...head must read merge_base=BASE_SHA, ahead=5, files=1.
CMP_READ="$(
  set -a; . "$SECUURA_ENV"; set +a
  HEAD_SHA="$HEAD_SHA" BASE_SHA="$BASE_SHA" python3 - <<'PY'
import json, os, sys, urllib.request
t = os.environ.get("GH_TOKEN", "")
api = "https://api.github.com/repos/Secuura/Distributed_Secuura/compare/" + os.environ["BASE_SHA"] + "..." + os.environ["HEAD_SHA"]
try:
    c = json.load(urllib.request.urlopen(urllib.request.Request(api, headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}), timeout=60))
except Exception as e:
    print("UNREADABLE " + type(e).__name__, file=sys.stderr); sys.exit(0)
print("mb=%s ahead=%d files=%d" % (c["merge_base_commit"]["sha"], c["ahead_by"], len(c.get("files") or [])))
PY
)"
[ -n "$CMP_READ" ] || { echo "REFUSING: could not read the compare from the GitHub compare API (env file missing/unreadable, or the API refused)" >&2; exit 13; }
CMP_WANT="mb=$BASE_SHA ahead=$AHEAD_WANT files=$FILES_WANT"
[ "$CMP_READ" = "$CMP_WANT" ] || { echo "REFUSING: the compare does not read as the brief pins it: got '$CMP_READ', brief pins '$CMP_WANT'" >&2; exit 10; }

# The develop pin, judged by CONTENT against the one PR file (exact path): a move that does not touch it
# is disjoint; a move that touches it is GUARDED unless content-cleared (landed at the head's own blob).
CUR_DEV="$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)"
[ -n "$CUR_DEV" ] || { echo "REFUSING: could not read origin develop (git ls-remote)" >&2; exit 18; }
if [ "$CUR_DEV" = "$DEVELOP_SHA" ]; then
  DEV_NOTE="origin develop still $DEVELOP_SHA (M38; git ls-remote)"
else
  DEV_JUDGEMENT="$(
    set -a; . "$SECUURA_ENV"; set +a
    DEVELOP_SHA="$DEVELOP_SHA" CUR_DEV="$CUR_DEV" DOC_FILE="$DOC_FILE" DOC_HEAD_BLOB="$DOC_HEAD_BLOB" python3 - <<'PYJ'
import json, os, sys, urllib.request
t = os.environ.get("GH_TOKEN", "")
api = "https://api.github.com/repos/Secuura/Distributed_Secuura"
pinned = os.environ["DEVELOP_SHA"]; cur = os.environ["CUR_DEV"]
try:
    c = json.load(urllib.request.urlopen(urllib.request.Request(api + "/compare/" + pinned + "..." + cur, headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}), timeout=60))
except Exception as e:
    print("UNJUDGEABLE compare unreadable: " + type(e).__name__); sys.exit(0)
files = c.get("files") or []
if c.get("status") != "ahead" or len(files) > 250:
    print("UNJUDGEABLE status=%s files=%d" % (c.get("status"), len(files))); sys.exit(0)
DOC_FILE = os.environ["DOC_FILE"]; DOC_HEAD_BLOB = os.environ["DOC_HEAD_BLOB"]
by_name = {f["filename"]: f for f in files}
if DOC_FILE not in by_name:
    print("DISJOINT commits=%d files=%d" % (c["ahead_by"], len(files))); sys.exit(0)
if by_name[DOC_FILE].get("sha") == DOC_HEAD_BLOB:
    print("LANDED874 %s now at the head's own blob — #874 has already merged into develop" % DOC_FILE); sys.exit(0)
print("GUARDED " + DOC_FILE); sys.exit(0)
PYJ
  )"
  case "$DEV_JUDGEMENT" in
    DISJOINT*) DEV_NOTE="origin develop MOVED $DEVELOP_SHA -> $CUR_DEV: ${DEV_JUDGEMENT#DISJOINT } — disjoint from the one PR file; the gate re-reads the document on the then-current develop-merged tree" ;;
    LANDED874*) echo "REFUSING: ${DEV_JUDGEMENT#LANDED874 } — this PR is no longer open work; rewrite the brief" >&2; exit 19 ;;
    *) echo "REFUSING: origin develop is at $CUR_DEV (pinned $DEVELOP_SHA) and the move touches the PR's file without a content clearance: ${DEV_JUDGEMENT:-no judgement} — confirm the delta, then re-pin deliberately (launcher DEVELOP_SHA + brief TARGET + prompt)" >&2
       exit 18 ;;
  esac
fi

grep -q 'TIER 2' "$BRIEF" && grep -q 'TIER 2' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the tier" >&2; exit 7; }
grep -q 'ROUND 1' "$BRIEF" && grep -q 'ROUND 1' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the round" >&2; exit 15; }
head -1 "$PROMPT_FILE" | grep -q 'ultrathink' || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 8; }
grep -qF "$REAL_BRIEF" "$PROMPT_FILE" || { echo "REFUSING: prompt does not name the brief path" >&2; exit 9; }
grep -qF "$HEAD_SHA" "$PROMPT_FILE" && grep -qF "$HEAD_SHA" "$BRIEF" \
  || { echo "REFUSING: brief or prompt does not name the head SHA $HEAD_SHA — a gate about another SHA is another gate" >&2; exit 20; }
grep -qi 'MAIL YOUR VERDICT' "$PROMPT_FILE" || { echo "REFUSING: prompt does not tell the agent to MAIL its verdict" >&2; exit 12; }
grep -qi 'NEVER run a push, the real pre-push hook, or preflight.sh inside the Secuura checkout' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid pushing / running the hook in the real checkout" >&2; exit 11; }
grep -qi 'no memory maintenance' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid memory maintenance inside the gate session" >&2; exit 14; }
grep -qi 'NEVER print a credential value' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid printing a credential value" >&2; exit 17; }
grep -qi 'KS-926 is Done and ARCHIVED' "$BRIEF" \
  || { echo "REFUSING: brief does not state the archived-ticket exception — a gate that tries commentCreate on KS-926 will get 'Entity not found' and may misread it" >&2; exit 21; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  head $HEAD_SHA present at $BRANCH on origin"
  echo "  compare: $CMP_READ (GitHub compare API)"
  echo "  $DEV_NOTE"
  echo "  brief, prompt, QA project and repo all present"
  echo "  brief and prompt agree on TIER 2 and ROUND 1"
  echo "  prompt opens with the thinking directive and names the brief"
  echo "  brief and prompt both name the head SHA"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  echo "  brief states the KS-926 archived-ticket exception"
  exit 0
fi

[ -z "${QA874_BRIEF:-}${QA874_PROMPT:-}${QA874_HEAD:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$DEV_NOTE" >&2
[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — launch this from a pane (cockpit.sh add), never from inside a Bash tool" >&2; exit 22; }
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
