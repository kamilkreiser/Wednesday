<h1>AI machine combinations: decision paper</h1>
<div class="sub">For Kam Kreiser · prepared by Wednesday (research analyst, Claude Opus 5.5) · 26 October 2026, AEDT · all prices AUD incl. GST, read 2026-10-26 unless stated · <b>quality is weighted above speed throughout</b> (your 20:29:55 instruction)</div>

<div class="box">

## Executive summary

**Recommendation.** Your split is right in shape: one local box per client is the simplest way to keep Datasec and Secuura apart. Change three things:

1. **Make the laptop 64 GB, and take the fleet off it.** At 32 GB the laptop is today's measured bottleneck.
2. **Don't replace the HP with a like-for-like GB10 until a one-day trial has run.** The strongest local coding model today, DeepSeek **V4.1** Flash, needs a 256 GB box. A 128 GB GB10 can't run it at a quality worth having.
3. **Be clear about what the local box does for QA.** It runs the test suites. It does not yet judge PRs.

| Role | Machine | AUD |
|---|---|---|
| Datasec local model box | 256 GB Mac Studio (ordered; chip/config/price of your order not in our records — figure shown is Apple AU's current list price for the M5 Ultra 36/80-core, 256 GB, 1 TB) | 17,449 (list) |
| Secuura local model box, **if the trial passes** (expected) | A second Mac Studio M5 Ultra, 256 GB, 1 TB, running V4.1 Flash | 17,449 |
| Secuura local model box, **if the trial fails** | GB10 Founders Edition 4 TB (same chip as the HP). Reproduces today's Spark exactly | 8,879–9,399 |
| Travelling laptop | MacBook Pro 14" M5 Pro, 18-core CPU, 64 GB, 1 TB | 5,799 |
| At-desk fleet host (seats, test suites, Docker) | your existing 96 GB M3 Ultra Mac Studio [ours: `2026-10-10_mac-ram-local-coding-models/REPORT.md` §2] | 0 |
| **Total** (list-price based) | Recommended / fallback | **40,697 / 32,127–32,647** |

**The local model and how to run it.** For Secuura, **DeepSeek V4.1 Flash** on the 256 GB Studio, served with ds4 or oMLX on Apple's MLX/Metal stack, one client per box. Two ways to load it:

- **Q2, fully in memory:** reported 28–30 tok/s on an M5 Ultra.
- **Q3–Q4 with part of the model on the SSD (higher quality):** about 10–20 tok/s [est].

Speed is secondary, so the higher quant is the pick. V4 Flash stays as the fallback; it is measured at 16–18/23 on our hard set.

**One-line answers to tonight's questions**

- **Your split.** Agree, with the three changes above. Suites run on CPU cores, so put them on the desktop host, not the model box. A GB10 serving DeepSeek has only about 10 GB left for suites and Docker [ours].
- **Returning the HP.** Yes, return it. It is the dearest GB10 in Australia (A$11,599–12,413) for the same chip that the NVIDIA Founders Edition sells for at A$8,879–9,399. AU stock is still priced at the old US price (US$6,950 since 2 Oct), so if a GB10 is the answer, buy soon.
- **Local coding models.** Shortlist for a measured trial on our 23-task set: V4.1 Flash, MiMo, GLM Flash, and Qwen3-Coder (section 7). DeepSeek V4 Flash (16/23) and Ornith 122B (12/23) are measured already.
- **V4.1 Flash with part of the model on the SSD.** It works on Macs today. The table of word-lookup data V4.1 consults ("Engram") costs about 1% of speed when it is read from the SSD [reported]. Putting experts on the SSD is what lets the Q3–Q4 quants fit in 256 GB. No-one has published a measured Q4 run on a 256 GB Mac; our estimate is 10–20 tok/s.
- **Splitting the model across a Mac, the Spark and the SSD.** No. Only llama.cpp's networked mode joins a Mac and a CUDA box into one model; its own README calls it "fragile and insecure", and the one measured Mac + Spark split lost 43–47% of decode speed [reported]. The Spark also goes back.
- **Joining the laptop to the Studio over Thunderbolt.** Possible (MLX or exo, Mac-to-Mac) but not worth it. No Studio + MacBook benchmark exists, a working laptop adds little memory, and the model drops whenever the laptop travels. For more than 256 GB, buy the 512 GB Studio.
- **The engine.** Tuesday, Wednesday and Friday stay on Claude Code with the newest Opus for coordination. Routing stays as the approved table sets it. A local box adds capacity for briefed tickets and runs the deterministic test suites. It replaces no gate, design, deploy, or client-facing step (section 4).

**What we measure first when the Studio lands**

1. Before the HP goes back, run **V4.1 Flash on the 23-task hard set**, either through a zero-retention hosted provider or on the Studio itself. It is the same harness as `spark-ab/`, and the hosted route costs under US$1. **Buy the second Secuura box only if V4.1 beats V4 Flash's 16/23 by at least 3 tasks.**
2. On the Studio: Q2 in memory against Q3/Q4 with SSD offload (speed and score), then memory headroom next to Tuesday's seats.

</div>

<h2 class="pb">1. BLUF: do we agree with your setup?</h2>

Every number carries a label. **[ours]** means we measured it on our own machines (file path given). **[reported]** means a third party measured it (source in section 9). **[vendor]** means the maker reported it about its own product. **[est]** means our own arithmetic or a judgement; nobody has measured it.


**Broadly yes. Here is where we agree:**

- A dedicated 256 GB Studio for Datasec matches the hard rule that keeps the clients apart. It also matches Tuesday's ruling from 22 October: the local tiers collapse into Sonnet until the box arrives (`learnings/2026-10-22_tuesday-sonnet-default-usage-is-a-guide.md`).
- A separate local box for Secuura is the right pattern. On 25 September you ruled that Secuura code may go to the Spark, one client per task (`fleet/specs/model-routing.md` §2, P4). **Your 20:26 message sets the Datasec use of the 256 GB Studio; Tuesday's routing table** (which today says "no local tier" for Datasec, P4) **needs updating to use it.**

**Caveat 1: "QA" is two jobs, and only one of them is ready for the local box.**

- **Mechanical QA works today, and it needs no model.** That covers fetching the head, red/green on base against head, suite counts, lint and planted violations. `spark_gate.sh` matched the Claude gates' facts exactly, in about 85 s [ours: `learnings/2026-10-26_spark-gate-pilot-if-it-works-put-it-into-practice.md`, calibration 1].
- **Review judgement fails today.** The Spark's review was wrong in all three calibrations:
  - **Calibration 1:** it missed findings and raised false positives.
  - **Calibration 2:** on a tier-1 PR it produced no verdict at all, because of a repetition loop. It found 0 of 7 findings.
  - **Calibration 3:** it gave two false NO GOs out of two, where Sonnet's gate said GO WITH NOTES.
  - That is **0 promotable rounds** [ours, same file]. Tier 1 stays on Opus, tier 2 stays on Sonnet, and the Spark stays a shadow.
- So the box can do most of the heavy **testing**, but not the **QA judgement**. That still costs Claude tokens. The gain is that the gate no longer pays to re-run suites.

**Caveat 2: the laptop is the measured bottleneck, not the Spark.**

- On 26 October the 32 GB MacBook Pro ran 4–6 Claude seats, test suites and Docker. It hit load 77–97 on 12 CPUs, with the Docker VM at 870–920% CPU and `docker ps` hung for more than 4 minutes.
- At other times the cause was node test suites (~808% CPU), Photos media analysis (load 51), or Spotlight indexing the new worktrees (load 18–20).
- Gates and pushes had to queue behind a load waiter all day [ours: `daily/2026-10-26.md` 12:1x, 14:18, 14:46, 16:52].
- Ornith 122B cannot run on that laptop at all.
- **Fix:**
  - Run the at-desk fleet (seats, suites, Docker) on your existing 96 GB M3 Ultra Mac Studio [ours: `2026-10-10_mac-ram-local-coding-models/REPORT.md` §2].
  - Buy a 64 GB laptop with 18 CPU cores for travel.
  - A 128 GB laptop only earns its price if you want a local model *on the road*. It cannot comfortably host a model and the seats at the same time: about 100–110 of 128 GB [est: `2026-10-26_deepseek-quant-on-spark/report.md`].

**Caveat 3: the model box and the suites compete for memory.**

- DeepSeek V4 Flash loads 95.4 GiB on the Spark's 121 GB [ours: `daily/2026-10-26.md` 12:24].
- Ornith 122B used 111–112 of 121 GB [ours: `2026-10-26_ornith122b-vs-deepseek-spark/report.md`].
- That leaves roughly 10–25 GB for test suites and throwaway Postgres containers.
- So "the Spark does the heavy testing" works only for light suites. Heavy suites belong on the desktop host.

## 2. Recommendation and alternatives

**Recommended (quality-first, phased):**

- Studio 256 for Datasec (ordered), a second Studio 256 for Secuura (gated on the trial), a MacBook Pro M5 Pro 64 GB, and your existing 96 GB M3 Ultra Mac Studio as the at-desk fleet host [ours: `2026-10-10_mac-ram-local-coding-models/REPORT.md` §2]. The 256 GB Studio figure is Apple AU's current list price; your order's chip, config and price are not in our records.
- **A$40,697** (A$23,248 of it is already committed or is the laptop).
- **Fallback if V4.1 does not beat V4 Flash by 3 or more of 23 tasks:** a GB10 Founders Edition instead of the second Studio, **A$32,127–32,647**.
- **Why a second Studio over a GB10 for Secuura:**
  - A GB10 tops out at V4 Flash, 128 GB class. V4.1 Flash only fits a GB10 at 1.6-bit. At that size the quantised model's next word matches the full model's only 69–88% of the time [reported: modemguides].
  - V4.1 is the bigger quality step:
    - [vendor] DeepSWE 77.0 (1017 build) against V4 Flash 54.4.
    - [reported, independent] Vals Terminal-Bench 2.1 74.5%.
  - Secuura's work is the security-sensitive work, and you asked for quality over speed.

| Option | What it is | AUD | Gains | Loses | Client isolation |
|---|---|---|---|---|---|
| **R (recommended)** | Studio 256 ×2 (one per client) + MBP M5 Pro 64 GB + existing 96 GB Studio as fleet host | **40,697** | V4.1 Flash for both clients; one stack (MLX) to maintain; 1.2 TB/s bandwidth | No CUDA, so no EXL3 or vLLM batching; prefill slower than a GB10 [reported] | Best: one box per client |
| **A (your plan)** | Studio 256 (Datasec) + GB10 (Secuura) + laptop | 32,127 (Founders 4 TB A$8,879) to 32,647 (in-stock A$9,399) | Reproduces today's Spark exactly: V4 Flash EXL3 3-bit, 33 tok/s, 16/23 [ours]; fast prefill (~1,030 tok/s [ours]) | Secuura stays a model generation behind (no V4.1); two stacks (CUDA + MLX) | Best: one box per client |
| **B** | Studio 256 + **Strix Halo** 128 GB (Minisforum MS-S1 Max) + laptop | 28,967 (sale price) | Cheapest | No EXL3 (CUDA-only), so V4 Flash runs as GGUF. GGUF was already 3× slower end-to-end on the GB10 [ours]. Strix Halo prefill is 2–9× slower again under load [reported: StorageReview]. Our prompts are 14–71K tokens, so a 71K prompt waits about 4 minutes [est]. ROCm/Vulkan are less mature | One box per client |
| **C** | **One 512 GB Studio** shared by both clients + laptop | price not published ("coming late October"); about 25,000–30,000 [est] + 5,799 | Best single-box quality: V4.1 Q4 fully in memory, 20–41 tok/s on an M3 Ultra 512 [reported]; KLD (how far the quantised model's predictions drift from the full model's; lower is better) 0.009 for Q4 against 0.138 for Q2 [vendor: Unsloth] | One request at a time across both clients; a single point of failure; your 256 GB order would need changing; Datasec on a shared box is unruled | Workable only with per-client run directories, one client per task and no shared caches. It needs your ruling |
| **D** | Studio 256 + **Studio M5 Max 128 GB** for Secuura + laptop | 31,897 | Cheaper than a GB10. Runs V4 Flash 2-bit through ds4 at 27–39 tok/s [reported: ds4 PERFORMANCE.md, M5 Max]; IQ2_XXS scored 18/23 on our set [ours, on the GB10]; one stack | Same model tier as A (no V4.1); prefill 400–790 tok/s [reported], below the GB10's | One box per client |
| **E** | Studio 256 + **two GB10s joined** over their QSFP ports (Secuura) + laptop | 41,006 (two Founders Editions at A$8,879) | V4.1-Flash at EXL3 2.9 bpw: 73 tok/s for one request, ~2,000 tok/s prefill [reported: tonyd2wild]; CUDA batching | 2.9-bit is lower quality than a Q4 on a Studio; two boxes and a cluster to maintain; unmeasured by us | One cluster per client |

<span class="small">Laptop in every option: MacBook Pro 14" M5 Pro, 18-core CPU / 20-core GPU, 64 GB, 1 TB, A$5,799 (Apple AU). It has the same 18-core CPU count as the M5 Max at A$2,100 less; the GPU doesn't matter if the laptop hosts no model. Choose 2 TB if worktrees will live on the internal disk. The Studio 256 GB price is today's configurator price for the 36/80-core chip, A$17,449. Our 10 October read showed 256 GB on the 30/64-core chip at A$15,499; today's read says 256 GB needs the 36/80 chip. Your order's exact price is not in our files.</span>

## 3. Machine table

| Machine | AU price (source, read 2026-10-26) | Memory / bandwidth | DeepSeek fit and speed | Concurrency | Stack | Verdict |
|---|---|---|---|---|---|---|
| **Mac Studio M5 Ultra 256 GB** 1 TB / 2 TB | **17,449** / 18,199 (Apple AU list; your order's config/price not in our records) | 256 GB / 1.2 TB/s | **V4 Flash 4-bit:** fits (peak 142 GB); 35 tok/s on M3 Ultra [reported: omlx.ai]. **V4.1 Q2 in memory:** 28–30 tok/s on M5 Ultra [reported: ds4 #1239]; up to 54–75 tok/s with forks [reported: niklaslenz]. **V4.1 Q3/Q4 with SSD offload:** 10–20 [est]; oQ3e paged on an M3 Ultra 256: 10–15 [reported] | Batch 4 gave 78.8 tok/s total on V4 Flash [reported]; we would run one per client | MLX / oMLX / ds4 / llama.cpp Metal | **Buy** (ordered) |
| Mac Studio M5 Ultra 512 GB | Not published ("late October"); 25–30k [est] | 512 GB / 1.2 TB/s | V4.1 Q4 fully in memory: 20–41 tok/s on M3 Ultra 512 [reported: IngeniousIdiocy, PR #3574] | as above | as above | The quality ceiling; wait for the price |
| Mac Studio M5 Max 128 GB | 8,649 (Apple AU) | 128 GB / 614 GB/s | V4 Flash 2-bit (~81–92 GB): 27–39 tok/s [reported: ds4]. V4.1 only by streaming from the SSD | 1 | MLX / ds4 | Cheap V4 Flash box (option D) |
| MacBook Pro 14" M5 Pro 64 GB | 5,799 (Apple AU) | 64 GB / 307 GB/s | Not a model host | n/a | n/a | **Buy** as the laptop |
| MacBook Pro 14" M5 Max 64 / 128 GB | 7,899 / 10,299 (Apple AU) | 614 GB/s | 128 GB: V4 Flash 2-bit fits (~92 GB) but not beside the seats [est] | 1 | MLX | Only if you want a model on the road |
| **NVIDIA DGX Spark Founders** 4 TB | **8,879** (Landmark, stock not stated) · 9,399 (MSY/Umart, in stock) · 9,999 (Scorptec/PLE) | 128 GB (121 usable) / 273 GB/s | **V4 Flash EXL3 3-bit: 33 tok/s, 16/23 [ours]**; GGUF 19.5 tok/s [ours]. V4.1 only at 1.6-bit | Our setup runs one request at a time (`MAX_NUM_SEQS=1`) [ours]; vLLM can batch: 32 parallel requests gave ~353 tok/s on gpt-oss [reported: llama.cpp] | CUDA 13, vLLM, SGLang, EXL3: mature | Best-value GB10 |
| ASUS Ascent GX10 1 TB / 4 TB | 8,999 (Scorptec) / 11,549–11,999 | same | same chip | same | same | Fine; 1 TB is tight next to 200 GB of weights |
| MSI EdgeXpert 4 TB | 9,974–9,999 (MegaBuy / Scorptec) | same | same | same | same | OK |
| Gigabyte AI TOP ATOM 4 TB | 9,999 (Scorptec / MSY, in stock) | same | same | same | same | OK |
| Lenovo ThinkStation PGX | 9,402 (1 TB, MediaForm, index snippet) / 10,760 (2 TB) | same | same | same | same | Dearer |
| Dell Pro Max GB10 4 TB | 12,546 (Dell AU) | same | same | same | same | Dearer |
| **HP ZGX Nano G1n** 4 TB (our demo) | 11,599 (Prology, index snippet) · 12,413 (Techbuy, backorder) | same | same (it *is* our Spark) | same | same | **Overpriced; return it** |
| Acer Veriton GN100 4 TB | 8,899 (Prology) | same | same | same | same | Out of stock |
| **Strix Halo** 128 GB: Minisforum MS-S1 Max | 5,719 (sale; usually 7,149), Minisforum AU | 128 GB (up to ~96–112 usable by the GPU) / 256 GB/s | gpt-oss-120b: 34–54 tok/s decode, 340–459 tok/s prefill [reported: Hardware Corner, ComputingForGeeks]. V4 Flash GGUF unmeasured; slower than the GB10 [est] | 2–9× behind a GB10 under load [reported: StorageReview] | ROCm / Vulkan: maturing; results swing 2× by backend [reported] | Cheapest, weakest for our long prompts |
| Other Strix Halo 128 GB | GMKtec EVO-X2 6,471 (Amazon AU, imported) · Corsair AI WS 300 6,999 (JW) · Framework 6,069 (out of stock) · Beelink ≈6,804 (US price converted) · HP Z2 Mini G1a 128 GB: **no AU price** · MSI: **none found** | same | same | same | same | Same verdict |
| AMD "Gorgon Halo" 192 GB (Ryzen AI Max+ PRO 495) | **No AU stockist.** Framework 192 GB US$6,799 DIY ≈ A$10,637 (US price converted) | 192 GB / ~273 GB/s | Unmeasured by us | same | ROCm / Vulkan | Watch, not now |

<span class="small">Currency: RBA 26 Oct 2026, 1 AUD = 0.7031 USD; "US price converted" = US price ÷ 0.7031 + 10% GST. The Founders Edition US price rose to **US$6,950** on 2 Oct 2026 (The Register), which is ≈A$10,873 converted, so AU stock is still priced at the older US price. NVIDIA also launched a **64 GB GB10** from US$4,999 on 23 Oct. It is too small for DeepSeek. "Index snippet" rows came from a search index; the page itself was not opened live.</span>

## 4. The engine: Claude Code stays in charge

You asked that Tuesday, Wednesday and Friday stay on Claude Code with the best model, and that work is spread across Opus, Sonnet and the local models. That is exactly what the approved routing v1.0 does (`2_Project_Files/fleet/specs/model-routing.md`). New machines change **capacity**, not **who decides**.

| Work | Model today | What a new local box adds | What it does NOT replace |
|---|---|---|---|
| Coordination (Tuesday, Wednesday, Friday) | Newest Opus, row C9 | Nothing | The coordinator seat |
| Security and auth design; data-destroying paths; deploys | Opus, rows C3 / C4 / C6 | Nothing | All of it |
| Tier-1 gates | Opus (G1) | `spark_gate.sh` runs the suites first, so the gate spends its tokens on judgement only [ours] | The gate's verdict (0/3 calibrations) |
| Tier-2 gates, raising PRs, merges, builds | Sonnet (G2, C1, C5, C2) | The same facts.json pre-run; a shadow review that keeps adding calibration rows | The verdict, the raise and the merge |
| Briefed tickets, rungs 1–4 | Spark first (L1–L4); Ornith second | **Datasec gets a local lane for the first time** (your 20:26 message sets this; Tuesday's routing table needs updating to use it). Secuura gets V4.1 if the trial passes | Brief writing (the real cost) and the review of every local PASS |
| Running test suites, lint, red/green | Wherever the seat runs (the laptop today) | Desktop CPU cores; the laptop stops choking | Nothing; this is pure gain |

**Measured local record that supports this split:**

- Spark rungs 1–3: 48/48. Rung 4: 5/7, then 6/7 [ours: `model-routing.md` §4].
- Hard set: V4 Flash 16/23, Ornith 122B 12/23 [ours].
- Hosted replay of 48 Spark tasks: MiMo 46/48, GLM 45/48, V4 Flash 43/48 [ours: `2026-10-10_mac-ram-local-coding-models/REPORT.md`].
- Local models are good at spelled-out patches. They are weak at concurrency semantics and at fixing their own misconceptions from feedback [ours: `2026-09-22_spark-deepseek-v4-flash/HANDOFF.md`].

## 5. V4.1 Flash with SSD offload: what it means in practice

**What it is:**

- DeepSeek V4.1 Flash has 552B total parameters with 8–16B active per token, plus about 189 GiB of "Engram" tables (a large table of word-sequence lookups the model consults as it goes).
- ds4 builds: Q2 = 152 GiB of main weights, Q4 = 294 GiB. Engram is read from the file on demand in every mode [reported: ds4 MODELS.md].
- Llama.cpp merged V4.1 support only yesterday (PR #31086, 25 Oct). The Mac runtimes today are ds4 and oMLX.

| Build on a 256 GB Studio | Quality cost (lower KLD is better) | Speed | Label |
|---|---|---|---|
| Q2 fully in memory (ds4, 152 GiB) | Unsloth's nearest equivalent, UD-Q2_K_XL: KLD 0.138, top-1 match 91.5%. ds4's own Q2 has **no published quality number** | 28–30 tok/s on M5 Ultra; ~21 with experts streamed from the SSD | [vendor] KLD / [reported] speed |
| Q3 (oQ3e) with part of the model on the SSD | UD-IQ3_XXS: KLD 0.063, 94.6% | 10–15 tok/s paged; 25–30 when cut down to fit in memory (M3 Ultra 256) | [vendor] / [reported: drowzeys] |
| Q4 (294 GiB) with experts on the SSD | UD-Q4_K_XL: KLD 0.009, 98.2%; close to full precision | **No measured 256 GB run.** 10–20 tok/s [est]. Basis: 18.7–22 tok/s *measured* on a 128 GB M5 Max with a forked ds4 [reported: ds4 #1151], against 20–41 fully in memory on a 512 GB machine | [vendor] / [est] |
| *Comparison:* V4 Flash EXL3 3-bit on the Spark | 16/23 on our hard set; code correct on 21/23 | 33 tok/s; ~1 min per task | [ours] |

**Reading:**

- Offload is what lets a near-lossless Q4 fit in 256 GB.
- Reading Engram from the SSD costs about 1% of decode speed [reported: oMLX PR #3574]. Streaming experts from the SSD is the real cost: roughly half the speed of running fully in memory.
- At 10–20 tok/s, one of our tasks (25K tokens in, 1.5K out) takes about 1.5–3 minutes [est], against about 1 minute on the Spark. For overnight briefed tickets that is acceptable, and quality is the point.
- **V4.1 has never been run on our 23 tasks.** The quality case rests on vendor benchmarks plus one independent one, and on the Unsloth KLD tables, which the quant maker reports about its own builds. That is why the trial comes first.

## 6. Splitting one model across machines

**Two questions:** (a) a Mac, the Spark and the SSD together, and (b) the laptop joined to the Studio over Thunderbolt. **Short answer to both: no.** Neither beats one 256 GB Studio running a higher quant with part of the model on its SSD. Neither beats a 512 GB Studio if the model must sit fully in memory. No-one has published V4.1 Flash split across a Mac and a Spark, or across a Studio and a MacBook.

| Tool | Mixes Mac (Metal) and NVIDIA (CUDA) in one model? | Status |
|---|---|---|
| llama.cpp networked mode (RPC) | **Yes, the only proven tool** | Splits the model's layers between machines. The README calls it a "proof-of-concept… fragile and insecure" with no authentication, and every node must run the same build. A Mac and a Spark talk over plain TCP; the RDMA fast path works only between like machines [reported: llama.cpp RPC README] |
| exo | Demo only | The Spark-does-prefill, Mac-does-decode demo used an 8B model and gave a 2.8× end-to-end gain. Today's exo runs on CPU on Linux, so a Spark can't act as a GPU node [reported: EXO blog; exo README] |
| MLX distributed | Apple only, in practice | Ring over TCP, or RDMA over Thunderbolt 5 on macOS 26.2+ [reported: MLX docs via Geerling] |
| vLLM / SGLang | NVIDIA only | This is how two Sparks are joined |

**(a) Mac + Spark + SSD.**

- **Only measured Mac + Spark split:** an M2 Ultra and a Spark over 10GbE using llama.cpp's networked mode. Decode fell from 11.1 to 5.9 tok/s on a 72B model (−47%) and from 91.8 to 52.7 on a 7B (−43%) [reported: kjaiswal benchmarks].
- **Fit:** a 256 GB Studio plus the Spark's 128 GB would hold a Q3_K_M V4.1 (347 GB) with about 37 GB to spare [est]. Expect roughly half the Studio's single-box speed [est]. You also depend on a fragile, unauthenticated service across two machines and two operating systems.
- **The Spark must go back,** so the design would need a replacement GB10 just to make the split work.
- **The 256 GB Studio alone reaches Q4 quality** (KLD 0.009 [vendor]) with SSD offload at about 10–20 tok/s [est]. That is better quality than Q3 for one box's cost, with no network in the loop. **Verdict: no.**
- **If you ever want a GB10 path to V4.1, use two GB10s together, not a Mac + GB10.** Two Sparks running V4.1-Flash-1017 at EXL3 2.9 bpw over their QSFP ports report 73 tok/s for one request and ~2,000 tok/s prefill [reported: tonyd2wild, 2026-10-19]. About A$17,800 for two Founders Editions. The 2.9-bit build is lower quality than a Q4 on the Studio.

**(b) Laptop + Studio over Thunderbolt 5.**

- **It is technically real** with MLX (`mlx.launch` over RDMA) or exo, which needs matching macOS versions and every device cabled to every other.
- **Reported results are on four Studios, not a Studio and a laptop:**
  - Four M3 Ultra Studios ran DeepSeek V3.1 at ~21 tok/s without RDMA and ~32 tok/s with it.
  - Kimi K2 ran at ~30 tok/s.
  - Stability was "prerelease": a non-RDMA run crashed and rebooted both Macs [reported: Geerling Dec 2025; MacGeneration 2026-08-27].
  - **No Studio + MacBook benchmark exists.**
- **What the laptop actually adds:**
  - A 64 GB laptop running macOS, 2–4 Claude seats and test suites has about 0–20 GB spare [est]. Today's 32 GB laptop was saturated by seats alone.
  - A 128 GB laptop dedicated to the job might lend 80–100 GB [est]. That makes about 340–350 GB in total, which is no better than one 256 GB Studio streaming from its SSD.
  - **The laptop travels.** Every trip takes the model down, or strands half of it.
- **Verdict: no.** For more memory than 256 GB, buy the 512 GB Studio (option C) once its price is published.


## 7. Local coding models and how to deploy them

**How to read this:**

- Memory figures are weights only (parameters × bits ÷ 8) [est], unless a quant size is given.
- Benchmarks are mostly vendor-reported and use different harnesses, so **they do not compare across labs**.
- Independent sources: Artificial Analysis (AA, index and Terminal-Bench 4.0), and swebench.com, whose newest data is February 2026.
- Fit: **S256** = Studio 256 GB · **S512** = Studio 512 GB · **128** = a GB10, Strix Halo or 128 GB Mac · **S96** = your existing 96 GB M3 Ultra Studio, about 60–65 GB usable for a model beside the fleet [ours: `2026-10-10_mac-ram-local-coding-models/REPORT.md` §2].

<div class="small">

| Model (release) | Total / active | 4-bit / 8-bit | Licence | Coding scores: [vendor] / [independent] | Runs on | Our measurement |
|---|---|---|---|---|---|---|
| **DeepSeek V4.1-Flash-1017** (17 Oct) | 552B (+196B Engram) / 8–16B | ~298 GB RAM for Q4, Engram on SSD [Unsloth] / — | MIT | DeepSWE 77.0, TB4.0 42.3 / AA index 45, TB4.0 34%; Vals TB2.1 74.5 | S256 (Q2 in memory; Q3/Q4 with offload), S512 (Q4 in memory) | **None. Trial #1** |
| DeepSeek V4-Flash-0731 (our Spark model) | 284B / 13B | 142 / 284 | MIT | DeepSWE 54.4, TB2.1 82.7 / AA 34 | 128 (2–3-bit), S256 (4–8-bit) | **16/23 (3-bit), 18/23 (IQ2_XXS); 43/48 replay** |
| **MiMo-V2.6-Flash** (22 Sep) | 309B / 15B | 155 / 309 | MIT | DeepSWE 67.9, TB2.1 87.6 / AA 38, TB4.0 23% | S256 | **46/48 hosted replay** (easier set). Trial #2 |
| **GLM-5.3-Flash** (Aug) | 320B / 18B | 162–210 [Unsloth] / 320 | MIT | TB2.1 84.3 / AA 42, TB4.0 33% | S256 | **45/48 hosted replay**. Trial #3 |
| Qwen3.8-Flash-Next (Aug) | 180B incl. tables / 6B | 90 / 180 | Qwen Community 1.0 | SWE-Pro 62.5, LCB 91.9 / AA 40, TB4.0 25% | 128, S256 | Did not fit beside the fleet on S96 [ours]. Trial #4 (local only: no zero-retention host) |
| Qwen3.8-27B dense (Aug) | 27B | 13.5 / 27 | Apache-2.0 | SWE-Pro 61.7 / AA 34, TB4.0 6% | everything, including the laptop | None |
| Qwen3-Coder-Next (Feb) | 80B / 3B | 40 / 80 | Apache-2.0 | SWE-V 70.6 / AA 9 | S96, 128 | On disk on S96, unmeasured |
| MiniMax M3.1-Flash (Oct) | ~428B / 23B | 214 / 428 | "minimax-community" (terms not read) | DeepSWE 73.7 / AA 43 | S256 (4-bit, tight) | None. Hold: licence unread, and the weights' status conflicts between sources |
| GLM-5.3 (full) | 753B / 40B | 377 / 753 | GLM-5.3 licence | DeepSWE 66.9 / AA 45, TB4.0 42% | S512 (4-bit) | None |
| Kimi K2.6 / K3 | 1T / 32B; 2.8T / 104B | ~500 GB+ / ~1.5 TB native | Modified MIT; K3 needs a commercial licence above US$20M revenue | K2.6 SWE-V 80.2 / K3 AA 44 | **Does not fit** a single box below 512 GB; K3 not at all | — |
| DeepSeek V4-Pro | 1.6T / 49B | ~893 GB native | MIT | SWE-V 80.6 | Does not fit | — |
| gpt-oss-120b | 117B / 5.1B | ~63 GB (MXFP4) | Apache-2.0 | SWE-V 62.4 / swebench bash-only 26.0, AA 12 | everything | On disk on S96, unmeasured |
| Devstral 2 / Small 2 | 123B / 24B dense | 62 / 12 | Modified MIT / Apache-2.0 | SWE-V 72.2 / 68.0; swebench 53.8 / 56.4 | S96 / laptop | Superseded; Mistral now points to Medium 3.5 |
| Ornith 1.5 122B / 35B | 122B (~10B active) / 35B (3B active) | 61 / 17.5 | MIT | SWE-V 84.5, SWE-Pro 76.9 (122B) / **none** | 128 / S96 | **122B: 12/23** against V4 Flash's 16/23; 35B: 17/20 on our A/B. Vendor claims look inflated (the card's "single 80 GB GPU" claim is impossible at BF16) |

</div>

**Deployment stacks and what they mean for client isolation**

| Stack | Hardware | Batching | Maturity | Isolation note |
|---|---|---|---|---|
| vLLM / SGLang | GB10 (mature); Strix Halo (early ROCm) | Full continuous batching | Production on CUDA | One server per client, or strictly one client per request with prefix cache off or salted |
| EXL3 / ExLlamaV3 | NVIDIA only; it is our Spark's 3-bit build | Paged batching | Young (v1.6.5) | As above |
| llama.cpp / GGUF | All three (CUDA, ROCm/Vulkan, Metal) | `--parallel` slots | Mature; first to support new models. V4.1 merged 25 Oct (PR #31086) | Separate slot caches. Run one client per server process |
| MLX / mlx-lm, oMLX, ds4 | Apple only | oMLX: batching and an SSD KV cache | oMLX young but widely used; ds4 is the V4/V4.1 specialist | **oMLX's SSD KV cache persists prompts on disk:** use a per-client cache directory and wipe it between clients |
| Ollama / LM Studio | All | Limited (Ollama's MLX engine runs one request at a time) | Desktop-grade | Fine for trials, not for the fleet |
| **Hosted, zero data retention** (OpenRouter's ZDR filter; Fireworks, DeepInfra and Cerebras retain nothing by default; Together and Groq only once switched on) | None of ours | Unlimited | Production | Client code leaves our machines. We used this once, on 10 Oct, with your ruling (OpenRouter, pinned to ZDR endpoints). DeepSeek's own API "may train" on data, so never send work there |

**Worth a measured trial on our 23-task hard set** (same `spark-ab/` harness, sampler and checker; one client per task), in order:

1. **V4.1-Flash-1017**: the largest vendor and independent jump, and it fits S256.
2. **MiMo-V2.6-Flash**: best on our earlier hosted replay.
3. **GLM-5.3-Flash**: second-best on that replay.
4. **Qwen3.8-Flash-Next**: the strongest model that fits a 128 GB box. Local only, because there is no zero-retention host.

Steps 1–3 can run hosted under zero retention **before** the HP goes back, for under US$1, if you rule it as on 10 Oct.

**Not worth trialling now:**

- Kimi K2.6/K3 and V4-Pro: they don't fit.
- gpt-oss, Devstral: weak on independent boards.
- Ornith 1.5: already measured below V4 Flash.
- MiniMax M3.1: hold until its licence is read.


## 8. Measured, reported and estimated

**Measured by us (2026-09-22 to 2026-10-26):**

- V4 Flash EXL3 3-bit on the Spark: 33.2 tok/s end-to-end, 37 decode, ~1,030 prefill, 95.4 GiB loaded, one request at a time.
- 16/23 on the hard set. GGUF IQ2_XXS scored 18/23 and IQ1_M 16/23, at about 19.5 tok/s decode (3× slower end-to-end).
- Ornith 122B: 12/23 at 23.6 tok/s.
- Hosted replay: MiMo 46/48, GLM 45/48, V4 Flash 43/48.
- Spark review calibrations: 0 of 3 promotable. Deterministic runner: matched the Claude gates exactly.
- Laptop: load 50–97 with 4–6 seats, suites and Docker.
- Our 96 GB M3 Ultra Studio: about 60–65 GB usable for a model beside the fleet [ours: `2026-10-10_mac-ram-local-coding-models/REPORT.md` §2].

**Reported by others:** all Mac and M5 Ultra speeds, all GB10-against-Strix-Halo comparisons, every V4.1 speed and every quant-quality (KLD) figure.

**Estimated, not measured:**

- V4.1 Q4 with SSD offload at 10–20 tok/s on 256 GB.
- The 512 GB price.
- V4 Flash on Strix Halo.
- A 128 GB laptop hosting a model beside the seats.
- Every split-across-machines speed.
- Whether V4.1 beats 16/23 on our tasks: **the key unknown**.

**What to measure when the Studio arrives, in order:**

1. **V4.1 Flash on the 23-task set**, hosted with zero retention (under US$1) or on the Studio, scored against V4 Flash's 16/23. This decides the second box.
2. Q2 in memory against Q3/Q4 with offload on the Studio: score and time per task.
3. Memory headroom next to Tuesday's seats, read from the wired-memory limit and swap.
4. A shadow review on the Studio's model against Claude tier-2 gates. Is a bigger model enough to promote review? Today's answer is no.
5. MiMo and GLM on the same 23 tasks.

## 9. Sources

<div class="small">

**Our own files (measured; paths under `/Volumes/DevMASTER/WEDNESDAY/`):**

- `0_Brain/reference/2026-10-26_ornith122b-vs-deepseek-spark/report.md` · `…/2026-10-26_deepseek-quant-on-spark/report.md` · `…/2026-10-26_apple-silicon-inference-speedups/report.md` · `…/2026-10-26_deepseek-mac-four-comparisons/report.md`
- `…/2026-09-22_spark-deepseek-v4-flash/HANDOFF.md` and `STUDIO_HANDOUT_2026-09-25.md` · `…/2026-10-10_mac-ram-local-coding-models/REPORT.md` · `…/2026-10-10_mac-hosted-replay-harder/RESULTS.md` · `…/2026-10-08_omlx-flash-next/MODEL_RANKING.md`
- `2_Project_Files/fleet/specs/model-routing.md` (v1.0) · `0_Brain/learnings/2026-10-26_spark-gate-pilot-if-it-works-put-it-into-practice.md` · `0_Brain/learnings/2026-10-22_tuesday-sonnet-default-usage-is-a-guide.md` · `0_Brain/daily/2026-10-26.md`

**Prices (all read 2026-10-26):**

- Apple AU configurator, Mac Studio and MacBook Pro: apple.com/au/shop/buy-mac/mac-studio and …/macbook-pro (M5 Ultra 256 GB 1 TB, M5 Max 128 GB, MBP M5 Pro 64 GB, M5 Max 64/128 GB pages). Specs and bandwidth: apple.com/au/mac-studio/specs, apple.com/au/macbook-pro/specs
- GB10: staticice.com.au searches "DGX Spark", "GX10-GG0013BN", "GX10-GG0032BN", "EDGEXPERT-34SAU", "ATAGB10-9000" · ple.com.au/ai-pc/mini · core-electronics.com.au/nvidia-blackwell-spark.html · aiwarehouse.com.au (DGX Spark FE) · dell.com/en-au … dell-pro-max-fcm1253-micro · mediaform.com.au (GX10; ThinkStation PGX) · clickfrenzy.com.au (Lenovo PGX) · prology.net/au/vgn100-ud11-new · techbuy.com.au/p/560530
- Strix Halo: frame.work/au (Desktop DIY, mainboard) · au.minisforum.com/products/minisforum-ms-s1-max · amazon.com.au GMKtec EVO-X2 (B0F53XL9DP) · staticice "Corsair Workstation 300", "Z2 Mini G1a" · jw.com.au ROG Flow Z13 · bee-link.com GTR9 Pro · frame.work/blog/192gb-framework-desktop-open-for-pre-order
- Context: RBA exchange rates (rba.gov.au/statistics/frequency/exchange-rates.html) · The Register 2026-10-02 (DGX Spark price, 64 GB model) · blogs.nvidia.com/blog/local-ai-dgx-spark-64gb-sync · Tom's Hardware 2026-10-21 (Dell GB10 US prices)

**Performance and comparisons (read 2026-10-26):**

- github.com/ggml-org/llama.cpp/blob/master/benches/dgx-spark/dgx-spark.md · hardware-corner.net/first-dgx-spark-llm-benchmarks · storagereview.com (AMD Ryzen AI Halo vs DGX Spark, Jul 2026) · computingforgeeks.com/dgx-spark-vs-strix-halo-vs-mac-studio (2026-10-13) · community.frame.work/t/dgx-spark-vs-strix-halo-initial-impressions/77055 · petronellatech.com (DGX Spark vs Strix Halo vs Gorgon Halo)
- omlx.ai/benchmarks (66rvj1q7, dn0dqucy, osqlhjud, fpal51r3, 2jbv1kog, vd4ful4d) · bgr.com M5 Ultra review (2026-09-21) · implicator.ai (M5 Ultra prompt processing)
- V4.1 Flash: github.com/antirez/ds4 (README, docs/MODELS.md, docs/PERFORMANCE.md, issues #1151 and #1239) · dwarfstar.sh/docs/deepseek-v4-1-flash · unsloth.ai/docs/models/deepseek-v4.1-flash · github.com/ggml-org/llama.cpp/pull/31086 · omlx PRs #3574 and #4674 · github.com/IngeniousIdiocy/ds4-v41-m3ultra · niklaslenz.com/k/mac256 · huggingface.co/drowzeys (oQ3e MTP card) · elitetestengineering.substack.com · modemguides.com (V4.1 hardware reality check) · benchleader.com · kingy.ai · ukyo.dev/blog/ds41f · huggingface.co/ISTA-DASLab (GSQ card)
- Distributed: github.com/ggml-org/llama.cpp/blob/master/tools/rpc/README.md · github.com/kjaiswal/llama-cpp-distributed-benchmarks · blog.exolabs.net/nvidia-dgx-spark · github.com/exo-explore/exo · forums.developer.nvidia.com (Qwen3-235B multi-node, 2025-12-17) · github.com/tonyd2wild/DeepSeek-V4.1-Flash-vLLM-DGX-Spark · github.com/elsung/dgx-spark-deepseek-v4-flash · github.com/vcruz305/DeepSeek-V4.1-Flash-GGUF-DGX-Spark-recipe · jeffgeerling.com (RDMA over Thunderbolt 5, Dec 2025) · macg.co (M5 Ultra cluster, 2026-08-27) · heise.de/-11085716
- Models: Hugging Face model cards for deepseek-ai V4.1-Flash(-1017), V4-Flash-0731, V4-Pro · zai-org GLM-5.3(-Flash) · XiaomiMiMo MiMo-V2.6-Flash · Qwen Qwen3.8-Flash-Next, Qwen3.8-27B, Qwen3-Coder-Next · MiniMaxAI M3.1-Flash · moonshotai Kimi-K2.6, K3 · openai gpt-oss (arXiv 2508.10925) · mistralai Devstral-2 · ornith-ai Ornith-1.5 · artificialanalysis.ai comparison pages · swebench.com leaderboards.json · aider.chat leaderboards
- Zero-retention policies: openrouter.ai/docs (zdr; provider-logging) · docs.together.ai/docs/zero-data-retention · docs.fireworks.ai (data handling) · deepinfra.com/docs/data · console.groq.com/docs/your-data · support.cerebras.net (data retention)

Prices change daily, and AU GB10 stock is likely to reprice upward after NVIDIA's 2 Oct US increase. Rows marked "index snippet" were not opened live. No discounts are claimed except where the stockist's page showed a sale price.

</div>

