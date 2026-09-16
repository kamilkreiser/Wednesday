#!/bin/bash
# launch_qa_secuura_ks1183_1010.sh — cross-project QA agent, ONE TIER 1 ROUND 1 gate over Secuura/Blockchain PR #1010
# (KS-1183, Seat A successor) @ c3213b04e3ad96068c367f7e0ba426822d32cda9 — ONE commit on f7c2f4acb (#1008's squash), 2 files, both
# services/api-gateway: routes/verification.ts +42 -15 (the approve route's forward to originate gets proxyReq.setTimeout, default
# ORIGINATE_FORWARD_TIMEOUT_MS 15_000, optional deps.originateForwardTimeoutMs; at the bound 502 ORIGINATE_FORWARD_FAILED status 0, the
# pending document kept; proxyRes error/aborted/close settle 0) and the rebuilt ks1087 test (+241 -129). TIER 1: a new failure mode on an
# authenticated route mounted in every environment, deciding whether a pending document is DELETED.
#
# THE SHAPE, as read 03:47-03:55 AEST 2026-09-17 (git + the compare API agree): develop MOVED past the PR base before drafting —
# develop d067725ff (#1009's squash, 3 ks864 test files, file-disjoint) is NOT an ancestor of the head; compare develop...head =
# merge_base f7c2f4acb, diverged, ahead 1, behind 1, files 2. The compare is asserted as merge_base + ahead + files (exit 10); `behind`
# is deliberately NOT asserted — the develop arm judges every move by CONTENT, and the gate builds the merged tree itself.
#
# The develop pin is judged by CONTENT, not bare: (a) FIFTEEN files by blob at the CURRENT develop — verification.ts (base d0585dc34;
# the PR's own 04b3d980f -> exit 19 LANDED), the ks1087 test (base 7832724f3; the PR's own 4450587dc -> exit 19 LANDED), api-gateway
# src/index.ts (the mount, passes no override), src/middleware/auth.ts, src/services/redis.ts, src/services/enforcement.ts, package.json,
# vitest.config.ts, vitest.setup.ts, tsconfig.json, originate src/routes/documents.ts (the forward target), Dev eslint.config.mjs and the
# three nginx-gateway confs the 15 s default is measured against (nginx.conf 120 s, nginx-demo.conf 60 s, nginx-production.conf 30 s) —
# any blob nobody pinned -> exit 18; (b) if develop moved past d067725ff, the compare pinned...develop REFUSES (exit 18) when the delta
# touches a GUARDED path — those files, docs/openapi/, docker/nginx-gateway/, deployment/caddy/, any */nginx.conf, the Dev lockfile, issuer
# DocumentList.tsx, mcp-server api-client.ts — or cannot be judged; anything else proceeds and the gate re-derives the merged denominator.
# DEV_CONTENT_ALLOWED is empty: dependabot #649/#575 touch api-gateway package.json and the Dev lockfile — if one lands, re-pin deliberately.
#
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool — and never run it without --check to "prove" this guard. `--check` runs headless (it launches nothing).
# exit 22: the prompt must require node_modules farmed PER ENTRY (the #1009 gate's R-6: a wholesale link can write through to the checkout's .vite).
# exit 23: the prompt must carry the exact verdict subject and name coagent@ as the sender and wednesday-agent@ as the recipient.
# QA1010_CUR_DEV (test override, --check only): stands in for origin develop so the LANDED / GUARDED refusals can be proven.
#
# Adapted from launch_qa_secuura_ks1087_1008.sh by gen_launcher_1010.py (asserted substitutions + residual guard + output
# controls + bash -n): same guards and exit codes, re-pointed at #1010, plus exits 22/23. Exit codes 2..23 (19 = LANDED).
# Written by the generator because it contains a legitimate directory change.
#
# Usage: launch_qa_secuura_ks1183_1010.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..23 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QA1010_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1010-ks1183-tier1.md}"
PROMPT_FILE="${QA1010_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1010-ks1183-tier1.prompt.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
BRANCH='refs/heads/feature/ks-1183-workflow-approve-the-forward-to-originate-has-no-timeout-so'
HEAD_SHA="${QA1010_HEAD:-c3213b04e3ad96068c367f7e0ba426822d32cda9}"
MERGE_BASE='f7c2f4acb28875e3665a61c8eaaad5c54bd3aa55'   # the merge-base of the head with develop = the PR parent f7c2f4acb (#1008's squash); develop has moved past it (behind 1)
DEVELOP_SHA='d067725ff1c7f036dbf0f726b9bf12f4daefebe7'   # develop at draft time = #1009's squash, NOT an ancestor of the head (git ls-remote 03:47:16, branches API 03:55:15 AEST)
REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1010-ks1183-tier1.md"

