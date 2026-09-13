#!/bin/bash
# pretooluse_grep_case.sh — PreToolUse hook (matcher: Bash): ADVISORY ONLY, never a refusal.
# WARNS when a Bash call contains a counting/quiet/line-number grep (`-c`, `-q`, `-n`, any flag
# order, long forms too) whose pattern is a QUOTED MULTI-WORD PHRASE and carries no `-i` — or
# any grep whose pattern contains `$(`.
#
# WHY (consolidation 2026-09-14, promotion 15; ledger w=3 on 2026-09-11, a REGRESSION — three
# rows in one day, 67 in the family): a case-sensitive phrase grep returns 0 for "Context limit"
# when the file says "context limit", and that zero walks into a sentence to Kam as "no outage"
# / "never pushed". A false zero on a negative claim is the worst-direction error there is. The
# rule ("/usr/bin/grep -i plus a positive control from the same file") lived in ledger rows and
# lost to a reflex each time; this puts it IN THE PATH.
#
# WHY A WARNING AND NOT exit 2: a grep in a pipeline that the seat reads by eye must not be
# blocked (a gate with false positives gets routed around — ledger w=8, and both sibling hooks
# learned it on their first live fire). Exit is ALWAYS 0. The warning goes to stderr (debug
# log) AND, because Claude Code discards a hook's exit-0 stderr, as JSON `additionalContext`
# on stdout so the seat actually reads it (docs: hooks reference, PreToolUse decision control;
# no `permissionDecision` is emitted, so the permission flow is untouched).
#
# Same input contract as pretooluse_no_cd.sh: hook JSON on stdin; a parse failure PASSES
# silently (fail-open on the instrument, stated). Heredoc bodies are stripped before matching
# (prose quoting a grep is not a grep — the third false-positive class in this directory).
# The checker lives in grepcase.py BESIDE this file (the pathguard.py split): a single-quoted
# string bricks on an apostrophe (happened to the sibling twice) and bash 3.2 cannot parse a
# backtick-bearing heredoc inside `$( )` (happened to this file's first draft, caught by the
# exercise harness before wiring).
#
# Exercised before wiring (2026-09-14): fixtures + proof output beside the report at
# 5_Project_History/2026-09-14_consolidation-promotions/item1_grep_hook_exercise.txt.
CHECKER="$(dirname "${BASH_SOURCE[0]}")/grepcase.py"
if [ ! -f "$CHECKER" ]; then
  echo "pretooluse_grep_case: checker missing at $CHECKER — advisory skipped" >&2
  exit 0
fi
# stdin (the hook JSON) flows straight into the checker; its stdout (a JSON line or nothing)
# becomes this hook's stdout; its stderr stays on stderr. The exit code is ALWAYS 0.
python3 "$CHECKER"
exit 0
