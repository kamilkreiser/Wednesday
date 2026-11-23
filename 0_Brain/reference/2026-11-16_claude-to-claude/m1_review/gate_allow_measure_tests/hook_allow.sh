#!/bin/sh
# QA-ALLOW-MEASURE reproduction hook (independent of the builder's stub): log stdin, print the exact line
# crates/coagent-hook/src/main.rs:53-58 + :229-235 prints for an allow with AllowWhy::Owner's reason, exit 0.
cat >> "$1/stdin.jsonl"; echo >> "$1/stdin.jsonl"
printf '%s\n' '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"allow","permissionDecisionReason":"allowed by the owner"}}'
exit 0
