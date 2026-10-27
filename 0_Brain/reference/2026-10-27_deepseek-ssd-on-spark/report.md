# DeepSeek V4 Flash with part of the model on SSD, under a memory cap, on the Spark (2026-10-27)

Saved by Wednesday from the Opus measurement agent's final report (brief: `2_Project_Files/local-model/spark-ab/BRIEF_QUANT_SSD.md`). Kam, live 13:23:29 AEDT: *"can you measure the quant on the spark with some on the SSD. A setup that favours your workload and allows the v4 flash to do the QA and checks, as well as simple tasks"*.

**Answer in one sentence:** On the Spark, V4 Flash (UD-IQ2_XXS) held to a real 64 GB or 48 GB budget still gets simple tasks right (4/4 PASS, code byte-identical to the uncapped run), but it is not usable for QA or simple tasks there: prefill ~25 tok/s and decode 3.2 tok/s (64 GB) / 2.1 tok/s (48 GB), so a simple task takes 15-22 min and a gate review 18 min (vs ~2 min uncapped), and its QA review flipped to a false NO GO.

## BLUF
- Simple-task quality held: T03 (rung 1) and T06 (rung 2) PASS at both caps, byte-identical to the uncapped IQ2_XXS output.
- QA quality did NOT hold: PR #1712 replay (calibration 4) said NO GO with 2 false Majors at both caps (Claude gate: GO; recorded EXL3 Spark: GO WITH NOTES). The one matching run was a leaky-cap configuration (~80 GB actually resident), not a capped result.
- Speed is the deal-breaker: uncapped GGUF 355 / 19.5 tok/s (prefill / decode); 64 GB cap ~25 / 3.2; 48 GB cap ~25 / 2.1.
- Why: the only way to make the cap bite on the Spark was experts memory-mapped on the CPU side with the CPU doing expert maths (prefill CPU-bound at both caps); decode paging-bound (SSD reads 150-300 MB/s at 64 GB, ~505 MB/s at 48 GB; the drive does 5.4 GB/s sequential, but page faults are small reads).
- This does NOT settle the Mac question: on a Mac the GPU reads memory-mapped weights from unified memory with no cgroup in the way; macOS behaviour under memory pressure is UNMEASURED.
- Rung 1+2 was 2 of 10 tasks per cap (each task 15-22 min; the full set would have passed the 3-hour restore line).

## Per cap
| | 64 GB cap (memcg 52 GiB) | 48 GB cap (memcg 36 GiB) | Uncapped GGUF (10-26) |
|---|---|---|---|
| Total resident (est.) | ~63.2 GiB | ~47.2 GiB | 85.8 GiB |
| SSD page-in, decode | 147-295 MB/s | ~505 MB/s | 0 |
| Prefill tok/s | ~25 | ~25 | 355 |
| Decode tok/s | 3.2 | 2.1 | 19.5 |
| T03 (rung 1) | PASS, 1,092 s | PASS, 1,327 s | PASS, 120 s |
| T06 (rung 2) | PASS, 874 s | PASS, 1,060 s | PASS, 87 s |
| QA review #1712 | NO GO (mismatch), 1,102 s | NO GO (mismatch), 454 s decode-only | EXL3: GO WITH NOTES, 35.7 s |

Setup: pinned llama.cpp `server-cuda13` b11870, `-ngl 999 --cpu-moe -lm mmap --no-repack -c 131072 -np 1 -t 20`, container `--memory = --memory-swap = <cap>` (48 GB also `--cache-ram 0`); non-expert weights + KV + compute on the GPU (~10.5 GiB), experts as file-backed pages under the cap. Script `~/deepseek-v4-flash-gguf-ssd/serve_ssd.sh` on the box.

## Not measured
Eight of ten rung-1+2 tasks per cap; the full 23; a real Mac/Metal; a capped run with GPU expert maths (GPU access escapes the cgroup on this box); `--moe-cache-mib`, thread tuning, readahead; repeat runs; a second QA calibration PR.

## Instrument errors (the agent's own)
1. The first run's cap LEAKED (cgroup 52 GiB, process RssFile 80 GiB via GPU-side page faults): discarded as a cap test, treated as an upper bound; later runs checked as contained. 2. A container named -56g was lowered live to 52 GiB. 3. The 48 GB QA review measured decode only (prompt cache restored the prompt); re-run cold for T06/T03. 4. Page-in rates +/-10% (5 s sampler). 5. A doubled TSV name. 6. QA replay via a scratch `qa_replay.py` importing `spark_review.py` functions. 7. `wed_claim.sh claim` refused rc 9 (Wednesday's dirty tracked files); the work ran unclaimed.

## DeepSeek downtime and restore
Stopped 13:28:09 AEDT, healthy 15:28:36 AEDT: 2 h 00 min 27 s, one window. T06 re-run byte-identical to its pre-swap output (sha256 952a7723...779c, cmp rc 0); same container and image; `/v1/models` = deepseek-v4-flash-0731. Re-verified by Wednesday at 15:3x: `docker ps` shows the DeepSeek container Up (healthy). Nothing deleted; the test containers are Exited and kept.

## Files
TSVs (ids/verdicts): `spark-ab/results_iq2xxs_ssd64.tsv`, `results_iq2xxs_ssd48.tsv`, `results_deepseek_deepseek_restore_ssd.tsv`. Gitignored runs under `spark-ab/runs/`. On the box: `~/deepseek-v4-flash-gguf-ssd/`.
