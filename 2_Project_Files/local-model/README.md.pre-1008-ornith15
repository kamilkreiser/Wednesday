# ⏸ PARKED 2026-09-14 14:2x (Kam, panel 14:25: "Please remove Quen from the system as we won't use it going forward.")
Model removed (`ollama rm qwen3:30b-a3b`, `models/` 0 B), `ollama serve` stopped (pid 6442 killed; /api/tags down). Two mechanism-checked pilots FAILED (census 27/30 rows; code_patch ×2 — fix line right, test invalid): scoreboard rows 0.00. The harness (`local_model_task.sh`, `lib/`, `tasks/`, `runs/` evidence) stays so any future local model is a ten-minute trial on the same two tasks. Re-enable: `brew install ollama` (if absent) → `OLLAMA_MODELS=<this>/models ollama serve` → `ollama pull <model>` → `LM_UNPARK=1` for doctor.

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

## Task type `code_patch` (built 2026-09-14 13:20–14:00, Kam: "get Qwen to try one of the coding tasks")

**Files:** `tasks/code_patch/{task.md, checker.sh, prepare_clone.sh, sample_input.json}`.
**Pilot:** Secuura **KS-806** (`wallet.ts:200`, the `walletAddress.slice(0, 8)` synthetic-email
bucket). Run evidence: `runs/2026-09-14_ks806-code-pilot/` (every attempt kept whole —
`out.md.attemptN`, `.meta.json`, `harness.attemptN.out`, `checker.attemptN.out`, the
`task.md.attemptN` wording each attempt saw, plus the checker's own controls).

**Shape.** The input carries the ticket text verbatim, the FULL product file, a READ-ONLY
reference test (ks796 — the repo's own in-process route-contract precedent), the pinned
`tip` SHA and the paths. The model must answer with ONE fenced ```diff block touching
exactly `product_file` + ONE test file under `test_dir`. The checker (`checker.sh
<input.json> <out.md> <clone-dir>`) never edits the patch; it applies it in a scratch
clone pinned at the tip and prints seven assertions: **A1** one diff block, no prose ·
**A2** `git apply --check` (strict first; `--recount --ignore-whitespace` is the one
accommodation, reported apart) · **A3** touched set == {product, one test} · **A4
RED-FIRST** the test hunk alone fails at the tip with >=1 failed assertion (a load error
is NOT a red) · **A5 GREEN-AFTER** product hunk applied, the file passes · **A6** whole
service suite: no NEW red vs the untouched tip (both measured in the same run; develop's
own reds attributed) · **A7** `tsc --noEmit` rc 0. rc 0 only on 7/7. Untracked leftovers in
the clone are quarantined (`<clone>/../quarantine/<ts>/`), never deleted.

**Clone discipline.** `git clone --shared --no-checkout <source> <scratch>/clone` +
`checkout --detach <tip>` in the SESSION SCRATCHPAD (the pre-tool hook refuses git write
verbs anywhere else, and refuses them through a `$VAR` path — use the literal path).
`prepare_clone.sh <input.json> <clone>` symlink-farms the source's installed
`node_modules` INTO the clone (985 root entries + workspace dirs; `.vite` and
`.package-lock.json` become real clone-local dirs so vitest's cache never lands in the
source; `@secuura/shared` is re-pointed to the CLONE's `packages/shared`, which the script
builds with `tsc` because the source's `dist` was 12 days stale). No `npm ci`, no docker,
no stack. Measured in the clone: services/auth suite **709 tests / 15s**, `tsc` 4s, one
test file 7s — a full checker run is ~22s.

**Checker controls (all recorded in the run dir):** the builder's own reference patch
(`control_positive.mine.*` — NOT the model's; it exists so a checker that can never PASS
is caught) → **PASS 7/7**, red-first 2 failed / 3 run at the tip, 712/712 after, strict
apply. Planted third-file diff → **FAIL at A3** (n=3, other=1). Planted not-red-first
test → **FAIL at A4** (0 failed / 3 run at the tip) with A5–A7 still passing, i.e. the
assertion that catches it is the one that should.

**KS-806 pilot results (real model, `LM_NUM_CTX=32768`, `LM_MAX_LOAD=18`, load 6-7 at launch, no
`LM_FORCE`; tip pinned `f09b629457c5800b215621c31c680631f947e879` = origin/develop at 13:22 AEST):**

| attempt | wall | prompt tok | eval tok | tok/s | thinking chars | checker (v2, per-section) | failure shape |
|---|---|---|---|---|---|---|---|
| 1 (`task.md.attempt1`) | 203s | 11571 | 11737 | 63.6 | 37.5K | **FAIL** A5+A6 (2/7 failed) | product hunk right (`sha256(...).slice(0,24)`, +1/-1) but (a) BOTH hunk headers miscounted (`-199,7` for a 6/6 hunk; `+1,123` for 144 lines) and every context line over-indented by 2 spaces — strict `git apply` rejects it outright (checker v1 stopped at A2); with per-section `--recount --ignore-whitespace` it applies, and then (b) the test file calls `vi.mocked(userRepo.createUser)` without ever importing `userRepo` → `ReferenceError` in BOTH cells before AND after the fix. Red-first "yes" only in the degenerate sense (red on its own bug). |
| 2 (`task.md.attempt2`, wording tightened with 2a-2c diff mechanics + 6a-6b test rules) | 401s | 12102 | 22543 | 58.7 | 85.2K | **FAIL** A1+A5+A6 (3/7 failed) | (a) generation ran past `<\|endoftext\|>` into prose + a SECOND, degraded copy of the diff (`node/http` for `node:http`) — A1; (b) new-file hunk declared `+1,100` for 127 lines — strict apply "succeeds" and silently truncates the file at line 100 (checker v1 saw a load error; v2's audit catches the miscount and recounts); (c) with the full file applied, the test's `challengeId: 'CHALLENGE_ID'` fails the route's `z.string().uuid()` schema → 400, so its own CONTROL cell fails and `createUser` is never reached (0 created, expected 2) before AND after. Also 12 unused imports + implicit-`any` params (tsc on the test file rc 2, informational). |

**Reading.** The model got the one-line product fix right both times and copied the ks796 mock
shape plausibly, but a 30B-A3B model cannot yet produce a git-applicable unified diff reliably
(hunk counts, context indentation) nor a test that reaches the code under test — both attempts'
CONTROL cells failed, which is the tell. The checker never PASSed a model patch; it PASSed the
builder's control and FAILed both planted-bads on the right assertion. Nothing from this run is
PR-ready. What a Secuura seat would do with a PASSING patch is in the run report, not here.

**Checker v1 → v2 (same session, all five inputs re-run under v2, v1 outputs kept as
`checker.attemptN.out` / `*.checker.out` beside the v2 files):** v1 applied the whole diff with
`--include` and treated `--recount` as a global accommodation; attempt 1 showed `--recount` makes a
correctly-counted hunk swallow the next `--- /dev/null` header, and attempt 2 showed a miscounted
new-file hunk is accepted by strict apply and truncated silently. v2 splits the diff per file,
audits every hunk header against its actual line counts, and recounts only the miscounted
section, naming the accommodation in the A2 line.

**Environment note:** one baseline run of the untouched tip (checker.attempt2.out, v1) showed 4
develop-own reds (`db.retry`, `ks488-smtp-opt-in`, `ks949-platform-admin-seed-identity`,
`s130-f6-openapi-module`) that were green in the other six baseline runs — flaky under a
concurrent load, attributed by the delta logic and not counted against the patch.

**Gitignore state:** `2_Project_Files/local-model/models/` and `2_Project_Files/local-model/logs/`
were **already** gitignored (`.gitignore` lines 128-129, added at the runtime's own creation
earlier 2026-09-14) — `git check-ignore -v` confirms both; no `.gitignore` edit was needed.
`local-model/runs/` (this session's real task outputs, kept as pilot evidence) is currently
**untracked and NOT gitignored** — Wednesday should decide at commit time whether to track it
as pilot evidence or add a gitignore line for it.

## `LM_THINK` (added 2026-09-14 18:2x) and the night runner (`night/`)

**Un-parked, drive-local (2026-09-14 afternoon → evening):** the PARKED header above records the
Qwen removal at 14:25; the runtime came back the same day as a DRIVE-LOCAL Ollama v0.34.0
(`2_Project_Files/tools/ollama/ollama`, `OLLAMA_MODELS=<this>/models`, log
`logs/ollama_serve_v0.34.log`) with `gpt-oss:120b`, `gpt-oss:20b` and `ornith:35b` for the head-to-head
(`runs/2026-09-14_head-to-head-REPORT.md`). Kam's 18:15:36 ruling makes Ornith the night worker.

**`LM_THINK`** (env, default `1`): `1` sends `think:true` — the clean `content`/`thinking` split the
finding above describes; `0` sends `think:false` and strips any `<think>…</think>` block from the answer.
`0` is the workaround for Ornith's runtime cut (KS-806: `done:false`, content empty, thinking cut at the
same token twice — a server-side `cancel task`, deterministic at temperature 0). Measured 2026-09-14
18:21 on `ornith:35b` with a two-line diff task: `LM_THINK=0` → `done:true`, `done_reason:stop`,
151 chars of clean content, 0 thinking chars, 8.5 s wall (7.6 s of it model load). The meta sidecar
now records `think_field_requested`, `done` and the stderr line carries `done`/`done_reason`/
`content_chars`. Which mode a model needs is a per-model measurement (qwen3 needed `1`).

**`tasks/code_patch/task.md` is ticket-agnostic since 18:19** (backup `task.md.pre-0914-generic`): the
KS-806 fix expression, the `auth_find_user_by_wallet` rule and the "attempt 1 failed here" notes are
gone; the constraints stay, plus "fix every site the ticket names inside `product_file`" (the KS-871
lesson — all three models fixed `:280` and missed `:108`). Checker positive control re-run after the
edit: PASS 7/7, strict apply (the checker never reads task.md; the run proves the clone pipeline).

**`night/`** — the mechanism for the 2026-09-14 standing rule: `night_run.sh` (gates → memory clear →
queue → harness → checker), `build_input.sh` (ticket → contract input.json), `queue.md` (the curated
list + rejections), `done.md` (verdicts), `log/`, the launchd template + `install_night.command`.
Read `night/BUILD_REPORT.md` for what was exercised. Runs land in `runs/<date>_<ticket>-ornith35b-night/`.
