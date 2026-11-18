VERDICT: GO WITH NOTES — head 393e7e45794b54793c08fa3c8eaf55b10abb2da7

# QA gate M3-AUDIT-FIX (tier 1, the one short check of the fix round): `coagent-audit`, branch `m3-audit-fix`

Independent gate, 2026-11-18. Findings only. Nothing was fixed, committed, merged or pushed, and nothing was written in the project folder. The clone's `git rev-parse HEAD` is `393e7e45794b54793c08fa3c8eaf55b10abb2da7`, the head under test (TESTED). Main is taken as given: `c9a66534600e47fdd4a8da913df79d220086340b`. I did not read the remote (no `git ls-remote`, no credentials). `git merge-base --is-ancestor c9a6653 HEAD` gives exit 0, and HEAD is two commits on top of main (`6c0a1a4`, then `393e7e4`), so the branch merges onto that main as a fast-forward (TESTED locally).

My tests, driver and short logs are in `m1_review/gate_audit_fix_tests/`. To use them, drop `qa_fix.rs` into `crates/coagent-audit/tests/` and add `[[test]] name = "qa_fix"`.

Every figure below is marked TESTED (I ran it) or READ (I read it). The builder's figures are quoted as the builder's.

## BLUF (for the owner, in plain words)

1. **The roster fault (R5-m2) is fixed.** A member-list update that the product refuses (forged, unsigned, out of order, stale, a different copy of an existing one) is no longer written to disk at all. So it can no longer break restart or export:
   - Across 40 generated sessions (about 2,000 updates, with the disk failing writes, failing deletes or stopping for good at random points), the disk never held a refused version.
   - Restart, restart-with-anchor and export worked after every single step.
   - The product's answer always equalled the member-list library's own answer.
2. **The witnessing fault (R5-m1) is fixed for the case that was found, but not in every case.** In the case found, lowering your limits could leave a requester's allowance without room, so later actions were never witnessed. That lowering is now refused. Your limits stay as they were, and every checkpoint goes through (TESTED).
3. **The same effect can still be reached by a different route (new Minor, QA-m1).**
   - If you lower your limits so that your OWN seat, as a whole, is smaller than what it already holds, the new rule still accepts the change. It looks only at the allowance that owes a checkpoint, and that allowance still has room.
   - Every later checkpoint is then refused, including the one covering another member's request. Your log keeps a record nobody is witnessing until you raise the limits again or restart.
   - I showed this with no re-add and with your own free space empty: 10 of 10 checkpoints were refused, the payer had room, and raising the limits back let the next checkpoint through.
   - A peer cannot cause it alone, because it needs your own limit change. So it is a Minor, the same grade as R5-m1 itself. But the docs and BACKLOG say the only remaining case is a re-used slot, and that is not true.
4. The three permitted edits to the earlier gate's test file are exactly the ones ruled, each marked, and none of them is weaker. The four other gate files are byte-identical to main (TESTED by sha256).
5. Reproduced:
   - `check.sh`: exit 0, 879 passed / 0 failed / 18 ignored.
   - Audit red runner: 152 RED / 0 NOT-RED, GREEN 238.
   - Core red runner: 65 rows, GREEN 220.
   - All three equal the builder's figures (TESTED).
6. Mutation: the branch's own tests kill 18 of my 20 mutants. The remaining two are equivalent (written reasons in section 4).
7. **My recommendation: GO WITH NOTES.** Merge. You asked for both faults to be "fixed before the beta". Before then, decide whether rule (A) should also refuse a lowering that leaves the own seat smaller than what it holds (QA-m1), and have the docs sentence corrected either way.

## 1. Findings

