# CoAgent: lane plan for 2026-11-17 (General; Kam's personal project; no client)

Written for Friday by the architecture agent. Design basis: `/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/06_design-addendum-rulings-2026-11-17.md` (cited as **[06 §n]**). Nothing here was run or measured; every fact about code names where it was read.

Authority, as relayed in Friday's commission to me (Friday replaces this line with the board reference): Kam, 2026-11-17, verbatim, "yes, keep building today"; limits: no deploy, no publish, no spend; the repository stays private.

## 1. State the plan is built on

- `main` and the checkout `coagent/2_Project_Files` are both at `18005d63ae1311df9649893060caf1f98510a4c1` (`git rev-parse HEAD main`). Crates on main: `coagent-proto`, `-crypto`, `-roster`, `-relay`, `-ipc`, `-cli` (`git ls-tree -r --name-only main`).
- Three branches are IN FLIGHT and unmerged. What each touches, from `git diff --name-only main...<branch>`:

| Branch | Own crates | Files outside its own crates |
|---|---|---|
| `m1-daemon` | `crates/coagent-daemon`, `crates/coagent-mcp` | `BACKLOG.md`, `Cargo.lock`, `Cargo.toml`, `docs/DAEMON.md`, `scripts/red-controls-daemon.sh`, `scripts/test-daemon.sh` |
| `m2-policy` | `crates/coagent-policy` | `BACKLOG.md`, `Cargo.lock`, `Cargo.toml`, `docs/POLICY.md` |
| `m3-audit` | `crates/coagent-audit` | `BACKLOG.md`, `Cargo.lock`, `Cargo.toml`, **`crates/coagent-crypto/src/identity.rs`**, `docs/AUDIT.md`, **`docs/CRYPTO-GLUE.md`**, `scripts/red-controls-audit.sh` |

- So no in-flight branch touches `crates/coagent-roster`, `crates/coagent-relay`, `crates/coagent-cli`, `crates/coagent-ipc` or `crates/coagent-proto`. The audit branch does touch one file of `coagent-crypto` and appends to `docs/CRYPTO-GLUE.md`: no new lane may edit either until it has merged.
- The in-flight daemon and audit crates USE the roster crate's public API: `admit, Member, Role, RosterBody, RosterChain, SignedRoster, CAP` and `Member::new` with six arguments [branch m1-daemon: crates/coagent-daemon/src/engine.rs:42, 1761-1769]; `Member::new`, a `RosterBody { … }` literal, `Applied::Advanced { .. }`, `RosterError::Fork` [branch m3-audit: crates/coagent-audit/tests/common/mod.rs:42, 66; src/bundle.rs:720, 1074]. The in-flight daemon reads the relay's banner by the prefixes `url: ` and `fingerprint: ` [branch m1-daemon: crates/coagent-daemon/src/relay_child.rs:99-101]. A new lane that owns those crates keeps those surfaces stable.
- Disk: the seats report the volume 95% used with about 94 GiB free, and each lane's build directory at 0.5 to 1.1 GB [STATUS_M3_AUDIT A2.10; STATUS_M1_RELAY "Disk"].

## 2. Recommendation: start TWO lanes now, both at opus level

| | Lane | Why now |
|---|---|---|
| 1 | **M3-ROSTER**: limit of 4 and member proposals in the roster crate | It carries the two rulings that change the design most (n1, n2). Its crate is on main and nobody else's branch touches it. Everything about groups in the daemon waits on it. |
| 2 | **M1-RELAY-IDENTITY**: the relay's saved identity behind a deliberate option | It is the ruled answer to the daemon's main usability gap (REQUEST 1). Its two crates are on main and nobody else's branch touches them. |

The two lanes share no file. Neither edits root `Cargo.toml` or `Cargo.lock` (no new crate, no new dependency expected; a seat that finds it needs one stops and writes it under REQUESTS). Both append to `BACKLOG.md` in one separate commit, as every earlier seat did; that file conflicts at merge and is resolved by keeping both sides [STATUS_M1_RELAY ADDENDUM 3 item 1].

Everything else waits. The laptop already runs two build seats and a gate; a third new lane is not recommended.

## 3. The lanes

