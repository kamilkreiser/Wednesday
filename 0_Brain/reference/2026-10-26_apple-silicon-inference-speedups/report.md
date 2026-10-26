# Apple Silicon local-LLM speedups: what is real (2026-10-26)

Kam, live board 15:04:51, verbatim: "I have been hearing a lot of apple silicone builds and mlx and other(I cannot remember the name) running 5 - 15 times faster than generic builds. please look into this as well."
Researched by a Sonnet drafter (web search + fetch); text saved by Wednesday unedited. Every figure carries the drafter's source; credibility as the drafter rated it. Not independently re-checked by Wednesday.

**Research report: Apple Silicon local-LLM stacks, claimed speedups, and what they mean for us (2026-10-26)**

**BLUF**
- I found no primary source claiming 5-15x for MLX against a competent baseline.
- Honest like-for-like gains over llama.cpp Metal are about 1.0-1.9x for generation, with the largest gains on small and MoE models.
- 5-15x only appears against weak baselines (PyTorch MPS, CPU-only, or "no cache" for the first token).
- The name Kam can't recall is most likely **MLX**. Other candidates are **oMLX** (caching claims) and **Ollama's MLX backend**. For Apple's M5 chip, the "4x" figure is a prompt-processing claim.
- ds4, a DeepSeek-specific engine, already gets about 27-37 tok/s on the M3 Ultra. That is roughly our Spark's 33 tok/s, not a multiple of it.

**Stacks**

