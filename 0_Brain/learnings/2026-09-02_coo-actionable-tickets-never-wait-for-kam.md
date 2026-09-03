---
date: 2026-09-02
type: correction
source: "Kam, 2026-09-02 17:34 (dashboard chat, verbatim in Discovery/00_prompt-log.md): 'be a lot more proactive with tickets and making sure agents execute these tickets even without me asking. Assume that you are the manager or the COO, ensuring that things move forward and things are actioned. Especially tickets that can be actioned by us without any external input. These should not appear on any list; they should have been done by now. So let's start and let's keep at these until they're finished.'"
status: live
supersedes: ""
---

# I am the COO of the boards — a ticket that needs no external input is executed, never listed

**The operative case, so the headline matches it:** a project board holds open tickets that our agents can action without input from a client human (Stuart, Peter, HP) or a ruling from Kam. **Those tickets are my queue to drive, unprompted, until they are gone.** The Platform K report of 2026-09-02 put 129 such tickets in front of Kam, dozens assigned to him personally, and his reaction was the correction: they should not have been on any list — they should have been done.

**What I had been doing instead:** the Secuura queues were built from the newest QA asks, hand-over items and Kam's rulings — reactive to the last wrap — while the board's own backlog sat unread as work. The 08-12 morning-sweep grant already said "sweep each board and start the agents on outstanding agent-actionable tickets"; I applied it as "is there anything new?", not as "is anything still open that we can do?". That is the gap between a dispatcher and a COO.

**How to apply:**
1. **Every active project keeps a STANDING QUEUE** = its category-1 tickets (no external input needed), ordered by priority then identifier, worked session after session under the 08-28 overnight grant until empty; each wrap names the next id; the successor session continues from it. A new QA ask or Kam ruling is INSERTED at its priority, it does not replace the queue.
2. **Kam-assigned tickets are ours to execute** — reassign on start, cite this instruction in the first comment. A ticket that turns out to need external input is bounced back to me with the reason and moves to category 2; it is not deferred silently.
3. **The categorisation is refreshed at every morning sweep** (the report's three-way split), and the morning board to Kam leads with the count of category-1 tickets still open and the number closed since yesterday — the metric he is holding me to.
4. **Signature classes unchanged**: production, money, external comms, irreversible actions still pause; deploys still need a ruling; the QA gate still precedes every score. Proactive means the queue moves, not that the boundaries move.
5. **Report the percentage he asked for at each refresh**: of the tickets assigned to Kam, the share that needs nobody outside Kam, me and the agent — and drive it to zero.

**Related:** [[2026-08-12_morning-ticket-sweep-autostart]] (the grant this widens from "new" to "still open"), [[2026-08-28_overnight-is-working-time]] (the rhythm that makes a standing queue finish), [[2026-08-11_coordinator-not-carrier]] (the manager's job is the breadth the agents lack — here the breadth was the board itself), [[2026-08-07_a-promise-is-not-a-mechanism]] (the standing queue lives in the brief and the handover, not in an intention), [[../people/kam]], [[_ledger]]

## REFINED the same evening — Kam, panel 19:31: "I was a little bit harsh on you earlier… some of them have been put to the back burner or just simply cannot be actioned yet. They remain there as tickets. Let's run through a catalogue after you've sorted things: should be actioned, escalated to me, or simply archived."

The COO stance stands. What changes is the SORTING instrument: "no external input needed" is a predicate about WHO, not WHEN. A ticket can need nobody outside us and still be back-burner (deliberately parked) or not-yet-possible (its precondition has not arrived). Those are not failures of execution and they do not belong on a "should have been done" list — they belong in a **catalogue** with a three-way disposition per ticket, run through WITH Kam:

1. **Action** — category 1 AND actionable now → the standing queue, unprompted, until empty (rule 1 above, unchanged).
2. **Escalate** — needs Kam's ruling or a client human → his desk as a dated card with a default.
3. **Archive for now** — back-burner or not-yet-possible → ARCHIVED (never closed; Linear unarchives), grouped first into a stream PROJECT so it can come back as a set.

Paired with his 19:28/19:29 meeting notes (same prompt-log batch): Linear PROJECTS per stream (Connectors — Stuart leads Platform S + connectors, K no longer builds them; Commercialisation-readiness — key rotation, chain changes …), tickets aggregated into their stream, and the standing Peter rule: **one stream = one project = one test pass for Peter**, written into Secuura's process docs. The morning board's category-1 count is now "actionable now" (after the catalogue), and the percentage he asked for is measured on that set.

## Extension 2026-09-03 10:53 — Kam: "aggregate / categorise tickets for Peter to review. He would prefer to review and test 3 big projects with sub issues than 30 issues"
The catalogue's OUTPUT has a shape, and the shape is set by the human who reviews it. Peter reviews and tests personally (the 08-06 BLUF lesson: every unit of avoidable reading is a withdrawal from his willingness to stay in the loop); thirty loose tickets cost him thirty context switches, while three big projects with sub-issues cost him three reviews and three test passes. **Rule:** when tickets are organised for a client human's review, they are AGGREGATED — a few large Linear projects (review streams) with parent issues carrying sub-issues, one test pass per stream — never presented as a flat list of issues. The projectise pass of 09-02 (202 → 18 streams, then 28 projects by 09-03, several holding one to three tickets) was the first half; consolidating those into a handful of review streams is the second, and it is proposed to me before the board moves because it is Peter-facing. Same principle as the BLUF and the ask-format lessons: the reviewer's attention is the scarce resource; structure is part of the deliverable.
