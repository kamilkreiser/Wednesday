# Open-weight coding models: Kimi "Flash" check plus releases from mid-Sep to 12 Nov 2026
All sources were read on 2026-11-12. "UNVERIFIED" means I could not confirm the claim at a primary or official page.
"ARITH" marks my own arithmetic: 4-bit means about 0.5 bytes per parameter for weights only, before KV cache and 10-20% headroom. Figures marked "SRC" were measured or stated by a source.

## 1. Kimi / Moonshot: is there a "Kimi K Flash"?
- **No. Moonshot has published no "Flash" model.** The full Moonshot HF listing has 20 repos, and none is named Flash, Mini or Lite. The repos include Kimi-K3.1-Pro (2.8T), Kimi-K3 (2.8T), Kimi-K2.7-Code (1T), K2.6, K2.5, K2-Instruct/-0905/-Thinking/-Base (1T), Kimi-Linear-48B-A3B, Kimi-Dev-72B, Moonlight-16B-A3B and Kimi-VL-A3B.
  Sources: https://huggingface.co/models?author=moonshotai&sort=modified, plus the Kilo catalogue (its only Moonshot entry is K3.1 Pro): https://kilo.ai/new-open-weight-models
- The "Flash" name likely comes from other vendors' models: DeepSeek-V4.1-Flash(-1017), MiniMax-M3.1-Flash, MiMo-V2.6-Flash and GLM-5.3-Flash. **This is a guess, not a finding.**
- **Kimi-K3.1-Pro** (newest model):
  - 2.8T total / 104B active MoE, 1M context.
  - Weights are MXFP4 (QAT). The licence is the "Kimi K3.1 Pro License". Source: https://huggingface.co/moonshotai/Kimi-K3.1-Pro
  - API launch was 23 Oct (Kilo catalogue).
  - Weights went up on HF around 4 Nov 2026. Secondary sources give 2, 4 or 5 Nov (https://technode.com/2026/11/05/moonshot-ai-releases-kimi-k3-1-pro-model-weights/). The exact date is **UNVERIFIED** at Moonshot.
  - Licence terms are reported as MIT-style, with a separate deal needed for model-as-a-service providers above $20M revenue. **UNVERIFIED (secondary only).**
  - Download is about 1.56 TB (secondary source). **It does not fit either box.**
- **Kimi K3** (2.8T / 104B, Kimi K3 License): launched July 2026, weights out about 27-28 Jul. This is outside the window. Sources: https://the-decoder.com/moonshot-ai-releases-kimi-k3-open-weights-and-infrastructure-after-shaking-up-the-frontier-model-race/ and https://vdf.ai/blog/best-local-llm-for-coding/
- **Kimi-K2.7-Code** (1T): the HF repo was updated Jun 15. It is out of window and too big.

## 2-3. Candidates released or announced from about mid-Sep to 12 Nov 2026
GB10 = about 128 GB unified memory. Mac = 256 GB Mac Studio.

| Model (vendor) | Date | Total/Active | Ctx | Licence | Weights | Memory at practical quant | GB10 128GB | Mac 256GB (MLX?) |
|---|---|---|---|---|---|---|---|---|
| NVIDIA Nemotron-3.5-Super-VL-120B-A12B | 15 Oct (card) | 120B/12B, hybrid Mamba-MoE | 1M | OpenMDW-1.1 | Yes, BF16 + NVFP4 | NVFP4 is about 60-65 GB (ARITH) | **FITS (SRC: card lists a 1x DGX Spark deployment and vLLM quick start)** | Fits (ARITH). MLX 4-bit/3-bit community builds exist |
| Aleph Alpha Kolibri-1 | 3 Oct (card) | 78.1B/3.46B | 262K native, 1M validated | Apache 2.0 | Yes, FP8 + BF16 | FP8 about 78 GB (SRC: card); 4-bit about 40-44 GB (ARITH) | Fits (ARITH) | Fits (ARITH). MLX 4-bit and MXFP4 builds exist (nativ-community) |
| Liquid AI LFM2.5-24B-A2B | about 13 Oct (vdf); the card shows no date | 24B/2.45B | 131K | LFM Open License 1.0 (revenue cap per vdf, UNVERIFIED) | Yes | 4-bit about 13 GB (SRC: vdf) | Fits | Fits. Official MLX-4bit listed on the card |
| Xiaomi MiMo-V2.6-Flash (-RL; -MOPD on 27 Sep) | about 22 Sep (secondary; UNVERIFIED) | 309B/15B | 1M | MIT | Yes | MLX mxfp4-q8 build: about 167 GB on disk, about 170 GB to load (SRC: mlx-community card) | **No** (would need under 3-bit; ARITH, untested) | **FITS (SRC: 170 GB load)**. Many MLX builds, MTP variants included |
| MiniMax-M3.1-Flash | API 19 Oct; weights 23 Oct (secondary) | about 428B/23B (card text; HF metadata says 220B) | 1M | "minimax-community" (custom; reported sign-off needed above $20M revenue, UNVERIFIED) | Yes | MLX "Text-4bit" is 248 GB, about 249 GB peak (SRC) | No | **Too tight at 4-bit (SRC 249 GB)**. 3-bit / oQ3e MLX builds exist, size unread |
| Reflection Beam-1.0-501B-A23B | Announced 5 Oct; weights about 16 Oct (secondary) | 501.3B/23.4B | 1M | Apache 2.0 | Yes: BF16, FP8, NVFP4 (HF lists the NVFP4 repo at about 255B params) | NVFP4 is about 290 GB on disk (secondary, UNVERIFIED); 3-bit about 190 GB (ARITH) | No | 4-bit no (ARITH). Only one experimental MLX conversion found. 3-bit would be untested |
| DeepSeek-V4.1-Flash-1017 | 17 Oct (secondary) | 763B total (card); active not stated | 1M | MIT | Yes | 4-bit about 380 GB (ARITH) | No | No (only at about 2-bit, ARITH, and not advisable) |
| Meta Muse Spark Open | 15 Oct | 816B/42B | 1M | Muse Model License ("limited commercial terms") | Yes (HF etc.) | 4-bit about 408 GB (ARITH) | No | No |
| Z.ai GLM-5.3-Flash | **Release date UNVERIFIED.** vdf says Aug 2026, so probably outside the window | 320B/18B | not stated | MIT | Yes | 4-bit about 176 GB (SRC: vdf) | No | Fits (ARITH). MLX not checked |
| JetBrains Mellum2.1-Thinking | 8 Oct (vdf only; HF card returned 401) | 12B/2.5B | 131K | Apache 2.0 (vdf) | Yes (vdf) | about 6.7 GB at 4-bit (vdf) | Fits | Fits. **UNVERIFIED overall** |
| Prism ML Bonsai 2 27B (ternary) | 17 Sep (vdf only) | 27B dense | 262K | Apache 2.0 (vdf) | Yes (vdf) | 6-7 GB as shipped (vdf); needs Prism's llama.cpp fork | Fits | MLX unknown. **UNVERIFIED overall** |

Excluded:
- Nemotron 3.5 Lightning 30B-A3B: released 11 Aug, outside the window.
- Tencent Hy4-preview (780B): HF repo dated Aug 28.
- MiniMax-H3: a video model.
- Qwen: no new open-weight coder in the window. Qwen 4 is only teased (secondary: https://overchat.ai/ai-hub/qwen-4-release-date).

Sources for the table rows:
- Nemotron: https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Super-VL-120B-A12B-NVFP4 ; MLX: https://huggingface.co/models?search=mlx%20nemotron-3.5-super
- Kolibri: https://huggingface.co/Aleph-Alpha/Kolibri-1 ; MLX: https://huggingface.co/models?search=mlx-community%20Kolibri
- LFM2.5: https://huggingface.co/LiquidAI/LFM2.5-24B-A2B
- MiMo: https://huggingface.co/XiaomiMiMo/MiMo-V2.6-Flash-RL , https://huggingface.co/XiaomiMiMo/MiMo-V2.6-Flash-MOPD , https://huggingface.co/mlx-community/MiMo-V2.6-Flash-RL-mxfp4-q8
- MiniMax: https://huggingface.co/MiniMaxAI/MiniMax-M3.1-Flash , https://huggingface.co/mlx-community/MiniMax-M3.1-Flash-Text-4bit , https://technode.com/2026/10/23/minimax-releases-open-weights-for-428-billion-parameter-m3-1-flash-model/
- Beam: https://reflection.ai/blog/introducing-beam , https://huggingface.co/reflection/Beam-1.0-501B-A23B , https://huggingface.co/models?search=beam&author=reflection
- DeepSeek: https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017 , https://technode.com/2026/10/19/deepseek-releases-v4-1-flash-1017-with-stronger-coding-and-agent-capabilities/
- Muse: https://research.meta.ai/blog/muse-spark-open
- GLM: https://huggingface.co/zai-org/GLM-5.3-Flash
- Mellum, Bonsai, LFM date: https://vdf.ai/blog/best-local-llm-for-coding/ (page updated 14 Oct)

## 4. Published coding and instruction-following numbers (vendor-reported unless noted; harnesses differ, so the numbers are NOT comparable across rows)
- **Nemotron-3.5-Super-VL** (card, NVFP4 / BF16):
  - SWE-bench Verified 71.07 / 71.10
  - LiveCodeBench v6 87.41 / 88.22
  - Terminal-Bench 2.1 62.78 / 60.67
  - IFBench 71.50 / 70.86
- **Kolibri-1** (card, reasoning high):
  - SWE-bench Verified 66.4 (Harbor harness)
  - LiveCodeBench v6 85.9
  - HumanEval+ 92.7
  - TerminalBench 2.1 27.7
  - IFBench 78.1
- **LFM2.5-24B-A2B** (card):
  - SWE-bench Verified 51.00 (OpenCode harness). Qwen3.6-35B-A3B scored 66.20 in the same table.
  - IFEval 96.75, IFBench 74.69, Multi-IF 84.38. These are the highest instruction-following figures found, and they are vendor-run.
- **MiMo-V2.6-Flash-RL** (card):
  - DeepSWE v1.1 67.9
  - Terminal-Bench 2.1 87.6, TB 4.0 28.8
  - ProgramBench 26.0
  - SWE-bench Verified and LiveCodeBench not listed. The MOPD card lists no benchmarks.
- **MiniMax-M3.1-Flash** (card):
  - DeepSWE v1.1 73.7, Terminal-Bench 4.0 38.1, NL2Repo 61.2
  - SWE-bench Verified, LiveCodeBench and IFEval not listed.
- **Beam** (HF card, BF16 / FP8 / NVFP4; temp 0.7):
  - SWE-bench Verified 81.6 / 80.2 / 80.7
  - LiveCodeBench 88.3 / 88.1 / 88.3
  - Terminal-Bench 2.1 80.1 / 78.9 / 78.4
  - DeepSWE 43.3 / 43.0 / 42.7
  - IFBench 79.6 / 80.7 / 79.2
  - Harness not stated.
- **DeepSeek-V4.1-Flash-1017** (card):
  - DeepSWE v1.1 77.0 (base V4.1-Flash: 74.2)
  - Terminal-Bench 4.0 42.3 (base: 31.2)
  - ProgramBench 29.1, NL2Repo 68.2
- **Kimi-K3.1-Pro** (card, max effort):
  - DeepSWE v1.1 75.5, Terminal-Bench 4.0 65.7, ProgramBench 31.5
  - SWE-bench Verified and LiveCodeBench not listed.
- **GLM-5.3-Flash** (card): Terminal-Bench 2.1 84.3, DeepSWE 63.4 (asterisked on the card, unexplained).
- **Muse Spark Open**: the numbers appear to be in images and were not captured. **UNVERIFIED.**
- **Mellum2.1-Thinking**: 47.0 in the Pi harness vs 50.0 for Qwen3.5-9B (vdf only). **UNVERIFIED.**
- Third-party (vdf.ai) caveat: vendor scores use different harnesses and settings and are not directly comparable.
- No independent benchmark for the exact byte-reproduction / strict-checker task type was found for any model. The team's own A/B remains the only valid measure.

## What I could not verify
- Exact HF publish dates for K3.1-Pro weights, MiMo-V2.6-Flash, Beam weights and MiniMax weights. These come from secondary sources, and the cards give no date.
- DeepSeek-V4.1-Flash active-parameter count. vdf says "552B backbone, 8B/16B active" for V4.1-Flash, while the 1017 card says 763B total. The figures conflict.
- MiniMax-M3.1-Flash total size: 428B in the card text vs 220B in the HF metadata.
- Licence fine print for Kimi K3.1 Pro, MiniMax community, Muse and LFM1.0. I did not read the LICENSE files.
- MLX throughput (tok/s) for any candidate: none was published on the pages read.
- Ollama library availability: not checked.
- Mellum2.1 and Bonsai 2: vdf.ai only.
