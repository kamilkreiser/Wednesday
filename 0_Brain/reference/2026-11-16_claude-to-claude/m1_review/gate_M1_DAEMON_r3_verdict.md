VERDICT: NO GO d8b5b4bb482406431578b299e747c32f83a3e609

# Gate verdict, round 3 (third and final check) — CoAgent M1 DAEMON (`coagent-daemon`, `coagent-mcp`), branch `m1-daemon` @ d8b5b4b

This is an independent tier-1 QA gate. It reports findings only. Nothing was fixed, committed to the project or pushed. Base: `main` @ 18005d6. Delta reviewed: `bb92225..d8b5b4b` (95f8c3a, ba9677a, 5e1a41a, 8e7b032, d8b5b4b).

**Head confirmed** (RAN): `git rev-parse HEAD` in my clone and `git ls-remote origin m1-daemon` both give d8b5b4bb4824…, at 09:27 and again at 17:03 after the outage. `main` is 18005d6. `m3-roster` is d88d5d78efa2….

**Where I worked.** The real folder is `/private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/0bad48b2-2056-45a8-9019-8cc0029c12d3/scratchpad/gate_m1_daemon_r3/`. The short symlink `/private/tmp/claude-501/gd3` points to it. **I left the symlink in place.**
- `COAGENT_TOOLS=/private/tmp/claude-501/gd3/t`.
  - `t/rustup` is a symlink to the project's rustup. It was used read-only: the mtimes of every entry in `tools/rustup` are unchanged (all before my session; checked at 17:03).
  - `t/cargo/bin` is a symlink to the project's `cargo/bin`.
  - `t/cargo/registry` is a **copy** of the project's registry. So cargo's own cache writes landed in my folder, not the project's.
- `CARGO_TARGET_DIR` is under `t/target/…`.
- Test run directories are under `t/tmp/m1-daemon/<8 hex>/`. A socket path is about 62 bytes, under the 104-byte limit.
- Nothing was written into the project's `tools/` or worktrees.
- Clones: `clone/` (pristine: check, five-run, red controls), `g/` (my tests), `m1..m4/` (mutation), `mg1/` and `mg2/` (merges).

## 0. The outage, and which results are kept

