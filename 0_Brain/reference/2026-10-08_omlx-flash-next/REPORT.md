---
date: 2026-10-08
type: reference
source: research sub-agent commissioned by Wednesday 16:14 (Kam's live-board ask 16:12:39); saved by Wednesday from the agent's returned text (the harness refused the agent's own write)
status: live
---

# oMLX + Qwen3.8 Flash Next on the 96 GiB Studio (2026-10-08)

Evidence files beside this report:
- `video_transcript_GEO8nnkC5uY.txt`
- `readbench.py`: the disk test used below.
- `bench.py`: tonight's speed test, not yet run.

## BLUF
**Feasible tonight as a TEST, with Ornith unloaded and the Mac mostly idle. It cannot run beside Ornith.**
- **Speed (oMLX issue #4140):** this exact model on identical hardware (M3 Ultra, 60 GPU cores, 96 GiB, macOS 27.0) decoded at **62–78 tok/s on fresh prompts and about 80 tok/s on repeated ones**. The Spark runs at about 37 tok/s.
- **Memory is tight:** about 69 GiB must stay resident, against this Mac's GPU budget of **77.76 GiB** (measured). Ornith (about 20 GiB) cannot run at the same time. The apps running now hold about 34 GiB, so browsers and the like must close, or macOS will compress and swap.
- **The download is the critical path:** 106.3 GB at about 7.5 MB/s per stream measured (about 14.7 MB/s with two streams), so **2–4 hours**.
- **Fallback:** `gpt-oss:120b` is already on DevMASTER in the Ollama store (65.4 GB). The video cites 77 tok/s for it on a 96 GB M3 Ultra.
- **"Flash Next" is not the Spark's model.** Flash Next is Qwen3.8-Flash-Next; the Spark runs DeepSeek V4 Flash. "One on the Spark" would mean REPLACING DeepSeek there. The smallest CUDA checkpoint is 132.7 GB, against the Spark's 121 GB of memory, so that is not a tonight item.

## What the video claims
"A Guide To AI Model Sizes That Run On A 96GB Mac", The Stack (@the-stack-ai), published 2026-10-07, 22:25 long. The transcript came from YouTube's caption track (the player API); `yt-dlp` is not installed. **The presenter ran nothing themselves** (description; 1:28–1:46). Every speed is a reviewer's or a user submission to oMLX's public benchmark list.

| Time | Claim |
|---|---|
| 2:04–3:08 | The GPU budget is about 3/4 of RAM: about 72 GiB, or **83,494 MB on newer macOS**. |
| 11:50–12:55 | gpt-oss-120b (117B total, 5.1B active, 63.4 GB) ran at **77 tok/s on a 96 GB M3 Ultra**. |
| 15:32–15:48 | Flash Next 4-bit downloads are 106–112 GB. |
| 16:05–16:49 | It is a 125B MoE plus a 51B lookup table; about 30 GB of that table stays on the SSD. Only oMLX does this. |
| 16:54–17:25 | On a 96 GB M3 Ultra it fits only with the table offloaded. **Fresh prompts ran at 62–65 tok/s, repeats at about 80 tok/s**, and the slowdown tracked drive reads. |
| 17:25–17:54 | An anonymous "modified copy" on an M5 Ultra reached 93 tok/s (82 at 128K), peaking at 75 GB. Unverified. |
| 18:00–18:27 | llama.cpp/GGUF apps count the table against GPU memory through mmap, so they run out of memory. |
| 18:57–19:04 | DeepSeek V4 Flash is about 155 GB at 4-bit and **does not fit** on a 96 GB Mac. |

The video gives no setup steps and names no checkpoint. Kam's "reference table on the SSD" is the model's **n-gram embedding (PLE)**. It is neither the KV cache nor expert offload.

## What the sources say
**The model card**, Qwen/Qwen3.8-Flash-Next on Hugging Face:
- 125B parameters with 6B active, plus a 51B n-gram embedding and a 4B MTP head.
- 48 layers; 512 experts, 10 routed + 1 shared.
- 262,144 tokens of context natively, 1M with YaRN.
- Thinking mode is ON by default.
- The card says the n-gram embedding is "more amenable to offloading than MoE".
- Licence: `qwen-community-1.0`. **Terms unread.**

**Checkpoint: `Jundot/Qwen3.8-Flash-Next-oQ4e-mtp`**:
- 106,318,234,757 B (99.0 GiB) in 21 shards, 4-bit, group size 64, MTP head included. Made by oMLX's author.
- Pin revision `2615fc0e976e65c2f3b55daca3a948f1cdc5b9f8`. Not gated.
- **Split** (oMLX issue #3614, summed from the file headers): about 74.3 GB must stay in RAM; the table is about 32.0 GB. #4140 measured the table at 29.8 GiB.
- Other checkpoints, for comparison:

| Checkpoint | Size |
|---|---|
| mlx-community 4-bit | 111.5 GB |
| TensorFold 4-bit | 111.6 GB |
| nvidia NVFP4 (CUDA) | 132.7 GB |
| Qwen FP8 | 185.6 GB |

**oMLX** (github.com/jundot/omlx):
- Apache-2.0. Version v0.7.0 (2026-09-30); wheels about 39.6 MB, DMG about 831 MB.
- Python 3.11–3.13. Pins `mlx==0.32.2` plus an mlx-lm commit.
- Serves `/v1/chat/completions` and `/v1/messages`. Default port 8000.
- Caps its own memory at RAM − 8 GB by default.

**How the table offload works** (source read at v0.7.0, the `qwen4_exp/language.py` patch):
- mmap mode switches on when the checkpoint is larger than 0.70 × RAM. Here 99 GiB > 67.2 GiB. It can be forced with `OMLX_QWEN4_PLE_MODE=mmap`.
- The table is read from wherever the model files sit. That path is **read-only**.
- **SSD writes come from a different feature, the KV cache on disk.** Its default limit is 50% of free disk; #4140 reached about 92 GB. Cap it.

**Issue #4140** (open), measured on identical hardware:
- **Setup:** oMLX 0.7.0, the Jundot checkpoint, table offloaded; prompts of 111–134 tokens, 512 tokens out, thinking off, one request at a time.
- **Decode speeds:**
  - fresh prompts, first run: 62.2–64.6 tok/s;
  - fresh prompts, return run: 67.5–78.3 tok/s;
  - identical repeats: 80.1–80.8 tok/s;
  - MTP depth 2: about 1.18× faster.
- **What slows it:** fresh prompts cost 21–26 page-ins per token, and ms per token ≈ 12.5 + 0.139 × page-ins.

**Other issues relevant tonight:**
- **#3723:** on an M3 Ultra, decode slowed about 3.2× over about 10 hours of uptime; partly fixed on 09-18. Restart the server between long sessions.
- **#3240:** image input breaks; test with text only.
- **#3699:** the on-disk prompt cache never stores entries for this model type.

**The Spark** (notes in `../2026-09-22_spark-deepseek-v4-flash/`, not touched): it serves `deepseek-v4-flash-0731` on a GB10 with 121 GB of memory. oMLX is Apple Silicon only.

## This machine, measured (read-only, 16:14–16:25)
**Hardware:**
- Apple M3 Ultra (Mac15,14), 96 GiB, 28 CPU cores (20 performance + 8 efficiency), 60 GPU cores. macOS 27.0.1 (26A434).
- **GPU budget 77.76 GiB** (83,494,174,720 B, read with a Swift check). This matches the video exactly.
- `iogpu.wired_limit_mb` = 0 (the default).

**Memory in use (`vm_stat`):**

| Category | Size |
|---|---|
| Free | 24.2 GiB |
| Apps' own memory | 27.3 GiB |
| Wired | 6.4 GiB |
| File cache | 36.4 GiB |
| Swap | 0 |

`top`: 67G used, 29G unused. The biggest users are the Spotlight indexer (3.1 + 0.8 GiB), Safari/WebKit (1.6, 0.9, 0.7 GiB), Avast (0.9 GiB) and claude (0.8 GiB).

**Ollama:** the server is not running (nothing on 11434). `ornith-loop` and `ornith-night` both last exited 3. Models in `/Volumes/DevMASTER/SYSTEM/ollama/models` (269 GB in total):

| Model | Size |
|---|---|
| ornith:35b | 21.2 GB |
| ornith:35b-q8_0 | 36.9 GB |
| gpt-oss:120b | 65.4 GB |
| qwen3-coder-next | 51.7 GB (a different model from Flash Next) |
| qwen3.5-122b-q4km | incomplete |

**Ports:** the Spark tunnel is up on 47788. **47780 is unused** in Wednesday's block.

**Disks** (`readbench.py`, uncached, one run each, about 1.1 GB read per disk):

| Disk | Free | 1 GiB sequential read | Random 16 KiB reads, one at a time | Random 16 KiB reads, 8 threads |
|---|---|---|---|---|
| Internal | 275 GiB | 5.46 GB/s | 104 µs (9,580/s) | 39.3K/s |
| DevMASTER (Crucial CT2000P310SSD8, external enclosure, likely on the 80 Gb/s port) | 613 GiB | 4.20 GB/s | 150 µs (6,676/s) | 39.5K/s |

**Tooling:**
- `python3` is 3.14, which oMLX does not support. **Python 3.12 and 3.13 are present.**
- `uv`, `brew` and full Xcode are present.
- `mlx` 0.31.1 is installed globally, so oMLX goes in its own venv.
- No mlx-lm, oMLX or yt-dlp.

**Download from Hugging Face:** three 40 MB samples read 7.46, 7.55 and 7.19 MB/s per stream, about 14.7 MB/s with two streams. That gives **about 2.0–3.9 hours for 106.3 GB**.

**Fit (arithmetic, not a run):**
- About 69.2 GiB resident plus KV (about 24 KiB per token by estimate, so about 3 GiB at 128K; unmeasured) gives about 70–75 GiB, against a 77.76 GiB budget.
- Adding Ornith gives about 89 GiB, so the two cannot run together.
- Adding the current apps' about 34 GiB gives 104–109 GiB, against 96 GiB.
- DevMASTER may be about 5–8% slower than the internal SSD on fresh prompts (an estimate from #4140's formula); at 8 threads the two disks tie. **Use DevMASTER** (the portability rule). An internal copy is an A/B option only on Kam's word.
- The table reads are read-only, so wear comes only from the KV cache on disk. Cap it.

## Test plan for tonight
All paths are drive-local. `T=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/omlx`

0. **Kam's go first** (it installs software and downloads 106 GB). Then register port 47780 in `2_Project_Files/PORTS.md` and add `tools/omlx/` to `.gitignore`.
1. **Install:**
   ```
   export UV_CACHE_DIR=$T/uv-cache HF_HOME=$T/hf-home OMLX_BASE_PATH=$T/base
   uv venv --python /opt/homebrew/bin/python3.12 $T/venv
   uv pip install --python $T/venv/bin/python https://github.com/jundot/omlx/releases/download/v0.7.0/omlx-0.7.0-cp312-cp312-macosx_15_0_universal2.whl
   ```
   Check that `mlx` reports 0.32.2, and print `native_kernel_status()`. Missing custom kernels cost about 4% (#3723). The DMG installs into /Applications, off the drive, so it is Kam's call as a fallback.
2. **Download** (start early):
   ```
   $T/venv/bin/hf download Jundot/Qwen3.8-Flash-Next-oQ4e-mtp --revision 2615fc0e976e65c2f3b55daca3a948f1cdc5b9f8 --local-dir $T/models/Qwen3.8-Flash-Next-oQ4e-mtp
   ```
   Expect about 99 GiB in 21 files.
3. **Quiet the machine.** Ollama and Ornith stay down, with their loops paused. Quit the browsers and Spotify; run at most one Claude seat. Take a baseline of `vm_stat`, swap and `memory_pressure`.
4. **Serve:**
   ```
   OMLX_QWEN4_PLE_MODE=mmap $T/venv/bin/omlx serve --model-dir $T/models --host 127.0.0.1 --port 47780 --base-path $T/base --paged-ssd-cache-dir $T/cache --paged-ssd-cache-max-size 20GB --max-concurrent-requests 1
   ```
   Do NOT raise `iogpu.wired_limit_mb`. Watch `vm_stat 10`, `iostat -d disk3 disk6 10` and `pmset -g therm`.
5. **Smoke test:** `curl 127.0.0.1:47780/v1/models`, then `bench.py --reps 1`. It passes on non-empty text, the generated `parse_duration` passing its own asserts, and swap still 0.
6. **Speed:**
   - Short prompts: `bench.py --reps 3`, compared against #4140's 62–80 tok/s.
   - Our shape: `--prompt-file` with a client-neutral Wednesday tool file of 20–30K tokens, `--max-tokens 1024`. Record time to first token, decode speed, peak memory and disk MB/s.
   - Compare with the Spark: 37 tok/s decode, 1,030 tok/s prefill, 53.7 s for a turn of 23.6K tokens in and 1K out.
   - Claude Code against it via `ANTHROPIC_BASE_URL`: only if Kam asks (untested).
7. **Stop at once** if swap goes above 0, `memory_pressure` warns, any seat stalls, or there is a thermal warning.
8. **Rollback:** stop the server and quarantine `$T` (never-delete rule). No launchd jobs, sysctl changes, /Applications installs or `~/.omlx` are involved. Unregister port 47780.

**Fallback:** `gpt-oss:120b` through Ollama's `/v1` on port 11434, with the same `bench.py`. No install and no download needed.

## Open questions for Kam (one at a time)
1. Go for the 106 GB download and the drive-local install now?
2. Can the fleet go quiet during the test: Ornith loops paused, browsers closed?
3. DevMASTER only, or an A/B copy on the internal SSD as well?
4. ~~Is a study of replacing DeepSeek on the Spark worth doing?~~ **ANSWERED by Kam 16:55:29: "Keep the spark as is."**
5. Client code on this model, given the licence is unread?

## UNMEASURED
- Time to first token on 20K+ token prompts here, and therefore whether Claude-Code-shaped turns are usable.
- Decode speed on this box: every tok/s figure above is someone else's.
- Peak memory with the fleet running.
- DevMASTER vs the internal SSD under oMLX itself.
- Multi-stream download speed and the size of the install's dependencies.
- Whether the wheel includes the custom kernels.
- Heat in the external enclosure.
- Avast scanning the memory-mapped reads.
- The video's M5 Ultra figures and its "27 GB" table figure.
- How much of #3723 remains in v0.7.0.
- PLE offload on CUDA (the Spark).
- **Answer quality on our tasks.**
