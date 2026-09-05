---
date: 2026-08-26
type: correction
source: "w=2 same day, two sessions: the 10:5x session's addendum send guard read `${PIPESTATUS[0]}` in zsh (empty → verify+tap skipped, redone by hand); the 16:3x session's first brief_and_launch invocation did the same and printed `rc=` with nothing after it. Zero cost both times — the gated scripts print their own refusals and sequence by construction — but the guard I wrote around them was a check that could not fail."
status: live
supersedes: ""
tier: M
---

# In zsh there is no `PIPESTATUS` — an exit code read through a pipe is a check that cannot fail

**The operative case:** I am about to write `cmd | tail … ; echo "rc=${PIPESTATUS[0]}"` or
`if [ "${PIPESTATUS[0]}" = 0 ]` in a Bash tool call. **The tool runs zsh.** `PIPESTATUS`
is bash; zsh's equivalent is `$pipestatus[1]` (lowercase, 1-indexed). In zsh `${PIPESTATUS[0]}`
expands to the empty string — so `[ "" = 0 ]` is false and `echo "rc="` prints nothing, and
neither looks like an error. Twice today the guard around a refusable step silently read
nothing.

**Why it costs nothing today and could cost later:** the refusable steps (send_brief.sh,
brief_and_launch.sh) print their refusal text and the launcher branch is unreachable without
a verified send — the enforcement is in the script, not in my guard. Any hand-written guard
that depends on a piped exit status is decorative. If I ever chain a destructive step on
such a guard, it fires on an empty string.

**How to apply:**
1. Never branch on a piped command's status. Redirect to a file (`cmd > out 2>&1; rc=$?`),
   then `tail` the file. The rc is real and the output survives.
2. If a pipe is unavoidable: `$pipestatus[1]` in zsh, `${PIPESTATUS[0]}` in bash — and the
   Bash tool here is zsh (`echo $ZSH_VERSION` settles it).
3. Same family as [[2026-08-07_a-check-that-cannot-fail]] (a guard whose only possible reading
   is empty) and [[2026-08-17_check-the-refusal-before-the-kill]] (the refusal must be
   CONSUMED — an empty rc consumes nothing).

**Related:** [[2026-08-07_a-check-that-cannot-fail]], [[2026-08-17_check-the-refusal-before-the-kill]], [[_ledger]]
