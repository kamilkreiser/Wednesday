#!/bin/bash
# gate_stray_check.sh — refuse a GO while a stray file sits in the coordinator's own tree.
#
# WHY (ledger w=3, promoted 2026-10-20 00:5x): QA gates run as Agent-tool sub-agents whose cwd
# is the coordinator's tree, so a relative path or an `npm exec`/`vitest` run from the cwd writes
# INTO it. Three gates did it in one night: AJ1 left node_modules/.vite at the root, AL1 left an
# 8-byte `r2` (a mis-quoted echo redirect), AQ1 left node_modules/.vite again, each time with a
# brief line that said "write nothing here except verdict.md". A brief line is a rule; this is the
# mechanism. It sits in the GO path because a GO is the moment a gate's output is trusted.
#
# WHAT IT CHECKS: UNTRACKED paths only (`git status --porcelain`, `??` rows), outside the places
# seats, gates and screens are allowed to write. Modified TRACKED files are the coordinator's own
# work and are not this check's business. Ignored files are invisible to it by construction.
#
# Usage: gate_stray_check.sh            (tree = this script's ../.. ; override GATE_STRAY_TREE=<dir>)
# Exit:  0 clean (or GATE_STRAY_OK='<reason>' set: printed, then 0)
#        1 strays found (listed on stderr with the quarantine command to run)
#        2 not a git tree / git failed (refuses rather than passing blind)
set -u
SELF_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TREE="${GATE_STRAY_TREE:-$(cd "$SELF_DIR/../.." && pwd)}"

# Allowed homes for NEW files. Anchored at the start of the path. Everything else is a stray.
ALLOW_RE='^(0_Brain/|5_Project_History/|2_Project_Files/local-model/|2_Project_Files/fleet/briefs_staged/)'

OUT="$(git -C "$TREE" status --porcelain --untracked-files=all 2>&1)"; RC=$?
if [ $RC -ne 0 ]; then
  echo "gate_stray_check: REFUSED — git status failed in $TREE (rc $RC): $OUT" >&2
  exit 2
fi
STRAYS="$(printf '%s\n' "$OUT" | sed -n 's/^?? //p' | sed 's/^"//;s/"$//' | /usr/bin/grep -vE "$ALLOW_RE")"
if [ -z "$STRAYS" ]; then
  exit 0
fi
if [ -n "${GATE_STRAY_OK:-}" ]; then
  echo "gate_stray_check: strays present but GATE_STRAY_OK given — reason: $GATE_STRAY_OK" >&2
  printf '%s\n' "$STRAYS" | sed 's/^/  stray: /' >&2
  exit 0
fi
echo "gate_stray_check: REFUSED — untracked path(s) outside the allowed homes in $TREE:" >&2
printf '%s\n' "$STRAYS" | sed 's/^/  stray: /' >&2
echo "  If a path is YOUR OWN new work, commit it first. Otherwise a gate (or another sub-agent) wrote into this tree: MOVE each one to the session scratchpad's _quarantine_<date>/ (never delete), record it in the note, then re-send. Override only with a stated reason: GATE_STRAY_OK='<why>' (ledger w=3, 2026-10-20)." >&2
exit 1
