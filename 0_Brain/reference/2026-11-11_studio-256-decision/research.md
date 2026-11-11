---
date: 2026-11-11
type: reference
source: research sub-agent for Wednesday. Apple AU configurator read live 2026-11-11 ~21:20 AEDT (rendered in a browser). Web sources read 2026-11-11. Local files read-only. Builds on 0_Brain/reference/2026-10-09_studio-128-vs-256/REPORT.md, which this note does not repeat. Figures taken from that report are tagged [10-09 report]; they were not re-read today.
status: live
---

# 256 GB Studio vs a smaller coordinator Studio (2026-11-11)

## BLUF

1. **Kam's 30% test fails today, and more RAM does not fix the reason.** Since 2026-10-28 the Spark produced **454 PASS rounds from 137 Claude operator sessions**, about 3.3 PASSes per Claude session. For the rungs it is given (1-3), a Claude operator first writes the exact fix (the "golden") and proves it through the checker. That shows as **251 CONTROL-PASS rows** in the same window, and the Spark's output is then compared **byte-identical** to it. Every PASS still needs a Claude raise, gate and merge, and **280 held PASS paths are waiting** for that. So the local tier removes **typing, not thinking**. Its saving on cloud work is small and UNMEASURED; the files give no evidence that it comes near 30%. Source: `spark/done.md`, operator reports. Section C.
2. **A bigger model barely moves the part we can measure.** On the same 48 Spark tasks, hosted MiMo-V2.6-Flash scored 46/48 and GLM-5.3-Flash 45/48, against 43/48 for the Spark's model ([10-09 report] HOSTED_REPLAY_RESULTS.md). That is about 3 tasks out of 48, on work that Claude had already solved. MiMo ("Momo") and GLM-5.3-Flash at 4-bit are the main things 256 GB adds over 128 GB.
3. **What would pass the 30% test** is a local model that turns a prose ticket into a passing change with **no golden written by Claude**: rung 4-6 work and agentic work. Our data on that is thin (Spark rung 4: 5 of 7 tickets passed on round 1; prose: 1 PASS, then 0/1 in the 10-26 A/B). For a 256-class model it is **UNMEASURED**, and it can be measured hosted for a few dollars before buying anything.
4. **Store facts change the hardware picture.** Today **256 GB ships in 12-14 weeks** (in-store pickup 2 Mar 2027), while **128 GB (M5 Max) ships in 5-7 business days at A$8,649**. **96 GB is offered only on the M5 Ultra (A$9,499, 4-5 weeks)**, so 96 GB costs more than 128 GB. A 256 + 128 split over Thunderbolt 5 opens no model worth having: everything stronger than MiMo/GLM-Flash is still too big.
5. **Recommendation:** do not order the 256 GB now. If a coordinator machine is needed, buy the **128 GB M5 Max**. Run the hosted rung-4-6 and agentic test first; order the 256 only if it clears the thresholds in section E. The 12-14 week wait means a later order costs about one quarter's delay, not access.

## What you may not have considered

- **The Spark does not save brief-writing; brief-writing is the job.** The lesson `learnings/2026-09-18_ornith-is-cheap-the-brief-is-the-cost.md` says it plainly: *"the local model removes the cost of WRITING the fix, not the cost of SPECIFYING it."* Under the operator model, the specifying includes the exact `+` lines. A local tier earns its keep only when it removes Claude reasoning, not Claude keystrokes.
- **The local box is idle about 97% of the time.** Spark model time in `spark/done.md` from 2026-10-05 to 11-10 was **8.2 h of 888 h (0.9%)**; checker-inclusive round time was **24.5 h (2.8%)**. Shadow-gate runs are not in that file (UNMEASURED). Ornith on the 96 GB Studio has **one queue round since 2026-09-26** (`night/done.md`). We are short of Claude-written briefs, not of local compute.
- **Local review does not offload gates.** Spark shadow reviews against Claude gates: gate 82 recall 0/4, gates 83-85 missed findings, gate 86 found nothing new and gave 2 false positives, gate 87 matched only because the diff was empty (`IMPROVEMENTS.md`, 2026-11-02 01:5x row). Gates are a large share of Claude work, and they stay on Claude.
- **The 256-class models sit about at Claude Sonnet 5 / Opus 4.8 level, not Opus 5.5 level.** Independent DeepSWE scores: GLM-5.3-Flash 63±4, Opus 4.8 59±2, Sonnet 5 54±4, Opus 5 74±4. MiMo-V2.6-Flash is not on that board. So the realistic local target is Sonnet-seat work (raises, merges, C2 builds), not coordinator or Opus-gate work, and our local harness can only produce single-shot diffs, not run an agent loop. That limit is in the harness, not in RAM.
- **A "resilience" box needs a coordinator, and today the coordinator is Claude.** Under routing rule P2 (gauge ≥90%), the fleet runs as "Wednesday plus the local models", and Wednesday is Claude. If cloud access disappeared, the local tier as built would produce almost nothing, because nothing would write its briefs. Resilience requires a local model that can write briefs, which is UNMEASURED for every candidate.
- **The 128 GB Studio can't be both a coordinator and half of a model cluster.** A split needs its memory free. And every model that justifies a split is too big for 256 + 128 anyway (table B).
- **Hosted open models are a cheap measuring tool, not a fallback.** OpenRouter with zero data retention cost US$0.45 for all 48 tasks on three models ([10-09 report]). They are also cloud services, so they give no resilience. They do let us test the hypothesis before spending A$17k.

