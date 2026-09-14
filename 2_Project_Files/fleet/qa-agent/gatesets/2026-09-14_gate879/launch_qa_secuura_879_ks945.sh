#!/bin/bash
# launch_qa_secuura_879_ks945.sh — cross-project QA agent, TIER 2 (a pre-push build-integrity CHECKER —
# preflight leg 13's shared-relink guard — +77 -7 in a bash/awk RUN-line classifier, +191 in its own bash
# suite; a false CLEAN reproduces the #851 crash-on-start class, a false BLOCK costs one visible commit;
# no route, schema, migration, runtime, auth or network surface) gate ROUND 2 on Secuura/Blockchain PR
# #879 (KS-945), lane L8, seat s229, pane Secuura/Blockchain-B.
#
# THE PIN. Head 0374bec007d09d62afd8596d3d15abeead0526b9 — 4 commits (79f1fcb48 the original; 238f8ada0
# Peter's two asks built; f1803166f a --no-ff merge of develop 2d864ae92 carrying the leg-14 GIT_* strip;
# 0374bec00 a --no-ff merge of develop M38 0e78c7270). Base: origin develop M38
# 0e78c7270188ac45c1c29f927bdf90728f10215d (unmoved at drafting time). 2 files, +268 -7 vs the PR's
# original base (numstat vs M38 directly: check-shared-relink.sh +77/-7, check_shared_relink.test.sh
# +191/-0). Peter APPROVED at the OLD head 79f1fcb48 (review 5142129468, comment 5585683348,
# "THE UNIT TEST GAP IS EXACTLY TWO THINGS") — both asks are BUILT at this head, each with the tamper
# that proves it (2(d)/2(f) of the s229 brief).
#
# The develop pin is judged BY CONTENT against the guard's own two files (an exact-path list, not a
# prefix — these two files sit under a shared scripts/ directory other lanes also touch): a develop move
# whose files are all outside the two paths is DISJOINT and the gate proceeds; a move touching either
# path is GUARDED (exit 18) unless CONTENT-JUDGED into DEV_CONTENT_ALLOWED by blob (exit 0, printed as
# ALLOWED) — same mechanism as gate916/gate919/gate912r2, no entries pinned yet.
#
# Refuses when stdin is not a TTY (exit 22) unless run with --check.
#
# Usage: launch_qa_secuura_879_ks945.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..22 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QA879_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gate879/2026-09-14_secuura-879-ks945-tier2-r2.md}"
PROMPT_FILE="${QA879_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gate879/2026-09-14_secuura-879-ks945-tier2-r2.prompt.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
BRANCH='refs/heads/kamilkreiser/ks-945-install-detector-fail-closed'
HEAD_SHA="${QA879_HEAD:-0374bec007d09d62afd8596d3d15abeead0526b9}"
BASE_SHA='0e78c7270188ac45c1c29f927bdf90728f10215d'
DEVELOP_SHA='0e78c7270188ac45c1c29f927bdf90728f10215d'
AHEAD_WANT=4
FILES_WANT=2
REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gate879/2026-09-14_secuura-879-ks945-tier2-r2.md"

GUARD_FILE='Blockchain/Dev/scripts/check-shared-relink.sh'
SUITE_FILE='Blockchain/Dev/scripts/__tests__/check_shared_relink.test.sh'
GUARD_HEAD_BLOB='d41c79538503d6d31e2037b3f49e025ed38f2870'
SUITE_HEAD_BLOB='867ce728ab4aab4022befddc9cf5fa5e6df439ba'

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

# The compare: base...head must read merge_base=BASE_SHA, ahead=4, files=2.
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

# The develop pin, judged by CONTENT against the guard's own two files (exact paths, not a prefix): a
# develop move touching neither is DISJOINT; a move touching either is GUARDED unless content-cleared at
# the head's own blob (which would mean this PR's own files already landed on develop — moot, exit 19).
CUR_DEV="$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)"
[ -n "$CUR_DEV" ] || { echo "REFUSING: could not read origin develop (git ls-remote)" >&2; exit 18; }
if [ "$CUR_DEV" = "$DEVELOP_SHA" ]; then
  DEV_NOTE="origin develop still $DEVELOP_SHA (M38; git ls-remote)"
else
  DEV_JUDGEMENT="$(
    set -a; . "$SECUURA_ENV"; set +a
    DEVELOP_SHA="$DEVELOP_SHA" CUR_DEV="$CUR_DEV" GUARD_FILE="$GUARD_FILE" SUITE_FILE="$SUITE_FILE" \
    GUARD_HEAD_BLOB="$GUARD_HEAD_BLOB" SUITE_HEAD_BLOB="$SUITE_HEAD_BLOB" python3 - <<'PYJ'
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
GUARDED = [os.environ["GUARD_FILE"], os.environ["SUITE_FILE"]]
LANDED_OK = {os.environ["GUARD_FILE"]: os.environ["GUARD_HEAD_BLOB"], os.environ["SUITE_FILE"]: os.environ["SUITE_HEAD_BLOB"]}
by_name = {f["filename"]: f for f in files}
hits = sorted({f["filename"] for f in files if f["filename"] in GUARDED})
if not hits:
    print("DISJOINT commits=%d files=%d" % (c["ahead_by"], len(files))); sys.exit(0)
landed = sorted(h for h in hits if h in LANDED_OK and by_name[h].get("sha") == LANDED_OK[h])
guarded_remaining = sorted(h for h in hits if h not in landed)
if guarded_remaining:
    print("GUARDED " + " ".join(guarded_remaining)); sys.exit(0)
print("LANDED879 " + ",".join(landed) + " now at the head's own blob(s) — #879 has already merged into develop"); sys.exit(0)
PYJ
  )"
  case "$DEV_JUDGEMENT" in
    DISJOINT*) DEV_NOTE="origin develop MOVED $DEVELOP_SHA -> $CUR_DEV: ${DEV_JUDGEMENT#DISJOINT } — disjoint from the two guarded paths (the guard + its suite); the gate merges the then-current develop under the head in its OWN clone, re-states the delta by name and re-derives every leg" ;;
    LANDED879*) echo "REFUSING: ${DEV_JUDGEMENT#LANDED879 } — this PR is no longer open work; rewrite the brief" >&2; exit 19 ;;
    *) echo "REFUSING: origin develop is at $CUR_DEV (pinned $DEVELOP_SHA) and the move is not provably disjoint: ${DEV_JUDGEMENT:-no judgement} — confirm the delta, re-state it, then re-pin deliberately (launcher DEVELOP_SHA/*_BLOB + brief TARGET + prompt)" >&2
       exit 18 ;;
  esac
fi

grep -q 'TIER 2' "$BRIEF" && grep -q 'TIER 2' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the tier" >&2; exit 7; }
grep -q 'ROUND 2' "$BRIEF" && grep -q 'ROUND 2' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the round" >&2; exit 15; }
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
  echo "  brief and prompt agree on TIER 2 and ROUND 2"
  echo "  prompt opens with the thinking directive and names the brief"
  echo "  brief and prompt both name the head SHA"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  exit 0
fi

[ -z "${QA879_BRIEF:-}${QA879_PROMPT:-}${QA879_HEAD:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$DEV_NOTE" >&2
[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — launch this from a pane (cockpit.sh add), never from inside a Bash tool" >&2; exit 22; }
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
