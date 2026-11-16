GO WITH NOTES — at head 3f60cf4056b627b18a183d39de006d3cd524e845 (branch `m1-core`, base `13bd10e`)

# Tier-1 QA gate — CoAgent M1 CORE (coagent-proto, coagent-crypto, coagent-roster)

Gate run 2026-11-17 by an independent reviewer that did not write the code. Findings only: nothing was fixed, committed or pushed. All builds and runs were in a private clone at
`/private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/1d34e9cf-ed94-49aa-ba4c-99451dcbbc42/scratchpad/gate_m1_core/repo` (checked out at 3f60cf4), with `CARGO_TARGET_DIR` inside that scratch dir.
Tests named below as `gate_*` are in that clone only:
`crates/coagent-crypto/tests/gate_adversarial.rs` and `crates/coagent-roster/tests/gate_roster.rs`. A `gate_fail_*` test asserts a property the code should have and FAILS at 3f60cf4. A `gate_demo_*` test PASSES and shows a behaviour discussed below. A `gate_ok_*` test is an attack that was refused.

**No Blocker and no Major.** I found no way for either side to report `Paired` with keys that differ, no path from bytes to an application message without an AEAD open, no way to overwrite a channel in the map, and no roster rule I could bypass with convener-unsigned input. The notes below are real, though. The biggest is the test gaps: 11 of my 20 security mutations SURVIVED. The code I read is correct at those points, but nothing would catch a regression there.

## 1. Findings

