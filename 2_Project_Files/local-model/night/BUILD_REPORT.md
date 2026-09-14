# BUILD_REPORT — Ornith night runner + ticket list (2026-09-14 18:19–18:4x AEST)

Kam (panel 18:15:36, verbatim): *"lets use Ornith at night in the downtime (when no other agents run). clear system memory before it runs so that's not a problem. Set this up as a rule and get it working on the backlog. Prepare a list of tickets for it to work on."* Spec = the six clauses of `0_Brain/learnings/2026-09-14_ornith-runs-at-night-in-the-downtime-a-standing-rule.md`; commission = `night/COMMISSION_2026-09-14.md`. Built by the Wednesday-assistant builder subagent. **Not committed, not armed** — Wednesday commits and runs `install_night.command`. Nothing under `!CODING/` was written (source checkout `git status --porcelain --untracked-files=no` = 0 before and after every clone/checker run); no `rm`, no `cd` outside script subshells, no launchd install.

## FOUND

**Built (all under `2_Project_Files/local-model/`, plus one doctor.sh block and PORTABILITY item 15):**

| file | what |
|---|---|
| `tasks/code_patch/task.md` (+ `task.md.pre-0914-generic`, sha `342408d0…`) | ticket-agnostic: the sha256/24-hex fix paragraph, the `auth_find_user_by_wallet`/`userRepo` rules and every "attempt 1 failed here" note are gone (grep for `806|sha256|wallet|attempt 1|userRepo|createHash` → 0 hits); constraints kept; added "fix every site the ticket names inside `product_file`" and "the red cell asserts the BEHAVIOUR at the site(s) the ticket names" (the KS-871 partial-fix lesson). 73 changed lines. |
| `lib/lm_call.py`, `local_model_task.sh` | `LM_THINK` (default `1`; `0` → `think:false` + `<think>…</think>` strip); optional 8th argv; meta gains `done`, `think_field_requested` is now the real value; stderr line carries `think`/`done`/`done_reason`/`content_chars`; runs.log line carries `think=`. |
| `night/night_run.sh` (360 lines) | the runner — 5 gates with measurements, memory clear + assert, queue take/move, build → harness → `--shared` clone → prepare → checker, per-ticket run dir, gate re-check between tickets, cap N, log + `last_run.json`, exit 0/3/4. |
| `night/build_input.sh` (312 lines) | ticket → contract `input.json`: Linear read-only (key sourced from the Secuura `.env`, never printed), `ls-remote` develop tip (refuses if the object is not local — a fetch is a write verb), `git show` product + reference test, key set asserted identical to the KS-871 input's; refuses (rc 2) on archived / not Backlog-Todo / Peter-Stuart / PR attached / >1 product file or a second `.ts` basename / no fix shape or "decision needed" / non-vitest service / no in-process test importing the module / no defect line. Pins: `product= ref= line= ctx=`. |
| `night/queue.md` | the LIST: 3 fits (KS-871, KS-1072, KS-1087) with id · title · state · file · fix-shape sentence quoted · why · pins, and ~70 rejections by class with a one-line reason each. |
| `night/com.wednesday.ornith-night.plist` + `night/install_night.command` | scheduler-pattern template + installer (23:30 daily, `WED_AGENT` + `PATH` in EnvironmentVariables, launchd stdio to `~/Library/Logs/wednesday_ornith-night.{out,err}`); `--render-only <path>` lints without arming; refuses under `WED_AGENT=tuesday`. |
| `2_Project_Files/doctor.sh` | new block after the (stale) PARKED local-model block: job armed? · `ornith:35b` manifest on the drive + served? · queue non-empty? · last run's exit + age (0/3/4 = ok, else warn). |
| `PORTABILITY.md` item 15 | drive-local Ollama + the night job: what travels, what is per-Mac, what the Mac needs, the `sudo purge` honest limit, degrade path. |
| `README.md` (local-model) | section on `LM_THINK`, the un-park, the generic task.md, `night/`. |

