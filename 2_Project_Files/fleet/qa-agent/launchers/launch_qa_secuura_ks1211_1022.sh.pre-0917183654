#!/bin/bash
# launch_qa_secuura_ks1211_1022.sh — cross-project QA agent, ONE TIER 1 ROUND 1 gate over Secuura/Blockchain PR #1022
# (KS-1211, Seat B, rows 8-10 of the audit-baseline fix work: hono GHSA-gqvv-2mrq-wpjv, GHSA-g6gw-c38x-mqfc, GHSA-crvj-82cr-hjcx)
# @ 58684e6534b4d420c9fb9ea246d3a32c70c70828 — ONE commit on f8c7aaa39, FOUR files: hono 4.13.0 -> 4.13.8 in
# Blockchain/Dev/services/mcp-server/package-lock.json, services/originate/package-lock.json and the Blockchain/Dev root package-lock.json
# (which also carries the 12-entry flag reconciliation Wednesday ruled), and the three hono rows removed from
# Blockchain/Dev/scripts/audit/audit-baseline.json (38 -> 35). No manifest. Tier 1: hono ships in the mcp-server (and originate) images.
#
# THE SHAPE, as read 17:57-18:11 AEST 2026-09-17 (git ls-remote + the compare API agree): the head parent is f8c7aaa39 (the develop tip before #1019);
# origin develop is 581c9db0d (#1019 squash, 3 api-gateway files, disjoint). compare develop...head = merge_base f8c7aaa39, status diverged,
# ahead 1, behind 1, files 4. The compare is asserted as merge_base + ahead + files (exit 10); `behind` is deliberately NOT asserted, so a
# develop that moves on does not trip this guard — the develop arm judges the move by CONTENT.
#
# The develop pin is judged by CONTENT, not bare: (a) EIGHTEEN files by blob at the CURRENT develop — the four PR files (root lock base
# 17d2061b3 / own 99db3e7c2, audit-baseline.json base 03d1680e3 / own b78691b4c, mcp-server lock base 5171f5586 / own f942d659b, originate
# lock base 2d3439a8a / own d91d746ef; an own blob -> exit 19 LANDED), the Dev, mcp-server and originate package.json, audit-gate.mjs,
# audit-locks.mjs, lock-discovery.mjs, baseline-contract.mjs, scripts/audit/package.json, preflight.sh, lockfile-cleanroom.sh, both service
# Dockerfiles, and mcp-server src/http-server.ts + src/index.ts (the runtime-reach reading rests on them) — any blob nobody pinned -> exit 18;
# (b) if develop moved past 581c9db0d, the compare pinned...develop REFUSES (exit 18) only when the delta touches a GUARDED path — anything
# under Blockchain/Dev/scripts/audit/, Blockchain/Dev/scripts/preflight/ or Blockchain/Dev/services/mcp-server/, the Dev package.json or
# root package-lock.json, originate package.json / package-lock.json / Dockerfile, or .githooks/pre-push — or cannot be judged; anything else
# proceeds and the gate re-derives on the merged tree. #1021 (same ticket) edits audit-baseline.json, so #1021 landing first REFUSES here
# by design (the second PR merges develop in and gets a new head): re-pin deliberately. DEV_CONTENT_ALLOWED is empty.
#
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool. `--check` still runs headless (it launches nothing).
#
# Adapted from launch_qa_secuura_ks769_1020.sh by gen_launcher_1022.py (asserted substitutions + residual guard + output
# controls + bash -n): same guards and exit codes, re-pointed at #1022 and TIER 1. Exit codes 2..21 (19 = LANDED).
# Written by the generator because it contains a legitimate directory change.
#
# Usage: launch_qa_secuura_ks1211_1022.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..21 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QA1022_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1022-ks1211-hono-tier1.md}"
PROMPT_FILE="${QA1022_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1022-ks1211-hono-tier1.prompt.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
BRANCH='refs/heads/feature/ks-1211-bump-hono'
HEAD_SHA="${QA1022_HEAD:-58684e6534b4d420c9fb9ea246d3a32c70c70828}"
MERGE_BASE='f8c7aaa39dabfe6a3916e5be55d9ccd752e7d8ed'   # the merge-base of the head with develop = the PR parent (the develop tip before #1019)
DEVELOP_SHA='581c9db0db4201c42cbbf702f339b750989acdb1'   # develop at draft time = the #1019 squash, NOT the PR parent (ls-remote 17:57:05 + 18:11:01, compare API 17:57:27 AEST)
REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1022-ks1211-hono-tier1.md"

