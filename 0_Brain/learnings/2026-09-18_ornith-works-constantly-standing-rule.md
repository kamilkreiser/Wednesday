---
date: 2026-09-18
type: grant
source: Kam, panel 2026-09-18 09:16:16 AEST (view=wednesday), verbatim
status: live
tier: W
expires: none — Kam called it a STANDING RULE
---

# STANDING RULE: the local agent works CONSTANTLY on the tickets it can — an idle Ornith is a rule being broken, not a gap to notice later

**His words, verbatim (09:16:16):**
> *"The credits have reset, so please start up all agents and continue the work. Also, as a standing rule, I'd like the local agent to be constantly working on the tickets that it can."*

**What changed, and why it needed its own file.** Ornith's never-idle discipline existed before this — but as a CORRECTION, built from repeated failures (🔴 rows on 09-15, 09-16 and five times on 09-17) and carried in the ledger. A correction is something a seat is blamed for after the fact. **Kam has now made it a STANDING RULE, stated in the first person and unprompted**, which moves it from "a failure mode to avoid" to "a duty to schedule". The difference is operational: a duty is planned for at boot and at every checkpoint, not discovered when a tap fires.

**The qualifier is load-bearing: "the tickets that it CAN."** It is not an instruction to feed Ornith anything. Today produced three measured reasons a ticket is legitimately not for it — decision-class (the ticket's own words say a ruling comes first), infeasible-in-harness (KS-1237 X-INFO: the route is not served by that test file), and counter-spent (original + one rebrief both used). **Those remain valid answers.** What is NOT a valid answer is an empty queue with no reason recorded — that is the rule being broken.

## How to apply

1. **At boot and at EVERY checkpoint, check the queue before choosing your own next task.** `night/queue.md` empty + no runner = the standing rule is being broken right now.
2. **Keep a scoped-and-ready next job in the pickup at all times**, so refilling costs minutes rather than an hour of triage. Today's is KS-1230, with its handler line, test target and pre-flight check already recorded.
3. **When the pool genuinely thins, WIDEN rather than stop** ([[2026-09-15_never-idle-the-gatekeeper-widens-the-harness-when-the-pool-runs-dry]]) — and with agents available, the widening tool is a search commission, which is what a whole morning of hand-sampling proved slower than.
4. **If the queue must be empty, write WHY where the next reader lands** — the reason is the artefact, and "I didn't find anything" is not one.

**Family:** [[2026-09-15_never-idle-the-gatekeeper-widens-the-harness-when-the-pool-runs-dry]] (the correction this promotes) · [[2026-09-16_local-model-is-long-term-and-claude-takes-what-it-cannot-do]] (the router: Claude takes what Ornith cannot) · [[2026-09-16_if-something-blocks-move-on-to-the-next]] (a blocked item is skipped, never waited on) · [[2026-09-14_ornith-runs-at-night-in-the-downtime-a-standing-rule]] (the night shape this widens to all hours).

## EXTENSION 2026-09-25 15:33 — Kam, live board (view=wednesday), verbatim: *"I understand why Ornith is idle.  I expect it will be until we get some tickets which are suitable for Ornith"*
- **An idle Ornith whose queue is empty FOR A WRITTEN, MEASURED REASON is accepted by Kam, and is not a rule being broken.** Today's reason: three screens over ~280 KS tickets found no briefable one-file candidate outside the live lanes (the why-line in `night/queue.md`).
- **What still binds:** rule 4 above (write WHY the queue is empty where the next reader lands), and re-screen whenever the pool changes (a lane wraps and frees files, new tickets are filed, a gate's NOT-PINNED rows arrive). The G7 idle alarm is silenced with `night/PAUSE_QUEUE` plus the reason, never by ignoring it.
- **The medium work goes to the Spark now** (Kam 2026-09-25 15:28), so a ticket too big for Ornith is not an Ornith gap; it is the Spark's queue.