| id | sev | what | input that shows it | exact output seen | file:line |
|---|---|---|---|---|---|
| **QA-m1** | Minor | **Rule (A) does not cover the own-seat cap, so a lowering it accepts still blocks witnessing for good.** `checkpoint_now` asks `own_room` for room. For a checkpoint paid by an allowance, `own_room` checks that allowance (rule (A) protects it) AND the seat of the member's own slot (the R4-m2 check, `session.rs:947-955`, closing reserve 0). Rule (A) looks only at owing allowances. A lowering can leave the own seat holding more than one seat while the payer allowance still has room. Every checkpoint is then refused `LogFull`, the requester's event and the member's later events are never witnessed, and the member's own records are refused too. It lasts until the owner raises the limits or restarts (the defaults come back). This is R5-m1's effect under the seat's name. It needs no re-add (contrary to STATUS Q1 and the new BACKLOG entry) and no free-part involvement (contrary to Friday's premise that a free-part-only lowering touches only own-only checkpoints). `docs/AUDIT.md` R5-m1 entry, "What remains, stated", names only "its free part unable to pay for a checkpoint covering only its own events" and the charging-table row names only "the seat cap of a re-used slot": both false by omission in this state. A peer alone cannot cause it. | `qa_finding_lowering_accepted_by_rule_a_blocks_an_allowance_paid_checkpoint_seat_records`: limits seat (64 KiB, 512); six requesters fill their allowances, each covered by a checkpoint they pay; H requests once; V has made no own record; V lowers the record limit to 49 per seat. Also `…_seat_bytes`: V fills its free part, H requests once, V lowers bytes. | TESTED: "G accepted 42, its checkpoint [Ok(7), Ok(14), Ok(21), Ok(28), Ok(35), Ok(42)]; H's allowance (525, 1); V's seat (25049, 49); lowering to StoreLimits { bytes: 524288, records: 392 } (allowance (4677, 3), seat (65536, 49)): try_set_limits Ok(()); then 10 checkpoints: 0 Ok, 10 refused LogFull; payer slot Some(3) usage (525, 1) of allowance (4677, 3) (room: true); newest covered Some(42) …; free part (0, 0); own record Err(LogFull); raising back Ok(()), checkpoint then Ok(43)". Bytes variant: "lowering to … (allowance (2281, 36), seat (32447, 512)): Ok(()); 5 checkpoints [Err(LogFull) ×5]; payer Some(3), room true" | `src/session.rs:584-596` (rule (A)), `:947-955` (own-seat check), `:1465-1469`; `docs/AUDIT.md` R5-m1 entry and charging row; `BACKLOG.md` new "N1's state" entry |
| QA-n1 | Note | `docs/AUDIT.md` "Changing the limits" says "An allowance whose events are all covered may be lowered to exactly its usage". In fact it may be lowered to ANY value, far below its usage: the rule does not look at it. Friday's scoping intended this (an allowance owing nothing is not checked), so the code is as ruled. The doc sentence understates it, and it is how QA-m1's seat over-fill arises. | QA-m1 records input | TESTED: allowances at ~(4,6xx, 7) records accepted under a new allowance of (4677, 3) | `docs/AUDIT.md` "Changing the limits" |
| QA-n2 | Note | After `resume` the limits are the defaults. A lowering that rule (A) refuses (through `set_limits`) leaves the member at the DEFAULT limits, which are higher than the owner intended, and says nothing. The BACKLOG daemon-lane entry the brief asked for states exactly this. | `qa_ok_rule_a_edges_*` | TESTED: "after resume: no call StoreLimits { bytes: 40779920, records: 228832 }; same Ok(()); much lower Err(LogFull) (limits then StoreLimits { bytes: 40779920, records: 228832 })" | `BACKLOG.md` new daemon entry |
| QA-n3 | Note | The two retired M11 runner rows: nothing in the runner guards the audit's own lifetime backstops now. Two branch tests in `check.sh` still go red when the backstop is removed (mutant M15). The rule "no store call for a refused version" holds without the backstops (the roster crate refuses 257 first). Retirement accepted. | mutant M15 | TESTED: killed by `gate_r4::r4_guard_roster_lifetime_backstops`, `m11_the_roster_lifetime_backstops_refuse_version_257_and_a_33rd_key`; my bound test "257 Err(RosterLifetime) with 0 store calls" | `scripts/red-controls-audit.sh` (retired rows), `src/session.rs:1201-1205` |
| QA-n4 | Note | The R5-m1 gate test's `eprintln!` still prints the test's own variable `low` as if applied ("V lowers its records to 26 … free part … of (8179, 13)") although the member refused it. Cosmetic; the builder says so in STATUS. | `gate_r5` R5-m1 finding test | READ (STATUS §4 item 2) | `tests/gate_r5.rs:638-647` |
| QA-n5 | Note | Memory cost of the second chain: `roster_versions` and the check chain each hold up to 256 versions of at most 65,539 bytes. That is about 33.5 MB extra in the worst case beyond the roster crate's own copy, and about 7.6 MB at the largest realistic version (the 14,827-byte figure of U6). Bounded by the backstop. | read | READ | `src/session.rs:180-182` |
| QA-n6 | Note | Mutants M18 and M19 survive every test. Both are equivalent (reasons in section 4). | mutation | TESTED | `src/session.rs:1281-1284`, `:1226` |

No Blocker, no Major. One Minor (QA-m1), six Notes.

## 2. What I reproduced (TESTED unless marked)

| claim (builder, STATUS) | mine |
|---|---|
| `check.sh`: exit 0, "CHECK OK", 879 / 0 / 18 | exit 0; "CHECK OK: fmt, clippy, test, deny all passed"; summed 879 passed / 0 failed / 18 ignored; warning "unused workspace dependency `rand_core`" as before (`check_sh_tail.txt`) |
| `red-controls-audit.sh`: 150 cfg + 2 source-mutant rows, 152 RED, 0 NOT-RED, GREEN 238, "RED CONTROLS OK" | identical, exit 0 (`red_audit_tail.txt`, `red_audit_rows.txt`, 152 rows). The new rows are red on their own property text. `roster_store_first`: "R5-m2 property: step 0 (Forged, store mode 2): the store holds roster version 2, which the roster crate refuses in order: Err(BadSignature)". `limits_strand_payer`: "R5-m1 property: step 24: a policy checkpoint was refused LogFull because its payer, the allowance of slot 0, lacks room …". `own_cp_unchecked` is red on the unedited `gate_r4::r4_guard_an_own_checkpoint_is_space_checked` ("left: Ok(())") and on `m23_*` ("M23: an own checkpoint with no room in the free part was not refused"). `requested_cp_on_free` is red on the rewritten P10 ("P10 (d1): step 9: a checkpoint covering a request of slot 0 was not charged to that allowance.") |
| `red-controls-core.sh`: 65 rows, GREEN 220, "RED CONTROLS OK" | identical: "rows: 65", 0 NOT-RED, "GREEN: 220 tests ok", exit 0 (`red_core_tail.txt`) |
| `r4_guard_an_own_checkpoint_is_space_checked` green and unedited | `gate_r4.rs` sha256 `addc9f79…` equals main; green in check.sh and in my whole-suite run |
| gate files release `--ignored` (builder: gate 2/2, r2 3/3, r3 1 of 2 N9, r4 1/1, r5 1/1) | NOT run by me (section 6) |

## 3. Scope, public surface, gate files (B)

- **`git diff --stat c9a6653 HEAD`** (TESTED): 11 files, +2,648 / −102. Files: `BACKLOG.md`, `crates/coagent-audit/{Cargo.toml, build.rs, src/session.rs, tests/a5_requester_pays.rs, tests/fix_notes_pinned.rs, tests/fix_r5m1_limits.rs, tests/fix_r5m2_roster_check_first.rs, tests/gate_r5.rs}`, `docs/AUDIT.md`, `scripts/red-controls-audit.sh`. Nothing else: no `Cargo.lock`, no other crate.
- **Public surface** (TESTED: sorted `pub` lines of every `src` file, main against head): only `session.rs` differs. The one added item is `pub fn try_set_limits(&mut self, limits: StoreLimits) -> Result<(), AuditError>`, and `pub fn set_limits(&mut self, limits: StoreLimits)` is unchanged. The three new fields are private.
- **sha256, main against head** (TESTED, all SAME):
  - `gate.rs` `d6a29f1e…`
  - `gate_attacks.rs` `6ef41612…`
  - `gate_r2.rs` `adca67f3…`
  - `gate_r3.rs` `c1726e9d…`
  - `gate_r4.rs` `addc9f79…`
  - the four wrappers
  - `gate_return*.rs`
- **`gate_r5.rs`** goes from `245e35e0…` (= the r5 gate's file) to `d16e82d5…` (TESTED). I read its diff line by line. The changed lines are exactly the three ruled edits, each under a `// RULING (Friday, 2026-11-18, audit-fix brief; …)` marker with the old line(s) quoted.

| edit | old | new | my ruling |
|---|---|---|---|
| R5-m2, old line 1041 | `assert!(after > before, "not shown: nothing left behind")` | `assert!(after == before && res.is_ok() && res2.is_ok() && next_ok.is_ok() && exp.is_ok(), …)` | ACCEPT. Asserts exactly the four things ruled. It compares record counts, not contents, and does not assert that the answer is `Roster(Gap)`; the builder's `r5m2_gate_input_*` and my property assert the answer. Stronger than "not shown". |
| R5-m1, old lines 641-645 | `assert_eq!(cp0, Err(LogFull))` and `own_ok > 0 && cp_refused == 20 && cp_ok == 0 && covered.is_none()` | `assert_eq!(cp0, Ok(()))` and `cp_refused == 0 && cp_ok == 20 && covered == Some(v.own().seq())` | ACCEPT. Exactly the fixed property for that input (the first checkpoint Ok, none refused, newest own event covered). |
| R5-m1 property, `r5_prop_peers_request` | (a) the reach count "checkpoint refused: its allowance cannot pay (after Lower)" required > 0; (b) `v.set_limits(lim);` at old lines 377 and 401 | (a) removed from the must-reach list, then `assert_eq!(…, 0, …)`; (b) `v.set_limits(lim); lim = v.limits();` | ACCEPT. Only (a) and (b). The generator and every other assertion are byte for byte. Line 206 (new session) is untouched, which is correct: a new session owes nothing (my edge test, and the builder's). The == 0 assertion is stronger than the old line. Because this count is bumped for ANY `LogFull` with a payer after a lowering, it would also catch QA-m1's state if the generator reached it (it did not; my mutant M01 shows the property goes red without rule (A)). |

## 4. Rulings

**Friday: rule (A) is the whole rule, with no free-part clause. SOUND for what it targets, INCOMPLETE for what it is for.**
- It closes the measured R5-m1 exactly:
  - The gate input is refused.
  - Exact boundary: allowance exactly (1564, 36) → `Ok(())`, one seat byte less (1563, 36) → `Err(LogFull)`.
  - 279 limit changes in steps down, up, down, zero, `usize::MAX` and `bytes: 1`: 216 accepted, 63 refused. After each accepted change every owing allowance kept room; after each refused one the limits were unchanged.
  - In 40 generated sessions (with V removed 36 times and re-added 22 times, slot-0 fallback, 164 resumes with none / same / lower / different limits) no checkpoint was refused because its payer lacked room.
  - All of the above TESTED.
- Its premise was "the free part keeps its closing reserve and its own space check; a lowering that leaves the free part unable to pay affects only own-only checkpoints". That premise does not hold. The own-seat check of R4-m2 applies to allowance-paid checkpoints too, so a lowering can block them (QA-m1).
- No second rule is invented here (the brief forbids it). The owner's options are a seat clause in rule (A), or accepting the state and correcting the docs. The free-part behaviour itself is unchanged as ruled: the r4 guard is green and unedited, and its runner rows are red.

**Friday: `LogFull` reused, no new variant. SOUND.** A caller cannot tell "refused by the rule" from "log full" by the error alone, but `limits()` reads back what is in force, and the doc says so.

**Friday: `set_limits` = `try_set_limits` with the result dropped. SOUND as built.**
- The body is exactly `let _ = self.try_set_limits(limits);` (READ).
- Mutant M09 (bypass) is killed by `r5m1_set_limits_is_try_set_limits_with_the_answer_dropped` and four others (TESTED).
- I found no invariant elsewhere in the crate that assumes a `set_limits` took effect. Every reader uses `self.limits`. The one assumption that existed was in the gate property's model, and it is fixed by edit (b).
- The residual risk is QA-n2 (defaults after resume), which BACKLOG states.

**The builder's choice for R5-m2 (second roster chain rebuilt from held versions). SOUND.**
- `RosterChain::apply_with_report` assigns state only on success (`coagent-roster/src/lib.rs:871-872`; a `Fork` mutates nothing). So the check chain and the member's chain are both a function of the sequence of applied versions, and `roster_versions` is that sequence (READ).
- My attacks on agreement all agree with the roster crate's own answer computed from what is STORED:
  - after resume (361 resumes inside the property)
  - after refused versions of every kind
  - after a failed write
  - after removal and add
  - at the 256-version bound, where a failed write at 256 forces a rebuild from 255, then 256 is accepted by both the member and a resumed member, and 257 is refused with 0 store calls
- Reach in my property: next accepted 273, next with store failed 225, forged 161, unsigned 166, gap 181, out of order 206, broken chain 173, stale 98 (64 more "stale" draws equal to the current version, `Unchanged`), duplicate 152, fork 128 (store failed 27) (TESTED).
- Cost bound: at most 256 versions, enforced by the lifetime backstop before any check. The rebuild runs only after a failed write or on the first newer version after start/resume. Builder's measurement, READ: 0.36 s debug for the rebuild.
- Memory: QA-n5.

**`join_author`, `commit_own`, `checkpoint_now`. The builder's sentences are TRUE.**
- `join_author` does every check before its one write. TESTED: other session, non-member, own anchor each refused with 0 store calls; a good anchor is 1 call; a duplicate is 0 calls.
- `commit_own`: `AuthorChain::commit` checks exactly author, session, `seq + 1` and `prev_hash`, which `prepare` set from the same unchanged state (READ, `chain.rs:233-246`).
- `checkpoint_now`: `commit_head` checks `author_seq == seq`, `hash == last_hash`, and that the last checkpoint is below, which `prepare_head` guaranteed when it returned `new = true` (READ, `chain.rs:398-440`).
- So their delete-if-refused branches are unreachable in the normal build.

**The two retired M11 rows. ACCEPT** (QA-n3).

**The retired source-mutant row `mut_deleted_digest_kept` (R26). ACCEPT as equivalent.** `delete` has four call sites (READ: `session.rs:1142, 1241, 1483, 1892`):
- 1241 is under the red control `roster_store_first`.
- 1142 and 1483 are numbered own keys.
- 1892 deletes only `PeerEvent` / `PeerHead` keys.

No fixed-part key reaches `delete` in the normal build.

**Q2, the conflict-slot write for a refused `Fork`. ACCEPT.** It is design 07's evidence. It is only ever a starter-signed version (validated before `Fork` is raised), it is never among the roster versions, and restart and export accepted it in every step of my property.

### Mutation (E)

My driver is `mutate_fix.py`. One mutant at a time goes into `src/session.rs` of a scratch copy, and the whole `coagent-audit` suite runs with `--no-fail-fast`, including my `qa_fix` at `QA_FIX_CASES=15`. Results are in `mutation_summary.txt` and `mutation_qa_texts.txt` (TESTED).

At 15 cases my generated R5-m1 property never reaches "limit change refused" and fails on that reach text whatever the mutant. Such failures are NOT counted as kills below. Only failures on a property text count.

| id | mutant | branch tests failing | my tests killing (property text) |
|---|---|---|---|
| M01 | rule (A) removed | 8 (incl. gate_r5 finding + property, r5m1_*) | edges ("owing allowance of slot 2 at (1048, 2) has no room …"), prop ("checkpoint refused because its payer slot 5 lacks room") |
| M02 | bytes `>` → `>=` | 1 (exact boundary) | edges |
| M03 | records `>` → `>=` | 5 | none (only the spurious reach) |
| M04 | bytes clause dropped | 5 | edges, prop |
| M05 | records clause dropped | 7 | none counted |
| M06 | owing range includes the last checkpoint's number | 7 | none counted |
| M07 | every allowance treated as owing | 7 | none counted |
| M08 | rule asks the OLD limits | 7 | edges, prop |
| M09 | `set_limits` bypasses the rule | 5 | none counted |
| M10 | hold-back one byte short | 1 (exact boundary) | edges |
| M11 | store before check (no delete) | 11 (incl. gate_r5 R5-m2 finding) | R5-m2 prop ("forged refused by the roster crate … but answered Store(…)") |
| M12 | old chain not brought level after the swap | 36 | R5-m2 prop, bound test, R5-m1 prop |
| M13 | rebuild skips a held version | 9 | R5-m2 prop ("out of order … answered differently …"), bound test |
| M14 | accepted version not recorded among held versions | 3 | R5-m2 prop, bound test |
| M15 | lifetime backstops removed | 2 (QA-n3) | none counted |
| M16 | roster refusal mapped to `LogFull` | 6 | R5-m2 prop |
| M17 | failed write keeps the one-ahead check chain | 5 | R5-m2 prop ("out of order (mode 0) answered differently") |
| M18 | refused path drops the check chain | 0 | 0: **EQUIVALENT**. A refused version leaves the chain unchanged, so dropping it only forces a rebuild from `roster_versions`, which gives the same state. Performance only. |
| M19 | held current number routed through the check chain (`>` → `>=`) | 0 | 0: **EQUIVALENT**. For a version at or below the current one the check chain answers `Unchanged` / `Stale` / `Fork` without changing. `Ok(Unchanged)` restores it, and `Fork` goes to the same `roster_refused` (conflict write unchanged). Answers and writes are identical. |
| M20 | swap before write in `apply_newer` | 4 | R5-m2 prop ("member and store disagree") |

Totals: 18 of 20 killed by the branch's own tests. Of those 18, my tests also kill 12 on a property text (M01, M02, M04, M08, M10, M11, M12, M13, M14, M16, M17, M20). No mutant is killed only by mine. Survivors: M18, M19, both equivalent with the written reasons above.

## 5. Docs and backlog (F, READ against the code and my tests)

- "A newer roster version is checked, then stored, then applied …": TRUE (property, bound test).
- "One qualification (gate r5 N2)": TRUE.
- "Changing the limits … the rule, whole …": TRUE. Two exceptions:
  - "may be lowered to exactly its usage" understates (QA-n1).
  - Saying nothing about the own seat leaves QA-m1 unstated.
- The R5-m1 entry, "What remains, stated: … its free part unable to pay for a checkpoint covering only its own events …": INCOMPLETE (QA-m1).
- Charging-table row: "No limit change can take that room away": TRUE of the allowance's room. "a checkpoint can still be refused … by the seat cap of a re-used slot": TRUE, but not the only case (QA-m1).
- "Restart" addition ("limits that were in force when the store was written are always taken again"): TRUE in my edge test ("same Ok(())"). The builder's 24-case property is READ.
- BACKLOG:
  - R5-m1 and R5-m2 are kept, marked `- [x] … — CLOSED in commit 6c0a1a4 …` with the tests and red rows, original sentence unchanged, nothing deleted (TESTED by diff: lines changed in place, none removed).
  - The gate r4 N4 sentence is corrected.
  - The daemon-lane entry ("after `resume` the limits are the defaults, and a `set_limits` the rule refuses leaves them there") is present.
  - The new "N1's state" entry attributes the seat-cap block to a re-add only; QA-m1 shows it is wider.

## 6. Hygiene (G, TESTED)

- Case-insensitive scan of the 2,648 added lines of `git diff c9a6653 HEAD` gave 0 hits each for:
  - the owner's short first name, full first name and surname
  - the account name and the machine's host and computer names (read from the system)
  - the email domain and mail host
  - the drive name and "laptop"
  - the other drive's name and "t9"
  - `/volumes`, `/users/`, `/home/`, `/private/`
  - both client names
  - the project folder's name
  - "!coding"
- Remaining hits:
  - "friday": 6, the coordinator seat's role in ruling markers, not a person.
  - "general": 1, the English word in "a general property".
- Positive controls: "audit" 143 hits in the same file. The owner's short first name: 6 hits in the project's `CLAUDE.md` with the same command.
- Fixtures: every new test generates its identities from `common::fixed_identity` and its stores in memory. No file read, no recorded data.

## 7. NOT TESTED

- The remote: no `git ls-remote`. Main is as given; I did not check whether it moved.
- The five gate files in `--release -- --ignored`. The builder's figures (including the known N9 panic at `gate_r3.rs:407:18`) are READ only.
- My generated properties ran at 40 cases (debug), about 2,000 roster steps and about 3,000 R5-m1 steps. They never reached QA-m1's seat state; the two deterministic tests show it. The builder's 1,024-case release run is READ.
- A second volume kind or a real on-disk store, Windows or Linux, real hosts, crash timing on a real disk: the stops are simulated by a store that refuses every call after its k-th.
- `archive_and_release` all-or-nothing (deferred, BACKLOG). N1 and N2 pins: READ, not attacked.
- The builder's cost measurements (3 ms per version, 0.36 s rebuild): READ.

## 8. What I used on disk

- Work area `/private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/d534540a-a4f0-44ac-a3a3-685bcd5abffc/scratchpad/gate_audit_fix/` (not on the project volume), about 2.5 GB in total.
- Copies: `clone` (pristine, for check.sh and both runners), `atk` (clone + my test), `mut` and `mut2` (mutant copies).
- Target directories:
  - `t1` 1.4 GB: check.sh, core runner, second mutant worker.
  - `t2` 355 MB, plus the runner's own `t2-mut` 149 MB: audit runner.
  - `t3` 362 MB: my tests, first mutant worker.
- Cargo home: a symlink to the project's `tools/cargo/bin`, with my own registry (200 MB from `cargo fetch --locked`, the only network use). The project's `tools/target` was not touched and nothing was deleted outside my area. The project volume showed 80 GiB free before and after.
- Processes left: none.
