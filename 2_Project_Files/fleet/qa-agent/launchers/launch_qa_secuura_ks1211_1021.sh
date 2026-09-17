#!/bin/bash
# launch_qa_secuura_ks1211_1021.sh — cross-project QA agent, ONE TIER 2 ROUND 1 gate over Secuura/Blockchain PR #1021
# (KS-1211, Seat B, row 6 of the audit-baseline fix work, GHSA-2wm5-q62r-hmrv colord) @ 742e1c6080f2527973268146611930e4a70edef2 —
# ONE commit on f8c7aaa39, THREE files: colord 2.9.3 -> 2.10.0 in systemTest/akto/package-lock.json and
# systemTest/api-explorer/package-lock.json (declarer stylelint ^2.9.3, dev-only), and the colord row removed from
# Blockchain/Dev/scripts/audit/audit-baseline.json (38 -> 37). No manifest.
#
# THE SHAPE, as read 17:46-17:56 AEST 2026-09-17 (git ls-remote + the compare API): the head parent is f8c7aaa39. origin develop was
# f8c7aaa39 at 17:46 and MOVED to 581c9db0d (#1019, KS-1187, api-gateway only: proxy.ts + two tests) by 17:54. compare develop...head =
# merge_base f8c7aaa39, status ahead, ahead 1, files 3 (behind 0 at 17:48, behind 1 after #1019). The
# compare is asserted as merge_base + ahead + files (exit 10); `behind` is deliberately NOT asserted, so a develop that moves on does not
# trip this guard — the develop arm judges the move by CONTENT.
#
# The develop pin is judged by CONTENT, not bare: (a) THIRTEEN files by blob at the CURRENT develop — the three PR files
# (audit-baseline.json base 03d1680e3 / own c73fcebed, the akto lock base 6b348adcc / own c4d30077f, the api-explorer lock base 8be03ee9c /
# own 78589de7e; an own blob -> exit 19 LANDED), the two harness package.json, audit-locks.mjs, audit-gate.mjs, lock-discovery.mjs,
# baseline-contract.mjs, scripts/audit/package.json, preflight.sh, lockfile-cleanroom.sh and systemTest/CLAUDE.md (the harness quality-gate
# rule) — any blob nobody pinned -> exit 18; (b) if develop moved past f8c7aaa39, the compare pinned...develop REFUSES (exit 18) only when the
# delta touches a GUARDED path — anything under Blockchain/Dev/scripts/audit/ or Blockchain/Dev/scripts/preflight/, either harness
# package.json or package-lock.json, systemTest/CLAUDE.md, or .githooks/pre-push — or cannot be judged; anything else proceeds and the gate
# re-derives every count on the merged tree. Seat B's next row PRs all edit audit-baseline.json, so one of them landing first REFUSES here
# by design: re-pin deliberately. DEV_CONTENT_ALLOWED is empty.
#
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool. `--check` still runs headless (it launches nothing).
#
# Adapted from launch_qa_secuura_ks769_1020.sh by gen_launcher_1021.py (asserted substitutions + residual guard + output
# controls + bash -n): same guards and exit codes, re-pointed at #1021. Exit codes 2..21 (19 = LANDED).
# Written by the generator because it contains a legitimate directory change.
#
# Usage: launch_qa_secuura_ks1211_1021.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..21 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QA1021_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1021-ks1211-colord-tier2.md}"
PROMPT_FILE="${QA1021_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1021-ks1211-colord-tier2.prompt.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
BRANCH='refs/heads/feature/ks-1211-bump-colord'
HEAD_SHA="${QA1021_HEAD:-742e1c6080f2527973268146611930e4a70edef2}"
MERGE_BASE='f8c7aaa39dabfe6a3916e5be55d9ccd752e7d8ed'   # the merge-base of the head with develop = the PR parent (develop moved on to #1019, api-gateway only)
DEVELOP_SHA='581c9db0db4201c42cbbf702f339b750989acdb1'   # develop at draft time = #1019's squash (KS-1187), a child of the PR parent, 3 api-gateway files, 0 guarded (ls-remote 17:54:41 AEST)
REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1021-ks1211-colord-tier2.md"

