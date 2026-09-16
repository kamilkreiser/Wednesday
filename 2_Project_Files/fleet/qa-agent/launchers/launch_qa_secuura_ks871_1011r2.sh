#!/bin/bash
# launch_qa_secuura_ks871_1011r2.sh — cross-project QA agent, ONE TIER 1 ROUND 2 gate (round 2 of 2 under the cap) over Secuura/Blockchain
# PR #1011 (KS-871, Seat A successor item A12) @ 6dc8256448b50de6a15519001a4f7032ace1ae19 — three commits: the round-one commit, a --no-ff merge
# of develop 1125607e9 (22c0a51a8), and the round-two commit. Delta over 1125607e9 = 4 files, all services/api-gateway: src/middleware/audit.ts
# +18 -4 (auditPath = req.path captured at entry, used for details.path AND deriveAction) and three ks871 test files (one NEW real-app file).
# TIER 1 (Wednesday's ruling): the audit middleware writes the audit trail for EVERY audited request, and the audit trail is a security control.
#
# THE SHAPE, as read 05:15-05:27 AEST 2026-09-17 (git + the compare API agree): merge-base 1125607e9; develop has since moved to 79432c797
# (#1012, KS-745: routes/audit-export.ts + a new ks745 test), so develop is NOT an ancestor of the head: compare develop...head = merge_base
# 1125607e9, status diverged, ahead 3, behind 1, files 4. The compare is asserted as merge_base + ahead + files (exit 10); `behind` is
# deliberately NOT asserted, so a develop that moves on does not trip this guard — the develop arm judges the move by CONTENT.
#
# The develop pin is judged by CONTENT, not bare: (a) FOURTEEN files by blob at the CURRENT develop — audit.ts (develop a7be8626f; this PR's
# own 052131de0 -> exit 19 LANDED), api-gateway src/index.ts (the /api/v1 strip and the audit mount), src/routes/proxy.ts (the erasure door),
# src/middleware/normalisePath.ts, src/routes/versioning.ts (the production 307), src/db.ts (the mocked sink), src/middleware/auth.ts,
# package.json, vitest.config.ts, vitest.setup.ts, tsconfig.json (the exclude the including tsc overrides), Dev eslint.config.mjs, and the two
# census route files develop changed since the prior round: src/routes/audit-export.ts (#1012) and src/routes/verification.ts (#1010) — any
# blob nobody pinned -> exit 18; (b) if develop moved past 79432c797, the compare pinned...develop REFUSES (exit 18) only when the delta touches
# a GUARDED path — those fourteen files, the three ks871 tests, the Dev lockfile — or cannot be judged; anything else proceeds and the gate
# merges develop and re-runs the census on the merged tree.
# DEV_CONTENT_ALLOWED is empty: dependabot #649/#575 touch api-gateway package.json and the Dev lockfile, eight more touch the lockfile —
# if one lands, this launcher refuses and the brief is re-pinned deliberately.
#
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool. `--check` still runs headless (it launches nothing).
# exit 22: the prompt must require node_modules farmed PER ENTRY (the #1009 gate's R-6: a wholesale link can write through to the checkout's .vite).
# exit 23: the prompt must carry the exact ROUND 2 verdict subject and name coagent@ as the sender and wednesday-agent@ as the recipient.
# exit 24: brief AND prompt must name the prior round's REPORT path (BRIEF_TEMPLATE round-N rule: the QA agent has no inbox).
# exit 25: brief AND prompt must require the per-finding CLOSED / STILL OPEN / NEW disposition (round 2 of 2: closed instances ship, residue is ticketed).
# QA1011R2_CUR_DEV: a --check-only test override for the develop SHA (negative fixtures); a launch with it set refuses (exit 16).
#
# Adapted from launch_qa_secuura_ks871_1011.sh by gen_launcher_1011r2.py (asserted substitutions + residual guard + output
# controls + bash -n): same guards and exit codes, re-pointed at round 2, plus exits 24/25. Exit codes 2..25 (19 = LANDED).
# Written by the generator because it contains a legitimate directory change.
#
# Usage: launch_qa_secuura_ks871_1011r2.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..25 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QA1011R2_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1011r2-ks871-tier1.md}"
PROMPT_FILE="${QA1011R2_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1011r2-ks871-tier1.prompt.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
BRANCH='refs/heads/feature/ks-871-ornith-audit-path-captured-at-entry'
HEAD_SHA="${QA1011R2_HEAD:-6dc8256448b50de6a15519001a4f7032ace1ae19}"
MERGE_BASE='1125607e978d6ad637720c985e43e3d79fecdf88'   # the merge-base of the head with develop: 1125607e9, which the branch merged at 22c0a51a8 (develop has since moved on; behind 1)
DEVELOP_SHA='79432c797cfb6e647acdd8798dace000a0b35d75'   # develop at draft time, NOT an ancestor of the head (git ls-remote 05:15:30 and 05:26:47, branches API 05:16:42 AEST)
R1_REPORT='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks871-1011-0a1f8900c-tier1-r1/'
REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1011r2-ks871-tier1.md"

