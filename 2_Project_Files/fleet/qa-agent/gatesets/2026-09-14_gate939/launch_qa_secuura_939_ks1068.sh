#!/bin/bash
# launch_qa_secuura_939_ks1068.sh — cross-project QA agent, TIER 2 (a widened blockchain-blob type + a comment
# clause + a compile-time contract test; through code, no runtime/service surface — the reach question is
# `tsc` itself) gate, ROUND 1, ONE PASS, Secuura/Blockchain PR #939 (KS-1068), lane L2, seat s226, pane
# `Secuura/Blockchain-C`. Commissioned as a THIRD set mid-session alongside gate919/gate916 (Wednesday,
# 2026-09-14 17:04 AEST): same shape, same END STATE.
#
# THE PIN. Head `284661efe262b825d83b31b875020ff7765757b8` — chain 481e0267f (the PR's own 09-10 commit) ->
# 91fb13c6e (--no-ff merge of develop M38) -> 284661efe (the R2 comment clause). Base: origin develop M38
# 0e78c7270188ac45c1c29f927bdf90728f10215d (merge-base of head and develop = develop itself). The three files
# (+ the audit-baseline control row) are judged by BLOB, not by path, exactly as gate912r2's DEV_CONTENT_ALLOWED
# does: a develop move that lands one of #939's own files at the HEAD's own blob means #939 already merged and
# this gate is moot (exit 19); a develop move under one of the guarded paths to any OTHER blob is GUARDED (exit
# 18, re-pin deliberately); a develop move disjoint from all of them proceeds (rc 0), printed and re-stated.
#
# GUARDED prefixes — deliberately narrower than a blanket "originate/src/" refusal, since PR #919 and other L2
# lane siblings touch that prefix routinely and disjointly:
#   Blockchain/Dev/services/originate/src/repositories/documentRepo.ts
#   Blockchain/Dev/services/originate/src/routes/documents.ts
#   Blockchain/Dev/services/originate/src/__tests__/ks1068-blockchain-blob-type.test.ts
#   Blockchain/Dev/packages/shared/
#   Blockchain/Dev/scripts/audit/audit-baseline.json
#   Blockchain/Dev/package-lock.json
#
# Refuses when stdin is not a TTY (exit 21) unless run with --check.
#
# Usage: launch_qa_secuura_939_ks1068.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..21 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QA939_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gate939/2026-09-14_secuura-939-ks1068-tier2.md}"
PROMPT_FILE="${QA939_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gate939/2026-09-14_secuura-939-ks1068-tier2.prompt.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
BRANCH='refs/heads/feature/ks-1068-threadtoken-confidence-blockchain-blob-type'
HEAD_SHA="${QA939_HEAD:-284661efe262b825d83b31b875020ff7765757b8}"
DEVELOP_SHA='0e78c7270188ac45c1c29f927bdf90728f10215d'
REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gate939/2026-09-14_secuura-939-ks1068-tier2.md"

TEST_FILE='Blockchain/Dev/services/originate/src/__tests__/ks1068-blockchain-blob-type.test.ts'
REPO_FILE='Blockchain/Dev/services/originate/src/repositories/documentRepo.ts'
DOC_FILE='Blockchain/Dev/services/originate/src/routes/documents.ts'
BASELINE_FILE='Blockchain/Dev/scripts/audit/audit-baseline.json'
LOCK_FILE='Blockchain/Dev/package-lock.json'
SHARED_PREFIX='Blockchain/Dev/packages/shared/'

TEST_HEAD_BLOB='f45d3743c943fe2ac5f4406bcdb42e9979cd98a7'
REPO_HEAD_BLOB='6e059d36c50a82016faca14111c28ec35bc4f237'
DOC_HEAD_BLOB='f403c37a57aee22d582d3a34247682cc39b9139b'
BASELINE_OK_BLOB='03d1680e3c7a87f8df70e71082b67775536acde5'

[ -d "$QA_DIR" ]         || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]          || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ]    || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]           || { echo "repo under test missing: $REPO" >&2; exit 5; }

LSR="$(git -C "$REPO" ls-remote origin "$BRANCH")"
if ! printf '%s\n' "$LSR" | grep -q "^${HEAD_SHA}[[:space:]]${BRANCH}\$"; then
  echo "REFUSING: $HEAD_SHA is not at $BRANCH on origin — the head moved; the brief is about a different SHA" >&2
  printf '%s\n' "$LSR" >&2
  exit 6
fi

CMP_READ="$(
  set -a; . "$SECUURA_ENV"; set +a
  HEAD_SHA="$HEAD_SHA" DEVELOP_SHA="$DEVELOP_SHA" python3 - <<'PY'
