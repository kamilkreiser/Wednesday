VERDICT: NO GO — head d88d5d78efa264abbca78e97c143698718393931

---
date: 2026-11-17
type: reference (QA gate verdict, tier 1, round 2 of 2, findings only)
project: General / CoAgent (no client)
subject: branch m3-roster, crate coagent-roster
base: main 18005d63ae1311df9649893060caf1f98510a4c1; round 1 at 0a47fc9
---

# Gate M3-ROSTER round 2: verdict

Head confirmed by `git rev-parse HEAD` on a fresh clone of `m3-roster`: `d88d5d78efa2…` (RAN). Merge-base with `origin/main` = `18005d6` (RAN). All work in scratch clones; nothing pushed; no git write verb inside the project tree. Red-control logs went to a scratch `COAGENT_TOOLS` (symlinked toolchain), not to the project's `tools/tmp`.

**Why NO GO.** One Major, and it is a test gap, not wrong behaviour. The code now does the right thing on every input I found. But the round-1 Major F2 was ordered fixed "as a class", with a property test as its guard. **That guard does not guard it.** If the validator call that `approve` now makes is deleted, or if a refused approval goes back to staling and charging everyone else, the branch's whole suite stays green: 109 tests, the gate file included, and the property test too (mutants N01, N03 to N06 and N33, all RAN). There is a real input on which that validator call is the only defence (R2-1). The red row the builder offers for this property (`approve_no_validate`) only goes red because it is widened to switch off `receive`'s checks as well, so what it shows is that `receive` is guarded. Because nobody else reviews this code, a guard that cannot fail counts as no guard. The fix is small: one test on the reachable input below, plus that input added to the property generator.

Everything else holds. Every figure in STATUS reproduced. Round-1 F1, F4, F7, F8, F10 and F11 are closed, and F2's behaviour is fixed. The rest is Minor or Note.

## 1. Findings

