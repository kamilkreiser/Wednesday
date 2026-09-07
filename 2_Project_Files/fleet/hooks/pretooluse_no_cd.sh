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

# ── ADDED 2026-09-07 (ledger w=2, the SECOND write verb run in another project's checkout in 24h):
# refuse `git -C <path outside WEDNESDAY>` followed by a WRITE verb. This is rule 4 of
# 2026-09-06_other-projects-repos-are-read-only-git-verbs-that-write, promoted from candidate to
# mechanism because the rule was READ AT BOOT and broken four hours later — the write verb sat
# mid-command as setup for a read (`fetch` before `merge-base --is-ancestor`), so the sentence being
# composed matched the rule while the command did not. Intent is not what writes; verbs are.
#
# SCOPED DELIBERATELY NARROW, because a gate with false positives gets routed around (the same
# lesson this file already learned at 02:3x): the verb must be the git SUBCOMMAND of that same
# invocation — i.e. directly after `-C <path>` and any leading flags — never merely present
# somewhere in the command. Briefs written by this seat routinely contain the words fetch/push/
# merge inside quoted heredocs, and those MUST pass.
#
# The tool's cwd is pinned to WEDNESDAY by the `cd` refusal above, so the `-C` form is the only
# realistic vector. Residual, stated rather than implied: a bare `git <writeverb>` would not be
# caught if the cwd were ever outside WEDNESDAY — which the cd clause is what prevents.
GITCHK=$(printf '%s' "$CMD" | python3 -c '
import re, sys
cmd = sys.stdin.read()
OWN = "/Volumes/DevMASTER/WEDNESDAY"
WRITE = ("fetch","pull","push","worktree","checkout","reset","stash","commit","tag","gc",
         "clean","am","apply","cherry-pick","rebase","revert","prune","repack","update-ref",
         "symbolic-ref","switch","restore","mv","init","submodule")
# NARROWED at build time, BEFORE arming, because the first exercise fired on this hook own
# test harness — a quoted fixture, not a real invocation. Anchor the match to a COMMAND
# POSITION (line start, or after ; & | ( backtick $( then do), so an example quoted inside a
# brief, a heredoc or a test fixture cannot trip it. This is the same narrowing the cd clause
# above needed at 02:3x on 2026-09-02, for exactly the same reason: a gate with false positives
# gets routed around, and this file has already learned that once.
#
# Learned while building it, worth keeping: the hook GATES THE CALL THAT EDITS THE HOOK, so a
# clause and its own narrowing cannot ship in one Bash call — the un-narrowed version refuses it.
# Edit the file with a non-Bash tool, then exercise it from fixtures on disk.
pat = re.compile(
    r"""(?:^|[;&|(`\n]|\$\(|\bthen\s|\bdo\s)\s*"""
    r"""git\s+-C\s+(?P<path>"[^"]*"|\x27[^\x27]*\x27|[^\s]+)\s+"""
    r"""(?P<flags>(?:-[^\s]+\s+)*)"""
    r"""(?P<verb>[a-z][a-z-]*)""", re.X | re.M)
for m in pat.finditer(cmd):
    path = m.group("path").strip("\x27\"")
    verb = m.group("verb")
    rest = cmd[m.end():m.end()+80]
    hit = verb in WRITE or (verb == "merge-tree" and "--write-tree" in rest)
    if not hit:
        continue
    # $VAR / ${VAR} paths cannot be resolved here: treat as OUTSIDE unless they literally
    # name WEDNESDAY. Fail CLOSED on the unknown, since the whole class is about other trees.
    if path.startswith(OWN):
        continue
    print("%s|%s" % (verb, path))
    break
' 2>/dev/null)
if [ -n "$GITCHK" ]; then
  V="${GITCHK%%|*}"; P="${GITCHK#*|}"
  cat >&2 <<MSG
REFUSED by pretooluse_no_cd.sh: \`git -C $P $V\` is a WRITE verb pointed OUTSIDE
/Volumes/DevMASTER/WEDNESDAY. Another project's \`.git\` is its files — hard rule 1, manage don't do
(ledger w=2, 2026-09-07; lesson 2026-09-06_other-projects-repos-are-read-only-git-verbs-that-write).

READ verbs are fine there: ls-remote · log · show · diff · cat-file · ls-tree · rev-parse ·
rev-list · merge-base · grep · for-each-ref · status.

To verify a merge or a head: \`git -C <path> ls-remote origin\` plus the agent's own receipt.
If you genuinely need write verbs, clone by SHA into this session's scratchpad and run them THERE.
MSG
  exit 2
fi

exit 0
