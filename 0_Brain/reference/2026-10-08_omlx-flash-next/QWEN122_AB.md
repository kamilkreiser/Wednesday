# Qwen3.5-122B-A10B 4-bit on the Studio: A/B vs Ornith 1.0/1.5 and the Spark (2026-10-08)

Kam's request (18:19 and 18:20, verbatim): "Please test Qwen 122B" ... "in addition to the 20. run something hard that the spark would be working on. Comparison is with the spark".

Run dir: `2_Project_Files/local-model/runs/ab_qwen122_2026-10-08/` (gitignored). Memory samples are in `mem/`, and the leg-1 log is `leg1.log`.

## BLUF

- **The memory guard killed it before it answered a single prompt.** 122B loaded (25 s) and sat idle beside the three live seats. The first checker of leg 1 then ran: the jest suite for the task 01 *control*, with no model request yet. Within about 7 seconds swap grew from 906 MB to 4,499.5 MB (+3,593 MB, limit +256 MB), and memory_pressure free fell to 34%. The guard killed oMLX at 18:57:55.
- **Per the brief, I stopped and did not retry.** No clear-trip, no looser setting.
- **Does it fit beside three seats? No, not with the checker workload alongside it.** The weights fit: oMLX admitted 68.17 GB against its 72.2 GB balanced ceiling, above its own 64.98 GB soft target, and gave no 507. The machine did not cope once one jest suite started. The model had not yet wired its buffers for inference, so real decoding would have needed more memory, not less.
- **Is it better than Ornith 1.5 on the 20? Unknown: 0 of 20 tasks ran.** The server log shows 0 `/v1/chat/completions` requests.
- **How does it compare with the Spark on the hard tasks? Unknown: 0 of 5 ran.** The candidates were chosen (below), but the model never came up for them.
- **Decode tok/s, prefill tok/s and wall per task: not measured.** Load time was measured: 25 s for the model, 43 s from start to ready.
- **Action needed by Wednesday or Kam:**
  - `omlx/state/GUARD_TRIPPED` is now set. Until a human runs `bash 2_Project_Files/local-model/omlx_serve.sh clear-trip`, `omlx_serve.sh start` refuses. That includes the night runner's G5 auto-start of the deployed Ornith 1.5. Right now G2 refuses anyway, because the seats are live.
  - The Ornith symlink was quarantined, not deleted, by `render()`. The next default `start` recreates it and quarantines the Qwen symlink.

## Per-task tables

### Leg 1: the same 20 prompts and the same checker (1.0 / 1.5 / 122B)

1.0 and 1.5 come from `ORNITH15_AB.md`. 122B: only task 01 got as far as its control.

| # | Task | 1.0 | 1.5 | 122B | 122B wall / decode / prefill |
|---|---|---|---|---|---|
| 01 | KS-1344 r2 | PASS 7/7 | PASS 7/7 | **NOT RUN.** Setup OK: prompt sha256 matches 1.0's record (7d4142e0…), clone HEAD == tip 179a4f32, prepare_clone rc 0. The control (1.0's out.md re-graded) gave **PASS 7/7**, checker wall 60 s, source dirty 0 → 0. The model call got `Connection refused` (the server was already killed), so harness rc 4. | — |
| 02–20 | (see ORNITH15_AB.md) | 17/20 total | 17/20 total | **NOT RUN.** The driver stopped on `GUARD_TRIPPED` at 18:58:31. | — |

**Totals: 1.0 17/20 · 1.5 17/20 · 122B 0/20 attempted.**

### Leg 2: Spark-tier hard tasks (Spark vs 122B)

