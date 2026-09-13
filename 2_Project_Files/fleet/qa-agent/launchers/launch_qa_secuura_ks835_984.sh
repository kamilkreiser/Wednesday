#!/bin/bash
# launch_qa_secuura_ks835_984.sh — cross-project QA agent, TIER 1 (an auth door: what an OAuth-minted bearer CARRIES —
# `scopes`, `authMethod` — and what the api-gateway's scope gate does with it; through code AND live on real in-process
# loopback listeners, no stack) gate ROUND 1 on Secuura PR #984 (KS-835) @ d00a2015c: the consent grant now reaches the
# token. jwt.ts: OAuthMintOptions.scopes REQUIRED, OAuthTokenClaims.authMethod?: 'oauth', the access (:205) and refresh
# (:229) mints carry `{ scopes: [...oauth.scopes], authMethod: 'oauth' }` for an OAuth mint and the role default with no
# label for a login mint; oauth.ts: the code grant passes parseScopeString(result.scope || '') (:848), the refresh grant
# re-mints decoded.scopes ?? [] (:954); api-gateway scopes.ts: the attachScopes docblock only (no behaviour change);
# the lane's ks823 test states a grant in its mint helper; two NEW tests (auth 5 cells raw socket + real jwt.ts;
# gateway 6 cells, all controls, on a 127.0.0.1 listener). Six files +398 -25 over the STACK PARENT. Round 1 on this PR.
#
# THE STACKED SHAPE. #984 is the THIRD commit of a stack on origin develop M18 8861e6216: #982 (KS-790, e62eab87a) ->
# #983 (KS-823, f62c975c1) -> #984 (KS-835, d00a2015c). All three PRs have base develop (GitHub, 07:15 AEST 2026-09-14).
# The gate judges #984's OWN delta against its STACK PARENT f62c975c1 (six files) AND the merged shape: develop is an
# ANCESTOR of the head (0 behind / 3 ahead), so the head tree 39ab0226a IS the stack merged onto live develop — the
# full auth (53/707) and gateway (35/349) suites and the ks860 loopback guard run on it. The "merge-base" pin of the
# template is therefore the STACK-PARENT pin here: the GitHub compare f62c975c1...d00a2015c must read merge_base
# f62c975c1, ahead 1, SIX files (exit 10). The merge seat is queued to squash #982 then #983 onto develop before #984;
# when those land, develop's copies of jwt.ts and oauth.ts CHANGE — EXPECTED, not a hit — so the develop guard judges a
# move by CONTENT, on TWO files (GitHub contents API): jwt.ts blob d0d55c11b (M18's = #982's; #982 does not touch it)
# or 62b6db272 (#983 landed) -> green; 26562a224 (#984's own) -> exit 19, the PR has landed and there is nothing to
# gate; any other blob -> exit 18. oauth.ts blob 4b03f555e (M18) / 80e05458e (#982 landed) / de00ffcea (#983 landed) ->
# green; 0bab1b8bd (#984's own) -> exit 19; any other -> exit 18. Any OTHER file of the move under the GUARDED list —
# routes/proxy.ts (the seven scope-gated mounts), gateway middleware/auth.ts (:370 copies the claims), gateway
# middleware/scopes.ts (#984's own comment-only file), services/enforcement.ts and middleware/rateLimitEnforce.ts (the
# label's other consumers), services/auth/src/routes/auth.ts (POST /api/auth/refresh — the brief's H-launder),
# services/auth/src/services/oauth.ts and types/index.ts, packages/shared/src/security/scopes.ts (the role defaults),
# the ks860 loopback guard file — -> exit 18; the auth/gateway __tests__ moved by #982/#983 landing are NOT guarded;
# otherwise the launcher proceeds and prints the move, which the gate re-states (brief TARGET: develop's own count + 22
# auth / + 6 gateway, 0 failed). If #982/#983 merge before the gate finishes, the PR's GitHub delta shrinks; the verdict
# is on head d00a2015c regardless, and the brief says so.
#
# origin develop at pin time: 8861e6216 (M18, #980's squash, 12:00:26Z 2026-09-13; read 07:09:19 and 07:15:57 AEST
# 2026-09-14) — unmoved since the builder's cut.
#
# Adapted from launch_qa_secuura_ks828_900_981.sh by gen_launcher_984.py (asserted substitutions, TWO asserted block
# replacements — the two-file blob-judged develop guard and the --check block — three asserted insertions: the exit-20
# head-SHA-in-both guard (from the #980 round-2 template), the exit-21 stdin-is-not-a-TTY guard (the 2026-09-13 ledger:
# a QA launcher run inside a Bash tool execs claude HEADLESS, parented to the caller's shell; --check stays headless-
# safe), the TIER 1 wording; residual guard): the same guards and exit codes plus 20 and 21, re-pointed at #984.
#
# Written by the generator because it contains a legitimate `cd`.
#
# Usage: launch_qa_secuura_ks835_984.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..21 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QA984_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-14_secuura-984-ks835-tier1.md}"
PROMPT_FILE="${QA984_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-14_secuura-984-ks835-tier1.prompt.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
BRANCH='refs/heads/feature/ks-835-security-oauth-consent-is-decorative-the-granted-scope-never'
HEAD_SHA="${QA984_HEAD:-d00a2015c89a4720eaeab64482bbd9b89d878024}"
STACK_PARENT='f62c975c11ec97cdef04500fd98a43618e702763'
DEVELOP_SHA='8861e62161466c40f08d2b10a30edeb203123993'
JWT_FILE='Blockchain/Dev/services/auth/src/services/jwt.ts'
OAUTH_FILE='Blockchain/Dev/services/auth/src/routes/oauth.ts'
JWT_BLOBS_OK='d0d55c11beab2bfd8f8140e12de4016cac742134 62b6db272c911557d764ee2f0e77f1df26923426'   # M18 (= #982's) · #983 landed
JWT_BLOB_HEAD='26562a22470af688ae733000792a2b0321650145'                                             # #984's own -> landed
OAUTH_BLOBS_OK='4b03f555e25bf1221081fdd38f530b983cc763e0 80e05458e9759fbc6c7f33bc8cd90060d30e6149 de00ffceaccd8155349e8de10aaeab3a94c33529'   # M18 · #982 · #983
OAUTH_BLOB_HEAD='0bab1b8bdd7c9cb2b085bf94d5487a308eb51dd0'                                           # #984's own -> landed
REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-14_secuura-984-ks835-tier1.md"