## A. Hardware: Apple AU store, read live 2026-11-11 ~21:20 AEDT

Sources: apple.com/au/shop/buy-mac/mac-studio and its per-configuration pages (rendered); apple.com/au/mac-studio/specs/ (read 2026-11-11).

| Config | Chip | Bandwidth | Price (AUD, 1 TB) | Ships / pickup |
|---|---|---|---|---|
| 96 GB | M5 Ultra 30c CPU / 64c GPU (96 GB is Ultra-only) | 1.2 TB/s | **A$9,499** | 4-5 weeks; pickup Tue 22/12/2026 |
| 128 GB | M5 Max 18c / 40c | 614 GB/s | **A$8,649** | **5-7 business days**; pickup Tue 24/11/2026 |
| 256 GB | M5 Ultra 30c / 64c | 1.2 TB/s | **A$15,499** (the store offers it; the specs page lists 256 GB only for the 80c chip, an Apple inconsistency) | **12-14 weeks**; pickup Tue 02/03/2027 |
| 256 GB | M5 Ultra 36c / 80c | 1.2 TB/s | **A$17,449** (A$11,449 + A$6,000) | **12-14 weeks**; pickup 02/03/2027 |
| 512 GB | M5 Ultra 36c / 80c only | 1.2 TB/s | **A$34,699** (A$11,449 + A$23,250) | 10-11 weeks; pickup Fri 05/02/2027 |

- The "512 GB coming late October" footer from 10-09 is gone. 512 GB is now orderable.
- All models have Thunderbolt 5 (120 Gb/s). The Ultra has 6 TB5 ports; the Max has 4 TB5 ports plus 2 front USB-C ports at 10 Gb/s. Apple's specs page does not mention RDMA.
- The supply context matches Kam's fear. The DRAM shortage delayed the M5 Studio ([AppleInsider, 2026-04-19](https://appleinsider.com/articles/26/04/19/mac-studio-touchscreen-macbook-pro-delayed-by-memory-shortages)). Helium spot prices rose 40-100% after the Middle East conflict ([The Star, 2026-03-26](https://www.thestar.com.my/business/business-news/2026/03/26/middle-east-tensions-rattle-chip-supply-chains-raise-gas-risks); [Prospect, 2026-04-13](https://prospect.org/2026/04/13/how-iran-war-threatens-ai-economy-semiconductors-supply-chain-strait-hormuz)). How much of the 12-14 weeks is caused by the war rather than AI demand: UNMEASURED.

## B. Models: what fits

Usable memory per machine: 128 GB ≈ 103-120 GB; 256 GB ≈ 206-258 GB (default budget up to a raised `iogpu.wired_limit_mb`) [10-09 report]. 256 + 128 ≈ 309-377 GB, **only if the 128 is otherwise idle**. "~arith" sizes = total params × 4.5 bits / 8, not measured. Speeds are community oMLX rows from the [10-09 report]; none was measured on our harness.

