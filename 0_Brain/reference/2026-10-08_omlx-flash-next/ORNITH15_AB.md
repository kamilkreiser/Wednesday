# Ornith 1.5 vs Ornith 1.0: A/B on 20 graded night tasks (2026-10-08)

Run dir: `2_Project_Files/local-model/runs/ab_ornith15_2026-10-08/` (gitignored). The per-task evidence is in `tasks/<id>/{control,m15}/`, and the table data is in `results.json`.

## BLUF

- **Pass count is a tie: 17/20 for Ornith 1.5 and 17/20 for Ornith 1.0.** Same 20 prompts (sha256 identical to 1.0's record), same checker, first attempt. Applying night_run's retry-once rule leaves both at 17/20.
- **The two models disagree on two tasks, one each way.**
  - KS-1344 r1: 1.5 PASSES where 1.0 failed.
  - KS-1131 r3: 1.5 FAILS where 1.0 passed.
  - 1.5's two real failures are the same model error. The brief has a bare identifier `gap,` among quoted strings, and 1.5 rewrote it as the string `'gap'` / `'gap,'`. The retry repeated the error.
  - One shared FAIL (KS-1143 r1) is a harness/task-type defect, not either model. Leaving it out, the score is **17/19 each**.
- **Speed:**
  - Median decode: **82.4 tok/s for 1.5** (oMLX, 8-bit) vs **78.6 tok/s for 1.0** (Ollama).
  - Median wall per task: **13.4 s for 1.5**. For 1.0 it is 25.6 s as recorded, or 16.4 s once Ollama's model-load time is subtracted.
  - Median prefill: 2,299 vs 1,721 tok/s.
- **Memory stayed safe:** swap never grew (1002.06 MB baseline, 962.06 MB at the end), memory_pressure free never went below 52%, no guard trip, no 507.
- Conclusion: on this set, 1.5 is **faster but not more accurate**.

## Per-task table

The 1.0 numbers come from its recorded run. "ctl" is the current checker re-run on 1.0's own out.md: 20/20 reproduce the recorded verdict. Walls are client wall-clock. 1.0 tok/s is Ollama's eval rate from run.log. 1.5 tok/s is decode only, measured client-side (first to last streamed token); the server's own figure agrees within 0.4 tok/s on every task. Prompt token counts are identical for both models on all 20 tasks.

| # | Task (1.0 run) | Type | 1.0 verdict (ctl) | 1.5 verdict | 1.5 failed clause | Class | 1.0 wall s (no-load) | 1.5 wall s | Prompt tok | Completion 1.0 / 1.5 | tok/s 1.0 / 1.5 | Outputs identical |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 01 | KS-1344 r2 (09-26 night2) | code_patch | PASS 7/7 | PASS 7/7 | — | — | 64.1 (15.1) | 12.8 | 18,764 | 313 / 282 | 78.55 / 80.35 | no |
| 02 | KS-1344 r1 (09-26 night) | code_patch | **FAIL** (A5, A6) | **PASS 7/7** | — | 1.0 FAIL = model | 16.8 (14.7) | 12.2 | 18,354 | 313 / 309 | 78.34 / 81.77 | no |
| 03 | KS-1337 | code_patch | PASS 7/7 | PASS 7/7 | — | — | 60.4 (25.9) | 23.4 | 16,481 | 1,301 / 1,300 | 79.37 / 82.44 | yes |
| 04 | KS-1110 r2 | code_patch | PASS 7/7 | PASS 7/7 | — | — | 11.3 (11.3) | 9.7 | 9,191 | 512 / 511 | 79.89 / 86.77 | yes |
| 05 | KS-1110 r1 | code_patch | PASS 7/7 | PASS 7/7 | — | — | 63.6 (12.0) | 10.3 | 10,621 | 505 / 504 | 80.28 / 85.33 | yes |
| 06 | KS-1140 | code_patch | PASS 7/7 | PASS 7/7 | — | — | 61.0 (20.8) | 18.8 | 14,019 | 969 / 1,059 | 78.36 / 83.72 | no |
| 07 | KS-1128 (night & night2, same prompt) | code_patch | PASS 7/7 | PASS 7/7 | — | — | 44.0 (42.3) | 35.5 | 28,301 | 1,637 / 1,624 | 73.06 / 77.17 | no |
| 08 | KS-1281 | code_patch | PASS 7/7 | PASS 7/7 | — | — | 21.8 (20.2) | 17.2 | 12,102 | 1,018 / 1,018 | 77.82 / 84.19 | no |
| 09 | KS-1131 r4 | code_patch (self-testing) | PASS 7/7 | PASS 7/7 | — | — | 18.9 (17.5) | 14.5 | 14,999 | 653 / 654 | 77.49 / 82.43 | no |
| 10 | KS-1131 r3 | code_patch (self-testing) | PASS 7/7 | **FAIL** at A3c, retry also FAIL A3c | A3c: the brief's `+      gap,` is absent; 1.5 wrote `'gap',` | **model** | 17.3 (17.3) | 13.9 (retry 14.6) | 14,165 | 700 / 630 | 80.23 / 81.91 | no |
| 11 | KS-1131 r1 | code_patch (self-testing) | FAIL A3c (its retry FAIL A3c) | FAIL A3c, retry also FAIL A3c | A3c: same `gap,` line (1.5 wrote `'gap'`, retry `'gap,'`); 1.0 had dropped a different line, the `it('KS-1131 F-A …` title | **model** (both) | 27.8 (17.4) | 13.8 (retry 14.7) | 14,075 | 691 / 630 | 77.82 / 82.18 | no |
| 12 | KS-1143 r2 | code_patch (self-testing) | PASS 7/7 | PASS 7/7 | — | — | 25.6 (15.4) | 13.1 | 18,098 | 386 / 387 | 79.46 / 81.04 | no |
| 13 | KS-1143 r1 | code_patch | FAIL A3 | FAIL A3 | A3: touched set n=1, tests=0 ("cannot sequence red-first without exactly one test file") | **harness** (both) | 25.7 (15.5) | 13.0 | 17,803 | 402 / 387 | 78.57 / 79.62 | no |
| 14 | KS-965 | doc_patch | PASS 8/8 | PASS 8/8 | — | — | 22.9 (12.7) | 11.2 | 9,046 | 637 / 636 | 80.19 / 85.42 | yes |
| 15 | KS-851 | test_only | PASS 8/8 | PASS 8/8 | — | — | 18.0 (8.0) | 6.8 | 9,399 | 250 / 249 | 81.28 / 84.85 | yes |
| 16 | KS-1081 r2 | test_only | PASS 8/8 | PASS 8/8 | — | — | 8.6 (8.6) | 7.4 | 6,737 | 411 / 410 | 80.11 / 86.82 | yes |
| 17 | KS-1139 r2 | test_only | PASS 8/8 | PASS 8/8 | — | — | 9.0 (9.0) | 7.7 | 7,084 | 423 / 422 | 79.29 / 86.96 | yes |
| 18 | KS-1033 r2 | bash_patch | PASS 7/7 | PASS 7/7 | — | — | 32.1 (32.1) | 29.2 | 9,480 | 2,128 / 2,127 | 78.69 / 84.40 | no |
| 19 | KS-1084 r3 | code_patch | PASS 7/7 | PASS 7/7 | — | — | 42.3 (40.6) | 35.7 | 27,218 | 1,670 / 1,669 | 72.88 / 76.08 | yes |
| 20 | KS-1084 r2 | code_patch | PASS 7/7 | PASS 7/7 | — | — | 40.4 (40.4) | 35.3 | 26,988 | 1,688 / 1,672 | 74.20 / 77.31 | no |

**Totals:**
- PASS, first attempt: 1.0 17/20, 1.5 17/20.
- Both pass: 16 tasks. Only 1.5 passes: #02. Only 1.0 passes: #10. Both fail: #11 and #13.
- Byte-identical out.md between the two models: 8/20.
- Sum of walls: 1.0 631.7 s as recorded (396.8 s without load), 1.5 341.5 s.

## FOUND

1. **Accuracy is a tie on this set.** The one-each disagreement (#02 vs #10) is far too few to show a difference.
2. **1.5's only real failure is one repeatable defect.** It turns a bare-identifier `+` line, sitting among quoted-string `+` lines, into a quoted string.
   - It did this on both KS-1131 rounds whose brief contains `+      gap,` (#10, #11), and on both of their retries.
   - It passed the round whose rebrief has no such line (#09, r4).
   - 1.0 passed #10, the same brief.
3. **1.5 fixed the 1.0 miss on KS-1344 r1.** 1.0 put the `mockLoggerError.mockClear()` lines after the call, so A5 and A6 went red. 1.5 put them before it, giving PASS 7/7 on the original brief. 1.0 needed a second round to pass this task.
4. **Most outputs are the same or nearly the same.**
   - 8/20 are byte-identical.
   - Where they differ and both pass, 1.5's diff is usually cosmetic: it drops the function-context text after `@@ … @@` and one trailing context line.
   - #11 vs #13: 1.5 gives byte-identical output for KS-1143 r1 and r2. r1 fails at A3 only because r1's input predates the self-testing mode, which is the task-type defect recorded in done.md line 495.
5. **Speed:**
   - Decode: 1.5 is faster on every task, median 82.4 vs 78.6 tok/s (+4.8%).
   - Prefill: median 2,299 vs 1,721 tok/s (+34%).
   - Loading: 1.5 loaded once, in 12.35 s; 1.0's Ollama runs often paid a reload of 10 to 52 s.
   - Wall: like-for-like (1.0 without load) the median is 13.4 vs 16.4 s.
   - The 8-bit 1.5 at about 35 GB is still faster than 1.0's Ollama build (`ornith:35b`, 21.2 GB). The q4 label comes from the store listing in REPORT.md; the quantization was not re-measured here.
6. **Template and parser work with no client fix needed.**
   - `chat_template_kwargs.enable_thinking=false` gives 0 reasoning characters and no `<think>` leak on all 23 requests.
   - Every answer was a single fenced ```diff that the checker's A1 accepted.
   - Prompt token counts equal 1.0's on all 20 tasks, so the tokenizer is the same.

## TESTED

- **The set:** the 20 most recent Ornith 1.0 rows in `night/done.md` that have a RESULT verdict, deduplicated by prompt hash. done.md lines 515 to 487, excluding line 498.
  - The 1.0 records are 17 PASS and 3 FAIL.
  - Two duplicate pairs were collapsed: KS-1128 night/night2 and KS-1145 night/night2 each have one identical prompt. KS-1145 falls outside the 20.
  - **Excluded:** KS-1131 night2 (09-25 09:59, done.md line 498). Its prompt hash matches no preserved task.md version (current or any `.pre-*`), so the prompt cannot be reproduced. The next row, KS-1084 r2, takes its place.
  - Rows after 09-26 in done.md are Spark (deepseek) runs, not Ornith.
- **Reproducibility checks:**
  - For every task, sha256(task.md + input.json) equals the hash in 1.0's meta. Five tasks needed `task.md.pre-0925-redprefix` (#11, #12, #13, #19, #20).
  - Every clone's HEAD equals the input's tip. Tips: 179a4f32, 6ab9d502, 2bc5ccf6 and 3bad652d, all present in the source object store.
- **The control:** the current checker re-run on 1.0's own out.md in the same clone reproduced all 20 recorded verdicts. So the checker version, the clone and node_modules all grade as they did then.
- **The retry:** night_run's retry-once rule (its retry_feedback builder, copied verbatim) fired for 1.5 on #10 and #11. Both retries still FAILED A3c.

## HOW

- **Instrument:**
  - Server: oMLX 0.7.0 on 127.0.0.1:47780, `--memory-guard balanced`, `--max-concurrent-requests 1`.
  - Isolation: the server ran with its own `--base-path` (a copy of `tools/omlx/base/settings.json`), so the shared settings file is unchanged (checked with diff). The copy changed only the model_dir (a symlink to the 1.5 model only, so the 104 GB Flash model was not discoverable), the SSD cache dir (run dir, 10 GB cap) and max_context_window (65536, matching 1.0's num_ctx). Memory tier `balanced` was untouched.
  - Client: `omlx_call.py`, the oMLX twin of `lib/lm_call.py`.
    - It imports lm_call's SYSTEM_PREAMBLE and builds the identical user message.
    - Sampler matched to 1.0: temperature 0, repetition_penalty 1.15 over the last 512 tokens, max_tokens 32768, thinking off.
    - Streaming, so decode tok/s excludes prefill.
- **Grading:** the same per-ticket steps as night_run (`ab_item.sh`):
  1. a `git clone --shared --no-checkout` of the Secuura checkout, created under the run dir, detached at the tip;
  2. `prepare_clone.sh`;
  3. the task type's `checker.sh`, with TMPDIR in the run dir.
- **Order:** one task at a time; the checker ran after each model call. 1.0 was not re-run: all its records reproduced.
- **Controls:** prompt hash identity; the checker control on 1.0's output; the source checkout's tracked-modified count was 0 before and after every checker run (42 runs).
- **NOT tested:**
  - **Different engine and quantization.** 1.0 ran on Ollama, in the build named in REPORT.md's store listing; 1.5 ran on MLX 8-bit. The speed numbers compare the two stacks as deployed, not the two models at equal quantization. Ornith 1.0 on oMLX was not run.
  - **Sampler mapping.** Ollama's repeat_penalty and mlx's repetition_penalty share a name and a window, but equivalence of the two implementations was not measured.
  - **Single sample per task.** Temperature 0, so there is no variance estimate. With N=20 and a 1-1 split there is no statistical power.
  - **Different conditions.** 1.0's timings were taken on 09-22 to 09-26 under that day's load; 1.5's today, at a 1-min load average of 24.8 to 36.8 (two live seats).
  - **Context limits.** No task needed more than 28,301 prompt tokens, so oMLX behaviour near the 65K context is unmeasured.
  - **Possible untracked writes in the source checkout.** Writes into the source through the symlinked node_modules are unmeasured; only the tracked-modified count was checked.

## Memory readings

| When | vm_stat free pages (16 KB) | Wired | swap used | memory_pressure free | top PhysMem | 1-min load |
|---|---|---|---|---|---|---|
| Baseline, before load (17:36:38) | 4,531,681 (69.1 GiB) | 389,210 pages (5.9 GiB) | 1002.06 MB / 2048 MB | 92% | 25G used (6080M wired, 911M compressor), 70G unused | 24.81 |
| Loaded, after the last task (18:02:48) | 969,786 (14.8 GiB) | 2,637,267 pages (40.2 GiB) | 962.06 MB | 56% | 80G used (41G wired, 939M compressor), 15G unused | 36.80 |
| After stop (18:03:02) | 4,383,418 (66.9 GiB) | 365,535 pages (5.6 GiB) | 962.06 MB | 92% | 28G used (6088M wired, 939M compressor), 67G unused | 33.22 |

- **Ollama:** it was not running at the start (nothing on 11434, `/api/ps` refused), so there was nothing to unload. It was left down.
- **oMLX:** it reported the model at 34.91 GB actual, with a process memory ceiling of 70.6 GB for the balanced tier.
- **Guard** (a 2-second loop: swap growth over 256 MB above baseline, or free below 10%):
  - It never tripped.
  - Maximum swap was 1002 MB (growth ≤ 0); minimum free was 52%.
  - There was no HTTP 507.
- **Cleanup:**
  - The server was stopped with SIGINT and shut down cleanly ("Finished server process").
  - The guard was stopped through its stop file.
  - `lsof` shows nothing listening on 47780, and no omlx process remains.
- **Side effects outside the run dir:**
  - oMLX's startup re-published `~/.omlx/bin/omlx-cluster-python`, a symlink to the drive venv's python. The directory already existed from the 17:04 session.
  - `tools/omlx/base` was not used.
- **Left on disk (run dir, gitignored, about 15 GB):**
  - `cache/`: 9.9 GB of oMLX SSD KV cache.
  - `clones/`: 4.9 GB, 14 scratch clones.
  - `tmp/`: 19 MB.
  - These can be quarantined when no longer needed. No model files were touched.
