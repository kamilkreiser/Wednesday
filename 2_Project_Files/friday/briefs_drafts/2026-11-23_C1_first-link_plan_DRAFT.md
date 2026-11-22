DRAFT, NOT ISSUED.

# CoAgent C1 (and C2 if time): the first link across machines, Mon 2026-11-23

For Friday. Client: General. Project: CoAgent ("Claude to Claude"). Documents only: nothing was run in the project, nothing launched, mailed, committed or pushed.

**Tags.** READ = read at branch head `3337192` (`33371921670acfcb6fc7634d0c4eacafa9800a8d`, "W-DAEMON notes round"), path:line; files outside the repo are named in full. MEASURED = a read-only command run on this Mac on 2026-11-22 20:06 AEDT. REASONED = my inference. UNVERIFIED = not established.

**Authority.** The owner, 2026-11-20: card `general-c2c-win-mac-relay-home-network-1120` = "Yes, for each Windows test session" (plan 15 Q5 option a: opened for the session, stopped when it ends, times recorded; READ `15_windows-plan-2026-11-20.md:268-274`), and `general-c2c-win-first-link-ungated-1120` = a (READ plan 15:232-239). lan.md's own authority line names the 2026-11-19 sentence "only for this test" (READ `preview/demo/lan.md:3-6`); for this session the 11-20 card is the authority and Friday records it in the session notes before the relay starts.

---

## 0. The shape in one paragraph