[ -d "$QA_DIR" ]         || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]          || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ]    || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]           || { echo "repo under test missing: $REPO" >&2; exit 5; }

# The head, pinned at its branch on origin (one ls-remote at run time).
LSR="$(git -C "$REPO" ls-remote origin "$BRANCH")"
if ! printf '%s\n' "$LSR" | grep -q "^${HEAD_SHA}[[:space:]]${BRANCH}\$"; then
  echo "REFUSING: #1011 — $HEAD_SHA is not at $BRANCH on origin — the head moved; the brief is about a different SHA" >&2
  printf '%s\n' "$LSR" >&2
  exit 6
fi

# The compare (GitHub compare API), asserted whole (merge_base + ahead + files; NOT behind — see the header):
# develop...#1011 = merge_base 1125607e9 ahead 3 files 4 (behind 1 at draft; behind deliberately not asserted).
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
[ "$COMPARE" = "$MERGE_BASE ahead=3 files=4" ] || { echo "REFUSING: #1011 develop...head reads '$COMPARE', brief pins '$MERGE_BASE ahead=3 files=4'" >&2; exit 10; }

# The develop pin, judged by CONTENT (see the header): fourteen files by blob at the CURRENT develop, then — if develop
# moved — the pinned...develop delta against the GUARDED list with the DEV_CONTENT_ALLOWED blobs cleared.
CUR_DEV="${QA1011R2_CUR_DEV:-$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)}"
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
  D + "services/api-gateway/src/middleware/audit.ts":              ({"a7be8626ff1d79a0887fb8d31c44286472157644": "develop"}, {"052131de06c3f510e4bcaadc9b6831d0cca617c2": "#1011 round-2 own"}),
  D + "services/api-gateway/src/index.ts":                         ({"6f38c819e48162e3179aaf557085766f91beecc1": "develop"}, {}),
  D + "services/api-gateway/src/routes/proxy.ts":                  ({"b99f45a4c9c89088a7809de5f26c4f56fc94819c": "develop"}, {}),
  D + "services/api-gateway/src/middleware/normalisePath.ts":      ({"1a7312a8675ffdfe263060bb5d60aa837111431a": "develop"}, {}),
  D + "services/api-gateway/src/routes/versioning.ts":             ({"697bbb48bd93775572c7bde41c303eb4775ee920": "develop"}, {}),
  D + "services/api-gateway/src/db.ts":                            ({"9144c532bca9911da6cedd569e575c5aa6bc6c52": "develop"}, {}),
  D + "services/api-gateway/src/middleware/auth.ts":               ({"20311010db0eb8ba097644ce105cf8df966ce456": "develop"}, {}),
  D + "services/api-gateway/package.json":                         ({"841d8c6adcd71e885c01e65c22da9418daff276a": "develop"}, {}),
  D + "services/api-gateway/vitest.config.ts":                     ({"5888e0b320d934f6f434e0e5ca3c74a995cecc02": "develop"}, {}),
  D + "services/api-gateway/vitest.setup.ts":                      ({"22c1107683b8192df3bfd3e929aa94aff3dc7d45": "develop"}, {}),
  D + "services/api-gateway/tsconfig.json":                        ({"c981e6a92fdd2417fa35070eb979c5f1c77ffbcd": "develop"}, {}),
  D + "eslint.config.mjs":                                          ({"8c5374c6022eb0a3f449f41a570db61294aa63f1": "develop"}, {}),
  D + "services/api-gateway/src/routes/audit-export.ts":           ({"d87c04979e2bbfb28505d4ba7c63d252f0fbe302": "develop"}, {}),
  D + "services/api-gateway/src/routes/verification.ts":           ({"04b3d980f657b13717060e9547d92970100b2557": "develop"}, {}),
}
state = []
for f, (ok, landed) in JUDGED.items():
    try:
        blob = get("/contents/" + f + "?ref=" + cur)["sha"]
    except Exception as e:
        print("UNJUDGEABLE develop blob unreadable for " + f.split("/")[-1] + ": " + type(e).__name__); sys.exit(0)
    short = f.replace(D, "")
    if blob in landed:
        print("LANDED develop " + short + " blob " + blob[:9] + " = " + landed[blob] + " — #1011 has landed; this brief is stale"); sys.exit(0)
    if blob not in ok:
        print("GUARDED develop " + short + " blob " + blob[:9] + " — a version nobody pinned"); sys.exit(0)
    state.append(f.split("/")[-1] + " " + blob[:9] + " = " + ok[blob])
