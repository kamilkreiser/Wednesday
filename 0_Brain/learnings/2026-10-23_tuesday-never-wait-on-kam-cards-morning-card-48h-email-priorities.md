---
date: 2026-10-23
type: grant
source: Kam, live board 2026-10-23 11:13:53 AEDT, view=tuesday
status: live
tier: W
---

# Tuesday never waits on Kam: everything awaiting him is a fleet-activity card, the morning brings a summary-and-plan card, 48 hours unanswered means an email, and agents work the tickets in the order HPSM-POC, then the Calculator, then Composer

**The operative case, so the headline matches it:** Tuesday is about to (a) mention that something is waiting on Kam, (b) open the morning, (c) leave a seat or the machine idle, or (d) let a card sit unanswered. Do the following:
- (a) It is a card on fleet activity, posted in the same action as the mention.
- (b) The morning starts with a summary-and-plan card.
- (c) Agents work the tickets, in project priority order.
- (d) After 48 hours, email Kam.

**His words, verbatim (11:13:53):**
> *"1) lets create a Jira board for security composer. you should have access to do it and have my permission to do so, if you cannot, please put it on the fleet activity with steps and I will create one. 2) you mentioned 11 items on security composer waiting on my - my fleet activity board is empty. Please put these 11 and anything else that you are waiting on my on on the fleet activity 3) please amend the morning ritual, create a morning fleet activity item with a summary and plan for the day (same format as all others) and flag items awaiting my action (these should be already listed on the board so I do not need descriptions but rather something like - awaiting on 11 items for xxx project, 2 for xx project, etc) 4)Never wait on me, if you or the agents are idle, work through the tickets. Now, spin up as many agents as possible to work through them. 5)naturally if there is a blocker, dont push past it but flag it and remind me / escalate it so it does not slow things down. 6)if there is an unanswered item for more than 48 hours, escalate by emailing me 7)priorities for projects - HPSM-POC then Calculator, then composer so allocate agents based on that priority"*

**How to apply:**
1. **Composer Jira:** a Composer agent creates the project under its own identity, with Kam's permission. The earlier hold on key `PCOMP` (C-71) is lifted by this message. If the token refuses, Tuesday posts a card with literal steps for Kam.
2. **Anything awaiting Kam is a card, never a sentence.** A report that says "N items wait on you" names N cards that exist on the board. Each candidate is verified at source before it is carded; a stale "waiting" row is closed rather than carded.
3. **Morning card, every morning:** the same shape as every other card (BLUF, options, recommended, default). It holds the summary, the day's plan, and counts of what awaits him per project ("awaiting 11 for Composer, 2 for HPSM-POC"), with no descriptions, because those already live on the board.
4. **Never idle:** when a seat or the machine has room, the next action is a ticket lane. Launch as many agents as the code partition and the machine allow (load1 < 7, waves of launches), allocated in the order **HPSM-POC → MPS Calculator → Security Composer**.
5. **Blockers:** never pushed past. They are flagged as a card, re-raised, and escalated so they do not slow anything.
6. **48 hours unanswered → email Kam** at kamil.kreiser@datasec.com.au. The subject names the card, and the body carries its BLUF and default. This is a mechanism, not a habit.
7. Unchanged: the v1.3 signature classes, the QA gate before every merge, CodeQL, client isolation, and the routing table (Sonnet first on this seat).

**Family:** [[2026-09-24_decisions-go-on-the-fleet-activity-panel]] · [[2026-10-12_secuura-done-when-tested-works-deployed-and-never-idle]] (Wednesday's twin) · [[2026-09-02_coo-actionable-tickets-never-wait-for-kam]] · [[2026-09-15_never-idle-the-gatekeeper-widens-the-harness-when-the-pool-runs-dry]] · [[2026-08-16_an-ask-without-a-default-is-an-indefinite-hold]] · [[2026-09-11_a-number-left-for-kam-in-a-handover-reaches-no-surface-he-reads]] · [[2026-08-03_go-slow-earn-autonomy]] (rule 5: every grant recorded).
