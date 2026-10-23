---
date: 2026-10-23
type: preference
source: Kam, live board 2026-10-23 14:31:46 + 14:31:59 (view=wednesday)
status: live
tier: W
---

# Anything that needs Kam is a fleet-activity card; every morning opens with ONE summary card that COUNTS what waits on him; never wait on him; a blocker is flagged, never pushed past; 48 hours unanswered = an email to him

**The operative case, so the headline matches it:** Wednesday is about to tell Kam something he must act on or decide (a login, a deploy hold, a ruling), or it is the morning session, or a card of his has sat unanswered. **The ask is a CARD on the live board's fleet activity, never only a chat line. The morning starts with one card. Silence for 48 hours is an email.**

**His words, verbatim (14:31:46):**
> *"Please put any items that require my attenti on the fleet activity 2) please amend the morning ritual, create a morning fleet activity item with a summary and plan for the day (same format as all others) and flag items awaiting my action (these should be already listed on the board so I do not need descriptions but rather something like - awaiting on 11 items for xxx project, 2 for xx project, etc) 4)Never wait on me, if you or the agents are idle, work through the tickets. Now, spin up as many agents as possible to work through them. 5)naturally if there is a blocker, dont push past it but flag it and remind me / escalate it so it does not slow things down. 6)if there is an unanswered item for more than 48 hours, escalate by emailing me 7)priorities for projects - HPSM-POC then Calculator, then composer so allocate agents based on that priority"*
> 14:31:59: *"ignore point 7"*

## How to apply
1. **Kam's attention = a card.** `decision_queue.sh add` with options, a recommendation and a default, the moment the item exists. A chat line may point at the card; it never replaces it. (Same rule as Friday's 2026-09-24 fleet-activity lesson and the 2026-10-12 needs-go-on-his-board grant; this seat put a login ask and a deploy hold in chat only earlier today: ledger row.)
2. **Morning card (boot prompt step 10a):** one card in the standard format: where things stand, today's plan, and COUNTS of items awaiting him per project ("awaiting 3 for Secuura/Blockchain, 1 for WED"). No descriptions: the items are already cards.
3. **Never wait on him.** While a card waits, agents work the tickets (as many as the code partition and the allowance allow). An idle floor with an open backlog is the failure.
4. **Blockers:** flag, remind, escalate. Never push past one to keep moving.
5. **48 hours unanswered:** `2_Project_Files/tools/stale_card_escalate.sh --send` at every boot (step 10b). One digest mail to kreiser.org@me.com from wednesday-agent@, per card at most once a day; Datasec and Friday cards are their seats' to escalate. Arms run 2026-10-23: quiet now (0), fire with the clock +3 days (1), reminder suppressed 5 h after a send and re-fires after 25 h, dry-send writes no state, the open 14 Oct Datasec card excluded.
6. **Point 7 is withdrawn by him** (project priorities HPSM-POC/Calculator/Composer are Datasec's and not this seat's anyway).

**Family:** [[2026-09-24_decisions-go-on-the-fleet-activity-panel]] · [[2026-10-12_secuura-done-when-tested-works-deployed-and-never-idle]] · [[2026-08-16_an-ask-without-a-default-is-an-indefinite-hold]] · [[2026-09-15_never-idle-the-gatekeeper-widens-the-harness-when-the-pool-runs-dry]] · [[2026-08-07_a-promise-is-not-a-mechanism]] (the 48 h rule is a script, not a note).
