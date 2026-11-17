VERDICT: GO WITH NOTES — head 44662d58bc7f91f3d4dbece95abeb32da9b88f4a

---
date: 2026-11-17
type: reference (QA gate verdict, tier 1, round 3 of 3, short third check, findings only)
project: General / CoAgent (no client)
subject: branch m3-roster, crate coagent-roster, delta d88d5d7..44662d5
base: local main 18005d6; remote main 454bfb5 (relay-identity merged since)
---

# Gate M3-ROSTER round 3: verdict

**BLUF.** The one thing that blocked the last check is fixed. A proposal that reuses a request number already on the member list is now refused when it arrives, before the owner sees a card. Removing the deeper safety check behind it now makes the project's red-control run fail. I could not reach that deeper check in a normal build with any input, order or restart, so the coordinator's ruling about it is sound. The three edits to the second gate's test file are confined, marked and at least as strict as what was ordered. One Minor test gap remains: nothing in the branch's own tests would notice if a request cancelled by an approval were also reported a second time later. I confirmed that this does not happen, and my test covers it.

Head confirmed by `git rev-parse HEAD` on a fresh clone of `m3-roster`: `44662d58bc7f91f3d4dbece95abeb32da9b88f4a` (TESTED). All work in scratch clones under the session scratchpad; nothing committed to or pushed from the project; merge commits only in a throwaway clone.

## 1. Findings

| id | severity | what | input | exact output | file:line |
|---|---|---|---|---|---|
| R3-1 | **Minor** (test gap; code correct) | "Proposals an approval made stale are reported by that approval (`made_stale`), never by `tick`" (docs) is unguarded by the branch's suite. Mutant X06 (an approval's staled proposals are also marked unreported, so the next `tick` reports them a second time) survives all 16 test targets plus lib tests, both gate files included. | a, b, c pending; `approve_with_report(c)` → `made_stale` = [a, b]; sign; `tick(v3)` | Under X06, branch suite: `SURVIVED` (driver), and re-run a second way: `gate_return_a5` 10 passed, `gate_return_a3` 19 passed, `qa_r2` 12 passed, `intake` 18 passed. My `r3_r2_3_…` panics: `R3 R2-3: a proposal made stale by an approval was reported again by tick: [(ProposalId(0101…), Stale), (ProposalId(0202…), Stale)]`. Unmutated: green ×3 (TESTED). | `src/intake.rs:637` (stale branch of `approve_with_report`); `docs/ROSTER.md:220` |
| R3-2 | Note | Docs over-state an assertion: "refused approvals are exactly 0 in the normal build and 12 with the receive id check off (both asserted)". The 0 is asserted (`assert_eq!(…, 0)`); the 12 is only asserted `> 0`. | read `gate_return_a3.rs:428-442` | the runner prints `12 refused approvals` (TESTED) | `docs/ROSTER.md:207` |
| R3-3 | Note | `IntakeAccounting` doc: "A refusal changes none of it (the ends that refusal's own expiry pass makes aside …), except … ONE bounded crowded-out counter". A refusal also DROPS counters: the same pass prunes counters of keys that stopped being guests. | v6 counted once; v6 demoted to observer; junk `receive` from v1 against the new version | `Err(Malformed)`; accounting before `crowded_guests: 1, crowded_refusals: 1`, after `crowded_guests: 0, crowded_refusals: 0` (TESTED, `qa_r3_note.rs`). The behaviour is right and documented in §2.5 ("dropped at the next call"); only the doc sentence's "except" list is incomplete. | `src/intake.rs:161` |
| R3-4 | Note | Gate file `qa_r2.rs` keeps two comments that now describe the old behaviour ("the muted, quota-exhausted H1 still has its counter moved…", "`accounting()` … does not see the counter"), and the test name `r2_f2_…_reaches_a_card` now asserts the opposite. The ruling allowed only assertion changes, so leaving them was correct; the seat flagged them. Cosmetic. | read | — | `tests/qa_r2_m3/qa_r2.rs:400`, `:410` |
| R3-5 | Note (process) | The second line of defence (the validator run in `approve`) is guarded only by `scripts/red-controls-roster.sh` (its must-stay-green row `intake_roster_id_unchecked` on `a5_r2_1_…` and on the property test), not by `scripts/check.sh`. If the run were deleted, `check.sh` would still exit 0; only the roster runner would fail. Under the ruling there is no other way. The merge procedure should run the roster runner. | N01/N03 to N06/N33, normal build | branch suite `SURVIVED`; receive-id-check-off build `KILLED` by `a5_r2_1_…` and `f2_property_…` (TESTED) | `scripts/red-controls-roster.sh` EQUIV rows |
| R3-6 | Note (merge order; carried from R2-7) | Unchanged. In the merge with the audit branch's newer head `52d12e9`, the audit test still fails on this branch's 32-entry lifetime bound. It is the audit seat's job to adapt it (already recorded in REQUESTS). | throwaway merge 454bfb5 + 44662d5 + 52d12e9 | `roster+audit passed 292 failed 1`; `u6_a_valid_roster_version_near_the_encoding_cap` panics "the roster chain accepts the version: LifetimeExceeded" (TESTED) | `crates/coagent-audit/tests/a3_unknowns.rs:248` (audit branch) |
| R3-7 | Note (merge) | Remote `main` moved to `454bfb5` (relay-identity) after this branch's base, so the merge is no longer a fast-forward. Merging 44662d5 into 454bfb5 conflicts in `BACKLOG.md` only. The merged tree passes `cargo check --workspace --all-targets` (exit 0) and `cargo test --workspace --exclude coagent-daemon` (434 passed, 0 failed) (TESTED). Main's changes since 18005d6 touch no roster file and none of the protected files (blob ids equal, TESTED). | — | — | — |

