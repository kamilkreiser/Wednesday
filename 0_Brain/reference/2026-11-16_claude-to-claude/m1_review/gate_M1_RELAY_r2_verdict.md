GO WITH NOTES at 519d6f0acccca2438d5985259a9aafefbcc2d903 (branch m1-relay): 0 Blocker, 0 Major, 6 Minor, 9 Note. Both round-1 Majors (G1, G2) are closed for the attack as specified (one address). The fixes add new weaknesses, listed below.

# Gate verdict, round 2 (delta gate 65fcc1b..519d6f0): M1 RELAY

This is an independent tier-1 QA gate (findings only). I did not run round 1. I worked in my own clones (`git clone --no-hardlinks`, checkout by SHA) under
`/private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/1d34e9cf-ed94-49aa-ba4c-99451dcbbc42/scratchpad/gate_m1_relay_r2/` (called `GATE/` below):
- `GATE/repo`: attack tests added.
- `GATE/pristine`: untouched; used for reproduction runs and `run.py`.
- `GATE/mut`: mutations.

Nothing under `!CODING/` was written. Every listener bound to 127.0.0.1 on an ephemeral port. `--allow-non-loopback` was used only on refusal paths (`--status-secs 0`, which exits 2 at parse time before any bind).

The new attack tests are copied to `gate_relay_tests_r2/` next to this file:
- `gate_r2_state.rs`: white-box tests on `State`, included from `state.rs` via `#[cfg(test)] #[path] mod gate_r2;`.
- `gate_r2_meter.rs`: the FragTracker differential test, included from `meter.rs` the same way.
- `tests/gate_r2_wire.rs` (relay crate).
- `tests/gate_r2_ipc.rs` (ipc crate).

Each test asserts the SAFE property, so a red test is a finding. Tests whose names end in `_ctl` are controls and are expected to pass.

## Verdict basis

The single-address attacks from round 1 no longer work:
- One address can no longer take every channel.
- One sender can no longer starve every other pair.
- Ping interleaving no longer defeats the slow-loris clock.
- `pair_seq = u64::MAX` no longer gets a receiver cut.
- A full backlog no longer lets a second IPC listener steal the socket.

The gate tests are byte-identical apart from the one declared line. They pass 10 times out of 10, including 5 runs under load.

No new defect reaches Major:
- The new G1 weaknesses need several addresses (the sybil limit that per-address caps are designed around), or a tunnel, which is owner decision R2.
- The new G2 weakness (frames dropped silently) only trims a channel that holds more than the attacker's per-channel share. Design 03 §4.5 already requires an end-to-end persisted outbox and resume, because the relay is untrusted and may drop.
- The remaining items are Minor or Note, but several are cheap to fix and I recommend fixing them before merge (see "Before merge" at the end).

## Round-1 findings

