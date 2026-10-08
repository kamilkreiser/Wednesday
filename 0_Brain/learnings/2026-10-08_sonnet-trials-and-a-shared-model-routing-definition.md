---
date: 2026-10-08
type: grant
source: Kam, live board 2026-10-08 20:34:09 view=wednesday
status: live
tier: W
---

# Trial Sonnet seats against the Spark and Opus, find Sonnet's limits, and write ONE model-routing definition that Tuesday and Friday can use too

**The operative case, so the headline matches it:** Wednesday is about to launch a Claude seat, or to choose which worker takes a task. **The worker is no longer "Opus 5.5 by default."** There are now four tiers to route between (Ornith 1.5 · the Spark · Sonnet · Opus). Until the definition below exists and has evidence behind it, Sonnet seats are TRIALS: measured, never assumed equivalent to Opus.

**His words, verbatim (20:34:09):**
> *"Ok, thank you for the analysis.  In that case I agree.  lets run the normal set up along with the spark and Ornith 1.5.   In addition to this, I have been thinking about the following - We currently launch every agent with Opus 5.5.  Can you experiment in launching some agents using the latest version of Sonet.   1)to compare how it performs against the Spark 2)determine where its limits lie.  that way we can use the local models for some tasks, sonnet for others and Opus for the rest.  Sonnet looks like it 8x of time wo the weekly limits would stretch much further.  As you do this work, I would like you to create a definition that can be used by you and shared with the Tuesday and Friday agents so they too can decide when to use Sonnet based on the complexity of the task ahead"*

**Wednesday's reading, receipted on the panel at 20:3x (his word corrects it):**
1. "In that case I agree" answers the Qwen 122B result: it does not fit beside the fleet, so the normal setup continues with **the Spark and Ornith 1.5**. Qwen 122B stays parked.
2. **Sonnet trials:** launch some agent seats on the latest Sonnet (Sonnet 5.5), on REAL work, and measure (a) against the Spark on the same kind of task, and (b) where Sonnet's limits are, by climbing task difficulty the way the Ornith and Spark ladders did.
3. **A routing definition** (local · Sonnet · Opus by task complexity), written so Wednesday, Tuesday and Friday all apply the same predicate. Shared as a file in the shared tooling, and sent to the other two seats by coordination mail. It carries NO client content.
4. "8x" is Kam's estimate of how much further Sonnet stretches the weekly allowance. **Unmeasured by Wednesday: measure the real usage per seat-hour in the trial and report it.**

**How to apply:**
1. **The mechanism, measured 2026-10-08:** the model is pinned in each PROJECT's launcher (`--model`), which Wednesday never edits. A trial switches ONE seat after launch with `/model claude-sonnet-5-5` in that seat's pane (the 2026-09-30 per-session precedent for QA gates), and the seat is told by mail which model it runs on. A durable per-launch knob is a project-launcher change: the project's own agent makes it on a brief, or Kam does.
2. **Trial design (Wednesday's, to be shown to Kam with the first results):** same brief shape and same gates as an Opus seat; record per seat: model, task rung, rounds, defects the QA gate found, Wednesday's corrections, wall-clock, ctx used, and the weekly gauge before and after. Compare with the Spark on tasks of the same rung, and with the Opus seats of the same week. **The QA gate still precedes every merge; a Sonnet seat never merges without it.**
3. **Start where a failure is cheap:** raise seats on held, already-gated passes (one PR each) and brief drafters, before any merge seat, deploy seat or security-surface work. Climb only on evidence, one notch at a time.
4. **The definition lives in ONE file** (`2_Project_Files/fleet/specs/model-routing.md`, to be written), versioned, with its evidence basis on each line ([[2026-09-08_a-new-rule-is-most-dangerous-just-after-adoption]]: a single unverified instance is a pilot, not a rule).
5. **Usage:** the trials start when the allowance allows: this account is at 98% on 2026-10-08 20:3x (renews ~09:00 AEDT Fri 9 Oct). The first Sonnet seat is the first raise seat after the renewal, unless Kam says otherwise.

**Family:** [[2026-09-25_three-tier-routing-ornith-spark-cloud-always-on]] (this adds a fourth tier) · [[2026-09-25_spark-calibrate-like-ornith-start-high-oversight]] (the ladder method) · [[2026-09-30_qa-gates-may-switch-to-opus48-when-flagged]] (per-session `/model`) · [[2026-09-14_do-not-guess-a-comparison-a-citation-you-did-not-open-is-a-guess]] (the 8x is his estimate; measure it) · [[2026-08-03_go-slow-earn-autonomy]] (rule 5: every grant recorded).
