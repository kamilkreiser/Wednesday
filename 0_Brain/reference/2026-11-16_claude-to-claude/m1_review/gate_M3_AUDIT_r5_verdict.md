VERDICT: GO WITH NOTES — head 5f4577c8ca1421a45798b072c182aa60ff47339c

# QA gate M3-AUDIT round 5 (the short check after addenda 5 and 6): `coagent-audit`, branch `m3-audit`

Independent gate, 2026-11-18. Findings only: nothing fixed, committed, merged or pushed; nothing written in the project folder. Clone `git rev-parse HEAD` = `5f4577c8ca1421a45798b072c182aa60ff47339c` = the head under test (TESTED). Working folder: `/private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/80ecfb7f-8674-4d45-8f56-097f69bdbe0b/scratchpad/gate_audit_r5/` (`clone` pristine: check.sh and both red runners; `atk` my tests; `mut/mut1..3` mutants). My tests, drivers and results: `m1_review/gate_audit_tests_r5/` (drop `gate_r5.rs` into `crates/coagent-audit/tests/` and add `[[test]] name = "gate_r5"`; the crate has `autotests = false`).

## BLUF (for the owner)

1. The Major is closed: when other members ask your computer to record things, the checkpoints covering those records are now paid from the asking members' allowances. With the previous gate's input your free space stays at exactly 0, and you can still record 4,808 actions of your own, against 4,810 with no requests (the 2 lost are the stated effect of longer sequence numbers).
2. In 512 generated sessions where peers make requests (with removals, re-adds, slots changing hands, lowered limits and restarts), your free space only ever held your own records and the checkpoints covering only them. No allowance went over its limit. Restarts rebuilt the same charges. A peer never caused an extra free-space checkpoint, and a checkpoint was never refused unless you had lowered your own limits.
3. The four Minors are fixed as ruled, each shown by my own tests; the new restart check (`resume_with_anchor`) refused every missing or rolled-back record I tried and accepted every store that was merely ahead of it.
4. Three new Minors, none reachable by a peer alone. (a) If you lower your own limits below what a requester has used, every later checkpoint is refused, so your own later actions are recorded but never witnessed, until a different requester's request gets in. (b) A refused member-list version is written to disk first, and if removing it fails or the computer stops at that moment, the log can no longer be restarted or exported. (c) Three new restart checks have no test that fails without them; the code is correct, and I wrote the missing tests.
5. Every gate-file edit is one Friday permitted, marked, and not weaker; the merge of main is clean and touches nothing it should not; the docs are true, with three small qualifications.
6. My recommendation: GO WITH NOTES. Merge, and put the three Minors on the backlog.

## 1. Findings

