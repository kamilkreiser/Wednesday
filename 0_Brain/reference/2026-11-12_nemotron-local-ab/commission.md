# Nemotron-3.5-Super-VL LOCAL arm on the Spark A/B task set — operator commission, Wednesday (14:49 seat), 2026-11-12 ~14:55 AEDT. Operator model: Opus 5.5 (box surgery: a Spark model swap and restore; routing v1.0 Opus row for deploy-with-box-rights, as the five-model commission).

## Kam's words (live board 14:52:59, view=wednesday, verbatim)
"I read that the NVIDIA Nemotron 3.5 Super VL (120B-A12B) fits on a single NVIDIA DGX Spark.  can you confirm.  How did it perform in the tests compared to flash 4.  is it worth changing the model on our HP spark to it"
Wednesday's panel reply (bf-dcc2039b9c7c9e9a): not tested yet; she will run it on the Spark against the same 23 questions and put Flash 4 back, about an hour.

## Read WHOLE first
In `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-12_five-model-ab/`: `commission.md` (Method, BOX DISCIPLINE, Output — all stand), `RECOMMISSION.md`, `RECOMMISSION2.md`, `report.md`. Then `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark-ab/ab.py` (it already has a `nemotron` arm added by the 11-12 operator: read it, check it targets the local server you will start), `BRIEF.md`, `RESULTS_LOG.md`.

## Do, in order
1. Spark idle check: `python3 /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/spark_status.py` (Wednesday read IDLE, queue 0, no round at 14:53). Note: a gate (gate 330) may call the Spark for a one-request shadow review; if a request is in flight, wait for it; a swap simply makes later shadow calls fail, which the gate is told to tolerate.
2. RECORD the current serving state (container, image, command, model, port) to `serving_before.txt` in THIS folder.
3. Serve Nemotron-3.5-Super-VL-120B-A12B NVFP4 from the verified weights in `/home/datasec-rd/five-model-ab-1112/` per NVIDIA's single-Spark vLLM setup. FIT is the first answer Kam wants: record load success/failure, memory used, load time, max context you could set. If it does not load or is unusably slow, that IS the result: say so with the measurement, restore, stop.
4. `--model control` must reproduce all 23 recorded verdicts (with `--nm-source 2_Project_Files/local-model/spark-ab/work/nm_src_1112`), else STOP.
5. Run `--model nemotron` T01-T23, same prompts, temperature 0, same max_tokens, thinking OFF where the model allows (prove: reasoning tokens 0; if it cannot be off, say so and record them), one request at a time. results_nemotron.tsv beside ab.py; jsonl under runs/. Record prefill/decode tok/s from a measured call.
6. RESTORE DeepSeek V4 Flash exactly as recorded in step 2 and prove it with `ab.py --model deepseek --only T01 --label restore1112b --nm-source …` = PASS. A Spark left on the test model is a failure of this commission.
7. Append ONE row to `RESULTS_LOG.md` (same columns) by copy-and-mv.

## Output
`report.md` in THIS folder, BLUF first: does it fit (measured), total out of 23 with task x verdict, against V4 Flash local 16/23, V4.1 hosted 19, MiMo 19, GLM-5.3 Flash 20 (read from RESULTS_LOG); speed vs V4 Flash on the Spark if V4 Flash's speed is on record (else say not recorded); memory headroom left for the Spark's other routines; what it does NOT measure (single run, temp 0, one flip is noise). No recommendation prose — Wednesday writes that for Kam. If your Write is refused, return the text in full.

Constraints: exactly the five-model commission's (no cd — a hook refuses even the word in a command; no bare `=====` shell word; no rm (quarantine); never print a secret or key; no push, PR, board, Linear or mail; no hosted calls needed). Do not delete or move any weights. If /Volumes/DevMASTER drops: stop, wait, re-read what you wrote, check the Spark's serving state, then resume or restore.