[ -d "$QA_DIR" ]         || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]          || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ]    || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]           || { echo "repo under test missing: $REPO" >&2; exit 5; }

# The head, pinned at its branch on origin (one ls-remote at run time).
LSR="$(git -C "$REPO" ls-remote origin "$BRANCH")"
if ! printf '%s\n' "$LSR" | grep -q "^${HEAD_SHA}[[:space:]]${BRANCH}\$"; then
  echo "REFUSING: #1021 — $HEAD_SHA is not at $BRANCH on origin — the head moved; the brief is about a different SHA" >&2
  printf '%s\n' "$LSR" >&2
  exit 6
fi

# The compare (GitHub compare API), asserted whole (merge_base + ahead + files; NOT behind — see the header):
# develop...#1021 = f8c7aaa39 ahead 1 files 3 (behind 0 at draft time — deliberately not asserted).
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
[ "$COMPARE" = "$MERGE_BASE ahead=1 files=3" ] || { echo "REFUSING: #1021 develop...head reads '$COMPARE', brief pins '$MERGE_BASE ahead=1 files=3'" >&2; exit 10; }

# The develop pin, judged by CONTENT (see the header): thirteen files by blob at the CURRENT develop, then — if develop
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
  D + "scripts/audit/audit-baseline.json":         ({"03d1680e3c7a87f8df70e71082b67775536acde5": "base"}, {"c73fcebeda52cab362533193a961b661010a92b3": "#1021 own"}),
  "systemTest/akto/package-lock.json":         ({"6b348adcccdf1c3bc7ff216eb4936c2d057a7fd0": "base"}, {"c4d30077f8857e9579897097a6fd362e8ed367f1": "#1021 own"}),
  "systemTest/api-explorer/package-lock.json": ({"8be03ee9cd6d388e630cb153535da4a310521a5e": "base"}, {"78589de7e1165c64ef74707fdc75e1515fd6eae5": "#1021 own"}),
  "systemTest/akto/package.json":              ({"3aecaf4852620ea29dcf4d0473761111cbbf92f6": "base"}, {}),
  "systemTest/api-explorer/package.json":      ({"46141226323996c6a24fb16a01155395e5c959cf": "base"}, {}),
  D + "scripts/audit/audit-locks.mjs":             ({"aff23b0420ced863884787443a35f28cf727bd09": "base"}, {}),
  D + "scripts/audit/audit-gate.mjs":              ({"8e236ee70ce1a4634552596fb86fcffce234f221": "base"}, {}),
  D + "scripts/audit/lock-discovery.mjs":          ({"3dd903b527f26c758cc1da84b10cc0a0db3b1d46": "base"}, {}),
  D + "scripts/audit/baseline-contract.mjs":       ({"2504d9a28dc017fcaabfc88248bf1c64431eb38a": "base"}, {}),
  D + "scripts/audit/package.json":                ({"d5977b6a13638558ef57e8c294809d7ada8be6cd": "base"}, {}),
  D + "scripts/preflight/preflight.sh":       ({"28d3636c13a4259bbdade8b15ac527cbe93742c3": "base"}, {}),
  D + "scripts/preflight/lockfile-cleanroom.sh": ({"518bffeeaf4a3c47a4660f594f822f34e26c2d15": "base"}, {}),
  "systemTest/CLAUDE.md":                      ({"357015b941af9e8dfcbb2e159f150dadbcde6e27": "base"}, {}),
}
state = []
for f, (ok, landed) in JUDGED.items():
    try:
        blob = get("/contents/" + f + "?ref=" + cur)["sha"]
    except Exception as e:
        print("UNJUDGEABLE develop blob unreadable for " + f.split("/")[-1] + ": " + type(e).__name__); sys.exit(0)
    short = f.replace(D, "")
    if blob in landed:
        print("LANDED develop " + short + " blob " + blob[:9] + " = " + landed[blob] + " — #1021 has landed; this brief is stale"); sys.exit(0)
    if blob not in ok:
        print("GUARDED develop " + short + " blob " + blob[:9] + " — a version nobody pinned"); sys.exit(0)
    state.append(f.split("/")[-1] + " " + blob[:9] + " = " + ok[blob])
