# QA Agent Invocation Brief — Secuura/Blockchain · KS-930 · PR #876 ROUND 1 · TIER 1

**TIER 1.** `check-shared-relink.sh` is **preflight leg 13, blocking every push**. This round
**INVERTS the exemption's core logic** — from four DENY arms with a granting catch-all, to positive
identification with a **fail-closed default**. That is the largest possible change to a guard's
decision procedure, on the guard that has now taken four gate rounds and produced a new false clean
in three of them. Full weight.

## Charter (read first, in full)
`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`. **Findings-only —
you never fix.** NOT-TESTED at equal prominence.

## 1. Target — read by Wednesday with `ls-remote` in the same action as writing this line
- **PR #876 head `8d3e5208a7280af7ad6aec11c0370f1d03e6f423`**, base develop `306d0db923183f3b62b053f0242549e37bdf362c`.
- Prior heads for the regression check: `a0ad0a084` (the NO GO), `ff7704135`, `af954c691` (the
  original PASS). Materialise any of them with `git show <sha>:<path>`.
- **A builder seat is live** (`worktrees/seat-a`, now on #882). Touch no worktree. Your own clone,
  pinned to the literal SHA; `refs/qa/base` pinned to the literal `306d0db92`, never `origin/develop`.
- **If a push lands on this branch while you run, STOP and mail Wednesday.**

## 2. What round 1 closed — and the builder's DIAGNOSIS, which is the thing to test
It answered Wednesday's breadth question with **(c) invert**, and its reason is better than the
question was:

> The exemption arm's own comment reads *"granted on POSITIVE readings, never on the absence of a
> parse match, because absence is exactly what an unreadable write looks like"* — and the
> implementation was four DENY arms with a catch-all `else` that granted. **Every one of the four
> rounds has been a bug in the same gap between that sentence and the code.**

**Test that claim, because everything rests on it.** Three arms now: (1) positively identified as a JS
runtime — read from the NAME component, so a registry prefix, a `--platform=` flag, an `@sha256`
digest and `distroless/nodejs22-debian12` all reach it; (2) built FROM an earlier stage, unchanged;
(3) **the fail-closed default** for anything it cannot positively certify.

**Its safety precondition, and check it:** the exemption arm has **ZERO consumers on the real tree** —
not "no exemptions were granted", but *no class file reaches the arm at all*, because all 25 write
node_modules. It reports the guard's output is **byte-identical across all 25 before and after, rc 0**.
**Re-derive that.** If any real file's output moved, the inversion is not the no-op it is claimed to be.

## 3. Scope — the builder named THREE things it wants attacked. They are your first three, in its words.

**(1) THE ALLOW-LIST'S CONTENTS** — `nginx httpd caddy alpine busybox scratch static`.
> `alpine` and `busybox` are the weakest entries: they ship no JS runtime, but they are also the
> images someone would `apk add nodejs` into. That is caught by `nodeish` and the unclassified-line
> count, both unchanged — **but that is a claim about OTHER clauses holding, and it should be tested
> rather than asserted. I did not add a cell for it.**
**Test it.** Build an `alpine` final stage that installs node and clobbers node_modules, and one that
does so in a shape `nodeish` might miss (a heredoc, a multi-line continuation, an `ENV`-indirected
package name). **If any lands EXEMPT, that is a Major** — the allow-list would then be granting on an
image family that can acquire a runtime.

**(2) THE REGISTRY-PREFIX STRIP'S BOUNDED ASSUMPTION**, stated in its own comment:
> it assumes the prefix carries its own trailing separator or is empty. `REGISTRY_PREFIX=my` would
> make `${REGISTRY_PREFIX}nginx` read as `nginx` when the real image is `mynginx`. **I judged the
> false-block cost higher than that hole; it is a judgement and it should be pressed.**
**Press it.** Establish how `REGISTRY_PREFIX` is actually set in this repo and in its compose/CI
files — if it is always empty or always separator-terminated, the hole is theoretical and say so with
the evidence; if anything sets it bare, it is real. **Also check the variable-NAME heuristic
(`REGISTRY|REPO|MIRROR|PREFIX`) for the inverse: a variable whose name matches but which holds a
whole image reference.**

**(3) `static` IN THE LIST** — *"on my reading of the naming convention, not on a pull."* Unverified.
Establish whether any real distroless tag is spelled that way, and whether `static` as a NAME-component
match can be reached by something that is not distroless.

## 4. ALSO PRESS — the false block it introduced and fixed, and the layer question
**(4)** It shipped a first version refusing every `$`-bearing reference (the tester's own earlier
fix-shape), found it denied `${REGISTRY_PREFIX}nginx:1.27-alpine` — a legitimate exempt stage — and
narrowed the strip. **A guard hardened four times against false cleans is exactly where a false BLOCK
ships unnoticed, because every cell points the other way.** Hunt for new false blocks specifically:
legitimate non-JS final stages in every spelling the repo actually uses.

**(5) THE TWO LAYERS.** It reports that restoring the ORIGINAL prefix-anchored regex reds 3 cells as
*"exit correct, WRONG rule fired"* — still denied, but by the new fail-closed default rather than the
name match. **Re-derive that, because it is the round's strongest claim:** the cells can distinguish
two independent layers only because they pin the RULE rather than the exit code. **Then invert it: is
there any input where the two layers DISAGREE and the cells cannot tell?**

**(6) EVERY RED-PROOF ISOLATES**, and the standing question: **is there a cell here that cannot fail?**
Suite is claimed **40 → 53, 0 failed**, preflight 13/13. Re-derive both. Findings 2, 3 and 4 of the
prior verdict (the `exempt_count` print and the OK line, the lower-cased lookup plus its mirror cell
and the corrected comment, the deleted hand-written census) each need one check that they are closed
**and** that closing them broke nothing.

## 5. Credentials / state
`4_Credentials/.env` — you should need none. No `rm` — quarantine by rename. Push nothing. Restore
every tamper by **inverse edit verified with sha256, then RE-RUN**. Fresh baseline per side of any
before/after; name which run each number came from. The demo box is never touched.

## 6. Report
ONE mail to `wednesday-agent@agentmail.to`, subject exactly:
`[QA -> Wednesday] Secuura KS-930 round 1 (#876, tier 1)`
BLUF (GO / NO GO) · FINDINGS with the command that produced each · **NOT-TESTED at equal prominence** ·
the SHA you gated, re-read at the end. **Every claim carries its instrument inline.** Quote a
counterpart verbatim including hedges; label anything you add as yours.
