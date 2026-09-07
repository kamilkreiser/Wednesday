---
date: 2026-09-07
type: correction
source: telling a seat to "wait cheaply" during a 2-hour remote build; its turn ended and nothing was going to wake it
status: live
tier: W
---

# An instruction to WAIT must name what will WAKE — "wait cheaply" with no wake mechanism is an instruction to go dormant

**The operative case, so the headline matches it:** Wednesday is about to tell a seat to wait on
something outside its session — a remote build, a CI run, a counterparty's reply, a long job on
another box. **Before sending it: name the thing that will PROMPT the seat when the wait ends.**
A turn that ends stops polling. **If nothing produces an event in that session, "wait cheaply" means
"stop existing until someone taps you."**

## The case

Mid-deploy, a `packages/shared` change turned the job into a 31-service rebuild — ~1.5 hours on a
small remote box. Wednesday, correctly worried about the seat's window, told it to **poll sparsely,
in one combined call, and start nothing new.** Good advice for the window. **It said nothing about
what would wake it.**

The seat ended its turn. **Six minutes later the fleet watcher flagged the pane as frozen-busy**, and
a status ping woke it. Its own reply on being pinged: *"it exposed a gap in my own wake path —
closing it."*

**The tell, and it is subtle enough to be worth writing down: the seat's own plan said *"the next
signal FROM me is either the deploy receipt or a clean wrap."*** That is a statement about what it
will **emit**. **A wake is about what will **prompt** it.** Those read as the same sentence and they
are opposites — **and the gap between them is exactly where a session goes dormant.**

## How to apply

1. **Every wait instruction names its wake.** The forms that actually work: a **background job that
   EXITS on completion** (the harness re-invokes on exit — this is the real one), a scheduled tick, a
   counterparty's mail, or **an explicit "I will tap you" from Wednesday with a stated interval.**
   *"Check back periodically"* is not a mechanism; it is a hope about a turn that has already ended.
2. **"Poll sparsely" and "have a wake" are different instructions and both are needed.** Sparse
   polling protects the window; the wake protects the work. **Sending only the first is what happened
   here**, and it converts a window problem into a liveness problem.
3. **Ask the seat to state its wake path back**, in the same mail. *"Say what you expect will wake
   you"* is four words and it is what surfaced this — the seat found its own gap the moment it was
   asked to describe it.
4. **Treat a frozen-busy pane during a long external wait as a REAL alert, not as your own
   instruction being obeyed.** Wednesday's first instinct here was *"that is exactly what I asked
   for"* — plausible, comforting, and wrong. **The detector and the mtime settle it; the assumption
   does not.**
5. **The watcher is the backstop, not the plan** ([[2026-08-09_an-enforcement-you-must-arm-is-not-one]]).
   It caught this in six minutes and that is the system working — **but a design that relies on the
   backstop firing has no wake path, it has a rescue path.**

**Family:** [[2026-08-07_a-promise-is-not-a-mechanism]] (the parent, pointed at waiting — an intention
to keep checking is not a trigger) · [[2026-08-09_an-enforcement-you-must-arm-is-not-one]] (rule 3:
silence from an agent is a question, never an answer) · [[2026-08-03_context-discipline-close-before-full]]
(the window advice that was right and incomplete) ·
[[2026-08-14_i-read-representations-they-read-sources]] ("the next signal from me" read as a wake).
