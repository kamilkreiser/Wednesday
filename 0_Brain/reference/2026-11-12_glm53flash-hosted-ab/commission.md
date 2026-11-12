# GLM-5.3 Flash, HOSTED arm on the Spark A/B task set — operator commission, Wednesday (12:3x seat), 2026-11-12 ~13:0x AEDT. Operator model: claude-sonnet-5-5 (hosted-only measurement; no box surgery).

## Kam's words (live board 13:03:56, view=wednesday, verbatim)
"can you please use open router and test GLM-5.3 Flash against the questions"
Wednesday's reading: "the questions" = the same task set the five-model A/B used today (Kam's 07:40 "using the same questions as before"): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark-ab/tasks.json` T01-T23, run by `ab.py`.

## Model id (read by Wednesday from OpenRouter's public /api/v1/models at 13:0x, never typed from memory)
`z-ai/glm-5.3-flash` ("Z.ai: GLM 5.3 Flash", context 1,048,576, prompt $0.0000000399/token, completion $0.0000000784/token). NOT the `:batch`, `flashx` or `~z-ai/glm-flash-latest` variants. Re-read the id from the API yourself before the first call.

## Read WHOLE first
`/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-12_five-model-ab/commission.md`, `RECOMMISSION.md`, `RECOMMISSION2.md` (the method, the privacy pins, the budget-file pattern, the `--nm-source` checker fix; every constraint there stands). Then `ab.py`, `BRIEF.md` and the 10-27 report (`0_Brain/reference/2026-10-27_v41-hosted-trial/report.md`).

## Do, in order
1. **Privacy pins FIRST:** read `https://openrouter.ai/api/v1/models/z-ai/glm-5.3-flash/endpoints`. A provider is usable ONLY if it can be pinned with data_collection deny + zdr true + no fallbacks (Kam's 10-27 10:06 terms). Name the provider you pin and the endpoint fields that show it. If NO provider qualifies, STOP: write report.md saying so with the endpoint data, run nothing.
2. Add a `glm53flash` hosted arm to `ab.py` by COPY AND MV (never an in-place edit of a running file), pinned as above, thinking/reasoning OFF if the model allows it (prove it: reasoning tokens 0; if it cannot be turned off, say so and record the reasoning tokens).
3. Re-run `--model control` with `--nm-source 2_Project_Files/local-model/spark-ab/work/nm_src_1112` after your edit: all 23 recorded verdicts must reproduce, else STOP.
4. Run `--model glm53flash` over T01-T23, same prompts (byte identity with the recorded rounds, as before), temperature 0, same max_tokens, one request at a time, `--nm-source` as above. A SEPARATE budget file `runs/glm53flash1112_budget.json`, cap **$2** (the whole 23 should cost cents); print the cost per call from usage.cost.
5. Read-only state check for Wednesday: does `0_Brain/reference/2026-11-12_five-model-ab/report.md` exist, and which results_*.tsv files exist for mimohosted / v41hosted (row counts)? Report it; do NOT run those arms.

## Output
`report.md` in THIS folder, BLUF first: GLM-5.3 Flash total out of 23 (task x verdict with clause), against the recorded totals of the other arms you can READ from their tsv files (V4 Flash local 16/23 and V4.1 hosted 17/23 on 10-27; MiMo hosted and V4.1 hosted 1112 only if their tsv files are complete, else say "incomplete"); speed (seconds per task); cost; the pinned provider; what it does NOT measure (single run at temperature 0; one task flipping is within noise). No ranking prose beyond the numbers. If your Write is refused, return the text in full.

Constraints: no cd (a hook refuses it, even the word in prose), no bare `=====` shell word, no rm (quarantine), never print a secret or key (read OPENROUTER_API_KEY inside python from 4_Credentials/.env, never in argv), no push, no PR, no board or Linear write, no mail. Do NOT touch the Spark's serving state (hosted only). Read-only git with GIT_OPTIONAL_LOCKS=0 in any Secuura checkout. If /Volumes/DevMASTER drops: stop, wait, re-read the budget file before the next call.
