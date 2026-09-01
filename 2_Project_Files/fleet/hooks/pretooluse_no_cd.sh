#!/bin/bash
# pretooluse_no_cd.sh — PreToolUse hook (matcher: Bash): REFUSE any Bash tool call whose
# command contains a `cd` as a command (line start, or after ; && || | or a subshell paren).
# WHY (ledger w=5 in the relative-path/`cd` family, 2026-09-02): the Bash tool's cwd persists
# across calls AND across parallel calls in one batch; a `cd` anywhere poisons every later
# relative path. Five instances in two seats (three on 09-02 00:4x–00:59, one at 02:1x, one at
# the 02:26 boot: `cd 0_Brain/learnings` broke a parallel batch of reads). The rule "never cd,
# absolute paths" lived in a ledger row + a handover line and lost to a reflex each time.
# Enforcement sits IN the path (an-enforcement-you-must-arm-is-not-one): exit 2 blocks the call.
# Reads the hook JSON on stdin; never discards stderr; a parse failure PASSES (fail-open on the
# instrument, stated) so a hook bug cannot brick every Bash call.
INPUT=$(cat)
CMD=$(printf '%s' "$INPUT" | python3 -c 'import json,sys
try:
    d=json.load(sys.stdin); print(d.get("tool_input",{}).get("command",""))
except Exception as e:
    print("", end=""); print("pretooluse_no_cd: could not parse hook input: %s" % e, file=sys.stderr)')
# NARROWED 02:3x the same seat, after its FIRST LIVE FIRE was a FALSE POSITIVE: the first regex
# also matched `(` and `|` before cd, so the prose "(cd family)" inside a quoted heredoc refused a
# note write — and then refused the fix that mentioned it. A gate with false positives gets routed
# around (ledger w=8 lesson); command positions only: line start, `;`, `&&`, `||`, `then`, `do`.
if printf '%s\n' "$CMD" | grep -qE '(^|;|&&|\|\||then |do )[[:space:]]*cd([[:space:]]|$)'; then
  cat >&2 <<MSG
REFUSED by pretooluse_no_cd.sh: this Bash call contains a \`cd\`. The tool's cwd persists across
calls (ledger w=5, 2026-09-02) — never cd; write every path absolute; run tools as
\`bash /abs/path/tool.sh\` (they self-locate). Re-issue the call without the cd.
MSG
  exit 2
fi
exit 0