[ -d "$QA_DIR" ]         || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]          || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ]    || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]           || { echo "repo under test missing: $REPO" >&2; exit 5; }

if ! git -C "$REPO" ls-remote origin "$BRANCH" | grep -q "^${HEAD_SHA}[[:space:]]"; then
  echo "REFUSING: $HEAD_SHA is not at $BRANCH on origin — the head moved; the brief is about a different SHA" >&2
  git -C "$REPO" ls-remote origin "$BRANCH" >&2
  exit 6
fi

# The STACK-PARENT pin: the judged delta is STACK_PARENT...HEAD and must be exactly ONE commit on SIX files.
STACK_READ="$(
  set -a; . "$SECUURA_ENV"; set +a
  HEAD_SHA="$HEAD_SHA" STACK_PARENT="$STACK_PARENT" python3 - <<'PY'
import json, os, urllib.request
t = os.environ.get("GH_TOKEN", "")
u = "https://api.github.com/repos/Secuura/Distributed_Secuura/compare/" + os.environ["STACK_PARENT"] + "..." + os.environ["HEAD_SHA"]
r = urllib.request.urlopen(urllib.request.Request(u, headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}), timeout=60)
c = json.load(r)
print("%s ahead=%d files=%d" % (c["merge_base_commit"]["sha"], c["ahead_by"], len(c.get("files") or [])))
PY
)"
[ -n "$STACK_READ" ] || { echo "REFUSING: could not read the stack-parent compare from the GitHub compare API" >&2; exit 13; }
[ "$STACK_READ" = "$STACK_PARENT ahead=1 files=6" ] \
  || { echo "REFUSING: the judged delta is not ONE commit on SIX files over the stack parent: compare reads '$STACK_READ', brief pins '$STACK_PARENT ahead=1 files=6'" >&2; exit 10; }

