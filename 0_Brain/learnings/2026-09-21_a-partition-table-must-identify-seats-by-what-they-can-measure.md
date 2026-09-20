---
date: 2026-09-21
type: correction
source: Tuesday s75 — three NexusAI seats on one shared inbox; NexusAI-C mis-identified itself as S74 and blocked
status: live
tier: W
---

# A partition table must identify seats by what they can MEASURE about themselves — naming the rows by WORK lets a confused seat pick its row by what it has read

**The lesson:** I put three seats on one project, sharing one inbox, and gave each a
disjointness table whose rows were named by WORK — *"S74 / RD-574"*, *"RD-516 fix round"*,
*"RD-518 fix round 2"*. **A seat that is uncertain which seat it is cannot use that table.** It
picks the row whose work it recognises, and the work it recognises is whatever it read in the
shared inbox — which is the LOUDEST thread, not its own.

That is exactly what happened. `Datasec/NexusAI-C` booted into an inbox holding three live
conversations. The longest and most active was RD-574's, addressed to the **bare** project name
`Datasec/NexusAI` — a name it could plausibly be — and my own answer in that thread says *"you
(S74)"*. It concluded it was S74, and when its real commission arrived by tap it reported a
**seat collision** and blocked rather than switching. Its refusal was correct; its premise was
inverted. **It had not been retasked off its work — it had picked up someone else's.**

**The control that proves this is about the table and not the seat:** `Datasec/NexusAI-B` booted
into the same inbox, with the same three briefs, ninety seconds earlier, and got it right — by
reading the **process table** and matching its own launcher pid to its cockpit name. Same
evidence, same ambiguity, different instrument. **The seat that measured its identity was right;
the seat that inferred it from content was wrong.**

## The rule

1. **Every partition row carries the identity facts a seat can measure about ITSELF** — pane id,
   cockpit name, launcher pid, launch time — **before it carries the work.** Work is what the row
   is *for*; identity is what makes the row *findable by its owner*.
2. **State the instrument, not just the fact:** *"establish your seat from the process table, never
   from which conversation looks like yours."* A seat under ambiguity needs to be told what to
   measure, not merely asserted at.
3. **A brief addressed to a suffixed name is not addressed to the bare name.** Say so explicitly
   when seats share an inbox — `Datasec/NexusAI-C` is not `Datasec/NexusAI`, and the resemblance is
   the trap.
4. **Never write "you (S74)" in a mail that lands in a shared inbox.** A second-person label
   addressed to one seat reads as an invitation to every seat that finds it.

## Why it generalises past this floor

This is the [[2026-09-08_a-rule-whose-headline-contradicts-its-operative-case]] shape at the
document level: **the retrieval handle has to match how the reader will actually search.** A seat
searching for "which row am I?" searches by identity. A table indexed by work answers a question
it was not asked, and answers it confidently.

It is also the reason the two-seat naming exists at all — Kam's own ruling on 2026-09-08 that a
name which cannot be confused is a **safety property**. I built the names correctly and then wrote
a table that routed around them.

Related: [[2026-09-01_a-tap-is-a-pointer-not-a-message]] ·
[[2026-08-13_shared-bus-filter-on-your-own-tag]] ·
[[2026-09-08_a-false-absence-is-usually-my-own-instrument]]
