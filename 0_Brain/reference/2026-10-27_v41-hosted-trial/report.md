# DeepSeek V4.1 Flash (17 Oct) hosted trial, 2026-10-27

**BLUF: V4.1 Flash 17/23 vs V4 Flash 16/23 (verdict columns of results_v41hosted.tsv and results_deepseek.tsv), a difference of +1. Rule "buy the second 256 GB box only if V4.1 beats V4 Flash by at least 3 tasks": NOT met.**
Tasks V4.1 lost that V4 won: T08, T12, T15. Tasks V4.1 won that V4 lost: T04, T16, T18, T19. Single run at temperature 0; one task flipping is within noise of this set.

| task | rung | expected | V4 Flash | V4.1 Flash (hosted) |
|---|---|---|---|---|
| T01 | R1 | CAN | PASS | PASS |
| T02 | R1 | CAN | PASS | PASS |
| T03 | R1 | CAN | PASS | PASS |
| T04 | R1 | PARTIAL | FAIL (A2a) | PASS |
| T05 | R1 | PARTIAL | FAIL (A2a) | FAIL (A1) |
| T06 | R2 | CAN | PASS | PASS |
| T07 | R2 | CAN | PASS | PASS |
| T08 | R2 | CAN | PASS | FAIL (A2a) |
| T09 | R3 | CAN | PASS | PASS |
| T10 | R3 | CAN | PASS | PASS |
| T11 | R3 | CAN | PASS | PASS |
| T12 | R3 | PARTIAL | PASS | FAIL (A3x) |
| T13 | R4 | PARTIAL | PASS | PASS |
| T14 | R4 | PARTIAL | PASS | PASS |
| T15 | R4 | PARTIAL | PASS | FAIL (A2a) |
| T16 | R6 | PARTIAL | FAIL (A2a) | PASS |
| T17 | R4 | CANNOT | FAIL (A2a) | FAIL (A2a) |
| T18 | R4 | CANNOT | FAIL (A2a) | PASS |
| T19 | R3 | CANNOT | FAIL (B3x) | PASS |
| T20 | R3 | CANNOT | FAIL (B3x) | FAIL (B3x) |
| T21 | R2 | CAN | PASS | PASS |
| T22 | R3 | PARTIAL | PASS | PASS |
| T23 | R2 | CAN | PASS | PASS |

## Facts
- Provider actually used (response `provider` field, every call): DeepInfra. Pinned order DeepInfra, only deepinfra, allow_fallbacks false, data_collection deny, zdr true, quantizations fp8. OpenRouter lists DeepInfra fp8 in three tiers (flex/base/priority); the response does not say which tier served, only fp8 was permitted. Quantization reported by the endpoint listing: fp8.
- Thinking: requested OFF with `reasoning: {"enabled": false}`. Proven on T01 (proof run) and across all 23: reasoning_tokens total 0, thinking_chars 0, no think leak (the harness would have marked HARNESS otherwise).
- Cost (OpenRouter usage.cost): $0.0632 for the 23 tasks (+ $0.0022 for the T01 proof call), cap $5.00.
- Tokens: 595838 prompt + 43845 completion. Model wall-clock summed: 371 s (16.1 s per task).
- Same prompts (byte identity proven for all 23 against each Spark round's meta), temperature 0, max_tokens 16384, same checker per task. One request at a time.
- Local modes regression: `--model control` re-run after the edit reproduced all 23 recorded verdicts (results_control_recheck1027.tsv, identical to results_control.tsv on id/verdict/clause).

## What this does NOT measure
FP8 hosted weights of the 17 Oct build, not a 2/3/4-bit quant on a 256 GB Mac and not 1-bit. Local speed is untested (hosted seconds say nothing about a Mac). Different build from V4 Flash 0731, so the delta mixes model version with nothing else but is not a quantization-loss measure. N=1 per task.

## Instrument errors and UNMEASURED
- Unmeasured tasks: none (no clone failures, no HARNESS verdicts).
- Instrument notes: ab.py gained a hosted arm (backup-free edit via copy and mv). The budget file for this run is runs/v41hosted/budget.json (separate from hosted/state/budget.json, which was not touched), and the proof call's cost sits in runs/v41hosted_proof/. The V4 Flash baseline was a different build served from the Spark with `chat_template_kwargs.thinking=false`; the hosted arm uses OpenRouter's `reasoning.enabled=false`, an equivalent but not identical switch. Results tsv has no cost column (same columns as the others); cost is in meta and results.jsonl. A proof run (label `proof`) wrote results_v41hosted_proof.tsv and results_control_recheck1027.tsv beside the others.