The Mac runs two long-lived programs: an outside relay (`coagent relay`) listening on the Mac's home-network address, and a host daemon (`coagentd`) that uses that relay. The host makes an invitation. The PC runs `coagentd.exe` as the guest and joins with the invitation's line; it only dials out (READ plan 15:94; DAEMON.md:633-638). "Connected" means `status` on BOTH sides shows `session.connected: true` (READ `docs/DAEMON.md:170`; `lan.md:65`). No Claude Code on either side in C1. No gate on either side (REASONED: no agent runs on the Mac either, so the Mac's gate has nothing to judge; see 8, decision D1).

## 1. The network facts

| Fact | Value | Tag |
|---|---|---|
| Mac address | `en0` = `192.168.7.98`, mask `255.255.252.0`, router `192.168.4.1` (network `192.168.4.0/22`) | MEASURED (`ipconfig getifaddr en0`, `getoption en0 subnet_mask`, `router`). DHCP can change it overnight: re-read at T-15. |
| Mac firewall | "Firewall is disabled. (State = 0)", stealth off, block-all off | MEASURED (`socketfilterfw --getglobalstate`, `--getstealthmode`, `--getblockall`; lan.md:35-37 names the first) |
| PC addresses | Ethernet `192.168.1.12`, Wi-Fi `192.168.4.23`, both category Public | READ machine report lines 61-62 |
| Route PC to Mac | The PC's Wi-Fi `192.168.4.23` is inside the Mac's `192.168.4.0/22` IF the PC's Wi-Fi mask is also /22 (same router). The Ethernet `192.168.1.12` is a different network. Which interface Windows uses for `192.168.7.98` is not known; the machine report has no masks or routes. | REASONED; UNVERIFIED (U1) |
| Windows firewall | The guest only connects OUT; no listening port, so no inbound rule and no prompt expected; the Public profile matters only for inbound | REASONED (plan 15:94; machine report line 13 warns about inbound only). Outbound default-allow on this PC: UNVERIFIED |
| Mac firewall prompt | Off tonight, so no prompt is expected. If the owner has switched it on, macOS may ask whether `coagent` may accept incoming connections: the answer is **Allow**, for this session, under his card; record the time. A newer macOS "local network" privacy prompt for Terminal is possible: UNVERIFIED; answer Allow the same way. If it is on and nothing is asked, it may drop silently (lan.md:36-37): the PC's reachability check (step P4) settles it. | MEASURED + REASONED |
| The URL form | An IP-address URL works because the client checks the certificate PIN, not the host name | READ lan.md:23 |

## 2. Who runs the Mac side: recommendation

**Recommended: the owner types the Mac's three commands (relay, host daemon, invite) into Terminal from a sheet Friday gives him; Friday runs only the Mac-side `ctl` reads and message commands (status, inbox_read, inbox_ack, send) against the host's data folder in `/private/tmp`.**

Why:
1. The relay is the ONLY thing that listens beyond loopback (READ lan.md:4). The owner ruled it; he starts it and stops it (Ctrl-C) with his own hands, and the times are his to see.
2. Any firewall or privacy dialog appears on the Mac's screen for his Terminal; he answers it there (REASONED).
3. The invitation line holds the link secret (single use, 600 s; READ lan.md:46-48, one-mac.md:32). Printed in his Terminal it never enters Friday's stored transcript or any mail (lan.md:47-48: "the owner's hands, or a channel that is not stored").
4. Friday runs nothing long-lived and edits no project file: the binaries come from Friday's scratch build and the data lives in `/private/tmp/c2c-c1` (lan.md:33: "paths in your own scratch root, never under the project").

Rejected: (b) a short-lived seat: adds an agent, model spend and background processes for three commands; no gain. (c) Friday runs everything in the background: the secret lands in her transcript and a dialog may sit unanswered on a screen nobody watches.

## 3. The Mac side (host), exact

`BIN` = `target/debug` of Friday's scratch clone of MERGED main, built with `cargo build --locked -p coagent-daemon --bins` and `cargo build --locked -p coagent-cli --bin coagent` (the same two builds the PC ran; READ WO-4 results). Whether such a build exists tonight: UNVERIFIED (U4). Root: `/private/tmp/c2c-c1` (short: `.../h/ipc/daemon.sock` is 34 bytes, under the 103 limit of one-mac.md:15-16).

| # | Command (owner, Terminal) | Expect | Tag |
|---|---|---|---|
| M1 | `mkdir -m 700 /private/tmp/c2c-c1` | — | REASONED (the daemon makes one level only: DAEMON.md:55-56) |
| M2 | Terminal R: `"$BIN/coagent" relay --listen 192.168.7.98:7443 --allow-non-loopback --status-secs 60 --identity-file /private/tmp/c2c-c1/relay.id` | prints `coagent relay: HOSTING A RELAY on 192.168.7.98:7443 (NOT loopback: other machines can connect)`, `url: wss://192.168.7.98:7443/v1`, `fingerprint: <hex>`, a WARNING block, then a reminder line every 60 s. **Record the time.** | READ lan.md:24-29, 42; `crates/coagent-cli/src/relay_cmd.rs:24, 31-34, 40-57`; args.rs:9-12. The `/v1` suffix: READ lan.md:24 |
| M3 | Terminal D-h: `"$BIN/coagentd" --data-dir /private/tmp/c2c-c1/h --relay-url <url from M2> --relay-pin <fingerprint from M2> --idle-exit-secs 86400 2> /private/tmp/c2c-c1/h.log` | keeps running. No `--gate` (D1). `--idle-exit-secs` because the default 600 s exits an idle daemon | READ lan.md:44; main.rs:24, 165-181 (the two flags go together; `sha256:` and colons are stripped); DAEMON.md:25-26 |
| M4 | (after the PC passes P5) `"$BIN/coagentd" ctl --data-dir /private/tmp/c2c-c1/h '{"v":1,"id":1,"cmd":"invite"}'` | one JSON line; `result.line` is `coagent join <blob>`; `expires_in_s` | READ lan.md:45; DAEMON.md:171; invite.rs:150-151 |
| M5 | Friday: `"$BIN/coagentd" ctl --data-dir /private/tmp/c2c-c1/h '{"v":1,"id":2,"cmd":"status"}'` | after the join: `session.connected: true`. **This is "the Mac shows connected".** | READ DAEMON.md:170; one-mac.md:33 ("may take ~15 s") |

The host daemon starts no relay child, so it needs no `--coagent` (REASONED from DAEMON.md:212 "start the relay child if needed (or use --relay-url/--relay-pin)").

**How the line crosses** (decision D2, Friday's). The blob is base64url of a JSON object with the relay URL, a 64-hex pin, a 32-hex mailbox id and the secret (READ invite.rs:2-3, 106-124), so the line is roughly 250-300 characters (REASONED estimate, not measured). Options: (a) a text file on a USB stick the owner carries, then he deletes it himself; (b) he retypes it from the Mac screen into the PC's join window (error-prone; a typo costs a re-invite, nothing worse). Never mail, never the seat's prompt. Recommend (a), (b) as fallback. A dry run of M2-M4 on loopback tonight would measure the real length.

## 4. The PC side (guest), exact

Built on the PC from a bundle of merged main (WO-7 step 1-3; LF clone, target `C:\c2c\t7`, because long paths are off: machine report line 67). Only `coagentd.exe` is needed: the guest runs no relay (READ DAEMON.md:633).

**Data folder: a made-up profile, `C:\wdc7\prof\g`, with `set USERPROFILE=C:\wdc7\prof` in the daemon's window only, as WO-6 did.** Why: it is the exact form that ran at `5b008c8` (READ WO-6 results part 2; DAEMON.md:675-681); everything sits in one test folder outside the owner's real profile, which the "delete nothing" rule makes easier to leave in place; the daemon refuses a folder outside `USERPROFILE` and trusts `USERPROFILE` as it finds it (READ DAEMON.md:532-535, 560-563), which on the owner's own machine is the ruled posture (card `general-c2c-win-data-folder-1120` a; DAEMON.md:521-523). The alternative `%USERPROFILE%\c2c7\g` works the same (REASONED) and writes into his real profile. The `ctl` windows do NOT need `USERPROFILE` set: `ctl` only names the pipe from the folder text (READ main.rs:237-241; `crates/coagent-ipc/src/endpoint.rs:139-146`).

**Quoting.** On the Mac single quotes keep the JSON whole; in Command Prompt they do not. Every PC `ctl` call goes through small `.cmd` files the seat writes (WO-7), using `"{\"v\":1,...}"`, which the Rust program reads back as one argument (REASONED from the Microsoft C argument rules; UNVERIFIED on this PC, U3). `status` is run FIRST, so a quoting fault shows before the secret is spent (`ctl` with a wrong argument count prints the usage, READ main.rs:230-235).

| # | Who / where | Command | Expect | Tag |
|---|---|---|---|---|
| P1 | owner, new Command Prompt (window W1) | `mkdir C:\wdc7\prof` then `set USERPROFILE=C:\wdc7\prof` then `C:\c2c\t7\debug\coagentd.exe --data-dir C:\wdc7\prof\g --idle-exit-secs 86400 2> C:\wdc7\g.log` | keeps running | READ lan.md:62; WO-6 step 4a |
| P2 | seat | `type C:\wdc7\g.log` | the notice "Windows: the data folder is inside your user profile folder (USERPROFILE), and that is the only check…", "created a new device identity …", "started: key id …, IPC socket ready" | READ DAEMON.md:525-527; WO-6 part 2 logs |
| P3 | seat | `Get-NetIPConfiguration` and `Find-NetRoute -RemoteIPAddress 192.168.7.98` (read-only) | which interface and source address reach the Mac | UNVERIFIED that these read-only cmdlets run without elevation here (general knowledge) |
| P4 | seat | `Test-NetConnection 192.168.7.98 -Port 7443` | `TcpTestSucceeded : True` | the Windows counterpart of lan.md:61 `nc -vz`; general knowledge, UNVERIFIED here |
| P5 | seat | `cmd /c C:\c2c\wo7\status.cmd` | `"ok":true`, `data_dir_check` present, `session` empty | READ DAEMON.md:170, 527-528 |
| P6 | owner, new Command Prompt (window W2) | `C:\c2c\wo7\join.cmd`, paste or type the line at its prompt | `"ok":true`, `paired`, `peer_key_id`, `session_id` | READ DAEMON.md:172; lan.md:64. Line or bare blob both accepted: invite.rs:154-164 |
| P7 | seat | `status.cmd` every 5 s, up to 60 s | `session.connected: true` | READ lan.md:65; one-mac.md:33, 60 |
| stop | owner, W1 | **Ctrl-C ONCE** (the C key, not Break) | "Ctrl-C received; stopping", then "stopped" | READ DAEMON.md:603-617 (a second Ctrl-C ends it mid-shutdown; closing the window is the crash path) |

## 5. The session, minute by minute (owner about 30 min)

Before the owner sits down (no owner time): PC seat has done WO-7 part 1 (bundle, clone, build, the three `win_` test targets, helper files) and mailed it; Friday has built `BIN` and re-read the Mac's address and firewall state.

| Min | Where | Owner does | Owner sees | STOP if / record |
|---|---|---|---|---|
| 0 | Mac | M1, M2 | the HOSTING banner, `url:`, `fingerprint:` | STOP if "cannot bind"/address error: the Mac's address changed; re-read `ipconfig getifaddr en0` and retry with it. Record the time listening began. Any dialog: Allow (his card), record the exact text |
| 3 | Mac | M3 | nothing (it runs); Friday checks `h.log` shows "started" and M5 answers `ok` | STOP on any error line in `h.log`; record it |
| 5 | PC | P1 | the window sits | STOP if it returns at once: the seat reads `g.log` (folder refused, notice missing); record exact text |
| 7 | PC | nothing (seat: P2-P5) | — | STOP at P4 False (no route or a block: section 7 rows 1 and 3). STOP at P5 if the usage text or "cannot connect" (quoting, or P1 not running) |
| 12 | Mac | M4; carries the line (D2) | one JSON line with `line` | the 600 s clock starts; record the time |
| 15 | PC | P6 | `paired` | `invite not readable` / `invite_refused`: a typo or expiry; go back to M4 (an invite is single use; one-mac.md:60-61). Record each try |
| 17 | both | nothing (seat P7; Friday M5) | — | not `connected` within 60 s: record both `status` lines whole; STOP |
| 18 | — | **C1 done.** Friday records the sheet (section 9) | | |
| 18-27 | both | C2, section 6 | | |
| 27 | PC, Mac | Ctrl-C once in W1; Ctrl-C in D-h; Ctrl-C in R | stop lines; relay gone | **Record the time the relay stopped listening.** (lan.md:81) |

## 6. C2 if time: a request and a reply each way, with `ctl` only

This is a `ctl` version of the plan's C2. The plan's C2 proper adds a Claude Code session with the message tools on Windows (READ plan 15:91); that is NOT in tomorrow's 30 minutes unless Friday adds it (Q1 = a allows it ungated). Every text carries the marker `C2X-` so the logs can be searched for it afterwards.

| # | Side | Command | Expect | Tag |
|---|---|---|---|---|
| C2-1 | PC (seat) | `send-request.cmd` (kind `request`, text `C2X-1 request from Windows: please reply`) | `id`, `seq`, `sent_now` | READ DAEMON.md:173; lan.md:67 |
| C2-2 | Mac (Friday) | `ctl … '{"v":1,"id":3,"cmd":"inbox_read"}'` | `messages[0].text` = the C2X-1 text, its `id`, `ack` (ungated: the text is printed) | READ DAEMON.md:174; lan.md:69 |
| C2-3 | Mac | `… '{"v":1,"id":4,"cmd":"inbox_ack","args":{"upto":<ack>}}'` | `removed` | READ DAEMON.md:175; lan.md:70 |
| C2-4 | Mac | `… '{"v":1,"id":5,"cmd":"send","args":{"kind":"reply","re":"<id from C2-2>","text":"C2X-2 reply from the Mac"}}'` | `id`, `seq` | READ DAEMON.md:173. Whether `re` is required for a reply: UNVERIFIED; it is given |
| C2-5 | PC | `read.cmd`, then `ack.cmd <ack>` | the C2X-2 text; `removed` | as above |
| C2-6 | Mac | `… send` kind `request`, text `C2X-3 request from the Mac: please reply` | `id` | |
| C2-7 | PC | `read.cmd`, `ack.cmd <ack>`, `reply.cmd <id>` (text `C2X-4 reply from Windows`) | | |
| C2-8 | Mac | `inbox_read`, `inbox_ack` | the C2X-4 text | |
| C2-9 | both | Mac: `grep -c 'C2X-' /private/tmp/c2c-c1/h.log` and the relay terminal's text; PC: `findstr /c:"C2X-" C:\wdc7\g.log` | 0 everywhere (the ciphertext claim, as one-mac.md:43) | READ one-mac.md:43 |

**Success:** four `C2X-` texts each read on the far side, both inboxes acknowledged, zero `C2X-` in any log or relay output.

## 7. What could go wrong, and the fallback

| Fault | Sign | Fallback |
|---|---|---|
| No route between the machines | P4 False; P3 shows the Ethernet `192.168.1.x` interface chosen | The owner's choice at the screen: unplug the PC's Ethernet for the session so Wi-Fi carries it, or put the Mac on the PC's other network. A Wi-Fi that isolates its clients: UNVERIFIED; then no fix tonight. Record P3 whole |
| The Mac's address changed | M2 refuses the address | re-read, restart M2 with the new address; M3 with the new `url:`; tell the seat the new address (not secret: mail is fine) |
| The host line wrong (typo, cut, expired, used) | `invite not readable` or `invite_refused` (fixed texts that never echo the input: invite.rs:69, 82-90; DAEMON.md:198-199, 217-218) | M4 again, a fresh line |
| A firewall block | P4 False with a good route; or a dialog | Mac: if the firewall is on, the owner allows `coagent` for this session or switches it off and back on after (his act); record. Windows: a prompt is not expected (outbound only); if one appears the seat does not answer it; the owner decides, recommended Cancel (the guest needs no inbound). A third-party security suite: UNVERIFIED |
| The daemon refuses the folder | P1 exits; `g.log` has the refusal text | `USERPROFILE` not set in W1 (cmd `set`, not PowerShell), a typo, or a relative path (DAEMON.md:532-535). Fix and rerun the same line. A pipe-name refusal: shorten the folder (DAEMON.md:598-599) |
| Quoting | P5 prints the usage or a `malformed`/`bad_args` error | the seat records the exact `.cmd` text and output; tries the pwsh 7.6 single-quote form from WO-7; the secret is not spent yet |
| Stale `preview/demo/windows.md` | — | WO-7 does not use it. Stale at `3337192`: lines 3-5 say `coagentd.exe` is not built (it was, WO-4 onward; DAEMON.md:650-651); lines 26-36 copy `.exe` files from the Mac kit (tomorrow builds on the PC); line 33-36 `--coagent` hint (not needed by a guest); lines 73-98 use single quotes, which Command Prompt does not honour (REASONED). Correct still: lines 16-19 (guest needs no relay flags), 69-70 (line not by email). A doc fix is the project's, after the session |
| A second Ctrl-C or a closed window | no "stopped" line | the crash path the recovery rules cover (DAEMON.md:610-617); record; use a fresh folder for any rerun |
| Host restart mid-session | guest loses the session | `--identity-file` keeps the relay's pin across a relay restart (lan.md:28-29); a restarted `coagentd` host needs a new line (main.rs:29-33) |

## 8. Decisions Friday makes before the session

- **D1.** Host ungated (this plan) vs the full lan.md tier 1 (host with `--gate`, `setup.sh` tree, and the host's Claude Code steps 6 and 8 of one-mac.md: model runs; READ lan.md:15, 38-44, 68). Recommend ungated for tomorrow: the 30 minutes prove the link, and nothing on the Mac acts without an agent.
- **D2.** How the line crosses (section 3).
- **D3.** Whether the owner's machines are in one room (the 600 s clock between M4 and P6). UNVERIFIED.

## 9. What the owner must do, and how long

1. At the Mac (about 5 min): type M1, M2, M3 from Friday's sheet; answer any dialog with Allow; later M4 and carry the line (2 min).
2. At the PC (about 5 min): open Command Prompt, type the three P1 lines; later run `join.cmd` and paste the line.
3. Wait while the seats check (about 10 min across C1 and C2).
4. At the end (2 min): Ctrl-C once in each of the three windows (PC W1, Mac D-h, Mac R).

Total about 30 minutes for C1 and C2 together; C1 alone about 18.

Record sheet (Friday fills): tier reached · Mac address and firewall state at T-0 · relay listening from/to · P3, P4 results · P1 notice line · join tries · minutes to `connected` · C2 four texts and C2-9 counts · any dialog text and the owner's answer · Windows-side stop lines.
