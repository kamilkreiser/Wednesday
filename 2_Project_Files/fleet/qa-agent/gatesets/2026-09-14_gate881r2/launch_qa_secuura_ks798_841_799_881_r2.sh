#!/bin/bash
# launch_qa_secuura_ks798_841_799_881_r2.sh — cross-project QA agent, TIER 1 (an auth surface: the OAuth consent page —
# a rendered page that authenticates a user and mints an authorization code; through code AND live in the gate's own
# Express apps: the product's real CSRF middleware, a real proxy front, jsdom driving the page) gate, ROUND 2 of the PR
# (round 1 was Peter Obeden's human review — CHANGES_REQUESTED on KS-799 only; there is NO round-1 QA report), on
# Secuura PR #881 (KS-798 / KS-841 / KS-799) @ 8ac9db66f — FIVE commits: Peter's head 787771b97 (3 commits, 2026-09-06)
# + the FIX ffcea35cb (parent 787771b97, tree 12dd42b2e, THREE files: oauth.ts +105 -57 blob 01c2d320f -> ffb573842,
# ks799-consent-script-csp-and-execution.test.ts NEW 414 lines blob 995ee34ce, ks799-consent-form-csrf-submit.test.ts
# +21 -10 blob 08803feb2 -> a83594c38) + the MERGE 8ac9db66f (parents ffcea35cb + origin develop M18 8861e6216, tree
# 136e6c8cc = `git merge-tree --write-tree 8861e6216 ffcea35cb` EXACTLY — the mechanical union; Wednesday's YES
# 13:33:35Z after the 09-07 branch's first push was refused by its own stale audit legs 6/7). PR files API: 6 files
# +1095 -24 vs develop (the three above + ks798-*, ks841-*, ks781-n1-* — Peter's signed-off bytes, blob-identical to
# 787771b97).
#
# Why a round 2: Peter measured that the round-1 inline <script> is refused by script-src 'self' as the browser sees it
# through the proxy (helmet on the auth service replaces the gateway's 'unsafe-inline' via http-proxy's setHeader), so
# the page fell back to the native headerless POST -> 403 CSRF_TOKEN_MISSING, the very symptom KS-799 exists to remove.
# s212 delivered Peter's option (2): the script bytes moved verbatim to CONSENT_SUBMIT_SCRIPT served by
# GET /api/oauth/consent.js (application/javascript, no-store) and the page carries <script src>; plus his "executing
# test" (jsdom clicks Authorize through the served script). No CSP header authored, no CSRF exemption, index.ts untouched.
#
# The gate establishes: (1) the delta is EXACTLY the three fix files and the merge is the union (tree-sha equality);
# (2) RED-FIRST in the gate's clone — the final test bytes against r1's oauth.ts red C1/C2/C4/the text cell
# `4 failed | 8 passed (12)` with C1 naming script-src 'self', head bytes 12/12, the five PR files 5/24/24, the auth suite
# 54/703 at head (= the merged tree on M18); (3) the tamper table suite RUNNING — T1/T2/T3 (3/3/2) + gate-designed
# Tg-A (1: C2 only — jsdom ignores the media type), Tg-B (6: C1 blind to a tag that never runs), Tg-C (3), Tg-D (5);
# (4) LIVE legs in the gate's own Express apps: G1 the gateway's REAL createCsrfMiddleware in front of the real router
# (200 {redirect} with the page's request shape; 403 CSRF_TOKEN_MISSING without the header; 403 CSRF_ORIGIN_INVALID on a
# foreign origin — Peter's #1 measured as a mechanism), G2 the gateway's real specRouteMap on the unlisted path (falls
# through), G3 the real router behind a real http-proxy front carrying the gateway's CSP (script-src 'self' as the
# browser sees it; the script fetched THROUGH the front; the click sends the two headers); (5) the widened-guard rule
# (full packages/shared at head, ks860 loopback cell green); (6) Peter answered point by point; delivered-vs-
# commissioned; findings-only; NOT-TESTED at equal prominence.
#
# Merge-base = origin develop M18 8861e6216 ITSELF (develop is an ancestor of the head; GitHub compare develop...head:
# ahead 5 / behind 0, 6 files — exit 10 if the merge-base changes). origin develop = M18 8861e6216 (the newest develop
# squash, 12:00:26Z 09-13; read 07:10 and 07:15 AEST 2026-09-14). The develop pin below is DISJOINTNESS-CHECKED, not bare: if
# origin develop has moved past M18, the GitHub compare of that delta is read and the launcher REFUSES (exit 18) only
# when the delta touches a GUARDED path — the six PR files, anything under Blockchain/Dev/services/auth/ (the 703
# ratio and the merge shape), the four api-gateway files the live legs mount or read (csrf.ts, specRouteMap.ts,
# index.ts, routes/proxy.ts), the production nginx conf, the OpenAPI spec, anything under
# Blockchain/Dev/packages/shared/src/__tests__/ (the walking guards), or the root lockfile — or cannot be judged
# (unreadable, not ahead, >250 files); otherwise it proceeds printing the move and its file count, which the gate
# re-states and merges onto (brief items 1, 2, 3, 7). A refusal means: confirm the new delta, then re-pin DEVELOP_SHA
# here AND in the brief's TARGET section AND the prompt — a different brief, a deliberate edit.
#
# Adapted from the #980 round-2 launcher by gen_launcher_881r2.py (asserted substitutions + one asserted insertion,
# residual guard): the same guard family and exit codes 2..20, re-pointed at #881 round 2 (exit 19 = the round-1 READ —
# Peter's review 5140256072 + his comment 5583115315 on disk — named in the brief AND present; exit 20 = the full head
# SHA in both brief and prompt), PLUS exit 21 = stdin is not a TTY on a real launch (--check is exempt: it launches
# nothing). A gate launched inside a Bash tool runs headless, parented to the caller's shell, invisible to Kam, and
# dies at the caller's rotation (2026-09-13 ledger) — this launcher refuses that.
#
# Written by the generator because it contains a legitimate `cd`.
#
# Usage: launch_qa_secuura_ks798_841_799_881_r2.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..21 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QA881R2_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-14_secuura-881-ks798-841-799-tier1-r2.md}"
PROMPT_FILE="${QA881R2_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-14_secuura-881-ks798-841-799-tier1-r2.prompt.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
BRANCH='refs/heads/feature/ks-798-the-consent-page-posts-the-redirect-uri-in-the-client_id'
HEAD_SHA="${QA881R2_HEAD:-8ac9db66f6fd0d751f74ecc95bb314210a31ec52}"
MERGE_BASE='8861e62161466c40f08d2b10a30edeb203123993'
DEVELOP_SHA='8861e62161466c40f08d2b10a30edeb203123993'
REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-14_secuura-881-ks798-841-799-tier1-r2.md"

