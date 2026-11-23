#!/bin/bash
# QA-R3 F-B: phrases of the old M9 claim, at a rev, in the spike folder + the two documents. usage: overclaim_grep.sh <clone> <rev>
C=$1; R=$2
for p in "approved it in the control" "had approved it in the control" "decided before the reviewer" "Reviewed, then allowed" "does review" "decided first" \
         "reviewer approved" "reviewer APPROVED" "APPROVED the call" "reviewed and APPROVED" "for a reviewed call" "review context was sent" "no review context" \
         "beats a" "the reviewer reviewed" "before any reviewer" "before the reviewer" "reviewer does not skip" "server reviews inside"; do
  n=$(git -C "$C" grep -F -c -i "$p" "$R" -- spikes/U-B1-hook-allow-silent BACKLOG.md docs/M0-OUTCOMES.md | awk -F: '{s+=$NF} END{print s+0}')
  printf '%-34s %s\n' "\"$p\"" "$n"
done
