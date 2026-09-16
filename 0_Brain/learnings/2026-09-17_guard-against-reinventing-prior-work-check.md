---
date: 2026-09-17
type: preference
source: Kam, panel (view=tuesday) 2026-09-17 08:22:42 and 08:27:06 AEST
status: live
tier: W
---

# Tuesday is the guard against reinventing the wheel: every brief carries a PRIOR-WORK CHECK, and a READY FOR QA without a PRIOR WORK section goes back

**The operative case, so the headline matches it:** Tuesday is writing a brief, reviewing a READY FOR QA, or commissioning a gate for any Datasec project, and the work rebuilds, replaces, removes or redesigns something that already exists. **Before it is accepted, the agent must have shown what was built before and why.**

**His words, verbatim (08:22:42):**
> *"I've noticed that recently Claude has been reinventing the wheel and redoing things without fully checking what's been built before and why. Can you act as a guard to make sure that this doesn't happen? I don't want each project to redo what we've already done without the necessary context and potentially take the project further back."*

**And the principle for what to do with what is found (08:27:06, on the NexusAI package lineage):**
> *"Fantastic, thank you for checking. Keep what works and what is logical. Improve what needs work."*

**The case that earned it, the same morning:** NexusAI's package lineage found 22 deploy-time setup features and checks present in earlier offers (the AI one-token preflight, the Key Vault read-back, Redis wiring, post-deploy next steps) that had disappeared from main with no recorded reason. Nobody removed them on purpose; successive rebuilds simply did not look back.

## How to apply
1. **Every Datasec brief carries the PRIOR-WORK CHECK standing line:** before rebuilding, replacing, removing or redesigning anything, look (git log -S / --follow / blame, the project's CLARIFICATIONS, history and handovers, the tickets, earlier versions or packages), write down what existed and WHY with its source, then keep what works and is logical, improve what needs work, remove only with a stated reason.
2. **Every READY FOR QA must carry a PRIOR WORK section** (or "nothing replaced"). Tuesday returns a handover without it; this is the in-path check, not a hope.
3. **Every gate brief asks the tester to verify the PRIOR WORK section against the history** for anything replaced or removed.
4. **Tuesday's own briefs obey it too:** before commissioning a rebuild, Tuesday asks the agent what exists rather than specifying from scratch (the 2026-09-16 SME rule: the agent holds the history).
5. **Scope:** Tuesday's seat and the Datasec projects, as he addressed it on the Tuesday tab. Whether Wednesday adopts it is hers and Kam's (a board message is not a fleet rule).

**Family:** [[2026-08-13_establish-authority-before-reconciling]] (reconciliation destroys evidence) · [[2026-09-07_a-rule-for-creation-is-not-a-mandate-to-retrofit]] (enumerate what already occupies the slot) · [[2026-09-16_what-keeps-a-seat-correct-is-not-all-in-git]] · [[2026-09-14_the-coordinator-adds-value-or-it-is-waste-three-duties-not-watching]] (duty 2: check the output as a manager).
