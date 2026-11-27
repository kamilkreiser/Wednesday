# B2144 (Kam personal, NOT Datasec) -- make LTX Desktop fit for adult (18+) video generation on this Mac, and a workflow for different types of scene

Commissioned by Tuesday s333 on Kam's terminal words of 2026-11-27: "can you please amend ltx. its not quite fit for purpose yet. review [a PicassoIA blog post] ... as well as anything you think necessary to create a workflow for different types of porn videos". The blog post was read: it is an advert for a hosted service with no local detail (useful only for its prompt layering: subject, then motion in time order, then camera, then light; and the image-to-video route). Prior work: B2141 (`~/LTX-build/REPORT.md`, read it whole): the heretic-on-LTX bf16 text encoder is installed, `use_local_text_encoder` true, `~/LTX-build/bin/LTX-Load.command` and `LTX-Unload.command`.

## Hard lines (non-negotiable; a step that would cross one is skipped and named in the report)
- Adults only. Nothing that depicts or suggests anyone under 18: no LoRA, preset, keyword or negative-prompt gap aimed at youthful looks (teen, schoolgirl, petite-young, loli and the like). The workflow's negative prompt INCLUDES terms pushing away from youthful features.
- No real person's likeness: no LoRA, preset or reference trained on or named for a real person (celebrity, model, creator). Read each LoRA's page; if the trigger or description names a person, it is out.
- No non-consent, violence-sexual or bestiality material: no LoRA or preset for it.
- No cloud: nothing the user types for these videos may leave the machine. The prompt enhancer must not use Gemini or any API for this; local only, or off.
- Never delete: replace by moving the old file into `~/LTX-build/backup-<date>/`; back up `settings.json` before any change and show the diff.
- Never print or copy any API key or token (settings.json holds three: read around them).
- Downloads only from Hugging Face or Civitai pages you have read, with the file's sha256 checked against the page; licence noted. If Civitai needs a login or API key, STOP that part and say so (Kam's to give).

## Find out first (read-only, report each with its source line)
1. What the prompt enhancer does to an explicit prompt and which provider it uses with `prompt_enhancer_provider_preference` null and `assistant_provider` gemini (read the backend code). Whether a local enhancer (`assistant_local_model` qwen3.5:9b via Ollama, if present) is wired, and whether it sanitises.
2. What `nag_scale` (11.0) is: NAG's default negative text, and whether it pushes away from nudity. Where the negative prompt lives and whether it can be set.
3. How LTX Desktop discovers LoRAs (the folder layout under `models/loras/<name>/`, any manifest or catalogue in the backend or app.asar), whether a user-added LoRA for this model family (LTX-2.x / ltx-2.5) is loaded and with what strength control, and whether image-to-video is available locally.
4. The community state of adult LoRAs for THIS model family (LTX-2 / 2.3 / 2.5) on Hugging Face and Civitai: names, base-model compatibility, sizes, licences, and the hard-line check for each. List them; do not install yet beyond what step "Change" allows.

## Change (only what the findings support)
- Prompt enhancer: off for this use, or switched to a local model that does not sanitise (proved by one test prompt of an adult scene, the enhanced text compared). Default: OFF, with `explore_auto_enhance_prompts` off too.
- NAG / negative prompt: set so it does not suppress adult content and does carry the under-18 guard terms.
- LoRAs: install at most the compatible, hard-line-clean ones the findings justify (prefer general anatomy/realism LoRAs over act-specific ones), each in its own folder in the layout the app reads, proved by the app listing it.
- One short real test generation at low resolution to prove the pipeline runs end to end on MPS (timings, memory); LTX-Unload after.

## The workflow document (`~/LTX-build/WORKFLOW.md`)
- Presets per scene type as SETTINGS, not explicit text: resolution, frames, fps, steps, guidance, LoRA and strength, text-to-video vs image-to-video, seed handling, for scene types such as solo, couple, softcore/glamour, explicit close, POV camera, and longer clips by extend.
- A prompt TEMPLATE with labelled slots (who: adults, described by appearance; setting; action over seconds 1-5; camera move; lighting and lens; style) and the negative prompt; slots are for Kam to fill: no library of explicit example prompts.
- How to load and unload, where outputs land, and the known limits on this Mac (what is slow, what fails).

## Report
`~/LTX-build/REPORT-B2144.md`: FOUND / CHANGED (each with before and after, backup path) / TESTED (with controls) / NOT DONE (with why, incl. anything blocked by a hard line or a login). Return 10 lines to Tuesday, the first `DONE` or `BLOCKED: <reason>`.
