VERDICT: NO GO — head 52d12e9f9acf0356ba936afe7f5f1c814b3e40ba

# QA gate M3-AUDIT round 4 (the one check after design 07): `coagent-audit`, branch `m3-audit`

Independent gate, 2026-11-17. Findings only: nothing fixed, committed, merged or pushed; nothing written in the project folder. Clone `git rev-parse HEAD` = `52d12e9f9acf0356ba936afe7f5f1c814b3e40ba` = the head under test (TESTED). Working folder: `/private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_audit_r4/` (`clone` pristine: check.sh + red runner; `atk` my tests; `mut1..3` mutants; `ref` earlier gates' files unchanged; `mrg_main`, `mrg_roster` merges). My tests, drivers and results: `m1_review/gate_audit_tests_r4/` (drop `gate_r4.rs` into `crates/coagent-audit/tests/` and add `[[test]] name = "gate_r4"`; the crate has `autotests = false`).

## BLUF (for the owner)

1. The redesign is built faithfully and the class the three earlier checks found is closed for what other members SEND: in 256 generated sessions (honest, hostile and outside members; removals, re-adds, new keys in used seats; full seats; restarts; release) the counted size always equalled the real stored size, no seat or table went over its limit, nothing acknowledged was lost, every export verified, and member-list changes always applied.
2. Every Blocker and Major of rounds 1 to 3 is fixed, each shown by a test of mine that fails on the old behaviour.
3. One Major remains, in the same class, at a place design 07 did not price: when your computer records actions because other members asked (`record_for`), the checkpoints that cover those actions are paid from YOUR OWN "free" space, which the design says nobody else can touch.
4. Measured with the default limits: seven members each staying inside their allowance, one request a minute for about 80 hours, use 78.9% of your free space while you record nothing yourself; afterwards you can record 1,014 actions of your own instead of 4,810.
5. Four Minors: a failed disk write leaves the log permanently unexportable; a member re-added by the starter into a used seat can overfill that seat; a restart silently accepts a store missing whole records (all damaged or cut records are caught); four design rules had no test (I wrote guards; the code was correct).
6. The fix for the Major is small and local (charge such checkpoints to the requesters' allowances, or hold back checkpoint room inside each allowance), but it changes a design rule, so it is the owner's call; everything else could be merged as notes.

## 1. Findings

| id | sev | what | input that shows it | exact output seen | file:line |
|---|---|---|---|---|---|
| **R4-M1** | **Major** | Checkpoints that cover events recorded at a PEER'S request are charged to the member's FREE part. Design 07 §1.4 (b) "Nothing a peer does can consume it"; §1.6 item 2 "the free part's usage is a function of V's own `record`, `announce_share_level` and checkpoint calls alone"; §2 row 1 "can never … use … the free part"; `docs/AUDIT.md:133-134` and `:237` ("with all seven hostile V still has its whole free part"). The seat's P2 harness treats `record_for` as the victim's own call and keeps it in every run (`tests/a3_props.rs:440-444`), so P2 never tested it. Bounded by V's checkpoint cadence (at most one checkpoint per V checkpoint call, each needing a new event) and only when V acts on requests, which design D5 makes the daemon's rule. | 8 members, V = slot 1, default policy (50 events or 60 s); each minute one `record_for` from the next of 7 requesters, then V's `checkpoint(now)`; V records nothing of its own; then V records tiny own events until refused. `r4_finding_release_requested_checkpoints_default_limits` (release) and `r4_finding_requested_events_drive_checkpoints_into_the_free_part` (debug, small limits) | TESTED, release, default limits: "4809 requested events (2533236 bytes in allowances) over 4809 minutes … made 4809 checkpoints, free part used 1999437 bytes (78.9%) with no own record; own records then possible 1014, against 4810 without the requests (free used 0)". Debug, seat 32 KiB: free used 11583 of 16256 bytes, own records 7 against 29. | `src/session.rs:1039-1061` (`checkpoint_now` charges `Part::OwnHead`, `own_room(Part::OwnHead, …)` = free part), `:1010` (`record_for`), `:654-692` (`own_room`) |
| R4-m1 | Minor | A store write that fails after the space check leaves the chain advanced in memory and the record absent (§1.7 step 6 "apply and store, all or nothing"). The next write succeeds, so the stored chain has a hole: every later export fails `verify`, `resume` refuses the store. Same order in `receive`. Needs a failing `Store` (the trait allows it; `MemStore` never fails; no daemon store yet). | `Flaky` store: write 2 fails, write 3 succeeds. `r4_finding_a_failed_store_write_leaves_the_own_chain_ahead_of_the_store`, `…_leaves_a_hole_in_a_received_chain` | TESTED: own "in memory seq 3, stored own events 2; export+verify Ok(Err(VerifyError { class: Header, what: \"sequence\" … seq: Some(2) })); resume Err(NoSuchEvent(3))"; received "re-send Err(Receive(Replay { seq: 2 })) … stored seqs [1, 3] … resume Err(Receive(Gap { expected: 2, got: 3 }))" | `src/session.rs:853` then `:861` (commit before write); `:1152-1162` (receive); `:1050` then `:1051` (checkpoint); `:1086` then `:1094` (countersignature) |
| R4-m2 | Minor | When the starter removes the member ITSELF and re-adds it into a slot whose seat still holds a removed member's records, `seat_usage` adds the own usage on top and `own_room` checks only the own parts: that seat holds more than a seat (§1.6 item 3). Total stays under the bundle caps (at most one extra seat by arithmetic). While the member is not in the roster, `local_slot()` falls back to slot 0 and charges the own usage to slot 0's occupant. | X fills seat 2 at V; starter removes X, removes V, re-adds V in slot 2, adds a new member in slot 1; V records. `r4_finding_own_seat_re_added_into_a_used_slot_exceeds_the_seat` | TESTED: "seat 2 now (20203, 4) (seat limit (16384, 64), own limit (16320, 64))" | `src/session.rs:491-493`, `:497-507`, `:654-692` |
| R4-m3 | Minor | `resume` silently accepts a store that is missing WHOLE records at a tail or in a fixed slot: the latest roster version (the member forgets a removal), an evidence record, an attestation, a cross-check slot, the newest peer event, the newest peer checkpoint. Every flipped byte and every truncated record is caught. | every record of a 13-record store: a bit flipped every 7th byte and the last, cut to half, removed. `r4_damaged_store_fails_closed_or_is_reported` | TESTED: "resume refused 1504, export refused 308, identical export 0, SILENT 6"; the 6: "record removed (key n=2 …) in Fixed(Roster)", "… Fixed(Evidence)", "… Fixed(Attestation)", "… Fixed(HeadsSeen)", "(key n=3) in PeerEvent(2)", "(key n=3) in PeerHead(2)". (The first run asserted none silent and went red on these six.) | `src/session.rs:291-437` (no count or anchor of what was stored) |
| R4-m4 | Minor | Design rules with NO test in the branch that fails without them (code correct on every input I tried): roster lifetime backstops (M11), the FIRST roster conflict kept (M22), own checkpoint space-checked (M23), conflict slot rebuilt by `resume` (M28); and "one requester cannot use another's allowance" (M14) killed only by my tests. | my mutants, whole branch suite `--no-fail-fast` | TESTED: M11, M22, M23, M28 SURVIVED the branch suite (0 failures; rc=0); M14 killed by 0 branch tests. My guards kill each: `r4_guard_roster_lifetime_backstops` ("v257 Err(RosterLifetime)"; 33rd key RosterLifetime), `r4_guard_the_first_roster_conflict_is_kept`, `…_survives_resume`, `r4_guard_an_own_checkpoint_is_space_checked`, `r4_guard_one_requester_cannot_use_anothers_allowance` | `src/session.rs:914`, `:929`, `:1049`, `:397`, `:1010` |
| N1 | Note | Merge with main `454bfb5` is NOT clean: one text conflict, `BACKLOG.md` (both sides append). Union resolution in a throwaway copy: `check.sh` exit 0, 485 passed / 0 failed / 16 ignored, tree `2ec29094…`. The seat's merged tree used 18005d6 (its local `main`), not 454bfb5. | `git merge 454bfb566dd…` | TESTED: "CONFLICT (content): Merge conflict in BACKLOG.md"; then "CHECK OK" | `BACKLOG.md:142-279` (merged copy) |
| N2 | Note | Roster branch (`44662d5`) merged on top: CONFIRMED, `u6_a_valid_roster_version_near_the_encoding_cap` fails ("the roster chain accepts the version: LifetimeExceeded"); everything else passes (workspace 597 passed, 1 failed, 16 ignored). For whichever merges second. Also: the audit backstop counts DISTINCT keys ever, the roster counts ENTRIES (members + removed); both are 32, so the roster refuses first, but an "equal constants" test (07 §1.4 a) would not show the semantics differ. | merge main then roster, `cargo test --workspace --no-fail-fast` | TESTED | `tests/a3_unknowns.rs:248`; roster `src/lib.rs:66, 556` |
| N3 | Note | Gate files: two `RULING REQUESTED` edits outside Friday's table still await a ruling (`gate_attacks.rs:88` fixture only; `gate_r2.rs:650` `r1.is_ok()` → `== Err(NotNewer)`). By reading `chain.rs:495-553`, `NotNewer` is checked after the countersigner rule and the signature, so the edit does not weaken rule 1. The ruled edit of `r3_finding_fork_from_an_author_at_quota…` accepts ANY `Receive(_)` error (`gate_r3.rs:785-787`); `r4_fixed_r3_n2_*` asserts `Fork` with evidence exactly. | diff vs the reference copies | READ + TESTED | as named |
| N4 | Note | Once the free part is full, events recorded at a peer's request are still accepted but can never be checkpointed (the checkpoint is `LogFull`), so peers never witness them. Inherent to 07 as written; worsened by R4-M1. | `r4_guard_an_own_checkpoint_is_space_checked` | TESTED: "last requested Ok(()); last checkpoint Err(LogFull)" | `src/session.rs:1049` |
| N5 | Note | I-A1 with I-A7: a member's later countersignature with `held_from: None` (e.g. its seat for the author became full) replaces its earlier `Some(n)`, so the author loses its only proof that this member held its events. | by reading | READ | `src/chain.rs:546-582` |
| N6 | Note | `resume` comes back with DEFAULT limits; the daemon must call `set_limits` again or the limits silently rise. Documented. | by reading | READ | `src/session.rs:288-289` |
| N7 | Note | A peer's checkpoint naming roster version 0 (or any version not held) is accepted, stored and countersigned. Not storage; outside this gate's scope; flagged. | `r4_extreme_numbers_*` | TESTED: "head 1/0: Ok(None)" | `src/received.rs:480-522` |
| N8 | Note | A person's first name in branch docs. | name scan of `git diff origin/main...HEAD` | TESTED | `BACKLOG.md:196` |
| N9 | Note | `gate_r3::r3_release_flood_measurements` part (c) fails in release (seat's A3-Q2, reproduced): the flooding peer's own free part fills first. `#[ignore]`d. | `cargo test --release --test gate_r3 -- --ignored` | TESTED: "panicked at crates/coagent-audit/tests/gate_r3.rs:407:18: … Err value: LogFull" | `tests/gate_r3.rs:407` |

No Blocker. One Major (R4-M1). GO requires no Major.

## 2. Design 07, rule by rule (my mutants: plain-code edits, one at a time, whole `coagent-audit` suite `--no-fail-fast` plus `gate_r4`; driver `mutate_r4.py`, results `mutation_final_all33.txt`, `mutation_round1_*.txt`)

| rule (07 §) | code | branch test that fails without it (first named) | my mutant: result |
|---|---|---|---|
| 1.4b seat byte limit, exact size | `session.rs:643` | `p3_bounds_and_exact_accounting` (+2 r2m1 tests) | M01 KILLED (seat 3, r4 2) |
| 1.4b seat record limit | `:646` | `p01_a_seat_stops_at_its_record_limit`, `p3_*` | M02 KILLED |
| 1.4b seat = one eighth | `:629` | `p01_*`, `p3_*`, 2 r2m1 | M29 KILLED |
| 1.4b closing checkpoint held back | `:686` | `own_size_exact_*` only | M03 KILLED (1 test) |
| 1.4b requested allowance size | `:663` | `p3_*`, `p7_*` | M04 KILLED |
| 1.4b one requester cannot use another's allowance | `:1010` | none | M14 SURVIVED the branch; killed by `r4_guard_one_requester_*` (R4-m4) |
| 1.4b record charged to its author's seat | `:1157` | `p2_seats_do_not_interfere`, `p01_*`, 4 gate_r3 | M15 KILLED (seat 10) |
| 1.4b own checkpoints space-checked in the free part | `:1049` | none | M23 SURVIVED the branch; killed by `r4_guard_an_own_checkpoint_*` (R4-m4) |
| 1.4b own seat = seat − 1 byte/record (P7) | `budget.rs:157` | `n15_*`, `own_size_exact_*` | M25 KILLED |
| 1.4a roster lifetime backstops | `:914` | none | M11 SURVIVED the branch; killed by `r4_guard_roster_lifetime_backstops` (R4-m4) |
| 1.4a cross-check two slots per reporter | `:210` | `r2m1_a_heads_seen_record_is_stored_only_when_it_advances`, gate_r3 fresh-empty, `m20_*` | M10 KILLED |
| 1.4a / P27 evidence cap 4 | `:721` | `p27_the_evidence_cap_is_four`, `p4_*` | M09 KILLED |
| 1.5 D / 1.8 checkpoint beyond a full seat → fixed slot | `:1241` | `p3_*` | M08 KILLED |
| 4.1 FIRST roster conflict kept | `:929` | none | M22 SURVIVED the branch; killed by `r4_guard_the_first_roster_conflict_is_kept` (R4-m4) |
| 4.2 replacing a slot releases the old charge | `:568-570` | `p3_*`, `p5_*`, 2 replacements | M05 KILLED |
| 4.2 non-advancing cross-check is NotNewer | `:1384` | `p08_*`, `p09_*` ×2, `p4_*` | M21 KILLED |
| 1.7 step 3 fork evidence stored (event) | `:1145` | `p6_*`, `p19_*`, `p27_*` | M18 KILLED |
| 1.7 step 3 fork evidence stored (checkpoint) | `:1233` | `p1b_*`, `p6_*` | M19 KILLED |
| 1.7 step 5 space check on a received event | `:1151` | `a1_m4_*`, `p01_*`, 4 gate_r3 … | M07 KILLED (seat 10) |
| 1.7 step 5 exact framed size | `:131` | `own_size_exact_*` | M24 KILLED |
| 1.9 release deletes from the store | `:608` | `p9_*`, `p3_*`, `p5_*`, `p8_*` | M06 KILLED |
| 1.9 release only for a non-member | `:1423` | `p9_*` | M17 KILLED |
| 1.10 start refuses a used store | `:258` | `p5_*`, gate_r3 restart | M12 KILLED |
| 1.10 resume charges each record to its part | `:375` | `p1c_*`, `p3_*`, `p5_*` | M13 KILLED |
| 1.10 resume rebuilds cross-check slots | `:391` | `p4_*`, `p5_*` | M26 KILLED |
| 1.10 resume rebuilds evidence | `:394` | `p5_*` | M27 KILLED |
| 1.10 resume rebuilds the conflict slot | `:397` | none | M28 SURVIVED the branch; killed by `r4_guard_…_survives_resume` (R4-m4) |
| 1.11 / R2-M1 nothing from a removed reporter | `:1370` | `a1_m1_*`, gate_r2 readd, gate_r3 convener, `p4_*`, replacement | M16 KILLED |
| R2-M1 no countersignature from a removed member | `:1080` | `r2m1_nothing_from_a_removed_member_*` | M20 KILLED |
| P1–P9 as properties | `a3_props.rs` | the seat's runner: **133 of 133 RED** on their property's text (TESTED, below) | builder's cfg controls, all RED |

Every rule I could locate has code; 24 of 29 of my mutants are killed by the branch's own tests; the 5 it misses are R4-m4 and are killed by my guards. My check mutants M30–M33 show my finding tests can go red: M30 (own checkpoints outside the free part) kills `r4_finding_requested_*`; M31/M32 (store before advancing) kill the two R4-m1 tests; M33 kills the R4-m2 test (TESTED, `mutation_final_all33.txt`).

**Interpretations I-A1 to I-A10** (built on, not ruled). Wrong as stated: **I-A9** ("a requester cannot use up your log"): the requester's checkpoints land in the free part (R4-M1). Weakened by combination: **I-A1 with I-A7** (N5). **I-A2**: the fixed capacity is effectively smaller than stated while R4-M1 stands. I-A3, I-A4, I-A5, I-A6, I-A8, I-A10: no objection.

## 3. The storage-accounting class: my own property (`r4_prop_storage_accounting`)

Generator: 3–8 members, victim V in slot 1 (not the starter), seats of 1.5–40 KB and 3–80 records (so full seats, full allowances and full free parts are reached), 20–90 steps from 16 operations: honest events of three sizes up to the maximum (4,000-byte summary, 60,000-byte full before redaction) in bursts; checkpoints (with extra events, so beyond-the-seat slots fill); forked events and forked checkpoints; replays; own records; `record_for` (members and an outsider); own checkpoints; countersignatures (latest replaces; `held_from` Some/None); cross-check records (broadcast and addressed); removals; re-adds of removed keys into any free slot; fresh keys into slots whose seat holds records; archive-and-release (and release of a current member); `resume`; roster replays; an outsider sending an event, a checkpoint or a cross-check record. After EVERY step: I1 `store_usage` = real framed size of `Store::list`; I2 seats + fixed tables = real size; I3 every seat, allowance and the free part within its limit (bytes and records); I4 every fixed table within slots and bytes, every record within its kind's maximum and under the key of its own kind; I5 within capacity; I6 every acknowledged event (peer and own) still in the store (until released, when it must be in the release's file); I7 the export verifies; any refused or no-op input leaves the store byte-identical; a valid roster version is never refused; a fork is always `Fork` and its evidence stored (until 4); `resume` gives identical `status()` and byte-identical export.

TESTED, release, 256 cases: **passed**. Rule-path counts (each must be > 0): peer event accepted 3,126; max size 941; refused seat full 1,733; checkpoint logged 959, to latest slot (seat full) 139, replaces latest slot 88; fork evidence stored 686; evidence cap reached 15; replay refused 320; own free accepted 708, refused free full 1,343; requested accepted 153, allowance full 1,009, causer not member 115; own checkpoint 464, refused full 10; attestation stored 265, replaced or replayed 55; cross-check stored 525, replaced 194, refused 49; roster applied 305, with a seat (nearly) full 361; re-added 188; new key into a used seat 67; release with records 173, empty 145, current refused 441; resume 751; roster replay 368; outsider refused 351. (Debug run of 64 cases in the final run: passed.)

Red once each (TESTED, builder's cfg red controls on MY test, `red_controls_on_r4_tests.txt`): `shared_peer_pool` → "I3: seat 0 holds (1575, 3), above its limit (1500, 3)"; `uncharged_slot` → "I2: seats (0, 0) + fixed (0, 0) != store (1806, 1)"; `release_keeps_charge` → "I2: seats (525, 1) + fixed (3250, 2) != store (3250, 2)"; `resume_all_own` → "resume: status differs"; `roster_on_seat` → "a valid add was refused: LogFull". My plain mutants M01, M02, M04–M09, M13, M15, M17–M19, M27, M29, M30 also kill it.

What it did NOT find, and why R4-M1 is outside it: it measures that V's free part never exceeds its limit, not who caused it to fill; R4-M1 is within every limit and is a who-pays question (found by reading, then measured).

## 4. Earlier Blockers and Majors (classes: A-B1 confidentiality; A-M1 cross-check correctness; A-M2 author/verify consistency; A-M3 signing domains; A-M4, R2-M1, R3-M1 storage accounting)

| id | fixed? | my test (passes now) | the same test under the old behaviour (builder's red control, TESTED) |
|---|---|---|---|
| A-B1 (Blocker) | fixed | `r4_fixed_a_b1_*`: 0 header entries reach a `nothing` member; forged broadcast with a header → `Err(Evidence(HeaderInBroadcast))`; header bytes absent from its store and export, present at A (control) | `hs_headers_to_nothing` → RED "a heads-seen record to a nothing member carries headers" |
| A-M1 | fixed | `r4_fixed_a_m1_*`: B holds a chain of D, D removed; C still gets the evidence (`Ok(1)`) | `hs_current_roster` → RED "equivocation not caught after a removal: Err(Evidence(NotAMember))" |
| A-M2 | fixed | `r4_fixed_a_m2_*`: a joiner's countersignature of a checkpoint before its anchor → `NotMember`; of its anchor → Ok; export verifies | `cs_rule_current_only` → RED "a joiner countersigned before its anchor" |
| A-M3 | fixed | `r4_fixed_a_m3_*`: 30 audit-domain signatures over chosen 32-byte values, 0 verify as device bindings; real binding verifies (control) | `audit_under_binding` → RED "audit-domain signatures verified as device bindings: [\"Header\", …]" |
| A-M4 | fixed | `r4_fixed_a_m4_*`: 1,500 checkpoints, all countersigned; 1,025 stored (default limits) / 10 (4 KiB seat); export 428,715 bytes parses and verifies | `head_no_cap` → RED "1500 checkpoints stored for one author" |
| R2-M1 | fixed | `r4_fixed_r2_m1_*`: 2,000 replays and 2,000 fresh records from a removed reporter: 0 accepted, store unchanged, own record Ok | `hs_accept_removed_reporter` → RED (store grew) |
| R3-M1 (a)(b)(c) | fixed | `r4_fixed_r3_m1_*`: 600 events flooded into C (starter) and into H (non-starter): their own chains 0; C's seat at V full from its OWN events; removal applies; the removed member's checkpoint `NotMember`, cross-check `ReporterRemoved` | `receipt_on_receive` → RED "a received event wrote into the receiver's own chain"; `roster_on_seat` → RED "the removal was refused with the starter's seat full: Err(LogFull)" |
| R3-n2 (Note, exact form) | fixed | `r4_fixed_r3_n2_*`: fork from an author with a full seat → `Fork`, only `Fixed(Evidence)` changed | `space_before_fork` → RED "…was not answered Fork: Err(LogFull)" |

Earlier gates' reference files, UNCHANGED, against this head (TESTED, `ref_ref*.txt`): round 1 `gate_attacks.rs` does not compile (`domain::sign`/`verify` private, `nested_message` gone: the A-M3 fix); round 2 `gate_r2.rs` does not compile (`note_share_level` takes the signed statement: the R2-m2 fix); the branch carries ruled copies of both, which pass. Round 3 `gate_r3.rs`: 6 pass, 5 fail — exactly the five 07 §4.3 rules void (convener quota, receipts proxy, restart, evidence-not-stored, fork-gives-LogFull) — and `r3_ok_colluder_advancing…` loops to its 5,000,000 guard (void: records replace one slot); I stopped it after 17 minutes.

## 5. Bounds and hostile input

- Extreme numbers on the new paths (`r4_extreme_numbers_*`, TESTED, debug so overflow would panic): checkpoints at 0, 1, 2^62−1, 2^62, 2^62+1, u64::MAX × roster version 0, 1, 2, u64::MAX; cross-check records likewise; `held_from` 0, 1, 2, u64::MAX, None: no panic; `author_seq` > 2^62 → `BadField`; unheld versions → `RosterBehind`; out-of-range `held_from` → `FieldLimit("held_from")`; store accounting exact; export verifies. Red once under `head_no_max_seq` ("verify(&v.export…).is_ok()" failed).
- Damaged store: R4-m3 (deletions silent; 1,812 flips/truncations all caught).
- Nothing grows from another member's input outside its seat or a fixed slot: property I1–I5 above; release (4) seven seats full: store 35,676,812 bytes, own record, roster, evidence, export all Ok.
- Recorded fixtures: none read from a drive; the only file read by a test is the crate's own `src/` (`tests/determinism.rs:57`). Name/path scan of the branch diff: one person's name (N8); no home directory, machine name or drive path (`gate_r2.rs:688` is an example.com URL; `.local` hits are `self.local`).

## 6. The seat's figures, reproduced

| seat's claim | mine (TESTED) |
|---|---|
| `check.sh` at 52d12e9: exit 0, 265 passed, 0 failed, 11 ignored | **exit 0, "CHECK OK", 265 / 0 / 11** (`check_sh_tail.txt`) |
| audit red-control runner: 133 of 133 RED, GREEN 162, RED CONTROLS OK | **rows: 133; 133 RED, 0 NOT-RED; "GREEN: 162 tests ok"; "RED CONTROLS OK"; exit 0** |
| release (1) receipt-proxy: 28,968 events at C, 0 reach V, removal Ok | **28968; 0; C's seat at V (0, 0); Ok(()); 1.71 s** |
| release (2) 1,008 max-size per peer, seat 5,095,341, export verifies | **1008 each, (5095341, 1008), store (15289101, 3026), export 15289692 bytes verifies; 7.56 s** |
| release (3) 100,000 removed-member attempts, 0 accepted | **0 accepted, ReporterRemoved, store (4158, 2) unchanged, own Ok; 3.31 s** |
| release (4) seven seats full, then own/roster/evidence/export Ok | **each (5095279, 1058); store (35676812, 7410); all Ok; export 35677403 verifies; peak RSS of the a3_release process 404,865,024 bytes** |
| gate release `--ignored`: gate 2/2, gate_r2 3/3, gate_r3 1 of 2 (part (c) LogFull, A3-Q2) | **2/2; 3/3; 1 of 2, same panic at gate_r3.rs:407** |
| U5 slot maxima; U6 confirmed | not re-measured (READ from the seat; U6 seen again in N2) |
| merged tree with 18005d6: exit 0, 414 / 16 | not reproduced: main is now 454bfb5 (N1) |
| gate_r3.rs byte-identical at the first commit | **sha256 47de59fc… at 4bc3d36 = the round-3 reference copy**; every later edit carries a RULING marker (13 in gate_r3, 2 + 1 "RULING REQUESTED" in gate_r2, 1 "RULING REQUESTED" in gate_attacks) |
| only merged-crate change is c407fe7 | **`git log origin/main..HEAD -- crates/coagent-crypto crates/coagent-proto crates/coagent-roster` → c407fe7 only**; outside the audit crate: BACKLOG.md, Cargo.lock, Cargo.toml, identity.rs, docs/AUDIT.md, docs/CRYPTO-GLUE.md, red runner |

## 7. NOT TESTED

- The core red-control runner (`red-controls-core.sh`): no core crate changed since c407fe7; not run.
- Real event sizes (U2) and a real daemon store (only `MemStore` and my `Flaky` wrapper); crash consistency of a real store (R4-m1/m3 are the shape of it).
- Memory of `verify` alone (U4); only process peak RSS.
- The R4-M1 effect with a non-default checkpoint policy or a daemon that checkpoints less often; and whether a daemon would in fact honour one request a minute for 80 hours.
- Seal and continue (not built, I-A2); the re-anchor path after a release is re-added (BACKLOG).
- Linux/Windows; a fuzzer on `Bundle::parse`; the provisional-member path beyond "an outsider is refused".
- Timing figures were taken while no other build of mine ran, but another gate may have been building on this laptop; no timing-sensitive test failed.
- U6 near-maximum roster version on this head (READ from the seat; seen failing only after the roster merge, N2).

## 8. Commands to re-run (from the working folder above; `env.sh` sets `CARGO_HOME` to the shared populated home, `RUSTUP_HOME` to the project's toolchain, read-only)

```
. env.sh; cargo fetch --locked --manifest-path clone/Cargo.toml
bash run_check.sh                      # check.sh in clone  -> check.log
bash run_red.sh                        # seat's red runner  -> red.log
bash run_atk.sh -- --test-threads 4    # gate_r4 debug (R4_CASES=64 default) -> atk.log
bash run_atk_rel.sh                    # gate_r4 release --ignored (R4-M1 default limits) + 256-case property
bash run_rel.sh                        # seat's a3_release and the three gate files, release --ignored
python3 mutate_r4.py <workdir> 3 out.json [ids]   # needs copies mut1..3 with gate_r4 registered
python3 mutsummary.py <workdir>/mutlogs out.json
bash run_red_r4.sh                     # gate_r4 tests under the builder's red controls
bash run_merges.sh; bash run_mrg_roster3.sh       # merged trees (union-resolve BACKLOG.md first)
bash run_ref.sh                        # the earlier gates' reference files, unchanged
```