| id | sev | what | input that shows it | exact output seen | file:line |
|---|---|---|---|---|---|
| **R5-m1** | Minor | A checkpoint whose payer (by I-A11/I-A12) has no room is refused `LogFull` (rule (c)), and EVERY later checkpoint is too. Its range starts after the last STORED own checkpoint, so the same requested event stays the newest one in range, and the same payer is asked each time. V's own later events are accepted into the free part and are never covered, so they are never witnessed. The other requesters' events in that range are not witnessed either. It ends only when a DIFFERENT requester's request is accepted; when the lowering shrank every allowance, none can be, and the block is permanent. Reachable only when the room I-A13 held back is missing: in every state I generated, that meant V's own `set_limits` lowering mid-session. With limits never lowered: 0 refusals in 512 property cases (TESTED) and 400 of 400 checkpoint calls paid (`r5_ok_without_lowering_*`, TESTED). A peer cannot cause it. `docs/AUDIT.md` names the `LogFull` but not that it repeats for good. Design question: refuse a `set_limits` that leaves an allowance below its usage plus one checkpoint, or another remedy of the owner's choice. | `r5_finding_a_payer_that_cannot_pay_blocks_every_later_checkpoint`: H requests 1, G requests until refused, V lowers its record limit until G's allowance cannot hold one more record, then 20 × (own record, `checkpoint_now`); then H requests again | TESTED: "G accepted 1, G's allowance (524, 1); V lowers its records to 26 per seat (allowance (1168, 1)); first checkpoint Err(LogFull); then 12 own records accepted, 0 checkpoints Ok, 20 refused LogFull; newest covered own seq None of 14; free part (6293, 12) of (8179, 13); H's new request Err(LogFull), checkpoint then Err(LogFull)" | `src/session.rs:628-648` (`head_payer`), `:1276-1285` (`checkpoint_now`), `:536` (`set_limits`) |
| **R5-m2** | Minor | `apply_roster` (made store-first by the seat's item (d)) writes a NEWER version to the store BEFORE the roster crate validates it, and deletes it again if the version is refused. If that delete fails (the `Store` trait allows it), or the process stops between the two writes, the refused version stays in the store. It can be a version anyone sends, unsigned or forged, because nothing has validated it yet. From then on, `resume` refuses the store and the export does not verify, even after the real next version is applied. This is the R4-m1 class, newly created by the fix: before it, a version was stored only after it applied. | `r5_finding_a_refused_roster_version_with_a_failing_remove_stays_in_the_store`: a version with a gap, offered while `remove` fails | TESTED: "apply Err(Store(Unavailable(\"r5: remove fails\"))); records 2 -> 3; resume Err(Roster(Gap { have: 1, got: 4 })); the real next version then Ok(()); resume Err(Roster(Gap { have: 2, got: 4 })); export verify Err(VerifyError { class: Roster, what: \"roster version refused\", author: None, seq: None })" | `src/session.rs:1135-1142` |
| **R5-m3** | Minor | Three rules of the new anchor have NO test, in the branch or in the gate files, that fails without them (the code is correct): (R18) a replaced slot that holds a DIFFERENT record of the SAME order is `Older`. For example, the same member's countersignature of the same checkpoint with `held_from` changed from None to Some(1): plain `resume` accepts it, and the anchor is its only check (this is N5's proof). (R23) the 512 KiB byte bound of `from_bytes`. (R26) a fixed record's digest is dropped when it is deleted; without that, after any refused newer roster version, the anchor names a record that is not in the store, and a GOOD store is refused at restart. My guards fail under each mutant. | my mutants R18, R23, R26, whole branch suite `--no-fail-fast`; then my guards `r5_guard_*` | TESTED: branch suite 0 failures for each; my guards red: R18 "with anchor Ok(())"; R23 "524289 bytes -> Ok(())"; R26 "Err(Missing { part: Fixed(Roster), …, n: 4 })"; all three green on the branch ("with anchor Err(Older { part: Fixed(Attestation), … n: 0 })", "Err(Malformed(\"too large\"))", "Ok(())") | `src/anchor.rs:215`, `:261`; `src/session.rs:772` |
| N1 | Note | A peer's requests CAN make an own-choice record refused, beyond (d3), in one state: V removed and re-added into a slot whose seat still holds an earlier occupant's records (R4-m2's state). The seat cap counts the allowances too, and arrival order decides. This is consistent with 07 ("the newcomer in that slot has what is left of the seat"), but `docs/AUDIT.md` "V still has its whole free part" is not true in that state. The slot-0 fallback while V is off the roster (A5-Q1) is the same mechanism. | `r5_finding_requests_refuse_own_records_in_a_reused_slot` | TESTED: "with requests 4 accepted, then 1 own records (free (524, 1), seat 2 (15705, 12)); without requests 8 own records (free (4192, 8), seat 2 (15625, 11)); free part limit (8160, 32)" | `src/session.rs:868-876` |
| N2 | Note | After a failed write on a FIRST event or checkpoint from an author, the member is not exactly as before: `chain_for` has already inserted an EMPTY received chain, visible only through `peer()`. Nothing is stored or exported; `resume` drops it. This predates the change (any refused first event does the same). | `r5_ok_all_or_nothing_on_every_write_path`, received event | TESTED: "ONLY difference an empty received chain: [\"peers: [\\\"None\\\", … ] -> [\\\"Some((None, None))\\\", … ]\"]" | `src/session.rs:1361-1364` |
| N3 | Note | The seat's 1% bound in the edited release assertion (item (a)) is about ten times looser than the (d3) bound: derived from the measured width differences it is 4 records; measured loss 2; 1% is 48. It hides nothing, because my release test asserts the derived bound. | `r5_release_width_bound_default_limits` (release) | TESTED: "own records 4808 with, 4810 without; lost 2; sum of width differences 1107 bytes; one tiny own record ~524 bytes; derived bound 4 records; seat's 1% bound 48" | `tests/gate_r4.rs:194` |
| N4 | Note | `docs/AUDIT.md`'s "room for requested events alone is at most 361,547 / 2,042" is true as an upper bound (362,063 − 516; 2,043 − 1). With the default policy and one request a minute, each event gets its own checkpoint, and events get 55% of the allowance bytes. | `r5_release_*` | TESTED: "2688 requests; all allowances (2532570, 5376), of which requested events (1415469, 2688) (55% of the bytes) and checkpoints (1117101, 2688)" | `docs/AUDIT.md` table row "held back in each allowance" |
| N5 | Note | I-A11 (the newest pays) lets one requester's events ride on another requester's checkpoint. The cost is bounded: a requester never pays more than one checkpoint per request of its own, and that room was held back when the request was accepted. | `r5_newest_pays_*` (asserts paid ≤ own requests) | TESTED: "A accepted 3 (allowance (1572, 3), checkpoints paid 0), H accepted 2 (allowance (1461, 3), checkpoints paid 1)" | `src/session.rs:644-647` |
| N6 | Note | The M11 red row (`no_lifetime_backstop`) is red on WHICH error comes back, not on a refusal going missing: after the roster merge the roster crate itself refuses version 257 (`TooManyVersions`). The audit backstop is now defence in depth. | seat's runner row M11 | TESTED: "M11: roster version 257 was not refused by the lifetime backstop / left: Err(Roster(TooManyVersions))" | `src/session.rs:1113` |
| N7 | Note | Mutants R05 (the record half of the I-A13 hold-back) and R22 (the entry bounds of `from_bytes`) are killed only by my tests, not the branch's. R17 (the anchor's "newest of a run Missing" check) survives everything, and I judge it equivalent in effect: a removal shortens the run (`Behind`), and a hole with later records is refused by `resume` itself. | mutation table | TESTED | `src/session.rs:834`; `src/anchor.rs:183`, `:191`, `:263` |
| N8 | Note | U6 keeps its name and now asserts that the cap is unreachable, as addendum 5 allowed. Its "at most 14,827 with every proposal field" uses the seat's own 1,024-byte-per-member margin, not a measurement. | read | READ | `tests/a3_unknowns.rs:183, 199-270` |
| N9 (known) | Note | `gate_r3::r3_release_flood_measurements` part (c), unedited and `#[ignore]`d (A3-Q2). | `cargo test --release --test gate_r3 -- --ignored` | TESTED: "panicked at crates/coagent-audit/tests/gate_r3.rs:407:18" | `tests/gate_r3.rs:407` |

