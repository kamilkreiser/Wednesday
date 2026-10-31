#!/bin/bash
# pretooluse_pipe_rc.sh — PreToolUse hook (matcher: Bash): ADVISORY ONLY, never a refusal.
# Warns when a `$?` is read straight after a pipeline (the rc of `cut`/`head`, not of the command
# being checked). WHY: Tuesday ledger 2026-11-01 w=3 REGRESSION (three piped-rc controls; one was the
# guard before a pane close). Same contract as pretooluse_grep_case.sh: the checker is piperc.py
# beside this file; its stdout (one JSON additionalContext line or nothing) is this hook's stdout;
# exit is ALWAYS 0 (a gate with false positives gets routed around).
CHECKER="$(dirname "${BASH_SOURCE[0]}")/piperc.py"
if [ ! -f "$CHECKER" ]; then
  echo "pretooluse_pipe_rc: checker missing at $CHECKER — advisory skipped" >&2
  exit 0
fi
python3 "$CHECKER"
exit 0
