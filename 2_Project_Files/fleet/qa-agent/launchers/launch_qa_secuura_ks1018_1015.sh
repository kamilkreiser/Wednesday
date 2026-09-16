#!/bin/bash
# launch_qa_secuura_ks1018_1015.sh — cross-project QA agent, ONE TIER 1 ROUND 1 gate over Secuura/Blockchain PR #1015
# (KS-1018, Seat A) @ 77145ce84353534ba381688d5bbd16ff9ff27aef — TWO commits on 523f283c6 (#1011's squash): 6e30fe9f5 (a held local-model
# READY applied byte-equal + seat cells) and 77145ce84 (typing of the test, declared casts only). 2 files, all services/auth:
# src/routes/users.ts +14 -4 (getVerificationRequest / findPendingVerificationRequest / listUserVerificationRequests log `DB <fn> failed`
# {error, code} and rethrow an infrastructure DB error as 503) and the NEW src/__tests__/ks1018-security-correctness-three-verification-
# store-reads.test.ts (+216). TIER 1: auth-service error classification on routes whose base behaviour under a DB fault is a WRITE.
#
# THE SHAPE, as read 06:28-06:41 AEST 2026-09-17 (git ls-remote + the compare API agree): develop = 523f283c6 = the grandparent of the
# head; compare develop...head = merge_base 523f283c6, ahead 2, behind 0, files 2. The compare is asserted as merge_base + ahead + files
# (exit 10); `behind` is deliberately NOT asserted — the develop arm judges every move by CONTENT.
#
# The develop pin is judged by CONTENT, not bare: (a) EIGHTEEN files by blob at the CURRENT develop — users.ts (base 89da72df7; the PR's
# own 8ef9065e2 -> exit 19 LANDED), the ks1018 test (ABSENT at base; the PR's own 6723276d0 or its commit-1 0fb3e7197 -> exit 19 LANDED),
# middleware errorHandler.ts / authenticate.ts, repositories dbErrors.ts / userRepo.ts, db.ts, src/index.ts, auth.openapi.ts, auth
# package.json / vitest.config.ts / vitest.setup.ts / tsconfig.json, Dev eslint.config.mjs, docs/openapi/secuura-api.yaml and the three
# schema sources (migrations/001, docker/init/03, deployment/azure/migrate/init.sql) — any blob nobody pinned -> exit 18; (b) if develop
# moved past 523f283c6, the compare pinned...develop REFUSES (exit 18) when the delta touches a GUARDED path — services/auth/src/, the
# auth config files, packages/shared/src/, docs/openapi/, eslint.config.mjs, the Dev lockfile, migrations/, docker/init/,
# deployment/azure/migrate/ — or cannot be judged. An api-gateway-only move (#1014 KS-1176, A9 KS-1072) proceeds: the gate names it.
# DEV_CONTENT_ALLOWED is empty: dependabot #948/#649/#575 touch services/auth/package.json and the Dev lockfile — if one lands, re-pin deliberately.
#
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool — and never run it without --check to "prove" this guard. `--check` runs headless (it launches nothing).
# exit 22: the prompt must require node_modules farmed PER ENTRY (the #1009 gate's R-6: a wholesale link can write through to the checkout's .vite).
# exit 23: the prompt must carry the exact verdict subject and name coagent@ as the sender and wednesday-agent@ as the recipient.
# QA1015_BRIEF / QA1015_PROMPT / QA1015_HEAD / QA1015_CUR_DEV (test overrides, --check only): a launch with any set refuses (exit 16).
#
# Generated from launch_qa_secuura_ks999_1013.sh (the #1013 gate's launcher, verdict GO WITH FINDINGS) by gen_launcher_1015.py
# (asserted substitutions + residual guard + bash -n): same guards and exit codes, re-pointed at #1015. Exit codes 2..23 (19 = LANDED).
#
# Usage: launch_qa_secuura_ks1018_1015.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..23 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QA1015_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1015-ks1018-tier1.md}"
PROMPT_FILE="${QA1015_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1015-ks1018-tier1.prompt.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
BRANCH='refs/heads/feature/ks-1018-ornith-verification-store-reads-rethrow-infra'
HEAD_SHA="${QA1015_HEAD:-77145ce84353534ba381688d5bbd16ff9ff27aef}"
MERGE_BASE='523f283c6cd2550263ec9869dc5ee722be40df4e'   # the merge-base of the head with develop = the parent of commit 1, 523f283c6 (#1011's squash)
DEVELOP_SHA='523f283c6cd2550263ec9869dc5ee722be40df4e'   # develop at draft time = the merge-base (git ls-remote 06:28:52 and 06:40:55, branches API 06:31:06 AEST)
REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1015-ks1018-tier1.md"

