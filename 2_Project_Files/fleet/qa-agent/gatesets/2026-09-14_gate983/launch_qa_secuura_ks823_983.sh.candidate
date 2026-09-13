#!/bin/bash
# launch_qa_secuura_ks823_983.sh — cross-project QA agent, TIER 1 (a security surface: the OAuth token endpoint's
# refresh_token grant — client authentication + a client_id binding claim on OAuth-minted token pairs; through code AND
# live over a real Express app on a loopback port in the gate's OWN by-SHA clone, the s128 precedent) gate ROUND 1 on
# Secuura PR #983 (KS-823) @ f62c975c1 — STACKED on PR #982 (KS-790) @ e62eab87a, both on origin develop M18 8861e6216
# (merge-base = M18; develop...head: ahead 2 / behind 0 / 5 files; this PR's OWN delta = `git diff e62eab87a f62c975c1`
# = 4 files +395 -22: routes/oauth.ts +82 -10, services/jwt.ts +31 -10, NEW ks823-refresh-grant-client-auth-and-binding
# .test.ts +276, ks790-token-pre-auth-user-lookup.test.ts +6 -2 (its refresh cases now present the client credential and
# a bound stub token; its 17 expect( lines byte-identical)). Head tree db10aea98; the commit was AMENDED once before the push
# (1a26eb795 -> f62c975c1, tree identical — a foreign ticket id removed from the message).
#
# What the gate establishes: (1) the DELTA onto its parent is exactly those 4 files (blob/diff/numstat) and the parent is
# still #982's head; (2) RED-FIRST — the new 11-cell suite against the PARENT's product reads `7 failed | 4 passed (11)`,
# every refusal cell answering 200 WITH A TOKEN, and 11/11 at head; (3) the refresh branch authenticates the client BEFORE
# the token is verified (readClientId -> getAppByClientId, is_active pinned -> verifyClientSecret -> verifyRefreshToken ->
# denylist -> binding -> user -> mint), measured over a raw socket with the real jwt.ts and by the gate's own shapes (body
# vs Basic, mismatched Basic userid, empty/array client_id, form-urlencoded, a deactivated PUBLIC app — the cell the null-app
# guard alone earns); (4) the tamper table with the suite RUNNING — the builder's T1..T4 re-run (T4 is a CRASH red: the
# guard deleted -> TypeError -> 500) plus the gate's non-crashing T4' and the jwt.ts half-tampers; (5) the FAIL-CLOSED arm
# (unbound tokens refused) — ACCEPTED by Wednesday for the gate; the deploy-time consequence is stated, not graded; (6) the
# MERGED shape onto the live develop (a fast-forward while develop is still M18: the merged tree == the head tree) with the
# full auth suite 52 files / 702 tests and the widened ks860 loopback guard GREEN on both new test files; (7) HUNT THE CLASS —
# the sibling POST /api/auth/refresh (routes/auth.ts:658-699, untouched, blob 132d3b8d3 at head AND develop) accepts any
# valid refresh token with no client and re-mints UNBOUND — measured, reported as pre-existing with a control at develop,
# never charged to #983 as a regression; (8) findings-only; board search by SYMBOL/path is Wednesday's; a NOT-TESTED list.
#
# Merge-base = M18 8861e6216 (GitHub compare develop...head; exit 10 if it changes). The STACK PARENT refs/pull/982/head
# must still read e62eab87a (exit 21) — a fix round on #982 makes this brief's delta and red-first about a different
# product. origin develop = M18 (read 07:08:53 AEST 2026-09-14 by ls-remote; unmoved since s212's READY). The develop pin
# below is DISJOINTNESS-CHECKED, not bare: if origin develop has moved past M18, the GitHub compare of that delta is read and
# the launcher REFUSES (exit 18) only when the delta touches a GUARDED path — anything under Blockchain/Dev/services/auth/
# (the 702 ratio and the lane's files), the ks860 loopback guard in packages/shared (it walks services/auth/src/__tests__),
# the api-gateway auth/scopes middleware (the claim consumers, #984's files) or the root lockfile — or cannot be judged
# (unreadable, not ahead, >250 files); otherwise it proceeds printing the move and its file count, which the gate re-states
# (brief items 1 and 2). #982's OWN squash onto develop hits routes/oauth.ts and is the ruled merge order arriving: exit 18
# then means "re-pin DEVELOP_SHA here AND in the brief's TARGET section AND the prompt, and item 2 is a real three-way merge".
#
# Refuses when stdin is not a TTY (exit 22) unless run with --check: this launcher execs an interactive agent; run inside a
# Bash tool it runs headless, invisible and parented to the caller's shell (2026-09-13, Wednesday's own #962 instance).
#
# Adapted from the INSTALLED #980 round-2 launcher by gen_launcher_983.py (asserted substitutions, three asserted insertions,
# one asserted removal, residual guard): same guard family and exit codes 2..18, 20 (the round-2 exit-19 report guard removed;
# exit 21 = the stack parent moved; exit 22 = no TTY), re-pointed at #983.
#
# Written by the generator because it contains a legitimate `cd`.
#
# Usage: launch_qa_secuura_ks823_983.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..22 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QA983_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-14_secuura-983-ks823-tier1.md}"
PROMPT_FILE="${QA983_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-14_secuura-983-ks823-tier1.prompt.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
BRANCH='refs/heads/feature/ks-823-security-the-apioauthtoken-refresh_token-grant-authenticates'
HEAD_SHA="${QA983_HEAD:-f62c975c11ec97cdef04500fd98a43618e702763}"
MERGE_BASE='8861e62161466c40f08d2b10a30edeb203123993'
STACK_PARENT='e62eab87a6263e25c41c9bb814d5831842bb6c7e'
STACK_PARENT_REF='refs/pull/982/head'
DEVELOP_SHA='8861e62161466c40f08d2b10a30edeb203123993'
REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-14_secuura-983-ks823-tier1.md"

