---
date: 2026-09-25
type: grant
source: Kam, terminal, 2026-09-25 ~11:4x
status: live
tier: W
---

# Standing routine: Ornith for the simplest tasks, the Spark for medium and normal ones, cloud agents only when necessary. Wednesday orchestrates and tests everything, the routine always runs, and from 70% of the weekly allowance cloud agents are minimised

**His words, verbatim:** *"Were you able to use and continue connect to the spark.  if So, please create a new workflow where you use Ornith for the simplest task, Spark for medium and normal tasks, and escalate to cloud agents when necessary and relevant. Still orchestrate everything and test everything. This routine should always run, and once you get to 70% of the weekly usage, minimize cloud agents."*

**The operative case, so the headline matches it:** Wednesday is about to route a ticket or a task to a worker. **Ask which tier it fits: Ornith (the simplest, one file, a spelled-out fix, a checker that can fail), the Spark (medium and normal work), or a cloud agent (only when the first two cannot).** Then read the 7-day gauge: at 70% or above, cloud agents are MINIMISED. That cut sits below the 90% hard stop, which still stands.

**How to apply:**
1. **Route by tier, per task, and say which tier and why** in the brief or receipt ("Ornith: one file, fix spelled out" / "Spark: medium, N files" / "cloud: <which clause the first two fail>"). The counters stay: Ornith gets the original brief + ONE rebrief (2026-09-16); the Spark the same (2026-09-23 kit).
2. **Orchestrate and test everything:** every worker's output is read at source by Wednesday and gated as now (the QA gate, Wednesday's completion check, hold_ready for local passes). Local workers never merge; a Claude seat raises, and Wednesday GOs.
3. **Always running:** the routine is the default day and night, with no "idle" state. When a pool thins, widen the harness or write briefs (the 09-15 and 09-18 rules).
4. **70% gauge:** above it, a cloud agent is launched only when nothing local can do the work AND the work matters now (a deadline, a fuse, Kam waiting). Say which in the launch receipt. **90% stays the hard stop** (usage_gate.sh).
5. **CLIENT SCOPE — NOT assumed:** the Spark is Datasec hardware (login `datasec-rd`), and Kam's scope card (Friday's `spark-studio-client-scope`, ruled c: "decide after the Studio can connect") is open. **Until he says Secuura code may go to the Spark, Secuura work routes Ornith → cloud, and the Spark takes only client-neutral work.** Asked on the panel the same minute. (Hard rule 2: no cross-client leak by inference.)
6. **State at the grant:** Studio→Spark login WORKS (NVIDIA Sync alias `Spark`), but the model FAILS to start (tilelang import error, 2026-09-25 01:37Z and 01:40Z; reported to Friday). The Spark tier is unavailable until that is fixed.

**Mechanism OWED (a grant is not a mechanism):** a 70% advisory in `fleet/usage_gate.sh` (rc 0 but loud, naming this rule) beside the 90% refusal; a routing line in the brief template; a Spark leg in the doctor check once the model runs. Built at the next boundary with room, not in this seat past 70% context.

**Family:** [[2026-09-16_local-model-is-long-term-and-claude-takes-what-it-cannot-do]] · [[2026-09-23_use-the-local-model-as-much-as-possible]] · [[2026-09-23_spark-kit-running-a-local-coding-model]] · [[2026-09-14_at-90pct-weekly-usage-no-new-agents-wednesday-plus-local-model]] · [[2026-08-03_go-slow-earn-autonomy]] (rule 5: recorded) · [[2026-08-03_role-beyond-code-three-priorities]] (no cross-client leak).
