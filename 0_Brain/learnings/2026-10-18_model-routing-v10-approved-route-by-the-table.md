---
date: 2026-10-18
type: grant
source: Kam, live board 2026-10-18 20:55:59 (card wed-model-routing-v10-approve-1018 = a)
status: live
tier: W
---

# Routing v1.0 is IN FORCE: every launch routes by `fleet/specs/model-routing.md`, and every Opus use names its table row

**The operative case, so the headline matches it:** Wednesday (or Tuesday or Friday) is about to launch a seat, a gate or a drafter, or route a task. **Open `2_Project_Files/fleet/specs/model-routing.md` v1.0, run its four checks (P1-P4), take the row, and write the receipt line `model: <id from models_latest.json> -- <row id> -- <P1-P4> -- <gauge %>`.** The "Opus 5.5 for every agent" override is lifted.

**His words, verbatim (card tap):** *"Decision wed-model-routing-v10-approve-1018: a — Approve all seven recommendations"* (option detail: "v1.0 replaces v0.1 and the boot line 'Opus 5.5 for every agent' is lifted; tier-2 gates go to Sonnet; Fable 5.1 gets one gate and one coordinator trial.").

**What the seven mean, applied:**
1. v1.0 replaces v0.1; the boot line in `Launch_Wednesday.command` now says route by the table (changed by copy + mv, backup `.pre-1018-routingv10`).
2. Tier-2 gates (tests, docs, config, tooling, already-gated follow-ups) run on **Sonnet** (`claude-sonnet-5-5`); tier 1 stays Opus.
3. Security-design and data-destroying builds stay on Opus.
4. The Spark may take fully spelled-out edits inside auth/security files; each such PR gets a tier-1 Opus gate.
5. A round counts when the model's output was judged (brief defects included); harness refusals, lost verdicts and outputs shown correct do not.
6. Ornith 1.5 is the second local lane, behind the Spark.
7. **Fable 5.1 (`claude-fable-5-1`, a level above Opus): one trial tier-1 gate and one trial coordinator task**, measured against Opus, before any rule. OWED: the next tier-1 gate after #1568 runs on Fable (Agent tool `model:` cannot name Fable, so it is a cockpit seat with `/model claude-fable-5-1`, or ask Kam if the Agent tool lacks it).

**Unchanged:** the counter, the 80-90% band and the 90% stop, the signature classes, the QA gate before every merge, one client per local task.

**Family:** [[2026-10-08_sonnet-trials-and-a-shared-model-routing-definition]] · [[2026-10-09_spark-first-model-choice-is-wednesdays-after-sonnet-analysis]] · [[2026-10-18_new-account-tickets-backlog-routing-definition-spark-max]] · [[2026-08-03_go-slow-earn-autonomy]] (rule 5: every grant recorded).
