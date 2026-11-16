GO WITH NOTES — at head bcb55e0d70236308046be5f40d9b11e892ce2327 (branch `m1-core`, delta `3f60cf4..bcb55e0`, 4 commits)

# Tier-1 QA gate, round 2 (DELTA gate) — CoAgent M1 CORE

Gate run 2026-11-17 by an independent reviewer. I did not write this code and did not run round 1. Findings only: nothing fixed, committed or pushed. All runs were in my own clones under
`/private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/1d34e9cf-ed94-49aa-ba4c-99451dcbbc42/scratchpad/gate_m1_core_r2/` (`repo` for tests, `repo-mut` for mutations, `repo-seam` for the F9 probe), each at bcb55e0. Toolchain: the pinned 1.100.0 (`RUSTUP_TOOLCHAIN=1.100.0`, clippy 0.1.100), `CARGO_TARGET_DIR` in scratch.
My attack tests: `gate_core_tests_r2/gate_r2.rs` (beside this file; in my clone at `crates/coagent-crypto/tests/gate_r2.rs`). `gate_r2_fail_*` asserts a property the code should have and FAILS at bcb55e0; `gate_r2_demo_*` passes and shows a behaviour; `gate_r2_ok_*` is an attack that was refused. Mutation driver and raw results are there too (`mutations_r2.py`, `mutations_r2_results.txt`).

**Why GO WITH NOTES and not GO.** No Blocker and no Major. All eleven round-1 survivors are now caught. Every round-1 finding is closed or has its conservative half built. But the F1 fix is incomplete: **one** local press still lets a peer spend all three attempts and lock the pair (R2-1). A peer can also still make a human's "no match" vanish (R2-2), and 11 of my 28 new mutations survive. One survivor is a free-guess regression that no test would catch (N03). I recommend fixing R2-1 and R2-2 and adding the N03/N05/N06 guards **before merge**. Each is small and inside the scope already ordered for F1 and F3. Everything else can be deferred.

## 1. Gate-test integrity (the builder edited round 1's tests)

