---
date: 2026-10-09
type: reference
source: research sub-agent commissioned by Wednesday 16:39 (Kam's live-board ask 16:38:17); returned as text because the harness refused the agent's own write, saved by Wednesday 17:0x. Built on 10-08 REPORT/MODEL_RANKING/QWEN122_AB/ORNITH15_AB and the Spark HANDOFF/STUDIO_HANDOUT. Every external figure read 2026-10-09 16:40-17:45 AEDT by the agent. Wednesday spot-checked against the agent's saved Apple page (scratchpad studio/buy.html): prices 4,299 / 5,199 / 9,499 / 11,449 present, and "512GB memory option for M5 Ultra coming late October" present.
status: live
---

# Second Mac Studio: 128 GB vs 256 GB, and the models each runs (2026-10-09)

Kam (live board 16:38, verbatim): "Considering getting another studio, the two options are 128 gigabytes of RAM or 256 gigabytes of RAM. Can you please evaluate the best models that can be run on either? I think from our previous discussion, the 128 can run the same model as the Spark. What about the 256 model? Are there much more capable models that could be run in addition to Flash?"

**Every figure carries its instrument.** [HF API] = summed file sizes from `huggingface.co/api/models/<repo>/tree/main`, read 2026-10-09 · [oMLX id] = a community row at `omlx.ai/benchmarks/performance/<id>`, read 2026-10-09 (date after the id = row submission date) · [ds4] = `github.com/antirez/ds4` main, read 2026-10-09 · [card] = HF model card README, read 2026-10-09 · [measured here] = Wednesday's own files · [arith] = arithmetic with inputs shown · UNMEASURED / UNREAD = no source today.

## BLUF

1. **128 GB runs** the Spark's model (DeepSeek V4 Flash 0731) at about 2.4 bits per weight: **44.2 tok/s decode, 509 tok/s prefill at 32K**, measured by others on a 128 GB M5 Max [oMLX 2m0de93y, 10-09] (the Spark does 37 / 1,032). It also runs Qwen3.8 Flash Next 4-bit at **56-89 tok/s decode, ~2,500 tok/s prefill**. **One at a time; neither fits beside Ornith 1.5 8-bit** (measured system peaks 103.8 GB and 109.5 GB of 137.4 GB [oMLX 2m0de93y, wxpvn7wx]).
2. **256 GB adds:** (a) the Spark's model at native 4-bit (unpruned) **plus** Ornith 1.5 8-bit together [arith: 161.8 + 36.8 = 198.6 GB vs a default GPU budget of 206-223 GB; never run together]; (b) ~1.5× speed on that model, **67.2 tok/s decode, 1,223 prefill at 32K** [oMLX xjji8ftx, 10-06] (M5 Ultra 1.2 TB/s vs M5 Max 614 GB/s, Apple); (c) a tier that does not fit in 128: DeepSeek **V4.1**-Flash, MiMo-V2.6-Flash 4-bit, GLM-5.3-Flash 4-bit.
3. **"Much more capable"? On paper yes; on our work unknown.** Makers' DeepSWE v1.1: V4.1-Flash 74.2, MiMo 67.9, GLM-5.3-Flash 63.4 vs **54.4** for the Spark's model [cards]. Independent board: GLM-5.3-Flash 63 ±4 vs V4 Flash 53 ±4 [deepswe.datacurve.ai, updated 2026-09-22]; **V4.1 and MiMo are not on it.** V4.1 on a 256 GB M5 Ultra runs **14-29 tok/s with 81 s to first token at 32K** (experts + Engram table spill to SSD) [oMLX bzzb9hns + 5 siblings, 10-04], and only at 2-3 bits, where ds4's own fixture shows a clear quality loss vs 4-bit.
4. **Recommendation: 256 GB, if the box's job is a local tier ABOVE the Spark, or the Spark-tier model and Ornith on one box.** 128 GB buys a second Spark-class lane, slightly faster than the Spark, nothing more capable. Price 256 GB/1 TB: **A$17,449** [arith: Apple AU A$11,449 for M5 Ultra 36c/80c 96 GB/1 TB + A$6,000 for 256 GB; the A$6,000 read at Man of Many 27 Aug 2026, NOT on Apple's page]. **128 GB price UNREAD** (M5 Max 18c/40c 64 GB/1 TB starts A$5,199; the 128 GB upgrade price loads dynamically). **Apple's page says a 512 GB M5 Ultra is "coming late October"** (price unpublished) — that is the real target if V4.1 at full quality is the goal.
5. **UNMEASURED:** every tok/s figure (strangers' rows, none on our harness); every model on our Secuura tickets except the Spark's own 3.0 bpw REAP-pruned build; quality cost of 2.4/3/4-bit builds; default GPU budget on 128/256 GB; the 128 GB price.

## The two machines (Apple, read 2026-10-09)
apple.com/au/mac-studio/specs/ and apple.com/au/shop/buy-mac/mac-studio (prices from the page's embedded price JSON).

| | 128 GB option | 256 GB option |
|---|---|---|
| Chip | **M5 Max** 18c CPU / **40c GPU** only | **M5 Ultra** 36c CPU / **80c GPU** only (30c/64c Ultra cannot take 256) |
| Memory bandwidth | **614 GB/s** | **1.2 TB/s** |
| Price (AUD) | from A$5,199 (64 GB/1 TB); 128 GB upgrade **UNREAD** | A$11,449 (96 GB/1 TB) + A$6,000 (Man of Many; UNREAD on Apple) = **A$17,449** [arith] |
| Next step | none | 512 GB "coming late October" (Apple configurator footer) |

The choice is not just RAM: Max vs Ultra is 2× bandwidth and 2× GPU cores, and MoE decode tracks bandwidth. Our current Studio: M3 Ultra 60c GPU, 96 GiB [measured here, 10-08 REPORT.md].

## GPU memory budget
- **Measured here:** this 96 GiB M3 Ultra exposes **77.76 GiB (83,494,174,720 B)** to the GPU at default `iogpu.wired_limit_mb`=0 [10-08 REPORT.md] = **0.810 × RAM** [arith]. `sysctl` today: `iogpu.wired_limit_mb: 0`, `hw.memsize: 103079215104`.
- Common rule of thumb "~3/4 of RAM" (llmconfigurator.com, osxdaily; mlx-lm #883 2026-02-12). Our 0.81 disagrees; both shown below, **neither measured on 128/256 GB**.
- Raising: mlx-lm README: "`sudo sysctl iogpu.wired_limit_mb=N` … larger than the model in MB but smaller than the machine's memory". Resets at reboot; guides leave 8-16 GB for macOS; undocumented by Apple; mlx-lm #883 reports a kernel panic at 80.14 GB wired on 96 GB. "Raised" below = RAM − 16 GiB. A sudo change = **Kam's call**.

| Budget [arith] | 128 GiB (137.4 GB) | 256 GiB (274.9 GB) |
|---|---|---|
| Default at 0.75 | 103.1 GB | 206.2 GB |
| Default at 0.81 (our measured fraction) | 111.3 GB | 222.7 GB |
| Raised to RAM − 16 GiB | 120.3 GB | 257.7 GB |

**Dedicated vs shared:** tables assume a dedicated model server (as the Spark is). If it also hosts seats/checkers, the practical budget on this 96 GiB Mac was **~60-65 GB** [measured here, MODEL_RANKING.md correction box]; Qwen 122B at 68 GB tripped the swap guard with one jest checker [measured here, QWEN122_AB.md].

**Ornith 1.5 35B-A3B:** MLX 8-bit 36.8 GB, 4-bit 19.5 GB [HF API]; 8-bit ran beside 3 seats here with no swap growth [measured here, ORNITH15_AB.md].

**KV cache is small vs weights:** V4.1-Flash 890 B/token [card] → 0.12 GB at 128K [arith]; V4 Flash ~4× that [card] → ~0.47 GB at 128K [arith]; MiMo-V2.6-Flash 23,040 B/token → 3.0 GB at 128K [arith from card config]. Where an oMLX row gives a measured 32K footprint, the fit column uses it.

## Option A: 128 GB (M5 Max 40c, 614 GB/s)

| Model · quant | File size (source) | Fits? | Beside Ornith 1.5? | Speed @32K decode / prefill tok/s (source) |
|---|---|---|---|---|
| **DeepSeek V4 Flash 0731** (Spark's model; 284B/13B active, 1M ctx [card]) · MLX 2.4-bit mixed | 92.8 GB [HF API mlx-community/DeepSeek-V4-Flash-0731-2.4bit-mixed]; ds4 Q2 ~81 GiB (87.0 GB) [ds4] | **YES** — footprint 89.71 GB @32K, wired peak 94.53, in use 103.76 of 128 [oMLX 2m0de93y, 10-09] | **NO** — 8-bit 126.5 > 120.3; 4-bit 123.3 of 137.4 [arith] | **44.2 / 509** [2m0de93y]; 44.6 / 623 [bmxh02yb]; oQ2e-mtp 54.9 / 663 [av61pveu]; ds4 Q2 34.4 / 557 [ds4]. Spark: 37 / 1,032 [measured, Spark HANDOFF] |
| **Qwen3.8 Flash Next** (125B/6B + 51B n-gram table, 262K [card]) · oQ4e-mtp | 106.3 GB [HF API]; mlx-community 4-bit 111.5 GB | **YES** — footprint 87.21 GB, in use 109.52 @32K [oMLX wxpvn7wx, 10-08] | **NO** — 146.3 > 137.4 RAM [arith] | **78.2 / 2,525** [wxpvn7wx]; 88.6 [97otwmgo]; 56.4 [yua4gypy]; 56.1 [ktoscn7f]; 16.1 outlier [2iolu6mv]; ds4 Q4K 48.4 / 1,330 [ds4 QA §18] |
| **GLM-5.3-Flash** (320B/18B [card]) · 2-bit | ds4 Q2 ~90 GiB (96.6 GB); antirez Q2 96.5 GB [HF API] | **MARGINAL** (ds4: "close enough to a 128 GB machine's memory budget that other workloads and context size matter") | NO | **9.3-24.6 / 192-332** [5 rows, 09-21…26]; 2-bit quality UNMEASURED |
| **gpt-oss-120b** (117B/5.1B) · MXFP4 | 63.4 GB [HF API] | YES | **YES** — 100.2 < 103.1 [arith, weights only] | **61.8-66.6 / 1,094-2,089** [5 rows] |
| **Ornith 1.5 35B-A3B** · 8-bit | 36.8 GB [HF API] | YES | (itself) | **91.0 / 4,142** [91f99c7h]; oQ8e-mtp 101.2-107.5; this Mac: 82.4 / 2,299 [measured here] |
| Too big | MiniMax-M2.7 4-bit 128.7 GB; Step-3.7-Flash 4-bit 110.8 GB (raised only); V4 Flash 4-bit 151.5 GB [HF API] | NO | | V4.1 by SSD streaming on M5 Max 128: **8.3 / 61** [zycxgdnr, 3-bit] — not usable |

**Kam's premise:** yes in effect, with a caveat. Today's 12:27 answer was about **Flash Next (Qwen)**. The Spark's DeepSeek also fits in 128 GB but at ~2.4 bpw with all 256 experts; the Spark runs **EXL3 3.0 bpw with experts pruned 256 → 216** [Spark HANDOFF §8]. Same model, different compression; quality on our tickets UNMEASURED. On the makers' scores Flash Next sits a little ABOVE V4 Flash 0731 (DeepSWE 58.7 vs 54.4, SWE-Pro 62.5 vs 56.0 [Qwen card]) and is faster on the M5 Max (~78 vs 44 decode; 2,525 vs 509 prefill).

## Option B: 256 GB (M5 Ultra 80c, 1.2 TB/s)

| Model · quant | File size (source) | Fits? | Beside Ornith 1.5 8-bit? | Speed @32K decode / prefill tok/s (source) |
|---|---|---|---|---|
| **DeepSeek V4 Flash 0731** native MXFP4 (Spark's model, unpruned) | mlx-community 4-bit 151.5 GB; 8-bit 155.1 GB [HF API] | **YES** — footprint 161.82 GB @32K [oMLX xjji8ftx, 10-06] | **YES on paper** — 198.6 < 206.2 / 222.7, 7.6-24.1 GB spare [arith]; never run together | **67.2 / 1,223** [xjji8ftx, MTP 3]; 65.1 / 1,229 [dts7mkyt]; 56.7 [vwgenzyj]. All on **64c**; 80c UNMEASURED |
| **DeepSeek V4.1-Flash** (552B backbone, 8B/16B active, +196B Engram table, 1M ctx, multimodal [card]) · Q2 / oQ3e | ds4 Q2: 341 GiB file, **main weights 151.8 GiB (163.0 GB)** resident, Engram from disk [ds4]; oMLX oQ3e-mtp 355.3 GB [HF API] | **YES, main weights only** — oMLX footprint **211.66 GB**, in use 233.12 GB at 0.85 resident fraction [bzzb9hns, 10-04] (over 206.2, under 222.7) | **NO** — 248.5 > 222.7 [arith] | **13.6-29.3 / 290-479, TTFT 81 s @32K** [6 rows, M5 Ultra 64c]; ds4 Q4 fully resident on a **512 GB** M3 Ultra: 18.1 / 716 [ds4 QA §17] |
| **MiMo-V2.6-Flash-RL** (309B/15B, 1M, MIT [card]) · 4-bit MTP | 164.3 GB + ~7.4 GB side modules [HF API]; mxfp4-q8 167.3 GB | **YES** — 167.3 < 206.2 [arith; no measured footprint] | **TIGHT** — 201.1 GB weights, 5 GB under 206.2; treat as no | **68.6 / 2,329** [d5cyrurj, 80c]; MOPD 73.6 / 2,475 [vk738nty, 64c]; 54.1-54.2 without MTP |
| **GLM-5.3-Flash** (320B/18B, MIT) · 4-bit | mlx 4-bit 204.0 GB; ds4 Q4 191.1 GB; unsloth UD-Q4_K_XL 199.7 GB | **YES** — oQ4e footprint 177.26, in use 194.83 [b4gh11eo, 10-08] | **NO** — 214.1 > 206.2 [arith] | **wide spread:** 56.6 / 1,942 [64c, no MTP]; 99.4 [64c]; **126.1-128.3 / 2,340** [80c]; oQ4-MTP 61.7-86.1 |
| **Qwen3.8 Flash Next** · oQ6e / oQ8e | 150.4 / 194.9 GB [HF API] | YES (oQ8e only at 0.81) | oQ6e 187.2 → **YES** [arith] | oQ6e **113.8 / 4,538** [80c]; oQ4e 99.9-127.6 / ~5,600 |
| **Ornith-1.5-397B** · Q4_K_M | 244.3 GB [HF API] | RAISED LIMIT ONLY (13 GB spare) | NO | UNMEASURED |
| **Qwen3.5-397B-A17B** · 4-bit | 223.9 GB [HF API] | RAISED LIMIT ONLY | NO | 32.2 / 366 on M3 Ultra 60c 256 GB [y6t7xpjx, 05-29] |
| Out of reach | V4 Pro 4-bit 837 GB; GLM-5.3 full 4-bit 418 GB; Kimi K3 1,561 GB; MiniMax-M3 4-bit 241.5 GB (raised only); Qwen3.8-2.4T 4,892 GB [HF API] | | | |

## Capability: the 256-only tier vs Flash

| Model | Fits on | DeepSWE v1.1 (maker) | DeepSWE (**independent**) | Terminal-Bench 2.1 (maker) | SWE-bench Pro |
|---|---|---|---|---|---|
| Claude Opus 5 (reference) | cloud | 74.0 [V4.1 card] | **74 ±4** | 89.1 | — |
| **DeepSeek V4.1-Flash** | 256, slow | **74.2** | not listed | **90.6** | — |
| **MiMo-V2.6-Flash** | 256 | **67.9** | not listed | 87.6 | — |
| **GLM-5.3-Flash** | 256 at 4-bit; 128 at 2-bit only | 63.4 [10-08 MODEL_RANKING; not re-read today] | **63 ±4** | 84.3 (same caveat) | — |
| Qwen3.8 Flash Next | 128 and 256 | 58.7 | not listed | — | 62.5 |
| Ornith-1.5-397B | 256, raised only | 56.0 | — | 86.1 | 65.1 |
| **DeepSeek V4 Flash 0731 (the Spark)** | 128 and 256 | 54.4 | **53 ±4** | 82.7 | **56.0 [Qwen card] vs 64.4 [Ornith card]** |
| Ornith 1.5 35B-A3B | anywhere | 22 [10-08] | — | 67.8 | 59.6 |

Independent board: deepswe.datacurve.ai ("updated September 22, 2026"; all models on mini-swe-agent).
- **Agree:** where both exist, independent matches makers within error (Opus 5 74/74.0; V4 Flash 53/54.4; GLM-5.3 full 69/66.9; Kimi K3 69/67.5; V4 Pro 63/62.7).
- **Disagree / uncheckable:** SWE-bench Pro for the Spark's own model differs by 8.4 points between two makers' tables; **V4.1's 74.2 and MiMo's 67.9 have no independent check** (V4.1 scored on DeepSeek's own harness at 1M context); **every score is full precision** — the 256 GB runs V4.1 at 2-3 bits with Engram on SSD, and ds4's fixture shows Q2 clearly losing to Q4 on V4.1 (mean NLL 0.365 vs 0.247; top-token agreement 2,697 vs 2,896 of 2,994) [ds4 QA §17]. **The 74.2 does not transfer to the build that fits.** MiMo and GLM at 4-bit are closer to their scored precision.

**Kam's "metrics don't always tell the truth", already shown here:** Ornith 1.5 35B's maker DeepSWE went 0 → 22 and SWE-Pro 50.4 → 59.6, yet both versions scored **17/20** on our 20 graded Secuura night tasks [measured here, ORNITH15_AB.md]. The Spark's model sits mid-table on makers' charts yet passed **42/46** rows in `spark/done.md` [10-08 MODEL_RANKING]. So "+10 to +20 DeepSWE points" is a **hypothesis for our tickets**; the Spark ladder and our A/B harness are the real test.

## Recommendation
**Buy 256 GB if the second Studio's job is "a tier above the Spark, locally"; buy 128 GB only if its job is "a second Spark-class lane".**
- 256: holds the Spark-tier model at native 4-bit AND Ornith 8-bit (198.6 GB [arith]); ~1.5× faster on that model (67 vs 44 decode, 1,223 vs 509 prefill); the only option that can try MiMo 4-bit (~69 tok/s), GLM-5.3-Flash 4-bit (57-128) and V4.1 at 2-3 bits (14-29 tok/s — an overnight / hard-ticket tier, not a daily driver).
- 128: duplicates the Spark rather than exceeding it; can never hold the Spark-tier model plus Ornith; its best fit, Flash Next 4-bit, is at most a small step above V4 Flash on makers' scores, and is the model that failed to load beside the fleet here on 10-08 [measured here].
- **What could reverse it:** the price gap (128 GB price UNREAD); **512 GB "late October"** — ds4 says V4.1 at Q4 needs 512 GB for full residency, so for V4.1 at full speed and quality 512 GB is the real target (price unpublished); if the box is shared with seats, subtract ~35-40 GB of practical budget [measured here].

## First-week measurements (if bought)
1. Memory ground truth: default GPU budget (`recommendedMaxWorkingSetSize`, as on 10-08) and `iogpu.wired_limit_mb` — settles 0.75 vs 0.81.
2. Spark model like-for-like: V4 Flash MXFP4 on oMLX with `bench.py`; replay the Spark's 46 `spark/done.md` rows with the same prompts and checker; compare pass count, decode/prefill, wall time.
3. Co-residency: V4 Flash 4-bit + Ornith 1.5 8-bit together, the 20-task Ornith set during the replay; record swap, `memory_pressure`, guard trips.
4. 256-only ladder: MiMo 4-bit → GLM-5.3-Flash 4-bit → V4.1 Q2/oQ3e on QWEN122_AB.md's 5 hard tasks + the 20-task set; pass/fail, TTFT on 20-70K prompts, wall time per turn.
5. Quant check: V4 Flash 2.4-bit vs 4-bit on the same 46 rows (what the 128 GB's compression costs on OUR work).
6. Stability: 10-hour soak (oMLX #3723), `pmset -g therm`, `iostat` for V4.1's Engram/SSD reads.

## UNMEASURED / UNREAD
- 128 GB upgrade price (AUD); the A$6,000 256 GB upgrade read only at Man of Many.
- Default GPU budget on 128/256 GB.
- Every tok/s figure (oMLX community rows / ds4 docs); wide spreads (GLM-5.3-Flash 56-128 on one chip class); V4 Flash 4-bit has no 80c M5 Ultra rows; Ornith-1.5-397B no Mac speed; Kimi K3 / MiniMax-M3 queries rate-limited (429), neither fits anyway.
- V4.1 and MiMo on no independent board; GLM-5.3-Flash card not re-read today.
- Quality at 2-3 bits on our tickets, for every model.
- Licences: only the DeepSeek, MiMo and GLM-5.3-Flash cards' MIT re-read.

## Sources read 2026-10-09 (by the research agent)
Apple: apple.com/au/mac-studio/specs/; apple.com/au/shop/buy-mac/mac-studio (embedded prices m5max-18-32 A$4,299, m5max-18-40 A$5,199, m5ultra-30-64 A$9,499, m5ultra-36-80 A$11,449; footer "512GB memory option for M5 Ultra coming late October"). Man of Many manofmany.com/tech/mac-studio-m5-max-m5-ultra (updated 27 Aug 2026). mlx-lm README + issue #883. HF API sizes for every repo named. Cards: deepseek-ai DeepSeek-V4-Flash-0731 / -V4-Flash / -V4.1-Flash; zai-org GLM-5.3-Flash; XiaomiMiMo MiMo-V2.6-Flash-RL; MiniMaxAI MiniMax-M2.7, M3; Qwen Qwen3.8-Flash-Next, Qwen3.5-397B-A17B; ornith-ai Ornith-1.5-397B; moonshotai Kimi-K3; stepfun-ai Step-3.7-Flash. ds4: MODELS.md, PERFORMANCE.md, SSD_STREAMING.md, QA_BEFORE_RELEASES.md §16-18. oMLX rows by id (detail pages read for 2m0de93y, xjji8ftx, bzzb9hns, b4gh11eo, wxpvn7wx). deepswe.datacurve.ai (updated 2026-09-22). Wednesday's files: 2026-10-08_omlx-flash-next/{REPORT, MODEL_RANKING, QWEN122_AB, ORNITH15_AB}.md; 2026-09-22_spark-deepseek-v4-flash/{HANDOFF, STUDIO_HANDOUT_2026-09-25}.md; daily/2026-10-09.md 12:27. Raw evidence: session scratchpad `studio/` (not durable).
