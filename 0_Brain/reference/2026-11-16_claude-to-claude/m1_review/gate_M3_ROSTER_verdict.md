VERDICT: NO GO — head 0a47fc9b16770754874a376edb27a03a432f8775

---
date: 2026-11-17
type: reference (QA gate verdict, tier 1, findings only)
project: General / CoAgent (no client)
subject: branch m3-roster, crate coagent-roster
base: main 18005d63ae1311df9649893060caf1f98510a4c1
---

# Gate M3-ROSTER — verdict

Head confirmed by `git rev-parse HEAD` on a fresh clone of `m3-roster`: `0a47fc9b16770754874a376edb27a03a432f8775` (RAN). Base `origin/main` = `18005d63ae13…` = merge-base (RAN).
Everything ran in a scratch clone; nothing pushed; no git write verb inside the project tree.

**Why NO GO.** Two Majors, both RAN, both with no test in the builder's suite:
- **F1** a member admitted through a proposal as an OBSERVER can never be promoted to guest: every version that tries, and every later first roster that carries it, is refused by every member (the coordinator's extra item; confirmed).
- **F2** the intake hands the starter an approval body that every validator then refuses, while it has already marked the proposal approved and every other pending proposal stale (charging their quotas). A hostile guest triggers it at will with a candidate that reuses the guest's own signing key. This makes the builder's DESIGN QUESTION 8 ("an approval can never build a version the validator refuses") false.

Everything else claimed in STATUS reproduced: suite green 5/5, 29/29 roster red rows red on their named property, 65/65 core rows red, gate files byte-identical, no dependency, pinned encoding confirmed independently against bytes MAIN produced. The signature construction holds up to every attack I ran.

## 1. Findings

| id | severity | file:line | exact sequence | RAN / REASONED |
|---|---|---|---|---|
| F1 | **Major** | `src/lib.rs:659-664` (rule), called for every entry with a record on EVERY version at `lib.rs:596-598` | v1 starter; v2 adds guest P; P proposes C as **observer**; v3 adds C through the proposal as observer (accepted); v4 = v3 with C's role set to guest (an act the roster otherwise allows; control: the same promotion of a DIRECTLY invited observer is accepted). `apply(v4)` → `Err(ProposedRoleRaised(C))`. A joiner given v4 as first roster → `Err(ProposedRoleRaised(C))`. So the promotion is impossible for the rest of the session, and a starter daemon that signs it produces a version nobody accepts. Mirrors (all accepted, RAN): proposed guest admitted as observer then promoted back to guest; proposed guest demoted then promoted; proposer later removed (entry kept, still attributed; the chain holder does not mark it unchecked because it checked at admission; a later joiner marks it "not checkable"). The record STAYS verifiable after a promotion: the rebuilt body takes the role from the record, not the entry (`rebuilt_proposal`, `lib.rs:188`; my test verifies the rebuilt proposal after the promotion: OK). **Ruling:** the I-7 rule ("never admitted above the proposed role") is an ADMISSION rule. It belongs in the transition for newly added entries (`check_transition` added-branch, i.e. where `n.added_in == next.version`), not in the single-version shape check. On a first roster a joiner cannot tell admission from later promotion, so it must not apply it to entries with `added_in < version`. The design text itself lists it under "rule 1, one version alone" (06 §2.4), so the builder followed the design literally: the design owner must correct §2.4 rule 1 at the same time. Guard needed: a test that admits an observer through a proposal and promotes it (mine: `qa_extra_promote_a_proposed_observer_to_guest`). Not a security hole (no one gains anything); Major because an allowed starter act is permanently lost for proposed observers, nobody noticed, and no test covers role changes of proposed entries. | RAN (`qa_gate.rs` `qa_extra_*`, 3 runs identical) |
| F2 | **Major** | `src/intake.rs:263-275` (checks 6-7 compare key ids only), `intake.rs:363-411` (`approve` mutates state, then returns a body it never validated) | Guests P, Q. Q proposes C (pending). P builds a candidate with **P's own signing key and a fresh Noise key** (valid binding, new key id) and proposes it. Intake accepts (key id is new, not a member, not removed). Starter approves P's card → `approve` returns a body, marks P's proposal Approved and **Q's Stale** (Q's quota already charged, 1 of 8). Starter signs; every validator, the starter's own included → `Err(DuplicateDeviceKey(twin))`. Second path (Minor on its own): at version 256 the intake accepts a proposal and `approve` builds version 257 → `Err(TooManyVersions)`; outcome left `Approved`. Who causes it: one guest (needs the starter's human to click Approve on a card whose key words look like any newcomer's). Who pays: every other guest with a pending proposal (stale + quota), and the starter (an approval that produced nothing). Fix shape: in `approve`, run the same `validate_body` + transition rules on the body BEFORE changing any record; refuse at intake check 6/7 a candidate whose `sign_pub` or `noise_static` equals a current member's; refuse at check 8 when `version == MAX_VERSIONS`. | RAN (`qa_intake_approval_of_a_twin_key_builds_a_refused_body_and_stales_others`, `qa_intake_approval_at_version_256_builds_a_refused_body`) |
| F3 | Minor | `src/intake.rs:296-312` (3 session slots shared by all guests), docs/ROSTER.md §3 states no time bound | Colluding guests keep the 3 session pending slots full within their own quotas; an honest guest is refused `SessionPendingFull` with no card, so the starter never learns it tried. Measured with an optimal attacker (most-quota-left first), honest guest retrying every minute, starter idle: 1-2 hostile guests: 0 min; 3: **80 min**; 4: **100 min**; 5 (the maximum with a free seat at limit 8): **130 min**. Bound = ceil(8·h/3)·TTL. The starter ends it at any time with one "decline and mute" per hostile guest (or a removal); a plain decline does not (the guest re-proposes at once). Bounded and self-limiting, so not the R3-M1 shape, but the time bound and the "honest proposer is invisible to the starter" effect are nowhere stated. | RAN (`qa_starvation_by_colluding_guests`, 3 runs identical) |
| F4 | Minor | `src/intake.rs:222` and STATUS DQ6 | The `member.propose` envelope body is a JSON value; serde_json's `Value` sorts object keys, `ProposalBody` is encoded in declaration order. A proposal taken out of an envelope value and re-serialised is NOT canonical: `receive` → `Err(Malformed)` for an honest proposal. The daemon cannot satisfy DQ6 as written ("pass the canonical encoding of its proposal value") without carrying the proposal as an opaque string or decoding it first (which defeats the 2,048-bytes-before-decoding bound). Needs a wire decision before the daemon lane. | RAN (`obs_dq6_proposal_through_a_json_value_is_not_canonical`) |
| F5 | Minor | `src/intake.rs:400-409` vs `tick` `intake.rs:187-217` | Proposals made stale by an approval are never returned by `tick` (they are no longer pending), and `approve` returns only the body. After approving A, `outcome(B) = Stale` but `tick` reports `[]`. The daemon has no list from which to send B's proposer its `stale` result; B's daemon waits until its own TTL. | RAN (`obs_approval_staled_proposals_are_not_reported_by_tick`) |
| F6 | Minor | `src/lib.rs:668-674`; docs/ROSTER.md §4 row "Propose a removed person … Refused before any card" | DQ3 confirmed: removed member R; guest P proposes R's **signing key with a new Noise key**; intake accepts; validator accepts (`Advanced{added:[new id]}`); the new entry gets the lowest free slot (2, R had 3), so the per-slot verify-attempt inheritance of `insert_with_slot` does not apply. The doc's "refused before any card" over-claims. See the DQ3 ruling in §6 for what this does and does not reset. | RAN (`qa_dq3_removed_signing_key_comes_back_through_a_proposal`) |
| F7 | Minor | mutation survivors M11, M42, M48, M52, M56, M57, M58, M60 (table §4) | Real checks with no guarding test: version-1 proposals refused (DQ4) has no test; intake check 4 with the right version and a wrong hash has no test; `approve` with `added_at` > 64 has no test (would also build a refused body); `receive`/`approve` with a roster of another session or where the local device may not approve (`WrongRoster`/`NotApprover` on receive) has no test; `SignedProposal::decode`'s own 2,048 bound has no test; the proposer-side refusals of `propose()` (observer, removed candidate, starter) have no test. | RAN |
| F8 | Minor | `crates/coagent-roster/src/lib.rs:10,59-60,446`, `intake.rs:144`, `README.md`, `docs/ROSTER.md` §1-2, `tests/limit.rs:2` | Seven committed lines name the owner ("Kam") and quote internal card ids (`general-c2c-…-1117`). The n6 rule for commits is "no user names". No absolute path, user path, or other project's name was found in added lines (scan RAN with a positive control: the same pattern finds 7 hits on head, 0 on main). | RAN |
| F9 | Note | `src/intake.rs:229-230` | `receive` runs `tick` before any check, so a REFUSED input changes the accounting when a pending proposal has passed its TTL (pending 1 → 0 on a `Malformed` input). It stores nothing new; the "a refusal stores nothing" tests pass only because none of them crosses a TTL. | RAN (`qa_intake_refusal_after_an_expiry_changes_accounting`) |
| F10 | Note | `src/lib.rs:675-678` | `DuplicateProposalId` is per version only: after the entry holding id 7 is removed, a new entry admitted through a fresh proposal with id 7 is accepted. Harmless (the signature binds candidate, version and hash; the intake refuses id replay itself), but "duplicate ids" is not a session-wide property. | RAN |
| F11 | Note | `src/lib.rs:448-465` | "Who may sign a version" is in two places, not one: `is_roster_signer` checks the `convener` field, and the cryptographic decision is `pinned.verify(...)` against the key pinned at `start`. A deputy that signs versions would need both changed. Today both say "starter", consistently. | REASONED |
| F12 | Note | merged `m1-daemon` | 28 process-level daemon tests fail in my scratch tree with "timed out waiting for: daemon IPC ready". The same 28 fail identically on the UNMERGED `origin/m1-daemon` in the same environment (control RAN, see §5): the test harness puts its Unix socket under `$COAGENT_TOOLS/tmp/…`, and my scratch path makes it 162 bytes (> 104 on macOS). Environmental, not caused by m3-roster; those 28 tests are UNKNOWN for the merge. | RAN (control) |

No Blocker. Rejected attacks (all RAN unless marked): see §7.

## 2. Measured totals

| What | Result | RAN |
|---|---|---|
| `git rev-parse HEAD` | `0a47fc9b1677…` (matches) | RAN |
| `scripts/check.sh` (fmt, clippy -D warnings, test, deny) | **5 of 5 runs exit 0**, each `CHECK OK`, 301 workspace tests passed, 0 failed per run (machine busy: run 5 times) | RAN |
| `coagent-roster` tests | **69 passed, 0 failed** (matches STATUS) | RAN |
| `scripts/red-controls-roster.sh` | exit 0, **29 rows, 29 RED, 0 NOT-RED**; release build with a roster control refused; unknown name refused; green 69 | RAN |
| each roster red row on its NAMED property | 29 logs read: each has exactly **one** panic, in the named guard, whose text is the property sentence (e.g. `count_vs_max` → "a fifth member was accepted at a limit of 4"; `approval_raises_cap` → "an approval changed the limit"; `intake_no_expiry` → "a proposal was still pending after its time"). No row went red on a second rule. | RAN |
| `scripts/red-controls-core.sh` | exit 0, **65 rows, 0 NOT-RED**; `roster_no_cap` RED on `test7_ninth_member_is_refused` (unchanged); green 149 | RAN |
| gate files `tests/gate_roster.rs`, `tests/gate_return.rs`, `tests/roster.rs`, `scripts/red-controls-core.sh` | blob ids identical to main, diff 0 bytes (positive control: `src/lib.rs` diff 30,426 bytes) | RAN |
| root `Cargo.toml`, `Cargo.lock`, crate `Cargo.toml`, `docs/CRYPTO-GLUE.md` | identical to main | RAN |
| files changed vs main | `BACKLOG.md` (10 lines added, 0 removed: append only); `crates/coagent-roster/{README.md, build.rs, src/lib.rs, src/intake.rs (new), src/proposal.rs (new), tests/admit_propose.rs, api_stability.rs, intake.rs, lifetime.rs, limit.rs, pinned_encoding.rs, prop_common/mod.rs, proposal.rs (all new)}`; `docs/ROSTER.md` (new); `scripts/red-controls-roster.sh` (new). 16 files. Nothing else. | RAN |
| `pub` lines removed from `src` | 0 (control: 81 `pub` lines added) | RAN |
| pinned encoding, independently | (a) the head's `pinned_encoding.rs` run on a MAIN checkout passes (hash `46d31987…`, bytes equal). (b) On main I generated 5 fresh identities and a 3-version chain (guest, observer, slot 7, empty `added_at`, a removal), saved secrets, encodings and hashes; on the head every version decodes, re-encodes byte-identically, hashes identically, rebuilds byte-identically from `Member::new`, and validates through `start`/`apply` and as a joiner's first roster with no unchecked proposals. | RAN |
| my QA tests (`qa_gate.rs`, 22 tests) | 3 runs: 19 pass, **3 fail = F1, F2 (twin key), F2 (version 256)**, identical each run | RAN |
| mutations | **61** written; 49 killed; **12 survived** (table §4) | RAN |
| `unsafe` in crate | none besides `#![forbid(unsafe_code)]` (lib.rs:28) | RAN |
| clock reads in `src` (`Instant::now`, `SystemTime`, `UNIX_EPOCH`, `chrono`) | none (control: `Instant::now` found in `tests/prop_common/mod.rs`) | RAN |
| hash-ordered containers in `src` | none (control: 12 `BTreeMap` hits in lib.rs) | RAN |
| new dependency | none | RAN |
| anything for a deputy | none: only three comments mention a deputy; no type, field, function or branch | RAN |

## 3. Caused-by / charged-to (step 5)

| Stored or counted thing | Caused by | Charged to | Bound | Can it stop someone else acting, and for how long |
|---|---|---|---|---|
| pending proposal (per proposer) | the proposing guest | that guest (1) | 1 | No |
| pending proposals (session) | any guests | **shared, nobody's own budget** | 3 | Yes: stops OTHER guests proposing. Bounded by the attackers' quotas: ≤ ceil(8·h/3)·10 min, measured 130 min at h = 5 (F3). Ended by the starter: one decline-and-mute per hostile guest. Honest proposer gets no card, starter not told. |
| quota used | the proposing guest | that guest | 8 per session | Not directly; BUT an approval charges nothing new while making every OTHER pending proposal stale: their quota was already spent (F2 makes this attacker-triggerable). |
| remembered ids (`records`) | guests | shared map | 248 (31 × 8), `IdsFull` unreachable by arithmetic (equivalent mutant M46) | No |
| muted set | the starter's act | starter | ≤ 31 | No |
| roster entries (members + removed) | starter | session | 32 | Only the starter can fill it; once full nobody can be added (intended). A guest cannot spend it: proposals add nothing until approved. |
| roster versions | starter | session | 256 | Same; at 256 the intake still accepts and approves (F2, second path). |
| `seen` versions per member | starter | each member | 256 × ≤ 65,535 bytes | No |
| starter approving / removing / changing the limit | — | — | — | Nothing a guest does blocks `next_with_cap`, removal, or a direct invite: they do not touch the intake. A guest can make one specific approval useless (F2). |

## 4. Mutation table (61 mutants on the new code; the builder's tests only)

Driver: `gate_roster_tests_m3/mutate.py` (each mutant: one textual change, `cargo test -p coagent-roster` over the builder's 12 test targets, file restored). Baseline green first.

| id | mutation | result |
|---|---|---|
| M01 | cap > CAP+1 | killed |
| M02 | cap 2 accepted | killed |
| M03 | count rule removed | killed |
| M04 | count limit +1 | killed |
| M05 | slot `>=` → `>` | killed |
| M06 | version bound +1 | killed |
| M07 | entries bound +1 | killed |
| M08 | entries bound −1 | killed |
| M09 | proposer = candidate allowed | killed |
| M10 | proposer = starter allowed | killed |
| **M11** | at_version 0 allowed (version-1 proposals) | **SURVIVED** — real unguarded check (DQ4 has no test). F7 |
| M12 | shape at_version+1 = added_in removed | killed |
| M13 | role upgrade allowed | killed |
| M14 | I-6 `<=` → `<` | killed |
| M15 | duplicate id allowed | killed |
| M16 | unchecked not reported | killed |
| M17 | first-roster signature error ignored | killed |
| M18 | unchecked report dropped next version | killed |
| M19 | cap change never reported | killed |
| M20 | cap change from/to swapped | killed |
| M21 | observer proposer allowed (transition) | killed |
| M22 | transition at_hash unchecked | killed |
| **M23** | transition at_version unchecked | SURVIVED — equivalent: the shape rule forces `at_version = added_in − 1` and the transition forces `added_in = next.version = held.version + 1` (REASONED) |
| M24 | `is_roster_signer` always true | killed |
| M25 | `CapUnchanged` removed | killed |
| M26 | helper skips `validate_body` | killed |
| M27 | admit: observer may propose | killed |
| M28 | admit: anyone sends result | killed |
| M29 | silent drop (control on old rule) | killed |
| M30 | transition proposal rules skipped | killed |
| M31 | free seat `>=` → `>` | killed |
| M32 | intake lifetime off by one | killed |
| M33 | per-proposer pending off by one | killed |
| M34 | session pending off by one | killed |
| M35 | quota off by one | killed |
| M36 | expiry `>=` → `>` | killed |
| **M37** | `tick` staleness ignores hash | SURVIVED — equivalent for a caller that passes its own chain's versions (one hash per number); unguarded if a caller passes a forked version. Note |
| M38 | approve: role raise allowed | killed |
| M39 | approve: others stay pending | killed |
| M40 | intake session check removed | killed |
| M41 | intake: starter may propose | killed |
| **M42** | intake check 4 ignores hash | **SURVIVED** — real unguarded check; with it broken, a wrong-hash proposal is pending and its approval builds a body the validator refuses (`ProposalNotForPrevious`). F7 |
| M43 | candidate key id unchecked | killed |
| M44 | member candidate allowed | killed |
| M45 | removed candidate allowed | killed |
| **M46** | `IdsFull` removed | SURVIVED — equivalent by the stated arithmetic (31 proposers × 8) |
| M47 | `may_approve` always true | killed |
| **M48** | approve: `added_at` unchecked | **SURVIVED** — real unguarded check (another refused-body path). F7 |
| **M49** | approve: lifetime re-check removed | SURVIVED — equivalent: receive checked it and any roster change makes the proposal stale before approve |
| M50 | mute not recorded | killed |
| M51 | quota not charged | killed |
| **M52** | receive: roster/session/approver check removed | **SURVIVED** — real unguarded check (`WrongRoster`, `NotApprover` on receive). F7 |
| M53 | label bytes changed consistently | killed (the cross-domain test pins the exact signed message) |
| M54 | label separator dropped | killed |
| M55 | label dropped | killed |
| **M56** | `SignedProposal::decode` 2,048 check removed | **SURVIVED** — real unguarded check for any caller of `decode` other than the intake. F7 |
| **M57** | `propose()`: observer allowed | **SURVIVED** — proposer-side convenience check untested. F7 |
| **M58** | `propose()`: removed candidate allowed | **SURVIVED** — same. F7 |
| M59 | `verify()`: WrongProposer removed | killed |
| **M60** | `propose()`: starter allowed | **SURVIVED** — same. F7 |
| M61 | `Member::proposed` records entry role | killed |

Mutations are textual; no mutant failed to compile or apply.

## 5. Step 7: merge and compile with the unmerged crates

| Tree | Merge | `cargo check --locked --workspace --all-targets` | `cargo test --locked --workspace --no-fail-fast` |
|---|---|---|---|
| `origin/main` (18005d6) + m3-roster | fast-forward to 0a47fc9 (no merge commit) | = head: clippy clean in check.sh ×5 | = head: 301 passed, 0 failed ×5 |
| `origin/m1-daemon` at **bb92225** (newer than the 8e7b032 the brief cites) + m3-roster | **conflict in `BACKLOG.md` only** (both appended); resolved by keeping both sides; merge commit 77f2d7a (scratch only) | **exit 0** (one pre-existing workspace warning `unused workspace dependency rand_core`, root Cargo.toml, not touched by m3-roster) | 321 passed, **28 failed**: all 28 are process-level daemon tests failing with "timed out … daemon IPC ready" (22), "in-process daemon IPC ready" (5), "exactly one daemon runs" (1). Control: see the line below. Roster crate tests in this tree: pass. Daemon unit tests (14) pass. |
| control: `origin/m1-daemon` bb92225 UNMERGED, same environment | — | — | 270 passed, **28 failed: the identical set of 28 test names** (`diff` of the sorted FAILED lines: identical). So the merge adds no failure; the 28 are environmental (F12). |
| `origin/m3-audit` at **882e094** + m3-roster | **conflict in `BACKLOG.md` only**; `Cargo.lock` auto-merged; resolved as above; merge commit ba994e8 (scratch only). Note: m3-audit is based on an older main, so the merge also brings main's newer commits. | **exit 0** (same pre-existing `rand_core` warning) | **417 passed, 0 failed** (includes the audit crate's tests that build rosters, `Applied::Advanced { removed, .. }`, `RosterError::Fork`, `LocalNotMember`) |

The builder's REQUEST 4 ("UNKNOWN until run") is therefore closed for compilation and for the audit crate; for the daemon's process-level tests it stays UNKNOWN (F12).

## 6. Rulings on the builder's eight DESIGN QUESTIONS

| DQ | Ruling | Why |
|---|---|---|
| 1 approval makes every other pending proposal stale | **sound** | Two approvals against one version would be a self-signed fork; RAN `qa_two_approvals_race`. But the stale ones are not reported (F5). |
| 2 I-6 checked on every version alone | **sound** | With the append-only `removed` list and recorded removal versions it equals the transition rule and also covers a joiner. Mutation M14 killed. |
| 3 I-6 compares key ids only | **sound as a statement; the residue needs the owner** | RAN (F6): a removed person's signing key returns with a new Noise key through a guest's proposal; the new entry takes another slot, so per-slot attempt inheritance does not help. It does NOT reset the verify-attempt accounting of the design, IF the daemon builds 06 §5.2(b)(2) (every entry added after any removal inherits the highest count used with any removed entry; REASONED, that rule is key-independent and unbuilt). Until the daemon builds it, the gap is real, but it is no wider than a removed person returning with an entirely fresh identity, which no key rule can stop. Owner question: is "previously removed signing key" worth a card warning? It needs the removed entries' signing keys in the roster. Fix the doc's over-claim either way. |
| 4 proposals in version 1 refused | **sound** | No version 0 exists. Untested (M11 survived): add a test. |
| 5 joiner's own proposer check is the daemon's | **sound** | The crate cannot know whom the joiner paired with; `proposer_of(local)` exposes it. |
| 6 intake takes canonical bytes | **unsound as written / needs the design owner** | F4: bytes taken from an envelope JSON value are not canonical, so honest proposals are refused. The wire format must carry the proposal opaquely (string) or the bound must move. |
| 7 `next_with_cap` refuses the limit in force | **sound** | A no-op change is not a limit change. |
| 8 approval can never build a version the validator refuses | **unsound** | F2: two counterexamples RAN (twin device key; version 256) and two more by unguarded checks (M42 wrong hash, M48 long `added_at`). |

## 7. Attacks that did not succeed (RAN unless marked)

- Every `cap` 0..=255 in version 1 and in version 2 from 4 and from 8: exactly 4 and 8 accepted, 9..=255 `CapExceeded`, others `BadCap`; refused versions leave version, hash, cap, member list, roles, slots, proposers and unchecked list unchanged; the report names old and new values.
- Lowering 8 → 4 in all 256 slot arrangements (starter in slot 0 and in slot 6): accepted exactly when ≤ 4 members all below slot 4; `next_with_cap` agrees in every case; raising back always accepted.
- One version that lowers and removes: accepted when the remaining members fit, `BadSlot` otherwise, chain unchanged; a non-starter's cap change `BadSignature`.
- Lifetime via `start`: 32 entries accepted, 33 `LifetimeExceeded`; versions 256 accepted, 257 and `u64::MAX` refused; `next_with_cap` at 256 → `TooManyVersions`.
- Signature confusion: a canonical roster body always begins with `{`, the proposal message with `c`; `canonical::decode::<RosterBody>` refuses label‖0‖body; a proposal signature grafted on a roster (starter as proposer) → `BadSignature`; a roster signature on a proposal → refused; a raw Roster-domain signature over label‖0‖body → `BadSignature` as a roster. No other code on main, m1-daemon or m3-audit signs in the Roster domain (grep RAN; m3-audit has its own domains). `verify_strict` is used, so no signature malleability.
- Replay of a genuine proposal after a no-change version and after a limit-only version: `BadProposalVersion` as signed, `BadProposalSignature` when at_version/at_hash are rewritten; a fresh proposal against the new version accepted.
- Reuse of a genuine proposal for another candidate, role, proposer or session: `BadProposalSignature` each, chain unchanged.
- Two different entries rebuilding the same signed bytes: impossible within a version (key id must match keys and keys are unique); across versions the record pins `added_in`. REASONED.
- Proposer proposing its own second device (same signing key): refused by the validator (`DuplicateDeviceKey`), though accepted by the intake (F2).
- Joiner's first roster with proposer present, removed, and removed-then-re-added under the same key: checked when present (bad signature → `BadProposalSignature`), reported unchecked when absent.
- Intake: time backwards keeps a proposal pending; expiry exactly at TTL (not 1 ns before); far-future time expires; id replay after expiry and after decline → `DuplicateId`; inside check 9 the earliest sub-check reports (`QuotaUsed` before `Muted` and `DuplicateId`; `SessionPendingFull` before quota and mute); two approvals racing → second `NotPending(Stale)`; cap-only change makes a pending proposal stale and its quota stays used.
- `admit`: `member.propose` refused from an observer, `member.propose.result` refused from a guest (builder's tests, killed mutants M27, M28, M47). Call sites (grep RAN): `is_roster_signer` used by `check_roster_signer` and `admit` only; `may_approve` by `ProposalIntake::new`, `check_roster` and `admit` only; no other `convener` comparison decides signing or approving (the other three decide "the starter does not propose").

## 8. For the owner, in plain words

1. The member list still cannot be forged: only the starter can sign it, and nobody can claim that a member proposed someone they did not propose.
2. The new limit works as you ruled: 4 by default, 8 at most, only you can change it, and every member is told when it changes.
3. Not yet trustworthy: someone added through a proposal as an observer can never later be made a guest, because the program refuses that change (F1).
4. Not yet trustworthy: a member can trick your approval screen so that pressing Approve adds nobody and cancels everyone else's waiting requests (F2).
5. A group of members can keep the queue of requests full for about two hours at most; you stop it by choosing "Decline and stop proposals" for each of them.

## 9. What I could not do

- The 28 process-level daemon tests could not run in my scratch path (socket path over the macOS limit; identical on the unmerged branch). UNKNOWN for the merge; closed by running the merged tree from a short path (the project's own `tools/tmp`).
- Mutation runs, starvation and the QA tests ran on a busy machine; the QA tests ran 3 times with identical results; check.sh 5 times.

## 10. Artefacts

Sources only, in `gate_roster_tests_m3/`: `qa_gate.rs` (head tests, needs the crate's `tests/common` and `tests/prop_common`), `qa_pin_gen.rs` (run on main with `QA_PIN_OUT=<file>`; the head test reads it with `QA_PIN_IN`), `mutate.py` (driver), `mutation_results.tsv`, `qa_gate_results.txt`.
