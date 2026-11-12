# Nemotron-3.5-Super-VL-120B-A12B NVFP4, LOCAL on the Spark — operator report (saved by Wednesday 2026-11-12 ~16:2x; the operator's Write was refused)

## BLUF
- **Fit: YES, on the third launch.** Weights 70.1 GiB; container start 04:25:53Z -> `/v1/models` 200 at 04:36:19Z (~10.4 min); max context 1,048,576; KV cache 24.56 GiB at `--gpu-memory-utilization 0.75`. Launches A and B were OOM-killed (A: Wednesday's operator omitted NVIDIA's two video flags; B: global OOM during FlashInfer MoE autotune). C = video flags + `--disable-flashinfer-autotune` serves. NVIDIA's recipe as written does NOT fit without that flag.
- **Score 16/23** = V4 Flash local 16, on different tasks (Nemotron only: T05, T19, T20; Flash only: T10, T11, T15; both fail T04, T16, T17, T18). V4.1 hosted 19, MiMo hosted 19, GLM-5.3 Flash hosted 20, Nemotron HOSTED (CoreWeave) 14.
- **Speed: faster.** 49.1 s/task vs V4 Flash 57.4; e2e 39.7 vs 33.2 completion tok/s. Decode 41.5-51.3 tok/s (MTP 5 draft tokens) vs V4 Flash 37.13 on record (2026-09-22 HANDOFF, not re-measured). Prefill 2,219 vs 1,032 tok/s.
- **Thinking OFF proven** (`enable_thinking=false`; reasoning_tokens 0 on all 23).
- **Branch (a): NEMOTRON LEFT SERVING** under Kam's 15:12:11 rule (>= 16, stable, faster). Proof: `ab.py --model nemotron --only T01 --label keep1112` = PASS (BYTE-IDENTICAL golden, 23.6 s).
- **Restore = one step:** `ssh hp-loan-spark 'docker stop ab1112-nemotron-c && docker start deepseek-v4-flash-spark-deepseek-v4-flash-1'`, then `ab.py --model deepseek --only T01 ...`. The DeepSeek container is stopped (never removed), unchanged from `serving_before.txt` (this folder). Earlier restores ~3m25s.
- **Spark had no model 15:00-15:36 AEDT (36 min).**