| id | sev | file:line | what | how demonstrated | direction |
|---|---|---|---|---|---|
| F1 | Minor | coagent-crypto/src/sas.rs:234-235, 254-273 | The ceremony runs without the local human. A peer's `commit` is answered in `Idle` with no local `verify_start`. A peer's `request` makes the committer commit on its own. Either way the local attempt count drops and words reach the local human unprompted. A peer (the middleman, in the G4 scenario) can burn all 3 attempts and lock the pair before any human presses Verify. This turns a would-be HARD STOP (evidence against the convener) into a quiet `Locked`. G4 §6 says the ceremony runs "when a human presses Verify". The 3×2^-31 bound still holds; this is denial of service plus suppressed detection, not a higher match probability. | **RAN** `gate_fail_peer_cannot_consume_local_attempts_without_local_verify`: FAILS, the pair goes `Locked` with zero local presses. | Accept `commit`/`request` only while the local side is armed (local Verify pressed within a time window). Otherwise refuse without counting, or surface it as "peer asks to verify" for the human to accept. |
| F2 | Minor | coagent-crypto/src/channel_map.rs:76-92, 165-176 (pair = `(session, peer KeyId)`) | The cap and the hard stop are keyed on the peer KEY, not on the roster slot or person. A hostile convener whose ceremony hit HARD STOP can remove "P" and re-add "P" under a fresh key. The roster rules allow that as a new entry. That key gets a fresh channel and 3 fresh attempts, so the "per pair per session" cap of G4 §6 can be refreshed as often as humans will repeat the ceremony. | **RAN** `gate_demo_hard_stop_and_cap_reset_by_a_fresh_key_for_the_same_slot` (passes: insert accepted, `attempts_left: 3`). | Design owner: also count per slot or per session, and/or have a HARD STOP make the daemon distrust the convener's later re-adds of that slot (or flag them loudly). Ties to DQ 8. |
| F3 | Minor | coagent-crypto/src/channel_map.rs:222-251, sas.rs:315 | `verify_confirm(matched)` is not bound to the words the human compared. The peer can replace a pending ceremony: an invalid step returns `AwaitingHuman{w1}` to `Idle`, then a new commit/open gives `AwaitingHuman{w2}`. A "match" the human gave for w1 then pins w2's ceremony. Match probability is still blind per ceremony, so this is a UI-race hazard, not a break. | **RAN** `gate_demo_confirm_is_not_bound_to_the_words_shown` (passes). | Have `verify_confirm` take the words (or a ceremony id) it confirms, and refuse on mismatch. |
| F4 | Minor (test gap) | coagent-crypto/src/kk.rs:35-49 | No test pins the KK prologue. Dropping the roster hash from it (M09) or dropping both slots (M10) passes the whole suite. The roster hash in `h` is what G4 §6 relies on for "a match also exposes roster equivocation", and the brief's §4 names the prologue contents. | **RAN** mutations M09 and M10: SURVIVED. | Add a test: two members with different `roster_hash`, or with swapped slots, must fail KK. |
| F5 | Minor (test gap) | coagent-crypto/src/pairing.rs:148-163 | No test checks what the key-confirmation MAC covers. M01 (same role label both ways) and M02 (drop `h` from the MAC) both SURVIVED. Today reflection is still stopped by the per-direction transport keys, but neither binding has a guard. | **RAN** M01 and M02: SURVIVED. Reflection of a confirm checked by **reasoning only**. | Unit tests: a MAC computed for the other role is refused, and a MAC over a different `h` is refused. |
| F6 | Minor (test gap) | coagent-crypto/src/pake.rs:157-167, 176-191, 213-217 | Context binding is untested. Dropping `ctx` from the SPAKE2 identities (M13) or from the HKDF info (M14) passes everything. That is the "a code cannot be replayed against another relay or mailbox" property. | **RAN** M13 and M14: SURVIVED. | Test: the same code with a different `relay` or `mailbox` on one side must fail on both sides. |
| F7 | Minor (test gap) | coagent-roster/src/lib.rs:320-323, 346-350 | (a) The check that `key_id` equals the id computed from the keys is untested (M19 SURVIVED). The impact is limited because `admit` uses the channel's true id. (b) A first roster whose member is both `removed{at_version:n}` and re-added with `added_in:n` is refused only by `<=`. Weakening it to `<` (M08) SURVIVED. | **RAN** M19 and M08: SURVIVED. | One test each. |
| F8 | Minor (test gap) | coagent-crypto/src/channel_map.rs:111-121 | "Closing a channel mid-ceremony counts as a failed attempt" is untested. Removing the `v.abort()` in `close` (M11) SURVIVED. The existing test calls `verify_abort` BEFORE `close`, so it never exercises this path. | **RAN** M11: SURVIVED. | Close while in `CommitSent`/`RevealSent`/`AwaitingHuman` and assert the attempt was counted and the state is `Idle`/`Locked`. |
| F9 | Minor | coagent-crypto/src/channel.rs:211 | `Channel::seal_record` is `pub`. A local caller can send a `Rekey` record without rotating its own outgoing key, which breaks the channel for good: every later envelope gets `AeadOpenFailed`. It also skips the sender's epoch counting and the `NotConfirmed` gate. Receivers still check everything, so this is an API footgun, not a remote attack. | **RAN** `gate_demo_public_seal_record_can_desynchronise_rekey` (passes). | Make it `pub(crate)`, or keep `Rekey`/`KeyConfirm`/`Envelope` out of the public path. The hostile-peer tests can use a test-only feature. |
| F10 | Minor | coagent-crypto/src/identity.rs:286 | Low-order X25519 static keys are accepted; only all-zero is refused. A member, or a convener, can register a small-order Noise key with a valid binding signature. Anyone who hand-rolls Noise can then complete KK as that slot, because `ss` and `es` become known. The convener can already lie about keys, so the realistic gain is repudiation by the member itself. Already in BACKLOG. | **Reasoning only.** I did not build a hand-rolled Noise responder. | Reject the 12 known small-order encodings, or check that the DH output is non-zero after the handshake. |
| F11 | Minor | coagent-crypto/src/pake.rs:218 (dependency `spake2` 0.4.0) | The code words go into `spake2::Password(Vec<u8>)`, and `Spake2` keeps `password_vec`. spake2 0.4.0 has no zeroize at all: 0 hits for "zeroize", against 76 for "Password", in its `lib.rs`. So the secret words outlive `Zeroizing`. BACKLOG and CRYPTO-GLUE mention only `snow`. | **RAN** a grep of the registry source. | Add to BACKLOG/CRYPTO-GLUE. The impact is low, since a code is single-use. |
| F12 | Note | coagent-roster/src/lib.rs:393-407 | `RosterChain::start` takes no local key. A first roster that does not list the joiner, at any version, is accepted (DQ 15). A hostile convener can give a joiner a private history. That only shows up as KK failures with other members (prologue mismatch), never as `ForkEvidence`, until the §3.9 head exchange exists. | **RAN** `gate_demo_first_roster_need_not_contain_the_joiner_and_may_be_any_version` (passes). | `start(…, local: &KeyId)` should require self-membership. Document that fork evidence needs cross-member exchange. |
| F13 | Note | coagent-roster/src/lib.rs:455-510 | A role change between versions (observer to guest) is accepted, and `Applied` does not report it. 04 §3.6 suspends grants on "any roster change", so the caller needs to see it. | **RAN** `gate_demo_role_change_is_not_reported_in_applied` (passes). | Add `role_changed` to `Applied::Advanced`. |
| F14 | Note | coagent-roster/src/lib.rs:316-337 | Two members may share one Noise static key under different key ids: the attacker signs the victim's Noise key with the attacker's own signing key. The validator accepts it. KK is still safe because the slots in the prologue differ, by my reading. | **RAN** `gate_demo_two_members_share_one_noise_static` (passes). KK safety is reasoning only. | Refuse duplicate `noise_static` and duplicate `sign_pub` in `validate_one`. |
| F15 | Note | coagent-crypto/src/channel.rs:235-265 | Forgery attempts at the expected `seq` are unlimited and never close the channel: 10,000 tampered frames, then the genuine one still opens. That is the intended "no burn" behaviour, and with ChaCha20-Poly1305 it is no practical oracle. Also, `open` allocates `ct.len()` bytes before `snow` refuses an oversized message, so the input size is not capped up front. | **RAN** `gate_demo_unbounded_failed_opens_leave_channel_open`. The allocation point is reasoning only. | Cap `frame.len()` at `SEQ_LEN + MAX_MESSAGE` before allocating. Consider a failure counter for logging. |
| F16 | Note | coagent-proto/src/canonical.rs:28-38 | The canonical decoder held against every malleability probe I tried. In `body`, `1` and `1.0` are two distinct canonical values: integer and float, each with exactly one accepted spelling. Consumers that compare numbers must not assume one form. `ProtoError::Malformed(e.to_string())` echoes peer-supplied text from serde errors (log injection, not secrets). | **RAN** `gate_ok_decoder_refuses_noncanonical_variants` (passes; see §3). | Document the number rule. Strip the input from error strings before logging. |
| F17 | Note | coagent-crypto/src/channel.rs:279-284; pairing.rs:313-317 | Defence-in-depth checks without tests: a `KeyConfirm` after confirmation (M15; `ChannelMap::open` refuses it anyway), and an inviter refusing a joiner hello that names a session (M17). | **RAN** M15 and M17: SURVIVED. | Optional tests. |
| F18 | Note | coagent-crypto/tests/verify_ceremony.rs:146-159 | `test6_commitment_binds_the_handshake_hash` does not guard what it is named for. With `h` removed from `commitment()` (M03) it still passes: the test's own formula includes `other_h`, so it mismatches anyway. M03 was caught only by `test6_last_mover_…`'s formula-equality assert (and by my `gate_demo` test). | **RAN** M03. | Assert that a commitment made by the CODE for `h` opens under `h` and does not open under `h'`. |

