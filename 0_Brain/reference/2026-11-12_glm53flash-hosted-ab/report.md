# GLM-5.3 Flash, hosted, on the Spark A/B task set (T01-T23) - 2026-11-12 ~13:3x-14:1x AEDT

## BLUF
- **GLM-5.3 Flash (hosted): 20/23 PASS.** FAIL: T07 (B3b), T16 (A1, no patch: hit max_tokens 16384 with finish_reason=length, 15,368 reasoning tokens spent), T18 (A2a).
- **Pinned provider: DeepInfra, fp4 (tag `deepinfra/fp4`)**, `only:[deepinfra]`, `allow_fallbacks:false`, `data_collection:deny`, `zdr:true`, `quantizations:[fp4]`. All 23 responses report `provider: DeepInfra`.
- **Reasoning could NOT be turned off.** `reasoning:{enabled:false}` returned HTTP 400 "Reasoning is mandatory for this endpoint and cannot be disabled". Run with reasoning ON (default); 32,323 reasoning tokens over 23 tasks (of 72,828 completion tokens). This differs from the other arms, which ran with thinking off, so it is not a like-for-like arm.
- **Cost: $0.1169 for the 23 tasks** (sum of usage.cost); budget file `runs/glm53flash1112_budget.json` total **$0.1338** against the $2 cap (includes one refused HTTP 400 call booked at worst case $0.0132, and a 1-task probe of T01 at $0.0037).
- **Speed:** 580.7 s model time over 23 tasks = **25.2 s/task** (range 4.8 s T20 to 75.5 s T16). Checker time excluded.

## Comparison (totals from the tsv files; same 23 tasks)
| Arm | Total | Fails | Model time (sum) | Source |
|---|---|---|---|---|
| V4 Flash local (Spark) | 16/23 | T04 T05 T16 T17 T18 T19 T20 | 1320 s | results_deepseek.tsv |
| V4.1 hosted, 10-27 | 17/23 | T05 T08 T12 T15 T17 T20 | 371 s | results_v41hosted.tsv |
| V4.1 hosted, 11-12 rerun | 19/23 | T08 T15 T17 T20 | 302 s | results_v41hosted_rerun1112.tsv (23 rows, complete) |
| MiMo hosted (Cohere fp8) | 19/23 | T15 T16 T17 T18 | 408 s | results_mimohosted.tsv (23 rows, complete) |
| **GLM-5.3 Flash hosted (DeepInfra fp4, reasoning ON)** | **20/23** | T07 T16 T18 | 581 s | results_glm53flash.tsv |

## GLM-5.3 Flash, task x verdict
| Task | Rung | Expect | Verdict | Clause | Tokens in+out | Model s | Spark (recorded) |
|---|---|---|---|---|---|---|---|
| T01 | 1 | CAN | PASS | - | 18784+1816 | 12.6 | PASS |
| T02 | 1 | CAN | PASS | - | 32985+1049 | 8.8 | PASS |
| T03 | 1 | CAN | PASS | - | 13852+1827 | 14.2 | PASS |
| T04 | 1 | PARTIAL | PASS | - | 13031+1526 | 14.4 | FAIL |
| T05 | 1 | PARTIAL | PASS | - | 30785+1452 | 9.5 | FAIL |
| T06 | 2 | CAN | PASS | - | 15929+825 | 8.6 | PASS |
| T07 | 2 | CAN | **FAIL** | B3b | 17999+1076 | 13.4 | PASS |
| T08 | 2 | CAN | PASS | - | 33819+1972 | 23.6 | PASS |
| T09 | 3 | CAN | PASS | - | 21201+2325 | 16.2 | PASS |
| T10 | 3 | CAN | PASS | - | 16942+1551 | 25.9 | PASS |
| T11 | 3 | CAN | PASS | - | 39646+3995 | 22.2 | PASS |
| T12 | 3 | PARTIAL | PASS | - | 68671+3327 | 21.4 | PASS |
| T13 | 4 | PARTIAL | PASS | - | 17060+4017 | 41.5 | PASS |
| T14 | 4 | PARTIAL | PASS | - | 20150+880 | 9.5 | PASS |
| T15 | 4 | PARTIAL | PASS | - | 14342+5945 | 58.3 | PASS |
| T16 | 6 | PARTIAL | **FAIL** | A1 | 21638+16384 | 75.5 | PASS |
| T17 | 4 | CANNOT | PASS | - | 24803+3726 | 24.3 | FAIL |
| T18 | 4 | CANNOT | **FAIL** | A2a | 25322+3323 | 60.1 | FAIL |
| T19 | 3 | CANNOT | PASS | - | 12950+943 | 8.0 | FAIL |
| T20 | 3 | CANNOT | PASS | - | 13723+943 | 4.8 | FAIL |
| T21 | 2 | CAN | PASS | - | 16123+4876 | 42.6 | PASS |
| T22 | 3 | PARTIAL | PASS | - | 62160+4325 | 23.1 | PASS |
| T23 | 2 | CAN | PASS | - | 18072+4725 | 42.2 | PASS |

