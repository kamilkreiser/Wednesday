#!/bin/bash
# launch_qa_secuura_ks999_1013.sh — cross-project QA agent, ONE TIER 1 ROUND 1 gate over Secuura/Blockchain PR #1013
# (KS-999 items 1 + 3 + 4, Seat A successor) @ 5fbfb66a927ea50a8ad0531f344b58a33f7bd9c2 — ONE commit on 1125607e9 (#1010's squash),
# 3 files, all services/auth: repositories/userRepo.ts +11 -7 (getUserById now `return await fromRow(...)`, so a subject-DEK read
# failure inside fromRow reaches the KS-253 classifier: 503 instead of a raw 500; a doc comment), the NEW
# __tests__/ks999-getuserbyid-awaits-fromrow.test.ts (+97) and __tests__/ks949-platform-admin-seed-identity.test.ts (+18 -3).
# TIER 1: a 500 -> 503 change on the normal production read path of the auth service, reached by every route that calls
# getUserById directly or through updateUser / getUserByIdPlatformScope.
#
# THE SHAPE, as read 04:44-04:49 AEST 2026-09-17 (git ls-remote + the compare API agree): develop = 1125607e9 = the PR parent;
# compare develop...head = merge_base 1125607e9, ahead 1, behind 0, files 3. The compare is asserted as merge_base + ahead + files
# (exit 10); `behind` is deliberately NOT asserted — the develop arm judges every move by CONTENT.
#
# The develop pin is judged by CONTENT, not bare: (a) TWENTY-ONE files by blob at the CURRENT develop — userRepo.ts (base 822b3fcd8;
# the PR's own 9060b308e -> exit 19 LANDED), the ks949 test (base 67316e5da; the PR's own 4f03e6f4f -> exit 19 LANDED), the ks999 test
# (ABSENT at base; the PR's own 04ce4e156 -> exit 19 LANDED), the calling routes users.ts / mfa.ts / wallet.ts / oauth.ts / auth.ts,
# middleware errorHandler.ts / authenticate.ts, repositories/dbErrors.ts, services/subjectDeks.ts / passwordLoginGate.ts, src/index.ts,
# packages/shared crypto/subjectDek.ts, auth package.json / vitest.config.ts / vitest.setup.ts / tsconfig.json, Dev eslint.config.mjs and
# docs/openapi/secuura-api.yaml — any blob nobody pinned -> exit 18; (b) if develop moved past 1125607e9, the compare
# pinned...develop REFUSES (exit 18) when the delta touches a GUARDED path — services/auth/src/, services/auth/ config files,
# packages/shared/src/crypto/, docs/openapi/, eslint.config.mjs, the Dev lockfile — or cannot be judged.
# DEV_CONTENT_ALLOWED is empty: dependabot #948/#649/#575 touch services/auth/package.json and the Dev lockfile — if one lands, re-pin deliberately.
#
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool — and never run it without --check to "prove" this guard. `--check` runs headless (it launches nothing).
# exit 22: the prompt must require node_modules farmed PER ENTRY (the #1009 gate's R-6: a wholesale link can write through to the checkout's .vite).
# exit 23: the prompt must carry the exact verdict subject and name coagent@ as the sender and wednesday-agent@ as the recipient.
# QA1013_CUR_DEV (test override, --check only): stands in for origin develop so the LANDED / GUARDED refusals can be proven.
#
# Derived by hand from launch_qa_secuura_ks1183_1010.sh (the #1010 gate's launcher, verdict GO WITH FINDINGS): same guards and exit
# codes, re-pointed at #1013; the JUDGED map gains an ABSENT state for the file the PR adds. Exit codes 2..23 (19 = LANDED).
#
# Usage: launch_qa_secuura_ks999_1013.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..23 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QA1013_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1013-ks999-tier1.md}"
PROMPT_FILE="${QA1013_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1013-ks999-tier1.prompt.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
BRANCH='refs/heads/feature/ks-999-ornith-getuserbyid-awaits-fromrow'
HEAD_SHA="${QA1013_HEAD:-5fbfb66a927ea50a8ad0531f344b58a33f7bd9c2}"
MERGE_BASE='1125607e978d6ad637720c985e43e3d79fecdf88'   # the merge-base of the head with develop = the PR parent 1125607e9 (#1010's squash)
DEVELOP_SHA='1125607e978d6ad637720c985e43e3d79fecdf88'   # develop at draft time = the PR parent (git ls-remote 04:44:09, branches API 04:48:55 AEST)
REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1013-ks999-tier1.md"

