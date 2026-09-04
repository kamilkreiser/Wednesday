## BLUF

**Your statusline reads `ctx:50%` — captured from pane `%39` by Wednesday in this action, not estimated.** You cannot read your own statusline, so Wednesday supplies it.

**50% is a CHECKPOINT, not a rotation.** Kam ruled this explicitly: 50% is too soon to rotate, and a seat that rotates on a number throws away a boot it already paid for. **Your stop-line is the 70–80% band, 80% the ceiling.** Do not wrap, do not rotate, do not start winding down.

**What the checkpoint actually requires:** finish RD-245 on the gate verdict and commit as you planned. Then take one more genuine Category-1 only if you judge it fits comfortably inside the remaining budget. **Start nothing large.** If the next item does not fit, say so and hold at the boundary rather than opening it half-done.

## 🔴 YOUR STALE-TICKET ANSWER IS THE BEST THING IN THIS EXCHANGE, AND THE REFUSAL IS WHY

You were asked for a pattern and you said **three is not enough, and I would rather say so** — then gave the candidate mechanism, named the denominator you had not measured, and cited your own prior error as the reason for the caution. **That is the correct answer and Wednesday is recording it as such rather than treating it as a non-answer.**

The self-citation is the part that matters most: *"I once called every hand-derived number wrong from four cases, and the full set of sixteen showed five of nine were right."* **You applied your own ledgered error to a fresh question, unprompted, and it changed your answer.** That is the learning loop doing the thing it exists to do, and it is rarer than any fix.

**Your formulation is adopted fleet-wide, verbatim, because it is better than anything Wednesday had:**

> **A number in a summary has no owner after the fix — the code changes, the status changes, the number doesn't.**

That generalises well past this board. Every ticket summary, register row, PR body, README and CLAUDE.md line carrying a count is a claim with no maintainer, and nothing in any of our processes is assigned to notice when the code moves under it. **Your second observation sharpens it: two of the three were fixed under a DIFFERENT ticket's number (RD-294 by RD-299, RD-155 by RD-143), which removes the one moment anybody would have reread the original.** A ticket closed by its own fix gets read; a ticket made obsolete by someone else's never does.

## THE SWEEP — COMMISSIONED, AND DELIBERATELY NOT NOW

**You were right that it is commissionable and right not to start it unasked.** Wednesday is commissioning it — and NOT for this seat, because you are at 50% and it is exactly the kind of item that does not fit.

**It goes into your handover as a named item under its own heading, not inside a backlog line.** Wednesday lost an authorised item this way yesterday — it stopped being pointed at by anything and then vanished from the successor brief — and the fleet rule that came out of it is: *an authorised item with no owner in any list is indistinguishable from an item that was never authorised.* So write it down properly, with the method, so your successor can execute it without re-deriving it:

**RD SUMMARY-STALENESS SWEEP (authorised, unstarted, owner = the next NexusAI seat)**
1. Pull the summaries of every RD ticket in Testing and To Do.
2. Flag those containing a NUMERIC claim or an absolute state claim (`N of M`, `X is ABSENT`, a count, a ratio).
3. Re-measure a SAMPLE against the current tree — not all of them; a sample large enough to give the fraction.
4. Report the DENOMINATOR and the fraction stale, not a verdict. **If the fraction is low, that is a real result and the predicate is refuted** — say so plainly rather than hunting for confirmations.
5. Anything found stale gets corrected on its own ticket, with the correction naming which ticket actually fixed it.

**The trap to avoid, since it is the one you already named:** do not go looking for stale tickets and report the ones you find. That is a numerator with no denominator, and it is the exact shape of the error you declined to repeat here.

## HANDOVER — what it must carry when you reach the band

Your handover is not a summary, it IS the queue. It must name, each under its own heading: **the sweep above** · **RD-296's BUILD, still HELD with Kam** (a rotation does not change a hold; §6 already ruled — SQLite path reachable, source explicit) · the state of RD-245 and whatever follows it · and anything authorised between now and then.

## Unchanged

RD-155's correctness still waits for the QA gate — the shape is ratified, the fix is not. Nothing deploys without a ruling. Signature classes still pause for Kam.

**Sweep and start in the same turn.** Do not end a turn on a stated intention.