Method (RAN): `cmp` of the reference copies against `79499f6` (both byte-identical, so the builder's first commit added them unchanged), then `diff -u` of the reference copies against bcb55e0. Every difference, ruled:

| # | file / test | difference | ruling |
|---|---|---|---|
| D1 | gate_adversarial.rs header | `use std::time::Instant` → `{Duration, Instant}` | Needed for the new API. OK. |
| D2 | `gate_fail_peer_cannot_consume_local_attempts_without_local_verify` | one `assert!(\n !words_shown_unprompted,\n "…"\n );` collapsed to one line | **Whitespace only.** The expression and message are identical. No other hunk touches this test, so its logic is byte-for-byte the round-1 logic. It calls `ChannelMap::open` with no time (clock `None`, so unarmed): it tests the zero-press case, which is fixed. |
| D3 | `gate_demo_hard_stop_and_cap_reset_by_a_fresh_key_for_the_same_slot` | both sides press (`verify_start(…, now, 60 s)`); the crossing `request` is delivered to m0; the shown words are passed to `verify_confirm` | Needed. Without m2's press the commitment is declined. Without delivering the request, the next frame is out of sequence (`OutOfOrder`). The conclusion (plain `insert` of a fresh key in the same slot gets `attempts_left: 3`) is **unchanged and still demonstrated**. Not weakened. |
| D4 | `gate_demo_confirm_is_not_bound_to_the_words_shown` | a press before each ceremony; final assert flipped from "stale yes pins w2" to `Err(WordsChanged)` | Presses are needed (F1). The flip is the ordered F3 behaviour, and the red row `confirm_unbound` makes it fail. **But** the junk line that cancels `AwaitingHuman{w1}` without a press is unchanged and still works. That residual is R2-2. The edit hides nothing that R2-2 does not report. |
| D5 | gate_roster.rs header | import `RosterError` | Needed. OK. |
| D6 | `gate_demo_two_members_share_one_noise_static` | flipped to `Err(DuplicateDeviceKey(kid))`; `start` gets a local id | Ordered F14 behaviour, asserted on the exact error and key id. Strong. OK. |
| D7 | `gate_demo_first_roster_need_not_contain_the_joiner_and_may_be_any_version` | flipped to `Err(LocalNotMember)`. Dropped: the asserts `version()==6` and "joiner absent from the accepted chain" | The flip is ordered (F12), and the test now also asserts that the joiner is absent from the roster body. **Lost:** the "may be any version" half is no longer demonstrated. A first roster at v6 that DOES list the joiner is still accepted (reasoned from `start`, lib.rs:419-437: no version rule). That is DQ 15, an open owner item, not a guard that was removed. Note only. |
| D8 | `gate_demo_role_change_is_not_reported_in_applied` | local = the observer; flipped to `role_changed: [observer]` | Ordered (F13). It covers the local-member case. OK. |

**Ruling: no edit weakens a test or makes one pass for the wrong reason.** All four flips are exactly the behaviour changes the addendum ordered. Each flipped test goes red under its red control (RAN, §3). The builder's own pre-existing tests (roster.rs, mesh.rs, roles.rs, no_secret_in_debug.rs, verify_ceremony.rs) were also diffed. They received signature changes only, plus one assertion that was strengthened (`other_transition_rules` now checks `role_changed`). verify_ceremony.rs keeps every test name, its assert count went from 40 to 72, and each removed assert line reappears in its new-API form (RAN grep).

## 2. Round-1 findings F1–F18

| F | status | how I know |
|---|---|---|
| F1 | **CLOSED WITH A NEW ISSUE** | Zero-press case fixed (gate_fail test green; RAN). One-press case is not: R2-1 (RAN). Also R2-4 (`open` without time) and the N05/N06 survivors. |
| F2 | conservative half built, **WITH A NEW ISSUE** | `insert_with_slot` inherit and refuse paths work (builder test plus N11/N12/N13 caught; RAN). The slot record is not shared by concurrent channels in one slot, and plain `insert` bypasses it: R2-5 (RAN). N10 survives. The rest is the owner's call (A1.6-1). |
| F3 | **CLOSED WITH A NEW ISSUE** | A stale "yes" is refused (RAN). A "no" can be dropped: R2-2 (RAN). The binding check survives a first-word-only mutation (N08). |
| F4 | CLOSED | M09, M10 caught by `f4_kk_prologue_binds_roster_hash_and_slots` (RAN). |
| F5 | CLOSED | M01, M02 caught (RAN). |
| F6 | CLOSED | M13, M14 caught (RAN). Split `pake_finish` → `pake_raw_key` + `derive`: same `derive(&key, &ctx)` call on the same SPAKE2 output; `pake_raw_key` is a private `fn` returning `Zeroizing<Vec<u8>>`; no new `pub`, no Debug (reasoned, diff read). |
| F7 | CLOSED | M08, M19 caught (RAN). |
| F8 | CLOSED | M11 caught (RAN). |
| F9 | **CLOSED WITH A NEW ISSUE** | `seal_record` is absent from a plain build (RAN, probe compile error). It is present in any non-test binary built with `--workspace --all-targets`, and in an optimised custom profile: R2-6 (RAN). The build.rs mutation N28 is caught by the runner row (RAN). |
| F10 | CLOSED (test gaps) | Static check: exact on my independent list plus brute sweeps (RAN `gate_r2_ok_small_order_detection_is_exact_on_sweeps`). Ephemeral: KK msg1 (builder) and KK msg2 (mine, RAN). XX msg1/msg2 are unguarded (N18, N19 survive). The builder's red row is red on error kind only (R2-10). |
| F11 | CLOSED | BACKLOG and CRYPTO-GLUE G-5 entries present (read). |
| F12 | CLOSED | `LocalNotMember` (RAN, row red). The "any version" part is still owner DQ 15. |
| F13 | CLOSED (test gap) | Reported in every direction for members present in both versions, including the local member (reasoned, lib.rs:510-517; RAN demo for observer→guest). The N25 survivor shows only one change is ever tested. |
| F14 | CLOSED (per version) | Both kinds refused (N21, N22 caught; RAN). Reuse of a removed member's keys by a later entry is not refused (R2-11, reasoned). |
| F15 | CLOSED (test gap) | `MAX_FRAME = 8 + 65_535 = 65_543`. A legitimate maximum record is exactly `MAX_FRAME`, so `>` is correct (reasoned from `seal_raw`). No test pins the boundary: N23 (`>=`) survives. The counter is a `u64` incremented once per failed AEAD open, so overflow is unreachable (reasoned). |
| F16 | CLOSED | `describe()` gives category and position only (RAN row). Grep of every `format!`/`to_string`/`Malformed(` in the three crates' src: the remaining strings are fixed literals. `RoleError::{ObserverMayNot,ConvenerOnly}(kind.to_string())` fires only when `kind` equals one of five fixed literals, so no peer text is echoed. `CryptoError::Noise(snow::Error::to_string())` is snow's fixed text (reasoned). |
| F17 | CLOSED | M15, M17 caught (RAN). |
| F18 | CLOSED | M03 caught by `test6_commitment_binds_the_handshake_hash` (RAN). |

## 3. Reproduction (all RAN)

- `scripts/check.sh` (`bash <abs path>`, my target dir): **exit 0, 81 passed, 0 failed**. fmt and clippy `-D warnings` OK, `licenses ok`. The only warning is the known `unused workspace dependency rand_core`. Matches the builder.
- Red controls: a copy of `scripts/red-controls-core.sh` with only `cd` and `LOGDIR` repointed into scratch, run with its own target dir. **46 rows, 46 RED; release-seam control passes; green run 78 tests ok; exit 0.** Matches the builder. I read the panic text of all 29 new rows. Each goes red on its named property, as follows: a wrong status/step (`Reveal` vs `Decline`, `Locked`, `attempts_left 3 vs 2`, `InProgress`), the stale-words refusal (`None` vs `WordsChanged`), equal keys for different contexts, the named binding messages ("roster hash must be bound", "initiator slot must be bound", the MAC messages), an input accepted (`None` vs the expected roster error), `role_changed: []`, `AeadOpenFailed` vs `TooLarge`, a 0-vs-1 counter, the error text quoting `"ZZPEERTEXTZZ"`, `…0080 not detected`, and the build.rs refusal text.
  - **`ephemeral_small_order_ok` (red on error kind only): what it guards.** The test splices a small-order point into the first 32 bytes of a genuine KK msg1. Without the check, `snow` refuses it anyway (the msg1 payload tag no longer verifies), so the handshake fails either way. The row therefore guards only that the check exists and runs **before** `snow` on KK msg1. It does not demonstrate any security effect, and it does not guard KK msg2 or either XX message (N17–N19 survive). It is harmless but weak. The meaningful case, a self-consistent small-order ephemeral from a hand-rolled peer, is tested by nobody.
- Scope (`git diff --stat 3f60cf4..bcb55e0`): **clean.** 31 files: the three crates (src, tests, build.rs, Cargo.toml), `docs/CRYPTO-GLUE.md`, `scripts/red-controls-core.sh`, `BACKLOG.md`, `Cargo.lock`, and root `Cargo.toml` with +1/−0 lines, ADDED under `[workspace.dependencies]`: `curve25519-dalek = { version = "=4.1.3", default-features = false }`. 4.1.3 was already in `Cargo.lock` at 3f60cf4 (`git show 3f60cf4:Cargo.lock`), via snow/spake2. Its licence is BSD-3-Clause (its Cargo.toml in the registry), and `cargo deny` passed. The lock delta is only the crate's own dependency list (+`curve25519-dalek 4.1.3`, +the self dev-dependency `coagent-crypto`). Note: 5.0.0 is also in the graph (via ed25519-dalek 3), so 4.1.3 is the right match for snow's X25519.

## 4. Mutations (RAN; one at a time in `repo-mut`; full `cargo test -p coagent-proto -p coagent-crypto -p coagent-roster --no-fail-fast`; file restored after each; tree clean after the run)

### 4.1 Round 1's twenty, re-applied to bcb55e0

| id | result |
|---|---|
| M01 | caught: `pairing::tests::confirm_mac_binds_the_role` |
| M02 | caught: `pairing::tests::confirm_mac_binds_the_handshake_hash` |
| M03 | caught: `test6_commitment_binds_the_handshake_hash`, `test6_last_mover_…`, `gate_demo_confirm_…` |
| M04 | caught: `test6_last_mover_responder_cannot_change_its_value_after_the_opening` |
| M05 | caught: `a_sender_that_never_rekeys_is_refused` |
| M06 | caught: `test7_replayed_old_version_is_refused` |
| M07 | caught: `test7_forked_chain_is_refused_with_evidence` |
| M08 | caught: `f7_readd_in_the_removing_version_is_refused` |
| M09 | caught: `f4_kk_prologue_binds_roster_hash_and_slots` |
| M10 | caught: `f4_kk_prologue_binds_roster_hash_and_slots` |
| M11 | caught: `f8_closing_a_channel_mid_ceremony_counts_the_attempt` |
| M12 | caught: `envelope::tests::binding_mismatches_are_rejected`, `test4_envelope_from_disagreeing_…` |
| M13 | caught: `pake::tests::spake2_identities_bind_relay_and_mailbox` |
| M14 | caught: `pake::tests::hkdf_info_binds_relay_and_mailbox` |
| M15 | caught: `f17_key_confirm_after_confirmation_is_refused_by_the_channel` |
| M16 | caught: `test6_mismatch_pins_nothing_and_is_a_hard_stop` |
| M17 | caught: `pairing::tests::inviter_refuses_a_joiner_hello_that_names_a_session` |
| M18 | caught: `other_transition_rules` |
| M19 | caught: `f7_entry_key_id_must_match_its_keys` |
| M20 | caught: `test7_forked_chain_is_refused_with_evidence` |

**20 of 20 caught. All eleven round-1 survivors (M01, M02, M08, M09, M10, M11, M13, M14, M15, M17, M19) are now caught**, each by a builder test, not by a gate test.

### 4.2 New mutations on the delta (28)

| id | mutation | result |
|---|---|---|
| N01 | arming: window expiry ignored | caught: `f1_a_peer_cannot_run_…` |
| N02 | arming: unknown time (`None`) counts as armed | caught: `f1_a_peer_cannot_run_…` |
| N03 | committer un-counts a `decline` also in `AwaitingHuman` (a free guess after the words) | **SURVIVED** |
| N04 | no un-count on decline | caught: `honest_ceremony_…` |
| N05 | responder press not used up by an accepted commitment | **SURVIVED** |
| N06 | committer press not used up at the reveal | **SURVIVED** |
| N07 | unarmed committer counts the declined request | caught: `f1_…`, `honest_ceremony_…` |
| N08 | words binding compares only the first word | **SURVIVED** (first run looked "caught" only by the flaky test9, R2-8; re-run clean: survived) |
| N09 | a "no" for stale words is honoured (the direction I recommend in R2-2) | caught by `f3_the_answer_is_bound_to_the_words_compared`, which pins the refusal |
| N10 | slot inheritance: an existing per-key record is not raised to the slot count | **SURVIVED** |
| N11 | slot hard-stop check removed at insert | caught: `f2_…` |
| N12 | `sync_slot` does not record the hard stop | caught: `f2_…` |
| N13 | `sync_slot` does not record attempts | caught: `f2_…` |
| N14 | small-order check removed from `verify_device` | caught: `f10_small_order_noise_keys_are_refused` |
| N15 | small-order: compare one output byte | caught: 6 tests (genuine keys refused) |
| N16 | ephemeral read at the wrong offset (1..33) | caught: `f10_small_order_ephemeral_…` |
| N17 | KK initiator skips the responder-ephemeral check (msg2) | **SURVIVED** in the builder's suite (my `gate_r2_ok_ephemeral_…` catches it, RAN) |
| N18 | XX inviter skips the joiner-ephemeral check (msg2) | **SURVIVED** |
| N19 | XX joiner skips the inviter-ephemeral check (msg1) | **SURVIVED** |
| N20 | self-membership checks the convener, not `local` | caught: `f12_…`, gate demo |
| N21 | duplicate check: `sign_pub` not checked | caught: `f14_shared_device_keys_are_refused` |
| N22 | duplicate check: `noise_static` not checked | caught: `f14_…`, gate demo |
| N23 | `MAX_FRAME` comparison `>` → `>=` (refuses a legitimate maximum frame) | **SURVIVED** |
| N24 | `MAX_FRAME` cap doubled | caught: `f15_…` |
| N25 | `role_changed` reports only the first changed member | **SURVIVED** |
| N26 | `tick` lets time go backwards | **SURVIVED** |
| N27 | a crossing request makes the committer re-commit | caught: 6 tests |
| N28 | build.rs test-seam guard never fires | caught by the runner row `(test-seam in release)` (RAN its command), not by the suite |

**17 caught, 11 survived.** The security-relevant survivors are N03 (a middleman's free guess), N05 and N06 (one press, many ceremonies), N08 (weak words binding), and N17–N19 (ephemeral checks on three of the four message positions). The others are boundary or reporting gaps.

## 5. New findings

| id | sev | file:line | what | how demonstrated | direction |
|---|---|---|---|---|---|
| R2-1 | Minor (fix before merge) | coagent-crypto/src/sas.rs:285-297, 410-418 (`on_message` → `fail_current`) | **One committer press buys the peer three ceremonies.** An invalid message aborts the running ceremony: `fail_current` sets Idle and leaves the attempt counted, but it does not clear `armed_until`. The peer's next `request` finds the side still armed, and it commits again. After three rounds the pair is Locked on a single press, with no words ever shown and no hard stop. This violates the F1 rule "a press arms ONE ceremony", and it is the round-1 F1 harm (quiet lock, suppressed detection) behind one press instead of none. | **RAN** `gate_r2_fail_one_committer_press_cannot_be_spent_on_three_ceremonies` (FAILS: `(3, Locked)`), and `gate_r2_fail_one_press_locks_the_pair_over_a_real_channel` (FAILS: Locked, over a real KK channel and the map). | Clear `armed_until` whenever a counted ceremony ends (in `fail_current`), or when the first commitment of a press is counted. Add the test and a red row. |
| R2-2 | Minor (fix before merge) | sas.rs:423-441 (`human_says`); channel_map.rs:327-359; test verify_ceremony.rs:482-485 | **A human's "no" can be made to vanish.** After words are shown, any invalid peer message (or a close) returns the pair to Idle with the attempt counted. The human's "no" for the words they were actually shown is then refused (`UnexpectedMessage`), and a "no" for stale words is refused with `WordsChanged`. The mismatch never becomes a HARD STOP. G4 §6: "a mismatch read aloud is a hard stop". A "no" can never raise trust, so honouring it is always safe. The builder's `f3` test pins the refusal of a stale "no" (my N09 shows it). | **RAN** `gate_r2_fail_a_no_for_shown_words_is_always_a_hard_stop` (FAILS: `Err(UnexpectedMessage)`, `Unverified{2}`). | Keep the last words shown per pair. A "no" naming any words this pair showed is a hard stop for the pair and its slot. Refuse only a stale "yes". Change the `f3` assertion accordingly. |
| R2-3 | Minor (design; claim correction) | sas.rs:42 doc, CRYPTO-GLUE, G4 ANALYSIS §6 ("≤ 3 × 2^-31") | **Blind guesses per pair per session: 5, not 3.** A middleman M controlling both channels makes itself committer on both sides (it grinds its key ids; the KK initiator is the lower id). It learns each side's words before that side shows anything, because it holds its `open`. So a mismatch is never displayed and no hard stop can fire. Each comparison needs a fresh ceremony on only ONE side, and the cap is per side. Schedule (A1,B1) (A2,B1) (A3,B1) (A3,B2) (A3,B3) = **2·MAX_ATTEMPTS − 1 = 5** independent 31-bit comparisons, ending with both sides Locked and silent (≈ 2.3 × 10^-9, not 1.4 × 10^-9). The decline un-count adds **nothing**: an un-count happens only before `r_C` is revealed, and each guess needs a counted ceremony (RAN `gate_r2_ok_decline_uncount_gives_no_extra_guess_against_one_side`: 50 decline/request rounds per press, still exactly 3 ceremonies per side). The count is **unbounded** across plain-`insert` re-adds of fresh keys (F2 remainder) and across daemon restarts (BACKLOG). This is not introduced by the delta. Round 1 accepted the 3× figure. | **RAN** `gate_r2_demo_middleman_gets_five_blind_comparisons_per_pair_per_session` (passes: 5 comparisons, both Locked, nothing shown). The probability per comparison is reasoned from G4 §6. | Design owner: state the bound as (2·cap − 1)·2^-31 per human pair per session, or lower the cap. Make the slot path mandatory (A1.6-1c) so re-adds do not reset it. |
| R2-4 | Minor | channel_map.rs:238-253 (`ChannelMap::open`) | `open` judges arming against the **last time the map was told**. A daemon that calls `open` (public, no time argument) instead of `open_at` never lets a window expire: a commitment an hour after the press is taken. The safe behaviour depends on the caller choosing the right one of two public functions. | **RAN** `gate_r2_demo_open_without_time_never_expires_the_window` (passes: `InProgress`). | Make `open` take `now`, or make the time-less `open` treat ceremony messages as unarmed. |
| R2-5 | Note | channel_map.rs:130-150, 159-166 | The slot record is inherited **only at insert**. Two keys of one slot that are open at the same time (fresh key inserted before the old channel is closed) do not share it. The old key's hard stop leaves the new key's channel up with 3 fresh attempts. A plain `insert` after a slot hard stop is accepted. Order-dependent: "a fresh key inherits used attempts" holds only if the caller closes first. | **RAN** `gate_r2_demo_slot_record_not_shared_by_concurrent_channels` (passes). | On a slot hard stop, close and refuse every pair whose `slot_of` is that slot. Have `sync_slot` raise all pairs in the slot. Or make the map refuse a second open channel per (session, slot). |
| R2-6 | Note | coagent-crypto/Cargo.toml (self dev-dependency with `test-seam`); build.rs:54-58 | Feature unification puts the seam into **non-test binaries**. `cargo build --workspace --all-targets` (what `check.sh`'s clippy step and `cargo test --workspace` do) compiles any workspace binary depending on coagent-crypto with `test-seam` on. build.rs checks only `PROFILE == "release"`. A custom profile `inherits = "dev"` with `opt-level = 3` gives an optimised binary with the seam, and build.rs passes it. Also `cargo test --release -p coagent-crypto` can no longer build. No such binary exists today (coagent-cli does not depend on crypto). | **RAN** probe crate `zz-probe` (`gate_core_tests_r2/seam_probe_*`): `cargo build -p zz-probe` gives E0599 (good). `--workspace --all-targets` builds it, and the binary prints the address of `seal_record`. `--profile ship` (inherits dev, opt 3) does the same. `cargo test --release` gives "the test-seam feature is for test builds only". | Move the hostile-peer tests into crate-internal `#[cfg(test)]` modules, or gate the seam on a `cfg` the test scripts set (`RUSTFLAGS=--cfg coagent_test_seam`) instead of a Cargo feature. At least document it. |
| R2-7 | Minor (test gaps) | see §4.2 | 11 new survivors. Most important: **N03**. A middleman's un-count after the words would give it a free guess per ceremony, and nothing catches it. Then N05/N06 (press reuse), N08 (binding), N17–N19 (three of four ephemeral positions untested). | **RAN** mutations. | One test per survivor. My `gate_r2.rs` catches N03 (`gate_r2_ok_decline_uncount_…` fails under it) and N17 (`gate_r2_ok_ephemeral_check_…` fails under it) (**RAN**, each mutant applied with only `gate_r2.rs` added). |
| R2-8 | Note | coagent-crypto/tests/no_secret_in_debug.rs:131-133 | `test9_no_secret_bytes_in_debug_or_display` is **flaky**. It asserts that no code word occurs as a substring of any Debug output, but "stage" is in the 1,296-word list and also a Debug field label (`Pairing { …, stage: AwaitPake }`). So the test fails whenever "stage" is drawn: about 3/1296 ≈ 0.23 % of runs, plus a negligible "cafe"-in-hex chance. | **RAN**: observed once in about 50 suite runs (mutation N02's log: `code word \`stage\` in: Pairing { … stage: AwaitPake }`). The rate is reasoned. | Draw the test's code with words that are not Debug labels, or match the redaction form instead of raw substrings. |
| R2-9 | Note | sas.rs:132-141, 316, 366-369 | `decline` tells the peer whether this side's human has pressed: a presence and timing signal to a middleman. Unbounded `request`/`commit` floods each produce a `decline` frame and `peer_asks_to_verify`, a UI nuisance with no rate limit. Neither affects match probability. | Reasoned. RAN flood of 50 per press inside the R2-3 bound test. | Owner: rate-limit `peer_asks_to_verify` in the daemon. Accept the signal or drop the reply (A1.6-2). |
| R2-10 | Note | gate_return.rs:216-234; runner row `ephemeral_small_order_ok` | The row guards only "the check exists and runs before snow on KK msg1". See §3. | **RAN** row and N16/N17. | Add msg2 and XX cases. A hand-rolled peer would be needed for the real effect. |
| R2-11 | Note | coagent-roster/src/lib.rs:320-350 | The duplicate-key rule is **per version**. A removed member's `noise_static`/`sign_pub` may reappear in a later version under a new key id: the attacker's signing key binds the victim's Noise key, the round-1 F14 shape across versions. The convener is already trusted to add anyone, so the gain is small. | Reasoned (validate_one sees only the current members; `check_transition` compares by key id). | Optional: also refuse keys of `removed` entries. |

**Answers to the specific attack questions in the brief:**
- A peer can consume local attempts **without** a press: no (RAN, the gate_fail test plus builder tests). **With one press**: yes, all three (R2-1).
- Decline flooding: no extra attempts or guesses (RAN). Commit exactly at the window edge: accepted, inclusive at `now + window` and declined 1 ns later (RAN `gate_r2_ok_window_edges`). `now = None`: unarmed (RAN, builder test plus N02 caught). Time going backwards: a `now` before the press still counts as armed (RAN). The map's `tick` ignores backward steps, untested (N26).
- Two ceremonies to words inside one window on one press: no, on both roles (RAN). Two counted ceremonies on one press: yes, committer side (R2-1).
- Un-count abuse by a hostile responder for unlimited guesses: no (RAN, the 3-per-side bound holds). Middleman total: **5 per pair per session**, unbounded with key re-adds or restarts (R2-3).
- F3: a peer swap whose words collide (2^-31) is equivalent to a successful guess and now needs a second press (reasoned). A stale "no" is refused, which I judge wrong (R2-2).
- F2: `insert` bypasses the slot record when the caller uses it (by design, owner A1.6-1c). Inheritance holds only if the old channel is closed before the new key is inserted (R2-5). `sync_slot` and the override are driven only by local state and local calls, and the slot number comes from the caller (the convener's roster), never from peer frames (reasoned).
- F10: the claim is correct. A clamped scalar is 8·m with m < 2^252 < ℓ < ℓ′, so the output is zero iff the order divides 8 (curve) or 4 (twist). dalek reduces non-canonical input and ignores bit 255. The 7 values (0, 1, two order-8 points, p−1, p, p+1) plus their top-bit forms are all detected, and sweeps of [0,4096) and [p−4096, p+18] find no others (RAN). Offsets: every message 1 and 2 of XXpsk3 (psk at msg3) and KK begins with `e` (32 bytes), so `get(..32)` is right. No 48-byte assumption, because the length comes from snow. Short input gives `BadKey`, and every prefix length of KK msg1 and msg2 errors without panicking (RAN). Unchecked: the hello static of XX is processed by snow (`es`/`se`) before `verify_device` refuses it. The pairing then fails, so nothing is gained (reasoned). Rekey has no DH.
- F6: unchanged in substance (§2).

## 6. DECISIONS FOR THE OWNER (A1.6) and the `decline` wire step

- **A1.6-1 (F2 remainder):** agree it is the owner's call. My input: (c) should be **yes**, make the slot path mandatory, because with plain `insert` the per-pair cap means nothing against a hostile convener (R2-3 unbounded). (a) and (b) are design. Also fix R2-5 when the daemon wiring lands. This does not block merge.
- **A1.6-2 (`decline`):** **safe as implemented with respect to match probability** (RAN, R2-3 bound test). The un-count is sound only because it is restricted to `CommitSent`. That restriction is load-bearing and **unguarded** (N03 survives), so add the guard before merge. The step leaks press status to the peer (R2-9). The alternative ("no reply plus a counting time-out") costs honest users an attempt per mistimed press, so `decline` is the better choice. It is a wire addition for the owner's sign-off, alongside DQ 1, 2, 3, 7, 9.
- **Must be fixed before merge rather than deferred:** R2-1 (the F1 fix is incomplete, inside the ordered scope), R2-2 (the F3 handling of "no"), and guards for N03, N05, N06. The rest (R2-3 to R2-11, the other survivors) can be deferred with BACKLOG entries.

## 7. What I did not examine

- No hand-rolled Noise peer, so a self-consistent small-order ephemeral or static end to end is untested by me as well (F10 effect is reasoned). The XX ephemeral paths (N18, N19) were mutated but not exercised by a test of mine.
- No fuzzing, no timing measurement, no memory inspection for zeroize, no `cargo deny` advisories (licences only, via check.sh).
- Not read line by line: the builder's `gate_return.rs` roster tests beyond their red evidence; the 417-line rewrite of `verify_ceremony.rs`, which I checked by test names, assert counts, removed-assert reappearance and mutation results, not every line; `frame_decoder_prop.rs`; the word list contents; snow/spake2/dalek internals (dalek's non-canonical handling is reasoned and checked by the sweep).
- Not checked: interaction with the RELAY crate or a daemon; persistence across restarts (still in memory, BACKLOG); 03 §10.3; 04 §3.3-3.6 beyond what the findings cite. I read G4 ANALYSIS §6 in full.
- R2-3's probability arithmetic is reasoned from G4 §6. The test demonstrates the schedule and the absence of any display or hard stop, not the probabilities.

## 8. My own slips (none affects a finding)

- My first `git -C $VAR checkout` calls were refused by the workspace's no-cd hook (it could not see that the variable pointed into scratch). I re-ran them with literal scratch paths. No effect on any repo outside scratch.
- Two of my own tests had bugs on the first run: the third press hit `Locked` (expected), and I dropped a crossing `request` frame, which broke the sequence order. I fixed both. The final run is 7 pass and 3 FAIL, the three FAILs being the intended `gate_r2_fail_*`.
- N21 and N22 first failed to build (type inference on an unused `BTreeSet`). I re-wrote them so the set stays typed, re-ran, and both were caught.
- N08 first read as "caught". The only failing test was the flaky test9 (R2-8). A re-run shows it SURVIVED. This is also how I found R2-8.
- The mutation runs did not include my `gate_r2.rs`; they ran in a separate clone. Nothing in "caught" is credited to my tests.
