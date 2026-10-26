# Spark quant test: can a smaller DeepSeek V4 Flash build hold its quality? (commissioned 2026-10-26)

**Authority, verbatim (Kam, typed in Wednesday's terminal 2026-10-26 ~14:59 AEDT):**
> "will deepseek run on a 128GB laptop (with you and other agents on it)?  maybe test a slightly smaller quant"

This follows his 12:32:27 instruction ("when the spark is idle, please test ... run the same test on the current spark model for comparison"); the Spark's ticket queue is empty for a measured reason (0_Brain/reference/2026-10-26_spark-screen-new-tickets/report.md).

## Facts measured by Wednesday before this brief (2026-10-26 ~15:0x)
- **The Spark's DeepSeek is ALREADY a 3-bit quant:** `/home/datasec-rd/DeepSeek-v4-Flash-One-DGX-Spark/data/tp1/config.json` quantization_config = `quant_method exl3, bits 3.0, codebook mcg`, with an fp8 base config. Weights load at 95.39 GiB. EXL3 runs only on NVIDIA GPUs, so a Mac cannot use this copy.
- Baseline on today's task set (`spark-ab/tasks.json`, 23 tasks): **DeepSeek EXL3-3.0 = 16/23** (`results_deepseek.tsv`), control 17/23.
- Candidate builds of the SAME model (`unsloth/DeepSeek-V4-Flash-0731-GGUF`, sizes summed from the HF tree): UD-IQ1_M 86.9 GB · UD-IQ2_XXS 90.9 GB · UD-IQ2_M 90.9 GB · UD-Q2_K_XL 96.8 GB · UD-IQ3_XXS 104.2 GB. The MLX 3-bit is 125 GB; the MLX 2-bit repo is empty.
- A 128 GB Mac has, at most, roughly 90-100 GB for weights + context once macOS and the seats run (UNMEASURED on a real 128 GB Mac). So the question that matters is: **does UD-IQ2_XXS (91 GB) keep DeepSeek's quality?** UD-IQ1_M (87 GB) is the stretch arm.
- On the Spark: only the image `nvcr.io/nvidia/vllm:26.09-py3` exists; no llama.cpp. Whether vLLM 0.29 loads this GGUF for DeepSeek V4: UNMEASURED.

## The job, in order (same rules as BRIEF.md; read it first)
0. **Measure the serving route, change nothing.** Is there a working way to serve the GGUF on GB10/arm64: vLLM's GGUF loader in that image, or a llama.cpp CUDA build (an official arm64 CUDA container, or built in a container, never on the host)? Prove it can load the model's ARCHITECTURE before downloading 91 GB. **If no route exists, STOP and report. Do not touch DeepSeek.**
1. Download UD-IQ2_XXS to a NEW directory on the Spark while DeepSeek keeps serving. Verify sizes (and sha256 where the listing gives them).
2. Swap (stop DeepSeek, never remove it), serve UD-IQ2_XXS, and run the IDENTICAL 23 prompts through `ab.py` (same sampler, same checker), writing `results_iq2xxs.tsv`. Record load time, memory, and tok/s.
3. Only if time allows, and only if IQ2_XXS scores at least 14/23: do the same with UD-IQ1_M as `results_iq1m.tsv`.
4. **RESTORE DeepSeek exactly as before and prove it answers** (one task re-run, byte-identical to its earlier output). This step is not optional. If anything fails or runs past ~3 hours, restore first, then report.

## Output
- Report: write the content of `0_Brain/reference/2026-10-26_deepseek-quant-on-spark/report.md` into your final message (the sub-agent cannot write report files; Wednesday saves it). Include: per-rung PASS for EXL3-3.0 (from results_deepseek.tsv) vs IQ2_XXS (vs IQ1_M), the failure causes, serving facts, DeepSeek downtime, and "What I could not test". Add a short section estimating fit on a 128 GB Mac from your measured weights + KV, marked as an estimate.
- New results TSVs beside the others (ids/verdicts only). Anything with Secuura content stays in the gitignored `runs/` and `work/`.

## Boundaries
As BRIEF.md: Secuura content only; nothing to any board, PR, human or other project; no money; nothing on the laptop's Docker; the box is otherwise untouched; never delete (stop containers, keep weights, including the Ornith directory already there); never `cd` in a Bash call; never print a secret.
