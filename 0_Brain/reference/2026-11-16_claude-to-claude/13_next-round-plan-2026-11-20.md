# CoAgent: plan for the next build round (2026-11-20)

Status: plan and two draft briefs. Nothing built, nothing run, no card posted, nothing launched.

## BLUF

1. Seven lanes with disjoint files (§2). **Start today, in parallel: L1 POLICY-MODE, L2 AUDIT-HOST, L4 SPIKES, L5 ROSTER-NOTES**; L7 PREVIEW-TIDY is an hour for the first idle seat. L1 and L2 hold the two heavy-run slots.
2. L3 RELAY-RECONNECT (the guest reconnects by itself after a host restart) waits for the owner's decision I-11. L6 GATE-BIND (session binding, truthful cards) waits for L3 and L4.
3. L1 needs no merge first: neither preview lane touches the policy crate. L2 needs the seal merged. L4 and L7 need the preview lanes merged.
4. D-2 (deputy): recommend "your next change to the member list settles everyone the deputy let in" (§3, option a). The smallest build, and it removes the case instead of working around it.
5. After this round the owner sees fewer red cards and a demo that runs anywhere; the log and the "approvals off" rules exist under test but are not connected to anything he can switch on (§4, §5).
6. Draft briefs for L1 and L2 are in §7. Seven candidate questions for the owner are in §6; the mode's eleven are in doc 12 §5.
7. Not read by me: designs 04-07 and 09 bodies, the STATUS bodies, the seal's verdict (still running). Marked where it matters.

---

## 0. How to read this

- Assumption given to me: the two preview lanes (`p1p-gate`, `p1p-demo`) and `m3-audit-seal` merge today. At the time of writing none had: lane A's STATUS last line was "IN PROGRESS: 09:30 final runs on b7e8da4", lane B's was waiting for lane A, the seal's was `READY FOR QA M3-AUDIT-SEAL` and its verdict file held 12 bytes (check running).
- SHAs read: **main** = `32beb563837341560b908d9ba5b0a60de240d860`; **p1p** = `b7e8da4` (local `p1p-gate`); **demo** = `ba6cdb7` (local `p1p-demo`); **seal** = `841c4459e5cdda0637e4df2cdf77ba133f51bd18`. All four objects exist locally; nothing was fetched. `m3-audit-seal` and `p1p-demo` do not yet contain main's deputy commits (their diff against main removes the deputy files), so each must merge main before its merge check.
- "Doc 12" = `12_both-agree-mode-design-review.md` in this folder; F-n are its findings.
- UNDECIDED names who decides: **the owner** for product behaviour, safety boundaries and anything a person notices; **the coordinator** for build mechanics inside a ruling.
- Nothing was built, run or posted.

---

## 1. Inventory: every open item on the table

### 1.1 The live demo's findings (`p1p_review/live_demo_report.md`)

| # | Item | Source | Where it lives in code | State |
|---|---|---|---|---|
| LD-1 | A reply whose text names an excluded path is refused (Surprise 2; step 7e) | report, "Surprises" 2 | policy: free text is matched against exclusions by name [main: crates/coagent-policy/src/engine.rs:393-395; src/action.rs:214, :522] | by design, fails safe. Whether to change it: UNDECIDED (the owner, Q-B below) |
| LD-2 | Every guest-side card says "requested by peer key …", also for calls the guest's own owner typed (Surprise 5) | report, "Surprises" 5 | `origin = Member(peer)` whenever a session is active [p1p: crates/coagent-daemon/src/gate.rs:353-356]; rendered at [p1p: gate.rs:529-531] | display wrong; lane L6 |
| LD-3 | After a host daemon restart the link does not reconnect: the relay child has a new certificate and the guest needs the `relay.moved` line (Surprise 6; step 10b) | report, "Surprises" 6 | [main: BACKLOG.md:232-236] (REQUEST R1); the relay CLI already accepts `--identity-stdin` [p1p: crates/coagent-cli/src/args.rs:10, :23, :121]; the daemon does not use it (no match for `identity-stdin` under `crates/coagent-daemon/src` at `b7e8da4`) | lane L3; needs the owner's decision I-11 (design 08 §3 item 6b says "decision I-11 is Kam's"; I did not read I-11 in design 06: UNVERIFIED) |
| LD-4 | Prompt-heavy: every inbox read, every ToolSearch and every send asks (BLUF last line; step 6, 7a) | report | `inbox_read`/`wait` untaught [main: crates/coagent-policy/src/known.rs:60-61, :93-95]; `ToolSearch` taught at T2 [main: known.rs:71]; send is T3 because unscanned [main: engine.rs:515; action.rs:562] | lane L1 for the two entries; the scanner is later (§1.7) |
| LD-5 | Claude Code 2.1.328 starts in auto mode; the spikes ran 2.1.325 (Surprise 1). The Write ask shows Claude Code's own dialog, not the card text (Surprise 7) | report | host behaviour | lane L4 (measure) |
| LD-6 | Whether Claude Code passes `tool_use_id` or a session id to the MCP server: NOT settled ("UNKNOWNs settled" item 4) | report | needed to bind the witness (P1-7) | lane L4 |

### 1.2 The preview check's notes (`p1p_review/gate_P1P_verdict.md`, lines 17-25) and lane A's BACKLOG entries (added lines of `BACKLOG.md` at `b7e8da4` against main)

P1-1, P1-2, P1-4, P1-5, P1-6, P1-8 were fixed in lane A's addendum 1 (commit `750fc05`, its subject line lists them). Left for later:

| # | Item | Source | State |
|---|---|---|---|
| P1-3 | A shell call whose working directory is under a folder named like the exclusion is denied; the demo's `private` folder under `/private/tmp` | verdict line 19; lane A BACKLOG "A relative `--exclude` glob covers the whole workspace …" | demo scripts: lane L7. Whether a relative exclusion should be relative to each workspace root: UNDECIDED (the coordinator; policy dialect) |
| P1-7 | A witness from another Claude Code session releases a read, and the taint goes to the wrong session | verdict line 23; lane A BACKLOG "Gate mode: a witness from ANOTHER Claude Code session …" and "The liveness witness is bound by tool name and time" | lane L6, after L4 settles LD-6 |
| P1-9 | The ask reason in Claude Code's prompt carries the card's command, targets and MCP input | verdict line 25; lane A BACKLOG "(P1-9)" | UNDECIDED (the owner: what the terminal prompt shows); lane L6 builds the ruled form |
| A-B1 | `KNOWN_TOOLS` entries owed for `inbox_read` and `wait` | lane A BACKLOG first added entry; [main: BACKLOG.md:556-560] | lane L1 |
| A-B2 | The hook client is a separate binary, not `coagent hook` | lane A BACKLOG | M5 packaging; not this round |
| A-B3 | A tool call over 128 KiB is denied by the hook (a large `Write`) | lane A BACKLOG | lane L6; the form of the fix is UNDECIDED (the coordinator) |
| A-B4 | Gate mode gates every session that loads the plugin (no session binding) | lane A BACKLOG; [p1p: docs/DAEMON.md:513-515] | lane L6 |
| A-B5 | The daemon does not learn the owner's answer to a terminal prompt | lane A BACKLOG | lane L6 (needs a `PermissionRequest` or `PostToolUse` path; L4 measures) |
| A-B6 | The red-controls row format cannot carry cargo `--features` | lane A BACKLOG | lane L6 (script) |
| B-B1..6 | Lane B's own list: witness binding; hook docs describe an `mcp_server` object; fixtures built from the 2.1.325 shape; hook command shell form versus exec form; MCP path with spaces; no version-floor guard | `preview/BACKLOG-PREVIEW.md` at `ba6cdb7`, lines 6, 14, 23, 30, 39, 47 (titles read; bodies not read) | lane L7, except the first (L6) |

### 1.3 The deputy's deferred items (`m1_review/gate_M3_DEPUTY_verdict.md` lines 19-25; [main: BACKLOG.md:614-638])

