#!/bin/bash
# launch_qa_secuura_ks1073_1005.sh — cross-project QA agent, ONE TIER 1 ROUND 1 gate over Secuura/Blockchain PR #1005
# (KS-1073, Seat A) @ e5e7ff99dbc4881784ce0beacefb4e7e36c55cf9 — ONE commit on dd66863dd, 2 files under services/api-gateway:
# routes/verification.ts +15 -12 (ONE product line: the statusless on-chain carve-out made tier-1 only via the doc-level
# `_source !== 'anchor_store'` conjunct; the rest comment) and a new 3-cell test file. TIER 1: a product change on the
# verification path — the predicate that decides what a verifier is told is on-chain.
#
# THE SHAPE, as read 00:05-00:14 AEST 2026-09-17 (git + the compare API agree): the head's parent is dd66863dd (#1002's squash),
# and develop is 40fe4db69 (#1004's squash, a child of dd66863dd touching packages/shared only). compare develop...head =
# merge_base dd66863dd, status diverged, ahead 1, behind 1, files 2. The compare is asserted as merge_base + ahead + files
# (exit 10); `behind` is deliberately NOT asserted, so a develop that moves on does not trip this guard — the develop arm judges
# the move by CONTENT.
#
# The develop pin is judged by CONTENT, not bare: (a) EIGHT files by blob at the CURRENT develop — verification.ts (base
# c83a2ae27; the PR's own de34b2de7 -> exit 19 LANDED), api-gateway src/index.ts / vitest.config.ts / package.json /
# tsconfig.json, the ks1057 verify-confidence test, originate routes/documents.ts (the tier-1 document body), anchoring
# src/index.ts (formatAnchorResponse) — any blob nobody pinned -> exit 18 (the new test file is NOT judged: it is absent on
# develop, and verification.ts already detects a landing); (b) if develop moved past 40fe4db69, the compare pinned...develop
# REFUSES (exit 18) only when the delta touches a GUARDED path — services/api-gateway/src/routes/, api-gateway src/index.ts,
# the api-gateway config trio, the ks1057 test, originate routes/documents.ts, anchoring src/index.ts, eslint.config.mjs, or
# the Dev lockfile — or cannot be judged; anything else (#923's ks570 test, #995's utils/trustHeaders.ts, packages/shared)
# proceeds and the gate re-derives counts on the merged tree.
# DEV_CONTENT_ALLOWED is empty: no open lane PR touches a guarded path except dependabot #649/#575 (api-gateway package.json)
# — if one lands, this launcher refuses and the brief is re-pinned deliberately.
#
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool. `--check` still runs headless (it launches nothing).
#
# Adapted from launch_qa_secuura_ks932_1004.sh by gen_launcher_1005.py (asserted substitutions + residual guard + output
# controls + bash -n): same guards and exit codes, re-pointed at #1005. Exit codes 2..21 (19 = LANDED).
# Written by the generator because it contains a legitimate directory change.
#
# Usage: launch_qa_secuura_ks1073_1005.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..21 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QA1005_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1005-ks1073-tier1.md}"
PROMPT_FILE="${QA1005_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1005-ks1073-tier1.prompt.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
BRANCH='refs/heads/feature/ks-1073-ornith-tier2-statusless-carveout'
HEAD_SHA="${QA1005_HEAD:-e5e7ff99dbc4881784ce0beacefb4e7e36c55cf9}"
MERGE_BASE='dd66863dd2858e97344652c1106d38f5e352a41b'   # the merge-base of the head with develop = the PR base (#1002's squash; develop moved on to #1004)
DEVELOP_SHA='40fe4db6963cd11dba06bd46e0b00af39e68ef3a'   # develop at draft time = #1004's squash, a child of the base, packages/shared only (read 00:05:37 and 00:07:38 AEST)
REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1005-ks1073-tier1.md"

[ -d "$QA_DIR" ]         || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]          || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ]    || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]           || { echo "repo under test missing: $REPO" >&2; exit 5; }

# The head, pinned at its branch on origin (one ls-remote at run time).
LSR="$(git -C "$REPO" ls-remote origin "$BRANCH")"
if ! printf '%s\n' "$LSR" | grep -q "^${HEAD_SHA}[[:space:]]${BRANCH}\$"; then
  echo "REFUSING: #1005 — $HEAD_SHA is not at $BRANCH on origin — the head moved; the brief is about a different SHA" >&2
  printf '%s\n' "$LSR" >&2
  exit 6
fi