T07: 30 reasoning tokens, finish stop, clause B3b. T16: finish_reason=length, content 3,750 chars, no patch extracted. T18: finish stop, 931 reasoning tokens.

## Privacy pin evidence (step 1)
- `GET /api/v1/models/z-ai/glm-5.3-flash/endpoints` (read 13:0x) listed, among others: Relace fp4, Wafer nvfp4, PrimeIntellect, OpenInference (status -2), DeepInfra `deepinfra/fp4` status 0, 100% uptime. The per-model endpoints response has NO data-policy or ZDR field (fields: name, tag, quantization, status, uptime, pricing, supported_parameters, ...).
- ZDR evidence is `GET /api/v1/endpoints/zdr` (1081 rows): it lists `DeepInfra | z-ai/glm-5.3-flash-20260826`, tag `deepinfra/fp4`, quantization fp4, status 0. Same list also has Z.AI fp8, Wafer nvfp4/us and others.
- Pin used: provider order/only DeepInfra, no fallbacks, `data_collection:deny`, `zdr:true`. `assert_or_routing` refuses any request without exactly this pin, and the run stops if the response's provider is not deepinfra (all 23 served by DeepInfra). `data_collection:deny` is a request-side routing constraint; the endpoints API does not expose a per-endpoint data-collection field, so it was not independently read from an endpoint record. Same basis as the 10-27 and MiMo arms.
- Why DeepInfra: it was the 10-27 provider and is the only DeepInfra tier listed for this model (fp4); not chosen for quality.

## Method and checks
- Model id read from the API at run time: `z-ai/glm-5.3-flash` (not :batch, flashx, or `~z-ai/glm-flash-latest`). Listed price $0.0000000399 / $0.0000000784 per token is Relace's; the pinned DeepInfra rate is $0.00000015 / $0.0000005, used for the budget reservation.
- ab.py edited by copy and mv twice; backups `ab.py.pre-1112-glm53flash` and `ab.py.pre-1112-glm53flash-reasoning`. Changes: the `glm53flash` arm (pin above, `thinking_forced:true`, no `reasoning` field sent), and the budget tag now uses the model's own quant.
- `--model control --label glm1112 --nm-source .../work/nm_src_1112`: **23/23 recorded verdicts reproduced** (17 PASS), results_control_glm1112.tsv. The control ran after the first (arm-only) edit and before the reasoning edit; the second edit touches only the hosted branch (control makes no model call).
- Prompts byte-identical to the recorded rounds (sha256 + prompt_bytes proof passed for all 23). Temperature 0, max_tokens 16384, one request at a time, same checker.
- Budget: the first T01 attempt (reasoning disabled) got HTTP 400 and was booked at worst case $0.0132; the T01 probe and the full run followed. 26 budget entries, none left reserved.
- Spark not touched. Read-only state check (step 5): `0_Brain/reference/2026-11-12_five-model-ab/report.md` does **not exist** (folder holds commission.md, RECOMMISSION.md, RECOMMISSION2.md, serving_state_before*.txt). results_mimohosted.tsv: 23 rows (19/23), complete; results_mimohosted_proof.tsv 1 row. results_v41hosted.tsv: 23 rows (17/23); results_v41hosted_rerun1112.tsv: 23 rows (19/23); results_v41hosted_proof.tsv 1 row. No other arm was run.
- Artefacts: `spark-ab/results_glm53flash.tsv`, `results_glm53flash_probe.tsv` (T01 probe), `runs/glm53flash/` (gitignored, full outputs), `runs/glm53flash.log`.

## What this does NOT measure
- A single run at temperature 0; one task flipping is within noise (V4.1 moved 17 to 19 between two runs of the same arm). 20 vs 19 vs 19 is not a separable difference.
- Reasoning was ON for this arm and OFF for the V4 Flash and V4.1 arms (MiMo's setting as recorded in its own run). Output-token counts, speed and cost are not comparable across arms for that reason; T16's length failure is a direct consequence of reasoning consuming the 16,384 max_tokens.
- fp4 quantisation at DeepInfra; a different provider or tier could behave differently. Speed is hosted network plus provider load at ~13:30-14:10, not hardware throughput.
- Tasks are 23 Secuura tasks from one codebase; no generalisation beyond them. The Spark's recorded verdicts are from earlier days, same checker (control reproduced).