| id | severity | file:line | exact sequence | RAN / REASONED |
|---|---|---|---|---|
| R2-1 | **Major** (test gap; code correct) | `src/intake.rs:529-541` (validator run and refused-approval path in `approve_with_report`); guard `tests/gate_return_a3.rs:275-377` | **Reachable input where the validator run is the only defence.** Version 3 holds C, admitted through P's proposal with id 7. The starter's daemon builds a NEW `ProposalIntake` for the session (the intake lives only in memory, so this happens on any restart). Q proposes D (pending). Hostile P proposes E **with proposal id 7**. `receive` → `Ok` (card shown): check 10 looks only at the intake's own records, never at the ids already on the roster. `approve` → `Err(InvalidApproval(DuplicateProposalId(E)))`, E's proposal is `RefusedInvalid`, Q is still pending and uncharged, and Q's later approval validates. That is correct. **Mutants on this path that the branch's 109 tests do not kill:** N01 (no validator run), N03 (`validate_body` dropped), N04 (refused proposal left pending), N05 (refused approval stales every other pending proposal: the round-1 F2 harm), N06 (refused approval charges every proposer), N33 (recorded as `Declined`). Each of them is killed by my `qa_r2.rs::r2_f2_proposal_id_carried_by_an_existing_entry_reaches_a_card`. **Property-test coverage:** with `receive` intact, every invalid candidate kind the generator makes (sign twin, Noise twin, current member, version 256) is refused at `receive` and the case `continue`s. The test's `Err(_)` branch ("a refusal touches no one else") is therefore never reached in a green build. The positive control asked for (break the validation call alone, see the test fail) **does not fail**. **Fix shape:** add the input above as a test and as a generator case (fresh intake + reused roster id). Separately (R2-2), make `receive` refuse it. | RAN (mutation table §6; qa_r2 3 runs identical) |
| R2-2 | Minor | `src/intake.rs:426-431` (check 10) | Same sequence as R2-1. A proposal whose `proposal_id` is already carried by an entry of the current roster reaches the human's card, can never be approved, and costs the proposer one quota unit when the approval is refused. Cheap fix: check 10 also refuses ids present in `roster.signed().body.members[*].proposal`. Related note for the daemon lane: the intake has no persistence, so a restart also forgets mutes and quotas (a muted hostile guest is unmuted by a restart). | RAN |
| R2-3 | Minor | `src/intake.rs:449-457` (`pending` discards `tick`'s list), `:296`, `:275`, `:279` | **F5 class not fully closed.** A at t0 (pending); B at t0+5 min; the starter approves B at t0+10 min. The `tick` inside `approve` expires A and throws away the list of what it ended. `made_stale` = [] and a later `tick` = [], so A's expiry is never reported. The same happens when any `receive` (even junk bytes from any guest) or `decline` arrives after a TTL. The daemon learns about A only by polling `outcome`. Its effect is the same as round-1 F5: the proposer waits for its own TTL. Fix shape: return the internal tick's list, or keep an "ended, not yet reported" list that `tick` drains. | RAN (`r2_f5_expiry_swallowed_by_an_internal_tick`) |
| R2-4 | Minor | `src/intake.rs:406-416`, `:148-159`, `:6`; `docs/ROSTER.md:160-165` | **The crowded-out counter (F3).** (a) It is incremented before the quota and mute checks, so a muted, quota-exhausted hostile guest still moves its own counter: RAN, 5 refusals → 5. Any guest can make its own counter look like an honest crowded-out member's, so the counter tells the starter that slots were full, not who is honest. (b) It is not in `accounting()`. The module doc ("nothing is stored"), the `IntakeAccounting` doc ("everything it stores") and docs §2.5 ("nothing NEW is stored"; "every refusal asserts the intake's accounting is unchanged") are now false for `SessionPendingFull`, and every "a refusal stores nothing" test is blind to the counter (RAN: accounting identical while the counter moved). (c) Unguarded: N17 (counters kept after demotion to observer) and N18 (counted on `ProposerHasPending` too) survive the branch's suite. What holds: no guest can move another's counter (the sender is channel-authenticated; a forged `proposer` → `ProposerNotSender`, not counted); an invalid proposal is not counted (checks 1-8 come first); at most one `u32` per current guest, saturating; no proposal content stored; pruned on `tick` when the key stops being a guest (the counter has no time bound and the docs claim none). | RAN (`r2_f3_counter_who_can_move_it`) |
| R2-5 | Minor | `src/intake.rs:274-277`; `tests/gate_return_a3.rs:527-536` | **F4: the string bound is applied before decoding, but nothing tests it.** The only test sends 4,098 `'0'`s. With the string check removed (N20), widened (N22) or set to `>=` (N21), that input still ends `TooLarge` through `receive`'s own byte check, so all three survive. Impact is low, since a channel frame is at most 65,535 bytes anyway. My test (4,097 characters, odd, must be `TooLarge`; 4,096 characters must be `Malformed`) kills all three. Encoding itself is sound: lowercase hex only. Upper case in any single letter, a leading or trailing space, a newline, `0x`, empty, non-ASCII, odd length and trailing bytes are each refused (48 spellings, RAN, accounting unchanged). The mapping is one-to-one, so no two accepted strings decode to the same bytes (REASONED), and canonical decoding refuses any re-encoding of the bytes. | RAN |
| R2-6 | Minor | `docs/ROSTER.md:248`, `:260`; test name `proposal.rs::item4_removed_candidate_cannot_come_back_through_a_proposal` | **F6 docs are still partly over-claimed.** Line 242 is now exact. But line 248 says re-proposing "the same person under a fresh key" is "**Closed** by the inheritance rule of 06 §5.2 (c)". That rule is not built, and round 1 showed a returning signing key lands in another slot. The builder's own new design question asks whether the rule should follow the signing key at all. Line 260 says "a member cannot propose a removed key"; true only for the same key id. The removed device's signing key with a new Noise key is accepted (RAN again, `r2_f2_candidate_variants`; gate `qa_dq3_*`). Should read "the same key id". | RAN (grep) / REASONED |
| R2-7 | Note (merge order) | m3-audit `crates/coagent-audit/tests/a3_unknowns.rs:125` (audit's own test, not this branch) | In the scratch merge of `origin/m3-audit` 4bc3d36 + m3-roster, 235 passed and **1 failed**: `u6_a_valid_roster_version_near_the_encoding_cap` panics with "the roster chain accepts the version: LifetimeExceeded". Its history removes and re-adds members many times, passing m3-roster's new 32-entry lifetime bound; its comment considers only the 256-version bound. Control: the same test on UNMERGED 4bc3d36 passes (RAN). Not a defect of m3-roster (the bound was ordered), but whichever branch merges second must adapt that test: the audit seat's job. | RAN |
| R2-8 | Note | `docs/ROSTER.md:204-205` | The starvation figures reproduce exactly: 0, 0, 80, 100, 130 min for 1 to 5 hostile guests (RAN, gate test). "Bound: ceil(8·h/3)·TTL" is an upper bound (110 and 140 for h = 4 and 5, against 100 and 130 measured), and it applies only for h ≥ 3 (for h ≤ 2 the measured time is 0). Say so. | RAN / REASONED |
| R2-9 | Note | `src/intake.rs:266-283` | `receive_wire` runs `tick` on its own `TooLarge` / `Malformed` refusals (consistent with F9), but nothing guards this (N25, N38). Its `check_roster` (N39) is untested at that level: without it, a caller passing another session's roster would stale every pending proposal on a malformed string. These are caller-error paths; record only. | RAN |
| R2-10 | Note | gate file, 5 lines | The ruled edit's marker names the coordinator seat ("Friday") five times in a committed file. It is prescribed by addendum 4, and it is a seat name, not a person. F8 scan otherwise clean (§2). | RAN |

No Blocker. One Major.

## 2. Measured totals (all RAN; `/Volumes/Laptop-DEV` checked mounted after every run)

| What | Result |
|---|---|
| `git rev-parse HEAD` | `d88d5d78efa2…` (matches the brief) |
| `scripts/check.sh` ×5 | **5/5 exit 0** (`CHECK OK`); each run 341 workspace tests passed, 0 failed (round 1: 301) |
| `coagent-roster` tests | **109 passed, 0 failed** (matches STATUS) |
| `scripts/red-controls-roster.sh` | exit 0, **45 rows, 45 RED, 0 NOT-RED**; release build refused; unknown name refused; green 109. Every row's log has exactly one failing test and one panic, and the panic text is the named property. All 14 new rows were read, e.g. `approve_no_validate` → "an approval produced a body the validator refused … (cap 4, guests 2, plain, sign_twin)" (a sign twin got through only because the widened control also switches off `receive`, see R2-1); `crowded_unreported` → "an honest proposer crowded out was not counted"; `decode_no_size_check` → "a proposal over 2,048 bytes was parsed before the size check". |
| `scripts/red-controls-core.sh` | exit 0, **65 rows, 0 NOT-RED**; `roster_no_cap` RED on `test7_ninth_member_is_refused`; green 189 |
| gate file `qa_gate.rs` | **22/22 pass** (check.sh ×5 and once with output) |
| my QA tests `qa_r2.rs` (12) | 3 runs: 12/12 pass, identical. They are written to the CURRENT behaviour and record facts. R2-1 to R2-5 are shown by mutants these tests kill and the branch's tests do not. |
| protected files | `tests/gate_roster.rs`, `tests/gate_return.rs`, `tests/roster.rs`, `scripts/red-controls-core.sh`, root `Cargo.toml`, `Cargo.lock`, crate `Cargo.toml`, `docs/CRYPTO-GLUE.md`: blob ids identical to main, diff 0 bytes. Positive control: `src/intake.rs` diff 28,317 bytes. |
| gate file vs reference | reference sha256 `864b352b…a6c`; commit `7fea47b` added it byte-identical (sha256 of `git show` equal); `ecbd848` is its only other commit; now `f9cd325e…09c`. `diff` against the reference shows **only** the one ruled test (§3). |
| F8 scan | Every file changed vs main (21) was scanned for owner name, user names, card ids, absolute or user paths, mail domains, other clients and coordinator names. HEAD: 0 real hits; 2 false positives (`$COAGENT_TOOLS/tmp/…`, a relative path); the "Friday" markers (R2-10); "Priya" is the design files' placeholder name (in 04/06, not a person). Positive control: the same pattern on the same files at 0a47fc9 gives 13 hits. |
| public API since 0a47fc9 | added only (`Approval`, `approve_with_report`, `receive_wire`, `crowded_out[_counts]`, `to_wire`, `Outcome::RefusedInvalid`, four `IntakeError` variants). Neither in-flight crate uses `Outcome`, `IntakeError` or the intake (grep RAN on both heads), so the new enum variants break nothing. Every item they use (`Applied`, `ForkEvidence`, `RosterChain`, `RosterError`, `SignedRoster`, `ValidRoster`, `body_hash`, `sign`, `Member::new`, `Removed`, `RosterBody`, `Role`, `CAP`, `admit`) is unchanged in shape (diff RAN; `api_stability.rs` unchanged since 0a47fc9). |
| mutations | 61 round-1 (60 applied, M49's code no longer exists) + 39 new = **100**: **80 killed, 19 survived, 1 not applicable**. Table §6. |

## 3. Ruling on the gate-file edit and on the coordinator's ruling

- **The edit has teeth, and nothing else in the file changed.** (a) If the twin is accepted at `receive`, `assert_eq!(rx, Err(CandidateSignKeyInUse))` fails; under the red control it goes RED on exactly that sentence (RAN). (b) If Q's proposal is staled or Q is charged at that point, the `outcome` and `used_by` asserts fail. (c) If the later honest approval built a refused body, `approve` now returns `Err` and `.unwrap()` panics. If `approve` ever stopped validating, the original final `apply(...).is_ok()` assertion still catches it. Every changed line carries `// RULING (Friday, 2026-11-17, addendum 4)` with the old line quoted. Setup and `println!`s are kept. The diff against the reference is that one test only. Cosmetic: the kept `println!` still says "after approving the twin".
- **What the edit lost.** The gate file no longer exercises "a refused approval leaves the others untouched". That half moved to the builder's own `f2_candidate_*` tests, which reach it only under a red control. Combined with R2-1, no green-build test covers that half at all.
- **The coordinator's ruling was sound.** The test as written could pass only if the property were broken, because it demanded that `receive` accept the twin. Rewriting it in place was right. A slightly better form would have kept both branches in the gate file (refused at `receive`: assert the variant; accepted: `approve` must return `InvalidApproval` and leave Q untouched), as the builder's own `f2_*` test does. The gap that matters is R2-1, not the edit.
- **The wrapper** (`tests/qa_gate.rs`: `#[rustfmt::skip]`, `#[path]`) is acceptable. **The five allowed lints** (`unused_imports`, `clippy::int_plus_one`, `clippy::err_expect`, `clippy::needless_range_loop`, `clippy::explicit_counter_loop`) are all style lints scoped to that module; none can hide a failing assertion. **The two re-export files** (`pub use crate::common::*;`) are acceptable. They give the gate file the crate's `tests/common` and `tests/prop_common`, which are unchanged since 0a47fc9, so the gate's helpers mean what they meant in round 1.

## 4. Round-1 findings

| id | status |
|---|---|
| F1 (Major) | **closed.** Every promotion and demotion sequence of proposed, lowered-proposed and directly invited members is accepted by a holder and by a joiner given each version first (11 versions, RAN). A raise on the admitting version is refused, alone and combined with a limit raise plus another member's promotion, by holder and joiner, chain unchanged. Remove and re-add with the OLD record: added_in 5 → `BadProposalVersion`, added_in 3 → `ReaddWithoutNewEntry`. A NEW proposal for the removed key: `ProposedRemovedKey` (validator) and `CandidateRemoved` (intake). A direct re-add as guest is accepted with no proposer; that is the starter's act, and none of these counts as an "admission" through a proposal. Joiner limit: a joiner given v4 built on a version every holder refused (C admitted above its proposed role) accepts it. That is exactly what docs §2.4 states ("it trusts the chain it was given"), so the docs are truthful. A hostile starter can always reach "proposed observer is now a guest" in two versions; holders see it as `role_changed: [C]`, later joiners cannot tell. This follows from the ruling (promotion is a starter right) and is not a hole. Mutants N27-N30 all killed. |
| F2 (Major) | **behaviour fixed; guard not effective → R2-1 (Major).** No input found on which `approve` returns `Ok` with a body that a fresh chain (holder or joiner) refuses. Inputs tried (RAN): members' Noise key, signing key, both keys; the removed member's key id and its signing key; another PENDING candidate (whole, and its signing key); the proposer; the starter; the starter's Noise key and signing key; `added_at` empty, 64 bytes of 4-byte characters, 65 (`FieldLimit`, proposal stays pending); role combinations (`RoleRaised`, pending); cap filled by a direct invite (`NotPending(Stale)`, then `NoFreeSeat`); lifetime 31 → approval to 32 valid, 32 → `LifetimeFull`; version 255 → 256 valid, 256 → `VersionBound`; another session's roster (`WrongRoster`, nothing changed); time backwards 900 s (valid). The `added_at` content has no rule other than length, and the canonical encoder round-trips any string ≤ 64 bytes (REASONED from `canonical.rs`). State-then-error: only the documented `RefusedInvalid` of the one proposal, plus `tick` effects (R2-3). |
| F3 | **changed → R2-4 (Minor).** Bounded, visible, no content stored, cannot be moved by another guest; measured bound unchanged (R2-8). It can be moved by its own guest even when muted or out of quota; it is outside `accounting()`; two mutants survive. |
| F4 | **closed in substance; R2-5 (Minor, test gap).** |
| F5 | **closed for approvals** (`made_stale` complete: empty when nothing is pending; nothing on a refused approval; declined and already-expired proposals not listed; N12 and N13 killed). **New gap R2-3** for expiries swallowed by internal ticks. |
| F6 | **partly closed → R2-6 (Minor).** |
| F7 | **closed.** M11, M42, M48, M52, M56, M57, M58, M60, re-applied to the moved code: **all 8 killed**, each by its new guard. |
| F8 | **closed** (scan §2; R2-10 note). |
| F9 | **closed as documented**, contradicted only by the counter (R2-4b). |
| F10 | **closed** (docs §2.4 row states the per-version rule; true, gate `qa_joiner_*` RAN). |
| F11 | **closed** (docs §7 and the `is_roster_signer` comment name both places; `f11_*` passes; mutant M24 killed). |
| F12 | not this branch: the daemon's 28 process tests were not run here (a separate gate runs them). |

## 5. Caused-by / charged-to: new or changed state

| Stored or counted thing | Caused by | Charged to | Bound | Can it stop someone else acting? |
|---|---|---|---|---|
| crowded-out counter | the guest whose valid proposal hit full session slots, including itself when muted or out of quota | that guest's own counter | 1 `u32` per current guest (≤ 7), saturating, pruned on `tick` | No. But a guest can inflate its own counter, so the counter cannot single out the honest guest (R2-4). |
| `RefusedInvalid` record | the proposer whose approval the validator refused (reachable: R2-1 / R2-2) | that proposer (one quota unit, one remembered id) | inside the existing 8-per-proposer quota and 248 ids | No, as the code stands (RAN). If the refused path regressed (N05, N06) it would stale and charge everyone, and no branch test would notice (R2-1). |
| `made_stale` list | the starter's approval | nobody (returned, not stored) | ≤ 2 (3 pending − 1) | No |
| swallowed expiry reports | any caller of `receive`, `approve` or `decline`, including any guest sending junk | proposers whose expiry goes unreported | — | Not blocking: their own TTL ends it (R2-3) |
| wire string | a guest | the starter's daemon (one buffer) | 4,096 characters before decoding (RAN by behaviour; unguarded, R2-5) | No |
| session pending slots (unchanged) | colluding guests | shared | 3 | yes, bounded: 80/100/130 min for 3/4/5 hostile guests, starter idle; ended by one decline-and-mute each (RAN) |

## 6. Mutation table (100 mutants; driver `mutate_r2.py`; "branch suite" = all 14 test targets plus lib tests of the crate, including `qa_gate.rs` and `gate_return_a3.rs`; "qa_r2" = re-run of survivors against my round-2 tests only, for information)

`*` marks a round-1 mutant whose text was adapted because the head moved the code.

| id | mutation | branch suite | qa_r2 |
|---|---|---|---|
| M01 | cap above max | killed | — |
| M02 | cap 2 accepted | killed | — |
| M03 | count rule removed | killed | — |
| M04 | count limit +1 | killed | — |
| M05 | slot >= → > | killed | — |
| M06 | version bound +1 | killed | — |
| M07 | entries bound +1 | killed | — |
| M08 | entries bound −1 | killed | — |
| M09 | proposer = candidate allowed | killed | — |
| M10 | proposer = starter allowed | killed | — |
| M11* | at_version 0 allowed | killed (`f7_m11_…`) | — |
| M12* | shape at_version+1 = added_in removed | killed | — |
| M13* | role upgrade allowed (now `check_admission_role`) | killed | — |
| M14 | I-6 <= → < | killed | — |
| M15 | duplicate id allowed | killed | — |
| M16 | unchecked not reported | killed | — |
| M17 | first-roster signature error ignored | killed | — |
| M18 | unchecked report dropped next version | killed | — |
| M19 | cap change never reported | killed | — |
| M20 | cap change from/to swapped | killed | — |
| M21 | observer proposer allowed (transition) | killed | — |
| M22 | transition at_hash unchecked | killed | — |
| **M23** | transition at_version unchecked | SURVIVED | survived. **Equivalent** (round-1 reasoning unchanged: the shape rule forces at_version = added_in − 1 and the transition forces added_in = held + 1) |
| M24 | `is_roster_signer` always true | killed | — |
| M25 | helper `CapUnchanged` removed | killed | — |
| M26 | helper skips `validate_body` | killed | — |
| M27 | admit: observer may propose | killed | — |
| M28 | admit: anyone sends result | killed | — |
| M29 | silent drop (control) | killed | — |
| M30 | transition proposal rules skipped | killed | — |
| M31 | free seat >= → > | killed | — |
| M32* | intake lifetime off by one | killed | — |
| M33 | per-proposer pending off by one | killed | — |
| M34 | session pending off by one | killed | — |
| M35 | quota off by one | killed | — |
| M36 | expiry >= → > | killed | — |
| **M37** | `tick` staleness ignores hash | SURVIVED | survived. **Equivalent** for a caller passing its own chain's versions (as round 1) |
| M38 | approve: role raise allowed | killed | — |
| M39* | approve: others stay pending | killed | — |
| M40 | intake session check removed | killed | — |
| M41 | intake: starter may propose | killed | — |
| M42* | intake check 4 ignores hash | killed (`f7_m42_…`) | — |
| M43 | candidate key id unchecked | killed | — |
| M44 | member candidate allowed | killed | — |
| M45 | removed candidate allowed | killed | — |
| **M46** | `IdsFull` removed | SURVIVED | survived. **Equivalent** (31 × 8 arithmetic) |
| M47 | `may_approve` always true | killed | — |
| M48* | approve: `added_at` unchecked | killed (`f2_an_overlong_added_at_…`) | — |
| M49 | approve lifetime re-check removed | n/a: code removed and replaced by the validator run (N01-N03) | — |
| M50 | mute not recorded | killed | — |
| M51 | quota not charged | killed | — |
| M52 | receive: roster/approver check removed | killed (`f7_m52_…`) | — |
| M53 | label changed consistently | killed | — |
| M54 | label separator dropped | killed | — |
| M55 | label dropped | killed | — |
| M56* | `decode` 2,048 check removed | killed (`f7_m56_…`) | — |
| M57* | `propose()`: observer allowed | killed (`f7_m57_…`) | — |
| M58 | `propose()`: removed candidate allowed | killed (`f7_m58_…`) | — |
| M59 | `verify()`: WrongProposer removed | killed | — |
| M60* | `propose()`: starter allowed | killed (`f7_m60_…`) | — |
| M61 | `Member::proposed` records entry role | killed | — |
| **N01** | approve: validator run removed (receive intact) | **SURVIVED** | killed. **Real, unguarded: R2-1** |
| **N02** | approve: transition rules not run | SURVIVED | survived. **Equivalent in practice**: every transition rule an approval body could break (added_in, proposer guest, at_version/hash, signature, role) is enforced earlier by `receive`/`approve`'s own checks (REASONED); a second line only |
| **N03** | approve: `validate_body` not run | **SURVIVED** | killed. **Real: R2-1** |
| **N04** | refused approval leaves proposal pending | **SURVIVED** | killed. **Real: R2-1** |
| **N05** | refused approval stales every other proposal | **SURVIVED** | killed. **Real: R2-1** (the round-1 F2 harm) |
| **N06** | refused approval charges every proposer | **SURVIVED** | killed. **Real: R2-1** |
| N07 | receive: signing-key compare removed | killed | — |
| N08 | receive: Noise-key compare removed | killed | — |
| N09 | signing key compared with wrong field | killed | — |
| N10 | version bound >= → > | killed | — |
| N11 | version bound removed | killed | — |
| N12 | made_stale never filled | killed | — |
| N13 | made_stale wrong proposer | killed | — |
| N14 | crowded counter not incremented | killed | — |
| N15 | crowded counter +2 | killed | — |
| N16 | crowded counters never pruned | killed | — |
| **N17** | crowded counters kept for observers | SURVIVED | killed. **Real: R2-4** |
| **N18** | crowded counted on ProposerHasPending | SURVIVED | survived. **Real, unguarded: R2-4** |
| N19 | `crowded_out` always 0 | killed | — |
| **N20** | receive_wire: string bound removed | SURVIVED | killed. **Real: R2-5** |
| **N21** | receive_wire: > → >= | SURVIVED | killed. **Real: R2-5** |
| **N22** | receive_wire: bound doubled | SURVIVED | killed. **Real: R2-5** |
| N23 | wire: upper case accepted | killed | — |
| N24 | wire: odd length accepted | killed | — |
| **N25** | receive_wire: no tick on TooLarge | SURVIVED | survived. Real but trivial (R2-9) |
| N26 | to_wire upper case | killed | — |
| N27 | transition: admission rule skipped | killed | — |
| N28 | first roster: admission rule skipped | killed | — |
| N29 | first roster: admission rule on every entry (F1 back) | killed | — |
| N30 | first roster: admission rule on wrong version | killed | — |
| N31 | approve: version +2 | killed | — |
| N32 | approve: wrong prev_hash | killed | — |
| **N33** | refused approval recorded as Declined | **SURVIVED** | killed. **Real: R2-1** |
| N34 | approve: added_at bound +1 | killed | — |
| N35 | approve: last free slot | killed | — |
| **N36** | crowded prune: convener term dropped | SURVIVED | survived. **Equivalent**: the starter can never be counted (check 3 refuses it before check 9) |
| N37 | version-zero rule on wrong value | killed | — |
| **N38** | receive_wire: no tick on Malformed | SURVIVED | survived. Real but trivial (R2-9) |
| **N39** | receive_wire: roster check removed | SURVIVED | survived. Real, caller-error path (R2-9) |

Round-1 set: 57 killed, 3 survived (all three the equivalents already accepted in round 1), 1 n/a. New set: 23 killed, 16 survived, of which 2 are equivalent (N02, N36) and 14 are real unguarded checks; 6 of those 14 make up R2-1. Every mutant applied and compiled.

## 7. Merge and compile results (scratch only; merge commits never pushed)

| Tree | Merge | `cargo check --locked --workspace --all-targets` | tests run |
|---|---|---|---|
| `origin/main` 18005d6 + m3-roster | **fast-forward** to d88d5d7 | (in check.sh) | `scripts/check.sh` **exit 0**, 341 passed, 0 failed |
| `origin/m1-daemon` **d8b5b4b** (newer than round 1's bb92225) + m3-roster | conflict in `BACKLOG.md` only (both appended), resolved keeping both; merge commit 3ef3bf4 | **exit 0** (only the pre-existing `unused workspace dependency rand_core` warning) | `coagent-roster` 109/0; `coagent-daemon --lib` 17/0. The daemon's process tests were left to the other gate, as briefed. |
| `origin/m3-audit` **4bc3d36** (newer than round 1's 882e094) + m3-roster | conflict in `BACKLOG.md` only; `Cargo.lock` auto-merged; merge commit cfbbd6c | **exit 0** (same pre-existing warning) | `coagent-roster` + `coagent-audit`: **235 passed, 1 failed** (`a3_unknowns::u6_…`, `LifetimeExceeded`). Control on unmerged 4bc3d36: passes. → R2-7 |

## 8. For the owner, in plain words

1. The member list still cannot be forged: only you can sign it, and nobody can claim a member proposed someone they did not.
2. Someone added through a proposal as an observer can now be made a guest later; the round-1 problem is fixed.
3. Your approval screen can no longer be tricked into adding nobody and cancelling everyone else's requests. The program now checks every approval before acting on it.
4. Not yet trustworthy: if someone later breaks that check by accident, no test would notice, and there is a real way to trigger it. One more test is needed before this is accepted.
5. You can now see that a member's requests were refused because the queue was full. The count does not tell you which member is being honest, and a few small reports (expired requests) can still go missing.

## 9. What I could not do

- The daemon's process-level tests on the merged tree (left to the separate gate, as briefed; socket-path limit).
- Mutation and red-control runs overlapped on a busy machine. Each result line records that the drive was mounted. No build or test failed with a missing path or a network error.

## 10. Artefacts

`gate_roster_tests_m3_r2/`: `qa_r2.rs` (12 tests; drop into `crates/coagent-roster/tests/`; uses the crate's `common` and `prop_common`), `qa_r2_results.txt`, `mutate_r2.py` (driver), `mutation_results.tsv`, `precheck.py`, `check5.sh`, `runners.sh`, `merges.sh`.
