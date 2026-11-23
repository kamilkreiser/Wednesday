# C3: the gate on Windows (lane W-GATE). Draft plan, 2026-11-23

DRAFT for Friday. Read-and-draft only: nothing in the project was changed, nothing was built, no test, no model run, no network call.

**Tags.** READ = I read that file and line. Bare `name:n` is a file in the repository at main `3164374` (read with `git show 3164374:<path>`). "plan 15" = `0_Brain/reference/2026-11-16_claude-to-claude/15_windows-plan-2026-11-20.md`; "04" = `04_design-revision-rulings.md` in the same folder; "WO-n" = the PC results file `windows/2026-11-2x_WO-n_results.md` there; "machine report" = `windows/2026-11-21_machine-report.md`. RAN = a read-only command I ran on the Mac today (named). REASONED = my inference. UNVERIFIED = not established today.

---

## 1. BLUF for the owner

1. **What C3 proves.** That on Windows the gate's hook really stops an action it is told to stop (a file write, a PowerShell command), and that it also stops the action when our program is dead, missing or hangs. Until that is shown there is no gate on Windows (READ 04:679). A second, smaller test checks that Windows file names cannot be spelled to sneak past it (READ 04:682).
2. **What it needs from you.** One yes on the board: about 44 short test runs of the smallest Claude model on your PC (each a few seconds), by the PC helper on its own or with you at the keyboard, your choice. Nothing else is needed to start: no install, no Administrator, no settings change.
3. **What could stop it.** (a) The test fails: then Windows has no gate until a fix is found (READ 04:679). (b) The second half of the test needs your PC to behave as if Git for Windows were not installed. I could not establish from sources that this can be done without uninstalling it. If not, I will ask you separately; the first half goes ahead either way.
4. **What C3 does not yet do.** It does not switch the gate on for the Windows agent. The program still refuses that on Windows (READ `crates/coagent-daemon/src/main.rs:96-102`). Turning it on is a later build, once these tests pass.
5. **Already done, so not asked again.** The local connection test that plan 15 put first (the single-user half of W3) already ran on your PC on 21 November and passed (READ WO-1:25-32, item 8).

---

## 2. What exists and what is missing, from source

### 2.1 `coagent-hook`: written for Windows, and how it behaves there

- **No platform split in the hook itself.** It forbids unsafe code (READ `crates/coagent-hook/src/main.rs:19`) and has no `cfg(unix)`/`cfg(windows)` line; its only `cfg!` lines are red controls (READ `main.rs:95, 111, 167, 181, 212`). Its one dependency on our code is `coagent-ipc` (READ `crates/coagent-hook/Cargo.toml:18`).
- **How it finds the daemon.** `coagent_ipc::endpoint_for_data_dir(&dir)` (READ `main.rs:123`). On Windows that makes the folder absolute and returns the named pipe `\\.\pipe\coagent-<encoded path>` (READ `crates/coagent-ipc/src/endpoint.rs:138-146`, rule at `:49-63`). Plan 15 said this line still built `daemon.sock` (READ plan 15:164); the code is newer and now uses the shared function. Two sources disagree; the code at `3164374` is the newer one.
- **What it does when the daemon is missing.** Connect fails, so the answer is "unreachable", then exit 2 with the one stderr line `coagent gate: daemon unreachable or refused - call blocked` (READ `main.rs:37, 136-139, 148-152, 164-171`). The same for a closed connection, a deadline of 10 s, an unreadable answer or any refusal (READ `main.rs:9-14, 35, 127-135, 174-226`). A crash or missing binary is left to `onFailure: "block"` (READ `main.rs:13`).
- **Has it run on Windows?** It was built on the PC (READ WO-1:22) and its 1 test passed there (READ WINDOWS-FINDINGS.md:16, "hook 1"). It has never been called by Claude Code on Windows: the C2 plugin had no hooks folder (READ WO-11:100) and the daemon there ran with `"gate":"off"` (READ WO-14_4:69). That exit code 2 blocks a call on Windows as on macOS is UNVERIFIED.
- **The connection code it uses is unchanged since it was tested on the PC.** RAN today: `git diff --quiet b8aa8b7 3164374 -- crates/coagent-ipc crates/coagent-hook` exit 0 (b8aa8b7 is the head WO-1 tested, READ WO-1:18).

