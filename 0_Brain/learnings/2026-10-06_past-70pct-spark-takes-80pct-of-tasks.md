---
date: 2026-10-06
type: grant
source: Kam, live board 2026-10-06 09:37:54 (view=wednesday)
status: live
tier: W
---

# Past 70% of the weekly allowance, the Spark takes 80% of tasks; Claude seats only for what it cannot do

**His words, verbatim (09:37:54):**
> *"we are past 70% of the weekly allowance.  We now need to switch to using the spark for 80% of tasks"*

**The operative case, so the headline matches it:** Wednesday is about to launch a Claude seat, a QA gate or a drafter subagent, or to route a ticket, while the weekly gauge is at or over 70%. **Route to the Spark first.** A Claude launch happens only when the task is something the Spark structurally cannot do: raise a PR, run a QA gate, merge, or a task that failed the Spark counter (original + one rebrief). Each launch receipt names that reason.

**Wednesday's reading, receipted on the panel 09:3x with a correction offer:** the seats already running (E 6th KS-1256, B 65th #1393 round 2, gate66, gate67) finish their current work. Every NEW task routes Spark-first. Brief-writing for the Spark is a cost that sits on Claude, so keep it lean: batch briefs, and prefer tickets whose fix shape is already spelled out.

**How to apply:**
1. **Measure the 80%, don't assert it.** At every checkpoint and in the daily receipt, count tasks routed to the Spark versus Claude seats/gates started since 2026-10-06 09:37 (from `local-model/spark/` run dirs and the cockpit launch log), and report the share.
2. A Claude launch receipt says which clause applies: "cloud: raise/gate/merge" or "cloud: Spark counter exhausted on <ticket>".
3. **Unchanged:** 90% is the hard stop (`usage_gate.sh`); the QA gate before every merge; the signature classes; client scope (one client per Spark task). This tightens [[2026-09-25_three-tier-routing-ornith-spark-cloud-always-on]] rule 4 into a numeric target, and supersedes [[2026-10-04_as-much-secuura-work-as-possible-spark-and-claude]]'s "Claude in parallel" half while the gauge is at or over 70%.
4. **Expiry:** the gauge's own renewal (~5 days at the ruling). Below 70% after the renewal, re-read the rule; do not assume either way. Recorded in EXPIRING-GRANTS.

**Family:** [[2026-09-25_three-tier-routing-ornith-spark-cloud-always-on]] · [[2026-10-05_spark-target-50-tasks-a-day]] · [[2026-09-14_at-90pct-weekly-usage-no-new-agents-wednesday-plus-local-model]] · [[2026-08-03_go-slow-earn-autonomy]] (rule 5: every grant recorded).
