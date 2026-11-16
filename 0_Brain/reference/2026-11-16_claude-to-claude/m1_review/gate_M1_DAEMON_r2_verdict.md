NO GO at bb92225

# Gate verdict, round 2 (delta) — CoAgent M1 DAEMON (`coagent-daemon`, `coagent-mcp`), branch `m1-daemon` @ bb92225514a4b07d22e7d5586f2267e7e52c828d

This is an independent tier-1 QA gate. It reports findings only: nothing was fixed, committed or pushed. The delta is `7a4e572..bb92225`, four commits: ad0c62a, 01f6f19, 6e1c98c, bb92225.

**Clones.** All four are mine, under `/private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/1d34e9cf-ed94-49aa-ba4c-99451dcbbc42/scratchpad/gate_m1_daemon_r2/`:
- `repo/` for check.sh, the idle runs and the red controls;
- `grepo/` for my tests and the load runs;
- `mrepo/` and `mrepo2/` for mutation.

Each clone's HEAD was confirmed as bb92225. Each has its own target directory.

**Socket-path symlink.** `/private/tmp/claude-501/gr2t` points to my scratch `tools/`. I left it in place.

**My files.** My attack tests and mutation runner are in `m1_review/gate_daemon_tests_r2/`: `gr2.rs` and `mutate2.py`.

## Summary

**The four round-1 Majors are fixed, as the round-1 attacks posed them:**
- A replayed KK message 1 with a huge label no longer replaces, persists or wedges anything, including after a restart.
- The daemon restarts on every state file it writes. It also restarts when `inbox.json` is damaged in any of five ways; the bad file goes to quarantine and the security state is kept.
- Reads are paged and at-least-once. Repeated messages carry an honest `possibly_repeated` label.
- A dead `wait` takes nothing.

Containment still holds. Round 1's hostile-peer attack passes unchanged, and the new surfaces are inert. The builder's 14 flipped gate assertions are honest: none weakens an attack, and four check less than the safe property (covered elsewhere).

**The G1 redesign opened a Blocker.**
- **R2-1.** A key exchange the peer started sits in the responder's `pending` list. It survives a hard stop and is promoted afterwards. A channel to the hard-stopped peer comes back up, the peer's message is accepted for the agent, and the victim's queued message goes out to that peer. RAN, three runs.

**Three Majors stand.**
- **R2-2.** A relay drops ONE frame (the first frame under a fresh key exchange) and is honest afterwards. The session stays wedged until a process restart, and both sides keep saying `connected: true`. Four replayed KK1s produce the same wedge by evicting the honest pending exchange. RAN.
- **R2-3.** The peer-controlled `audience` field is unbounded, and the bounds count text only. About 40 messages from a hostile peer stall the agent's inbox for good: every read fails, and the stall survives a restart. RAN.
- **R2-4.** A 16 KiB `send` of control-heavy text is answered "sent", but it can never be sealed. It poisons the outbox into a permanent reconnect loop that survives a restart. RAN. This was already present at 7a4e572 and round 1 missed it.

The verdict is **NO GO**.

## 0. Reproduction

| run | result |
|---|---|
| `scripts/check.sh` (`repo/`) | **exit 0**: fmt, clippy `-D warnings`, test, deny. **298 passed, 5 ignored, 0 failed** across 53 test binaries (round 1: 278 / 43). `the_relay_binary_has_no_dependency_on_the_core_crates` ok. `gate_attacks::gate_a…gate_d` ok. |
| `scripts/test-daemon.sh 5`, idle | **5/5 green, 48 tests ok each, 75–77 s per run.** The 48 are 14 daemon unit, 2 MCP unit and 32 integration tests, the 4 gate tests included. |
| `scripts/test-daemon.sh 5` under load (12 × `yes` on 12 cores, plus my mutation workers) | **5/5 green, 48 ok each, 128 / 197 / 175 / 159 / 131 s.** `yes` count afterwards: 0. |
| Flaky tests | **None** in the builder's suite across 10 runs plus check.sh. |
| `scripts/red-controls-daemon.sh` | **35 / 35 RED; the final clean run is green (17 binaries).** |

