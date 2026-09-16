#!/bin/bash
# launch_qa_secuura_ks745_1012.sh — cross-project QA agent, ONE TIER 1 ROUND 1 gate over Secuura/Blockchain PR #1012
# (KS-745, Seat A successor) @ e225a49480e16bb77251a5d7cbd16afdf2929550 — ONE commit on d067725ff (develop = #1009's squash), 2 files, both
# services/api-gateway: routes/audit-export.ts +4 -2 (the admin audit export fetches the security list route /api/audit, was /api/audit/logs
# which matched /api/audit/:id and 404'd, and reads data.data.logs) and the new ks745 test (+69). TIER 1 (Wednesday's ruling): before the PR
# the export 404'd and returned nothing; after it the export returns security audit-log entries — a NEW data path out of the audit store,
# and who can read which tenant's entries through it is the lead question.
#
# THE SHAPE, as read 04:13-04:21 AEST 2026-09-17 (git ls-remote + the PR and compare APIs agree): develop d067725ff IS the PR parent and the
# merge-base; compare develop...head = merge_base d067725ff, ahead 1, behind 0, files 2. The compare is asserted as merge_base + ahead + files
# (exit 10); `behind` is deliberately NOT asserted — the develop arm judges every move by CONTENT, and the gate builds the merged tree itself.
#
# The develop pin is judged by CONTENT, not bare: (a) FIFTEEN files by blob at the CURRENT develop — audit-export.ts (base a301f5e22; the PR's
# own d87c04979 -> exit 19 LANDED), the ks745 test (ABSENT on develop; the PR's own fb6a33957 -> exit 19 LANDED), api-gateway src/index.ts (the
# :801 mount), middleware/auth.ts, middleware/audit.ts (base a7be8626f OR #1011's f5a83ba2c — a known sibling lane), routes/admin.ts,
# package.json, vitest.config.ts, vitest.setup.ts, tsconfig.json, security src/index.ts (the list route :732-777), shared middleware/index.ts
# (authenticate), shared security/keyRevokePolicy.ts (isPlatformRole), docs/openapi/secuura-api.yaml (the export IS in the spec), Dev
# eslint.config.mjs — any blob nobody pinned -> exit 18; (b) if develop moved past d067725ff, the compare pinned...develop REFUSES (exit 18)
# when the delta touches a GUARDED path — those files, services/security/src/, packages/shared/src/middleware/, packages/shared/src/security/,
# docs/openapi/, the Dev lockfile — or cannot be judged; anything else proceeds and the gate re-derives the merged denominator.
# DEV_CONTENT_ALLOWED pins #1011's audit.ts blob only; dependabot #649/#575 touch api-gateway + security package.json and the lockfile — if one
# lands, re-pin deliberately.
#
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool — and never run it without --check to "prove" this guard. `--check` runs headless (it launches nothing).
# exit 22: the prompt must require node_modules farmed PER ENTRY (the #1009 gate's R-6: a wholesale link can write through to the checkout's .vite).
# exit 23: the prompt must carry the exact verdict subject and name coagent@ as the sender and wednesday-agent@ as the recipient.
# QA1012_CUR_DEV (test override, --check only): stands in for origin develop so the LANDED / GUARDED refusals can be proven.
#
# Adapted from launch_qa_secuura_ks1183_1010.sh by gen_launcher_1012.py (asserted block replacements + residual guard + output
# controls + bash -n): same guards and exit codes, re-pointed at #1012. Exit codes 2..23 (19 = LANDED).
# Written by the generator because it contains a legitimate directory change.
#
# Usage: launch_qa_secuura_ks745_1012.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..23 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QA1012_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1012-ks745-tier1.md}"
PROMPT_FILE="${QA1012_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1012-ks745-tier1.prompt.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
BRANCH='refs/heads/feature/ks-745-ornith-audit-export-list-route'
HEAD_SHA="${QA1012_HEAD:-e225a49480e16bb77251a5d7cbd16afdf2929550}"
MERGE_BASE='d067725ff1c7f036dbf0f726b9bf12f4daefebe7'   # the merge-base of the head with develop = the PR parent d067725ff (#1009's squash) = develop at draft time (behind 0)
DEVELOP_SHA='d067725ff1c7f036dbf0f726b9bf12f4daefebe7'   # develop at draft time (git ls-remote 04:13:27, branches API 04:19:32 AEST)
REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1012-ks745-tier1.md"

