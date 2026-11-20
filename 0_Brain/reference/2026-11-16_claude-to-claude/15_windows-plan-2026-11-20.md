DONE

# CoAgent on Windows: plan of 2026-11-20

Written by a design and discovery agent for Friday. Documents only: nothing was built and nothing in the project was changed.

**How to read the tags.** READ = I read that file and line at the code head or in the design folder. MEASURED = I ran the command named and report its output. DOCS = read today at the URL given. REASONED = my inference, not a measurement. UNVERIFIED = not checked today.

**Code head.** `2bba2a468a5cce04f5d7189bdf76cbbecfbfab14`, clone `/private/tmp/claude-501/mcs2/clone` (MEASURED: `git -C … rev-parse HEAD`). A bare `crates/…:n` below is a line at that head. "03", "04", "05", "06", "12", "13" are the design files in this folder.

**The owner's words this plan answers** (as given to me by Friday; verbatim except the two bracketed places, where a seat's name and another project's name are left out under this document's naming rule): "lets prioritise the work on windows.  it would be great to have this running as [another seat] is working on [another project] that will need windows". Earlier the same day: "I am also back home and have revived my old windows machine ... the machine is not very powerful so I do not recommend doing much work on it" and "ideally, it would also be a good test of Claude to Claude for you to communicate with that machine".

**What is still unknown.** The machine report has not arrived. The Windows version, processor, memory, and whether WSL or a compiler exists are UNKNOWN. Every step below says what each answer changes.

---

## 1. BLUF for the owner

