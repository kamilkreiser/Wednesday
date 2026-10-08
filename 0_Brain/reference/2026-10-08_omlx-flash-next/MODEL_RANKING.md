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