No Blocker. No Major. One Minor.

## 2. R2-1 (the Major) and addendum 6 §3

**Is it closed?** Yes, in the only form the code now allows.
- Removing the validator run (N01), `validate_body` (N03), the refused-approval bookkeeping (N04, N33), or bringing back the round-1 harm (N05 stales everyone, N06 charges everyone): every one of these survives the branch's normal-build suite, and **every one is KILLED** in the build with the `receive` id check switched off, by `a5_r2_1_…` and `f2_property_…`. The baseline failures of that build are discounted (`a5_r2_2_…`, which is that control's own red row, and my two R2-2 tests) (TESTED, `mutation_results.tsv`). In the project's runner these are the must-stay-green rows: `intake_roster_id_unchecked GREEN a5_r2_1_… (second line holds)` and `… f2_property_… (second line holds; refused approvals > 0)` (TESTED). If the validator run is deleted, those rows go NOT-GREEN and the runner exits 1 (REASONED from the runner code and the N01 result).
- N02 (transition rules not run): survives in both builds. **Equivalent.** The only refusal any reachable input produces is `DuplicateProposalId`, which is a single-version rule. Every transition rule an approval body could break (added_in, proposer a guest of the held version, at_version and at_hash, proposal signature, admission role) is enforced earlier by `receive` checks 3 to 5 or by staleness and approve's role check (READ `lib.rs` `check_transition`/`check_added_proposal`).

**Is the validator run really unreachable in a normal build?** I found no input that reaches it.
- READ: I took every rule of `validate_body`, `check_proposal_shape` and `check_transition` that a new proposed entry can break, and matched each to a check that comes first. Key and key-id duplicates (check 7), binding (check 6), slot, cap and lifetime (check 8 plus approve's free-slot search), version bound (check 8), `added_at` length (approve), proposer ≠ candidate (the candidate is not a member), proposer ≠ starter (check 3), at_version/at_hash (check 4, and staleness on every later call), the removed-key rule (check 7), role (approve's `RoleRaised`), duplicate proposal id (check 10, now including roster entries). `rebuilt_proposal` rebuilds exactly the fields the proposer signed, so the signature re-check cannot diverge.
- TESTED, `qa_r3.rs::r3_a6_validator_run_unreached_by_random_sequences`: 600 seeded sequences, 54,000 steps. Steps cover receives from any key (guests, observer, starter, outsiders, a wrong sender), candidates from members, outsiders, removed keys and four key twins, ids from a set of 10 (so ids carried by entries come back), the current or the previous version, plain and wire, approvals with any role and `added_at` of 60 to 66 bytes, declines and decline-and-mutes, time jumps up to 2×TTL, the starter's own invites, removals, role flips and limit raises, and 948 restarts (a fresh intake). Result: **657 approvals, `InvalidApproval` 0, `IdCarriedByRoster` 143**, and every approved body accepted by a chain holder; 3 runs identical. **Positive control:** the same test with the receive id check switched off reports `InvalidApproval 24, first invalid: seed 2: DuplicateProposalId(…)` and goes red, so the search does reach the run when the input exists. It also never found any other refusal reason.
- The same test checks two more properties on every step. Every Expired or Stale end is reported exactly once per intake (by `tick` or by `made_stale`), checked at each restart and at the end. A `SessionPendingFull` moves the sender's counter by exactly 1 if it is unmuted with quota left, and by 0 otherwise. Both held throughout.

