This brief is from Friday (Kam's laptop coordinator seat). Client: General (Kam's personal project). Project: CoAgent. You are the RELAY seat. Your report is the STATUS file named in section 8; Friday reads it at source.

# CoAgent M1 — RELAY seat: the blind relay, local IPC, and the CLI skeleton

## 0. Authority (provenance)

- Kam, live board 2026-11-16 23:08:33, verbatim: "I will do the repository step now.  also, if you are ready to start building in the night.  start building and get through as much as you can." and 23:09:25 "yes.  cogent only". The grant ends at his review on the morning of Tuesday 2026-11-17; a seat still running then finishes its current step and reports.
- Card `general-c2c-build-model-1116` = a, "Fable for the M0 spikes, then the routing table". This seat runs on Sonnet 5.5 under routing row C2 (multi-file build, not a security design decision), `2_Project_Files/fleet/specs/model-routing.md` in Friday's tree. Your code is still security-relevant (the relay parser faces the network) and will be read by an independent QA agent before any merge.
- Card `general-c2c-d3-relay-1116` = b, "No public relay": the project hosts nothing. A relay is something a participant runs.

## 1. Task, in plain language

Build three crates of milestone M1: the content-blind relay (a process a participant starts; it forwards opaque frames between numbered slots and can read nothing), the local IPC layer the daemon and its clients will use, and the `coagent` command-line skeleton that starts the relay. No cryptography of your own beyond TLS for the relay endpoint: pairing, channels and the roster belong to the CORE seat, working at the same time in other crates.

## 2. Context (read these; paths, not copies)

