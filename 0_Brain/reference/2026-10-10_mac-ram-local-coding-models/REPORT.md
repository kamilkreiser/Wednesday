---
date: 2026-10-10
type: reference
source: research sub-agent commissioned by Wednesday 20:3x for Kam's live-board question (20:30:48, 20:32:41, 20:34:27). Saved by Wednesday from the agent's returned text (the agent's own file write was refused by the harness). Web figures (prices, specs, third-party tok/s) are the AGENT's reads on 2026-10-10, NOT re-verified by Wednesday; figures tagged [ours] cite our own files.
status: live
---

# Which Mac: Studio 256 GB, Studio 128 GB or MacBook Pro 128 GB (2026-10-10)

**Tags.** [ours: file] = measured on our machines. [web: URL, read 2026-10-10] = read today by the researcher. [10-09 study] = `0_Brain/reference/2026-10-09_studio-128-vs-256/REPORT.md`. [arith] = arithmetic, inputs shown. **UNMEASURED** = no source.

## BLUF
1. **Don't buy yet. Run a cheap test first (under US$1 hosted, plus a week of free gauge logging).** If it passes, buy the **Mac Studio M5 Ultra 256 GB, 30-core CPU / 64-core GPU, 1 TB, A$15,499**, as a dedicated model box beside this Studio, not a second fleet machine.
2. **Why not now:** the local tier is held back by the supply of well-briefed tickets and by the Claude work around every local task (brief, review, raise, gate, merge), not by RAM or speed. The Spark's median model time is 45 s per task [ours: `local-model/spark/done.md`, 58 rows]; 33 of 52 recent local passes are already on develop; today's screen found 1 ticket that fit. A bigger box only stretches the allowance if its model can take work **Sonnet or Opus does today with no quality drop**, and nothing measured shows that yet.
3. **Why 256 GB if we buy:** only 256 GB holds MiMo-V2.6-Flash beside Ornith. MiMo is the strongest model tested on our tickets: **46/48 vs the Spark's 43/48** [ours: `2026-10-09_studio-128-vs-256/HOSTED_REPLAY_RESULTS.md`]. 128 GB only adds a second Spark-class lane that is slower than the Spark on our prompt sizes (§3), and that lane is not the bottleneck.
4. **The MacBook Pro 128 GB is a laptop decision, not an allowance decision**: same M5 Max as the 128 GB Studio for A$2,100–2,800 more; it only helps the fleet while it sits on the desk.

## At a glance
| | Studio 128 GB | Studio 256 GB | MacBook Pro 128 GB |
|---|---|---|---|
| Chip at this RAM | M5 Max 18c CPU / 40c GPU only | **M5 Ultra** 30c/64c or 36c/80c | M5 Max 18c / 40c GPU only |
| Memory bandwidth | 614 GB/s | 1.2 TB/s | 614 GB/s |
| AUD (Apple AU configurator, read 2026-10-10 ~20:30) | **A$8,199** (512 GB SSD); A$8,649 with 1 TB | **A$15,499** (30c/64c, 1 TB); A$17,449 (36c/80c) | **A$10,299** (14", 2 TB); **A$10,999** (16", 2 TB) |
| Best tested model that fits | V4 Flash (the Spark's model) 2.4-bit, or Flash Next 4-bit; never beside Ornith | **MiMo 4-bit** or V4 Flash 4-bit, **plus** Ornith 1.5 8-bit | as Studio 128 |
| Our-ticket evidence | V4 Flash 43/48 (hosted fp8 and the Spark's 3.0 bpw); 2.4-bit UNMEASURED | MiMo **46/48** (hosted fp8); 4-bit UNMEASURED | as Studio 128 |
| Our 25K-in / 1.5K-out turn [arith] | ~83 s (Spark ~64 s) | ~42 s (V4 Flash) / ~33 s (MiMo) | ~83 s, if it does not throttle |
| Beside the fleet? | Tight (§2) | Yes | Not its job |
| Travels | No | No | **Yes** |
| Adds allowance savings | Little | **Only if** the trial passes | Only on the desk |

Price arithmetic (configurator): Studio M5 Max 40c A$5,199 + A$3,000 (128 GB) = A$8,199 · M5 Ultra 30c/64c A$9,499 + A$6,000 (256 GB) = A$15,499 · M5 Ultra 36c/80c A$9,499 + A$1,950 + A$6,000 = A$17,449. Specs (apple.com/au/mac-studio/specs/, /macbook-pro/specs/): 128 GB only with the M5 Max 40c; M5 Ultra comes with 96, 256 or 512 GB (512 GB "coming late October", price unpublished); no 128 GB Ultra; no MacBook Pro above 128 GB.
**Corrections to the 10-09 study:** 256 GB is offered on the 30c/64c Ultra too (the study said 36c/80c only); the A$6,000 upgrade and the A$8,199 128 GB price are now read on Apple's page.

## 1. Kam's lens: stretch the week's allowance without losing quality
- Gauge: 83% used with 5 d 12 h left [ours: `dashboard/data/usage_wednesday.json`, 2026-10-10T09:36Z]; 89% at 05:53 on 10-08 [`daily/2026-10-08.md`].
- **A local task replaces only the build step.** Claude still does the brief ("removes the cost of WRITING the fix, not SPECIFYING it", `learnings/2026-09-18_ornith-is-cheap-the-brief-is-the-cost.md`), the review of every Spark PASS, the Sonnet raise, the Opus gate and the Sonnet merge. **The allowance cost of each stage is UNMEASURED** (`fleet/specs/model-routing.md` §6).
- What the local tier already does: Spark since 10-05: 51 PASS / 6 FAIL / 1 REFUSED; 33 of 52 recent passes merged [`2026-10-10_spark-hold-census/CENSUS.md`]; week 09-29→10-05: 24 tasks in ~13 min of model time.

**A new Mac saves allowance only if it (a) moves Sonnet build work local (needs a model above the Spark), (b) cuts brief cost (a model that copes with looser briefs), or (c) moves drafting/review local (no evidence; touches the quality chain).** Quality is a hard constraint:

| Task kind | 128 (Studio or MBP) | 256 | Evidence |
|---|---|---|---|
| Rung 1–2, spelled-out brief, not security | already local; no gain | already local; no gain | Spark 51/58; Ornith 1.5 17/20 [ORNITH15_AB.md] |
| A second lane for the same work | capacity nobody uses | same | the queue is the limit |
| Multi-file, rung 3 | same model as the Spark | **trial first** | no model above the Spark tested on rung 3 [`2026-10-07_spark-rung3/REPORT.md`] |
| Loose briefs (rung 6) | no change | **trial first** | UNMEASURED |
| Tickets Sonnet builds today | trial first | **trial first** (the only plausible candidate) | the replay used Spark-briefed tasks only ("may flatter the Spark") |
| Briefs, review, raise, merge (Sonnet) | stay cloud | stay cloud until a separate trial | none |
| Gates, security, rulings (Opus) | stay cloud | stay cloud | rule (model-routing.md) |

**Mix across the four tiers:** Studio 128 = Opus/Sonnet unchanged, a third Spark-class lane, never beside Ornith (measured peaks 103.8 / 109.5 GB on a 128 GB M5 Max [10-09 study]) → net ≈ zero (inference). Studio 256 = a possible tier ABOVE the Spark (MiMo or GLM 4-bit) beside Ornith; moves part of Sonnet's build share local ONLY if the trial passes at the Opus gate's current rate → net UNMEASURED, plausibly modest. MacBook Pro 128 = as Studio 128 for the fleet.
**Honest finding (inference):** the biggest lever on the weekly gauge today is ROUTING (Sonnet seats, batched gates, fewer duplicate reads), which §6 is measuring. Hardware becomes first-order only if a local model can take a Claude stage without losing quality, and only the 256 GB box can hold a candidate.

## 2. Headroom (measured on our 96 GB Studio)
| Event | Model | Result |
|---|---|---|
| 10-08 17:04, seats live [`daily/2026-10-08.md`] | Flash Next, 72.65 GB | HTTP 507: does not fit under the 57.72 GB ceiling (57.58 GB reclaimable) |
| 10-08 17:12, apps quit, two seats | same | 507 at 72.57 GB; on the aggressive tier swap jumped and the guard killed the server |
| 10-08 18:56, three seats + a jest checker [QWEN122_AB.md] | Qwen 122B, 65.6 GB | swap 906 → 4,499 MB in ~7 s; killed before its first prompt |
| 10-08 17:36–18:03, two seats [ORNITH15_AB.md] | Ornith 1.5 8-bit, 34.9 GB | 42 checker runs, swap never grew |
| default | — | GPU cap 77.76 GiB of 96 (0.81 × RAM) |

[arith] With the fleet and its checkers, a model safely gets ~60–65 GB of 96 (fleet + macOS ~30–35 GB, checkers spike). **128 GB shared with the fleet ≈ 90 GB for a model, below V4 Flash 2.4-bit's measured 103.8 GB peak: it would not run safely beside the fleet** (fits on a dedicated box). **256 GB shared ≈ 185 GB**: MiMo 4-bit (167 GB file) or V4 Flash 4-bit (161.8 GB measured) fits; adding Ornith (36.8 GB) gets tight. Mac memory is fixed at order. **Recommended shape: a second, dedicated box**; the fleet and Ornith stay on this 96 GB Studio.

## 3. Speed
Anchors [ours]: Ornith 1.5 8-bit on this M3 Ultra 82.4 tok/s decode, 2,299 prefill, 13.4 s median/task [ORNITH15_AB.md]; the Spark 37.13 decode, 1,032 prefill, 53.7 s for 23.6K in / 1K out [Spark HANDOFF.md §4].

| Model | M5 Max 128 | M5 Ultra 256 | Source |
|---|---|---|---|
| V4 Flash | 2.4-bit: 44.2 / 509 @32K | 4-bit, 64c: 67.2 / 1,223 @32K | [10-09 study] |
| MiMo 4-bit | doesn't fit | 68.6 / 2,329 (80c); 73.6 / 2,475 (64c) | [10-09 study] |
| Flash Next 4-bit | 78.2 / 2,525 @32K; 49.9 / 2,085 @64K | 87.8 decode @16K; 60.6 @128K; 2,887 prefill @16K | [10-09 study]; [web: omlx.ai/benchmarks row ud23dple]; [web: macstories.net M5 Ultra review] |
| GLM-5.3-Flash | 2-bit only: 9–25 decode | 4-bit: 41 / 1,107 @16K | [web: MacStories]; [10-09 study] |
| Ornith 1.5 8-bit | 91.0 / 4,142 | UNMEASURED | [10-09 study] |

Our turn, 25K in / 1.5K out [arith: 25,000 ÷ prefill + 1,500 ÷ decode]: Spark ~64 s · M5 Max 128 V4 Flash 2.4-bit **~83 s** · M5 Ultra 256 V4 Flash 4-bit ~42 s · M5 Ultra 256 MiMo 4-bit ~33 s. **Strength: medium to weak** (third-party idle-machine rows; MacStories saw M5 Ultra decode swing 52–108 tok/s).

## 4. Quality for our work
1. Hosted replay, 48 Spark tasks, same inputs and checker [HOSTED_REPLAY_RESULTS.md, "indicative, not decisive"]: **MiMo 46/48** (lost none of the Spark's passes) · GLM-5.3-Flash 45/48 · V4 Flash fp8 43/48 · Spark (V4 Flash 3.0 bpw, pruned) 43/48.
2. Compression: fp8 and 3.0 bpw both 43/48 (no measurable cost); 2.4-bit (the 128 GB build) UNMEASURED.
3. Ornith 1.5 vs 1.0: 17/20 each, despite the maker's +9 SWE-Pro points [ORNITH15_AB.md]; the benchmark overstated the gain.
4. Spark algorithm tasks: V4 Flash 84.3% first try, 98.1% after one repair; Ornith 81.8%, no gain from repair; Opus 4.8 and Opus 5 100%; hard suite V4 Flash 90.1% vs Opus 5 100% (fails concurrency logic; does not fix misconceptions from feedback) [Spark HANDOFF §5c–5d].
5. Ornith 1.0 over time: 85.9% since 09-17 (255 PASS / 42 FAIL) [MODEL_RANKING.md].
**Classes:** 35B (Ornith) good at single-file patches from tight briefs, weak with feedback, loose briefs, unbriefed tests. Flash (the Spark) good at multi-file from tight briefs and mechanical fixes; can't fix semantic or concurrency misconceptions. 256-only models (INFERENCE): maker DeepSWE MiMo 67.9, GLM 63.4 vs 54.4 for the Spark's model; an independent board GLM 63 ±4 vs V4 Flash 53 ±4. The gap might carry harder rungs; on our easy set the edge is only +3 of 48.

## 5. Decision
**Test, then, if it passes, buy the Studio M5 Ultra 256 GB 30c/64c at A$15,499.** Why 30c/64c: the 80c costs A$1,950 more; decode depends on bandwidth (both 1.2 TB/s); the 64c rows are not slower on decode; prefill difference UNMEASURED.
- **Studio 128 (A$8,199):** cheapest; a backup if the Spark fails. Against: slower than the Spark on our prompts, can't hold a big model and Ornith together, no new quality tier.
- **MacBook Pro 128 (A$10,299 14" / A$10,999 16"):** portability; runs Ornith 1.5 8-bit easily and Flash Next or V4 Flash 2.4-bit alone. Against: same chip as the Studio 128 for A$2,100–2,800 more; throttling risk (Notebookcheck title "M5 Max with inconsistent performance and throttling issues – MacBook Pro 14", title only, page 403; a Hacker Noon opinion that the 16" sustains more, snippet only); sustained LLM speed UNMEASURED; a laptop is a poor 24/7 lane. **If the MacBook, choose the 16".**
- **The Spark:** keep it alongside (Kam ruled "Keep the spark as is", 10-08); a 256 GB box sits above it.
- **Cost per useful capability [arith]:** hosted MiMo US$0.160 for 48 tasks (~US$0.0033/task, ~US$183 for 50 tasks/day over three years) vs local A$15,499. **The hardware buys independence and keeps client code in-house; it does not make each task cheaper.** Sending client code to a zero-retention host is Kam's call. The OpenRouter key was revoked 2026-10-10 20:36.

**Cheapest experiment before buying:**
1. **Hosted replay of HARDER tasks (under US$1, ~1 hour):** MiMo, GLM and V4 Flash on the Spark's FAIL and counter-exhausted rows, the five hard tasks in QWEN122_AB.md, 5–10 tickets Sonnet built this week (e.g. KS-1434), and a few loose-brief tasks (KS-1456-loose); same checker plus the Opus gate on every PASS. **Pass bar: match Sonnet's gate outcome** (today 0.96–0.98, one Major in ten). Needs a NEW hosted key and Kam's word on client code going to the host.
2. **Log the gauge before and after every seat, by stage, for a week (free).** The only way to put a number on the allowance any Mac would save.
3. **On this 96 GB Studio (free):** Ornith 1.5 on a loose brief; `gpt-oss-120b` (on disk) on the 20-task set when the fleet is quiet.
4. **Decision rule:** buy the 256 if MiMo or GLM pass most Sonnet-built tickets at the gate AND Sonnet build work is a big share of the gauge; buy nothing if they only match the Spark on harder tickets (work on brief supply and routing instead); buy the MacBook Pro 16" 128 only if portable local coding is wanted for its own sake.
5. **Timing:** the 512 GB M5 Ultra is "coming late October", price unpublished; waiting costs nothing while the test runs.

## 6. NOT MEASURED
- **Speed and fit:** every M5 Max / M5 Ultra tok/s figure (none on our harness or under fleet load); 64c vs 80c prefill; default GPU budget on 128/256 GB (0.81 × RAM extrapolated from our 96 GB); MiMo 4-bit running footprint (167 GB is a file size); big model plus Ornith together on 256 GB; the ~90 GB / ~185 GB shared budgets.
- **Quality:** 2.4-bit and 4-bit on our tickets; any model above the Spark on rung 3+, loose briefs or Sonnet-built tickets; all makers' benchmark scores (the independent board covers GLM and V4 Flash only).
- **Allowance:** the cost of each stage, and so the allowance any config would save.
- **Hardware and price:** MacBook Pro thermals and noise; Mac Studio noise (one reviewer); resale value of this Studio; Apple AU return window; the 512 GB price and date; prices exclude AppleCare and discounts.

## Sources (read 2026-10-10 by the researcher)
Apple: apple.com/au/mac-studio/specs/ · apple.com/au/macbook-pro/specs/ · apple.com/au/shop/buy-mac/mac-studio · apple.com/au/shop/buy-mac/macbook-pro.
Reviews/benchmarks: macstories.net/stories/m5-ultra-mac-studio-review-the-dream-mac-for-local-ai-agents/ · contextstudios.ai/blog/mac-studio-m5-ultra-local-ai-guide · hardware-corner.net/m5-max-local-llm-benchmarks-20261233/ · omlx.ai/benchmarks (row ud23dple) · everymac.com (AU base prices agree) · notebookcheck.net (title only) · hackernoon.com/dont-buy-the-wrong-macbook-pro-the-m5-trap-apple-wont-mention (snippet only).
Ours: `2026-10-09_studio-128-vs-256/{REPORT,HOSTED_REPLAY_RESULTS,HOSTED_API}.md` · `2026-10-08_omlx-flash-next/{REPORT,MODEL_RANKING,ORNITH15_AB,QWEN122_AB}.md` · `2026-10-08_ornith15-deploy/REPORT.md` · `2026-09-22_spark-deepseek-v4-flash/HANDOFF.md` · `2026-10-07_spark-rung3/REPORT.md` · `2026-10-10_spark-screen/SCREEN_0600.md` · `2026-10-10_spark-hold-census/CENSUS.md` · `1_Project_Definition/Architecture/2026-09-14_local-model-headroom.md` · `2_Project_Files/local-model/{README.md,spark/done.md,night/done.md}` · `fleet/specs/model-routing.md` · `daily/2026-10-08.md` · `dashboard/data/usage_wednesday.json` · learnings 2026-09-18, 2026-10-05, 2026-10-06.
