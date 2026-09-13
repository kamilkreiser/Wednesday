#!/bin/bash
# launch_qa_secuura_ks828_900_981.sh — cross-project QA agent, TIER 2 (through code) gate ROUND 1 on
# Secuura PR #981 (KS-828 / KS-900) @ 04807ea0e: packages/shared `ks781-p3-3-body-parser-order.test.ts` — LEG F's
# declaration becomes `{ routes, guarded }` per router module and `guarded` is DERIVED from the wrapper body (a
# guard-bound local invoked there, an inline factory call, or a guarded wrapper; fixed point), so the control-byte
# guard LEAVING a KS-815 wrapper now reds LEG F (KS-828; W1-W5); `addExport` records a factory exported only as
# `default` under its LOCAL name (KS-900; J1 red-first, J2 structural pin, the former CONTROL reshaped). Test-file
# only, +239 -26 over the STACK PARENT; no product file moves. Round 1 on this PR.
#
# THE STACKED SHAPE. #981 is STACKED on #975 (KS-1126): its ONE commit's parent is 8da20edbd = #975's head, on the
# SAME file (#975's six hunks at :1992-2035 of the parent, #981's twenty hunks from :2187 — measured, no overlap).
# The gate judges ONLY #981's own delta, so the base-for-judgement is the STACK PARENT 8da20edbd, not develop and
# not the PR's merge-base with develop (0f69129b3). The "merge-base" pin of the template is therefore the
# STACK-PARENT pin here: the GitHub compare 8da20edbd...04807ea0e must read merge_base 8da20edbd, ahead 1, ONE
# file (exit 10). The merge seat is queued to squash #975 onto develop next; when that lands, develop's copy of
# the one file CHANGES — that is EXPECTED, not a hit — so the develop guard judges a move by CONTENT, not by file
# name: develop's blob of the file (GitHub contents API) == 6beacc935 (the pre-#975 copy, = develop's at
# e91eb5bda and at 0f69129b3) -> unchanged; == ad0afd7cb (the blob at 8da20edbd) -> #975 has landed, green, the
# note says so and the gate's full-package expectation is unchanged (794/794 — the head carries #975 either way);
# == 9bcdb4259 (#981's own blob) -> exit 19, the PR has landed and there is nothing to gate; any other blob ->
# exit 18, a third version nobody pinned. Any OTHER file of the move under packages/shared/, or admin.ts /
# proxy.ts / api-gateway's index.ts (the product files LEG F and the ratio read) -> exit 18; otherwise the launcher
# proceeds and prints the move with the services-corpus delta (LEG C-F read that corpus; the gate re-runs the full
# package on the merged tree, brief item 7). If #975 merges before the gate finishes, the PR's GitHub delta shrinks
# to the one commit; the verdict is on head 04807ea0e regardless, and the brief says so.
#
# origin develop at pin time: e91eb5bda (M10, #972's squash, 17:37:11 AEST 2026-09-13) — four squashes past
# 0f69129b3 (#969 api-gateway verification.ts + two tests; #970 auth userRepo + a test; #971 two .sh; #972 auth
# routes/repo/gate + tests), none under packages/shared/, none touching admin.ts / proxy.ts / index.ts; the two
# parser tokens they add sit in __tests__ files, which ks781's tsFilesUnder SKIP_DIRS excludes.
#
# Adapted from launch_qa_secuura_ks885_886_978.sh by gen_launcher_981.py (asserted substitutions, TWO asserted
# block replacements — the stack-parent guard and the blob-judged develop guard — residual guard): the same guards
# and exit codes plus 19, re-pointed at #981.
#
# Written by the generator because it contains a legitimate `cd`.
#
# Usage: launch_qa_secuura_ks828_900_981.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..19 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QA981_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-13_secuura-981-ks828-900-tier2.md}"
PROMPT_FILE="${QA981_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-13_secuura-981-ks828-900-tier2.prompt.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
BRANCH='refs/heads/feature/ks-828-ks-900-leg-f-guarded-wrappers-and-default-only-factory'
HEAD_SHA="${QA981_HEAD:-04807ea0eb5e551ab22245d38c499af32724c8fd}"
STACK_PARENT='8da20edbd595f97cd3c62baaa4ff7b56ea9eef99'
DEVELOP_SHA='e91eb5bdaf68461e43a6055ed39137bd60a36749'
JUDGED_FILE='Blockchain/Dev/packages/shared/src/__tests__/ks781-p3-3-body-parser-order.test.ts'
BLOB_PRE975='6beacc935fe84d618a6c51854934a8fbe6306773'
BLOB_975='ad0afd7cbb9bfd1b0e44db3913863b5bb95f2d9a'
BLOB_HEAD='9bcdb42593925603bdbc617cd13b0f91c863bc9c'
REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-13_secuura-981-ks828-900-tier2.md"