## 2. Reproduction (all RAN, in the clone)

- `scripts/check.sh`: **exit 0**. fmt ok, clippy `-D warnings` ok, `cargo test --workspace --locked` gave **51 passed, 0 failed** (48 CORE + 3 relay placeholders), `cargo deny check licenses` gave "licenses ok". The only warning is the manifest warning `unused workspace dependency rand_core` (scaffold; already in BACKLOG).
- Red controls: I ran a copy of `scripts/red-controls-core.sh` with only `cd` and `LOGDIR` repointed into scratch. **17 of 17 rows RED, green run 48 tests ok, exit 0.** For each row I read the panic text, and each went red on the named property: input accepted, wrong status, or secret printed, not a side error. Notes: `roster_no_version_check` also switches off the transition rules, so it is a combined control. `sas_no_cap` goes red on a status assertion (`Unverified{0}` vs `Locked`), not on a fourth ceremony actually running.
- Builder's numbers in STATUS (51 / 17 / 48) reproduced exactly.

## 3. Adversarial attempts that were REFUSED (ran or reasoned, as marked)

- Decoder (RAN): duplicate key in `body`, duplicate struct field, `1e0`, `-0`, `15e-1`, `é` for `é`, trailing space, BOM, `01`, dropped `null` field, 5,000-deep nesting. All were refused, with no stack overflow.
- No `Inbound` without AEAD (reasoned + builder proptest RAN): `Inbound` has private fields, no constructor, no `Deserialize`, and is built only at channel.rs:294. `admit` takes `&Inbound`. `decode_for_channel` yields only a wire `Envelope`.
- Key confirmation (reasoned): the inviter reports `Paired` only after AEAD-opening AND HMAC-verifying the joiner's confirm (`verify_slice`, constant time). The joiner does the same for the inviter's. Both MACs cover `h`, which covers both hellos, both statics and the PSK, with role labels per direction. A reflected confirm fails the AEAD (keys are per direction). Wrong code: the joiner fails at msg3. The inviter never succeeds, even if the abort is swallowed (builder test RAN). An attacker who guesses wrong gets no offline dictionary test from msg3: by my reading of SPAKE2, testing another password needs CDH.
- Channel map (reasoned + builder test RAN): no path overwrites an existing `(session, peer)`. The same key under two sessions gives two independent channels. A hard stop removes the channel and refuses re-insert.
- Roster (RAN builder tests + reasoned): signer pinned, version/gap/stale, prev_hash, fork evidence, cap, slot bound, duplicate key/slot, append-only `removed`, silent drop, member change, convener self-removal. I found no panics on attacker data: `check_transition` slicing is guarded by short-circuit; `have + 1` is unreachable at `u64::MAX` because `got <= have` returns first.
- Panics (reasoned, grep of src): no `unwrap`/`expect`/unchecked indexing on peer data in the src of the three crates. `WORDS[...]` indices are bounded by `index_of`/`random_below`/`encode31`.
- Secrets (reasoned + builder test RAN): every type holding key material has a hand-written redacting `Debug`. No secret type implements serde. `Secret32`/`Zeroizing` are used for our own secrets. `CryptoError` carries no key bytes. Comparisons of public values (commitment, keys) are non-constant-time, which is acceptable. The MAC check is constant time.

