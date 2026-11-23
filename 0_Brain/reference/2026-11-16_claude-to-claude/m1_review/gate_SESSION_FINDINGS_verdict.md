VERDICT: GO WITH NOTES — head 663c93eccd4f758379973f8f2b6c26b1fc7bab59

# QA-SESSION-FINDINGS verdict (independent check, tier 2: documentation only)

Branch `session-findings`, head `663c93eccd4f758379973f8f2b6c26b1fc7bab59`, base main `3164374a8a20d73296558997438b97a41a7837ad`.
TESTED = I ran it. READ = I read it at the head. I ran no build, no test, no product program, no model; I wrote nothing in the project except my status file.

## BLUF (four points)

1. **Words only: yes.** Four `.md` files changed and nothing else (0 non-`.md` paths, control passed); no code, test, script, Cargo or `preview/lib` path; and nothing in the tree reads any of the four files (21 non-`.md` mentions, every one a comment).
2. **The "what ran" claims are honest.** 85 tagged statements checked against their sources: 80 supported, 3 over-claimed (all small: a self-report not labelled as one, and one ambiguous RAN tag), 1 under-claimed (a stale NEVER RUN), 1 wrong (a negative claim about the logs). No RAN tag names the wrong build, date or machine. The counts in the two-agent section are right (5 `gate: ask`, 2 `handed out 1 message(s)`; I counted them).
3. **Nothing makes the product sound safer than it is.** Both "known limit" paragraphs (hand `send` passes the gate; unread peer text sits in clear in a file) match the rehearsal report and the code at the head. No names, addresses, drive letters, ids or invitation lines in the added lines. The owner's sentence is character-for-character the coordinator's 10:25 record.
4. **Owed before merge: nothing blocking.** Worth fixing in a quick follow-up commit (not required): the branch shifted `lan.md` by 6 or more lines, so 12 of the 15 `lan.md:NN` pointers in `windows.md` now point at different text (Minor 1). Four other Minors and two Notes are below.

## 1. Head and base proofs (TESTED)

- `git ls-remote` against the GitHub remote: `refs/heads/session-findings` = `663c93eccd4f758379973f8f2b6c26b1fc7bab59`; `refs/heads/main` = `3164374a8a20d73296558997438b97a41a7837ad`. Both equal the brief's.
- I fetched both into my own clone; `git merge-base --is-ancestor base head` = true; two commits between them (`4bc0ad9`, `663c93e`). Main has NOT moved, so the merge brings in nothing beyond the branch.
- The builder's status file (`coagent/5_Project_History/STATUS_SESSION_FINDINGS.md`) ends `READY FOR QA SESSION-FINDINGS`, with the head line `663c93eccd4f758379973f8f2b6c26b1fc7bab59` above it.

## 2. Item 4.1 Scope (TESTED)

- `git diff --stat base...head`: `BACKLOG.md` 45, `docs/DAEMON.md` 35, `preview/demo/lan.md` 38, `preview/demo/windows.md` 90; 4 files, 195 insertions, 13 deletions (as the builder says).
- `--name-only`: exactly those four. `grep -v -c '\.md$'` = **0**; control `printf 'a.rs\nb.md\n' | grep -vc '\.md$'` = 1. `--name-status` is four `M`; `--summary` is empty (no mode change, no add, no delete, no rename).
- `git diff base...head -- '*Cargo.toml' Cargo.lock` = 0 bytes. Two-dot and three-dot diffs are identical.
- `cargo fmt --all --check`: NOT run (optional; the diff has no `.rs`, so it cannot change).

## 3. Item 4.2 Nothing reads the changed files (TESTED)

