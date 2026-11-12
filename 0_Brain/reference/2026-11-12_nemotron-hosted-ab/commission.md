# Nemotron-3.5-Super-VL, HOSTED arm on the Spark A/B task set — operator commission, Wednesday (14:49 seat), 2026-11-12 ~15:02 AEDT. Operator model: Sonnet 5.5 (hosted-only measurement; no box surgery).

## Kam's words (live board, view=wednesday, verbatim)
14:52:59: "I read that the NVIDIA Nemotron 3.5 Super VL (120B-A12B) fits on a single NVIDIA DGX Spark.  can you confirm.  How did it perform in the tests compared to flash 4.  is it worth changing the model on our HP spark to it"
15:00:29: "can you please test it on openrouter"
A LOCAL run on the Spark is running in parallel by another operator (`0_Brain/reference/2026-11-12_nemotron-local-ab/`). DO NOT touch the Spark, its serving state, or that folder. Your edits to `ab.py` must not collide with that operator's: work by COPY AND MV, re-read ab.py immediately before your mv, and if it changed since you copied it, re-apply your change on the new copy. Use a SEPARATE results file and budget file.

## Model id (read by Wednesday from OpenRouter's public /api/v1/models at 15:01, never typed from memory)
`nvidia/nemotron-3.5-super-vl` ("NVIDIA: Nemotron 3.5 Super VL", context 1,048,576, prompt $0.00000015/token, completion $0.00000047/token). NOT the `:free` variant (free endpoints typically log/train on prompts; the prompts carry Secuura code). Re-read the id from the API yourself before the first call.

## Read WHOLE first
`/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-12_glm53flash-hosted-ab/commission.md` and its `report.md` (the identical recent method — follow it step for step, substituting this model), then the five-model folder's `commission.md`, `RECOMMISSION.md`, `RECOMMISSION2.md`.

## Do, in order (as the GLM commission)
1. **Privacy pins FIRST:** read `https://openrouter.ai/api/v1/models/nvidia/nemotron-3.5-super-vl/endpoints`. Usable ONLY if pinnable with data_collection deny + zdr true + no fallbacks. Name the provider and the fields. If none qualifies, STOP: report.md says so with the endpoint data; run nothing.
2. Add a `nemotronhosted` arm to `ab.py` by COPY AND MV, pinned, reasoning OFF if allowed (prove reasoning tokens 0; else record them and say it cannot be off).
3. `--model control` with `--nm-source 2_Project_Files/local-model/spark-ab/work/nm_src_1112` reproduces all 23 recorded verdicts, else STOP.
4. Run `--model nemotronhosted` T01-T23, temp 0, same max_tokens, one at a time. Budget file `runs/nemotronhosted1112_budget.json`, cap **$2**. Cost per call from usage.cost.
5. Append ONE row to `RESULTS_LOG.md` by copy-and-mv (re-read it immediately before the mv; the local operator may also append).

## Output
`report.md` in THIS folder, BLUF first: total out of 23 (task x verdict with clause) against V4 Flash local 16, V4.1 hosted 19, MiMo hosted 19, GLM-5.3 Flash 20 (from RESULTS_LOG), seconds per task, cost, pinned provider, what it does NOT measure (single run, temp 0, one flip is noise; hosted precision may differ from the local NVFP4 build). No ranking prose. If your Write is refused, return the text in full.

Constraints: exactly the GLM commission's (no cd — a hook refuses it; no bare `=====` shell word; no rm; never print a key — read OPENROUTER_API_KEY inside python from 4_Credentials/.env; no push, PR, board, Linear or mail). If /Volumes/DevMASTER drops: stop, wait, re-read the budget file before the next call.
