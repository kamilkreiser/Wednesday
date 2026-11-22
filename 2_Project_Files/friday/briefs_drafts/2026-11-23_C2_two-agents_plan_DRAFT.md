DRAFT, NOT ISSUED.

# CoAgent C2: an agent on each machine, talking (plan for a later session)

For Friday. Client: General. Project: CoAgent ("Claude to Claude"). Documents only: nothing was run in the project, launched, mailed, committed or pushed.

**Tags.** READ = read by SHA at main `3164374a8a20d73296558997438b97a41a7837ad` (path:line), or in Friday's clean clone at `3337192` for `preview/demo/{lan,one-mac}.md`, `setup.sh`, `make-plugin.sh`, `preview/plugin-template/**`, `preview/lib/pvpaths.py` (unchanged between the two SHAs: `git diff --stat 3337192 3164374` lists only `preview/demo/windows.md` under `preview/`, and nothing under `crates/coagent-mcp` or `crates/coagent-ipc`). FRIDAY = a fact Friday holds (her daily note 2026-11-23 09:55/09:56, the PC's WO results files). MEASURED = a read-only command run by this drafter on 2026-11-23. REASONED. UNVERIFIED.

## 1. C2 in its smallest honest form

| Machine | Programs | Flags / config |
|---|---|---|
| MAC (host) | relay `coagent relay` (the one listener, the owner's card of 20 Nov); host `coagentd`; Claude Code (interactive) with the full preview plugin (MCP + hook) IF gated (D-2 below) | relay: as C1 (FRIDAY, sheet 17:25). Host gated: `setup.sh`'s D-h line (READ setup.sh:50: `--gate --workspace ws-h --exclude '<ws>/secret/**' --gate-dir plugin-h --idle-exit-secs 86400`) plus `--relay-url/--relay-pin` (READ lan.md:44). Ungated: C1's Window 2 line as it ran. |
| PC (guest) | `coagentd.exe` (guest, as C1), `coagent-mcp.exe`, Claude Code 2.1.330 (FRIDAY, machine report f) | daemon: `--data-dir C:\wdc11\prof\g --idle-exit-secs 86400`, NO `--gate` (READ windows.md:53; lan.md:16 "daemon WITHOUT `--gate` (M1 mode)"); the guest needs no relay flags (READ windows.md:14-17) |

**The MCP-only plugin.** The template has three parts: `.claude-plugin/plugin.json` (name `coagent`), `.mcp.json.tmpl` (server `link` -> `@BIN@/coagent-mcp --data-dir @DATA@`, READ .mcp.json.tmpl:1-8) and `hooks/hooks.json.tmpl` (PreToolUse `*` and ConfigChange -> `coagent-hook`, `onFailure: block`, READ hooks.json.tmpl:4-28). `make-plugin.sh` is bash that runs `python3 -I preview/lib/pvpaths.py render` (READ make-plugin.sh:20); render substitutes the two placeholders and writes all four files (READ pvpaths.py:109-146). lan.md tier 2 then moves `hooks/` into a quarantine folder by hand (READ lan.md:71-72). Tool names: `mcp__plugin_coagent_link__send`, `__inbox_read`, `__wait` (READ plugin-template/README.md:29-31; confirmed live on the Mac on 2026-11-19, FRIDAY daily 11-19 22:16).

**What differs on Windows.** (a) `pvpaths.py` checks for `coagent-hook` and `coagent-mcp` WITHOUT `.exe` (READ pvpaths.py:122-125), so render refuses on Windows (REASONED). (b) It needs `python3`; the PC has Python 3.12.10 (FRIDAY, machine report e) but whether `python3` is that or the Store alias: UNVERIFIED. (c) Its socket-length check is the macOS 103-byte rule (READ pvpaths.py:24, 126-128), meaningless for a pipe. **So on Windows the helper writes the plugin by hand: `plugin.json` copied byte for byte, a `.mcp.json` with `C:\\c2c\\t11\\debug\\coagent-mcp.exe` and the data folder, and NO `hooks/` folder at all** (nothing to quarantine). The `.mcp.json` must spell the data folder exactly as the daemon was started: `coagent-mcp` takes the folder text and turns it into the pipe name (READ coagent-mcp/src/main.rs:463-479); it does not check `USERPROFILE`, so it can run with the helper's real profile while the daemon runs under the made-up one (REASONED from the same lines; WO-11 step 6 proves it). The manifest's description says "every tool call ... goes through the CoAgent gate" (READ plugin.json:4): wrong for the PC's copy; kept byte for byte so the name stays `coagent`; say so in the record.

## 2. What has NEVER run on Windows, and how WO-11 proves each piece alone

| Piece | Status | WO-11 proof (no owner, no model run) |
|---|---|---|
| `coagent-mcp.exe` built | RAN (WO-1 built it at `b8aa8b7`, FRIDAY WO-1 results:22) | rebuilt at `3164374`; its own tests (2 unit, main.rs:550-580; 2 in stdout_audit.rs:53-90) never run on Windows |
| `coagent-mcp.exe` -> named pipe -> live daemon | NEVER RUN | stdio JSON-RPC by hand from a file (WO-11 step 6), lines taken from the repo's tests: READ delta.rs:826, 834, 837; common/mod.rs:339 |
| a real Claude Code launching it from a plugin on Windows | NEVER RUN | only `claude plugin validate` (READ one-mac.md:22; no model run, REASONED); the live load needs a model run: card Q4 |
| the plugin layout on Windows | NEVER RUN | written by hand (WO-11 step 8) |
| a bash script on Windows | NEVER RUN, and NOT needed | left out (section 1); a finding for the project: `make-plugin.sh` does not know `.exe` |
| `claude -p` on Windows with `--plugin-dir` | NEVER RUN | `claude --help` text only (WO-11 step 4) |

Expected by hand on an UNPAIRED rehearsal daemon (all REASONED from source, never run): `initialize` answers `protocolVersion` "2025-06-18", `capabilities.tools`, `serverInfo.name` "coagent" (main.rs:399-417; version "0.0.1", root Cargo.toml:22); `tools/list` the three tools (main.rs:89-121); `tools/call inbox_read` and `send` -> `isError:true`, text `coagent: the daemon refused (no_session).` (main.rs:311; engine.rs:1674, 1824; ipc.rs:58); `wait` with `timeout_s` 1 -> `coagent: no new peer messages.`, `isError:false` (ungated `take_ticket` returns no ticket before any session check, engine.rs:1874-1876; empty timed-out page, engine.rs:2752; main.rs:196-197); daemon stopped -> `coagent: the CoAgent daemon is not running.` (main.rs:292). The notification gets no reply (main.rs:395-397); answers may come in any order (each line is its own task, main.rs:533-536); at end of input it finishes the open calls, then exits (main.rs:539-543).

## 3. The two agents and their exchange

- **PC agent:** one headless `claude -p` run, started by the PC's helper, cwd `C:\c2c\wo11\ws-g` (empty), plugin `C:\c2c\wo11\plugin-g`. Asked to: send kind `request` "C2W-1 request from the Windows agent: please reply"; call `wait` (timeout_s 300) until it has BOTH a reply whose `re` is its id AND a request from the peer; answer that request with kind `reply`, `re` = its id, "C2W-4 reply from the Windows agent"; print the ids and texts; use no other tool.
- **MAC agent:** one interactive Claude Code session in `ws-h` with `plugin-h` (READ setup.sh:64). Prompt M-1 (owner pastes): "Check your coagent inbox with the inbox_read tool. Then use the coagent send tool, kind reply, re set to that message's id, text exactly: C2W-2 reply from the Mac agent. Then use the coagent send tool, kind request, text exactly: C2W-3 request from the Mac agent: please reply." Prompt M-2: "Read your coagent inbox with inbox_read and show me what arrived."
- **Markers** `C2W-1` to `C2W-4` (C1 used `C2X-`; FRIDAY). Afterwards `grep -c 'C2W-'` on the relay log and both daemon logs must be 0 with a positive control (as C1; READ one-mac.md:43).
- **Model:** the smallest current model, read from the coordinator's `models_latest.json` (`0_Brain/dashboard/data/models_latest.json`, path MEASURED; never typed). **Runs:** PC 1 (a second only if the first times out), Mac 1 session with 2 prompts. **Accounts:** the PC's Claude Code is signed in by the owner: **the PC run is his spend.** The Mac session runs on the Mac's Claude Code sign-in (the one the 11-19 demo used, FRIDAY; which plan it bills: UNVERIFIED).

## 4. Headless or interactive

- **PC: headless.** lan.md tier 2 runs the guest with `claude -p` (READ lan.md:73) but passes no allow rule; "in `-p`, a call that would prompt is denied anyway" (READ spikes/G1-deny-blocks-write/RESULT.md:7). So as written lan.md:73 would have its `send` denied (REASONED: a finding for the project). The working form copies spike U4: `--permission-mode manual --allowedTools <the tool>` (READ spikes/U4-mcp-elicitation/run.sh:36; "`manual` = the CLI's name for default", G1 RESULT.md:6). Allow exactly the three coagent tools plus `ToolSearch` (one-mac.md:35: the deferred-tool loader "asks too"; REASONED harmless). Every other tool is denied, not asked: nobody answers anything on the PC. `--permission-mode` is passed explicitly because Claude Code 2.1.328 started in auto mode by default (FRIDAY daily 11-19 22:16 (d)) and because the helper's own settings may carry its skip-prompts choice (UNVERIFIED; WO-11 step 4 checks the flags). The list syntax of `--allowedTools` for several tools: UNVERIFIED (WO-11 step 4).
- **PC interactive instead** (card Q3 b): the owner types in a Command Prompt `claude --permission-mode manual --plugin-dir ...` and answers Claude Code's own prompt for each coagent call (about 4).
- **MAC: gated, interactive (recommended).** The owner's Q1 answer a reads "The Mac side stays gated. Claude Code's own prompts stay on" (READ plan 15:235, 98). What the gate adds on the day: every Mac tool call goes through the hook; `inbox_read` asks every time (READ REVIEW.md:117-118); `send` is a T3 ask showing the exact outgoing text (READ POLICY.md:245); the peer's text is released only to a witnessed call (DAEMON.md:798-829), so Friday's `ctl inbox_read` on the host gets `gate_missing` (engine.rs:87-88, 1821). What it costs: the session must be interactive (under `-p` every ask becomes a deny, READ lan.md:16); the owner presses Yes about 5 times; a stopped daemon blocks every call of that session (READ plugin README:12-15); the gated host with an OUTSIDE relay has never run (C1 was ungated, FRIDAY): Friday rehearses it on loopback first (section 5, F1). Ungated Mac = headless by Friday, fewer presses, but departs from his ruling's text: his card (Q2).

## 5. The session, step by step

Before (no owner): **F1 MAC (Friday):** new scratch build at `3164374` (`cargo build --locked --workspace --bins`; not the merge-check target dirs, whose last build state after the red-control runner is UNVERIFIED); `setup.sh /private/tmp/c2c-c2 "$BIN"` (refuses an existing root, READ setup.sh:26); a loopback rehearsal in ANOTHER root with relay on 127.0.0.1, gated host with `--relay-url`, ungated guest, invite into a private file, join, `status` (`gate` "on"/"off"), a `ctl send` from the guest, host `ctl inbox_read` -> `gate_missing`; `end` both; no model run. **F2 PC (helper):** WO-11 done and mailed. **F3 MAC:** re-read `ipconfig getifaddr en0`, firewall state, stick mount name; settings checksums before (READ lan.md:59-60).

| # | Machine: who | Does | Sees | STOP if |
|---|---|---|---|---|
| 1 | MAC: owner | Window 1, the relay block of C1 with `R=/private/tmp/c2c-c2`, output to `$R/r.log` with NO `tee` (C1 finding: tee loses the stop lines) | an empty window; Friday posts the `url:` line on the board | address error: Friday re-reads en0, new block |
| 2 | MAC: owner | Window 2, the gated host line (section 1) | nothing; Friday reads `h.log` "started" and `status` `gate:"on"` | any error line in h.log |
| 3 | PC: owner | W1, three lines as C1 with `C:\wdc11` (WO-11 step 9 prints them) | the window sits; helper reads `g.log` | the window returns to its prompt |
| 4 | PC: helper | `Test-NetConnection <addr> -Port 7443`; `status.cmd` | True; `"ok":true`, `session:null` | False, or anything but ok |
| 5 | MAC: Friday | ONE command: `status` (pairing null, session null) AND stick mounted, then invite -> file on the stick, compare, never print | "line written" | a waiting pairing: `end` first (answers `ended:false`, clears it; engine.rs:2016-2026); stick missing: stop, ask |
| 6 | PC: owner | `C:\c2c\wo11\join.cmd X:\c2c-line.txt` (X from the helper's Get-Volume) | `"paired":true` | `invite_refused`: Friday `end` + step 5 again |
| 7 | PC + MAC: helper / Friday | `status` both until `connected:true` (60 s) | connected | not within 60 s: both lines whole, stop |
| 8 | MAC: owner | Window 3: `cd /private/tmp/c2c-c2/ws-h && claude --model <from models_latest> --plugin-dir /private/tmp/c2c-c2/plugin-h`; accept folder trust; `/mcp` shows `link` | the session | `/mcp` without link: stop |
| 9 | PC: helper | `run-agent.cmd <model>` (WO-11 step 9 wrote it), output to a log | (in the log) the C2W-1 send | `send` denied or the server not loaded: stop, log whole |
| 10 | MAC: owner | paste M-1; Yes to the `inbox_read` ask, the two `send` asks | the C2W-1 text inside "COAGENT PEER DATA - UNTRUSTED" (READ main.rs:264-269) | the model refuses: the owner types the two sends himself (one-mac.md:55-57) |
| 11 | PC: helper | waits for the run to end; mails the log's last lines | C2W-2 and C2W-3 received, C2W-4 sent | run ends without both: one more run (card Q1 counts it) |
| 12 | MAC: owner | paste M-2; Yes | C2W-4 shown | — |
| 13 | PC + MAC: owner | PC W1 Ctrl-C ONCE; MAC Window 3 quit (Ctrl-C twice, one-mac.md:62), Window 2 Ctrl-C, Window 1 Ctrl-C | stop lines | no "stopped": record |
| 14 | MAC: Friday; PC: helper | `C2W-` counts 0 + control; settings checksums after, diff empty (lan.md:75, 82); relay times; `lsof` no listener | — | any marker hit: record as a finding |

**Owner's time:** about 35 minutes (REASONED: C1 took 09:34 to 09:55, FRIDAY; C2 adds steps 8-12). **Friday does herself:** builds, setup, every read, the invitation (step 5), every count; the owner only pastes, presses Yes, carries the stick and presses Ctrl-C.

## 6. The owner's decisions (card drafts)

**Q1. Model runs on your PC account.** BLUF: the Windows agent is Claude Code signed in as you; each run is your spend. a) yes, one run on the smallest model, a second only if the first times out; b) no: the PC stays `ctl`-only (= C1 again). Recommend a. Default: b.
**Q2. The Mac side gated or not.** BLUF: your 20 Nov answer said the Mac stays gated; that means about 5 Yes presses at the Mac and one more never-run combination (gate + outside relay), rehearsed by Friday first. a) gated, interactive, you press Yes; b) ungated, headless, Friday runs it, no presses. Recommend a. Default: a (your ruled text).
**Q3. How the Windows agent asks permission.** BLUF: the PC helper skips prompts by your standing choice; this is a different agent and that choice is not assumed. a) headless, only the three CoAgent tools allowed, everything else refused, nobody asked; b) interactive, Claude Code's own prompts on, you press Yes at the PC; c) the helper's skip-permissions flag (every tool allowed while it reads another machine's text). Recommend a (narrowest; but your 20 Nov text said "Claude Code's own prompts stay on": a refuses instead of asking). Default: b.
**Q4. One rehearsal model run on the PC before the day.** BLUF: the only way to see Claude Code load `coagent-mcp.exe` from the plugin without you there. a) yes, one headless run against the unpaired rehearsal daemon (it should get "no_session"); b) no, first seen on the day. Recommend a. Default: b.
**Q5. When.** BLUF: about 35 minutes at both machines, after WO-11 and Friday's F1. a) next morning you name; b) Friday proposes a slot on the board. Default: b.

