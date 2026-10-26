# Ornith 1.5 122B vs DeepSeek V4 Flash on the Spark (2026-10-26)

Kam, live board 12:32:27, verbatim: *"When the spark is idle, please test onrith on it and push it as much as you can. Give it things you think it can partially do and tasks it cannot do. But run the same test on the current spark model for comparison"*.
Run by an Opus teammate from `2_Project_Files/local-model/spark-ab/BRIEF.md`. The teammate's sub-agent could not write report files, so Wednesday saved this from its result and VERIFIED the totals (below).

## BLUF
- **On 23 identical real Secuura prompts, DeepSeek V4 Flash passed 16 and Ornith 1.5 122B passed 12.** Ornith won one task DeepSeek lost; DeepSeek won five Ornith lost.
- On the tasks expected to pass (11), DeepSeek passed all 11 and Ornith passed 7. On "partial" tasks (8), both passed 5. On tasks known to fail (4), both passed 0.
- Five of Ornith's 11 fails had CORRECT code (the checker's code legs passed; only the diff hunk-header line numbers were wrong). A repair round or a recount apply would likely recover several. Not tested.
- **Ornith is slower:** about 23.6 tok/s end-to-end against DeepSeek's 33.2. It takes 11 min to load. It fills the Spark: ~104 GB on the GPU, 111-112 of 121 GB host.
- **DeepSeek was down 62 min 59 s** (13:49:14 to 14:52:13 AEDT). It was restored as the same container, verified by Wednesday at 14:5x: `docker ps` shows it healthy, `/v1/models` = `deepseek-v4-flash-0731`, max_model_len 384000. A post-restore task (T06) gave a byte-identical output.

## Method
- 23 tasks rebuilt from past Spark run dirs (`tasks.json`), each prompt proven byte-identical to its original round (sha256 + prompt bytes). Both models got the same bytes.
- Sampler: temperature 0, max_tokens 16384, one request at a time, thinking OFF for both (Ornith's leak detector was proven to fire on a thinking-on probe; 0 leaks in 46 runs).
- Each task's expected outcome (CAN / PARTIAL / KNOWN-FAIL) was written BEFORE any run. T21-T23 came from the 2026-10-08 Qwen 122B leg-2 set.
- Checker control: the Spark's own original outputs, re-graded today, reproduced all 23 recorded verdicts (17 PASS, 6 FAIL). So the checker can pass and fail.

## PASS by rung (verified by Wednesday from the verdict column of results_*.tsv)
| Rung | Tasks | DeepSeek | Ornith |
|---|---|---|---|
| 1 (one file, one hunk, spelled out) | 5 | 3 | 2 |
| 2 (one file, multi-hunk) | 5 | 5 | 3 |
| 3 (two-three files) | 7 | 5 | 4 |
| 4 (loose brief) | 5 | 3 | 3 |
| 6 (prose only) | 1 | 0 | 0 |
| **Total** | **23** | **16** | **12** |
Control (the Spark's original outputs re-graded): 17/23. Restore check: 1/1.

## Failure causes
- **Ornith:** 5 fails with correct code but wrong hunk-header line numbers (T01, T02, T05, T08, T18); 3 patches that do not apply (T12, T17, T21); 2 that left out the required test file (T16, T19); 1 corrupt patch (T20).
- **Ornith's only win:** T04, where DeepSeek failed on header arithmetic.
- **DeepSeek is not fully deterministic at temperature 0:** 5 of 20 outputs differed from its original Spark outputs. T16 flipped PASS -> FAIL on header arithmetic.

## Ornith serving facts (teammate's measurement)
- Image `nvcr.io/nvidia/vllm:26.09-py3` (vLLM 0.29.0, arm64), checked inside the image before DeepSeek was stopped. The NVFP4 experts run weight-only through the Marlin kernel (GB10 has no native FP4 compute).
- Command in `spark-ab/serve_ornith.sh`: port 8888, `--max-model-len 131072 --max-num-seqs 1 --gpu-memory-utilization 0.85 --reasoning-parser qwen3`.
- Load 11 min 14 s (517 s reading weights, 97 s engine). Weights 66.9 GiB, KV 32.9 GiB (~2.38M tokens). Model time 1,817 s total vs DeepSeek's 1,320 s. Prefix cache: 0 hits.
- Weights: 23/23 files match the Hugging Face listing in size; 8/8 shards match its sha256.

## What was not tested
Rung 5 (no rebuildable task); more than one rung-6 task; DeepSeek's temperature-0 drift with repeat runs; Ornith at its recommended coding settings (temperature 0.6) or with thinking on; Ornith with a repair round.

## Instrument errors (the teammate's own)
The first rung-labelling search was wrong (replaced by reading each brief's `Rung:` line). One exited check container was accidentally re-run (harmless). Swap on the box rose to 3.8 GB during the download while DeepSeek was serving. Ornith's generation config defaults top_k 20 / top_p 0.95, which should be inert at temperature 0.
**Wednesday's own:** a first PASS count grepped "PASS" anywhere in the line (it matched the spark_verdict column) and read 17/17/18; recounted on the verdict column = 17/16/12.

## Files
Tracked (no code; a search for code markers = 0, with a positive control of 13 hits in a gitignored run output): `spark-ab/{BRIEF.md,.gitignore,ab.py,tasks.json,serve_ornith.sh,results_control.tsv,results_deepseek.tsv,results_ornith.tsv,results_deepseek_restore.tsv}`. Gitignored: `spark-ab/runs/`, `spark-ab/work/` (Secuura content).
