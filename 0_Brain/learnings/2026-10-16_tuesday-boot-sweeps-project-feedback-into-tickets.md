---
date: 2026-10-16
type: preference
source: Kam, live board 12:54:43 AEDT, view=tuesday
status: live
tier: W
---

# At every boot and every rotation, Tuesday sweeps each Datasec project for new feedback items, tickets them, and starts agents on them

**Kam's words, verbatim (live board, 12:54:43 AEDT, view=tuesday):** "So, as part of your startup process, and every time you renew your seat, check whether any of the projects have feedback items that have been added and categorize these as tickets and start actioning them."

**The operative case:** I am booting, or I have just rotated. Before I pick up the pickup's other work, I run the feedback sweep: for every active Datasec project, find feedback items added since the last sweep, make sure each one is a ticket (categorised), and launch or brief an agent to action them.

## How to apply
1. **When:** every boot and every rotation, not only the morning one. It sits beside the morning ticket sweep ([[2026-08-12_morning-ticket-sweep-autostart]]), and unlike that grant it is not limited to mornings.
2. **Where feedback lands is per project and must be measured, not assumed.** The in-app feedback buttons (MPS feedback pill, HPSM-POC Admin feedback screen to Jira, Composer, QuickQuote/Vision) and the reviews Kam forwards each land somewhere different. The first sweep's job includes writing down, per project, where its feedback lands and how to read it read-only. Record that map in `0_Brain/projects_index/` so later sweeps read it.
3. **"Since the last sweep"** needs a watermark per project, advanced only to the newest item actually processed ([[2026-08-04_never-blanket-markseen-mid-monitoring]]).
4. **Categorise as tickets:** each feedback item becomes a ticket on that project's own board, filed by that project's agent (never by Tuesday's hands: [[2026-08-03_grant-readonly-tracker-access]]). Duplicates of existing tickets get a comment, not a new ticket.
5. **Start actioning:** launch or brief the project's agent under the standing grants. Signature classes (production, money, external comms, irreversible) still pause for Kam. A word or a decision that is Kam's goes on a card with a default.
6. **Production is out of bounds for the sweep (first sweep, 12:58: a GET on the Vision Sales Portal's live feedback report ran `CREATE TABLE IF NOT EXISTS` on the production database; ledger 2026-10-16).** No HTTP to production hosts, not even GET, unless the route's code is read first and proves a pure read. Use the read-only signals the first sweep found: the feedback mail copied to tuesday-agent@ and each project's own Jira search. **Before raising any finding, check Kam's cards** (`decision_queue.sh show`): the Portal report exposure was already ruled 'c' (leave open) on 2026-09-23.
7. **The receipt goes to Kam**: "swept N projects, X new feedback items, Y tickets, agents started on Z", once per boot, not per item.

**Mechanism status (a promise is not a mechanism):** written into NEXT-PICKUP-TUESDAY.md as a standing FIRST WORK line the same session. Owed: a line in the boot prompt (Launch_Wednesday.command builds both seats' prompts, so it is shared tooling: claim with Wednesday first) and a sweep script that reads each project's feedback store.

**Related:** [[2026-08-12_morning-ticket-sweep-autostart]] · [[kams-observations-are-instructions-to-execute]] · [[2026-08-07_a-promise-is-not-a-mechanism]]
