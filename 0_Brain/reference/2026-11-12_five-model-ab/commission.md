# Five-model A/B on the Spark task set — operator commission, Wednesday (06:37 seat), 2026-11-12 ~07:5x AEDT. Operator model: claude-opus-5-5 (box surgery + measurement design; routing v1.0 Opus row for deploy-with-box-rights).

## Kam's words (live board 07:40:49, view=wednesday, verbatim)
"can you please test the 5 models.  using the same questions as before.  try to fit v4.1 flash on the spark.  the results for it should be much better than flash 4 and I remember you doing tests for it to validate this.  If flash 4.1 does not fit, test it on open router as well"

## The five (from Wednesday's 07:3x research, /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-12_new-local-model-research/research.md: read it whole)
1. DeepSeek V4.1 Flash 1017. TRY TO FIT IT ON THE SPARK. The model card's 763B is too big at 4-bit (about 380 GB, arithmetic), but the 10-26 / 10-27 seats ran V4 Flash at very low bit (iq1m, iq2xxs) with SSD offload: read 0_Brain/reference/2026-10-26_deepseek-quant-on-spark/ and 2026-10-27_deepseek-ssd-on-spark/ whole and reuse that method. If no quant that loads exists, or it loads and is unusably slow, say so with the measurement. ALSO re-run the hosted arm (`ab.py --model v41hosted`) once more: Kam asked for OpenRouter "as well", and a second hosted run measures the noise of the 10-27 single run.
2. NVIDIA Nemotron-3.5-Super-VL-120B-A12B (NVFP4): on the Spark (NVIDIA's card lists a 1x DGX Spark vLLM setup).
3. Aleph Alpha Kolibri-1 (FP8, about 78 GB): on the Spark.
4. Liquid LFM2.5-24B-A2B: on the Spark.
5. Xiaomi MiMo-V2.6-Flash: does NOT fit the Spark (about 170 GB at its MLX build); the Studio is not here. Run it HOSTED on OpenRouter IF a provider offers it with the SAME privacy pins as 10-27 (data_collection deny, zdr true, no fallbacks). If none does, it is NOT run: say so. Wednesday's reading of Kam's message: OpenRouter is his stated fallback for models that do not fit, so it covers MiMo too. It was offered to him for correction.

## Method (the 10-27 bar, unchanged)
- "The same questions as before" = /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark-ab/tasks.json (T01-T23), run by `ab.py` with the SAME prompts (prove byte identity against the recorded rounds, as 10-27 did), temperature 0, the same max_tokens, the same checker per task, one request at a time, thinking OFF where the model allows it (prove it: reasoning tokens 0).
- Read ab.py, BRIEF.md and the 10-27 report (0_Brain/reference/2026-10-27_v41-hosted-trial/report.md) whole first. Add a model arm by COPY AND MV, never an in-place edit of a running file. Re-run `--model control` after your edits: all 23 recorded verdicts must reproduce, else STOP.
- Per model: results_<model>.tsv beside ab.py (ids, verdicts, clause names, tokens, seconds; no code), full jsonl under runs/ (gitignored). Record the serving command, the quant, load time, and prefill/decode speed from a measured call.

## Box discipline (the Spark is shared and is the production local tier)
- BEFORE any swap: record the current serving state (the container, image, command, model, port) to a file. The Spark is idle at the commission (queue empty, written reason 07:18). Re-check that no round is running (`local-model/spark/spark_status` or the drainer pid). If one is, WAIT.
- AFTER the last local model: RESTORE DeepSeek V4 Flash exactly as recorded and prove it with one known task (T01 PASS) before you report. A Spark left on a test model is a failure of this commission.
- Disk: measure free space on the Spark before each download; never delete a model a seat uses; downloaded test weights go in a folder named for this test so they can be cleared on Kam's word (archive or remove only with his word, rule 2026-09-29).
- Memory: one model loaded at a time; unload before the next.

## Money and data
- OpenRouter spend cap $10 for the whole commission (10-27 cost $0.06 for 23 tasks). Use a SEPARATE budget file, as 10-27 did. Print the cost per hosted run from usage.cost.
- The prompts carry Secuura code. Hosted calls ONLY with data_collection deny + zdr true + pinned provider + no fallbacks (Kam's 10-27 10:06 terms). If a provider cannot be pinned that way, that model is NOT run hosted.
- Downloads come from the vendors' official HF repos or the named MLX/NVFP4 builds in the research file. No other source.

## Output
`report.md` in THIS folder, BLUF first: a table of task x model (PASS / FAIL with clause), each model's total out of 23 against V4 Flash 16/23 and V4.1-hosted 17/23 (10-27), speed per model, cost, what did not run and why, and what the result does NOT measure (single run at temperature 0; one task flipping is within noise, as 10-27 said). No ranking prose beyond the numbers. If your Write is refused, return the text in full.

Constraints: no cd, no rm (quarantine), never print a secret or key, no push, no PR, no board or Linear write, no mail. Read-only git in any Secuura checkout with GIT_OPTIONAL_LOCKS=0. Stop and report if the Spark becomes unreachable, a round starts, or the restore fails.
