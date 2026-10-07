---
date: 2026-10-08
type: preference
source: Kam, live board 2026-10-08 10:45:37 view=wednesday, right after ruling card secuura-ks1450-leg14-who-fixes-1008 = a ("Let us fix it now")
status: live
tier: W
---

# We fix our own problems and tickets — Peter is involved only sporadically, never as the default blocker

**The operative case, so the headline matches it:** a Secuura problem has turned up (a red gate, a defect in Platform K, a broken guard, a failing check), and Wednesday is about to route it to Peter, wait for his answer, or ask him a question before acting. **Stop. Fix it ourselves:** measure it, choose the remedy, build it through a seat, gate it, merge it, and leave Peter a short ticket note saying what changed so he can reshape it. Involve him only when the decision genuinely needs his knowledge or his authority, and then only now and then.

**His words, verbatim:** *"We are working on a new approach where we fix our own problems and tickets and only involve Peter sporadically."*

**How to apply:**
1. **Default to fixing, not asking.** "It's Peter's code" (his guard, his baseline, his test) is not by itself a reason to wait. Platform K is ours (Kam 2026-09-06). KS-1450 (Peter's guard KS-1386 + his baseline from #1424) is the first case: ruled (a), fixed by us.
2. **The quality bar does not drop.** Every fix goes through the tiered QA gate and Wednesday's completion check. A fix to someone else's guard is red-proofed so the guard still fails on the thing it exists to catch.
3. **Peter is TOLD, not ASKED:** one BLUF ticket comment per fix (what changed, why, how to reshape it). That comment is information, not a gate, and it is not a request for review.
4. **What still goes to Peter (sporadically):** knowledge only he has (why he designed something a certain way, when that changes the remedy); his own ticket assignments (a ticket on Peter stays his, per the 2026-09-06 correction); demo/UAT handovers where his nod is still the rule. Batch these; never one at a time.
5. **What does NOT change:** the v1.3 signature classes; client-facing communication is ticket comments only, and Kam sends anything else; ticket assignment rules.

**Family:** [[2026-09-02_coo-actionable-tickets-never-wait-for-kam]] (the same stance pointed at Peter instead of Kam) · [[2026-09-11_secuura-we-approve-and-merge-our-own-tested-work]] · [[2026-09-05_tickets-are-the-channel-whatsapp-via-kam-is-the-escalation]] · [[2026-09-01_qa-gate-before-my-verification]].
