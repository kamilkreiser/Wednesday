#!/bin/bash
# drafter_trapprobe_g24b.sh — the DRAFTER's own probe of #1250's `trap rss_cleanup_tmpdir EXIT INT TERM` (a PREDICTION instrument for the kit;
# the gate re-measures in its own clone). For each runner (develop's and #1250's, read with `git show` from the kit's scratch clone), builds a
# throwaway tree under <kit>/_sp/trapprobe/<label>/ with TWO fixture suites (a.test.sh sleeps 4 s, b.test.sh prints a marker), runs the runner in
# the background under a LONG TMPDIR (> 80 chars, so the KS-1135 substitution fires), sends SIGTERM to the RUNNER'S pid after 1 s, and records:
# the runner's rc, whether b.test.sh ran after the TERM, and whether the /tmp/rss.* dir the runner named still exists. Kills nothing but its own
# runner pid (and, at the end, its own sleep child by pid if still alive). Deletes nothing (the /tmp/rss.* dirs a develop run leaves are REPORTED).
# Usage: drafter_trapprobe_g24b.sh <kit dir>
set -u
K="${1:?kit dir}"; CL="$K/_sp/g24b_sp/clone.git"; P="$K/_sp/trapprobe/$(date -u +%H%M%S)"; mkdir -p "$P"
LONG="$P/$(printf 'z%.0s' $(seq 1 100))"; mkdir -p "$LONG"
probe() { # $1 label, $2 rev
  local R="$P/$1"; mkdir -p "$R/Blockchain/Dev/scripts/__tests__"
  git --git-dir "$CL" show "$2:Blockchain/Dev/scripts/run-shell-suites.sh" > "$R/Blockchain/Dev/scripts/run-shell-suites.sh"
  printf '#!/bin/bash\necho "a: start"; sleep 4; echo "a: end"\n' > "$R/Blockchain/Dev/scripts/__tests__/a.test.sh"
  printf '#!/bin/bash\necho "b: RAN AFTER THE TERM"\n' > "$R/Blockchain/Dev/scripts/__tests__/b.test.sh"
  ( TMPDIR="$LONG" exec bash "$R/Blockchain/Dev/scripts/run-shell-suites.sh" > "$R/runner.out" 2>&1 ) &
  local pid=$!
  sleep 1
  kill -TERM "$pid"
  wait "$pid"; local rc=$?
  local dir; dir="$(sed -n 's|.*the suites ran under \(/tmp/rss\.[A-Za-z0-9]*\) .*|\1|p' "$R/runner.out" | head -1)"
  echo "=== $1 ($2) runner rc after SIGTERM: $rc"
  echo "  b.test.sh ran after the TERM: $(grep -c 'b: RAN AFTER THE TERM' "$R/runner.out")"
  echo "  runner printed its verdict line: $(grep -c '^shell suites:' "$R/runner.out")"
  echo "  /tmp/rss dir named: ${dir:-NONE} | still exists: $([ -n "$dir" ] && [ -d "$dir" ] && echo YES || echo no)"
  echo "  --- runner output:"; sed 's/^/    /' "$R/runner.out"
}
echo "drafter_trapprobe_g24b.sh $(date -u +%FT%TZ) | bash $BASH_VERSION | long TMPDIR ${#LONG} chars"
probe develop 77c6426b96d9e48a758e68fa56e9138dc8509aa8
probe pr1250 c78f4093fb531bceb94a8e9defb59350d8c60b73
sleep 4
echo "own leftover sleep children (should be none after 4 s): $(pgrep -f "$P" | wc -l | tr -d ' ')"