Model rule given for this plan: a build on a security design surface = opus; a multi-file build that is not = sonnet.

| Lane | Owns (exclusive) | Must NOT touch | Branch / worktree | Depends on (on main now?) | Model, one-line reason | When |
|---|---|---|---|---|---|---|
| **M3-ROSTER** | `crates/coagent-roster/**`; the rows of `scripts/red-controls-core.sh` whose package is `coagent-roster`; new `scripts/red-controls-roster.sh`; new `docs/ROSTER.md` | every other crate (including the `build.rs` of proto and crypto); root `Cargo.toml`; `docs/CRYPTO-GLUE.md`; relay constants | `m3-roster` / `coagent/worktrees/m3-roster` | proto, crypto, roster: YES, on main | **opus**: the roster validator and a new signed object are the admission control of the session | NOW |
| **M1-RELAY-IDENTITY** | `crates/coagent-relay/src/tls.rs` and the crate's `lib.rs` export line, README, `PROTOCOL.md` identity note, new test files, new rows in `red-controls/run.py`; `crates/coagent-cli/**` | relay `limits.rs`, `state.rs`, `frame.rs`, `meter.rs`, the relay's gate test files, `MAX_SLOTS`; every CORE crate; the daemon | `m1-relay-identity` / `coagent/worktrees/m1-relay-identity` | relay, cli: YES, on main | **opus**: a private key at rest with ownership and permission checks, and the pin a joiner trusts | NOW |
| **N1-PASS** (limit of 4 everywhere else) | relay `MAX_SLOTS` and its texts [06 §1.1]; the audit crate's `1/7` divisor; the daemon's roster-equals-relay constant test; "cap 8" in `docs/CRYPTO-GLUE.md` and `PROTOCOL.md` | anything not on the [06 §1.1] table | `n1-pass` | AUDIT merged: NO. DAEMON merged: NO. M3-ROSTER merged: NO | **sonnet**: a constant followed through several crates, no new design. It edits gate test files, so it needs Friday's written ruling per file first | after AUDIT, DAEMON and M3-ROSTER merge |
| **CORE-FOLLOWUP** (the crypto REQUESTS) | `crates/coagent-crypto/**`: `SignDomain` values for proposals and for a signed relay-moved line (daemon R7); seeding stored verify counts (R2); `attempts_used` (R3); the KK label in the prologue (R6); plain `insert` made unreachable [06 §5.2]. One-line items in ipc (R4) and the relay client doc (R5) | roster, daemon, audit | `core-followup` | AUDIT merged (it edits `identity.rs`): NO. M3-ROSTER merged (to move its proposal signature to the real domain): NO | **opus**: signing domains and the verify-attempt state are the cryptographic glue | after AUDIT and M3-ROSTER merge |
| **GATE-HOOK** (milestone M2 integration) | the hook client, the daemon's gate decision path (the one release point `GateWitness`), the owner-only exact-command list [06 §6] | the policy crate's rules | to be named | POLICY merged: NO. DAEMON merged: NO | **opus**: it is the gate | after POLICY and DAEMON merge |
| **DAEMON-GROUPS** (milestone M3 wiring) | `crates/coagent-daemon`: sessions of up to 4, carrying proposals and results [06 §2], the inheritance rule [06 §5.2], share-level statements for the audit crate, pinned-contact check against the roster, use of the relay identity options | merged library crates | to be named | DAEMON, AUDIT, M3-ROSTER, CORE-FOLLOWUP, M1-RELAY-IDENTITY merged: NO (all five) | **opus**: it wires the security libraries to the network | last of this group |
| **CONNECT-GUIDE** (n5, paths 1 to 3) | the guided connection question and the candidate `kind` in the invite [06 §3] | the third-party path itself (mechanism UNDECIDED, [06 §3.4]) | to be named | DAEMON merged (the invite lives there): NO. M1-RELAY-IDENTITY merged (it shares `coagent-cli`): NO | **opus**: it changes the invite format and carries the "no third party without consent" rule | after DAEMON and M1-RELAY-IDENTITY merge |
| **WINDOWS** (spikes W1, W3; pipe identity checks R3) | `crates/coagent-ipc/src/windows.rs`; the Windows hook stub | everything else | to be named | the owner at the Windows machine | **opus**: the pipe's access control is the local trust boundary on Windows | Friday 2026-11-20, with him present |
| **DISCLOSURE-DOCS** (n7 obligations: README security status, `SECURITY.md`) | `README.md`, `SECURITY.md` | code | to be named | his answer on the publication card (the sweep says the README must change before publication) | **sonnet**: documents, several files, no design surface | after the publication card |