# The develop pin, judged by CONTENT (see the header). jwt.ts and oauth.ts are judged by their blob SHAs on develop
# (#982/#983 landing moves them — expected); GUARDED = the OTHER files whose movement changes this brief's expectations.
CUR_DEV="$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)"
[ -n "$CUR_DEV" ] || { echo "REFUSING: could not read origin develop (git ls-remote)" >&2; exit 18; }
DEV_JUDGEMENT="$(
  set -a; . "$SECUURA_ENV"; set +a
  DEVELOP_SHA="$DEVELOP_SHA" CUR_DEV="$CUR_DEV" JWT_FILE="$JWT_FILE" OAUTH_FILE="$OAUTH_FILE" \
  JWT_BLOBS_OK="$JWT_BLOBS_OK" JWT_BLOB_HEAD="$JWT_BLOB_HEAD" OAUTH_BLOBS_OK="$OAUTH_BLOBS_OK" OAUTH_BLOB_HEAD="$OAUTH_BLOB_HEAD" python3 - <<'PYJ'
import json, os, sys, urllib.request
t = os.environ.get("GH_TOKEN", "")
api = "https://api.github.com/repos/Secuura/Distributed_Secuura"
def get(p):
    return json.load(urllib.request.urlopen(urllib.request.Request(api + p, headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}), timeout=60))
jwt_f = os.environ["JWT_FILE"]; oauth_f = os.environ["OAUTH_FILE"]; cur = os.environ["CUR_DEV"]; pinned = os.environ["DEVELOP_SHA"]
jwt_ok = os.environ["JWT_BLOBS_OK"].split(); oauth_ok = os.environ["OAUTH_BLOBS_OK"].split()
try:
    jwt_blob = get("/contents/" + jwt_f + "?ref=" + cur)["sha"]
    oauth_blob = get("/contents/" + oauth_f + "?ref=" + cur)["sha"]
except Exception as e:
    print("UNJUDGEABLE develop blob unreadable: " + type(e).__name__); sys.exit(0)
def name(blob, ok, head, labels):
    if blob == head: return "LANDED"
    if blob in ok: return labels[ok.index(blob)]
    return "OTHER"
jn = name(jwt_blob, jwt_ok, os.environ["JWT_BLOB_HEAD"], ["M18 (= #982's; #982 does not touch it)", "#983 landed"])
on = name(oauth_blob, oauth_ok, os.environ["OAUTH_BLOB_HEAD"], ["M18", "#982 landed", "#983 landed"])
if jn == "LANDED" or on == "LANDED":
    print("LANDED984 develop's jwt.ts blob " + jwt_blob[:9] + " / oauth.ts blob " + oauth_blob[:9] + " = #984's own — the PR has landed; nothing to gate"); sys.exit(0)
if jn == "OTHER" or on == "OTHER":
    print("GUARDED develop's jwt.ts blob " + jwt_blob[:9] + " (" + jn + ") / oauth.ts blob " + oauth_blob[:9] + " (" + on + ") — a version nobody pinned (neither M18's, #982's, #983's nor #984's)"); sys.exit(0)
state = "develop's jwt.ts blob " + jwt_blob[:9] + " = " + jn + "; oauth.ts blob " + oauth_blob[:9] + " = " + on + " (the head tree is unchanged by a stack landing; the verdict stays on the head)"
if cur == pinned:
    print("OK " + state + " | origin develop still " + pinned + " (M18; git ls-remote)"); sys.exit(0)
try:
    c = get("/compare/" + pinned + "..." + cur)
except Exception as e:
    print("UNJUDGEABLE compare unreadable: " + type(e).__name__); sys.exit(0)
