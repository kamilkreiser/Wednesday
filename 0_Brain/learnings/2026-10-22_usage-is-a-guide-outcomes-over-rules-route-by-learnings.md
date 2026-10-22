---
date: 2026-10-22
type: grant
source: Kam, live board 2026-10-22 15:34:23 AEDT, view=wednesday (verbatim below)
status: live
tier: W
supersedes: the 90% HARD STOP of 2026-09-14_at-90pct-weekly-usage-no-new-agents-wednesday-plus-local-model and the band wording of 2026-10-14_80-to-90pct-limited-cloud-wednesday-and-spark (both become GUIDES, not stops)
---

# Weekly usage is a GUIDE, never a stop: route every task by what we have learned (Opus, Sonnet, Spark, Ornith), lean on Sonnet and the Spark past 70%, and when unsure ASK on fleet activity and keep going — nothing happening is the worst outcome

**The operative case, so the headline matches it:** Wednesday is about to hold back a launch, a deploy or a piece of work because the weekly gauge is high, or because a rule seems to say stop, or because she is unsure. **Don't stop.** Route the task by the model-routing learnings, launch it (past 70% lean harder on Sonnet and the Spark), and if genuinely unsure post a question card on fleet activity with a default and carry on with the next thing.

**His words, verbatim (15:34:23):**
> *"New instructions going forward - always use your learnings of Opus, Sonnet, spark and onrith task allocation.  Regardless of % of context.  2)use weekly usage % as a guide but don't let it stop productivity.  this should make sure that once we are over 70% we allocate more heavily to sonnet and spark but deployment, progress and outcomes are more important than rules.  3)If unsure, do not just stop, post a fleet activity question but the worst outcome is when nothing happens because of a rule I made kills productivity.  Lets check in together and work through things to constantly improve 4)you manage the tasks and workload on a daily stage, you are more knowledgeable than I on what works best so if you ever disagree with me just say so"*

**And 15:35:07, verbatim:** *"also, please instruct Tuesday about the task allocation findings.  Tuesday does not have a spark or the ram to run Onrith but it can use Sonnet"*

**Wednesday's reading (receipted on the panel 15:3x, bf-46fd385fecdff88b, with agreement stated):**
1. **Routing:** every launch routes by `2_Project_Files/fleet/specs/model-routing.md` (the learnings), whatever the context reading.
2. **Usage:** the weekly % is a GUIDE. Under 70%: route by the table. Over 70%: tilt to Sonnet and the Spark; Opus stays where the table needs it (security design, tier-1 gates, deploys with box rights). **No launch is refused for usage alone** when deployment, progress or an outcome needs it. Report the gauge in the launch receipt; do not wait on it.
3. **Unsure = a fleet-activity question card with a default, and keep working.** Never a silent stop.
4. **Wednesday owns the daily task and workload plan,** and says so plainly when she disagrees with him ([[2026-08-21_challenge-me-when-you-think-im-wrong]]).

**What does NOT change:** the v1.3 signature classes (production, money, external comms to humans, irreversible) still pause for his word; the QA gate before every merge; client isolation; the Spark and Ornith counters.

**Mechanism (a grant is not a mechanism):** `fleet/usage_gate.sh` still REFUSES at 90% (rc 3). Until it is changed to advisory (shared tooling, claim first), launches pass `WED_USAGE_STOP=100` naming THIS file. The 2026-10-20 Tuesday no-90% grant already covers her seat.

**Family:** [[2026-09-14_at-90pct-weekly-usage-no-new-agents-wednesday-plus-local-model]] (its hard stop retired) · [[2026-10-14_80-to-90pct-limited-cloud-wednesday-and-spark]] · [[2026-10-18_model-routing-v10-approved-route-by-the-table]] · [[2026-09-16_if-something-blocks-move-on-to-the-next]] · [[2026-08-16_an-ask-without-a-default-is-an-indefinite-hold]] · [[2026-09-14_the-coordinator-adds-value-or-it-is-waste-three-duties-not-watching]] · [[2026-08-03_go-slow-earn-autonomy]] (rule 5: every grant recorded).
