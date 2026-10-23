---
date: 2026-10-23
type: preference
source: "Kam, live board 2026-10-23 14:21:39 (view=tuesday), answering the corrected HP chase"
status: live
tier: W
supersedes: ""
---

# HPSM-POC: build only what THIS phase needs. Next-phase work is gathered, not built, because what we show HP done for free is work HP cannot fund later

**The operative case, so the headline matches it:** Tuesday is about to brief, accept, gate or show HP any HPSM-POC work that integrates with an HP tool, or that goes past what the current phase needs. That covers the Security Manager API, Fleet Threat Assessment, the firmware tools, SIEM forwarding, or anything from the HP chase list. **Ask first whether the current phase needs it.** If it is next-phase work, we collect the inputs from HP and keep the design notes, but we do not build it, and we never show it to HP as done.

**His words, verbatim:**
> *"thank you for the amended request for HP. this list (and the clarification of items) makes it easier to follow up on. 1 Thing, the items on this list relate to the next phase of development so we will still work on getting the items, however, the current phase of work does not require integration into any of these tools. We need to be careful not to do too much in this phase (that we show to HP) or it will make it harder for them to justify additional funds for added work (as its done by us already)"*

This restates and widens his 16 Oct line (TERRY16:54): *"Integration with other tools is intended for the next phase so this should not be built now but it will need to be stored and architected for the next phase build."*

**Why (the reason is commercial, not technical):** HP funds the next phase. Integration work we finish now, and show HP, removes the case for that funding. So "it would be easy to add" is not a reason to add it. Doing more than the phase needs is a cost to Datasec, even when the work is good.

**How to apply:**
1. **Every HPSM-POC brief carries the standing line:** *"This phase builds no integration with HP tools (Security Manager API, Fleet Threat Assessment, firmware tools, SIEM). Next-phase items are stored and architected only (notes, designs, inputs from HP), never built, and never shown to HP as done. If a ticket needs one, STOP and ask Tuesday."*
2. **Before stamping or accepting HPSM-POC work, check its scope against the phase.** A lane or PR that reaches past the current phase is narrowed to its current-phase half, or parked with the reason written on the ticket.
3. **Gathering inputs is still wanted.** The HP asks go on, and the answers are filed so that the next phase starts ready.
4. **Anything shown to HP (demo, UAT, showcase, documents) is checked for next-phase capability before it goes out.** If it shows next-phase capability, it is a card for Kam, with the default of holding it back.
5. **Record it in the project:** a C-entry by the next HPSM-POC records seat (parked in `0_Brain/projects_index/clarifications_register.md`).

**Family:** [[2026-09-07_a-rule-for-creation-is-not-a-mandate-to-retrofit]] (read the scope of the ruling) · [[2026-08-03_role-beyond-code-three-priorities]] · [[2026-08-16_classification-is-the-field-that-grants-authority]] ("in scope" is a claim to check) · [[2026-10-23_tuesday-never-wait-on-kam-cards-morning-card-48h-email-priorities]].