[ -d "$QA_DIR" ]         || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]          || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ]    || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]           || { echo "repo under test missing: $REPO" >&2; exit 5; }

# The head, pinned at its branch on origin (one ls-remote at run time).
LSR="$(git -C "$REPO" ls-remote origin "$BRANCH")"
if ! printf '%s\n' "$LSR" | grep -q "^${HEAD_SHA}[[:space:]]${BRANCH}\$"; then
  echo "REFUSING: #1012 — $HEAD_SHA is not at $BRANCH on origin — the head moved; the brief is about a different SHA" >&2
  printf '%s\n' "$LSR" >&2
  exit 6
fi

# The compare (GitHub compare API), asserted whole (merge_base + ahead + files; NOT behind — see the header):
# develop...#1012 = d067725ff ahead 1 files 2 (behind 0 at draft time; behind deliberately not asserted).
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
[ "$COMPARE" = "$MERGE_BASE ahead=1 files=2" ] || { echo "REFUSING: #1012 develop...head reads '$COMPARE', brief pins '$MERGE_BASE ahead=1 files=2'" >&2; exit 10; }

# The develop pin, judged by CONTENT (see the header): fifteen files by blob at the CURRENT develop, then — if develop
# moved — the pinned...develop delta against the GUARDED list with the DEV_CONTENT_ALLOWED blobs cleared.
CUR_DEV="${QA1012_CUR_DEV:-$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)}"
[ -n "$CUR_DEV" ] || { echo "REFUSING: could not read origin develop (git ls-remote)" >&2; exit 18; }
DEV_JUDGEMENT="$(
  set -a; . "$SECUURA_ENV"; set +a
  DEVELOP_SHA="$DEVELOP_SHA" CUR_DEV="$CUR_DEV" python3 - <<'PYJ'
import json, os, sys, urllib.request, urllib.error
t = os.environ.get("GH_TOKEN", "")
api = "https://api.github.com/repos/Secuura/Distributed_Secuura"
def get(p):
    return json.load(urllib.request.urlopen(urllib.request.Request(api + p, headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}), timeout=60))