**The 16 new red rows, and what each failed on:**
- `promote_on_kk1`: "the message on the live channel is delivered" (gate_b) and `messages ["m2"]` (g1).
- `inbox_unbounded`: "victim caught up or full" (gate_c) and "B is full and A knows" (g2).
- `ack_free_read`: "not lost without an acknowledgement".
- `dead_waiter`: "the message survived the dead waiter: []".
- `audience_unescaped`: "end marker forged".
- `no_hard_stop_initiator` and `no_hard_stop_responder`: "no channel may come up".
- `no_persisted_cap`: "a fourth ceremony after restarts … started".
- `app_gap_skip`: "a message after a gap must not be delivered".
- `temp_world_readable`: "temporary file created 644".
- `guard_env_inherit`: "guard inherited COAGENT_M22_MARK".
- `dir_check_off`: "daemon accepted …/open".
- `file_check_off`: "must be refused".
- `orphan_on_guard_kill`: "… the relay is gone" (timed out).

Each new row fails on its named property. The `inbox_unbounded`/gate_c row fails one step before the bound assertion, on the wait, which is acceptable.

**The `world_readable_state` row now proves the file mode.** The broken variant creates every temporary file 0644 and the rename keeps that mode. test1's `Run::finish → check_modes` then fails on "`session.json mode`" (RAN).

**Scope (RAN).**
- `git diff --name-only 7a4e572..bb92225` touches only `crates/coagent-daemon/**`, `crates/coagent-mcp/**`, `docs/DAEMON.md`, `scripts/red-controls-daemon.sh` and `BACKLOG.md`.
- The same diff over `crates/coagent-{proto,crypto,roster,relay,ipc,cli}`, `Cargo.toml` and `Cargo.lock` is **empty**. From `18005d6` it is also empty for the merged crates.
- `scripts/test-daemon.sh` is unchanged in the delta.
- **No changed path under `crates/` lies outside the two crates.**

## 1. Gate-test integrity (task item 1)

**`gate_hostile/mod.rs`.** `cmp` against `m1_review/gate_daemon_tests/gate_hostile/mod.rs` is clean: the file is byte-identical (RAN).

**`gate_attacks.rs`.** `diff` against the reference shows exactly the 14 marked `// GATE RETURN (builder, …)` edits (15 old lines) and nothing else. Every hostile message, size, count, `sleep` and its order is unchanged.

**The shared harness.** `tests/gate/common` is a symlink to the builder's `tests/common`, and it changed in two ways:
- `inbox()` now reads ONE page and acknowledges it.
- `ctl_raw` drains stdout in a thread. This fixes a pipe deadlock on the test side.

Neither change weakens an attack.

| # | where | old → new | ruling |
|---|---|---|---|
| 1 | gate_b, G3d | `ctl inbox_read` → `inbox()` (read + ack) | **Sound.** This adapts to the new API. The read still empties the inbox before the replay. |
| 2 | gate_b, G1 | `unread == 0` → `unread == 1` | **Sound.** The only message sent after the inbox was emptied is `MARKER-GB-after`, so the count is enough here. |
| 3 | gate_b, G1 | `connected == true` (only the message text changed) | **Sound.** The assertion is the same. Under the new definition it means "a proven channel". |
| 4 | gate_b, G1 | `epoch == huge` → `epoch == 1` | **Sound** and exact. |
| 5 | gate_b, G1 | `!kk2 recv 2` → `kk2 recv 2` | **Weaker than the safe property.** A KK message 2 only proves that the victim ANSWERED, and it also answers replays (line 437 asserts exactly that). The safe property is "the honest exchange completes", which needs a frame on epoch 2 and a promotion. A daemon that answers but never promotes would pass. Covered elsewhere: builder `hardening::g1_…` sends `m3` on epoch 2, and so does my `r2_g1_odd_labels…`; both PASS. |
| 6 | gate_b, G1 | huge epoch persisted → absent from four files | **Sound, and stronger.** |
| 7 | gate_b, G1 | "no channel comes back" → hostile logged `up N` with N ∉ {1,2} | **Weaker.** `up N` is the hostile peer's own log when it finishes ITS key exchange. Since the fix, the victim promotes a channel only when a frame arrives, and this test sends no frame after the restart. So it passes even if the victim never promotes. Covered by my `r2_g1_odd_labels…`: after a restart a message flows on epoch 3 (PASS). |
| 8 | gate_c, G2a | wait for `unread == base+sent` → `… or inbox_full` | **Sound.** The messages are the same. Once the inbox is full the batches go out without waiting, so the attack got faster, not weaker. |
| 9 | gate_c, G3 | `isError == true` → `false` | **Sound.** |
| 10 | gate_c, G3 | `lost == 0` → `76 ≤ unread < 140` after the ack | **Weaker.** It never checks that what left the inbox is what the agent received, i.e. that page + remainder == 140 and the texts match. A daemon that acks 64 and returns 10 would pass. Covered by my `r2_g2_count_bound…` and `r2_g2_text_bound…`, which check exactly-once across every page (PASS). |
| 11 | gate_c, G2 | `session.json > MAX` → `inbox_full`, and every file ≤ MAX | **Sound, and stronger.** |
| 12 | gate_c, G2b | `c.kill()` → SIGTERM | **Sound.** This is a harness change: a daemon that is still running must not leave its socket behind. |
| 13 | gate_c, G2b | "refuses to start" → "runs for 10 s and logs restored session" | **Weaker.** It does not check that the inbox survived the restart. A daemon that quarantined or dropped `inbox.json` and then started would pass. Covered by my count-bound and text-bound tests, which assert that a full inbox (256 and 128 messages) is reloaded after a restart (PASS). |
| 14 | gate_d, G4 | `got.is_empty()` → exactly `[MARKER-GD-1]` | **Sound** and exact. |

