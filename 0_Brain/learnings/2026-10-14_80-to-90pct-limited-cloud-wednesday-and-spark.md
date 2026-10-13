---
date: 2026-10-14
type: grant
source: Kam, terminal (Wednesday's pane), 2026-10-14 ~06:47 AEDT
status: live
tier: W
supersedes: the 70% thresholds in 2026-09-25_three-tier-routing-ornith-spark-cloud-always-on (rule 4) and 2026-10-06_past-70pct-spark-takes-80pct-of-tasks, for this seat — the band is now 80–90%
---

# From 80% to 90% of the weekly allowance, cloud agents are LIMITED and the work centres on Wednesday and the Spark; above 90% the hard stop stands

**His words, verbatim (answering the morning receipt and card `secuura-92pct-stop-ready-work-waits-1014`):**
> *"thank you. please move to working with the spark.  going forward once we reach 80 - 90% should be the start of limited cloud model usage and a focus on you and the spark"*

**The operative case, so the headline matches it:** Wednesday is about to launch a Claude seat, gate or drafter, or to choose who does the next piece of work, and the weekly gauge (`0_Brain/dashboard/data/usage_wednesday.json`, the statusline's 7-day figure) reads 80% or more. **Below 80%: the normal routing (Spark first for what it can be briefed for, Claude seats in parallel on disjoint code). From 80% to 90%: Wednesday and the Spark do the work; a cloud launch is the exception and its receipt names why the Spark and Wednesday cannot do it (raise, gate or merge of work already done, or the Spark counter exhausted). At 90% and above: the 2026-09-14 hard stop (`fleet/usage_gate.sh`), nothing Claude-shaped launches, no drafters.**

**Today's application (Wednesday's reading, receipted on the panel 06:48, bf-de0d07b13396, with a correction offer):** "move to working with the spark" answers the morning card as (b): the 92% stop is NOT lifted; Wednesday writes Spark briefs herself until the renewal (~Sun 18 Oct) or an account switch.

**How to apply:**
1. Read the gauge at every checkpoint and before every launch, in the same action as the decision.
2. In the 80–90% band, every cloud launch receipt carries `cloud (80-90% band): <why not Spark/Wednesday>`.
3. Brief-writing for the Spark in the band is Wednesday's own work first; a drafter is a cloud launch and follows rule 2.
4. Unchanged: the QA gate before every merge, the signature classes, the Spark counter (original + one rebrief, then a Claude seat), one client per Spark task.
5. **Mechanism:** the 80% advisory belongs in `fleet/usage_gate.sh` beside the 90% refusal (rc 0, loud, naming this file). Shared tooling: claim first (`wed_claim.sh`).

**Family:** [[2026-09-14_at-90pct-weekly-usage-no-new-agents-wednesday-plus-local-model]] (the hard stop above 90%, unchanged) · [[2026-09-25_three-tier-routing-ornith-spark-cloud-always-on]] · [[2026-10-06_past-70pct-spark-takes-80pct-of-tasks]] · [[2026-10-05_spark-target-50-tasks-a-day]] · [[2026-08-03_go-slow-earn-autonomy]] (rule 5: every grant recorded).
