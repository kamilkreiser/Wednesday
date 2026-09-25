---
date: 2026-09-25
type: preference
source: Kam, terminal, 2026-09-25 ~12:0x
status: live
tier: W
---

# The Spark is calibrated the way Ornith was: start with HIGH oversight, measure what the model can and cannot do, adjust task complexity and how much the brief guides it, and reduce oversight only once the capability is known

**His words, verbatim:** *"Working with the spark, keep a similar approach to what we did with a smaller LLM in testing its capability and adjusting the complexity, or how much you need to guide it. Once you have a good idea of what the metal can and cannot do, we can reduce the level of oversight. So, let's start with height."*
("the metal" = the model; "start with height" read as **start with HIGH oversight**. That reading was said back to him on the panel; his word corrects it.)

**The operative case, so the headline matches it:** Wednesday is about to send the Spark (DeepSeek V4 Flash) a task, or is deciding how much brief to write for it. **Use the Ornith method as the starting point, at FULL oversight:** exact edits by line with the current text, the checker with every clause, Wednesday's own source read of every PASS, one task at a time. Then record per task what the model got right and wrong, and **only loosen (less guidance, bigger tasks, lighter reads) on measured evidence.**

**How to apply:**
1. **Start high.** Every Spark task gets a full brief (the kit's `03_BRIEF_TEMPLATE.md` / the Ornith brief shape), a checker that can fail (smoke-test the harness first: a trivial change + two deliberate breaks), and Wednesday's line-by-line read of every PASS. A PASS is a candidate, never a merge.
2. **Measure capability as a ladder**, the way the Ornith week did: one-file + spelled-out fix → multi-hunk → multi-file → looser briefs (fix shape only, no exact lines) → a ticket described in prose. Record each rung's result (pass, fail and why: model / harness / brief) in an IMPROVEMENTS-style file for the Spark, scored at the weekly consolidation.
3. **Reduce oversight only on evidence, and one notch at a time:** a rung with a run of clean PASSes earns the next rung, or a lighter read on that rung. Say which notch was loosened and why in the receipt. Kam decides the big step ("reduce the level of oversight"); Wednesday proposes it with the numbers.
4. **The counter stands:** original brief + ONE rebrief, then Opus 5.5 in the cloud (the Spark kit, 2026-09-23).
5. **Blocked today:** the model does not start (the tilelang import failure, 2026-09-25; Friday is diagnosing). The calibration starts on the first healthy boot, with Friday's smoke tests first.

**Family:** [[2026-09-25_three-tier-routing-ornith-spark-cloud-always-on]] · [[2026-09-23_spark-kit-running-a-local-coding-model]] · [[2026-09-15_ornith-every-issue-gets-a-tooling-or-instruction-fix]] · [[2026-09-18_ornith-is-cheap-the-brief-is-the-cost]] · [[2026-08-03_go-slow-earn-autonomy]] (rule 4: pilot, measure, review; autonomy is earned).

## EXTENSION 2026-09-25 15:28 — Kam, live board (view=wednesday), verbatim: *"great.  Use the spark as much as possible and push it to its limits as part of the test.  from my laptop tests, it usually corrects things on the second pass with some assistance but after the second time, its a diminishing return game so switch to Opus5.5 after the second attempt"* · 15:28:32 *"and by test I mean give it real work but measure progress"*
- **The test IS real work.** No synthetic benchmark rounds: Secuura tickets from the real backlog, each one measured (rung · pass/fail · the cause of any fail (model / harness / brief) · rounds · wall-clock · tokens).
- **Push it to its limits:** climb the ladder as fast as the evidence allows, and keep going past the first failure to find where it actually breaks. A rung that fails twice is where its limit is, and that is recorded, not avoided.
- **The counter, confirmed by his own laptop tests:** original + ONE assisted second pass ("with some assistance" = a rebrief naming the specific miss); after that, Opus 5.5. Same as the 2026-09-23 kit counter.
- **As much as possible:** the Spark is the default for medium work while it is healthy; Ornith keeps the simplest; cloud only on the counter or on a clause the Spark cannot meet.
