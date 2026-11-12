# Spark A/B task-set results log (T01-T23, `tasks.json`, run by `ab.py`)

Kam, live board 2026-11-12 14:17:19 (verbatim): "that's great.  Please log the results.  we can test MiMo and GLM more thoroughly when we get the Studio"

One row per arm-run, newest first. Totals are out of 23, single run, temperature 0, scored by the same per-task checker. Source files beside this log (`results_*.tsv`) and the reports named per row. Noise: V4.1 hosted scored 17 then 19 on two runs of the same arm (only T05 and T12 differ), so a gap of one or two tasks is inside the noise.

| date | arm | where / provider | thinking | total /23 | failed | cost | speed | source |
|---|---|---|---|---|---|---|---|---|
| 2026-11-12 | Nemotron-3.5-Super-VL-120B-A12B NVFP4 | LOCAL, the Spark (vLLM v0.33.0, NVIDIA 1x-Spark recipe, native MTP 5, gpu-mem 0.75, autotune off) | off (enable_thinking=false; reasoning_tokens 0 on all 23) | 16 | T04, T10, T11, T15, T16, T17, T18 | local, no per-call cost | 49.1 s/task model time (V4 Flash local 57.4); decode 41.5-51.3 tok/s, prefill 2,219 tok/s measured | results_nemotron.tsv; 0_Brain/reference/2026-11-12_nemotron-local-ab/report.md |
| 2026-11-12 | Nemotron-3.5-Super-VL (`nvidia/nemotron-3.5-super-vl`) | hosted, OpenRouter -> CoreWeave nvfp4, zdr, data_collection deny, no fallbacks | off (reasoning tokens 0 on all 23) | 14 | T05 T10 T11 T14 T15 T16 T17 T18 T19 | $0.1128 | 118 s model time, 5.1 s/task | results_nemotronhosted_nhost1112.tsv; 0_Brain/reference/2026-11-12_nemotron-hosted-ab/report.md |
| 2026-11-12 | GLM-5.3 Flash (`z-ai/glm-5.3-flash`) | hosted, OpenRouter -> DeepInfra fp4, zdr, data_collection deny, no fallbacks | **ON (endpoint refused to disable it: HTTP 400 "Reasoning is mandatory")** | **20** | T07, T16 (max_tokens while reasoning), T18 | $0.1169 | 25.2 s/task model time | results_glm53flash.tsv; 0_Brain/reference/2026-11-12_glm53flash-hosted-ab/report.md |
| 2026-11-12 | MiMo-V2.6-Flash | hosted, OpenRouter -> Cohere fp8, same privacy pins | off | 19 | see report | $0.1001 (26 entries incl. proofs) | see report | results_mimohosted.tsv; 0_Brain/reference/2026-11-12_five-model-ab/report.md |
| 2026-11-12 | DeepSeek V4.1 Flash (rerun) | hosted, OpenRouter, same privacy pins | off | 19 | see report | $0.065 | see report | results_v41hosted_rerun1112.tsv; five-model report |
| 2026-10-27 | DeepSeek V4.1 Flash | hosted, OpenRouter, privacy pins | off | 17 | see report | $0.0632 | see report | results_v41hosted.tsv; 0_Brain/reference/2026-10-27_v41-hosted-trial/report.md |
| 2026-10-27 | DeepSeek V4 Flash | LOCAL, the Spark | off | 16 | see report | not recorded | not recorded | results_deepseek.tsv |

NOT RUN (2026-11-12): local Nemotron-3.5-Super, Kolibri-1, LFM2.5 and V4.1-local on the Spark (RECOMMISSION2 barred Spark swaps after three drive drops; LFM2.5 also failed on the vLLM 0.29 image, no sm_121 kernel). Weights for Nemotron and Kolibri are on the Spark in `/home/datasec-rd/five-model-ab-1112/`.

NEXT (Kam 14:17:19): test MiMo and GLM more thoroughly when the Studio arrives (WED-161, filed 2026-11-12): several runs per arm to measure the noise, thinking ON vs OFF where the model allows, and a local run on the Studio where the weights fit.
