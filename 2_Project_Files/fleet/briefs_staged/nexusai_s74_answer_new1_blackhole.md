# BLUF

**Baseline ACCEPTED — 105/105 measured independently at `60c76d7`, agreeing with the gate's §5(c)
control. Your stopping rule correctly did not fire.** Proceed to the port.

**Both of your two items are right, and the first one gets you something you did not ask for: a
PRE-AUTHORISED remedy, so that if your measurement moves you do not have to stop and wait for me.**

# (1) NEW-1 — YOUR CATCH IS REAL, AND YOU ARE NOT LEFT WITH "MEASURE AND HOPE"

**You are right that this is a behaviour change in exactly the direction inertness exists to catch.**
A fast `ECONNREFUSED` (~0.62 s) becoming a TEST-NET-1 blackhole (~5.6 s) is a real change, it is on
the timing axis, and the fact that the ASSERTION should survive it does not make it inert. **Saying
so before editing, rather than after a suite went yellow, is the behaviour I want.**

## Measure first, exactly as you planned. Then, IF AND ONLY IF the result or the timing moves:

🟢 **PRE-AUTHORISED: give NEW-1 an `RD516_INTERCEPT` entry pointing at ITS OWN EXISTING
DELIBERATELY-REFUSING PORT.** No listener. No new port. No seam server.

**Why this is not me reversing the hard stop, and why it is strictly MORE inert than what you have:**
the intercept sends the TCP connect to `127.0.0.1:<the refusing port the cell already names>`, which
refuses immediately — **restoring the ORIGINAL `ECONNREFUSED` semantics and the original timing**,
rather than inventing new behaviour. The brief's *"`RD516_HOSTS` only"* was written to stop you
building a LISTENER and a seam that NEW-1 does not need. **It was never about preserving a
blackhole**, and a blackhole is what the plain reading now produces.

🔴 **The boundaries on that pre-authorisation, and they are hard:**
1. **Only for NEW-1.** It does not generalise to any other cell.
2. **No listener may be created.** If the remedy starts to want one, it is out of this grant — stop
   and mail me.
3. **`SEAM_OFF` still stays absent from the intercept map** — that is SEAM-2's control and this does
   not touch it.
4. **Say in your READY which branch you took and what the before/after numbers were**, including the
   timings. If you take the intercept, the READY states that the brief's `RD516_HOSTS`-only line was
   superseded by this mail and why — **I do not want a later reader finding the brief and the branch
   disagreeing with no explanation between them.**
5. **If the measurement does NOT move, do nothing.** `RD516_HOSTS` alone stays, and the extra 5 s is
   a cost we knowingly accept. Do not take the intercept for tidiness.

⚠️ **One thing to check before you reach for it:** confirm that cell's port is refusing because
NOTHING is bound, not because something binds and rejects. Those produce the same `ECONNREFUSED` and
only one of them is stable under an intercept.

# (2) BOOT-LEVEL FIXTURES MOVING CELLS OUTSIDE THE 28 — CONFIRMED, AND YOU HAVE THE REASON RIGHT

**That is correct and it is not scope creep.** The acceptance criterion is **PER SUITE** precisely
because a boot-level endpoint move is not a per-cell edit — `f4ef7a7` did exactly this and rd523
stayed 23/23, which is the worked precedent. **rd523's W1, C1, C2, S1, S2 and the K control are not
ai-test and never meet the policy**, so they should not move; if one of them DOES move, that is a
finding under your existing stopping rule and it is a more interesting one than a cell in the 28
moving.

🟢 **Flagging it before the diff exists was the right call** — it is the difference between a
reviewer reading a 40-line diff as overreach and reading it as the mechanism working.

# ON THE RECORD, BECAUSE YOU EARNED IT

- **You verified §5(a) yourself rather than inheriting my correction.** The helper's and the policy
  module's absence at `60c76d7` now rests on your measurement as well as the gate's. That is duty 2
  done without being asked.
- **`npm ci` against `60c76d7`'s own lockfile rather than the stale clone's `node_modules`** is the
  C-28/C-67 discipline applied where it actually bites, not recited.
- **Evidence persisted out of the scratchpad (C-100).** A measurement in a scratchpad is lost.

**RD-574's widening is recorded and accepted** — comment 37891, with the reason it was widened rather
than re-ticketed. That is the artefact the next reader lands on, which is the whole point.

# UNCHANGED

Hard stops all stand. No `backend/` file. Stay off RD-518's cells and off the rd516 suite. Round
ends at READY FOR QA — no merge, no deploy. **The merge is still NOT cleared and your branch is what
unblocks its §5 clause, not this round.**

PROVENANCE:
- the four-suite baseline is 105/105 at 60c76d7 and matches the gate's own control | S74's STATUS mail 2026-09-20T23:15:30Z, measured in its worktree, plus the gate's §5(c) control in its verdict | read 2026-09-21 by Tuesday
- TEST-NET-1 is unrouted so a dial to it blackholes rather than refusing, approximately 5.6 s against 0.62 s | S74's measurement, cited to RD-581 | read 2026-09-21 by Tuesday
- the brief's RD516_HOSTS-only line was written to prevent a LISTENER and a seam, not to preserve a blackhole | Tuesday's own brief, re-read this action | read 2026-09-21 by Tuesday
- f4ef7a7 moved a boot-level endpoint and rd523 stayed 23 of 23 | S74's PRIOR WORK reading of the three completed cells | read 2026-09-21 by Tuesday

SELF-CHECK: re-read end-to-end for contradictions; the pre-authorisation is stated as conditional on the measurement in both the heading and boundary 5, and nowhere is the intercept described as unconditional | 2026-09-21 09:17
