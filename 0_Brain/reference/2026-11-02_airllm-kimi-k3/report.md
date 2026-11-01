---
date: 2026-11-02
type: reference
source: Sonnet research agent, commissioned by Tuesday s223 on Kam's 09:29:06 question; filed and re-checked by Tuesday
---

# AirLLM and Kimi K3 on a 128 GB M5 Mac

## Bottom line
- **Your doubt was right.** AirLLM does claim K3 runs in 3.72 GB of VRAM, measured on one RTX 6000 Ada. It gives no speed figure, and the claim is about NVIDIA CUDA machines.
- **On a Mac it does not run at all today.** AirLLM's own source refuses any model other than Llama or Mistral on macOS.
- **If it were ported,** K3 needs about 143 GB read for every token. On a 128 GB M5 Max that is about 10 to 11 seconds per token at SSD speed, and could be about 80 seconds per token with AirLLM's overhead.
- **What to do instead:** run a model that fits in RAM with MLX (about 100B to 125B total parameters at 4-bit), or use K3 through Moonshot's API or a server with far more memory.

## Re-checked by Tuesday at source (2026-11-02, read-only)
- `auto_model.py:31` `MLX_ARCHITECTURES = {"LlamaForCausalLM", "MistralForCausalLM"}`; `:69-70` raises `ValueError` for anything else.
- README `:38` the 3.72 GB claim; `:189` "only Llama-style models ... run on macOS for now".
- `k3_index.json`: total_size 1,560,860,324,864 bytes, 497,220 tensors, 96 shards.
- `hdr51.json` (layer 50): 5,404 keys, 16,990,092,800 bytes.
- `run_tl.log`: 1 token 17.53 s, 5 tokens 55.18 s, 9 tokens 27.33 s; maximum RSS 1,180,696,576 bytes; peak footprint 1,592,624,856 bytes.
- Cross-check of the per-token figure: 117 GB of BF16 non-expert weights is about 58B parameters, and 25.8 GB of 4-bit experts is about 52B, together about 110B against the model card's 104B active. Consistent.
- **Not re-checked:** the web sources below, and the arithmetic's assumption that layer 50 represents layers 1 to 92 beyond the total matching the index.

## 1. How AirLLM works (from source at /private/tmp/airllm-b/src/airllm)
- **Layer streaming.** The checkpoint is split into per-layer files. Each layer is loaded, run, then deleted (`del`, `gc.collect()`). In `airllm_llama_mlx.py`, every generated token reloads the embeddings, all layers, the norm and the output head from disk. Only the OS page cache carries weights between tokens.
- **Apple Silicon backend.** macOS always uses `AirLLMLlamaMlx`, a small MLX port of the Llama block; MLX, not MPS.
- **K3 support.** `airllm_kimi_k3.py` exists on the non-macOS torch path, streaming individual experts through forward hooks. The README says it needs `flash-attn`, a CUDA 12 build of torch and `transformers` 4.56.x. On a Mac, K3 would need a port.
- **Maintenance.** Latest commit 2026-11-01 is an automated star-chart refresh; last real commit 2026-10-19; K3 support 2026-08-21.
- **Speed claims.** The README has no tokens-per-second or seconds-per-token figure.