## 4. Mutation testing (RAN; one at a time, full `-p proto -p crypto -p roster` suite, file restored after each)

| id | mutation | result |
|---|---|---|
| M01 | confirm MAC: joiner label := "inviter" (same label both ways) | **SURVIVED** (F5) |
| M02 | confirm MAC: drop `h` | **SURVIVED** (F5) |
| M03 | SAS commitment: drop `h` | caught by `test6_last_mover_responder_cannot_change_its_value_after_the_opening` (and my gate_demo); see F18 |
| M04 | SAS words: drop `r_R` | caught by `test6_last_mover_responder_…` |
| M05 | receiver RekeyOverdue `>=` → `>` | caught by `a_sender_that_never_rekeys_is_refused` |
| M06 | roster: no gap check | caught by `test7_replayed_old_version_is_refused` |
| M07 | roster: no prev_hash check | caught by `test7_forked_chain_is_refused_with_evidence` |
| M08 | re-add rule `<=` → `<` | **SURVIVED** (F7) |
| M09 | KK prologue: drop roster hash | **SURVIVED** (F4) |
| M10 | KK prologue: drop both slots | **SURVIVED** (F4) |
| M11 | `ChannelMap::close` no longer aborts a running ceremony | **SURVIVED** (F8) |
| M12 | decoder: no `to` check | caught by `test4_envelope_from_disagreeing_…`, `envelope::tests::binding_mismatches_are_rejected` |
| M13 | SPAKE2 identities without ctx | **SURVIVED** (F6) |
| M14 | HKDF info without ctx | **SURVIVED** (F6) |
| M15 | channel accepts KeyConfirm after confirmation | **SURVIVED** (F17) |
| M16 | map insert refuses `Locked` instead of `HardStop` | caught by `test6_mismatch_pins_nothing_and_is_a_hard_stop` |
| M17 | inviter accepts a joiner hello naming a session | **SURVIVED** (F17) |
| M18 | roster: no session check | caught by `other_transition_rules` |
| M19 | roster: no key_id == computed id check | **SURVIVED** (F7) |
| M20 | roster: fork reported as Stale | caught by `test7_forked_chain_is_refused_with_evidence` |

9 caught, 11 survived. The surviving list is the missing-test list in F4–F8 and F17.

## 5. Scope check (RAN `git diff --stat 13bd10e..3f60cf4`)

**Clean.** 43 files, all under `crates/coagent-{proto,crypto,roster}/` (src, tests, build.rs, README, Cargo.toml), `docs/CRYPTO-GLUE.md`, `scripts/red-controls-core.sh`, `BACKLOG.md` and `Cargo.lock`. Root `Cargo.toml`: +4 lines, all ADDED under `[workspace.dependencies]`: a comment plus `zeroize =1.9.1`, `hmac =0.12.1` and `proptest =1.12.0` (dev only, `default-features=false, features=["std"]`). Licences were checked by `cargo deny` (ran). `serde_json` is not built with `preserve_order` or `arbitrary_precision` in today's graph (ran `cargo tree -e features -i serde_json`). The canonical test would catch `preserve_order`, because it rejects unsorted body keys.