**The honest queue count is 3, not 8–15.** The KS Backlog/Todo read (363 issues, `includeArchived:true`, 8 pages at 18:2x) was filtered to 286 non-archived non-Peter/Stuart, then to 55 naming exactly one `services/*/src|packages/shared/src` product file, plus the 2–3-file and bare-basename sets; every candidate that survived the title filter was read (`scratchpad/board/candidates_read{,2,3}.txt`, 33 tickets). What the backlog is made of: coverage-only tickets (the code is right, a pin is owed — the contract's RED-FIRST assertion A4 cannot pass on those), decision/ruling tickets, auth/oauth/security surfaces, originate + governance (jest — the checker runs vitest only), multi-service chains, shell/SQL/compose. The rejections are in the queue file so the next board seat does not re-read them. KS-849 (kyc stale timer) becomes a 4th line the moment Kam rules its option (a).

**Ornith's runtime cut is worked around (clause 5):** `LM_THINK=0` on `ornith:35b` → `done:true`, `done_reason:stop`, content present, `thinking_chars 0`, no leak (18:21:19–28; 8.5 s of which 7.6 s was model load). NOT re-proven on the KS-806 prompt that cut (that is a real-ticket run, which tonight's live fleet forbids) — the night's first KS-871 run is the proof at scale.

## TESTED (which branches ran for real)