**Is the composed row honest?** Yes. `intake_roster_id_unchecked+approve_no_validate` sets both `cfg` values (build.rs splits on `+` and refuses any unknown part). `a5_r2_1_…` takes its second-line branch, and `approve` returns `Ok`. The row is RED on "an approval produced a body the validator refused (a reused roster proposal id)" (TESTED). It is an extra row; the two single controls keep their own rows (TESTED: 58 rows all RED, 4 must-stay-green rows all GREEN).

**Are both counts asserted, and what are they?** Normal build: `assert_eq!(refused_approvals, 0)`, printed `396 cases, 84 approvals, 0 refused approvals, 18 reused-roster-id cases (12 refused as IdCarriedByRoster)`. Receive id check off: `assert!(refused_approvals > 0)`, printed `396 cases, 84 approvals, 12 refused approvals, 18 reused-roster-id cases (0 refused as IdCarriedByRoster)` (TESTED, runner log). The docs' "12 … asserted" is R3-2.

**Ruling on addendum 6 §3: sound.** No test can fail on removing the validator run in a normal build, because that run is unreachable there. Asking for one would force a test-only seam into production code. The composed row, the must-stay-green rows and the two asserted counts are the honest substitute, and they do fail when the second line is broken.

## 3. The three ruled edits to `qa_r2.rs`

The gate's original has sha256 `33f07c85…ef12` (TESTED; equal to the branch's commit `4aa9781`). The branch copy now has `1cb2b0c7…1d3c` (TESTED). I checked the diff against the original by script (TESTED). It changes only these three test functions. All 7 removed lines are quoted verbatim as `// old: …`. Each of the 17 added code lines has `// RULING (Friday, 2026-11-17, addendum 6)` within the lines above it. No `println!` or setup line was removed or changed. `qa_gate_m3/qa_gate.rs` is unchanged since d88d5d7 (0 diff lines, sha256 `f9cd325e…09c`). The wrapper `tests/qa_gate.rs` changed in comments only (the false "BYTE-IDENTICAL" claim was corrected). The new wrapper `tests/qa_r2.rs` and its two re-export files mirror the accepted `qa_gate.rs` pattern.

- **`r2_f2_proposal_id_carried_by_an_existing_entry_reaches_a_card`: ACCEPTED.** It asserts `rx == Err(IntakeError::IdCarriedByRoster)` (the named variant), identical accounting, P charged 0, approve of the id returns `UnknownProposal` (no card), `outcome == None`. Q's pending state, its quota and the later valid approval are kept. The added `let id = pid(7);` is not an assertion. It is needed so the unchanged lines compile, and it changes no behaviour. The new assertions are at least as sharp as R2-2. The control `intake_roster_id_unchecked` turns it RED on "the intake refuses an id an entry carries, by its named error" (TESTED).
- **`r2_f3_counter_who_can_move_it`: ACCEPTED.** Expected values are replaced, not deleted: 5 → 0 for the muted and quota-used guest, and `[(v1,5),(v5,1)]` → `[(v5,1)]`. A new assertion requires `accounting()` to move by exactly +1 counter and +1 refusal on v5's refusal, and each value has its one-line derivation. It is sharp: X08 and X09 (accounting fields zeroed) are killed by it (TESTED). One limit: its guest is muted AND quota-used, so on its own it cannot tell which condition the code checks. The branch's `a5_r2_4_…` and my `r3_r2_4_…` cover each condition separately (X01 and X02 killed by both, TESTED). Stale comments: R3-4.
- **`r2_f5_expiry_swallowed_by_an_internal_tick`: ACCEPTED.** On both paths (approve, junk receive) it asserts that `(a, Expired)` is counted exactly once across `made_stale` plus the next tick, and that a further tick does not report `a`. It goes RED under `ended_unreported` and `ended_reported_twice` (TESTED, runner). It matches R2-3 exactly.
- **Protected files.** `tests/gate_roster.rs`, `tests/gate_return.rs`, `tests/roster.rs`, `scripts/red-controls-core.sh`, root `Cargo.toml`, `Cargo.lock`, the crate `Cargo.toml` and `docs/CRYPTO-GLUE.md` all have blob ids identical to `origin/main` 18005d6 in my clone, and also to remote main 454bfb5 (TESTED). Positive control: `src/intake.rs` diff vs main is 34,621 bytes.