[ -d "$QA_DIR" ]         || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]          || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ]    || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]           || { echo "repo under test missing: $REPO" >&2; exit 5; }

if ! git -C "$REPO" ls-remote origin "$BRANCH" | grep -q "^${HEAD_SHA}[[:space:]]"; then
  echo "REFUSING: $HEAD_SHA is not at $BRANCH on origin — the head moved; the brief is about a different SHA" >&2
  git -C "$REPO" ls-remote origin "$BRANCH" >&2
  exit 6
fi

ACTUAL_MB="$(
  set -a; . "$SECUURA_ENV"; set +a
  HEAD_SHA="$HEAD_SHA" python3 - <<'PY'
import json, os, urllib.request
t = os.environ.get("GH_TOKEN", "")
u = "https://api.github.com/repos/Secuura/Distributed_Secuura/compare/develop..." + os.environ["HEAD_SHA"]
r = urllib.request.urlopen(urllib.request.Request(u, headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}))
print(json.load(r)["merge_base_commit"]["sha"])
PY
)"
[ -n "$ACTUAL_MB" ] || { echo "REFUSING: could not read the merge-base from the GitHub compare API" >&2; exit 13; }
[ "$ACTUAL_MB" = "$MERGE_BASE" ] || { echo "REFUSING: merge-base is now '$ACTUAL_MB', brief says '$MERGE_BASE'" >&2; exit 10; }

# The develop pin, disjointness-checked (see the header). GUARDED = the files whose movement changes this brief.
CUR_DEV="$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)"
[ -n "$CUR_DEV" ] || { echo "REFUSING: could not read origin develop (git ls-remote)" >&2; exit 18; }
if [ "$CUR_DEV" = "$DEVELOP_SHA" ]; then
  DEV_NOTE="origin develop still $DEVELOP_SHA (M18, the develop this brief's 54/703 was written against and the head already contains; git ls-remote)"
else
  DEV_JUDGEMENT="$(
    set -a; . "$SECUURA_ENV"; set +a
    DEVELOP_SHA="$DEVELOP_SHA" CUR_DEV="$CUR_DEV" python3 - <<'PYJ'
import json, os, sys, urllib.request
t = os.environ.get("GH_TOKEN", "")
u = "https://api.github.com/repos/Secuura/Distributed_Secuura/compare/" + os.environ["DEVELOP_SHA"] + "..." + os.environ["CUR_DEV"]
try:
    c = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}), timeout=60))
