#!/bin/bash
# launch_qa_secuura_ks769_1020.sh — cross-project QA agent, ONE TIER 2 ROUND 1 gate over Secuura/Blockchain PR #1020
# (KS-769, Seat A) @ 71bd80a35b406b9c99c7b96955a7521032d33c20 — ONE commit on d7e95cd9f, ONE file, +5 -1:
# Blockchain/Dev/scripts/audit/lock-discovery.mjs, OUT_OF_SCOPE_LOCKS mobile/secuura-app expires 2026-09-17 -> 2026-10-19 plus a
# four-line ruling comment (Kam ruled KS-769 "Dormant but kept"). The lapsed fuse refuses every Blockchain/Dev push at preflight legs 5 and 7.
#
# THE SHAPE, as read 15:42-15:46 AEST 2026-09-17 (git ls-remote + the compare API agree): the head parent is d7e95cd9f (the KS-1195 #1017
# squash) and origin develop IS d7e95cd9f. compare develop...head = merge_base d7e95cd9f, status ahead, ahead 1, behind 0, files 1. The
# compare is asserted as merge_base + ahead + files (exit 10); `behind` is deliberately NOT asserted, so a develop that moves on (#1018 and
# #1019 are open in the same lineage) does not trip this guard — the develop arm judges the move by CONTENT.
#
# The develop pin is judged by CONTENT, not bare: (a) TWELVE files by blob at the CURRENT develop — lock-discovery.mjs (base 2f54840ce; the
# PR own 3dd903b52 -> exit 19 LANDED), lock-discovery.test.mjs, baseline-contract.mjs (utcToday + isLapsed), baseline-contract.test.mjs,
# gate-exit-codes.test.mjs, audit-locks.mjs, audit-gate.mjs, audit-baseline.json (the other dated fuses), expected-case-count (59, leg 5),
# scripts/audit/package.json, scripts/preflight/preflight.sh, and the Dev package.json (the audit:contract script) — any blob nobody pinned
# -> exit 18; (b) if develop moved past d7e95cd9f, the compare pinned...develop REFUSES (exit 18) only when the delta touches a GUARDED
# path — anything under Blockchain/Dev/scripts/audit/, preflight.sh, the Dev package.json, or .githooks/pre-push — or cannot be judged;
# anything else proceeds and the gate re-derives every count on the merged tree. Lockfiles are deliberately NOT guarded: a dependency bump
# landing changes which advisories the gates report, and the gate re-measures that on the merged tree rather than refusing to start.
# DEV_CONTENT_ALLOWED is empty.
#
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool. `--check` still runs headless (it launches nothing).
#
# Adapted from launch_qa_secuura_ks864_1009.sh by gen_launcher_1020.py (asserted substitutions + residual guard + output
# controls + bash -n): same guards and exit codes, re-pointed at #1020. Exit codes 2..21 (19 = LANDED).
# Written by the generator because it contains a legitimate directory change.
#
# Usage: launch_qa_secuura_ks769_1020.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..21 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QA1020_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1020-ks769-tier2.md}"
PROMPT_FILE="${QA1020_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1020-ks769-tier2.prompt.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
BRANCH='refs/heads/chore/audit-fuse-mobile-tree-dormant-redate'
HEAD_SHA="${QA1020_HEAD:-71bd80a35b406b9c99c7b96955a7521032d33c20}"
MERGE_BASE='d7e95cd9f153e9036ed77935a73c93504fa6e3dc'   # the merge-base of the head with develop = the PR parent (the KS-1195 #1017 squash; develop has not moved)
DEVELOP_SHA='d7e95cd9f153e9036ed77935a73c93504fa6e3dc'   # develop at draft time = the PR parent itself (ls-remote 15:42:00, compare API 15:46:12 AEST)
REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1020-ks769-tier2.md"

[ -d "$QA_DIR" ]         || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]          || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ]    || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]           || { echo "repo under test missing: $REPO" >&2; exit 5; }

# The head, pinned at its branch on origin (one ls-remote at run time).
LSR="$(git -C "$REPO" ls-remote origin "$BRANCH")"
if ! printf '%s\n' "$LSR" | grep -q "^${HEAD_SHA}[[:space:]]${BRANCH}\$"; then
  echo "REFUSING: #1020 — $HEAD_SHA is not at $BRANCH on origin — the head moved; the brief is about a different SHA" >&2
  printf '%s\n' "$LSR" >&2
  exit 6
fi

# The compare (GitHub compare API), asserted whole (merge_base + ahead + files; NOT behind — see the header):
# develop...#1020 = d7e95cd9f ahead 1 files 1 (behind 0 at draft time — deliberately not asserted).
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
[ "$COMPARE" = "$MERGE_BASE ahead=1 files=1" ] || { echo "REFUSING: #1020 develop...head reads '$COMPARE', brief pins '$MERGE_BASE ahead=1 files=1'" >&2; exit 10; }