files = c.get("files") or []
if c.get("status") != "ahead" or len(files) > 250:
    print("UNJUDGEABLE status=%s files=%d" % (c.get("status"), len(files))); sys.exit(0)
GUARDED = ["Blockchain/Dev/services/api-gateway/src/routes/proxy.ts",
           "Blockchain/Dev/services/api-gateway/src/middleware/auth.ts",
           "Blockchain/Dev/services/api-gateway/src/middleware/scopes.ts",
           "Blockchain/Dev/services/api-gateway/src/services/enforcement.ts",
           "Blockchain/Dev/services/api-gateway/src/middleware/rateLimitEnforce.ts",
           "Blockchain/Dev/services/auth/src/routes/auth.ts",
           "Blockchain/Dev/services/auth/src/services/oauth.ts",
           "Blockchain/Dev/services/auth/src/types/index.ts",
           "Blockchain/Dev/packages/shared/src/security/scopes.ts",
           "Blockchain/Dev/packages/shared/src/__tests__/ks860-test-listeners-bind-loopback.test.ts"]
hits = sorted({x["filename"] for x in files if x["filename"] not in (jwt_f, oauth_f) for g in GUARDED if x["filename"] == g or (g.endswith("/") and x["filename"].startswith(g))})
if hits:
    print("GUARDED " + " ".join(hits)); sys.exit(0)
auth_tests = sum(1 for x in files if x["filename"].startswith("Blockchain/Dev/services/auth/src/__tests__/"))
gw_tests = sum(1 for x in files if x["filename"].startswith("Blockchain/Dev/services/api-gateway/src/__tests__/"))
print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d (auth __tests__ %d, gateway __tests__ %d) — disjoint from the two judged files (by blob) and the ten GUARDED paths; the gate re-reads develop at start and end and re-derives the full-suite counts on the merged tree (brief TARGET: develop's own + 22 auth / + 6 gateway, 0 failed)" % (pinned, cur, c["ahead_by"], len(files), auth_tests, gw_tests)); sys.exit(0)
PYJ
)"
case "$DEV_JUDGEMENT" in
  OK*) DEV_NOTE="${DEV_JUDGEMENT#OK }" ;;
  LANDED984*) echo "REFUSING: ${DEV_JUDGEMENT#LANDED984 } (develop $CUR_DEV)" >&2; exit 19 ;;
  *) echo "REFUSING: origin develop is at $CUR_DEV (pinned $DEVELOP_SHA) and the move is not provably disjoint: ${DEV_JUDGEMENT:-no judgement} — confirm the delta, re-state the ratio, then re-pin deliberately (launcher DEVELOP_SHA/*_BLOBS_OK + brief TARGET + prompt)" >&2
     exit 18 ;;
esac

grep -q 'TIER 1' "$BRIEF" && grep -q 'TIER 1' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the tier" >&2; exit 7; }
grep -q 'ROUND 1' "$BRIEF" && grep -q 'ROUND 1' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the round" >&2; exit 15; }
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
  echo "  head $HEAD_SHA present at $BRANCH on origin"
  echo "  stack parent still $STACK_PARENT and the judged delta is ONE commit on SIX files (GitHub compare API)"
  echo "  $DEV_NOTE"
  echo "  brief, prompt, QA project and repo all present"
  echo "  brief and prompt agree on TIER 1 and ROUND 1"
  echo "  prompt opens with the thinking directive and names the brief"
  echo "  brief and prompt both name the head SHA $HEAD_SHA"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  exit 0
fi

# The launch path execs an INTERACTIVE agent: it needs a pane. A launcher run inside a Bash tool inherits no TTY,
# execs claude headless, parented to the caller's shell, invisible to Kam, and dies at that seat's rotation
# (2026-09-13 ledger, the #962 gate). --check above is the headless-safe path; the launch refuses without a TTY.
[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — this launcher execs an interactive agent and must run in a pane (cockpit.sh add / a terminal); use --check for a headless guard run" >&2; exit 21; }
[ -z "${QA984_BRIEF:-}${QA984_PROMPT:-}${QA984_HEAD:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$DEV_NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