state = "; ".join(state)
if cur == pinned:
    print("OK " + state + " | origin develop still " + pinned + " (NOT an ancestor of the head: the gate merges it, so the merged tree differs from the head tree; git ls-remote)"); sys.exit(0)
try:
    c = get("/compare/" + pinned + "..." + cur)
except Exception as e:
    print("UNJUDGEABLE compare unreadable: " + type(e).__name__); sys.exit(0)
files = c.get("files") or []
if c.get("status") != "ahead" or len(files) > 250:
    print("UNJUDGEABLE status=%s files=%d" % (c.get("status"), len(files))); sys.exit(0)
GUARDED = [D + "services/api-gateway/src/middleware/audit.ts",
           D + "services/api-gateway/src/__tests__/ks871-audit-path-captured-at-entry.test.ts",
           D + "services/api-gateway/src/__tests__/ks871-the-audit-log-records-req-path.test.ts",
           D + "services/api-gateway/src/__tests__/ks871-real-app-canonical-audit-rows.test.ts",
           D + "services/api-gateway/src/index.ts",
           D + "services/api-gateway/src/routes/proxy.ts",
           D + "services/api-gateway/src/middleware/normalisePath.ts",
           D + "services/api-gateway/src/routes/versioning.ts",
           D + "services/api-gateway/src/db.ts",
           D + "services/api-gateway/src/middleware/auth.ts",
           D + "services/api-gateway/package.json",
           D + "services/api-gateway/vitest.config.ts",
           D + "services/api-gateway/vitest.setup.ts",
           D + "services/api-gateway/tsconfig.json",
           D + "eslint.config.mjs",
           D + "services/api-gateway/src/routes/audit-export.ts",
           D + "services/api-gateway/src/routes/verification.ts",
           D + "package-lock.json"]
# SUFFIX-GUARDED: none for this gate — every guarded path above is exact.
GUARDED_SUFFIX = []
# STYLE NOTE (912r2 launcher, measured): bash scans quote/paren state THROUGH this heredoc because it sits inside a
# command substitution — keep apostrophes and parentheses EVEN (this block uses none of the former), or the outer $( ) breaks.
# CONTENT-JUDGED allowlist: a hit under a GUARDED path clears ONLY if the per-file blob sha in the compare is EXACTLY one
# pinned here. EMPTY for this gate: at draft time 05:17 AEST no open PR touched a guarded path except dependabot bumps
# of api-gateway package.json and the Dev lockfile, which must NOT clear silently, so every guarded hit falls through to GUARDED and exit 18 — re-pin deliberately.
DEV_CONTENT_ALLOWED = {
}
hits = sorted({x["filename"] for x in files for g in GUARDED if x["filename"] == g or (g.endswith("/") and x["filename"].startswith(g))} | {x["filename"] for x in files for g in GUARDED_SUFFIX if x["filename"].endswith(g)})
by_name = {x["filename"]: x for x in files}
cleared = sorted(h for h in hits if h in DEV_CONTENT_ALLOWED and by_name.get(h, {}).get("sha") == DEV_CONTENT_ALLOWED[h])
remaining = sorted(h for h in hits if h not in cleared)
if remaining:
    print("GUARDED " + " ".join(remaining)); sys.exit(0)