[ -d "$QA_DIR" ]         || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]          || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ]    || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]           || { echo "repo under test missing: $REPO" >&2; exit 5; }

# The head, pinned at its branch on origin (one ls-remote at run time).
LSR="$(git -C "$REPO" ls-remote origin "$BRANCH")"
if ! printf '%s\n' "$LSR" | grep -q "^${HEAD_SHA}[[:space:]]${BRANCH}\$"; then
  echo "REFUSING: #1010 — $HEAD_SHA is not at $BRANCH on origin — the head moved; the brief is about a different SHA" >&2
  printf '%s\n' "$LSR" >&2
  exit 6
fi

# The compare (GitHub compare API), asserted whole (merge_base + ahead + files; NOT behind — see the header):
# develop...#1010 = f7c2f4acb ahead 1 files 2 (behind 1 at draft time; behind deliberately not asserted).
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
[ "$COMPARE" = "$MERGE_BASE ahead=1 files=2" ] || { echo "REFUSING: #1010 develop...head reads '$COMPARE', brief pins '$MERGE_BASE ahead=1 files=2'" >&2; exit 10; }

# The develop pin, judged by CONTENT (see the header): fifteen files by blob at the CURRENT develop, then — if develop
# moved — the pinned...develop delta against the GUARDED list with the DEV_CONTENT_ALLOWED blobs cleared.
CUR_DEV="${QA1010_CUR_DEV:-$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)}"
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
  D + "services/api-gateway/src/routes/verification.ts":           ({"d0585dc34ceb5e3580ade38633250a6ffeaebd69": "base"}, {"04b3d980f657b13717060e9547d92970100b2557": "#1010 own"}),
  D + "services/api-gateway/src/__tests__/ks1087-workflow-approve-deletes-the-pending-document.test.ts": ({"7832724f3f5f97fa1260e3525dee8c68bda21ba4": "base"}, {"4450587dc2a0530a60c0bf5d5117b4831f754de3": "#1010 own"}),
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
  D + "docker/nginx-gateway/nginx.conf":                           ({"3c5576adaba1e3073b715335ba68d6cbbadd739a": "base"}, {}),
  D + "docker/nginx-gateway/nginx-demo.conf":                      ({"005a4bc279c0dc18830e0eb1d0c5bd3fcae37163": "base"}, {}),
  D + "docker/nginx-gateway/nginx-production.conf":                ({"562891b4cb0d3257912f14e0c335478500ec0d12": "base"}, {}),
}
state = []
for f, (ok, landed) in JUDGED.items():
    try:
        blob = get("/contents/" + f + "?ref=" + cur)["sha"]
    except Exception as e:
        print("UNJUDGEABLE develop blob unreadable for " + f.split("/")[-1] + ": " + type(e).__name__); sys.exit(0)
    short = f.replace(D, "")
    if blob in landed:
        print("LANDED develop " + short + " blob " + blob[:9] + " = " + landed[blob] + " — #1010 has landed; this brief is stale"); sys.exit(0)
    if blob not in ok:
        print("GUARDED develop " + short + " blob " + blob[:9] + " — a version nobody pinned"); sys.exit(0)
    state.append(f.split("/")[-1] + " " + blob[:9] + " = " + ok[blob])
state = "; ".join(state)
if cur == pinned:
    print("OK " + state + " | origin develop still " + pinned + " (NOT an ancestor of the head: the gate builds the merged tree head + " + pinned[:9] + " in its own clone; git ls-remote)"); sys.exit(0)
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
           D + "docker/nginx-gateway/",
           D + "deployment/caddy/",
           D + "eslint.config.mjs",
           D + "frontend/issuer/src/components/DocumentList.tsx",
           D + "services/mcp-server/src/api-client.ts",
           D + "package-lock.json"]
