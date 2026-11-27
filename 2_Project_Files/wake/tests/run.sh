#!/bin/bash
# run.sh — the wake lane's test runner (WED-170 step 1).
#   tests/run.sh             every check (groups H handover, W wake pack, C census, P launcher proposal)
#   tests/run.sh --groups H  one or more groups
#   tests/run.sh --mutants   break each tool in a scratch copy and require the named check to go red
# Scratch copies and generated fixtures only; the real state, grants, ledger and pickup files are never
# write targets. The P group READS the real launcher and patches a scratch copy of it.
# WAKE_TEST_SCRATCH=<dir> chooses the scratch root (default: a fresh mktemp directory; nothing is deleted).
set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$SCRIPT_DIR/run_tests.py" "$@"