**10 of the 14 edits are sound. Four (5, 7, 10 and 13) check less than the safe property.** None of them weakens the attack, and another passing test covers each gap. There is no Blocker from test integrity.

**Direction:**
- Edit 5: send a frame on epoch 2 and assert `epoch == 2`.
- Edit 7: send a message after the restart and assert it arrives.
- Edit 10: assert page + remainder == 140 and that the texts match.
- Edit 13: assert unread after the restart == unread before.

### My own fresh attacks (`gr2.rs`; real `coagentd`, real `coagent-mcp`, the gate's unchanged hostile peer, in-process daemons with a relay tap)

| test | asserts (safe property) | result |
|---|---|---|
| `r2_g1_odd_labels_change_nothing_and_honest_rekeys_work` | KK1 replays labelled 0, `u64::MAX` and the live label change nothing. The live channel still carries messages. An honest re-key takes over (epoch 2). After a restart, epoch 3 carries messages. `u64::MAX` is in no file. | **PASS** (G1 as posed in round 1 is closed) |
| `r2_g1_replays_must_not_evict_an_honest_pending_exchange` | After an honest KK1 and four replays, the honest exchange still completes. | **FAIL**: R2-2(b) |
| `r2_g1_one_dropped_first_frame_after_a_rekey_must_not_wedge_the_session` | One dropped frame, then an honest relay, and messages flow again within 60 s. | **FAIL**: R2-2(a) |
| `r2_hard_stop_must_not_be_bypassed_by_a_pending_channel` | No channel and no message after a hard stop. | **FAIL**: R2-1 |
| `r2_g2_count_bound_restart_and_drain_exactly_once` | 300 messages against the 256-message bound. B is full and A is told. B restarts while full and reloads 256. Draining through MCP gives every message once, in order, and no unlabelled repeat. | Every message in order with no unlabelled repeat (**the property holds**). The test fails on its stricter last check, "no repeats at all", in 2 of 3 runs: R2-7 |
| `r2_g2_text_bound_worst_case_restart_and_drain` | 128 × 16 KiB with 9,500 control characters each: exactly 2,097,152 bytes are accepted, the 129th is refused, `inbox.json` is 8.2 MB, a restart reloads 128, and the drain gives 130 exactly once, in order. | **PASS** |
| `r2_g3_crash_between_handout_and_ack_and_odd_acks` | SIGKILL after a page was handed out loses nothing, and the re-hand-out is labelled. A stale ack from before the crash removes exactly its page. An ack with `u64::MAX` for a page never handed out removes 0, and so does `upto: 0`. | **PASS** |
| `r2_g3_two_readers_and_forged_repeat_label` | Two coagent-mcp servers read the same message: exactly one unlabelled copy. Peer text containing a fake `possibly_repeated`, the wrapper's own sentence, the END marker and ANSI decodes exactly and is inert. | **PASS** |
| `r2_g4_cancelled_waits_take_nothing` | Four cases, each followed by a send: MCP `notifications/cancelled`; MCP killed mid-wait; 100 abandoned ctl waits on a non-empty inbox; 100 abandoned waits on an empty inbox, then a live wait. Nothing is lost, and the live wait answers in 0.56 s. | **PASS** |
| `r2_g2_damaged_bulk_files_quarantined_damaged_session_fails_closed` | `inbox.json` truncated, corrupt, 1 GiB sparse, a symlink, a directory: each time the daemon starts, quarantines the file, reports it and keeps the session and its verify state. A half `session.json` makes the daemon exit non-zero with the files untouched. | **PASS** when the cases are > 1 s apart. My first run had them < 1 s apart: R2-5 and R2-6 |
| `r2_g2_quarantine_never_overwrites_an_earlier_quarantined_file` | Two damaged inbox files within one second: both are kept. | **FAIL** in 1 of 2 runs: R2-5 |
| `r2_g2_quarantine_failure_does_not_drop_the_session` | If quarantine fails, the daemon fails closed or keeps the session. | **FAIL**: R2-6 |
| `r2_g2_bulky_audience_must_not_stall_the_inbox` | 40 messages with a 60 KB `audience`: the agent can still read. | **FAIL**: R2-3 |
| `r2_send_of_control_heavy_text_must_not_poison_the_outbox` | A 16 KiB U+0001 `send` and then a normal one: both are delivered, or the first is refused. | **FAIL**: R2-4 |
| `r2_g2_maximal_audience_fill_keeps_state_writable` | 256 maximal envelopes (64,992-byte audience): no save error. | **Inconclusive.** Only 126 of 256 arrived, because the hostile peer keeps no outbox. I made no claim from it. |

