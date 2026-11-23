VERDICT: GO WITH NOTES — head d76a83bd4bffbcb366e5e7d8f65e1d76743ed51d

# QA-ALLOW-MEASURE: independent check of branch `allow-measure` (spike U-B1, measurements only)

Seat: QA-ALLOW-MEASURE, 2026-11-23. Brief: `2_Project_Files/friday/briefs_drafts/2026-11-23_coagent_QA-ALLOW-MEASURE_check_brief.md` (Friday).
Tags: TESTED = I ran it; READ = I read it. My scripts and outputs: `m1_review/gate_allow_measure_tests/` (listed at the end).

## BLUF (for the phone)
1. **Yes, Claude Code stays quiet when our hook says allow.** In default mode, with no allow rule, a file write and a shell command ran with no dialog. I saw this in the builder's runs and in my own separate run, where I checked every byte sent to the screen and no dialog was ever drawn. Without the hook, a dialog came up for both.
2. **The owner can be shown one line the model does not get: `systemMessage`.** It appeared on screen. The model did not quote it, and the request sent to the model right after the hook contains no trace of it. But Claude Code saves it in its transcript on disk and passes it to SDK hosts, so it is not private.
3. **A typed confirmation in a terminal is not agent-proof.** The agent's commands cannot open their own terminal. But a command the agent ran opened another terminal window of the same user by its device name, wrote on it and read a line typed there. That command ran because our hook allowed it. In APPROVE it would be asked first, but one approved command is enough.
4. **Still unmeasured:**
   - whether our allow beats auto mode's own reviewer when it would check or refuse a call;
   - whether our "ask" shows a dialog in auto mode, which is how fresh sessions start here;
   - the real plugin loading path, Windows and Linux;
   - whether the sandbox would block the terminal route.

## Head and base proofs (TESTED)
- `git ls-remote` against the GitHub remote, through the project deploy key: `d76a83bd4bffbcb366e5e7d8f65e1d76743ed51d refs/heads/allow-measure`, `3768a67d1d41b47439776657afbc114bd14bc439 refs/heads/main`. `merge-base` = `3768a67`, and there is one commit on the branch: `d76a83b`.
- The builder's STATUS (67 lines) ends with `d76a83bd…` and then `READY FOR QA ALLOW-MEASURE`.
- All comparisons were made by SHA in my clone `/private/tmp/claude-501/qam/clone`. In the project repo I used only `git --no-optional-locks remote get-url`.

## 1. Scope (TESTED)
- `git diff --name-status base...head`: 158 files `A`, all under `spikes/U-B1-hook-allow-silent/`, plus `M BACKLOG.md` and `M docs/M0-OUTCOMES.md`. Numstat: 30/0 and 19/0.
- Pure append: for both documents, the base file is a byte-for-byte prefix of the head file (194018 and 7359 bytes). Control: a copy of the base with one character changed failed the same test.
- Product paths: `git diff base...head -- crates scripts preview Cargo.toml Cargo.lock` is 0 bytes. No `Cargo` file is in the name list.
- Nothing walks `spikes/`:
  - `Cargo.toml` excludes `spikes`.
  - The policy tests read named files through `spike(rel)` (`crates/coagent-policy/tests/common/mod.rs:199-204`). None names U-B1: 0 hits for `U-B1` in crates, preview, ci and scripts. Positive control: the same grep finds `U6-` in `t01_table.rs`.
  - The `read_dir` calls found are all on test temp or store folders.
  - `ci/proposed-workflow.yml` runs only cargo fmt, clippy, test and deny.
  - The only `spikes/*` glob is `spikes/lib/common.sh:47-48`, a guard on a spike's own `work`/`raw`.
- **PASS.**

## 2. Every row against its raw capture (READ, with small TESTED counts)
Where "builder" is not written, the evidence is a committed raw file at the head (I extracted it with `git archive`). I also read the unredacted scratch logs; nothing from them is quoted here.