## 4. R2-2, R2-3, R2-4, R2-5, R2-9 as built

Each item has one adversarial test of my own (`qa_r3.rs`). It is green on the branch three times out of three, and RED against deliberate mutations (TESTED, `mutation_results_own.tsv`):

| item | my test | what it adds beyond the branch's tests | red against |
|---|---|---|---|
| R2-2 | `r3_r2_2_roster_carried_id_refused_for_any_proposer_and_after_restart` | id 7 offered by a guest who is NOT the entry's proposer, and by the proposer for another role; after a real approval moves the chain, a restarted intake refuses both the new entry's id 30 and id 7; nothing stored, nobody charged, no record, no card; fresh id accepted | the control (`r3_r2_2` in the base list), X03 (only same proposer), X04 (wrong error) |
| R2-3 | `r3_r2_3_end_inside_a_failing_call_reported_once_and_made_stale_never_twice` | ends inside calls that themselves FAIL (approve → `RoleRaised`, approve of an unknown id, decline of an unknown id, a too-large wire string, junk); `ended_unreported` = 1 then 0; first tick = exactly `[(a, Expired)]`; made_stale never reported again | N25, X06, X07, X10, X11 |
| R2-4 | `r3_r2_4_counter_mute_and_quota_separately_accounted_and_dropped` | muted guest WITH quota left, and quota-used guest NOT muted, each separately (3 tries each): counter 0, accounting unchanged; `ProposerHasPending` not counted; honest guest: accounting = before + exactly one counter and one refusal; demotion → dropped and accounting (0,0); re-promotion starts at 0 | N17, N18, X01, X02, X08, X09 |
| R2-5 | `r3_r2_5_wire_bound_edges` | 4,097 hex and 4,097 non-hex → `TooLarge`; 4,096 hex, 4,096 non-hex, 4,095 → `Malformed`; accounting unchanged | N20, N21, N22 |
| R2-9 | `r3_r2_9_tick_on_refused_wire_and_roster_check` | refused too-large and malformed strings expire `a`, next tick reports it once; another session's roster: `WrongRoster` for an oversized, a malformed and a valid string, `a` stays Pending, accounting unchanged | N20, N22, N25, N38, N39 |

Bounds (READ): the "unreported" flag sits on a record that is already kept, so it adds no entry. One call ends at most 3 pending proposals. The counter is one saturating `u32` per current guest, at most 7 by `CAP`, and counting requires a call, which prunes first. Saturation itself is NOT TESTED (it would take 2^32 calls).

## 5. Mutant table

Driver `mutate_r3.py` (adapted from `mutate_r2.py`; `*` = re-anchored on the same check because the head moved its text). "Branch suite" = all 16 test targets plus lib tests, both gate files included, NOT `qa_r3`. "id-off" = `COAGENT_RED_ROSTER=intake_roster_id_unchecked`, targets `gate_return_a5`, `gate_return_a3`, `qa_r3`, with the baseline failures subtracted. "qa_r3" = my tests alone (second pass). Every mutant applied exactly once (count = 1), and the file was restored and compared after each (TESTED).

