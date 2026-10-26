# Spark head-to-head: Ornith 1.5 122B vs DeepSeek V4 Flash (commissioned 2026-10-26)

**Authority, verbatim (Kam, live board 2026-10-26 12:32:27, view=wednesday):**
> "When the spark is idle, please test onrith on it and push it as much as you can. Give it things you think it can partially do and tasks it cannot do. But run the same test on the current spark model for comparison"

This supersedes his 12:26:55 "Don't test on the spark" for this test. Wednesday's reading, receipted on the panel at 12:3x with a correction offer: Ornith = `ornith-ai/Ornith-1.5-122B-NVFP4` (78 GB, MIT, released 2026-10-21); DeepSeek is stopped for the Ornith runs and restarted after; both models get the same task set.

## Facts measured by Wednesday before this brief (read-only, 2026-10-26 12:2x)
- Spark (ssh alias `ZGX-Nano-G1n`, login datasec-rd, NVIDIA GB10): 121 GB unified memory, 118 GB used; disk 3.6 TB, 3.2 TB free.
- Running: container `deepseek-v4-flash-spark-deepseek-v4-flash-1`, Up 10 days (healthy). Base dir `/home/datasec-rd/DeepSeek-v4-Flash-One-DGX-Spark` (weights in `data/`, 99 GB; `hf-hub/` 100 GB; `image-patch/serve-ds4-flash.sh`, `image-patch/entrypoint-256k.sh`). The server log reads "Model loading took 95.39 GiB"; the entrypoint default is GPU_MEMORY_UTILIZATION 0.9465 and MAX_MODEL_LEN 262144 (the container's env override was NOT checked).
- How it is normally restarted: see `0_Brain/reference/2026-09-22_spark-deepseek-v4-flash/HANDOFF.md` and the box's own run-a2.sh / RELOAD notes (the kit says "restart it with the box's own run-a2.sh / RELOAD notes before calling the endpoint broken"). READ these before stopping anything.
- Laptop to Spark tunnel: `2_Project_Files/local-model/spark/tunnel.sh` (127.0.0.1:47788).
- The Ornith model card (huggingface.co/ornith-ai/Ornith-1.5-122B) says "serves on a single 80GB GPU", needs vLLM >= 0.19.1 or SGLang >= 0.5.9, and uses `--tool-call-parser qwen3_coder`. Whether a vLLM build that runs NVFP4 on GB10 (aarch64) exists on the box is UNMEASURED.

## The job, in order
0. **Measure first, change nothing.** Inventory the box: the docker images present, whether any vLLM image >= 0.19.1 for aarch64/GB10 exists or can be pulled, free disk, DeepSeek's exact compose/run command and env, and how to restart it. Write it down before step 2.
1. **Download** `ornith-ai/Ornith-1.5-122B-NVFP4` to a NEW directory on the Spark (for example `/home/datasec-rd/ornith-1.5-122b-nvfp4/`) while DeepSeek keeps running. Verify the file count and sizes against the Hugging Face listing.
2. **Build the task set** from real Secuura work. Take the existing Spark run dirs and checkers (`2_Project_Files/local-model/spark/done.md`, `spark/state/`, `night/briefs/`, and the hosted replay harness `local-model/hosted/replay.py`, which already rebuilds the exact Spark prompt from a run dir and proves it by sha256). About 15-20 tasks across the ladder: rungs 1-3 (spelled-out, expected PASS), rung 4 (loose brief), rung 5-6 (prose-only), PLUS tasks the Spark is known to fail (rounds whose counter was spent and went to Opus; see `spark/done.md`, `2_Project_Files/local-model/SPARK_LADDER.md`, `2_Project_Files/local-model/IMPROVEMENTS.md`). Kam asked for "things it can partially do and tasks it cannot do": label each task's expected outcome BEFORE running it.
3. **Run DeepSeek first, on the task set, as it is now** (same sampler as the Spark rounds: temperature 0, thinking off, the Spark's max_tokens), through the same checker. One request at a time (MAX_NUM_SEQS=1).
4. **Swap:** stop the DeepSeek container (stop, never remove; never delete its weights or image). Serve Ornith with vLLM (OpenAI-compatible) on the same port the tunnel reaches, or a new port. Record the exact command and how long the load took and how much memory it took.
5. **Run Ornith on the identical prompts** (same bytes; prove it with the sha), the same sampler (temperature 0; thinking OFF if the model allows it, otherwise record the setting), the same checker.
6. **Restore:** stop Ornith, restart DeepSeek exactly as it was, and prove it answers (one known PASS task re-run gives the same verdict). Report the total DeepSeek downtime. **Steps 6's restore is not optional: if anything in 4-5 fails or runs past ~3 hours, restore DeepSeek first, then report.**

## Output
- Harness and task list (tracked, no Secuura code): `2_Project_Files/local-model/spark-ab/`. Anything holding Secuura code (run dirs, outputs) goes in a gitignored `spark-ab/runs/` (write the `.gitignore` line first).
- Report: `0_Brain/reference/2026-10-26_ornith122b-vs-deepseek-spark/report.md` — one row per task: task, rung, expected, DeepSeek verdict + failing leg, Ornith verdict + failing leg, tokens and wall-clock each, and a short cause for each FAIL (model / harness / brief). Then totals per rung, Ornith's serving facts (load time, memory, tokens/s), DeepSeek downtime, and "What I could not test".

## Boundaries
- One client's content per task (Secuura only). Nothing to any board, PR, human or other project. No money. Nothing on the laptop's Docker.
- The Spark box is otherwise untouched: only the new Ornith directory, the stop/start of the two servers, and the run outputs.
- Never `cd` in a Bash call; absolute paths. Never print a secret. If the vLLM route for NVFP4 on GB10 does not exist, STOP before stopping DeepSeek and report what was found.
