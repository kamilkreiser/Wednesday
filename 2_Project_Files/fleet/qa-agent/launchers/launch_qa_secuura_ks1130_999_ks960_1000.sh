#!/bin/bash
# launch_qa_secuura_ks1130_999_ks960_1000.sh — cross-project QA agent, TIER 2 (through code) gate ROUND 1 on
# TWO test-only Secuura PRs in ONE pass, one verdict per PR:
#   PR #999  (KS-1130) @ 91793e5d4, branch feature/ks-1130-ornith-tier2-twin-cells — three tier-2 twin cells
#            plus comment-only edits, 5 files under services/api-gateway;
#   PR #1000 (KS-960)  @ ab4a35d75, branch feature/ks-960-ornith-createuser-conflict-target-pin — one new auth
#            test file, does NOT close its ticket.
# Both are one commit on develop 0b25f823f (develop's tip when drafted); they share no file.
#
# Adapted from launch_qa_secuura_ks1099_960.sh by gen_launcher_999_1000.py (asserted substitutions, residual
# guard, positive controls): the same guards and exit codes 2..17, widened to TWO heads — exit 6 (a head moved)
# and exits 13/10 (merge-base unreadable / changed) run once per PR and name the PR. Two guards are ADDED from
# the one-launcher-many-heads family (launch_qa_secuura_AUTH4_983_984_986_987.sh / launch_qa_secuura_ks1061_931.sh):
# exit 20 (brief or prompt does not name a pinned head SHA) and exit 21 (the LAUNCH path refuses a non-TTY stdin).
# Exit 12 is strengthened: the prompt must also name wednesday-agent@agentmail.to.
#
# Written by the generator because it contains a legitimate `cd`.
#
# Usage: launch_qa_secuura_ks1130_999_ks960_1000.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..17, 20, 21 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QA9991000_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-16_secuura-999-1000-ks1130-ks960-tier2.md}"
PROMPT_FILE="${QA9991000_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-16_secuura-999-1000-ks1130-ks960-tier2.prompt.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
BRANCH='refs/heads/feature/ks-1130-ornith-tier2-twin-cells'
HEAD_SHA="${QA999_HEAD:-91793e5d4f4d4b70eec93662c45555472e2bb8a6}"
BRANCH_1000='refs/heads/feature/ks-960-ornith-createuser-conflict-target-pin'
HEAD_1000="${QA1000_HEAD:-ab4a35d75d9b7611b4588ce88a792a489a124324}"
MERGE_BASE='0b25f823f6660ac52b665f14055799ff0c3b616d'   # the merge-base of BOTH heads with develop
REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-16_secuura-999-1000-ks1130-ks960-tier2.md"

[ -d "$QA_DIR" ]         || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]          || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ]    || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]           || { echo "repo under test missing: $REPO" >&2; exit 5; }

# TWO heads, each pinned at its own branch on origin; a moved head names its PR (exit 6).
for pair in "999|$HEAD_SHA|$BRANCH" "1000|$HEAD_1000|$BRANCH_1000"; do
  PR_N="${pair%%|*}"; REST="${pair#*|}"; PR_HEAD="${REST%%|*}"; PR_BRANCH="${REST#*|}"
  if ! git -C "$REPO" ls-remote origin "$PR_BRANCH" | grep -q "^${PR_HEAD}[[:space:]]"; then
    echo "REFUSING: #$PR_N head $PR_HEAD is not at $PR_BRANCH on origin — the head moved; the brief is about a different SHA" >&2
    git -C "$REPO" ls-remote origin "$PR_BRANCH" >&2
    exit 6
  fi
done

# The merge-base, read once PER PR from the GitHub compare API (exit 13 unreadable, exit 10 changed).
for pair in "999|$HEAD_SHA" "1000|$HEAD_1000"; do
PR_N="${pair%%|*}"; PR_HEAD="${pair#*|}"
ACTUAL_MB="$(
  set -a; . "$SECUURA_ENV"; set +a
  HEAD_SHA="$PR_HEAD" python3 - <<'PY'
import json, os, urllib.request
t = os.environ.get("GH_TOKEN", "")
u = "https://api.github.com/repos/Secuura/Distributed_Secuura/compare/develop..." + os.environ["HEAD_SHA"]
r = urllib.request.urlopen(urllib.request.Request(u, headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}))
print(json.load(r)["merge_base_commit"]["sha"])
PY
)"
[ -n "$ACTUAL_MB" ] || { echo "REFUSING: could not read #$PR_N's merge-base from the GitHub compare API" >&2; exit 13; }
[ "$ACTUAL_MB" = "$MERGE_BASE" ] || { echo "REFUSING: #$PR_N merge-base is now '$ACTUAL_MB', brief says '$MERGE_BASE'" >&2; exit 10; }
done

grep -q 'TIER 2' "$BRIEF" && grep -q 'TIER 2' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the tier" >&2; exit 7; }
grep -q 'ROUND 1' "$BRIEF" && grep -q 'ROUND 1' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the round" >&2; exit 15; }
head -1 "$PROMPT_FILE" | grep -q 'ultrathink' || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 8; }
grep -qF "$REAL_BRIEF" "$PROMPT_FILE" || { echo "REFUSING: prompt does not name the brief path" >&2; exit 9; }
for sha in "$HEAD_SHA" "$HEAD_1000"; do
  grep -qF "$sha" "$PROMPT_FILE" && grep -qF "$sha" "$BRIEF" \
    || { echo "REFUSING: brief or prompt does not name the head SHA $sha — a gate about another SHA is another gate" >&2; exit 20; }
done
grep -qi 'MAIL YOUR VERDICT' "$PROMPT_FILE" && grep -qF 'wednesday-agent@agentmail.to' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not tell the agent to MAIL its verdict to wednesday-agent@agentmail.to" >&2; exit 12; }
grep -qi 'NEVER run a push, the real pre-push hook, or preflight.sh inside the Secuura checkout' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid pushing / running the hook in the real checkout" >&2; exit 11; }
grep -qi 'no memory maintenance' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid memory maintenance inside the gate session" >&2; exit 14; }
grep -qi 'NEVER print a credential value' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid printing a credential value" >&2; exit 17; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  #999 head $HEAD_SHA present at $BRANCH on origin"
  echo "  #1000 head $HEAD_1000 present at $BRANCH_1000 on origin"
  echo "  merge-base of both heads still $MERGE_BASE (GitHub compare API, one read per PR)"
  echo "  brief, prompt, QA project and repo all present"
  echo "  brief and prompt agree on TIER 2 and ROUND 1"
  echo "  prompt opens with the thinking directive and names the brief"
  echo "  brief and prompt both name both head SHAs"
  echo "  prompt tells the agent to MAIL its verdict to wednesday-agent@agentmail.to"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"
  exit 0
fi

[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — this launcher execs an interactive agent; run it in a cockpit pane, never inside a Bash tool" >&2; exit 21; }
[ -z "${QA9991000_BRIEF:-}${QA9991000_PROMPT:-}${QA999_HEAD:-}${QA1000_HEAD:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