1. **The shortest honest route is native Windows, in stages, with the Windows machine as the guest.** The Mac hosts the meeting point. The Windows machine only dials out to the Mac over the home network. All compiling happens on the Mac. The old machine only runs small finished programs. (Route C in section 2.)
2. **Less is broken than the notes said.** I type-checked every part for Windows today. Ten of eleven parts pass. Only the background program fails, with 23 errors that come from three causes: the data folder's permission checks, reading the user's identity, and the stop signals. (Section 3. The check used stand-in C files for eight parts, so it proves the Rust code only.)
3. **What you would see, step by step.** Step 1: one small file copied to the Windows machine, a command typed there, and the Mac shows "connected". No AI on the Windows side yet. Step 2: a Claude Code session on Windows and one on the Mac send each other a request and a reply. Step 3, later: the permission gate also runs on Windows, so every action there is checked.
4. **What is needed from you.** Four decisions, drafted as cards in section 5: whether the first link may run on Windows without the gate; where the Windows programs are built (this needs one install on the Mac, or a heavier one on the Windows machine); how the data folder is protected for the first link; and what may be installed on the Windows machine. Then about 30 minutes of your hands at the Windows machine for step 1, and again for step 2.
5. **Rough size (an estimate, sized by counting the files and lines each step touches and comparing with this week's lanes; not measured).** Step 1: about 12 to 20 agent-hours of build and check, in two lanes, plus 2 to 4 hours for the build kit. Step 2: 2 to 4 more hours, mostly at the machine. Step 3, the gate on Windows: 15 to 30 agent-hours and several sessions at the machine, because the six Windows experiments were never run and the first one can stop the plan.
6. **One thing to know before you say yes.** Native Windows has no Claude Code sandbox (DOCS: https://code.claude.com/docs/en/sandboxing). So even with our gate working there, an approved command on Windows can do anything your account can do. Running inside WSL 2 would give the sandbox back, but it is the Linux build, which has never been run, and it is not the native Windows the product has to support anyway.

---

## 2. Routes compared

### 2.1 What each route needs from the machine

| Machine report says | Route A or C (native) | Route B (WSL 2) |
|---|---|---|
| Windows older than 10 version 1809 | Claude Code is not supported (DOCS: https://code.claude.com/docs/en/setup, "Windows 10 1809+ or Windows Server 2019+"). Only step 1 (no AI on that side) is possible. | Not possible: `wsl --install` needs "Windows 10 version 2004 and higher (Build 19041 and higher) or Windows 11" (DOCS: https://learn.microsoft.com/en-us/windows/wsl/install). |
| Windows 10 between 1809 and 2004 | Works. | Only by the manual WSL install path. UNVERIFIED. |
| Less than 4 GB memory | Below Claude Code's stated need ("4 GB+ RAM", same setup page). Step 1 still possible. | Worse: a Linux virtual machine runs beside Windows. REASONED. |
| 32-bit Windows | Not possible: Claude Code needs "x64 or ARM64" (same page), and the installed build target is 64-bit (MEASURED, section 3.1). | Not possible. REASONED. |
| ARM64 Windows | Needs a different build target, which is not installed. UNVERIFIED whether the 64-bit Intel build runs there. | Needs an ARM64 Linux build. |
| Virtualisation off in firmware | No effect. | WSL 2 will not start until the owner turns it on in the firmware. UNVERIFIED (general knowledge). |
| Git for Windows absent | Fine for steps 1 and 2. Claude Code then "uses PowerShell as the shell tool instead" (DOCS, setup page). Step 3 must be tested both with and without it (READ 04:466). | Not needed ("WSL setups do not need Git for Windows", DOCS, setup page). |
| A Rust compiler and the Microsoft build tools present | Opens the option of building on the machine. Not recommended on a weak machine. | Not relevant. |

### 2.2 Route A: native Windows, everything at once

**What must be built.**
- The background program (`coagentd`) for Windows: the data folder checks, the user identity, the stop signals, the name of the local connection, stopping the helper process (section 3.3). MEASURED: 23 type errors today.
- The local connection on Windows (a named pipe): the code exists and type-checks but "has never been run" and has no check of who is calling (READ `crates/coagent-ipc/src/windows.rs:1-4, 18-24`; READ BACKLOG.md:162-166).
- The hook program wired the way Windows needs: one real `.exe` started with no shell (READ 04:449, 04:462). The preview's hook template is the shell form with single quotes (READ `preview/plugin-template/hooks/hooks.json.tmpl`, the two `"command"` lines). DOCS (https://code.claude.com/docs/en/hooks, "Failed hooks on Windows without Git Bash"): "put the program in `command` and its arguments in `args` to use exec form, and add `"onFailure": "block"`".
- The path rules for Windows: written and type-checked, "UNTESTED" (READ BACKLOG.md:57-60).
- A way to build `.exe` files, and the preview's set-up scripts redone for Windows (they are bash and Python: READ `preview/demo/setup.sh`, `preview/make-plugin.sh`, `preview/replay/run.sh` exist; contents not read line by line).

**What is unproven.** All six experiments W1 to W6 (READ BACKLOG.md:38-41; `spikes/W-native-windows/RESULT.md:1`: "NOT RUN"). W1 is blocking: "without a fail-closed hook on Windows there is no gate there" (READ 04:679).

**What the rulings and the design say.** Native Windows is in the one beta (READ 05:42, n8 "One beta with everything"; 06:586). The owner provides the machine (READ 05:29). Signing comes later and is his act (READ 05:38; 06:584). Every PowerShell command asks, as on the Mac (READ 05:37; 06:566-570).

**Weak machine.** All compiling can be on the Mac if a cross kit is installed there (card Q2). Running the finished programs is light. Running the test suites on the machine is not light (section 6, lane W-TESTS).

**Security.** No sandbox (DOCS above; READ 04:481-483). No Unix owner and mode checks: Windows needs its own access check on the data folder, which "needs its own design" (READ BACKLOG.md:240). The pipe is limited to the logon session by its access list, but the same-user caller check is not built (READ `windows.rs:18-24`).

**For the other project that will need Windows.** It gets what it needs: a real Windows machine with an agent session on it that other agents can reach.

**Cost of doing it all at once.** Nothing is visible to the owner until W1 passes, and W1 needs model runs on the machine with him present (READ 06:585: "Spikes W1 and W3 … wait for that day and need him present").

### 2.3 Route B: WSL 2 on the Windows machine, running the Linux build

**What must be built.** In code, possibly nothing: the Unix code paths are behind `cfg(unix)`, which Linux satisfies (READ `crates/coagent-daemon/src/datadir.rs:24`, `util.rs:53`, `engine.rs:296, 394`). Whether it compiles and passes on Linux is NOT MEASURED: no Linux build target is installed in the project toolchain (MEASURED: the toolchain folder holds only `aarch64-apple-darwin` and `x86_64-pc-windows-msvc`).

**What is unproven.** Linux has never been run: "Not run in M0: Linux halves (U3, U12)" (READ BACKLOG.md:38). Known Linux-specific doubts already on record: the ipc gate tests are compiled for macOS only (READ `crates/coagent-ipc/tests/gate_ipc.rs:3`, `gate_r2_ipc.rs:3`: `#![cfg(target_os = "macos")]`); the daemon tests use `lsof` and `/bin/kill` (READ BACKLOG.md:238); the socket path limit of 103 bytes is the macOS figure (READ `engine.rs:87-88`); identity-file leftovers on Linux are REASONED only (READ BACKLOG.md:544).

**What a Linux run would have to prove first.** (1) The whole workspace builds. (2) `scripts/check.sh` is green on Linux. (3) The red-control runners are red where they should be. (4) The same-user check on the socket works with Linux's credential call. (5) The replay (`preview/replay/run.sh`) passes 23 of 23.

**Can that be proven on this Mac?** No, not without a Linux container or virtual machine, and **a container or VM is NOT available unless the owner agrees**. The other place is inside WSL on the Windows machine itself, which is exactly the heavy work he asked us to avoid there. A hosted Linux build machine is a third place and is a spend decision (card Q2, option c).

**What the rulings and the design say.** "WSL2 remains supported as a Linux target" (READ 04:806). WSL 2 is offered as advice for a machine the host does not want exposed (READ 04:493). It does not satisfy "native Windows" in the beta (READ 05:42).

**Weak machine.** WSL 2 needs an administrator, a restart (DOCS: https://learn.microsoft.com/en-us/windows/wsl/install: "Open PowerShell in administrator mode … then restart your machine"), and memory for a Linux virtual machine beside Windows. Compiling would happen inside WSL on that machine, or on the Mac with a Linux cross kit (an install on the Mac, same kind of decision as card Q2).

**Security.** The best of the three: the Unix owner, mode and same-user checks apply as on the Mac, and Claude Code's sandbox is supported (DOCS, setup page table: WSL 2 "Supported"; sandboxing page: needs `bubblewrap` and `socat`).

**Network.** If the Mac hosts the meeting point, WSL only dials out, which the default network mode allows. A server inside WSL 2 is not reachable from the home network by default (DOCS: https://learn.microsoft.com/en-us/windows/wsl/networking, "This isn't the default case in WSL 2"). So the Windows machine could not host under this route without extra set-up.

**For the other project that will need Windows.** Weaker. The agent lives in Linux. Whether it can drive Windows programs from there, and whether the sandbox allows that, is UNVERIFIED.

### 2.4 Route C: native Windows in stages, Windows as the guest first (recommended)

The same destination as route A, cut so that each stage shows the owner something and nothing waits for the blocking experiment.

| Stage | What runs on the Windows machine | What it proves | Needs |
|---|---|---|---|
| C1 | `coagentd.exe` and its `ctl` command only. No Claude Code. | The link across machines, with the Mac's gate on the host side. This is tier 1 of the existing cross-machine recipe (READ `preview/demo/lan.md:15`). | Lanes W-IPC and W-DAEMON; a way to build `.exe` files (Q2); the data folder decision (Q3); the owner's word to open the Mac's meeting point to the home network (Q5). |
| C2 | Also a Claude Code session with our message tools only, no hook, the daemon not in gate mode. | An agent on each side talking. Tier 2 of the same recipe (READ `lan.md:16`). | `coagent-mcp.exe` (type-checks today, MEASURED); the owner's answer on an ungated first link (Q1). |
| C3 | The hook and the gate. | The full preview across Mac and Windows. | W1 passing in both set-ups; the Windows hook wiring; W3, W4. |

**Why the Windows machine is the guest.** The guest only makes an outgoing connection to the relay named in the invitation (READ `crates/coagent-daemon/src/main.rs:115-125`, the `--relay-url` and `--relay-pin` flags; READ `lan.md:21-31`). So the Windows side needs no listening port, no firewall change (the checking seat is forbidden to change one: READ `Launch_Friday_Windows.cmd:137-139`), and no helper-process handling. The expected firewall prompt when Windows hosts (READ 04:526, UNVERIFIED there) is avoided.

**What is unproven.** For C1 and C2: that the Windows code runs at all (never run), that an empty environment for child processes works on Windows, that the pipe name scheme is sound, that a copied unsigned program is allowed to start (READ 04:516, 04:527: UNVERIFIED there). For C3: everything in route A.

**Security differences, stated plainly.** In C2 the Windows agent is not gated by us. It still has Claude Code's own permission prompts. Both machines are the owner's and the link is on his home network. The Mac side stays gated. This is a posture decision and it is his (Q1).

**For the other project that will need Windows.** C2 already gives a native Windows agent session that another agent can send requests to. C3 makes it safe to leave less attended.

### 2.5 Recommendation

**Route C.** Reason: every hour goes into work the ruled beta needs anyway (native Windows, READ 05:42); the measured gap to a first link is small (three causes in one crate, section 3.2); the weak machine only runs finished programs and only dials out; and the blocking experiment W1 no longer stands between the owner and a first visible result.

**Route B is kept as a fallback, not started.** It becomes worth a card only if the machine report shows WSL 2 already installed and working, or if W1 fails on native Windows. Its real cost is not code but proof: Linux is unrun, and proving it needs a container, a VM, or heavy work on the weak machine.

---

## 3. Inventory, measured

### 3.1 How the measurements were made

- Toolchain set up as `/Volumes/Laptop-DEV/FRIDAY/2_Project_Files/friday/coagent_merge_check.sh` does: work dir `/private/tmp/claude-501/wplan`, `tools/cargo/bin` and `tools/rustup` as links, `COAGENT_TOOLS` and `CARGO_TARGET_DIR` exported inside the work dir, `. scripts/env.sh`. `cargo fetch --locked` exit 0.
- MEASURED: installed targets in toolchain 1.100.0 are `aarch64-apple-darwin` and `x86_64-pc-windows-msvc`. The `-gnu` Windows target is not installed, so it was not run.
- One cargo process at a time. Heavy-job count before each run: 1 every time.
- Nothing was installed. No `cargo build`, no `cargo test`.

**Two kinds of run, and they are not equal.**
- **Plain:** `cargo check --locked --target x86_64-pc-windows-msvc -p <crate> [--all-targets]`. A real result.
- **Stand-in:** the same command with three environment variables that point the C compiler step at files in my work dir: `CC_x86_64_pc_windows_msvc=/usr/bin/clang`, `CFLAGS_x86_64_pc_windows_msvc="-ffreestanding -I<work>/stubinc"` (three stub headers: `assert.h`, `string.h`, `stdlib.h`), `AR_x86_64_pc_windows_msvc=<work>/standin_lib.sh` (a wrapper that turns the Microsoft archiver's arguments into `ar`). I did this because one dependency, `ring v0.17.14`, compiles C code and this Mac has no C headers for Windows. The C objects it produces are never linked or run and may be wrong. **A stand-in result proves only that the Rust code type-checks.** Friday may discard these rows; the plain rows stand without them.

### 3.2 Results per crate

| Crate | Plain, library and programs | Stand-in, library and programs | With tests (`--all-targets`) |
|---|---|---|---|
| coagent-proto | exit 0, 0 errors | not needed | stand-in set-up: exit 0 |
| coagent-ipc | exit 0, 0 errors | not needed | plain: exit 0. Its two gate test files are empty on Windows (`#![cfg(target_os = "macos")]`) |
| coagent-policy | exit 0, 0 errors | not needed | stand-in set-up: exit 0 |
| coagent-hook | not run without tests | exit 0 | plain: exit 0 |
| coagent-mcp | not run without tests | exit 0 | plain: exit 0 |
| coagent-crypto | exit 101, 1 error | exit 0, 0 errors | stand-in: exit 0 |
| coagent-roster | exit 101, 1 error | exit 0, 0 errors | stand-in: exit 0 |
| coagent-audit | exit 101, 1 error | exit 0, 0 errors | stand-in: exit 0 |
| coagent-relay | not run plain (depends on `ring`) | exit 0, 0 errors | stand-in: exit 0 |
| coagent-cli | not run plain | exit 0, 0 errors | stand-in: exit 101, 26 errors, all in test files |
| coagent-daemon | not run plain | **exit 101, 23 errors**, all in the library | not run (the library does not compile) |

**The one plain failure (crypto, roster, audit; the same error).** `error: failed to run custom build command for 'ring v0.17.14'`, caused by `ring-0.17.14/include/ring-core/check.h:27:11: fatal error: 'assert.h' file not found`. `ring` reaches those crates through `snow` (MEASURED: `cargo tree --target x86_64-pc-windows-msvc -i ring`). This is the "C compiler for the Windows target" gap already on record (READ BACKLOG.md:167-170). It is a gap in this Mac's tools, not in the code.

**Daemon: 23 errors, three kinds, three causes** (stand-in; log `/private/tmp/claude-501/wplan/stub_check_coagent-daemon.log`).

| Kind | Count | First of its kind | Cause |
|---|---|---|---|
| E0425 "cannot find value" | 3 | `crates/coagent-daemon/src/engine.rs:299:38` (`uid`); then `:418:17` (`sigterm`), `:419:17` (`sigint`) | `uid` is set only under `#[cfg(unix)]` (`engine.rs:296-297`, from `util.rs:53-57`); the signal watchers exist only under `#[cfg(unix)]` (`engine.rs:394-401`) but are used unconditionally (`:418-419`). |
| E0599 "no method" | 11 | `engine.rs:299:18` (`DataDir::open`); then `gate.rs:255:33` (`read`), `gate.rs:469:14` (`write_atomic`), `store.rs:427:24`, `:448:21`, `:454:24`, `:466:21`, `:526:44` (`quarantine`), `:567:44`, `:577:21` (`quarantine_bytes`) | Every method of `DataDir` that touches the disk is `#[cfg(unix)]` (`datadir.rs:113, 149, 171, 206, 227, 243, 270, 298`). |
| E0277 "size not known" | 9 | `gate.rs:257:21` | Follow-on of the missing `read`. Not a separate cause. |

rustc stops at the library, so the `coagentd` program file `src/main.rs` was not type-checked for Windows. Read by eye instead (section 3.3).

**CLI tests: 26 errors** (stand-in; log `stub_alltargets_coagent-cli.log`): 10 × E0433 "cannot find `unix` in `os`", 15 × E0599 (Unix-only metadata methods `mode`, `uid`, `nlink`, `ino`), 1 other. Files: `crates/coagent-cli/tests/support/mod.rs` (11), `identity_file.rs` (5), `identity_cli.rs` (5), `cli.rs` (2). The CLI's own code type-checks.

### 3.3 Unix-only code, per crate, and what Windows needs

Class: **D** = a design question; **M** = a mechanical port; **R** = needs the real machine to test. Most items are M to write and R to trust.

**coagent-daemon**

| Where | What it is | What Windows needs | Decided by the design? | Class |
|---|---|---|---|---|
| `src/datadir.rs:76-107` (pure checks), `:113-135` `open`, `:149-165` `read`, `:171-200` `open_temp`, `:227-239` | Folder must be owned by this user, mode exactly 0700; files 0600; created private "from creation" | An access check in Windows terms: owner is this user, and the access list grants nobody else. Or an explicit decision to rely on the user profile's default permissions for now. | Not decided. "the data-directory ACL check on Windows needs its own design (04 §5.3)" (READ BACKLOG.md:240). 04:477 names only a fallback for the device key: "a file under the user profile and a restrictive ACL". A precedent, for the relay key on a Mac only: "Accept it for the beta and say so plainly" (READ 05:56). | **D** (card Q3), then M, then R |
| `src/datadir.rs:72` | `DataDir` holds `uid: u32` | A user identity that fits Windows (a security identifier as text), or none | Follows from the row above | D |
| `src/datadir.rs:206-223`, `:288-292`, `:310` | Atomic write: rename over the target, then open the folder and sync it | Rename over an existing file works differently on Windows, and opening a folder as a file to sync it is expected to fail there. UNVERIFIED (general knowledge of the Windows file API; not read today). | Not addressed | M, R |
| `src/datadir.rs:316-318`; also `crates/coagent-hook/src/main.rs:123`, `crates/coagent-mcp/src/main.rs:471` | The local connection's address is the file `<data dir>/ipc/daemon.sock`, computed in three places | A pipe name. The Windows back end refuses anything not of the form `\\.\pipe\<name>` (READ `crates/coagent-ipc/src/windows.rs:113-127`). So today, on Windows, the hook and the message tools would compile, fail to connect, and block every call. Needs one shared function that turns a data folder into a pipe name. | The design says only "named pipes" and "nothing above it knows which is in use" (READ 04:471-475). How the name is derived is not decided. | **D** (coordinator level), M |
| `src/engine.rs:87-88`, `:304-311` | Socket path limit 103 bytes | A pipe-name length limit instead. The Windows figure is UNVERIFIED. | No | M |
| `src/util.rs:50-57`, `src/engine.rs:296-297` | This process's user id, read from a Unix socket pair | The current user's security identifier. The ipc crate already reads the logon identifier from the process token (READ `windows.rs:140-217`). The daemon forbids `unsafe` (READ `src/lib.rs:18`), so the call must live in the ipc crate or a new small crate. | No | D (where the unsafe code lives), M |
| `src/engine.rs:394-401`, `:418-419` | Stop on SIGTERM and SIGINT | Ctrl-C handling, as the CLI already does: `tokio::signal::ctrl_c()` under `#[cfg(not(unix))]` (READ `crates/coagent-cli/src/relay_cmd.rs:95-99`). Windows has no SIGTERM; a closed window or a kill ends the process without the final save. The store is written atomically, so this is the crash path the recovery rules already cover. REASONED. | No | M, R |
| `src/relay_child.rs:163-172` | `kill_pid` runs `/bin/kill -KILL <pid>` | A Windows way to end a process by id. Only reached when this machine hosts and its guard has died. Not on the guest path. | No | M, R |
| `src/relay_child.rs:67-73`, `:196-197` | Children start with an EMPTY environment and working directory `/` | Whether a Windows program that opens network sockets starts correctly with an empty environment is UNVERIFIED. Host path only. | The rule itself is 04:404 | R |
| `src/main.rs:113` | The helper is found as `coagent` beside `coagentd` | `coagent.exe` | No | M |
| `src/main.rs:145-151` | Gate mode needs `HOME` | The user profile folder | 04:504 names `%USERPROFILE%` for the path rules | M |
| `tests/` | 14 test files and 2 support modules use Unix-only calls, `lsof`, `/bin/kill` or shell (MEASURED by search: `common/mod.rs`, `delta.rs`, `gate/gate_attacks.rs`, `gate/gate_hostile/mod.rs`, `gate/gr2.rs`, `gate/gr3.rs`, `hardening.rs`, `ipc.rs`, `p1p_daemon_down_blocks.rs`, `p1p_m1_unchanged.rs`, `p1p_support/mod.rs`, `p1p_taint_persists.rs`, `recovery_repro.rs`, `restart.rs`, `startup.rs`, `support/ext_relay.rs`) | A Windows test support layer. Several of these are check-owned files that may never be edited, so each needs a ruling. | No | D (rulings on protected files), M, R |

**coagent-ipc**

| Where | What it is | What Windows needs | Decided? | Class |
|---|---|---|---|---|
| `src/lib.rs:36-43` | Back end chosen at compile time | Nothing: both exist | Yes, 04:475 | done |
| `src/windows.rs:1-4`, `:403` | The whole Windows back end: "UNTESTED at run time", tests "NEVER RUN" | To be run on a Windows machine | W3 (04:681) | R |
| `src/windows.rs:18-24`, `:357-361` | No caller check: the access list is the only control; `rejected_count` is always 0; the client does not check the server | The same-user caller check, and a client-side check of the server | Yes: 04:474 "The daemon checks that the connecting process belongs to the same user"; 06:650 "Not built. Waits for spike W3 on the real machine". The API calls are "from memory [UNVERIFIED — spike W3]". | M, R |
| `src/lib.rs:50-51` | `check_peer` is exported on Unix only | A Windows counterpart for the pure comparison | Follows 04:474 | M |
| `tests/gate_ipc.rs:3`, `tests/gate_r2_ipc.rs:3` | Gate tests are macOS-only | Windows gate tests of the pipe (an independent check's job, after the machine exists) | No | later |

**coagent-cli**

| Where | What it is | What Windows needs | Decided? | Class |
|---|---|---|---|---|
| `src/lib.rs:9-10`, `src/relay_cmd.rs:119-125` | `--identity-file` is refused on Windows with a fixed message | Its permission checks written and run on Windows | Yes: 06:504 "refused with a plain message until the permission checks have been written and run there". READ BACKLOG.md:522-526. | D with Q3, M, R |
| `src/identity_stdin.rs:70-76` | Windows variant, "UNTESTED" | A run | No | R |
| `src/relay_cmd.rs:95-99` | Ctrl-C only on Windows | Nothing | n/a | R |
| `tests/` | 4 files Unix-only (26 errors, MEASURED) | Windows variants or a `cfg` line; gate status of each file not read | No | M |

**coagent-policy** (owned by the POLICY-MODE lane; nothing to build here now)

| Where | What it is | What Windows needs | Decided? | Class |
|---|---|---|---|---|
| `src/path/windows.rs`, `src/path/winrules.rs`, `src/path/mod.rs:11` | The Windows path rules. "type-checked for x86_64-pc-windows-msvc only; the spelling rules … are unit-tested as pure functions on macOS" (READ BACKLOG.md:57-60) | A run of its tests on Windows | W4 (04:682) | R |

**coagent-hook, coagent-mcp.** No platform-specific code (MEASURED: the search for `cfg(`, `std::os::` and friends finds only red-control lines). Both type-check plainly for Windows. Their one Windows fault is the connection address above. The hook's dependency test names `coagent-ipc` (READ `crates/coagent-hook/tests/tree.rs:23, 52`), so a shared address function belongs in the ipc crate, not in a new dependency.

**coagent-relay, coagent-proto, coagent-crypto, coagent-roster, coagent-audit.** No platform-specific code found by the same search. "relay crate not cross-checked for Windows" (READ BACKLOG.md:167) is now answered for the Rust code by the stand-in run (exit 0); the C part of `ring` is still unbuilt for Windows on this Mac.

**Outside the crates.**
- `scripts/check.sh` and every runner are bash (READ `scripts/check.sh:1-15`). On Windows they need Git Bash or a rewrite. M.
- The preview's set-up is bash and Python, and its hook template is shell form (section 2.2). M, R.
- `ci/proposed-workflow.yml:16` already names `windows-latest` in its matrix. It is a proposal file; whether any hosted run exists was not read.
- The licence checker step (`cargo deny`) was not run for Windows.

---

## 4. The six spikes W1 to W6

Source for all rows: 04:679-684 (pass rule and fallback) and `spikes/W-native-windows/RESULT.md` (what would be run). The folder `m0_review/` holds one file, `friday_rerun_G1_G2.md`, which is about the macOS runs of G1 and G2 that W1 would port; it contains no Windows statement (READ whole).

"Checking seat" = the small Claude Code session the launcher starts on the Windows machine. Its rules: nothing heavy, install only on the owner's yes, never change firewall, registry, security settings or user accounts, write only in its own folder (READ `Launch_Friday_Windows.cmd:129-143`).

| Spike | Meant to prove | Needs on the machine | Can the checking seat run it? |
|---|---|---|---|
| **W1** (blocking) | With a real `.exe` hook started with no shell and `onFailure: "block"`: a denied Write makes no file; a denied PowerShell command does not run; a killed or missing program blocks the call; in default and bypass modes; with and without Git for Windows. Also whether security software blocks the unsigned program. | Claude Code 2.1.295 or later (DOCS, hooks page: `onFailure` "Requires Claude Code v2.1.295 or later"). A stub `.exe` built elsewhere. The G1 and G2 case lists as PowerShell scripts. Model runs. For the second set-up: Git for Windows installed or removed. | Partly. It can copy files into its folder and run scripted `claude` calls, which is light. It cannot build the stub. Model runs need the owner's allowance. Installing Git for Windows is an install: his yes. The design wanted a clean machine (04:679); his machine is what it is: say so in the result. |
| **W2** | Installer-first order: the hook found on `PATH`; uninstall leaves no blocking hook behind. | A change to the user's `PATH`. | Not under its rules without the owner's yes to that exact change. Not needed before packaging. |
| **W3** | The pipe: a second user cannot open it; a second daemon cannot create it; 1,000 round trips, median under 20 ms; the device key stored in the credential store. | The ipc test program built elsewhere. **Two user accounts.** | Partly. The single-user parts (round trip, second daemon refused, timing) are light and need only a copied test program. The second-user part needs a second account, which the seat may not create: the owner creates it or it waits. The credential-store part needs code that does not exist. |
| **W4** | Every Windows spelling of a path is either made canonical or treated as outside the workspace. | The policy crate's test program built elsewhere. Some classes need short names, junctions or links to exist on disk. | Yes for running a copied test program. Creating junctions and links may need Developer Mode or an administrator (UNVERIFIED): the report's item h covers it. |
| **W5** | The relay can run confined and unable to read the user's profile. | Code that does not exist. | No. Not needed for a guest. |
| **W6** | The embedded terminal with a reliable Stop. | The console, which is not built (READ `preview/REVIEW.md:19-28`). | No. Not now. |

Order that follows: W3's single-user half first (it is the first link's own foundation), then W1, then W4. W2, W5, W6 wait.

---

## 5. Questions that are the owner's (card drafts; nothing is posted)

### Q1. May the first link run on the Windows machine without our gate?

- **Premises.** The gate on Windows depends on experiment W1, never run (READ BACKLOG.md:38-41; 04:679). The existing cross-machine recipe already has an ungated middle tier for a second machine (READ `preview/demo/lan.md:15-17`). Native Windows has no sandbox either way (DOCS: https://code.claude.com/docs/en/sandboxing). Claude Code's own prompts still apply on that side: unverified today as a statement about Windows; it is how Claude Code works in default mode.
- **a. Yes, on my own two machines.** The Windows agent talks to the Mac's agent before our gate exists there. The Mac side stays gated. Claude Code's own prompts stay on.
- **b. Program only, no agent, until the gate works.** The link is shown with typed commands on the Windows side. The agent waits for W1.
- **c. Nothing on Windows until the gate works.** Safest, slowest: no visible result until W1 passes.
- **Recommendation:** a, after b has been seen once.
- **Default that lets work continue:** b.

### Q2. Where are the Windows programs built?

- **Premises.** The Mac cannot build them today: it type-checks only, and one dependency's C code fails for lack of Windows headers (MEASURED, section 3.2). A cross kit exists: cargo-xwin "Cross compile Cargo project to Windows msvc target", "On macOS run `brew install llvm`", and "By using this software you are consented to accept the license at" a Microsoft link (DOCS: https://github.com/rust-cross/cargo-xwin, read through a summarising fetch; the licence text itself was not read). Building on the Windows machine needs a Rust toolchain and Microsoft's build tools; their size and whether they need an administrator are unverified. `ci/proposed-workflow.yml:16` lists a hosted Windows machine; its cost for a private repository is unverified.
- **a. On the Mac.** One install on the Mac, and accepting Microsoft's licence for the files it downloads. The old machine only receives finished programs.
- **b. On the Windows machine.** Installs there, and slow builds on a weak machine.
- **c. On a hosted build machine.** No install anywhere. A spend, and it also gives a place to run the Windows tests.
- **Recommendation:** a now; c is worth its own card when the Windows test suites exist.
- **Default that lets work continue:** none of the three. The two code lanes go on with type-checking only; no `.exe` exists until this is answered.

### Q3. How is the data folder protected on Windows for the first link?

- **Premises.** On the Mac the program refuses a data folder that is not the user's own with mode 0700 (READ `crates/coagent-daemon/src/datadir.rs:76-90, 114-135`). Windows has no such modes; its check "needs its own design" (READ BACKLOG.md:240). The folder holds the device key and unread messages in clear (READ `datadir.rs:5-9`; BACKLOG.md:242-246). A related ruling, for the relay key on a Mac: "Accept it for the beta and say so plainly" (READ 05:56). That a folder inside a Windows user profile is private to that user by default: unverified.
- **a. Accept the profile's own protection for now, and say so.** The program insists the folder is inside your user profile and prints that it checks nothing more. Fastest.
- **b. Build the Windows access check first.** The program reads the folder's owner and access list and refuses anything open to others. Adds a design step and a lane before the first link.
- **Recommendation:** a for the first link on your own machine, b before any Windows build goes to another person.
- **Default that lets work continue:** b (the stricter one). The connection lane does not depend on it.

### Q4. What may be installed or changed on the Windows machine?

- **Premises.** Claude Code installs without an administrator (DOCS: https://code.claude.com/docs/en/setup, "You do not need to run as Administrator"). Git for Windows is optional and changes which tools exist (same page); the design requires both set-ups to be tested (READ 04:466). WSL 2 needs an administrator and a restart (DOCS: https://learn.microsoft.com/en-us/windows/wsl/install). The W3 experiment needs a second user account (READ `spikes/W-native-windows/RESULT.md`, the W3 line). The checking seat may not create accounts (READ `Launch_Friday_Windows.cmd:137-139`).
- **a. Claude Code and our copied programs only.** Enough for the first link.
- **b. Also Git for Windows, when the gate tests start.** Needed to test the second set-up.
- **c. Also a second, empty user account, made by you.** Needed for one test of the local connection.
- **d. Also WSL 2.** Only if the fallback route is ever wanted.
- **Recommendation:** a now; b and c when their tests are ready; not d.
- **Default that lets work continue:** a.

### Q5. May the Mac open a meeting point to the home network for Windows test sessions?

- **Premises.** The cross-machine recipe says this is "the ONLY step that listens beyond loopback" and that it was opened "only for this test" on the owner's sentence of 2026-11-19 (READ `preview/demo/lan.md:4-6`; the sentence itself was not read by me). By default the program listens on this machine only (READ `lan.md:30-31`; `crates/coagent-cli/src/relay_cmd.rs:152-157`). The meeting point sees only scrambled bytes (READ `preview/REVIEW.md:15`).
- **a. Yes, for each Windows test session; stopped when the session ends; times recorded.**
- **b. Ask me each time.**
- **Recommendation:** a.
- **Default that lets work continue:** b.

### Q6. Unsigned test programs on your own machine (a confirmation, not a new decision)

- **Premises.** The ruling: sign through Microsoft's service, later, at the machine (READ 05:38). The design's default until then: unsigned "for internal builds only" (READ 04:788). Windows may warn on, or on some machines block, an unsigned program (READ 04:516; behaviour on this machine unverified).
- **a. Run unsigned test builds on my machine; if Windows blocks one outright, stop and tell me.**
- **b. No program runs there until signing is set up.**
- **Recommendation:** a.
- **Default that lets work continue:** a, as the design's stated default for internal builds.

---

## 6. Lanes

Rule, as in plan 13: each lane owns files no other open lane owns. In flight today: POLICY-MODE owns `crates/coagent-policy`; ROSTER-SETTLE owns the roster crate; RELAY-RECONNECT owns the daemon files `src/engine.rs`, `src/relay_child.rs`, `src/store.rs`, `src/datadir.rs`, parts of `src/main.rs`, `build.rs`, `tests/reconnect.rs`, `docs/DAEMON.md` §1-§7 and `scripts/red-controls-daemon.sh` (READ its brief, section 3) until it merges.

| Order | Lane | Starts |
|---|---|---|
| 1 | **W-IPC** | **Tonight.** No in-flight lane touches its paths. |
| 2 | **W-DAEMON** | After RELAY-RECONNECT merges, and after Q3 is answered or defaulted. |
| 2 (beside it) | **W-KIT** | After Q2 is answered. New files only. |
| 3 | **W-FIRST-LINK** (a run, not a build) | After 1, 2 and the kit; needs Q1, Q5, the machine report and the owner at the machine. |
| 4 | **W-GATE** | After the first link; needs model runs on the machine. |
| 5 | **W-TESTS** | After W-DAEMON; needs rulings on protected test files. |
| later | **W-CLI-ID** | With Q3's option b. |

### W-IPC: the local connection on Windows

- **Outcome.** The connection's Windows side has the same-user caller check the design asks for, the client checks the server, and one shared function turns a data folder into the connection's address on every system. The hook and the message tools call it.
- **Owned.** `crates/coagent-ipc/src/**`; `crates/coagent-ipc/Cargo.toml` (the Windows-only dependency line); new test files under `crates/coagent-ipc/tests/` with the prefix `win_`; `crates/coagent-ipc/README.md`; one line each in `crates/coagent-hook/src/main.rs` (`:123`) and `crates/coagent-mcp/src/main.rs` (`:471`); `BACKLOG.md` (append).
- **NOT in it.** The daemon (its own copy of the address at `datadir.rs:316-318` moves in W-DAEMON). The device key store. Any new dependency. The two gate test files.
- **Tested on the Mac.** The pure functions (the name scheme, the identity comparison) by ordinary tests; the whole crate, tests included, by a plain Windows type-check, which works on this Mac with no stand-in (MEASURED: ipc, hook, mcp `--all-targets`, exit 0 each); `scripts/check.sh` green and unchanged in count except for the new tests.
- **Needs the Windows machine.** Everything the Windows code does at run time. Its tests are written now and marked never run.
- **Collides with.** Nothing in flight. Later: the session-binding lane of plan 13 (L6) owns the hook and message-tool crates; W-IPC's one line in each must have merged before L6 starts.
- **Size.** S to M. About 4 to 8 agent-hours to build, 2 to 3 to check (estimate).

### W-DAEMON: the background program compiles and runs as a guest on Windows

- **Outcome.** `cargo check` for Windows is clean for the daemon, and the guest path (join, send, read, clean stop) is written for Windows.
- **Owned.** `crates/coagent-daemon/src/datadir.rs`, `src/util.rs`, `src/engine.rs` (the start, `:294-313`, and the signal block, `:394-419`, only), `src/main.rs` (`:113`, `:145-151`, `:187` only), `src/relay_child.rs` (`kill_pid` only), new tests with the prefix `win_`, `docs/DAEMON.md` (one new section), `BACKLOG.md`.
- **NOT in it.** The recovery machine, the gate logic, the store format, hosting a relay from Windows (the helper's empty environment stays unproven and is said so).
- **Tested on the Mac.** The whole existing suite, unchanged in result (the Unix code must not move in meaning); the pure Windows rules by unit tests; a Windows type-check. The type-check needs either the kit of Q2 or the stand-in method of section 3.1: Friday rules which.
- **Needs the Windows machine.** Every run-time fact: the atomic write, the folder check, Ctrl-C, the first join.
- **Collides with.** RELAY-RECONNECT on four files. It must not start before that merge.
- **Open before it starts.** Q3; where the unsafe Windows calls live (the daemon forbids unsafe: `src/lib.rs:18`), the coordinator's ruling.
- **Size.** M. About 6 to 10 agent-hours to build, 3 to 4 to check (estimate).

### W-KIT: a way to produce and carry the programs

- **Outcome.** One command on the Mac produces the four `.exe` files and a short text of what to type on the Windows machine.
- **Owned.** New files only: `scripts/windows/**`, `preview/demo/windows.md`.
- **NOT in it.** Signing, an installer, any change to `scripts/check.sh`.
- **Tested on the Mac.** The build itself. **Needs the machine.** That the programs start.
- **Collides with.** Nothing. `preview/**` had a tidy lane in plan 13 (L7): new file names only.
- **Size.** S. 2 to 4 agent-hours (estimate), after the install Q2 allows.

### W-FIRST-LINK: stages C1 and C2 on the real machines

- A run by Friday with the checking seat and the owner, following `preview/demo/lan.md` with the Windows machine as the second machine. No code. Records: Windows version, whether the unsigned program was allowed to start, the four facts of `lan.md:79-80`, the times the Mac's meeting point was open.
- **Size.** 1 to 2 hours per stage, about 30 minutes of the owner each (estimate).

### W-GATE: the gate on Windows

- **Outcome.** W1 run and recorded in both set-ups; the hook wired in exec form for Windows; W4 run.
- **Owned.** New folders under `spikes/`; a Windows hook template under `preview/` (new file); `docs/M0-OUTCOMES.md` (append).
- **NOT in it.** Any change to the policy crate (a W4 failure is a finding for the policy lane).
- **Tested on the Mac.** Almost nothing. **Needs the machine.** All of it, with model runs.
- **Collides with.** POLICY-MODE only if W4 finds a fault.
- **Size.** L. 15 to 30 agent-hours across several sessions (estimate); W1 can stop the plan (04:679).

### W-TESTS and W-CLI-ID

- **W-TESTS.** A Windows support layer for the daemon's and CLI's process tests (section 3.3 lists the files). Several are protected check files: each needs a ruling. Running them needs Q2's option c or a stronger machine. Size L, not estimated further.
- **W-CLI-ID.** `--identity-file` on Windows (06:504). Waits for the access check of Q3 option b.

---

## 7. Not read, not measured

- **The machine.** No report. Everything about it is unknown.
- **Linux.** Not compiled, not type-checked (no target installed), not run. Every Linux statement here is READ from the backlog or REASONED.
- **The `-gnu` Windows target.** Not installed, not run.
- **Windows linking and running.** Nothing was linked. No `.exe` exists. No Windows behaviour was observed.
- **The stand-in runs** prove Rust type-checking only (section 3.1). The C code of `ring` was not really built for Windows.
- **The daemon's program file and its tests** were not type-checked for Windows (the library fails first).
- **Design files.** Read in the parts named by the commission and by search for Windows terms: 00 whole; 05 whole; 04 §5 whole and the Windows rows of §7 to §10; 06 §4, §7 and its Windows lines; 12 §1; 13 §2. 03 only by its Windows lines. 07, 09, 10, 11, 14 only by search hits. The two PDF files not opened.
- **BACKLOG.md** read whole (754 lines).
- **Code.** Read whole: `datadir.rs`, `relay_child.rs`, the daemon's `main.rs`, the ipc crate's `lib.rs` and `windows.rs`, the CLI's `lib.rs`, `relay_cmd.rs`, `identity_stdin.rs`. Read in part: `engine.rs:280-430`, `util.rs:40-77`, `identity_file.rs:1-70`, the hook's `main.rs:60-150`, the message tool's `main.rs:440-490`. `unix.rs` of the ipc crate only by its public items. The policy crate's Windows files not read. The preview scripts not read line by line.
- **In-flight branches.** Not read. What I say about RELAY-RECONNECT's paths is from its brief.
- **Claude Code documentation.** Read today: the setup page, the sandboxing page (first 100,000 characters of 111,062), the hooks page (first 100,000 of 294,676). The fetch tool summarises; quotations are as it returned them. Not read: the tools reference, the plugin reference, the PowerShell tool page, anything on MCP servers on Windows. The hooks page's statement on the minimum version is the only version fact relied on.
- **Microsoft documentation.** Read: WSL install and WSL networking. Not read: named pipe functions, access lists, file rename and sync behaviour, SmartScreen, signing. Every Windows API statement in this plan is UNVERIFIED unless it quotes design 04.
- **cargo-xwin.** Its front page through a summarising fetch. Not tried.
- **Sizes.** Estimates by comparison, not measurements.