| # | Claim (RESULT.md row) | Tag | Exact supporting capture | Verdict |
|---|---|---|---|---|
| 1 | M1-default-ctl: dialog for Write and Bash, still up after 8 s, Escape, no files, 15/32 frames | MEASURED | `dialog.W.txt` "Do you want to create W1.txt?" / "❯ 1. Yes"; `dialog.B.txt` "Bash command … Do you want to proceed?"; `keys.log` 2× `KEY Escape`; `debug.excerpt.log` "Write tool permission denied", "Bash tool permission denied"; my frame count 15 of 32; `settings.json` = `{}` | SUPPORTED |
| 2 | M1-default-hook: both files, no key, 0/23 dialog frames, permissionDecisionMs 6 and 8 | MEASURED | `debug.excerpt.log` "Hook approved tool use for Write, bypassing permission prompt" then "tool_dispatch_start tool=Write … permissionDecisionMs=6" (same for Bash, =8); `keys.log` only 2 `SAY` lines and no KEY; my count 0 of 23; `cwd.listing.txt` B1.txt, W1.txt; hook stdin `"permission_mode": "default"` twice | SUPPORTED |
| 3 | M1-fresh-ctl: a fresh interactive session starts in auto mode; no dialog with no hook; classifier skipped | MEASURED | `startup-footer.txt` "⏵⏵ auto mode on"; `debug.excerpt.log` "Skipping auto mode classifier for Write: would be allowed in acceptEdits mode" (same for Bash); 0/23 dialog frames | SUPPORTED (see the M1 fresh point below) |
| 4 | M1-fresh-hook: hook saw `auto`, no dialog, the hook decided first | MEASURED | hook stdin `"permission_mode": "auto"` ×2; "Hook approved … bypassing permission prompt" ×2, ms 6 and 7; no "Skipping" line | SUPPORTED |
| 5 | Headless rows: init `default`, every Write/Bash issued ran, `permission_denials: []` | MEASURED | my parse of 5 streams: M3-hl Write; M5-hl Agent+Read; M6-hl Write+Bash; M7-hl Bash; M7-agentpane Bash. Every init `default`, every result `[]` | SUPPORTED |
| 6 | M2: Bash text `⎿ $ echo …` visible "at most 0.64 s" (default) and "1.25 s" (auto), then "Ran 1 shell command"; no text of ours | MEASURED | `frames.txt` default-hook: absent at t=…924.26, present at 924.57 only, absent at 925.21. So the bound the frames support is **< 0.95 s**, not 0.64 s. fresh-hook: absent at 789.85, present at 790.15 and 790.47, absent at 791.40, so **< 1.55 s**, not 1.25 s. Collapse to "Ran 1 shell command" and 0 hits of "owner" in every frame: confirmed | **OVER-CLAIMED** (the upper bounds; the rest is supported). Finding F1 |
| 7 | M3 interactive: only `systemMessage` on screen; PDR and ERR never; TSQ written to the terminal, title in one frame, replaced within 0.71 s; the model quoted only ADC | MEASURED | my marker counts. M3-int: SYS frames 10 / pane 1 (`⎿  PreToolUse:Write says: MK3SYSqig6a`), PDR 0, ERR 0, TSQ 0. M3-int-r2: `pane.bytes` TSQ 1, PDR 0, ERR 0; the title marker is in frame 9 only (absent at …166.53, present at 166.90, gone by 167.24, so < 0.71 s); the model's answer is `⏺ MK3ADCqig6a` only | SUPPORTED |
| 8 | M3 headless: SYS once as `system/informational`; ADC only in the model's answer and the result; the stream is not a full record of what the model receives | MEASURED | `stream.jsonl` line 7 `{"type":"system","subtype":"informational","content":"PreToolUse:Write says: MK3SYS9wg4y",…}`; ADC in events 11 and 12 only; event 7 (`user`/tool_result) holds no marker | SUPPORTED |
| 9 | M3 transcripts: ADC in an `api-request-blob`; SYS/PDR/TSQ/ERR in none; all five in `hook_success`, SYS also in `hook_system_message` | MEASURED (record names undocumented) | builder's `transcript_marker_counts.txt`. My own recount of the three transcripts (counts only) gives the same numbers, including M3-int-r2, which the builder did not record | SUPPORTED. Stronger evidence below (M3 point) |
| 10 | M4: 0 runs, by the table's condition | - | rows 2 and 4 | SUPPORTED |
| 11 | M5: subagent Read carried the parent's session id (= init = env), the parent's transcript path, plus `agent_id`/`agent_type` | MEASURED | `hook.stdin.jsonl` line 2: `"session_id": "<ID-1>"`, `env <ID-1>`, `agent_id abaa1aee6251cd375`, `agent_type general-purpose`. In the **unredacted** original: 1 distinct id across init, both events and both env values; the transcript_path is identical | SUPPORTED |
| 12 | M6: Write gives PostToolUse with whole content etc.; Bash exit 3 gives PostToolUseFailure `error: "Exit code 3\nM6-OUT\nM6-ERR"`; U9 exit 0 has stdout/stderr/interrupted/isImage/noOutputExpected | MEASURED | M6 `hook.stdin.jsonl`: `PostToolUse` Write `tool_response` keys `content, filePath, originalFile, structuredPatch, type, userModified`, `duration_ms 4`; `PostToolUseFailure` Bash `error` as quoted, `is_interrupt false`. No PostToolUse for the Bash although it was registered (`settings.json` lists PreToolUse, PostToolUse, PostToolUseFailure). U9 `raw/hook-on/input.…13617.json` keys as stated | SUPPORTED |
| 13 | M7-int: "not a tty", `??`, `/dev/tty: Device not configured` | MEASURED | `m7.out`: `M7 tty=not a tty` / `ps … ??  S` / `line 4: /dev/tty: Device not configured` / `M7_OPEN=fail` | SUPPORTED |
| 14 | M7-hl: the same with `claude -p` running inside the pane | MEASURED | `m7.out` same lines. Claude's own controlling tty was not recorded, but it follows from tmux starting it in the pane | SUPPORTED (Note N6) |
| 15 | M7-posctl: the probe run straight in the pane opened /dev/tty and read `TTYLINE77` | MEASURED (no model) | `m7.out`: `tty=/dev/ttys010`, `ps … s010 S+`, `M7_OPEN=ok`, `M7_READ=ok [TTYLINE77]` | SUPPORTED |
| 16 | M7-otherpane: a no-terminal process opened another terminal by path (`crw--w----`), wrote, and got the FIRST typed line | MEASURED (no model) | `other.out`: `runner tty=not a tty`, `?? `, `pane tty=/dev/ttys010 mode=crw--w----`, `WRITE_OPEN=ok`, `READ_OPEN=ok`, `OTHER_READER_GOT=[TTYLINE88]`; `pane_reader.out` `[TTYLINE99]` | SUPPORTED |
| 17 | M7-agentpane: the same done by a command the agent's Bash ran; its reader got `TTYLINE99` | MEASURED | hook stdin `"command": "bash otherprobe.sh /dev/ttys010"`; `other.out` `agent-cmd tty=not a tty`, `??`, `WRITE_OPEN=ok`, `READ_OPEN=ok`, `AGENT_READER_GOT=[TTYLINE99] rc=0`; `pane_reader.out` `[TTYLINE88]`. The mode bits were recorded in row 16, not in this case | SUPPORTED (Note N6) |
| 18 | VOID: none | - | every model case shows the tool call (hook stdin, a dialog, or the stream's tool_use) | SUPPORTED |
| 19 | Isolation: settings checksums identical before and after; no trust dialog | MEASURED | `checksums.before/after.txt` identical; no `trust.txt` in any raw folder. My own reading at 13:0x shows the same two sha256 values | SUPPORTED |
| 20 | `CLAUDE_CODE_AUTO_MODE_MODEL` ignored for `claude-sonnet-5[1m]`; no classifier request in any run | MEASURED | 12 of 12 full debug logs carry the WARN line; 0 classifier request/verdict lines and 0 sonnet dispatches in any log (my grep) | SUPPORTED |

**Counts: 20 rows. SUPPORTED 19, OVER-CLAIMED 1 (row 6), UNDER-CLAIMED 0, WRONG 0.**

Points the brief asked me to settle:
- **M1 default, dialog in any frame?**
  - None in 23 frames. Frames were saved only when the screen changed, 0.30 s apart at the closest; the longest gaps (≈16 s) are idle screens.
  - A key press would appear as a `KEY` line in `keys.log`, as in the control's `KEY Escape`. The hook case has none.
  - The sampler alone could miss a dialog shorter than about 0.3 s. Two other things rule one out:
    - The debug field the builder cites, `permissionDecisionMs=6/8`, is the time from the start of the permission check to dispatch. It is 6-8 ms, and next to it is the line "bypassing permission prompt". A dialog that then waits for a key cannot fit in 6 ms.
    - My own reproduction captured every byte the pane received, and no dialog text appeared in it (item 4).
  - In the control, the dialog is there for both tools: Write at 1 s, Bash at 2 s, each still up after 8 s.
- **M1 fresh: what the captures show.**
  - The footer reads "⏵⏵ auto mode on (shift+tab to cycle)" and the hook received `"permission_mode": "auto"`. In default mode the footer reads "⏸ manual mode on" while the hook gets `default`, so the screen name and the hook name differ.
  - The session's own settings cannot explain it. I read the keys of every settings file that could apply:
    - user settings in `$CLAUDE_CONFIG_DIR` and in `~/.claude`: no `permissions` block, no `defaultMode`, 0 allow rules;
    - no `settings.local.json` there, no managed settings, no project `.claude/` settings in any parent of the run folder;
    - the debug log watched only the config-dir settings file and the run's own file.
  - So on this machine a flagless start lands in auto by Claude Code's own default. The permission-modes page quoted in RESULT.md says the same.
  - Claude Code's state file carries cached server feature entries about auto mode (names only read). The start mode may therefore depend on the account or the server, not only on the version. RESULT.md correctly says "on this machine". The design should not assume it everywhere (Note N1).
  - In auto, both calls ran without a hook only because Claude Code judged them "allowed in acceptEdits mode". That says nothing about auto mode for other calls.
- **M3: is "the model never receives systemMessage" MEASURED?**
  - The builder had two instruments:
    - The model quoted only ADC, in three runs. This is a real but weak negative: a small model failing to quote something.
    - SYS is absent from `api-request-blob` records. That depends on an undocumented format. And blobs alone are not the request: I found that the second prompt and the tool result are in no blob.
  - **I closed that gap (TESTED, `m3_resolve_requests.py`).** Each `api-request` record names its messages by sha256. I reproduced the hash recipe from a blob's own hash, then resolved every name. In M3-int and in M3-int-r2, the request sent right after the hook resolves fully to three records: the assistant tool_use, the user tool_result, and the system blob carrying ADC. None holds SYS, PDR, TSQ or ERR, and ADC, the positive control, is found there.
  - So, at the turn after the hook: SYS was not in what Claude Code recorded as sent, the model did not quote it, and the control field was in both. MEASURED is fair for "not sent at that turn" on 2.1.330. "Never" (resume, compaction) stays UNVERIFIED, as RESULT.md says.
  - `systemMessage` reached the owner: it was on screen in both interactive runs.
  - The positive control is real: ADC was quoted by the model in all three runs and resolved into the request.
- **M5:** checked against the unredacted stdin (row 11).
- **M6:** row 12. The failure event's exit code is only text, and stdout and stderr are merged in it.
- **M7 and its additions:**
  - The agent's Bash had no terminal: `??` and "not a tty", in both the interactive and headless runs.
  - A command the agent ran opened `/dev/ttys010` (`crw--w----`: owner read/write, group write only) by its path, wrote `WRITTEN-BY-AGENT-COMMAND`, and got a typed line.
  - The typed lines were split between two readers (one to each), which shows a real race for input, not a copy.
  - **Not overstated.** The other terminal was a tmux pane the runner created. It is not a Terminal.app window, but it is the same kind of same-user pty, so the step to an owner's window is REASONED, and R7 marks it so.
  - **Slightly understated in one way, overstated in none.** RESULT.md does not say that the opening command ran because our hook answered allow. In APPROVE, that command would be asked first. The reach therefore needs one shell command that runs unasked or approved, or a background reader left from any earlier ALLOW period.
  - Claude Code's sandbox was not on in any run: 0 sandbox lines in all 12 debug logs. RESULT.md does not record this. It matters less after the owner ruled 12:33:20 that ALLOW terminal commands are not tied to the sandbox, but it is unmeasured whether the sandbox would block the device-path open (Finding F3).

## 3. The stub against the real hook (READ + TESTED)
- READ, `crates/coagent-hook/src/main.rs`:
  - `:229-235` builds `{"hookSpecificOutput":{hookEventName, permissionDecision, permissionDecisionReason}}`;
  - `:57-58` prints `v.to_string()` with `writeln!`;
  - the exit code is 0.
  - The keys are already in alphabetical order, so serde_json gives the same bytes with or without key-order preservation.
  - The reason for an owner allow is "allowed by the owner" (`crates/coagent-policy/src/engine.rs:172`).
- TESTED (`stub_vs_real.sh`):
  - The committed `hook_stub.py`, fed a synthetic PreToolUse event, printed exactly the expected 133-byte line, with exit 0 and an empty stderr. Control: a line with one byte changed is detected as different.
  - Each plain-allow case's committed `hook.out.PreToolUse.json` (M1 ×2, M5, M6, M7 ×3) is byte-identical to it. The three M3 files differ, as designed, by the documented extra fields.
  - Claude Code's debug log echoes the parsed object as exactly that shape in each hook case.
- Differences, and whether they could matter:
  - (a) Python launched with `-I` against a Rust binary: start-up latency only, measured 40-48 ms per call, well inside the 30 s timeout. Could not change behaviour.
  - (b) Loaded through `--settings`, not `--plugin-dir`: a different loading path. RESULT.md lists this as UNVERIFIED. Could matter in principle; not measured by either of us.
  - (c) The stub registers no `ConfigChange` hook, which the real plugin also has. No config change happened in any run, so no effect.
  - (d) **The four M1 runs ran with an earlier revision of `hook_stub.py`:** their stdin records lack the `env_CLAUDE_CODE_SESSION_ID` field, also in the unredacted original. So the committed stub is not byte-for-byte the program that ran M1. Its stdout is shown to be identical by the debug log, so no result changes (Finding F4).

## 4. My own reproduction (TESTED): **AGREES with the builder's M1**
- **Rig (mine, not the builder's runner):**
  - `qa_repro.sh` and a shell hook `hook_allow.sh` that prints the same 133-byte line with `printf`;
  - a private tmux server `tmux -L qam-<random>` per run;
  - Claude Code 2.1.330 interactive with `--permission-mode default --strict-mcp-config --no-chrome`, the hook ONLY through `--settings` (control: `{}`), with this seat's own wiring removed from the environment;
  - model `claude-haiku-5-5`, read at each run from `models_latest.json` `levels.haiku.model_id`;
  - frames polled every 0.1 s, and also **every byte the pane received** (`pipe-pane`), searched with escape sequences and whitespace removed.
- **Runs: 3 of my 4.**
  - Run 1 was **VOID**, a rig error. The workspace-trust dialog's default is "No, exit", my Enter took it, and Claude Code exited. 0 model dispatches in its debug log, no prompt reached a model, nothing was created. I fixed the rig to select "Yes, I trust this folder" explicitly.
  - Run 2: hook case. Run 3: no-hook control, same sitting, 30 s later, same prompts, same mode flag.
- **My pane, hook case:**
  - Footer `⏸ manual mode on`; hook stdin `permission_mode: default` for both calls.
  - The pane showed `⏺ Write(QW.txt)` / `⎿  Wrote 1 line to QW.txt` / `1 qa-write`, then for the Bash `Ran 1 shell command`.
  - Both files existed 1 s after each prompt. Keys after the trust dialog: only the two prompts.
  - 0 dialog frames in 32 frames (median gap 0.16 s). In the whole byte stream: "Do you want" 0, "Esc to cancel" 0, "Create file" 0, "Bash command" 0, while "Wrote 1 line" 1 and "Ran 1 shell command" 1.
  - Debug: "Hook approved tool use for Write, bypassing permission prompt", `permissionDecisionMs=7`; the same for Bash, `=8`.
- **My pane, control:**
  - Write dialog "Create file … Do you want to create QW.txt? ❯ 1. Yes … Esc to cancel" at 1 s, and Bash dialog "Bash command … Do you want to proceed?" at 2 s.
  - Each was held 3 s, then Escape; no files were created.
  - The pane ended with `Rejected write to QW.txt` and `Interrupted`. Debug: "Write tool permission denied", "Bash tool permission denied".
  - In its byte stream, "Do you want to create" 1 and "Do you want to proceed" 1, the **positive control for the byte instrument**. A first naive search without whitespace removal found 0 even here, so I kept only the robust form.
- **Isolation:**
  - Owner settings sha256 were identical before and after each run (`202ed862…`, `1a518679…`), the same values the builder recorded.
  - No allow rule, no bypass, no `--dangerously-skip-permissions`. Only `claude-haiku-5-5` was dispatched.
  - My tmux servers are gone. Their stale socket files were moved into my work dir, not deleted.
- **Raw capture:** `gate_allow_measure_tests/repro_raw/run-hook/`, `run-ctl/`, `run-hook_VOID1/`, and `model_runs.log`. It is redacted (UUIDs to `<ID-n>`, config dir to `<CCD>`, etc.), and my own scan finds 0 identity hits there (item 6).

## 5. Run count and ceiling (TESTED)
- **The builder made 12 model runs, counted three ways, all 12:**
  - `runs.log`: 12 lines;
  - scratch case folders with a debug log that dispatched to the model: 12, the four M1 + M3-int, M3-int-r2, M3-hl, M5, M6, M7-int, M7-hl, M7-agentpane;
  - Claude Code transcript folders for those run folders: 12, one main session each, plus one subagent file in M5.
  - M7-posctl and M7-otherpane have no debug log and no transcript: no model, as claimed. The ceiling is 16, so this is within it.
- **Ceiling:**
  - `count_run` (`am.sh`) counts non-empty lines of `runs.log` BEFORE each run and refuses when the count is ≥ 16.
  - Every model path goes through it: `hl()`, `tui_start()`, and `m7_hl` directly.
  - TESTED (`ceiling_test.sh`, the function extracted verbatim, `claude` shimmed, so no process ran): with 15 lines it allows "MODEL RUN 16 of 16"; with 16 lines it prints `RUNNER REFUSED: model run 17 would exceed the ceiling of 16 (count=16)` and exits 99.
  - The builder's own "recorded refusal" exists only as text in its STATUS. Its `ceiling-test.log` holds only the 16-line fake counter (Note N4).

## 6. Redaction and names (TESTED)
- **Method:**
  - My own scanner `qa_scan.py`, independent of `redact.py`. Names are read from the machine at run time and never written down.
  - Classes: account name, short first name as a word, email (generic plus the two known addresses), home path and any `/Users/<x>`, machine names (four variants), the config-dir literal, tokens (sk-ant, bearer, hex ≥ 40, opaque ≥ 48), UUIDs, `req_`, `msg_`.
  - Each file is scanned in four forms: as is, with ANSI/OSC removed (`pane.bytes`), with shell backslashes removed (`command.txt`), and with control characters removed.
  - Positive controls: a planted line hits every class; a name split by an escape sequence is caught in the escape-free form; a shell-escaped home path is caught in the unescaped form. `selftest PASS`.
- **Scope:** all 158 committed files of the spike folder and the 49 added lines of the two documents.
- **Results:**
  - Account name 0, home path 0, machine name 0, config-dir literal 0, in every form.
  - Email 1, request id 1, UUID 1: these are `redact.py`'s own synthetic selftest literals (`x@example.org`, `req_011ABCDEFGH`, `123e4567-…`), as the builder said.
  - Tokens 46: all checked by shape. They are the four sha256 settings checksums, path segments, and the thinking-block `signature` fields of four streams. None is a credential.
  - **`msg_` API message ids: 25, in 5 `stream.jsonl` files.** These are not in the brief's list, and main already carries the same kind in `spikes/B16-search-command-forms/raw/*.stream.jsonl` (Note N2).
  - **Not redacted, but no identity in them:**
    - the workspace path in shell-escaped form in the 10 `command.txt` files;
    - a URL-encoded form inside an OSC-8 link in `M3-int-r2/pane.bytes`.
    This contradicts RESULT.md's "Paths shown as `<RUN>`…" in letter only, since my scan found no name, home or host in them (Note N3).
- **Meaning check** (`redaction_meaning_check.py`; placeholders turned into wildcards, every line matched against its unredacted original):
  - `M3-hl/stream.jsonl`: 14/14 lines match, and the markers, decisions and `permission_denials` survive.
  - `M5-hl/hook.stdin.jsonl`: 3/3 lines match.
  - `M1-default-hook/debug.excerpt.log` against my own run of the builder's filter on the full log: 33/33 lines match. `allow` drops from 26 to 22, inside the replaced worktree path `…/allow-measure`, which is not a decision.
  - Lines the excerpt filter leaves out of the full logs (M1-default-hook, M1-default-ctl, M1-fresh-ctl, compared by message type) are start-up, file-write and MCP lines, and **Claude Code's six builtin hook modules** (`cc-plugin-privacy … tool.check`, `cc-plugin-diff … tool.call`, …). Those modules run in every case and its control alike, so none changes a verdict. They are worth knowing for the real product (Note N5).

## 7. Conclusions R1-R7 and the BACKLOG entries (READ)
- **R1-R7:** each is tied to a measurement and marked REASONED; none is stated as measured.
  - R1, R5, R6: no stronger than their rows.
  - R2: sound. It relies on U1 for a hook `ask` producing a dialog in bypass, but **a hook `ask` in auto mode is not measured**, and APPROVE in a flagless session depends on it (see what remains unmeasured).
  - R3: sound, but carries F1's number ("under 1.3 s" should read "under about 1.6 s").
  - R4: "without the model receiving it" holds at the turn after the hook, now with the request-chain evidence (section 2).
  - R7: true as worded ("not beyond reach just because /dev/tty fails"). It should add that the measured route needed one shell command that ran unasked, here because of our hook allow, and that the sandbox was off (F3).
- **BACKLOG, six entries, all in the file's form:**
  1. M7: fact correct. The text "a terminal prompt must not be counted as agent-proof" is a design conclusion inside a BACKLOG entry, and so are the title words "in a terminal window" (measured: a tmux pane pty) (F2).
  2. M6: fact correct. The "Scope:" line ("registers both events and parses the exit code from the error text") picks an implementation for the result lane, a design round's choice (F2). Cited `docs/DAEMON.md:869`; the "Registered for `PreToolUse` and `ConfigChange` only" text starts at `:868`.
  3. M3: fact correct; UNVERIFIED replay correctly flagged.
  4. M2: carries F1's numbers ("at most 0.64 s … 1.25 s", title "under 1.3 s").
  5. M1 auto / classifier: fact correct; it defers to Friday's ruling.
  6. `rustenv.sh`: READ only. The cited line 2 does compute the root three levels above `spikes/lib`, and `${BASH_SOURCE[0]:-$0}` explains the zsh case. Not re-run by me.
- **`docs/M0-OUTCOMES.md`** append: faithful to RESULT.md, except that it carries F1's "under 1.3 s" and drops the word "undocumented" for the transcript record in its M3 line.
- **NOT DONE (the auto classifier pair): declining was right.** The control would have sent a classifier request to `claude-sonnet-5[1m]`, which Claude Code would not let anyone pin down: the debug WARN line in all 12 logs. That conflicts with "smallest model only". What remains unmeasured because of it:
  - whether a PreToolUse allow overrides an auto-mode classifier that would REVIEW or DENY a call. In fresh-hook the hook decided first ("bypassing permission prompt", no classifier line), which suggests it does, but only for calls the classifier skipped anyway;
  - next to it, also unmeasured: whether a hook `ask` produces a dialog in auto mode.

## 8. Side effects (READ, plus my own)
- **Builder:**
  - Claude Code rewrote its own state file in the config dir and left 12 transcript folders under `projects/` for the run folders (confirmed by listing; counts read only).
  - I searched the config dir and `~/.claude` for any other file named with the 12 session ids: none.
  - Settings checksums are unchanged now.
  - Its private tmux server `am-qntc3t` is gone ("no server running"). **Its socket file is still in the tmux socket folder** (stale and harmless), and **Claude Code also left 12 empty scratchpad folder trees** (`/private/tmp/claude-501/-…-am-<case>-cwd/`, 0 files). STATUS does not mention either (Note N7).
  - No process of the builder's is running: `pgrep` for the stub, the runner, the probes and the tmux name found none.
- **Mine:**
  - 3 model runs.
  - Two folder-trust entries for `/private/tmp/claude-501/qam/run-{hook,ctl}/cwd` added by Claude Code to its state file, because I answered the trust dialog in my own pane. I did not edit or revert them.
  - Two transcript folders under the config dir's `projects/`, left in place.
  - Claude Code's two empty scratchpad folders for my runs, moved into my work dir.
  - My three tmux servers are gone, their stale sockets moved into my run folders.
  - No process of mine is left.

## Findings
| ID | Severity | Finding (exact capture) | Suggested fix, in words |
|---|---|---|---|
| F1 | Minor | M2's MEASURED upper bounds are tighter than the frames allow. `raw/M1-default-hook/frames.txt`: the command text is absent at `t=1795397924.26`, present at `924.57` only, absent at `925.21`, so visible < 0.95 s, not "at most 0.64 s". `raw/M1-fresh-hook/frames.txt`: absent at `789.85`, present at `790.15` and `790.47`, absent at `791.40`, so < 1.55 s, not 1.25 s. The builder used the first frame WITH the text instead of the last frame WITHOUT it, though it did this correctly for the 0.71 s title bound. I weighed §3's "MEASURED statement a capture contradicts": the claim's substance (the text goes within about a second and leaves "Ran 1 shell command") holds, and no conclusion, requirement or design choice depends on the bound, so I rate it Minor, not Major. Friday may rule otherwise | Change both numbers in RESULT.md (M2 row), BACKLOG entry 4 and M0-OUTCOMES ("under 1.3 s" becomes "under about 1.6 s; seen in 1 and 2 frames"), and state the bound rule (last frame without to first frame without) |
| F2 | Minor | Two BACKLOG entries carry design decisions. Entry 1: "a terminal prompt must not be counted as agent-proof" and the title's "in a terminal window" (measured: a tmux pane pty made by the runner, `raw/M7-agentpane/pane_tty.txt` `/dev/ttys010`). Entry 2: "Scope: … registers both events and parses the exit code from the error text" | Keep the facts and put the conclusions as "for the design round (P2 surface; result lane)". Say "another same-user pty (a tmux pane)" |
| F3 | Minor | The limits of M7+ are not all written down. (a) The agent's opening command ran because our hook answered allow (`raw/M7-agentpane/hook.stdin.jsonl` `"command": "bash otherprobe.sh /dev/ttys010"`, out = allow); in APPROVE it would be asked first. (b) Claude Code's sandbox was off: 0 sandbox lines in all 12 debug logs, and RESULT.md does not say so. (c) The device path was given to the agent in the prompt; discovery was not measured | Add one line each to the M7+ row or the instrument limits, and qualify R7 ("given one shell command that runs unasked or approved, or a reader left running from an earlier ALLOW period"). Keep the conclusion: a typed terminal confirmation is not agent-proof |
| F4 | Minor | The committed `hook_stub.py` is not the revision that ran the four M1 runs. `raw/M1-default-hook/hook.stdin.jsonl` and `M1-fresh-hook` lack `env_CLAUDE_CODE_SESSION_ID`, which the committed stub always writes (in the unredacted originals too). The printed JSON is shown identical by each run's debug log ("Parsed initial response: {…allow…allowed by the owner}") | Say so in cases.md: the M1 runs used the stub before the env-logging line was added; stdout unchanged; cite the debug lines |
| N1 | Note | The fresh start mode was auto with no settings key causing it (section 2); Claude Code's state file holds cached server feature entries about auto mode, so the start mode may differ by account, not only by version | Design: detect the mode from the hook's `permission_mode` at run time; never assume default |
| N2 | Note | 25 `msg_…` API message ids are committed in 5 streams (precedent on main: B16) | Add `msg_` to `redact.py`'s classes next time (also my QA redactor does it) |
| N3 | Note | The workspace path is left in shell-escaped form (10 `command.txt`) and URL-encoded form (`M3-int-r2/pane.bytes`); no identity in it | Redact the escaped and URL-encoded forms too, or soften RESULT.md's "Paths shown as …" |
| N4 | Note | The 17th-run refusal is recorded only in STATUS text; `tools/tmp/am/ceiling-test.log` holds the fake counter, not the refusal output | Keep the refusal's printed output in the spike folder |
| N5 | Note | 2.1.330 runs six builtin hook modules (`cc-plugin-privacy` `tool.check`, `cc-plugin-diff` `tool.call`, …) in every run; the debug excerpts drop them. The same in cases and controls, so not a confound | One line in RESULT.md's isolation section |
| N6 | Note | M7-agentpane's mode bits come from M7-otherpane (same path, earlier pane); M7-hl's claim that the `claude -p` process had a controlling tty is inferred from tmux, not recorded | Record `ls -l` of the tty and `ps -o tt` of the claude process in each case |
| N7 | Note | The builder's stale tmux socket `am-qntc3t` and 12 empty Claude Code scratchpad folders under `/private/tmp/claude-501/` are not in STATUS's side-effects list | Add them; move them into the scratch folder if wanted |

No Blocker. No Major.

## What was NOT checked
| Item | Why | Who could check it |
|---|---|---|
| Hook allow against an auto-mode classifier REVIEW/DENY | Needs a classifier request to an unpinnable larger model; outside the smallest-model rule | Friday's ruling on the model rule, then a builder seat |
| Hook `ask` in auto mode (does a dialog appear?), which APPROVE depends on in a flagless session | Not in this lane's table; no run budget for it here | A builder seat, 2 runs, same rig |
| The real plugin path (`--plugin-dir`, real `coagent-hook` + daemon) | No product build allowed in this check | The W-GATE-TEST or a later lane |
| Windows and Linux behaviour of 2.1.330 | Mac only | C3b |
| Whether the sandbox blocks opening another tty by path | Not run by the builder; not in my brief's 4 runs | A builder seat, 1 run with the sandbox on |
| Other routes to the owner's terminal (`tmux send-keys`, AppleScript, TIOCSTI) | Not tried by the builder (listed UNVERIFIED) | A builder seat |
| Replay of `hook_success`/`hook_system_message` records to the model on resume or compaction | Not measured | A builder seat |
| `cargo fmt --all --check` and the `rustenv.sh` BACKLOG claim | No build or tool chain run in this check; the folder holds no Rust | Read only here; anyone with the toolchain |
| The documentation quotes in RESULT.md, re-read against the live pages | Not fetched by me | Any seat with web access |
| Whether the frames' 16-s gaps hide anything | They are unchanged-screen gaps by construction (frames are saved only on change) | - |

## Files of this check (`m1_review/gate_allow_measure_tests/`)
- **Scripts:**
  - `stub_vs_real.sh` (+ `.out.txt`);
  - `ceiling_test.sh` (+ `.out.txt`);
  - `qa_scan.py` (+ `qa_scan.out.txt` for the committed files, `qa_scan_testsfolder.out.txt` for this folder);
  - `redaction_meaning_check.py`;
  - `m3_resolve_requests.py` (+ `.out.txt`) and `m3_transcript_marker_counts.py`;
  - `qa_repro.sh`, `hook_allow.sh`, `qa_repro_analyse.py`, `qa_bytes_dialog.py`, `qa_redact.py`.
- **Reproduction raw (redacted):** `repro_raw/run-hook/`, `repro_raw/run-ctl/`, `repro_raw/run-hook_VOID1/`, `repro_raw/model_runs.log`.
- **My own slip, recorded:** one early shell command of mine began with `cd /`, which the brief forbids. It changed nothing and was not repeated.