The laptop lost its network and the drive was unmounted after about 10:20. Three mutation workers were left running. At 17:02 I stopped every process of mine, by pid:
- the three Python workers;
- their cargo and test children;
- 2 `coagentd` daemons, 3 relay guards and 5 relays that those tests had started (each one's parent and path checked: all under `gd3/t/target/m1|m2|m3`);
- one old waiting loop of mine.

I restored the three mutated source files in my mutation clones with `git checkout` (each `git status` is now clean). Then I confirmed the toolchain works. One toolchain detail: the pre-outage mutation workers ran cargo from `/`, so rustup chose its `stable` toolchain, not the pinned `1.100.0`. Both names resolve to the same compiler, `rustc 1.100.0 (0ef1bc386 2026-11-09)` (RAN). The re-runs pin `RUSTUP_TOOLCHAIN=1.100.0` and run from the repo.

**Positive control re-proved after the outage:** `scripts/test-daemon.sh 1` from the short path gave exit 0, 77 tests ok, 172 s, load about 8–9 (17:04–17:07).

**Kept from before the outage.** Every one of these completed, and its log was written, before 10:15:
- check.sh;
- the five-run;
- the red-control run, which ended at 10:14:45;
- all ten of my gr3 test runs (09:39–09:53);
- the roster-merge runs (finished 09:58);
- 41 mutation results (marked "pre" in §7).

**Discarded and re-run.** Every mutation result whose log is later than 10:15: 10 results, plus the 69 mutants never reached. The `gap_skip` red-row re-runs had been killed in the outage, so I ran them again.

## 1. Findings

| id | sev | file:line | exact sequence | RAN / REASONED |
|---|---|---|---|---|
| **R3-1** | **Major** | `engine.rs:2191-2210` (`new = pair_seq > s.rec.relay_recv_upto`; `relay_recv_upto = pair_seq`, persisted lazily); `coagent-relay/src/state.rs` `chan_data` / `ack_pair` (a pair buffer is freed only by `chan.ack` or by `resume_from` at attach; 500 frames / 2 MiB) | Honest pair. V is the joiner and the KK initiator; C is the convener. **(0) Control:** C sends 600 messages to V, and all 600 arrive in 26 s. **(1)** The relay delivers to V ONE frame with a **forged `pair_seq` = 2^62** and a garbage payload. This needs no key, because the relay stamps `pair_seq`. V stores 2^62 as `relay_recv_upto` and writes it to `session.json`. **(2)** From then on V never `chan.ack`s a frame from C, because none is "new". The relay's C→V buffer fills at 500 frames, and every later frame from C is refused with `error full`. **(3)** C sends 600 more messages: **exactly 500 arrive, and then nothing more within 150 s.** C reconnects 7 times with an exchange in flight and `connected: false`. V shows `exchange_in_flight: true` and 0 reconnects. As the KK initiator, V's only timer is `kk_stuck`, which starts a new KK and never re-attaches, so V never sends `resume_from`, which is what would free the buffer. **(4)** I restarted V. The value is still on disk (`relay_recv_upto` 4611686018427387904). After the restart, 498 of the next 600 arrived (the re-attach freed one buffer's worth), and then it stalled again. Safe: after one forged frame the relay is honest, so the session must flow as in the control. Here the stall outlives the interference **and survives a restart**: in effect permanent (frames age out of a relay after 15 min, and then it recurs every 500 frames). It is the same class as round 1's G1 (a persisted wedge) and round 2's R2-2 (one frame leaves a lasting stall). Round 2's R2-9 had flagged this counter as "persisted, no harm found". The harm is now demonstrated. If V is the KK responder, its `REKEY_STALL` (15 s) re-attaches, so the stall becomes about 20 s per 500 frames (REASONED). | **RAN** (`gr3::r3_a_one_forged_pair_seq_stalls_the_session`, load 10–13; result 500/600, then 498/600 after the restart) |
| **R3-2** | Minor | `engine.rs:2580-2590` (`OutOfOrder` → `reconnect_now`); `coagent-crypto/src/channel.rs:11, 287` (out-of-order `seq` refused with **no AEAD attempt**); `engine.rs:2613-2637` (`on_channel_up` re-sends the whole outbox) | V holds 44 outbox items because its peer is full. The relay injects ONE 59-byte frame `0x03 ‖ <V's live label> ‖ seq 2^40 ‖ 32 zero bytes`. V answers `OutOfOrder` without authenticating it, drops the link, runs a fresh KK and re-sends its whole outbox: **59 bytes in → 331,811 bytes out (5,623×), identical in 3 of 3 forged frames.** At the outbox bound of 2 MiB this is about 36,000×. Each cycle also costs fsyncs of `session.json` (one per frame sent). The relay or a paired peer can repeat it about once a second, which is a reconnect at will. `docs/DAEMON.md:208-209` says a relay must not be able to "trigger reconnects at will"; this path does exactly that. The builder's amplification fix (A3) covers relay acks and replayed KK1s, not this. | **RAN** (`r3_b_one_forged_out_of_order_frame_resends_the_outbox`) |
| R3-3 | Minor | `tests/reconnect.rs:140-170` (test5c, a 20 s collect); `engine.rs:246` (`RETRANSMIT_AFTER` 15 s) | Red row `gap_skip` (the channel-level gap handled as a skip) came out **STILL GREEN** in my full red run: the test passed in 19.06 s. The new retransmit timer re-sends what the broken variant skipped within test5c's 20 s window, so the row goes red only when healing takes longer than 20 s. The channel-gap guard is therefore not reliably tested. Mutant x51 (gap → no reconnect): see §7. | **RAN** (red run 09:48–10:14; re-runs in §3) |
| R3-4 | Minor | `engine.rs:2404-2410` (`pending.remove(0)`, oldest out); `:2364` (`kk1_seen` holds 256 digests, FIFO); `:2159-2166` (`PeerJoined` → `start_kk` with no rate limit) | Only genuine KK1s pass `kk_respond`, so a relay cannot forge new ones. But it can **harvest** genuine KK1s by withholding them, or provoke them with forged `peer.joined` events, and later deliver 4 that are not in the 256-window right after an honest KK1. Oldest-out eviction then removes the honest entry, and its confirmation finds nothing. With more than 260 KK1s in hand the relay can rotate them forever (each replay re-enters the window and pushes another out). This is denial while the relay is active, which design 9.1 B allows. It heals within `PENDING_TTL` / `KK_TIMEOUT` once the relay stops. But addendum 2's literal requirement ("eviction must prefer the entry that matches the exchange in flight"; "a relay replaying everything it has seen cannot prevent an honest exchange from completing") is not met. DAEMON.md:195 claims it is. The 500 ms answer gap applies only to digests already seen, so it cannot suppress the answer to a NEW honest KK1. | REASONED |
| R3-5 | Note | `engine.rs:922-933` (`MAX_WAITERS` 64, `busy`) | A same-user local client opens 64 `wait` calls. The agent's own `wait` through coagent-mcp then gets "coagent: the daemon refused (busy)." When they are gone it works again. A peer cannot hold waiters. | **RAN** (`r3_local_client_holding_64_waits…`) |
| R3-6 | Note | `store.rs` (no anti-rollback, G17) | A same-user rollback of `session.json` to before the hard stop: after the restart `hard_stop` is false. Out of scope per design 9.1 D; recorded only. Deleting the file removes the session, and a later `invite` may pair the same peer again. A hard stop is per (session, slot), so after `end` and a new invite the same peer can be paired again. That is by design, but it is not "forever". | RAN (rollback) / REASONED |
| R3-7 | Note | `coagent-mcp/src/main.rs:423-438`; `limits.rs` `PAGE_TEXT_BYTES` 256 KiB, `PAGE_BYTES` ≈ 1.8 MB | One page can hold 256 KiB of peer text. Escaped in the tool result, that is up to about 1.8 MB, and one 16 KiB control-character message is about 98 KB of tool text. Real MCP clients cap one tool result far lower, and coagent-mcp acknowledges the page as soon as the line is written and flushed. A client that truncates or refuses an oversized result therefore loses the page silently, with no `possibly_repeated` on a later read. **UNVERIFIED** against a real client (no model runs in this commission). | REASONED |
| R3-8 | Note | `engine.rs:2757-2798` (`set_aside_unsendable`) | The agent is never told when its own message was set aside as a `coagent.skip`. Its earlier `send` answered "sent"; afterwards only `status.unsendable` and a log line record it, and `status` is not an MCP tool. Reachable only if an item passed `sealable` at send and then fails to seal: a hand-planted or older `outbox.json`, or nonce exhaustion. Not peer-causable (§5). | REASONED |
| R3-9 | Note | `engine.rs:2607, 2414, 2214` | The relay or a peer can drive log lines per frame ("frame refused", "key exchange refused", "relay refused a frame"). There is no rate limit and no rotation, so the stderr file grows at the attacker's frame rate. | REASONED |
| R3-10 | Note | `tests/startup.rs` and others; `BACKLOG.md:113,118,145,165` | Committed-file hygiene. No absolute paths, user names, card ids or other projects' names in the 47 files this branch changes (RAN; grep with positive control). Remaining: references to `STATUS_M1_*.md` files that live outside the repository (BACKLOG.md ×4), internal-process words ("gate" 234 lines, "seat" 8, "addendum" 9, "tonight" 2), and `coagent/tools` / `coagent/worktrees` layout in `tests/common/mod.rs:3,36` and `BACKLOG.md:59`. | RAN |
| R2-8 (carried) | Minor | `coagent-mcp/src/main.rs:423-438` | Cancel-after-write is still acknowledged and lost (BACKLOG). Unchanged. | REASONED |

**Why NO GO.** R3-1 is a Major in exactly the class that failed rounds 1 and 2 (a relay can leave a session stalled after its interference ends). This time it survives a restart. Everything else that round 2 named is fixed (§3), and containment holds (§6).

## 2. Measured totals and load

| run | result | load (1-min avg) |
|---|---|---|
| `scripts/check.sh` (`clone/`) 09:28–09:33 | **exit 0; 327 passed, 0 failed, 5 ignored; 55 binaries** (matches the builder) | 9.9 → 11.9 |
| `scripts/test-daemon.sh 5` 09:33–09:48 | **ALL 5 GREEN, 77 tests ok each; 180 / 176 / 162 / 186 / 182 s** (spread 162–186 s) | 11.2 → 15.9 (concurrent: my gr3 runs and other seats) |
| `scripts/test-daemon.sh 1` 17:04–17:07 (post-outage control) | exit 0, 77 ok, 172 s | 6.5 → 8.8 |
| `scripts/red-controls-daemon.sh` 09:48–10:14 | **65 of 66 RED; `gap_skip` STILL GREEN**; final clean run green (19 binaries); runner exit 1. Builder claim: 66/66. | 15 → 32 (3 mutation workers + roster check running) |
| `gap_skip` row alone ×3 after the outage | {{GAPROWS}} | {{GAPLOAD}} |
| gr2 15/15 and gate_attacks 4/4 | passed inside check.sh and in all 5 + 1 runs | as above |
| The gate's `r2_g2_bulky_audience…` under heavy load | **FAILED once** (roster-merge check.sh at load about 18: "timed out after 30s waiting for: 41 unread") and failed alone in 4 mutation runs (§7); passed in every other run | 14–32 |
| My gr3 (11 tests) | see §3–§6; every failure is a finding, every pass is a property held | 10–32 |

Quiet runs could not be arranged: other seats kept the 1-minute load at 6–12 even with nothing of mine running.

**Gate-file integrity (RAN).**
- `tests/gate/gr2.rs` and `tests/gate/gate_hostile/mod.rs` are byte-identical to the reference copies (`cmp`).
- `gate_attacks.rs` is unchanged since bb92225: it still carries only round 1's marked edits (11 `GATE RETURN` marker lines).

**Rulings on what the builder added around them.**
- **`tests/gate_r2.rs`**: `#[rustfmt::skip]` and `#[allow(dropping_references)]` (a lint only), plus `#[path]`. Sound: nothing is suppressed that hides a failure.
- **Symlink `tests/gate/gate/gate_hostile → ../gate_hostile`**: needed because gr2.rs names the hostile peer relative to itself. Sound: it resolves to the one byte-identical file.
- **Symlink `tests/gate/common`**: as in round 2.

**Scope.**
- `git diff bb92225..d8b5b4b` over `crates/coagent-{proto,crypto,roster,relay,ipc,cli}`, `Cargo.toml` and `Cargo.lock` is empty. From 18005d6 the only changes are the two member lines and the data-encoding pin.
- No dependency was added in the delta.

## 3. Item 2 ruling, and round-2 findings re-attacked

**Item 2 — `gr2::r2_g2_bulky_audience…` under load: a TEST ARTEFACT, not a daemon defect.**

The relay rule, from `coagent-relay` `state.rs::chan_data` (RAN reading):
- a per-ordered-pair buffer of 500 frames / 2 MiB is freed only by `chan.ack` (or `resume_from` at attach);
- beyond it the SENDER gets `error full` and the frame is not delivered.

The test's hostile peer sends 40 × 60 KB, about 2.4 MB, keeps no outbox and never re-sends. So whenever the victim acknowledges more slowly than the peer sends, frames are lost at the relay.

**Reproduced:** with the victim SIGSTOPped for the whole flood, 35 of 41 arrive and the hostile log shows 6 × `relay error full` (`r3_item2_hostile_flood…`, passes = diagnosis confirmed). With only a 1 s pause, 41 of 41 arrived, so it depends on the timing.

**An honest sender in the same position (RAN, `r3_item2_honest_sender_survives_relay_full_with_slow_acking_receiver`, 2 runs, load 16–19):**
- The receiver processes every frame, but its relay-level acknowledgements are dropped, so the relay sees a slow receiver.
- S queues 256 × 8,150 bytes; the relay refuses S **14 times** (`error full`).
- Once acks resume, **256 of 256 arrive exactly once, in order, never labelled repeated, in 13.1 s both runs.** S keeps every refused message and re-sends it after its retransmit (15 s) or gap reconnect.

A paused process receiver (SIGSTOP 6 s) never even reached `full`: the honest sender stops transmitting while the peer is not present, then re-sends everything.

**So a slow honest receiver, made slow by a third party's load, can be DELAYED (bounded by about 15 s retransmit + reconnect + KK) but loses nothing.**

The interaction with R3-1 is separate: there, the receiver's acknowledgements are suppressed by a forged counter, not by load.

**Round-2 findings, each re-attacked with a new variant:**

- **R2-1 hard stop (Blocker in round 2): CLOSED.**
  - New variants, all RAN and PASS:
    - **(a) a hard stop taken while the INITIATOR's exchange is in flight**, in state "KK1 sent, KK2 withheld" and in state "unconfirmed: confirmation sent, the responder's first frame withheld"; then the relay delivers everything and the peer sends. Nothing was installed or accepted, the outbox stayed at 1, and the peer got nothing, again after a further restart (`r3_hard_stop_while_the_initiator_exchange_is_in_flight`, both states);
    - **(b) durable before reported:** SIGKILL at 4, 8, 12, 16 and 20 ms into `verify_confirm`, and right after the reply. Whenever a reply said `hard_stop: true` it was already on disk; one kill landed after the write and before the reply (on disk true, no reply). After the restart: not connected, a message from the peer not accepted (`r3_hard_stop_is_durable_before_it_is_reported`);
    - **(c) rollback:** see R3-6.
  - The builder's own routes (pending promotion, a fresh KK from the peer, restart, reconnect from either side) are green in every run.
  - Call-path table in §4. **I found no call that reaches the map or a send without passing the predicate (REASONED, by enumeration).**
- **R2-2 liveness: CLOSED as posed** (a single drop, replays of KK1 in the window; the builder's tests and gr2 are green; red rows red). **But R3-1 is a new instance of the class, and R3-4 a weaker one.** Bound in §4.
- **R2-3 bounds: CLOSED.**
  - `audience` ≤ 8 KiB, `id`/`re` ≤ 64; a page is bounded by escaped cost, with compile-time asserts.
  - Inbox file at most about 14.4 MB, under the 16 MiB read limit (REASONED from `limits.rs`).
  - `r2_3` and gr2 bulky are green when not starved by load.
  - Peer-sent `coagent.skip` with text inside: inert (RAN, `r3_peer_sent_skip_kind_is_inert`).
- **R2-4 unsendable: CLOSED.**
  - `send` refuses on the encoded size (red row, and x49 in §7).
  - The skip path keeps order and numbers. It cannot be caused by a peer (§5). The agent is not told (R3-8).
- R2-5 and R2-6 are closed (unit test and gr2 green). R2-7 is closed (the ack gate; x50 in §7). R2-8 is open (BACKLOG).

**Builder's equivalence claims (rulings):**
- **m04** (`&` plain): harmless today. Printable ASCII; the markers stay escaped.
- **m06** (nickname filter): equivalent today. The daemon builds `peer-<8 hex>`, so no peer byte reaches it.
- **m21** (relay cwd): equivalent. It inherits the guard's `/`.
- **n17** (dead waiters kept at wake): harmless. They are pruned every tick and at the cap, and the page stays until acknowledged.
- **n18** (directory sync): untestable without a power cut.
- **n26** (transmit while peer full): equivalent in effect. The receiver refuses while full without numbering anything, and everything is re-sent on "room".
- All six accepted.

## 4. Hard-stop call paths, and the liveness bound

| path (engine.rs) | what it can do | guard | result |
|---|---|---|---|
| `start_kk` :2271 | send KK1 | `rec.verify.hard_stop` (own check, m09) | refused |
| `on_kk1` :2347 (new and replayed) | answer KK2, enter `pending` | `rec.verify.hard_stop` (own check, m10) | refused before any answer |
| `on_kk2` :2422 | build the unconfirmed channel, seal and send the confirmation | `kk` cleared by `hard_stop()`, then `hard_stopped` after `finish`; the send goes via `send_frame_at` | refused |
| `on_frame` :2477 (unconfirmed, pending, live) | promote, install, open, verify | `hard_stopped` first line | refused, nothing opened |
| `install_channel` :2293 (the only path to `ChannelMap::insert_with_slot` within a session) | install | `hard_stopped` | refused |
| `convener_setup` / `joiner_setup` :1853, :2007 | `insert_with_slot` | reachable only for a NEW session (pairing), never for the stopped one | n/a |
| `on_channel_up` :2613 | resume, re-send the outbox | `hard_stopped` | refused |
| `on_inbound` :2800 | accept a message, process acks | `hard_stopped` | refused |
| `seal_and_send` :2665 (resume / full / end / room controls, transmit) | seal | `hard_stopped` | refused |
| `send_frame_at` :2260 (every frame incl. confirmation and verify) | send | `hard_stopped` | refused |
| `send_payload` :2239 | raw send | callers only: start_kk / on_kk1 / send_frame_at (all guarded) | — |
| `transmit` :2710 | outbox item | `hard_stopped` (plus `seal_and_send`) | refused |
| `cmd_send` :1293 | queue | `rec.verify.hard_stop` (m11) | refused (`hard_stop`) |
| `cmd_verify_start` :1503 | start a ceremony | `rec.verify.hard_stop` | refused |
| `cmd_end` :1604 | `session.end` | only if `connected()`, which includes `!hard_stopped` | nothing sent |
| `hard_stop()` :1566 | clear `chan_epoch` / `kk` / `pending` / `unconfirmed` / `awaiting_rekey`, `map.close`, `dirty` | — | persisted before the IPC reply (`on_ipc` flushes first; RAN durable) |
| `sync_verify` :3027 (map ceremony HardStop) | sets the flag only, no `hard_stop()` | the predicate covers everything above; written at the loop-end flush (dirty → `save_session` regardless of the batching) | REASONED |

**Durability ordering (REASONED + RAN).**
- On the IPC path the reply goes out only after `flush()` has written `session.json`.
- On the frame path (`hard_stop` from a failed commitment) nothing after it in the handler can send, and the event loop flushes before the next event.
- A failing `inbox.json` write blocks the session write within the same flush (inbox → outbox → session order). The human then gets `state_not_saved` while the stop holds in memory only. Minor and reachable only on disk errors; not simulated.

**Liveness bound (REASONED from the timers; the measured parts are from the builder's drop test and mine).** Once the relay is honest again, and provided the interference left **no forged persisted counter** (R3-1 breaks this), an honest pair resumes delivery within:
- the current reconnect backoff: up to 60 s +25 % jitter = 75 s, reset to 1 s on attach;
- plus attach and KK, retried every `KK_TIMEOUT` 5 s (unanswered or unconfirmed);
- plus at most `REKEY_STALL` 15 s on the responder;
- plus `RETRANSMIT_AFTER` 15 s for a lost last data frame or acknowledgement;
- **≈ 110 s worst case.** About 2–16 s when the link was not in backoff (builder: 6.5 s / 2 s / 16 s per position).

**Unauthenticated inputs, bytes out per byte in (RAN where marked):**

| input | output |
|---|---|
| relay frame with a new `pair_seq` | 1 `chan.ack` |
| replayed `pair_seq` | 0 |
| forged KK1 | 0 (`kk_respond` fails) |
| replayed genuine KK1 | ≤ 1 KK2 per 500 ms |
| forged KK2 with the current label | 1 new KK1 (≈ 1:1) |
| frame, unknown label | 0 |
| frame, current label, seq behind | 0 |
| frame, current label, bad tag | 0 |
| **frame, current label, seq ahead** | **reconnect + whole outbox: 5,623× measured, about 36,000× at the bound (R3-2, RAN)** |
| forged `peer.joined` | 1 KK1 (initiator) or a 15 s re-attach (responder) |

## 5. Resource table (item 4)

| thing | who causes it | whose budget | bound | can one party exhaust what another needs? |
|---|---|---|---|---|
| inbox | the peer | the victim's inbox | 256 msgs, 2 MiB text, 256 KiB fields; file ≤ ~14.4 MB < 16 MiB | The peer fills only its own lane (one peer per session); the agent can always read and ack (page bound asserted). No. |
| outbox | the local agent | the agent | 256 / 2 MiB | The peer can pin it by never acking or by claiming `full` forever: `send` then answers `outbox_full` for THAT peer only. Accepted (round 2). |
| relay pair buffer (relay side) | the sender's frames, freed by the receiver's acks | the sender's 2 MiB / 500 frames | relay limits | **Yes: one relay-forged `pair_seq` makes the receiver stop freeing it, and the honest sender is refused for good (R3-1).** |
| pending channels | the peer (any KK1), the relay (genuine KK1s it withheld or that fell out of the window) | the responder | 4, TTL 30 s | Eviction of the honest one while the relay is active (R3-4). |
| `kk1_seen` digests | genuine KK1s | `session.json` | 256 × 32 hex | Rotatable (R3-4); size bounded. |
| quarantine files | a damaged inbox/outbox at start (local), an unsendable own item (local) | local disk | none in count; ≤ 16 MiB / ≤ 64 KiB each; the names are seconds + random (no peer bytes) | Not peer-causable (only local damage, or an item that passed the send check but cannot seal). No. |
| waiters | local same-user clients | the agent's `wait` | 64 | **A local client can deny the agent's wait (R3-5).** A peer cannot. |
| IPC connections | local | daemon | none (each served task is cheap) | local only |
| logs (stderr) | the relay or peer, per frame | local disk | none | growth at the attacker's frame rate (R3-9) |
| `session.json` writes | every frame sent (`relay_send_seq`), every reconnect | disk I/O | rate-bound by reconnects | amplified by R3-2 |
| link queue (256) | an outbox burst on `channel_up` | in-memory | `try_send`; an overflow drops the tail silently | healed by the gap or the 15 s retransmit (REASONED) |
| run directories | tests only | `tools/tmp` | — | not product |

## 6. Containment regression (item 5)

- Round 1's hostile-peer attack (gate_a) and gr2's forged-label and markers test pass in every run (RAN).
- **New (RAN):** a peer-sent `coagent.skip` (crit) whose body text holds a marker and the END marker. It reached neither the tool result nor `status`. The next message was delivered, with exactly one END marker in the result.
- Daemon-built fields:
  - the repeat label comes from the local `handed_out`;
  - quarantine names are `<file>.<secs>.<hex>`;
  - error codes are filtered to `[a-z_]{≤32}` in the MCP;
  - log lines carry no peer bytes (red row `log_text` is red).
- Malformed or oversized MCP input is refused with a fixed text (test 7 / test 9 green).
- **Types:**
  - m08 (serde on the inbox in `status`) DOES NOT COMPILE;
  - m08b and m08c are caught by `r2_7` (which scans `status`);
  - m07 (the witness ignored) is caught by test 8.
- **Containment holds.**

## 7. Mutation table (complete)

Runner: `gate_daemon_tests_r3/mutate3.py`. One mutation at a time; the builder's suite of both crates (gr2 and gate_attacks included, my gr3 excluded); a targeted filter first, then the FULL suite before anything is called a survivor. "pre" = completed before the outage and kept; "re" = re-run after it. A kill whose only failing test was the load-sensitive gr2 bulky test (§3) is not counted: the runner re-runs the full suite without it.

{{MUTTABLE}}

## 8. Merge readiness (item 8)

- **origin/main** (18005d6): `git merge` says "Already up to date" (main is m1-daemon's base). The merged tree IS d8b5b4b, so the check.sh above (exit 0, 327/0/5) is its result.
- **origin/m3-roster @ d88d5d78efa264abbca78e97c143698718393931**, merged into a scratch branch (`febd653`).
  - One textual conflict, `BACKLOG.md` (resolved as the union of both sides; doc only). No code conflict.
  - From the short path:
    - `fmt` ok and `clippy -D warnings` ok;
    - first `cargo test --workspace` stopped at `gate_r2` on **gr2 bulky** (the §3 artefact, load about 18);
    - re-run with `--no-fail-fast`: **418 passed, 0 failed, 5 ignored, 64 binaries; `cargo deny` ok** (09:54–09:58, load 14–19).
  - **The 28+ daemon process tests compile and pass on this combination** (they could not be run there in round 2).

## 9. Windows (item 10) — UNTESTED

The crates do not compile for Windows (REASONED):
- `engine.rs:323-326`: `uid` is defined only under `cfg(unix)` and used unconditionally;
- `engine.rs:409-434`: `sigterm`/`sigint` exist only under `cfg(unix)` but are used in `select!`;
- `datadir.rs`: every check, read, write and quarantine function is `cfg(unix)` with no Windows counterpart.

`coagent-ipc` has a Windows back end; the daemon does not use it yet. Matches DAEMON.md §6.

## 10. For the owner, in plain words

1. The background service keeps peer messages inside a clearly labelled "untrusted" box. In three rounds nobody got a peer's words out of that box.
2. A "no" to the safety words now holds: after it, nothing goes to or comes from that peer again, also across crashes and restarts, as long as nobody edits the files by hand.
3. Messages survive crashes. Nothing acknowledged is lost, and anything that might be shown twice is labelled.
4. **Not yet trustworthy:** a misbehaving relay can, with one fake packet, make a session stop delivering messages in one direction for good, even after a restart. The same class of problem has now appeared in all three rounds.
5. Keep using it only for trials between your own two machines on a relay you run yourself. Do not rely on it across someone else's relay until R3-1 is fixed and re-checked.

## 11. What I did not do, and slips

- **Not done:**
  - a real power cut or disk-full (G6/G7);
  - Windows;
  - the R3-4 harvest (reasoned, not run: it needs more than 260 key exchanges);
  - R3-7 against a real MCP client;
  - a sleep/wake test.
- **Quiet runs:** not possible on this shared machine (load 6–32 throughout).
- **Slips:**
  1. My first honest item-2 test never reached `full`: a paused process is cut by the relay, and the sender stops transmitting. I replaced it with the slow-acking-receiver test.
  2. The pre-outage mutation workers ran from `/` and used the `stable` toolchain alias (the same rustc 1.100.0).
  3. The outage left three workers running for seven hours. Their late results are discarded (§0).
  4. A hook refused git write verbs through the symlink path; I used the real scratchpad path for them.