[ -d "$QA_DIR" ]         || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]          || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ]    || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]           || { echo "repo under test missing: $REPO" >&2; exit 5; }

# The head, pinned at its branch on origin (one ls-remote at run time).
LSR="$(git -C "$REPO" ls-remote origin "$BRANCH")"
if ! printf '%s\n' "$LSR" | grep -q "^${HEAD_SHA}[[:space:]]${BRANCH}\$"; then
  echo "REFUSING: #1022 — $HEAD_SHA is not at $BRANCH on origin — the head moved; the brief is about a different SHA" >&2
  printf '%s\n' "$LSR" >&2
  exit 6
fi

# The compare (GitHub compare API), asserted whole (merge_base + ahead + files; NOT behind — see the header):
# develop...#1022 = f8c7aaa39 ahead 1 files 4 (behind 1 at draft time — deliberately not asserted).
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
[ "$COMPARE" = "$MERGE_BASE ahead=1 files=4" ] || { echo "REFUSING: #1022 develop...head reads '$COMPARE', brief pins '$MERGE_BASE ahead=1 files=4'" >&2; exit 10; }

# The develop pin, judged by CONTENT (see the header): eighteen files by blob at the CURRENT develop, then — if develop
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
  D + "package-lock.json":                         ({"17d2061b397595677ae789683b0ca1d4b8398bec": "base"}, {"99db3e7c2434f65eb64ab0d8db5775e11eefd6bd": "#1022 own"}),
  D + "scripts/audit/audit-baseline.json":         ({"03d1680e3c7a87f8df70e71082b67775536acde5": "base"}, {"b78691b4c7c75096e191b58af91d86fd1a824ca3": "#1022 own"}),
  D + "services/mcp-server/package-lock.json":     ({"5171f55862ea4354b7d3a3a050113c463794c96a": "base"}, {"f942d659b90b2314ccb5737cb41ecc3c0a70a306": "#1022 own"}),
  D + "services/originate/package-lock.json":      ({"2d3439a8a99b293a98b6a221414ee041d7d83466": "base"}, {"d91d746efb2b7fcd6d3168838925f40d7282ea32": "#1022 own"}),
  D + "package.json":                              ({"769b7adbda124bb200dd9827d2e4fbc5883e6124": "base"}, {}),
  D + "services/mcp-server/package.json":          ({"a97eaaab5b029ea2edfeba4bb9db5c83ef20e728": "base"}, {}),
  D + "services/originate/package.json":           ({"749912c592e8630fff348cc60e1bf49677c18ab1": "base"}, {}),
  D + "scripts/audit/audit-gate.mjs":              ({"8e236ee70ce1a4634552596fb86fcffce234f221": "base"}, {}),
  D + "scripts/audit/audit-locks.mjs":             ({"aff23b0420ced863884787443a35f28cf727bd09": "base"}, {}),
  D + "scripts/audit/lock-discovery.mjs":          ({"3dd903b527f26c758cc1da84b10cc0a0db3b1d46": "base"}, {}),
  D + "scripts/audit/baseline-contract.mjs":       ({"2504d9a28dc017fcaabfc88248bf1c64431eb38a": "base"}, {}),
  D + "scripts/audit/package.json":                ({"d5977b6a13638558ef57e8c294809d7ada8be6cd": "base"}, {}),
  D + "scripts/preflight/preflight.sh":            ({"28d3636c13a4259bbdade8b15ac527cbe93742c3": "base"}, {}),
  D + "scripts/preflight/lockfile-cleanroom.sh":   ({"518bffeeaf4a3c47a4660f594f822f34e26c2d15": "base"}, {}),
  D + "services/mcp-server/Dockerfile":            ({"60485f4a67ac8110f204777adf2df36dc2645da7": "base"}, {}),
  D + "services/originate/Dockerfile":             ({"ac2fb91bf7d814b407f41bcca904793b6d6d91c1": "base"}, {}),
  D + "services/mcp-server/src/http-server.ts":    ({"fce4a31793b3765de96fc387a2f306da5db15744": "base"}, {}),
  D + "services/mcp-server/src/index.ts":          ({"687512fe63fcec74342035c67e8ce99656b3e1a6": "base"}, {}),
}
state = []
for f, (ok, landed) in JUDGED.items():
    try:
        blob = get("/contents/" + f + "?ref=" + cur)["sha"]
    except Exception as e:
        print("UNJUDGEABLE develop blob unreadable for " + f.split("/")[-1] + ": " + type(e).__name__); sys.exit(0)
    short = f.replace(D, "")
    if blob in landed:
        print("LANDED develop " + short + " blob " + blob[:9] + " = " + landed[blob] + " — #1022 has landed; this brief is stale"); sys.exit(0)
    if blob not in ok:
        print("GUARDED develop " + short + " blob " + blob[:9] + " — a version nobody pinned"); sys.exit(0)
    state.append(f.split("/")[-1] + " " + blob[:9] + " = " + ok[blob])
