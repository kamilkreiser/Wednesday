---
date: 2026-11-02
type: reference
source: Kam live 10:30:50 + 10:36:05 ("can you look whether running MiMo using AirLLM is feasible on a 128gb Mac with you running alongside it for day to day tasks"); Sonnet research subagent commissioned by Wednesday; two load-bearing facts re-read at source by Wednesday 11:1x
status: live
---

# MiMo via AirLLM on a 128 GB Mac — feasibility

## BLUF
- **AirLLM: no.** On macOS it only loads Llama/Mistral; every MiMo model is refused before download.
  Re-read by Wednesday: `air_llm/airllm/auto_model.py:31` `MLX_ARCHITECTURES = {"LlamaForCausalLM", "MistralForCausalLM"}`; `:69-72` raises "is not supported on macOS yet".
- **Even if it ran, layer streaming is unusable:** MiMo-V2.6-Flash (~167 GB at 4-bit) ≈ 13 s/token at full SSD speed, ~95 s/token at AirLLM's measured 1.75 GB/s (estimates).
- **The usable route is RAM-resident, not AirLLM:** MiMo-V2.6-Flash (310B total / 15B active MoE) on llama.cpp (Metal, supports MiMoV2) at ~2.5-bit (~95-97 GB), GPU wired limit raised to ~110 GB; leaves ~14-18 GB for macOS + Wednesday (tight, workable). Est. 50-75 tok/s generation; 2.5-bit quality unmeasured.
- **Comfortable route:** MiMo-V2.6-Distill-Qwen-9B, MLX 4-bit, 7.1 GB, est. 45-55 tok/s, >100 GB spare.
- 4-bit / 3-bit Flash does NOT fit (167 GB / 116 GB). Pro (1.02T / 42B active, ~554 GB) is out.
- mlx-lm `mimo_v2` support is not merged (PR ml-explore/mlx-lm#1219 open) — llama.cpp is the runtime for the big one.

## Models (verified list: huggingface.co/api/models?author=XiaomiMiMo, re-read by Wednesday)
Newest: V2.6 Flash-MOPD / Pro-MOPD (09-27), V2.6 Distill-Qwen-9B / Flash-RL / Pro-RL (09-21), V2.5-DFlash (07-03), V2.5 (04-27). Older: V2-Flash (2025-12-16), MiMo-7B (2025-04-29).

| Model | Total/active | AirLLM Mac | Fits ~110 GB | Est. tok/s |
|---|---|---|---|---|
| MiMo-7B-RL | 7.8B dense | no | yes (MLX 4-bit 4.3 GB) | 70-90 |
| V2.6-Distill-Qwen-9B | 9.4B dense | no | yes (MLX 4-bit 7.1 GB) | 45-55 |
| V2-Flash | 309B/15B | no | only ~2-bit (101.6 GB) | 50-70 |
| V2.5 / V2.6-Flash | 310B/15B | no | ~2.5-bit yes (94.7-96.7 GB); 3-bit 116 GB no; 4-bit 167 GB no | 50-75 |
| V2.5/V2.6-Pro | 1.02T/42B | no | no (~554 GB) | n/a |

## Not measured
Every tok/s figure (arithmetic: active bytes / 614 GB/s × 50-65%); M5 Max bandwidth and SSD figures (Tuesday's report, Apple + Computerworld); the macOS ~75% default wired limit; prompt-processing speed; 2.5-bit quality; nothing downloaded or run.

## Related
Tuesday's K3/AirLLM report (attached to Kam's 10:36 message): same AirLLM restriction, measured 1.22 s/token TinyLlama on the M2 mini.