## 7. What could go wrong

| Fault | Sign | Fallback |
|---|---|---|
| Plugin not loaded on the PC | no `mcp__plugin_coagent_link__send` call in the log | run with `--mcp-config C:\c2c\wo11\plugin-g\.mcp.json` instead (tool names then differ: allow `mcp__link__*`, REASONED) |
| `-p` denies the call | log: permission denied for the tool | fix the allow list spelling from `claude --help`; no skip flag without Q3 c |
| Data folder spelled differently in `.mcp.json` | `coagent: the CoAgent daemon is not running.` | copy the exact text the daemon was started with (WO-11 step 7 shows what a case change does) |
| Gated Mac blocks everything | every call blocked | daemon not running or idle-exited: `status`; restart Window 2 (one-mac.md:58-59) |
| A waiting invitation refuses a new one | `session_active` | `end` (step 5) |
| The 600 s expire | `invite_refused` | `end`, new invite |
| The small model will not act on peer text | it refuses or asks | the owner types the sends (one-mac.md:55-57) |
| `wait` returns empty | "no new peer messages" | the agent calls it again (prompt says so); the run's own limit: UNVERIFIED |
| Step not labelled with its machine | the owner acts on the wrong one (C1 slip 1, FRIDAY) | every sheet line starts MAC: or PC: |

