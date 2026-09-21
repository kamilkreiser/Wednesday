#!/bin/bash
# nas_sync_lib.sh — the parser and argument builder behind the RETRY PASS in nas_sync.sh.
#
# It is a separate, sourceable file for ONE reason: the arms in
# fleet/tests/nas_sync_retry_arms.sh exercise EXACTLY the functions the nightly run uses,
# against captured logs, without running unison. A parser that lives inline in the run
# script can only be tested by running the run script (2026-08-07_a-check-that-cannot-fail).
#
# Facts these functions are built on (measured 2026-09-21 on the 03:30 log, od -c verified):
#   * unison 2.54.0 writes its per-run failure list at the END of the run as one line per
#     path, INDENTED BY TWO SPACES:  "  failed: WEDNESDAY/0_Brain/learnings/_ledger.md"
#     A `^failed:` anchor matches nothing; `grep -c 'failed: '` matched 67 = the "67 failed"
#     in unison's own summary line.
#   * the log is carriage-return separated (progress repaints) — normalise \r → \n first,
#     or every ^-anchored regex is blind (2026-09-11, the deletion alarm's own history).
#   * paths may contain spaces ("Notes (MASTER)/daily/…") and must stay ONE argv element.
#   * under `confirmbigdel = true` + `batch = true`, a `-path` target that is now ABSENT on
#     one side aborts the whole scoped run (rc=3, "The following paths have been completely
#     emptied in one replica"). Measured on a local scratch pair 2026-09-21 09:59. So the
#     list must lose (a) anything gone from the source before the retry starts, and (b)
#     anything the abort message names, before the next attempt.
#
# Agent-neutral: nothing here knows which seat is running.

# nas_norm LOG — normalised text of a unison log: \r → \n, ANSI colour/cursor codes stripped.
nas_norm() {
  local esc; esc="$(printf '\033')"
  tr '\r' '\n' < "$1" | sed -E "s/${esc}\[[0-9;?]*[A-Za-z]//g"
}

# nas_failed_paths LOG — the unique root-relative paths from "  failed: <path>" lines, in
# first-seen order, trailing whitespace removed. Prints nothing on a clean log.
nas_failed_paths() {
  nas_norm "$1" | sed -nE 's/^[[:space:]]*failed: (.+)$/\1/p' | sed -E 's/[[:space:]]+$//' \
    | awk 'NF && !seen[$0]++'
}

# nas_count FILE — number of non-empty lines. NOT `grep -c … || echo 0`: grep exits 1 on
# zero matches and that form prints "0\n0". awk prints exactly one number, always.
nas_count() { awk 'NF{n++} END{print n+0}' "$1"; }

# nas_emptied_paths LOG — the paths a confirmbigdel abort names, one per line:
#   The following paths have been completely emptied in one replica:
#     'd/gone.txt'
#   Unison may delete everything below these paths in the other replica.
nas_emptied_paths() {
  nas_norm "$1" | awk '
    /completely emptied in one replica/ {grab=1; next}
    grab && /^[[:space:]]*'"'"'.*'"'"'[[:space:]]*$/ { sub(/^[[:space:]]*'"'"'/,""); sub(/'"'"'[[:space:]]*$/,""); print; next }
    grab && NF {grab=0}
  '
}

# nas_build_path_args PATHSFILE — fills the global array NAS_PATH_ARGS with
#   -path <p1> -path <p2> …   for every non-empty line of PATHSFILE, nothing else.
# Callers pass "${NAS_PATH_ARGS[@]}" to unison. Bash 3.2-safe (no mapfile).
NAS_PATH_ARGS=()
nas_build_path_args() {
  NAS_PATH_ARGS=()
  local p
  while IFS= read -r p; do
    [ -n "$p" ] || continue
    NAS_PATH_ARGS+=( -path "$p" )
  done < "$1"
}

# nas_filter_present SRCROOT IN OUT DROPPED — copy the paths of IN that still exist under
# SRCROOT to OUT; the others (gone from the source since the main run) to DROPPED.
# A `-path` on a source-deleted file is exactly the abort case above; and a deletion is the
# one thing the retry pass must never be the first to propagate — the full run does that,
# with its alarm watching.
nas_filter_present() {
  local src="$1" in="$2" out="$3" dropped="$4" p
  : > "$out"; : > "$dropped"
  while IFS= read -r p; do
    [ -n "$p" ] || continue
    if [ -e "$src/$p" ] || [ -L "$src/$p" ]; then printf '%s\n' "$p" >> "$out"
    else printf '%s\n' "$p" >> "$dropped"; fi
  done < "$in"
}

# nas_minus A B OUT — lines of A that are not in B (exact match), order of A kept.
nas_minus() { awk 'NR==FNR{drop[$0]=1; next} !($0 in drop)' "$2" "$1" > "$3"; }
