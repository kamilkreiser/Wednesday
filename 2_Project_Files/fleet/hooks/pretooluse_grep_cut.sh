#!/bin/bash
# pretooluse_grep_cut.sh — PreToolUse hook (matcher: Bash): ADVISORY ONLY, exit always 0.
# Warns on grep | ... | cut -c in one pipeline (a hit hidden past the cut reads as a miss).
# Why and history: grepcut.py beside this file. Built 2026-11-10 (ledger, B 129th false absence).
CHECKER="$(dirname "${BASH_SOURCE[0]}")/grepcut.py"
if [ ! -f "$CHECKER" ]; then
  echo "pretooluse_grep_cut: checker missing at $CHECKER — advisory skipped" >&2
  exit 0
fi
python3 "$CHECKER"
exit 0