## 8. Not in C2

The hook and the gate on Windows (C3; W1 never run, plan 15:92, 219). Hosting from Windows (the daemon refuses, windows.md:25-27). Anything beyond the owner's two machines. `make-plugin.sh`/`setup.sh` on Windows. Session binding (`/collaborate`).

## NOTES FOR FRIDAY

- U1 `claude plugin validate`, `--allowedTools` list syntax and `--permission-mode manual` on 2.1.330: close by WO-11 step 4 output.
- U2 the Store-alias risk of `python3` on the PC: guessed; never invoked by WO-11.
- U3 gated host + outside relay: never run; close by F1.
- U4 which plan the Mac sign-in bills: ask or read the Mac's account state.
- U5 whether a case-changed data folder reaches the same pipe: WO-11 step 7 records it; I did not read `endpoint.rs` at this SHA.
- U6 the run time of one `-p` run with several 300 s waits: guessed sufficient.
- Guesses: 35 owner minutes; "about 5" Yes presses (3 in M-1, 1 in M-2, plus any ToolSearch ask); `ToolSearch` in the allow list being harmless; the `--mcp-config` tool prefix.
- lan.md:73 (no allow rule under `-p`) and `make-plugin.sh` without `.exe` are project findings, to go with the three C1 findings in one brief.
- The folder names (`C:\wdc11`, `C:\c2c\wo11`, `/private/tmp/c2c-c2`) are new; run the folder guard on WO-11 before sending. WO-11's DO NOT TOUCH line puts f1-f3 and tf1-tf3 under `C:\c2c\` and wf1-wf3, qf1-qf3 under `C:\` (tf3, wf3, qf3 READ in WO-10 results:21, 60, 153; the others guessed by pattern); its step 0 refuses any WHERE folder that already exists, which covers a wrong guess.
- WO-11 sends `C2W-0` through `send` to an unpaired daemon: it is refused, nothing is queued (REASONED, engine.rs:1673-1675).