- My own pattern (not the builder's), over every tracked file at the head: `(^|[^A-Za-z0-9_])(DAEMON|BACKLOG)\.md|(^|[^A-Za-z0-9_-])(lan|windows)\.md|demo/(lan|windows)|docs/DAEMON`, case-insensitive. 92 hits; 71 are in `.md` files (documents naming each other, not reads); **21 are in non-`.md` files: 19 `.rs`, 2 `Cargo.toml`.** Filter for lines that are not `//`, `//!`, `///`, `#`, `--`, `*` comments: **0 left.**
- The 21, ruled out one by one: `Cargo.toml:53` and `:63` (`#` comments naming BACKLOG); `//!`/`///`/`//` doc comments in `coagent-audit-host/src/fsio.rs:1`, `coagent-audit/tests/gate_r5_wrapper.rs:4`, `qa_fix_wrapper.rs:4`, `coagent-daemon/src/datadir.rs:477`, `engine.rs:5,133,497,507`, `gate.rs:1,23`, `ipc.rs:84`, `lib.rs:16`, `main.rs:6,11`, `release.rs:8`, `tests/p1p_deny_blocks.rs:38`, `tests/p1p_support/mod.rs:259`, `coagent-hook/src/main.rs:5`, `coagent-roster/src/deputy.rs:443`. A comment that names a file is not a read.
- Wider net: read/include calls naming any `.md` (`include_str!`, `read_to_string`, `File::open`, `cat`), globs of `*.md`, directory walks of `docs` or `preview/demo`, every `build.rs`, every `scripts/*.sh`, `ci/proposed-workflow.yml`, `deny.toml`. Result: no read of any of the four files.
- **Positive controls:** (a) `crates/coagent-cli/tests/identity_cli.rs:761` and `:1219` really read `README.md` (my wide net finds them); (b) `crates/coagent-policy/tests/t12_docs.rs:14,48,75,87` and `t21_bypass_refusals.rs:405` really read `docs/POLICY.md`, a docs file the branch does NOT change (so a docs-reading test exists in this tree and my net sees it).
- The builder's own command and mine agree (no non-comment read). Raw hits: `gate_session_findings_tests/step2_all_hits.txt`, `step2_nonmd_hits.txt`.

## 4. Item 4.3 Every tag against its source (READ; the main work)

Sources: rehearsal report (`RH`, by line); the PC results files (`WO-7p2`, `WO-10`, `WO-11`, `WO-12`, `WO-13`, `WO-14_1..4`, by line); the two Mac sessions' logs (`c1/`, `c2/`); the coordinator's daily record (`D 09:55`, `D 10:25`, `D 11:34`); the two-agents sheet; code at the head.

### 4a. The settle-at-least points

- **Hand `send` paragraph.** Every half is in the rehearsal: `ctl send` of a request (C2R-3) and of a reply with `re` (C2R-2) answered `ok:true`, `sent_now:true`, both read on the far side (RH 208-219, 231, 240); hand `inbox_read` and `wait` answered `gate_missing` at once (RH 205, 223, 225). Code opened at the head: `engine.rs:1177-1181` `Command::Send` goes straight to `cmd_send` (no `take_ticket`); `:1182-1185` `Command::InboxRead` calls `take_ticket` first; `Wait` too (`:1186`). I read the opening of `cmd_send` (from `:1664`: session, counters, hard stop, size, outbox checks) and searched `:1664-1790` for gate, witness, ticket and taint words: the only hit is a red-control comment. **SUPPORTED.**
- **"One invitation at a time".** `session_active()` (`engine.rs:1417-1424`) = a session not ended OR a pairing `Waiting`; `invite` refuses with the text "a session or pairing is already active" (`:1458-1464`). `PAIRING_TIMEOUT` = 600 s (`:74`), applied at `:2766-2770`. `cmd_end` (`:2016-2037`): aborts a waiting pairing with "ended by the local user"; `ended:false` only when `self.sess` is `None` (`:2024-2026`); otherwise `ended:true` (`:2036`), "ended or not". `ended:true` half RAN (RH 283-286, 296-298). `ended:false` half: no source prints the answer; the doc says UNVERIFIED and gives the reason; the only support is the first-link host log (`c1/mac_host.log:3-4`: "pairing FAILED: ended by the local user", then a new invite works). Honest. The 600 s figure is READ only and written so. The state test (`session` null or ended, AND `pairing` null or not waiting) matches RH 443-446 and the code. **SUPPORTED** (one ambiguous RAN attach: Minor 5).
- **Windows guide sections 2 and 5 (addendum 11).** §2 RAN: `WO-7p2:21-27` `TcpTestSucceeded : True`, `InterfaceAlias : WiFi` (step 8, the `3337192` build per `WO-7p2:8` and `windows.md:31-32`). §5, each step: `send` request `WO-7p2:53-55` (`ok:true`, `sent_now:true`, exit 0); `inbox_read` `:56-58` (two messages, `"ack":2`, exit 0, with a `chat.msg` whose `re` equals the send's id `1b7b…`); `inbox_ack` `:59-61` (`removed:2`); `reply` with `re` `:62-64` (`ok:true`, `sent_now:true`). "With the session's own text, not the `PVM-L1` text": the report does not print the text, but the Mac's own read (`c1/mac_read_1.json`) shows `C2X-1 request from Windows: please reply` with the same id. Anything tagged RAN that the file does not show: **none.** Still NEVER RUN and kept so: the PVM-L1 text.
- **Two agents (addendum 14).** Self-report kept apart from measurement: yes for the WO-14 run (the doc says "BY THE AGENT'S OWN REPORT (a self-report, not a measurement)"; measured items are `WO-14_4:128,130` log lines, `:142-151` empty folder, `:139-141` settings identical, `:135-138` marker count 0 with control, `:132-134` stop lines, `:17,152` exit code NOT recorded). **Counts, by me:** `grep -c 'gate: ask' c2/mac_host.log` = **5** (lines 11, 12, 14, 15, 17); `grep -c 'handed out 1 message(s)'` = **2** (lines 13, 18); the doc says 5 and 2. No approval count is written (the owner's "three" stays in the coordinator's record). Builds: morning `3337192` (`windows.md:31-32`, `WO-7p2:8`); second session `3164374` on both (PC `WO-11:12`; Mac scratch build `RH 17-19` and `D 11:34`). The run used the skip-permissions form: the WO-14 mails do not print the flags, but `WO-13` prints the final `run-agent.cmd` (`--dangerously-skip-permissions`, plugin folder with two files, no hooks) and it was the file run (`WO-14_3:6`).
- **Reconnect question (addendum 13).** `reconnects 1` in the first link: `WO-7p2:48,51,66`; the log line `session link down (relay refused chan.open (not_found)); reconnecting` at `WO-7p2:87`, `attached` at `:88`. `reconnects 0` in the second: `WO-14_2:8`, `WO-14_4:74,114`; the guest log printed whole (`WO-14_4:118-134`) has no such line. The entry asks and does not answer. Code at the head: `link.rs:290-291` (the "relay refused chan.open" text; `NotFound` retried only with `create`), `:153` (`create` is the convener's), `state.rs:611` ("no such channel"), `engine.rs:2477` (log text), `recovery.rs:1174` (`reconnects += 1`). One wrong sentence: Minor 2.
- **Relay stop lines.** First link (with `tee`): `c1/mac_relay.log` ends with reminder lines and no stop lines; `D 09:55` says "tee dies with it". Redirected: loopback RH 345-349; second session `c2/mac_relay.log:41-43` = `coagent relay: interrupt received; stopping` / `<epoch> relay stopped` / `coagent relay: stopped`; `D 11:34` agrees. The epoch quoted is a relay timestamp, not an id. **SUPPORTED.**
- **Headless line of `lan.md` tier 2.** Stays "NEVER RUN in this form"; the reasons for the flag order are tagged "REASONED from the help text; UNVERIFIED"; "would have been denied" is "REASONED; never run". Cites opened: `G1/RESULT.md:6,7`, `U2/RESULT.md:9`, `U4/run.sh:36`, `lib/common.sh:57`, `WO-11:34-73`. **SUPPORTED.**
- **Sign-in sentence (item 15).** `D 11:34`: the Mac's session "did not pick up the subscription … until I logged in"; tagged as the owner's report. **SUPPORTED.**
- **Used-line-file sentence (item 17).** Code opened by me: `engine.rs:1612-1625` any failed `mailbox_join` answers code `INVITE`, "invite refused by the relay (used, expired or unknown)"; `state.rs:328-360` unknown id = `NotFound` "no such mailbox", past expiry = `Expired` "mailbox expired", second joiner = `Full`; `:395-408` a burned mailbox is removed; burn at pairing seen in `c2/mac_relay.log:23`. The doc writes "READ, not run in these sessions" (no run of a spent line exists). The guard that refused to overwrite: `D 11:34`. **SUPPORTED.**

### 4b. The tag table (every tagged statement added by the branch)

Verdicts: S = SUPPORTED, OC = OVER-CLAIMED, UC = UNDER-CLAIMED, W = WRONG. Source cites are lines in the files named above.

| # | Statement (file) | Tag | Source line that supports it | Verdict |
|---|---|---|---|---|
| D1 | second `invite` while one waits → `session_active` (DAEMON §4) | RAN loopback + two machines | RH 277-282; D 09:55 slip 3 | S |
| D2 | 600 s, `PAIRING_TIMEOUT`, applied at 2766-2770 | READ | `engine.rs:74`, `:2766-2770` opened | S |
| D3 | `end` aborts a waiting pairing, state "failed", "ended by the local user" | READ | `engine.rs:2017-2022`; RH 286 | S |
| D4 | `ended:true` with a session record (ended or not), `ended:false` with none | READ | `engine.rs:2024-2026, 2036` opened | S |
| D5 | `ended:true` with a waiting pairing and an ended session | RAN loopback | RH 283-286, 296-298 | S |
| D6 | `ended:false` on the first link; printed answer not in record | RAN (clearing) / UNVERIFIED (answer) | `c1/mac_host.log:3-4` | S |
| D7 | next `invite` works after `end` | RAN both | `c1/mac_host.log:4`; RH 287-295 | S |
| D8 | a "both null" test refuses every re-invite because `status` keeps the ended session and finished pairing | RAN loopback | RH 265, 286 (state kept); no run of a refused invite | OC (Minor 5) |
| D9 | empty `--relay-url ""`/`--relay-pin ""` start; `relay_unavailable`; empty `mailbox open failed:` (DAEMON §7) | RAN loopback | RH 367-371 | S |
| D10 | `main.rs:165-180` takes both values as given | READ | opened | S |
| D11 | `Command::Send` → `cmd_send`, no witness; reads take one | READ | `engine.rs:1177-1185, 1664` opened | S |
| D12 | hand `request` and `reply` accepted and delivered, no prompt; hand `inbox_read`/`wait` refused `gate_missing` | RAN loopback | RH 205-231, 237-249 | S |
| D13 | any same-user process reaching the socket can send as this device | REASONED | DAEMON §3 "same uid only"; RH 244-249 | S |
| D14 | the owner's approval of a `send` ask guards the agent's words only | REASONED | RH 432-438 (F3) | S |
| D15 | `inbox.json` (0600) holds unread peer text in clear; markers found | RAN loopback | RH 365, 439-441 (F4) | S |
| D16 | the gate guards release over IPC, not the file | REASONED | RH 441-442 | S |
| B1 | hand `send` entry (symptom, code, POLICY.md:245, design questions) | RAN + READ | RH as D12; `POLICY.md:245` opened | S |
| B2 | clear text at rest entry; "owner's call" | RAN | RH 365 | S |
| B3 | empty relay flags entry (scope: refuse at start) | RAN + READ | RH 367-371; `main.rs` | S |
| B4 | lost invitation blocks a new one; two-machine and loopback evidence | RAN | D 09:55 slip 3; RH 277-298 | S |
| B5a | `pvpaths.py:122-125, 24, 126-128, 139-145`, `make-plugin.sh:20` | READ | all opened (`:122-125` `coagent-hook`/`coagent-mcp` without `.exe`; `:141,143` always `hooks/`) | S |
| B5b | hand-written MCP-only plugin RAN on the PC at `3164374` | RAN | `WO-11:99-100, 255-263`; `WO-12:15` | S |
| B6 | `setup.sh` headings skip `## 2.` | RAN loopback | RH 49-52, 108; `setup.sh:45,48` opened | S |
| B7 | `COMMANDS.txt` mode 644, holds no secret | RAN loopback / READ | RH 99, 108; `setup.sh:91` | S |
| B8 | `mkdir` before `setup.sh` collides | REASONED | RH 465-466; `setup.sh:26,30` | S |
| B9a | first link: `session link down (… not_found)`, `reconnects 1` | RAN two machines | `WO-7p2:48, 87-88` | S |
| B9b | second session: no such line, `reconnects 0` | RAN two machines | `WO-14_2:8`; `WO-14_4:74, 114, 118-134` | S |
| B9c | code lines `link.rs:288-291, 152-153`, `state.rs:608-611`, `engine.rs:2473-2479`, `recovery.rs:1174` | READ | all opened (text at `link.rs:291`, `create` at `:153`, `state.rs:611`, `engine.rs:2477`, `recovery.rs:1174`) | S |
| B9d | "the order across the two machines is not shown by any log read" | negative claim | the relay logs show connection order: `c1/mac_relay.log:38-45`, `c2/mac_relay.log:26-31` | W (Minor 2) |
| L1 | piped through `tee`, the relay's stop lines were lost | RAN two machines | `c1/mac_relay.log` tail; D 09:55 | S |
| L2 | redirected to a file, stop lines kept | RAN loopback | RH 345-349, 456-457 | S |
| L3 | same, on the second session | RAN two machines | `c2/mac_relay.log:41-43`; D 11:34 | S |
| L4 | terminal shows nothing while the relay runs | RAN loopback (untagged) | RH 134 | S |
| L5 | sign in before any step that starts `claude` | RAN, owner's report | D 11:34 | S |
| L6 | tier-2 line "NEVER RUN in this form" | NEVER RUN | none exists | S |
| L7 | the old line's `send` would have been denied | REASONED | `G1/RESULT.md:7`, `U2/RESULT.md:9` | S |
| L8 | the new form copies spike U4 | READ | `U4/run.sh:36` | S |
| L9 | prompt right after `-p`, allow list last | READ | `lib/common.sh:57` | S |
| L10 | a prompt after `--allowedTools` may be read as a tool name | REASONED; UNVERIFIED | `WO-11:69-73` | S |
| L11 | `ToolSearch` is called first: RAN on the PC (WO-12) | RAN | `WO-12:11-13` = the agent's own text (self-report), not labelled so here | OC (Minor 4) |
| L12 | `--permission-mode manual --allowedTools` appear in the PC's `--help` | RAN as `--help` only | `WO-11:34-73` | S |
| L13 | skip-permissions flag RAN on the PC, one model run, unpaired daemon | RAN | `WO-12:15, 36` | S |
| L14 | the flag allows every tool, no prompt | REASONED | `WO-13:39` | S |
| L15 | accepted by the owner for the development test agent on the owner's own PC only | owner's ruling | D 10:25; clarifications file | S |
| L16 | "every other tool is denied, not asked" (untagged) | REASONED | `G1/RESULT.md:7`, `U2/RESULT.md:9` | S (untagged) |
| L17 | marker count on `<root>/r.log` and both daemon logs | READ | agrees with step 4 | S |
| W1 | §2 `Test-NetConnection` answered `TcpTestSucceeded : True` | RAN two machines, `3337192` | `WO-7p2:21-27` | S |
| W2 | over the PC's wireless interface | RAN | `WO-7p2:25` `InterfaceAlias : WiFi` | S |
| W3 | build `3337192` for WO-7 part 2 | RAN | `WO-7p2:8`; `windows.md:31-32` | S |
| W4 | line length 363 (home network) and 359 (loopback), measured by the coordinator 2026-11-22 and 2026-11-23 | MEASURED | daily 11-22 ("359 characters"); D 09:55 ("363 … 359 on loopback"); RH 176 | S |
| W5 | a real line crossed through a one-line file read by `set /p`; `"paired":true`, exit 0, first try | RAN two machines, `3337192` | `WO-7p2:14-15, 46`; `set /p` form in `WO-11:203` (same helper form) | S |
| W6 | a line is single use; a spent, expired or unknown mailbox is refused | READ, not run | `engine.rs:1612-1625`; `state.rs:328-360, 395-408` opened | S |
| W7 | a spent line file on the drive: the coordinator's guard refused to overwrite | RAN two machines | D 11:34 | S |
| W8 | §5 heading "partly RAN; see each step" | RAN / NEVER RUN | per step below | S |
| W9 | "NEVER RUN with a Windows guest: on the first link the Mac host was driven by `ctl`" (§5) | NEVER RUN | stale: in the second session the Mac host side ran as an interactive gated session with a Windows guest (D 11:34; `c2/mac_host.log`); §7 says so | UC (Minor 3) |
| W10 | `send` answered `ok:true`, `sent_now:true`, exit 0, own text not PVM-L1 | RAN | `WO-7p2:53-55`; `c1/mac_read_1.json` | S |
| W11 | `inbox_read`: two messages, `"ack":2` | RAN | `WO-7p2:56-58` | S |
| W12 | `inbox_ack`: `"removed":2` | RAN | `WO-7p2:59-61` | S |
| W13 | `reply` with `re`: `ok:true`, `sent_now:true` | RAN | `WO-7p2:62-64` | S |
| W14 | the read showed the Mac's reply as `chat.msg` with `re` = the PC's request id | RAN | `WO-7p2:57` | S |
| W15 | §7 pvpaths/make-plugin cites | READ | opened (`pvpaths.py:24, 122-128, 141, 143`; `make-plugin.sh:20`) | S |
| W16 | two-file layout, no `hooks`; `plugin.json` copied; SHA-256 equals the template | RAN PC `3164374` | `WO-11:99-100`; I computed the template's SHA-256 = `27418b76…15b7` | S |
| W17 | manifest text says "goes through the CoAgent gate", untrue with no hooks | READ | `plugin.json:4` opened | S |
| W18 | `claude plugin validate`: exit 0, "passed with warnings" (no author; README, icon) | RAN PC | `WO-11:102-132` | S |
| W19 | `coagent-mcp.exe` by hand: `initialize`, `tools/list`, `no_session`, "no new peer messages", "daemon is not running" | RAN PC | `WO-11:82-89, 174-181` | S |
| W20 | the data folder in another letter case found the same daemon | RAN PC | `WO-11:91-98` | S |
| W21 | WO-12 run: exit 0 in 7.1 s; `ToolSearch` then `inbox_read` → `no_session` | RAN PC | `WO-12:15-16, 36-44`; tool calls are the agent's own text, not labelled | OC (Minor 4) |
| W22 | paired run: exit 0 in 136.1 s | RAN two machines | `WO-14_3:6-7, 39`; `WO-14_4:15, 163` | S |
| W23 | agent's own report: `ToolSearch` once, `send` twice, `wait` twice | self-report (labelled) | `WO-14_4:34-39, 98-99` | S |
| W24 | sent a `request` and a `reply` with `re`; received a `chat.msg` with `re` = its request id and a `request.new` | self-report (labelled) | `WO-14_4:26-32` | S |
| W25 | guest log "message 1 received (chat.msg)", "message 2 received (request.new)" | MEASURED | `WO-14_4:128, 130` | S |
| W26 | working folder empty after the run | MEASURED | `WO-14_4:142-151` | S |
| W27 | settings checksums identical before and after | MEASURED | `WO-14_4:139-141` vs `:50-51` | S |
| W28 | marker count 0 with a positive control | MEASURED | `WO-14_4:135-138` (the control finds the stop line, not a marker line) | S |
| W29 | stop lines "Ctrl-C received; stopping", "link closed: daemon stopping", "stopped" | MEASURED | `WO-14_4:132-134` | S |
| W30 | the program's exit code NOT recorded | NOT RECORDED | `WO-14_4:17, 152` | S |
| W31 | `3164374` builds on both machines | RAN | `WO-11:12`; RH 17-19; D 11:34 | S |
| W32 | the run used `claude -p`, the smallest current model, this plugin, the skip-permissions flag | RAN | `WO-13:11` (final `run-agent.cmd`), `WO-14_3:6` (model id, file run) | S |
| W33 | Mac: gated host (`--gate`), a separate relay, `--relay-url`/`--relay-pin`; started, invited, paired | RAN | `c2/mac_host.log:3-5`; sheet 25, 33; `c2/mac_relay.log:1-13` | S |
| W34 | interactive session with the kit's plugin read the request, sent a reply and a request, read the PC's reply; the owner answered the asks | RAN | D 11:34; `c2/mac_host.log:10-18`; `WO-14_4:88-89` | S |
| W35 | the host log shows 5 `gate: ask` lines | counted | my count 5 (lines 11, 12, 14, 15, 17) | S |
| W36 | the host log shows 2 `handed out 1 message(s)` lines | counted | my count 2 (lines 13, 18) | S |
| W37 | still NEVER RUN: allow-list form on the PC; that line anywhere; the gate on Windows | NEVER RUN | no source shows otherwise | S |
| W38 | "the Windows counterpart [of `nc -vz`] is UNVERIFIED" / "whether another Windows tool would serve: UNVERIFIED" | UNVERIFIED | none exists | S |
| W39 | the `PVM-L1` text stays NEVER RUN | NEVER RUN | the session sent `C2X-` texts | S |

**Totals: 85 tagged statements. SUPPORTED 80; OVER-CLAIMED 3 (D8, L11, W21); UNDER-CLAIMED 1 (W9); WRONG 1 (B9d).** (Rows: DAEMON 16, BACKLOG 13, `lan.md` 17, `windows.md` 39.)

Tags removed by the branch (the `-` lines): "NEVER RUN" on the §2 heading, on "A REAL line from the Mac", on the §5 heading; each has a result line (W1, W5, W10-W14). "REASONED from it" dropped from the quoting-form sentence in §5: the sentence is an instruction, and the added text says the report prints answers, not typed commands. No UNVERIFIED tag was removed without a source line.

## 5. Item 4.4 Safety of the wording (READ)

I read both "known limit" paragraphs and every BACKLOG entry as an attacker and as a first-time user.
- **Hand `send` paragraph:** it says plainly that any same-user process holding the socket can send with no ask, that it RAN on loopback only, and that the owner's Yes guards the agent's words only. It does not claim a fix. No sentence promises more than was shown.
- **Unread text at rest:** says the file holds unread text in clear until released and acknowledged and that the gate does not guard the file. No promise.
- **Nothing hidden that the sources show:** the rehearsal's other findings that touch safety (F2 hand reads refused, F4) are in; the witness-reuse limit just above (a same-user client can consume a live witness) is in the file already.
- **BACKLOG decisions:** the hand-`send`, lost-invitation and reconnect entries are questions (design round / diagnosis round); at-rest text is "the owner's call (no change proposed)". The empty-flags, make-plugin, `COMMANDS.txt` and `mkdir` entries state a fix's scope; the brief asked for exactly that (items 3, 5, 8). Nothing decides what the brief left open.
- Notes: see Note 1 and Note 2.

## 6. Item 4.5 Names scan (TESTED)

My script: `gate_session_findings_tests/names_scan.sh`. It scans all 184 added lines and the clarifications file, case-insensitive, in eight classes: person and client names; seat names and mail; home, volume and `/private/` paths; the PC's folders and drive letters; network addresses and interface names; mail addresses; sheet words; and **43 id prefixes** I extracted myself from the session logs, the PC mails and the rehearsal (every 32-64 hex run cut to 8, plus 8-hex after mailbox/session/channel/key id). I do not write any of them here.
- Result: **0 hits in every class, in the added lines and in the clarifications file.**
- Positive controls, one per class, each printed 1: a person name, a seat name, `/Volumes/x`, `/private/tmp`, a PC folder path, a drive-letter path, a private address, a second address form, a mail address, a sheet word, and one collected id prefix.
- Note: my first run of the script failed on this laptop's old shell (it printed all-zero controls); the controls caught it, I rewrote the script, and the run above is the second.
- No invitation line, no key id, no session id, no mailbox id. The only epoch number in the added lines is a relay timestamp in `lan.md`.

## 7. Item 4.6 The clarifications file (TESTED)

- `gate_session_findings_tests/clar_compare.py` extracts the owner's sentence from the coordinator's 10:25 record and from the file's one quote line, and compares as strings: **identical, 154 characters each, the two spaces after "development." present in both**, the sentence occurs once in the file. The only non-ASCII character in the file is the dash in the header lines, not in the quote.
- Card id `general-c2c-windows-agent-permission-mode-1123` and choice "c — Skip all prompts" match the 10:25 record. Date and time line (2026-11-23 10:24) matches the board message time in that record. Number C-1. Nothing is added inside the quote; the lines around it (header, the choice, "for the development test agent on his own PC") are the brief's own wording and sit outside the quote.
- The file is outside the repository (not in the diff): confirmed, the project's definition folder holds it and `DESIGN_POINTER.md` only.

## 8. Item 4.7 The builder's open points (READ)

- UNVERIFIED list (1-8): I **agree** with all eight. One note: item 4 (`set /p`) is backed by the same helper form printed in `WO-11:203`, though not by WO-7's own file, so it stays UNVERIFIED as the builder lists it.
- STOP Q1-Q4: ruled by the addendum; I agree the text now follows the rulings (Q2 → W1-W14, Q3 → L17, Q4 → B9).
- **STOP Q5 still open: for the coordinator.** The sign-in sentence belongs also in `preview/demo/one-mac.md` step 6 and `setup.sh`'s "## 5. Sessions" (not owned files). Not a blocker.

## 9. Findings

No Blocker. No Major.

**Minor 1: pointers to `lan.md` lines are stale in `windows.md`.** The branch added 6 lines at `lan.md` step 4 (and more at steps 6 and tier 2), which moved every later line. `windows.md` cites `lan.md` by line number 15 times; **12 of those 15 now point at different text** (for example `lan.md:61` "nc -vz" is now at line 67; `lan.md:67-70` "tier 1" now lands on "Reachability", "Daemon", "Join"; `lan.md:69` "reply is printed" is now line 78; `lan.md:62`, `:64`, `:65`, `:52-56`, `:46-48`, `:42`, `:33-48` also moved). Added or changed lines of the branch carry some of them: `windows.md:147` ("From `lan.md:67-70`", "`lan.md:68`") and `:162-163` ("`lan.md:69-70`", "`lan.md:69`"). The sentences stay true (the content exists in `lan.md`); the pointers lead a reader to the wrong lines. Fix in words: re-point each cite to the head's line, or cite by step name ("`lan.md` step 6, tier 1").

**Minor 2: a wrong negative claim in the BACKLOG entry on the first `chan.open` refusal.** Text: "the order across the two machines is not shown by any log read" (`BACKLOG.md`, "Why deferred"). The relay logs of both sessions show the connection order: first link `c1/mac_relay.log:38-45` (the PC's connection, then the Mac's channel creation, then the PC's second connection that attaches); second session `c2/mac_relay.log:26-31` (the Mac creates the channel, then the PC attaches). The reading is not conclusive (one-second timestamps), but the sentence is wrong as written. Fix in words: say the relay logs give an order by connection number (cite both ranges) and leave the question open, as the addendum asks.

**Minor 3: a NEVER RUN tag in `windows.md` §5 is stale after the second session.** Text: "(NEVER RUN with a Windows guest: on the first link the Mac host was driven by `ctl` instead)". In the second session the Mac host side ran as an interactive gated Claude Code session with a Windows guest (the document's own §7 says so). The tag under-claims and the two sections disagree. Fix in words: say the host side ran with a Windows guest on the second session (gated, with the PC's agent), and keep NEVER RUN only for a PC guest driven by `ctl` against that gated session, if that is what is meant.

**Minor 4: two PC-run statements give the agent's own account as a fact, without the "self-report" label that the same lane uses for WO-14.** `windows.md` §7 (WO-12 bullet) and `lan.md` tier 2 ("RAN on the owner's PC … the agent called `ToolSearch` and then `inbox_read`"). The only source for the tool calls is the agent's own text (`WO-12:11-13`). The answer text `no_session` and the exit 0 are measured. Fix in words: add "by the agent's own report" to the tool-call part, as in the WO-14 bullet.

**Minor 5: one ambiguous RAN tag in `docs/DAEMON.md` §4.** Text: "A test for 'both null' refuses every new invitation after an `end`, because `status` keeps the ended session and the finished pairing (RAN on Mac loopback, 2026-11-23)." What ran is the retention of the ended session and the finished pairing (RH 265, 286); no run showed a refused invite from a "both null" test (RH 443-446 says "would refuse"). Fix in words: put the RAN tag after the "because" clause only, and mark the refusal REASONED.

**Note 1 (wording; not a block):** the `--dangerously-skip-permissions` flag appears in `windows.md` §7 without the caution that `lan.md` carries ("allows EVERY tool with no prompt … development test agent on the owner's own PC only"). A first-time reader of `windows.md` alone could copy it. Add the same sentence or a pointer to `lan.md`.

**Note 2 (wording):** the new hand-`send` paragraph opens "The gate guards READS of peer text" and reports hand reads refused; the limit right above it (a same-user client can consume a live witness inside its time window) is what qualifies that. A one-clause cross-reference would keep a reader from taking "refused" as "always refused".

**Note 3 (for the coordinator; not this branch):** older text now reads behind the evidence: `docs/DAEMON.md` §6's list "a join through a relay hosted elsewhere: DONE … not another machine" and the NEVER RUN tags around Windows with an outside relay predate the first cross-machine link; they are true as history but a reader gets no pointer to `windows.md` §2, §5, §7. The addendum limited this lane to its closed list, so nothing was owed.

## 10. What was NOT checked

| Item | Why | Who could check |
|---|---|---|
| `cargo fmt --all --check` | optional by the brief; no `.rs` in the diff, so it cannot change | the builder's own run (exit 0) is on record; any seat |
| Whether the PC helper typed the quoting form of `windows.md` §4 for the WO-7 part 2 calls | the report prints answers, not command text | the PC helper (ask), or leave UNVERIFIED |
| `ended:false` printed on the first link | no source prints the answer | a one-line `end` run against a daemon with no session record (a later lane with a run) |
| The 2026-11-22 measurement of the 359-character line | I read the coordinator's 11-22 daily line and trust it as the source; I did not re-measure | any seat that can run `invite` on loopback |
| A spent line actually refused by a run | READ only; no run exists | a later lane with a run |
| That the owner pressed Yes on each ask | no source counts approvals (5 `gate: ask` lines; the owner's own report says "three" at one point) | the owner |
| Other at-rest files (e.g. `outbox.json`, logs) holding peer or own text | the rehearsal checked `inbox.json` only | a later seat with a file scan on a gated run |
| Content outside the four files (`one-mac.md`, `setup.sh`, the sheets) | not in the diff | the coordinator (STOP Q5) |
| The WO-14 PC mails' mid-run claims beyond the whole report | I read all four mails whole; I did not check the PC's own files | the PC helper |

## 11. Cleanup

My work dir is `/private/tmp/claude-501/qsf` (clone only, a remote `gh` added there). I started no process and left none running. Nothing outside my work dir was written except this verdict file, my status file in the project's history folder, and copies of my two scripts and my grep output in `gate_session_findings_tests/`. Nothing deleted.
