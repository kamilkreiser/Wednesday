#!/bin/bash
# launch_qa_nexusai_mktpkg_20a723b.sh — cross-project QA agent, TIER 1 gate, ROUND 2 of 2, on the
# Datasec/NexusAI Marketplace package: branch s51-marketplace-remediation @ 20a723b (range
# ed8b208..20a723b, 5 commits, on origin) AND the DRAFT submission zips S53 built from it.
# Kam asked 2026-09-11 08:06 whether the zip is ready; he uploads it himself.
#
# PATTERN: launch_qa_nexusai_s51remed.sh (round 1, ed8b208). Differences, each deliberate:
#   - new head/base/count; the branch is now pushed (the guard still reads the LOCAL ref, read-only);
#   - the DRAFT package folder must exist with both zips and MANIFEST.txt, or the gate has no subject;
#   - the brief must name round 1's report path (fleet rule 2026-09-10: a round-N brief names N-1's).
#
# ABSOLUTE PATHS ON PURPOSE (red-proof note in the Tuesday pickup). TRACKED in launchers/.
# Written with the Write tool because it contains a legitimate `cd`.
# Usage: launch_qa_nexusai_mktpkg_20a723b.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..16 a guard refused
set -u

QA_DIR='/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN'
TUE='/Volumes/KK_T9_External_HDD/TUESDAY'
BRIEF="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-11_nexusai-mktpkg-b8c4646-tier1r3.md"
PROMPT_FILE="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-11_nexusai-mktpkg-b8c4646-tier1r3.prompt.txt"
WT='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/wt-s51-mktremed'
PKG='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/evidence-s54-marketplace-package/DRAFT-submission-package-b8c4646'
R1='/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-11-mktpkg-20a723b-tier1r2'
BRANCH='refs/heads/s51-marketplace-remediation'
HEAD_SHA="${QA_HEAD_SHA_OVERRIDE:-b8c4646ab7d271567364876757403bfb8d23cf08}"
BASE_SHA='20a723b1fbdc5afeb2a1a3bd316d30689f75146b'
EXPECTED_COMMITS=10

[ -d "$QA_DIR" ]      || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]       || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ] || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$WT" ]          || { echo "worktree under test missing: $WT" >&2; exit 5; }

GOT="$(git --no-optional-locks -C "$WT" rev-parse "$BRANCH" 2>&1)"
[ "$GOT" = "$HEAD_SHA" ] || { echo "REFUSING: $BRANCH is at '$GOT', not $HEAD_SHA — the brief is stale" >&2; exit 6; }
git --no-optional-locks -C "$WT" merge-base --is-ancestor "$BASE_SHA" "$HEAD_SHA" 2>/dev/null || {
  echo "REFUSING: $BASE_SHA is not an ancestor of $HEAD_SHA — the base in the brief is wrong" >&2; exit 7; }
N="$(git --no-optional-locks -C "$WT" rev-list --count "${BASE_SHA}..${HEAD_SHA}" 2>&1)"
[ "$N" = "$EXPECTED_COMMITS" ] || { echo "REFUSING: expected $EXPECTED_COMMITS commits in range, found '$N'" >&2; exit 8; }

for f in "DRAFT-pending-regate_plan-managed-ai_b8c4646.zip" "DRAFT-pending-regate_listing-assets_b8c4646.zip" "MANIFEST.txt"; do
  [ -s "$PKG/$f" ] || { echo "REFUSING: DRAFT package file missing or empty: $PKG/$f" >&2; exit 9; }
done
[ -s "$R1/report.md" ] || { echo "REFUSING: round-1 report missing at $R1/report.md" >&2; exit 10; }
grep -qF "$R1" "$BRIEF" || { echo "REFUSING: brief does not name round 1's report path" >&2; exit 11; }

docker info >/dev/null 2>&1 || { echo "REFUSING: docker is not responding — the container-log check cannot run" >&2; exit 12; }

grep -q 'TIER 1' "$BRIEF" && grep -q 'TIER 1' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the tier" >&2; exit 13; }
head -1 "$PROMPT_FILE" | grep -q 'ultrathink' || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 14; }
grep -qF "$BRIEF" "$PROMPT_FILE" && grep -qF "$HEAD_SHA" "$PROMPT_FILE" || {
  echo "REFUSING: prompt does not name the brief path and the head" >&2; exit 15; }
grep -qi 'MAIL YOUR VERDICT' "$PROMPT_FILE" && grep -q 'tuesday-agent@agentmail.to' "$PROMPT_FILE" || {
  echo "REFUSING: prompt must say MAIL YOUR VERDICT and name tuesday-agent@agentmail.to" >&2; exit 16; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  $BRANCH == $HEAD_SHA; $BASE_SHA ancestor; range $EXPECTED_COMMITS commits"
  echo "  DRAFT package: both zips + MANIFEST present; round-1 report present and named in the brief"
  echo "  docker responding; tier agrees; prompt: directive, brief path, head, MAIL YOUR VERDICT, tuesday-agent@"
  exit 0
fi

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 17; }
exec claude --dangerously-skip-permissions --model claude-opus-5 "$(cat "$PROMPT_FILE")"
