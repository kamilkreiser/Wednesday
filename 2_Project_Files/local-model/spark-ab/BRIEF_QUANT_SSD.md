# Spark: DeepSeek V4 Flash with part of the model on SSD, inside a 128 GB-box memory budget (commissioned 2026-10-27)

**Authority, verbatim (Kam, live board, view=wednesday, 2026-10-27 13:23:29 AEDT):**
> "the Gorgon Halo is hard to get and there are none in the country as you mentioned.  so its a spark or 128gb Mac Studio.  can you measure the quant on the spark with some on the SSD.  A setup that favours your workload and allows the v4 flash to do the QA and checks, as well as simple tasks"

**The decision this feeds:** Kam is choosing between a second Spark and a 128 GB Mac Studio. The question is whether V4 Flash still does QA checks and simple tasks at a usable speed and quality when it may only keep PART of itself in RAM (the rest paged from SSD), leaving the rest of a 128 GB box for Wednesday and her seats.

## Read first (do not re-derive)
- `2_Project_Files/local-model/spark-ab/BRIEF_QUANT.md` and `BRIEF.md` (rules, harness, restore duty).
- `0_Brain/reference/2026-10-26_deepseek-quant-on-spark/report.md`: yesterday's result. UD-IQ2_XXS (84.6 GiB file) = 18/23, UD-IQ1_M = 16/23, EXL3-3.0 (the served DeepSeek) = 16/23; GGUF decode ~19.5 tok/s, prefill 355 tok/s (IQ2_XXS); IQ2_XXS at 131,072 ctx used 87,830 MiB on the GPU; the llama.cpp route that worked (`serve_gguf.sh`, `ab.py` GGUF mode). The IQ2_XXS and IQ1_M weights should still be on the box: check, do not re-download unless missing.
- QA-check calibration inputs: `2_Project_Files/local-model/gate/` (spark_gate.sh, spark_review.py, REVIEW_CHECKLIST.md) and the calibration rows in `0_Brain/learnings/2026-10-26_spark-gate-pilot-if-it-works-put-it-into-practice.md`.

## The job, in order
0. **Measure first, change nothing:** `ssh ZGX-Nano-G1n 'docker ps; free -g; df -h ~'`; the weight files present (sizes); the SSD's sequential read speed (one `dd`/`fio` read of an existing weight file, page cache dropped if you can, say if you cannot). Record the budget you will impose and WHY: target a resident cap that a 128 GB Mac running Wednesday + ~5 Claude seats could spare (yesterday's measurement on the 32 GB laptop with 5 seats: 71% free; state your assumption for a 128 GB box explicitly, e.g. 48 GB and 64 GB caps).
1. **Swap (stop DeepSeek, never remove it), then serve UD-IQ2_XXS with its memory CAPPED so part of it is paged from SSD**: llama.cpp with mmap on (no `--mlock`) inside a container with a hard memory limit (`docker run --memory=<cap>`), or llama.cpp's own partial offload (`-ngl` below the full layer count / `--override-tensor` expert tensors to CPU) combined with the cap. Prove the cap actually bites: resident memory under the cap during a run AND page-in from disk observed (vmstat/iostat or `/proc/<pid>/io` read_bytes rising during decode). A cap that never pages is not this test.
2. **Run at TWO caps if time allows (e.g. ~64 GB, then ~48 GB):** for each, (a) the rung-1 and rung-2 tasks of the 23-task set (`spark-ab/tasks.json`, the "simple tasks"), same sampler and checker as yesterday, results TSV per cap; (b) the QA-check workload: rerun ONE calibrated Spark gate review (calibration 3 or 4 input, whichever is fully recorded) through `spark_review.py` and compare its findings with the recorded verdict (match / miss / false finding). Record per cap: load time, resident memory, page-in rate, prefill tok/s, decode tok/s, wall-clock per task.
3. If the 64 GB cap scores at least yesterday's rung-1+2 figure (IQ2_XXS: 10/10) and time remains, optionally the full 23 at that cap.
4. **RESTORE DeepSeek exactly as before and prove it answers** (one task re-run byte-identical to its earlier output). NOT optional. If anything fails or runs past ~3 hours, restore first, then report.

## Output
Your final message carries the report text for `0_Brain/reference/2026-10-27_deepseek-ssd-on-spark/report.md` (Wednesday saves it): BLUF first, then a table per cap (pass counts, tok/s, resident GB, page-in MB/s, the QA-review match), what was NOT measured, your own instrument errors, the DeepSeek downtime with start/end times, and the restore proof. Answer Kam's question in one sentence at the top: does a memory-capped V4 Flash still do QA checks and simple tasks well enough, and at what speed. TSVs beside the others (ids/verdicts only). Secuura content stays in gitignored `runs/` and `work/`.

## Boundaries
As BRIEF.md: one client's content (Secuura) only; nothing to any board, PR, human or other project; no money; nothing on the laptop's Docker; never delete (stop containers, keep weights); the Spark is otherwise untouched. Claim the work: `2_Project_Files/tools/wed_claim.sh claim "Spark SSD-offload quant test (Kam 13:23)"` and release at the end.