## 6. The 16 design questions

| DQ | safe as built? | wire change / needs design owner | comment |
|---|---|---|---|
| 1 confirm after Noise, inside channel | yes | **yes** (03 §10.2 order; mailbox burn now triggered by `abort`, not `pake.confirm`) | Sound. Better than 03, because one MAC covers both the PAKE and the Noise result. |
| 2 `hello.session_id` | yes | **yes** | Inside the PSK-authenticated msg3, which is correct. |
| 3 roster `{body,sig}` + `added_in` | yes | **yes** | Fine. Add the F7 tests. |
| 4 cap == 8 exactly | yes | no | — |
| 5 failed opening = hard stop | yes | no | — |
| 6 hard stop scope | partly | design | It is local only; G4 says "shown on both consoles", and no message tells the peer. F2: keyed per key, so a re-add evades it. |
| 7 committer = Noise initiator; `request` | yes for match probability | **yes** (`SasMsg` record kind 4) | But see F1: peer-initiated ceremonies should need a local arm. The KK initiator is the lower key id, so a middleman can grind its key id to choose its role. That is harmless under commit-reveal (G4 §6). |
| 8 attempt count per (session, peer key), in memory | **no, as scoped** | design | F2 (fresh key = fresh cap). The restart reset is already in BACKLOG. |
| 9 in-band authenticated `Rekey` record | yes | **yes** (record kind 2) | F9 footgun. Time-based rekey is enforced only by the sender (acceptable). |
| 10 strict contiguous seq | yes (fail-closed) | design (relay must deliver in order per pair) | Any dropped frame wedges the channel until reconnect. That is acceptable given 03 §4.5 resume, but the daemon must treat `OutOfOrder` as "reconnect". |
| 11 public `decode_for_channel` | yes | no | It yields only `Envelope`, and `admit` needs `Inbound`. Acceptable. |
| 12 joiner hello exposed to an active attacker at msg2 | accepted risk | design | The active attacker learns the joiner's device public keys and display name without the code: a tracking identifier. Worth a line in the threat model. |
| 13 KK carries no hello | yes | design (features not negotiated on introduced pairs) | — |
| 14 observer chat without `audience` refused | yes | no | — |
| 15 joiner's first roster any version | **weak** | design | F12: also does not require the joiner to be in it. Equivocation surfaces as KK failure, not evidence. |
| 16 inviter completes first | yes | no | Keys never differ; the daemon must treat a silent peer as not connected. |

Flagged as wrong or incomplete: DQ 8 (F2), DQ 15 (F12), and the F1 aspect of DQ 7. Wire changes needing the design owner: DQ 1, 2, 3, 7, 9.

## 7. What I did NOT examine or could not verify

- **Not run:** a hand-rolled Noise peer for the low-order-key impersonation (F10), so that impact is reasoning only. No fuzzing (`cargo-fuzz`). No timing measurement of any comparison. No RFC 9382 vectors (not applicable to spake2 0.4).
- **Not read line by line:** the 1,296-word list contents (only the builder's shape test, which ran), `snow`/`spake2`/`ed25519-dalek` internals beyond the spake2 zeroize grep, the builder's `frame_decoder_prop.rs` strategy details, and `mesh.rs`/`roles.rs` beyond their red-control evidence.
- **Not checked:** zeroize behaviour at runtime (memory inspection); `cargo deny` advisories (only licences); the design documents' §10.2–10.4 in full (§4.2 rows and 04 §3.2–3.8 were read; 03 §10.3 was not); RELAY-crate interaction.
- The offline-dictionary resistance of SPAKE2 and the no-reflection argument (F5) are reasoning only.

## 8. My own slips (none affects a finding)

- My first mutation-script classifier reported every mutant as "BUILD ERROR", because it grepped `^error` and that also matches cargo's "error: test failed". I reclassified all 20 from the saved logs (`mut_M*.log` in the scratch dir) using `error[E`/"could not compile". The table above is the reclassified result.
- In the decoder probe, two of my variants were wrong at first. I expected `1.0` for `1` to be refused, but it is a distinct canonical value (now F16). My `é` escape was written as a literal `é`, a no-op variant. I fixed both and re-ran; the test now passes.
- The mutation runs included my own `gate_*` tests. `gate_fail_*` was excluded from "caught". `gate_demo_confirm_is_not_bound_to_the_words_shown` also caught M03, and the builder's suite caught M03 independently, so no counts change.