except Exception as e:
    print("UNJUDGEABLE compare unreadable: " + type(e).__name__); sys.exit(0)
files = c.get("files") or []
if c.get("status") != "ahead" or len(files) > 250:
    print("UNJUDGEABLE status=%s files=%d" % (c.get("status"), len(files))); sys.exit(0)
GUARDED = ["Blockchain/Dev/services/auth/src/routes/oauth.ts",
           "Blockchain/Dev/services/auth/src/__tests__/ks799-consent-script-csp-and-execution.test.ts",
           "Blockchain/Dev/services/auth/src/__tests__/ks799-consent-form-csrf-submit.test.ts",
           "Blockchain/Dev/services/auth/src/__tests__/ks798-consent-form-client-id.test.ts",
           "Blockchain/Dev/services/auth/src/__tests__/ks841-consent-form-pkce-and-client-id.test.ts",
           "Blockchain/Dev/services/auth/src/__tests__/ks781-n1-empty-mfacode-treated-as-absent.test.ts",
           "Blockchain/Dev/services/auth/",
           "Blockchain/Dev/services/api-gateway/src/middleware/csrf.ts",
           "Blockchain/Dev/services/api-gateway/src/specRouteMap.ts",
           "Blockchain/Dev/services/api-gateway/src/index.ts",
           "Blockchain/Dev/services/api-gateway/src/routes/proxy.ts",
           "Blockchain/Dev/docker/nginx-gateway/nginx-production.conf",
           "Blockchain/Dev/docs/openapi/secuura-api.yaml",
           "Blockchain/Dev/packages/shared/src/__tests__/",
           "Blockchain/Dev/package-lock.json"]
hits = sorted({f["filename"] for f in files for g in GUARDED if f["filename"] == g or (g.endswith("/") and f["filename"].startswith(g))})
if hits:
    print("GUARDED " + " ".join(hits)); sys.exit(0)
print("DISJOINT commits=%d files=%d" % (c["ahead_by"], len(files)))
PYJ
  )"
  case "$DEV_JUDGEMENT" in
    DISJOINT*) DEV_NOTE="origin develop MOVED $DEVELOP_SHA -> $CUR_DEV: ${DEV_JUDGEMENT#DISJOINT } — disjoint from the fifteen guarded paths (the six PR files, the services/auth/ prefix, the four gateway files, the nginx conf, the spec, the packages/shared tests prefix, the root lockfile); the gate merges the then-current develop, re-states the delta by name and re-derives the ratios (brief items 1, 2, 3, 7)" ;;
    *) echo "REFUSING: origin develop is at $CUR_DEV, not the pinned $DEVELOP_SHA, and the delta is not provably disjoint: ${DEV_JUDGEMENT:-no judgement} — confirm the delta, then re-pin deliberately (launcher DEVELOP_SHA + brief TARGET + prompt)" >&2
       exit 18 ;;
  esac
fi

grep -q 'TIER 1' "$BRIEF" && grep -q 'TIER 1' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the tier" >&2; exit 7; }
grep -q 'ROUND 2' "$BRIEF" && grep -q 'ROUND 2' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the round" >&2; exit 15; }
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

R1_READ='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-13_s212/item0/peter_comment_5583115315.md'
grep -qF "$R1_READ" "$BRIEF" && grep -qF '5140256072' "$BRIEF" \
  || { echo "REFUSING: brief does not name the round-1 READ (Peter's review 5140256072 and his comment 5583115315 on disk at $R1_READ) — there is no round-1 QA report for #881 and a gate cannot ask" >&2; exit 19; }
[ -s "$R1_READ" ] || { echo "REFUSING: the round-1 read named by the brief is missing or empty: $R1_READ" >&2; exit 19; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  head $HEAD_SHA present at $BRANCH on origin"
  echo "  merge-base still $MERGE_BASE (GitHub compare API)"
  echo "  $DEV_NOTE"
  echo "  brief, prompt, QA project and repo all present"
  echo "  brief and prompt agree on TIER 1 and ROUND 2"
  echo "  prompt opens with the thinking directive and names the brief"
  echo "  brief and prompt both name the head SHA $HEAD_SHA"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  echo "  brief names the round-1 read (Peter's review 5140256072 + comment 5583115315) and it is present on disk"
  echo "  (a real launch, not --check, additionally requires a TTY on stdin — exit 21)"
  exit 0
fi

[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — this launcher execs an interactive agent and must run in a pane (cockpit.sh add), never inside a Bash tool (a headless gate is invisible and dies with its caller; 2026-09-13 ledger)" >&2; exit 21; }
[ -z "${QA881R2_BRIEF:-}${QA881R2_PROMPT:-}${QA881R2_HEAD:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$DEV_NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