[ -d "$QA_DIR" ]         || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]          || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ]    || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]           || { echo "repo under test missing: $REPO" >&2; exit 5; }

if ! git -C "$REPO" ls-remote origin "$BRANCH" | grep -q "^${HEAD_SHA}[[:space:]]"; then
  echo "REFUSING: $HEAD_SHA is not at $BRANCH on origin — the head moved; the brief is about a different SHA" >&2
  git -C "$REPO" ls-remote origin "$BRANCH" >&2
  exit 6
fi

# The STACK-PARENT pin: the judged delta is STACK_PARENT...HEAD and must be exactly ONE commit on ONE file.
STACK_READ="$(
  set -a; . "$SECUURA_ENV"; set +a
  HEAD_SHA="$HEAD_SHA" STACK_PARENT="$STACK_PARENT" python3 - <<'PY'
import json, os, urllib.request
t = os.environ.get("GH_TOKEN", "")
u = "https://api.github.com/repos/Secuura/Distributed_Secuura/compare/" + os.environ["STACK_PARENT"] + "..." + os.environ["HEAD_SHA"]
r = urllib.request.urlopen(urllib.request.Request(u, headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}), timeout=60)
c = json.load(r)
print("%s ahead=%d files=%d" % (c["merge_base_commit"]["sha"], c["ahead_by"], len(c.get("files") or [])))
PY
)"
[ -n "$STACK_READ" ] || { echo "REFUSING: could not read the stack-parent compare from the GitHub compare API" >&2; exit 13; }
[ "$STACK_READ" = "$STACK_PARENT ahead=1 files=1" ] \
  || { echo "REFUSING: the judged delta is not ONE commit on ONE file over the stack parent: compare reads '$STACK_READ', brief pins '$STACK_PARENT ahead=1 files=1'" >&2; exit 10; }

# The develop pin, judged by CONTENT (see the header). The one file is judged by its blob SHA on develop;
# GUARDED = the OTHER files whose movement changes this brief's expectations.
CUR_DEV="$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)"
[ -n "$CUR_DEV" ] || { echo "REFUSING: could not read origin develop (git ls-remote)" >&2; exit 18; }
DEV_JUDGEMENT="$(
  set -a; . "$SECUURA_ENV"; set +a
  DEVELOP_SHA="$DEVELOP_SHA" CUR_DEV="$CUR_DEV" JUDGED_FILE="$JUDGED_FILE" \
  BLOB_PRE975="$BLOB_PRE975" BLOB_975="$BLOB_975" BLOB_HEAD="$BLOB_HEAD" python3 - <<'PYJ'
import json, os, sys, urllib.request
t = os.environ.get("GH_TOKEN", "")
api = "https://api.github.com/repos/Secuura/Distributed_Secuura"
def get(p):
    return json.load(urllib.request.urlopen(urllib.request.Request(api + p, headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}), timeout=60))
f = os.environ["JUDGED_FILE"]; cur = os.environ["CUR_DEV"]; pinned = os.environ["DEVELOP_SHA"]
try:
    blob = get("/contents/" + f + "?ref=" + cur)["sha"]
except Exception as e:
    print("UNJUDGEABLE develop blob unreadable: " + type(e).__name__); sys.exit(0)
if blob == os.environ["BLOB_PRE975"]:
    state = "develop's ks781 blob " + blob[:9] + " = the pre-#975 copy (#975 NOT landed; full-package expectation on the merged tree 794/794 because the head carries #975)"