[ -d "$QA_DIR" ]         || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]          || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ]    || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]           || { echo "repo under test missing: $REPO" >&2; exit 5; }

# The head, pinned at its branch on origin (one ls-remote at run time).
LSR="$(git -C "$REPO" ls-remote origin "$BRANCH")"
if ! printf '%s\n' "$LSR" | grep -q "^${HEAD_SHA}[[:space:]]${BRANCH}\$"; then
  echo "REFUSING: #1015 — $HEAD_SHA is not at $BRANCH on origin — the head moved; the brief is about a different SHA" >&2
  printf '%s\n' "$LSR" >&2
  exit 6
fi

# The compare (GitHub compare API), asserted whole (merge_base + ahead + files; NOT behind — see the header):
# develop...#1015 = 523f283c6 ahead 2 files 2 (behind 0 at draft time; behind deliberately not asserted).
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
[ "$COMPARE" = "$MERGE_BASE ahead=2 files=2" ] || { echo "REFUSING: #1015 develop...head reads '$COMPARE', brief pins '$MERGE_BASE ahead=2 files=2'" >&2; exit 10; }

# The develop pin, judged by CONTENT (see the header): eighteen files by blob at the CURRENT develop, then — if develop
# moved — the pinned...develop delta against the GUARDED list with the DEV_CONTENT_ALLOWED blobs cleared.
CUR_DEV="${QA1015_CUR_DEV:-$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)}"
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
  A + "src/routes/users.ts":                                                         ({"89da72df7bfab2275550de0868288b7958ea059c": "base"}, {"8ef9065e2fb24308daeb41820a227a4ee1d6ecc9": "#1015 own"}),
  A + "src/__tests__/ks1018-security-correctness-three-verification-store-reads.test.ts": ({"ABSENT": "base"}, {"6723276d016e4d6cf4ead8cb4f511ce5dad5ce53": "#1015 own", "0fb3e7197d5195608ff7decece9a4b766215095e": "#1015 commit-1 own"}),
  A + "src/middleware/errorHandler.ts":                                              ({"1cf66e74cd2bbe1d56f53c6f7ef5200e1835ee3c": "base"}, {}),
  A + "src/repositories/dbErrors.ts":                                                ({"f94faf0d3d3540990f8626fcb65c746737202ac4": "base"}, {}),
  A + "src/repositories/userRepo.ts":                                                ({"9060b308e6d6a82c8a79be7387032d2a18c4ac22": "base"}, {}),
  A + "src/db.ts":                                                                   ({"cf0ee130bb5228214a41e163b3be766b8aebbb72": "base"}, {}),
  A + "src/middleware/authenticate.ts":                                              ({"be7102929b44f7567b0cab4ec1c82f84d04bc58e": "base"}, {}),
  A + "src/index.ts":                                                                ({"edabbf87182311241662b20ac71d7244e923b5a3": "base"}, {}),
  A + "src/auth.openapi.ts":                                                         ({"2c356c3c7877add99f5e1a3c437d04ac8be3dc76": "base"}, {}),
  A + "package.json":                                                                ({"814e88419470b811f26f1593984071bb317608d8": "base"}, {}),
  A + "vitest.config.ts":                                                            ({"8bb96293a0f11a14d90e7c7893f32a053277bbdb": "base"}, {}),
  A + "vitest.setup.ts":                                                             ({"bc18c18755cb00f96e3e228ca34d99fd1266c20f": "base"}, {}),
  A + "tsconfig.json":                                                               ({"a7952bdeaf16e933432bb0e7136f484bb7288a40": "base"}, {}),
  D + "eslint.config.mjs":                                                           ({"8c5374c6022eb0a3f449f41a570db61294aa63f1": "base"}, {}),
  D + "docs/openapi/secuura-api.yaml":                                               ({"122d3a2f84cf77bf2b7e2dc51489a0d5f823db1f": "base"}, {}),
  D + "migrations/001_initial-schema.sql":                                           ({"271c42237e70f0fa9664ccdb5151a276e8b89157": "base"}, {}),
  D + "docker/init/03-service-tables.sql":                                           ({"9a6394ceb9389a17c9e177b3182b7612286f3c54": "base"}, {}),
  D + "deployment/azure/migrate/init.sql":                                           ({"f06d1882fcd23ce3d945c7ea16e5423b57279f0f": "base"}, {}),
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
        print("LANDED develop " + short + " blob " + blob[:9] + " = " + landed[blob] + " — #1015 has landed; this brief is stale"); sys.exit(0)
    if blob not in ok:
        print("GUARDED develop " + short + " blob " + blob[:9] + " — a version nobody pinned"); sys.exit(0)
    state.append(f.split("/")[-1] + " " + blob[:9] + " = " + ok[blob])
