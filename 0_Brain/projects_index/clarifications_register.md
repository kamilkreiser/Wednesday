# Datasec clarifications register (Tuesday seat)

**Why this file exists.** Kam, panel 2026-09-17 08:36:20 (view=tuesday), verbatim: *"Please keep these notes for future reference and create a rule to do so with any project so that clarification can be utilized at any time."* Each project keeps its own agent-written `1_Project_Definition/CLARIFICATIONS.md` (read at that agent's boot). This register does two things the project files cannot: it shows which projects have one, and it holds any Kam clarification for a project that has **no live agent**, verbatim, until that project's next session records it and mails back the C-number.

**Rule (every Datasec project):**
1. Every clarification, ruling or "this is how it was / how it should be" from Kam about a project is recorded in THAT project's CLARIFICATIONS file, verbatim with date and channel, the same session.
2. Project has a live agent → relay it, and the relay is not done until the agent mails back the C-number.
3. No live agent → park it below, verbatim. The project's next brief carries it under RULED BY KAM, and the row moves to "recorded" with the C-number.
4. A project with no CLARIFICATIONS file → its next brief's first item is to create one (format as NexusAI's: numbered C-entries, provenance on each, supersede never delete) and wire it into the project's boot read.

## Status by project (census 2026-09-17 08:3x, `ls` of each `1_Project_Definition/CLARIFICATIONS.md`)
| Project | File | Boot read | Notes |
|---|---|---|---|
| NexusAI | yes (C-01 … C-50) | yes | live S63 |
| HPSM | yes (C-01 … C-67) | yes | live S49 |
| ATTIO · Commercial Readiness · CypherKey · Feedback_System · HPAM · Lead_Bot · Marketing_Collateral · myPKI · RESEARCH · Security Review · Task_Dispatcher · Vision_Sales_Portal · Websites | **no** | — | create at next session |

## Parked clarifications (projects with no live agent)
- **2026-09-22 Vision_Sales_Portal / QuickQuote: a TESTER feature request, relayed by Kam** (live board 13:34:55, view=tuesday, verbatim excerpt): *"is it possible to have a way to pull up old quotes for modification in the QQ tool? ... not at the moment as its not a log in process but I could add this if you like ... Just added it as feedback ... it will have to wait until Monday ... OR maybe have a way to load quote after it is saved locally with the Email me the quote - so the storage burden for revisiting is on the person generating the quote. I think, the Qute number can be entered. it sends email to person who created it or checks that that user is in the system. If yes, pulls up the old quote. We could always have a golden key"*. Status: a REQUEST, not a ruling; Kam told the tester Monday. Next Vision brief carries it; a PRIOR-WORK CHECK first (QuickQuote already has sign-in + a quote number).
- **2026-09-22 Vision_Sales_Portal / QuickQuote: feedback routing (open, offered to Kam 13:3x).** Feedback is stored and mailed to `FEEDBACK_NOTIFY` (stage3/server.js:59, value from config, unread by Tuesday). Kam confirmed he gets it by email. Offered: he forwards to tuesday-agent@ now; adding Tuesday as a second recipient in the next QuickQuote release needs his go (live tool).

- **2026-09-22 Vision_Sales_Portal (QuickQuote + portal) + NexusAI: KAM RULING, live board 13:38:02 (view=tuesday), verbatim:** *"Update the code so it goes into the next change and bundle it so that when we finish the current round of changes in Nexus we make this update. It would be good if all feedback tools CC'd you in on them, and that way we have an active live monitoring system of anything that needs doing. I added one change above and will forward another once you get my email action both."* **Tuesday's reading (receipted 201):** (1) every feedback tool notifies tuesday-agent@agentmail.to as well as Kam: QuickQuote (FEEDBACK_NOTIFY, stage3/server.js:59), the Vision portal feedback store, and NexusAI's in-app feedback; (2) the QuickQuote bundle = the notify change + the tester's "pull up an old quote by quote number" request + the change Kam will email; it STARTS when the current NexusAI round finishes; (3) NexusAI's own notify change is a ticket for the round AFTER the resubmission. **OWED: brief a Vision seat with this bundle when the NexusAI round finishes. The live-tool deploy is covered by his "we make this update", flagged to him at deploy as a production change.**

## Recorded (relay closed)
- 2026-09-17 NexusAI: RD-474 ruling C-42, live listing C-43, RD-460 C-44, keep config/checks C-45, see-what-was-built C-46, RD-454 C-47, RD-470 C-48, prior-work check C-49/C-50; containers + GPT only (08:34:33) C-51 (5.3 medium = Phi-3 medium via Ollama, per RELEASE-NOTES-1.7.1.md:149).
- 2026-09-17 HPSM: re-verify C-62 (+ Tuesday readings C-63/C-64), prior-work check C-65/C-66.
