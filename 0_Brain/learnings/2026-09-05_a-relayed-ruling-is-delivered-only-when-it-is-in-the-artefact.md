---
date: 2026-09-05
type: correction
source: Kam's 2026-09-04 07:08 mysql2 ruling, found "unanswered" by the Secuura agent (s133) on 2026-09-05 13:50Z; the card-add gate refused the re-raise
status: live
tier: W
---

# A Kam ruling relayed to an agent is DELIVERED only when it sits in the artefact the next reader lands on — the row, the ticket, the PR — and every ruled-but-undelivered item rides in the successor brief under its own heading

**The operative case, so the headline matches it:** Wednesday is writing a SUCCESSOR brief, or a
morning sweep, or is about to card a question to Kam. **Before any of those: list the cards Kam has
RULED for that project since the last brief and ask, per card, WHERE the ruling now lives.** If the
answer is "on Kam's panel and in a mail to a seat that has since wrapped", it lives nowhere a
reader lands, and the next agent will find the question open and ask it again.

**The case.** Kam ruled `secuura-mysql2-fuse-measured` = EXTEND (to 2026-09-24, with the not-reachable
measurement written on the row) on 2026-09-04 at 07:08 and again at 08:33. Wednesday relayed it the
same morning — it is item "RULING 3 — mysql2 at position 3: yes" in the s123 plan answer and a bullet
in the s123 brief. s123's queue was then pre-empted (the KS-779 record, #799, the 14:38 fleet wrap),
the ruling was never written into `audit-baseline.json`, KS-763 or #801, and none of the ten successor
briefs after it (s124 … s133) carried it — each described the fuse as "the KS-763 pattern: sweep,
measure, regen". On 2026-09-05 at 13:50Z s133 verified the four rows read-only, found #801's body
still asking Kam the mysql2 question, found no ruling on KS-763, and reported it — correctly, from
every artefact it could read — as *"an open QUESTION TO KAM, unanswered since 2026-09-03"*. Wednesday
then began carding it a second time; `decision_queue.sh add` REFUSED and printed his 09-04 words.

**Why this is its own lesson (the w=2 diagnosis).** The 2026-09-04 w=1 row ("an authorised item with
no owner in any list is indistinguishable from one never authorised", s120's line) named the class
and filed no lesson. The mechanism is now clear and it has three parts, each of which passed on its
own: (1) the ruling was RELAYED (mail, DKIM, read) — so Wednesday's record shows it delivered;
(2) the agent's QUEUE absorbed it at position 3 and the queue was legitimately pre-empted — so the
agent's wrap shows a queue, not a debt; (3) the SUCCESSOR brief is built from the wrap and the board —
and a ruling that reached neither the wrap's debts nor the board is invisible to the brief. The card
gate built at w=2 of the sibling class (Kam's word lost across a rotation) caught the RE-RAISE; nothing
caught the NON-DELIVERY, because delivery was never a field anyone owned.

**How to apply:**
1. **A ruled card is not closed until its RECEIPT names the artefact** the ruling was written into
   (the row/ticket/PR/comment), read by Wednesday at origin or on the board. "Relayed to s123" is a
   step, not the receipt.
2. **Every SUCCESSOR brief carries a section `RULED BY KAM, NOT YET IN AN ARTEFACT`** — built from
   `decision_queue.sh list ruled` for that project since the previous brief, each card with its
   ruling verbatim and the artefact it must land in. Empty is a valid section; absent is not.
3. **The morning sweep diffs the ruled cards against the artefacts**, per project, and re-queues any
   ruling whose artefact does not carry it — before any brief is written (the sweep-before-brief rule).
4. **BUILT 2026-09-06 02:3x (w=3 reached on 2026-09-06 00:5x — the F-14 ruling; built by a Wednesday-assistant agent, verified and exercised by Wednesday: refuse path rc 1 with 0 sent lines, pass path on a stubbed copy, fails closed on a broken queue):** `decision_queue.sh` gains a `--delivered
   <artefact>` mark on a ruled card and a `list ruled --undelivered` view; `send_brief.sh --kind brief`
   to a project refuses when that view is non-empty for the project and the body lacks the section.
5. **Test by its handle:** if the successor could read every artefact the project owns and still not
   find the ruling, the ruling is not delivered.

**Family:** [[2026-08-07_a-promise-is-not-a-mechanism]] (a relay is a promise about an artefact) ·
[[2026-08-09_an-enforcement-you-must-arm-is-not-one]] (a filing duty that dies with its seat) ·
[[2026-08-14_i-read-representations-they-read-sources]] (the 09-04 w=82 row: a queue is a record of
what a seat FILED, not of what the principal DECIDED — this is its delivery half) ·
[[2026-08-16_a-recorded-blocker-is-not-a-boundary]] (a recorded question is a claim with a date) ·
[[2026-09-04_decisions-held-narration-drifted]] (the re-raise was caught by a mechanism, not by memory).

## EXTENSION 2026-09-06 02:2x (ledger w=4 of the family): WEDNESDAY'S OWN rulings to a project are rulings too — a scope/holds ruling given in an ANSWER to seat N lives in that mail and in nothing seat N+1 reads
**The case.** Wednesday ruled to the Secuura agent (s133) at 2026-09-05 23:24: *"do NOT narrate KS-823 in a published contract — a defect is not a guarantee."* The s134 SUCCESSOR brief carried the `RULED BY KAM, NOT YET IN AN ARTEFACT` section (Kam's cards, all four verified) and NOT that sentence; s134's F-1a fix wrote "an open defect, tracked as KS-823" into the PUBLISHED yaml, and the tester (KS-816/#831 gate, 16:03:01Z) paused it as approval-class, unable to size the exposure. Zero cost — the amendment removed it before the merge — and the same family as the three Kam-ruling instances above, in the costume the headline did not name: the section covers the PRINCIPAL's rulings and the coordinator's own scope rulings have no section at all.

**The rule, extended:**
1. **Every SUCCESSOR brief carries a SECOND section, `RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE`** — every scope, holds or "do not" ruling from Wednesday's ANSWERs to that project since the previous brief that still binds, each quoted in one line with its mail's timestamp. Empty is a valid section; absent is not. Built from the `briefs_staged/` answers to the project since the last `_successor_brief.md`, read — not from memory.
2. **A ruling that is meant to outlive the round it was given in is written on the TICKET by the agent in the same turn** ("do not narrate KS-823 in the published contract" belongs on KS-820's comment, not only in a mail) — Wednesday's ANSWER says so when it rules, and the agent's receipt names the comment.
3. **Enforcement candidate (w=3 of THIS costume promotes it):** `send_brief.sh --kind brief` greps the previous ANSWERs to the project for lines beginning `RULED` and refuses when none of them is quoted in the body.

**Family, extended:** [[2026-08-04_validate-brief-pointers]] (EXTENSION 2026-09-05 21:3x — a brief carries what the previous mails to the project decided; this is the SUCCESSOR-brief half) · [[2026-08-13_headline-must-match-the-operative-case]] (the section's name said "BY KAM" and the seat wrote exactly that).
