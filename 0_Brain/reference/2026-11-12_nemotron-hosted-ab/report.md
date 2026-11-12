# Nemotron-3.5-Super-VL HOSTED arm — report (operator's text, saved by Wednesday 2026-11-12 ~15:5x; the operator's Write was refused)

## BLUF
- **14/23 PASS** on OpenRouter, provider pinned CoreWeave nvfp4 (`only:[coreweave]`, no fallbacks, `data_collection:deny`, `zdr:true`, `quantizations:[nvfp4]`; on OpenRouter's ZDR list; same NVFP4 format as the local build). Reasoning OFF (0 reasoning tokens on all 23).
- FAILS: T05 A4 · T10 B2 · T11 A3x · T14 A1 (no patch) · T15 A2a · T16 A4 · T17 A3b · T18 A3b · T19 B3x.
- Cost $0.1128 (cap $2). Speed 118.0 s model time total, 5.1 s/task (2.4-9.1 s).
- Control: `--model control` reproduced all 23 recorded verdicts (17 PASS) — the first attempt was cut by the 15:01 stop and left an empty tsv; re-run in full as label nhost1112b.

| Arm | Total /23 | Fails |
|---|---|---|
| V4 Flash LOCAL (10-27) | 16 | T04 T05 T16 T17 T18 T19 T20 |
| V4.1 hosted (10-27) | 17 | T05 T08 T12 T15 T17 T20 |
| V4.1 hosted (11-12 rerun) | 19 | T08 T15 T17 T20 |
| MiMo hosted | 19 | T15 T16 T17 T18 |
| GLM-5.3 Flash hosted (reasoning ON) | 20 | T07 T16 T18 |
| **Nemotron hosted** | **14** | T05 T10 T11 T14 T15 T16 T17 T18 T19 |

Vs V4 Flash local, task by task: Nemotron hosted PASSES T04 and T20 where Flash failed; FAILS T10, T11, T14, T15, T16 where Flash passed.

## Task by task (rung · expect · verdict · tokens in+out · model s · V4 Flash local)
T01 1 CAN PASS 19960+1222 3.0 PASS · T02 1 CAN PASS 35689+655 3.3 PASS · T03 1 CAN PASS 14773+1694 5.5 PASS · T04 1 PARTIAL PASS 13838+1373 2.9 FAIL · T05 1 PARTIAL FAIL A4 32794+907 3.6 FAIL · T06 2 CAN PASS 17112+901 2.7 PASS · T07 2 CAN PASS 19629+1206 2.8 PASS · T08 2 CAN PASS 36594+2119 4.8 PASS · T09 3 CAN PASS 22751+2484 6.8 PASS · T10 3 CAN FAIL B2 18492+1693 5.6 PASS · T11 3 CAN FAIL A3x 42327+3708 7.0 PASS · T12 3 PARTIAL PASS 73009+3493 9.1 PASS · T13 4 PARTIAL PASS 18189+1292 5.5 PASS · T14 4 PARTIAL FAIL A1 21446+902 6.4 PASS · T15 4 PARTIAL FAIL A2a 15440+2115 4.9 PASS · T16 6 PARTIAL FAIL A4 23290+1819 4.6 PASS · T17 4 CANNOT FAIL A3b 26391+2796 6.9 FAIL · T18 4 CANNOT FAIL A3b 26936+2775 5.1 FAIL · T19 3 CANNOT FAIL B3x 13891+1040 2.4 FAIL · T20 3 CANNOT PASS 14704+1039 3.6 FAIL · T21 2 CAN PASS 17340+3079 6.8 PASS · T22 3 PARTIAL PASS 66482+2876 7.2 PASS · T23 2 CAN PASS 19946+3706 7.4 PASS

## Privacy pin evidence
Endpoints API read 15:0x: 9-10 endpoints (Darkbloom nvfp4, Io Net nvfp4, Crusoe bf16 status -2, CoreWeave nvfp4, PrimeIntellect nvfp4, Together, DeepInfra fp4, Venice fp4, BaseTen fp4, Nebius bf16); no data-policy field there. The ZDR list shows CoreWeave nvfp4 status 0, 100% uptime. `data_collection:deny` is a request routing constraint (same basis as earlier arms).

## Method
ab.py `nemotronhosted` arm by copy-and-mv with a hash re-check (backup ab.py.pre-1112-nemotronhosted; committed by Wednesday). A 3-variant probe (~$0.000013, outside the budget file) proved the pin is accepted and reasoning off. Prompts byte-identical to recorded rounds; temp 0; max_tokens 16384; one request at a time; same checker. Budget file runs/nemotronhosted1112_budget.json, 23 entries settled. RESULTS_LOG.md +1 row (backup RESULTS_LOG.md.pre-nemotronhosted). The Spark was not touched.

## What this does NOT measure
Single run at temp 0 (V4.1 moved 17 -> 19 between runs: a 2-task gap is within noise). Hosted precision/serving stack may differ from the local NVFP4 build: this arm does not predict the local result (local T01, T02 both PASS at 32.6 s / 27.9 s vs hosted 3.0 / 3.3 s, identical token counts; 21 local tasks pending at this report). Speed = hosted network + provider load 15:20-15:50, not Spark throughput. 23 tasks from one codebase.

Files: 2_Project_Files/local-model/spark-ab/results_nemotronhosted_nhost1112.tsv · results_control_nhost1112b.tsv · runs/nemotronhosted1112_budget.json · RESULTS_LOG.md.