state = "; ".join(state)
if cur == pinned:
    print("OK " + state + " | origin develop still " + pinned + " (#1019 squash on the PR parent, api-gateway only; git ls-remote)"); sys.exit(0)
try:
    c = get("/compare/" + pinned + "..." + cur)
except Exception as e:
    print("UNJUDGEABLE compare unreadable: " + type(e).__name__); sys.exit(0)
files = c.get("files") or []
if c.get("status") != "ahead" or len(files) > 250:
    print("UNJUDGEABLE status=%s files=%d" % (c.get("status"), len(files))); sys.exit(0)
GUARDED = [D + "scripts/audit/",
           D + "scripts/preflight/",
           "systemTest/akto/package.json",
           "systemTest/akto/package-lock.json",
           "systemTest/api-explorer/package.json",
           "systemTest/api-explorer/package-lock.json",
           "systemTest/CLAUDE.md",
           ".githooks/pre-push"]
# STYLE NOTE (912r2 launcher, measured): bash scans quote/paren state THROUGH this heredoc because it sits inside a
# command substitution — keep apostrophes and parentheses EVEN (this block uses none of the former), or the outer $( ) breaks.
# CONTENT-JUDGED allowlist: a hit under a GUARDED path clears ONLY if the per-file blob sha in the compare is EXACTLY one
# pinned here. EMPTY for this gate: at draft time 17:48 AEST no open PR shared a file with #1021 (PR files API, 21 open PRs),
# so every guarded hit falls through to GUARDED and exit 18 — re-pin deliberately.
DEV_CONTENT_ALLOWED = {
}
hits = sorted({x["filename"] for x in files for g in GUARDED if x["filename"] == g or (g.endswith("/") and x["filename"].startswith(g))})
by_name = {x["filename"]: x for x in files}
cleared = sorted(h for h in hits if h in DEV_CONTENT_ALLOWED and by_name.get(h, {}).get("sha") == DEV_CONTENT_ALLOWED[h])
remaining = sorted(h for h in hits if h not in cleared)
if remaining:
    print("GUARDED " + " ".join(remaining)); sys.exit(0)
tail = "the gate merges the then-current develop onto 742e1c608 in its own clone, re-runs the lock parse and both audit gates on the MERGED tree beside the base and head trees, and names the delta (brief item 5)"
if cleared:
    print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d, cleared BY BLOB under guarded paths: %s — %s" % (pinned, cur, c["ahead_by"], len(files), ",".join(x.split("/")[-1] for x in cleared), tail)); sys.exit(0)
print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d — disjoint from the GUARDED list (Blockchain/Dev/scripts/audit/, Blockchain/Dev/scripts/preflight/, the two harness package.json and package-lock.json, systemTest/CLAUDE.md, .githooks/pre-push); %s" % (pinned, cur, c["ahead_by"], len(files), tail)); sys.exit(0)
PYJ
)"
case "$DEV_JUDGEMENT" in
  OK*) DEV_NOTE="${DEV_JUDGEMENT#OK }" ;;
  LANDED*) echo "REFUSING: ${DEV_JUDGEMENT#LANDED } (develop $CUR_DEV) — re-pin deliberately: a different brief" >&2; exit 19 ;;
  *) echo "REFUSING: origin develop is at $CUR_DEV (pinned $DEVELOP_SHA) and the move is not provably disjoint: ${DEV_JUDGEMENT:-no judgement} — confirm the delta, then re-pin deliberately (launcher DEVELOP_SHA / JUDGED blobs / DEV_CONTENT_ALLOWED + brief TARGET + prompt)" >&2
     exit 18 ;;
esac
grep -q 'TIER 2' "$BRIEF" && grep -q 'TIER 2' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the tier" >&2; exit 7; }
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
  echo "  head on origin: #1021 $HEAD_SHA at $BRANCH"
  echo "  compare (GitHub API): develop...#1021 = $COMPARE"
  echo "  $DEV_NOTE"
  echo "  brief, prompt, QA project and repo all present"
  echo "  brief and prompt agree on TIER 2 and ROUND 1"
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
[ -z "${QA1021_BRIEF:-}${QA1021_PROMPT:-}${QA1021_HEAD:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$DEV_NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