# The compare (GitHub compare API), asserted whole (merge_base + ahead + files; NOT behind — see the header):
# develop...#1005 = dd66863dd ahead 1 files 2 (behind 1 — #1004 — deliberately not asserted).
COMPARE="$(
  set -a; . "$SECUURA_ENV"; set +a
  HEAD_SHA="$HEAD_SHA" python3 - <<'PY'
import json, os, urllib.request
t = os.environ.get("GH_TOKEN", "")
api = "https://api.github.com/repos/Secuura/Distributed_Secuura/compare/"
r = urllib.request.urlopen(urllib.request.Request(api + "develop..." + os.environ["HEAD_SHA"], headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}), timeout=60)
c = json.load(r)
print("%s ahead=%d files=%d" % (c["merge_base_commit"]["sha"], c["ahead_by"], len(c.get("files") or [])))
PY
)"
[ -n "$COMPARE" ] || { echo "REFUSING: could not read the compare develop...head from the GitHub compare API" >&2; exit 13; }
[ "$COMPARE" = "$MERGE_BASE ahead=1 files=2" ] || { echo "REFUSING: #1005 develop...head reads '$COMPARE', brief pins '$MERGE_BASE ahead=1 files=2'" >&2; exit 10; }

# The develop pin, judged by CONTENT (see the header): eight files by blob at the CURRENT develop, then — if develop
# moved — the pinned...develop delta against the GUARDED list with the DEV_CONTENT_ALLOWED blobs cleared.
CUR_DEV="$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)"
[ -n "$CUR_DEV" ] || { echo "REFUSING: could not read origin develop (git ls-remote)" >&2; exit 18; }
DEV_JUDGEMENT="$(
  set -a; . "$SECUURA_ENV"; set +a
  DEVELOP_SHA="$DEVELOP_SHA" CUR_DEV="$CUR_DEV" python3 - <<'PYJ'
import json, os, sys, urllib.request
t = os.environ.get("GH_TOKEN", "")
api = "https://api.github.com/repos/Secuura/Distributed_Secuura"
def get(p):
    return json.load(urllib.request.urlopen(urllib.request.Request(api + p, headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}), timeout=60))
cur = os.environ["CUR_DEV"]; pinned = os.environ["DEVELOP_SHA"]
D = "Blockchain/Dev/"
# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label})
JUDGED = {
  D + "services/api-gateway/src/routes/verification.ts":                                      ({"c83a2ae27d7ef03a3c1b0c02246154894064f372": "base"}, {"de34b2de7372873d60987f8bc742df3a13140265": "#1005 own"}),
  D + "services/api-gateway/src/index.ts":                                                   ({"6f38c819e48162e3179aaf557085766f91beecc1": "base"}, {}),
  D + "services/api-gateway/vitest.config.ts":                                               ({"5888e0b320d934f6f434e0e5ca3c74a995cecc02": "base"}, {}),
  D + "services/api-gateway/package.json":                                                   ({"841d8c6adcd71e885c01e65c22da9418daff276a": "base"}, {}),
  D + "services/api-gateway/tsconfig.json":                                                  ({"c981e6a92fdd2417fa35070eb979c5f1c77ffbcd": "base"}, {}),
  D + "services/api-gateway/src/__tests__/ks1057-verify-confidence-is-status-aware.test.ts": ({"aceaef1fa4fc33e8daa42f0b799e554eb4762770": "base"}, {}),
  D + "services/originate/src/routes/documents.ts":                                           ({"c3a818ac8ac8de1b385540d15e3fbb23200cea30": "base"}, {}),
  D + "services/anchoring/src/index.ts":                                                      ({"da4abd43292186da45c1533017fe042fa512bd43": "base"}, {}),
}
state = []
for f, (ok, landed) in JUDGED.items():
    try:
        blob = get("/contents/" + f + "?ref=" + cur)["sha"]
    except Exception as e:
        print("UNJUDGEABLE develop blob unreadable for " + f.split("/")[-1] + ": " + type(e).__name__); sys.exit(0)
    short = f.replace(D, "")
    if blob in landed:
        print("LANDED develop " + short + " blob " + blob[:9] + " = " + landed[blob] + " — #1005 has landed; this brief is stale"); sys.exit(0)
    if blob not in ok:
        print("GUARDED develop " + short + " blob " + blob[:9] + " — a version nobody pinned"); sys.exit(0)
    state.append(f.split("/")[-1] + " " + blob[:9] + " = " + ok[blob])
state = "; ".join(state)
if cur == pinned:
    print("OK " + state + " | origin develop still " + pinned + " (#1004 squash on the base, file-disjoint from #1005; git ls-remote)"); sys.exit(0)
try:
    c = get("/compare/" + pinned + "..." + cur)