| Model (total / active) | 4-bit size | 128 | 256 | 256+128 | Mac speed (decode tok/s) | Coding score (source) |
|---|---|---|---|---|---|---|
| DeepSeek V4 Flash 0731 (284B/13B), **the Spark's model** | 151.5 GB; 2.4-bit 92.8 | 2.4-bit only | **4-bit** | — | 44 (Max) / 67 (Ultra) | DeepSWE 53±4 indep. |
| Qwen3.8-Flash-Next (125B/6B) | ~106-111 | **yes, alone** | yes (6-8 bit) | — | 56-89 (Max) | DeepSWE 58.7, SWE-Pro 62.5 (maker) |
| gpt-oss-120b (117B/5.1B) | 63.4 | yes | yes | — | 62-67 | SWE-Pro 16.2 ([morphllm](https://www.morphllm.com/best-open-source-llm)) |
| **MiMo-V2.6-Flash** (309B/15B, MIT, 2026-09-21) | ~164-167 | no | **yes** | — | 68.6 (80c) | DeepSWE 67.9 (maker, **no independent check**); **our hosted replay 46/48** |
| **GLM-5.3-Flash** (320B/18B, MIT) | footprint 177 | 2-bit, marginal | **yes** | — | 57-128 (wide spread) | DeepSWE **63±4 indep.**; our replay 45/48 |
| DeepSeek V4.1-Flash (552B/16B + Engram) | Q4 needs 512 GB | no | 2-3 bit, Engram on SSD | — | 14-29, TTFT 81 s | DeepSWE 74.2 (maker harness; Q2 quality loss shown by ds4) |
| Qwen3.5-397B-A17B | 223.9 | no | raised limit only | yes | 32 (M3 Ultra) | SWE-V 76.2 (morphllm, vendor) |
| MiniMax M3 (428B/23B, **non-commercial default licence**) | 241.5 | no | raised limit only | yes | UNMEASURED | SWE-Pro 59.0 (morphllm) |
| Beam / Reflection (501B/23B, Apache, 2026-10-16) | ~282 (arith) | no | no | **yes** | UNMEASURED | SWE-V 81.6, SWE-Pro 66.1, **DeepSWE 43.3** (vendor) |
| Nemotron 3 Ultra (550B/55B) | ~310 (arith) | no | no | tight | UNMEASURED | SWE-V 70.7, TB2.1 56.4 |
| GLM-5.3 (753B) | 418 | no | no | **no** | — | DeepSWE 69±3 indep. |
| MiMo-V2.6-Pro (1.02T/42B) | ~574 (arith) | no | no | **no** | — | AA Index 46 (secondary source) |
| Muse Spark Open (816B/42B) | ~459 (arith) | no | no | **no** | — | not stated |
| DeepSeek V4 Pro (1.6T/49B) | 837 | no | no | **no** | — | DeepSWE 63±6 indep. |
| **Kimi K3 / K3.1 Pro** (2.8T/104B; K3.1 weights ~Nov 2-5) | ~1.56 TB | no | no | **no** | — | K3: DeepSWE 69±5 indep.; K3.1 Pro TB4.0 65.7 vs Opus 5.5 66.4 (vendor) |
| Kimi K2.7 Code (1T/32B) | ~560 (arith) | no | no | **no** | — | in-house bench only |

**Two-machine split:** RDMA over Thunderbolt 5 (macOS 26.2+) with exo is real. On M3 Ultra nodes, DeepSeek V3.1 671B went from 21.1 tok/s on one node to 27.8 on two ([AppleInsider, 2025-12-20](https://appleinsider.com/articles/25/12/20/ai-calculations-on-mac-cluster-gets-a-big-boost-from-new-rdma-support-on-thunderbolt-5); [Jeff Geerling](https://jeffgeerling.com/blog/2025/15-tb-vram-on-mac-studio-rdma-over-thunderbolt-5)). A mixed M5 Ultra + M5 Max pair has not been measured (UNMEASURED). The only models the split opens are Beam and Nemotron 3 Ultra, and neither beats GLM-5.3-Flash on the one independent agentic board. Kimi, GLM-5.3, MiMo-Pro and V4 Pro need 512 GB+ machines, and in practice two or more of them.

## C. Our measured local record (read-only)

| Fact | Number | Source |
|---|---|---|
| Spark hardware | NVIDIA GB10 box, ~121 GB host, DeepSeek V4 Flash 0731 EXL3 3.0 bpw (experts pruned 256→216), one request at a time | `reference/2026-10-26_ornith122b-vs-deepseek-spark/report.md`; [10-09 report]; `fleet/specs/model-routing.md` §1 |
| Spark model items 10-05 → 11-10 | **566 items, 492 PASS on round 1 (87%), 514 PASS eventually (91%)**, 620 model rounds | `local-model/spark/done.md` (control rows excluded) |
| Spark by rung | rung 1 13/13, rung 2 19/19, rung 3 16/16 (2 of them after harness re-checks); **rung 4: 7 tickets, 5 PASS round 1, 1 on rebrief, 1 to Opus; prose: 1 PASS** | `model-routing.md` §4a, `SPARK_LADDER.md` |
| Since 10-28 (operator era) | **454 PASS, 47 FAIL, 251 CONTROL-PASS (the Claude-written golden run first), 137 operator commissions** | `spark/done.md`; `0_Brain/reference/*spark-operator*` |
| A typical operator session | o143: 35 min, 2 tickets briefed, 2 PASS, both **byte-identical to the operator's golden**; Spark model time 87.7 s for round 1. Design calls were made by Claude ("DESIGN CALL BY ME, NOT IN THE TICKET") | `reference/2026-11-11_spark-operator-o143/report.md` |
| Waiting for Claude raise | 358 READY files → **280 held paths** (11-11 17:4x) | o143 report |
| Spark duty cycle | 8.2 h model / 24.5 h round in 37 days (0.9% / 2.8%) | `spark/done.md`, summed |
| Ornith (35B-A3B, on the 96 GB M3 Ultra Studio) | 486 graded rounds, **340 PASS (70%)**; queue use essentially stopped after 09-26 | `local-model/night/done.md` |
| Ornith 1.5 122B vs DeepSeek on the Spark (same 23 prompts) | 12 vs 16 PASS | 10-26 report |
| Hosted replay of 48 Spark tasks | MiMo 46, GLM-5.3-Flash 45, DeepSeek V4 Flash 43, Spark 43 | `hosted/done_*.md`; [10-09 report] |
| Spark as shadow gate | recall 0/4 (gate 82), misses at 83-85 | `IMPROVEMENTS.md` 2026-11-02 |
| Brief-free inputs | fail RED-FIRST "almost every time" | `learnings/2026-09-18_ornith-is-cheap-the-brief-is-the-cost.md` |
| Eligibility | o143 screened 541 KS backlog tickets: **1 run, 2 "candidates, not read"**; most files were already in open PRs or held READYs | o143 report §4 |

**Tier of work done:** spelled-out one-to-three-file patches with tests, plus OpenAPI/schema carves and bash guard fixes (routing rows L1-L3). Not done: design, auth design, gates, raises, merges, deploys (rows C1-C10, G1-G2).

**Bottleneck:** Claude-side work. Specifying each item, writing the golden, running the control, reading and holding the result, then raising, gating and merging it are all Claude. The Spark's speed is not the limit (the `2026-10-05_spark-target-50-tasks-a-day.md` lesson says so: "The Spark itself is never the limit at this scale").

**UNMEASURED:** Claude tokens or minutes per operator session (the commissions do not record the operator's model); the fleet-wide share of merged work that came from local PASSes; any weekly-gauge change caused by the Spark.

## D. Economics and resilience

- **Public Claude prices** ([claude.com/pricing](https://claude.com/pricing), read 2026-11-11, USD): Max US$100/mo (5× Pro); Ultra US$200/mo (10× Pro weekly, no 5-hour limit when verified). Opus 5.5 API: US$4 in / US$20 out per million tokens ([anthropic.com/claude-opus-5-5](https://www.anthropic.com/claude-opus-5-5), released 2026-09-22). Kam's actual spend was not read and is not estimated here.
- **Scale:** A$17,449 is roughly 57 months of one US$200 Ultra seat at an *assumed* 0.65 USD/AUD (exchange rate not read today). The purchase pays back only if it removes a large share of *seats*. Section C says it does not remove seats today, because the operators, raisers and gates are the seats.
- **What a 30% cut would require:** local work that replaces Claude reasoning, meaning (a) building from a ticket with no golden (rungs 4-6), and/or (b) Sonnet-seat agentic work: raise, merge, C2 builds. Neither has been measured for a 256-class model. The hosted A/B only measured work Claude had already solved.
- **Resilience it buys:** a local Sonnet-5-class coder that keeps spelled-out work moving if Anthropic capacity drops, and some hedge against price rises. **What it doesn't buy:** coordination, gates or tier-1 work. The independent DeepSWE gap is ~10 points below Opus 5 (63 vs 74). Opus 5.5 and Fable 5.1 are not on that board; Anthropic's own TB4.0 puts Opus 5.5 at 66.4 against Fable 5.1 at 55.8 (vendor figures, ±2.6).
- **A 128 GB box already covers the outage case for today's workload.** It runs the Spark's model at 2.4-bit (44 tok/s) [10-09 report] if the Spark dies. Whether 2.4-bit holds our pass rate is UNMEASURED (10-09 first-week item 5).

## E. Recommendation

**Buy the 128 GB M5 Max (A$8,649, about a week) as the coordinator machine. Do not order the 256 GB now. Spend about two weeks and under US$20 measuring whether a 256-class model can do Claude-side work, then decide.**

Reasoning: today's local tier passes about 90% of what it is given, and what it is given has already been solved by Claude. A stronger model raises that pass rate by about 3 tasks in 48 and leaves Claude's share unchanged. The 30% test depends on local models taking over the *specifying* and the *agentic* steps, and nobody has measured that. The 128 GB is cheaper than the 96 GB, arrives about 12 weeks sooner than the 256, can stand in for the Spark, and does not lock in A$17k on a hypothesis.

**The test (hosted, zero-retention, MiMo-V2.6-Flash and GLM-5.3-Flash, using the existing `hosted/replay.py` pattern):**
1. 20 real tickets at rungs 4-6, with **no golden**: the model gets the ticket, the file at the tip and the test harness. Same checker, same gate.
2. 10 Sonnet-seat tasks (raise a held PASS, C2 build) in an agentic loop, gated by Opus as usual.
3. Record the Claude minutes spent around each task (brief + gate), so that "Claude cost per local item" exists as a number.

**Buy the 256 GB if:** (1) ≥70% of the no-golden rung-4-6 tickets pass round 1 with gates finding no more Majors than on Sonnet builds, **and** (2) the measured Claude minutes per merged local item are ≤ one-third of the same item done by a Sonnet seat. Together those make 30% plausible. Prefer the 36c/80c chip: same memory price, faster prefill. **Stay at 128 GB if** pass rates hold only on spelled-out work.

**Case against this recommendation, stated fairly:**
- Lead times may keep growing and prices may rise (DRAM plus helium). Waiting could cost more than A$17k later, or make the machine unavailable.
- The 256 is the only path to running MiMo/GLM-Flash locally at all. A strong test result is still worth nothing if the hardware can't be had, and ordering now with the order cancellable before it ships hedges that. (Whether Apple allows cancellation before shipping was not checked: UNMEASURED.)
- The Spark is a single point of failure (63 min down on 10-26; the tunnel drops), and a 256 adds a second, better local lane.
- Benchmarks put GLM-5.3-Flash *above* Sonnet 5 on independent DeepSWE (63 vs 54), so the hypothesis that it could take Sonnet seats is not far-fetched.

**What would change the answer:**
- A model that fits in 256 GB at 4-bit scoring **≥70 on independent DeepSWE** (Opus 5 is 74). Watch V4.1-Flash successors and any MiMo/GLM "Flash" refresh.
- The hosted test clearing the thresholds above.
- Anthropic cutting weekly limits, or raising Max/Ultra prices, enough that the gauge hits P2 (≥90%) regularly.
- The 256 lead time getting longer, or the price rising, which argues for a cancellable order now.

## Sources (read 2026-11-11 unless marked)
- Apple AU: apple.com/au/shop/buy-mac/mac-studio and the /m5-max-…-128gb…, /m5-ultra-…-96gb/256gb/512gb… configuration pages (rendered ~21:20 AEDT); apple.com/au/mac-studio/specs/.
- Anthropic: anthropic.com/claude-opus-5-5; claude.com/pricing.
- Independent board: deepswe.datacurve.ai (updated 2026-09-22; mini-swe-agent harness).
- Model facts: huggingface.co/moonshotai/Kimi-K3; morphllm.com/best-open-source-llm (Nov 2026 update, mostly vendor-reported numbers); MiMo-V2.6 release (rits.shanghai.nyu.edu/ai/xiaomi-open-sources-mimo-v2-6-pro-and-flash-plus-its-rl-stack/, secondary); Kimi K3.1 Pro weights (technode.com/2026/11/05/moonshot-ai-releases-kimi-k3-1-pro-model-weights/, secondary; the 1.56 TB size was not confirmed on HF).
- Clustering: appleinsider.com/articles/25/12/20/…rdma-support-on-thunderbolt-5; jeffgeerling.com/blog/2025/15-tb-vram-on-mac-studio-rdma-over-thunderbolt-5.
- Supply: appleinsider.com/articles/26/04/19/…; thestar.com.my 2026-03-26; prospect.org 2026-04-13.
- [10-09 report] = 0_Brain/reference/2026-10-09_studio-128-vs-256/{REPORT,HOSTED_REPLAY_RESULTS}.md (oMLX speeds, HF sizes, GPU budget), not re-read today.
- Local: 2_Project_Files/fleet/specs/model-routing.md; 2_Project_Files/local-model/{spark/done.md, SPARK_LADDER.md, night/done.md, hosted/README.md, hosted/done_*.md, IMPROVEMENTS.md}; 0_Brain/reference/{2026-10-26_ornith122b-vs-deepseek-spark, 2026-11-11_spark-operator-o143}; 0_Brain/learnings/{2026-09-18_ornith-is-cheap-the-brief-is-the-cost, 2026-10-05_spark-target-50-tasks-a-day, 2026-10-28_never-keep-the-spark-idle-quota-and-capability-data}.md.
