# Five-model A/B on the Spark task set (T01-T23), 2026-11-12: report written from existing results

Written after the fact from the recorded tsv files; no run, API call or model was touched to produce it. Spark baselines are the recorded rounds; all other arms ran 2026-11-12 (hosted, via OpenRouter, privacy-pinned).

## BLUF
- Totals out of 23 (verdict column, count of PASS): **V4 Flash local (Spark) 16**, **V4.1 Flash hosted 10-27 17**, **V4.1 Flash hosted 11-12 rerun 19**, **MiMo-V2.6-Flash hosted (Cohere fp8) 19**, **GLM-5.3 Flash hosted (DeepInfra fp4, reasoning ON) 20**. Sources: results_deepseek.tsv, results_v41hosted.tsv, results_v41hosted_rerun1112.tsv, results_mimohosted.tsv, results_glm53flash.tsv (each 23 data rows).
- V4.1 hosted moved 17 -> 19 between two runs of the same arm (results_v41hosted.tsv vs results_v41hosted_rerun1112.tsv): that is the noise floor of this set; a one- or two-task gap between arms is inside it.
- Did NOT run: the local Nemotron-3.5-Super, Kolibri-1, LFM2.5 and V4.1-local (UD-IQ1_S) arms. RECOMMISSION2.md item 5 forbade any local Spark swap that session (three DevMASTER drive drops that day). There is no results tsv for any of them.
- Spark restore proof: `results_deepseek_restore1112.tsv` T01 = PASS (09:15:25, BYTE-IDENTICAL prompt), V4 Flash serving.
- Cost (OpenRouter usage.cost, budget files): MiMo $0.1001, V4.1 rerun $0.065, GLM $0.1169; total of the two shared-budget arms $0.1651 against a $10 cap (runs/fivemodel1112_budget.json). V4.1 10-27: $0.0632 (10-27 report).

## Task x arm (verdict column; clause = fail_clause column)
Columns: V4 = V4 Flash local, results_deepseek.tsv. V4.1a = hosted 10-27, results_v41hosted.tsv. V4.1b = hosted 11-12, results_v41hosted_rerun1112.tsv. MiMo = results_mimohosted.tsv. GLM = results_glm53flash.tsv.

| task | rung | expected | V4 | V4.1a | V4.1b | MiMo | GLM |
|---|---|---|---|---|---|---|---|
| T01 | 1 | CAN | PASS | PASS | PASS | PASS | PASS |
| T02 | 1 | CAN | PASS | PASS | PASS | PASS | PASS |
| T03 | 1 | CAN | PASS | PASS | PASS | PASS | PASS |
| T04 | 1 | PARTIAL | FAIL (A2a) | PASS | PASS | PASS | PASS |
| T05 | 1 | PARTIAL | FAIL (A2a) | FAIL (A1) | PASS | PASS | PASS |
| T06 | 2 | CAN | PASS | PASS | PASS | PASS | PASS |
| T07 | 2 | CAN | PASS | PASS | PASS | PASS | FAIL (B3b) |
| T08 | 2 | CAN | PASS | FAIL (A2a) | FAIL (A2a) | PASS | PASS |
| T09 | 3 | CAN | PASS | PASS | PASS | PASS | PASS |
| T10 | 3 | CAN | PASS | PASS | PASS | PASS | PASS |
| T11 | 3 | CAN | PASS | PASS | PASS | PASS | PASS |
| T12 | 3 | PARTIAL | PASS | FAIL (A3x) | PASS | PASS | PASS |
| T13 | 4 | PARTIAL | PASS | PASS | PASS | PASS | PASS |
| T14 | 4 | PARTIAL | PASS | PASS | PASS | PASS | PASS |
| T15 | 4 | PARTIAL | PASS | FAIL (A2a) | FAIL (A2a) | FAIL (A2a) | PASS |
| T16 | 6 | PARTIAL | FAIL (A2a) | PASS | PASS | FAIL (A2a) | FAIL (A1) |
| T17 | 4 | CANNOT | FAIL (A2a) | FAIL (A2a) | FAIL (A2a) | FAIL (A2a) | PASS |
| T18 | 4 | CANNOT | FAIL (A2a) | PASS | PASS | FAIL (A2a) | FAIL (A2a) |
| T19 | 3 | CANNOT | FAIL (B3x) | PASS | PASS | PASS | PASS |
| T20 | 3 | CANNOT | FAIL (B3x) | FAIL (B3x) | FAIL (B3x) | PASS | PASS |
| T21 | 2 | CAN | PASS | PASS | PASS | PASS | PASS |
| T22 | 3 | PARTIAL | PASS | PASS | PASS | PASS | PASS |
| T23 | 2 | CAN | PASS | PASS | PASS | PASS | PASS |
| **total** | | | **16** | **17** | **19** | **19** | **20** |

Fails by arm: V4 T04 T05 T16 T17 T18 T19 T20; V4.1a T05 T08 T12 T15 T17 T20; V4.1b T08 T15 T17 T20; MiMo T15 T16 T17 T18; GLM T07 T16 T18.

## V4.1 hosted run-to-run (10-27 vs 11-12), task by task
Differing tasks only: T05 FAIL(A1) -> PASS; T12 FAIL(A3x) -> PASS. The other 21 verdicts are identical (table above). 17 -> 19.