[ -d "$QA_DIR" ]         || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]          || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ]    || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]           || { echo "repo under test missing: $REPO" >&2; exit 5; }

if ! git -C "$REPO" ls-remote origin "$BRANCH" | grep -q "^${HEAD_SHA}[[:space:]]"; then
  echo "REFUSING: $HEAD_SHA is not at $BRANCH on origin — the head moved; the brief is about a different SHA" >&2
  git -C "$REPO" ls-remote origin "$BRANCH" >&2
  exit 6
fi

# THIS GATE'S OWN GUARD: #983 is STACKED on #982. The brief's delta (4 files +395 -22), its red-first (the 11 cells against
# the PARENT's product: 7 failed | 4 passed) and its "merge #982 first" instruction are all statements about e62eab87a.
# If #982 gets a fix round its head moves, and this brief describes a product that no longer exists at the parent ref.
if ! git -C "$REPO" ls-remote origin "$STACK_PARENT_REF" | grep -q "^${STACK_PARENT}[[:space:]]"; then
  echo "REFUSING: the stack parent $STACK_PARENT_REF is no longer $STACK_PARENT on origin — #982 moved; #983's delta and red-first are about a different product; rewrite the brief" >&2
  git -C "$REPO" ls-remote origin "$STACK_PARENT_REF" >&2
  exit 21
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
  DEV_NOTE="origin develop still $DEVELOP_SHA (M18, the develop this brief's 52/702 and its fast-forward merged shape were written against; git ls-remote)"
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
GUARDED = ["Blockchain/Dev/services/auth/",
           "Blockchain/Dev/packages/shared/src/__tests__/ks860-test-listeners-bind-loopback.test.ts",
           "Blockchain/Dev/services/api-gateway/src/middleware/auth.ts",
           "Blockchain/Dev/services/api-gateway/src/middleware/scopes.ts",
           "Blockchain/Dev/package-lock.json"]
hits = sorted({f["filename"] for f in files for g in GUARDED if f["filename"] == g or (g.endswith("/") and f["filename"].startswith(g))})
if hits:
    print("GUARDED " + " ".join(hits)); sys.exit(0)
print("DISJOINT commits=%d files=%d" % (c["ahead_by"], len(files)))
PYJ
  )"
  case "$DEV_JUDGEMENT" in
    DISJOINT*) DEV_NOTE="origin develop MOVED $DEVELOP_SHA -> $CUR_DEV: ${DEV_JUDGEMENT#DISJOINT } — disjoint from the guard's five paths (services/auth/, the ks860 loopback guard file, the two api-gateway middleware files, the root lockfile); the gate merges the then-current develop with a real three-way merge, re-states the delta by name and re-derives the auth ratio (brief items 1 and 2)" ;;
    *) echo "REFUSING: origin develop is at $CUR_DEV, not the pinned $DEVELOP_SHA, and the delta is not provably disjoint: ${DEV_JUDGEMENT:-no judgement} — confirm the delta, then re-pin deliberately (launcher DEVELOP_SHA + brief TARGET + prompt)" >&2
       exit 18 ;;
  esac
fi

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
  echo "  merge-base still $MERGE_BASE (GitHub compare API)"
  echo "  stack parent $STACK_PARENT_REF still $STACK_PARENT on origin (this PR's delta and red-first are about that product)"
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

[ -z "${QA983_BRIEF:-}${QA983_PROMPT:-}${QA983_HEAD:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$DEV_NOTE" >&2
# A launch needs a terminal: this execs an interactive agent. Inside a Bash tool there is no TTY and the gate would run
# headless, invisible and parented to the caller's shell (2026-09-13 ledger). --check never reaches this line.
[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — launch this from a pane (cockpit.sh add), never from inside a Bash tool" >&2; exit 22; }
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
