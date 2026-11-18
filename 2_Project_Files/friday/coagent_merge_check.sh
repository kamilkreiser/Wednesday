#!/bin/bash
# coagent_merge_check.sh — Friday's OWN clean-clone check of a CoAgent branch before a merge GO.
# WHY (2026-11-18): the method lived in a session scratchpad (mc_branch.sh) and was lost at every seat change.
# "Never merge on a seat's own figures": this runs the project's check in a clone no seat has touched.
#
# Usage: coagent_merge_check.sh <work dir (new or empty, in the session scratchpad)> <branch> <expected full sha> [runner script ...]
#   e.g. coagent_merge_check.sh "$SCRATCH/mc_audit_fix" m3-audit-fix 393e7e4...  scripts/red-controls-audit.sh
# Reads the project repository only (git clone from the local path is a read of the source). Writes only under
# <work dir>: clone/, tools/ (a cargo home whose bin and rustup are LINKS to the project's drive-local toolchain,
# so the registry cache is the check's own), target/, and the logs head.txt fetch.log check.log red_<n>.log.
# Exit: 0 all green · 2 usage/setup · 3 head mismatch · 4 fetch failed · 5 check.sh failed · 6 a runner failed.
# Network: `cargo fetch --locked` only. Nothing is deleted. bash 3.2 safe.
set -u
PROJ="/Volumes/Laptop-DEV/!CODING/Claude to Claude/coagent"
WORK="${1:?work dir}"; BRANCH="${2:?branch}"; WANT="${3:?expected full sha}"; shift 3
[ -x "$PROJ/tools/cargo/bin/cargo" ] || { echo "merge_check: no toolchain at $PROJ/tools/cargo/bin/cargo" >&2; exit 2; }
mkdir -p "$WORK" || exit 2
[ -e "$WORK/clone" ] && { echo "merge_check: $WORK/clone already exists; use a new work dir" >&2; exit 2; }
git clone --quiet --branch "$BRANCH" "$PROJ/2_Project_Files" "$WORK/clone" > "$WORK/clone.log" 2>&1 || { echo "merge_check: clone failed, see $WORK/clone.log" >&2; exit 2; }
HEAD_SHA="$(git -C "$WORK/clone" rev-parse HEAD)"
echo "branch=$BRANCH head=$HEAD_SHA want=$WANT $(date '+%F %H:%M')" > "$WORK/head.txt"
[ "$HEAD_SHA" = "$WANT" ] || { echo "merge_check: HEAD $HEAD_SHA is not the expected $WANT" >&2; exit 3; }
mkdir -p "$WORK/tools/cargo" "$WORK/target" || exit 2
ln -s "$PROJ/tools/cargo/bin" "$WORK/tools/cargo/bin" || exit 2
ln -s "$PROJ/tools/rustup" "$WORK/tools/rustup" || exit 2
export COAGENT_TOOLS="$WORK/tools" CARGO_TARGET_DIR="$WORK/target"
run_in_clone() { ( cd "$WORK/clone" && . scripts/env.sh && "$@" ); }
run_in_clone cargo fetch --locked > "$WORK/fetch.log" 2>&1 || { echo "merge_check: cargo fetch --locked failed, see $WORK/fetch.log" >&2; exit 4; }
run_in_clone bash scripts/check.sh > "$WORK/check.log" 2>&1; RC=$?
echo "check.sh exit $RC" >> "$WORK/head.txt"
[ "$RC" -eq 0 ] || { echo "merge_check: check.sh exit $RC, see $WORK/check.log" >&2; exit 5; }
N=0
for R in "$@"; do
  N=$((N+1))
  run_in_clone bash "$R" > "$WORK/red_$N.log" 2>&1; RC=$?
  echo "$R exit $RC" >> "$WORK/head.txt"
  [ "$RC" -eq 0 ] || { echo "merge_check: $R exit $RC, see $WORK/red_$N.log" >&2; exit 6; }
done
echo "MERGE CHECK OK $BRANCH $HEAD_SHA" >> "$WORK/head.txt"
cat "$WORK/head.txt"
