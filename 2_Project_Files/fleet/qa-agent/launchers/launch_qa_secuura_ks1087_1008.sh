#!/bin/bash
# launch_qa_secuura_ks1087_1008.sh — cross-project QA agent, ONE TIER 1 ROUND 1 gate over Secuura/Blockchain PR #1008
# (KS-1087 item 1, Seat A) @ dd7086d5aa574285beffc515f9371a438621f25d — ONE commit on develop 93629700c, 2 files, both
# services/api-gateway: routes/verification.ts +9 -1 (POST /api/workflow-instances/:id/approve awaits the forward status: non-2xx or a
# transport error answers 502 ORIGINATE_FORWARD_FAILED and keeps the pending document; only a 2xx deletes it) and a new 3-cell
# ks1087 test. TIER 1: a new 502 on an authenticated route mounted in every environment, deciding whether a document is DELETED.
#
# THE SHAPE, as read 00:55-01:06 AEST 2026-09-17 (git + the compare API agree): develop 93629700c is an ANCESTOR of the head
# (merge-base = develop, behind 0), so the merged tree IS the head tree. compare develop...head = merge_base 93629700c, status ahead,
# ahead 1, behind 0, files 2. The compare is asserted as merge_base + ahead + files (exit 10); `behind` is deliberately NOT asserted,
# so a develop that moves on does not trip this guard — the develop arm judges the move by CONTENT.
#
# The develop pin is judged by CONTENT, not bare: (a) ELEVEN files by blob at the CURRENT develop — verification.ts (base
# de34b2de7; the PR's own d0585dc34 -> exit 19 LANDED) and ten files the gate's predictions stand on: api-gateway src/index.ts (the
# unconditional mount), src/middleware/auth.ts (authenticateToken), src/services/redis.ts (the pending-document TTL),
# src/services/enforcement.ts (who writes the pending document), package.json, vitest.config.ts, vitest.setup.ts, tsconfig.json
# (the exclude the including tsc overrides), originate src/routes/documents.ts (the forward target) and Dev eslint.config.mjs —
# any blob nobody pinned -> exit 18 (the new ks1087 test is NOT judged: it is absent on develop, and verification.ts already
# detects a landing); (b) if develop moved past 93629700c, the compare pinned...develop REFUSES (exit 18) only when the delta touches
# a GUARDED path — those eleven files, the ks1087 test, docs/openapi/, the Dev lockfile, issuer DocumentList.tsx, mcp-server
# api-client.ts — or cannot be judged; anything else (the file-disjoint sibling lane PRs landing) proceeds and the gate re-derives
# the api-gateway denominator on the merged tree.
# DEV_CONTENT_ALLOWED is empty: dependabot #649/#575 touch api-gateway package.json and the Dev lockfile — if one lands, this
# launcher refuses and the brief is re-pinned deliberately.
#
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool. `--check` still runs headless (it launches nothing).
#
# Adapted from launch_qa_secuura_ks844_1006.sh by gen_launcher_1008.py (asserted substitutions + residual guard + output
# controls + bash -n): same guards and exit codes, re-pointed at #1008. Exit codes 2..21 (19 = LANDED).
# Written by the generator because it contains a legitimate directory change.
#
# Usage: launch_qa_secuura_ks1087_1008.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..21 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QA1008_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1008-ks1087-tier1.md}"
PROMPT_FILE="${QA1008_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1008-ks1087-tier1.prompt.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
BRANCH='refs/heads/feature/ks-1087-ornith-workflow-approve-keeps-pending'
HEAD_SHA="${QA1008_HEAD:-dd7086d5aa574285beffc515f9371a438621f25d}"
MERGE_BASE='93629700c3d219c1d8ca61d69150bb9b623fc1be'   # the merge-base of the head with develop = develop itself (develop is an ancestor of the head; behind 0)
DEVELOP_SHA='93629700c3d219c1d8ca61d69150bb9b623fc1be'   # develop at draft time = the PR base (git ls-remote 00:55:40, branches API 00:57:25 AEST)
REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1008-ks1087-tier1.md"