except Exception as e:
    print("UNJUDGEABLE compare unreadable: " + type(e).__name__); sys.exit(0)
files = c.get("files") or []
if c.get("status") != "ahead" or len(files) > 250:
    print("UNJUDGEABLE status=%s files=%d" % (c.get("status"), len(files))); sys.exit(0)
GUARDED = [D + "services/api-gateway/src/routes/",
           D + "services/api-gateway/src/index.ts",
           D + "services/api-gateway/vitest.config.ts",
           D + "services/api-gateway/package.json",
           D + "services/api-gateway/tsconfig.json",
           D + "services/api-gateway/src/__tests__/ks1057-verify-confidence-is-status-aware.test.ts",
           D + "services/originate/src/routes/documents.ts",
           D + "services/anchoring/src/index.ts",
           D + "eslint.config.mjs",
           D + "package-lock.json"]
# STYLE NOTE (912r2 launcher, measured): bash scans quote/paren state THROUGH this heredoc because it sits inside a
# command substitution — keep apostrophes and parentheses EVEN (this block uses none of the former), or the outer $( ) breaks.
# CONTENT-JUDGED allowlist: a hit under a GUARDED path clears ONLY if the per-file blob sha in the compare is EXACTLY one
# pinned here. EMPTY for this gate: at draft time 00:07 AEST no open lane PR touched a guarded path except dependabot
# api-gateway package.json bumps, which must NOT clear silently, so every guarded hit falls through to GUARDED and exit 18 — re-pin deliberately.
DEV_CONTENT_ALLOWED = {
}
hits = sorted({x["filename"] for x in files for g in GUARDED if x["filename"] == g or (g.endswith("/") and x["filename"].startswith(g))})
by_name = {x["filename"]: x for x in files}
cleared = sorted(h for h in hits if h in DEV_CONTENT_ALLOWED and by_name.get(h, {}).get("sha") == DEV_CONTENT_ALLOWED[h])
remaining = sorted(h for h in hits if h not in cleared)
if remaining:
    print("GUARDED " + " ".join(remaining)); sys.exit(0)
tail = "the gate merges the then-current develop onto e5e7ff99d in its own clone, rebuilds the shared dist there, runs the api-gateway suite on the MERGED tree beside the base and head trees, names the delta and re-derives every count (brief item 6)"
if cleared:
    print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d, cleared BY BLOB under guarded paths: %s — %s" % (pinned, cur, c["ahead_by"], len(files), ",".join(x.split("/")[-1] for x in cleared), tail)); sys.exit(0)
print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d — disjoint from the GUARDED list (api-gateway src/routes/, api-gateway src/index.ts + config trio, the ks1057 test, originate routes/documents.ts, anchoring src/index.ts, eslint.config.mjs, the lockfile); %s" % (pinned, cur, c["ahead_by"], len(files), tail)); sys.exit(0)
PYJ
)"
case "$DEV_JUDGEMENT" in
  OK*) DEV_NOTE="${DEV_JUDGEMENT#OK }" ;;
  LANDED*) echo "REFUSING: ${DEV_JUDGEMENT#LANDED } (develop $CUR_DEV) — re-pin deliberately: a different brief" >&2; exit 19 ;;
  *) echo "REFUSING: origin develop is at $CUR_DEV (pinned $DEVELOP_SHA) and the move is not provably disjoint: ${DEV_JUDGEMENT:-no judgement} — confirm the delta, then re-pin deliberately (launcher DEVELOP_SHA / JUDGED blobs / DEV_CONTENT_ALLOWED + brief TARGET + prompt)" >&2
     exit 18 ;;
esac
grep -q 'TIER 1' "$BRIEF" && grep -q 'TIER 1' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the tier" >&2; exit 7; }
grep -q 'ROUND 1' "$BRIEF" && grep -q 'ROUND 1' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the round (ROUND 1)" >&2; exit 15; }
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
  echo "  head on origin: #1005 $HEAD_SHA at $BRANCH"
  echo "  compare (GitHub API): develop...#1005 = $COMPARE"
  echo "  $DEV_NOTE"
  echo "  brief, prompt, QA project and repo all present"
  echo "  brief and prompt agree on TIER 1 and ROUND 1"
  echo "  prompt opens with the thinking directive and names the brief"
  echo "  brief and prompt both name the head SHA"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"
  exit 0
fi

[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — this launcher execs an interactive agent; run it in a cockpit pane, never inside a Bash tool (a headless gate is invisible and dies with the caller's shell)" >&2; exit 21; }
[ -z "${QA1005_BRIEF:-}${QA1005_PROMPT:-}${QA1005_HEAD:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$DEV_NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