import json, os, urllib.request
t = os.environ.get("GH_TOKEN", "")
u = "https://api.github.com/repos/Secuura/Distributed_Secuura/compare/" + os.environ["DEVELOP_SHA"] + "..." + os.environ["HEAD_SHA"]
r = urllib.request.urlopen(urllib.request.Request(u, headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}), timeout=60)
c = json.load(r)
print("mb=%s ahead=%d files=%d" % (c["merge_base_commit"]["sha"], c["ahead_by"], len(c.get("files") or [])))
PY
)"
[ -n "$CMP_READ" ] || { echo "REFUSING: could not read the compare from the GitHub compare API" >&2; exit 13; }
CMP_WANT="mb=$DEVELOP_SHA ahead=4 files=3"
[ "$CMP_READ" = "$CMP_WANT" ] || { echo "REFUSING: the compare does not read as the brief pins it: got '$CMP_READ', brief pins '$CMP_WANT'" >&2; exit 10; }

CUR_DEV="$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)"
[ -n "$CUR_DEV" ] || { echo "REFUSING: could not read origin develop (git ls-remote)" >&2; exit 18; }
if [ "$CUR_DEV" = "$DEVELOP_SHA" ]; then
  DEV_NOTE="origin develop still $DEVELOP_SHA (M38, git ls-remote)"
else
  DEV_JUDGEMENT="$(
    set -a; . "$SECUURA_ENV"; set +a
    DEVELOP_SHA="$DEVELOP_SHA" CUR_DEV="$CUR_DEV" \
    TEST_FILE="$TEST_FILE" REPO_FILE="$REPO_FILE" DOC_FILE="$DOC_FILE" BASELINE_FILE="$BASELINE_FILE" LOCK_FILE="$LOCK_FILE" SHARED_PREFIX="$SHARED_PREFIX" \
    TEST_HEAD_BLOB="$TEST_HEAD_BLOB" REPO_HEAD_BLOB="$REPO_HEAD_BLOB" DOC_HEAD_BLOB="$DOC_HEAD_BLOB" BASELINE_OK_BLOB="$BASELINE_OK_BLOB" \
    python3 - <<'PYJ'
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
GUARDED = [os.environ["TEST_FILE"], os.environ["REPO_FILE"], os.environ["DOC_FILE"], os.environ["BASELINE_FILE"], os.environ["LOCK_FILE"], os.environ["SHARED_PREFIX"]]
LANDED_OK = {os.environ["TEST_FILE"]: os.environ["TEST_HEAD_BLOB"], os.environ["REPO_FILE"]: os.environ["REPO_HEAD_BLOB"], os.environ["DOC_FILE"]: os.environ["DOC_HEAD_BLOB"]}
by_name = {f["filename"]: f for f in files}
hits = sorted({f["filename"] for f in files for g in GUARDED if f["filename"] == g or (g.endswith("/") and f["filename"].startswith(g))})
if not hits:
    print("DISJOINT commits=%d files=%d" % (c["ahead_by"], len(files))); sys.exit(0)
landed = sorted(h for h in hits if h in LANDED_OK and by_name[h].get("sha") == LANDED_OK[h])
guarded_remaining = sorted(h for h in hits if h not in landed)
if guarded_remaining:
    print("GUARDED " + " ".join(guarded_remaining)); sys.exit(0)
print("LANDED939 " + ",".join(landed) + " now at the head's own blob(s) — #939 has already merged into develop"); sys.exit(0)
PYJ
  )"
  case "$DEV_JUDGEMENT" in
    DISJOINT*) DEV_NOTE="origin develop MOVED $DEVELOP_SHA -> $CUR_DEV: ${DEV_JUDGEMENT#DISJOINT } — disjoint from the six guarded paths (#939's three files, the audit baseline, packages/shared/, the root lockfile); the gate merges the then-current develop under the head in its OWN clone, rebuilds packages/shared, re-derives tsc and every count (brief items 1-8)" ;;
    LANDED939*) echo "REFUSING: ${DEV_JUDGEMENT#LANDED939 } — this PR is no longer open work; rewrite the brief" >&2; exit 19 ;;
    *) echo "REFUSING: origin develop is at $CUR_DEV (pinned $DEVELOP_SHA) and the move is not provably disjoint: ${DEV_JUDGEMENT:-no judgement} — confirm the delta, re-state it, then re-pin deliberately (launcher DEVELOP_SHA/*_BLOB + brief TARGET + prompt)" >&2
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

[ -z "${QA939_BRIEF:-}${QA939_PROMPT:-}${QA939_HEAD:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$DEV_NOTE" >&2
[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — launch this from a pane (cockpit.sh add), never from inside a Bash tool" >&2; exit 21; }
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