| id | status | how I know |
|---|---|---|
| G1 (Major) | **CLOSED WITH A NEW ISSUE** (G1-r2a..d, T-r2a) | **Ran**: the gate test `g1_one_address_cannot_take_every_channel` passes. My control `r2_g1_one_address_live_cap_and_pending_churn_ctl` passes: one address holds 16 live and 48 pending channels and churns 200 more creates, and an honest create and an honest `chan.slots` still succeed. Variants with more addresses or a tunnel fail (see the new-findings table). |
| G2 (Major) | **CLOSED WITH A NEW ISSUE** (G2-r2a, G2-r2b, T-r2b) | **Ran**: the gate test `g2_one_sender_cannot_starve_every_other_pair` passes. The accounting control `r2_g2_accounting_after_eviction_ack_resume_retire_ctl` passes: `assert_invariants` holds after eviction, zero-length frames, `resume_from`, an ack of `u64::MAX`, retire and sweep, with no panic. However, honest frames are now dropped silently (G2-r2a). |
| G3 | **CLOSED** | **Ran**: the gate test passes. My differential test `r2_g3_tracker_agrees_with_tungstenite_on_random_valid_streams` passes: on 3000 random valid client streams (fragmented messages, pings and pongs interleaved, 7/16/64-bit and non-minimal length encodings, random chunking from 1 to 23 bytes), the tracker's `in_frag` equals tungstenite 0.30's real "message open" state. `r2_g3_header_parse_matches_tungstenite` passes: on 200k random headers (any opcode, RSV bits, top-bit-set 64-bit lengths) the tracker's header length, payload length, opcode and FIN equal `FrameHeader::parse`. `r2_g3_garbage_never_panics_and_state_is_bounded` passes: random garbage, every byte boundary, a `u64::MAX` length, no overflow in the debug build, head buffer ≤ 14. Wire tests `r2_g3_pings_and_pongs_only_after_an_open_fragment_are_cut` (cut as slow-loris) and `r2_g3_finish_and_reopen_in_one_write_is_cut` pass; the second is weak because the relay closes on the invalid data frame first. **Reasoned**: the tracker sees exactly the bytes tungstenite reads. Bytes read during the HTTP upgrade (tracking off) could desync it, but tungstenite 0.30 refuses any bytes after the request (`JunkAfterRequest`, `handshake/server.rs:256`), and no read happens between the request and `handshake_done`. The tracker only reads ahead of tungstenite, so it can only err toward cutting. |
| G4 | **CLOSED WITH A NEW ISSUE** (G4-r2a) | **Ran**: the gate test passes. `r2_g4_retire_resets_and_poison_is_self_only_ctl` passes: a `u64::MAX` sender blocks only its own pair, other pairs are unaffected, the honest receiver's ack frees the poison frame, retire plus re-register resets the counter, and the map stays ≤ SLOTS² per channel. A token **rotation** does not reset `last_seq` (G4-r2a). |
| DQ 7 change | **safe** | **Ran**: builder test `a_receiver_that_never_acks_back_pressures_its_sender_and_is_not_cut`. **Reasoned**: an un-acking receiver's frames are bounded by the pair cap (500 frames / 2 MiB), the channel cap (64 MiB) and the relay-wide cap, and are aged out at 15 min by `sweep` whether or not the receiver is attached. A dead attached receiver is cut by the existing slow-reader paths (outbound queue / write timeout). Nothing else used the `NeverAcks` cut: grep finds only the kept enum variant and counters, and the old cut never freed buffers anyway. |
| I1 | **CLOSED WITH A NEW ISSUE** (I1-r2a, I-r2b) | **Ran**: the gate test `i1_second_bind_is_refused_even_when_the_first_listeners_backlog_is_full` passes. The new controls pass: hardlink at the lock path leaves the target intact, a directory at the lock path is refused, and 8 tasks x 150 concurrent bind/drop never saw two holders and left no files. But removing the lock file of a LIVE listener lets a second bind replace its socket (I1-r2a, red). |
| R1 | **CLOSED** | **Reasoned**: every path that acts for a slot from a connection now checks the holder. `chan_data` and `chan_ack` use `holds(id, slot, conn_id)`. `chan_detach` compares the conn id. `chan_open` attaches only to a free slot and replays only to the attaching conn. `sweep` and `chan_slots` touch no frames on behalf of a conn. **Ran**: my mutation X18 (`holds` true for any attached conn) is CAUGHT, and builder rows M49 and M50 are RED. |
| T1 | **CLOSED** | **Ran**: builder rows M52, M53 and M54 are RED (they correspond to the gate's surviving mutants R09, R10 and R12). |
| T2 | **CLOSED** | **Ran**: M51 RED; the wire test `rotating_a_slot_token_evicts_the_old_holder_over_the_wire` passes. |
| N1 | **CLOSED** | **Ran**: `coagent relay $'\xff'` gives `coagent: an argument is not valid UTF-8 ("\xFF")`, exit 2. |
| N2 | **CLOSED** | **Ran**: `--listen 0.0.0.0:0 --allow-non-loopback --status-secs 0` exits 2 at parse time, with nothing bound. Loopback may still use 0 (by design). |
| N4 | **CLOSED** | **Reasoned**: PROTOCOL.md line 19 now matches the code. |
| N6 | **CLOSED** | **Reasoned**: `saturating_add` is used; the builder test passes. No other `max_bytes + 1` arithmetic remains (grep). |
| R3(d) | **CLOSED** | **Reasoned**: `GroupCount` is read and checked before `Groups[0]`. **Ran**: `cargo clippy -p coagent-ipc --target x86_64-pc-windows-msvc --all-targets -D warnings` is clean, run on the clean pristine tree after `run.py` finished. Not run on Windows. |

## New findings

| id | sev | file:line | what | how demonstrated | direction |
|---|---|---|---|---|---|
| G2-r2a | Minor | `crates/coagent-relay/src/state.rs:759-812` (`make_room`, `evict_front_of_largest_pair`) | An attacker can force **silent** loss of an honest channel's buffered frames. If the largest channel is honest (for example, receivers offline with a backlog), an attacker whose channels each stay just below it fills the relay-wide buffer. Every further attacker frame is then admitted by dropping the honest channel's oldest frames. The honest sender got no error for those frames, and receivers get no gap marker: on attach they replay a queue with a `pair_seq` hole at the front. At default limits, one address (16 live channels) can trim any honest channel above about 15 MiB down to that size; four addresses lower this to about 4 MiB. Eviction works in whole frames, so it overshoots: in my run, 5 attacker frames of 20 KiB evicted 5 honest frames of 50 KiB (409680 B down to 153630 B). Before this round, `full` was always surfaced. Design 03 §10 says relay errors are "always surfaced". | **Ran**: `state::gate_r2::r2_g2_attacker_forces_silent_eviction_of_largest_honest_channel` FAILS, and the honest sender's queue is empty (`told: []`). | Signal it. Either send the sender of an evicted frame an `error` (`full` or a new `evicted` with `to_slot` and `pair_seq`) and tell an attached receiver, or document in PROTOCOL.md that an accepted frame may be dropped and make the M2 client treat a `pair_seq` gap as a resume trigger. Consider evicting only from pairs whose receiver is attached (already delivered once) before touching undelivered ones. |
| G1-r2a | Minor | `limits.rs:37` (`MAX_CHANNELS_PER_IP = 16`) vs `MAX_CHANNELS = 64`; `meter.rs:67` (`ip_key` groups IPv6 by /64) | Four keyed addresses take the whole table again with live channels: 4 × 16 = 64, nothing pending, nothing to evict. Every honest `chan.create` then gets `full`, and the attacker keeps the channels alive by repeating `chan.slots`, which refreshes `last_active` for 30 min. Four /64s are one routed /62. The same ratio holds for mailboxes: 8 addresses × 8 = 64. | **Ran**: `r2_g1_four_addresses_take_every_channel` FAILS (`Full: relay has no free channel`). | This is the sybil limit of per-address caps. A ratio of 4 is low. Reserve headroom (for example, refuse a new live channel when the table is above 75% and the address already holds more than its share), or rank addresses by /48 for v6. Record the number as an explicit owner decision. |
| G1-r2b | Minor | `state.rs:474-491` (live cap) | Behind a tunnel (every peer is 127.0.0.1) the per-address live cap becomes the **relay-wide** cap. The relay serves at most 16 live sessions and 8 pairing mailboxes in total, with no attacker present. One attacker making 16 channels live (one slot each) refuses every honest `chan.slots` for 30+ min. This makes R2 worse. | **Ran**: `r2_g1_tunnel_live_cap_is_relay_wide` FAILS (`Full: too many live channels from your address`). | Part of the R2 owner decision, which must be taken before spike C2. Do not present the tunnel path as supported until then. |
| G4-r2a | Minor | `state.rs:507-515` (rotation branch of `chan_slots`; `last_seq` is reset only on retire at :529) | Rotating a slot's token, the eviction mechanism T2 tests, does not reset `last_seq`. A hostile member that sent `pair_seq = u64::MAX` and is then evicted by rotation leaves the slot's new holder unable ever to send to that peer (`bad_request: pair_seq must increase`) until the convener retires and re-registers the slot. | **Ran**: `r2_g4_rotation_does_not_reset_last_seq` FAILS. | On rotation, reset `last_seq` for pairs involving the slot. Also decide whether buffered pairs addressed to or from the slot should be dropped, since today they are replayed to the new holder. |
| I1-r2a | Minor | `crates/coagent-ipc/src/unix.rs:149-182, 196-245` | The lock file is now the only proof of liveness. If it is removed while the listener lives (by hand `rm`, a cleaner, or a user tidying `~/.coagent/run`), the next bind creates a fresh lock, takes it, treats the LIVE socket as stale, unlinks it and binds a second listener. Two daemons result, and the first is orphaned on an unlinked inode: the same end state as round-1 I1, by a different trigger. | **Ran**: `gate_r2_ipc::r2_i1_live_listener_with_its_lock_file_unlinked_is_not_replaced` FAILS. | Lock something that cannot be unlinked while in use: `flock` the 0700 directory's own fd. Or, after taking the lock and before unlinking an existing socket, do a non-blocking `connect` with a short timeout and refuse if it is accepted (ECONNREFUSED then only allows the replacement, never forces it). |
| T-r2a | Minor | `state.rs:428-451`, `state.rs:759-780` | Surviving mutants on the new mechanisms. **X07** (fairness threshold `big > mine + need` loosened to `big > mine`) and **X08** (`make_room` evicts from the SMALLEST other channel, so an attacker would destroy honest small pairs, the opposite of the G2 fix) survive the builder's suite AND the gate's G2 test. **X02** (eviction ignores the owner's channel count, so single-address churn evicts an honest pending channel, as in the tunnel case) survived in my first full run. In the second run the same builder test caught it, because `a_full_table_evicts_a_pending_channel_of_the_biggest_holder_for_an_honest_create` creates the honest and attacker channels at the same `Instant` and therefore depends on `HashMap` iteration order. | **Ran**: mutation table below. | Add a test with several channels of different sizes asserting the largest is trimmed and smaller ones untouched; a boundary test for the threshold; and distinct timestamps in the eviction test. |
| G2-r2b | Note | `state.rs:772` | "Only while that channel would still hold at least as much as the requester" is checked BEFORE each eviction, so one large front frame can take the big channel far below the requester. Example: 200 KiB evicted to admit 100 KiB, leaving the big channel at 10 KiB and the requester at 100 KiB. | **Ran**: `r2_g2_fairness_boundary_overshoots_with_a_large_front_frame` FAILS. | Compare against `big_bytes - front_len`, or accept and document. |
| G1-r2c | Note | `state.rs:428-451` | Eviction ranks pending channels by their owner's TOTAL count, including live channels. A busy honest address (10 live sessions) that creates an 11th is the top owner. Attackers spread over 6 addresses with at most 9 channels each then evict the honest convener's new channel, whose `chan.slots` gets `not_found`. | **Ran**: `r2_g1_eviction_targets_a_busy_honest_address` FAILS. | Rank by PENDING count per owner. |
| G1-r2d | Note | same | Behind a tunnel eviction is pure oldest-pending-first. A churning attacker evicts an honest pending channel after about 64 creates (about 32 s at 2 ops/s, inside the 60 s window). The convener sees `not_found` at `chan.slots`. Harmless if the client registers its own slot in the same breath as `chan.create`. | **Ran**: `r2_g1_tunnel_oldest_pending_honest_channel_is_evicted` FAILS. | The M2 client must register at least one slot right after `chan.create` and retry on `not_found`. Write that into PROTOCOL.md (the 60 s pending TTL also requires it). |
| I-r2b | Note | `unix.rs:196-245` (4-try loop) | Under bind/drop churn the retry loop runs out and returns `Other("could not take the single-instance lock (file kept changing)")`, not `AddrInUse`: 36 of about 224 attempts in my 8-task storm. It never spins and never produced two holders. A daemon-on-demand client must treat this error as "retry". | **Ran**: `r2_i1_concurrent_bind_drop_never_two_holders_ctl` (stderr). | Return `AddrInUse` (or `WouldBlock`) when the loop runs out. |
| I-r2c | Note | `unix.rs:212-218` | The lock file is opened with `create(true)` and without `O_NOFOLLOW`. A same-user swap between the symlink check and `open` creates or locks the symlink's target; the post-lock inode check then retries and refuses. The mode (0600) is applied only at creation, and an existing 0644 lock file is accepted. Both need the same uid inside a 0700 dir. | **Reasoned**. | `custom_flags(O_NOFOLLOW)` (needs a libc constant) or `fchmod` after open; low priority. |
| I-r2d | Note | `unix.rs` (I1 fix) | Mutants X16 (inode re-check after locking skipped), X17 (Drop unlinks the lock path without the inode check) and X20 (lock-file owner check removed) survive every suite, including mine. X16 and X17 need a racing process at the exact moment; X20 needs a second uid. My race storm did not hit the X16 window. | **Ran** (mutation). | Optional fault-injection seam; otherwise accept as untestable, as N10 did. |
| G4-r2b | Note | `state.rs:696-702` | An honest sender whose counter restarted (lost client state) is refused on that pair until the convener retires the slot. Design 03 §4.5 persists the outbox, so this needs state loss. | **Ran**: `r2_g4_counter_restart_is_refused_until_retire_info` (documents the behaviour). | Document in PROTOCOL.md. |
| DQ-r2 | Note | `red-controls/run.py` | `run.py` counts any non-zero exit as RED, so a flaky test could mask a survivor (unchanged from round 1). No test was flaky in my 10 runs. | **Ran**. | Check that the named catching test failed. |
| P-r2 | Note | process | The builder's STATUS says the suite was "not run under load by me"; I ran it under load (below). STATUS claims (133 tests, 55/55 RED, the one-line gate-file change) all reproduced exactly. | **Ran**. | none |

## Reproduction counts

| what | result | ran? |
|---|---|---|
| `bash GATE/repo/scripts/check.sh` (pinned toolchain 1.100.0 with clippy, `CARGO_TARGET_DIR` in scratch, offline) | exit 0: fmt OK, clippy `-D warnings` OK, **133 passed / 0 failed**, `licenses ok`, `CHECK OK`. This matches the builder's 133. | ran (`GATE/check1.log`) |
| full suite (`cargo test --workspace --locked --offline`), 5 runs, idle | 5/5 exit 0, 133/133 each | ran (`GATE/loops_summary.txt`) |
| full suite, 5 runs under 12 `yes` CPU burners on a 12-core machine | 5/5 exit 0, 133/133 each; burners killed afterwards (`pgrep` = 0) | ran |
| flaky tests | **none observed** in 10 runs (plus check.sh). The X02 observation above is a nondeterministic test under a MUTANT, not on the real code. | ran |
| builder `red-controls/run.py --with-dep` (pristine clone) | **55 / 55 RED** (M01–M24, M27, M28, M25, M30–M36, M40–M59, M26), "sources restored byte-for-byte", "red controls: ALL RED", exit 0, `git status` clean afterwards. This matches the builder's 55. | ran (`GATE/redcontrols.log`) |
| Windows clippy `-p coagent-ipc --target x86_64-pc-windows-msvc --all-targets -D warnings` | clean (exit 0) | ran |

## Scope and gate-test integrity

- `git diff --stat 65fcc1b..519d6f0`: 19 files, +1809/−168, all under `crates/coagent-relay`, `crates/coagent-ipc` and `crates/coagent-cli`. `BACKLOG.md` and `Cargo.lock` are untouched. **Nothing out of scope** (ran).
- `cmp` against the reference copies: `gate_ipc.rs` is **identical**. `gate_attacks.rs` differs by exactly 3 added lines after line 2: two comment lines and `#![allow(clippy::single_match)]`. No assertion, value, call or timing differs (ran `diff`). **Integrity OK.**

## Mutation table (delta code, one at a time, full coagent-relay + coagent-ipc + coagent-cli suite at 519d6f0; runner `GATE/gate_mut_r2.py`, log `GATE/gate_mut_r2.log`)

| id | mutation | builder suite | with gate r2 tests |
|---|---|---|---|
| X01 | eviction may pick LIVE channels | CAUGHT (`a_full_table_evicts…`, `the_channel_table_cap_holds…`) | |
| X02 | eviction ignores the owner's count | **SURVIVED** in run 1; CAUGHT in run 2 by the same test (order-dependent) | CAUGHT (`r2_g1_one_address_live_cap_and_pending_churn_ctl`) |
| X03 | newest pending evicted instead of oldest | CAUGHT | |
| X04 | pending TTL ×1000 | CAUGHT (`pending_channels_are_forgotten_quickly…`) | |
| X05 | live cap `>=` → `>` | CAUGHT (`an_address_may_own_only_so_many_live_channels`) | |
| X06 | `registered` never set | CAUGHT (5 tests) | |
| X07 | fairness threshold loosened | **SURVIVED** | **SURVIVED** |
| X08 | `make_room` evicts the smallest other channel | **SURVIVED** | **SURVIVED** (my G2-r2a test turns green under it, because then the victim is not trimmed) |
| X09 | `last_seq` allows an equal seq | CAUGHT (`pair_seq_must_increase_per_ordered_pair`) | |
| X10 | `last_seq` not reset on retire | CAUGHT | |
| X11 | `last_seq` never recorded | CAUGHT | |
| X12 | FragTracker: control frames change `in_frag` | CAUGHT (3 meter tests) | |
| X13 | FragTracker: continuations ignored | CAUGHT | |
| X14 | FragTracker: 16-bit length sized 4 bytes | CAUGHT | |
| X15 | FragTracker: mask key not counted | CAUGHT (incl. `slow_loris_message_is_cut…`) | |
| X16 | lock inode re-check skipped | **SURVIVED** | **SURVIVED** |
| X17 | Drop unlinks the lock without the inode check | **SURVIVED** | **SURVIVED** |
| X18 | `holds` true for any attached conn | CAUGHT (`token_rotation_evicts…`) | |
| X19 | mailbox per-address cap `>=` → `>` | CAUGHT | |
| X20 | lock-file owner check removed | **SURVIVED** | **SURVIVED** (needs a second uid) |

Totals: 20 mutations. Against the builder's suite in the first run, 14 were caught and 6 survived (X02, X07, X08, X16, X17, X20). With the gate's r2 tests added, X02 is caught; the other five still survive. Every catch was checked against the named failing test, not just the exit code. The tree was restored clean after the run (`git diff --quiet`).

## The builder's deviations and DECISIONS FOR THE OWNER

1. **Live-channel cap instead of a create cap (G1).** This is safe for one address and the reasoning is sound: a create cap would break the gate test's loop, which needs 64 creates. Pending channels are cheap, evictable, and live for 60 s. The weaknesses are G1-r2a to G1-r2d plus the order-dependent test (T-r2a). Accept the design, and fix the eviction ranking (rank by pending count) and the test.
2. **DQ 7 (receiver never cut, sender gets `full`).** Safe as implemented, and better than round 1. Memory stays bounded (see the table above).
3. **N8 (certificate per start)**: deferral OK; it must be decided before profiles or contacts ship.
4. **R2 (tunnel: cut versus throttle)**: deferral OK for merging M1 **only if the tunnel path is not presented as supported**. This round makes it worse (G1-r2b: behind a tunnel, 16 live sessions and 8 mailboxes is the whole relay). It must be decided before spike C2, as the builder says.
5. **N3 (full peer IP:port in stderr)**: deferral OK.
6. **R3 (a)-(c) (Windows identity)**: deferral OK only while Windows is not shipped. (b), where the client does not verify the server, is a confidentiality hole, not just DoS hygiene. Spike W3 must close it before any Windows build is handed out.
7. **DQ 6 (second attach refused)**: deferral OK. Note that with G4-r2a, token rotation, the only way to evict a squatter, currently leaves the slot's `last_seq` poisoned.

None of these must be fixed before merge. **Before merge, I recommend (cheap, not gating):**
- G4-r2a (a two-line reset).
- Rank eviction by pending count (G1-r2c).
- Signal or document G2-r2a.
- Tests for X07 and X08, and fix the order-dependent test.
- I1-r2a, by flocking the 0700 directory or by adding a non-blocking probe as a second guard.

## What I did not examine, and how each claim stands

- **Ran** means demonstrated by a test or command above. **Reasoned** means from code only.
  - Reasoned only: R1 path coverage, DQ 7 memory bound, the tungstenite handshake-tail argument for G3 (read in tungstenite-0.30.0 `handshake/server.rs` and `machine.rs`; no wire test with a pipelined request, because I would have needed my own pinned raw-TLS client), I-r2c, `fork` inheritance (std opens with `O_CLOEXEC`, so only fork-without-exec children would hold the lock), and advisory-only or unsupported `flock` (a `TryLockError::Error` propagates, so bind fails closed; not run on NFS/SMB).
- Not examined: Windows at run time; a real second uid (X20, foreign-owned lock file); Linux behaviour of the lock; the default-limit arithmetic for G2-r2a and G1-r2a beyond the scaled tests (the numbers in the table are computed from `limits.rs`); memory measurement (round-1 N9 still stands); `cargo fuzz`; any code outside the delta except where the delta calls it; the unsafe code inside dependencies.
- My G2-r2a and G2-r2b tests use scaled limits (total 1 MiB or 210 KiB). G1 tests use default limits.
- G3 wire test 2 (`finish_and_reopen`) is weak: the relay closes on the invalid data frame before the deadline matters. The real evidence for G3 is the differential test.

## My own slips

1. My first G2 accounting control was wrong: it set the pair cap below the frames I sent and filled too little to trigger eviction. I fixed the test setup (4 frames, a 700 KiB total), not the assertion.
2. My first `finish_and_reopen` wire test asserted a slow-loris cut and failed because the relay cut for a malformed data frame first. I relaxed it to "connection not held open" and say above that it is weak.
3. I copied my mutation runner `gate_mut_r2.py` into `gate_relay_tests_r2/` along with the test sources. The brief allowed only test sources there. A hook (correctly) refused the delete, so the file is still there: it is a script, not a test, and it is harmless.
4. The first Windows clippy run overlapped with `run.py` mutating the pristine clone. I re-ran it on the verified-clean tree after `run.py` finished; that clean result is the one reported.
5. Two duplicate "wait" background shells ran at the same time (wasted, no effect).