| # | branch | how | result |
|---|---|---|---|
| 1 | checker positive control after the task.md edit | KS-806 pilot `input.json` + `control_positive.mine.out.md` → scratch `--shared` clone at `f09b62945` → `prepare_clone.sh` → `checker.sh` (18:20:07–35) | **PASS 7/7**, strict apply, red-first 2 failed / 3 run, green 3/3, auth suite no new red, tsc rc 0; source checkout 0 modified |
| 2 | `LM_THINK=0` on `ornith:35b` | two-line diff task, `LM_NUM_CTX=4096`, load 3.87 < 16, no `LM_FORCE` (fleet live but the brief allowed a <30 s probe) | `done:true` / `stop`, 56 eval tokens at 89 tok/s, clean ```diff, 0 thinking chars; then `keep_alive:0` → `done_reason:"unload"`, `/api/ps` empty |
| 3 | **REFUSE live (a)** — real fleet, real clock | `night_run.sh` unmodified env, 18:32:24 | **rc 3 `G1-clock`** ("hour=18 outside 23:00-06:00") |
| 4 | **REFUSE live (b)** — real fleet, clock overridden | `NIGHT_HOUR_OVERRIDE=23` | **rc 3 `G2-panes`** naming the foreign pane `Secuura/Blockchain` (the three QA panes had closed between 18:2x and 18:32; the lane seat was live) |
| 5 | **REFUSE live (c)** — G3 on the real machine | scratch tmux socket with one fake `wednesday` pane + clock override, 18:33:29 | **rc 3 `G3-qa-procs`**: `pgrep -f launch_qa_ = 6` — another Wednesday seat was launching QA gatesets (`--check` runs) at that minute; a real refusal on a real measurement |
| 6 | **FIRE for real** — gates → memory → model → queue move → unload | `tmux -L scratch new-session -d -s fleet` + `@cockpit_name=wednesday`; `NIGHT_TMUX_SOCKET=scratch NIGHT_HOUR_OVERRIDE=23 NIGHT_QA_PGREP=zz_no_such_pattern_zz`; fake queue line `KS-0 input=<tiny_input.json> task=<tiny_task.md> nocheck=1 ctx=4096` (scratch queue/runs/log dirs) | **rc 0**: all 5 gates pass with measurements (load 2.00, `/api/tags` lists ornith), MEMORY: no loaded model, `memory_pressure free=91%`, `vm_stat` available 73.4 GB ≥ 30, **real Ornith call** (2.19 s, `done=True done_reason=stop content_chars=151`), verdict `HARNESS_ONLY`, line moved to `done.md` with verdict + run dir, gates re-checked, queue empty → stop, `ornith:35b unloaded at end`, `last_run.json` written |
| 7 | build path + BUILD_REFUSED + the unload of ANOTHER model | `gpt-oss:20b` loaded first (`keep_alive 10m`); `NIGHT_DRY_RUN=1` with scratch queue `KS-960` then `KS-871 ref=… line=280` | KS-960 → `BUILD_REFUSED rc=2 (no fix shape … a ruling, not a task)` and moved; KS-871 → real Linear read, `input.json` 33,108 B built, **`MEMORY: unloaded gpt-oss:20b (12.7 GB) keep_alive=0 → done_reason:"unload"`**, available 67.5 GB, verdict `DRY_RUN`, moved; rc 0 (attempted 2, run 1) |
| 8 | clone → prepare → checker inside the runner | scratch queue `KS-806 input=<pilot input> out=<control_positive>` (the `out=` test-only pin), `NIGHT_SCRATCH` in the scratchpad | **`RESULT: PASS (7/7)`** parsed as the verdict, clone at the pinned tip, checker 17 s, `source checkout tracked-modified: before=0 after=0` |
| 9 | `build_input.sh` on the three queue lines exactly as the runner calls them | bash loop over `queue.md` | KS-871 (pinned ref + line 280, ~8.3K prompt tokens) · KS-1072 (anchored on the quoted `(b.blockNumber \|\| 0) - (a.blockNumber \|\| 0)` → tip line 289, the ticket's `:240` had drifted to a comment) · KS-1087 (line 991 pinned, ~22.5K tokens → `ctx=49152`) — all rc 0, key set == KS-871 input |
| 10 | more builder refusals | KS-1129 (multi-site: "also cites anchorSchema.ts, documentRepo.ts, verification.ts"), KS-849 ("the fix-shape section itself says a decision/ruling is needed first"), KS-871 without `ref=` ("no in-process test imports middleware/audit") | rc 2 each, reason printed |
| 11 | installer without installing | `install_night.command --render-only <scratch>` → `plutil -lint` OK, 0 placeholders left, correct paths; `launchctl print gui/501/com.wednesday.ornith-night` → not loaded (expected); `WED_AGENT=tuesday` → rc 2 refusal | as expected |
| 12 | doctor.sh | full run 18:39 | `⚠ ornith night job NOT armed` (expected — Wednesday arms) · `✓ ornith:35b on the drive and served` · `✓ queue: 3 ticket(s)` · `✓ last run: rc 3 gate refused: G2-panes, 0.1h ago`; PREFLIGHT OK (7 warnings, 6 pre-existing) |

**NOT exercised (stated plainly):** (i) Ornith on a REAL ticket end-to-end (the fleet was live all evening; the brief forbade it) — the first real run is tonight's, and it is the first measurement of `think:false` on a 30K-token prompt and of `ctx=49152` on Ornith; (ii) the launchd fire itself (not armed); (iii) the `SKIP_MEMORY` branch (available memory never fell below 30 GB — the assertion ran, the skip path did not); (iv) the mid-run gate STOP after a real ticket (the re-check ran and passed each time; the stop path is the same `gates` function that refused in rows 3–5); (v) `HARNESS_FAIL` and `PREPARE_FAIL` branches; (vi) G3 passing on the real pattern (another seat was launching gates the whole time — G3 passed only under the documented test override).

## HOW

```
# step 1
cp -p task.md task.md.pre-0914-generic ; <Write the generic task.md> ; grep -n -i "806|sha256|wallet|attempt 1|userRepo|createHash" task.md → rc 1
git clone --shared --no-checkout "<SRC>" <scratch>/step1/clone ; git -C <clone> checkout --detach f09b6294… ; prepare_clone.sh <ks806 input> <clone> ; checker.sh <ks806 input> control_positive.out.md <clone>
# step 2
LM_MODEL=ornith:35b LM_THINK=0 LM_NUM_CTX=4096 LM_MAX_LOAD=16 bash local_model_task.sh <tiny task.md> <tiny input.json> <out.md> ; cat out.md.raw.json
curl -X POST :11434/api/generate -d '{"model":"ornith:35b","keep_alive":0}' ; curl :11434/api/ps
# step 5 (board read, read-only)
set -a; source "<Secuura>/4_Credentials/.env"; set +a ; python3 GraphQL issues(first:50, includeArchived:true, filter:{team KS, state.type in [backlog,unstarted]}) paged → scratchpad/board/ks_backlog_todo.json (363)
# step 7
bash night_run.sh                                      → rc 3 G1-clock
NIGHT_HOUR_OVERRIDE=23 bash night_run.sh               → rc 3 G2-panes
tmux -L scratch new-session -d -s fleet 'exec bash' ; tmux -L scratch set-option -p -t fleet:0.0 @cockpit_name wednesday
NIGHT_TMUX_SOCKET=scratch NIGHT_HOUR_OVERRIDE=23 NIGHT_QUEUE=<fire/queue.md> … bash night_run.sh   → rc 3 G3-qa-procs (6 live)
… NIGHT_QA_PGREP=zz_no_such_pattern_zz … bash night_run.sh                                       → rc 0, real model call
NIGHT_DRY_RUN=1 … (queue KS-960, KS-871) ; queue "KS-806 input=… out=…" with NIGHT_SCRATCH=<scratch>
bash install_night.command --render-only <scratch>/rendered.plist ; bash doctor.sh
tmux -L scratch kill-server
```
Scratch evidence (session scratchpad, not project files): `step1/` (control clone + checker.out), `step2/` (tiny probe + raw), `board/` (the Linear dump + the three candidate read files), `bi/` (built inputs), `fire/`, `dry/`, `chk/` (runner logs, done.md, run dirs), `rendered.plist`, `doctor.out`. The project-side `night/log/night_2026-09-14.log` + `last_run.json` hold rows 3–4 (the live refusals).

## CAVEATS

1. **Three tickets, not eight.** See FOUND. The list is honest about what the contract can check tonight; widening it needs either a test-only contract mode (red under a planted tamper, not at the tip — the coverage tickets) or a jest lane in the checker (originate). Neither is a one-evening change and neither was asked for.
2. **Line pins drift.** `KS-871 line=280` and `KS-1087 line=991` are as of develop `0e78c7270` (18:2x). The builder validates the line exists but cannot tell a drifted pin from a right one; the snippet-anchored path (KS-1072) is drift-proof. If `audit.ts`/`verification.ts` change before 23:30, re-pin or drop the pin and let the anchor pick (`KS-1087`'s anchor lands on the 200 body message line 999 — close, but the delete site is the defect).
3. **`ctx=49152` on Ornith is unmeasured.** The two `verification.ts` tickets carry ~22K prompt tokens; 32K left under 10K for the answer (Ornith's KS-871 answer was ~4.9K tokens WITH thinking). 48K is the first try; if the first night shows `done_reason: length`, the queue line takes `ctx=65536` (`ollama show ornith:35b` at 18:4x: context length 262144, 34.7B params — so 64K is inside the model's own window; memory for the KV cache is the only cost).
4. **The reference-test note is generated, not hand-written.** The 09-14 KS-871 note (hand-built) told the model exactly which mocks to return what; the script's note lists the reference file's `vi.mock` targets, quotes the fix sentence and names the defect line. Poorer guidance → expect a lower pass rate than the hand-built runs, honestly measured. KS-871's own line carries the same reference file the hand build used (`ks843`).
5. **G2 counts a finished-but-open pane as foreign.** A QA pane whose agent exited but whose shell stays open (`[cockpit] … exited — pane stays for inspection; exec bash`) keeps its `@cockpit_name`, so the census refuses. That is the conservative direction; the cost is a night lost if Wednesday wraps without closing panes. Doctor's last-run line will say `rc 3 gate refused: G2-panes` in the morning.
6. **G3 was never seen passing on the real pattern** (row 5 vs 6). `NIGHT_QA_PGREP` is a test-only override; the plist does not set it. If the morning shows `G3-qa-procs` refusals with no gate actually running, look for a stale `launch_qa_` shell (`pgrep -fl launch_qa_`).
7. **The memory assertion measures `free+speculative+inactive`** ("available"), with `free+speculative` and `inactive` printed apart, plus `memory_pressure`'s percentage. macOS keeps page cache as inactive pages, so "free" alone under-reports what the model can get; if Kam wants the stricter number, `NIGHT_MIN_FREE_GB` against `free+speculative` is a one-line change. `sudo purge` stays not-attempted (needs admin).
8. **`build_input.sh` cannot tell a coverage-only ticket from a defect** — KS-1123 builds fine (test-only ticket) and would FAIL A4 honestly at the checker. The queue's curation is what keeps those out; the builder's refusals are structural (files, fix shape, runner, reference), not semantic.
9. **`pgrep -x claude` is informational only** (printed in G3's line); the Wednesday pane itself is a claude process, so it cannot gate.
10. **The PARKED wording in `doctor.sh`'s local-model block and PORTABILITY item 14 is stale** (Qwen removed 14:25; Ollama came back drive-local for the head-to-head). Item 15 and the README section say so; the old lines were not rewritten (Wednesday's record to amend).
11. **Deletes: none.** Test artefacts are in the scratchpad; the scratch tmux server was killed (`tmux -L scratch kill-server` — a process, not a file). `night/log/` is not gitignored (the scheduler's `logs/` is) — Wednesday's call at commit time, same as `local-model/runs/`.
12. **`local-model/runs/` + `night/log/` gitignore state and the commit are Wednesday's;** nothing here was committed, no Linear write, no mail.
