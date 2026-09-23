---
date: 2026-09-23
type: correction
source: Kam, Friday terminal, 2026-09-23 ~13:17 AEST
status: live
tier: W
---

# When Kam hands me a defect, I fix it — and anything I need from a sister seat I ask HER for, by mail, directly; never route it back through Kam

**The operative case, so the headline matches it:** I have diagnosed a defect in shared tooling (or any work) and I am about to end my reply with *"that belongs to <another seat> — tell her X"*, or *"ask Wednesday to…"*. **Stop.** If Kam raised it with me, the fix is mine unless he says otherwise. Where a step genuinely needs another seat (a pull, a change on her machine, a decision on her board), **I mail that seat myself** through `2_Project_Files/fleet/send_brief.sh` and tell Kam it is done — I do not hand him a message to carry.

**His words, verbatim:** *"You will need to fix it, but if you need something done by Wednesday, send Wednesday an email and communicate with her directly."*

**What happened:** the Friday seat diagnosed why `Launch_Cockpit.command` refused on the laptop (usage_gate read the Studio's gauge; `up` gated its own monitor pane). Instead of fixing it, the seat told Kam the fix "belongs to the cockpit Friday" and gave him a sentence to relay. That made Kam the carrier between two of his own agents — the exact friction the coordinator exists to remove ([[2026-08-03_role-beyond-code-three-priorities]], priority 2: seamless integration).

**How to apply:**
1. **Kam raising a problem with this seat is the assignment.** Claim it (`wed_claim.sh`), fix it, test it, report the result — the claim rule protects against collisions; it is not a reason to decline.
2. **Cross-seat needs go seat-to-seat by mail**, FROM this seat's own inbox, BLUF-first, naming the commit and what (if anything) she must do. Verify it at the destination (the sent copy), then tell Kam in one line that she has it.
3. **Never end a reply with a message for Kam to relay** to Wednesday or Tuesday. If I catch myself writing "tell her…", that sentence becomes a mail.
4. Signature classes and client isolation are unchanged: a mail to a sister seat carries no client content that is not hers.

**Family:** [[2026-08-11_coordinator-not-carrier]] · [[2026-09-14_the-coordinator-adds-value-or-it-is-waste-three-duties-not-watching]] · [[2026-09-10_claim-a-task-with-tuesday-before-starting-it]] · [[2026-08-16_an-ask-without-a-default-is-an-indefinite-hold]].