## Owed by Wednesday (operator changed none)
1. **Every production caller asks for `deepseek-v4-flash-0731` and sends `chat_template_kwargs.thinking`** — fails on the model name; Nemotron reads `enable_thinking` and defaults thinking ON. Callers: `local_model_task.sh:83` (SPARK_MODEL default; via spark/round.sh:368 and night/briefs/KS-1350/golden/ks1350_round.sh:27); `lib/spark_call.py:98` (thinking kwarg; also :17, :160); `gate/spark_review.py:24` (MODEL), `:160` (thinking); `digest/digest.py:33` (MODEL), `:370` (thinking False); `stale_screen/screen.py:33` (MODEL), `:202` (thinking False). Not the Spark: hosted/replay.py:92 (OpenRouter). Health checks (spark/tunnel.sh, fleet/spark_status.py:54) read any model: UP.
2. **Restart policy `no`** on ab1112-nemotron-c (V4 Flash's was `on-failure:1`): a reboot/crash leaves nothing serving.
3. **The two failed launches caused host-wide OOM kills** (04:09-04:11Z, 04:25:25Z): NetworkManager, dgx-dashboard(s) came back; **rasdaemon is `failed`**; swap holds 9.7 GB.
4. **Headroom:** 12.9 GB available (V4 Flash left ~4 GB).

## Launches (serve script /home/datasec-rd/five-model-ab-1112/serve_nemotron.sh on the Spark; image vllm/vllm-openai:v0.33.0; NVIDIA's 1x DGX Spark Quick Start with native MTP x5 instead of the undownloaded LiLiCorr drafter; port 8888, served name `nemotron-3.5-super-vl`, max-num-seqs 1)
| # | container | extra args | result |
|---|---|---|---|
| A | ab1112-nemotron | none (video flags omitted) | OOM during encoder-cache profiling, exit 1 |
| B | ab1112-nemotron-b | + `--video-pruning-rate 0.5 --media-io-kwargs '{"video": {"fps": 2, "num_frames": 256}}'` | global OOM in FlashInfer MoE autotune, exit 137 |
| C | **ab1112-nemotron-c** | + `--disable-flashinfer-autotune` | **serving** |

## Control
`--model control --label nemo1112` reproduced 23/23 recorded verdicts. ab.py unchanged (its `nemotron` arm: served `nemotron-3.5-super-vl`, `enable_thinking: false`, 127.0.0.1:47788 tunnel). Byte identity proven for all 23.

## Task x arm
| task | exp | Nemo local | V4 Flash local | V4.1 h | MiMo h | GLM h | Nemo h |
|---|---|---|---|---|---|---|---|
| T01 | CAN | PASS | PASS | PASS | PASS | PASS | PASS |
| T02 | CAN | PASS | PASS | PASS | PASS | PASS | PASS |
| T03 | CAN | PASS | PASS | PASS | PASS | PASS | PASS |
| T04 | PARTIAL | FAIL A2a | FAIL A2a | PASS | PASS | PASS | PASS |
| T05 | PARTIAL | PASS | FAIL A2a | PASS | PASS | PASS | FAIL A4 |
| T06 | CAN | PASS | PASS | PASS | PASS | PASS | PASS |
| T07 | CAN | PASS | PASS | PASS | PASS | FAIL B3b | PASS |
| T08 | CAN | PASS | PASS | FAIL A2a | PASS | PASS | PASS |
| T09 | CAN | PASS | PASS | PASS | PASS | PASS | PASS |
| T10 | CAN | FAIL B3x | PASS | PASS | PASS | PASS | FAIL B2 |
| T11 | CAN | FAIL A3x | PASS | PASS | PASS | PASS | FAIL A3x |
| T12 | PARTIAL | PASS | PASS | PASS | PASS | PASS | PASS |
| T13 | PARTIAL | PASS | PASS | PASS | PASS | PASS | PASS |
| T14 | PARTIAL | PASS | PASS | PASS | PASS | PASS | FAIL A1 |
| T15 | PARTIAL | FAIL A2a | PASS | FAIL A2a | FAIL A2a | PASS | FAIL A2a |
| T16 | PARTIAL | FAIL A4 | FAIL A2a | PASS | FAIL A2a | FAIL A1 | FAIL A4 |
| T17 | CANNOT | FAIL A4 | FAIL A2a | FAIL A2a | FAIL A2a | PASS | FAIL A3b |
| T18 | CANNOT | FAIL A3b | FAIL A2a | PASS | FAIL A2a | FAIL A2a | FAIL A3b |
| T19 | CANNOT | PASS | FAIL B3x | PASS | PASS | PASS | FAIL B3x |
| T20 | CANNOT | PASS | FAIL B3x | FAIL B3x | PASS | PASS | PASS |
| T21 | CAN | PASS | PASS | PASS | PASS | PASS | PASS |
| T22 | PARTIAL | PASS | PASS | PASS | PASS | PASS | PASS |
| T23 | CAN | PASS | PASS | PASS | PASS | PASS | PASS |
| **total** | | **16** | **16** | **19** | **19** | **20** | **14** |

## Speed (sums over 23)
Nemotron local 1130.1 s (49.1/task), 611,023 prompt / 44,893 completion tokens, 39.7 tok/s e2e. V4 Flash local 1320.2 s (57.4/task), 595,815 / 43,775, 33.2. Streaming: 66,516-token prompt TTFT 29.98 s (2,219 tok/s prefill), 2,048 decoded at 51.3 tok/s; 73-token prompt 1,024 decoded at 41.5 tok/s.

## Does NOT measure
One run per arm at temp 0 (V4.1 moved 17->19 between runs: 16 vs 16 is a tie). Local vs hosted Nemotron differ on 9 tasks (same weights, different stacks). MTP on (speed, not outputs at temp 0). One cold load; no reboot test. Text only (no vision/video). Largest prompt 73,009 tokens. One codebase, single requests, no soak.

Files: spark-ab/results_nemotron.tsv, results_nemotron_keep1112.tsv, results_control_nemo1112.tsv, RESULTS_LOG.md (+1 row). Spark: serve_nemotron.sh, swap_times.txt; containers ab1112-nemotron and -b Exited (kept); -c serving.