How I chose them:
- From `spark/done.md`, the PASS rows with the highest completion tokens and the multi-file tiers.
- Plus the KS-1278 class (the Spark's one FAIL here, at A3 in r1, then passed in r3).
- Each one has a run dir with input.json, round.json and a recorded verdict.

| Spark run | Tier | Spark verdict | Golden | Spark model wall s | Prompt + completion tok | 122B |
|---|---|---|---|---|---|---|
| 10-07 KS-1410-apigw-batch-audit-export-500 | code_patch2 | PASS 7/7 + A2a | BYTE-IDENTICAL | 75.6 | 19,691 + 3,049 | NOT RUN |
| 10-07 KS-1410-apigw-notifications-500 | code_patch | PASS 7/7 + A2a | BYTE-IDENTICAL | 67.2 | 16,826 + 2,957 | NOT RUN |
| 10-05 KS-1278-revoke-atomic-r3 (r1 FAIL A3) | code_patch2 | PASS | DIFFERS (review: tree-identical) | 66.1 | 71,307 + 3,414 | NOT RUN |
| 10-05 KS-593-share-null-recipient-cp2 | code_patch2 | PASS 7/7 | DIFFERS | 116.4 | 64,837 + 2,760 | NOT RUN |
| 10-05 KS-1136-aggregate-unreadable-artefacts | bash_patch | PASS 7/7 | DIFFERS | 87.2 | 19,492 + 3,512 | NOT RUN |

**Like-for-like note for whoever runs leg 2 later:** the Spark prompt is not the Studio prompt.
- `lib/spark_call.py` sends `SYSTEM_PREAMBLE + "\n\n" + spark-kit/01_FOR_THE_LOCAL_MODEL.md` as the system message, at temperature 0 with no repetition penalty and max_tokens 16384.
- `lib/omlx_call.py` sends `SYSTEM_PREAMBLE` alone, with repetition_penalty 1.15 over the last 512 tokens and max_tokens 32768.
- A fair re-run needs an oMLX client that sends the Spark's messages. Check it with `prompt_bytes`: the Spark recorded 70,129 B for KS-1410 batch.
- It also needs round.sh's checker leg: `code_patch2/checker.sh` + `a2a_anchor.py`, `spark_checker.sh` for code_patch, and the golden `cmp` / tree compare.
- I did not build that client: the model was down before leg 2 began.

## FOUND

1. **122B loads quickly and oMLX admits it, but the Mac does not hold it beside three seats plus a checker.**
   - Load timeline (2-second samples):
     - Free memory dropped from 71.3 GiB to 0.06 GiB in 9 s (18:56:16 → 18:56:25).
     - memory_pressure free bottomed at 38% (18:56:33), then settled at 74%.
     - Swap did not move during the load or while idle (906.06 MB throughout).
   - At 18:57:48–55, with the 01 control's jest suite running, memory_pressure free went 74% → 48% → 35%. Swap jumped to 3,870 MB in my sampler and 4,499.5 MB in the guard's.
2. **The trip was not caused by inference.** No chat request had been sent. The load came from the idle model plus one node/jest checker plus the seats.
   - In today's Ornith 1.5 run the same kind of checker ran 42 times with a 35 GB model, and swap never grew.
   - The difference is the 30 GB of extra weights.
3. **oMLX itself warned that this was a squeeze**, verbatim from serve.out:
   - "Admitting 'Qwen3.5-122B-A10B-4bit' above the admission soft target with no idle model left to evict (68.17GB > 64.98GB, ceiling 72.20GB)".
   - It also noted that Apple's Metal cap is 77.8 GB, below oMLX's static 88.3 GB, and left the cap at the default (iogpu.wired_limit_mb untouched).
4. **oMLX unloaded cleanly when killed:** "freed=64.82GB (expected>=64.65GB)". Actual model size: 65.64 GB.
5. **Side effects of the test:**
   - The swap file grew from 2,048 MB to 4,096 MB total, and 2,701 MB is still in use after the stop (906 MB before).
   - Swapouts rose by 376,625 pages (16 KB each), about 5.7 GiB.
   - The swap that remains is pages the OS pushed out of other processes (the seats). It drains as they are touched.

## TESTED

- **The model folder** loads in oMLX 0.7.0 under the tracked `omlx_serve.sh`. The log notes MTP heads declared but no mtp.* weights (attachment skipped), MoE gate+up fusion on 48 layers, and the VLM engine with the qwen3_coder tool parser.
- **Load time:** 25 s for the model (POST /load), 43 s for the whole `start` (8 s to /health).
- **The memory guard works as designed.** It tripped on swap growth, killed the server with SIGINT, wrote GUARD_TRIPPED, and the next `start` would refuse.
- **The leg-1 harness** (`q_item.sh`, a copy of `ab_item.sh` with only the model id, client path and out dir changed) works end to end up to the model call:
  - task 01's prompt hash matched;
  - the clone sat at the tip;
  - the control re-graded **PASS 7/7**;
  - the Secuura checkout had 0 tracked modifications before and after (checked again at the end: 0).

## HOW

- **Server:** `omlx_serve.sh start` with `OMLX_MODEL=Qwen3.5-122B-A10B-4bit`, `OMLX_MODEL_SRC=2_Project_Files/tools/omlx/models/Qwen3.5-122B-A10B-4bit` and `OMLX_MIN_FREE_GB_TO_LOAD=75`. Available memory at start was 88 GB (92% of 96 GiB).
  - Everything else was the script's defaults: memory tier `balanced`, port 47780, 65,536 context cap, max_concurrent 1, guard at +256 MB swap or <10% free.
  - Nothing loosened; `iogpu.wired_limit_mb` untouched.
- **Client and harness:** `lib/omlx_call.py` (tracked; the request body is the same as the Ornith A/B) through `runs/ab_qwen122_2026-10-08/q_item.sh`. The driver `drive_leg1.sh` runs setup, control and model per task, one at a time, and stops on a 507 or GUARD_TRIPPED.
- **Instruments:**
  - `mem/memsampler.sh`, every 2 s: wired, free, swap used, memory_pressure free %, load, oMLX RSS. Output in `mem/samples.tsv`, 83 rows, 18:55:49 → 18:58:50.
  - Before and after snapshots: `mem/00_baseline.txt` and `mem/99_after_stop.txt`.
  - The guard's own log: `omlx/state/logs/guard.log`.
- **Write scope:**
  - Everything went into the gitignored run dir, plus oMLX's own gitignored `omlx/state/` (rendered settings, symlink, logs, trip file).
  - The scratch clone is under the WEDNESDAY tree.
  - No tracked file edited, no git operation. `night/queue.md`, `done.md` and the night runner were not touched. Nothing deleted.

## NOT TESTED

- **Quality and speed, on everything:** no leg-1 task, no leg-2 task, no decode tok/s, no prefill tok/s, no wall per task. The model never received a prompt.
- **Whether it fits with fewer seats**, or with no checker running at the same moment. One trip is a single sample; I did not retry, by rule.
- **Peak wired during inference.** Wired peaked at 18.97 GiB during load and sat at about 6.2 GiB idle. Inference would wire the weights; Ornith 1.5 showed 41 GiB wired after tasks.
- **The leg-2 client** (the Spark's system prompt sent to oMLX), which was not built.
- **Concurrency:** ornith-loop fires `night_run.sh` every 900 s. During the test it was blocked by G2 (seats live), so it did not interfere. If it had passed G2, its `start` would have found our server and tried to load Ornith into a model_dir without it.

## Memory readings

| When | vm_stat free | Wired | Swap used | memory_pressure free | top PhysMem | 1-min load |
|---|---|---|---|---|---|---|
| Baseline (18:55:39) | 4,740,965 pages (72.3 GiB) | 381,310 pages (5.8 GiB) | 906.06 MB / 2,048 MB | 92% | 23G used (5957M wired, 1084M compressor), 72G unused | 4.20 |
| Load trough (18:56:33) | 0.89 GiB | **18.97 GiB (peak)** | 906.06 MB | **38%** | — | 6.17 |
| Loaded, idle (18:56:39, omlx_serve "ready") | 44,122 pages (0.7 GiB) | 9.6 GiB (status 6.2 GiB a moment later) | 906.06 MB | 71–74% | — | 6.31 |
| Trip (18:57:55) | 0.02 GiB | 7.63 GiB | **4,499.5 MB (guard; peak)**, 3,870.6 MB (sampler) | **34% (guard)**, 35% (sampler) | — | 13.41 |
| After stop (18:58:55) | 5,065,399 pages (77.3 GiB) | 391,029 pages (6.0 GiB) | 2,701.44 MB / **4,096 MB** | 93% | 18G used (6108M wired, 65M compressor), 77G unused | 8.81 |

- **Peak oMLX RSS:** 38.74 GiB, during the load. It was 8.99 GiB idle (the weights are mapped, not counted as RSS).
- **Ollama:** down at the start (nothing on 11434, `/api/ps` refused) and down at the end. Not started.
- **oMLX:** killed by the guard at 18:57:55 ("Finished server process [95681]"). Then `omlx_serve.sh stop` ("no server of ours running"). `lsof` shows nothing on 47780, and no omlx or guard process remains. My sampler is stopped.
- **Left in place deliberately:** `omlx/state/GUARD_TRIPPED` ("2026-10-08 18:58:00 TRIP swap_used=4499.50M grow=3593M free=34% killed pid=95681"). Clearing it is a human decision.
- **Left on disk (run dir, gitignored):** one scratch clone (`clones/ks1344_179a4f32`) and task 01's control evidence. No model file touched.