| id | mutation | branch suite | id-off | qa_r3 | ruling |
|---|---|---|---|---|---|
| N01 | approve: validator run removed | survived | **killed** (`a5_r2_1`, `f2_property`) | survived | equivalent in a normal build (unreachable, §2); guarded by the id-off build |
| N02 | approve: transition rules not run | survived | survived | survived | equivalent: the only reachable refusal is a single-version rule |
| N03 | approve: `validate_body` not run | survived | **killed** (same two) | survived | as N01 |
| N04 | refused approval leaves proposal pending | survived | **killed** | survived | as N01 |
| N05 | refused approval stales everyone | survived | **killed** | survived | as N01 |
| N06 | refused approval charges everyone | survived | **killed** | survived | as N01 |
| N33 | refused approval recorded as Declined | survived | **killed** | survived | as N01 |
| N17 | counters kept for observers | killed (`a5_r2_4_a_counter_is_dropped…`) | — | killed | closed |
| N18 | counted on `ProposerHasPending` | killed (`a5_r2_4_a_guest_with_its_own_pending…`, 2 `item8_…`) | — | killed | closed |
| N20 | wire bound removed | killed (`a5_r2_5`, `a5_r2_9_a_too_large…`, `qa_r2::r2_f4…`) | — | killed | closed |
| N21 | wire `>` → `>=` | killed (`a5_r2_5`, `qa_r2::r2_f4…`) | — | killed | closed |
| N22 | wire bound doubled | killed | — | killed | closed |
| N25* | no expiry pass on TooLarge | killed (`a5_r2_9_a_too_large…`) | — | killed | closed |
| N38* | no expiry pass on Malformed | killed (`a5_r2_3`, `a5_r2_9_a_malformed…`) | — | killed | closed |
| N39* | `receive_wire` roster check removed | killed (`a5_r2_9_receive_wire_refuses…`) | — | killed | closed |
| X01 | counter: mute condition dropped | killed (`a5_r2_4_a_muted…`) | — | killed | closed |
| X02 | counter: quota condition dropped | killed (`a5_r2_4_a_muted…`) | — | killed | closed |
| X03 | roster id check only for the same proposer | killed (`a5_r2_2`) | — | killed | closed |
| X04 | roster id refused as `DuplicateId` | killed (`a5_r2_1`, `a5_r2_2`, `f2_property`, +) | — | killed | closed |
| X05 | tick reports only expiries | killed (`a5_r2_3`) | — | killed | closed |
| **X06** | approval's made_stale also reported by tick | **SURVIVED** | — | killed (`r3_r2_3`, `r3_a6`) | **real, unguarded: R3-1** |
| X07 | `ended_unreported` always 0 | killed (`a5_r2_3`) | — | killed | closed |
| X08 | `crowded_refusals` always 0 | killed (`a5_r2_4`, `item8_three…`, `qa_r2::r2_f3`) | — | killed | closed |
| X09 | `crowded_guests` always 0 | killed (same three) | — | killed | closed |
| X10 | receive: no expiry pass | killed (`a5_r2_3`, `f9_…`) | — | killed | closed |
| X11 | new pending proposal marked unreported | killed (`a5_r2_3`) | — | killed | closed |

Totals: 26 mutants. Branch suite: 18 killed, 8 survived. Of the 8, 6 are killed in the id-off build (N01, N03-N06, N33), 1 is equivalent (N02) and 1 is real (X06 → R3-1). Of the round-2 gate's 14 real survivors, none remains open.

## 6. Docs sentences (as they now read; TESTED/READ against the code)

| place | now reads | verdict |
|---|---|---|
| module doc (`src/intake.rs:6-11`) | "A refusal stores no proposal and no record. A refusal for a full session (`SessionPendingFull`) of a guest that would pass the quota and mute checks stores ONE bounded counter and nothing else … Every call first ends the pending proposals that expired or went stale; those ends wait for the next `tick`, which reports each exactly once." | **true** (`r3_r2_3`, `r3_r2_4`, `r3_a6`) |
| `IntakeAccounting` (`src/intake.rs:160-164`) | "…everything it stores: proposals, ids, quotas, mutes, the crowded-out counters and the ends waiting to be reported. A refusal changes none of it (the ends that refusal's own expiry pass makes aside, gate return F9), except that a refusal for a full session … moves ONE bounded crowded-out counter" | **true except the incomplete exception list** (a refusal can also drop counters, R3-3) |
| `docs/ROSTER.md` §2.5 | "A refusal for a full session therefore stores ONE bounded counter (one `u32` per current guest, saturating, dropped at the next call once the key stops being a guest, removed or made an observer) and nothing else; the counters are part of the intake's accounting … What it does NOT tell: that the guest is honest" | **true** (`r3_r2_4`; saturation READ) |
| "Closed by the inheritance rule" (`docs/ROSTER.md:286`) | removed; now "OPEN, with the design owner. The verify-words inheritance rule of 06 §5.2 (c) is not built…" | **true** (READ) |
| "the same key id" (`docs/ROSTER.md:280`, `:298`) | "What is refused (intake check 7, and every validator, I-6): the SAME KEY ID…"; "I-6 a member cannot propose the same key id as a removed entry…" | **true** (READ `receive` check 7, `check_proposal_shape`) |
| starvation (`docs/ROSTER.md:230-232`) | "For h ≥ 3 hostile guests, ceil(8·h/3)·`PROPOSAL_TTL` is an UPPER bound (h = 3: 80 minutes, measured 80; h = 4: 110, measured 100; h = 5: 140, measured 130); for h ≤ 2 the measured time is 0." | **true** as arithmetic with TTL = 600 s (READ); the measured figures are the round-2 gate's (not re-measured) |
| "never by `tick`" (`docs/ROSTER.md:220`) | "Proposals an approval made stale are reported by that approval (`made_stale`), never by `tick`." | **true** (TESTED) but unguarded by the branch (R3-1) |
| "(both asserted)" (`docs/ROSTER.md:207`) | "…exactly 0 in the normal build and 12 with the receive id check off (both asserted)" | **over-stated** (R3-2) |

