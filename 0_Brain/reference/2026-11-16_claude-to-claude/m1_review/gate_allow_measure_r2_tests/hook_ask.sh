#!/bin/sh
# QA-ALLOW-MEASURE-R2 stub hook: logs the PreToolUse event and answers `ask` in the real coagent-hook shape
# (crates/coagent-hook/src/main.rs:209 -> pre_tool_use("ask", reason), printed by :57-58 as one line). $1 = log dir.
cat >> "$1/stdin.jsonl"; printf '\n' >> "$1/stdin.jsonl"
printf '%s\n' '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"ask","permissionDecisionReason":"coagent asks: QA2ASKzq7 approve this call (QA-R2 stub)"}}'
exit 0