# SUFFIX-GUARDED: any portal or service nginx.conf in front of the gateway.
GUARDED_SUFFIX = ["/nginx.conf"]
# STYLE NOTE (912r2 launcher, measured): bash scans quote/paren state THROUGH this heredoc because it sits inside a
# command substitution — keep apostrophes and parentheses EVEN (this block uses none of the former), or the outer $( ) breaks.
# CONTENT-JUDGED allowlist: a hit under a GUARDED path clears ONLY if the per-file blob sha in the compare is EXACTLY one
# pinned here. EMPTY for this gate: at draft time 03:55 AEST no open lane PR touched a guarded path except dependabot
# bumps of api-gateway package.json and the Dev lockfile, which must NOT clear silently, so every guarded hit falls through to GUARDED and exit 18 — re-pin deliberately.
DEV_CONTENT_ALLOWED = {
}
hits = sorted({x["filename"] for x in files for g in GUARDED if x["filename"] == g or (g.endswith("/") and x["filename"].startswith(g))} | {x["filename"] for x in files for g in GUARDED_SUFFIX if x["filename"].endswith(g)})
by_name = {x["filename"]: x for x in files}
cleared = sorted(h for h in hits if h in DEV_CONTENT_ALLOWED and by_name.get(h, {}).get("sha") == DEV_CONTENT_ALLOWED[h])
remaining = sorted(h for h in hits if h not in cleared)
if remaining:
    print("GUARDED " + " ".join(remaining)); sys.exit(0)
tail = "the gate merges the then-current develop onto c3213b04e in its own clone, rebuilds the shared dist there, runs the api-gateway suite and the outcome probe on the MERGED tree beside the base and head trees, names the delta and re-derives every count, above all the api-gateway denominator (brief items 1, 8 and 9)"
if cleared:
    print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d, cleared BY BLOB under guarded paths: %s — %s" % (pinned, cur, c["ahead_by"], len(files), ",".join(x.split("/")[-1] for x in cleared), tail)); sys.exit(0)
print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d — disjoint from the GUARDED list (api-gateway verification.ts + the ks1087 test + index.ts + auth.ts + redis.ts + enforcement.ts + package.json + vitest config/setup + tsconfig, originate routes/documents.ts, docs/openapi/, docker/nginx-gateway/, deployment/caddy/, any nginx.conf, eslint.config.mjs, the two route consumers, the Dev lockfile); %s" % (pinned, cur, c["ahead_by"], len(files), tail)); sys.exit(0)
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
grep -qi 'node_modules per ENTRY' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not require node_modules farmed per ENTRY (a wholesale link can write through to the checkout .vite cache)" >&2; exit 22; }
grep -qF '[QA -> Wednesday] TIER 1 GATE #1010 (KS-1183) c3213b04e' "$PROMPT_FILE" && grep -qF 'coagent@agentmail.to' "$PROMPT_FILE" && grep -qF 'wednesday-agent@agentmail.to' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry the exact verdict subject, the coagent@ sender and the wednesday-agent@ recipient" >&2; exit 23; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  head on origin: #1010 $HEAD_SHA at $BRANCH"
  echo "  compare (GitHub API): develop...#1010 = $COMPARE"
  echo "  $DEV_NOTE"
  echo "  brief, prompt, QA project and repo all present"
  echo "  brief and prompt agree on TIER 1 and ROUND 1"
  echo "  prompt opens with the thinking directive and names the brief"
  echo "  brief and prompt both name the head SHA"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  echo "  prompt requires node_modules farmed per ENTRY"
  echo "  prompt carries the exact verdict subject, coagent@ sender, wednesday-agent@ recipient"
  [ -n "${QA1010_CUR_DEV:-}" ] && echo "  (develop read from the QA1010_CUR_DEV test override, not ls-remote)"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"
  exit 0
fi

[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — this launcher execs an interactive agent; run it in a cockpit pane, never inside a Bash tool (a headless gate is invisible and dies with the caller's shell)" >&2; exit 21; }
[ -z "${QA1010_BRIEF:-}${QA1010_PROMPT:-}${QA1010_HEAD:-}${QA1010_CUR_DEV:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$DEV_NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