## 7. What I reproduced (all TESTED in my clone; scratch `CARGO_HOME` with `bin` linked to the project toolchain, project `rustup` read-only, own target dirs)

| what | result | seat's figure |
|---|---|---|
| `cargo fetch --locked` | `fetch_rc=0` | — |
| `scripts/check.sh` | exit 0, `CHECK OK: fmt, clippy, test, deny all passed`, **363** tests passed, 0 failed | 363, exit 0 ✔ |
| `scripts/red-controls-roster.sh` | exit 0, `rows: 58`, 58 RED, 0 NOT-RED; `equivalence rows: 4`, all GREEN; release build refused; unknown name refused; `GREEN: 131 tests ok`; `ROSTER RED CONTROLS OK` | 58 / 4 / 131 ✔ |
| property counts | normal 0 refused approvals (12 `IdCarriedByRoster` of 18); id-off 12 | 0 / 12 ✔ |
| gate files | `qa_gate.rs` and `qa_r2.rs` green inside `check.sh` | 22/22, 12/12 ✔ |
| merge 454bfb5 + 44662d5 | `BACKLOG.md` conflict only; check exit 0; workspace minus daemon 434 passed, 0 failed | — |
| + `m3-audit` 52d12e9 | check `--all-targets` exit 0 (no public item the audit crate uses broke); roster+audit 292 passed, 1 failed (R3-6) | — |
| `m1-daemon` 77642ad on main+roster | `BACKLOG.md` conflict only; check `--all-targets` exit 0; daemon lib 17/0 | — |
| name/path scan of every file changed in d88d5d7..HEAD (owner, user, host, drive paths, `/Volumes/`, `/Users/`, `/home/`, `/private/tmp`, coordinator names, card ids, mail) | **0 hits**; positive control 1 hit. The seat name appears only in the prescribed RULING markers (17 in `qa_r2_m3/qa_r2.rs`, 1 in the `tests/qa_r2.rs` wrapper comment) | ✔ |

## 8. NOT TESTED

- The daemon's process-level tests on any merged tree (only its lib tests, 17/0).
- The audit test on unmerged `52d12e9` as a control (the round-2 gate ran it on `4bc3d36`; READ).
- Starvation timings (not re-measured; round-2 figures).
- Counter saturation at `u32::MAX`.
- The core runner `scripts/red-controls-core.sh` (byte-identical to main; not re-run).
- A counter kept when a key is demoted and re-promoted with no intake call in between. That is not a defect: the intake only sees rosters handed to its calls, and at the next call the key is a guest again.

## 9. Re-run

Artefacts in `gate_roster_tests_m3_r3/`: `qa_r3.rs` (6 tests; drop into `crates/coagent-roster/tests/`), `qa_r3_note.rs` (R3-3), `mutate_r3.py` (`[OWN=1] mutate_r3.py <copy> <target> <out.tsv> [ids]`), `mutation_results.tsv`, `mutation_results_own.tsv`, `qa_r3_results.txt` (tails), `runners.sh` (the exact scripts: environment, check, red runner, mutation passes, the three merges).

```
git clone --branch m3-roster <project>/2_Project_Files <scratch>/clone   # assert HEAD 44662d5
export CARGO_HOME=<scratch>/ch RUSTUP_HOME=<project>/tools/rustup CARGO_TARGET_DIR=<scratch>/target COAGENT_TOOLS=<scratch>/tools
cargo fetch --locked --manifest-path <scratch>/clone/Cargo.toml
bash <scratch>/clone/scripts/check.sh; bash <scratch>/clone/scripts/red-controls-roster.sh
cp qa_r3.rs <scratch>/clone/crates/coagent-roster/tests/ && cargo test --locked --manifest-path <scratch>/clone/Cargo.toml -p coagent-roster --test qa_r3 -- --nocapture
COAGENT_RED_ROSTER=intake_roster_id_unchecked cargo test … --test qa_r3   # r3_a6 must go red: InvalidApproval > 0
python3 -I mutate_r3.py <scratch>/mut <scratch>/target_mut out.tsv; OWN=1 python3 -I mutate_r3.py <scratch>/mut <scratch>/target_mut own.tsv
```
