This brief is from Friday (the owner's laptop coordinator seat). Client: General. Project: CoAgent. Questions go in your STATUS file ("the coordinator" below is Friday); you have no mailbox. You are a NEW seat, WIN-IPC, with no memory of earlier seats. You work on a NEW branch `win-ipc` in a NEW worktree `worktrees/win-ipc` beside the repository, cut from `origin/main` at `2bba2a468a5cce04f5d7189bdf76cbbecfbfab14`. Your report is a NEW file `coagent/5_Project_History/STATUS_WIN_IPC.md`. Its last line is always exactly one of: `IN PROGRESS: <what>` (with `WAITING FOR A HEAVY SLOT` inside it only while you are blocked for one), `STOP Q<n> (coordinator): <question>`, `READY FOR QA WIN-IPC`.

# WIN-IPC: the local connection on Windows gets its caller check, and one function names the connection for a data folder on every system

Every line number below was read by the drafter at `2bba2a4` in a clean clone. A bare `[:n]` is a line of `crates/coagent-ipc/src/windows.rs`; other files are named. "04", "05", "06" are the design files of section 0 item 1. If a line does not say what this brief says it does, quote it and STOP.

Words: the DAEMON is `coagentd`. Its CLIENTS are the hook program (`coagent-hook`) and the message tools (`coagent-mcp`). The CONNECTION is the local channel between them: a Unix socket in the data folder on macOS and Linux, a named pipe on Windows. "The machine" is the owner's Windows machine, which no seat has used yet.

**The honest limit of this build, stated first.** No Windows machine is available to you. Your Windows code is type-checked and never run. Every Windows test you write is compiled, not executed, and is labelled so, exactly as the crate already does [:403]. What you CAN prove on this machine: the pure functions, by ordinary tests; and that nothing changed for a non-Windows build.

## 0. Start (changes no rule)
1. **Read WHOLE, in order:** the project's `CLAUDE.md`; this file; design 04 (`/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/04_design-revision-rulings.md`, READ-ONLY) §5.3 (lines 468-477) and the W3 row (line 681) and rows W-c, W-d (lines 760-761); design 06 (`06_design-addendum-rulings-2026-11-17.md`, same folder, READ-ONLY) lines 585 and 650; the plan this lane comes from (`15_windows-plan-2026-11-20.md`, same folder, READ-ONLY) sections 3 and 6; `crates/coagent-ipc/README.md`; `crates/coagent-ipc/src/lib.rs`, `windows.rs`, `unix.rs`, `error.rs`, `stream.rs` whole; `crates/coagent-hook/src/main.rs` and `crates/coagent-mcp/src/main.rs` whole (you change one line in each); `crates/coagent-daemon/src/datadir.rs` lines 315-318 (read only).
2. **Worktree, from the remote only.** `git fetch origin`; `git ls-remote origin main` and `git rev-parse origin/main` must both print the SHA above, or a later SHA whose `git diff --stat 2bba2a4 <sha> -- crates/coagent-ipc crates/coagent-hook crates/coagent-mcp` is empty. Otherwise record what you see and STOP. STOP also if the branch or the worktree folder exists.
3. **Protected files: sha256 at the start, each value recorded.** Values read by the drafter at `2bba2a4` (`git show <sha>:<path> | shasum -a 256`):
   - `crates/coagent-ipc/tests/gate_ipc.rs` 15162be89db6d087452df94c129a5c6e43f77e2de69805385689fb35dfb7e76e
   - `crates/coagent-ipc/tests/gate_r2_ipc.rs` 28b8dc91b1c28508be03b2fb90b40bb560f728a893854dbbf9408a88d55c9ac9
   - `crates/coagent-hook/tests/tree.rs` b94cdba9a53279e61936f445821922a3c8900828a461bf0a00cf9c08433e7e80 (it asserts the hook's dependency list, lines 23 and 52: this is why the new function lives in `coagent-ipc` and no dependency is added)
   - `crates/coagent-mcp/tests/stdout_audit.rs` 1cc61041e469ce717b0c0bab191a6e1ad4d65c2bf175ddc7f70017e40b83714a
   - Files of OTHER lanes that spell the socket's file name `daemon.sock` and must stay green and unedited: `crates/coagent-daemon/tests/common/mod.rs` 08ed3f585cf09a22bc0e1cc93a7e0b953cb43c37ee7107a66db6336282d0e5c9; `tests/ipc.rs` 7ae8babc5d652f6881f891d6f93b21c65b8fd75db9f41b5887c699cdd4f58bf8; `tests/startup.rs` 67632552f2d0f1fc0bf703cfebce6f64c73e32ef3b5147ecf3125b5dbc1ff40c; `tests/p1p_support/mod.rs` 7ff299ef6c718d77b37507d60a2c9f92066f20a2889039f088d7a3e76f587502; `tests/p1p_daemon_down_blocks.rs` 7e4eb4db37557e2ef92621dfb49dc502e8c0e151a9cc4576770a3130ed65e7be. Also, never edited by you: `preview/demo/setup.sh` 09e6628b48e5cac7771071115ba3e948c3faa01219b97a61c6192d61bd2fdd04; `preview/replay/run.sh` c6f283cc7216b69820efc23b446e83438260e7cdc919818958878422ab1fd9a2; `preview/lib/pvpaths.py` 12d04d1494ce013b5abe64eefee59deb1c0e3f6697eff0df355be8eb00773d8a.
   - Start values of the files you WILL change, so the check can see exactly what moved: `crates/coagent-ipc/src/windows.rs` cdeb4551b5b81dc8c16a0d32b2ab165cb51b7cc8e735859ae86795cd32514c8b; `src/lib.rs` e5b7017972d8757e14ba3aad0bbdd177342272038ed333bf398795a72e1d11d9; `src/unix.rs` 4307c723b481bb1c5492acc39bbcd0dffc19ea76c8dc816889a3a7e6ff31ee5d; `src/error.rs` 10390e247c24bb90fa241de57ef2a37576d7b47eae63a3441f5be00b676628e5; `crates/coagent-ipc/Cargo.toml` ba3aa9e82b2b6feb224f09f18841ef629dda9136bc62f4ff31f1078141ead88f; `crates/coagent-hook/src/main.rs` 918c8a6284316171b7eaa7dc5849723ae4276cc00671830c2cb74d82f34573b2; `crates/coagent-mcp/src/main.rs` c6ad78e288594a322c2dbed31c4abbb20eaa892a113ffc5ad69b9ec664953d87.
   Any difference in a protected file: quote it and STOP. A protected file that changes colour because of your change: record its failure text and STOP (never edit it).
4. **Start runs, tails recorded,** each to its final line with the exit code captured in the same command, one at a time (section 6):
   - `scripts/check.sh` is NOT run as a start run: the coordinator already holds it. Baseline at `2bba2a4`, Friday's own clean-clone run of 2026-11-20: exit 0, "CHECK OK", 1,253 passed, 0 failed, 21 ignored, summed over 167 `test result:` lines. Your FINAL run (section 5) is compared with these figures. If your base is a later main than `2bba2a4`, say so and ask in STATUS for the baseline of that head; do not spend a heavy run on it.
   - The Windows type-check, which is this lane's second gate: `cargo check --locked --target x86_64-pc-windows-msvc -p coagent-ipc --all-targets`, then the same with `-p coagent-hook`, then `-p coagent-mcp`. Expected, MEASURED by the drafter at `2bba2a4` on this machine with the project toolchain 1.100.0: exit 0 and 0 errors for each of the three. These three crates do not depend on `ring`, so they need no C compiler for Windows. Do NOT run this for any other crate: it fails in a dependency's build script for a reason that is not yours (plan 15, section 3.2).

## 1. The authority
- **The owner's words of 2026-11-20** (verbatim except the two bracketed places, where a seat's name and another project's name are left out on purpose): "lets prioritise the work on windows.  it would be great to have this running as [another seat] is working on [another project] that will need windows". And: "ideally, it would also be a good test of Claude to Claude for you to communicate with that machine".
- **The owner's rulings of 2026-11-17, verbatim options** (`05_kam-rulings-2026-11-17.md`, same READ-ONLY folder): line 29, card `windows-testing-1117`: a: "I will provide a Windows machine or VM". Line 42, card `n8-first-version`: a: "One beta with everything" (the recorded consequence: the beta carries native Windows).
- **Design 04 §5.3, the text this lane builds (quoted).**
  - [04:471] "IPC: named pipes, not Unix sockets."
  - [04:472] "The daemon therefore always creates its pipe with an explicit security descriptor granting access only to the user's logon session". ALREADY BUILT [:249-251, :262-285].
  - [04:473] "The first pipe instance is created with the first-instance flag; if creation fails because the name already exists, something else owns the name and the daemon refuses to start and says so". ALREADY BUILT [:335-344].
  - [04:474] "**Caller check.** The daemon checks that the connecting process belongs to the same user before accepting a hook or MCP request, the Windows counterpart of the same-uid check. The specific API calls are from memory [UNVERIFIED — spike W3]." NOT BUILT [:18-24, :357-361]; `BACKLOG.md:162-166`.
  - [04:475] "One `IpcListener`/`IpcStream` abstraction with a Unix-socket implementation and a named-pipe implementation; nothing above it knows which is in use." HALF TRUE TODAY: the two clients and the daemon each build the address `<data dir>/ipc/daemon.sock` themselves (`crates/coagent-hook/src/main.rs:123`, `crates/coagent-mcp/src/main.rs:471`, `crates/coagent-daemon/src/datadir.rs:316-318`), and the Windows back end refuses any address that is not `\\.\pipe\<name>` [:113-127]. So on Windows both clients would compile, fail to connect, and block every call.
  - [04:681] the W3 pass rule: "A process running as a second user cannot open the pipe; a second daemon cannot create it; hook round-trip under 20 ms median (measured); key stored and read back."
  - [06:650] "Named-pipe caller and server identity checks | Not built. Waits for spike W3 on the real machine". This lane writes the code and the tests; the run on the real machine is a later step that is not yours.
- Method: ONE build (you), then ONE independent check. You do not merge. No deploy, no publish, no spend. The repository stays private.

## 2. The coordinator's rulings (each CONFIRMED by Friday on 2026-11-20 after reading the draft and the plan whole)

For each item: **Non-Windows effect** says exactly what changes for a build that is not Windows. **Protected names** lists any protected test file that mentions a name the item touches.

- **P-1 (CONFIRMED). One public function names the connection for a data folder.** Add `pub fn endpoint_for_data_dir(data_dir: &Path) -> io::Result<PathBuf>` to `coagent-ipc`, exported from `src/lib.rs` on every system.
  - On Unix it returns exactly `data_dir.join("ipc").join("daemon.sock")`, never an error: the same value the three call sites build today.
  - On Windows it returns `\\.\pipe\` followed by the name of P-2.
  - **Non-Windows effect:** one new public function whose result is byte-identical to today's three hand-built paths. No behaviour changes.
  - **Protected names:** it reproduces the spelling `daemon.sock`, which these protected or foreign files also spell: `crates/coagent-daemon/tests/common/mod.rs`, `tests/ipc.rs`, `tests/startup.rs`, `tests/p1p_support/mod.rs`, `tests/p1p_daemon_down_blocks.rs`, `preview/demo/setup.sh`, `preview/replay/run.sh`, `preview/lib/pvpaths.py`, and the texts `docs/DAEMON.md`, `preview/demo/lan.md`, `preview/demo/one-mac.md`. None is edited; all must stay green.

- **P-2 (CONFIRMED). The pipe name is a pure function of the data folder's path, compiled and tested on every system.** `pub fn pipe_name_for(absolute_path: &str) -> Result<String, IpcError>`, with no `cfg` on it, so its tests run here.
  - Input: an absolute path as text. The Windows caller makes it absolute with `std::path::absolute` (no file is opened, no link is followed) before calling.
  - Rule: fold ASCII letters to lower case; turn every `/` into `\`; drop one trailing `\`; then encode: ASCII letters, digits, `.`, `_` and `-` stay; every other byte of the UTF-8 form becomes `~` and two lower-case hex digits. The name is `coagent-` plus the encoded text.
  - Refuse (a new `IpcError` variant, kind `InvalidInput`) an empty input, an input that is not absolute by the Windows spelling rules you can state without a system call, and a name longer than a constant `MAX_PIPE_NAME`. PROPOSED value 200, NOT VERIFIED against Microsoft's limit (the drafter did not read it): mark the constant PROPOSED in its doc comment.
  - Why no hash: the crate has no hash dependency and none may be added (P-6).
  - Known limit to write in the README, not to fix: two spellings of one folder that differ by more than case and slash direction (a short name, a link, a mapped drive) give two names, so a client given the other spelling does not find the daemon and its call is blocked. That fails closed.
  - **Non-Windows effect:** one new public pure function and one new error variant, used by nothing on a non-Windows build except tests. `IpcError` is an enum other crates may match on: check with `git grep -n "IpcError::" -- crates` that no crate outside `coagent-ipc` matches it exhaustively; if one does, STOP. (The drafter's case-insensitive search at `2bba2a4` found `IpcError` in no `.rs` file outside `crates/coagent-ipc/src/`, with 16 matching lines in `error.rs` as the positive control.)
  - **Protected names:** none found by the drafter's search for `IpcError` in the protected files of section 0 item 3 (the two ipc gate files mention `coagent_ipc` and `IpcListener` only). Re-check and record.

- **P-3 (CONFIRMED). The two clients call P-1.** `crates/coagent-hook/src/main.rs:123` and `crates/coagent-mcp/src/main.rs:471` each read `let sock = dir.join("ipc").join("daemon.sock");`. Replace each with a call to `coagent_ipc::endpoint_for_data_dir(&dir)`. On an error the hook returns `Outcome::Blocked` (as it does for every other start-up failure, `main.rs:74-79, :116-122`) and the message tool prints its usage-style error and exits 2 (as `main.rs:466-469`). Nothing else in either file changes.
  - **Non-Windows effect:** none. The function cannot fail on Unix and returns the same path.
  - **Protected names:** `crates/coagent-hook/tests/tree.rs` asserts the hook's dependency tree (it names `coagent-ipc` at lines 23 and 52); this item adds no dependency, so it must stay green. `crates/coagent-mcp/tests/stdout_audit.rs` (its first 40 lines read by Friday at `2bba2a4`) audits the source text of `coagent-mcp`: no `print!` or `println!` anywhere, and `stdout()` exactly once, inside `fn writer`. Your error arm may use `eprintln!` only. Read the file whole before you edit `coagent-mcp`, and STOP if it pins anything else you would touch.
  - NOT in this item: the daemon's own copy (`crates/coagent-daemon/src/datadir.rs:316-318`) and `coagentd ctl` (`src/main.rs:187`). Another open lane owns those files. A later lane moves them.

- **P-4 (CONFIRMED). The same-user caller check on the Windows listener** [04:474].
  - A pure decision, compiled on every system so it is tested here: `pub fn check_peer_sid(peer: &str, expected: &str) -> Result<(), IpcError>`: `Ok` only when both are non-empty and equal as text after ASCII upper-casing. Refusal is a new `IpcError` variant that carries NO identifier text (an identifier names an account).
  - In `accept` [:371-376], after `connect().await` and before the connected instance is handed out: read the client's process id from the pipe, open that process for limited query only, read its token's user identifier as text, compare with this process's own token user identifier (read once at `bind_with` [:331-350] and kept). On any failure of any step, or a mismatch: do not hand the connection out, disconnect that instance, add one to a real counter, and keep accepting. `rejected_count` [:357-361] returns that counter.
  - The order "create the next instance BEFORE handing the connected one out" [:363-376] stays.
  - The calls, by the names found in the vendored bindings (`windows-sys-0.61.2` in the cargo registry; the drafter confirmed these symbols exist there, and did NOT read Microsoft's pages for their behaviour): `GetNamedPipeClientProcessId` (module `Win32::System::Pipes`), `OpenProcess` and `OpenProcessToken` (`Win32::System::Threading`), `GetTokenInformation` with `TokenUser`, `ConvertSidToStringSidW` (already used at [:200]). Take every signature from that vendored source, never from memory. This needs the feature `Win32_System_Pipes` added to the Windows-only dependency line (`crates/coagent-ipc/Cargo.toml:17-18`).
  - Every `unsafe` block carries a `// SAFETY:` comment, and all `unsafe` stays in `src/windows.rs` [:26-28].
  - A stated limit to write down, not to solve: a process id can be reused between the client's connect and your lookup. Say so in the module notes.
  - **Non-Windows effect:** one new public pure function and one new error variant. The Windows-only dependency line gains a feature; it is inside `[target.'cfg(windows)'.dependencies]`, so a non-Windows build compiles nothing new. Run `cargo metadata --locked` (or the start check) to show `Cargo.lock` is unchanged; if it changes, STOP.
  - **Protected names:** `rejected_count` and `PeerPolicy` appear in no protected file (drafter's search). `IpcListener` appears in `crates/coagent-ipc/tests/gate_ipc.rs` and `gate_r2_ipc.rs`; both are compiled only on macOS (line 3 of each) and use the Unix listener, which this item does not touch.

- **P-5 (CONFIRMED). The client checks the server.** In Windows `connect` [:384-399], after the pipe opens: read the server's process id (`GetNamedPipeServerProcessId`), read its token user identifier the same way, and refuse (the P-4 variant, kind `PermissionDenied`) unless it equals this process's own. This closes the gap the module itself names [:22-24]: "the client does not verify that the server end belongs to the same user".
  - **Non-Windows effect:** none.
  - **Protected names:** none.

- **P-6 (CONFIRMED, and tightened by Friday). No new dependency, and `crates/coagent-ipc/src/unix.rs` is NOT EDITED AT ALL.** P-1's Unix half lives in `src/lib.rs` (or a new module of yours), not in `unix.rs`. Reason, read by Friday at `2bba2a4`: another crate's red-control runner, `crates/coagent-relay/red-controls/run.py` (lines 134 and 174), mutates this crate's Unix source by exact text match on `IpcError::PathIsSymlink` and `IpcError::AddrInUse` blocks. For the same reason the two existing `IpcError` variants `PathIsSymlink` and `AddrInUse`, and the doc comment line `/// A listening local-IPC endpoint.`, keep their exact text wherever they stand today. If you cannot do P-1 without a line in `unix.rs`: STOP. Root `Cargo.toml` and `Cargo.lock` are not touched.
  - **Non-Windows effect:** none, by construction.
  - **Protected names:** `check_peer` and `PeerPolicy`: no protected file mentions them (drafter's search over `crates/*/tests`, `scripts`, `preview`, `docs`).

- **Closed list.** Each item names the places it permits. An edit beyond them is a STOP question, never a judgement call.

## 3. Files
**Owned:** `crates/coagent-ipc/src/**` EXCEPT `src/unix.rs` and anything under `src/unix/` (P-6); `crates/coagent-ipc/Cargo.toml` (the `windows-sys` feature list only, and `[features]` for red controls if you need them); new test files `crates/coagent-ipc/tests/win_name.rs` (runs everywhere), `crates/coagent-ipc/tests/win_pipe.rs` (first line `#![cfg(windows)]`); `crates/coagent-ipc/README.md`; `crates/coagent-hook/src/main.rs` (P-3's one statement and its error arm only); `crates/coagent-mcp/src/main.rs` (P-3's one statement and its error arm only); `BACKLOG.md` (append, and closing in the file's own form).
**Forbidden:** every other crate, the daemon above all; root `Cargo.toml`; `Cargo.lock`; any new dependency; the protected files of section 0 item 3; `scripts/**`; `preview/**`; `docs/**`; `main`.
**Named collisions:** (1) the daemon files `datadir.rs`, `engine.rs`, `main.rs` belong to another open lane tonight: you read them, never edit them. (2) A later lane (session binding) will own the hook and message-tool crates: your one statement in each must be merged before it starts. If you find you need a file outside the owned list: STOP.

## 4. The work, in order (tests first; each item green before the next; record each step's totals)
1. **Tests first.** Write `tests/win_name.rs` against P-1, P-2 and the pure half of P-4. It does not compile yet; commit it. Cases, at least:
   - Unix shape of P-1: for 1,000 generated folder paths, the result equals `join("ipc").join("daemon.sock")` (on Unix builds).
   - P-2 examples written out by hand in the test (a drive path, a path with a space, one with a non-ASCII letter, one with `~`, forward slashes, mixed case, a trailing separator), each with its exact expected name.
   - P-2 properties, fixed seed printed on failure, at least 50,000 generated inputs: the output holds only `[a-z0-9._~-]`; two inputs that differ only by ASCII case or by slash direction give one name; two inputs that differ in any other way give two names (decode the name back and compare); a name over the limit is refused, one at the limit is accepted.
   - P-4 pure half: equal, different, empty on either side, case-different.
2. **P-2, then P-1** (Unix half and the Windows half's call into P-2). `win_name.rs` green.
3. **P-3.** The whole workspace suite green with no test edited; the three Windows type-checks of section 0 item 4 exit 0.
4. **Windows tests, written and compiled, never run:** `tests/win_pipe.rs` and the module tests [:401-442]. Each carries the line `NEVER RUN (no Windows machine)` in its doc comment. At least: a round trip through `endpoint_for_data_dir`; a second bind on one name is refused; a same-user client is admitted and `rejected_count` stays 0; 1,000 round trips with the median printed (the W3 figure [04:681]; no assertion on time); the client refuses a pipe served by a different identity (written with the expected identity passed in, since no second account exists here); one `#[ignore]` test whose doc comment says exactly what the owner must set up for the second-account case of [04:681] and what it then asserts.
5. **P-4, then P-5.** The three Windows type-checks exit 0 with `-D warnings` (use `cargo clippy --locked --target x86_64-pc-windows-msvc -p coagent-ipc --all-targets -- -D warnings`; if clippy cannot run for that target here, record the exact message and STOP).
6. **Red controls for what runs here.** The crate has no runner today (the drafter found none under `crates/coagent-ipc/`). Add two, each a `cfg` switch refused in a release build, each red on its OWN assertion text, run by a small script of your own inside the crate (`crates/coagent-ipc/red-controls.sh`, owned): `red_name_keeps_case` (P-2 does not fold case: the "case gives one name" property fails) and `red_name_drops_escape` (a non-allowed byte is dropped, not encoded: the "different inputs give different names" property fails). Then the clean run green. A red control for the Windows run-time checks cannot be shown red here: say so in STATUS as NOT DONE, with the control you would add.
7. **README and module notes:** what is enforced on Windows after this build; what is still never run; the name rule and its known limit; the process-id reuse limit; the exact list of what a first run on the machine must do (this replaces the list at `README.md:44` onwards, kept and extended, never shortened).
8. **BACKLOG:** update `BACKLOG.md:162-166` in the file's own form (the caller check is now WRITTEN, still never run: it stays open, with what remains); append an entry for each limit above and one for the daemon's own copy of the address still to be moved.

## 5. Final tree (all before READY)
1. Merge, never rebase: `git fetch origin`; if `origin/main` moved, `git merge origin/main`; a conflict outside your owned paths (other than `BACKLOG.md`, where both sides are kept): STOP. Re-run everything below on the merged tree.
2. `scripts/check.sh` exit 0, totals recorded (start against end; the only new tests are yours).
3. The three Windows type-checks and the clippy line of step 5, each exit 0, tails recorded.
4. Your red-control script to its final line, exit code captured in the same command: both rows red on their own text, the clean run green.
5. Every protected file byte-identical to section 0 item 3 (sha256 listed again). `Cargo.lock` byte-identical to the start.
6. `git diff --stat origin/main...HEAD`: every path within section 3's owned paths. For `coagent-hook` and `coagent-mcp`, paste the whole diff: it must be P-3 and nothing else.
7. Proof that the Unix back end did not move: `git diff --stat origin/main...HEAD -- crates/coagent-ipc/src/unix.rs crates/coagent-ipc/src/unix` prints nothing (with a positive control: the same command without the path filter lists your files); and `git grep -c "IpcError::PathIsSymlink\|IpcError::AddrInUse" -- crates/coagent-ipc/src` printed at the start and at the end, equal.
8. A case-insensitive scan of every ADDED line for any person, account, machine, drive or client name and any home or volume path: zero hits, with a positive control (a planted string in a scratch file that the same scan finds).
9. Push the branch; record `git ls-remote origin win-ipc`; `git merge-base --is-ancestor origin/main HEAD` exit 0; read `git ls-remote origin main` again just before the last line (if it moved, back to item 1).
10. While a STOP is open the last line is that question, not READY.

## 6. Standing rules
- Heavy runs: THREE at once machine-wide, by the rules other seats already follow: read `2026-11-20_coagent_HEAVY-SLOT_PRIORITY_v2.md` and `2026-11-20_coagent_HEAVY-SLOT_PRIORITY_v2_AMENDMENT-1_three_slots.md` in Friday's briefs_drafts WHOLE. Your place in the order is LAST: RELAY-RECONNECT (and its check, QA-RELAY-RECONNECT), POLICY-MODE, ROSTER-SETTLE, then you. `scripts/check.sh` and any single cargo run you expect to pass five minutes count as heavy; the three Windows type-checks of section 0 are light. Before each heavy run, count REAL JOBS with exactly: `ps -ax -o command= | grep -c -E '^(/bin/)?bash (scripts/(check\.sh|red-controls-[a-z-]+\.sh|test-daemon\.sh|test-p1p\.sh)|crates/coagent-policy/red-controls\.sh)'`. At 3 or more, wait and re-count every 2 minutes; and do not start while the last line of any of `STATUS_RELAY_RECONNECT.md`, `STATUS_POLICY_MODE.md`, `STATUS_ROSTER_SETTLE.md` contains `WAITING FOR A HEAVY SLOT`. While YOU are blocked, your own last line carries that marker. No chaining: each next run is a new start with a new count. Start your own scripts as `bash scripts/check.sh` from the worktree root so the count sees them. While a run is going, keep the last line `IN PROGRESS: <what>` and refresh it at least every 20 minutes. A test failure in a run that overlapped two other heavy jobs is re-run alone before it is believed; record both.
- Install nothing. No `rustup target add`, no new tool. The Windows target you need is already in the project toolchain (MEASURED by the drafter).
- Never delete: quarantine with a header. Never weaken, ignore or delete a test; a builder test made meaningless gets its old line quoted in STATUS and a replacement.
- Never call a Windows behaviour proven. Every Windows statement in code comments, README and STATUS is one of: WRITTEN AND TYPE-CHECKED, or NEVER RUN. An API fact comes from the vendored bindings' source with its file and line, or is marked UNVERIFIED.
- Fixtures are generated inside the test or in scratch. No person's, machine's or drive's name and no real path in code, tests, docs, commits or STATUS output.
- After ANY context compaction, re-read this brief and your STATUS file WHOLE before writing anything more.
- No model runs. Network: only `git fetch`, your branch's push, and crates already in `Cargo.lock`.
- A red control is red on its NAMED property, not a side effect; no assertion on truncated text; no test depends on map order; "equivalent mutant" is a written claim.
- The owner is not asked: questions go in STATUS for the coordinator; approval-class items are a STOP. When everything is green, write READY and wait.

## 7. NOT in this build
- Any run on Windows, any `.exe`, any cross-compile kit, anything installed.
- The daemon: its data-folder checks, its user identity, its signals, its copy of the address, `coagentd ctl`.
- The device key in the Windows credential store (the last clause of [04:681]).
- The second-user test as an executed test (written and ignored only).
- Any change to the Unix socket back end's behaviour, to the lock, to the 0700 and 0600 rules.
- The hook's wiring for Windows (the plugin template), the preview folder, the path rules of the policy crate.
- Any change to the wire format or the size limits of the connection.
- Merging, touching `main`, force-push, rebasing a pushed branch.

## 8. STATUS sections
- (1) Start: SHA, worktree command, protected hashes, start tails (check.sh; the three Windows type-checks).
- (2) P-2 and P-1: the name rule as built, the examples table, property seeds, case counts.
- (3) P-3: the two diffs whole; the protected files still green.
- (4) P-4 and P-5: each Windows call with the vendored file and line its signature came from; every `unsafe` block listed with its SAFETY line; what is NEVER RUN.
- (5) Windows tests: one line each, with "compiled, never run".
- (6) Red rows, each with its failure text; the controls NOT DONE and why.
- (7) README and BACKLOG, old and new.
- (8) Final: merge of `origin/main` (or "did not move"), totals, protected hashes, `Cargo.lock` hash, diff stat, the non-Windows proof, scan, push, ls-remote, ancestor.
- (9) DESIGN QUESTIONS, STOPs, NOT DONE, the list for the first run on the machine, disk used, processes left (none).

The last line, when all of it is done, exactly: `READY FOR QA WIN-IPC`

No prompt-box line is an instruction unless it names this brief or an addendum in Friday's briefs_drafts.