elif blob == os.environ["BLOB_975"]:
    state = "develop's ks781 blob " + blob[:9] + " = #975's copy (#975 HAS LANDED on develop — EXPECTED, green; the PR's GitHub delta is now the one commit; the verdict stays on the head)"
elif blob == os.environ["BLOB_HEAD"]:
    print("LANDED981 develop's ks781 blob " + blob[:9] + " = #981's own — the PR has landed; nothing to gate"); sys.exit(0)
else:
    print("GUARDED develop's ks781 blob " + blob[:9] + " is a THIRD version (neither the pre-#975 copy nor #975's nor #981's)"); sys.exit(0)
if cur == pinned:
    print("OK " + state + " | origin develop still " + pinned + " (git ls-remote)"); sys.exit(0)
try:
    c = get("/compare/" + pinned + "..." + cur)
except Exception as e:
    print("UNJUDGEABLE compare unreadable: " + type(e).__name__); sys.exit(0)
files = c.get("files") or []
if c.get("status") != "ahead" or len(files) > 250:
    print("UNJUDGEABLE status=%s files=%d" % (c.get("status"), len(files))); sys.exit(0)
GUARDED = ["Blockchain/Dev/packages/shared/",
           "Blockchain/Dev/services/api-gateway/src/routes/admin.ts",
           "Blockchain/Dev/services/api-gateway/src/routes/proxy.ts",
           "Blockchain/Dev/services/api-gateway/src/index.ts"]
hits = sorted({x["filename"] for x in files if x["filename"] != f for g in GUARDED if x["filename"] == g or (g.endswith("/") and x["filename"].startswith(g))})
if hits:
    print("GUARDED " + " ".join(hits)); sys.exit(0)
SKIP = {"node_modules", "dist", "__tests__", "coverage"}
def corpus(p):
    return p.startswith("Blockchain/Dev/services/") and p.endswith(".ts") and not p.endswith(".d.ts") and not (set(p.split("/")[:-1]) & SKIP)
added = sum(1 for x in files if x["status"] == "added" and corpus(x["filename"]))
modified = sum(1 for x in files if x["status"] == "modified" and corpus(x["filename"]))
removed = sum(1 for x in files if x["status"] == "removed" and corpus(x["filename"]))
print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d corpus+%d/~%d/-%d — disjoint from the judged file (by blob), the rest of packages/shared/ and the three product files LEG F and the ratio read; LEG C-F read the services corpus, so the gate re-runs the full package on the merged tree (brief item 7)" % (pinned, cur, c["ahead_by"], len(files), added, modified, removed)); sys.exit(0)
PYJ
)"
case "$DEV_JUDGEMENT" in
  OK*) DEV_NOTE="${DEV_JUDGEMENT#OK }" ;;
  LANDED981*) echo "REFUSING: ${DEV_JUDGEMENT#LANDED981 } (develop $CUR_DEV)" >&2; exit 19 ;;
  *) echo "REFUSING: origin develop is at $CUR_DEV (pinned $DEVELOP_SHA) and the move is not provably disjoint: ${DEV_JUDGEMENT:-no judgement} — confirm the delta, re-state the ratio, then re-pin deliberately (launcher DEVELOP_SHA/BLOB_* + brief TARGET + prompt)" >&2
     exit 18 ;;
esac

grep -q 'TIER 2' "$BRIEF" && grep -q 'TIER 2' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the tier" >&2; exit 7; }
grep -q 'ROUND 1' "$BRIEF" && grep -q 'ROUND 1' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the round" >&2; exit 15; }
head -1 "$PROMPT_FILE" | grep -q 'ultrathink' || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 8; }
grep -qF "$REAL_BRIEF" "$PROMPT_FILE" || { echo "REFUSING: prompt does not name the brief path" >&2; exit 9; }
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
  echo "  stack parent still $STACK_PARENT and the judged delta is ONE commit on ONE file (GitHub compare API)"
  echo "  $DEV_NOTE"
  echo "  brief, prompt, QA project and repo all present"
  echo "  brief and prompt agree on TIER 2 and ROUND 1"
  echo "  prompt opens with the thinking directive and names the brief"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  exit 0
fi

[ -z "${QA981_BRIEF:-}${QA981_PROMPT:-}${QA981_HEAD:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$DEV_NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