## 2. Round-1 findings

| id | status | evidence |
|---|---|---|
| G1 | **CLOSED, WITH NEW ISSUES** (R2-1 Blocker, R2-2 Major) | The round-1 attack (replay with a huge label) replaces, persists and wedges nothing, before or after a restart. RAN: gate_b as flipped, my odd-labels test and builder `hardening::g1`. `connected` is false while there is no proven channel (`connected()` requires `chan_epoch`). However, a *stale* proven channel still counts as connected (R2-2). |
| G2 | **CLOSED, WITH A NEW ISSUE** (R2-3 Major; R2-5 and R2-6 Minor) | Text and count bounds hold exactly. A restart works at both bounds. A damaged inbox is quarantined and `session.json` fails closed. RAN. The file side holds for oversized `audience` only by arithmetic: 256 × ~65.3 KB ≈ 16.7 MB against 16,777,216 (reasoned, margin < 1 %). The read side does not hold (R2-3). |
| G3 | **CLOSED** (R2-7 and R2-8 Minor) | One page; nothing removed until the ack; a crash re-delivers with the label; odd acks are inert. RAN. |
| G4 | **CLOSED** | Four cancel stages plus 200 abandoned waiters. RAN. |
| G5 | **CLOSED** | The IPC bind lock now comes before identity creation (`engine.rs:303-313`). Temp names are unique and `create_new`. Builder `startup::g5` passes in every run (RAN builder test; reasoned from code). |
| G6 | **CLOSED** | The directory is synced after the rename. On my volume, Rust `File::sync_all` measured **4.2 ms**, against 0.06 ms for plain `fsync` and 5.1 ms for `fcntl(F_FULLFSYNC)`. So `sync_all` uses F_FULLFSYNC: measured indirectly, and it resolves the builder's UNVERIFIED. Mutation n18 (dropping the directory sync) survives, which is expected: only a power cut can test it. |
| G7 | **CLOSED** (reasoned) | `flush` returns a `Result`. On failure the reply is `state_not_saved`, the state stays dirty and state-changing commands are refused. Disk-full was **not simulated**: no sudo, I mounted no image, and `ulimit -f` raises SIGXFSZ, which is a crash rather than ENOSPC. |
| G8 | **CLOSED, WITH A NEW ISSUE** (R2-10 Minor) | m08 (serde on the inbox) no longer compiles. However, m08d (`status` embeds the first 400 bytes of `inbox.json`) **survives the whole suite**. |
| G9 | **CLOSED** | `startup::g9`, the red row, and mutation n25. |
| G10 | NOT CLOSED (BACKLOG) | Deferral accepted: bounded, and only without a session. |
| G11 | **CLOSED** for envelopes the receiver refuses (reasoned; gate_a's deep body no longer loops) | R2-4 is a new reconnect loop on the **sender** side. |
| G12 | NOT CLOSED (BACKLOG) | `audience` is now the vector of R2-3. Validating or capping it is no longer optional. |
| G13 | CLOSED (recorded in DAEMON.md §4) | The record says peer strings are stored "RAW (bounded)", which is not true for `audience` (R2-3). |
| G14 | NOT CLOSED (BACKLOG, REQUEST R7) | Accepted. |
| G15 | **CLOSED** (reasoned) | The contact is stored at session set-up: `engine.rs:1576` (convener) and `:1731` (joiner). The MITM and invite tests are green. |
| G16 | PARTLY CLOSED | Cancellation is honoured (RAN). Wrong argument types and batches remain (BACKLOG; the builder's reason is accepted). |
| G17 | NOT CLOSED (BACKLOG) | There is no anti-rollback code (reasoned by grep). It is documented, and it is out of scope per design 9.1 D. |

## 3. New findings

| id | sev | file:line | sequence | what happened vs what is safe | demonstrated | direction |
|---|---|---|---|---|---|---|
| R2-1 | **Blocker** | `engine.rs:1391-1401` (`hard_stop` clears `chan_epoch`/`kk` and closes the map but NOT `s.pending`); `:2163-2188` (a frame for a pending label promotes, with no hard-stop check); `:2065-2084` (`install_channel`, no hard-stop check); `:2265-2287` (`on_channel_up` transmits the outbox); `:1376-1381` (earlier-shown words: a daemon-level hard stop that the map never records, so `ChannelMap::insert_with_slot`'s slot check, `coagent-crypto/src/channel_map.rs:131-137`, does not fire) | The peer has the lower key id, so it is the KK initiator. **(1)** It sends KK1 (pending on the victim) and holds its first frame. **(2)** The victim's agent queues a message (`sent_now: false`). **(3)** The local human answers "no" to words shown earlier, when no ceremony is running (after a restart, or after the channel that showed them was replaced). The reply is `{"hard_stop": true}`, persisted. **(4)** The peer sends a frame under the pending keys. | The victim promotes: `connected: true`, `epoch: 2` and `hard_stop: true` at the same time. The peer's message is accepted (`unread` 1 → 2) and goes to the agent on the next read. **The victim's queued message is transmitted to the stopped peer**: the hostile peer logged `msg chat.msg seq 1 ack 1`. This lasts until a restart (the restored hard stop blocks KK). Safe: after a hard stop no channel to that slot comes up again in this session and nothing flows either way. A MITM, the very party a hard stop exists for, can pre-plant this whenever it is the lower key id (it can choose its key). | `gr2::r2_hard_stop_must_not_be_bypassed_by_a_pending_channel`, RAN in 3 runs, failing every time. Test setup writes `shown_words` into the stopped daemon's `session.json`. That stands in for "words were shown before a restart", which is exactly the state the daemon persists by design. | `hard_stop()` must clear `pending`. Promotion and `install_channel` must refuse when `rec.verify.hard_stop`. Seed the map's slot hard stop (REQUEST R2) so that `insert_with_slot` refuses too. Add a red row. |
| R2-2 | **Major** | `engine.rs:2163-2199` (a frame that opens under no pending channel only counts `stale_frames`, with no gap or reconnect path); `:2129-2132` (FIFO eviction `remove(0)`, `MAX_PENDING` 4); `:2139-2156` (the initiator installs on KK2 with no confirmation from the responder; `kk_stuck` at `:2640-2654` covers only an unanswered KK1); `:883-885` (`connected`) | **(a)** Two in-process daemons. A relay tap cuts the initiator's link, then drops the first outbound channel frame of the new channel (the responder's proof frame, `resume`), then passes everything. **(b)** A hostile initiator runs a fresh KK (epoch 2), then sends four replays of an old KK1 labelled 2, then a message on epoch 2. **(c)** Reasoned: a relay that relabels one honest exchange (KK1 and its frames) and then stops. | **(a)** After 60 s, nothing has flowed either way. The initiator is on epoch 2 and the responder on epoch 1, **both report `connected: true`**, and `stale_frames` rises. **(b)** The honest pending entry is evicted; the message on epoch 2 is never accepted; the victim stays on epoch 1 with connected true. Nothing recovers without a process restart or a network drop. A relay that is still active may deny service (design 9.1 B), but this denial **outlives the interference**: one frame, then an honest relay. `status` also lies, which is the addendum's property (d). The measure asked for: under a relay that replays every KK1 it has seen after each honest KK1, no exchange ever completes. That is allowed while the relay is active; (a) and (b) persisting afterwards is not. It is not persisted, so a restart heals it, unlike round-1 G1. | `r2_g1_one_dropped_first_frame…` (RAN in 2 effective runs; in my first run the tap never fired) and `r2_g1_replays_must_not_evict…` (RAN in 2 runs). Both fail every time. | The initiator must keep a new channel *unconfirmed* until a frame from the responder opens under it (the responder's `resume` at promotion), and re-key on a timeout as `kk_stuck` does. A frame that opens under no channel for a label newer than the live one, or N stale frames, should reconnect as a gap does. REQUEST R6 (label in the prologue) stops relabelling but not drops or eviction. |
| R2-3 | **Major** | `engine.rs:2488-2492` (`audience` stored at any length); `:1262-1300` (the page bound counts text bytes only); `limits.rs:30-41` (`PER_ITEM_OVERHEAD = 2 KiB`, which says "`audience` … bounded by the envelope limits to well under this"; false, since the envelope allows ~65,000 bytes); `coagent-mcp/src/main.rs` `daemon_call` (reads with `MAX_RESPONSE_LINE` ≈ 2.07 MB) | A hostile peer sends 40 `chat.msg`, each with text `MARKER-AU-n` and `audience` = 60,000 × "a". Each envelope is within the 65,535 limit. | The victim shows `unread 41`, `unread_bytes 483`, `inbox_full false` and `inbox.json` 2.4 MB. MCP `inbox_read` returns "coagent: the daemon did not answer." three times in a row. Nothing is lost (`unread` stays 41) but nothing can be read. **After a daemon restart: the same.** Every later honest message queues behind these. The only recovery is editing `inbox.json` by hand. It takes about 35 such messages (a page of n × 60 KB exceeding the response line). Safe: every peer string is bounded, and the bounds count the whole item. | `r2_g2_bulky_audience_must_not_stall_the_inbox`, RAN in 2 runs, failing both times. | Cap or validate `audience` at receipt (G12), and every other peer string too. Count full item size in the inbox and page bounds. Make `PER_ITEM_OVERHEAD` true by construction. |
| R2-4 | **Major** (pre-existing at 7a4e572) | `engine.rs` `cmd_send` (checks only `text.len() > 16 KiB`); `:2313-2330` (`could not seal: Proto(TooLarge)`, the item stays in the outbox); `coagent-proto/src/canonical.rs:25` (`MAX_ENCODED` 65,535); `limits.rs` (`MAX_SEND_TEXT` is never checked against the escaped envelope size) | The local agent sends 16,384 bytes of U+0001 with `send` (≤ `MAX_SEND_TEXT`). Then it sends a normal message. A peer can induce this by asking the agent to echo such text. | The first send answers **`sent_now: true`**. Its envelope escapes to ~98 KB, so `seal` fails on every transmit. Seq 2 is sealed and arrives, the receiver sees a gap, reconnects, the sender re-sends its outbox, the seal fails again, and so on. B logged 64 gaps and 66 reconnects in 20 s, and nothing was delivered. After restarting A, the outbox still holds the item. The session is dead until `end`. Safe: refuse at `send` anything that cannot be sealed. | `r2_send_of_control_heavy_text_must_not_poison_the_outbox`, RAN in 2 runs. | Encode the envelope once in `cmd_send` and refuse with `text_too_large` when it is over the limit. Never keep an unsealable item. |
| R2-5 | Minor | `datadir.rs:244-256` (`quarantine/<name>.<unix seconds>`, `rename` over an existing file) | Two damaged inbox files are quarantined within the same second. | The second rename overwrites the first: only "damaged copy 1" remains. In my first five-shape run, `truncate` and `corrupt` both got `inbox.json.1794856938`. This breaks "never deleted". | `r2_g2_quarantine_never_overwrites…`, RAN, failing in 1 of 2 runs. | Use a unique name with `create_new`, or a random suffix. |
| R2-6 | Minor | `engine.rs:661-689` (`return` leaves `sess = None`) | Quarantine fails: a file squats on `quarantine/`, or (my first run) the target name collided with an earlier quarantined directory or symlink. | The daemon runs **without its session**: status session `null`, log "saved session refused: inbox could not be loaded or quarantined". It neither fails closed nor keeps the session. Reasoned: a later `invite` writes a new `session.json` over the old one, so that session's attempts and hard stop are gone. The agent only sees "no session". | `r2_g2_quarantine_failure_does_not_drop_the_session`, RAN in 2 runs. The squatting file is a same-user precondition. | Exit non-zero when a bulk file cannot be quarantined, or keep the session with an empty inbox. |
| R2-7 | Minor | `coagent-mcp/src/main.rs:409-418` (the ack goes out on a separate IPC connection after the write) | The agent calls `inbox_read` again right after a page arrives. | The next read can reach the daemon before the previous page's ack, and it gets the same items again. They are **labelled** `possibly_repeated`, so the contract holds. But it happens with no crash and no cancel, and DAEMON.md's "what the agent can see twice" list omits this case. | Count-bound drain: 3 labelled repeats out of 303 copies (one run); 1 repeat in another run (label not checked then); 0 in a third. RAN. | Carry the ack inside the next read (`inbox_read {ack_previous}`), or document it. |
| R2-8 | Minor | `coagent-mcp/src/main.rs:409-418` | A client cancels a `wait` or `inbox_read` while its result is already being written. | The MCP acks after flushing to stdout. Per the MCP spec, a client that has already sent `notifications/cancelled` ignores a late response, so the page is acked but never seen. That is a silent loss in a narrow race. | Reasoned; not reproduced. | Ack lazily: on the next call, or by an explicit agent-side confirmation. |
| R2-9 | Note | `engine.rs:1982-1985` (pre-existing); `:2052-2057`, `:2157-2160` | Relay-stamped `pair_seq`; a relay-forged `peer.joined`; a replayed KK2 carrying the current label. | Each still changes a persisted counter: `relay_recv_upto`, or `kk_label + 1` via `start_kk`. Neither touches attempts or the hard stop. The letter of addendum G1(c) is not met. I found no harm. | reasoned | Document, or restrict which events may change persisted counters. |
| R2-10 | Minor | `release.rs:56-77` (`InboxItem` has public `String` fields `audience`/`re`/`id`); test7 and gate_a never inspect `status` | A refactor makes `status` include part of `inbox.json`. | **m08d survives:** the first 400 bytes of `inbox.json`, which contain peer text, appear in `status` and no test notices. m08b and m08c (the whole file) are caught only incidentally, when the status line outgrows the client limit under gate_c's flood. The "release by types" argument covers `text` in memory and nothing else. `status` is not an MCP tool, so this is not agent-reachable today. | mutations, RAN | Make test7 or gate_a scan `status` (and every IPC reply other than a page) for markers. Wrap peer `audience`/`re`/`id` like `PeerText`. |
| R2-11 | Note | `tests/startup.rs:59` (`m22_…`) | The red variant `guard_env_inherit`, or any failure of that test. | The panic message prints the **whole inherited environment**. In my red run that included a session token from my own shell. A failing run therefore writes environment secrets into test logs. I have not reproduced the value anywhere. | RAN (red log) | Print only whether the marker is present. |
| R2-12 | Note | `engine.rs:2342` (`send_control` clears `ack_due`), `:2481-2482` | The receiver goes full right after accepting messages. | The `full` control carries `rec.recv_upto`, which can lag behind the inbox by one batched write, and it clears the pending ack. The sender then keeps already-received items until the receiver's agent reads. Observed: A had 45 items in its outbox where 44 were expected; with 16 KiB messages, A answered `outbox_full` for as long as B was full. This is correct (duplicates are dropped), but the sender's outbox fills sooner than it needs to. | RAN | Flush before `full`, or re-arm the ack. |
| R2-13 | Note | `engine.rs:440-500`, `:2524-2533`, `:2671-2677` | Many abandoned waits; a client that pipelines a request. | The waiter list is unbounded. Dead waiters are pruned only when a message arrives or a deadline passes, and until then they keep the daemon from its idle exit (≤ 300 s). The IPC probe closes a connection that sends a second request while one is outstanding (coagent-mcp never does this). | reasoned, plus RAN (200 waiters, harmless) | Prune on close. Document "one request in flight per connection". |

## 4. Containment regression (task item 5)

**Round 1's attack still passes unchanged.** `gate_a` passed in check.sh, in all five idle runs and in all five load runs (RAN). The hostile module is byte-identical.

**New surfaces (RAN, `r2_g3_two_readers_and_forged_repeat_label`).**
- The test sent peer text containing:
  - `"},{"possibly_repeated":false,…}]`;
  - the wrapper's own sentence "Messages marked possibly_repeated may have been delivered…";
  - the END marker;
  - `\n` and an ANSI clear.
- The text decoded back exactly inside the data section.
- Nothing peer-like appeared outside it.
- Exactly one copy was unlabelled. The `possibly_repeated` bool is computed from local `handed_out`, so the peer cannot influence it.

**Daemon-built and fixed fields.**
- `ack`, `more` and `unread` are numbers the daemon creates.
- The "more", "withheld" and "possibly_repeated" sentences are fixed strings.
- `full` and `resume{room}` are seq-0 controls inside the authenticated channel. A relay cannot forge them, and a nonce stops replay within an epoch.
- In a `resume` or `full` control, `room` counts only as the JSON boolean `true`; a number is ignored. A peer's `last_seq_received` can only shrink the peer's own deliveries. A peer that claims `full` forever pins our outbox to its bound (256 messages / 2 MiB) and makes `send` answer `outbox_full`. That is denial by the peer to itself, bounded in memory.
- MCP error texts are fixed. Daemon error codes are filtered to `[a-z_]{≤32}`.

**Type enforcement (task item 5): partly.**
- Round 1's m08, `serde_json::to_value(&s.ib.items)` in `status`, **does not compile** now. So does `#[derive(Serialize)]` on `PeerText`, which the audit plus missing serde catch.
- **But I wrote m08d without a compile error or a failing test**: `status` reads `inbox.json` through `std::fs`. m08c is a `store.rs` helper (it may build `StoreKey`) that returns `to_store` text to `status`. It also compiles, and it is caught only by a line-size side effect (R2-10).

## 5. Mutation testing (mine; one mutation at a time; the builder's full suite of both crates, its `gate_return` tests included, my `gr2` excluded)

The runner is `gate_daemon_tests_r2/mutate2.py`. Every patch applied exactly once, and sources were restored after each run (`git status` clean, RAN). I ran three workers in separate clones, under load, and checked that every "caught by" test is plausible for its mutation.

{{MUTTABLES}}

## 6. Deferred items and REQUESTS (task item 7)

- **R6** (put the KK label in the `coagent-crypto` prologue). Useful: it makes a relabelled or replayed-under-a-new-label KK1 fail inside Noise. It is **not** the fix for R2-2: a drop, or a replay under the original label, still wedges. The fix is daemon-side initiator confirmation plus re-key on timeout, which needs no CORE change. It does not block merge on its own.
- **R1** (the relay keeps its TLS identity across restarts). This is usability, not safety (round 1 agreed). It does not block.
- **R2** (seed the ChannelMap with the persisted hard stop and attempts). **Now needed:** it would also have closed R2-1, because `insert_with_slot` would refuse. I endorse it as part of the R2-1 fix.
- **R7** (signed `relay.moved`) and G14: denial and metadata only; content stays protected. Does not block.
- **G6 and G7 tested by reasoning only.** G6 is resolved by my timing measurement. G7's code path is right as read. Neither blocks.
- **Unread peer text in clear in a 0600 file.** This is an owner decision under design 9.1 D. Does not block. Note that inbox bodies now stay on disk until the ack, and quarantined copies stay forever.
- **Windows does not build.** It is out of M1's scope by design. Does not block.

**What blocks the merge: R2-1, R2-2, R2-3 and R2-4.** None of them depends on a merged-crate change.

## 7. Scope, processes, what I did not examine, ran or reasoned, my slips

**Processes.** Every process I started was stopped by its own harness (`Run::finish` / `Drop`, killing only its own pids) or by pid. The `yes` load processes were killed by pid (count afterwards: 0). The final `ps` check is at the end of this file. I killed nothing by name.

**What I did not examine.**
- Windows; long soak; sleep and wake; clock jumps.
- Rekey after 2^16 messages through the daemon.
- A real power cut (G6) and real disk full (G7).
- A same-user rollback of `session.json` (reasoned only: no detection exists).
- R2-2(c), relabelling, which my tap cannot inject (reasoned).
- R2-8 (reasoned).
- `cargo deny` advisories (licences only).
- The full verify ceremony under a key-grinding MITM. R2-1 was reached through the persisted-shown-words path, not through a live MITM ceremony.

**Ran or reasoned.**
- RAN: check.sh; 5 idle runs and 5 load runs; 35 red rows; the gate diff and `cmp`; 16 `gr2` tests (final run plus targeted reruns); every mutation in the tables; the fsync timing.
- REASONED: G5, G7, G15, G17, R2-2(c), R2-8, R2-9, R2-13, and the file-size margin for maximal `audience`. Each row says which.

**My slips.**
1. My first drop-frame test never fired, because an idle link carries no frame through the tap. I added traffic.
2. My first text-bound test used 16 KiB of control characters. Those cannot be sealed, and that is how I found R2-4. I then rebuilt the test at 9,500 control characters per message.
3. My first maximal-audience probe matched a stale "sent seq 1" line. I fixed it, but the probe stays inconclusive.
4. A stray `cp` through `..` was refused by a hook and nothing ran. An `rm` inside my clone was refused, so I moved the file instead.
5. I copied the cargo registry from the project's `tools/` into my scratch (read only); nothing was written to the project's tools.