state = "; ".join(state)
if cur == pinned:
    print("OK " + state + " | origin develop still " + pinned + " (= the #1019 squash, the develop tip at draft time, NOT the PR parent; git ls-remote)"); sys.exit(0)
try:
    c = get("/compare/" + pinned + "..." + cur)
except Exception as e:
    print("UNJUDGEABLE compare unreadable: " + type(e).__name__); sys.exit(0)
files = c.get("files") or []
if c.get("status") != "ahead" or len(files) > 250:
    print("UNJUDGEABLE status=%s files=%d" % (c.get("status"), len(files))); sys.exit(0)
GUARDED = [D + "scripts/audit/",
           D + "scripts/preflight/",
           D + "services/mcp-server/",
           D + "package.json",
           D + "package-lock.json",
           D + "services/originate/package.json",
           D + "services/originate/package-lock.json",
           D + "services/originate/Dockerfile",
           ".githooks/pre-push"]
# STYLE NOTE (912r2 launcher, measured): bash scans quote/paren state THROUGH this heredoc because it sits inside a
# command substitution — keep apostrophes and parentheses EVEN (this block uses none of the former), or the outer $( ) breaks.
# CONTENT-JUDGED allowlist: a hit under a GUARDED path clears ONLY if the per-file blob sha in the compare is EXACTLY one
# pinned here. EMPTY for this gate: at draft time 17:57 AEST #1021 touched audit-baseline.json and ten Dependabot PRs the root lock (PR files API, 21 open PRs),
# so every guarded hit falls through to GUARDED and exit 18 — re-pin deliberately.
DEV_CONTENT_ALLOWED = {
}
hits = sorted({x["filename"] for x in files for g in GUARDED if x["filename"] == g or (g.endswith("/") and x["filename"].startswith(g))})
by_name = {x["filename"]: x for x in files}
cleared = sorted(h for h in hits if h in DEV_CONTENT_ALLOWED and by_name.get(h, {}).get("sha") == DEV_CONTENT_ALLOWED[h])
remaining = sorted(h for h in hits if h not in cleared)
if remaining:
    print("GUARDED " + " ".join(remaining)); sys.exit(0)
tail = "the gate merges the then-current develop onto 58684e653 in its own clone, names the merged tree and its delta, and proves the audit inputs blob-identical to head or re-runs the gates there (brief item 5)"
if cleared:
    print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d, cleared BY BLOB under guarded paths: %s — %s" % (pinned, cur, c["ahead_by"], len(files), ",".join(x.split("/")[-1] for x in cleared), tail)); sys.exit(0)
print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d — disjoint from the GUARDED list (Blockchain/Dev/scripts/audit/, scripts/preflight/, services/mcp-server/, the Dev package.json and root lock, originate package.json / lock / Dockerfile, .githooks/pre-push); %s" % (pinned, cur, c["ahead_by"], len(files), tail)); sys.exit(0)
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
  echo "  head on origin: #1022 $HEAD_SHA at $BRANCH"
  echo "  compare (GitHub API): develop...#1022 = $COMPARE"
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
[ -z "${QA1022_BRIEF:-}${QA1022_PROMPT:-}${QA1022_HEAD:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$DEV_NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
