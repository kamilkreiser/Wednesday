#!/usr/bin/env bash
# =============================================================================
# TESTS for Blockchain/Dev/scripts/check-akto-container-names.sh - a docker verb followed by
# option flags before the container name must still be flagged.
# =============================================================================
# The first alternative of the gate's pattern is `docker <verb> <optional quote>akto-<role>` with
# only whitespace between the verb and the name, so the everyday forms `docker exec -it akto-mongo
# mongosh` and `docker logs --tail=50 akto-testing` pass the gate although they target slot 1.
# Real grep and find, a private fixture tree; nothing outside the temp dir is read.
# Usage: bash Blockchain/Dev/scripts/__tests__/check_akto_container_names_flags.test.sh
# =============================================================================

set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SUBJ="${CHECK_AKTO_CONTAINER_NAMES_SH:-$HERE/../check-akto-container-names.sh}"
[[ -r "$SUBJ" ]] || { echo "FATAL: check-akto-container-names.sh not readable at $SUBJ" >&2; exit 2; }
WORK="$(mktemp -d "${TMPDIR:-/tmp}/akto-flags.XXXXXX")"
trap 'rm -rf "$WORK"' EXIT
PASS=0
FAIL=0

run_case() {   # $1 = case name, $2 = line planted in scripts/z.sh -> prints the gate's exit code
  local d="$WORK/$1"
  mkdir -p "$d/src" "$d/bin" "$d/scripts"
  printf 'export const a = 1;\n' > "$d/src/ok.ts"
  printf 'export const b = 1;\n' > "$d/bin/ok.ts"
  printf '#!/bin/bash\n%s\n' "$2" > "$d/scripts/z.sh"
  bash "$SUBJ" "$d" >"$WORK/$1.out" 2>&1
  echo $?
}

check() {   # $1 = label, $2 = want rc, $3 = got rc
  if [[ "$3" == "$2" ]]; then
    echo "PASS: $1"; PASS=$((PASS+1))
  else
    echo "FAIL: $1 (want rc $2, got rc $3)"; FAIL=$((FAIL+1))
  fi
}

# CELL 1 (RED at the tip) - short flags between the verb and the name.
check "docker exec -it akto-mongo is flagged" 1 "$(run_case c1 'docker exec -it akto-mongo mongosh')"

# CELL 2 (RED at the tip) - a long flag with its value attached, and a quoted name.
check "docker logs --tail=50 \"akto-testing\" is flagged" 1 "$(run_case c2 'docker logs --tail=50 "akto-testing"')"

# CELL 3 (RED at the tip) - two flags in a row.
check "docker exec -i -t akto-mongo is flagged" 1 "$(run_case c3 'docker exec -i -t akto-mongo mongosh')"

# CELL 4 (GREEN CONTROL, tip AND after) - the plain literal is still flagged.
check "CONTROL docker exec akto-mongo is still flagged" 1 "$(run_case c4 'docker exec akto-mongo mongosh')"

# CELL 5 (GREEN CONTROL, tip AND after) - the derived form with flags is the fix, not the defect.
check "CONTROL docker exec -it with the AKTO_PREFIX form is clean" 0 "$(run_case c5 'docker exec -it "${AKTO_PREFIX:-akto}-mongo" mongosh')"

# CELL 6 (GREEN CONTROL, tip AND after) - flags before a non-akto container are clean.
check "CONTROL docker exec -it other-container is clean" 0 "$(run_case c6 'docker exec -it other-mongo mongosh')"

echo ""
echo "Results: $PASS passed, $FAIL failed"
[[ "$FAIL" -eq 0 ]]