cur = os.environ["CUR_DEV"]; pinned = os.environ["DEVELOP_SHA"]
D = "Blockchain/Dev/"
# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label}); ABSENT = the file does not exist at that develop (contents API 404)
JUDGED = {
  D + "services/api-gateway/src/routes/audit-export.ts":            ({"a301f5e22ceeb4adb37bd8b924eaade09e07394f": "base"}, {"d87c04979e2bbfb28505d4ba7c63d252f0fbe302": "#1012 own"}),
  D + "services/api-gateway/src/__tests__/ks745-audit-export-calls-the-list-route.test.ts": ({"ABSENT": "base, absent"}, {"fb6a33957d07256bef1d45d1a66d6f333233ba50": "#1012 own"}),
  D + "services/api-gateway/src/index.ts":                          ({"6f38c819e48162e3179aaf557085766f91beecc1": "base"}, {}),
  D + "services/api-gateway/src/middleware/auth.ts":                ({"20311010db0eb8ba097644ce105cf8df966ce456": "base"}, {}),
  D + "services/api-gateway/src/middleware/audit.ts":               ({"a7be8626ff1d79a0887fb8d31c44286472157644": "base", "f5a83ba2cde6c64eb5540976c55867d637e8f6eb": "#1011 KS-871 landed"}, {}),
  D + "services/api-gateway/src/routes/admin.ts":                   ({"f47dd6a655702ffbfc402ca920a33c4619d62c4b": "base"}, {}),
  D + "services/api-gateway/package.json":                          ({"841d8c6adcd71e885c01e65c22da9418daff276a": "base"}, {}),
  D + "services/api-gateway/vitest.config.ts":                      ({"5888e0b320d934f6f434e0e5ca3c74a995cecc02": "base"}, {}),
  D + "services/api-gateway/vitest.setup.ts":                       ({"22c1107683b8192df3bfd3e929aa94aff3dc7d45": "base"}, {}),
  D + "services/api-gateway/tsconfig.json":                         ({"c981e6a92fdd2417fa35070eb979c5f1c77ffbcd": "base"}, {}),
  D + "services/security/src/index.ts":                             ({"0903ce4380f219765ac63f5f9399d1bf0b4f230a": "base"}, {}),
  D + "packages/shared/src/middleware/index.ts":                    ({"3a67987a7be4a4c02f8326bf8a840a2c2b4efbf3": "base"}, {}),
  D + "packages/shared/src/security/keyRevokePolicy.ts":            ({"86b55405290f6337def1221c869fab68bdf7c2b2": "base"}, {}),
  D + "docs/openapi/secuura-api.yaml":                              ({"122d3a2f84cf77bf2b7e2dc51489a0d5f823db1f": "base"}, {}),
  D + "eslint.config.mjs":                                          ({"8c5374c6022eb0a3f449f41a570db61294aa63f1": "base"}, {}),
}
state = []
for f, (ok, landed) in JUDGED.items():
    try:
        blob = get("/contents/" + f + "?ref=" + cur)["sha"]
    except urllib.error.HTTPError as e:
        if e.code != 404:
            print("UNJUDGEABLE develop blob unreadable for " + f.split("/")[-1] + ": HTTP " + str(e.code)); sys.exit(0)
        blob = "ABSENT"
    except Exception as e:
        print("UNJUDGEABLE develop blob unreadable for " + f.split("/")[-1] + ": " + type(e).__name__); sys.exit(0)
    short = f.replace(D, "")
    if blob in landed:
        print("LANDED develop " + short + " blob " + blob[:9] + " = " + landed[blob] + " — #1012 has landed; this brief is stale"); sys.exit(0)
    if blob not in ok:
        print("GUARDED develop " + short + " blob " + blob[:9] + " — a version nobody pinned"); sys.exit(0)
    state.append(f.split("/")[-1] + " " + blob[:9] + " = " + ok[blob])
state = "; ".join(state)
if cur == pinned:
    print("OK " + state + " | origin develop still " + pinned + " (= the PR parent: merged tree = head while develop is unmoved; git ls-remote)"); sys.exit(0)
try:
    c = get("/compare/" + pinned + "..." + cur)
except Exception as e:
    print("UNJUDGEABLE compare unreadable: " + type(e).__name__); sys.exit(0)
files = c.get("files") or []
if c.get("status") != "ahead" or len(files) > 250:
    print("UNJUDGEABLE status=%s files=%d" % (c.get("status"), len(files))); sys.exit(0)
GUARDED = [D + "services/api-gateway/src/routes/audit-export.ts",
           D + "services/api-gateway/src/__tests__/ks745-audit-export-calls-the-list-route.test.ts",
           D + "services/api-gateway/src/index.ts",
           D + "services/api-gateway/src/middleware/auth.ts",
           D + "services/api-gateway/src/middleware/audit.ts",
           D + "services/api-gateway/src/routes/admin.ts",
           D + "services/api-gateway/package.json",
           D + "services/api-gateway/vitest.config.ts",
           D + "services/api-gateway/vitest.setup.ts",
           D + "services/api-gateway/tsconfig.json",
           D + "services/security/src/",
           D + "services/security/package.json",
           D + "packages/shared/src/middleware/",
           D + "packages/shared/src/security/",
           D + "docs/openapi/",
           D + "eslint.config.mjs",
           D + "package-lock.json"]