## Speed and tokens (sums over the 23 rows of each tsv: model_s, prompt_tok, completion_tok)
| arm | model time | per task | prompt tok | completion tok | source |
|---|---|---|---|---|---|
| V4 Flash local (Spark) | 1320.2 s | 57.4 s | 595,815 | 43,775 | results_deepseek.tsv |
| V4.1 hosted 10-27 | 370.9 s | 16.1 s | 595,838 | 43,845 | results_v41hosted.tsv |
| V4.1 hosted 11-12 | 301.5 s | 13.1 s | 595,838 | 43,825 | results_v41hosted_rerun1112.tsv |
| MiMo hosted | 407.8 s | 17.7 s | 588,083 | 42,699 | results_mimohosted.tsv |
| GLM hosted | 580.7 s | 25.2 s | 569,987 | 72,828 | results_glm53flash.tsv |

Per-task figures are the sum divided by 23. Hosted seconds are network plus provider load, not hardware throughput. Spark prefill/decode tokens-per-second: not recorded in any tsv used here.

## Cost
| arm | cost | source |
|---|---|---|
| V4 Flash local | not recorded (local, no per-call cost) | n/a |
| V4.1 hosted 10-27 | $0.0632 for 23 tasks (+ $0.0022 proof call) | 2026-10-27_v41-hosted-trial/report.md |
| V4.1 hosted 11-12 | $0.065 (23 settled entries, model `v41hosted`) | runs/fivemodel1112_budget.json |
| MiMo hosted | $0.1001 (26 settled entries, model `mimohosted`; includes the T01 proof and repeated T01 calls, so it is above the 23-task cost; per-23-task figure not separated) | runs/fivemodel1112_budget.json |
| GLM hosted | $0.1169 for 23 tasks; budget file total $0.1338 incl. a refused HTTP 400 booked at worst case and a T01 probe | 2026-11-12_glm53flash-hosted-ab/report.md (runs/glm53flash1112_budget.json) |

## Providers and pins
- MiMo: pinned to Cohere fp8 (DeepInfra's MiMo endpoint was down), data_collection deny, zdr, no fallbacks (RECOMMISSION2.md; budget tag `cohere/fp8`).
- V4.1 11-12: pins as 10-27 (DeepInfra fp8; 10-27 report). Provider field of the 11-12 rerun: not re-read for this report.
- GLM: DeepInfra fp4, only:[deepinfra], no fallbacks, data_collection deny, zdr true (GLM report). Reasoning could not be disabled (endpoint HTTP 400 "Reasoning is mandatory"); 32,323 reasoning tokens, T16 hit max_tokens 16384 (finish length) -> A1. results_glm53flash.tsv shows finish values stop and length, thinking_chars sum 114,642.
- All other hosted rows: finish = stop on all 23, thinking_chars 0 (tsv columns). Reasoning-token counts are not a tsv column; "reasoning OFF" for them rests on the commission request and thinking_chars 0.

## What did NOT run, and why
- Nemotron-3.5-Super-VL-120B-A12B (NVFP4, local Spark): not run. Weights were downloaded and verified on the Spark in /home/datasec-rd/five-model-ab-1112/ (RECOMMISSION2.md); no serving test, no tsv.
- Kolibri-1 (FP8, local Spark): not run; weights downloaded and verified, same note.
- LFM2.5-24B-A2B (local Spark): not run; it failed to start on the NVIDIA vLLM 0.29 image (no sm_121 FlashAttention-2 kernel), per RECOMMISSION2.md.
- V4.1 Flash local (UD-IQ1_S, 233 GB): not run; the download and a llama.cpp image re-pull were still running at 08:55 per RECOMMISSION2.md. Their later state: not recorded in the files used here.
- Reason for all four: RECOMMISSION2.md item 5 deferred local swaps to a later commission after three drive drops.
- GLM-5.3 Flash was not one of the five in commission.md; it was added later and is reported as an extra arm.

## What this does NOT measure
- Single run at temperature 0 per arm. V4.1 hosted moved 17 -> 19 between two runs, so one or two tasks is within noise; 20 vs 19 vs 19 is not a separable difference.
- The GLM arm ran with reasoning ON because the endpoint refused to disable it; the other arms ran with thinking off. Tokens, speed and cost are not comparable across arms for that reason, and T16's length failure follows from it.
- Hosted quantisations differ (V4.1 fp8, MiMo fp8, GLM fp4) from the local V4 Flash on the Spark; hosted seconds say nothing about local hardware speed.
- No local arm of any of the four new models was measured, so nothing here says whether they fit or how fast they run on the Spark.
- 23 Secuura tasks from one codebase; no generalisation beyond them. V4 Flash and V4.1 are different builds.

## Files used (all in /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark-ab/)
- results_deepseek.tsv (24 lines = header + 23 rows), results_v41hosted.tsv (24), results_v41hosted_rerun1112.tsv (24), results_mimohosted.tsv (24), results_glm53flash.tsv (24).
- results_deepseek_restore1112.tsv (header + 1 row, T01 restore proof); results_mimohosted_proof.tsv (header + 1 row, not tabulated).
- runs/fivemodel1112_budget.json (cost). Control: results_control_recheck1112b.tsv and ...c.tsv, results_control_glm1112.tsv reproduced 23/23 recorded verdicts (RECOMMISSION2.md, GLM report); not re-read here.
- Not used: other results_*.tsv (iq1m, iq2xxs*, ornith, partial results_control_recheck1112.tsv, older deepseek_restore*, glm53flash_probe) belong to earlier or other arms.
- Reports read: commission.md, RECOMMISSION.md, RECOMMISSION2.md, 2026-10-27_v41-hosted-trial/report.md, 2026-11-12_glm53flash-hosted-ab/report.md.
