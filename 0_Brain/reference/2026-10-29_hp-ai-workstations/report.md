# HP AI machines for very large local LLMs: research report

**For:** Kam · **Prepared:** 2026-10-29 by a Wednesday research agent · **Rule:** no guessing.

**How to read the sources:** each `[Sn]` tag points to a URL in the Sources section. **Every one of those pages was read on 2026-10-29**, except where the Sources entry says "search snippet only (page not opened)". Each figure is labelled as one of three kinds:
- **vendor spec**,
- **independent measurement**,
- **my arithmetic**, with the working shown.

Where I found nothing, the text says **NOT FOUND** or **UNMEASURED**.

---

## BLUF

- **Buy the HP ZGX Fury G1n AI Station (GB300).** It is the only HP machine that reaches your 512 GB floor and nearly reaches 750 GB.
  - Memory: **748 GB coherent**, made up of **252 GB HBM3e on the GPU (7.1 TB/s)** and **496 GB LPDDR5X on the CPU (396 GB/s)**. HP says the GPU can use the CPU memory coherently [S1][S2].
  - It is listed on hp.com/au-en [S3], but no AU price is published.
  - US reseller CDW lists it at **US$152,955** [S4]. HP Japan lists it from **¥28,490,000 incl. tax** [S5]. Wholesale is unknown.
