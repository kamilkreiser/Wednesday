#!/bin/bash
# launch_qa_secuura_919_ks739.sh — cross-project QA agent, TIER 2 (a route error-mapping branch + a regenerated
# OpenAPI spec description; through code AND a targeted Schemathesis pass on the one published operation it
# touches, `postDocumentsByIdTransferCustody`) gate, ROUND 1, ONE PASS, Secuura/Blockchain PR #919 (KS-739),
# lane L2, seat s226, pane `Secuura/Blockchain-C`.
#
# THE PIN. Head `4736e22771c12e56d004f58a67f960ddbc0b0508` (a --no-ff merge of the PR's own 09-09 commit
# d0aff46d4 and develop M38 0e78c7270; check:openapi passed rc 0 directly on the merged tree, no regeneration
# commit needed). Base: origin develop M38 0e78c7270188ac45c1c29f927bdf90728f10215d. The four files (+ the
# audit-baseline control row) are judged by BLOB, not by path, exactly as gate912r2's DEV_CONTENT_ALLOWED does:
# a develop move that lands ANY of the four PR files at the HEAD's own blob means #919 already merged and this
# gate is moot (exit 19); a develop move that touches one of the PR's own paths to any OTHER blob is GUARDED
# (exit 18, re-pin deliberately); a develop move disjoint from all of them proceeds (rc 0), printed and re-stated.
#
# GUARDED prefixes (a develop move under these — that is not one of the four PR files' own known blobs — refuses):
#   Blockchain/Dev/services/originate/src/routes/documents.ts
#   Blockchain/Dev/services/originate/src/originate.openapi.ts
#   Blockchain/Dev/docs/openapi/secuura-api.yaml
#   Blockchain/Dev/services/originate/src/__tests__/ks739-transfer-custody-lookup-4xx-mapping.test.ts
#   Blockchain/Dev/scripts/audit/audit-baseline.json
#   Blockchain/Dev/package-lock.json
#
# Refuses when stdin is not a TTY (exit 21) unless run with --check: this launcher execs an interactive agent;
# run inside a Bash tool it runs headless, invisible and parented to the caller's shell (2026-09-13 ledger).
#
# Usage: launch_qa_secuura_919_ks739.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..21 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QA919_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gate919/2026-09-14_secuura-919-ks739-tier2.md}"
PROMPT_FILE="${QA919_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gate919/2026-09-14_secuura-919-ks739-tier2.prompt.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
BRANCH='refs/heads/feature/ks-739-transfer-custody-maps-a-401403-from-userslookup-to-502'
HEAD_SHA="${QA919_HEAD:-4736e22771c12e56d004f58a67f960ddbc0b0508}"
DEVELOP_SHA='0e78c7270188ac45c1c29f927bdf90728f10215d'
REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gate919/2026-09-14_secuura-919-ks739-tier2.md"

YAML_FILE='Blockchain/Dev/docs/openapi/secuura-api.yaml'
OAI_FILE='Blockchain/Dev/services/originate/src/originate.openapi.ts'
DOC_FILE='Blockchain/Dev/services/originate/src/routes/documents.ts'
TEST_FILE='Blockchain/Dev/services/originate/src/__tests__/ks739-transfer-custody-lookup-4xx-mapping.test.ts'
BASELINE_FILE='Blockchain/Dev/scripts/audit/audit-baseline.json'
LOCK_FILE='Blockchain/Dev/package-lock.json'

YAML_HEAD_BLOB='8c3df719459a21ecd119aea8ca125130289f7e92'
OAI_HEAD_BLOB='509f13abb2910ea51fe1d0093d6268caf579f750'
DOC_HEAD_BLOB='a18a8ac57ac36387101fa404b990be58f1d77878'
TEST_HEAD_BLOB='1b0eb5dd81839dd6e402ff4e6fa87b0b24877885'
BASELINE_OK_BLOB='03d1680e3c7a87f8df70e71082b67775536acde5'

[ -d "$QA_DIR" ]         || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]          || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ]    || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]           || { echo "repo under test missing: $REPO" >&2; exit 5; }

# The head must still be at its branch on origin — the verdict is per this SHA.
LSR="$(git -C "$REPO" ls-remote origin "$BRANCH")"
if ! printf '%s\n' "$LSR" | grep -q "^${HEAD_SHA}[[:space:]]${BRANCH}\$"; then
  echo "REFUSING: $HEAD_SHA is not at $BRANCH on origin — the head moved; the brief is about a different SHA" >&2
  printf '%s\n' "$LSR" >&2
  exit 6