| # | Item | State |
|---|---|---|
| D-2 | After ANY later starter version, a provisional newcomer cannot start and a later joiner refuses earlier admissions; views differ until the grant is renewed. "DESIGN DECISION NEEDED BEFORE THE DAEMON WIRES THE DEPUTY IN" [main: BACKLOG.md:624-628] | UNDECIDED (the owner): §3 |
| D-3 | Fork evidence about the deputy is kept per session, first come (4 pairs) [main: BACKLOG.md:629-633] | UNDECIDED (the coordinator: a bound inside design 06 §2.8.9); lane L5 |
| D-7 | The daemon must use `admit_view`, not `admit` [main: BACKLOG.md:634-638] | later lane L9 (deputy wired into the daemon) |
| D-4, D-5 | The generated property never reaches several refusal classes; `CandidateKeyInUse` has no test (verdict lines 22-23) | lane L5 |
| D-1 | "Drop is not sticky" (verdict line 19) | closed on main by "dropping is lasting" [main: docs/ROSTER.md:419-436] |
| — | `admit_view` repeats `admit`'s observer list [main: BACKLOG.md:614-618] | lane L5; editing `admit` needs the coordinator's word |

### 1.4 The seal's daemon preconditions and open questions (design 10 §2.1, §2.2, §7.2; [seal: BACKLOG.md:590-629])

| # | Item | State |
|---|---|---|
| D-S1 | Seal policy driven only by the owner's command, time, or the member's own space [seal: BACKLOG.md:590] | lane L2 |
| D-S2 | No other mutating call between `seal_export` and `seal_commit` [seal: BACKLOG.md:595] | lane L2 |
| D-S3 | Persist the bundle and the pending anchor before the commit; promote after [seal: BACKLOG.md:600] | lane L2 |
| DQ-S1 | The default seal policy [seal: BACKLOG.md:610] | UNDECIDED (the owner). IS1 ("Only you or your settings decide") says who; it does not say which setting is the default. L2 builds every trigger and defaults to "the owner's command only" |
| DQ-S2 | Archive retention [seal: BACKLOG.md:605] | UNDECIDED (the owner for the default). L2 builds "keep everything, delete nothing" |
| DQ-S5 | Should a lone format-3 `verify` refuse a file it cannot link [seal: BACKLOG.md:615] | UNDECIDED (the coordinator as design owner); not this round |
| DQ-S6 | Re-anchoring and seals [seal: BACKLOG.md:620] | with the re-anchor item below; not this round |
| — | A `seal_commit` whose rebuild fails after the commit put [seal: BACKLOG.md:625] | lane L2 handles the documented recovery (`resume_with_anchor(plan.post_anchor)`) |

`STATUS_M3_AUDIT_SEAL.md` (578 lines): I read its last line and its section headings only ("Design questions (none open as a STOP)", line 530). Its body is UNVERIFIED by me.

### 1.5 The daemon notes [main: BACKLOG.md:589-613]

| # | Item | State |
|---|---|---|
| R6-2 | Clearing row 54's clock on a forward acknowledgement is untested (:589) | lane L3 (it owns `recovery.rs` tests this round) |
| R6-3 | Row 54's clock is counted under the name "T-RTO" (:594) | lane L3 |
| R6-4 | Cost under a sustained hostile peer, about 15.5 frames/s (:599) | Note; no action asked |
| R6-5 | The generated hostile-peer property draws no peer messages and no peer-started key exchanges (:604) | lane L3 |
| — | The round-2 check's bulky-audience test can fail under heavy load (:609) | the check's file; a ruling for the coordinator, not a builder edit |
| G10, G12, G14, G16, G17, R2-8, R4-9, R4-10, the 64-wait finding | [main: BACKLOG.md:262-336] | G14 (unsigned `relay.moved`) falls away if L3 lands; the rest not this round |

### 1.6 Audit notes still open [main: BACKLOG.md]

For the daemon lane (all in L2 or L8): D3 message rate (:398), D5 `record_for(causer)` (:403), D7 total across sessions (:408), `resume` returns default limits (:443, :469), received-chain state is rebuilt only by export (:355), signed share-level statements must be delivered by the daemon (:379).
Crate-level, not this round: redaction misses (:360, :389), no re-anchor path (:364, :418), receipt headers reveal to a `nothing`-level member (:374), small notes (:394), a release-only gate measurement (:423), resume diagnostics (:428), `archive_and_release` is several writes (:433; crash order fixed on the seal branch), full part never checkpointed (:438), N1/N2/N8 (:457-468), seat cap in a re-used slot (:476), QA-n4 (:496), fork answered `Store` (:501), QA3-n1..n3 (:574-588), full capture not built (:346), unattested tail (:350), `Envelope.sig` doc (:341).

### 1.7 What the plans say comes after the preview

- Design 08 §3 item 6 (order recommended then): (a) deputy: done, on main; (b) daemon follow-ups: "use the saved relay identity (`--identity-stdin`; decision I-11 is Kam's), the roster's new calls (`apply_with_report`, `approve_with_report`, default limit 4, proposal carried as one opaque string), the member-invite transport and approval card"; (c) audit seal-and-continue: built, in check; (d) connection choice at start-up (n5): "needs the third-party service decided first; it is UNDECIDED and must not be guessed"; (e) the console and Windows.
- Design 08 §4, decisions waiting: which third-party connection service; "Whether provisional members (let in by a deputy) take part in the audit exchange (UNDECIDED; default: they do not)"; the open readings of designs 06 and 07; how the repository is opened at the beta.
- Design 03 §12 (lines 915-920): **M2** "The gate — CONTROLLED, terminal-only": hook adapter, policy engine, held requests, native-prompt approvals, gated shares, liveness invariant, audit chain. Acceptance: "Sam asks, Kam approves each step in his terminal, one step is denied and provably does not run, `coagent audit verify` passes on both sides." **M3** browser console. **M4** approved trust (grants, live stream, revoke, presence). **M5** release (packaging, marketplace, `coagent doctor`, soak, private beta).
- Where the tree stands against M2 after today's merges: hook adapter, policy, liveness and deny are there (preview). Missing for M2's acceptance: session binding, held requests, the daemon learning the owner's answer, the scanner on shares, the audit log wired into the daemon, `coagent audit verify`.

### 1.8 The both-agree mode (doc 12)

- Buildable now: the policy-crate part (doc 12 §4.1): lane L1.
- Measurements the mode needs: U-B1, the sandbox probe, user-scope `ConfigChange`: lane L4.
- Design 11 needs a revision before any daemon work (doc 12 F-4, F-5, F-9, F-11, F-12, F-14) and eleven owner answers (doc 12 §5).

---

## 2. Lanes

Rule used: each lane owns files no other open lane owns. Shared files are named, and touching one outside the stated line is a STOP in both lanes.

**Shared files and the rule for each**
- Root `Cargo.toml` and `Cargo.lock`: only L2 may touch them this round (one member line; lock regenerated). Any other lane that finds it needs them: STOP.
- `BACKLOG.md`: every lane appends at the end and closes entries in the file's own form; nobody edits another line. Merge conflicts here are resolved by keeping both sides.
- `docs/DAEMON.md`: L3 owns §1 to §7, L6 owns §8. They do not run at the same time anyway.
- `crates/coagent-daemon/src/engine.rs`: L3 owns it while L3 is open. L6 starts only after L3 has merged. L2 does not touch the daemon crate at all.
- `scripts/check.sh`: nobody.

