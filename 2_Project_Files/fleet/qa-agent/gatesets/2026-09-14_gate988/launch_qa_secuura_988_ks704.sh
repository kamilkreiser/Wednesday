#!/bin/bash
# launch_qa_secuura_988_ks704.sh — cross-project QA agent, TIER 2 (a k6 gate-report helper printing
# three already-collected status-code counters under a FAILED rate gate + one relabelled metrics-table
# row + a one-line call-site wiring change + a doc sample block; through code, no service, route, spec,
# Dockerfile, compose or .env key) gate ROUND 1 on Secuura/Blockchain PR #988 (KS-704), lane L10, seat
# s227, pane Secuura/Blockchain-D.
#
# THE PIN. Head 8cb99a002c5177bb1418ee1fab7cd2974076989a — ONE commit on
# feature/ks-704-k6-gate-reports-a-failure-rate-with-no-status-code-breakdown. Base: origin develop M38
# 0e78c7270188ac45c1c29f927bdf90728f10215d (unmoved at drafting time). 4 files, +287 -10 (numstat,
# re-derived: quick-start.md +12/-1, cli.ts +1/-1, report.ts +108/-8, the new test +166/-0).
#
# The develop pin is judged BY CONTENT: this PR touches nothing outside systemTest/performance/, so any
# develop move whose files are all outside that prefix is DISJOINT and the gate proceeds; a move
# touching anything under systemTest/performance/ is GUARDED (exit 18) unless CONTENT-JUDGED into
# DEV_CONTENT_ALLOWED by blob (exit 0, printed as ALLOWED) — same mechanism as gate916/gate912r2, no
# entries pinned yet.
#
# Refuses when stdin is not a TTY (exit 22) unless run with --check.
#
# Usage: launch_qa_secuura_988_ks704.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..22 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QA988_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gate988/2026-09-14_secuura-988-ks704-tier2.md}"
PROMPT_FILE="${QA988_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gate988/2026-09-14_secuura-988-ks704-tier2.prompt.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
BRANCH='refs/heads/feature/ks-704-k6-gate-reports-a-failure-rate-with-no-status-code-breakdown'
HEAD_SHA="${QA988_HEAD:-8cb99a002c5177bb1418ee1fab7cd2974076989a}"
BASE_SHA='0e78c7270188ac45c1c29f927bdf90728f10215d'
DEVELOP_SHA='0e78c7270188ac45c1c29f927bdf90728f10215d'
AHEAD_WANT=1
FILES_WANT=4
REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gate988/2026-09-14_secuura-988-ks704-tier2.md"

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

# The compare: base...head must read merge_base=BASE_SHA, ahead=1, files=4.
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

# The develop pin, judged by CONTENT: this PR touches nothing outside systemTest/performance/, so a move
# entirely outside that prefix is disjoint; any move touching systemTest/performance/ is GUARDED unless
# content-cleared.
CUR_DEV="$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)"
[ -n "$CUR_DEV" ] || { echo "REFUSING: could not read origin develop (git ls-remote)" >&2; exit 18; }
if [ "$CUR_DEV" = "$DEVELOP_SHA" ]; then
  DEV_NOTE="origin develop still $DEVELOP_SHA (M38; git ls-remote)"
else
  DEV_JUDGEMENT="$(
    set -a; . "$SECUURA_ENV"; set +a
    DEVELOP_SHA="$DEVELOP_SHA" CUR_DEV="$CUR_DEV" python3 - <<'PYJ'
import json, os, sys, urllib.request
t = os.environ.get("GH_TOKEN", "")
u = "https://api.github.com/repos/Secuura/Distributed_Secuura/compare/" + os.environ["DEVELOP_SHA"] + "..." + os.environ["CUR_DEV"]
try:
    c = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}), timeout=60))
except Exception as e:
    print("UNJUDGEABLE compare unreadable: " + type(e).__name__); sys.exit(0)
files = c.get("files") or []
if c.get("status") != "ahead" or len(files) > 250:
    print("UNJUDGEABLE status=%s files=%d" % (c.get("status"), len(files))); sys.exit(0)
# DEV_CONTENT_ALLOWED: grows only when a future drafter measures a specific systemTest/performance/ blob
# safe by content, never by path. Empty today.
DEV_CONTENT_ALLOWED = {}
GUARDED_PREFIX = "systemTest/performance/"
hits = sorted({f["filename"] for f in files if f["filename"].startswith(GUARDED_PREFIX)})
cleared = sorted(h for h in hits if h in DEV_CONTENT_ALLOWED and next((x["sha"] for x in files if x["filename"] == h), None) == DEV_CONTENT_ALLOWED[h])
remaining = sorted(h for h in hits if h not in cleared)
if remaining:
    print("GUARDED " + " ".join(remaining)); sys.exit(0)
if cleared:
    print("ALLOWED commits=%d files=%d cleared=%s" % (c["ahead_by"], len(files), ",".join(cleared))); sys.exit(0)
print("DISJOINT commits=%d files=%d" % (c["ahead_by"], len(files))); sys.exit(0)
PYJ
  )"
  case "$DEV_JUDGEMENT" in
    DISJOINT*) DEV_NOTE="origin develop MOVED $DEVELOP_SHA -> $CUR_DEV: ${DEV_JUDGEMENT#DISJOINT } — disjoint from systemTest/performance/ (this PR's only guarded prefix); the gate re-derives every leg on the then-current develop and re-states the delta by name" ;;
    ALLOWED*) DEV_NOTE="origin develop MOVED $DEVELOP_SHA -> $CUR_DEV: ${DEV_JUDGEMENT#ALLOWED } — the cleared files sit under systemTest/performance/ but were CONTENT-JUDGED, not path-excused" ;;
    *) echo "REFUSING: origin develop is at $CUR_DEV (pinned $DEVELOP_SHA) and the move touches systemTest/performance/ without a content clearance: ${DEV_JUDGEMENT:-no judgement} — confirm the delta, then re-pin deliberately (launcher DEVELOP_SHA + brief TARGET + prompt)" >&2
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
  exit 0
fi

[ -z "${QA988_BRIEF:-}${QA988_PROMPT:-}${QA988_HEAD:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$DEV_NOTE" >&2
[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — launch this from a pane (cockpit.sh add), never from inside a Bash tool" >&2; exit 22; }
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
