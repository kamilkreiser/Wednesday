---
date: 2026-08-16
type: principle
source: "Secuura/Blockchain session 37, establishing four security-review sections in one sitting. Its own one-line summary: 'three of the four register sections overstate, and the one live escalation was hiding under a stale row that would have been discounted wholesale.' Sixth protocol improvement handed to me by a delegated agent."
status: live
supersedes: ""
---

# An overstated record gets discounted WHOLESALE — and the discount lands on the row that is real

**The operative case:** I am about to read, triage, brief from, or act on a register, review,
audit, backlog, risk log or ticket whose rows someone else wrote. **The question is not "is this
row true?" It is "which direction is this row wrong in?" — because the answer is different per
row, and getting one row's direction wrong costs nothing while getting another's costs
everything.**

## The case

A security register's Review A led with *"no role check — any authenticated user can mint a key
for any tenant."* **That half had been false for two weeks** — the role gate landed nine days
after the row was written, and the lines the row cites now contain **the fix**.

**A triager checking the headline finds the fix, marks the row stale, and moves on.**

Underneath it, unchanged and live: **any caller in the admin role set mints a key into any
tenant — and that set includes tenant-scoped roles.** One customer's org admin, into another
customer's tenant, with a wildcard scope the provisioning branch explicitly forbids. **The
overstated half was standing in front of an understated one.**

**Three of the register's four sections overstated. One escalation was real. The discount that
correctly applies to three would have been applied to all four.**

## The second layer, which is the part I had never considered

**The same ticket carried a later re-reconnaissance marking four rows "still present." All four
had been fixed.** So a triager working from the *original* record re-investigates a defect that
is gone, and a triager working from the *correction* does exactly the same thing.

🔴 **A correction that is itself stale is worse than no correction, because it carries the
authority of having been checked.** "Someone looked at this on the 13th" is the strongest reason
not to look again, and it is exactly what makes it dangerous when the looking was wrong.

## Why this is distinct from the lessons it sits beside

[[2026-08-16_a-recorded-blocker-is-not-a-boundary]] says a recorded claim is a claim. **This is
about what happens at the level of the whole document:** individual rows being wrong is normal
and survivable; **a pattern of rows being wrong in the same direction destroys the document's
signal, and the destruction is indiscriminate.** Credibility is spent collectively and
recovered individually — which is the wrong way round for anyone relying on it.

**It also inverts the usual worry.** I spend most of my discipline on not overstating my own
claims. This says the cost of overstatement is not that the overstated claim gets acted on —
it is that **the accurate claims next to it stop being acted on.**

## How to apply

1. **Check every row in BOTH directions.** For each: could this be *less* true than written
   (fixed, superseded, never real)? Could it be *more* true (narrower precondition but a higher
   ceiling, as here)? **A row wrong in its headline is not therefore wrong in its body** — the
   Review A row was false in its precondition and true, and worse, in its consequence.
2. **Date every row against the code, not against the document.** The row was written
   2026-07-21; the fix landed 2026-07-30. **A `git log -S` on the cited symbol settles in one
   command what reading the row never can.**
3. **Treat a re-recon with the same suspicion as the original.** Ask when it ran and against
   which ref. **"Already re-checked" is a claim with a date on it.**
4. **When I report a mixed register, state the stale half as loudly as the live half.** Burying
   the correction protects my finding's drama at the cost of the reader's trust — and the next
   register they read will be discounted because of it.
5. **Writing registers: a row that overstates costs more than a row omitted.** Prefer *"I could
   not establish X"* to a confident row, because an unestablished row invites work and an
   overstated one poisons the well.

**Related:** [[2026-08-16_a-recorded-blocker-is-not-a-boundary]] (the row-level version, and its
"recorded exclusion" extension), [[2026-08-13_headline-must-match-the-operative-case]] (a
headline that misdescribes its own body is how this starts),
[[2026-08-06_bluf-write-for-the-reader]] (the reader who stops early must not be misled — here
they stop early and are misled into stopping),
[[2026-08-16_classification-is-the-field-that-grants-authority]], [[_ledger]]