fi

# The compare: develop...head must read merge_base = develop itself (the head already carries the merge-in),
# ahead_by >= 1, exactly 4 files.
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
CMP_WANT="mb=$DEVELOP_SHA ahead=2 files=4"
[ "$CMP_READ" = "$CMP_WANT" ] || { echo "REFUSING: the compare does not read as the brief pins it: got '$CMP_READ', brief pins '$CMP_WANT'" >&2; exit 10; }

# The develop pin, judged by CONTENT (DEV_CONTENT_ALLOWED style, per gate912r2): a develop move that lands one
# of #919's own files at the HEAD's own blob means the PR already merged (exit 19, moot); a develop move under
# one of the six guarded paths to any OTHER blob is GUARDED (exit 18); a disjoint move proceeds (rc 0).
CUR_DEV="$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)"
[ -n "$CUR_DEV" ] || { echo "REFUSING: could not read origin develop (git ls-remote)" >&2; exit 18; }
if [ "$CUR_DEV" = "$DEVELOP_SHA" ]; then
  DEV_NOTE="origin develop still $DEVELOP_SHA (M38, git ls-remote)"
else
  DEV_JUDGEMENT="$(
    set -a; . "$SECUURA_ENV"; set +a
    DEVELOP_SHA="$DEVELOP_SHA" CUR_DEV="$CUR_DEV" \
    YAML_FILE="$YAML_FILE" OAI_FILE="$OAI_FILE" DOC_FILE="$DOC_FILE" TEST_FILE="$TEST_FILE" BASELINE_FILE="$BASELINE_FILE" LOCK_FILE="$LOCK_FILE" \
    YAML_HEAD_BLOB="$YAML_HEAD_BLOB" OAI_HEAD_BLOB="$OAI_HEAD_BLOB" DOC_HEAD_BLOB="$DOC_HEAD_BLOB" TEST_HEAD_BLOB="$TEST_HEAD_BLOB" BASELINE_OK_BLOB="$BASELINE_OK_BLOB" \
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
GUARDED = [os.environ["YAML_FILE"], os.environ["OAI_FILE"], os.environ["DOC_FILE"], os.environ["TEST_FILE"], os.environ["BASELINE_FILE"], os.environ["LOCK_FILE"]]
LANDED_OK = {os.environ["YAML_FILE"]: os.environ["YAML_HEAD_BLOB"], os.environ["OAI_FILE"]: os.environ["OAI_HEAD_BLOB"],
             os.environ["DOC_FILE"]: os.environ["DOC_HEAD_BLOB"], os.environ["TEST_FILE"]: os.environ["TEST_HEAD_BLOB"]}
by_name = {f["filename"]: f for f in files}
hits = sorted({f["filename"] for f in files if f["filename"] in GUARDED})
if not hits:
    shell = sum(1 for x in files if x["filename"].endswith(".test.sh"))
    print("DISJOINT commits=%d files=%d" % (c["ahead_by"], len(files))); sys.exit(0)
landed = sorted(h for h in hits if h in LANDED_OK and by_name[h].get("sha") == LANDED_OK[h])
guarded_remaining = sorted(h for h in hits if h not in landed)
if guarded_remaining:
    print("GUARDED " + " ".join(guarded_remaining)); sys.exit(0)
print("LANDED919 " + ",".join(landed) + " now at the head's own blob(s) — #919 has already merged into develop"); sys.exit(0)
PYJ
  )"
  case "$DEV_JUDGEMENT" in
    DISJOINT*) DEV_NOTE="origin develop MOVED $DEVELOP_SHA -> $CUR_DEV: ${DEV_JUDGEMENT#DISJOINT } — disjoint from the six guarded paths (the four PR files, the audit baseline, the root lockfile); the gate merges the then-current develop under the head in its OWN clone, re-states the delta by name and re-derives every count (brief items 1-8)" ;;
    LANDED919*) echo "REFUSING: ${DEV_JUDGEMENT#LANDED919 } — this PR is no longer open work; rewrite the brief" >&2; exit 19 ;;
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

[ -z "${QA919_BRIEF:-}${QA919_PROMPT:-}${QA919_HEAD:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$DEV_NOTE" >&2
# A launch needs a terminal: this execs an interactive agent. Inside a Bash tool there is no TTY and the gate
# would run headless, invisible and parented to the caller's shell (2026-09-13 ledger). --check never reaches this.
[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — launch this from a pane (cockpit.sh add), never from inside a Bash tool" >&2; exit 21; }
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