### 2.2 What the kit's plugin maker does not do for Windows

`preview/make-plugin.sh` is a bash script that hands off to Python (READ `make-plugin.sh:1, 20`). In `preview/lib/pvpaths.py`:

| What | Where | Effect on Windows |
|---|---|---|
| Looks for `coagent-hook` and `coagent-mcp` with no `.exe` | READ `pvpaths.py:122-125` | Refuses a Windows bin folder (REASONED: `isfile` of the name without `.exe` is false). |
| Always makes `hooks/` and writes `hooks/hooks.json` | READ `pvpaths.py:139-145` | No way to make the MCP-only plugin C2 used; the PC helper wrote that by hand (READ WO-11:99-100). |
| Applies the macOS socket length rule, 103 bytes of `<data>/ipc/daemon.sock` | READ `pvpaths.py:24-25, 126-128` | Wrong rule. On Windows the limit is the pipe name's, at most 200 bytes after the prefix (READ `endpoint.rs:23`). |
| Forbidden-folder check built on `HOME` and `/` | READ `pvpaths.py:45-50, 60-61` | REASONED: with `HOME` unset and backslash paths this check would not match, so it would let through an out-dir inside the Claude config folder. Not run. |
| Refuses a single quote in any path | READ `pvpaths.py:73-75` | A shell-quoting rule; not needed in exec form, harmless. |
| Files made with mode 0600 | READ `pvpaths.py:103-106` | No meaning on Windows (REASONED). |
| Runs under bash | READ `make-plugin.sh:1` | Needs Git Bash; not there in the "without Git" set-up (REASONED). |

Also: the template's `plugin.json` says every call "goes through the CoAgent gate" even when no hooks are loaded (READ WO-11:101). A Windows template should not say that when it has no hooks.

### 2.3 What a Windows hook entry must look like

Today's template, both events (READ `preview/plugin-template/hooks/hooks.json.tmpl:9-12` and `:21-24`):

```
"type": "command",
"command": "'@BIN@/coagent-hook' --data-dir '@DATA@'",
"timeout": 30,
"onFailure": "block"
```

That is shell form: one string with single quotes, run by a shell. On Windows a shell-form string goes to "Git Bash on Windows, or PowerShell when Git Bash isn't installed" (READ 04:448), so the quoting meaning changes with the set-up. Exec form: when `args` is present Claude Code "spawns it directly with `args` as the argument vector. There is no shell", and "On Windows, exec form requires `command` to resolve to a real executable such as a `.exe`" (READ 04:449). Placeholders keep native backslashes in an exec-form hook (READ 04:456).

What must differ, for `PreToolUse` (matcher `*`) and `ConfigChange` alike (REASONED from 04:449 and the template):

```
"type": "command",
"command": "@BIN@\\coagent-hook.exe",
"args": ["--data-dir", "@DATA@"],
"timeout": 30,
"onFailure": "block"
```

No quotes inside `command`; the program name ends in `.exe`; the arguments move to `args`. The `.mcp.json` template is already in command-and-args form (READ `.mcp.json.tmpl:4-5`) and worked on Windows when written by hand (READ WO-12:6-7). The hook argument parser takes exactly `--data-dir <dir>` (READ hook `main.rs:76-79`), which this form passes as two elements. That Claude Code 2.1.330 on Windows honours this form: UNVERIFIED (it is what W1 tests).

### 2.4 What gate mode needs on Windows that has never run