[ -d "$QA_DIR" ]         || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]          || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ]    || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]           || { echo "repo under test missing: $REPO" >&2; exit 5; }

# The head, pinned at its branch on origin (one ls-remote at run time).
LSR="$(git -C "$REPO" ls-remote origin "$BRANCH")"
if ! printf '%s\n' "$LSR" | grep -q "^${HEAD_SHA}[[:space:]]${BRANCH}\$"; then
  echo "REFUSING: #1013 — $HEAD_SHA is not at $BRANCH on origin — the head moved; the brief is about a different SHA" >&2
  printf '%s\n' "$LSR" >&2
  exit 6
fi

# The compare (GitHub compare API), asserted whole (merge_base + ahead + files; NOT behind — see the header):
# develop...#1013 = 1125607e9 ahead 1 files 3 (behind 0 at draft time; behind deliberately not asserted).
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
[ "$COMPARE" = "$MERGE_BASE ahead=1 files=3" ] || { echo "REFUSING: #1013 develop...head reads '$COMPARE', brief pins '$MERGE_BASE ahead=1 files=3'" >&2; exit 10; }

# The develop pin, judged by CONTENT (see the header): twenty-one files by blob at the CURRENT develop, then — if develop
# moved — the pinned...develop delta against the GUARDED list with the DEV_CONTENT_ALLOWED blobs cleared.
CUR_DEV="${QA1013_CUR_DEV:-$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)}"
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
A = D + "services/auth/"
# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label}); ABSENT = the contents API answers 404 at develop
JUDGED = {
  A + "src/repositories/userRepo.ts":                               ({"822b3fcd8404b81f0e0a56dcebed784278771c8b": "base"}, {"9060b308e6d6a82c8a79be7387032d2a18c4ac22": "#1013 own"}),
  A + "src/__tests__/ks949-platform-admin-seed-identity.test.ts":   ({"67316e5da73c5269a2a19688afe16029d1bbfe0b": "base"}, {"4f03e6f4f132bc7a8f3c3577684f6eef3bf8ce03": "#1013 own"}),
  A + "src/__tests__/ks999-getuserbyid-awaits-fromrow.test.ts":     ({"ABSENT": "base"}, {"04ce4e1564e9d27406185391dbb20924d3423b67": "#1013 own"}),
  A + "src/routes/users.ts":                                        ({"89da72df7bfab2275550de0868288b7958ea059c": "base"}, {}),
  A + "src/routes/mfa.ts":                                          ({"87d3ee1079fe90010f45955dbaf4307ae595b205": "base"}, {}),
  A + "src/routes/wallet.ts":                                       ({"3134e9525fcf972f81a5c74a8fc77fe3df15c367": "base"}, {}),
  A + "src/routes/oauth.ts":                                        ({"3ae75ea1351a503d2f8f4c0f366598ee2917fd56": "base"}, {}),
  A + "src/routes/auth.ts":                                         ({"18946cd7c5c394d89ecbecf860ab66a96b1e22c7": "base"}, {}),
  A + "src/middleware/errorHandler.ts":                             ({"1cf66e74cd2bbe1d56f53c6f7ef5200e1835ee3c": "base"}, {}),
  A + "src/middleware/authenticate.ts":                             ({"be7102929b44f7567b0cab4ec1c82f84d04bc58e": "base"}, {}),
  A + "src/repositories/dbErrors.ts":                               ({"f94faf0d3d3540990f8626fcb65c746737202ac4": "base"}, {}),
  A + "src/services/subjectDeks.ts":                                ({"2d83a9ff54533cc3623ff119f005766a7a84e1b0": "base"}, {}),
  A + "src/services/passwordLoginGate.ts":                          ({"684b713758d859b9fca9df2e41e2a2f39cbf17df": "base"}, {}),
  A + "src/index.ts":                                               ({"edabbf87182311241662b20ac71d7244e923b5a3": "base"}, {}),
  D + "packages/shared/src/crypto/subjectDek.ts":                   ({"48c215dbb50d9879cd5f92b0492abe0eec6ef7c3": "base"}, {}),
  A + "package.json":                                               ({"814e88419470b811f26f1593984071bb317608d8": "base"}, {}),
  A + "vitest.config.ts":                                           ({"8bb96293a0f11a14d90e7c7893f32a053277bbdb": "base"}, {}),
  A + "vitest.setup.ts":                                            ({"bc18c18755cb00f96e3e228ca34d99fd1266c20f": "base"}, {}),
  A + "tsconfig.json":                                              ({"a7952bdeaf16e933432bb0e7136f484bb7288a40": "base"}, {}),
  D + "eslint.config.mjs":                                          ({"8c5374c6022eb0a3f449f41a570db61294aa63f1": "base"}, {}),
  D + "docs/openapi/secuura-api.yaml":                              ({"122d3a2f84cf77bf2b7e2dc51489a0d5f823db1f": "base"}, {}),
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
        print("LANDED develop " + short + " blob " + blob[:9] + " = " + landed[blob] + " — #1013 has landed; this brief is stale"); sys.exit(0)
    if blob not in ok:
        print("GUARDED develop " + short + " blob " + blob[:9] + " — a version nobody pinned"); sys.exit(0)
    state.append(f.split("/")[-1] + " " + blob[:9] + " = " + ok[blob])
state = "; ".join(state)
if cur == pinned:
    print("OK " + state + " | origin develop still " + pinned + " (= the PR parent: the merged tree is content-identical to the head until develop moves; git ls-remote)"); sys.exit(0)
try:
    c = get("/compare/" + pinned + "..." + cur)
except Exception as e:
    print("UNJUDGEABLE compare unreadable: " + type(e).__name__); sys.exit(0)
files = c.get("files") or []
if c.get("status") != "ahead" or len(files) > 250:
    print("UNJUDGEABLE status=%s files=%d" % (c.get("status"), len(files))); sys.exit(0)
GUARDED = [A + "src/",
           A + "package.json",
           A + "vitest.config.ts",
           A + "vitest.setup.ts",
           A + "tsconfig.json",
           D + "packages/shared/src/crypto/",
           D + "docs/openapi/",
           D + "eslint.config.mjs",
           D + "package-lock.json"]
# STYLE NOTE (912r2 launcher, measured): bash scans quote/paren state THROUGH this heredoc because it sits inside a
# command substitution — keep apostrophes and parentheses EVEN (this block uses none of the former), or the outer $( ) breaks.
# CONTENT-JUDGED allowlist: a hit under a GUARDED path clears ONLY if the per-file blob sha in the compare is EXACTLY one
# pinned here. EMPTY for this gate: at draft time 04:48 AEST the open PRs touching a guarded path were dependabot bumps of
# services/auth/package.json and the Dev lockfile, which must NOT clear silently — every guarded hit falls through to GUARDED and exit 18.
DEV_CONTENT_ALLOWED = {
}
hits = sorted({x["filename"] for x in files for g in GUARDED if x["filename"] == g or (g.endswith("/") and x["filename"].startswith(g))})
by_name = {x["filename"]: x for x in files}
cleared = sorted(h for h in hits if h in DEV_CONTENT_ALLOWED and by_name.get(h, {}).get("sha") == DEV_CONTENT_ALLOWED[h])
remaining = sorted(h for h in hits if h not in cleared)
if remaining:
    print("GUARDED " + " ".join(remaining)); sys.exit(0)
tail = "the gate merges the then-current develop onto 5fbfb66a9 in its own clone, rebuilds the shared dist there, runs the auth suite and the route probe on the MERGED tree beside the base and head trees, names the delta and re-derives every count, above all the auth denominator (brief items 1, 6 and 11)"
print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d — disjoint from the GUARDED list (services/auth/src/ + the auth config files, packages/shared/src/crypto/, docs/openapi/, eslint.config.mjs, the Dev lockfile); %s" % (pinned, cur, c["ahead_by"], len(files), tail)); sys.exit(0)
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
grep -qF '[QA -> Wednesday] TIER 1 GATE #1013 (KS-999) 5fbfb66a9' "$PROMPT_FILE" && grep -qF 'coagent@agentmail.to' "$PROMPT_FILE" && grep -qF 'wednesday-agent@agentmail.to' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry the exact verdict subject, the coagent@ sender and the wednesday-agent@ recipient" >&2; exit 23; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  head on origin: #1013 $HEAD_SHA at $BRANCH"
  echo "  compare (GitHub API): develop...#1013 = $COMPARE"
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
  [ -n "${QA1013_CUR_DEV:-}" ] && echo "  (develop read from the QA1013_CUR_DEV test override, not ls-remote)"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"
  exit 0
fi

[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — this launcher execs an interactive agent; run it in a cockpit pane, never inside a Bash tool (a headless gate is invisible and dies with the caller's shell)" >&2; exit 21; }
[ -z "${QA1013_BRIEF:-}${QA1013_PROMPT:-}${QA1013_HEAD:-}${QA1013_CUR_DEV:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$DEV_NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