[ -d "$QA_DIR" ]         || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]          || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ]    || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]           || { echo "repo under test missing: $REPO" >&2; exit 5; }

# The head, pinned at its branch on origin (one ls-remote at run time).
LSR="$(git -C "$REPO" ls-remote origin "$BRANCH")"
if ! printf '%s\n' "$LSR" | grep -q "^${HEAD_SHA}[[:space:]]${BRANCH}\$"; then
  echo "REFUSING: #1008 — $HEAD_SHA is not at $BRANCH on origin — the head moved; the brief is about a different SHA" >&2
  printf '%s\n' "$LSR" >&2
  exit 6
fi

# The compare (GitHub compare API), asserted whole (merge_base + ahead + files; NOT behind — see the header):
# develop...#1008 = 93629700c ahead 1 files 2 (behind 0; behind deliberately not asserted).
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
[ "$COMPARE" = "$MERGE_BASE ahead=1 files=2" ] || { echo "REFUSING: #1008 develop...head reads '$COMPARE', brief pins '$MERGE_BASE ahead=1 files=2'" >&2; exit 10; }

# The develop pin, judged by CONTENT (see the header): eleven files by blob at the CURRENT develop, then — if develop
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
  D + "services/api-gateway/src/routes/verification.ts":           ({"de34b2de7372873d60987f8bc742df3a13140265": "base"}, {"d0585dc34ceb5e3580ade38633250a6ffeaebd69": "#1008 own"}),
  D + "services/api-gateway/src/index.ts":                         ({"6f38c819e48162e3179aaf557085766f91beecc1": "base"}, {}),
  D + "services/api-gateway/src/middleware/auth.ts":               ({"20311010db0eb8ba097644ce105cf8df966ce456": "base"}, {}),
  D + "services/api-gateway/src/services/redis.ts":                ({"47659ee9c9f06acf9ac64e09b2dc207113ba92ea": "base"}, {}),
  D + "services/api-gateway/src/services/enforcement.ts":          ({"533cd309c56b8167ebe00b620744259b3cc186cc": "base"}, {}),
  D + "services/api-gateway/package.json":                         ({"841d8c6adcd71e885c01e65c22da9418daff276a": "base"}, {}),
  D + "services/api-gateway/vitest.config.ts":                     ({"5888e0b320d934f6f434e0e5ca3c74a995cecc02": "base"}, {}),
  D + "services/api-gateway/vitest.setup.ts":                      ({"22c1107683b8192df3bfd3e929aa94aff3dc7d45": "base"}, {}),
  D + "services/api-gateway/tsconfig.json":                        ({"c981e6a92fdd2417fa35070eb979c5f1c77ffbcd": "base"}, {}),
  D + "services/originate/src/routes/documents.ts":                ({"c3a818ac8ac8de1b385540d15e3fbb23200cea30": "base"}, {}),
  D + "eslint.config.mjs":                                          ({"8c5374c6022eb0a3f449f41a570db61294aa63f1": "base"}, {}),
}
state = []
for f, (ok, landed) in JUDGED.items():
    try:
        blob = get("/contents/" + f + "?ref=" + cur)["sha"]
    except Exception as e:
        print("UNJUDGEABLE develop blob unreadable for " + f.split("/")[-1] + ": " + type(e).__name__); sys.exit(0)
    short = f.replace(D, "")
    if blob in landed:
        print("LANDED develop " + short + " blob " + blob[:9] + " = " + landed[blob] + " — #1008 has landed; this brief is stale"); sys.exit(0)
    if blob not in ok:
        print("GUARDED develop " + short + " blob " + blob[:9] + " — a version nobody pinned"); sys.exit(0)
    state.append(f.split("/")[-1] + " " + blob[:9] + " = " + ok[blob])
state = "; ".join(state)
if cur == pinned:
    print("OK " + state + " | origin develop still " + pinned + " (the PR base, an ancestor of the head: merged tree = head tree; git ls-remote)"); sys.exit(0)
