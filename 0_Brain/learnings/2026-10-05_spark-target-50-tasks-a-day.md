---
date: 2026-10-05
type: preference
source: Kam, Wednesday's terminal, 2026-10-05 ~11:0x AEDT
status: live
tier: W
---

# The Spark's target is 50 tasks a day — push it harder; the bottleneck is ours, so build the pipeline, not the effort

**His words, verbatim:** *"push the spark harder, aim for 50 a day"* — after Wednesday measured the
week (2026-09-29 → 10-05): 24 tasks, 24/24 first-round PASS, ~13 min of Spark time in total
(median 39 s/task), against ~20 cloud-only merges.

**The operative case, so the headline matches it:** Wednesday is choosing what to do at a checkpoint,
or planning a Secuura day. **Ask: is the Spark on track for 50 tasks today, and if not, which stage
of the pipeline is starving it?** Briefs → runs → checker → Wednesday's read → hold → raise → gate →
merge. The Spark itself is never the limit at this scale.

**How to apply:**
1. **The runner is durable and in-tree** (`2_Project_Files/local-model/spark/`), never a session
   scratchpad script: the round tooling died with its scratchpad twice (IMPROVEMENTS 2026-09-30,
   2026-10-05), which is rebuild cost at every rotation.
2. **A standing brief queue:** every checkpoint counts briefs waiting; under ~15 waiting, commission
   brief-writing drafters (parallel, partitioned by ticket) the same action. Brief-writing is the
   real cost ([[2026-09-18_ornith-is-cheap-the-brief-is-the-cost]]).
3. **Climb the ladder to widen the pool** ([[2026-09-25_spark-calibrate-like-ornith-start-high-oversight]]):
   multi-file, looser briefs, carves of big tickets. 50/day is not reachable on rung 1-2 alone.
4. **Raises are batched:** a raise seat takes many held passes per round, file-disjoint, gated in
   batches ([[2026-09-18_minimise-gate-duplication-batch-them]]).
5. **Report the count daily** in the morning receipt: tasks run, PASS rate, merged, and the stage
   that limited the day. The target is a measurement, not a feeling.
6. Unchanged: the counter (original + one rebrief, then Opus 5.5), the QA gate before every merge,
   client scope (one client's content per task), the signature classes.

**Family:** [[2026-09-25_three-tier-routing-ornith-spark-cloud-always-on]] ·
[[2026-10-04_as-much-secuura-work-as-possible-spark-and-claude]] ·
[[2026-09-14_the-coordinator-adds-value-or-it-is-waste-three-duties-not-watching]] (duty 3).
