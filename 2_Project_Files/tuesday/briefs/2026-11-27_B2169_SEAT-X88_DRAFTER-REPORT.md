STARTABLE: YES (once X85 is READY: the kit refuses at Step 0 until then; X85 had not run at drafting)

# B2169 lane T, seat X88: drafter report (in-session read-only drafter, Opus, for Tuesday s334)

Clocks by `date`: first `Fri 27 Nov 2026 18:26:34 AEDT`; tools sha 18:34:24; sidecar written by `fill.py` (its first line); stamp_check 18:39:22 rc 0. Kit: `tuesday/briefs/2026-11-27_B2169_SEAT-X88_oxpd2-s14b-forwarder-test.md` (+ `.measured`, 82 claims, 82 measured). Scratch `<d>` = `fleet/state/s334/d2169-T/` (`seat-tools/`, `test/`, `gen/`, `_quarantine/`).

## BLUF
1. **The test is buildable at A$0 with no install and no lab change.** The lab already takes `--soap-port` (read, write, echo) and `--tree-port` (read only) and accepts `127.0.0.1` as a host, so a Python forwarder in the seat's own `gate/` sits between the lab and the M577 with the SOAP port kept at 7627 (no port remap, the HP constraint C2:154). The callback crosses it by telling the printer `http://<mac>:18632/...` while the lab listens on `127.0.0.1:18632` (`--callback-bind`, `Oxpd1EchoVerb.cs:253`).
2. **One finding of my own: macOS refuses a non-root bind of `127.0.0.1:443` (errno 13, MEASURED, `<d>/test/harness-run1.out`).** So the tree port goes through `127.0.0.1:10443` and `oxpd1 read --tree-port 10443`. Write and echo never fetch the tree (`Oxpd1Command.cs:358` is the only `GetDiscoveryTreeAsync` call), so only read needs it.
3. **What it settles and what it cannot (in the kit's scope line 2):** it settles whether the M577 answers OXPd 1.x SOAP (an admin read, the Test service write and undo, the guest echo) when a forwarder opens the stream and the URL/`To` host is `127.0.0.1`; whether TLS stays end to end (the pins through the forwarder must equal the direct pins); and whether the callback works through a forwarder. It cannot test a printer-side caller address other than this Mac's: en0 is the Mac's only LAN address (MEASURED), so the printer sees 192.168.20.220 both ways. That matches design 2A, where the printer sees only the connector's address. It also cannot test TLS on the callback (the listener is plain HTTP, `README.md:331`), or the product's URL host (the lab has `UseProxy = false`, `DeviceChannel.cs:54`). **A REFUSED therefore does not separate the two causes** (Q5).
4. **The order is after X85.** X85's E02 is the route test (owed 118), and a forwarded callback cannot be read while the route is unknown. X88 keeps a direct control beside each forwarded request, so it stands alone once it runs.
5. **The forwarder `fwd.py` (sha `5e534e0e...52f0`)** has a closed list of three pairs, never reads or logs payload, logs one line of counts per connection, caps at 32 connections, idles out at 120 s and has a lifetime bound. On loopback it passed 21 of 21 synthetic cases (`<d>/test/harness-run5.out`). It has never run against the printer or on the LAN address.

## Facts re-measured (instrument, clock)
- Origin `main` = `760e1a644ce9a419cf1b9132d0776e9e5eac1cac`, open PRs 0, private `true` (`gh api -X GET`, project GH_CONFIG_DIR, 18:27:37 / 18:34:04). BASE tree read from X85's drafter tarball `fleet/state/s334/d2159-L9/src_760e` (the same sha).
- X85 not run: no `2026-11-27_B2159_SEAT-X85_STATUS.md` in OXPd Briefs and no `.tools/b2159-x85` (`ls`, 18:27:23); its kit's Stamp slots unfilled. `.tools/b2169-x88` absent.
- **Seat X88 free (program check):** 0 of 80 non-`.pre-` SEAT kits of 11-26/11-27 name `X88` or ports 18630 to 18639 (word-bounded grep; control `18627` hit X85's kit and report = 2); `ls briefs | grep -c -i X88` = 0 before my write; tmux shows 3 panes, 0 named Datasec (no OXPd pane live).
- Ports: no listener on 443, 7627 (18:29:39), 10443, 7627, 18630 to 18639 (18:38:01) (`lsof -sTCP:LISTEN`). Lab tests bind port 0 only (`grep` over BASE tests: the `7627` hits are URI strings).
- This Mac: en0 192.168.20.220 (the only LAN inet, `ifconfig`); route gateway 192.168.20.1 en0; the firewall disabled; dotnet 10.0.404; load 5.37 19.97 18.20; **the wave lock folder EXISTS** (`ls -d`, 18:34:04): the build may wait.
- Tools: the four X85 tools copied byte for byte (`cp -c`; sha equal to `d2159-L9/seat-tools/`, heavy.py canonical `31adedc8...`).
- Prior work: STATUS files with `fwd.py|forwarder` 0 of 118, with `--tree-port` 0 (control `EnableTestService --execute` 2). B2068 STATUS holds the pin on 3 lines.
- Lab source pointers, every one by `grep -n` (`<d>/gen/facts.out`): DeviceChannel.cs:54; Oxpd1Client.cs:69, :78, :86 (the URL is the envelope `To`); Oxpd1Command.cs:20, :309, :358, :399; Oxpd1EchoVerb.cs:253, :388, :393; README.md:35, :37-:38, :144-:149, :326, :331, :337.

## Prototype checks run (rule: STOP-severity checks run once on my own output)
`fwd.py` (harness-run5, loopback): the closed list refused 4 shapes (exit 2, FIRED); a loopback or public `<mac>` was refused (FIRED); 1 MiB passed unchanged both ways with matching log counts (PASS); a refused target closed the client (PASS); a second live listener ended exit 3 with nothing left listening (FIRED); SIGTERM and `--max-seconds` both ended it (PASS); the TLS certificate sha was unchanged through it (PASS); no payload in the log (PASS); the real pairs `127.0.0.1:10443` and `127.0.0.1:7627` bound with nothing connecting (PASS). Run 2 exposed a TIME_WAIT re-bind failure, fixed with SO_REUSEADDR: BSD still refuses a second live listener, re-proved in run 5. Never run: the `<mac>:18632` pair (it would listen on the LAN), and any lab run (no build, no lock taken).

## Chain inputs (DRAFTER_RULES MEASURED LITERALS 4)
| Step | Inputs | From |
|---|---|---|
| 0 | stamp; X85 STATUS READY | Tuesday; seat X85 (absent now: refuse until present) |
| 1 | five tools (exist), origin, credentials by name, B2068 kit (exists) | `<d>/seat-tools`; GitHub; `.env` (never read); OXPd Briefs |
| 2 | lane | 1 |
| 3 | fwd.py, fwdlog, `<mac>`, free ports | 1, 1, 2, 2 |
| 4 | dll, lab_run_env, session, forwarder | 1, 1, 2, 3 |
| 5 | pins, enabled.py | 4, 1 |
| 6 | branch, `<via>` | 5 |
| 7 | E01 exit 0, X85 leg, the forwarder's `<mac>` pair | 6, 0, 3 |
| 8 | W22's printed undo | 6 |
| 9 | pid, session | 3, 4 to 8 |

## D-decisions (Tuesday's defaults in the kit)
D1 after X85 READY, serial; D2 a direct control beside each forwarded request; D3 the direct host is the IP, not the `.local` name (both runs then name an IPv4 literal); D4 `<via>` is the forwarder when R02F is ACCEPTED, else direct, and each undo on its write's host; D5 a direct W23D fallback if the forwarded undo fails (undo-owed then shows owed on 127.0.0.1 by host as typed: a DEVIATION when R04D reads false); D6 findings are not STOPs; D7 no retry and no forwarder restart.

## Q-questions for Tuesday (each with a default)
- Q1 (STOP-class) order: **a** after X85 READY, X85's callback field picks full or leg S.
- Q2 (STOP-class) credentials: **a** as X85 (envsecret by name, pipe, random guest).
- **Q4, the partition the commission asked for: should X85 be amended instead?** Default **a: NO.** Keep X85 as drafted and run X88 after it. X85's CA store test does not depend on the forwarder. Amending it re-opens a kit drafted for M-a. X88's direct controls let it stand alone. Alternative **b**: X88's steps go into X85 as its Part 2. That saves one build (two heavy jobs) and one session, but X85 holds the printer about twice as long. Alternative **c**: drop X85's E02 and let X88's E02D be the route test, with X88 first.
- **How they differ:** X85 does the CA import and remove, plus the Test service, plus one direct sync echo and one direct async echo, with nothing in between. X88 writes only the Test service, puts `fwd.py` between the lab and the printer, and pairs each forwarded request with a direct one.
- Q5 a REFUSED at R02F: default, record it as a finding with the cause not separated. Alternative: commission a CONNECT-proxy option in the lab (a code change) so the URL keeps the printer's address, as the product would.
- Q3 Test service found on: leave it. Q6 direct host: the IP. Q7 ports: 127.0.0.1:7627, 127.0.0.1:10443, `<mac>`:18631, `<mac>`:18632. Q8 names: `.tools/b2169-x88`, pane `Datasec/OXPd2-X88`. Q9 forwarder lifetime: 5400 s.

## UNMEASURED
- Whether the M577 answers anything through a forwarder (the whole point; NEVER RUN).
- Whether `fwd.py` can bind `<mac>:18632` while the lab binds `127.0.0.1:18632`. DERIVED: BSD allows two specific addresses on one port, and if the lab cannot listen it exits 8 having sent nothing.
- The format of the lab's `from` field (`IPEndPoint` text, DERIVED from `:393`).
- Whether .NET sends SNI for an IP literal: assumed no, which is why D3 uses the IP; not load-bearing.
- The router's 192.168.8 -> 192.168.20 forwarding (X85 measures it).
- Relay's delay, the TLS callback, and the CONNECT-proxy path.

## Outside-the-fences disclosure
- Writes: only the kit, `.measured` and this report under `tuesday/briefs/`, plus scratch under `fleet/state/s334/d2169-T/`. I moved one `__pycache__`, which an `-I -c` import in my harness had made, from `seat-tools/` to `d2169-T/_quarantine/` (nothing deleted).
- Local listeners: brief loopback listeners on 28700 to 28704 (synthetic), and ONE 2-second bind of `127.0.0.1:10443` and `127.0.0.1:7627` with nothing connecting. One failed bind attempt on `127.0.0.1:443`.
- No device contact, no LAN listener, no name lookup, no Azure, no `.env` read, no Source_Documents or key folder, no project write, no Jira, GitHub write, card or mail. `openssl req` made a synthetic 1-day TLS key and certificate in `<d>/test/` (`tls.key`, `tls.crt`), for the passthrough case only.
- I read X85's and B2068's kits, the X85 report only as a port-scan hit (file name, not its text) and OXPd Briefs STATUS file names and contents (counts only).
