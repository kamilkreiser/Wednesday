---
date: 2026-11-01
type: reference
source: research sub-agent commissioned by Wednesday on Kam's signed mail of 2026-11-01 09:52 AEDT
status: live
---

# Video review: MacBook M5 Max + Mac Studio M5 Ultra running a 432 GB model (2026-11-01)

**Tags.** [video-desc] = the video's own YouTube description, read in full. [HF] = model card. [video] would mean heard in the video itself: **I had NO transcript and did not watch the video**, so nothing here is tagged [video]. [independent: URL] = another source. [arith] = arithmetic. UNMEASURED = no source.

## BLUF
1. The video (AIex The AI Workbench, 30 Oct 2026, 12 min) pairs a Studio M5 Ultra 256 GB with a MacBook Pro M5 Max 128 GB over **one Thunderbolt 5 cable (RDMA, MLX distributed, JACCL backend)** and runs DeepSeek V4.1 Flash (432 GB, mixed 4.5 bpw) at **about 55 tok/s generation** [video-desc]. **No prompt-processing (prefill) speed and no context length are given anywhere I could read**, and prefill is what matters for our ~25K-token prompts.
2. **For Kam: a 32 GB or 64 GB MacBook adds little.** It adds only 32 or 64 GB to a 256 GB Studio, so it unlocks no new model class; the video's big model needed the 128 GB laptop. The same creator measured the pair as *slower* than the Studio alone until two fixes were applied, and even fixed gave only about +15% on a small model [video-desc]. Don't buy a laptop for this.
3. **One thing does not add up and is unexplained:** 256 + 128 = 384 GB of memory, yet the model is 432 GB (402 GiB). I could not find how it fits (SSD streaming of the Engram tables is my guess, unverified). Treat the "432 GB across two Macs" headline as unverified until the video or scripts say how.
4. The video's two required fixes (a fast-sync env var, bandwidth-weighted split) are worth reusing when the Studio arrives and we try any pair.

## What the video shows (tagged claims)

**Provenance.** Title "I Joined Macbook M5 Max and Studio M5 Ultra to Run a 432 GB Model"; channel AIex The AI Workbench; published 2026-10-30; length 734 s [oEmbed + page metadata]. **Transcript: not retrievable** (YouTube caption URL returned empty; the page fetch returned only the title). Everything below comes from the description text (which includes chapters), the Hugging Face card, and Apple/MLX docs. I cannot say what is shown on screen.

Chapters [video-desc]: 0:00 Two Macs, one 432 GB model · 0:24 Yesterday: slower than one Mac · 1:22 The two Macs · 2:48 DeepSeek V4.1 Flash on both Macs · 3:56 Why two Macs were slower · 5:46 Has anyone done this? · 6:17 Live: what it writes · 8:36 A real job (a shop page) · 9:44 What about an M3 Ultra? · 10:37 How to set it up · 11:19 Verdict.

| Item | Claim |
|---|---|
| Hardware | Mac Studio M5 Ultra 256 GB + MacBook Pro M5 Max 128 GB [video-desc] |
| Model | DeepSeek V4.1 Flash, "oQ4e" quant by Jundot, ~432 GB (402.4 GiB) [video-desc, HF] |
| Quant detail | 4.365 bpw excluding Engram tables, 4.529 bpw whole checkpoint; 73% of weights MXFP4, 0.8% MXFP8, 25.8% Engram tables at affine 4-bit; made with oMLX v0.7.1; MIT licence; includes a multi-token-prediction head (not tried in the video) [HF] |
| Size of model | 552B backbone, 763B total logical weights incl. 196.6B Engram tables, vision encoder and MTP head; active params and context length NOT stated [HF] |
| Memory split | NOT stated as GB per machine. A bandwidth-weighted split means the MacBook "reads about 29% of the bytes per token" [video-desc]. [arith] 29% of 432 = ~125 GB on the laptop, ~307 GB on the Studio, which exceeds 256 GB. So the split cannot be a plain in-RAM shard of all 432 GB; unexplained |
| Software | MLX distributed, **JACCL backend**, RDMA; launched per MLX docs with `mlx.launch --backend jaccl --hostfile ...` [video-desc; independent: MLX docs]. Versions of MLX/macOS: NOT given in the description |
| Interconnect | One Thunderbolt 5 cable, RDMA [video-desc]. Mac Studio M5 Ultra spec: TB5 up to 120 Gb/s [independent: Apple newsroom] |
| macOS | Not stated. RDMA over Thunderbolt exists since macOS 26.2 [independent: MLX docs]; Apple's page says the new Studio needs macOS 27 [independent: Apple newsroom] |
| Generation speed | Benchmark decode **56.3-57.4 tok/s over 256 tokens**; ~55 tok/s via chat endpoint; ~51 tok/s in recorded demos with screen recording [video-desc] |
| Prefill speed | **Not given** |
| Context tested | **Not given** (256-token decode benchmark only) |
| Small-model results (Qwen3.8 27B 4-bit) | Studio alone 54.3 tok/s; MacBook alone 33.4; both Macs 20.5-23 untuned (28 Oct, slower than Studio alone); 55.6-55.8 with fast sync only; **61-64 with the weighted split too** (a first run of 37.3 was contaminated by another app) [video-desc] |
| Fix 1 | `MLX_METAL_FAST_SYNCH=1`: one small exchange ~250 us to ~33 us [video-desc]. MLX docs warn it can deadlock and wedge the GPU, so it is off by default [independent: MLX docs] |
| Fix 2 | Split layers by memory bandwidth, not in half, so neither Mac waits [video-desc] |
| Cost | Apple UK configurator, 29 Oct 2026, 2 TB SSD: Studio GBP 11,299 + MacBook Pro GBP 6,699 = **GBP 17,998** [arith from video-desc]. Which RAM/chip variants those prices refer to is implied (256 GB Ultra / 128 GB Max) |
| Honesty notes | M3 Ultra comparison is an estimate from published bandwidth, not measured. Narration is an AI voice clone; the setup and benchmarks were run by Claude Code on his Macs. Scripts to go on GitHub "if it proves reliable" (not yet) [video-desc] |