## 2. Kimi K3 facts
- `moonshotai/Kimi-K3` (https://huggingface.co/moonshotai/Kimi-K3): 2.8T total parameters, 104B active, 93 layers (1 dense), 896 experts with 16 selected per token plus 2 shared, 1,048,576-token context, custom licence.
- The shipped checkpoint is already 4-bit (MXFP4) and is 1.56 TB. No smaller official quantisation was found.
- **Per-token read,** from the layer-50 header: 16 experts at 17.55 MB = 280.8 MB; non-expert weights 1,267.7 MB per layer. (1,267.7 + 280.8) MB x 92 layers = **142.5 GB**.

## 3. Test: TinyLlama 1.1B through AirLLM on this Mac mini (M2, 24 GB, shared with live agents)
- Model 2.1 GB, 22 layers; mlx 0.32.4; started at load1 6.22; weights removed afterwards.
- Import 10.6 s; init and split 12.52 s; peak RSS 1.18 GB, peak footprint 1.59 GB.

| Tokens | Time | Usable? |
|---|---|---|
| 1 | 17.53 s | yes |
| 5 | 55.18 s | no, load1 rose to about 21 |
| 9 | 27.33 s | yes |

- **Cleanest speed:** (27.33 - 17.53) / 8 = **1.22 s per token**, one run on a shared machine, uncertain by about a factor of two.
- **Effective read rate:** about 2.1 GB per pass / 1.22 s = about **1.75 GB/s**, derived, not read from an I/O counter. That is far under the SSD's speed, so AirLLM's MLX path looks limited by its own overhead, not by the disk.

## 4. Estimate for a 128 GB M5 Mac
**Hardware.** 128 GB means the M5 Max. Apple: up to 614 GB/s memory bandwidth, SSD up to 14.5 GB/s (https://www.apple.com/au/newsroom/2026/03/apple-introduces-macbook-pro-with-all-new-m5-pro-and-m5-max). Measured SSD 12.6 GB/s (https://www.computerworld.com/article/4148742/heres-what-5849-gets-you-in-an-m5-max-macbook-pro.html).
**Assumptions.** About 12 GB of RAM for macOS, the KV cache and apps; compute ignored because decoding is memory-bound.

| Case | Arithmetic | Seconds per token |
|---|---|---|
| (a) all in RAM (impossible: 1.56 TB against 128 GB) | 142.5 GB / 614 GB/s | 0.23 |
| (b) cache-hot floor (not reachable: one pass exceeds the cache and reads cyclically) | 100 GB / 300 GB/s + 42.5 GB / 12.6 GB/s | about 3.7 |
| (c) cold, SSD-bound | 142.5 GB / 14.5 to 12.6 GB/s | 9.8 to 11.3 |
| (c) with the overhead measured on the M2 | 142.5 GB / 1.75 GB/s | about 81 (a warning, not a prediction) |

A 500-token answer takes about 83 minutes at 10 s per token, or about 11 hours at 81 s per token. None of these rows can run today, because AirLLM refuses K3 on macOS.

**What fits instead (estimates from parameter counts, not downloads).** A 125B-total MoE at 4-bit is about 63 GB; about 10B active is about 5 GB per token; 5 / 614 gives a bound of 8 ms per token, about 120 tokens/s, with real runs usually about half to two thirds of that (an assumption). A dense 70B at 4-bit is about 40 GB, a bound of 65 ms per token.

## 5. Addendum: a 256 GB Mac (Tuesday, 2026-11-02 10:2x; arithmetic by program, on Kam's 10:18:28 question)
**What changes:** the shared (non-expert) weights now fit. **What does not:** K3 is still about six times the memory (1.56 TB), AirLLM still refuses K3 on macOS, and the chosen experts still change from token to token.
- Per token: 116.6 GB shared + 25.8 GB experts = 142.5 GB.
- Cache at 256 GB: about 244 GB after 12 GB for the system (assumption). After the shared weights, 127 GB is left, about 9% of the 1,447 GB of experts. At 128 GB the shared weights alone (116.6 GB) fill the 116 GB cache, which is why that case had no hot path.
- Shared weights from RAM: 116.6 GB / 819 GB/s = 0.14 s, read as about 0.3 s allowing a copy. 819 GB/s is the M3 Ultra's listed figure (https://ispace.ge/en/product/mac-studio-mu973ru-a); WHICH chip the 256 GB Mac has was not read.
- Experts from SSD, all misses: 25.8 GB / 12.6 GB/s = 2.05 s (the M5 Max's measured rate); 25.8 / 6 = 4.3 s (6 GB/s is an ASSUMED lower rate: no measured SSD figure was found for a 256 GB Mac).

| Case | Seconds per token |
|---|---|
| 256 GB, shared weights hot, experts cold, a loader without AirLLM's overhead | about 2 to 5 |
| Same, if tokens reuse experts already cached | lower, by an amount UNMEASURED |
| 256 GB, AirLLM's overhead as measured on the M2 (warm cache, so more RAM does not remove it) | about 81 (142.5 / 1.75; a warning, not a prediction) |

A 500-token answer at 2 to 5 s per token takes about 17 to 42 minutes. What fits instead, at the 0.5 GB per billion parameters used above: about 380B at the commonly cited 75% GPU limit (192 GB), up to about 480B if that limit is raised. Those are estimates, not downloads.

## 6. Addendum: a smaller model on 128 GB (Tuesday, 2026-11-02 10:2x; Kam's 10:23:24 and 10:23:52 questions)
**Nothing here was run.** Figures are from web sources not checked against the model repositories, and arithmetic by program. No M5 benchmark was found. Several guides looked unreliable.

**MiMo V2.6 Flash does not fit on 128 GB.** 309B total, 15B active, 48 layers, 256 experts with 8 per token. The MLX 4-bit builds are about 156 to 167 GB (https://huggingface.co/TensorFold/MiMo-V2.6-Flash-RL-MLX-4bit-MTP, https://openclawdc.com/blog/can-i-run-mimo-v2-6-flash-locally/). AirLLM's Mac path takes only Llama and Mistral; MiMo's architecture name was not read.

**If its weights were paged from SSD** (a bound, ignoring the KV cache and assuming misses spread evenly; 8.1 GB active per token, SSD 12.6 GB/s, memory 614 GB/s):

| Memory for the model | Share resident | Seconds per token | Tokens per second |
|---|---|---|---|
| 52 GB (64 GB for the seat, 12 GB for macOS) | 31% | about 0.46 | about 2.2 |
| 64 GB (macOS inside the seat's 64 GB) | 38% | about 0.41 | about 2.4 |
| 112 GB (most to the model) | 67% | about 0.23 | about 4.4 |

That is about 20 to 50 times better than K3's 9.8 to 11.3 s by the same arithmetic, but it is unmeasured, and the seat's own memory pressure would make it worse.

**What fits outright (sizes by program from parameter counts, 4.3 bits per weight unless stated):**

| Model (names from the guides, unverified) | Size | Fits 52-64 GB? | Fits about 112 GB? | Reported speed |
|---|---|---|---|---|
| A 33B to 35B coder (Laguna XS 2.1 at Q8; Ornith 35B at Q4) | 33 GB; 19 GB | yes | yes | about 26 tok/s on an M4 Max for a 32B-class model |
| GLM-5.2 Air 106B-A12B, 4-bit | 57 GB | no room for the KV cache | yes | bound about 95 tok/s (614 / 6.45 GB); no real figure found |
| DeepSeek V4 Flash, Q4 | about 80 GB by one guide; another says cloud only for 128 GB | no | yes, if real | not found |
| gpt-oss 120B, Q6 | 93 GB | no | yes, tight | 14 to 20 tok/s on an M4 Max 128 GB |

Sources: https://openclawdc.com/blog/best-models-macbook-pro-128gb/, https://bestllmfor.com/best/macbook-pro-m4-max/, https://bestllmfor.com/meilleur-llm/mac-128gb/, https://www.cloudrift.ai/blog/state-of-open-coding-models-2026.

## Not measured
- K3 itself: nothing downloaded or run; every K3 number is arithmetic from the index and the layer-50 header.
- Any M5 hardware; the test ran on an M2.
- Disk read rate by an I/O counter; a clean repeat of the timing; cold-cache behaviour.
- AirLLM's torch/MPS path, and whether `AirLLMKimiK3` would work on a Mac after a port.
- The K3 licence text (secondary sources disagree) and K3's `config.json` (the fetch returned no JSON).
- Variation in size between layers.
- Whether MLX has a K3 implementation.
- The sizes of the fitting models; the macOS default GPU memory limit (commonly about 75% of RAM) is an assumption.