## 4. Order in which lanes become possible

1. **Now:** M3-ROSTER, M1-RELAY-IDENTITY.
2. **When AUDIT merges:** nothing new alone. (`identity.rs` and `docs/CRYPTO-GLUE.md` become free.)
3. **When AUDIT and M3-ROSTER have merged:** CORE-FOLLOWUP.
4. **When POLICY and DAEMON have merged:** GATE-HOOK.
5. **When DAEMON and M1-RELAY-IDENTITY have merged:** CONNECT-GUIDE (paths 1 to 3 only).
6. **When AUDIT, DAEMON and M3-ROSTER have merged:** N1-PASS, once Friday has ruled on the gate test files it must edit.
7. **When all of DAEMON, AUDIT, M3-ROSTER, CORE-FOLLOWUP and M1-RELAY-IDENTITY have merged:** DAEMON-GROUPS.
8. **2026-11-20, owner present:** WINDOWS.
9. **After the publication card:** DISCLOSURE-DOCS.

## 5. What cannot start yet, and why (plainly)

- **Anything in the daemon.** The daemon crate is in flight, at its third check. Groups in the daemon, proposals on the wire, the inheritance rule, the guided connection question and the gate hook all live there.
- **Anything in `coagent-crypto`.** The audit branch edits `identity.rs`. This is why M3-ROSTER signs proposals through a labelled work-around and lists the real signing domain as a REQUEST [06 §2.3].
- **The limit of 4 outside the roster crate.** The relay constant sits under gate test files a seat may not edit without a ruling; the audit and daemon crates are in flight. Until N1-PASS, the roster says 4 and the relay still allows 8 slots. That is safe: the roster validator in every daemon is the rule and the relay limit is a courtesy [04 §3.8].
- **The third-party connection path.** The mechanism is UNDECIDED [06 §3.4]. No lane may build against one.
- **All Windows behaviour.** Untested until the owner is at the machine.
- **The browser console, Approved Trust, the release.** Milestones M4 to M6; they sit behind everything above.

## 6. Merge hazard to plan for

M3-ROSTER changes `CAP` from 8 to 4 while two unmerged crates import `CAP`. In its own worktree its `scripts/check.sh` is green or red on main's crates only, because the audit and daemon crates do not exist on main. When M3-ROSTER later merges main into its branch (after AUDIT and DAEMON have landed), an audit or daemon test that builds more than four members, or relies on a share of one seventh, may fail. UNKNOWN whether any does: I read the audit crate's use of `CAP` and `1/7` [branch m3-audit: tests/common/mod.rs:71; src/session.rs:13], not every test. What closes it: running `scripts/check.sh` on the merged tree. The M3-ROSTER seat must not fix another crate; it reports the failures under REQUESTS, and they become N1-PASS's first items. Friday then merges M3-ROSTER and N1-PASS in one step, or holds M3-ROSTER until N1-PASS is ready.

## 7. Briefs written for the two lanes that start now

- `/Volumes/Laptop-DEV/FRIDAY/2_Project_Files/friday/briefs_drafts/2026-11-17_coagent_M3_ROSTER_brief.md`
- `/Volumes/Laptop-DEV/FRIDAY/2_Project_Files/friday/briefs_drafts/2026-11-17_coagent_M1_RELAY_IDENTITY_brief.md`

Both follow the format of the M3 AUDIT and M1 DAEMON briefs. Report files: `coagent/5_Project_History/STATUS_M3_ROSTER.md` and `STATUS_M1_RELAY_IDENTITY.md`. Last lines: `READY FOR QA M3-ROSTER` and `READY FOR QA M1-RELAY-IDENTITY` (file names with underscores, last lines with hyphens, as the existing briefs do).