**Independent coverage of the same setup: none found.** Searches for "432 GB" with M5 Max/Ultra returned nothing. Related, but a different setup: exo clustering of Mac Studios over TB5 RDMA, tensor-parallel, full-mesh cabling, `rdma_ctl enable` from Recovery; its numbers are M3 Ultra (e.g. 26.2 tok/s on 2 nodes, 31.9 on 4, vs 17.2/15.2 without RDMA); no prefill figures; cost example 4 x M5 Ultra 256 GB about US$43,796 plus ~US$600 cabling [independent: https://alphasignal.ai/news/exo-turns-four-mac-studios-into-a-4-8tb-s-ai-cluster]. Apple claims 3x inference for a four-Studio cluster (Apple's own July 2026 test, no config) [independent: Apple newsroom]. A MacRumors comment (unverified) says clusters above two machines have been buggy [independent: MacRumors].

## What it means for Kam's Studio

Prior study: Studio M5 Ultra 256 GB, 1.2 TB/s, A$15,499, justified mainly as the only box that holds MiMo-V2.6-Flash 4-bit beside Ornith (46/48 vs the Spark's 43/48 on our tickets), and its own BLUF said "don't buy yet, test first" [ours: `0_Brain/reference/2026-10-10_mac-ram-local-coding-models/REPORT.md`]. This video does not change that.

**1. What a Studio + laptop pair can hold [arith].** Total memory: 256 + 32 = 288 GB; 256 + 64 = 320 GB; video's 256 + 128 = 384 GB. Each machine also needs OS and app headroom, and the usable GPU share of RAM was not measured here (UNMEASURED; macOS caps GPU-wired memory below 100% by default). So with a 32 GB laptop you gain at most ~24-30 GB of model room, with a 64 GB laptop at most ~50-60 GB. A 432 GB model is out of reach of either (288 or 320 GB < 402 GiB), unless the unexplained mechanism in BLUF point 3 turns out to work with less memory, which is UNMEASURED.

**2. Is pairing worth it for 25K-token agentic prompts?** Not on this evidence.
- Gains the creator saw were small: 54.3 to 61-64 tok/s on a 27B model, +13 to +18% [arith from video-desc], and that needed two non-default fixes after a result that was 2.3x slower untuned (23.5 vs 54).
- A 32 or 64 GB laptop would hold a smaller share than the 128 GB one, and the split is by bandwidth (~614 GB/s vs 1.2 TB/s, so a bandwidth-proportional share is 614/(1228+614) = 33% for the laptop), so the laptop would be capped by its RAM, not its speed. Its contribution to generation would be at most one third.
- Prefill is compute-bound; in principle a second GPU (M5 Max 40-core vs Ultra 64/80-core) adds compute, but **no prefill number exists in the video, exo coverage or Apple's claim**. The 25K-token turn is therefore UNMEASURED for any pair. Generation (the only thing measured) is the part that matters less for us.
- Reliability: runs depend on a deadlock-prone env var, a Recovery-mode setting on each Mac, direct cabling, and matched OS builds. Our fleet value is predictable queue throughput; this adds a second machine that must be online and a laptop that sleeps and throttles.

**3. Models newly unlocked vs the 256 GB Studio alone.** Only models between roughly the Studio's usable memory and that plus the laptop's. From our known set: nothing identified. MiMo 4-bit and V4 Flash 4-bit already fit on 256 GB [ours: prior report]. Candidates in the 250-330 GB band (e.g. MiMo at 6-8 bit) are UNMEASURED: I did not look up their sizes, and the prior report has no quality evidence above 4-bit. Models of 400+ GB (this video's) need either a 128 GB laptop or a second Ultra, or the 512 GB Studio (late October release, price unpublished at 2026-10-10 [ours: prior report]).

**4. Where the video is genuinely useful.** The fast-sync and bandwidth-weighted-split findings generalise to any 2-node setup, including two Studios later. And the quant it uses (V4.1 Flash at ~4.5 bpw, from MXFP4 weights) is a data point for what a Flash-class model costs in RAM: 432 GB, far more than the Spark's 3.0 bpw V4 Flash. Don't assume "V4 Flash" in our notes equals this checkpoint; V4.1 Flash is newer, 763B logical weights.

## Setup checklist for when the Studio arrives
(From MLX docs and exo coverage; not tested by us. Test on the Studio alone first.)
1. Update the OS: RDMA needs macOS 26.2 or later; Apple lists macOS 27 for the new Studio. Both Macs must run matching versions, including beta build numbers [independent: alphasignal; MLX docs].
2. Single-machine baseline first (V4 Flash 4-bit, MiMo 4-bit with `mlx-lm`/`mlx-vlm`): record decode AND prefill at 25K tokens. This is the number the prior report's Gate needs.
3. Only if pairing is still of interest: cable with Thunderbolt 5 (not the TB5 port next to Ethernet on a Studio, per exo notes). Disable the Thunderbolt Bridge; give each link its own isolated local network.
4. On each Mac: shut down, boot to Recovery, Terminal, `rdma_ctl enable`, reboot. Cannot be done remotely. Verify with `ibv_devices` (look for `rdma_en*`).
5. `mlx.distributed_config --hosts A,B --over thunderbolt --backend jaccl --auto-setup --output hosts.json` (needs passwordless sudo and SSH).
6. Launch: `mlx.launch --verbose --backend jaccl --hostfile hosts.json -- python script.py`. Add `MLX_METAL_FAST_SYNCH=1` only after a baseline, and expect possible GPU wedge; keep a reboot path.
7. Always compare against the Studio alone at the same model, same prompt length. Per the creator, an untuned pair can be slower than one machine.
8. Never put MLX/exo ports or the hostfile on an untrusted network; no credentials in hostfiles.

## UNMEASURED / could not verify
- Transcript and on-screen content of the video: not read. All claims come from the description.
- Prefill tok/s and context length for the 432 GB run: not given.
- How 432 GB (402 GiB) fits in 256 + 128 = 384 GB: not explained.
- Per-machine memory split in GB; MLX, macOS and mlx-vlm versions used.
- Whether JACCL/RDMA works with a 32 GB or 64 GB MacBook, and thermal behaviour of a laptop under sustained load.
- Quality of the oQ4e checkpoint (no benchmark on our tickets); whether it beats MiMo 46/48.
- Whether Kam's laptops have Thunderbolt 5 (not checked; M5 Max laptops do per Apple, our 32 GB machine's model unknown).
- Any measurement by us. Nothing was run.
- TN3205 (Apple technote) page body could not be fetched; RDMA requirements taken from the MLX docs instead.

## Sources (read 2026-11-01)
- Video: https://youtu.be/zY11Mss9fsw (title, author, publish date, length, full description with chapters; no transcript)
- YouTube oEmbed for the same video (title, channel)
- Model card: https://huggingface.co/Jundot/DeepSeek-V4.1-Flash-oQ4e-mtp
- MLX distributed docs (JACCL, RDMA, env vars): https://ml-explore.github.io/mlx/build/html/usage/distributed.html
- Apple newsroom, new Mac Studio: https://www.apple.com/newsroom/2026/08/apple-introduces-new-mac-studio-with-m5-max-and-m5-ultra/
- exo cluster coverage: https://alphasignal.ai/news/exo-turns-four-mac-studios-into-a-4-8tb-s-ai-cluster
- MacRumors on clustering: https://macrumors.com/2026/08/26/new-mac-studio-can-be-clustered-together/
- Apple TN3205 (cited by the creator, page body not retrievable): https://developer.apple.com/documentation/technotes/tn3205-low-latency-communication-with-rdma-over-thunderbolt
- Prior study: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-10_mac-ram-local-coding-models/REPORT.md

## Wednesday's verification (2026-11-01, on receipt)
- **Model card, re-read by Wednesday:** 432.033 GB / 402.363 GiB, 4.529 average bpw, mixed MXFP4 / MXFP8 / BF16. This matches the report. The card gives no hardware guidance.
- **The YouTube page, re-fetched by Wednesday, returned the TITLE ONLY.** Everything above attributed to [video] (hardware, 55 tok/s, the two fixes) is the sub-agent's reading of the description, and Wednesday has NOT re-read it. Treat those figures as one source, unconfirmed.
- The memory-fit gap the BLUF flags (384 GB of RAM, 402 GiB of weights) is unresolved. The obvious hypothesis is that some tables are memory-mapped from SSD, but that is UNMEASURED.