- **DeepSeek V4.1 Flash fits with room to spare.** The native weights are 510 GB [S10]. On one GB300 station it was measured at **about 90 tok/s for a single stream, and 153 tok/s after tuning** [S20][S21].
- **Kimi K3 (Moonshot's latest, 2.8T parameters) does NOT fit at native precision.**
  - Its weights are 1,561 GB. Even two linked Furies hold only 1,496 GB.
  - One Fury can run it only as a community 1-2-bit quant (466-649 GB). Nobody has published quality or speed figures for that.
  - My bandwidth ceiling for it is about 24-41 tok/s. That is an estimate, not a measurement.
  - If you want a Kimi model at native precision on one box, **Kimi K2.6 or K2.7-Code (1T parameters, native INT4, 595 GB) fits**. Its speed is UNMEASURED. The bandwidth ceiling is about 33 tok/s.
- **Linking Sparks:**
  - HP officially supports linking **two** ZGX Nanos [S7]. NVIDIA's cluster tool supports **up to four**, and four needs a switch [S24].
  - Four Sparks give 512 GB. A community 4-Spark rig runs DeepSeek V4.1 Flash at about **58 tok/s** [S26], roughly a third to two-thirds of the Fury's speed.
  - Kimi K3 at native precision would need about 13 Sparks, far outside what is supported.
- **Not established:** any AU price, any wholesale price, Kimi K3 quality and speed at 1-2-bit, and any Kimi K2.6 benchmark on a GB300 station.

---

## Recommendation

1. **Primary: one HP ZGX Fury G1n, 4 TB storage configuration.**
   - Memory cannot be changed: it is soldered SOCAMM plus on-package HBM. Storage must be chosen at purchase [S2].
   - It needs a **dedicated 200-240 V circuit**. HP says a standard outlet is not suitable and to consult an electrician [S1].
   - The power supply is 1600 W Titanium [S2]. My arithmetic: 1600 W ÷ 230 V ≈ 7 A at full load.
   - It weighs **41 kg or more** and is liquid-cooled. It can stand as a tower or go in a 5U rack [S1][S2].
2. **Model plan on that box:**
   - DeepSeek V4.1 Flash (the -1017 checkpoint) at native FP8/FP4 is the daily driver. It fits, and vLLM publishes a recipe for "DGX Station (GB300)" [S20].
   - For Kimi, use **K2.6 or K2.7-Code at native INT4**, which fits.
   - Treat Kimi K3 as an experiment on 1-2-bit quants until someone publishes quality numbers.
3. **Upgrade path, if native Kimi K3 ever matters:**
   - HP supports linking **two** Furies [S2]. That gives 1,496 GB, still about 65 GB short of K3's native 1,561 GB before any KV cache (my arithmetic).
   - Two Furies would run K3 only at the UD-Q2_K_XL quant (861 GB) [S13].
   - Native K3 is a rack-class job. The vLLM recipe says "At least 8x GB300" [S22].
4. **Alternative, not recommended for your goal: a 4-Spark cluster.**
   - You own one Spark, so this means three more ZGX Nanos plus a switch, for 512 GB nominal.
   - It runs V4.1 Flash, but at roughly a third to two-thirds of the Fury's single-stream speed.
   - It cannot reach 750 GB within NVIDIA's supported setup. See the Spark-linking section.
5. **Do not buy a Z8 Fury G6i for this.**
   - Its GPU memory tops out at 384 GB: four 96 GB cards linked over PCIe, with no NVLink [S16]. That is below your 512 GB floor.
   - Its 2 TB of DDR5 is CPU memory, which is far slower for model weights.

---

## The HP range

Machines are listed by memory a model can use. Rows marked "below floor" are included for scale only.

| Machine | AU listed? | US listed? | Model-usable memory (and how it splits) | GPU | Memory bandwidth | List price AU / US | Source |
|---|---|---|---|---|---|---|---|
| **HP ZGX Fury G1n AI Station** | **Yes**, product page on hp.com/au-en [S3]. **No AU price and no AU reseller listing FOUND** | Yes [S1] | **748 GB coherent**: 252 GB HBM3e on the GPU plus 496 GB LPDDR5X SOCAMM on the CPU (4×128 GB). HP calls it "Coherent memory". HP case-study quote: "the Grace memory pool absorbs its expert overflow over a coherent link" [S1][S2] | 1× NVIDIA Blackwell Ultra (GB300). An optional RTX PRO 4000 or 2000 is for display only [S2] | HBM 7.1 TB/s. LPDDR5X 396 GB/s [S2] | AU: **NOT FOUND**. US: **US$152,955.00** at CDW (E70LKUT#ABA, 4 TB, "Sign in for your price") [S4]. JP: **¥28,490,000~ incl. tax** from HP Japan [S5]. B&H (US$132,000) and buyzero (€130,000) are search snippets only, not opened [S6] | [S1][S2][S3] |
| HP ZGX Fury, two units linked | As above | As above | 2 × 748 = **1,496 GB** across two boxes (my arithmetic). HP: "supports linking two ZGX Fury devices" via ConnectX-8 with 2×400 Gb QSFP112 [S2] | 2× GB300 | The link measured about 98 GB/s (NCCL) over two 400G DACs [S19] | 2× the above | [S2][S19] |
| HP Z8 Fury G6i (tower) | Yes, page on hp.com/au-en [S15]. AU price **NOT FOUND** | Yes [S15] | **384 GB GPU**: up to 4× RTX PRO 6000 Blackwell Max-Q at 96 GB each. Each card has its own memory and they talk over PCIe: "Neither platform supports NVLink" [S15][S16]. Plus up to **2 TB DDR5-6400** CPU RAM (16 DIMMs, 8 channels) [S16b] | Up to 4× RTX PRO 6000 Max-Q (300 W, 96 GB GDDR7) [S17] | 1,792 GB/s per GPU [S17]. DDR5: 8 channels × 6400 MT/s × 8 B = **409.6 GB/s theoretical** (my arithmetic) | US: "starts at roughly $7900". A two-GPU review unit is given as both "$52,139" and "$74,878" in the same review [S16]. Four-GPU price **NOT FOUND** | [S15][S16][S16b] |
| HP Z6 G5 (below floor) | Yes, page on hp.com/au-en | Yes | Up to **288 GB GPU** (3× RTX PRO 6000 Max-Q), plus up to 1 TB DDR5 [S18] | Up to 3× RTX PRO 6000 Max-Q | 1,792 GB/s per GPU [S17] | NOT FOUND | [S18] |
| HP Z4 Rack G5, your link (below floor) | Yes, page on hp.com/au-en | Yes | Up to **96 GB GPU** (1× RTX PRO 6000 Max-Q, 300 W) or 2× RTX 4000 Ada. Up to **256 GB DDR5 ECC**. 1U, with 2× 675 W PSU bays [S14] | 1× RTX PRO 6000 Max-Q | 1,792 GB/s [S17] | NOT FOUND | [S14] |
| HP ZGX Nano G1n, "the Spark" (below floor) | Yes, HP AU page [S7]. Techbuy AU: **A$13,929.30 incl. GST** (RRP A$18,229.20), 4 TB, D0YU0PT, on backorder [S8]. The HP AU shop URL for D0YU1PT redirected to the HP homepage today | Yes [S7]. US prices come from search snippets only (CDW US$6,799 / US$7,046.99; STH US$7,399) and are not verified | **128 GB** LPDDR5x unified [S9] | GB10 | **273 GB/s** [S9] | See left | [S7][S8][S9] |
| HP Z2 Mini G1a, Strix Halo (below floor) | Yes, page on hp.com/au-en | Yes | **128 GB** unified, with up to **96 GB** assignable to the GPU [S23] | Radeon 8060S (Ryzen AI Max+ PRO 395) | NOT FOUND in the HP datasheet | NOT FOUND | [S23] |

**Scope check.** HP's "AI stations" pages (US and AU) list only two products: the ZGX Fury and the ZGX Nano [S1][S7]. I found no other HP machine whose GPU-usable memory reaches 512 GB.

**Note on the 784 GB figure.** Press coverage of the NVIDIA DGX Station and the Dell GB300 quotes **784 GB**, with 288 GB of HBM3e. That comes from a TechRadar search snippet I did not open [S6]. HP's own datasheet says **748 GB, with 252 GB HBM3e** [S2]. Use HP's figure for the HP machine.

---

## The models

| Model | Total params | Active params | Context | Native weights on disk | Other published sizes | Source |
|---|---|---|---|---|---|---|
| **DeepSeek V4.1 Flash** (released 2026-10-16), plus the **-1017** update (2026-10-17) | Model card: "552B backbone parameters" plus "Engram conditional memory (196B parameters)". HF safetensors metadata: 763.2B total, which includes vision and draft layers. I have not verified how HF counts packed FP4 | "8B parameters per token during prefill and 16B during decode". 384 routed experts plus 1 shared, 6 active | 1M tokens (max_position_embeddings 1,048,576) | **510.3 GB**, FP8 with FP4 experts (config: `expert_dtype: fp4`). Same size for -1017 | NVIDIA NVFP4: 429.0 GB. Unsloth GGUF (-1017): UD-Q8_K_XL 508.4 GB, UD-Q4_K_XL 500.7, UD-Q3_K_XL 485.1, UD-IQ3_XXS 394.7, UD-Q2_K_XL 334.8, UD-IQ1_S 233.0. antirez Q2: 365.7 GB | [S10][S11][S12][S13] |
| **KV cache for V4.1 Flash** | The card gives "890 bytes per token" (FP4 main KV) | | | | 1M tokens ≈ **0.89 GB**. 128K ≈ 0.12 GB per sequence (my arithmetic: 890 B × tokens) | [S10] |
| **Kimi K3** (Moonshot's latest; repo updated 2026-09-02, the newest moonshotai model on HF today) | **2.8T** (HF metadata: 2,779.9B) | **104B**. 16 of 896 experts, plus 2 shared. 93 layers (69 KDA + 24 gated MLA) | 1,048,576 | **1,560.9 GB**, native MXFP4 weights (quantisation-aware trained) | NVIDIA NVFP4: 1,609.9 GB. Unsloth GGUF: UD-Q8_K_XL 1,561.2, UD-Q4_K_XL 1,508.7, UD-Q2_K_XL 861.3, UD-IQ2_XXS 711.1, UD-IQ1_M 648.9, UD-IQ1_S 594.0, UD-TQ2_0 551.5, UD-TQ1_0 508.9, UD-Q1_0 466.4 GB. Pruned "REAP" variants (441-479 GB) remove experts, so they are a different model | [S11][S13][S30] |
| **KV cache for Kimi K3** | My arithmetic from the config: 24 MLA layers × (512 + 64) × 2 bytes (BF16) = **27,648 B/token**. That is 3.6 GB at 128K, 7.2 GB at 256K and 29 GB at 1M. The KDA layers add a fixed state per sequence. I estimate it at 69 × 96 heads × 128 × 128 × 2 B ≈ **0.22 GB per sequence**, assuming a 128×128 BF16 state per head (state dtype not verified) | | | | | [S30] (config) |
| Kimi K2.6 / K2.7-Code (the previous Kimi generation) | 1T (HF: 1,026.9B) | 32B | 256K | **595.2 GB**, native INT4 | KV (my arithmetic): 61 layers × 576 × 2 B = 70,272 B/token. That is 9.2 GB at 128K and 18.4 GB at 256K | [S11][S31] |
| DeepSeek V4 Flash (what the Spark runs today) | 284B | 13B | 1M | **159.6 GB** native (HF API), "FP4 + FP8 Mixed" | 159.6 GB is more than one Spark's 128 GB, so your Spark must be running a community quant. Which one is **NOT ESTABLISHED**. A guide reports Q2-class files of about 81-98 GB for one Spark [S27] | [S11][S12] |

**How I determined "latest".** I sorted the Hugging Face API by lastModified for the `deepseek-ai` and `moonshotai` organisations today [S11].
- DeepSeek: the newest are `DeepSeek-V4.1-Flash-1017` (2026-10-17) and `DeepSeek-V4.1-Flash` (2026-10-16). So "V4.1 Flash" exists under exactly that name.
- Moonshot: the newest is `Kimi-K3` (2026-09-02), then `Kimi-K2.7-Code` (2026-06-15) and `Kimi-K2.6` (2026-05-19).

---

## Will it drive the model?

**Assumptions:**
- One user and 128K context, unless stated otherwise.
- Speed estimates are **bandwidth-bound ceilings, not benchmarks**: decode tok/s is at most memory bandwidth ÷ bytes read per token. Real speed is lower because of compute, kernel and routing overhead, and higher where speculative decoding helps.
- When a model is split between HBM and LPDDR, I assume about **220 GB of weights stay in HBM**. That is 252 GB of HBM minus the KV cache, activations and CUDA context, and it is my own assumption.

### 1. HP ZGX Fury (748 GB = 252 GB HBM + 496 GB LPDDR)

**DeepSeek V4.1 Flash at native precision: FITS.**
- Fit: 510.3 GB of weights plus 0.12 GB of KV at 128K (0.89 GB at 1M) ≈ 511 GB, which is under 748 GB.
- The published vLLM recipe for "DGX Station (GB300)" [S20]:
  - Runs on one GPU (TP1). It keeps the "Engram tables (189 GiB) and 60 GiB of routed experts in pinned host memory" using `--cpu-offload-gb 60`.
  - Reports "~430 of the 494 GiB Grace pool is in use".
  - Says the KV pool "holds about 3.09M tokens at full 1M context".
- **Measured, vLLM recipe** (`vllm-openai:nightly-dee37d89`): 90.5 tok/s for 1 stream, and about 416-423 tok/s aggregate at 16 streams [S20].
- **Measured, NVIDIA forum** (one DGX Station GB300, update of 2026-09-18): single-stream prose "89.3 → 153.1 tok/s" after pinning experts, and 809 tok/s at 16 streams [S21].
- **Measured, two linked GB300 stations** (an HP ZGX Fury plus an ASUS, with prefill and decode on separate boxes): 441 tok/s for 1 stream and 5,248 tok/s at 256 streams, on a 512-in/512-out workload [S19].
- **My ceiling estimate:**
  - Bytes per parameter: 510.3 GB ÷ 763.2B ≈ 0.67 B. At 16B active parameters, that is about 10.7 GB read per token.
  - If everything sat in HBM: 7,100 GB/s ÷ 10.7 GB ≈ 660 tok/s.
  - With 15 of the 40 expert layers on LPDDR (the forum setup [S21]), and assuming routed experts are about 80% of the bytes read: about 110 tok/s.
  - The measured 90-153 tok/s (the 153 includes speculative decoding) is consistent with that.

**Kimi K3 at native precision (1,560.9 GB): DOES NOT FIT** (1,561 GB > 748 GB).

**Kimi K3 as a community quant on one Fury:**
- Which quants fit:
  - UD-Q1_0 (466 GB) fits, with about 280 GB left over.
  - UD-IQ1_M (649 GB) fits, with about 99 GB left for the OS, KV cache and runtime.
  - UD-IQ2_XXS (711 GB) leaves only about 37 GB. I treat that as not practical.
- My ceilings:
  - IQ1_M averages 648.9 GB × 8 ÷ 2.78T ≈ 1.87 bits per parameter. 104B × 1.87 / 8 ≈ 24.3 GB read per token. With 34% of that in HBM: 0.34 × 24.3/7,100 + 0.66 × 24.3/396 ≈ 41.7 ms, so **about 24 tok/s at most**.
  - Q1_0 (1.34 bits, 17.4 GB per token, 47% in HBM): **about 41 tok/s at most**.
- **Quality at 1-2 bits: UNMEASURED.** I found no published eval. **Speed on a GB300: UNMEASURED.**
- Software:
  - Unsloth says "To run Kimi K3, use our llama.cpp PR fork" [S13]. It does not run on standard llama.cpp.
  - The vLLM K3 recipe's minimum is "At least 8x GB300". It documents no path for a single station [S22].
- The only published run of a 1-bit K3 on a small box is **0.70 tok/s**. That was one DGX Spark streaming experts from SSD (UD-IQ1_S, 634.6 GB) [S28]. The Spark is far smaller than a Fury, so this does not predict Fury speed.

**Kimi K2.6 / K2.7-Code at native INT4 (595.2 GB): FITS.**
- Fit: 595.2 GB plus 9.2 GB of KV at 128K (18.4 GB at 256K) ≈ 614 GB, which is under 748 GB.
- My ceiling: 595.2 ÷ 1,026.9 ≈ 0.58 B per parameter. 32B × 0.58 ≈ 18.5 GB per token. With 37% in HBM, that is about 30 ms per token, so **about 33 tok/s at most**.
- **Measured on a GB300 station: NOT FOUND.**
- vLLM can offload weights to CPU memory on this platform; the V4.1 recipe uses the same `--cpu-offload-gb` mechanism [S20]. A K2.6-specific DGX Station recipe was NOT FOUND.

### 2. HP Z8 Fury G6i (4 × 96 GB = 384 GB of GPU memory on separate cards over PCIe, plus up to 2 TB DDR5)

- **DeepSeek V4.1 Flash at native precision (510 GB): does not fit in GPU memory.**
  - About 126 GB or more would sit in DDR5 and be read over PCIe.
  - I did not source the PCIe link rate today. It is a small fraction of the GDDR7's 1,792 GB/s.
- **V4.1 Flash quantised to fit in GPU memory only:**
  - UD-Q2_K_XL (334.8 GB) fits, leaving about 49 GB for KV and runtime. NVFP4 (429 GB) and the IQ3 quants (395 GB and up) do not fit.
  - Ceiling: four GPUs splitting the work give about 4 × 1,792 = 7,168 GB/s combined. The cost of PCIe traffic between the cards is UNMEASURED.
  - A benchmark of this model on this machine: **NOT FOUND**.
- **Kimi K3: no** (1,561 GB).
- **Kimi K2.6: does not fit in GPU memory** (595 GB > 384 GB). It would need heavy DDR5 offload, and that speed is UNMEASURED.

### 3. Four linked ZGX Nanos ("Sparks")

Covered in the next section.

---

## Linking Sparks (HP ZGX Nano): how many, and is it worth it?

**(1) What is officially supported**

- **HP** [S7][S9]:
  - Quote: "connecting two HP ZGX Nano systems together", for models of "up to 405 billion parameters".
  - It "Requires compatible QSFP cable. Sold separately".
  - The Nano has **2 QSFP ports at 200 Gbps** and a **ConnectX-7 200 GbE** controller.
  - **HP documents two units, not more.**
- **NVIDIA**, from the Sync Cluster Assistant docs for DGX Spark [S24]:
  - Its tool "supports two to a maximum of four DGX Spark devices".
  - **Two or three units can be cabled directly** (three as a ring of three cables). **Four units require a switch.** You cannot mix the two layouts.
  - Use "one cable per link". The supported cables are QSFP112 400 GbE DACs: Amphenol NJAAKK-N911 and Luxshare LMTQF022-SD-R.
  - The expected negotiated speed is **200 Gbit/s per link**.
  - Clusters outside two to four units "must be configured manually".
  - NVIDIA also publishes a "Connect Multiple DGX Spark through a Switch" playbook [S25]. I found it but did not read it in full.
- **Not established:** whether HP supports NVIDIA's Sync tool, or the switch layout, on the HP-branded ZGX Nano. It is the same GB10 chip, but HP's own pages say two.
- **NVIDIA forum moderator** (NVES, 2025-12-18): a four-box cluster is not one machine with "combined GPU memory" transparently. You run a distributed job with MPI or NCCL frameworks [S29].

**(2) More than two in practice (community setups, not official)**

- **Four Sparks in a ring with no switch.** Patrick Moorhead's rig, reported by Wccftech on 2026-10-05 [S26]:
  - Model: DeepSeek V4.1 Flash, "memory footprint is 476 GB".
  - Single request: "~58 tok/s prose, ~96 tok/s code". Peak: "494 tok/s (code, 32 concurrent requests)".
  - The inference engine and quant are not named.
  - A four-unit ring is outside NVIDIA's documented support, which requires a switch for four [S24].
- **Two Sparks.** Flowtivity, 2026-10-21 [S32]:
  - Model: DeepSeek V4.1 Flash, split across both Sparks (TP=2), at 131K context.
  - Result: **37.7 tok/s decode** (35.1 end to end), with about 113 GB used per unit.
  - The weight quant is not stated.
- **Eight Sparks on two switches.** A reseller blog says it runs this setup and calls it outside NVIDIA's support. I saw only a search snippet and did not open the page [S33].

**(3) Memory and speed for N units**

My arithmetic, from 128 GB per unit [S9] and about 121 GiB visible per unit [S28].

| Units | Nominal memory | Support status | DeepSeek V4.1 Flash (510 GB native) | Kimi K3 (1,561 GB native) |
|---|---|---|---|---|
| 1 (the one you own) | 128 GB | — | No. Only aggressive quants exist, and even UD-IQ1_S at 233 GB does not fit | No |
| 2 | 256 GB | HP and NVIDIA | Quant only. UD-IQ2_XXS (300.5 GB) does NOT fit; UD-IQ1_S (233 GB) does. Measured 37.7 tok/s with an unstated quant [S32] | No |
| 3 | 384 GB | NVIDIA (direct ring) | Quant only (UD-Q2_K_XL, 334.8 GB) | No |
| 4 | 512 GB | NVIDIA (switch required) | The community ran it at a 476 GB footprint: **about 58 tok/s prose** [S26]. The native 510 GB would leave almost nothing for the OS and KV | Only UD-Q1_0 (466 GB) or the pruned REAP versions. UNMEASURED |
| 13 | 1,664 GB | Unsupported | — | Bare minimum for native: 1,560.9 GB ÷ 129.9 GB (121 GiB) ≈ 12.0, so 13 units with no headroom |

- **The links between units are the bottleneck.** Each link runs at 200 Gb/s, which is **25 GB/s** (my arithmetic). Compare:
  - each Spark's own memory: **273 GB/s** [S9];
  - the link between two Furies: about **98 GB/s** measured [S19];
  - the HBM inside one Fury: **7,100 GB/s** [S2].
- **Scaling seen in practice:** going from two to four Sparks took V4.1 Flash from 37.7 to about 58 tok/s. That is roughly 1.5× for twice the hardware. These are two different community setups, so the comparison is loose [S26][S32].
- **Kimi K3 at UD-Q1_0 on four Sparks** reads about 17.4 GB per token.
  - If the work split perfectly across all four (tensor parallel), the ceiling would be about 63 tok/s: 4 × 273 GB/s ÷ 17.4 GB.
  - If the units process the model in sequence (pipeline parallel), it is about 16 tok/s: 273 ÷ 17.4.
  - Real speed will be lower. UNMEASURED.

**(4) Spark cluster vs one Fury**

- **Cost:**
  - Three more Nanos at Techbuy's price: 3 × A$13,929.30 = **A$41,788** incl. GST, plus a 200/400G switch and cables (switch price NOT FOUND).
  - Four new Nanos would be A$55,717.
  - One Fury at CDW is US$152,955. That is a US price; the AU price was NOT FOUND.
- **Fit:**
  - Four Sparks top out at 512 GB, which is your floor with no headroom. The Fury gives 748 GB, close to your ideal.
  - Neither setup runs Kimi K3 at native precision.
- **Speed on V4.1 Flash, one user:** four Sparks manage about 58 tok/s (community) against the Fury's 90-153 tok/s (vLLM recipe and forum). The Fury is also the only option with a published vendor recipe [S20].
- **Verdict:**
  - Sparks are a cheaper way to reach the 512 GB floor, at lower speed. Beyond two units, the wiring is not something HP documents.
  - The Fury is the one that actually drives these models well.

---

## Configuration for the recommended machine (ZGX Fury G1n)

**What you choose and what is fixed** [S2]:
- **Memory:** fixed at 496 GB LPDDR5X-6400 SOCAMM plus 252 GB HBM3e, for 748 GB coherent. There is nothing to choose.
- **Storage:** 2 TB or 4 TB, chosen at purchase.
  - The OS sits on two Gen5 M.2 drives mirrored (RAID 1). Data sits on two Gen6 M.2 drives striped (RAID 0).
  - Pick **4 TB**: V4.1 Flash is 510 GB and K2.6 is 595 GB.
  - Usable data capacity is NOT FOUND. HP says "Available capacity will vary by configuration". If the 4 TB is the total across all four drives and the data pair is about half of it, that would be about 2 TB for models (my arithmetic).
- **Optional display GPU:** RTX PRO 4000 (24 GB) or RTX PRO 2000 (16 GB). It handles video output only, so the GB300 is left free for models [S2]. It is not needed for model capacity.
- **Networking:** ConnectX-8 with two 400 Gb QSFP112 ports, needed only if you later link a second Fury (cable sold separately). Plus 10 GbE RJ-45 [S2].
- **Software:**
  - Ships with Ubuntu 24.04 LTS, NVIDIA AI Developer Tools and HP Z Runtime. It is certified for Red Hat Enterprise Linux.
  - Windows is "coming soon"; HP Japan says December 2026 or later [S1][S5].
- **Inference engines:**
  - **vLLM** has a DGX Station (GB300) recipe for V4.1 Flash [S20].
  - Moonshot recommends **vLLM, SGLang or TokenSpeed** for K3 [S30], but I found no recipe for a single station.
  - llama.cpp support for K3 is only in a **fork** [S13].
  - TensorRT-LLM support for these models: **NOT CHECKED**.
- **Site needs:** dedicated 200-240 V circuit, 1600 W power supply, 41 kg or more, liquid-cooled, air drawn in at the front and out the back [S1][S2].

**What you gain or lose against the alternatives:**
- **One superchip (Fury) vs several separate GPUs (Z8):**
  - The Fury puts 748 GB behind one GPU, with no splitting the model across cards and no PCIe hops.
  - The cost is that only 252 GB is fast HBM. Anything beyond that is read from LPDDR at 396 GB/s, which is what limits the Kimi estimates above.
  - The Z8 has 384 GB of fast GDDR7 spread over four cards with no NVLink. That is less capacity, and traffic between the cards goes over PCIe [S16].
- **One Fury vs a Spark cluster:**
  - The Fury has more memory, measured single-stream speed on V4.1 Flash about 1.5-2.6× higher, and it is one officially supported box.
  - The Spark cluster is cheaper, but needs a switch beyond three units, and HP officially supports only two.
- **Two Furies:**
  - 1,496 GB, officially supported as a pair.
  - Measured at 441 tok/s single-stream on V4.1 Flash with prefill and decode on separate boxes [S19].
  - Still short of native Kimi K3.

---

## What was NOT established

- **Australian prices** for the ZGX Fury, Z8 Fury G6i, Z6, Z4 Rack and Z2 Mini. The HP AU pages exist but show no price, and I found no AU reseller listing for the Fury.
- **Any wholesale price.**
- **HP's own AU store price for the ZGX Nano.** The URL redirected today. A search snippet showed A$6,329, which I could **not verify**.
- **The B&H (US$132,000) and buyzero (€130,000) prices.** These are search snippets only; the pages returned errors 403 and 429.
- **Kimi K3 quality at 1-2-bit quants**, and **K3 speed on any GB300 station**: UNMEASURED.
- **Kimi K2.6 / K2.7-Code speed on a GB300 station**: UNMEASURED.
- **Any Z8 Fury G6i result for a 500B+ mixture-of-experts model**: NOT FOUND.
- **Which quant your Spark runs** for DeepSeek V4 Flash. The native 159.6 GB does not fit in 128 GB, so it must be a quant.
- **HP support for more than two linked ZGX Nanos**, and whether NVIDIA's Sync cluster tool is supported on HP units.
- **TensorRT-LLM support** for V4.1 Flash or K3 on GB300: not checked.
- **Usable data-drive capacity** on the Fury's 4 TB configuration.
- **K3's KDA state size per sequence.** My 0.22 GB figure is an estimate based on an assumed state shape.
- **PCIe link rates.** I did not source them today and used no numeric PCIe figure.
- **All bandwidth estimates are ceilings, not benchmarks.** The 220 GB "stays in HBM" figure is my assumption.

---

## Sources

All pages below were read on 2026-10-29 unless marked "search snippet only".

- [S1] HP ZGX Fury AI station (US): https://www.hp.com/us-en/workstations/ai-stations/zgx-fury-ai-station.html
- [S2] HP ZGX Fury G1n datasheet (August 2026): https://h20195.www2.hp.com/v2/GetPDF.aspx/c09307810
- [S3] HP ZGX Fury AI station (Australia): https://www.hp.com/au-en/workstations/ai-stations/zgx-fury-ai-station.html
- [S4] CDW, HP ZGX Fury G1n E70LKUT#ABA: https://www.cdw.com/product/hp-zgx-fury-g1n-workstation-arm-neoverse-v2-496-gb-4-tb-ssd-tower/9247261
- [S5] HP Japan newsroom, 2026-10-26 (price ¥28,490,000~ incl. tax; Windows from December 2026 or later): https://jp.ext.hp.com/info/newsroom/2026/20261026/
- [S6] Search snippets only (pages blocked or not opened):
  - https://www.bhphotovideo.com/c/product/1998077-REG/hp_e70lkut_aba_zgx_fury_g1n_ai.html
  - https://buyzero.de/en/products/hp-zgx-fury-g1n-ai-station-nvidia-dgx-station-gb300
  - TechRadar, 784 GB figure: https://www.techradar.com/pro/hp-and-dells-latest-nvidia-powered-pcs-are-likely-to-be-some-of-the-most-expensive-workstations-ever-launched
- [S7] HP ZGX Nano AI Station and AI stations index:
  - US: https://www.hp.com/us-en/workstations/zgx-nano-ai-station.html
  - AU: https://www.hp.com/au-en/workstations/zgx-nano-ai-station.html
  - Index (US): https://www.hp.com/us-en/workstations/ai-stations.html
  - Index (AU): https://www.hp.com/au-en/workstations/ai-stations.html
- [S8] Techbuy AU, ZGX Nano D0YU0PT: https://www.techbuy.com.au/p/562851/SYSTEMS_IBM_LENOVO_SYSTEMS/HP/D0YU0PT.asp
- [S9] HP ZGX Nano datasheet: https://h20195.www2.hp.com/v2/GetPDF.aspx/c09208797
- [S10] DeepSeek-V4.1-Flash model card and config:
  - https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash
  - -1017: https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017
- [S11] Hugging Face API (file sizes, parameter metadata, organisation listings):
  - https://huggingface.co/api/models/deepseek-ai/DeepSeek-V4.1-Flash?blobs=true
  - https://huggingface.co/api/models/moonshotai/Kimi-K3?blobs=true
  - https://huggingface.co/api/models/moonshotai/Kimi-K2.6?blobs=true
  - https://huggingface.co/api/models/moonshotai/Kimi-K2.7-Code?blobs=true
  - https://huggingface.co/api/models/deepseek-ai/DeepSeek-V4-Flash?blobs=true
  - https://huggingface.co/api/models?author=deepseek-ai&sort=lastModified
  - https://huggingface.co/api/models?author=moonshotai&sort=lastModified
- [S12] Other DeepSeek pages:
  - DeepSeek-V4-Flash model card: https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash
  - NVIDIA NVFP4: https://huggingface.co/nvidia/DeepSeek-V4.1-Flash-NVFP4
  - antirez GGUF: https://huggingface.co/antirez/deepseek-v4.1-flash-gguf
- [S13] Unsloth GGUFs (sizes summed via the HF API):
  - https://huggingface.co/unsloth/Kimi-K3-GGUF
  - https://huggingface.co/unsloth/DeepSeek-V4.1-Flash-1017-GGUF
- [S14] HP Z4 Rack (your link) and AU page:
  - https://www.hp.com/us-en/workstations/z4-rack.html
  - https://www.hp.com/au-en/workstations/z4-rack.html
- [S15] HP Z8 Fury G6i:
  - US: https://www.hp.com/us-en/workstations/z8-fury.html
  - AU: https://www.hp.com/au-en/workstations/z8-fury.html
- [S16] StorageReview, HP Z8 Fury G6i review (2026-06-23): https://www.storagereview.com/review/hp-z8-fury-g6i-review-one-xeon-up-to-four-blackwell-gpus
- [S16b] HP Z8 Fury G6i datasheet: https://h20195.www2.hp.com/v2/GetPDF.aspx/c09238030
- [S17] NVIDIA RTX PRO 6000 Blackwell Max-Q: https://www.nvidia.com/en-us/products/workstations/professional-desktop-gpus/rtx-pro-6000-max-q/
- [S18] HP Z6 G5:
  - US: https://www.hp.com/us-en/workstations/z6.html
  - AU: https://www.hp.com/au-en/workstations/z6.html
- [S19] StorageReview, two GB300 stations (HP ZGX Fury + ASUS), 2026-10-05: https://www.storagereview.com/review/dgx-station-gb300-cluster-two-towers-two-400g-dacs
- [S20] vLLM recipe, DeepSeek-V4.1-Flash (DGX Station GB300 entry; page updated 2026-10-25): https://recipes.vllm.ai/deepseek-ai/DeepSeek-V4.1-Flash
- [S21] NVIDIA Developer Forum, "Deepseek 4.1 Flash - DGX Station" (posts of 2026-09-10 and 2026-09-18): https://forums.developer.nvidia.com/t/deepseek-4-1-flash/382896
- [S22] vLLM recipe, Kimi-K3 (updated 2026-10-26): https://recipes.vllm.ai/moonshotai/Kimi-K3
- [S23] HP Z2 Mini G1a:
  - Page: https://www.hp.com/us-en/workstations/z2-mini-a.html
  - Datasheet: https://h20195.www2.hp.com/v2/GetPDF.aspx/c09086887
- [S24] NVIDIA Sync, Cluster Assistant: https://docs.nvidia.com/sync/0.117.3/cluster-assistant.html
- [S25] NVIDIA playbook, multiple Sparks through a switch (found via search, not read in full): https://build.nvidia.com/spark/multi-sparks-through-switch/multi-sparks
- [S26] Wccftech, four DGX Sparks running DeepSeek V4.1 Flash (2026-10-05): https://wccftech.com/the-552b-deepseek-v4-1-flash-model-offers-a-peak-output-of-494-tokens-second-when-powered-by-an-at-home-rig-spanning-4x-nvidia-dgx-spark-units/
- [S27] Kingy.ai, DeepSeek V4 Flash and Kimi K3 on DGX Spark: https://kingy.ai/ai/ai-guides/deepseek-v4-flash-kimi-k3-dgx-spark/
- [S28] Classmethod, Kimi K3 on one DGX Spark via SSD expert streaming (2026-08-06): https://dev.classmethod.jp/en/articles/dgx-spark-pulsar-ssd-expert-streaming/
- [S29] NVIDIA forum, clustering four DGX Sparks: https://forums.developer.nvidia.com/t/what-is-the-best-practices-for-clustering-4x-dgx-spark-units-into-a-single-unified-system/355131
- [S30] Kimi-K3 model card and config: https://huggingface.co/moonshotai/Kimi-K3
- [S31] Kimi-K2.6 and K2.7-Code model cards and config:
  - https://huggingface.co/moonshotai/Kimi-K2.6
  - https://huggingface.co/moonshotai/Kimi-K2.7-Code
- [S32] Flowtivity, DeepSeek V4.1 Flash on two DGX Sparks (2026-10-21): https://flowtivity.ai/blog/deepseek-v41-flash-dual-dgx-spark-agent/
- [S33] Search snippet only: https://petronellatech.com/blog/4-dgx-sparks-switch-or-switchless-ring/