1. **The program refuses `--gate` on Windows** (W-8): exit 2 with "the gate's Windows path rules and its hook have not been run there" (READ `crates/coagent-daemon/src/main.rs:96-102`; `engine.rs:98`; BACKLOG.md:1022-1025). The library can still be given a gate config on Windows (READ BACKLOG.md:1094-1097).
2. **Gate mode reads `HOME`** and refuses to start without it (READ `main.rs:195-200`). On Windows the profile folder is `USERPROFILE` (the daemon's own Windows rule uses it: READ `main.rs:48-53`). Whether `HOME` is set on the PC: UNVERIFIED.
3. **The gate judges every path by the Unix rules.** `HostOs::Posix` and `PosixNormaliser` are fixed in four places (READ `crates/coagent-daemon/src/gate.rs:30, 223, 236, 352, 390`). The Windows normaliser exists but nothing in the tree uses it outside its own file (RAN: `git grep WindowsNormaliser 3164374 -- crates` finds only `crates/coagent-policy/src/path/windows.rs:10, 12`).
4. **The Windows path rules have never run.** `windows.rs` is "UNTESTED: compiled (type-checked) ... only; never run" (READ `crates/coagent-policy/src/path/windows.rs:1`), and has no tests in the file (RAN: `grep -c '#\[test\]'` = 0); the spelling rules have one pure test (READ `winrules.rs:89-94`); the path test file is Unix-only (READ `crates/coagent-policy/tests/t04_paths.rs:3`); BACKLOG.md:57-60. The policy's Windows reserved-name list lacks `CLOCK$` (READ BACKLOG.md:1099-1101).
5. **A gated agent run headless cannot send.** Under the gate, `-p` turns every ask into a deny (READ `preview/demo/lan.md:16`). So a gated Windows agent needs a person answering its prompts (tier 3, READ `lan.md:17`), or a mode that allows without asking.
6. **Where this touches the owner's two modes** (noted only, not designed). "Approve and monitor" is the gated agent with a person answering, item 5. "Allow and monitor" is closest to the "both agree" mode, which is shipped dark (READ `docs/POLICY.md:64-68`); even with it on, a `PowerShell` command is never allowed by the mode and a `Bash` command only with a verified sandbox (READ `POLICY.md:86-91`), and native Windows has no sandbox (READ 04:452). REASONED: on Windows that mode would still ask on every shell command.

---

## 3. W1, the blocking experiment, as an exact run list

### 3.1 What it is ported from

- The spike text: port the hook client and stub daemon to one `.exe` over a named pipe; settings via `--settings` with an exec-form hook, `onFailure:"block"`; re-run the G1 and G2 case lists as PowerShell scripts; add "deny a `PowerShell` tool command"; default and bypass modes; both Git set-ups; record whether Defender or SmartScreen blocks the unsigned stub (READ `spikes/W-native-windows/RESULT.md:7-12`). Pass rule (READ 04:679).
- G1: 6 runs, 2 modes x (no hook, hook allow, hook deny), Write of `CANARY.txt` (READ `spikes/G1-deny-blocks-write/run.sh:10, 57-62`; `RESULT.md:4`).
- G2: 10 runs, all in bypassPermissions (READ `spikes/G2-dead-daemon-blocks/run.sh:13, 35-80`; `RESULT.md:4`).
- Why the macOS harness cannot be copied: the stub daemon and client use Unix sockets (READ `spikes/lib/stub_daemon.py:19`, `hook_client.py:16`); the hook is written in shell form with an environment assignment and `python3` (READ `spikes/lib/mk_settings.py:10`); the runner uses `timeout` and `[ -S ... ]` (READ `spikes/lib/common.sh:57, 78`); the model file path is a Mac path (READ `common.sh:13`).
- A known instrument fault to fix in the port: the summary keeps only the first 400 characters of a tool result, so the "onFailure" text check depends on the folder's path length (READ `m0_review/friday_rerun_G1_G2.md:12-13`). Text checks must read the whole result.

### 3.2 Proposed shape (a choice for Friday, not the owner)

- **Hook:** the REAL `coagent-hook.exe`, in the exec form of section 2.3, for every case except the crash case. REASONED: this tests the product's hook, not a stand-in. It departs from RESULT.md:7, which asks for a stub client; Friday rules.
- **Daemon side:** a new small spike program (Rust, path dependency on `coagent-ipc`, like `spikes/G1-G3-mesh/` has its own `Cargo.toml`) that binds `endpoint_for_data_dir(<dir>)` with `IpcListener::bind` (READ `crates/coagent-ipc/src/windows.rs:526`), logs each event to `events.jsonl`, and answers the hook's `gate` request with `{"id":1,"ok":true,"result":{"decision":<d>,"reason":<r>,"halt":false}}` (shape READ hook `main.rs:106-107, 174-195`). Modes: `allow`, `deny`, `hang` (never answer), as `stub_daemon.py` had (READ `stub_daemon.py:8-10`).
- **Crash role:** the same spike program run as the hook, exiting 1 with nothing on stdout (the real hook never exits 1: READ hook `main.rs:53-72`).
- **Missing role:** `command` naming a `.exe` that does not exist.
- **Runner:** a PowerShell script per RESULT.md:9, with Python 3.12 (present on the PC: READ machine report:53) allowed for the summary and settings helpers. Model id passed in by the work order. Each case's checks as G1/G2: the model really issued the call (else the case is VOID), the session's `permissionMode`, the file on disk, the daemon's witness (READ G1 `run.sh:28-54`; G2 `run.sh:15-31`).

### 3.3 The cases, one set-up

Prompt for the W family: G1's, word for word (READ G1 `run.sh:10`). For the P family: the same shape with "Use the PowerShell tool exactly once to run: `Set-Content -Path CANARY.txt -Value canary`" (new; REASONED). Default mode is the CLI's `manual` (READ G1 `run.sh:33`; listed by 2.1.330: READ WO-11:45-48) with `--allowedTools Write` or `PowerShell` so the control can succeed (READ G1 `run.sh:19-21`).

Every case below is ONE `claude -p` model run, smallest model.

| # | Case | Mode | Hook | Expected | A failure means |
|---|---|---|---|---|---|
| W1 | write, no hook | default | none | file created | the control is broken: case set void |
| W2 | write, hook allow | default | real hook, stub `allow` | created; stub saw PreToolUse(Write) with mode default | hook or pipe not reached on Windows |
| W3 | write, hook deny | default | real hook, stub `deny` | NOT created; tool result an error | **deny does not hold: no gate (blocking)** |
| W4 | write, no hook | bypass | none | created | control broken |
| W5 | write, hook allow | bypass | stub `allow` | created; mode bypassPermissions seen | as W2 |
| W6 | write, hook deny | bypass | stub `deny` | NOT created | **blocking** |
| P1-P6 | as W1-W6 with the PowerShell tool | both | as above | as above; stub saw `tool_name` PowerShell | P3/P6: **a denied PowerShell command ran: blocking** |
| F1 | no hook | bypass | none | created | control broken |
| F2 | daemon alive | bypass | stub `allow` | created | as W2 |
| F3 | daemon killed before | bypass | real hook, no stub | NOT created; text "daemon unreachable" | **dead daemon lets calls through: blocking** |
| F4 | daemon killed mid-call | bypass | stub `hang`, killed after the event arrives | NOT created | **blocking** |
| F5 | hook crashes, `onFailure:block` | bypass | crash role | NOT created; text `blocking because onFailure is "block"` | **blocking** |
| F6 | hook crashes, `onFailure` unset | bypass | crash role | created (fails open) | if NOT created: Windows differs from macOS here; record, not blocking |
| F7 | hook program missing, block | bypass | missing `.exe` | NOT created | **blocking** |
| F8 | missing, `onFailure` unset | bypass | missing `.exe` | created (fails open) | as F6 |
| F9 | daemon never answers, timeout 5 s, block | bypass | stub `hang` | NOT created; text `onFailure is "block"` | **blocking** |
| F10 | same, `onFailure` unset | bypass | stub `hang` | created (fails open on macOS) | as F6. REASONED: the real hook gives up after 10 s with exit 2 (hook `main.rs:35`), so F10 can only fail open if Claude Code's 5 s timeout fires first. |

Expected results are the macOS results (READ G1 `RESULT.md:8-13`; G2 `RESULT.md:6-18`). None has run on Windows.

Also recorded with NO model run: whether Windows warns on or blocks the built programs (RESULT.md:11; 04:516, 04:527). The PC is not a clean machine (READ machine report:9, 33-55): say so in the result (plan 15:219 says the same).

### 3.4 The count

**44 model runs = 2 set-ups x (Write 3 cases x 2 modes + PowerShell 3 cases x 2 modes + fail-closed 10 cases x 1 mode) = 2 x (6 + 6 + 10).**

- Read literally, 04:679 wants the fail-closed cases in default mode too: **64 runs = 2 x (6 + 6 + 10 x 2)**. REASONED for 44: bypass is the mode where nothing but the hook stands in the way (READ G2 `run.sh:3`), and macOS ran G2 in bypass only.
- F1 and F2 repeat W4 and W5 in shape (G2's prompt adds "or fails": READ G2 `run.sh:11`). Dropping them gives **40 = 2 x 20**.
- Re-runs: a case where the model never issues the call is void and must be run again (READ G1 `run.sh:28-30`). On macOS 0 of 16 were void (READ G1 `RESULT.md:13`, G2 `RESULT.md:18`: 22/0 and 26/0 passes). Allowance proposed: up to 6 (an estimate).
- **Ask: 44 plus up to 6 re-runs = at most 50.**

**Model level.** The smallest current model suffices: each case needs one tool call. G1 and G2 ran on `claude-haiku-5-5` (READ G2 `output.txt` header line; `friday_rerun_G1_G2.md:3`), and so did both C2 runs on the PC (READ WO-12:15; WO-14_4:15). The id is read from the live model list on the day, never typed in a script (READ `common.sh:12-13`).

**Wall time (estimate).** RAN today on the Mac, from the committed raw `result` events of G1 and G2: 16 runs, 82.1 s of model time in all, 3.8 s to 10.5 s each; the stream's `total_cost_usd` summed to 0.055 USD. On the PC one short run took 7.1 s wall (READ WO-12:16). Estimate: 10 to 20 s per case with start and checks, so about 4 to 8 minutes of runs per set-up, and 30 to 45 minutes per set-up for the helper with set-up and report. The cost figure is the stream's own number on macOS; how runs on the owner's account on the PC are billed: UNVERIFIED.

### 3.5 "Git for Windows present" versus "absent"

- **Present is the PC as it is.** Git 2.53 and Git Bash are installed; Claude Code there has a Bash tool (Git Bash) and a PowerShell tool (pwsh 7.6) (READ machine report:43-46, 58). Set-up A needs nothing.
- **What differs without it.** "Claude Code doesn't register the Bash tool at all" and PowerShell is enabled automatically (READ 04:445); a shell-form hook string goes to PowerShell instead of Git Bash (READ 04:448); the Monitor tool is gone (READ 04:454); and a shell-form hook that fails with `onFailure` unset can block instead of fail open (READ 04:450). Our exec-form hook avoids the shell difference (READ 04:466). So set-up B mainly checks the W and P families and the three fail-open controls in a session without a Bash tool.
- **Can set-up B be had without uninstalling?** UNVERIFIED. I did not read how Claude Code finds Git Bash on Windows (whether by `PATH`, a fixed install folder, the registry or a setting), so I cannot say that removing the Git folders from `PATH` in the run's own window hides it. Such a change would touch nothing on the machine beyond that one process (REASONED), so it is inside the helper's rules.
- **The measurement that settles it, at no extra model run:** run case W1 of set-up B FIRST in a window whose `PATH` has every Git for Windows folder removed, and read the session's tool list from the stream's first (`system`/`init`) event, which lists the tools (RAN today: the committed G1 stream `default-deny.stream.jsonl` line 1 has a `tools` field). If the list has no `Bash` and has `PowerShell`, set-up B is real; carry on. If `Bash` is still listed, stop set-up B there (1 run spent) and post card Q2.
- The same `tools` field also proves set-up A has a `PowerShell` tool; if it has none, the P cases of set-up A are void (UNVERIFIED whether the tool is on by default with Git present; the machine report says it runs pwsh, READ :58).

---

## 4. W4 and W3's single-user half

### 4.1 W4 (path spellings)

- **Needs.** One test per spelling class: drive-relative, UNC, `\\?\`, 8.3 short names, case, trailing dots and spaces, `file:stream`, junctions and links, forward slashes (READ `RESULT.md:18-19`; 04:499), plus reserved names and MSYS `/c/...` (READ 04:499). Pass: every class canonical or outside the workspace, none inside wrongly (READ 04:682).
- **A copied test program suffices.** A small new crate under `spikes/` with a path dependency on `coagent-policy`, calling `WindowsNormaliser.normalise(raw, cwd, env)` (READ `windows.rs:12-13`) over a table, built on the PC as the helper has done for a scratch crate before (READ WO-1:42-43). It changes nothing in the policy crate (plan 15:339). **0 model runs.**
- **Fixtures on disk.** Junctions: `mklink /J` worked without Administrator on the PC (READ BACKLOG.md:240, run 2). Symbolic links: Developer Mode is on (READ machine report:68); that it lets a normal window make one: UNVERIFIED. 8.3 short names: whether the drive makes them, and whether checking needs Administrator: UNVERIFIED; a short name that does not exist is recorded as "not tested". Case-sensitive folders: marking one was refused without elevation (READ BACKLOG.md:1088). Long paths are off (READ machine report:67).
- **What W4 does not show.** That the gate uses these rules: it does not (section 2.4 item 3).

### 4.2 W3's single-user half

- **Already RAN on the PC, 2026-11-21 (WO-1):** `cargo test -p coagent-ipc` 26 passed, 0 failed, 1 ignored (the second-account test) (READ WO-1:25-32); 1,000 round trips median 241.2 microseconds against the 20 ms bar (READ WO-1:61); a second daemon refused; the pipe's access list one entry for the logon session; the caller and owner checks across processes (READ WO-1:47-57, 95-99). Plan 15:226 ("W3's single-user half first") is overtaken.
- **The code tested is the code at `3164374`** (RAN: `git diff --quiet`, section 2.1).
- **Left in the single-user half:** README item 12, the two run-time red controls, not done because it needs a source change (READ WO-1:67). A scratch copy on the PC can do it with no model run. Items 11 and 20 need Administrator, item 5 another logon session (READ WO-1:58, 66, 94). Not needed for C3 (REASONED); not asked.
- **Proposed:** re-run `cargo test -p coagent-ipc` at the C3 head in WO-A (a minute, 0 model runs) and the red controls in a scratch copy. The second-account half (items 1, 9, 15, 17, 19, 22) and the credential store (no code: READ plan 15:221) stay out of C3.

---

## 5. Lane proposal

### 5.1 Split

- **C3a, W-GATE (this draft):** prove W1 and W4 on the PC. No product code changes.
- **C3b, a later lane (not briefed here):** the gate on Windows for real: lift the W-8 refusal, `USERPROFILE` for `HOME`, the Windows normaliser and `HostOs::Windows` chosen in `gate.rs`, the plugin maker's Windows branch, then a gated Windows agent with a person answering (section 2.4). Starts only after C3a passes (04:679). It touches daemon files and the preview kit, so it needs its own collision check.

### 5.2 C3a files (new files only, as plan 15:338 allows)

- `spikes/W1-windows-exec-hook/`: `Cargo.toml`, `Cargo.lock`, `src/main.rs` (daemon, crash roles), `run.ps1`, `cases.md`, `RESULT.md`, `raw/` (filled from the PC).
- `spikes/W4-windows-paths/`: crate, table, `RESULT.md`.
- `preview/plugin-template-windows/hooks/hooks.json.tmpl` (section 2.3 form) and a `plugin.json` whose description does not claim a gate it lacks. Plan 15:338 says "a Windows hook template under `preview/` (new file)"; the folder name is a proposal.
- Appends: `docs/M0-OUTCOMES.md` (a Windows section; it says today "Nothing here was measured on Linux or Windows", READ `M0-OUTCOMES.md:4`), `BACKLOG.md`.
- **Needs Friday's ruling:** `spikes/W-native-windows/RESULT.md` says "NOT RUN" (READ :1); updating it edits an existing file.
- **NOT in it:** `crates/**` (any W4 fault is a finding for the policy lane, plan 15:339), `preview/lib/pvpaths.py`, `preview/make-plugin.sh`, `crates/coagent-daemon/**`.

### 5.3 Built and checked on the Mac

- The spike program compiles and runs on macOS too (the ipc crate has a Unix back end: READ `crates/coagent-ipc/src/lib.rs:54-60`), so its allow/deny/hang roles can be checked against the real `coagent-hook` on the Mac by piping a hand-made PreToolUse event into the hook: 0 model runs.
- A Windows type-check and build of both spike crates with the kit's method (`cargo xwin`, READ BACKLOG.md:240; `scripts/windows/build.sh:17`).
- `run.ps1` cannot run on the Mac (REASONED: no PowerShell there assumed; UNVERIFIED whether `pwsh` is installed on the Mac).

### 5.4 Only the PC can show

Everything in section 3.3, the W4 table on a real disk, the Windows warning on the programs.

### 5.5 PC work orders, in order (times are estimates)

| WO | Who | What | Model runs | Time |
|---|---|---|---|---|
| WO-A | helper alone | bundle at the C3 head into `C:\c2c\<new>`; build hook, daemon, spike programs; `cargo test -p coagent-ipc`; ipc red controls in a scratch copy; W4 table; the model-free hook-to-stub check for every mode; settings checksums before and after; any Windows warning on the programs | 0 | 45 to 60 min |
| WO-B | helper alone, or the owner at the keyboard (card Q1) | W1 set-up A, 22 cases | 22 (+ re-runs) | 30 to 45 min |
| WO-C | as WO-B | W1 set-up B: case W1 first as the probe (section 3.5); stop if `Bash` is still listed | 22 (+ re-runs), or 1 if the probe fails | 30 to 45 min |

Rules as the earlier orders: no firewall, registry, security-setting or account change; per-user installs only for a build or test (none needed: Rust and the build tools are there, READ WO-1:9-12, machine report:51); nothing needing Administrator; the hook loaded only by `--settings` (READ G1 `RESULT.md:5`), so the owner's settings files stay unchanged and are checksummed as before (READ WO-12:29-30, 55-57).

### 5.6 Independent check

A QA seat that did not build it: re-derives every verdict from the `raw/` streams and stub logs (not from the helper's summary), checks each "NOT created" case for a real attempt (void rule), checks text assertions read the whole tool result (`friday_rerun_G1_G2.md:16`), and re-runs the Mac-side model-free checks. 0 model runs on the PC. An optional second sitting on the PC re-running W3, P3, F3 and F7 in set-up A would be 4 more runs: NOT in the ask.

### 5.7 Size (estimate)

Mac build 6 to 10 agent-hours, check 2 to 3; PC about 2 to 2.5 hours of helper time over three orders; owner: one card answer, plus up to about 1.5 hours at the keyboard only if he picks that option. Plan 15:342 estimated 15 to 30 agent-hours for all of W-GATE; that figure includes the C3b work (REASONED) and predates the kit and the PC's Rust tools.

---

## 6. Questions that are the owner's (card drafts)

### Q1. May the PC helper make up to 50 small model runs for the Windows gate test?

- **Premises.**
  - His allowance so far was "a rehearsal and the day" of C2 (READ `briefs_drafts/2026-11-23_windows-pc_WO-12_C2_rehearsal_run.md:5-7`), and both runs are spent (READ WO-12:8; WO-14_4:7). More runs are a new ask.
  - The test is the blocking one for a gate on Windows (READ 04:679).
  - 44 runs = 2 set-ups x 22 cases, plus up to 6 re-runs (section 3.4). Smallest model (section 3.4).
  - On macOS 16 runs of the same kind took 82 s of model time and the stream reported 0.055 USD in all (RAN today, section 3.4). Billing on his PC account: UNVERIFIED.
  - The PC helper asked him at the keyboard before each earlier run (READ WO-12:8; WO-14_4:15).
  - Each run writes one test file in a throwaway folder; the hook is loaded only for the run; his settings are checksummed before and after (section 5.5).
- **a. Yes, up to 50 runs, by the helper on its own, in two sittings, each reported.**
- **b. Yes, up to 50 runs, but only with me at the keyboard** (two sittings of about 30 to 45 minutes; estimate).
- **c. Yes, up to 70: the full reading of the design** (64 runs = the fail-closed cases in both modes too, plus 6 re-runs).
- **Recommendation:** a. These runs only write a test file in a throwaway folder, and the helper reports every one.
- **Default that keeps work moving:** no model run. WO-A (0 runs) and all the Mac work go ahead.

### Q2 (post ONLY if the WO-C probe shows Claude Code still finds Git Bash). The "without Git" half of the test

- **Premises.** The design requires both set-ups tested (READ 04:466, 04:679). Git for Windows is installed on the PC (READ machine report:43-44). Hiding it from the run's own window did not work (WO-C probe, to come). Whether removing and reinstalling Git for Windows needs Administrator: UNVERIFIED.
- **a. You uninstall Git for Windows for one sitting and reinstall it after** (your hands; possibly Administrator).
- **b. Leave the PC as it is; record W1 as run in one set-up only;** the second waits for another machine or a later choice.
- **Recommendation:** b. The first half already shows whether the hook blocks on Windows; uninstalling touches your other work.
- **Default that keeps work moving:** b.

No third card: nothing else in C3a needs an install, a removal or Administrator (sections 4.1, 4.2, 5.5).

---

## 7. What can start today with no answer from him (Mac only, 0 model runs)

1. Write the W1 spike program (daemon, crash roles) and `run.ps1` with the case table of section 3.3, the void rule and untruncated text checks.
2. Build it on macOS and check its roles against the real `coagent-hook` by piped events (allow, deny, daemon absent, hang until the 10 s deadline).
3. Type-check and build it, and the W4 crate, for Windows with the kit.
4. Write the W4 table; its pure part (`winrules::classify`) already runs on every system (READ `winrules.rs:1-2`).
5. Write the Windows hook template (section 2.3) and its `plugin.json`.
6. Draft WO-A (no model) and the C3b notes (section 2.4 list) for a later brief.

---

## 8. NOT READ / NOT MEASURED

- How Claude Code on Windows finds Git Bash, so whether a `PATH` change hides it (section 3.5). Not read; no network call.
- Whether exit code 2, exec form, `onFailure`, a hook timeout and the killing of a timed-out hook behave on Windows as on macOS. Docs read only through 04's quotations (04:445-456); nothing run.
- Whether `HOME` is set on the PC; whether the PowerShell tool is on in set-up A (the machine report says it runs pwsh).
- Whether Defender, SmartScreen or Smart App Control act on programs built on the PC (earlier PC-built programs started: WO-1, WO-11; kit-built copies never started: READ BACKLOG.md:870-873).
- Symbolic link creation without Administrator under Developer Mode; 8.3 short names on the PC's drive.
- Billing of model runs on the owner's account on the PC.
- `docs/POLICY.md` read in the parts found by searching for hook, mode, bypass, PowerShell and Windows (lines 1-30, 60-100, 125-160, 198-206, 281-360 by search hits), not whole; it has no `onFailure` text (it puts the hook binary out of scope: READ `POLICY.md:25`).
- `BACKLOG.md` read by searching for Windows, `.exe`, hook and plugin, not whole (1,135 lines).
- `preview/demo/lan.md` read lines 1-40 only; `preview/demo/windows.md` whole.
- `crates/coagent-daemon/src/gate.rs` read at lines 1-40 and 215-245 and by search, not whole; `crates/coagent-policy/src/path/windows.rs` lines 1-40 only; `winrules.rs` lines 1-30 and its test.
- `scripts/windows/build.sh` read by search only; `docs/WINDOWS-TESTS.md`, `docs/DAEMON.md` not opened.
- `spikes/lib/stream_summary.py` read by search only; `tui.sh`, `rustenv.sh`, `stub_mcp.py` not opened.
- 04 read at lines 445-545 and 665-700, not the rest of 500-700 beyond those (545-665 not read).
- The PC results WO-2 to WO-10 and WO-13, WO-14 parts 1 to 3 not read whole (WO-13 line 11 and 39 by search).
- The design files 05 and 06 that plan 15 cites (05:42, 06:585) not opened.
- No wall time or cost on the PC was measured; every PC time in this draft is an estimate.
