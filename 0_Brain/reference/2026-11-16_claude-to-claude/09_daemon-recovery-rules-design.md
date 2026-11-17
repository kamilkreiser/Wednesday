---
date: 2026-11-17
type: reference
source: design drafter commissioned by Friday; inputs are the three M1-DAEMON gate verdicts, branch m1-daemon at d8b5b4b and main at 18005d6 (both read with git show, nothing checked out, nothing run), the daemon brief and its three addenda, STATUS_M1_DAEMON.md, STATUS_M3_ROSTER.md (the daemon-lane request), design files 03, 04, 05, 06 and 07
status: live (design for the owner's review; nothing built, no code run, no test run)
project: General / CoAgent (no client)
---

# CoAgent daemon: the recovery rules, designed as a whole

**Authority.** The owner's ruling on the live board, verbatim option text as Friday relayed it: "Design the recovery rules as a whole first, then one build and one check".

## 1. Eight sentences for the owner

1. Today the background service believes things nobody has proven to it (numbers and notices that the connection server, the relay, writes on the outside of every packet) and it writes some of them to disk.
2. That is why one fake number stopped a session for good in the third check, why the first two checks found the same kind of fault elsewhere, and why reading the code for this design turned up ten more places of the same kind that no check has run yet (section 5.3).
3. The redesign has one idea: nothing unproven is ever remembered or obeyed, and every state in which one side waits for the other has a clock that ends in one single procedure, "start again from what both sides have proven".
4. So whatever a relay or a stranger sends, once it stops the two sides are exchanging messages again within two minutes (a proposed figure, not measured), nothing reaches the assistant twice without a label, and nothing confirmed as received is lost without being reported.
5. It is tested by starting two services in every kind of muddled state and checking that they recover, and not by replaying the attacks already found.
6. The cost: the recovery part of the service is rebuilt as one separately testable piece and not patched; a packet lost in the middle of a healthy session now heals in about 17 seconds where it took about 2; and a relay that keeps interfering can still block a session for as long as it keeps interfering.
7. Nothing changes in the cryptography or in the relay's protocol.
8. Five decisions stay with Kam (section 10.2); the main one is whether a session should ever end by itself because the other person has been away a long time.

**How to read the labels.** **[d8b5b4b: file:line]** means I read that line with `git show m1-daemon:<path>`; `git rev-parse m1-daemon` returned `d8b5b4bb482406431578b299e747c32f83a3e609`. Paths are under `crates/coagent-daemon/src/` unless a crate is named. **[main: file:line]** is the same for `main`, which returned `18005d63ae1311df9649893060caf1f98510a4c1`; the diff between the two over `crates/coagent-relay` and `crates/coagent-crypto` is empty. In a **[main: …]** label a bare `state.rs`, `frame.rs`, `limits.rs` or `PROTOCOL.md` is under `crates/coagent-relay/`, and `channel.rs`, `kk.rs` or `channel_map.rs` under `crates/coagent-crypto/src/`. A bare file name with no label, in a table's source column, is at d8b5b4b. **[r1 / r2 / r3 verdict …]** is the named part of a gate verdict in `m1_review/`. **REASONED** means my argument from reading; nothing has attacked it. **PROPOSED** means a number I chose; none is measured. **not read** marks anything I state without having read it. A and B are the two daemons; the *initiator* is the one with the lower key id [d8b5b4b: engine.rs:2232-2237].

---

## 2. Threat and fault model

### 2.1 What a relay frame is, and which parts are proven

A data frame on the wire has three layers. "Proven" means: covered by an authenticated decryption under keys that only the roster-pinned peer can hold.

| Layer | Field | Who writes it | Proven? | Where read |
|---|---|---|---|---|
| Relay header | `to_slot` (1 byte) | sender | **No** | [main: coagent-relay/src/frame.rs:581-609] |
| Relay header | `from_slot` (1 byte) | **the relay overwrites it** | **No** | [main: coagent-relay/PROTOCOL.md:42-43; state.rs:706-707, 767-773] |
| Relay header | `pair_seq` (8 bytes) | the sending daemon; the relay only checks it increases | **No** | [main: state.rs:740-746]; taken from the frame as it arrives [d8b5b4b: link.rs:347-353] |
| Daemon payload | tag (1 byte: key-exchange message 1, message 2, or channel frame) | sender | **No** | [d8b5b4b: wire.rs:1-10, 75-92] |
| Daemon payload | label ("epoch", 8 bytes) | sender | **No** ("a routing hint only") | [d8b5b4b: wire.rs:82-85; docs/DAEMON.md:183-184]; it is not in the handshake's bound data [main: coagent-crypto/src/kk.rs:35-55] |
| Key-exchange message 1 | Noise KK bytes | initiator | Proven to come from the peer's key for this session, roster and slots, **but not fresh**: the same bytes can be delivered again | [main: kk.rs:4-11; d8b5b4b: engine.rs:2340-2346] |
| Key-exchange message 2 | Noise KK bytes | responder | **Proven and fresh** for the initiator (bound to its new one-time key) | [d8b5b4b: engine.rs:2418-2419, 2432-2439] |
| Channel frame | `seq` (8 bytes, the encryption counter) | sender | Proven **only if the frame opens**. The comparison "behind / ahead of the expected number" is made **before** any decryption | [main: coagent-crypto/src/channel.rs:6-13, 283-288] |
| Channel frame | ciphertext | sender | **Proven**; session, sender and receiver are checked against the channel | [main: channel.rs:15-16, 291-313, 338] |
| Inside the ciphertext | application `seq`, `ack`, type, body, `last_seq_received` | sender | **Proven** | [d8b5b4b: engine.rs:2640-2662, 2800-2866] |
| Relay control lines | `peer.joined`, `peer.left`, `ok`, `error <code>` | the relay | **No** | [d8b5b4b: link.rs:357-362] |

The link to the relay is TLS with a pinned certificate. That proves the daemon is talking to the relay named in the invitation; it proves nothing about what that relay forwards [04 §4.4, line 408].

**Everything marked "No" is called a HINT in this document.** So are: the order and timing of arrivals, the connection going up or down, and the "behind / ahead" verdict of a channel frame that did not open.

### 2.2 Who can do what

| Actor | Can | Cannot (given the cryptography as built) |
|---|---|---|
| **Honest peer** | Send proven frames in order; be slow; be absent; restart; have a full inbox or a full disk. | — |
| **Hostile peer** (holds its own roster key) | Send any proven content: any application number, any `ack`, any `last_seq_received`, `full` for ever, a new key exchange at any time, `session.leave`. Start key exchanges it never finishes. | Speak as anyone else; read or write the local store; make the local daemon lose a message it did not itself send. It can always end or stall **its own** session: that is not an attack this design removes. |
| **Hostile or broken relay** | Read every HINT; write every HINT; drop, delay, duplicate, reorder, truncate and replay any frame it ever carried, including key-exchange messages it withheld earlier; forge presence and error lines; refuse or cut connections; swallow acknowledgements. | Make a frame open; read content; produce a fresh key-exchange message; add a party [03 §9.1 row B]. **Denial while it is acting is accepted by the design** [03 §9.1 row B: "Denial of service" under what is left]. What is not accepted is denial that continues after it stops. |
| **A party holding no session key and not the relay** | Nothing on an established link: it cannot get past the pinned TLS. If it can reach the relay it can attach only with a slot token (denial-of-service hygiene, not security [main: PROTOCOL.md:68-69]); with a stolen token it becomes a relay-grade forger of HINTS for that slot, no more. | Anything a relay cannot. |
| **The network** | Drop a connection at any byte; black-hole it; deliver nothing for hours. | Reorder or alter bytes inside one TLS connection. |
| **Either daemon restarting** (crash, SIGKILL, reboot) | Stop between any two steps; lose everything in memory. | Lose what was written and synced: state files are written to a temporary name, synced, renamed, and the directory synced [r2 verdict, G6 row; code in datadir.rs, not re-read by me]. |
| **The disk** | Be full (a write fails); hold a damaged bulk file (inbox or outbox). | Present a half-written state file as whole (the rename rule above). A **rolled-back** file (an older valid copy put back by the same user) is outside the model, as in [03 §9.1 row D] and [r3 verdict R3-6]; section 3.3 row 44 says what then happens. |

---

## 3. The rules and the recovery table

### 3.1 States

One per session and peer (one peer in this build; every rule is stated per ordered pair).

| State | Meaning | In the code today |
|---|---|---|
| DETACHED | no relay connection | `link` is `None` [d8b5b4b: engine.rs:179] |
| NO-CHANNEL | attached; no channel that both sides have proven | `attached`, `chan_epoch` is `None` [engine.rs:180-182] |
| LIVE | a proven channel, and each side has the other's position | `connected()` [engine.rs:967-976], plus rule R4's position |
| HELD | LIVE, and one side has said its inbox is full | `peer_full` / `refusing_full` [engine.rs:221-224] |
| STOPPED | the safety-words check failed; final for this session and slot | `rec.verify.hard_stop` [engine.rs:984-988] |
| ENDED | ended by a local command or a proven `session.end` / `session.leave` | `rec.ended` [engine.rs:2856-2862] |
| EXHAUSTED | a local counter reached its limit (rule R10); final | new |

### 3.2 The rules

**R1. Two kinds of state.** Every value the daemon holds is either PROVEN-ONLY or SCRATCH. PROVEN-ONLY changes only through a local act (a command, the daemon's own counter) or a frame that opened under a proven channel. SCRATCH lives in memory, is bounded, and may be wrong. **Everything on disk is PROVEN-ONLY.** A HINT may do exactly three things: pick which held channel a frame is tried against; raise a counter; cause one of the rate-bounded replies listed in R6. A HINT never closes, replaces or installs a channel, never starts a re-attachment, never changes `connected`, never reaches a file. One named exception, kept from the current build: the responder stores a 16-byte digest of each genuine key-exchange message 1 (at most 256) [d8b5b4b: engine.rs:2358-2393; store.rs:234-243]; such a message passed the Noise check under the peer's key, the digest orders nothing, and losing it is harmless.

**R2. No relay number is ever stored or compared.** The field `relay_recv_upto` is removed. An arriving `pair_seq` is not read. The daemon's acknowledgements to the relay exist only to empty the relay's buffer, so they carry no number taken from a frame: each is a FLUSH, `upto = u64::MAX` ("drop everything you hold for me from that slot"). A FLUSH is sent (a) as `resume_from` in every attach, (b) at most once per 100 ms tick in which at least one data frame arrived, (c) every 5 s while attached, whether or not anything arrived. The relay as built accepts it: the acknowledgement is a plain `u64` and frees every buffered frame at or below it [main: state.rs:669-704; frame.rs:282-284, 674] (REASONED, not run: U-D2). On load, a `session.json` that still has `relay_recv_upto` is accepted and the value discarded, so an installation already poisoned as in R3-1 heals at its next start.

*Why flushing loses nothing.* Every attachment pair runs a fresh key exchange [d8b5b4b: engine.rs:2159-2166; docs/DAEMON.md:186-188] and the channel is dropped with the link [engine.rs:2116-2133]. So a frame the relay buffered before this attachment was sealed under keys this daemon no longer holds and can never open. While both are attached the relay hands each frame to the receiver's socket in the same step that buffers it [main: state.rs:780-797]. The durable copy of every message is the sender's outbox, not the relay's buffer.

**R3. A number is durable before it is used.** (a) An outbox item, with its application number, is written and synced before any frame carrying it is sealed. (b) The daemon's own relay send number is reserved in blocks: the ceiling `current + 4096` is written and synced before the first number of a block is used, and a restart continues from the stored ceiling. (c) A restart takes, for every position, the larger of the bulk file's value and the floor in `session.json`, as today [d8b5b4b: engine.rs:753-754].

**R4. One recovery procedure, RESYNC.** Drop the link if there is one; take a token (R6); attach with a FLUSH; the initiator starts a key exchange; the new channel is confirmed both ways exactly as the current build does it (the responder's pending list, the initiator's unconfirmed channel, promotion only on a frame that opens under the new keys [engine.rs:2347-2542]); then POSITION: the first frame each side sends on a new channel is its proven `resume` or `full` carrying `last_seq_received`, and **nothing leaves the outbox on a channel until the peer's position has arrived on that channel**. The outbox is then trimmed to that position and the sender emits, in order, every number above it and below its next number: the held item, or a `coagent.skip` for a number it no longer holds (the existing record a receiver numbers and never delivers [engine.rs:234-235, 2885-2894]). Sending goes through a pump: a frame is sealed only when a place in the link queue has been reserved, and at most 128 frames or 1 MiB are in flight (sent on this channel, not yet acknowledged by the peer).

**R5. Only clocks on proven state, and local events, start a RESYNC.** The triggers are: the oldest in-flight item unacknowledged for 15 s (T-RTO); HELD with a non-empty outbox for 30 s (T-HELD); attached with no proven channel for 15 s on the responder (T-KEYING, repeating with the existing backoff up to 60 s); the connection going down; the relay refusing the attach; a seal failure of the "counter used up / rekey overdue" kind. No HINT is a trigger. Key-exchange clocks act on the same link and take no token: message 1 unanswered or channel unconfirmed for 5 s restarts the exchange, as today [engine.rs:3091-3112]; and an initiator that is attached with no proven channel and no exchange in flight starts one every 15 s (doubling to 60 s) **whether or not the relay has announced the peer** (T-BLIND).

**R6. Budgets on everything a HINT or a peer can make the daemon do.** Attachments: a bucket of 5, one more every 12 s, whatever the cause. Key-exchange starts: at most 1 per second. Key-exchange messages 1 processed: at most 8 per second, the rest counted and dropped. Answers to a replayed message 1: at most 1 per 500 ms (kept [engine.rs:248, 2375-2383]). FLUSH: as in R2. Log lines caused by frames: at most 60 per minute per category, the rest counted. The existing reconnect backoff (1 s doubling to 60 s, jittered [docs/DAEMON.md:244-245]) is kept unchanged underneath the bucket.

**R7. Presence is a HINT.** `peer.joined` may make the initiator start a key exchange (within the 1-per-second limit). It does nothing else. In LIVE it sets no "awaiting" flag and cannot make `connected` false. `peer.left` changes a status field only.

**R8. A proven number that makes no sense is refused, counted and reported; it is not chased.** An application number above "next expected" is not delivered and not numbered, the direction is shown as `desync` in status, and no RESYNC is started (a new channel cannot repair it: the number is the peer's own statement). The next in-order message clears the flag. A peer's `ack` or `last_seq_received` above what was ever sent is clamped to the highest number sent.

**R9. Durable before told, in both directions.** Kept from the build: a command's reply goes out after the save [engine.rs:949-957]; an acknowledgement to the peer names only what is on disk [engine.rs:3163-3167, 2624-2625]; while a save is failing, state-changing commands are refused and nothing new is acknowledged to anyone [engine.rs:886-894, 631-639]. New: R3 (a) puts the save before the send as well.

**R10. Final states have proven or local causes only.** STOPPED, ENDED and EXHAUSTED are entered on a local command, a proven frame, or the daemon's own counter reaching `2^62` (application numbers, relay send number). Never on a HINT, and never because time passed (subject to decision D-1). All arithmetic on stored or received numbers is checked; a stored position above `2^62` makes the file that holds it count as damaged.

**R11. Start-up fails closed on the security file and reports loss from a bulk file.** A `session.json` that is unreadable, or whose record does not validate against the roster and contacts, makes the daemon exit non-zero with nothing changed. A damaged `inbox.json` or `outbox.json` is moved to `quarantine/` as today [engine.rs:717-752], and the loss is counted in a fixed notice (decision D-2).

**R12. Status says what is proven.** `connected` is true exactly in LIVE and HELD. Status also gives `not_connected_since`, `last_proven_frame_s` (seconds since a frame from the peer last opened), `oldest_unacked_s`, `desync`, and one counter per kind of HINT. It never implies more than that.

### 3.3 The table: state × event

"Told" is what the local person or assistant can see. "Final?" says whether the session is declared dead. Rows 1-15 are HINTS (except rows 4 and 9, which are the daemon's own counters) and all have the same shape on purpose.

| # | State | Event | Action | Written to disk before the action | Told | Final? |
|---|---|---|---|---|---|---|
| | | **Relay header numbers** | | | | |
| 1 | any attached | data frame whose `pair_seq` is from the future (any value up to `u64::MAX`), the past, repeated, non-monotonic, or 0 | The field is not read (R2). The payload goes to rows 7-24. The tick's FLUSH is marked due. | nothing | nothing | no |
| 2 | any attached | forged `pair_seq` on a frame whose payload is garbage (the third check's R3-1) | Payload fails to decode or opens under nothing: `unknown_frames` +1. Nothing else. | nothing | counter | no |
| 3 | any attached | `from_slot` is not the peer's slot | `refused` +1; dropped [kept: engine.rs:2187-2190] | nothing | counter | no |
| 4 | any | own relay send number reaches `2^62` | EXHAUSTED. Reachable only from a damaged or edited file: the counter rises by one per frame sent and by 4096 per restart (R3 b). | the state | "This session's connection counter is used up. End it and pair again." | **yes** |
| 5 | LIVE | relay answers `full`, `rate_limited` or any error to a data frame | `relay_refused` +1. Nothing else: if the frame was really refused the peer will not acknowledge it and T-RTO starts a RESYNC. With an honest relay this cannot happen to an honest pair: R4's in-flight limit (1 MiB, 128 frames) is half the relay's per-pair buffer (2 MiB, 500 frames [main: limits.rs:17-19]) and the receiver flushes within 100 ms (R2). | nothing | counter | no |
| 6 | LIVE | relay answers `bad_request` to own frame (own number not above the relay's) | As row 5. **Cannot arise from a crash**: R3 (b). Cannot arise from a relay restart: the relay keeps its per-pair number only while it runs [main: state.rs:186-188]. It arises from a rolled-back file: row 44. | nothing | counter | no |
| | | **Label and tag** | | | | |
| 7 | any attached | frame with a label matching no held channel, or a label from the future, the past, or at the numeric limit | Tried against at most 6 held channels by label (live, unconfirmed, 4 pending); none opens: `unknown_frames` +1 [kept: engine.rs:2508-2541] | nothing | counter | no |
| 8 | any attached | unknown tag, short payload, oversize payload | `refused` +1 [kept: engine.rs:2323-2331; wire.rs:76-91] | nothing | counter | no |
| 9 | any | own key-exchange label reaches `u64::MAX` | Wraps. It is a HINT for the other side too, so reuse is harmless: same-label entries already sit side by side [STATUS A1.2 G1 row]. Today `kk_label + 1` is unchecked [engine.rs:2280]. | nothing | nothing | no |
| | | **Channel counter (before the frame opens)** | | | | |
| 10 | LIVE | frame for the live channel, counter ahead of the expected one: a gap, a jump, `2^40`, `u64::MAX` (the third check's R3-2) | `gap_hints` +1. **No reconnect.** Today this reconnects and re-sends the whole outbox [engine.rs:2580-2590, 2613-2637]. A real loss is healed by the sender's T-RTO. | nothing | counter | no |
| 11 | LIVE | counter behind the expected one, or repeated (a replay of an old valid frame of this channel) | `stale_frames` +1 [kept: engine.rs:2591-2595; main: channel.rs:283-285] | nothing | counter | no |
| 12 | LIVE | expected counter, but the frame does not open (a flipped bit) | `failed_opens` +1; the next valid frame still opens [main: channel.rs:291-309] | nothing | counter | no |
| 13 | any | replay of a valid frame of an **earlier** channel | Its keys are gone (dropped with the link, or replaced at promotion [engine.rs:2129-2133, 2305-2306]): row 7. | nothing | counter | no |
| | | **Presence and connection** | | | | |
| 14 | NO-CHANNEL | `peer.joined` (true or forged) | Initiator: start a key exchange, at most 1 per second; an exchange younger than 1 s is left alone. Responder: nothing (T-KEYING is already running). | nothing | `peer_present` | no |
| 15 | LIVE / HELD | `peer.joined` or `peer.left` (true or forged) | Initiator on `joined`: may start a key exchange (1 per second); the live channel stays until a new one is proven. Otherwise a status field only. Today a forged `peer.joined` makes a responder report "not connected" and reconnect after 15 s [engine.rs:2167-2171, 973, 3113-3127]. | nothing | `peer_present` | no |
| 16 | any attached | connection lost, or cut in the middle of a message (one message is one frame, or two when a rekey record goes first [main: channel.rs:196-217]) | DETACHED. The channel and all SCRATCH are dropped. RESYNC when a token and the backoff allow. The half-sent message is still in the outbox and is sent again after POSITION; the receiver drops it by number if it had arrived. | nothing new (the outbox item was written at `send`, R3 a) | `connected: false`, `not_connected_since` | no |
| 17 | DETACHED | relay unreachable, or it refuses the attach | Retry under the backoff and the bucket. Convener only: re-create the channel on `not_found` [kept: link.rs:286-327]. | nothing | as row 16, plus the stage that failed | no |
| 18 | DETACHED | the relay presents a different certificate (it restarted without a saved identity, or something is in its place) | Not attached; retried at the slowest cadence. No automatic recovery exists: the joiner needs a new line from the starter [docs/DAEMON.md:250-254; 06 §4.3]. Whether the starter's daemon re-supplies the identity to its own relay is [06 I-11], still open (D-5). | nothing | the fixed text of [06 §4.3] | no |
| 19 | both DETACHED | both sides reconnect at the same moment | Each attaches with a FLUSH. Whichever attaches second makes the relay announce both [main: state.rs:635-643]. The initiator starts the exchange; if the announcement is lost, T-BLIND starts it within 15 s. A message 1 sent before the responder attached is flushed and replaced by the next one. | nothing | — | no |
| | | **Key exchange** | | | | |
| 20 | any attached, responder | a genuine message 1 not seen before | Answer; hold its channel in the pending list (4, oldest out, 30 s) [kept: engine.rs:2385-2413]. The live channel is untouched. | digest, lazily (R1's exception) | `pending_exchanges` | no |
| 21 | responder | a replayed message 1 (digest known) | Answer at most once per 500 ms; no pending place [kept: engine.rs:2369-2384] | nothing | counter | no |
| 22 | responder | a forged message 1 (fails Noise) | `refused` +1; at most 8 per second are even examined (R6) | nothing | counter | no |
| 23 | initiator, exchange in flight | message 2 that completes it | Unconfirmed channel; send own position on it as the confirmation [kept: engine.rs:2450-2468] | nothing | — | no |
| 24 | initiator | forged or replayed message 2 carrying the in-flight label | The exchange is lost [engine.rs:2429-2438]; a new one starts within the 1-per-second limit. | nothing | counter | no |
| 25 | responder | a frame opens under a pending channel | Promote it; **read the peer's position from it; send own position; then** run the pump (R4). Today the outbox is re-sent before the peer's position is used [engine.rs:2529-2535, 2613-2637]. | nothing | `connected: true` | no |
| 26 | initiator | a frame opens under the unconfirmed channel | Confirm; read the peer's position; run the pump. | nothing | `connected: true` | no |
| 27 | NO-CHANNEL | message 1 unanswered 5 s / channel unconfirmed 5 s / pending entry 30 s old / no position 5 s after promotion | New exchange on the same link (no token) / entry dropped / RESYNC. | nothing | `exchange_in_flight` | no |
| 28 | NO-CHANNEL, initiator | attached, no exchange in flight, no announcement of the peer (a suppressed `peer.joined`) | T-BLIND: start an exchange every 15 s, doubling to 60 s. Today nothing starts one [engine.rs:2159-2166 is the only start besides the stuck-exchange timer, which requires `peer_present`: 3091-3112]. | nothing | — | no |
| 29 | NO-CHANNEL, responder | no proven channel for 15 s | T-KEYING: RESYNC (the re-attach is what tells an initiator that still believes its old channel). Repeats with the backoff up to 60 s. | nothing | — | no |
| | | **Proven application frames** | | | | |
| 30 | LIVE | `seq` = next expected | Accept into the inbox (bounded), or number and drop a refused type [kept: engine.rs:2885-2964]. The acknowledgement to the peer waits for the save. | the inbox (within 250 ms), then the ack | the assistant's next read | no |
| 31 | LIVE | `seq` at or below the last received (from the past, repeated) | Drop; one coalesced acknowledgement [kept: engine.rs:2870-2873] | nothing | nothing | no |
| 32 | LIVE | `seq` above next expected (future, a gap, non-monotonic, up to `u64::MAX`) | R8: not delivered, not numbered, `app_gaps` +1, `desync: true`, **no RESYNC**. An honest sender cannot produce it: the pump emits every number in order, held item or skip (R4), on a channel that delivers in order or not at all [main: channel.rs:283-288]. | nothing | `desync` in status | no |
| 33 | LIVE | `ack` or `last_seq_received` above anything sent, or `2^64-1` | Clamp to the highest number sent; the outbox is trimmed to it. The peer has only skipped its own deliveries. | the outbox | — | no |
| 34 | LIVE | `ack` or `last_seq_received` lower than before (non-monotonic) | No effect on the outbox. On a **new** channel the lower position is where the pump starts; numbers no longer held go out as skips (R4). | nothing | `lost_outbound` if skips were sent | no |
| 35 | LIVE | proven `full` | HELD: the pump stops. T-HELD is armed. | nothing | `send` answers "not delivered: recipient full" [kept: engine.rs:1385-1388] | no |
| 36 | HELD | proven `resume` with `room` | LIVE; the pump runs. | nothing | — | no |
| 37 | HELD, outbox not empty | 30 s with no change (the `room` frame was lost, or the belief is stale) | T-HELD: RESYNC; the new channel's POSITION says `full` or not. Today nothing ever leaves this state [engine.rs:3135-3147 excludes `peer_full`; no other timer in 3040-3181]. | nothing | — | no |
| 38 | LIVE | oldest in-flight item unacknowledged 15 s | T-RTO: RESYNC [kept: engine.rs:3131-3151] | nothing | `oldest_unacked_s` | no |
| 39 | LIVE | proven `session.end` / `session.leave` | ENDED [kept: engine.rs:2856-2862] | the state | "the peer ended the session" | **yes** |
| 40 | any | the safety-words check fails, or a local "no" | STOPPED; every channel, pending and unconfirmed entry is dropped [kept: engine.rs:1566-1585; r3 verdict §4] | the state, before the reply | hard stop | **yes** |
| | | **Restart and disk** | | | | |
| 41 | restart | messages accepted by `send` but **never sent** | They are in `outbox.json`. After RESYNC and POSITION the pump sends them in order. | — | — | no |
| 42 | restart | messages **sent, not acknowledged** | Same. The receiver drops the ones it already has (row 31). Nothing is delivered twice into the inbox. | — | — | no |
| 43 | restart | messages **received, not yet read**, or handed to the assistant and not confirmed | They are in `inbox.json` with their hand-out count; a second hand-out is labelled `possibly_repeated` [kept: engine.rs:1422-1470; r2 verdict G3 row]. Received but not yet saved: never acknowledged (R9), so the peer sends them again. | — | the label | no |
| 44 | restart | `session.json` is an older valid copy (outside the model) | Numbers may be reused: the relay answers `bad_request` (row 6) and the peer may report `desync`. Not repaired automatically. Both are visible in status at once and stay visible. | — | `relay_refused`, `desync` | no (the person ends it) |
| 45 | running | a crash between the save and the send (`send` saved the item, the frame never left) | Row 41. | (already written) | `send` never answered; the message is delivered once; a retry by the assistant is a second message with its own number | no |
| 46 | running | a crash between the send and the save | **Cannot happen**: R3 (a) orders save, then seal. Today the frame is queued first and the save follows [engine.rs:1375-1384, then 949-957]: section 5.3 item F-A. | — | — | — |
| 47 | restart | `session.json` unreadable, or its record fails validation | Exit non-zero, nothing changed (R11). Today three validation failures run on with no session [engine.rs:698-716], which lets a later invitation overwrite the stored hard stop: F-E. | nothing | start-up error | **yes, until repaired by hand** |
| 48 | restart | `outbox.json` damaged | Quarantine [kept: engine.rs:739-752]. The next number stays above every number used (R3 c). On the next channel the numbers that were in the file go out as skips (R4), so the receiver sees no gap. Today the next message is an application gap for ever: F-D. | the quarantine move | notice: "n queued messages could not be loaded and will not be sent" (D-2) | no |
| 49 | restart | `inbox.json` damaged | Quarantine [kept: engine.rs:720-738]. The floor in `session.json` stops the peer's numbers being accepted twice. The unread messages in the file were acknowledged and cannot be asked for again. | the quarantine move | notice: "n received messages could not be loaded; the file is kept at <path>" (D-2) | no |
| 50 | running | a state write fails (disk full) | Nothing new is acknowledged to the peer or the assistant; `send` and other state-changing commands answer `state_not_saved`; receiving continues only into the bounded in-memory inbox; the write is retried every tick [kept: engine.rs:560-641, 886-894]. A hard stop taken while writes fail holds in memory only [r3 verdict §4, durability ordering]: stated, not fixed. | — | `state_not_saved` | no |
| 51 | any | a local or received application number reaches `2^62` | EXHAUSTED (R10). Today the additions are unchecked [engine.rs:2810, 2818, 2879, 2243]. | the state | as row 4 | **yes** |
| 52 | LIVE | sealing fails because the channel's counter is used up or a rekey is overdue | RESYNC (a fresh channel). Today any seal failure other than "no channel" sets the message aside as unsendable [engine.rs:2748-2749]. A message too large to seal is still set aside, as today. | nothing | — | no |
| | | **Absence** | | | | |
| 53 | NO-CHANNEL | the peer never returns | Initiator: T-BLIND every 60 s. Responder: T-KEYING every 60 s. `send` is accepted until the outbox bound (256 messages, 2 MiB), then answers `outbox_full`. Nothing is dropped. The session does **not** end by itself (R10; D-1 asks Kam, because [03 §4.5] says pause at 5 minutes and end at 30). | nothing | `connected: false`, `not_connected_since`, `sent_now: false` | no, pending D-1 |

---

## 4. The invariants

Each is one sentence and each is a test in section 6.

| # | Invariant |
|---|---|
| **V1** | **No hint is remembered:** no byte of any state file changes because of an input that did not open under a proven channel, except the bounded list of key-exchange digests. |
| **V2** | **No hint is obeyed:** such an input never closes, replaces or installs a channel, never starts a re-attachment, and never changes `connected`. |
| **V3** | **Bounded answers:** over any second, the frames the daemon sends because of unproven input are at most 10 flushes, 2 answers to replayed handshakes, 8 answers to new handshakes and 1 handshake start, and never one byte of the outbox. |
| **V4** | **Recovery from anywhere:** from any SCRATCH state of both sides and any valid stored state, once the relay is honest, both daemons run, the disk is writable, the session is not final and the receiver's inbox has room, every message in an outbox is in the peer's inbox within 120 s (PROPOSED) of that moment or of its `send`, whichever is later. |
| **V5** | **No waiting without a clock:** in every state that is not final, if the outbox is not empty or there is no proven channel, a deadline is armed whose expiry starts a key exchange or a RESYNC. |
| **V6** | **Once into the inbox, in order:** each application number from the peer enters the inbox at most once and in increasing order, across any crashes, restarts and reconnections. |
| **V7** | **Labelled repeats only:** a message is handed to the assistant a second time only with `possibly_repeated: true`. |
| **V8** | **Nothing acknowledged is lost silently:** every message acknowledged to the peer is in the inbox, was confirmed by the reader, or is in a quarantined file counted in a notice; and every message `send` accepted is in the outbox, acknowledged by the peer, or set aside and counted in a notice. |
| **V9** | **Write before send:** no frame leaves the daemon carrying an application number or a relay number that is not already on disk, so no crash makes a number carry two different messages. |
| **V10** | **A restart never lowers a counter:** after any crash and restart, every position and every limit on the peer (next send number, last received, relay send number, verify attempts, hard stop) is at least what any reply or frame before the crash stated. |
| **V11** | **Attachment budget:** in any window of T seconds the daemon attaches to the relay at most 5 + T/12 times, whatever anyone sends, so the outbox is re-sent at most that often. |
| **V12** | **Quiet when nobody interferes:** with an honest relay, no restart and no disk fault, an honest pair completes any workload within the bounds with zero re-attachments, zero relay refusals and zero gaps. |
| **V13** | **Final states have causes:** STOPPED, ENDED and EXHAUSTED are entered only on a local command, a proven frame or a local counter limit. |
| **V14** | **Everything is bounded:** after every step every buffer, list and counter of section 7 is at or under its limit, and log lines caused by frames stay under their rate. |
| **V15** | **Status is true:** `connected` is true exactly when a channel proven by both sides exists and both positions were exchanged on it, and status counts equal the files. |
| **V16** | **Start-up fails closed:** a security file that is unreadable or does not validate makes the daemon exit non-zero with no file changed, and a damaged bulk file is quarantined, never deleted and never the cause of a later gap. |

Sixteen invariants. Properties the earlier rounds closed and this design must not disturb are carried as regression checks, not restated: peer-text containment, the hard-stop predicate at every channel path [r3 verdict §4], the verify-attempt count across restarts, the release point and its witness.

---

## 5. The rule that removes the class

### 5.1 What the class is

Three rounds, one shape: **an input nobody proved changed something that lasts, or was answered with something expensive.**

| Round and id | The unproven input | What it changed or caused | Recovery situation (table row) |
|---|---|---|---|
| r1 G1 (Major) | the label on a replayed handshake message | replaced the live channel; **stored** the label; refused every later exchange, also after a restart | 7, 20, 21 |
| r2 R2-2 a (Major) | one dropped frame | a state with no clock: stalled until a process restart; status said connected | 27 |
| r2 R2-2 b (Major) | four replayed handshake messages | evicted the honest pending exchange | 21 |
| r2 R2-9 (Note) | relay `pair_seq`, forged `peer.joined`, replayed message 2 | each still changed a stored counter; "no harm found" | 1, 14, 24 |
| r3 R3-1 (Major) | one forged `pair_seq` | **stored**; relay acknowledgements stopped; the sender was refused for good, also after a restart | 1, 2 |
| r3 R3-2 (Minor) | one forged channel counter | a reconnect and the whole outbox again: 59 bytes in, 331,811 out | 10 |
| r3 R3-4 (Minor) | genuine handshake messages the relay withheld | evict the honest pending exchange while the relay keeps doing it | 20 (bounded, not removed: 5.4) |
| r3 R3-3 (Minor) | — | the gap test could not fail: another healing path masked it | section 6 |

Neighbours with the same result (a stall that stores itself or feeds itself) from a different cause, each closed in its round and kept closed here: r1 G2 and G3 (the daemon's own file too large to load; a read that consumed), r1 G4 (a dead waiter), r1 G11 and r2 R2-4 (an unusable message at the head of a queue, re-sent for ever, surviving a restart), r2 R2-5 and R2-6 (damaged files), r1 G6 and G7 (a write that did not last or did not happen: rows 46 and 50), r2 R2-12 (an acknowledgement that lagged at "full": row 35), r1 G17 and r3 R3-6 (a rolled-back file: row 44, outside the model). Findings that are not recovery situations and that this design does not touch: r1 G5, G8-G10, G12-G16; r2 R2-3, R2-10, R2-11, R2-13; r3 R3-5, R3-10. Carried unchanged: r2 R2-8 and r3 R3-7 (a page acknowledged that the client never showed) are about the hand-out contract with the assistant, [STATUS A2.8] leaves them with the design owner, and they stay in BACKLOG.

Each round's fix removed one edge from "unproven input" to "lasting state". The rounds kept finding the next edge because the edge **type** was still allowed.

### 5.2 The rule, and why the family cannot come back

**The rule is R1 with R5:** a HINT may be counted, may select a channel to try, and may draw one of four rate-bounded replies; it may do nothing else; and every waiting state has a clock on proven state.

The argument (REASONED):

1. *Nothing a relay does can survive a restart.* Everything on disk is PROVEN-ONLY (V1). The third check's value could not be written: there is no field to write it to (R2), and no other HINT has one.
2. *Nothing a relay does can outlast it by more than a stated time.* What a HINT can touch is SCRATCH. From **any** SCRATCH state the clocks of R5 reach LIVE within the bound (V4, V5). This is the step the earlier fixes lacked: they reasoned about the states the known attacks produce; V4 is stated, and tested, over all states.
3. *Nothing a relay sends can be made expensive.* A HINT causes no re-attachment and no retransmission (V2), and the replies it can draw are bounded per second (V3). The outbox is re-sent only after the peer's proven position, only above it, and at most as often as the attachment budget allows (R4, V11).

Finding by finding: **G1**: the label is a HINT; it selects a channel to try and is never stored or compared (rows 7, 9). **R2-2 a**: a state without a clock fails V5; the test is over every state and every frame position, not eleven. **R2-2 b**: kept fix (digests), now under V1's named exception. **R2-9**: "harmless" stored counters no longer exist; the note's direction ("restrict which events may change persisted counters") is the rule. **R3-1**: R2. **R3-2**: row 10; a forged counter is answered with nothing. **R3-3**: section 6's isolation rule.

### 5.3 More instances of the same family, found by reading (REASONED, not run by anyone)

The rule was applied to the code as a checklist: for every stored field and every action, "what unproven input reaches it?", and for every state, "which clock leaves it?". Ten places fail. None was reported by a gate. The build seat's first step reproduces or refutes each (U-D1).

| | What | Where | Rule that closes it |
|---|---|---|---|
| F-A | `send` hands the frame to the link before the item and its number are saved. A crash in between, then a restart, gives the same number to the **next** message; the peer drops that message as a duplicate and acknowledges it; `send` said "sent". | engine.rs:1375-1384 (transmit inside `cmd_send`), then 949-957 (the save) and 2870-2873 (the peer's duplicate rule) | R3 a |
| F-B | A lost `room` message leaves the sender holding for ever: the retransmit clock excludes a full peer and no other clock runs. | engine.rs:2837-2855, 3135-3147 | R5 T-HELD |
| F-C | A suppressed `peer.joined` leaves both sides attached with no key exchange for ever. The relay announces presence only at attach. | engine.rs:2159-2166, 3091-3112; main state.rs:635-643 | R5 T-BLIND |
| F-D | A damaged outbox file at restart loses its numbers; the next message is an application gap; the receiver reconnects for ever. | engine.rs:739-754, 2879-2883 | R4 skips, R8 |
| F-E | Three validation failures in `restore` return success with no session, so a later invitation can overwrite the stored hard stop: the shape of r2 R2-6 on the other exits of the same function. | engine.rs:698-716 | R11 |
| F-F | A frame is sealed, then silently dropped when the link queue (256) is full: the daemon breaks its own channel. The third check lists it in its resource table as healed by the gap or the retransmit. | engine.rs:2245; link.rs:221 | R4 pump |
| F-G | The reconnect backoff is reset by `Attached`, which the relay controls, so a relay that attaches and cuts holds the daemon at one reconnect a second, each with a key exchange and the outbox. | engine.rs:2151-2153, 2216-2227 | R6 bucket |
| F-H | A forged `peer.joined` to a responder in a healthy session sets "awaiting rekey": status turns to not connected and the link is restarted after 15 s unless a proven frame happens to arrive. | engine.rs:2167-2171, 973, 3113-3127 | R7 |
| F-I | Unchecked additions on stored and received numbers. | engine.rs:2243, 2280, 2810, 2818, 2879 | R10 |
| F-J | The outbox is re-sent on every new channel before the peer's position is read. This, not the reconnect, is what made R3-2 a 5,623-fold amplifier while the peer was full. | engine.rs:2613-2637 | R4 POSITION |

Also by reading: the branch at engine.rs:2809-2814 reads a counter (`authentic_refused`) that no line increments (the only other occurrences are its declaration and three initialisations: 226, 798, 1891, 2069). It is dead code and goes.

### 5.4 What the rule does not remove

- **A relay that keeps interfering keeps denying.** Design [03 §9.1 row B] accepts that. The claim here is about what happens when it stops.
- **R3-4 is bounded, not removed.** A key-exchange message 1 proves who made it and not when. A relay that withheld four genuine ones can spend them to push an honest exchange out of the pending list, once each, for as long as it has a supply; the supply grows at most one per second (R6). When it stops, the next exchange completes. Removing this needs the responder to contribute freshness before it stores anything, which is a change to the handshake in the merged cryptography crate (D-3). Binding the label into the handshake (REQUEST R6 in STATUS) would not remove it either [r2 verdict §6].
- **A hostile peer can stall its own session** (never acknowledge, say `full` for ever, send gaps). Bounded in memory; visible in status; not a loss for anyone else.
- **A peer whose disk is full cannot acknowledge.** The other side re-sends at the attachment budget and shows `oldest_unacked_s` rising.

---

## 6. The tests: for each invariant, the test that fails without it

**The harness (the first thing built).** The recovery logic becomes one pure piece, `recovery`: `step(state, event, now) -> ordered list of actions`, with an explicit clock, the way the relay's own state module is built ("plain synchronous code … with an explicit clock, so every rule … can be unit-tested without a network" [main: state.rs:2-3]). The model harness runs two such pieces, a model relay, a model disk and an adversary, in simulated time. Because actions are an ordered list (`Persist(x)`, `Send(y)`, `Reply(z)`), a crash can be injected **between any two actions**. Simulated time removes the machine-load sensitivity the third check met [r3 verdict §2, §3 item 2]. A second, smaller layer repeats one schedule per table group with real `coagentd` processes, the real relay and the existing tap [link.rs:45-54].

**The adversary's alphabet** (the generator's input space for every property that says "any input"): deliver; drop; duplicate; replay any earlier frame, including one it withheld; reorder; rewrite `pair_seq`, `from_slot`, the label or the channel counter to any of {0, 1, the last value minus one, the last value, plus one, 2^40, 2^62, `u64::MAX`, random}; flip a ciphertext bit; truncate; change the tag; forge `peer.joined`, `peer.left`, `ok`, `error` with every code; cut the connection at any frame; refuse an attach; swallow an acknowledgement. **Faults:** crash either daemon between any two actions; fail a write; damage the inbox or outbox file; plant any `u64` in any stored number. **Local events:** send, read, confirm a read, wait and cancel, end, advance the clock. **A hostile peer** adds every proven frame with any `seq`, `ack` and `last_seq_received` from the same set.

**Three rules that make "this test cannot fail" impossible to say.**
1. *Red on its own words.* Each red control is a deliberate one-line break behind the existing `cfg(coagent_red = …)` switch and must fail the named property on that property's own assertion text.
2. *Reach is counted.* Every property counts how many generated schedules exercised the rule it guards and fails if the count is zero. A green run prints the count.
3. *Isolation.* Where two mechanisms can heal the same fault, the property pins the start state so that exactly one can, and asserts **which** one fired. This is the lesson of R3-3: the gap row stayed green because the retransmit clock healed what the broken gap path skipped.

| Inv. | Property (name) | Generator's input space | Red control (the one-line break) that must turn it red |
|---|---|---|---|
| V1 | `hints_never_reach_disk`: the bytes of every state file are identical before and after | any state × any sequence of unproven inputs from the alphabet, no proven frame, no local event | `store_pair_seq` (write the arriving `pair_seq` into the record: the line of R3-1); `store_label` (round 1's G1) |
| V2 | `hints_never_act`: the set of held channels, the attachment count and `connected` are identical before and after | as V1, from LIVE and from HELD | `gap_reconnects` (reconnect on a counter ahead: today's engine.rs:2589); `presence_unsettles_live` (today's 2167-2171) |
| V3 | `answers_are_bounded`: frames sent per simulated second ≤ the stated counts; outbox bytes sent = 0 | as V1, at 10,000 inputs per second for 60 s, outbox full of maximum-size items | `flush_per_frame`; `answer_every_replay` (exists); `resend_before_position` (today's order: F-J) |
| V4 | `recovers_from_any_state`: every outbox item is in the peer's inbox within 120 s | **every combination** of the SCRATCH fields of both sides (attached, present, exchange in flight, unconfirmed, 0-4 pending entries with any labels, live channel present / absent / different on the two sides, `peer_full` true or false on either side, bucket full or empty, backoff anywhere, relay buffer empty or full of junk) × any valid stored state; then an honest relay | one per clock, each under the isolation rule: `no_rto` (exists as `no_retransmit_timer`), `no_held_clock`, `no_blind_exchange`, `no_keying_clock`, `no_confirm_timer` (exists), `no_idle_flush` |
| V5 | `every_waiting_state_has_a_deadline`: `next_deadline(state)` is not `None` | the same state space as V4 | `held_has_no_deadline` |
| V6 | `inbox_once_in_order` | any adversary schedule × crashes between any two actions × a hostile peer's numbers | `dup_accept` (accept `seq` at or below the last); `app_gap_skip` (exists) |
| V7 | `repeats_are_labelled` | reads, confirmations and cancellations interleaved with crashes | `ack_free_read` (exists); `label_off` |
| V8 | `no_silent_loss`: the ledger (acknowledged = inbox + confirmed + counted in a notice; accepted = outbox + acknowledged + counted in a notice) balances after every step | any schedule × damaged inbox or outbox at any restart | `silent_quarantine` (the notice count is not raised); `skip_fill_off` (F-D) |
| V9 | `write_before_send`: at every crash point, every number seen on the wire is on the model disk; after the restart no number carries two contents | sends × crashes between any two actions | `send_before_persist` (today's order: F-A); `reserve_after_use` |
| V10 | `restart_never_lowers` | any prefix, crash, restart; compare with every reply and frame recorded before | `restore_drops_floor` (remove the `max` at engine.rs:753-754); `verify_in_memory` (exists) |
| V11 | `attachment_budget` | any adversary schedule, including cut-after-attach loops and a hostile peer's gaps, over 600 s | `no_bucket` |
| V12 | `honest_runs_are_quiet`: attachments after the first = 0; relay refusals = 0; `gap_hints` = 0 | honest relay; workloads up to both outbox bounds in both directions at once; receiver readers of any speed | `seal_without_place` (F-F); `no_inflight_limit` |
| V13 | `final_states_have_causes` | any schedule with no local end, no proven end and no verify failure, run for 24 simulated hours with the peer absent | `end_on_absence` |
| V14 | `everything_bounded`: every size of section 7 checked after every step | any schedule | `pending_unbounded` (exists); `log_per_frame`; `counter_wraps` |
| V15 | `status_is_true`: `connected` equals the model's "both proved and both positions known", checked after every step | any schedule | `connected_before_position`; `connected_on_presence` |
| V16 | `startup_fails_closed` | every way the record can fail validation × every damaged bulk file | `restore_fail_open` (today's engine.rs:698-716: F-E); `quarantine_fail_open` (exists) |

**Named process tests, real binaries** (one per situation Kam was told about): the third check's own two tests added unchanged first (`r3_a_one_forged_pair_seq_stalls_the_session`, `r3_b_one_forged_out_of_order_frame_resends_the_outbox`; their files are in `m1_review/gate_daemon_tests_r3/`, not read by me); a `session.json` with `relay_recv_upto` planted at 2^62 starts and delivers 600 of 600; a SIGKILL placed between the save and the send, and one placed where the old code sent first; a damaged outbox, then a new message, then delivery; a dropped `room`; a suppressed `peer.joined`.

**Existing tests that change, by reading (U-D3 replaces this with what runs).** `reconnect.rs::test5c_a_gap_produces_a_reconnect_not_a_skip` asserts a reconnect follows the gap within a 20 s collect [d8b5b4b: tests/reconnect.rs:140-167]; under row 10 the reconnect comes from T-RTO, so the test is rewritten with a short injected clock and asserts which clock fired. The red row `gap_skip` is retired with the reason written in the runner (its "broken" variant is now the specified behaviour); `ack_every_frame` is replaced by `flush_per_frame`. A gate file is never weakened: an assertion the redesign makes meaningless is marked with a ruling comment, the old line quoted, and replaced by a test of the property in its new form, as [07 §4.3] did.

---

## 7. Bounds

Nothing in this table grows with peer or relay input beyond the limit shown. Numbers marked PROPOSED are mine and unmeasured; the others are in the code.

| Thing | Limit | At the limit | Source |
|---|---|---|---|
| Inbox | 256 messages; 2 MiB text; 256 KiB other fields | proven `full` to the sender; nothing accepted or numbered | limits.rs:17-20, 50 |
| Outbox | 256 messages; 2 MiB text | `send` answers `outbox_full` | limits.rs:22-24 |
| In flight on one channel | 128 frames; 1 MiB | the pump waits for acknowledgements | PROPOSED (half of main limits.rs:17-19) |
| Link queue | 256 frames | the pump waits; nothing is sealed without a place | link.rs:221; R4 |
| Pending key exchanges | 4; 30 s each | oldest out | engine.rs:238-240 |
| Unconfirmed channel | 1; 5 s | new exchange | engine.rs:207, 64 |
| Key-exchange digests | 256 | oldest out | store.rs:243 |
| Skips emitted after one POSITION | 256 | more than 256 numbers missing: `desync`, nothing sent | PROPOSED (= outbox bound) |
| Waiting `wait` calls | 64 | `busy` | engine.rs:250 |
| State file | 16 MiB | the writer refuses | limits.rs:77 |
| Relay send number block | 4096 per save | next block saved first | PROPOSED |
| Application and relay numbers | 2^62 | EXHAUSTED | PROPOSED |
| Every HINT counter | `u64`, saturating | stays at the maximum | PROPOSED |
| Log lines caused by frames | 60 per minute per category | counted, not written (closes r3 R3-9) | PROPOSED |
| Attachments | 5, plus 1 per 12 s | wait for a token | PROPOSED |
| Reconnect backoff | 1 s doubling to 60 s, up to 25% jitter | stays at 60 s | docs/DAEMON.md:244-245; r3 verdict §4 |
| Key-exchange starts | 1 per second | deferred to the end of the second | PROPOSED |
| Handshake messages 1 examined | 8 per second | counted and dropped | PROPOSED |
| Answers to a replayed message 1 | 1 per 500 ms | not answered | engine.rs:248 |
| FLUSH | 1 per 100 ms when frames arrived; 1 per 5 s otherwise | coalesced | PROPOSED; tick is engine.rs:417 |
| Acknowledgement to the peer | coalesced 150 ms, after the save | — | engine.rs:68, 3157-3171 |
| Bulk file write | within 250 ms; forced before any reply | — | engine.rs:232 |
| Key-exchange clock | 5 s | new exchange, same link | engine.rs:64 |
| T-BLIND | 15 s doubling to 60 s | new exchange | PROPOSED |
| T-KEYING | 15 s, then the backoff to 60 s | RESYNC | 15 s is engine.rs:243 |
| T-RTO | 15 s | RESYNC | engine.rs:246 |
| T-HELD | 30 s | RESYNC | PROPOSED |
| Connect / relay reply | 5 s per candidate / 10 s | attach fails | link.rs:21-23 |
| Quarantined files | no count limit; local causes only (a damaged file, an unsendable own message) | — | r3 verdict §5 |

**The 120 s of V4, derived (REASONED).** Worst case is a link that was in backoff when the interference stopped: up to 75 s (60 s plus jitter) to the next attempt, which is longer than any detection clock (30 s) plus a token (12 s); then attach (10 s), key exchange with one retry (10 s), positions and first delivery (5 s): 100 s, rounded up. From a healthy-looking but stale channel it is 30 + 12 + 10 + 10 + 5 = 67 s. The third check reasoned about 110 s for the current code [r3 verdict §4].

**What the relay holds for a pair** is the relay's own bound and unchanged: 500 frames, 2 MiB, 15 minutes [main: limits.rs:17-21]. Under R2 the daemon empties it every 100 ms while frames arrive and every 5 s otherwise.

---

## 8. The public surface: what changes and who must adapt

No other branch depends on the daemon crates: a search of `m3-roster`, `m3-audit`, `m2-policy` and `m1-relay-identity` for the two crate names finds one comment, in the roster branch's `tests/api_stability.rs` (lines 1-5), which pins the roster calls the daemon makes.

| Surface | Change | Who must adapt |
|---|---|---|
| Relay protocol and relay crate | **None.** The daemon sends `chan.ack` and `resume_from` with `u64::MAX`, which the protocol already allows (U-D2). | Nobody. **REQUEST to the relay lane (optional):** one test pinning "an acknowledgement above the highest number sent frees the pair's buffer and changes nothing else", so the behaviour this design relies on cannot change silently. |
| `m1-relay-identity` | None. It changes `tls.rs`, `lib.rs` and the CLI only (its diff against main). Row 18 stays a human step until [06 I-11] is ruled (D-5). | Nobody. |
| Cryptography crate | **None.** REQUEST R6 (label in the handshake) is not needed by these rules; REQUEST R2 (seed the channel map with a stored hard stop) stands as it was. | Nobody. |
| Roster crate, `m3-roster` | None. The daemon's roster calls are unchanged, so `api_stability.rs` keeps compiling. `BACKLOG.md` conflicts textually at merge, as the third check found [r3 verdict §8]. | Nobody for this build. See 8.1 for the roster seat's request. |
| Audit crate, `m3-audit` | None now. When audit messages ride the per-pair channel they inherit V6 and R4: a number sent as a skip is an audit message that will not arrive on that pair, which the audit crate already detects by its own per-author numbers [07 §1.2 row 14]. [07 D5, D7] stay with the daemon lane and are not part of this build. | Nobody. |
| Policy crate, `m2-policy` | None. The release point and its witness are untouched [engine.rs:1457-1458]. **If D-2 is ruled yes**, two fixed daemon-built sentences join the fixed text a tool result may contain. | `m2-policy` only if D-2 = yes and only if it pins the list of fixed sentences (not read). |
| `session.json` | `relay_recv_upto` is no longer written and is discarded on read; `relay_send_seq` becomes a reserved ceiling. The record is `deny_unknown_fields` [store.rs:188], so the loader must name the legacy field. | Daemon only. |
| Local IPC `status` | Added: `not_connected_since`, `last_proven_frame_s`, `oldest_unacked_s`, `desync`, `lost_inbound`, `lost_outbound`, `gap_hints`, `relay_refused`. `gaps` keeps its name and now counts application gaps only. Removed: nothing (`relay_recv_upto` was never in it [engine.rs:1014-1056]). | The daemon's own tests. |
| MCP tool results | Unchanged unless D-2 = yes. | — |
| `DaemonConfig` | The new clocks are fields, as the backoff bounds already are [STATUS §1 item 1]. | Tests. |
| `docs/DAEMON.md` | The key-exchange, send/receive and reconnect sections are rewritten from section 3.3. | — |

### 8.1 The roster seat's request to the daemon lane

Recorded in STATUS_M3_ROSTER.md (lines 746-747), in the gate's words: "the intake has no persistence, so a restart also forgets mutes and quotas (a muted hostile guest is unmuted by a restart)."

**Decision: named, and out of scope of this build.** The intake is not wired into the daemon at d8b5b4b (the word does not occur in `engine.rs`; the positive control `kk_respond` occurs twice), and this build stays a two-member session. But the request is an instance of V10 ("a restart never lowers a limit on the peer"), so the rule already covers it: **when the daemon lane wires the intake, its mutes, quotas and remembered proposal ids are security state: stored in `session.json`, saved before their effect is reported, and restored at start.** That needs a way to rebuild an intake from stored accounting. The roster branch exposes `accounting()` and one constructor, `new` (intake.rs:197, 632; I read the list of public functions, not their bodies). **Named item for `m3-roster`, due when the intake is wired, not now:** a restore constructor from a snapshot, with a test that a restored intake refuses exactly what the original refused.

---

## 9. Build order, and what the one check should attack

Each step ends green on `scripts/check.sh` and on its own exit test, and is pushed. No step changes a merged crate.

| Step | What | Exit test |
|---|---|---|
| 0 | **Reproduce before changing.** Add the third check's test files unchanged. Write one failing test each for R3-1, R3-2 and F-A to F-J at d8b5b4b. | A table in STATUS: each item reproduced, or refuted with the reason. Nothing else proceeds on a refuted item without a note to Friday. |
| 1 | **Extract `recovery`** as the pure, clock-explicit state machine with ordered actions. No behaviour change. | The whole existing suite, the 66 red rows and both gate files give the same results as at d8b5b4b (the row `gap_skip` is recorded as it actually behaves; the third check saw it green). |
| 2 | **The model harness**: two machines, model relay, model disk, adversary, crash injection between actions. Properties V6, V7 and V14 green on unchanged behaviour; V1, V2, V4, V9 written and recorded **red** with the failing schedule printed. | The red list matches section 5.3. A differential test runs the same schedules against the real relay state module or a real relay process and gets the same deliveries (U-D4). |
| 3 | **R2**: remove `relay_recv_upto`; FLUSH; legacy load. | V1 green for `pair_seq`; the third check's `r3_a` green; the planted-file process test green. |
| 4 | **R3 and R9**: save before send; reserved relay numbers. | V9, V10 green; both SIGKILL process tests green. |
| 5 | **R4**: POSITION before any outbox frame; skips for numbers not held; the pump and the in-flight limit. | V8 (outbound), V12 green; `r3_b` green with 0 outbox bytes per forged frame; damaged-outbox process test green. |
| 6 | **R5, R6, R7, R8**: HINTS never act; a clock in every waiting state; the bucket and the rates; presence; proven nonsense. | V2, V3, V4, V5, V11, V15 green, each red control red under the isolation rule; dropped-`room` and suppressed-`peer.joined` process tests green. |
| 7 | **R10, R11, R12**: checked arithmetic and EXHAUSTED; fail closed at start; notices (if D-2); log rates; dead code removed. | V13, V14, V16 green. |
| 8 | **Close.** `docs/DAEMON.md` rewritten from the table; the red-control runner with every old and new row; `scripts/test-daemon.sh 5`; BACKLOG; STATUS with the measured recovery time against the 120 s. | Runner: every row red on its named property, clean run green; five runs green; every property prints a non-zero reach count. |

**The single list for the ONE independent check.** Attack these, in this order of value:

1. **V4's state space.** Find a SCRATCH state the generator does not produce, or a stored state it calls invalid that the daemon can in fact write. A state outside the generator is the next R3-1.
2. **A HINT I did not list.** Any value the daemon reads that is not in section 2.1's table: a relay control field, a length, a timing, an ordering between the control and data streams.
3. **A stored field a HINT still reaches**, including through the digest exception, through status counters that are saved, or through the legacy loader.
4. **Each clock alone.** For every clock, a start state only it can heal, with the red control red; and the reverse: a red control that stays green because another clock heals it (the R3-3 pattern).
5. **Crash points.** A crash between every pair of actions of `send`, receive, read, confirm, hard stop and reserve; then number reuse, double delivery or silent loss.
6. **POSITION.** Outbox bytes on a channel before the peer's position; a position frame lost, duplicated or sent twice by a hostile peer; skips for more than 256 numbers.
7. **The budget arithmetic.** Bytes out per byte in, for every unproven input, measured against V3; attachments per minute under a cut-after-attach relay and under a hostile peer.
8. **The 120 s.** A state from which recovery takes longer, especially with an empty bucket, a link in maximum backoff, and both sides in HELD.
9. **Honest quiet (V12).** An honest workload that makes the relay answer `full`, or that triggers one re-attachment.
10. **Regression of what held**: containment, the hard stop on every path through the new state machine, verify counts across restarts, bounds at both ends of every page.
11. **The withheld-handshake attack (5.4)**, run this time (it needs more than 260 exchanges), to confirm it ends when the relay stops and to measure how long that takes.
12. **Whether the tests can fail**: mutate each new rule; a survivor is a finding.

---

## 10. Interpretations, decisions, unknowns

### 10.1 INTERPRETATIONS

| # | The text | The reading taken | The alternative |
|---|---|---|---|
| I-D1 | Brief §2: "a gap is `OutOfOrder`: the daemon treats it as 'reconnect'"; brief §5 test 5: "an injected gap produces a reconnect, not a silent skip". | The gap verdict is made before decryption, so it is a HINT: it is counted, and the reconnect comes from the sender's 15 s acknowledgement clock. Nothing is skipped either way. | Reconnect at once on the unproven verdict, limited by the bucket: about 2 s to heal a real loss, and a relay can spend the bucket with 59-byte frames. |
| I-D2 | Addendum 1, G1 (c): "an unauthenticated message never changes persisted state". | Literal and total, with one named exception (the handshake digests). The second check's "no harm found" counters are removed, not tolerated. | Allow counters judged harmless. That judgement was wrong once (R2-9 became R3-1). |
| I-D3 | Addendum 2 item 3: "a relay replaying everything it has seen cannot prevent an honest exchange from completing". | Replays of anything **delivered** before never take a place; and when the relay stops, the exchange completes within the bound. A relay still spending withheld messages may deny while it does [03 §9.1 row B]. | Literal: also while the relay is acting. Needs a handshake change (D-3). |
| I-D4 | [03 §4.4]: a relay buffer "so a short drop loses nothing"; [04 §3.8]: buffered per ordered pair. | The daemon does not rely on the relay's buffer for delivery: a fresh key exchange per attachment makes buffered frames unreadable, and the outbox is the durable copy. So the buffer is flushed whole. | Keep channel keys across attachments so buffered frames stay readable. That means storing channel keys and contradicts "a fresh handshake per connection" [03 §10.4]. |
| I-D5 | PROTOCOL.md: `chan.ack` is "cumulative, per ordered pair". | An acknowledgement above anything sent means "all of it", as the relay code does. | Acknowledge the largest number seen in the tick, without storing it. It still reads a HINT, and a relay that replays one old frame last in each tick keeps the buffer full. |
| I-D6 | [03 §4.5]: "exchange `resume{last_seq_received}`, and replay the outbox". | In that order: the replay starts after the peer's position has arrived and covers only what is above it. | Replay at once and let the receiver drop duplicates (today's behaviour, and R3-2's amplifier). |
| I-D7 | Brief §5 test 5: "delivered exactly once, in order". | When a damaged outbox file has lost messages, their numbers are sent as skips, the loss is counted and reported, and later messages flow. | End the session when an outbox file is damaged. |
| I-D8 | The current code reconnects on a proven application gap [engine.rs:2879-2883]; the red row asserts only that the message "must not be delivered". | Not delivered, counted, shown as `desync`, no reconnect: a new channel cannot repair a number the peer itself stated. | Reconnect (today). With a peer that keeps doing it, a loop at the attachment budget. |
| I-D9 | Addendum 2 item 3: "`connected` is true only when messages can flow". | True when a channel proven by both sides exists and positions were exchanged; status adds how long since a frame last opened. A channel can have broken silently since; the first message then heals it within the bound. | An authenticated heartbeat so that `connected` means "proven in the last N seconds". A new feature and steady background traffic; not added. |
| I-D10 | [03 §10.4]: "token bucket per session (default 50 messages/s …)". | Not part of recovery. The in-flight limit of R4 exists only to keep an honest sender inside the relay's buffer. | Build the per-session rate limit here. |
| I-D11 | The roster seat's request (8.1). | Covered by V10 as a rule; built when the intake is wired. | Build persistence for an object the daemon does not yet hold. |
| I-D12 | [06 §4.3] fixed text for a changed relay identity: "do not retry". | Addressed to the person. The daemon keeps trying at its slowest cadence, because a refused TLS handshake is safe and the host may restart the relay with the saved identity. | Stop trying until a new line is pasted. |
| I-D13 | [03 §9.1 row D] puts a same-user attacker out of scope; the third check records file rollback as out of scope (R3-6). | A rolled-back state file is outside the fault model; row 44 says what is then visible. A crash and a full or damaged disk are inside it. | Add a rollback counter in the identity file [r1 verdict G17, direction]. |

### 10.2 UNDECIDED, for the owner

| # | The decision | Options | Recommendation |
|---|---|---|---|
| **D-1** | **Should a session ever end by itself because the other person has been away?** The first design says: pause after 5 minutes, end after 30 [03 §4.5]. The current build does neither. | (a) Never: it shows "not connected since …", keeps your unsent messages, and ends only when you or they end it. (b) As first designed: 5 and 30 minutes. (c) End after a long period, such as 7 days. | **(a).** With (b), a relay that withholds traffic for 30 minutes, or a laptop asleep over lunch, ends a session for good: the fault this redesign exists to remove, built in on purpose. |
| **D-2** | **Should the assistant be told when messages were lost on your own computer** (a damaged file, a message that could not be sent)? Today only the status command and a log line say so, and the assistant cannot see either [r3 verdict R3-8]. | (a) Yes: one fixed, count-only sentence in the next tool result. (b) No: status and log only. | **(a).** Otherwise the assistant was told "sent" and never learns otherwise. It adds two fixed sentences to what a tool result may contain. |
| **D-3** | **Accept that a relay which keeps interfering can block the key exchange by spending handshake messages it withheld earlier** (5.4; the third check's R3-4)? | (a) Accept and say so: it ends when the relay stops. (b) Commission a change to the handshake in the merged cryptography crate so the responder adds freshness. That reopens a crate that passed two checks, and costs a build and a check of its own. | **(a).** The first design already accepts denial by an active relay. |
| **D-4** | **Accept the proposed recovery times**: back to work within two minutes after interference stops, and about 17 seconds (was about 2) for a single lost packet in an otherwise healthy session? | (a) Accept. (b) Faster: more background traffic and a weaker limit on what a hostile relay can make your computer send. | **(a)**, and revisit after the build seat has measured it. |
| **D-5** | **Already with you as [06 I-11], not new:** within one session, should the starter's computer hand its restarted relay the same identity, so the other side reconnects without a pasted line? | As [06 §4.2] sets out. | It decides whether table row 18 is a recovery or a human step. This design works with either. |

### 10.3 UNKNOWN: why, and what closes it

| # | Unknown | Why | What closes it |
|---|---|---|---|
| U-D1 | Whether F-A to F-J behave as I read them | Nothing was run | Step 0 |
| U-D2 | That the relay accepts `upto = u64::MAX` in `chan.ack` and in `resume_from`, end to end | Read in the state and frame modules (the frame tests encode `u64::MAX`); not run through a socket | A test in step 0; the fallback is I-D5's alternative |
| U-D3 | Which existing tests and red rows change colour beyond those named in section 6 | Nothing was run; the third check's own test files were not read | The build seat's run at each step |
| U-D4 | Whether the relay's state module can be used directly by the model harness | I did not read the relay crate's `lib.rs` exports | Step 2; otherwise a small model relay checked against a real relay process |
| U-D5 | The real recovery time against the 120 s, and the real cost of the 5 s idle flush | Derived from clocks | Step 8, measured in simulated and in real time |
| U-D6 | The third check's mutation results | Its table is an unfilled placeholder in the file I read (`{{MUTTABLE}}`, line 225; `{{GAPROWS}}`, line 67) | Friday, from the gate's own logs |
| U-D7 | Whether [03], [04] or [06] say anything on recovery outside the sections I read | I read those three in part (appendix) | A full read by whoever briefs the build seat, or a correction to this file |

### 10.4 Every number proposed here

All "proposed, not measured": 120 s (V4); FLUSH at 100 ms and 5 s; the bucket (5, 12 s); 1 key-exchange start per second; 8 handshake messages examined per second; T-BLIND 15 to 60 s; T-HELD 30 s; in flight 128 frames and 1 MiB; reserve block 4096; the limit 2^62; 256 skips; 60 log lines per minute. Kept from the code and not mine: every other figure in section 7.

---

## Appendix: what I read

**Whole:** the three verdicts (`gate_M1_DAEMON_verdict.md`, `_r2_`, `_r3_`); `05_kam-rulings-2026-11-17.md`; `07_audit-storage-accounting-redesign.md`; the daemon brief and addenda 1, 2 and 3; at main: `coagent-relay/PROTOCOL.md`, `coagent-crypto/src/channel.rs`; at d8b5b4b: `limits.rs`.

**In part, by line range:** at d8b5b4b `engine.rs` lines 142-285, 400-805, 883-1081, 1278-1497, 1566-1586, 2080-3229 (not read: pairing, invite and join, verify commands, relay child handling outside those ranges); `link.rs` 1-420; `wire.rs` 1-110; `store.rs` 186-290 and its list of types and functions; `docs/DAEMON.md` 181-256; `tests/reconnect.rs` 120-170. At main: `coagent-relay/src/state.rs` 154-192, 596-800, 830-894 and its outline; `frame.rs` 578-628 and the lines naming `upto` and `resume_from`; `limits.rs` by search; `coagent-crypto/src/kk.rs` 1-75; `channel_map.rs` 225-262. `STATUS_M1_DAEMON.md` lines 1-35, 75-93, 167-187, 209-245, 273-290, 302-401, 442-466. `STATUS_M3_ROSTER.md` lines 735-752 and a search for "intake". `03_architecture-design.md` §1, §3.5, §4.2-4.5, §9.1, §9.6, §10; `04_design-revision-rulings.md` §1, §3.5, §3.7, §3.8, §4.4; `06_design-addendum-rulings-2026-11-17.md` the revision note, §4, and the daemon and relay rows of §8 and §9.

**Not read:** `datadir.rs`, `release.rs`, `relay_child.rs`, `ipc.rs`, `invite.rs`, `coagent-mcp`; the relay's `server.rs`, `client.rs`, `tls.rs`, `lib.rs`; the cryptography crate's `noise.rs`, `sas.rs`, `pairing.rs`; every test file except the lines named; the three gates' test folders and mutation drivers; the other branches beyond the searches named in section 8.