tail = "the gate merges the then-current develop onto 6dc825644 in its own clone, rebuilds the shared dist there, runs the api-gateway suite and the audit census on the MERGED tree beside the base and head trees, names the delta and re-derives every count, above all the api-gateway denominator (brief items 1, 8 and 11)"
if cleared:
    print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d, cleared BY BLOB under guarded paths: %s — %s" % (pinned, cur, c["ahead_by"], len(files), ",".join(x.split("/")[-1] for x in cleared), tail)); sys.exit(0)
print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d — disjoint from the GUARDED list (api-gateway audit.ts + the three ks871 tests + index.ts + proxy.ts + normalisePath.ts + versioning.ts + db.ts + auth.ts + audit-export.ts + verification.ts + package.json + vitest config/setup + tsconfig, eslint.config.mjs, the Dev lockfile); %s" % (pinned, cur, c["ahead_by"], len(files), tail)); sys.exit(0)
PYJ
)"
case "$DEV_JUDGEMENT" in
  OK*) DEV_NOTE="${DEV_JUDGEMENT#OK }" ;;
  LANDED*) echo "REFUSING: ${DEV_JUDGEMENT#LANDED } (develop $CUR_DEV) — re-pin deliberately: a different brief" >&2; exit 19 ;;
  *) echo "REFUSING: origin develop is at $CUR_DEV (pinned $DEVELOP_SHA) and the move is not provably disjoint: ${DEV_JUDGEMENT:-no judgement} — confirm the delta, then re-pin deliberately (launcher DEVELOP_SHA / JUDGED blobs / DEV_CONTENT_ALLOWED + brief TARGET + prompt)" >&2
     exit 18 ;;
esac
grep -q 'TIER 1' "$BRIEF" && grep -q 'TIER 1' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the tier" >&2; exit 7; }
grep -q 'ROUND 2' "$BRIEF" && grep -q 'ROUND 2' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the round (ROUND 2)" >&2; exit 15; }
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
grep -qF '[QA -> Wednesday] TIER 1 GATE #1011 ROUND 2 (KS-871) 6dc825644' "$PROMPT_FILE" && grep -qF 'coagent@agentmail.to' "$PROMPT_FILE" && grep -qF 'wednesday-agent@agentmail.to' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry the exact ROUND 2 verdict subject, the coagent@ sender and the wednesday-agent@ recipient" >&2; exit 23; }
grep -qF "$R1_REPORT" "$PROMPT_FILE" && grep -qF "$R1_REPORT" "$BRIEF" \
  || { echo "REFUSING: brief or prompt does not name the prior round REPORT path $R1_REPORT — the QA agent has no inbox; a carry-forward with no pointer can only be answered with I could not" >&2; exit 24; }
grep -qF 'CLOSED / STILL OPEN / NEW' "$PROMPT_FILE" && grep -qF 'CLOSED / STILL OPEN / NEW' "$BRIEF" \
  || { echo "REFUSING: brief or prompt does not require the per-finding CLOSED / STILL OPEN / NEW disposition — round 2 of 2: closed instances ship and residue is ticketed" >&2; exit 25; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  head on origin: #1011 $HEAD_SHA at $BRANCH"
  echo "  compare (GitHub API): develop...#1011 = $COMPARE"
  echo "  $DEV_NOTE"
  echo "  brief, prompt, QA project and repo all present"
  echo "  brief and prompt agree on TIER 1 and ROUND 2"
  echo "  prompt opens with the thinking directive and names the brief"
  echo "  brief and prompt both name the head SHA"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  echo "  prompt requires node_modules farmed per ENTRY"
  echo "  prompt carries the exact ROUND 2 verdict subject, coagent@ sender, wednesday-agent@ recipient"
  echo "  brief and prompt name the prior round REPORT path"
  echo "  brief and prompt require CLOSED / STILL OPEN / NEW per finding"
  [ -n "${QA1011R2_CUR_DEV:-}" ] && echo "  (develop read from the QA1011R2_CUR_DEV test override, not ls-remote)"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"
  exit 0
fi

[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — this launcher execs an interactive agent; run it in a cockpit pane, never inside a Bash tool (a headless gate is invisible and dies with the caller's shell)" >&2; exit 21; }
[ -z "${QA1011R2_BRIEF:-}${QA1011R2_PROMPT:-}${QA1011R2_HEAD:-}${QA1011R2_CUR_DEV:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$DEV_NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
