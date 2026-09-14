#!/bin/bash
# pretooluse_no_rm.sh — PreToolUse hook (matcher: Bash): REFUSE a Bash call that DELETES a file
# outside the session scratchpad. Kam, 2026-08-26 (twice in one message): "Do not delete any
# files, especially files that we are working on. Better cleanup is worthwhile." — cleanup means
# QUARANTINE (a dated folder), never removal. The rule lived as a sentence in every brief and
# was broken TWICE on 2026-09-14 by subagents tidying their own run dirs (a Sonnet re-pin drafter
# 12:4x, an Opus pilot drafter 15:2x), both disclosed, both zero cost, both the same reflex.
# w=2 in the subagent costume → the mechanism, not a stronger sentence
# (an-enforcement-you-must-arm-is-not-one). Subagents run the same Bash tool, so the same hook.
#
# WHAT IT REFUSES (command position only — line start, `;`, `&&`, `||`, `|`, `then`, `do`, `$(`):
#   rm …            unless EVERY non-flag argument is a literal absolute path under /private/tmp/
#                   or /tmp/ (the session scratchpad lives there). A `$VAR` argument REFUSES —
#                   the hook cannot see what it expands to, and a quarantine `mv` needs no rm.
#   git rm …        always (untrack + delete); `git rm --cached` alone is allowed (it untracks).
#   find … -delete  unless the find root is under /private/tmp/ or /tmp/.
#   unlink …        same rule as rm.
# It does NOT touch: prose mentioning rm inside a quoted heredoc body (the word must sit at a
# command position), `rm` as part of another word (`rmdir` is separate and NOT refused —
# an empty directory holds nothing), `--rm` docker flags, `rm` inside single quotes passed
# to another program (git grep 'rm ' …) — the regex anchors on command position.
# Fail-open on the INSTRUMENT (a parse error passes, stated on stderr) so a hook bug cannot
# brick every Bash call. Exit 2 = refused.
INPUT=$(cat)
printf '%s' "$INPUT" | python3 "$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)/norm.py"
rc=$?
exit $rc