No Blocker, no Major: GO WITH NOTES.

## 2. Rulings

**I-A11 (one checkpoint, one payer: the requester of the newest requested event it covers). SOUND.** One payer and never split; it is a function of the store keys (1,207 restarts in my property, each with identical charges, status and anchor: TESTED). Cost moves between requesters (N5), but is bounded by the hold-back. Mutant R01 (the oldest pays) is killed by the branch (`a5_m1_one_checkpoint_one_payer_the_newest_requester`, P10) and by mine.

**I-A12 (a checkpoint covering at least one requested event is paid that way; the free part pays only for one covering none). SOUND.** (d1) held at every step of 512 cases, checked against my own model of who pays, read from the store keys alone ("checkpoint paid by an allowance" 695, "paid by the free part" 742). Peers never caused more free-paid checkpoints than the same schedule without them (0 of 512 cases: TESTED).

**I-A13 (room for one checkpoint held back in the requester's allowance). SOUND as a guarantee against peers, at a stated cost.** After every accepted request the allowance kept room for 516 bytes and 1 record (1,206 accepted requests checked). No checkpoint was refused while the limits had never been lowered. Cost: at default limits 2,688 requests are accepted where 4,809 were before (TESTED: gate_r4 release, and mine). Its companion rule (c) is sound, but where the room is nevertheless missing it leads to R5-m1.

**I-A14 (anchor plus `resume_with_anchor`; plain `resume` unchanged and documented). SOUND.** In a 15-state progression (own and requested events, both kinds of own checkpoint, peer events and checkpoints, two countersignatures replacing each other, two cross-check records replacing each other, fork evidence, a roster version, a joiner's anchor):
- An anchor NEWER than the store was refused in 105 of 105 pairs ("Missing" 102, "Older" 3).
- An OLDER anchor was accepted in 105 of 105.
- Every one of the 14 records removed in turn was refused and named (part and key).
- Every fixed record with a flipped byte was refused (6 of 6). All TESTED.
- The bound holds: the largest encoding (522 runs, 540 slots, every number at its maximum) is 172,974 bytes, under the 524,288-byte limit. It reads back, and one run or one slot more is refused (TESTED).

Leaving plain `resume` as it is, with the gate's R4-m3 assertion unedited, is ACCEPTABLE. Its doc now says plainly what it does not detect. The daemon-lane request to restart only through `resume_with_anchor` is recorded in BACKLOG. The residual risk sits with the daemon lane: R4-m3 is reduced from Minor to a Note on that lane. The new code's untested checks are R5-m3.

**I-A15 ((d1), (d2), (d3) replace 07 §1.6 item 2). A REAL security property, not a weakening an attacker can use.** The withdrawn form failed only where V's own later records used room that a requester's payment left free: V benefits, the peer gains nothing. Across 512 cases:
- In 25 of them an own call was refused only in the run WITH peers, and every one of those 25 came after an own record that only the peers' run had accepted (0 without: TESTED).
- 119 own calls were accepted only with peers.
- (d2): 987 steps with no own call, free part (0, 0) at each.
- (d3) held for 3,141 own records stored in both runs; 423 were larger with peers, all within the width bound.

Two qualifications, neither a peer attack on the free part: the re-used slot (N1), where the seat cap rather than the free part decides; and (d3) itself. The binding form promises what the free part HOLDS, not that V is never refused; the docs should say so where they say "whole free part" (N1).

**Gate-file edits** (diff against `gate_audit_tests_r4/gate_r4.rs`, sha256 `75e63652…`, and `git diff 52d12e9 HEAD`; READ and TESTED):

| file, test | change | ruling | marked, old quoted | not weaker | my ruling |
|---|---|---|---|---|---|
| `gate_attacks.rs:88` | marker text only ("RULING REQUESTED" → "RULING (Friday, 2026-11-18, addendum 5)") | A5 §2 A1 | yes | no code changed | ACCEPT |
| `gate_r2.rs:650` | marker text only; the positive form `r1 Ok` is asserted in `a5_guards::ruling_a5_a_v1_head_countersignature_before_any_newer_one_is_accepted` (passes in check.sh) | A5 §2 A2 | yes | no code changed | ACCEPT |
| `gate_r3.rs` | no change since 52d12e9; sha256 `c1726e9d…` = the seat's | — | — | — | — |
| `gate_r4.rs` R4-M1 debug (old 160-163) | `free_with == 0 && own_with == own_without` | A5 §2 B, A6 §2 | yes | exact; stronger than "not shown" | ACCEPT |
| `gate_r4.rs` R4-M1 release (old 187) | `free_with == 0 && own_with <= own_without && lost*100 <= own_without` | same | yes | loose bound (N3), but `free_with == 0` is exact | ACCEPT (item (a)) |
| `gate_r4.rs` R4-m1 ×2 (old 260-267, 320-323) | assert the fixed property exactly | A5 §2 B | yes | yes | ACCEPT |
| `gate_r4.rs` R4-m2 (old 382-385) | seat 2 within one seat, bytes and records | A5 §2 B | yes | yes | ACCEPT |
| `gate_r4.rs` guard M23 (old 1707, 1714) | two lines: no closing checkpoint; V lowers its limits instead of a request | A6 §2 | yes | final `assert_eq!(c2, Err(LogFull))` unchanged; under `own_cp_unchecked` RED on "left: Ok(())" (seat's runner row, TESTED) | ACCEPT (item (b)); its doc comment and `eprintln!` labels now describe the old setup (cosmetic) |
| `gate_r4.rs` R4-m3 (old 1534, now 1558) | unchanged | A5 §2 B | — | — | ACCEPT (item (c)) |

Nothing else differs in any gate file. sha256 (TESTED): gate_attacks `6ef41612…`, gate_r2 `adca67f3…`, gate_r3 `c1726e9d…`, gate_r4 `8b7ac445…`, all equal to the seat's report.

**The seat's items.**
- (a) The 1% bound: ACCEPT. Justified, but loose by a factor of about ten (N3).
- (b) The guard edit: ACCEPT. It still goes red without the space check.
- (c) `r4_damaged_store_*` left unedited: ACCEPT.
- (d) `apply_roster` and `join_author` made store-first: ACCEPT for `join_author`. For `apply_roster`, R5-m2: store-first before validation creates a new way to leave a bad record behind.
- (e) The two lifetime bounds count different things, but neither side accepts what the other refuses: NOT REFUTED. The roster crate keeps the `removed` list append-only and requires a disappearing member to be listed (`coagent-roster/src/lib.rs:16-17, 886-907`). So every key ever (`keys_ever` = members of any held version) is an entry of the latest version: distinct keys ≤ entries. The version bounds are both "> 256". The audit backstop can only fire where the roster refuses too (READ). N6 is the other face of this.
- (f) The cost of I-A13: REPRODUCED. 2,688 requests; 2,532,570 bytes in allowances; 361,547 / 2,042 is right as arithmetic and as an upper bound (N4).

## 3. Mutation (my driver `mutate_r5.py`; one mutant at a time; whole `coagent-audit` suite `--no-fail-fast` plus `gate_r5`; `mutation_r5_summary.txt`, logs in the working folder)

| id | rule | result (branch tests failing / gate_r5 failing) |
|---|---|---|
| R01 | I-A11 newest pays (→ oldest) | KILLED 2 / 2 |
| R02 | coverage after the previous own checkpoint (→ from 1) | KILLED 5 / 2 |
| R03 | coverage excludes the previous checkpoint's event (→ prev..=n) | KILLED 3 / 2 |
| R04 | I-A13 hold-back, bytes | KILLED 1 / 1 |
| R05 | I-A13 hold-back, records | KILLED 0 / 1 (mine only, N7) |
| R06 | an allowance-paid checkpoint uses the held room (→ asks a second hold-back) | KILLED 4 / 2 |
| R07 | rule (c), never the free part instead (→ free part as fallback) | KILLED 1 / 2 |
| R08 | room asked of the paying part (→ always the free part) | KILLED 1 / 2 |
| R09 | R4-m1 own record order | KILLED 2 / 1 |
| R10 | R4-m1 own checkpoint order | KILLED 1 / 1 |
| R11 | R4-m1 received event order | KILLED 2 / 1 |
| R12 | R4-m1 joiner's anchor order | KILLED 1 / 1 |
| R13 | R4-m1 countersignature put back | KILLED 1 / 1 |
| R14 | R4-m1 roster version order | KILLED 1 / 2 |
| R15 | a refused newer roster version removed again | KILLED 4 / 0 |
| R16 | anchor: shorter run `Behind` | KILLED 1 / 1 |
| R17 | anchor: newest of a run `Missing` | SURVIVED (equivalent in effect, N7) |
| R18 | anchor: replaced slot strictly newer (→ >=) | SURVIVED both suites; my guard KILLS it (R5-m3) |
| R19 | anchor: older replaced slot refused (→ any different order) | KILLED 1 / 1 |
| R20 | anchor: session checked | KILLED 1 / 0 |
| R21 | `anchor()` run count | KILLED 1 / 1 |
| R22 | `from_bytes` entry bounds | KILLED 0 / 1 (mine only, N7) |
| R23 | `from_bytes` byte bound | SURVIVED both suites; my guard KILLS it (R5-m3) |
| R24 | `restore_countersig` puts the earlier one back | KILLED 1 / 1 |
| R25 | anchor digests kept on write | KILLED 2 / 2 |
| R26 | anchor digests dropped on delete | SURVIVED both suites; my guard KILLS it (R5-m3) |
| R27 | R4-m2 seat check keeps the part's hold-back | KILLED 1 / 0 |

23 of 27 killed by the two suites; 21 by the branch alone. Surviving: R17 (equivalent) and R18, R23, R26 (R5-m3; my guards kill each: `guards_vs_mutants.txt`).

**My own tests red once each** (TESTED, `red_controls_on_r5_tests.txt`; the builder's cfg controls at 64 cases):
- `requested_cp_on_free`: the property on "(d1) step 11: free_usage (5131, 10) != model (4717, 9)"; the block test "left: Ok(()) right: Err(LogFull)".
- `requested_no_holdback`: the property on "I-A13: request 1 of slot 0 accepted without room for its checkpoint: (524, 1) of (528, 1)".
- `commit_before_write`: "own record: the member changed although the write failed: [\"own seq: 0 -> 1\"]"; R5-m2 on "not shown: nothing left behind".
- `own_seat_overfill`: N1's test on "not shown".
- `anchor_not_checked`: "anchor at 'own event' accepted the older store at 'start'".
- `own_cp_unchecked`: the property on "step 12: free part grew to (2580, 2) above its limit".
- My plain mutants also kill them (table above).

## 4. Reproduced

| seat's claim | mine (TESTED) |
|---|---|
| `check.sh` at 5f4577c: exit 0, "CHECK OK", 650 / 0 / 17 | exit 0, "CHECK OK: fmt, clippy, test, deny all passed", 650 passed / 0 failed / 17 ignored (`check_sh_tail.txt`) |
| `red-controls-audit.sh`: 149 rows, 149 RED, "GREEN: 207 tests ok", "RED CONTROLS OK" | rows: 149; 149 RED, 0 NOT-RED; "GREEN: 207 tests ok"; "RED CONTROLS OK: every guard went red under its control, on its property, and green without"; exit 0 (`red_audit.log`) |
| `red-controls-core.sh`: 65 rows, "GREEN: 220", "RED CONTROLS OK" | rows: 65; 0 NOT-RED; "GREEN: 220 tests ok"; "RED CONTROLS OK"; exit 0 (`red_core.log`) |
| rows red for the RIGHT reason (sampled) | 22 rows read against their rule: the 16 of addendum 5, the four the seat repaired, and two more on P2 and P8. Each is red on its own property's text, for example `free_records_unreserved` "P1(c): an own free record of 826 bytes was refused LogFull although …", `shared_peer_pool` "P2: seat 6's charges or LogFull refusals depend on other seats' inputs", `cs_rule_current_only` "countersigner not a member at that roster version", `own_seat_too_large` "P7: event 9 … was refused by an honest peer with equal limits: LogFull". One qualification: N6 |
| gate files release `--ignored`: 2/2, 3/3, gate_r3 1 of 2 (N9), gate_r4 1/1 "2688 … free part used 0 … 4808 against 4810" | identical: gate 2/2; gate_r2 3/3; gate_r3 1 of 2, panic at gate_r3.rs:407:18; gate_r4 "2688 requested events (2532570 bytes in allowances) … free part used 0 bytes (0.0%) … own records then possible 4808, against 4810" (`rel_gates.txt`) |
| (a) gate input, free part stays 0 | REPRODUCED (above, and `r5_release_*`: "free part before own records 0") |
| merge 3709ef8 = parents ba187c1 + da4655e; ancestor check exit 0 | `git log -1 --format='%H %P' 3709ef8` → "3709ef8f… ba187c1f… da4655ed…"; `merge-base --is-ancestor da4655e HEAD` → 0 |
| diff vs main: 59 files, only the named places; identity.rs = c407fe7 exactly | `git diff --stat da4655e HEAD`: 59 files, 23,273 insertions. Outside `crates/coagent-audit/`: BACKLOG.md, Cargo.lock, Cargo.toml (adds the crate to the workspace), crates/coagent-crypto/src/identity.rs, docs/AUDIT.md, docs/CRYPTO-GLUE.md, scripts/red-controls-audit.sh. The identity.rs diff against main and c407fe7's diff have the same sha1 of +/- lines (`bb940a8f…`). No diff at all in coagent-proto, coagent-roster, coagent-relay, coagent-cli |
| BACKLOG union | `git diff --numstat da4655e HEAD -- BACKLOG.md` → 110 added, 0 deleted; `ba187c1 HEAD` → 74 added, 0 deleted: both sides kept whole |
| `git ls-remote origin m3-audit` = 5f4577c | not run (no network); the project repo's `m3-audit` cloned at 5f4577c and its `refs/remotes/origin/main` = da4655e (TESTED locally) |
| name scan: no person's name or home path | case-insensitive scan of the 23,332 added lines of `git diff da4655e...HEAD` for the owner's first name, full first name and surname, the account name, the machine name, `/users/`, `/home/`, `/volumes`, drive names and client names: 0 hits for any person, machine, drive or home path (positive control "audit": 1,700). Remaining hits: `/users/` 1, an `example.com/users/@alice` test string (`tests/gate_r2.rs:688`); `.local` 23, all `self.local`; "Friday" 29, the coordinator seat's name in ruling markers, a role and not a person. Report: none |

Note on refs: in my clone `origin/main` is the project's LOCAL `main` (18005d6, stale); every comparison above uses `da4655e` by SHA.

## 5. Docs (`docs/AUDIT.md`), against the code

| sentence (quoted) | verdict |
|---|---|
| (d1) "every record in the free part is an own-choice event of V … or an own checkpoint that covers no event recorded at a peer's request … a checkpoint covering one is paid by the allowance of the NEWEST such event's requester, whole" | TRUE (property, 512 cases) |
| (d2) "if V makes no own-choice call and no explicit own checkpoint call, the free part is empty (0 bytes, 0 records), whatever peers do" | TRUE (987 steps), and true even with explicit checkpoint calls that cover only requests |
| (d3) "… larger … by at most the difference in decimal width of the two sequence numbers … measured: 939 against 937 bytes" | TRUE (3,141 records checked; `withdrawn_d_cause1_*` passes in check.sh) |
| "seven requested allowances … each paying for its requested events AND the own checkpoints that cover them" | TRUE |
| "so the room for requested events alone is at most 361,547 each / 2,042 each" | TRUE as an upper bound (N4: 55% at one request a minute) |
| "V's own checkpoint covering an event recorded at G's request … `LogFull` if the room is nevertheless missing (e.g. V lowered its limits); never the free part" | TRUE but INCOMPLETE: it does not say that every later checkpoint is then refused too (R5-m1) |
| "with all seven hostile V still has its whole free part (nothing they cause is charged to it, (d1))" | TRUE for the free part's content; not true in the re-used slot state (N1) |
| "written to the store FIRST and applied after, so a store write that fails leaves the member exactly as before the call" | TRUE for put failures, with two qualifications: an empty received chain (N2), and a refused roster version with a failing remove (R5-m2) |
| "`resume` … does NOT detect a store missing WHOLE records … `resume_with_anchor` refuses any store holding less than the anchor says … a store ahead of the anchor … is accepted … At most 522 runs and 540 slots … at most 512 KiB … take a new anchor after `archive_and_release`" | TRUE (section 2, I-A14) |
| U6: "the largest one's record is 6,635 bytes, at most 14,827 with every proposal field" | 6,635 TESTED by the seat's test in check.sh; 14,827 rests on an own margin (N8) |

## 6. NOT TESTED

- `git ls-remote` (no network). Linux/Windows. A real daemon store or crash timing: R5-m2 is shown with a failing `remove` only.
- R5-m1 with any trigger other than V lowering its limits. I found none, and the property generated slot changes (51), removals (647) and restarts (1,207) without one. A different, untested trigger cannot be excluded.
- Removal and re-adding of V ITSELF inside the property (only the dedicated N1 test covers it). The slot-0 fallback while V is off the roster (A5-Q1) was read only.
- The full earlier-gate campaigns; this check covered the delta only. `archive_and_release` all-or-nothing (deferred by the seat, BACKLOG).
- Timing: another gate's builds ran on this laptop; no timing-sensitive test failed.

## 7. Commands to re-run (from the working folder; `env.sh` = shared cargo home, the project's `tools/rustup` read-only, own target dirs)

```
bash fetch.sh                       # cargo fetch --locked; build
bash run_check.sh                   # check.sh in clone -> check.log
bash run_red.sh                     # red-controls-audit.sh then red-controls-core.sh -> red_audit.log, red_core.log (COAGENT_TOOLS = scratch)
bash run_atk.sh -- --nocapture      # gate_r5 debug (R5_CASES=96 default; 512 used for the figures)
bash run_atk.sh --release r5_release -- --ignored --nocapture
bash run_rel_gates.sh               # the four gate files, release --ignored
bash run_red_r5.sh                  # gate_r5 under the builder's red controls
bash run_mut.sh; python3 out/mutsummary_r5.py mut/mutlogs out.txt     # 27 mutants (copies mut/mut1..3 with gate_r5 registered)
bash out/guards_vs_mutants.sh       # my anchor guards under R17, R18, R23, R26
```
