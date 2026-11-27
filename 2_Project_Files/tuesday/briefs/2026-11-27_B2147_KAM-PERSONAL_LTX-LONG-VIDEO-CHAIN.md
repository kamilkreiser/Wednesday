# B2147 (Kam personal, NOT Datasec) -- long videos (target 5 minutes) by chaining LTX clips, in the Prompt and Video Builder

Kam's words (Tuesday terminal, 2026-11-27), verbatim: "also, it would be good if I could build a long (target 5min video) using the prompt builder. LTX allows for a max 20sec video but allows for opening image. In prompt builder, I could pick 1st image, how many 20s slots the prompt is for, and pick a new prompt or multiple at different points. Also, LTX allows for the start image. for longer videos, we would need to take the last image of a scene to be the first image of the new 20sec sectioin"

Prior work (read whole first):
- `~/LTX-build/REPORT.md` and `~/LTX-build/REPORT-B2144.md`: the backend on 127.0.0.1:41954 behind a per-launch Bearer token, the custom LoRA, image-to-video by Start Frame, the settings.
- `~/LTX-build/WORKFLOW.md`, `~/LTX-build/PROMPT-BLOCKS.md`, `~/LTX-build/bin/prompt_builder.py`.
- The page `~/LTX-build/wizard/` (`build_wizard.py` generates `index.html` from `template.html` and imports prompt_builder.py, so they never drift; `test_wizard.js`).
- Hard lines of the B2144 brief: `tuesday/briefs/2026-11-27_B2144_KAM-PERSONAL_LTX-ADULT-WORKFLOW.md` (adults only, no real-person likeness, no non-consent, nothing to the cloud, never delete, never print a key or token). They bind here unchanged.

## Find out first (read-only; each answer with its source line or measurement)
1. The real maximum clip length and fps per resolution in this LTX Desktop, and the frame counts it allows (read the backend's limits). Kam says 20 s; confirm it.
2. Whether the backend's own routes can run an image-to-video generation from a script: start frame, prompt, negative prompt, LoRA and strength, resolution, length, seed. Also where the output file lands, and how a script learns that a job finished. How the per-launch token can be obtained by a local script without printing it (if only Electron holds it, say so).
3. Whether ffmpeg/ffprobe is on this Mac, at which path. If it is missing, find a drive-local or Python route to read the last frame and to concatenate (no Homebrew install without saying so first).
4. Time per clip on this Mac (Apple M5 Max, 128 GB) at 540p and 720p for 20 s, measured on at least one real image-to-video run with a NON-explicit adult prompt. From that, the projected wall-clock time for a 5-minute video (15 clips of 20 s), and whether it fits overnight.

## Build
- **The page: a new part "C: Long video planner"** in the Prompt and Video Builder (the template plus generator; keep A and B working):
  - target length (default 5:00) and segment length (default the measured maximum, at most 20 s), with the number of slots computed;
  - first image: a file picker that records the file name, plus a text field for its full path (a page cannot read paths);
  - a timeline of slots where Kam assigns a prompt built in Part A to a run of slots ("prompt 1 for slots 1-4, prompt 2 for slots 5-9 ..."), with several prompts at different points; every prompt passes the same refusals as Part A;
  - render settings per plan;
  - an EXPORT of the plan as a JSON file (download, and a Copy button) that the runner reads.
- **The runner `~/LTX-build/bin/long_video.py <plan.json>`** (Python 3, drive-local, stdlib plus ffmpeg):
  - **automatic mode** if finding 2 allows it: for each slot, generate with that slot's prompt and start frame, wait for the output, extract the LAST frame of the clip as the next slot's start frame, and continue; resumable (a state file; a finished clip is never re-made), with progress printed and a log;
  - **assisted mode** if it does not: after Kam generates each clip in LTX, the runner takes that clip, extracts its last frame and tells him the exact start-frame file and prompt for the next slot;
  - then stitches all clips into one file with ffmpeg. Drop the first frame of each later clip (it repeats the previous clip's last frame), re-encode once, keep the fps, and write a list of the clips used.
  - All outputs go under `~/LTX-build/long/<plan-name>/` (clips/, frames/, final.mp4, plan.json copy, log). Nothing is ever deleted (re-runs write new names).
- Drift: say in WORKFLOW.md what chaining does to faces and bodies over 15 clips (a known weakness of last-frame chaining), and how the planner reduces it: the same appearance block in every prompt, an optional re-anchor to the first image every N slots if the backend allows a second reference. Do not promise what was not measured.

## Test
- `node --check` and `test_wizard.js` extended to the planner: slots computed right; a youth word refused in any slot's prompt; the export JSON round-trips into the runner's loader.
- A real 2-slot chain at low resolution and a short length: two clips, the second's start frame equal by hash to the first clip's extracted last frame, the stitch plays with the summed duration minus one frame (ffprobe), and the output folder as stated. NON-explicit adult prompt only.
- LTX quit with `LTX-Unload.command` at the end.

## Report
Return 10 lines: first `DONE` or `BLOCKED: <reason>`, then the findings (max length, automatic or assisted, ffmpeg, time per clip and the 5-minute projection), what changed, the test results, and what was not done. Write the full report to `~/LTX-build/REPORT-B2147.md` if the harness lets you. Otherwise put it below the 10 lines for Tuesday to save.
