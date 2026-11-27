# B2148 (Kam personal, NOT Datasec) -- Wan 2.2 on this Mac: set up, then a timed side-by-side with LTX for long adult video

Kam's word (Tuesday terminal, 2026-11-27): "go with your recommendation". That recommendation, as Tuesday gave it:
- set up Wan 2.2 in ComfyUI, with Draw Things as the fallback;
- the 5B model first, then 14B if memory and time allow;
- one timed non-explicit test clip, compared with LTX's 20-second clip time;
- check whether the SVI 2 Pro long-video workflow runs on Apple Silicon;
- the test render waits until the LTX long-video agent (B2147) has finished.

Machine: Kamil's Mac Studio, Apple M5 Max, 128 GB, macOS (measure free disk first).

Hard lines (as in B2144, `tuesday/briefs/2026-11-27_B2144_KAM-PERSONAL_LTX-ADULT-WORKFLOW.md`):
- Adults only, and the negative prompt carries the under-18 guard terms.
- No LoRA or model trained on, or named for, a real person.
- No non-consent material.
- Nothing typed for these videos leaves the machine.
- Downloads only from Hugging Face pages (or the official GitHub) that you have read, each sha256 checked; licence noted.
- Never delete: move to `~/Wan-build/_quarantine/`.
- Never print a key or token.
- No Homebrew, system-wide install or sudo without stopping to say so. Python environments are self-contained under `~/Wan-build/`.

## PHASE 1 (now): research and set up, NO GENERATION
1. Free disk (`df -h ~`), and the sizes of what you would download. Stop and say so if they would leave less than 100 GB free.
2. Which route runs Wan 2.2 best on Apple Silicon today, with sources:
   - ComfyUI on MPS, and in which precision (fp16/bf16; GGUF only if fp16 is infeasible);
   - Draw Things;
   - Lightricks-style native apps.

   Pick one and say why.
3. Install it under `~/Wan-build/`: ComfyUI in its own venv (official repo, a pinned commit), the Wan 2.2 TI2V-5B weights and its VAE and text encoder from the official Wan-AI Hugging Face repos, each hash checked. Also image-to-video if it is a separate model.
4. Long video: does SVI 2 Pro, or another Wan 2.2 continuation method that carries motion between segments, run on MPS? Read its requirements (custom nodes, CUDA-only kernels). If it is installable, install it, but do not run it yet.
5. Adult LoRAs for Wan 2.2 on Hugging Face (Civitai is region-blocked from this Mac): list candidates with base-model compatibility, licence and the hard-line check. Do not install yet.
6. Write `~/Wan-build/SETUP.md`: what is installed, where, how to start it (a `~/Wan-build/bin/Wan-Start.command` that starts ComfyUI on 127.0.0.1 only and opens the browser), and how to stop it (`Wan-Stop.command`).

Then RETURN to Tuesday with 10 lines, first `PHASE1 DONE` or `BLOCKED: <reason>`. Leave nothing running.

## PHASE 2 (only when Tuesday messages you "phase 2: go"): the timed test
- One NON-explicit adult image-to-video test (a woman in her thirties walking in a garden): Wan 2.2 5B at 480p and at 720p, the longest native length.
- Record wall time, peak memory, frames and fps.
- If the 14B fits, one run of it at 480p.
- If SVI 2 Pro installed: a 2-segment continuation, timed, with a check for a visible seam.
- Write `~/Wan-build/REPORT-B2148.md` (or return it for Tuesday to save). Include the projected time for a 5-minute video next to LTX's figure from `~/LTX-build/REPORT-B2147.md`, and a recommendation: LTX, Wan 2.2, or both, for which use.
- Stop ComfyUI at the end.
