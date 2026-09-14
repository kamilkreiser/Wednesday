# Local model (Kam, panel 2026-09-14 11:26 — "let's try it out … download and implement Qwen 3 30b and use it within the workflow in conjunction with other agents. Assign simple and manageable tasks to it as you see fit.")

- **Runtime:** `ollama serve` (Homebrew `/opt/homebrew/bin/ollama`), models ON THE DRIVE: `OLLAMA_MODELS=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/models` (portability rule — weights travel with the drive; `models/` is gitignored). Started detached 2026-09-14 11:3x (python `start_new_session`; `setsid` does not exist on macOS). Logs: `logs/ollama_serve.log`, `logs/pull_*.log`.
- **Model:** `qwen3:30b-a3b` (Qwen3 30B MoE, 3B active; ~18 GiB Q4). Pull started 11:3x. Headroom analysis: `1_Project_Definition/Architecture/2026-09-14_local-model-headroom.md`.
- **Pilot scope (Wednesday's, under the 09-14 model-tiering rule):** simple, mechanism-checked board tasks only — (1) a state-line census of N tickets from a Linear JSON dump → a markdown table (checked by `board_count.sh` + a diff against the JSON); (2) a facts-only ticket comment from the s218/s222 template + the ticket's own JSON → a comment body (checked: 0 at-signs, every id present in the input, read back by id after a Secuura seat posts it — the local model never holds a board identity); (3) classification of tickets against a WRITTEN predicate (checked by a second read). NO rulings, NO briefs, NO gates, NO coordination (its window cannot hold the board — Kam's 11:13 point).
- **Harness (owed — the successor commissions an assistant agent):** `local_model_task.sh <task.md> <input.json> <out.md>` → POST `http://127.0.0.1:11434/api/chat` with a bounded prompt (the task file + input, `num_ctx` set explicitly, `think: false` unless the task says otherwise), writes the output file + a `.meta.json` (model, timings, tokens); every task's checker script beside it; a scoreboard row per task tagged `qwen3:30b-a3b`. Doctor check + PORTABILITY item for the runtime (rule 3a).
- **Load rule:** the model counts as a seat — no local generation while a tier-1 gate runs suites at load > ~16.

## Harness (built 2026-09-14)

**Usage:** `2_Project_Files/local-model/local_model_task.sh <task.md> <input.json> <out.md>`
Writes `<out.md>` (the model's answer, cleaned) and `<out.md>.meta.json` (timings/tokens/load).
Logs one line per run to `local-model/logs/runs.log`. bash 3.2-compatible (no `declare -A`,
no `timeout` — the HTTP call's wait lives in `lib/lm_call.py`, called by the wrapper).

**Env vars:** `LM_MODEL` (default `qwen3:30b-a3b`) · `LM_NUM_CTX` (default `16384`) ·
`LM_MAX_LOAD` (default `16`, the load-rule threshold above) · `LM_FORCE=1` (run anyway when
the load rule would refuse — every pilot run below needed this: the fleet was at load 18-20
the whole session) · `OLLAMA_URL` (default `http://127.0.0.1:11434`).

**Exit codes:** `0` ok · `2` usage / missing input file / ollama not answering `/api/tags` ·
`3` load rule refused (no `LM_FORCE`) · `4` HTTP/JSON failure talking to the model.

**The `think` field finding (probed 2026-09-14, ollama 0.18.2):** the obvious reading —
`"think": false` disables reasoning — is WRONG for this model/version. Sending `think: false`
does not stop the model reasoning, it just stops ollama separating the reasoning out, so it
leaks into `message.content` ahead of the real answer (and without even a matching opening
`<think>` tag — ollama's chat template consumes that as part of the PROMPT, so only a
trailing `</think>` shows up in what comes back). Qwen3's own `/no_think` directive in the
user turn sometimes suppresses it but was NOT reliable on a realistic task+input prompt (it
still reasoned for ~700 words on the first `state_census` attempt — kept on disk as
`runs/state_census/out.md.first-run-think-leak` + its meta sidecar). **`think: true` is what
actually works**: ollama then returns a clean, separate `message.thinking` field and a
`message.content` that is exactly the final answer, verified on all three pilot tasks. The
harness sends `think: true` and writes only `content` to `<out.md>`; `thinking` length (not
text) is recorded in the meta sidecar as `thinking_chars`. A belt-and-suspenders strip for
`</think>` leakage stays in `lib/lm_call.py` in case a future ollama version regresses.

**Measured defaults:**
- Model's own default context length (`ollama show qwen3:30b-a3b`): **262144** tokens.
- Harness default `num_ctx` sent per request: **16384** (well inside the model default;
  raise via `LM_NUM_CTX` for larger inputs).
- Tokens/sec observed across the three real pilot runs below: **88–94 tok/s** (`eval_count /
  eval_duration`), all under fleet load 18-20 — faster off-peak is expected but unmeasured.
- First model load into memory (`load_duration` on the very first call this session): ~3.3s
  (already-warm model after that).

**The three pilot tasks** (`local-model/tasks/<name>/`, each `task.md` + `checker.sh
<input.json> <out.md>` + `sample_input.json` with synthetic KS-9xxx identifiers — no real
ticket text):
- **state_census** — array of issues → one markdown table sorted by identifier + a
  `counts:` line by state type. Checker: every input id present exactly once, no invented
  ids, counts line matches a python recomputation from the JSON.
- **facts_comment** — one issue + a facts list → a `## BLUF`-first, facts-only comment body.
  Checker: 0 `@` characters, every id in the output (`KS-\d+`, `#\d+`, 7–40 hex) traces back
  to the input, first line starts `## BLUF`, under 1,500 chars.
- **predicate_classify** — array of issues + a WRITTEN predicate → `identifier | A|B|UNKNOWN
  | reason` per issue. Checker: one line per input id in order, class in `{A,B,UNKNOWN}`, and
  the real check — a python reimplementation of the SAME predicate agrees with the model on
  every row (the "second read"; disagreements are printed, not silently accepted).

**Results (real model + real checker, `LM_FORCE=1`, fleet load 18-20 throughout):**

| task | attempt | wall clock | eval tokens | tok/s | checker | planted-bad |
|---|---|---|---|---|---|---|
| state_census | 1 | 56.9s | 4586 | 89.2 | **FAIL** — harness bug: `think:false` leaked ~700 words of chain-of-thought into `out.md` ahead of the table (see finding above; not a task-wording defect, so the task file was not touched) | — |
| state_census | 2 (after fixing `lib/lm_call.py` to `think:true`) | 63.3s | 5391 | 88.0 | **PASS** — all 8 ids present once, no invented ids, counts line exact | **FAILs correctly** on a planted output with a dropped id, an invented id, and a wrong count |
| facts_comment | 1 | 44.5s | 3934 | 91.2 | **PASS** — 0 `@`, all ids traced to input, BLUF first line, 551 chars | **FAILs correctly** on a planted output with 2 `@` mentions and 2 invented ids |
| predicate_classify | 1 | 19.6s | 1747 | 94.0 | **PASS** — second-read python reimplementation agrees with the model on all 7 rows (including the one `UNKNOWN` row, a missing-`state`-field issue) | **FAILs correctly** on a planted output with one wrong class and one out-of-domain class value (`C`) |

**Gitignore state:** `2_Project_Files/local-model/models/` and `2_Project_Files/local-model/logs/`
were **already** gitignored (`.gitignore` lines 128-129, added at the runtime's own creation
earlier 2026-09-14) — `git check-ignore -v` confirms both; no `.gitignore` edit was needed.
`local-model/runs/` (this session's real task outputs, kept as pilot evidence) is currently
**untracked and NOT gitignored** — Wednesday should decide at commit time whether to track it
as pilot evidence or add a gitignore line for it.