### L1 — POLICY-MODE
- **Outcome:** the permission rules can decide "approvals off" exactly as ruled, proven by tests, with no way in the tree to switch it on; and reading the inbox stops being a red card.
- **Owned:** `crates/coagent-policy/**` (except its check-owned test files), `docs/POLICY.md`, `BACKLOG.md` (append).
- **Forbidden:** every other crate; root `Cargo.toml`, `Cargo.lock`; any new dependency; the check-owned files under `crates/coagent-policy/tests/`.
- **Base:** main as it is (`32beb56`). No merge needed first: neither preview lane touches the policy crate.
- **Closes:** doc 12 §4.1 items 1-9 (with F-3, F-7, F-8, F-10, F-15 built in); A-B1 / LD-4 (the two `KNOWN_TOOLS` entries) [main: BACKLOG.md:556-560].
- **Tests in words:** the order (every earlier deny still wins); each refused class with the existing spelling corpora; every other action becomes an allow; shell only when the caller says the sandbox was verified; expiry; a generated property that the mode never weakens steps 1 to 6 and that with the mode absent the answer equals today's; eleven red controls, each red on its own assertion.
- **Size:** M. **Check tier:** 1 (security boundary).
- **UNDECIDED:** which later-running writes are refused (doc 12 Q-3) and what a whole-folder search does (Q-4): the owner. The brief builds the safe reading and lists both as open. The tier of the two entries: the coordinator (the brief says T2).
- **Foreseeable collision:** L6 will later call the new decision function from `gate.rs`. L1 must not touch the daemon; L6 must not touch the policy crate. A change either needs in the other's crate is a STOP.

