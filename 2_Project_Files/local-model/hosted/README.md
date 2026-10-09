# hosted/ — replay the Spark's Secuura tasks on hosted models (2026-10-09)

Kam, live board 17:26, card `wed-hosted-replay-key-and-code-1009` = a: replay our Spark local-model tasks on hosted
models through OpenRouter. Secuura code goes ONLY to zero-retention providers. US$5 cap.
Model facts and prices: `0_Brain/reference/2026-10-09_studio-128-vs-256/HOSTED_API.md` (re-confirmed by the public
`GET /api/v1/models/<id>/endpoints` on 2026-10-09).

| file | what |
|---|---|
| `replay.py --model mimo\|glm\|deepseek [--dry-run] [--only TAG,..] [--limit N] [--keep-clone]` | the replay |
| `check.sh <run> <tier> <tip> <work> [golden]` | round.sh steps 7/9/10: clone at the Spark's tip, the SAME checker, golden compare |
| `tests/test_replay.py` | 15 tests (below) |
| `done_<model>.md` | one row per replayed task (tracked, like `spark/done.md`) |
| `runs/ work/ state/` | gitignored — they hold Secuura code (see `.gitignore`) |

## Run it

1. Put the key in `4_Credentials/.env` as `OPENROUTER_API_KEY=...` (never on a command line; replay.py reads it by name
   and never prints or stores it — the request bodies carry no key).
2. Check: `python3 /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/hosted/replay.py --model deepseek --dry-run`
3. Run one model at a time, cheapest first:

       python3 /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/hosted/replay.py --model deepseek
       python3 /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/hosted/replay.py --model mimo
       python3 /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/hosted/replay.py --model glm

   A first smoke of one task: add `--limit 1`. Exit: 0 all PASS · 1 a FAIL verdict · 2 refused (no key, routing,
   budget, byte-identity) · 4 HTTP/shape · 5 HARNESS (checker leg / thinking leaked / wrong provider served) · 64 usage.

## What it sends, and where

- **Which tasks:** every `spark/done.md` row with a run dir — 48 today (49 rows; the REFUSED KS-1333 round has none).
  Repeated rounds (KS-948 ×3, KS-593 adminconfig ×2, KS-1355 dev-reload ×2, KS-1438 ×2) are separate inputs (their
  tips/inputs differ) and are each replayed.
- **The prompt, byte for byte:** the messages `lib/spark_call.py` built — system = `lm_call.SYSTEM_PREAMBLE` (imported)
  + `"\n\n"` + `spark-kit/01_FOR_THE_LOCAL_MODEL.md`; user = `"## TASK\n" + task.strip() + "\n\n## INPUT (JSON)\n" +
  input.strip() + "\n"`, from the Spark run dir's own `input.json` and the task file round.sh chose (run-dir `task.md`
  for the *2 tiers, `task_selftest.md` for self-testing bash). Before anything is built, `build_messages` PROVES it:
  `sha256(task + input)` must equal the Spark's `meta.sha256_task_plus_input` and the UTF-8 byte length of system +
  user must equal `meta.prompt_bytes`; either mismatch refuses that task. All 48 pass today. Same sampler as the Spark:
  temperature 0, max_tokens 16384 (GLM 32768, below).
- **Where:** `POST https://openrouter.ai/api/v1/chat/completions`, with provider routing
  `{"only": [<pin>], "allow_fallbacks": false, "zdr": true, "data_collection": "deny", "quantizations": ["fp8"]}`.
  `send()` calls `assert_routing` immediately before the network and REFUSES a body missing any of the four fields
  or carrying another value (test: a body without `zdr` never reaches the network function).

| `--model` | OpenRouter id | pinned provider | thinking | max_tokens | $/M in/out |
|---|---|---|---|---|---|
| `mimo` | `xiaomi/mimo-v2.6-flash` | DeepInfra fp8 | OFF: `reasoning.enabled=false` + `thinking.type=disabled` | 16384 | 0.14 / 0.28 |
| `glm` | `z-ai/glm-5.3-flash` | Z.ai fp8 | **effort "low"** (cannot be disabled) | 32768 | 0.15 / 0.50 |
| `deepseek` | `deepseek/deepseek-v4-flash-0731` | DeepInfra fp8 | OFF: `reasoning.effort=none` | 16384 | 0.06 / 0.18 |

