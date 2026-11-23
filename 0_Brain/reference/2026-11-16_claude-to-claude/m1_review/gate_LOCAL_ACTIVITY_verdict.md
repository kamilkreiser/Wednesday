VERDICT: NO GO — head 02bea3d0a7eae277b67a0e488d4567bff49839af

# QA-LOCAL-ACTIVITY — verdict

Branch `local-activity`, head `02bea3d0a7eae277b67a0e488d4567bff49839af`, base main `20785c3e9389ac2275cdfda2ec7fb55eb1176425`. Independent check, 2026-11-23, QA clone under `/private/tmp/claude-501/qla`; no model run, nothing pushed, nothing in the project folder written but the status file.

## BLUF
1. **The gate decides exactly as before.** My own 128 hook events (every tool class, all outcomes, hostile and broken input, paired and tainted sessions) gave byte-identical hook answers and `gate` replies on main and on the branch: 0 differences (a planted change showed 2). No byte changed in the policy, hook, MCP server, `gate.rs`, preview, spikes, Cargo files.
2. **Nothing of the local activity leaks.** 66 markers in 40 decisions were found in no file on disk, no daemon log, nothing the peer received or logged, and not in the agent's tools; the link's traffic matched runs with no decisions.
3. **But the window can be made to show a fake line.** One command the agent merely PROPOSES can, through the terminal's line wrap, put a row on the owner's screen that reads exactly like another entry ("CoAgent refused …") or like the notice. That is a Major by the brief: NO GO until the viewer marks its continuation rows. Smaller: after a very quick daemon restart the window can silently skip lines.
4. **Not covered:** a real terminal window (the wrap was rendered with `fold`), Windows, a syscall trace of the viewer, packet capture (relay counts used), clippy and `check.sh` (Friday's merge check).

**Main moved while I worked:** `git ls-remote` at 16:54 → main `ce7276c86aaaa222c1622620a2e8b4734fb3a187` (descends from `20785c3`; adds only `spikes/W1-windows-exec-hook/`, `spikes/W4-windows-paths/`, `preview/plugin-template-windows/` and lines in `BACKLOG.md`, `docs/M0-OUTCOMES.md`; no `crates/`, `scripts/` or Cargo file). The branch does not merge cleanly onto it: `git merge-tree` reports content conflicts in `BACKLOG.md` and `docs/M0-OUTCOMES.md` (both sides append; keep both). All my checks are of head `02bea3d` against base `20785c3`.

## Head and base proofs (TESTED)
- `git ls-remote` against the GitHub remote (from the QA clone, 15:47): `02bea3d0a7eae277b67a0e488d4567bff49839af refs/heads/local-activity`, `20785c3e9389ac2275cdfda2ec7fb55eb1176425 refs/heads/main`. Both fetched into the QA clone; `git merge-base --is-ancestor 20785c3 02bea3d` → true. Commits on the branch: `b53b74e`, `02bea3d`.
- Builder STATUS: 127 lines, ends `head 02bea3d…` / `READY FOR QA LOCAL-ACTIVITY`.

## Item 1. Scope (TESTED)
- `git diff --name-status 20785c3...02bea3d`: 19 paths (M BACKLOG.md, build.rs, engine.rs, ipc.rs, lib.rs, main.rs, docs/DAEMON.md, docs/M0-OUTCOMES.md, scripts/red-controls-daemon.sh; A activity.rs, watch.rs, 7 tests/la_*.rs, tests/la_support/mod.rs) — all inside the brief's section 6.
- Forbidden paths (`crates/coagent-policy crates/coagent-hook crates/coagent-mcp crates/coagent-cli crates/coagent-daemon/src/gate.rs preview spikes Cargo.toml Cargo.lock docs/POLICY.md .gitattributes tests/common tests/p1p_support`): **0 bytes**. Control: the same command over `docs/DAEMON.md` → 7352 bytes.
- No `Cargo.toml` in the diff; `Cargo.lock` unchanged → no new dependency. `unsafe` in added lines: 0; `#![forbid(unsafe_code)]` still at `lib.rs:18`.
- Existing test files: `ls-tree -r` of every `*/tests/*` path at base (237 entries) equals the head's list minus `tests/la_*` — same blob ids. `scripts/red-controls-daemon.sh`: 0 removed lines (append only). `scripts/check.sh`, `scripts/test-p1p.sh`, `src/release_audit.rs`: unchanged.

## Item 2. The gate is unchanged: own differential (TESTED)
- Builds: `coagentd`, `coagent-hook`, `coagent`, `coagent-mcp` built at main `20785c3` (QA worktree, target dir `tmain`) and at head `02bea3d` (QA clone, target dir `thead`), `cargo build --workspace --bins --locked`, both exit 0.
- Driver: `gate_local_activity_tests/diff_gate.py` (own corpus, no builder event reused). Same root path for both builds (`/private/tmp/claude-501/qla/dg`, moved aside after each run), fixed session ids and tool-use ids. Four phases: (1) gated daemon, no session: 76 JSON events + 6 raw stdin inputs (not JSON, empty, array, over 1 MiB, NUL bytes, bad UTF-8); (2) paired with an ungated peer over loopback (origin Member): 12 events; (3) a session TAINTED by a witnessed inbox read of a peer message while paired (context from the peer): 9 events; (4) link ended: the tainted session (ClosedTainted: T0 reads are the allow) and an untainted one: 26 events. Every event goes through the real hook (stdout, stderr, exit code recorded) AND, unless it is raw stdin, through `coagentd ctl … gate {event}` (the whole response line recorded).
- Corpus covers: Read (workspace, excluded, outside, `~/.ssh` key, `~/.aws/credentials`, the gate's own `gate.json`, `..` into the excluded folder, relative), NotebookRead, LS, Glob (workspace, home), Grep, Write (workspace, excluded, `~/.bashrc`, `.git/hooks`, `gate.json`), Edit, MultiEdit, NotebookEdit, WebFetch (https, file://), WebSearch, Bash (simple, rm -rf, sudo, `dangerouslyDisableSandbox`, `git worktree remove`, a `coagentd` word, `claude --dangerously-skip-permissions`, cat of an excluded file, curl|sh, background, ESC/OSC/CSI/U+202E/U+200B/CR/LF/quotes/JSON-in-string hostile text, ~60 KB command, 200 KB command), Agent (local, `isolation: remote`, `name` teammate), Task, TodoWrite, TaskCreate, AskUserQuestion, EnterPlanMode, ExitPlanMode, ToolSearch, CronList, own MCP send/share/inbox_read/wait, another MCP tool, an unknown tool, a hostile tool name; `permission_mode` absent, unknown with ESC, plan, dontAsk, bypassPermissions, a number; missing tool_input, non-object input, missing session; ConfigChange ×2 sources; PostToolUse, Stop, UserPromptSubmit, no event name, numeric event name, `pretooluse` lower case.

| outcome (hook) | count |
|---|---|
| ask | 87 |
| deny | 26 |
| block (ConfigChange) | 5 |
| allow | 4 |
| fail-closed exit 2 (raw stdin) | 6 |
| **hook runs** | **128** |
| `gate` IPC calls (raw stdin and the 200 KB event excluded) | 122 |

- Comparison (`cmp.py`, byte for byte per record): **0 differing records out of 257** (hook stdout, stderr and exit; IPC response line). One normalisation only: the paired peer's 64-hex key (a new random identity per run; the script asserts it is ONE key per run; 48 occurrences per run, in "requested by peer key …" and "peer text in this session from: …"). Without it the 14 paired records differ only in that key — shown before the normalisation was added.
- Control: the same head build with ONE event planted (`--plant`: the first Read names `readme-PLANTED.txt`) → `differing records: 2` (that event's hook record and its IPC record), exit 1. The comparison can fail.
- The gated daemon's stderr: 274 lines in both builds; after normalising keys, addresses, pids, mailbox/session ids and relay clock, the same.

## Item 3. Nothing leaks (TESTED + READ)
READ: `ActivityLog` is a field of `Engine` (`engine.rs:297`, `:446`); it is written at exactly one place, `self.activity.record(event, &v)` in `cmd_gate` (`engine.rs:1932`), after `g.decide` and after the unchanged `log!("gate: {}", v.decision)`; the returned `_line` is used only inside the two `#[cfg(coagent_red = …)]` blocks (compiled out of a clean build). It is read at exactly one place, `self.activity.page(after)` in the `Command::Activity` arm (`engine.rs:1233`), whose `Response` goes back only on that IPC connection. No other mention in `src/` (grep of `activity\.|ActivityLog|Command::Activity`). Nothing in the send queue, store, save (`flush` writes only the session/inbox/outbox state, unchanged), `log!`, audit or `coagent-mcp` (0 mentions of `activity` under `crates/coagent-mcp`, `coagent-hook`, `coagent-audit*` besides a pre-existing unrelated comment in `coagent-audit/tests/qa_fix.rs:862`). `Engine` has no `Debug` derive that could print it. `activity.rs` logs only under the red `activity_to_stderr` cfg.

TESTED: `gate_local_activity_tests/leak.py`, head build, five runs. A (gated) JOINS B (ungated) so that B's own relay child logs, per connection, "closed … after N frames, M payload bytes in". Each run: pair; a 12-second phase in which A decides 38 marked events through the real hook (36 reach the daemon: ask 21, deny 12, block 3, plus 2 raw inputs that fail closed in the hook) — 66 distinct markers placed in command text, paths, description, Write content, Edit strings, URL host and path, WebFetch prompt, tool name, `permission_mode`, session id, send text, ConfigChange path, a Stop event field, an unreadable event's tool name; then the SAME fixed traffic in every mode (A→B chat, B→A request, B reads, A taints a fixed session by a witnessed inbox read); `end`; after the link closed 4 more marked decisions (allow 3 — Grep/Glob/Read by the tainted session with markers in the pattern and the mode — and ask 1); A's MCP server asked `initialize`, `tools/list`, `resources/list`, `prompts/list`, `resources/templates/list`; stop.

| run | marked decisions | A's connection at B's relay | A's `session` counters before = after the decisions (outbox, send_next, recv_upto, unread, unread_bytes, unknown/stale frames, gaps, refused, lost …) | B's counters before = after | marker hits (19 files) |
|---|---|---|---|---|---|
| control 1 | 0 | 6 frames, 2413 bytes | equal | equal | 0 |
| control 2 | 0 | 5 frames, 1955 bytes | equal | equal | 0 |
| decide | 40 | 6 frames, 2413 bytes | equal | equal | 0 |
| decide + `coagentd watch` attached | 40 | 6 frames, 2413 bytes | equal | equal | 0 |
| decide + 2nd local client calling `activity` in a loop (3983 requests) | 40 | 5 frames, 1955 bytes | equal | equal | 0 |

- The frame and byte counts of A's relay connection fall exactly on the two values the control runs show (the 5/6 difference is one 458-byte frame of timing, present without any decision). 36 marked decisions of several hundred bytes each would add frames or kilobytes; none appear.
- Searched as bytes (case-insensitive tag): every file under the run root — A's data dir (`session.json`, `gate.json`, `outbox.json`, `inbox.json`, `identity.key`, `contacts.json`), B's data dir (the same five), `a.stderr`, `b.stderr` (B's daemon AND its relay's log), A's workspace, HOME and TMPDIR (both empty) — plus B's `inbox_read` page, both daemons' `status` while paired and B's at the end, A's MCP listings. **0 hits in every run.** The agent-side and owner-side outputs (hook stdout: 22 marked reasons; viewer: 32; poller: 32) hold markers, as they must (the hook's answer is byte-equal to main by item 2).
- A's stderr: only `coagentd: gate: <decision>` for the decisions (3 allow, 23 ask, 3 block, 12 deny), no "activity".
- A's MCP server: `tools/list` = `["send", "inbox_read", "wait"]`; `resources/list`, `prompts/list`, `resources/templates/list` → `-32601 method not found`; no "activity" in its output.

## Item 4. The IPC command (TESTED; `ipc_probe.py`, output `ipc_probe.out.txt`; raw Unix-socket client, so oversized answers would be measured, not refused by a client)
- Argument shapes: `after` absent / `args` absent / `args: null` / `after` > u64 / `1e30` / `-1` / `"5"` / `1.5` / `1.0` / `null` / `true` / an extra field / `args: "0"` → `bad_args` (connection kept); `0` and `18446744073709551615` → ok, empty, `dropped 0`. `args: [0]` (a JSON array) is accepted as `after: 0` — serde's positional struct form, the same for every command of `ipc.rs` (Note N-4). Daemon alive after all of them.
- Paging: 1 large (61,350-byte reason) + 1100 small decisions → a walk from 0 gives 1000 contiguous lines (seq 102..1101) in 16 pages, `dropped 101` on the first page, no gap, no repeat; `after=1050` → 1051..1101, `dropped 0`; `after=last` → empty, `next=last`, `more=false`; `after` > last → empty with `last` told. Byte bound: +120 large → 68 lines kept (seq 1154..1221), contiguous, `dropped 1153` = first kept − 1, 4 pages. Largest answer 1,045,102 bytes < `MAX_RESPONSE_LINE` 2,074,720 (limits.rs:75, computed). 
- Burst: 50 threads × 20 `activity {after:0}` (≈1 MiB answers each) while 200 `gate` decisions run: 0 errors, every decision answered `ask`, the record contiguous to 1421 afterwards. Hook latency through the REAL hook under 50 clients hammering: median 0.88 s, max 0.89 s (exit 0), against the hook's 10 s deadline (`burst_latency.py`); idle: < 0.01 s.
- A 200 KB `activity` request line: the daemon closes the connection (over the request line limit); daemon alive.
- Read-only: `status` byte-identical before/after 50 `activity` calls; no file of the data dir created or modified (mtimes) by 20 calls.
- Restart: a new daemon on the same data dir answers `after: 1421` with no lines and `last: 0`.
- `--gate` off: `{"ok":false,"error":{"code":"gate_off",…}}`.
- Idle timer (`--idle-exit-secs 3`): a gated daemon polled ONLY by `activity` every 0.2 s exits after 3.3 s; polled by `status` every 0.2 s it is still alive after 12 s (as on main, where every command resets it). READ: `engine.rs:1156-1158` skips `last_activity` for `Activity` only; `changes_state` excludes it (`:1160`), so no flush is forced; the dispatch arm (`:1229-1236`) touches nothing but `self.activity.page`.

## Item 5. The viewer (TESTED; `viewer_probe.py`, `softwrap.py`, `stub_viewer.py`; output `viewer_probe.out.txt`)
- 108 decisions through the real gate, 20 hostile strings each as tool name, as mode and inside a Bash command (OSC title set with BEL and with ST, CSI clear+home, RIS `ESC c`, 8-bit CSI U+009B, CR + the notice, LF + a forged entry, LF + the notice, U+202E/U+202C, U+2066/U+2069, U+200B/C/D, U+FEFF, U+2028 + forged entry, U+2029, U+0085 + forged entry, NUL, DEL, U+061C, U+180E, a tag character U+E0041, U+FFF9) plus 45 plain reads: 26,958 bytes of output, **no byte < 0x20 but LF, no 0x7f, no character of category Cc/Cf/Zl/Zp**; line 1 is exactly the notice, line 2 the header; 108 entry lines numbered 1..108 in order; the notice again before entries 21, 41, 61, 81, 101 (lines 23, 44, 65, 86, 107), each followed by an entry; no line starts with the notice text unless it is the notice; every line is the notice, the header or starts with `#<seq>`. Text checked: "Only you see this. Nothing here is sent to the other side." (FR-4, exact).
- Hostile text shows escaped, e.g. `tool T\u{1b}]0;PWNED-TITLE\u{7}`, `Claude Code mode: m\u{1b}[2J\u{1b}[H`.
- **Soft wrap (Finding MJ-1):** one proposed Bash command whose text is `echo build ok` + dots + an 80-character copy of an entry + the notice padded with dots gives, on an 80-column terminal (rendered with `fold -w 80`), these rows of ONE printed entry:
  ```
  row 4:  code given to it as text or on a pipe; command: echo build ok..................
  row 5: #4 00:00:01 UTC | CoAgent refused | tool Bash | Claude Code mode: default | coag
  row 6: Only you see this. Nothing here is sent to the other side.......................
  ```
  Row 5 reads as a separate entry, row 6 as the notice. No space is needed (dots pad), so collapsing spaces would not stop it. The agent only has to PROPOSE the command: the line is shown on decision, before and whatever the owner answers. Wrap points for 100, 120, 160, 200 columns were also hit by space padding in `viewer_probe.py`.
- Gate off: one line, exit 3. No daemon: "coagentd watch: the daemon is not running (nothing answers on its socket)", exit 1, at once. Daemon SIGKILLed while it runs: "…the daemon stopped; nothing more will be shown", exit 1 after 0.08 s. Daemon frozen with SIGSTOP (accepts, never answers): the same line, exit 1 after 5.06 s (within GONE_BOUND 6.5 s).
- **Restart under the viewer (Finding m-1):** viewer had seen seq 1..3; the daemon was SIGKILLed and a new one started on the same data dir and decided 6 calls before the viewer's next poll (twice, same result). The viewer printed, with no "restarted" or "stopped" line:
  ```
  #1 … Read: <ws>/old0      #2 … <ws>/old1      #3 … <ws>/old2
  #4 … Read: <ws>/new3      #5 … <ws>/new4      #6 … <ws>/new5
  ```
  The new daemon's lines 1..3 (`new0..new2`) were never shown, and the numbering reads as one unbroken run. The owner CAN be misled about missing lines.
- 200 KiB reason (only from a stub on the socket: the gate cannot produce one within the 128 KiB request; the largest real reason seen was 61,350 bytes): printed whole as one 204,874-byte line. The same stub shows the viewer prints raw ESC/CR/LF if something other than the daemon answers on the socket (known, BACKLOG "does not re-escape"; Note N-2).
- Input and files: READ `watch.rs` (no stdin, no file API; `la_source_audit` enforces the words); TESTED: the viewer run with a filled stdin pipe, an empty cwd, empty HOME/TMPDIR: all still empty afterwards. Not traced at syscall level (dtruss needs root).

## Item 8. Docs, words and BACKLOG (READ)
- `docs/DAEMON.md` §3 row `activity`: fields `lines[]` {seq, at_ms, event, tool, mode, decision, reason}, ≤ 64 lines and ≤ 1 MiB of JSON, `next`, `last`, `dropped`, `more`, gate mode only, does not reset the idle timer — each matches `activity.rs:209-237` and `engine.rs:1156-1160,1229-1236`, and item 4's runs.
- §8 "Local activity": record (1000 lines / 4 MiB, oldest out; 256 KiB cut with marker) = `activity.rs:26-34,118-139,193-200`; viewer cadence 0.5 s, 5 s timeout, GONE_BOUND 6.5 s = `watch.rs:32-37`; notice text = `watch.rs:25` = FR-4 exactly; "reads no input and draws with no cursor control" = READ `watch.rs`. The four limits of the brief's §8 are there (same-user read, decision not outcome, shell text not effects, memory only / restart empties), plus the builder's two (kind/target only through an ask's reason; the U-B1 M7 terminal note, marked REASONED in BACKLOG). No word says a call "ran"; the viewer's words are allowed/asked/refused/blocked (`watch.rs:55-65`), and an allow line printed by the clean viewer reads "CoAgent allowed" (leak run "decide + viewer").
- One sentence the code does not fully bear out: "a daemon that stops or is killed while it runs → 'coagentd watch: the daemon stopped; nothing more will be shown'; each is one plain line and exit code 1 within 6.5 s" — not when the daemon is restarted within one poll (Finding m-1). The same holds for `docs/M0-OUTCOMES.md`'s "A missing or stopped daemon is said in one line".
- BACKLOG: the seven r3 entries (M-1, N-b, N-c, N-d, N-e, N-f, N-g) match `gate_ALLOW_MEASURE_r3_verdict.md` Findings table (places, symptoms, fixes) — N-a correctly left out (FR-10). The builder's three own entries state facts: the M7 entry says REASONED and "not run against the viewer"; "does not re-escape" is true (stub test, item 5); "UTC only" is true (`watch.rs:68-71`). Items 8-12 (W-GATE-TEST r2) correctly not written: the base has no `spikes/W1-windows-exec-hook/`.

## Item 9. Names and ids (TESTED; `scan.py`, run with `python3 -B -I`)
- Words and roots passed on the command line only (account name, host name in three forms, home folder, volume root, workspace folder, the coordinator folder, three mail addresses, two name words), each in plain, backslash-escaped, URL-encoded (two forms) and slug spellings, case-insensitive; plus UUID, `toolu_…`, `msg_0…`, `req_0…` classes: 41 patterns.
- Controls: a copy of `watch.rs` with one planted line naming the home folder, and a planted binary with the host name between NUL and 0xFF bytes → `scanned 21 files (19 from the branch, 2 controls), 41 patterns: 7 hits`, all in the two controls.
- The 19 files the branch adds or changes, blobs at `02bea3d`: `scanned 19 files … 41 patterns: 0 hits`.
- (The coordinator seat's role name appears in new comments and docs, e.g. `watch.rs:23` "Friday's ruling P9", as it does 8 times in `docs/DAEMON.md` on main: a role, not a person or account; not a finding.)

## Item 6. Each red control (TESTED + READ)
- `RED_ONLY='^(activity_|watch_)' bash scripts/red-controls-daemon.sh` in the QA clone (own `COAGENT_TOOLS`, target dir `tred`; heavy count 1 before), 15:59–16:22: **12/12 `RED (as required)`**, `final clean run: green (57 test binaries; ignored under rulings: 2)`, exit 0 (`red_la.out.txt`).
- Each row's own log: the named test fails at its own assertion — LA-1 count 6 ≠ 7 (`la_every_decision.rs:100`); LA-2 reason cut to `coagent asks: Write (Edit, T1)` (`:155`); LA-4 `"default"` ≠ null (`la_mode_as_reported.rs:45`); LA-5 A's `send_next` 1 → 7 (`la_nothing_to_peer.rs:52`); LA-6 stderr (`la_nothing_kept.rs:136`) and disk (`:122`); LA-7 raw 0x1b (`la_viewer.rs:47`); LA-8 first line is the header (`:99`); LA-9 1005 ≠ 1000 (`la_bounded.rs:86`) and "CoAgent ran" ≠ "CoAgent allowed" (`:167`); LA-10 ok answer (`la_viewer.rs:123`); LA-12 no exit within 6.5 s (`:139`).
- READ every `cfg(coagent_red …)` branch: each is in the real code path and changes only its own thing (`activity.rs:112,122,168,173,187,193`; `engine.rs:1229-1233` gate-off arm, `:1934-1949` the two `#[cfg]` blocks next to the one `record` call; `watch.rs:58,147,185,208`). `activity_to_peer` uses the real `cmd_send`; `activity_on_disk` writes in the data dir; `activity_to_stderr` uses the real `log!`.
- Gating: `build.rs` `LA_RED` (12 names) with `rustc-check-cfg`; refuses an unknown name, any other red variable at the same time, and a release profile. TESTED: `COAGENT_RED_LA=watch_says_ran cargo build --release -p coagent-daemon` → exit 101, "COAGENT_RED_LA is for test builds only" (`build.rs:287`). The clean release `coagentd` contains 0 × "CoAgent ran", 0 × "activity.red", 0 × "activity: " (and 1 × "CoAgent allowed", 1 × the notice).
- `watch_says_ran` judged: `la_bounded` catches it only by calling `watch::decision_words("allow")` directly; no la_* test prints an allow line through the viewer. The function IS the one `render` uses for every line (READ `watch.rs:88`), and TESTED: the red build's real viewer, attached while a tainted closed session's Grep/Glob/Read were allowed, printed `#38 … | CoAgent ran | tool Grep` (3 lines), so the break is in the printed path and a printed-output test would catch it. A real test: run the viewer in `la_every_decision`'s scenario (it already produces an allow) and assert the printed allow line holds "| CoAgent allowed |" and no " ran". Note N-3.
- The 12 `la_*` tests clean, three times, QA build `thead`: 3 × (la_bounded 1, la_every_decision 2, la_mode_as_reported 1, la_nothing_kept 1, la_nothing_to_peer 1, la_source_audit 1, la_viewer 4) = 3 × 11 test fns in 7 binaries, all `ok`; no flake. (The brief's "12" counts property 12's `la_daemon_gone`, which is one of la_viewer's 4.)

## Item 7. Older checks and pinned files (TESTED)
- `bash scripts/test-p1p.sh` (QA clone, `thead`): `run 1/1: exit 0/0, 16 tests ok, 27 s` / `ALL 1 RUNS GREEN`.
- `cargo test -p coagent-daemon --test release_audit --test ipc --test acceptance --test win_guards`: acceptance `ok. 2 passed`, ipc `ok. 1 passed`, release_audit `ok. 1 passed`, win_guards `ok. 5 passed`.
- `cargo fmt --all --check` (QA clone): exit 0, no output. (clippy not re-run: see "not checked".)
- P1P red rows re-run (heavy count 0 before): `RED_ONLY='^(hook_|gate_unknown|witness_|waiter_|taint_|configchange_)' bash scripts/red-controls-daemon.sh`, 16:24–16:53: **13/13 `RED (as required)`** (P1P-1, -3 ×2, -4, -5a, -5c, -5e, -6, -7, -A1-1, -A1-M4, -A1-M2, -A1-4), final clean run green (57 binaries), exit 0 (`red_p1p.out.txt`).

## The builder's section 9 choices, judged
- `la_support` moving `p1p_support::Run`'s directory to `tmp/la/`: fine; `p1p_support` itself untouched (blob equal).
- Answer fields `lines/next/last/dropped/more`: fine for paging (item 4); `last` alone cannot show a restart that catches up within one poll (m-1) — a per-start id is needed.
- Exit codes 1 gone / 2 usage / 3 gate off: fine, tested.
- Header and UTC times: fine for a first slice; no date on the line (Note in BACKLOG already).
- No second escape in the viewer: acceptable by Friday's ruling FR-1 scope, but the stated reason ("would mask the red control") is a test-design reason, not a product one (N-2).
- Two extra limits in docs: both true and useful.

## Findings
| ID | Severity | Finding (exact place) | Reproduction | Suggested fix, in words |
|---|---|---|---|---|
| MJ-1 | **Major** (display safety: "a line that can be made to look like the notice or like another line") | `crates/coagent-daemon/src/watch.rs:74-91` (`render`) and `:212` print each entry as ONE physical line of any length; the reason holds the agent's command text verbatim (display-safe per character, but any length up to the card-field cut, any visible filler). The terminal's soft wrap then starts rows at text the agent chose. With one proposed Bash command, at 80 columns, row 5 of the entry reads `#4 00:00:01 UTC \| CoAgent refused \| tool Bash \| Claude Code mode: default \| coag` and row 6 reads `Only you see this. Nothing here is sent to the other side.……` — a forged entry and a forged notice. Dots pad, so no whitespace is needed. The agent need not run anything: the line appears on decision, whatever the owner answers in Claude Code. Not covered by the documented M7 limit (that one needs a process writing to the tty; this needs only the command TEXT, sandbox or not). The builder's tests check bytes per printed line only. | `python3 -B gate_local_activity_tests/softwrap.py <head bin dir> <new root> <new out dir>` (prints the rows, rendered with `fold -w 80`) | Make every physical row of the viewer's output unambiguous without knowing the width: hard-wrap each entry's free text in the viewer at a fixed width (e.g. 72 columns) and start every continuation row with a fixed mark no entry and no notice starts with (e.g. `   ┆ `), so a terminal of at least that width never soft-wraps and a forged `#…`/notice text is always visibly a continuation. Add a test with a filler-aligned forge (this repro) at 80/100/120 columns asserting that no row other than a real entry starts with `#<digits> ` and no row other than the notice equals it. |
| m-1 | Minor | `watch.rs:190-195`: a restart is detected only as `last < after`. A daemon killed and restarted within one 0.5 s poll that decides more calls than the viewer had seen is not noticed: no "restarted"/"stopped" line, its first lines are never shown, and the numbering reads as one unbroken run (shown: old 1..3 then new 4..6; new 1..3 lost). `docs/DAEMON.md` §8 ("a daemon that stops or is killed while it runs → … the daemon stopped … within 6.5 s") and `docs/M0-OUTCOMES.md` ("A missing or stopped daemon is said in one line") do not hold in that case. Narrow (needs a sub-0.5 s restart), not inducible by the agent without an approved command, hence Minor. | `viewer_probe.py`, part "restart under the viewer" (twice, same result) | Put a per-start id (random, or the daemon's start time + pid) in every `activity` answer; the viewer prints "the daemon restarted; the lines before it are gone" and resets `after` when it changes. Or, in words, state the case in §8. |
| N-1 | Note | `watch.rs:79,84-86`: fields are joined with ` \| `, and tool name and mode may contain ` \| ` (display-safe characters), so within one line a tool name like `Bash \| Claude Code mode: plan` adds a second "mode" field. The decision word comes before the tool and cannot be moved. Tool names come from Claude Code / MCP servers, modes from Claude Code. | — | Quote the tool and mode (e.g. `tool "…"`) or escape `\|` in those two fields. |
| N-2 | Note | `watch.rs:84-89` prints daemon fields without a second escape: a stub on the socket (same user, only while no daemon holds it) makes the viewer print raw ESC/CR/LF (`stub_viewer.py`). Already in BACKLOG; the reason given there (masking LA-7's red) is a test-design reason. | `python3 -B stub_viewer.py <bin> <root>` | Escape in the viewer too, and let LA-7's test assert on the IPC answer (raw) as well as on the printed bytes. |
| N-3 | Note | `la_bounded.rs:160-167`: `watch_says_ran` is caught by a direct call of `watch::decision_words`, not by a printed line. The break IS in the printed path (red build printed `CoAgent ran` on three real allows, item 6), so the property holds, but no test prints an allow. | item 6 | Attach the viewer in `la_every_decision` (which has an allow) and assert the printed allow line. |
| N-4 | Note | `ipc.rs` `args()`: `args: [0]` is accepted as `{after: 0}` (serde's positional form). Shared by every command on main; harmless. | `ipc_probe.out.txt` | None needed; mention if the protocol is ever specified strictly. |
| N-5 | Note | `la_source_audit.rs` is a word check (`std::fs`, `stdin`, …): an alias (`use std as s; s::fs::…`) would pass. Same style as `release_audit.rs`. | READ | Accept as a tripwire; reviews remain the real check. |
| N-6 | Note | A frozen daemon (SIGSTOP: accepts, never answers) is reported as "the daemon stopped" (5.06 s). Correct in effect; "does not answer" would be the exact word. | `viewer_probe.py` | Optional wording. |

No Blocker. One Major (MJ-1).

## What was NOT checked
| item | why | who could check it |
|---|---|---|
| The viewer on a real terminal emulator (soft wrap was rendered with `fold -w 80`, which wraps ASCII exactly as a terminal does) | no interactive terminal driven in this seat | the owner, by running `softwrap.py`'s command in a real window |
| The viewer and `activity` on Windows | `--gate` refused there; nothing built or run | a Windows seat |
| Syscall-level proof the viewer opens no file and reads no input | dtruss/fs_usage need root | READ + empty cwd/HOME/TMPDIR test instead |
| Packet-level capture of the relay link | not set up; the relay's own per-connection frame and byte counts were used instead (item 3) | a seat with a capture tool |
| `cargo clippy -p coagent-daemon --all-targets -- -D warnings` | not re-run (builder's claim) ; `cargo fmt --check` re-run clean | Friday's merge check (`scripts/check.sh`) |
| `scripts/check.sh` whole, `cargo deny` | brief: Friday's clean-clone merge check runs it | Friday |
| Real Claude Code / a model | brief: no model run | — |
| A reason > 256 KiB through the real gate (the cut marker) | the gate cannot produce one within the 128 KiB request (largest seen 61,350 bytes); only the unit test covers the cut | — |

## Cleanup
No daemon, relay, viewer or test process of mine is left (`pgrep` on the work dir: none). Everything I made is under `/private/tmp/claude-501/qla` (clone, worktree of main, target dirs, run roots moved aside, never deleted) and the copies in `m1_review/gate_local_activity_tests/`.
