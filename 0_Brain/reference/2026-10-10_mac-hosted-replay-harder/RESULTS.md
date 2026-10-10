---
date: 2026-10-10
type: reference
source: test sub-agent for Wednesday. Kam ruled card wed-mac-purchase-test-first-1010 = (a) at ~20:56 AEDT; extended 20:58:21 (flagship on SSD), 21:00:03 / 21:02:26 ("Ornith-397B"), 21:11:45 (512 GB question). Runs 21:03–22:2x AEDT.
status: live
---

# Hosted replay, harder set: MiMo / GLM / V4 Flash vs the Spark (2026-10-10)

**Tags.** [ours: file] = our files · [run] = this replay (`done_<model>.md` beside this file) · [web: URL, read 2026-10-10] · [arith] = arithmetic, inputs shown · **UNMEASURED** = no source.

## BLUF
- **On the 13 harder runnable tasks: MiMo-V2.6-Flash 10/13, GLM-5.3-Flash 10/13, hosted DeepSeek V4 Flash 6/13, the Spark 6/13** [run; Spark from `spark/done.md` + run-dir `round.json`].
- **The gap is in the briefs the Spark failed:** MiMo and GLM each passed **5 of the Spark's 7 FAILs**. Those 7 are the FIRST-round briefs that Wednesday later re-briefed. MiMo and GLM coped with the brief as first written. Each lost 1 of the Spark's 6 PASSes: the KS-1410 loose brief, on an off-by-one hunk header (A2a).
- **Hosted V4 Flash (the Spark's model at fp8) matched the Spark's count but not the same tasks:** +2 / −2.
- **Spend: US$0.1505** against the US$5 cap (harness `state/budget.json`, 93 entries, all settled), plus about US$0.00002 for three harmless provider probes outside the harness.
- **Flash Next:** it IS on OpenRouter (`qwen/qwen3.8-flash`, HF id `Qwen/Qwen3.8-Flash-Next`), but only on Alibaba, which is not zero-retention. OpenRouter refused the zdr pin with 404 "No endpoints found matching your data policy". **Not run and not substituted.** Running it means sending Secuura code to a retaining provider, which is Kam's call.
- **Ornith-397B:** it exists (Qwen3.5-MoE layout, 512 experts, 10 routed + 1 shared, ~17B active). It is **not on OpenRouter** (0 of 458 models read today), so it could not be added. It is **not viable as a lane on a 256 GB Studio** (§4).
- **Decision rule (REPORT §5):** this result **does not yet meet the "buy 256" condition.** That condition needs Sonnet-built tickets passing at the **Opus gate**, and both are untested here. It does **not** trigger "buy nothing" either, because MiMo and GLM did **better** than the Spark on harder tickets, not merely matched it. Next step: gate a sample of the PASS diffs (§3), then replay Sonnet-built tickets once they have Spark-format inputs.

## 1. Task set (13 runnable, 3 not runnable)
Inputs are the Spark's own run-dir `input.json` (+ `task.md` for the *2 tiers). The harness proved them byte-identical to what the Spark sent: `sha256(task+input)` and `prompt_bytes` matched for 13/13 [run, dry-run line]. Selection list: scratchpad `replay1010/tasks_done.md`.

| # | Task (Spark run dir) | Why chosen | Tier | Spark |
|---|---|---|---|---|
| 1 | 10-05 KS-1278-revoke-atomic (r1) | Spark FAIL | code_patch2 | FAIL A3 |
| 2 | 10-05 KS-948-mixed-backtick (r1) | Spark FAIL | code_patch | FAIL B4 |
| 3 | 10-05 KS-593-adminconfig-negative-offset (r1) | Spark FAIL | code_patch | FAIL A3d |
| 4 | 10-08 KS-1438-html-docs-check-resolved-paths (r1) | Spark FAIL | bash | FAIL B3x |
| 5 | 10-09 KS-1438-…-r2 | Spark FAIL, **round counter spent** (`spark/queue.md` :14 "counter spent → Claude seat") | bash | FAIL B3x |
| 6 | 10-10 KS-1417-p1-env-example-dead-gateway-port (r1) | Spark FAIL (unclosed fence) | code_patch | FAIL B1 |
| 7 | 10-05 KS-1278-revoke-atomic-r2 | Spark FAIL (round.json; not a done.md row) | code_patch2 | FAIL |
| 8 | 10-07 KS-1410-apigw-batch-audit-export-500 | QWEN122_AB hard 5 | code_patch2 | PASS |
| 9 | 10-07 KS-1410-apigw-notifications-500 | QWEN122_AB hard 5 | code_patch | PASS |
| 10 | 10-05 KS-1278-revoke-atomic-r3 | QWEN122_AB hard 5 | code_patch2 | PASS |
| 11 | 10-05 KS-593-share-null-recipient-cp2 | QWEN122_AB hard 5 | code_patch2 | PASS |
| 12 | 10-05 KS-1136-aggregate-unreadable-artefacts | QWEN122_AB hard 5 | bash | PASS |
| 13 | 10-10 KS-1410-apigw-audit-export-502-loose | loose brief (rung 4) | code_patch | PASS |

**NOT RUNNABLE (no input invented):**
- **KS-1456-loose:** the brief exists (`night/briefs/KS-1456-run-migrations-failed-run-message-loose/`), but no Spark round was ever run on it, so there is no `input.json` and no Spark verdict. Building one needs `round.sh` (steps 4–6), which writes into `spark/state` and `spark/cache`, outside this test's write scope.
- **KS-1434 and the other Sonnet-built tickets:** they have no Spark-format input.
- **KS-1229-R16B-LOOSE:** an Ornith brief with no Spark run.

## 2. Results (parsed from `done_<model>.md`, latest PASS/FAIL row per task)
| # | Task | Spark | V4 Flash hosted | MiMo | GLM |
|---|---|---|---|---|---|
| 1 | KS-1278 r1 | FAIL | FAIL | FAIL | FAIL |
| 2 | KS-948 r1 | FAIL | FAIL | FAIL | FAIL |
| 3 | KS-593 adminconfig r1 | FAIL | **PASS** | **PASS** | **PASS** |
| 4 | KS-1438 r1 | FAIL | FAIL | **PASS** (byte-identical) | **PASS** (byte-identical) |
| 5 | KS-1438 r2 (counter spent) | FAIL | FAIL | **PASS** (byte-identical) | **PASS** (byte-identical) |
| 6 | KS-1417 p1 r1 | FAIL | **PASS** | **PASS** | **PASS** |
| 7 | KS-1278 r2 | FAIL | FAIL | **PASS** | **PASS** |
| 8 | KS-1410 batch | PASS | PASS | PASS | PASS |
| 9 | KS-1410 notifications | PASS | FAIL (A2a; checker 7/7) | PASS | PASS |
| 10 | KS-1278 r3 | PASS | FAIL (A3x) | PASS | PASS |
| 11 | KS-593 share cp2 | PASS | PASS | PASS | PASS |
| 12 | KS-1136 aggregate | PASS | PASS | PASS | PASS |
| 13 | KS-1410 502 loose | PASS | PASS | FAIL (A2a off by +1; checker 7/7) | FAIL (A2a off by +1; checker 7/7) |
| | **PASS** | **6/13** | **6/13** | **10/13** | **10/13** |
| | Spark FAIL → model PASS | — | 2 | 5 | 5 |
| | Spark PASS → model FAIL | — | 2 | 1 | 1 |
| | cost (usage.cost, settled) | $0 | $0.0274 | $0.0523 | $0.0707 |

- **Tasks 1–2 fail for every model and the Spark.** On task 1 MiMo's and GLM's patch trees are golden-identical but stop at A3 ("cannot sequence red-first without exactly one test file"). That looks like a brief/checker-shape fault in the r1 brief, not a model fault (inference; Wednesday to judge).
- **Stability of the 10-09 run on the overlapping 9 tasks (temperature 0):** GLM 0 flips; hosted V4 Flash 1 flip (KS-1410 notifications PASS on 10-09, FAIL at A2a today); MiMo 0 flips on the same 9 (8 of them now on Makora, not DeepInfra). Hosted temperature-0 output is **not fully deterministic** [run vs `hosted/done_*.md`].
- **Hosted V4 Flash vs the Spark (same model):** hosted fp8 unpruned vs the Spark's pruned EXL3 3.0 bpw. +2/−2 on 13 is noise-sized; no quality gap shown.

### Controls and deviations (read before quoting)
- **Same harness, unmodified:** `2_Project_Files/local-model/hosted/replay.py` + `check.sh`, pointed by its own env vars at this folder (`runs/`, `state/` gitignored here; `git check-ignore` verified). Clones went to scratch (`replay1010/work`) and were removed after each check. No Secuura checkout was written (check.sh clones from `spark/cache/src` with read verbs only).
- **Routing:** every request pinned `only:[provider]`, `allow_fallbacks:false`, `zdr:true`, `data_collection:"deny"`, `quantizations:["fp8"]`, and asserted before send.
- **MiMo provider changed mid-run (deviation):** DeepInfra returned "xiaomi/mimo-v2.6-flash is temporarily rate-limited upstream" on 6/6 attempts for tasks 2, 3, 4 and 5 (rows `SKIPPED-RATE-LIMIT`). A harmless-prompt probe at 22:1x then showed DeepInfra still 429 while Makora, Venice and Io Net answered. **MiMo task 1 ran on DeepInfra fp8; tasks 2–13 ran on Makora fp8** (OpenRouter ZDR list; wrapper `replay1010/bin/mimo_makora.py` overrides only the provider pin and price). The 10-09 MiMo figures were all DeepInfra.
- GLM thinks at effort "low" (it cannot be disabled), as on 10-09. MiMo and V4 Flash ran with thinking off; the harness verified 0 reasoning chars (no HARNESS rows).
- DeepSeek also hit DeepInfra 429s (18 retries in the log) but completed all 13.

## 3. PASS diffs for Wednesday's Opus-gate sample (paths relative to this folder)
Not gated here; that needs a QA seat. 26 PASSes in total.
- **The 10 that beat the Spark (gate these first):**
  - MiMo: `runs/mimo/hosted_mimo_2026-10-10_spark_secuura_2026-10-05_KS-593-adminconfig-negative-offset-r2/`, `…_2026-10-08_KS-1438-html-docs-check-resolved-paths-r2/`, `…_2026-10-09_KS-1438-html-docs-check-resolved-paths-r2-r2/`, `…_2026-10-10_KS-1417-p1-env-example-dead-gateway-port-r2/`, `…_2026-10-05_KS-1278-revoke-atomic-r2/`.
  - GLM: `runs/glm/hosted_glm_2026-10-10_spark_secuura_2026-10-05_KS-593-adminconfig-negative-offset/`, `…_2026-10-08_KS-1438-html-docs-check-resolved-paths/`, `…_2026-10-09_KS-1438-html-docs-check-resolved-paths-r2/`, `…_2026-10-10_KS-1417-p1-env-example-dead-gateway-port/`, `…_2026-10-05_KS-1278-revoke-atomic-r2/`.
  - (V4 Flash hosted: `runs/deepseek/…KS-593-adminconfig-negative-offset/`, `…KS-1417-p1-env-example-dead-gateway-port/`.)
- **Each diff is at `<run dir>/out.md.checker/patch.diff`.** The full list of 26 is in scratchpad `replay1010/passdiffs.txt`; it can be regenerated from the `run dir` column of the PASS rows in `done_*.md`.

## 4. Kam's SSD question and the Ornith-397B flagship
**What "SSD offload" means on a Mac.** In an MoE model each token uses only a few experts. If the weights do not fit in unified memory, a runtime can keep the always-used weights (attention, shared expert, router) resident and **read the routed experts, or a lookup table, from the SSD on demand**. That is done by mmap plus the OS page cache, or by an explicit expert cache. Speed then depends on the cache-hit rate and the SSD read rate, not only on memory bandwidth.

**Is it "only Flash Next"? No.** Flash Next's specific trick is offloading its **51B n-gram table (PLE)**. oMLX 0.7.0 does that for that model only: `OMLX_QWEN4_PLE_MODE=mmap` in its `qwen4_exp` patch [ours: `2026-10-08_omlx-flash-next/REPORT.md`]. oMLX's README describes only a KV-cache SSD tier, not weight offload [web: github.com/jundot/omlx, read 2026-10-10]. Other runtimes stream **experts** for other models:
- **ds4 (antirez):** "SSD streaming keeps a bounded cache of routed experts and reads missing experts from the GGUF". On Metal it covers DeepSeek and GLM. On a 128 GB M5 Max: **GLM 5.3 Flash Q4_K (177.77 GiB) 121 t/s prefill, 11.9 / 14.9 t/s generation**; DeepSeek Flash Vision Exp MXFP4 300 t/s prefill, 11.9 / 19.3 t/s generation. It publishes no resident baseline. "Generation is usually more sensitive to cache misses than prefill." [web: raw.githubusercontent.com/antirez/ds4/main/docs/SSD_STREAMING.md, read 2026-10-10]
- **flash-moe (danveloper):** Qwen3.5-397B-A17B on an **M3 Max 48 GB** with a 17.5 GB/s SSD. 4-bit experts: **4.36 tok/s** (3.90 baseline); 2-bit 5.74 tok/s ("Breaks JSON/tool calling"). Disk 209 GB (4-bit), about 6 GB RAM, about 71% page-cache hit rate. **It runs K=4 routed experts per layer**, where the model's config says 10 [web: github.com/danveloper/flash-moe, read 2026-10-10; HF config read 2026-10-10]. That makes it a reduced model.
- V4.1 by SSD streaming on an M5 Max 128: 8.3 / 61 tok/s [ours: 10-09 REPORT.md, row zycxgdnr].

**Speed cost, Flash Next:** table offloaded on an M3 Ultra 96 GB, decode 62–65 tok/s on fresh prompts vs about 80 on repeats; ms/token ≈ 12.5 + 0.139 × page-ins [ours: 10-08 REPORT, oMLX #4140]. Fully resident on bigger Macs: M5 Max 128 78.2 decode / 2,525 prefill at 32K; M5 Ultra 87.8 decode at 16K [ours: 10-10 REPORT §3].

**Flash Next vs the Spark's DeepSeek V4 Flash:**
- **Our tasks:** UNMEASURED. It was not run (no ZDR endpoint), and the 96 GB Studio could not load it (HTTP 507 at 72.65 GB on 10-08 [ours: 10-10 REPORT §2]).
- **Speed/fit:** about 2× the Spark's decode and about 2.4× its prefill on a 128 GB M5 Max (78.2 / 2,525 vs 37.13 / 1,032 [ours: REPORT §3]), in about 74 GB resident [ours: 10-08 REPORT]. It fits a 128 GB box alone, but not beside the fleet with Ornith.
- **Makers' score:** DeepSWE 58.7 vs 54.4 for the Spark's model [ours: MODEL_RANKING.md; 10-09 REPORT]. That figure is not ours.

**Ornith-397B (Kam 21:02:26):**
- **Layout:** `ornith-ai/Ornith-1.5-397B`, MIT, `qwen3_5_moe`. 60 layers, 512 experts, 10 routed + 1 shared per token, 262K context [HF config, read 2026-10-10]. About 17B active [ours: MODEL_RANKING.md]. Also published as 1.0-397B and 1.5-397B-DFlash.
- **Sizes:**
  - BF16 403.4B params, 806.8 GB.
  - FP8 418.4 GB.
  - NVFP4 (CUDA) 241.8 GB.
  - GGUF Q4_K_M 244.3 GB, Q8_0 428.5 GB.
  - Same-architecture MLX 4-bit (Qwen3.5-397B-A17B) 223.9 GB [ours: 10-09 REPORT].
- **Published Apple-silicon runs:** **none for Ornith-397B** (search 2026-10-10 found none).
  - Same architecture, resident, 4-bit, M3 Ultra 512 GB: **36.0 / 34.4 tok/s decode, 420 / 506 prefill at 1K / 4K, peak 209.7 / 211.5 GB** [web: omlx.ai/benchmarks/679bs0za, read 2026-10-10].
  - Same architecture, SSD-streamed: flash-moe above (4.36 tok/s at K=4 on 48 GB).
  - A 256 GB SSD-streamed run of either: UNMEASURED.
- **Viability on a 256 GB Studio: not viable as a lane.**
  - 4-bit needs about 210 GB at peak (measured on the 512 GB box), against a default GPU budget of 206–223 GB on 256 GB [ours: 10-09 REPORT].
  - So it runs fully resident only with the wired limit raised and the box doing nothing else: no Ornith 1.5, no agent fleet, no checkers.
  - Streaming some experts from SSD would free room, but the only runtime published for this layout (flash-moe) cuts the experts to 4 of 10 and was measured at 4.36 tok/s. On 256 GB the cache-hit rate would be far higher, but that speed is UNMEASURED.
  - Even resident, prefill of 420–506 tok/s puts a 25K-token prompt at about 50–60 s before the first token [arith: 25,000 / 506 to 25,000 / 420], against about 24 s on the Spark [arith: 25,000 / 1,032].
  - **It is also not on OpenRouter**, so it could not be replayed on our tickets. **Not added; nothing substituted.**
- **The DeepSeek / MiMo / GLM flagships** (Kam's 20:58 wording, before the Ornith correction) are larger still. On 256 GB they would also be SSD-streamed, so they were not added either (§5 has sizes).

## 5. What a 512 GB M5 Ultra Studio adds (Kam 21:11:45)
- **Availability / price:**
  - Apple AU shop page today: footer "512GB memory option for M5 Ultra coming late October". No 512 GB price in the page data [web: apple.com/au/shop/buy-mac/mac-studio, read 2026-10-10].
  - Spec page: "512GB unified memory (M5 Ultra with 36-core CPU and 80-core GPU)", no price, bandwidth "1.2TB/s" [web: apple.com/au/mac-studio/specs/, read 2026-10-10].
  - So the floor is the 36c/80c base, A$11,449 [shop page data], plus an unpublished memory price: **UNMEASURED**.
- **What fits fully in memory on 512 GB but not on 256 GB** (budget ≈ 0.81 × 512 ≈ 415 GB, extrapolated from our 96 GB [ours: REPORT §6]; sizes [HF API, read 2026-10-10]):

  | Model | Size | 512 GB | Beside Ornith 1.5 8-bit (36.8 GB) + fleet? |
  |---|---|---|---|
  | **Ornith-397B 4-bit** | 224–244 GB | **Yes, resident, no SSD** | Yes (about 261–281 GB) [arith] |
  | Ornith-397B 8-bit | Q8_0 428.5 GB | No (over the extrapolated budget) | No |
  | **MiMo-V2.6-Flash 8-bit** (309B) | ≈309 GB [arith] | Yes: the **same precision as the hosted fp8 runs that scored 10/13 and 46/48** | Tight (≈346 GB) [arith] |
  | V4 Flash 8-bit (284B) / GLM-5.3-Flash 8-bit (320B) | ≈284 / ≈320 GB [arith] | Yes | Tight |
  | GLM-5.3 flagship (753B; FP8 755.6 GB) | 4-bit ≈377 GB [arith] | Alone, tight | No |
  | MiMo-V2.6-Pro (1.02T; 573.5 GB as shipped) | 4-bit ≈512 GB [arith] | No | No |
  | DeepSeek V4 Pro 0813 (1.65T; 892.7 GB as shipped) | 4-bit ≈825 GB [arith] | No | No |

- **Speed:** the bandwidth is the same 1.2 TB/s as the 256 GB Ultra, so the same model decodes at the same speed. Decode is bounded by active bytes per token:
  - Ornith-397B 4-bit: ≈17B × 0.5 B ≈ 8.5 GB per token → ceiling ≈ 141 tok/s [arith]. The measured same-architecture figure is 34–36 tok/s on an M3 Ultra (above).
  - MiMo 8-bit: 15B active × 1 B ≈ 15 GB → ceiling ≈ 80 tok/s, half the 4-bit ceiling [arith]. Measured 4-bit on the M5 Ultra is 68.6–73.6 [ours: REPORT §3]. 8-bit is UNMEASURED; expect it lower (inference).
  - Every M5 Ultra 512 GB figure: UNMEASURED.
- **Allowance:** 512 GB mainly buys **running a flagship (Ornith-397B) or 8-bit Flash models locally**. Neither is shown to save more allowance than 256 GB at today's quality bar:
  - the models that beat the Spark here (MiMo, GLM Flash) already fit 256 GB at 4-bit;
  - 4-bit vs fp8 quality on our tickets is UNMEASURED;
  - Ornith-397B's quality on our tickets is UNMEASURED (not hosted).
  - The allowance saved by any configuration is UNMEASURED (REPORT §6). Inference: the extra over 256 GB is a capability and precision purchase, not an allowance one.

## 6. NOT MEASURED / owed
- **The Opus gate** on any PASS (§3): needs a QA seat.
- **Sonnet-built tickets:** no Spark-format inputs exist. **KS-1456-loose:** never run by the Spark.
- **Flash Next on our tickets:** blocked on the retention ruling.
- **Ornith-397B and all flagships on our tickets.**
- **4-bit / 8-bit local quality of MiMo and GLM;** every M5 Ultra 256 / 512 tok/s figure for these models.
- **The 512 GB price.**
- **Variance:** one sample per model per task; hosted temperature 0 flipped 1 of 9 for V4 Flash.

## Sources (read 2026-10-10)
- **OpenRouter:**
  - `openrouter.ai/api/v1/models` (458 models; raw JSON in scratchpad `replay1010/or/`) and `/api/v1/models/<id>/endpoints`.
  - `/api/v1/endpoints/zdr`.
  - The 404 data-policy response for `qwen/qwen3.8-flash`.
- **Hugging Face API:** `ornith-ai` org listing, `Ornith-1.5-397B{,-GGUF,-FP8,-NVFP4}` (sizes, config), `zai-org/GLM-5.3` (params, config), `deepseek-ai/DeepSeek-V4-Pro{,-0813}`, `XiaomiMiMo/MiMo-V2.6-Pro-RL`.
- **Runtimes and benchmarks:** github.com/danveloper/flash-moe · raw.githubusercontent.com/antirez/ds4/main/docs/SSD_STREAMING.md · github.com/jundot/omlx · omlx.ai/benchmarks/679bs0za.
- **Apple:** apple.com/au/mac-studio/specs/ · apple.com/au/shop/buy-mac/mac-studio.
- **Ours:**
  - `2026-10-10_mac-ram-local-coding-models/REPORT.md`
  - `2026-10-09_studio-128-vs-256/{REPORT,HOSTED_REPLAY_RESULTS,HOSTED_API}.md`
  - `2026-10-08_omlx-flash-next/{REPORT,QWEN122_AB,MODEL_RANKING}.md`
  - `2_Project_Files/local-model/spark/{done.md,queue.md}`
  - `local-model/hosted/{replay.py,check.sh,README.md,done_*.md}`
  - `fleet/specs/model-routing.md` §6