- A response that shows reasoning for mimo/deepseek, or names a provider other than the pin, is recorded HARNESS
  (round.sh does the same for leaked thinking), not a model verdict.
- **Checker:** the hosted `out.md` (+ `.meta.json` with `done_reason`, which checker A1 reads) is written in
  spark_call.py's shape (same strip and unfenced-diff wrap, `DIFF_GRAMMAR` imported), then `check.sh` clones
  `spark/cache/src` at the Spark round's own tip and runs the SAME scripts round.sh ran for that tier
  (`spark_checker.sh` / `code_patch2/checker.sh` / `bash_patch/checker.sh` / `bash_patch2/checker.sh` + A2a), then the
  golden cmp / tree compare. The clone is removed after the check (`--keep-clone` keeps it); nothing is written under
  `!CODING/`.

## The cap

`state/budget.json` holds ONE running total for all three models. Each request is RESERVED at its worst case
(Spark prompt tokens × 1.3 + max_tokens, at the table's prices) before it is sent and SETTLED to the response's
`usage.cost` (or tokens × the prices when `cost` is absent) after. A request whose worst case would take the total
over `HOSTED_BUDGET_USD` (default 5.00) is refused and the drain stops; a crash or timeout mid-request leaves the worst
case charged. Pre-flight (from the 2026-10-09 dry-run, Spark's own token counts): **deepseek $0.080 · mimo $0.177 ·
glm $0.205+ (a FLOOR: its thinking tokens are unmeasured)**; worst cases $0.23 / $0.42 / $1.00 — all three ≤ $1.66
even at worst case. The budget file is per machine (gitignored): run all three from the same machine.

## NOT like-for-like with the Spark

- **GLM thinks.** GLM-5.3-Flash cannot disable thinking; it runs at effort "low" while the Spark ran thinking OFF, so
  it gets extra reasoning, and its max_tokens is 32768 (reasoning spends the same budget). Its cost and latency are
  not comparable; its verdicts favour it, if anything.
- **Weights/precision.** The Spark served a pruned DeepSeek V4 Flash 0731 as EXL3 3.0 bpw; the hosted runs are fp8
  (DeepSeek on DeepInfra = the unpruned 0731 at fp8; MiMo maps to `MiMo-V2.6-Flash-RL` fp8). A deepseek gap between
  hosted and Spark measures quantisation + pruning, not the model.
- **Tokenizer/usage.** Prompt token counts differ by model; the Spark's own counts are only the estimate's basis.
- **Thinking-off field for MiMo** is OpenRouter's `reasoning.enabled=false` plus the provider-native field from the
  litellm note; whether DeepInfra honours either is checked per response (reasoning chars must be 0, else HARNESS).
- **Base:** each replay is checked at the Spark round's own tip (from its `round.json`), not today's develop — the same
  tree the Spark's patch was judged against.

## Tests (`python3 -m unittest discover -s local-model/hosted/tests -v`; `HOSTED_SKIP_CHECKER=1` skips the ~2 min clones)

routing green for all 3 models + red (no `zdr` → refused, network function never called, nothing charged; each field
missing or wrong → refused) · budget red at the cap with a fake usage feed (2 sent, 3rd refused), cost-absent computed
from tokens, cap shared across models, `main()` stops the drain at the cap and never prints the key · dry-run makes
zero network calls with the socket layer blocked (control: the block catches a real attempt) · missing key = rc 2, one
line · byte identity on 3 real inputs (code_patch KS-723, bash_patch KS-998, code_patch2 KS-1410 = 70,129 B, the
QWEN122_AB reference) + red (one byte changed → refused) · checker positive controls on real Spark outputs: KS-998
PASS (TREE-IDENTICAL), KS-723 code_patch PASS (prepare_clone + jest), KS-1438 r2 FAIL at B3x — each reproduces the
recorded RESULT / SPARK RESULT lines and golden · end to end: `main()` with a fake POST returning the Spark's own KS-998 answer -> out.md -> check.sh -> PASS TREE-IDENTICAL row in done_deepseek.md, clone removed, no key in request.json.
