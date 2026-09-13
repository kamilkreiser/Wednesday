#!/bin/bash
# launch_qa_secuura_ks790_982.sh — cross-project QA agent, TIER 1 (through code AND live where a surface exists: the OAuth
# token grants — an auth door) gate, ROUND 1, on Secuura PR #982 (KS-790) @ e62eab87a — ONE commit on origin develop M18
# 8861e6216 (= the merge-base = the PR's parent; compare ahead 1 / behind 0), THREE files +280 -5: routes/oauth.ts (+23 -5;
# the CODE delta is -4/+3 — `:29` import { generateTokenPair, verifyRefreshToken }; `:808` and `:867` userRepo.getUserById
# -> userRepo.getUserByIdPreAuth at the authorization_code and refresh grants of POST /api/oauth/token; develop's `:832`
# in-handler require('../services/jwt') removed; 20 comment lines; blob 4b03f555e -> 80e05458e), NEW
# __tests__/ks790-token-pre-auth-user-lookup.test.ts (249 lines, cfed82d54, raw socket, listen(0, '127.0.0.1'), 6 cells) and
# ONE 8-line hunk in __tests__/ks820-821-token-client-auth-and-apptype.test.ts (a getUserByIdPreAuth mock entry — taken on
# the 15-minute fallback, ACCEPTED by Wednesday 2026-09-14; the gate verifies it is the ONE hunk and that it is load-bearing).
#
# WHY TIER 1, stated here so this file and the brief cannot drift apart: on SHAPE the change is two one-token swaps and an
# import — a tier 2. It is tier 1 because of what it REACHES: /token is the door that turns an authorization code or a
# refresh token into a full token pair, and on every fail-closed-RLS deployment (migration 039, a NOBYPASSRLS role, no tenant
# GUC on a bearer-less request) that door has been shut by accident — the plain RLS-scoped lookup read ZERO rows and the
# handler answered 400 invalid_grant "User not found" for EVERY code. The swap OPENS it; everything downstream of the lookup
# runs for the first time under 039 once this merges (Wednesday's ruling 3: all four PRs of the lane are tier 1). A tier keyed
# on the shape of a change is blind to what the change reaches.
#
# The gate establishes: (1) the delta is exactly the three files / four oauth.ts hunks / one ks820 hunk; (2) red-first both ways
# (4 failed | 2 passed (6) at develop's oauth.ts; 6/6, 19/19, 51 files / 691 at head; develop alone 50 / 685); (3) the product
# path over REAL HTTP through the real router at BOTH SHAs — LIVE on a 039 database if the docker daemon is already up
# (qa982-* only; never started by the gate), else stub-modelled with the REAL userRepo + jwt and the blocker named; (4) the
# tamper table with the suite running (T1, T2, T3d/T3b, T4, T5, T6, Tk); (5) the ks781 authorize-side gates still in front of
# the door; (6) the merged shape + the widened-guard rule (packages/shared green; the ks860 loopback cell reads the new file);
# (7) the enabling change at the BUILT artefact (tsc both trees, diff oauth.js); (8) delivered-vs-commissioned; (9) three
# pre-existing Records measured, not graded; findings-only; NOT TESTED at equal prominence. #982 is the BASE of the stack
# #982 -> #983 -> #984; the PRED line says it merges FIRST.
#
# Merge-base = the PR's parent M18 8861e6216 (GitHub compare develop...head: ahead 1 / behind 0 — exit 10 if it changes).
# origin develop = M18 8861e6216 (the last squash of 2026-09-13, 12:00:26Z; read 07:08 AEST 2026-09-14). The develop pin below is
# DISJOINTNESS-CHECKED, not bare: if origin develop has moved past M18, the GitHub compare of that delta is read and the
# launcher REFUSES (exit 18) only when the delta touches a GUARDED path — the three PR files, anything under
# Blockchain/Dev/services/auth/ (the 691 ratio moves), the ks860 loopback guard file, or migrations/039_rls_fail_closed.sql
# — or cannot be judged (unreadable, not ahead, >250 files); otherwise it proceeds printing the move and its file count,
# which the gate re-states (brief items 1 and 6). A refusal means: confirm the new delta, then re-pin DEVELOP_SHA here AND in
# the brief's TARGET section AND the prompt — a different brief, a deliberate edit.
#
# NEW in this launcher (exit 21): the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent;
# run it in a cockpit pane, never inside a Bash tool — a gate launched there runs headless, invisible to Kam, and dies with
# the caller's shell (2026-09-13 ledger). `--check` still runs headless (it launches nothing).
#
# Adapted from the #980 round-2 launcher by gen_launcher_982.py (asserted substitutions, residual guard): the same guard
# family and exit codes 2..18, 20, 21 (code 19 — the template's round-1-report guard — is not carried: this is a ROUND 1).
#
# Written by the generator because it contains a legitimate `cd`.
#
# Usage: launch_qa_secuura_ks790_982.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..21 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QA982_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-14_secuura-982-ks790-tier1.md}"
PROMPT_FILE="${QA982_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-14_secuura-982-ks790-tier1.prompt.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
BRANCH='refs/heads/feature/ks-790-oauth-authorization_code-token-exchange-uses-getuserbyid'
HEAD_SHA="${QA982_HEAD:-e62eab87a6263e25c41c9bb814d5831842bb6c7e}"
MERGE_BASE='8861e62161466c40f08d2b10a30edeb203123993'
DEVELOP_SHA='8861e62161466c40f08d2b10a30edeb203123993'
REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-14_secuura-982-ks790-tier1.md"

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
  DEV_NOTE="origin develop still $DEVELOP_SHA (M18, the PR's parent and the develop this brief's 51/691 was written against; git ls-remote)"
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
           "Blockchain/Dev/services/auth/src/__tests__/ks790-token-pre-auth-user-lookup.test.ts",
           "Blockchain/Dev/services/auth/src/__tests__/ks820-821-token-client-auth-and-apptype.test.ts",
           "Blockchain/Dev/services/auth/",
           "Blockchain/Dev/packages/shared/src/__tests__/ks860-test-listeners-bind-loopback.test.ts",
           "Blockchain/Dev/migrations/039_rls_fail_closed.sql"]
hits = sorted({f["filename"] for f in files for g in GUARDED if f["filename"] == g or (g.endswith("/") and f["filename"].startswith(g))})
if hits:
    print("GUARDED " + " ".join(hits)); sys.exit(0)
print("DISJOINT commits=%d files=%d" % (c["ahead_by"], len(files)))
PYJ
  )"
  case "$DEV_JUDGEMENT" in
    DISJOINT*) DEV_NOTE="origin develop MOVED $DEVELOP_SHA -> $CUR_DEV: ${DEV_JUDGEMENT#DISJOINT } — disjoint from the guard's six paths (#982's three files, the services/auth/ prefix, the ks860 loopback guard file, migration 039); the gate merges the then-current develop, re-states the delta by name and re-derives the ratio (brief items 1 and 6)" ;;
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
  echo "  $DEV_NOTE"
  echo "  brief, prompt, QA project and repo all present"
  echo "  brief and prompt agree on TIER 1 and ROUND 1"
  echo "  prompt opens with the thinking directive and names the brief"
  echo "  brief and prompt both name the head SHA $HEAD_SHA"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"
  exit 0
fi

[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — this launcher execs an interactive agent; run it in a cockpit pane, never inside a Bash tool (a headless gate is invisible and dies with the caller's shell)" >&2; exit 21; }
[ -z "${QA982_BRIEF:-}${QA982_PROMPT:-}${QA982_HEAD:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$DEV_NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
