# Hosted replay results: 48 Spark tasks, three hosted models (2026-10-09)

**BLUF:** On the same 48 Secuura tasks, each with byte-identical inputs and the same checker, **MiMo-V2.6-Flash passed 46/48, GLM-5.3-Flash 45/48, and DeepSeek V4 Flash 43/48, against the Spark's 43/48.** Total spend was $0.45 against the $5 cap. MiMo is the only model that passed every task the Spark passed. **Differences of 1-3 tasks out of 48 are small: indicative, not decisive.**

## Results (parsed by column from `2_Project_Files/local-model/hosted/done_<model>.md`, latest row per task)
| model (provider, quant) | PASS | both PASS | this model only | Spark only | cost (usage.cost) |
|---|---|---|---|---|---|
| MiMo-V2.6-Flash (DeepInfra, fp8, thinking off) | **46/48** | 43 | 3 | **0** | $0.160 |
| GLM-5.3-Flash (Z.AI, fp8, thinking LOW, cannot be disabled) | 45/48 | 42 | 3 | 1 | $0.197 |
| DeepSeek V4 Flash (DeepInfra, fp8, thinking off) | 43/48 | 42 | 1 | 1 | $0.076 |
| Spark (local DeepSeek V4 Flash, reference) | 43/48 | — | — | — | $0 |

## How (instrument + controls)
- Harness: `2_Project_Files/local-model/hosted/replay.py`. Every request was pinned to the named provider, with zero data retention, data collection denied and fp8. The prompts are the Spark's own `input.json`, and the checker is the Spark's own.
- Parser control: the same column parse reproduces GLM's figures recorded at 18:40 (45/48, 42/3/1).
- MiMo first lost 4 tasks to a provider 429. Those were re-run (resume only), and all 4 PASSED.

## What this does NOT show
- **Small sample, and the tasks were briefed for the Spark:** the 48 tasks were chosen and briefed to suit the Spark, and that may flatter the Spark or models like it.
- GLM ran with low thinking; the others ran with none. Speed on our own hardware is unmeasured (this was hosted fp8, not a local quant).
- Whether MiMo runs well on a 256 GB Studio is still **unmeasured**: the 4-bit size (~164 GB) is arithmetic, and there is no published measured footprint.