try:
    c = get("/compare/" + pinned + "..." + cur)
except Exception as e:
    print("UNJUDGEABLE compare unreadable: " + type(e).__name__); sys.exit(0)
files = c.get("files") or []
if c.get("status") != "ahead" or len(files) > 250:
    print("UNJUDGEABLE status=%s files=%d" % (c.get("status"), len(files))); sys.exit(0)
GUARDED = [D + "services/api-gateway/src/routes/verification.ts",
           D + "services/api-gateway/src/__tests__/ks1087-workflow-approve-deletes-the-pending-document.test.ts",
           D + "services/api-gateway/src/index.ts",
           D + "services/api-gateway/src/middleware/auth.ts",
           D + "services/api-gateway/src/services/redis.ts",
           D + "services/api-gateway/src/services/enforcement.ts",
           D + "services/api-gateway/package.json",
           D + "services/api-gateway/vitest.config.ts",
           D + "services/api-gateway/vitest.setup.ts",
           D + "services/api-gateway/tsconfig.json",
           D + "services/originate/src/routes/documents.ts",
           D + "docs/openapi/",
           D + "eslint.config.mjs",
           D + "frontend/issuer/src/components/DocumentList.tsx",
           D + "services/mcp-server/src/api-client.ts",
           D + "package-lock.json"]
# SUFFIX-GUARDED: none for this gate — every guarded path above is exact or a directory prefix.
GUARDED_SUFFIX = []
# STYLE NOTE (912r2 launcher, measured): bash scans quote/paren state THROUGH this heredoc because it sits inside a
# command substitution — keep apostrophes and parentheses EVEN (this block uses none of the former), or the outer $( ) breaks.
# CONTENT-JUDGED allowlist: a hit under a GUARDED path clears ONLY if the per-file blob sha in the compare is EXACTLY one
# pinned here. EMPTY for this gate: at draft time 00:57 AEST no open lane PR touched a guarded path except dependabot
# bumps of api-gateway package.json and the Dev lockfile, which must NOT clear silently, so every guarded hit falls through to GUARDED and exit 18 — re-pin deliberately.
DEV_CONTENT_ALLOWED = {
}
hits = sorted({x["filename"] for x in files for g in GUARDED if x["filename"] == g or (g.endswith("/") and x["filename"].startswith(g))} | {x["filename"] for x in files for g in GUARDED_SUFFIX if x["filename"].endswith(g)})
by_name = {x["filename"]: x for x in files}
cleared = sorted(h for h in hits if h in DEV_CONTENT_ALLOWED and by_name.get(h, {}).get("sha") == DEV_CONTENT_ALLOWED[h])
remaining = sorted(h for h in hits if h not in cleared)
if remaining:
    print("GUARDED " + " ".join(remaining)); sys.exit(0)
tail = "the gate merges the then-current develop onto dd7086d5a in its own clone, rebuilds the shared dist there, runs the api-gateway suite on the MERGED tree beside the base and head trees, names the delta and re-derives every count, above all the api-gateway denominator (brief items 8 and 11)"
if cleared:
    print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d, cleared BY BLOB under guarded paths: %s — %s" % (pinned, cur, c["ahead_by"], len(files), ",".join(x.split("/")[-1] for x in cleared), tail)); sys.exit(0)
print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d — disjoint from the GUARDED list (api-gateway verification.ts + the ks1087 test + index.ts + auth.ts + redis.ts + enforcement.ts + package.json + vitest config/setup + tsconfig, originate routes/documents.ts, docs/openapi/, eslint.config.mjs, the two route consumers, the Dev lockfile); %s" % (pinned, cur, c["ahead_by"], len(files), tail)); sys.exit(0)
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
  echo "  head on origin: #1008 $HEAD_SHA at $BRANCH"
  echo "  compare (GitHub API): develop...#1008 = $COMPARE"
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
[ -z "${QA1008_BRIEF:-}${QA1008_PROMPT:-}${QA1008_HEAD:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$DEV_NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