| Stack | What it is | Claim | Baseline | Source, date | Credibility |
|---|---|---|---|---|---|
| MLX / mlx-lm | Apple's framework | M5 first-token time 3.3-4.06x faster (decode only 19-27%) | M4 chip, same MLX | [Apple ML research](https://machinelearning.apple.com/research/exploring-llms-mlx-m5), Nov 2025 (a second source says Jan 2026) | High, but it is a chip-versus-chip claim |
| vllm-mlx (paper) | Batching server on MLX | 21-87% over llama.cpp; 4.3x aggregate at 16 concurrent requests | llama.cpp (the 4.3x is against its own single request) | [arXiv 2601.19139](https://arxiv.org/abs/2601.19139), Jan 2026; M4 Max | High (peer-reviewed) |
| Ollama 0.19 (MLX preview) | Ollama with an MLX backend, for safetensors models only | Decode 58 to 112 tok/s (1.93x); prefill 1154 to 1810 (1.57x) | Ollama 0.18, Q4_K_M | [Ollama blog](https://ollama.com/blog/mlx), 2026-03-30 | Medium. Hardware isn't stated, and the baseline changes both version and quant |
| llama.cpp (Metal) | The generic baseline | n/a | n/a | n/a | n/a |
| LM Studio | Runs both llama.cpp and MLX engines | None found | n/a | n/a | n/a |
| oMLX | MLX server with RAM+SSD KV cache and batching | Time to first token from 30-90 s to under 5 s; up to 4x at high concurrency | A cold, uncached first token | [ToolRadar and SourceForge](https://sourceforge.net/mirror/omlx/), no methodology | Low. Third-party text, and the 4x is a concurrency figure |
| oMLX speculative decoding | Draft-token decoding | Qwen3.6-35B-A3B 89.6 to 140.4 tok/s (1.57x), M3 Ultra | Same model without speculation | [oMLX 0.5.0.dev1](https://r.datuan.dev/r/oMLX/top), date unverified | Medium (maintainer post) |
| MTPLX | Native MTP runtime | 2.24x decode on Qwen 3.6 27B | Same model without MTP | [SourcePulse](https://www.sourcepulse.org/projects/29507173) | Medium |
| ds4 (antirez) | DeepSeek V4 Flash-only Metal engine | No multiplier claimed | n/a | [GitHub](https://github.com/antirez/ds4), undated | High for what it is |
| vLLM-Metal | vLLM on Apple GPUs | None | n/a | [Docker blog](https://www.docker.com/blog/docker-model-runner-vllm-metal-macos/) found llama.cpp about 1.2x faster on a 1B model | Medium |

The largest honest multipliers are batching (up to 4.3x at 16 concurrent requests), caching (28x for repeated images) and speculative decoding (about 1.6-2.2x). The caching and batching figures don't apply to one user generating one stream.

**Like-for-like**
- **Small models.** On an M4 Max, Qwen3-0.6B ran at about 525 tok/s on MLX against 281 on llama.cpp ([arXiv](https://arxiv.org/abs/2601.19139); [summary](https://www.promptquorum.com/local-llms/mlx-vs-ollama-vs-llama-cpp-mac)).
- **Large models.** Past about 27B parameters the gap closes to roughly 0-20%, which one source attributes to memory bandwidth (secondary blogs; see the search results above).
- **MoE models.** Ollama's Qwen3.5-35B-A3B result (1.9x decode) is the best MoE data point, but it mixes engine and quant changes ([Ollama blog](https://ollama.com/blog/mlx)).
- **Prompt processing.** The big hardware win is the M5's Neural Accelerators, which give about 4x faster prompt processing and only 19-27% faster generation ([Apple](https://machinelearning.apple.com/research/exploring-llms-mlx-m5)). That is an M5-versus-M4 comparison, not MLX versus llama.cpp. I found no clean MLX-versus-llama.cpp prompt-processing comparison on DeepSeek-class MoE models.
- **DeepSeek V4 Flash on Mac.** Secondary-source single runs, all with ds4 at Q2 ([ModelFit](https://modelfit.io/blog/deepseek-v4-flash-0731-128gb-macbook/); [yage.ai](https://yage.ai/share/ds4-deepseek-v4-flash-mac-en-20260522.html)):

| Mac | Generation | Prefill |
|---|---|---|
| M3 Ultra 512 GB | 27-37 tok/s | 84-479 tok/s (varies with context length) |
| M5 Max 128 GB | 34 tok/s | 287 tok/s |
| M3 Max 128 GB | 27 tok/s | 259 tok/s |

- **MLX on DeepSeek V4 Flash.** Reddit-sourced reports of 25-35 tok/s, relayed by a [guide](https://www.compute-market.com/blog/deepseek-v4-flash-local-hardware-guide-2026). Unverified.
- **Slow case.** An M1 Ultra with 128 GB got 5-6 tok/s in LM Studio on UD-IQ3_XXS, and 15-16 with an unofficial patch (same sources).

**ESTIMATE (not measured)**
- **Generation on a 256 GB Studio:** about 25-40 tok/s with ds4 or MLX at Q2-Q4. That is roughly parity with the Spark's 33 tok/s. I expect speculative decoding to add up to about 1.5-2x, but no published figure exists for V4 Flash on Mac. Treat it as upside only.
- **Binding limit is memory bandwidth.** The model reads about 13B active parameters per token, roughly 7-8 GB at 4.5-5 bits. At 819 GB/s that gives a ceiling near 100 tok/s. Observed speeds are about a third of that ([guide](https://www.compute-market.com/blog/deepseek-v4-flash-local-hardware-guide-2026); the ceiling arithmetic is the fetch tool's own check, not the page's). I did not verify the 819 GB/s figure; the guide attributes it to both the M4 Max and an M5 Ultra.
- **Prefill, where the Mac is weaker.** The Studio's prefill of 300-480 tok/s will likely trail the Spark's GPU. I have no Spark prefill figure to compare.
- **Quant pick.** With 256 GB, UD-Q4_K_XL (155 GB) leaves about 90 GB for KV cache. UD-IQ3_XXS (104 GB) is the faster, safer middle option. Start by benchmarking Q4 against IQ3 with ds4 and with MLX on our own prompts.

**What I could not verify**
- Any primary "5-15x" claim. It may be a garbled version of the 2-3x Ollama-versus-MLX comparison or the 4x M5 prompt-processing figure.
- ds4's own throughput numbers. Its README links a chart I couldn't read, so all ds4 figures come from secondary sources.
- A published MLX speedup for MTP on DeepSeek V4 Flash. I also couldn't confirm that the "-mtp" MLX builds exist.
- Hardware for the Ollama benchmark, and the dates of the oMLX claims.
- Whether the 25-35 tok/s MLX reports use the 4-bit build.
- Apple's publication date (Nov 2025 versus Jan 2026).
- The blog benchmarks I found (the M4 Max 0.6B-27B table, the 10-20% decode gap above 14B) are blog-level; I did not cross-check them.