# The develop pin, judged by CONTENT (see the header): twelve files by blob at the CURRENT develop, then — if develop
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
  D + "scripts/audit/lock-discovery.mjs":          ({"2f54840ce6470e4e8eadeab603a9db7fa3eb49b9": "base"}, {"3dd903b527f26c758cc1da84b10cc0a0db3b1d46": "#1020 own"}),
  D + "scripts/audit/lock-discovery.test.mjs":     ({"f102d9d4c4523091fe4e3119d6c539fb29bfd904": "base"}, {}),
  D + "scripts/audit/baseline-contract.mjs":       ({"2504d9a28dc017fcaabfc88248bf1c64431eb38a": "base"}, {}),
  D + "scripts/audit/baseline-contract.test.mjs":  ({"2379c0aeee6e3e3f0c4ef3a2512e3a590ad47d29": "base"}, {}),
  D + "scripts/audit/gate-exit-codes.test.mjs":    ({"40079f6fb41e146a34a66463e352b9c0a49f91e8": "base"}, {}),
  D + "scripts/audit/audit-locks.mjs":             ({"aff23b0420ced863884787443a35f28cf727bd09": "base"}, {}),
  D + "scripts/audit/audit-gate.mjs":              ({"8e236ee70ce1a4634552596fb86fcffce234f221": "base"}, {}),
  D + "scripts/audit/audit-baseline.json":         ({"03d1680e3c7a87f8df70e71082b67775536acde5": "base"}, {}),
  D + "scripts/audit/expected-case-count":         ({"04f9fe46068b397a6fc24d647b7e3ec4315c15e7": "base"}, {}),
  D + "scripts/audit/package.json":                ({"d5977b6a13638558ef57e8c294809d7ada8be6cd": "base"}, {}),
  D + "scripts/preflight/preflight.sh":       ({"28d3636c13a4259bbdade8b15ac527cbe93742c3": "base"}, {}),
  D + "package.json":                         ({"769b7adbda124bb200dd9827d2e4fbc5883e6124": "base"}, {}),
}
state = []
for f, (ok, landed) in JUDGED.items():
    try:
        blob = get("/contents/" + f + "?ref=" + cur)["sha"]
    except Exception as e:
        print("UNJUDGEABLE develop blob unreadable for " + f.split("/")[-1] + ": " + type(e).__name__); sys.exit(0)
    short = f.replace(D, "")
    if blob in landed:
        print("LANDED develop " + short + " blob " + blob[:9] + " = " + landed[blob] + " — #1020 has landed; this brief is stale"); sys.exit(0)
    if blob not in ok:
        print("GUARDED develop " + short + " blob " + blob[:9] + " — a version nobody pinned"); sys.exit(0)
    state.append(f.split("/")[-1] + " " + blob[:9] + " = " + ok[blob])
state = "; ".join(state)
if cur == pinned:
    print("OK " + state + " | origin develop still " + pinned + " (= the PR parent, the KS-1195 #1017 squash; git ls-remote)"); sys.exit(0)
try:
    c = get("/compare/" + pinned + "..." + cur)
except Exception as e:
    print("UNJUDGEABLE compare unreadable: " + type(e).__name__); sys.exit(0)
files = c.get("files") or []
if c.get("status") != "ahead" or len(files) > 250:
    print("UNJUDGEABLE status=%s files=%d" % (c.get("status"), len(files))); sys.exit(0)
GUARDED = [D + "scripts/audit/",
           D + "scripts/preflight/preflight.sh",
           D + "package.json",
           ".githooks/pre-push"]
# STYLE NOTE (912r2 launcher, measured): bash scans quote/paren state THROUGH this heredoc because it sits inside a
# command substitution — keep apostrophes and parentheses EVEN (this block uses none of the former), or the outer $( ) breaks.
# CONTENT-JUDGED allowlist: a hit under a GUARDED path clears ONLY if the per-file blob sha in the compare is EXACTLY one
# pinned here. EMPTY for this gate: at draft time 15:46 AEST no open PR touched a guarded path (PR files API, 20 open PRs),
# so every guarded hit falls through to GUARDED and exit 18 — re-pin deliberately.
DEV_CONTENT_ALLOWED = {
}
hits = sorted({x["filename"] for x in files for g in GUARDED if x["filename"] == g or (g.endswith("/") and x["filename"].startswith(g))})
by_name = {x["filename"]: x for x in files}
cleared = sorted(h for h in hits if h in DEV_CONTENT_ALLOWED and by_name.get(h, {}).get("sha") == DEV_CONTENT_ALLOWED[h])
remaining = sorted(h for h in hits if h not in cleared)
if remaining:
    print("GUARDED " + " ".join(remaining)); sys.exit(0)
tail = "the gate merges the then-current develop onto 71bd80a35 in its own clone, runs the audit legs on the MERGED tree beside the base and head trees, names the delta and re-derives every count and the fuse census (brief item 6)"
if cleared:
    print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d, cleared BY BLOB under guarded paths: %s — %s" % (pinned, cur, c["ahead_by"], len(files), ",".join(x.split("/")[-1] for x in cleared), tail)); sys.exit(0)
print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d — disjoint from the GUARDED list (Blockchain/Dev/scripts/audit/, scripts/preflight/preflight.sh, the Dev package.json, .githooks/pre-push); %s" % (pinned, cur, c["ahead_by"], len(files), tail)); sys.exit(0)
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
  echo "  head on origin: #1020 $HEAD_SHA at $BRANCH"
  echo "  compare (GitHub API): develop...#1020 = $COMPARE"
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
[ -z "${QA1020_BRIEF:-}${QA1020_PROMPT:-}${QA1020_HEAD:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$DEV_NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