# SUFFIX-GUARDED: none for this gate (no proxy config is in the question; the export is gateway-answered).
GUARDED_SUFFIX = []
# STYLE NOTE (912r2 launcher, measured): bash scans quote/paren state THROUGH this heredoc because it sits inside a
# command substitution — keep apostrophes and parentheses EVEN (this block uses none of the former), or the outer $( ) breaks.
# CONTENT-JUDGED allowlist: a hit under a GUARDED path clears ONLY if the per-file blob sha in the compare is EXACTLY one
# pinned here. ONE entry for this gate: #1011 (KS-871, 0a1f8900c, a sibling tier-1 lane) changes middleware/audit.ts to exactly
# f5a83ba2c — if it lands first the gate proceeds and must re-derive the merged tree with it (its EXCLUDED_PREFIXES names /api/admin/audit).
# Dependabot bumps of api-gateway or security package.json and the Dev lockfile must NOT clear silently — every other guarded hit is exit 18.
DEV_CONTENT_ALLOWED = {
  D + "services/api-gateway/src/middleware/audit.ts": "f5a83ba2cde6c64eb5540976c55867d637e8f6eb",
}
hits = sorted({x["filename"] for x in files for g in GUARDED if x["filename"] == g or (g.endswith("/") and x["filename"].startswith(g))} | {x["filename"] for x in files for g in GUARDED_SUFFIX if x["filename"].endswith(g)})
by_name = {x["filename"]: x for x in files}
cleared = sorted(h for h in hits if h in DEV_CONTENT_ALLOWED and by_name.get(h, {}).get("sha") == DEV_CONTENT_ALLOWED[h])
remaining = sorted(h for h in hits if h not in cleared)
if remaining:
    print("GUARDED " + " ".join(remaining)); sys.exit(0)
tail = "the gate merges the then-current develop onto e225a4948 in its own clone, rebuilds the shared dist there, runs the api-gateway suite, the tenant probe and the real-app reach rows on the MERGED tree beside the base and head trees, names the delta and re-derives every count (brief items 1, 7, 8 and 10)"
if cleared:
    print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d, cleared BY BLOB under guarded paths: %s — %s" % (pinned, cur, c["ahead_by"], len(files), ",".join(x.split("/")[-1] for x in cleared), tail)); sys.exit(0)
print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d — disjoint from the GUARDED list (api-gateway audit-export.ts + the ks745 test + index.ts + auth.ts + audit.ts + admin.ts + package.json + vitest config/setup + tsconfig, services/security/src/ + package.json, packages/shared/src/middleware/ + security/, docs/openapi/, eslint.config.mjs, the Dev lockfile); %s" % (pinned, cur, c["ahead_by"], len(files), tail)); sys.exit(0)
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
grep -qF '[QA -> Wednesday] TIER 1 GATE #1012 (KS-745) e225a4948' "$PROMPT_FILE" && grep -qF 'coagent@agentmail.to' "$PROMPT_FILE" && grep -qF 'wednesday-agent@agentmail.to' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry the exact verdict subject, the coagent@ sender and the wednesday-agent@ recipient" >&2; exit 23; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  head on origin: #1012 $HEAD_SHA at $BRANCH"
  echo "  compare (GitHub API): develop...#1012 = $COMPARE"
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
  [ -n "${QA1012_CUR_DEV:-}" ] && echo "  (develop read from the QA1012_CUR_DEV test override, not ls-remote)"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"
  exit 0
fi

[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — this launcher execs an interactive agent; run it in a cockpit pane, never inside a Bash tool (a headless gate is invisible and dies with the caller's shell)" >&2; exit 21; }
[ -z "${QA1012_BRIEF:-}${QA1012_PROMPT:-}${QA1012_HEAD:-}${QA1012_CUR_DEV:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$DEV_NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