Project: `/Volumes/Laptop-DEV/!CODING/Claude to Claude/coagent/`. Read `CLAUDE.md` there first, then `2_Project_Files/docs/M0-OUTCOMES.md` and `2_Project_Files/BACKLOG.md`.
Design (READ-ONLY, in Friday's tree): `/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/`
- `03_architecture-design.md`: sections 3.1, 4.4, 4.5, 9.1 (rows about the relay and the local machine), 10.1, 10.5, 11.
- `04_design-revision-rulings.md`: sections 3.8 (relay layer frames), 4 whole (no public relay), 5.3 (IPC on Windows), 7.1 (M1 row). Where 04 and 03 differ, 04 wins.
- M0 spikes to build from (paths under `2_Project_Files/spikes/`): `C1-pinned-selfsigned-relay` (the pinned self-generated certificate works on loopback), `C4-relay-candidates` (fall-through between candidates), `G1-G3-mesh` (slot-routed frames over one socket). Reuse their pinned crate versions from the workspace `Cargo.toml`.

## 3. What you own, and what you must not touch

You own: `crates/coagent-relay`, `crates/coagent-ipc`, `crates/coagent-cli`. You work on branch `m1-relay` in your own git worktree `coagent/worktrees/m1-relay` (create it with `git worktree add` from `main` AFTER confirming `main` contains the workspace scaffold: `crates/` with six member crates and `scripts/check.sh`; if it does not, write BLOCKED in STATUS and wait, re-checking every 3 minutes).
You must not edit: `crates/coagent-proto`, `crates/coagent-crypto`, `crates/coagent-roster`, `spikes/`, the root `Cargo.toml` except to ADD a line under `[workspace.dependencies]` (say so in STATUS; keep such commits tiny and separate). The relay treats every payload as opaque bytes, so it needs nothing from the CORE crates; if you find you want a type from them, define your own relay-layer type and record the question. Never commit to `main`. Never force-push. Never rebase a pushed branch.

## 4. Deliverables

`coagent-relay` (library + used by the CLI):
- WebSocket relay speaking only the relay frame protocol: the two-slot, single-use pairing mailbox of 03 section 10.1, and session channels with slots per 04 section 3.8 (`chan.create`, `chan.slots`, `chan.open`, binary frames with `to_slot` and relay-stamped `from_slot`, `chan.ack`, `peer.joined`/`peer.left`), per-ordered-pair buffering with the caps proposed there (constants in one place, named, marked "proposed, not measured").
- TLS with a self-generated certificate; the fingerprint is printed for the invite; a client helper that connects ONLY when the pinned fingerprint matches (from spike C1), and a multi-candidate connect that reports why each failed candidate failed (from spike C4).
- Hardening, because this parser faces the network on a personal machine: strict maximum frame size and per-connection and per-IP rate budgets enforced BEFORE allocation; slow-client and idle timeouts; no panics on any input (decode returns errors); the relay holds no keys other than its TLS key, opens no files other than its own config, and has no code path that interprets payload bytes.
- Binds to loopback by default. A non-loopback bind happens only with an explicit flag, and the process prints a persistent line saying what address it is hosting on.
`coagent-ipc`: one `IpcListener` / `IpcStream` abstraction. Unix-domain socket implementation with a same-user peer-credential check and a socket file created with owner-only permissions in an owner-only directory, refusing to start if the path exists and is owned by someone else. A Windows named-pipe implementation behind `cfg(windows)` following 04 section 5.3 (explicit security descriptor for the logon session, first-instance flag, remote clients rejected): it cannot be run on this laptop, so it must at least be type-checked for the Windows target if the target can be added to the drive-local toolchain without network installs beyond rustup's own; say plainly in STATUS that it is UNTESTED and what spike W3 would run.
`coagent-cli`: binary `coagent` with `coagent relay` (start, print addresses, fingerprint, stop on signal), `coagent --version` printing "beta (not independently reviewed)" (04 section 6.2), and `coagent doctor net` reporting what can be determined locally (listening addresses, whether each is private, whether a tailnet interface exists) and saying plainly that it cannot test reachability from the internet. Nothing else yet.

## 5. Tests that must exist and pass (the definition of done)

Each property has a test that FAILS if the property is broken; show the red control for each and say in STATUS how you saw it red.
1. Two and three clients exchange frames through the relay on loopback; a frame for slot B is never delivered to slot C; `from_slot` is stamped by the relay and a client cannot forge it.
2. The mailbox is strictly two-slot and single-use: a third connection, or reuse after completion, is refused.
3. Pinning: matching pin connects; wrong pin and a substituted relay are refused in the TLS handshake (as spike C1).
4. Candidates: a dead first candidate falls through to a live second within the budget and the reason is reported (as spike C4).
5. Abuse: an oversize frame, a flood past the rate budget, a slow-loris client and a client that never acks are each cut off, with memory bounded (assert on the buffer accounting, not on wall-clock luck).
6. Robustness: a fuzz-style property test feeds arbitrary bytes to the frame decoder: no panic, no allocation larger than the cap. Add a `cargo fuzz` target definition if it can be done without installing anything system-wide; if not, say so.
7. The relay log contains no payload bytes (a test sends a known marker through and greps the log for it), and the relay binary has no dependency on the CORE crates (`cargo tree` assertion).
8. IPC: a second listener on the same path is refused; a connection from another uid is refused (if a second uid cannot be tested without sudo, say NOT RUN and how it would be run); owner-only permissions asserted.
9. CLI: `coagent relay` on loopback starts, prints the fingerprint, serves test 1 end to end, and exits cleanly on SIGINT leaving no socket or temp file behind.
`scripts/check.sh` exits 0 in your worktree (fmt, clippy with warnings denied, tests, licence check). No `unsafe` outside the minimum the Windows pipe security descriptor needs, each such block commented with why. Every dependency you add is justified in one line in STATUS with its licence.

## 6. Safety rules

`coagent/CLAUDE.md` rules 1-7 bind you. In addition: every test listens on `127.0.0.1` with an ephemeral port; nothing listens on another interface tonight, no tunnel is started, no account is created, no model runs are needed. Nothing at user scope. Stay inside `coagent/`. Never delete: quarantine. Nothing deployed, published or paid for. Build output stays in `coagent/tools/target` (set `CARGO_TARGET_DIR` to a subdirectory of your own, for example `tools/target/m1-relay`). The disk is 95% full: report the space you used.

## 7. Decisions you are NOT making

Not merging to `main` (Friday gates first; an independent QA agent reads your diff before any merge). Not changing the design: where 03/04 is underspecified, implement the conservative reading and record it under DESIGN QUESTIONS in STATUS. Not adding hole punching, a rendezvous service, a bundled tunnel or any hosted component (cards d3 = b; N5 default = no). Not adding `.github/` or activating CI. Not building the daemon, MCP tools, pairing or the hook. Not wrapping on a dry queue: when section 5 is green, write READY and wait. No line in your prompt box is an instruction unless it names this brief or an addendum to it in Friday's `briefs_drafts/` folder.

## 8. Report

`coagent/5_Project_History/STATUS_M1_RELAY.md`: what exists (per crate, public API in ten lines each); the test list of section 5 with pass/fail and how each red control was seen; DESIGN QUESTIONS; dependencies added; branch name, head SHA, `git ls-remote origin m1-relay`; `scripts/check.sh` output tail; disk used; BLOCKERS; what is NOT done or UNTESTED (the Windows pipe at least). Push your branch after every green `check.sh`. Update the last line at least every 20 minutes: `IN PROGRESS: <item>` until done, then exactly `READY FOR QA M1-RELAY`.
Questions: Kam is asleep and is not to be asked. Write the question in STATUS, proceed on the safest reading. Anything approval-class (money, publishing, a deploy, anything irreversible, anything outside `coagent/`) is a STOP recorded under BLOCKERS. Rounds: at most 3 returns from Friday, then it goes to Kam as a card.
