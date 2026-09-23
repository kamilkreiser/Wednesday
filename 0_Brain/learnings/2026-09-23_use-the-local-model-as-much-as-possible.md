---
date: 2026-09-23
type: preference
source: Kam, terminal, 2026-09-23 ~15:3x AEST — "also, please use the local LLM as much as posible for tasks and tickets"
status: live
tier: W
---

# Route tasks and tickets to the LOCAL model (the Spark) first — as much as possible; Claude seats take what it cannot do

**The operative case, so the headline matches it:** Friday is about to hand a task or a ticket to a worker (a Claude build seat, a
subagent, or herself). **Ask first: can the local model do this, under the kit's rules?** If yes, it goes to the Spark
(DeepSeek V4 Flash, `learnings/2026-09-23_spark-kit-running-a-local-coding-model.md`). Claude seats take what it cannot do.

**How to apply:**
1. **The Spark loop must be PROVEN before real tickets go near it:** the owed smoke test (a trivial known change plus the two
   deliberate breaks) comes first. "As much as possible" makes that the next piece of work; it does not waive it.
2. **Route per ticket, by the kit's predicate** (one product file · the fix shape spelled out · a runnable test nearby · not an
   auth/credential/security surface · a runner the checker can run). Greenfield multi-file scaffolding usually fails it: a Claude
   seat builds the skeleton, then per-file tasks go to the Spark. **Carve tickets so more of them fit**: that is how "as much as
   possible" is achieved, not by forcing unfit tickets through.
3. **The counter still binds:** original brief + ONE rebrief, then the ticket goes to Opus 5.5 in the cloud.
4. **Client scope of the box:** the Spark is `datasec-rd` hardware. Datasec work (HPSM-POC, HPSM, …) is in scope; Secuura code
   stays off it until Kam rules (open question on the Spark lesson).
5. **Record the routing** in every brief or receipt: "local — <why it fits>" or "Claude — <which clause fails>". The routing
   predicate is measured at the weekly consolidation (how many local, how many reallocated, and why).

**Family:** [[2026-09-23_spark-kit-running-a-local-coding-model]] · [[2026-09-16_local-model-is-long-term-and-claude-takes-what-it-cannot-do]] (Wednesday's same rule for Ornith) · [[2026-09-23_build-seats-run-in-cockpit-panes]].
