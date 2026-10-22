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

## EXTENSION 2026-10-22 (w=2 of "acked an idle wake without reading progress") — a LIVE waiter is not a WORKING waiter; before acking, read a figure that MOVES
**The case.** D 29th's build waiter was written with an unquoted heredoc, so every path it polled expanded to the filesystem root and its done-test could never be true. The build finished at 07:53:16Z (18:53 AEDT); the seat learned it at 09:2xZ, 1 h 31 m later, when the waiter hit its own bound. Wednesday acked the seat's idle wake three times on "1 shell still running" in the pane footer, the last one at about 19:0x AEDT, after the build had finished. The 21 Oct row was the same shape: acked on "a hook process is running".
**Diagnosis (why the 21 Oct rule did not fire):** that rule said "read the ARTEFACT the seat waits for (origin ref, PR, file)". For a remote build the artefact is on a box Wednesday has no access to, so Wednesday fell back to the nearest thing it COULD read, process liveness, and treated it as the artefact. A liveness signal is a representation of progress, not progress. The rule named artefacts Wednesday can always read; it said nothing about the case where it cannot.
**The rule, extended:**
1. **Before acking an idle wake on a seat that waits on remote work, read a figure that MOVES** — the waiter's own last heartbeat line (ask the seat for its heartbeat path at launch), a progress counter, free disk, load. Process liveness ("N shells running", a hook process) is never enough.
2. **When Wednesday cannot read any moving figure, do not ack: tap the seat** with a pointer asking for its heartbeat's last line. That costs one turn; an hour of a finished build costs more.
3. **Every waiter a brief asks for must print a figure that changes,** and the brief says where that heartbeat lands, so the coordinator can read it.
**Mechanism candidate (w=3 promotes it):** `wake_ack.sh` refuses on a seat whose last mail named a background wait unless a `--progress '<figure> <value>'` argument is given and differs from the previous ack's.
