---
date: 2026-09-07
type: correction
source: a board catalogue finding — one failure filed four times in 31 hours, every session having correctly run a control
status: live
tier: M
---

# A control proving "this failure is not mine" answers the wrong question — the next one is "then who already filed it?"

**The operative case, so the headline matches it:** an agent hits a failing check, a red suite, a
broken guard, a lint error it did not cause. **It does the right thing: it runs a control and
establishes the failure is PRE-EXISTING, not its own doing.** It then files a ticket. **Stop there.
The control answered "is this mine?" and the question that actually decides what to do next is
"has someone already filed this?"** Those are different questions, and only the first one has a
control.

## The case, stated without a client in it

One guard failing on the mainline was filed **four separate times across 31 hours**, by four
sessions. **Every one of them did the disciplined thing** — ran a control, proved with evidence that
the red pre-dated its own work, and declined to claim it. **Not one of them searched the board for
the failure first.** Two of the four went further and independently identified the same root cause,
in the same words.

The same pattern produced **five findings carried by fourteen tickets** on that board.

**So this is not a discipline failure. It is a discipline that STOPS ONE QUESTION SHORT** — which
makes it far more durable than carelessness, because every session involved was doing exactly what
it had been taught, and each one's own record looks correct in isolation.

## Why it is invisible from inside a session

**A duplicate is only visible from OUTSIDE the session that files it.** Within one session the
sequence is flawless: hit red → control → not mine → file → move on. Nothing in that loop can
surface the other three. It took a whole-board pass to see it at all, which means **it will recur
until something in the path checks, not until agents try harder.**

**And the cost is not just the duplicate ticket.** The board grows with work that reads as new
findings; the count that a principal reads as "how much is wrong" inflates; and the reviewer's
attention — the scarce resource — is spent four times on one thing.

## How to apply

1. **Before filing ANY finding, search the board for it.** Search by the SYMBOL, the file path, or
   the error string — **never by your own phrasing of the problem**, which is exactly the thing that
   differs between four sessions describing one failure. Say in the ticket what you searched and
   found nothing: *"searched `<symbol>` and `<path>`, 0 open hits."* That line is cheap and it makes
   the absence checkable.
2. **A control that proves "not mine" is HALF the check.** Pair it, always: *"pre-existing (control:
   red at base) AND unfiled (search: 0 hits)."* A finding reported with only the first half is
   incomplete, and a coordinator receiving one should ask for the second.
3. **If it IS already filed, add your evidence to the existing ticket and say so** — the second
   session's control is worth more than the second session's ticket, because two independent proofs
   of the same red is genuinely stronger evidence than one.
4. **When several sessions work one repo in a window, the risk is highest** — a relay, an overnight
   run, parallel seats. The same red is in front of all of them.
5. **For whoever writes the brief:** this belongs in the standing lines, not in an agent's memory.
   An agent cannot see the other three sessions; only the path can.

## The general shape, worth keeping past this instance

**A check that is correct, disciplined and answers a slightly different question than the one the
decision needs is the hardest kind to catch** — it passes every review, it produces evidence, and it
feels like rigour. The tell is when the check's OUTPUT and the DECISION it feeds are not the same
proposition: *"the red is not mine"* is about attribution; *"this should be filed"* is about
novelty. **Whenever a control's conclusion has to be silently widened to justify the next action,
that widening is where the defect lives.**

**Family:** [[2026-08-07_a-check-that-cannot-fail]] (the parent family — but note this check CAN
fail and did its job; it simply measured a different proposition than the one being decided) ·
[[2026-08-14_i-read-representations-they-read-sources]] (a control's output is not the claim built on
it) · [[2026-09-02_coo-actionable-tickets-never-wait-for-kam]] (Kam's aggregation rulings — the
board's shape is the reviewer's reading cost) · [[2026-08-06_bluf-write-for-the-reader]] (four
tickets spend a reviewer's attention four times on one thing).
