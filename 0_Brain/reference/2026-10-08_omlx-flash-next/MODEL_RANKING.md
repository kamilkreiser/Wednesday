---
date: 2026-10-08
type: reference
source: model-ranking research sub-agent (commissioned 16:57 on Kam's ask); saved by Wednesday from the agent's returned text. Part 1 of 2: the Ornith-sibling and all-routes widening (Kam ~17:1x) was sent to the same agent and returns separately.
status: live
---

# Best model for the 96 GiB M3 Ultra (part 1)

> ⚠ **Wednesday's correction, measured on this Mac on 2026-10-08 (17:04 and 17:11), which the agent did not have:**
> Qwen3.8-Flash-Next does NOT run here alongside the fleet, even with every app quit.
> - First run: oMLX refused it by 80 MB (72.65 GB needed against a 72.57 GB dynamic ceiling).
> - Second run, with the memory guard on `aggressive`: wired memory reached 56G and swap grew more than 800 MB within 2 s, so Wednesday's guard killed the server.
> - So the agent's #1 is **not usable here in practice.**
> - The practical budget is about **60–65 GB of model**, with two Claude seats and macOS live.
> - **On that budget the agent's own table points to #2, Qwen3.8-27B (17 GB 4-bit / 30 GB 8-bit), as the realistic pick.** #4 Qwen3-Coder-Next (already on disk) is the zero-download fallback.

## Agent's bottom line (as returned; every speed is a community measurement on an M3 Ultra / 96 GB, none run here)

**Flash Next has the strongest coding scores of anything that fits on paper.** At a 32K-token prompt it decodes at 44–70 tok/s and reads the prompt at 952–1,077 tok/s.

**Stronger models (GLM-5.3-Flash, DeepSeek-V4.1-Flash, MiMo-V2.6-Flash) need 90–152 GiB even at 2-bit.** They would have to stream experts from the SSD, which has not been measured on any 96 GB Mac. The nearest published figures are 12–16 tok/s on a 128 GB M5 Max and about 1–1.6 tok/s on a 48 GB M4 Pro.

**Qwen3.8-27B is the runner-up**, a dense model at 17 GB (4-bit) or 30 GB (8-bit):
- SWE-bench Pro 61.7, against Flash Next's 62.5.
- DeepSWE 42.2, against 58.7 (it is weaker on agentic work).
- It fits beside Ornith.
- Prompt reading is slow, about 390 tok/s at 32K, so a 25K-token prompt waits roughly a minute for its first token.

**Licence:** the agent read Qwen Community 1.0. Internal use is allowed. A separate licence is needed only to sell a hosted model service or coding-assistant product, or (for the display rules) above 100M MAU or US$20M monthly revenue.

## Ranked table (quality first, then speed)

| # | Model | Total / active | Size | Fit | Runtime | M3U/96 GB speed at 32K | Coding (maker's) | Context | Licence |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Qwen3.8-Flash-Next oQ4e-mtp | 125B / 6B, plus a 51B table | 106 GB (about 74 GB resident) | Table on the SSD | oMLX 0.7 | Prompt 952–1,077, decode 44–70 [B1] | SWE-Pro 62.5 · DeepSWE 58.7 · LCB v6 91.9 · SWE-Multi 81.0 [C1] | 262K | Qwen Community 1.0 |
| 2 | **Qwen3.8-27B** oQ4e / oQ8e | 27B dense | 17 / 30 GB | Resident | oMLX | Q4: prompt 391, decode 65.9 · Q8: prompt 291, decode 62.9 [B2] | SWE-Pro 61.7 · Terminal-Bench 2.1 73.0 · DeepSWE 42.2 · LCB v6 90.3 [C2] | 262K | Apache-2.0 |
| 3 | Qwen3.5-122B-A10B oQ4-mtp | 122B / 10B | 72.9 GB | Resident, tight (like #1, too big here in practice) | oMLX | Prompt 517–648, decode 42–59 [B3] | SWE-V 72.0 · Terminal-Bench 2 49.4 · LCB v6 78.9 [C3] | 262K | Apache-2.0 |
| 4 | **Qwen3-Coder-Next** (ON DISK) | 80B / 3B | 44.8 GB MLX 4-bit (51.7 GB in our Ollama store) | Resident | oMLX / MLX | Prompt 1,283–1,342, decode 49–65 [B4] | SWE-V 70.6 · SWE-Pro 44.3 · Terminal-Bench 2.0 36.2 · Aider 66.2 [C4] | 262K | Apache-2.0 |
| 5 | gpt-oss-120b (ON DISK) | 117B / 5.1B | 63.4 GB | Resident (borderline here) | oMLX / Ollama | Prompt 754–857, decode 31–60 [B5] | SWE-V 62.4 · Aider polyglot 44.4 [C5] | 131K | Apache-2.0 |
| 6 | GLM-5.3-Flash | 320B / 18B | 90 GiB Q2 | Expert streaming | ds4 / oMLX | Unmeasured on 96 GB; 128 GB M5 Max 12–15 [D2] | DeepSWE 63.4 · Terminal-Bench 2.1 84.3 [C6] | — | MIT |
| 7 | DeepSeek-V4.1-Flash | 552B, 8–16B active, plus a 196B Engram table | 152 GiB Q2 | Streaming + Engram on the SSD | ds4 / oMLX | Unmeasured; about 16 on a 128 GB M5 Max [D3] | DeepSWE 74.2 · Terminal-Bench 2.1 90.6 [C7] | 1M | MIT |
| 8 | Step-3.7-Flash, 2-bit | 198B / about 11B | — | Resident at 2-bit | oMLX | 8K: prompt 469, decode 39.6 [B6] | SWE-Pro 56.3 (full precision); 2-bit quality unmeasured [C8] | 256K | Apache-2.0 |

## Evidence gaps (agent)
- None of these was measured on our box. The community numbers mix builds and MTP settings.
- The scores are mostly the makers' own: SWE-Pro for the newest models, SWE-V for older ones, so there is no common yardstick. DeepSWE v1.1 is the closest: Flash Next 58.7, GLM-5.3-Flash 63.4, MiMo 67.9, V4.1-Flash 74.2, Qwen3.8-27B 42.2.
- There is no independent measure of 4-bit quality (oMLX's 100-question samples are noisy), and no quality data at all for 2-bit or pruned variants.
- SSD expert or Engram streaming has not been measured on any 96 GB Mac.
- Our own task shape (20–30K-token briefed patches) has not been tested on any of these.

## Sources (agent's list, abbreviated)
**Model cards:**
- C1: huggingface.co/Qwen/Qwen3.8-Flash-Next (and its LICENSE)
- C2: Qwen/Qwen3.8-27B
- C3: Qwen/Qwen3.5-122B-A10B
- C4: Qwen/Qwen3-Coder-Next
- C5: openai/gpt-oss-120b and arxiv 2508.10925 Table 3
- C6: zai-org/GLM-5.3-Flash
- C7: deepseek-ai/DeepSeek-V4.1-Flash
- C8: stepfun-ai/Step-3.7-Flash
- C9: XiaomiMiMo/MiMo-V2.6-Flash-RL
- C10: mistralai/Mistral-Small-4-119B-2603

**Speeds:** omlx.ai/benchmarks/performance/<id>
- B1: 5qfskq4q, rjljbjnf, ip5iukwh, si6ti9o5, m5lpwu1b
- B2: e8xc8oci, x9kd5f5f, bopebjcc, 3dprl1it
- B3: tdw6tx8i, 7z2jc2fo, awgp0exu
- B4: 8gd5zkr2, xjf1c9yp, myr8non8
- B5: r8zj8266, 4odzn4sz, qb844csb
- B6: y2qhj32t, 0tj9l68t

**Runtimes:**
- github.com/jundot/omlx (releases; PR #3865; issue #3574)
- github.com/antirez/ds4 (docs/MODELS.md, SSD_STREAMING.md, PERFORMANCE.md)
- evanwtf/local-llm issue #321

---

# Part 2 — Ornith identified, every route ranked (agent's text, saved by Wednesday 17:2x)

## Recommendation (agent)
**Ornith‑1.5‑35B‑A3B at 8‑bit (~37 GB) for the Mac.**
- It is the newer version of the same family we run.
- It fits the measured 60–65 GB budget with the fleet up.
- It has the fastest published speeds on an identical Mac.
- The publisher reports it is well above 1.0.

**First test:** an A/B on the night queue against Qwen3.8‑27B 8‑bit (~30 GB), one at a time. They can't both be resident.

**Flash Next:** fleet-quiet windows only; never the daily driver.

## Ornith identified (manifests + GGUF headers)
- `ornith:35b` (Q4_K_M, 21.17 GB) and `ornith:35b-q8_0` (36.90 GB) = **Ornith‑1.0‑35B**, deepreinforce‑ai, MIT.
  - 256 experts, 8 active (~3B active).
  - 262,144 context; `qwen35moe` architecture (Qwen3.5‑35B‑A3B base).
- The Ollama library holds only 1.0. **Ornith 1.5 is on Hugging Face:** 9B; **35B‑A3B** (GGUF Q4 21.7 / Q8 37.8 GB; MLX 4‑bit 19.5 / 8‑bit 36.8 GB); 397B (~17B active; Q4 244 GB). The 397B fits on nothing we have, the Mac and Spark together included (217 GB).

**Publisher scores, 1.0‑35B → 1.5‑35B‑A3B → 1.5‑397B:**

| Benchmark | 1.0‑35B | 1.5‑35B‑A3B | 1.5‑397B |
|---|---|---|---|
| SWE‑V | 75.6 | **79** | 86 |
| SWE‑Pro | 50.4 | **59.6** | 65.1 |
| TB2.1 | 64.2 | **67.8** | 86.1 |
| DeepSWE | 0 | **22** | 56 |
| NL2Repo | 34.6 | **46.2** | 59.5 |

The 1.5 scores use OpenHands for SWE and Claude Code for DeepSWE, averaged over 5 runs.

## Our own records (counted)
**Ornith 1.0** (`night/done.md`):
- 470 graded runs: 337 PASS / 133 FAIL (71.7%).
- **From 09‑17 on: 255 PASS / 42 FAIL (85.9%).**
- 148 of 164 queue items passed at least once.
- Median turn: 12,945 tokens in, 989 out, 26 s wall (~43 output tok/s, Ollama).

**Spark, DeepSeek V4 Flash** (`spark/done.md`):
- 46 rows: 42 PASS, 3 FAIL, 1 REFUSED (10‑05 to 10‑07).
- A different, later task set, so not a head‑to‑head with Ornith.

## Ranked for this Mac (fits = within 60–65 GB with the fleet up)
Speeds are oMLX community rows on an M3U/60c/96GB, prefill / decode tok/s.

1. **Ornith‑1.5‑35B‑A3B**, MIT, 8‑bit 36.8 GB.
   - Speed: 8‑bit at 16K 1,933 / 158.2 [4iguebdl]; 4‑bit at 32K 1,753 / 126.5 [8ue0u0sx].
   - Est. ~26 s for a 25K‑in, 1.5K‑out turn.
   - SWE‑V 79, SWE‑Pro 59.6, TB2.1 67.8, DeepSWE 22.
2. **Qwen3.8‑27B**, Apache, oQ8e 30 GB.
   - Speed at 32K: 291–391 / 63–66.
   - Est. ~90–110 s per turn.
   - SWE‑Pro 61.7, TB2.1 73.0, DeepSWE 42.2. Better scores, but prefill is 4–6× slower.
3. Flash Next. Does NOT fit with the fleet (measured); quiet windows only.
4. Qwen3‑Coder‑Next (on disk). Speed 1,342 / 65.3. SWE‑V 70.6, SWE‑Pro 44.3.
5. gpt‑oss‑120b (on disk). 63.4 GB, borderline.
6. Not on the live budget:
   - Qwen3.5‑122B (72.9 GB).
   - GLM‑5.3‑Flash and DeepSeek‑V4.1‑Flash (streaming only, unmeasured at 96 GB).

## Routes
- **Mac:** Ornith 1.5 > Qwen3.8‑27B > Flash Next (quiet only) > Coder‑Next > gpt‑oss.
- **Spark:** unchanged, the medium tier (stronger by vendor scores than anything on the Mac's live budget; 93% PASS on ours).
- **Both:** no route pools memory for one model. The practical form is a checker‑gated cascade: Mac Ornith 1.5 → Spark → cloud. This is the agent's design inference, unmeasured.
- **Cloud (Opus 5.5):** the top tier. Its figures are second‑hand; there is no cloud baseline on our harness.

## Gaps
- No speed here was measured on our machine.
- Vendor harnesses differ, by up to 8 points for the same model.
- Ornith 1.5 has never run on our harness, and its chat template/parser under Ollama is unknown. oMLX runs the MLX build directly.
- No 4‑bit vs 8‑bit coding‑quality data.

## Next step
Download `ornith-ai/Ornith-1.5-35B-A3B-MLX-8bit` (36.8 GB). Re‑run the 20 most recent night‑queue items Ornith 1.0 already graded, then A/B it against Qwen3.8‑27B on the same items.

**Licence (Flash Next):** internal use is free. A separate licence is needed only to sell inference or an AI coding/office product.

## Sources (agent)
**Model cards:**
- deepreinforce-ai/Ornith-1.0-35B
- ornith-ai/Ornith-1.5-35B-A3B (‑GGUF, ‑MLX-8bit, ‑MLX-4bit) and Ornith-1.5-397B
- ollama.com/library/ornith/tags
- Qwen/Qwen3.8-27B (Jundot oQ4e/oQ8e)
- Qwen3.8-Flash-Next (+ LICENSE)
- Qwen3-Coder-Next
- gpt-oss-120b
- GLM-5.3-Flash
- DeepSeek-V4.1-Flash and V4-Flash-0731

**oMLX:** rows 4iguebdl, 1h5tnslo, 8ue0u0sx, e8xc8oci, bopebjcc, 4vwvolmh, 5qfskq4q, rjljbjnf, si6ti9o5, m5lpwu1b, 8gd5zkr2, myr8non8, r8zj8266, 4odzn4sz, tdw6tx8i; PR #3865; issue #3574.

**ds4:** docs MODELS/SSD_STREAMING/PERFORMANCE; evanwtf/local-llm #321.

**Cloud (second‑hand):** llm-stats.com and benchlm.ai Opus 5.5 pages.