state = "; ".join(state)
if cur == pinned:
    print("OK " + state + " | origin develop still " + pinned + " (= the merge-base: the merged tree is content-identical to the head until develop moves; git ls-remote)"); sys.exit(0)
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
           D + "packages/shared/src/",
           D + "docs/openapi/",
           D + "eslint.config.mjs",
           D + "migrations/",
           D + "docker/init/",
           D + "deployment/azure/migrate/",
           D + "package-lock.json"]
# STYLE NOTE (912r2 launcher, measured): bash scans quote/paren state THROUGH this heredoc because it sits inside a
# command substitution — keep apostrophes and parentheses EVEN (this block uses none of the former), or the outer $( ) breaks.
# CONTENT-JUDGED allowlist: a hit under a GUARDED path clears ONLY if the per-file blob sha in the compare is EXACTLY one
# pinned here. EMPTY for this gate: at draft time 06:31 AEST the open PRs touching a guarded path were dependabot bumps of
# services/auth/package.json and the Dev lockfile, which must NOT clear silently — every guarded hit falls through to GUARDED and exit 18.
DEV_CONTENT_ALLOWED = {
}
hits = sorted({x["filename"] for x in files for g in GUARDED if x["filename"] == g or (g.endswith("/") and x["filename"].startswith(g))})
by_name = {x["filename"]: x for x in files}
cleared = sorted(h for h in hits if h in DEV_CONTENT_ALLOWED and by_name.get(h, {}).get("sha") == DEV_CONTENT_ALLOWED[h])
remaining = sorted(h for h in hits if h not in cleared)
if remaining:
    print("GUARDED " + " ".join(remaining)); sys.exit(0)
tail = "the gate merges the then-current develop onto 77145ce84 in its own clone, rebuilds the shared dist there, runs the auth suite and the route probe on the MERGED tree beside the base and head trees, names the delta and re-derives every count, above all the auth denominator (brief items 1, 7 and 10)"
print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d — disjoint from the GUARDED list (services/auth/src/ + the auth config files, packages/shared/src/, docs/openapi/, eslint.config.mjs, the Dev lockfile, migrations/, docker/init/, deployment/azure/migrate/); %s" % (pinned, cur, c["ahead_by"], len(files), tail)); sys.exit(0)
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
grep -qF '[QA -> Wednesday] TIER 1 GATE #1015 (KS-1018) 77145ce84' "$PROMPT_FILE" && grep -qF 'coagent@agentmail.to' "$PROMPT_FILE" && grep -qF 'wednesday-agent@agentmail.to' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry the exact verdict subject, the coagent@ sender and the wednesday-agent@ recipient" >&2; exit 23; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  head on origin: #1015 $HEAD_SHA at $BRANCH"
  echo "  compare (GitHub API): develop...#1015 = $COMPARE"
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
  [ -n "${QA1015_CUR_DEV:-}" ] && echo "  (develop read from the QA1015_CUR_DEV test override, not ls-remote)"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"
  exit 0
fi

[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — this launcher execs an interactive agent; run it in a cockpit pane, never inside a Bash tool (a headless gate is invisible and dies with the caller's shell)" >&2; exit 21; }
[ -z "${QA1015_BRIEF:-}${QA1015_PROMPT:-}${QA1015_HEAD:-}${QA1015_CUR_DEV:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$DEV_NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