### L2 — AUDIT-HOST
- **Outcome:** the signed log can live on disk under a running program: it survives a restart, and it files itself away only when the owner, a timer or the owner's own space says so.
- **Owned:** a NEW crate `crates/coagent-audit-host/**` (name is the coordinator's), `docs/AUDIT-HOST.md` (new), `scripts/red-controls-audit-host.sh` (new), ONE added member line in root `Cargo.toml`, `Cargo.lock` regenerated for that member only, `BACKLOG.md` (append).
- **Forbidden:** `crates/coagent-audit/**` (merged and checked; a needed change is a STOP), the daemon crate, every other crate, any new external dependency.
- **Base:** main AFTER the seal merge.
- **Closes:** D-S1, D-S2, D-S3; "`resume` returns with DEFAULT limits" [main: BACKLOG.md:443-447, :469-475]; the mechanical half of D5 (an API that cannot record a peer-caused event without naming the peer); the recovery path for a failed rebuild [seal: BACKLOG.md:625]. Builds DQ-S1 and DQ-S2 as settings with safe defaults.
- **Tests in words:** a file store that passes the audit crate's own store expectations; a stop after every store call of open, record, seal and release, then restart, with nothing lost and nothing accepted twice; a seal that no peer input can start, stop or make stale; the file is durable before the log forgets anything; limits after a restart equal the limits before it; a generated run of mixed events, seals and restarts compared with an in-memory run.
- **Size:** L. **Check tier:** 1 (data loss).
- **UNDECIDED:** DQ-S1 default and DQ-S2 retention (the owner). Whether provisional members take part in the audit exchange (the owner; design 08 §4, default "they do not"): not built here.
- **Foreseeable collision:** root `Cargo.toml`/`Cargo.lock` with any lane that adds a crate (none planned: STOP if one appears). L8 will later wire this crate into the daemon; L2 must not reach into the daemon to "try it".

### L3 — RELAY-RECONNECT
- **Outcome:** after the host's program restarts, the guest reconnects by itself, with nothing to paste.
- **Owned:** `crates/coagent-daemon/src/engine.rs`, `src/relay_child.rs`, `src/store.rs`, `src/datadir.rs`, `src/recovery.rs` (tests and the clock's name only), new tests under `crates/coagent-daemon/tests/` with the prefix `rr_`, `docs/DAEMON.md` §1-§7, `scripts/red-controls-daemon.sh` (append rows).
- **Forbidden:** `src/gate.rs`, `src/release.rs`, `src/release_audit.rs`, `crates/coagent-hook/**`, `crates/coagent-mcp/**`, `crates/coagent-cli/**`, `crates/coagent-relay/**` (both merged and checked: the relay already accepts a given identity).
- **Base:** main AFTER `p1p-gate` merges (lane A changed `engine.rs`).
- **Closes:** LD-3; [main: BACKLOG.md:232-236] (R1); makes G14 moot; R6-2, R6-3, R6-5.
- **Tests in words:** restart the host's relay child and then the whole host daemon: the guest reconnects with no human step and the relay's certificate fingerprint is the same; the saved identity is 0600, never logged, and a damaged one refuses the start; the old `relay.moved` path still works for a deliberately new identity.
- **Size:** M. **Check tier:** 1 (a key on disk; a human-visible behaviour).
- **UNDECIDED:** decision I-11 (the owner, per design 08 §3 item 6b). **This lane does not start until it is ruled.**
- **Foreseeable collision:** `engine.rs` and `docs/DAEMON.md` with L6: L6 waits for L3's merge.

### L4 — SPIKES (measurements, no product code)
- **Outcome:** the six host behaviours the next designs rest on are measured, each with a one-page result.
- **Owned:** new folders under `spikes/` only (throwaway, not workspace members), `docs/M0-OUTCOMES.md` (append a dated section), `BACKLOG.md` (append).
- **Forbidden:** everything under `crates/`, `preview/`, `scripts/`.
- **Base:** main AFTER both preview lanes merge (it uses their binaries and plugin template).
- **Rows:** (1) U-B1: with no allow rule, in default and in auto mode, does a hook `allow` run the call with no prompt (doc 12 F-13; LD-5); (2) may a `PreToolUse` hook change the tool input together with `allow`, and can a fixed prefix prove `SANDBOX_RUNTIME=1` and an unreadable canary inside the command (doc 12 F-6 Route P), including: can an earlier command plant the variable; (3) does the sandbox wrap `Monitor` and background commands, and does a sandbox exemption show anywhere a hook can see; (4) does switching the sandbox off inside the host fire `ConfigChange`, and is a user-scope settings edit blocked (U-B4) [main: BACKLOG.md:13-17]; (5) what does the MCP server receive that names the call or the session (LD-6; `preview/BACKLOG-PREVIEW.md` line 14); (6) do a local subagent's tool calls carry the parent's session id, and does `/clear` issue a new one (doc 12 F-24; design 11 U-B7).
- **Tests in words:** each row is a scripted run against the real host with the smallest model, its raw output kept, its result one of CONFIRMED / REFUTED / NOT MEASURABLE with the reason.
- **Size:** S to M. **Check tier:** 2 (a reviewer re-reads the raw output; no independent re-run unless a row decides a safety boundary: row 2 does, so row 2 gets a second pair of eyes).
- **UNDECIDED:** whether model runs are allowed this round and on which model (the owner's standing allowance; the live demo used the smallest model, logged). A scratch user configuration is needed for row 4 (the coordinator).
- **Foreseeable collision:** none (new folders).

### L5 — ROSTER-NOTES
- **Outcome:** the deputy's small check notes are closed, and the decision on D-2 is built the day it is ruled.
- **Owned:** `crates/coagent-roster/**` (except its check-owned test files), `docs/ROSTER.md`, `scripts/red-controls-roster.sh` (append rows).
- **Forbidden:** every other crate. `crates/coagent-audit/**` imports this crate: any change to a public item's signature is a STOP.
- **Base:** main (`32beb56`).
- **Closes:** D-4, D-5; D-3 and the shared observer list once the coordinator rules; D-2 once the owner rules (§3).
- **Tests in words:** a test that fails if `CandidateKeyInUse` is removed; the generated property reaches each refusal class at least once (counted); for D-2, the check's probes G3 and G4 turned into tests of the ruled behaviour.
- **Size:** S now, M with D-2. **Check tier:** 1 (who is a member).
- **UNDECIDED:** D-2 (the owner); D-3's bound and the edit to `admit` (the coordinator).
- **Foreseeable collision:** with L2 through the audit crate's use of roster types: public signatures stay as they are.

### L6 — GATE-BIND (second wave)
- **Outcome:** only the linked Claude Code session is gated, a read is tied to the call that asked for it, cards say truthfully who asked, and the program learns what the owner answered.
- **Owned:** `crates/coagent-daemon/src/gate.rs`, `src/release.rs`, `src/release_audit.rs`, `src/ipc.rs`, then `src/engine.rs` after L3 has merged; `crates/coagent-hook/**`; `crates/coagent-mcp/**`; `docs/DAEMON.md` §8; `scripts/test-p1p.sh`; `scripts/red-controls-daemon.sh` (append rows).
- **Forbidden:** the policy crate; the audit crates; `preview/**`.
- **Base:** main after L3 and after L4's rows 1, 5 and 6.
- **Closes:** A-B4 (session binding), P1-7, LD-2, P1-9 (as ruled), A-B3, A-B5, A-B6.
- **Tests in words:** an unlinked session is not decided at all and a stopped daemon does not block it; a witness recorded for one session cannot release a read in another; a card names the peer only when peer text is in that session's context; the owner's answer is known to the daemon and a refused read does not taint.
- **Size:** L. **Check tier:** 1.
- **UNDECIDED:** what the terminal prompt shows (P1-9, the owner); the meaning of "requested by" on a card (the coordinator, inside design 03 §5.2; the owner sees the result).

### L7 — PREVIEW-TIDY
- **Outcome:** the demo and the replay run from any folder and say plainly what a first-time user will meet.
- **Owned:** `preview/**`.
- **Forbidden:** everything else.
- **Base:** main after `p1p-demo` merges.
- **Closes:** P1-3 (the demo's folder name and anchored exclusion), B-B2 to B-B6, the REVIEW lines for LD-1, LD-4, LD-5.
- **Tests in words:** the replay passes 23 of 23 from a root under `/private/tmp` and from the project's own tools folder; each of its red rows fails on its own line.
- **Size:** S. **Check tier:** 2.
- **UNDECIDED:** nothing.

### Later waves (named so nothing is lost; not briefed here)
- **L8 DAEMON-AUDIT-WIRE:** the daemon records every decision through L2 and `coagent audit verify` exists (M2's acceptance). After L2 and L6.
- **L9 DEPUTY-WIRE:** the daemon carries admissions and uses `admit_view` (D-7). After L5 with D-2 ruled, and after L6.
- **L10 SHARE-SCANNER:** the daemon scans outgoing shares before the decision (doc 12 F-2; design 03 M2 "gated shares"). After L6.
- **L11 MODE-AGREEMENT:** rounds, consents, leases. After a revised design 11, L9, L10, and the console.
- The console (M3), trust grants (M4), packaging and Windows (M5), the connection service (n5, UNDECIDED: the owner).

### Order, and what starts today

| When | Lanes | Why |
|---|---|---|
| **Today, in parallel** | **L1**, **L2** (the moment the seal merges), **L4** (the moment both preview lanes merge), **L5** | four seats; L1 and L2 are the two with heavy runs, so they hold the two heavy slots; L4 runs no cargo suites; L5's suites are small and wait for a free slot |
| Today, small | L7, given to whichever seat is idle first after `p1p-demo` merges | an hour's work; no heavy run |
| When I-11 is ruled | L3 | blocked on the owner |
| After L3 and L4 | L6 | shares `engine.rs` with L3; needs L4's answers |
| After L2 and L6 | L8, L10 | |
| After L5 (D-2 ruled) and L6 | L9 | |

If only two seats are free: L1 and L2. If three: add L4, because its answers unblock the most (L6, the mode, the sandbox question).

Check order: L1 and L2 each get a full independent check (tier 1). L5 gets a short one. L4 and L7 are reviewed by reading, except L4 row 2.

---

## 3. D-2, the deputy liveness question (candidate card for the owner)

**The problem in plain words.** While you are away, your deputy can let in people whom another guest proposed. Each such admission points at the member list as it was when the proposal was made. The moment you change the member list for any other reason, two things stop working: a person the deputy lets in afterwards cannot start (their computer is handed an earlier admission that points at a list it never saw), and anyone who joins later refuses those earlier admissions. People's computers then disagree about who is in the session and cannot connect to each other, until you renew the deputy's seats. Nothing unsafe happens: computers refuse what they cannot check. But the deputy stops being useful after your first ordinary change. Source: [main: BACKLOG.md:624-628]; the check's probes G3 and G4 (`gate_M3_DEPUTY_verdict.md` line 20).

**The options.**

| | What happens | What it costs |
|---|---|---|
| **a. Your next change settles it** | Whenever you change the member list, you are shown the people your deputy let in and you keep or drop each one (kept people become ordinary members; the default is "keep all"). After any change of yours, no deputy admission is left hanging, so nobody is ever handed one they cannot check | Smallest build: keeping a provisional person already exists (`next_keeping`, [main: docs/ROSTER.md:417-418]); one rule changes ("admissions of the same grant stand across your next version", [main: docs/ROSTER.md:414-416]). You must answer one extra question on every change. A person you drop this way stays out for the session unless you add them yourself [main: docs/ROSTER.md:419-425]. REASONED by me from the roster document; I did not read design 06 §2.8, so the design owner should confirm it breaks nothing there |
| **b. Hand over the history** | The person who proposed (or the deputy) gives a newcomer every member list you signed since the deputy's seats were set aside, so the newcomer can check every admission fully | Full checking is kept and nothing changes for you. More to build and to bound: up to 256 lists of up to 65,535 bytes each [main: docs/ROSTER.md:265-266] instead of one list and seven admissions [main: docs/ROSTER.md:564]; the storage table and the start procedure change; a new independent check |
| **c. Accept "cannot check" with a label** | A computer that cannot check an earlier admission accepts it and marks the person "not checked by this computer" | Smallest change after (a), but it weakens the rule that every member checks every admission: a later joiner trusts the deputy and the proposer on their word for those people |
| **d. Leave it** | You renew the deputy's seats after every change | Nothing to build. Renewing drops everyone the deputy let in, and dropped people cannot be let in again by a deputy for the rest of the session; the list of dropped people holds 32 [main: docs/ROSTER.md:419-428] |

**Recommended: a.** A change to the member list means you are at your computer, which is exactly when the deputy is not needed, and it removes the unsolvable case instead of working around it. If you want people to stay "provisional" across your changes, the answer is (b), at about three times the work.

---

## 4. What the owner can see and try after this round

If L1, L2, L4, L5 and L7 land (the lanes that can start today):

- **Fewer red cards in the demo.** When an agent checks its messages, you get an ordinary card instead of the red "unknown tool" card. Sending still asks every time.
- **The demo runs from any folder** and its notes tell you up front what will ask and why a reply that mentions a protected file is refused.
- **Nothing new on screen for "approvals off".** The rules for it exist and are tested, but there is no switch yet. You can read the list of what would still be refused.
- **The log can be kept on disk and filed away** by a test program, and it survives being stopped at any moment. It is not yet connected to the running product, so you will not see log files from a demo session.
- **Six measured answers** about Claude Code, including the one that decides whether "approvals off" can be silent at all, and whether CoAgent can check your sandbox by itself.
- **The deputy's loose ends tidied**; the deputy still cannot be used in a live session.

If L3 also runs (needs your I-11 answer): **you can restart the host's program and the guest reconnects by itself.**

## 5. What is still NOT there

- **No console.** Everything happens in the terminal and in Claude Code's own prompts. No approval queue, no chat dock, no Stop/Pause buttons (design 03 M3).
- **No switch for "approvals off"**, no agreement between people, no live stream (doc 12 §4.2).
- **No trust grants**: nothing is ever allowed for a period; every call is decided one by one (M4).
- **The program does not know what you answered** to a prompt, so it asks the same thing again and keeps no record of the answer.
- **Every Claude Code session that loads the plugin is gated**, linked or not (session binding comes with L6).
- **No audit log in a live session**, and no `coagent audit verify` command (L8).
- **Outgoing messages are not scanned for secrets**; every send asks instead (L10).
- **The deputy and member invitations are not in the running program** (L9; design 08 item 6b).
- **Sessions of more than two people** are not carried by the running program.
- **No packaging**: no install command, no signed build, no marketplace entry, no `coagent doctor` for the gate (M5).
- **No Windows.** The daemon does not compile there [main: BACKLOG.md:237-241]; the Windows spikes were never run [main: BACKLOG.md:38-41].
- **No hosted relay choice**: which outside connection service to use is undecided (design 08 §4).
- **No external review, no beta.**

## 6. Candidate questions for the owner from this plan (nothing is posted)

- **Q-A (D-2).** §3. Recommend **a**.
- **Q-B (LD-1).** A reply that mentions the name of a protected file is refused. Keep that? (a) Keep it; the agent must describe the refusal without the name. (b) Allow the name, never the content. **Recommend (a)** for now: it fails safe, and the demo notes will say so.
- **Q-C (I-11).** May the host's program keep the relay's identity on disk so a restart reconnects by itself? **Recommend yes**, stored like the device key (owner-only file). I did not read I-11's own text; the card must quote it.
- **Q-D (DQ-S1).** When should the log be filed away by default? (a) Only when you say. (b) Automatically when your own space is nearly full. (c) On a timer. **Recommend (a) as the shipped default until the console exists**, (b) afterwards.
- **Q-E (DQ-S2).** How many filed-away logs are kept? **Recommend: all, nothing deleted automatically**, with the disk use shown.
- **Q-F (P1-9).** Should the terminal prompt show the whole command and inputs, or a short summary? **Recommend the whole thing**: you approve what you can see.
- **Q-G.** May the measurement lane (L4) run Claude Code with the smallest model, about a dozen short runs? **Recommend yes.**
- Doc 12 §5 carries the eleven questions about the mode (Q-1 to Q-11). Q-3 and Q-4 are the two L1 builds on a safe reading while they wait.

---
## 7. Draft build briefs for the two lanes to start first

Both are DRAFTS for the coordinator to complete and send. `<…>` marks a value only the coordinator has (a SHA at launch, start totals from its own clean-clone run). Paths are relative to the repository root. Every file:line was read at the SHA named in the brief's first paragraph.

---

### 7.1 DRAFT BRIEF — POLICY-MODE

This brief is from the coordinator. Project: CoAgent. You are a NEW seat, POLICY-MODE, with no memory of earlier seats. You work on a NEW branch `policy-mode` in a NEW worktree `worktrees/policy-mode` beside the repository, cut from `origin/main` at `32beb563837341560b908d9ba5b0a60de240d860`. Your report is a NEW file `STATUS_POLICY_MODE.md` in the project history folder. Its last line is always exactly one of: `IN PROGRESS: <what>`, `STOP Q<n> (coordinator): <question>`, `READY FOR QA POLICY-MODE`.

# POLICY-MODE: the "both agree" mode's decision steps in `crates/coagent-policy`, shipped dark

Every line number below was read at `32beb56` with `git show`. A bare `[:n]` in section 2 is a line of `crates/coagent-policy/src/engine.rs`; other files are named. If a line does not say what this brief says it does, quote it and STOP.

## 0. Start (changes no rule)
1. **Read WHOLE, in order:** the project's `CLAUDE.md`; this file; design 11 (`11_both-agree-bypass-mode-design.md`) §3 and §10.2-10.4; its review (`12_both-agree-mode-design-review.md`) §1, §3 findings F-1, F-3, F-6, F-7, F-8, F-10, F-15, and §4.1; `docs/POLICY.md` whole; `crates/coagent-policy/src/engine.rs`, `state.rs`, `known.rs`, `patterns.rs` whole. Where design 11 and its review differ, the review and this brief win.
2. **Worktree, from the remote only.** `git fetch origin`; `git ls-remote origin main` and `git rev-parse origin/main` must both print the SHA above, or a later SHA whose `git diff --stat 32beb56 <sha> -- crates/coagent-policy docs/POLICY.md` is empty. Otherwise record what you see and STOP. STOP also if the branch or the worktree folder exists.
3. **Protected files: sha256 at the start, each value recorded.** Under `crates/coagent-policy/tests/`, values read by the drafter at `32beb56`:
   - `q01_gate_attacks.rs` 368fe3eea6426af4e4550bc25d3cfdacde921ea65b0cb591efbe1aa745451550
   - `r2_gate_attacks.rs` 2169c25ac8b057b5acdddc1c404b394bc81bc4bdb00b5e02b3552bbba50ab50d
   - `r3_gate_attacks.rs` 2e3f799ed40ab505597d8df9f8ac587b6402612738fa144a297f26ad32a3f71f
   - `r4_gate_attacks.rs` 89b48198c8b1758d8ab947a216937c606fc46ee0579cb5c85bd0d1f5085a02cf
   - `r5b_bound_probe.rs` 05be31e0d9f426236eff245d660faa2021f634d03e074135da22d21c2ea44ab8
   - `r5b_r4_regressions.rs` e845c11b50a5ccd617549be1728b141619703d223cb30b7bee588ba08b75203f
   - `r5b_shell_t3.rs` b4425d8b1b0e6306106b1071da03953a39a8121381934a3682e517868e1fbddd
   - `qa_strict.rs` 75b80cad8f671e9b1c5263b4f77113d5550a7b0a48ebab4e972f763bf2dc7f6b
   - `qa_strict_m2/qa_strict.rs` 694d07c672b3dde3ebd6f7675d9a48168b72924b4d19cca86e6db56cd584bfb3
   - `qa_strict_m2/common/mod.rs` 1670356301cfdaed77bbc67114645de68aed5440348d9fee66f50f02d1338c4c
   - `common/mod.rs` e4b20635c03ebebd578dae741c64d58825e51536d8b607859b55fd8599f3fc59 (protected if any file above includes it: check and record. UNVERIFIED by the drafter.)
   - Also the two `_quarantine_*` folders of the crate: never edited, never deleted.
   Any difference: quote it and STOP.
4. **Start runs, tails recorded:** `scripts/check.sh` and `crates/coagent-policy/red-controls.sh` (47 rows at `32beb56`), each to its final line with the exit code captured in the same command. Expected totals: `<the coordinator's clean-clone figures>`. A different total or any failure: STOP.

## 1. The authority
- The owner's words for the mode, verbatim: "what I meant by bypass permission.  the same setting as in claude.  if both users agree to let the agents work, monitoring but no approval for any aciton necessary".
- The owner's rulings of 2026-11-20, verbatim options: card `general-c2c-bypass-d1-hard-refusals-1119`: "a — Yes, they all still hold". Card `general-c2c-bypass-d2-shell-in-mode-1119`: "a — Only with the sandbox on". Card `general-c2c-bypass-d3-who-agrees-1119`: "a — Every member, observers included".
- The owner's ruling of 2026-11-17 that stays true OUTSIDE the mode: every terminal command asks; no recogniser of safe shell commands is ever built.
- Method: ONE build (you), then ONE independent check. You do not merge. No deploy, no publish, no spend. The repository stays private.

## 2. The coordinator's rulings (RULED for this build)
- **R1 (dark).** This build adds a decision the tree cannot reach. No crate other than `coagent-policy` is touched; nothing constructs the mode value outside this crate's tests.
- **R2 (one new function, the old one untouched in meaning).** `decide` keeps its signature [`src/engine.rs:620`] because the protected files and the daemon call it. Add `decide_with_mode(action, state, mode: Option<&BypassView>, surface, now)`. `decide(a, s, f, n)` becomes exactly `decide_with_mode(a, s, None, f, n)`. The mode is NOT a field of `State` (review F-10).
- **R3 (the mode value).** `BypassView { consent_set_id: String, expires_at: Timestamp, bound_sessions: BTreeSet<String>, shell_verified: bool }`. No profile enum (D1 and D2 are ruled). `shell_verified` is an input the caller will compute later; this crate never computes it.
- **R4 (placement).** Two steps after [7b] [`src/engine.rs:698-703`] and before [8] [`:704-708`]:
  - **[7c]** only when `mode` is `Some`, `now < expires_at`, and `action.session_id` is in `bound_sessions`: if the assessment carries a refused class (R5) → `Deny(BypassRefused { reason })`, text "coagent: not allowed even with approvals off: <reason>".
  - **[7d]** same condition: a shell command (`Strict::Shell`, [`src/known.rs:88-90`]) is allowed only when `shell_verified` is true AND `action.tool_name == "Bash"`; any other shell command CONTINUES to [8] unchanged (it asks, as today). Everything else → `Allow(Bypass { consent_set_id })`.
  - Steps [1] to [7b] are not edited.
- **R5 (the refused classes; a closed list).** From existing reasons: `CredentialPath`, `CredentialFolder` [`:447-451`]; `CriticalSpelling` [`:452-454`]; `PermissionModeChange` [`:542-544`, `:565-571`]; `SandboxBypass` [`:545-547`]; `ShareFlaggedOrUnscanned` [`:513-517`]; `UnknownTool`, `RemoteSubagent`, `PossibleTeammate`, `WorktreeRemoval` (every `Strict` except `Shell`, [`src/known.rs:107-116`]); `Privilege` [`:553-555`]. New:
  - **may read excluded:** `a.may_read_excluded` [`:396-404`] (review F-3). INTERPRETATION, built as refused, open for the owner (review Q-4).
  - **gate-file read:** a target with a read role that matches the hard-deny set. Today the match is made only for write roles and command-text mentions [`:407-417`]; add one assessment field for the read case. It changes NO decision when `mode` is `None` (review F-7).
  - **later-running write outside the workspace or under `.git`:** `Reason::RepositoryConfigWrite` [`:421-425`] where the matched pattern's root is `Home` [`src/patterns.rs:341-361`] or the pattern is `.git/**` [`:218-222`]. Other `T3_WRITES` rows stay allowed. INTERPRETATION, built as stated, open for the owner (review Q-3).
  - **new word list** `BYPASS_REFUSED_WORDS` in `src/patterns.rs`: `coagent`, `coagentd`, `coagent-hook`, `coagent-mcp`, `claude`. Matched like `T3_PRIVILEGE` [`:551-555`]. Add no other word without a STOP.
- **R6 (the record's input).** `would_have_been(&Action, &State) -> (Tier, Vec<Reason>)`: the tier and reasons of the ordinary assessment, display-safe as a card's are.
- **R7 (the two entries).** Add `mcp__plugin_coagent_link__inbox_read` and `mcp__plugin_coagent_link__wait` to `KNOWN_TOOLS` [`src/known.rs:48-73`] as `Kind::Other`, lowest `Tier::T2`, each with a true one-line reason and its source (the MCP server in `crates/coagent-mcp`, which you read but do not edit). Update `docs/POLICY.md` §3a. Under the standing ruling "one entry per tool that exists in the tree" (`BACKLOG.md:556-560`). Close that entry and note that the preview lane's own entry for the same two tools is closed by this commit.
- **Closed list.** Each ruling names the places it permits. An edit beyond them is a STOP question, never a judgement call.

## 3. Files
**Owned:** `crates/coagent-policy/src/**`; `crates/coagent-policy/Cargo.toml` (`[features]` only: new `red_*` lines); `crates/coagent-policy/red-controls.sh` (append rows only); new test files `crates/coagent-policy/tests/t20_bypass_order.rs`, `t21_bypass_refusals.rs`, `t22_bypass_allows.rs`, `t23_bypass_expiry.rs`, `t24_bypass_property.rs`, `t25_known_own_tools.rs`; builder-owned tests `t01` to `t19` ONLY where a row for the two new entries is required (each change listed in STATUS, old line quoted); `docs/POLICY.md`; `BACKLOG.md` (append, and closing in the file's own form).
**Forbidden:** every other crate; root `Cargo.toml`; `Cargo.lock`; any new dependency; the protected files of section 0 item 3; `scripts/**`; `main`.
**Named collision:** another lane will later call `decide_with_mode` from the daemon. If you find you need a change outside this crate: STOP.

## 4. The work, in order (each item green before the next; record each step's totals)
1. Tests first: write `t20` to `t25` against the API of section 2. They do not compile yet; commit them.
2. R7 (the two entries) with `docs/POLICY.md` §3a; `t25` and `t12_docs` green. A protected file that changes colour because the two tools are no longer strict: record its failure text and STOP (do not edit it).
3. R2 and R3: the type, the new function, `decide` delegating. The whole existing suite is green with no test edited.
4. R4 and R5: [7c], [7d], the new assessment field, the word list, `AllowWhy::Bypass`, `DenyReason::BypassRefused` with display-safe texts.
5. R6.
6. `t24_bypass_property.rs`, fixed seed printed on failure, at least 200,000 generated cases: (a) for every state and action, if `decide` denies at steps [1] to [6], `decide_with_mode` with ANY mode returns the same deny; (b) with `mode = None` the two functions return equal values; (c) no refused class of R5 is ever allowed; (d) no shell command is allowed unless `shell_verified` and the tool is `Bash`; (e) an expired mode, or a session not in `bound_sessions`, returns exactly `decide`'s answer; (f) a closed, tainted link returns exactly `decide`'s answer. Print how many generated cases reached each of: a mode allow, each refused class, a shell fall-through. Each count must be above zero.
7. Red controls, one feature each, each red on its OWN assertion text and added as a row: `red_bypass_skips_hard_deny`, `red_bypass_skips_exclusion`, `red_bypass_allows_may_read_excluded`, `red_bypass_allows_credentials`, `red_bypass_allows_gate_reads`, `red_bypass_allows_untaught`, `red_bypass_allows_home_persistence`, `red_bypass_on_closed_link`, `red_bypass_shell_without_verified_sandbox`, `red_bypass_ignores_expiry`, `red_bypass_unbound_session`.
8. `docs/POLICY.md`: §2 gains [7c] and [7d]; §4 gains the word list (generated row, `t12_docs`); §10 gains every conservative choice made here; §11 gains "known limits": the word list and every shell row are text matching only.

## 5. Final tree (all before READY)
1. Merge, never rebase: `git fetch origin`; if `origin/main` moved, `git merge origin/main`; a conflict outside your owned paths: STOP. Re-run everything below on the merged tree.
2. `scripts/check.sh` exit 0, totals recorded (start against end).
3. `crates/coagent-policy/red-controls.sh` to its final line, exit code captured in the same command: every row red on its own text, the clean run green; rows 47 + 11.
4. The property run of item 6 on the final tree, reach counts recorded.
5. Every protected file byte-identical to section 0 item 3 (sha256 listed again).
6. `git diff --stat origin/main...HEAD`: every path within section 3's owned paths.
7. Dark check: `git grep -n "BypassView\|decide_with_mode" -- crates` lists files under `crates/coagent-policy/` only. Record the output.
8. A case-insensitive scan of every ADDED line for any person, account, machine, drive or client name and any home or volume path: zero hits, with a positive control (a planted string in a scratch file that the same scan finds).
9. Push the branch; record `git ls-remote origin policy-mode`; `git merge-base --is-ancestor origin/main HEAD` exit 0; read `git ls-remote origin main` again just before the last line (if it moved, back to item 1).
10. While a STOP is open the last line is that question, not READY.

## 6. Standing rules
- At most TWO heavy runs at once, machine-wide. Before each, count the running check and red-control scripts; at two, wait.
- Never delete: quarantine with a header. Never weaken, ignore or delete a test; a builder test made meaningless gets its old line quoted in STATUS and a replacement.
- Fixtures are generated inside the test or in scratch. No person's, machine's or drive's name and no real path in code, tests, docs, commits or STATUS output.
- After ANY context compaction, re-read this brief and your STATUS file WHOLE before writing anything more.
- No model runs. Network: only `git fetch`, your branch's push, and crates already in `Cargo.lock`.
- A red control is red on its NAMED property, not a side effect; no assertion on truncated text; no test depends on map order; "equivalent mutant" is a written claim.
- The owner is not asked: questions go in STATUS for the coordinator; approval-class items are a STOP. When everything is green, write READY and wait.

## 7. NOT in this build
- Any way to switch the mode on: rounds, consents, words, leases, the console, IPC verbs, wire messages.
- Verifying the sandbox (`shell_verified` is an input here).
- The secret scanner; `share_flagged` stays as it is.
- Recording, the stream, `PostToolUse`.
- Any change to what `decide` returns when the mode is absent, other than R7's two entries.
- Any change to the free-text exclusion rule, to `T3_WRITES`, to `CREDENTIALS`, or to any existing word list.
- The daemon, the hook, the MCP server, the preview folder.
- Merging, touching `main`, force-push, rebasing a pushed branch.

## 8. STATUS sections
- (1) Start: SHA, worktree command, protected hashes, start tails.
- (2) R7: the two entries, the doc rows, any builder-test row changed (old line quoted).
- (3) R2 to R6: the `pub` diff; each step's totals; the new assessment field and the proof that it changes nothing with the mode absent.
- (4) Tests: `t20` to `t25` one line each; the property's six clauses with seeds, case count and reach counts.
- (5) Red rows, each with its failure text.
- (6) Docs and BACKLOG, old and new; the two INTERPRETATIONS of R5, "built as stated, open for the owner".
- (7) Final: merge of `origin/main` (or "did not move"), totals, protected hashes, diff stat, dark check, scan, push, ls-remote, ancestor.
- (8) DESIGN QUESTIONS, STOPs, NOT DONE, disk used, processes left (none).

The last line, when all of it is done, exactly: `READY FOR QA POLICY-MODE`

---

### 7.2 DRAFT BRIEF — AUDIT-HOST

This brief is from the coordinator. Project: CoAgent. You are a NEW seat, AUDIT-HOST, with no memory of earlier seats. You work on a NEW branch `audit-host` in a NEW worktree `worktrees/audit-host` beside the repository, cut from `origin/main` at `<MAIN SHA AFTER THE SEAL MERGE>`. Your report is a NEW file `STATUS_AUDIT_HOST.md` in the project history folder. Its last line is always exactly one of: `IN PROGRESS: <what>`, `STOP Q<n> (coordinator): <question>`, `READY FOR QA AUDIT-HOST`.

# AUDIT-HOST: a new crate that keeps the signed log on disk, restarts it, and files it away only on the owner's side

Line numbers for `crates/coagent-audit` below were read by the drafter at `841c4459e5cdda0637e4df2cdf77ba133f51bd18` (the seal branch before its merge). **First act: re-read each cited line at your base SHA and record the line number you find.** A symbol that is missing or has a different signature: quote it and STOP.

## 0. Start (changes no rule)
1. **Read WHOLE, in order:** the project's `CLAUDE.md`; this file; design 10 (`10_audit-seal-and-continue-design.md`) whole, with §2.1, §2.2, §2.8 and §7 twice; design 07 (`07_audit-storage-accounting-redesign.md`) §1.3 to §1.8 and §5.3; `docs/AUDIT.md` whole (§1B is the seal); the audit lane's last verdict file; `crates/coagent-audit/src/store.rs`, `session.rs`, `segment.rs`, `anchor.rs` whole; `docs/DAEMON.md` §2 (how the daemon writes files: you copy the method, not the code).
2. **Worktree, from the remote only.** `git fetch origin`; `git ls-remote origin main` and `git rev-parse origin/main` must both print the base SHA. If not: record and STOP. STOP if the branch, the worktree folder or a folder `crates/coagent-audit-host` exists.
3. **Protected: the whole of `crates/coagent-audit/`.** Record `git rev-parse <base>:crates/coagent-audit` (the tree hash) at the start and again at the end; they must be equal.
4. **Start runs, tails recorded:** `scripts/check.sh` and `scripts/red-controls-audit.sh`, each to its final line with the exit code captured in the same command. Expected totals: `<the coordinator's clean-clone figures>`. A different total or any failure: STOP.

## 1. The authority
- The owner, card `audit-fixed-capacity-1117`, option verbatim: "Fixed capacity now, seal and continue as the next piece". Seal and continue is merged at your base.
- The owner's rulings of 2026-11-20, verbatim options: card `general-c2c-seal-is1-who-decides-1119`: "a — Only you or your settings decide". Card `general-c2c-seal-is6-own-schedule-1119`: "a — Each on their own schedule".
- The daemon preconditions this build exists to meet: D-S1, D-S2, D-S3 (design 10 §2.1, §2.2, §2.8; the three `BACKLOG.md` entries of those names).
- Method: ONE build (you), then ONE independent check. You do not merge. No deploy, no publish, no spend. The repository stays private.

## 2. The coordinator's rulings (RULED for this build)
- **R1 (a new crate, nothing wired).** `crates/coagent-audit-host`, a library with no binary. It depends on `coagent-audit`, `coagent-proto`, `coagent-crypto`, `coagent-roster` and on workspace dependencies already in `Cargo.lock`. No other crate depends on it in this build. It does not depend on `coagent-daemon`.
- **R2 (the file store).** One type implementing `coagent_audit::Store` (`put`, `remove`, `list`; [`crates/coagent-audit/src/store.rs:50-59`]). Each `put` and `remove` is durable before it returns (write to a fresh temporary file created owner-only, sync, rename, sync the directory: the method `docs/DAEMON.md` §2 "Atomic writes" describes). The directory is owner-only; a directory or file with other rights, or one that cannot be read cleanly, refuses the open (fail closed). State every bound (file count, bytes) and prove it against the audit crate's own limits.
- **R3 (open and restart).** One `open` that resumes with the kept anchor (`resume_with_anchor`, [`src/session.rs:627`]), falls back to `resume` [`:334`] only as design 10 §2.8's table allows, then re-offers the caller's limits with `try_set_limits` [`:710`] and reads `limits()` [`:814`] back. The limits in force after a restart equal the limits in force before it, or the open says exactly what differs. This closes the two `BACKLOG.md` entries "For the daemon lane: `resume` returns with DEFAULT limits" and "after `resume` the limits are the defaults".
- **R4 (recording names its causer).** The host's record call takes a `Causer` that is either `LocalHuman` or `Member(key id)`; it calls `record` [`:1559`] for the first and `record_for` [`:1576`] for the second. There is no way to record a member-caused event as local without writing `LocalHuman` at the call site (the `BACKLOG.md` entry D5).
- **R5 (D-S1, the seal's triggers, by type).** `SealTrigger` has exactly these constructors: `OwnerCommand`, `Timer`, `OwnFreePartAt(threshold)`, `OwnSeatAt(threshold)`. Nothing that carries a peer's key, a peer's seat, a requested allowance or a received message can produce one. The DEFAULT policy is `OwnerCommand` only (DQ-S1 is the owner's and is open: list it as "INTERPRETATION, built as the safe default, open for the owner"). The other three are built and tested but off unless the caller's settings turn them on.
- **R6 (D-S2, the window).** Between `seal_export` [`:2179`] and `seal_commit` [`:2280`] the host makes no other mutating call on the member. Calls that arrive in the window wait in a queue with a stated bound; when the bound is reached the caller is told `busy` and nothing is dropped silently. A `SealStale` answer is retried once from a new plan, then reported.
- **R7 (D-S3, the file first).** The plan's bundle is written durably to the archive folder, and the plan's post-seal anchor is saved as "pending" beside the current anchor, BEFORE `seal_commit`. After the commit the pending anchor is promoted and the old one dropped. A restart at any point between these steps ends in one of the states of design 10 §2.8's table, each tested. If `seal_commit` returns an error after its commit put, the host drops the member and re-opens with the pending anchor (the `BACKLOG.md` entry "a `seal_commit` whose in-memory rebuild fails AFTER the commit put").
- **R8 (DQ-S2, retention).** Sealed files are kept, never deleted by this crate. A setting `keep_at_most` exists and is parsed, and a value other than "all" is refused with a clear error in this build (the owner has not ruled). Report the disk use of the archive in the status call.
- **R9 (what a peer can cost).** Write the storage table of this crate in `docs/AUDIT-HOST.md` in design 07's form: for every file and every queue, who causes it, who is charged, its bound, what filling it can block and what it can never block. A row you cannot bound is a STOP.
- **Closed list.** Each ruling names the places it permits. An edit beyond them is a STOP question.

## 3. Files
**Owned:** `crates/coagent-audit-host/**` (new); `docs/AUDIT-HOST.md` (new); `scripts/red-controls-audit-host.sh` (new, in the form of `scripts/red-controls-audit.sh`); root `Cargo.toml`: ONE added line in `[workspace] members`; `Cargo.lock`: regenerated, and its diff must add the new package and nothing else; `BACKLOG.md` (append, and closing in the file's own form).
**Forbidden:** `crates/coagent-audit/**` and every other crate; any new external dependency (a `Cargo.lock` diff that adds any package other than `coagent-audit-host` is a STOP); any new signing domain; `scripts/check.sh` and the other runners; `main`.
**Named collision:** root `Cargo.toml` and `Cargo.lock`. No other lane may touch them this round. If `origin/main` arrives with a change to either that you did not make: STOP before merging.

## 4. The work, in order (each item green before the next; record each step's totals)
1. Re-read every cited line at the base and record it (section 0).
2. Tests first, committed before any source: the store's behaviour (every `Store` call, then a fresh process reads the same content); the open/restart rules of R3; the causer rule of R4; the trigger type of R5; the window of R6; the restart table of R7.
3. R2, the file store. Then run the audit crate's own store-facing test helpers against it where they are generic over `Store` (list which are and which are not; do not edit them).
4. R3, open and restart.
5. R4, recording.
6. R5 to R7, the seal driver.
7. **Stop-anywhere test.** A store wrapper that stops after the j-th call. For every j across: open, a mixed run of recording and receiving, a full seal (export, file, pending anchor, commit, promote), and a release: snapshot the folder, re-open in a fresh member, and assert (a) the open succeeds, (b) no numbered own record is lost or re-used, (c) the archive plus the store together verify with the audit crate's `verify_segments`, (d) re-running the interrupted step completes it.
8. **Generated property**, fixed seed printed on failure, at least 1,024 cases of at least 40 steps: the same sequence of events, seals and restarts applied to this host and to an in-memory member gives equal anchors, equal usage figures and equal exported bundles. The alphabet includes a peer that sends in every window and fills its seat; assert that it never causes a seal, never makes one fail twice, and that the number of archive files equals the number of triggers the owner's side produced. Print reach counts for: a seal, a stale plan, a queued call, a restart inside a seal, a full seat.
9. Red controls, each red on its OWN assertion text: `seal_on_peer_seat` (a peer's full seat produces a trigger), `seal_interleaved` (a received message is processed inside the window), `commit_before_file_durable`, `pending_anchor_not_saved`, `anchor_promoted_before_commit`, `resume_keeps_default_limits`, `record_peer_as_local`, `put_not_durable` (return before sync), `open_ignores_file_rights`, `queue_unbounded`.
10. `docs/AUDIT-HOST.md`: what the crate is and is not; the storage table (R9); the restart table; each INTERPRETATION "built as stated, open for the owner"; what the daemon lane must still do (rate limits D3, totals across sessions D7, delivering share-level statements).

## 5. Final tree (all before READY)
1. Merge, never rebase: `git fetch origin`; if `origin/main` moved, `git merge origin/main` (after the named-collision check of section 3). Re-run everything below on the merged tree.
2. `scripts/check.sh` exit 0, totals recorded (start against end; the difference is your tests).
3. `scripts/red-controls-audit.sh` unchanged and green as at the start; `scripts/red-controls-audit-host.sh` to its final line, exit code captured in the same command, every row red on its own text, the clean run green.
4. The stop-anywhere test and the 1,024-case property on the final tree, in release, reach counts recorded.
5. `git rev-parse HEAD:crates/coagent-audit` equals the value of section 0 item 3.
6. `git diff --stat origin/main...HEAD`: every path within section 3's owned paths; the `Cargo.lock` diff quoted whole.
7. `cargo tree -i coagent-audit-host`: no crate depends on it. Record the output.
8. A case-insensitive scan of every ADDED line for any person, account, machine, drive or client name and any home or volume path: zero hits, with a positive control.
9. Push the branch; record `git ls-remote origin audit-host`; `git merge-base --is-ancestor origin/main HEAD` exit 0; read `git ls-remote origin main` again just before the last line (if it moved, back to item 1).
10. While a STOP is open the last line is that question, not READY.

## 6. Standing rules
- At most TWO heavy runs at once, machine-wide. Before each, count the running check and red-control scripts; at two, wait. The release property run counts as heavy.
- Never delete: quarantine with a header. Never weaken, ignore or delete a test.
- Every test writes only under a scratch folder the test creates and names; never a real drive, never the user's home. No person's, machine's or drive's name and no real path in code, tests, docs, commits or STATUS output.
- After ANY context compaction, re-read this brief and your STATUS file WHOLE before writing anything more.
- No model runs. Network: only `git fetch`, your branch's push, and crates already in `Cargo.lock`. Report disk used by your scratch and target folders.
- A red control is red on its NAMED property, not a side effect; no assertion on truncated text; no test depends on map order or on timing shorter than a stated margin; "equivalent mutant" is a written claim.
- The owner is not asked: questions go in STATUS for the coordinator; approval-class items are a STOP. When everything is green, write READY and wait.

## 7. NOT in this build
- Any change to `crates/coagent-audit`.
- Wiring into the daemon; any IPC command; any network message; any announcement of a seal to peers.
- The default seal policy beyond `OwnerCommand` (DQ-S1) and any deletion of archive files (DQ-S2).
- Recording for the "both agree" mode: no mode allowance, no reserve, no new fixed slot (design 11 §5 is under revision).
- Message rate limits (D3), totals across sessions (D7), share-level statement delivery, re-anchoring, provisional members in the audit exchange.
- A `coagent audit verify` command.
- At-rest encryption of the store.
- Windows.
- Merging, touching `main`, force-push, rebasing a pushed branch.

## 8. STATUS sections
- (1) Start: base SHA, worktree command, the audit crate's tree hash, start tails, each cited line re-read with its number at the base.
- (2) R2: the store, its bounds, which of the audit crate's generic tests ran against it.
- (3) R3 and R4: the open rules, limits before and after a restart (printed), the causer type.
- (4) R5 to R7: the trigger type, the window and its bound, the file-first order, the restart table row by row with its test.
- (5) Tests: the stop-anywhere test (how many stop points, all four assertions); the property with seed, case count and reach counts.
- (6) Red rows, each with its failure text.
- (7) Docs and BACKLOG, old and new; R9's storage table; the INTERPRETATIONS.
- (8) Final: merge of `origin/main` (or "did not move"), totals, tree hash, diff stat, the `Cargo.lock` diff, `cargo tree -i`, scan, push, ls-remote, ancestor.
- (9) DESIGN QUESTIONS, STOPs, NOT DONE, disk used, processes left (none).

The last line, when all of it is done, exactly: `READY FOR QA AUDIT-HOST`

---

## Appendix: what I read, and what I could not

Read: `p1p_review/live_demo_report.md` whole; `p1p_review/gate_P1P_verdict.md` findings and merge-check lines; `m1_review/gate_M3_DEPUTY_verdict.md` findings table; design 08 whole; design 10 §0, §2.1-2.2, §7; design 03 §12 table and line 671; `BACKLOG.md` at `32beb56` lines 1-359 whole and 360-638 by title plus the entries cited; the BACKLOG additions at `b7e8da4` and `841c445`; `preview/BACKLOG-PREVIEW.md` at `ba6cdb7` (titles); `docs/ROSTER.md` §8.1-8.2 and the lines cited; the AUDIT-SEAL brief (sections 0-3, 5-8) as the model of a brief; the policy and gate source listed in doc 12's appendix; signatures in `crates/coagent-audit/src/session.rs` and `store.rs` at `841c445`.

Not read: designs 04, 05, 06 (so I-11, the 06 §2.8 deputy text and 06 §2.4 rule 3 are cited through other documents and marked UNVERIFIED); design 07 and 09 bodies; `STATUS_*.md` bodies (last lines and headings of the seal's only); the PHASE1-PREVIEW brief (its size was read, not its text; the AUDIT-SEAL brief served as the model); the bodies of lane B's backlog entries; `m1_review/gate_M3_AUDIT_SEAL_verdict.md` (the check was still running); start totals for either brief (the coordinator's clean-clone run supplies them).
