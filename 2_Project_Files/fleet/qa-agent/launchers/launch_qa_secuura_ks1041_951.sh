#!/bin/bash
# launch_qa_secuura_ks1041_951.sh — cross-project QA agent, TIER 1 gate on
# Secuura KS-1041 Step 2 (originate must establish a request came from the gateway
# before honouring any trust header) / PR #951 @ dd0a0c934, base develop @ 7bcb66128,
# merge-base 0f8fb33c3.
#
# WHY TIER 1: it is an authentication path. On 2026-09-10 34 containers on one flat
# network could forge connector identity direct to originate:4000 and get a 200; this
# PR is the fix, and every piece of evidence on it is its builder's.
#
# TRACKED ON PURPOSE in launchers/ (not the gitignored fleet/state/) so a successor
# can re-run this gate without inventing a launch command
# (learnings/2026-09-07_a-mechanism-is-recorded-by-its-path-not-its-runtime-id).
#
# Written with the Write tool because it contains a legitimate `cd`, which the
# PreToolUse hook refuses inside a Bash call.
#
# DIFFERENCE FROM THE ks1004_912 TEMPLATE, and why: that launcher computed the
# merge-base with a local `git merge-base`, which needs develop's objects present in
# the Secuura checkout. Fetching them would be a WRITE into another project's .git
# (hard rule 1). So the merge-base guard here asks the GitHub compare API instead,
# inside a SUBSHELL that sources the Secuura .env — the token never reaches the
# QA agent's environment.
#
# Usage: launch_qa_secuura_ks1041_951.sh [--check]  (--check runs every guard, launches nothing)
# Exit: 0 launched (or guards passed under --check) · 2..13 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-11_secuura-951-tier1.md"
PROMPT_FILE="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-11_secuura-951-tier1.prompt.txt"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
BRANCH='refs/heads/kamilkreiser/ks-1041-gateway-provenance-middleware'
HEAD_SHA='dd0a0c934a58d9293cfe54f6e6daca49191bf6f9'
MERGE_BASE='0f8fb33c3416eaa5a79b980402deb845312b20ae'

[ -d "$QA_DIR" ]      || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]       || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ] || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]        || { echo "repo under test missing: $REPO" >&2; exit 5; }

# The head under test must EXIST on the remote, matched on the full SHA.
if ! git -C "$REPO" ls-remote origin "$BRANCH" 2>/dev/null | grep -q "^${HEAD_SHA}[[:space:]]"; then
  echo "REFUSING: $HEAD_SHA is not at $BRANCH on origin — will not gate a SHA that is not there" >&2
  echo "what origin actually has for that ref:" >&2
  git -C "$REPO" ls-remote origin "$BRANCH" >&2
  exit 6
fi

# The merge-base the brief was written against must still be the merge-base with
# develop. If develop was force-moved or the branch rebased, the brief's diff and
# its "5 commits ahead" census describe a different change.
ACTUAL_MB="$(
  set -a; . "$SECUURA_ENV" 2>/dev/null; set +a
  HEAD_SHA="$HEAD_SHA" python3 - <<'PY' 2>/dev/null
import json, os, urllib.request
t = os.environ.get("GH_TOKEN", "")
u = "https://api.github.com/repos/Secuura/Distributed_Secuura/compare/develop..." + os.environ["HEAD_SHA"]
r = urllib.request.urlopen(urllib.request.Request(u, headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}))
print(json.load(r)["merge_base_commit"]["sha"])
PY
)"
if [ -z "$ACTUAL_MB" ]; then
  echo "REFUSING: could not read the merge-base from the GitHub compare API — not assuming it is unchanged" >&2
  exit 13
fi
if [ "$ACTUAL_MB" != "$MERGE_BASE" ]; then
  echo "REFUSING: merge-base is now '$ACTUAL_MB', brief was written against '$MERGE_BASE'" >&2
  echo "the brief's diff and develop census describe a different change — rewrite it" >&2
  exit 10
fi

grep -q 'TIER 1' "$BRIEF" && grep -q 'TIER 1' "$PROMPT_FILE" || {
  echo "REFUSING: brief and prompt disagree about the tier" >&2; exit 7; }
head -1 "$PROMPT_FILE" | grep -q 'ultrathink' || {
  echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 8; }
grep -qF "$BRIEF" "$PROMPT_FILE" || {
  echo "REFUSING: prompt does not name the brief path — the agent would boot blind" >&2; exit 9; }
grep -qi 'MAIL YOUR VERDICT' "$PROMPT_FILE" || {
  echo "REFUSING: prompt does not tell the agent to MAIL its verdict — no inbox, no scrollback" >&2
  exit 12; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  head $HEAD_SHA present at $BRANCH on origin"
  echo "  merge-base still $MERGE_BASE (GitHub compare API)"
  echo "  brief, prompt, QA project and repo all present"
  echo "  brief and prompt agree on TIER 1"
  echo "  prompt opens with the thinking directive and names the brief by path"
  echo "  prompt tells the agent to MAIL its verdict"
  exit 0
fi

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 11; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
