#!/bin/bash
# launch_qa_secuura_kintsugi_4554b25e2.sh — cross-project QA agent, TIER 1 gate ROUND 1
# on the Secuura KINTSUGI DEPLOY of develop 4554b25e2 (s187, 2026-09-11 22:16-22:21Z).
#
# The first deploy gate in this fleet: the subject is a running box, not a PR. Unauthenticated,
# from outside. Adapted from launch_qa_secuura_ks1094_958.sh: the PR head/merge-base guards
# become an origin-develop guard plus a target-reachable guard, and three new prompt clauses are
# required — no account / login / upload (exit 18), never touch demo (exit 19), and the
# credential-print ban (exit 17, kept).
#
# Written with the Write tool because it contains a legitimate `cd`.
#
# Usage: launch_qa_secuura_kintsugi_4554b25e2.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..19 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QAK_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-12_secuura-kintsugi-4554b25e2-tier1.md}"
PROMPT_FILE="${QAK_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-12_secuura-kintsugi-4554b25e2-tier1.prompt.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
DEVELOP_SHA="${QAK_HEAD:-4554b25e21dfd01113bf40e8f6d34573345a5f37}"
TARGET="${QAK_TARGET:-https://kintsugi.secuura.net/health}"
REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-12_secuura-kintsugi-4554b25e2-tier1.md"

[ -d "$QA_DIR" ]         || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]          || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ]    || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]           || { echo "repo under test missing: $REPO" >&2; exit 5; }

if ! git -C "$REPO" ls-remote origin refs/heads/develop | grep -q "^${DEVELOP_SHA}[[:space:]]"; then
  echo "REFUSING: origin develop is not $DEVELOP_SHA — develop moved; the deployed revision and develop now differ" >&2
  git -C "$REPO" ls-remote origin refs/heads/develop >&2
  exit 6
fi

CODE="$(curl -sS -o /dev/null -m 20 -w '%{http_code}' "$TARGET" 2>&1)"
[ "$CODE" = "200" ] || { echo "REFUSING: target $TARGET answered '$CODE', not 200 — the box is not up to be gated" >&2; exit 13; }

grep -q 'TIER 1' "$BRIEF" && grep -q 'TIER 1' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the tier" >&2; exit 7; }
grep -q 'ROUND 1' "$BRIEF" && grep -q 'ROUND 1' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the round" >&2; exit 15; }
head -1 "$PROMPT_FILE" | grep -q 'ultrathink' || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 8; }
grep -qF "$REAL_BRIEF" "$PROMPT_FILE" || { echo "REFUSING: prompt does not name the brief path" >&2; exit 9; }
grep -qi 'MAIL YOUR VERDICT' "$PROMPT_FILE" || { echo "REFUSING: prompt does not tell the agent to MAIL its verdict" >&2; exit 12; }
grep -qi 'NEVER run a push, the real pre-push hook, or preflight.sh inside the Secuura checkout' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid pushing / running the hook in the real checkout" >&2; exit 11; }
grep -qi 'no memory maintenance' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid memory maintenance inside the gate session" >&2; exit 14; }
grep -qi 'NEVER print a credential value' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid printing a credential value" >&2; exit 17; }
grep -qi 'NEVER create an account, log in with real credentials, or upload anything to kintsugi' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid accounts, real logins and uploads on kintsugi" >&2; exit 18; }
grep -qi 'NEVER touch demo' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid touching demo" >&2; exit 19; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  origin develop is $DEVELOP_SHA (the deployed revision)"
  echo "  target $TARGET answers 200"
  echo "  brief, prompt, QA project and repo all present"
  echo "  brief and prompt agree on TIER 1 and ROUND 1"
  echo "  prompt opens with the thinking directive and names the brief"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  echo "  prompt forbids accounts, real logins and uploads on kintsugi"
  echo "  prompt forbids touching demo"
  exit 0
fi

[ -z "${QAK_BRIEF:-}${QAK_PROMPT:-}${QAK_HEAD:-}${QAK_TARGET:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
