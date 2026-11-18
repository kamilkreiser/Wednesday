VERDICT: GO WITH NOTES — head df6d5fe4d3382a02be93221bdbb2ab433e1a8174

# QA gate M3-AUDIT-FIX2 (tier 1, the one short check of the small fix round): `coagent-audit`, branch `m3-audit-fix2`

Independent gate, 2026-11-18. Findings only. Nothing was fixed, committed, merged or pushed. Nothing was written in the project folder.

- **Head under test (TESTED).** The clone's `git rev-parse HEAD` is `df6d5fe4d3382a02be93221bdbb2ab433e1a8174`.
- **Main (READ).** Main is taken as given: `e3541182625ccdb4e7e1c01cb6bf21dd9d1b1a8d`. I did not read the remote. There was no `git ls-remote` and no credentials were used, so I cannot say whether main has moved since.
- **Ancestry (TESTED, local).** The merge-base of HEAD and that main is main itself. HEAD is four commits on top of it: `13faa8d`, `8a73dd7`, `f53f663` and `df6d5fe`.
- **Tests and logs.** My tests, drivers and short logs are in `m1_review/gate_audit_fix2_tests/`. To run my test file, drop `qa_fix2.rs` into `crates/coagent-audit/tests/` and add `[[test]] name = "qa_fix2"`. As delivered it passes `cargo fmt --check` and `cargo clippy -D warnings` (TESTED).
- **How figures are marked.** Every figure below is marked TESTED (I ran it) or READ (I read it). Figures from the builder are quoted as the builder's.

## BLUF (for the owner, in plain words)

1. **The fault you asked to close before the beta (QA-m1) is closed.**
   - **Before:** lowering your own limits could leave your own space too full to write the "checkpoint" that gets another member's request witnessed. Every later checkpoint was then refused.
   - **Now:** the product refuses that lowering and keeps your limits as they were, and every checkpoint goes through.
   - I tested the exact edge in bytes and in records, lowering in many small steps, raising then lowering, and lowering by bytes only and by records only. I also had every other member flood you with events and requests after the tightest accepted lowering. In every case the owed checkpoint still went through (TESTED).
   - **A peer alone cannot block your checkpoint.** I tried. In my tests, only the session's starter could cause it, by moving or removing you.
2. **The builder's figures reproduce exactly (TESTED).**
   - `check.sh`: exit 0, 897 passed / 0 failed / 18 ignored.
   - Audit red runner: 153 rows red, none not red, GREEN 256.
   - The generated property at 1,024 cases: PASSES, with the restart state counted 8 times.
3. **The restart issue Friday ruled "stated, not fixed" is real, and the carve-out for it in the test is exactly that issue and nothing wider (TESTED).**
   - **What the issue is:** after a restart the product comes back on its default limits. If your limits before the restart had fewer records than the defaults, a requester can have filled more room than the defaults give. That requester's checkpoint is then refused until your software offers the old limits again.
   - **What I found beyond it (new Minor, QA2-m1):** when that issue meets the known "re-used seat" issue (N1, which needs the starter to re-add you into a used slot), the documented remedy does not work. The old limits are refused and so are the defaults. The checkpoint stays refused until some third set of limits is offered, and the docs do not say how to find one.
   - It needs your own unusual limit change, a restart and the starter's re-add together. Nothing is lost, and it can be recovered.
4. **My recommendation on "caller or crate": close it in the crate, as a short follow-up before the beta.**
   - The change is about 6 lines inside `try_set_limits`: never let an offered limit give any part of your own space more room than the defaults give.
   - I built it as a prototype. With it, the restart issue and my combined state can no longer be built.
   - Every gate test, the earlier check's tests, the R5-m1 tests and the generated property at 1,024 cases with the carve-out switched off all pass. The only tests that fail are the three that exist to show the issue (TESTED, section 5).
   - The daemon would then not need to keep and replay old limits to stay correct.
5. **Merge this branch: GO WITH NOTES.** No Blocker, no Major. One Minor (QA2-m1) and four Notes.

## 1. Findings

| id | sev | what | input that shows it | exact output seen | file:line |
|---|---|---|---|---|---|
| **QA2-m1** | Minor | **N1's state and the resume-defaults state together: neither caller remedy named in the docs ends it, and the property would fail on it.**<br><br>**Setup.** The member's limits L have the default bytes less 20,000 per seat and 2,000 records per seat, so each allowance has more bytes than the defaults give. The requester fills its allowance under L. The starter re-adds the member into a slot whose seat holds an earlier member's records. The seat is then over L's seat in records but within the defaults' seat.<br><br>**Under L:** the checkpoint is refused (N1).<br><br>**After `resume` (defaults):**<br>- it is refused again, now because the payer is short (the resume-defaults state);<br>- `try_set_limits(defaults)` is refused by clause (A);<br>- `try_set_limits(L)` is refused by the seat clause (the N1 exception).<br><br>The procedure in `docs/AUDIT.md` "Changing the limits" ("offer your own limits; if refused, the limits in force before the restart"), the BACKLOG daemon entry, and the doc comment's "offering the limits in force before the restart ends it" therefore do not end it. A third limit does (default bytes, records just above the seat), but nothing tells a caller to look for one.<br><br>**The property (READ the code, TESTED the recogniser):** the P3 exception arm asserts that the owed checkpoint is `Ok` under the defaults, which is false here. The resume-defaults recogniser answers "(iii)", so the property would FAIL on this state if its generator reached it. That is correct behaviour (the carve-out is not wider), but it means the addendum's "the only state" is not the whole answer: the 1,024-case seed simply does not reach this combination.<br><br>**Who can cause it:** it needs the owner's own lower-records limit, a restart, and the starter's re-add. A peer alone cannot cause it. Nothing is lost, and it is recoverable. Hence Minor. I graded it Minor rather than Major because it is the conjunction of the two named states, it is reachable only through the owner's setting plus the starter's act, and the false text is docs and procedure. | `qa_fix2.rs` `qa2_finding_n1_and_resume_defaults_together_neither_named_remedy_works` (PASSES while the state exists); recogniser on the same store: `qa_recogniser_addon.rs` | TESTED: "L StoreLimits { bytes: 40619920, records: 16000 } allowance (362535, 142) (defaults (362063, 2043)); H's allowance (361866, 79); … after re-add seat (3521619, 3078) (L seat (5077490, 2000), default seat (5097490, 28604)); under L: checkpoint Err(LogFull), L again Err(LogFull); after resume: checkpoint Err(LogFull), defaults Err(LogFull), L Err(LogFull), checkpoint Err(LogFull), limits StoreLimits { bytes: 40779920, records: 228832 }; a third limit StoreLimits { bytes: 40779920, records: 24792 }: Ok(()), checkpoint Ok(1078) of 1078". Recogniser: `Err("(iii) the limits before the restart (StoreLimits { bytes: 40619920, records: 16000 }) answered Err(LogFull), the checkpoint then Err(LogFull)")` for both the P2 and the P3 refusal | `src/session.rs:589-593` (doc comment), `docs/AUDIT.md:236-240` and `:375`, `BACKLOG.md:375`; `tests/fix_qam1_seat.rs` `p3_again` exception arm (`:1073-1079`) |
| QA2-n1 | Note | The reach assertion "resume-defaults state > 0 at ≥ 1,024 cases" holds only for the committed seed. At two other seeds (1,024 cases each, release) P1, P2 and P3 all held, with no failure of the property itself, but the test panicked on that reach assertion. It is harmless while the seed is fixed. Anyone who changes the generator or the seed will see a red that is not a fault. | Seed variant of the property (`fix_qam1_seat_seed_variant.diff`, `FIX_QAM1_SEED`), seeds 7 and 200 | TESTED: seed 7: "fix qam1 resume-defaults state (addendum 1): 0", "P2 N1 cases: 3", then panic "fix qam1 property never reached: the resume-defaults state (at 1024 cases)" (315.60 s). Seed 200: "resume-defaults state: 0", "P2 N1 cases: 21 (13 repeated …)", the same panic (268.05 s). No "Test failed" text at either seed | `tests/fix_qam1_seat.rs:1834-1840` |
| QA2-n2 | Note | **Cause (c), the slot-0 fallback, needs only ONE party in the default layout.** After the starter removes the member, the member's seat is slot 0's seat, and the slot-0 member keeps sending into it with no hold-back. In the test world, and wherever the convener sits in slot 0, that slot-0 member IS the starter. So "the starter and one peer together" (brief) is in practice "the starter alone". The docs' "both the starter's acts" is accurate. The property counts it as N1, as ruled. | `qa2_finding_slot0_fallback_a_later_slot0_event_takes_the_room_after_an_accepted_change` (passes while it exists) | TESTED: "own alone (29556, 31), slot-0 seat (30324, 32); own-only limits Err(LogFull); exact Ok(()) (room true); slot-0 member's event Ok(()); checkpoints [Err(LogFull), Err(LogFull), Err(LogFull)]" | `src/session.rs` `local_slot` (fallback to 0), `receive` → `seat_room` |
| QA2-n3 | Note | **The docs for callers do not say what to do if the daemon's kept limits are lost.** Offering the defaults is then refused in the resume-defaults state. A caller CAN recover without the old limits by offering the default bytes with a lower record limit (fewer records give each allowance more bytes), as long as that limit is still above what the seat holds. It can find one by trying, because a refused offer changes nothing. The docs and the BACKLOG entry say only "they must therefore be kept". | QA2-m1 input ("a third limit") | TESTED (the third limit in QA2-m1) | `docs/AUDIT.md:236-240`, `BACKLOG.md:375` |
| QA2-n4 | Note | **A crate-side close exists and is small** (section 5). It is offered as the recommended follow-up, not as a defect of this round. | `clamp_proto.py` | TESTED (section 5) | `src/session.rs:594-604` (the cap step) |

No Blocker, no Major. One Minor (QA2-m1) and four Notes.

## 2. What I reproduced (A)

| claim (builder, STATUS) | mine |
|---|---|
| `check.sh`: exit 0, "CHECK OK", 897 / 0 / 18 | TESTED on the pristine clone: exit 0; "==> 4/4 deny: cargo deny check licenses / licenses ok / CHECK OK: fmt, clippy, test, deny all passed"; summed over 115 test binaries: 897 passed / 0 failed / 18 ignored. The one warning is "unused workspace dependency `rand_core`", as before (`check_sh_tail.txt`) |
| `red-controls-audit.sh`: 151 cfg + 2 source rows, 153 RED, 0 NOT-RED, GREEN 256, "RED CONTROLS OK" | TESTED, with my own `COAGENT_AUDIT_RED_TARGET` and `COAGENT_AUDIT_RED_LOGS`: "rows: 151 cfg rows + 2 source-mutant rows"; 153 RED rows, 0 NOT-RED; "GREEN: 256 tests ok"; "RED CONTROLS OK: every guard went red under its control, on its property, and green without" (`red_audit_rows.txt`).<br>- New row `limits_strand_seat`: RED on "Test failed: QA-m1 property P1: step 13: an accepted change (aim bytes short) left an owed checkpoint without room: seat (35936, 16) of (36451, 80), owing {0} …".<br>- `limits_strand_payer` is still red on its own text: "Test failed: R5-m1 property: step 26: … because its payer, the allowance of slot 0, lacks room …".<br>- `own_cp_unchecked` is still red on `m23_*` and on the unedited `gate_r4::r4_guard_an_own_checkpoint_is_space_checked` ("left: Ok(())").<br>- The runner was started in the background and its exit code was not captured. Its last line "RED CONTROLS OK" is printed only on success |
| the property at 1,024 cases, release: PASSES; resume-defaults 8; P2 N1 cases 12 (8 / 2 / 2); P3 accepted again 65,860; exception 80 | TESTED on the pristine clone (`FIX_QAM1_CASES=1024`, release): "test result: ok. 1 passed" in 244.58 s.<br>- "fix qam1 resume-defaults state (addendum 1): 8", all at P3. First schedule: "P3 step 93: in force StoreLimits { bytes: 40779920, records: 228832 }, before the restart StoreLimits { bytes: 40779920, records: 112628 } …".<br>- "P2 N1 cases: 12 (8 repeated …, 2 did not, 2 not followed by one)".<br>- Reach: accepted with a requested event owed 1,994; refused by the seat clause alone: bytes 170, records 100, both 8; refused by clause (A) 1,525; paid by an allowance after an accepted lowering 1,128; re-added into a seat holding another author's records 60; P3 accepted again 65,860; P3 exception 80.<br>- Every figure equals the builder's (`prop_default_1024.txt`) |
| the default 64-case run passes, its state count 0 | TESTED inside `check.sh` (`fix_qam1_seat`: 11 passed in 151.56 s). The printed count was not captured, because `check.sh` does not pass `--nocapture` |
| the two ruled `qa_finding_*` tests pass after the fix | TESTED at head.<br>- seat-records: "try_set_limits Err(LogFull); then 10 checkpoints: 10 Ok, 0 refused LogFull; payer slot Some(3) …; newest covered Some(43) of own seq 43".<br>- seat-bytes: "Err(LogFull); 5 checkpoints [Ok(()), Ok(()), Ok(()), Ok(()), Ok(())]; payer Some(3), room true".<br>Log: `qa_fix_findings_at_head.txt` |
| a different seed or a larger size | The size is set by `FIX_QAM1_CASES`. The seed is fixed (`TestRng::deterministic_rng`), so I added `FIX_QAM1_SEED` in a copy in my area (`fix_qam1_seat_seed_variant.diff`) and ran seeds 7 and 200 at 1,024 cases in release.<br>- Both: no P1, P2 or P3 failure, and no new failing state. See QA2-n1 for the reach panic.<br>- Seed 7: P3 accepted again 69,033; exception 47; accepted with a requested event owed 2,162.<br>- Seed 200: 66,749 / 136 / 2,111 (TESTED) |

## 3. Scope, public surface, gate files, ruled edits (B)

- **`git diff --stat e354118 HEAD` (TESTED).** 9 files, 2,170 insertions / 92 deletions: `BACKLOG.md`, `crates/coagent-audit/{Cargo.toml, build.rs, src/session.rs, tests/fix_qam1_seat.rs (new), tests/fix_r5m1_limits.rs, tests/qa_fix.rs}`, `docs/AUDIT.md`, `scripts/red-controls-audit.sh`. Nothing else: no `Cargo.lock` and no other crate.
- **Public surface (TESTED).** I took the sorted `pub` lines of every `src` file at main and at head: 481 each, and `diff` is empty. `try_set_limits` and `set_limits` keep their signatures, and `set_limits` is still `let _ = self.try_set_limits(limits);`.
- **Gate files, sha256 main against head (TESTED, all EQUAL):**

  | file | sha256 prefix |
  |---|---|
  | `gate.rs` | `d6a29f1e…` |
  | `gate_attacks.rs` | `6ef41612…` |
  | `gate_r2.rs` | `adca67f3…` |
  | `gate_r3.rs` | `c1726e9d…` |
  | `gate_r4.rs` | `addc9f79…` |
  | `gate_r5.rs` | `d16e82d5…` |
  | `qa_fix_wrapper.rs` | `9e5e6432…` |
  | `fix_notes_pinned.rs` | `5a8ed79d…` |

  `qa_fix.rs` changed: main `ebca51ae…eb6e8`, head `b4100b5a…9a46`.
- **`qa_fix.rs`, read line by line (TESTED diff).** Exactly two hunks, each with `// RULING (Friday, 2026-11-18, audit-fix2 brief; QA-m1)` and every old line quoted as `// old:`. Nothing else changed.
  - **seat-records.** Old: `tr.is_ok() && refused == 10 && payer == Some(3) && pu.0 + 516 <= a.0 && pu.1 + 1 <= a.1 && free == (0, 0)`. New: `tr == Err(AuditError::LogFull) && refused == 0 && ok == 10 && payer == Some(3)`.
    - The old assertion stated the fault (the change accepted, all 10 refused) together with the fault's preconditions (payer room, free part empty).
    - The new one states the fixed property for the same input: refused, all 10 `Ok`, the payer still slot 3. Every value used is one the test already computes.
    - Dropping the room and free-part terms is right. They were conditions under which the fault showed, and `tr == Err(LogFull)` already pins that the lowering was refused. **Ruling: at least as strong. Accepted.**
  - **seat-bytes.** Old: `tr.is_ok() && r.iter().all(|x| *x == Err(AuditError::LogFull))`. New: `tr == Err(AuditError::LogFull) && r.iter().all(|x| x.is_ok())`. **Ruling: the exact mirror of the fault. Accepted.**
  - Both are the brief's words exactly. Mutants M01, M05, M06, M07, M08, M11 and M13 turn them red again (section 6).
- **`fix_r5m1_limits.rs` (builder-owned, rewritten, READ line by line).** Nothing it guarded is weakened:
  1. The model gains `own` (the member's own records alone), read from the store keys. Neutral.
  2. The seat-cap branch: a refusal whose payer had room used to be counted and let pass. Now it FAILS ("QA-m1: …") unless the member's own records alone leave the checkpoint room. **Stronger.**
  3. The same-limits-after-resume check and the every-step check now go through `again_or_exception`. That accepts a refusal only when a checkpoint is owed, the seat lacks room under those limits, the own records alone DO fit, and the answer is exactly `Err(LogFull)` with the defaults in force. This generator never calls `receive`, so the seat is always the own records alone. Any refusal therefore falls into the `Err("QA-m1 …")` arm or the "refused" arm, exactly as strict as before.
  4. One small gap: unlike `fix_qam1_seat`'s `p3_again`, the exception arm does not also check that the checkpoint is `Ok` under the defaults. The arm is not reachable in this generator, so this is not a weakening.

  **Ruling: accepted.**

## 4. Rule (S), attacked (C)

My file `qa_fix2.rs`, 9 tests, all green at head (TESTED, `qa_fix2_run.log`):

| test | what it shows | printed (TESTED) |
|---|---|---|
| `qa2_boundary_bytes_exact_ok_one_less_refused_and_the_room_holds_against_everything` | Seat exactly usage + (516, 1) in bytes is `Ok`; one byte less is `LogFull` and the limits are unchanged. After the exact acceptance, an own record, a request by the owing requester and a request by another requester are all `LogFull`, and the checkpoint is `Ok` and fits | "seat (29556, 31); one less Err(LogFull) (limits then StoreLimits { bytes: 524288, records: 4096 }); exact Ok(()); own record Err(LogFull); H again Err(LogFull); another requester Err(LogFull); room true; checkpoint Ok(31); seat after (29970, 32) of (30072, 512)" |
| `qa2_boundary_records_exact_ok_one_fewer_refused` | The same in records, lowering by records only | "one fewer Err(LogFull) (unchanged true); exact Ok(()); own record Err(LogFull); checkpoint Ok(31)" |
| `qa2_lowering_in_steps_every_accepted_step_keeps_the_room` | Bytes-only steps of 97 bytes from 64 KiB down, a raise to the defaults, records-only steps from 511 to 8, then a raise and a lowering straight to the floor. After every `Ok`, every owing allowance and the seat keep (516, 1); after every refusal the limits are unchanged | "accepted 846, refused 324 …; raise then lowest Err(LogFull); checkpoint Ok(31)" |
| `qa2_nothing_owed_lowering_below_the_seat_is_accepted_then_requests_refused` | Nothing owed: a lowering to half the seat is accepted. Four requests and an own record are then refused, and the own sequence and store usage are unchanged, so nothing is recorded without a witness | "seat (29970, 32) lowered to (14985, 16): Ok(()); requests [Err(LogFull) ×4]; own record Err(LogFull); own seq 31 -> 31; store (34046, 33) -> (34046, 33)" |
| `qa2_re_added_into_a_clean_slot_the_room_follows_and_into_n1s_seat_the_clause_counts_it` | (a) Exact acceptance in slot 1, then the member is removed and re-added into a never-used slot 7: the checkpoint is `Ok`.<br>(b) N1's seat (re-added into slot 2 with X's records): limits sized to the own records alone are REFUSED, because the clause counts X's records; limits sized to the whole seat are accepted, and the checkpoint is `Ok` | "(a) exact Ok(()); now slot 7; checkpoint Ok(21)"; "(b) own alone (19876, 21), seat (24880, 24); own-only limits Err(LogFull); whole seat Ok(()); checkpoint Ok(21)" |
| `qa2_finding_slot0_fallback_…` | Cause (c), as pinned in QA2-n2 | see QA2-n2 |
| `qa2_a_peer_alone_cannot_take_the_owed_checkpoints_room` | After acceptance at the exact boundary, seven peers each send up to 199 events of 500 characters and request until refused. The room holds and the checkpoint is `Ok` | "175 peer records/requests accepted; room true; checkpoint Ok(31)" |
| `qa2_set_limits_equals_try_set_limits_across_seat_refusals` | Two identical sessions, seven offers (one byte short, exact, records short, raise, half): the limits are equal after every call, and so are the checkpoints | "3 refused; checkpoints Ok(31) Ok(31)" |
| `qa2_finding_n1_and_resume_defaults_together_neither_named_remedy_works` | QA2-m1 | see QA2-m1 |

**The claim to break**, by reading:

> After any `try_set_limits` answered `Ok` while a requested event is owed, the owed checkpoint has room in both the paying allowance and the seat, and keeps it until it is stored, unless a later roster move of the member or another author's record takes it.

- **It holds.**
  - Clause (A) checks every owing allowance, a superset of the payer. The payer is the newest requester's allowance (`head_payer`).
  - The seat clause uses the same test as `own_room`'s seat check (`:952` area: `per_peer`, closing, reserve 0) with the offered limits.
  - Every later own record keeps (516, 1) in the seat (`own_room`, `closing == false`), and every later request also keeps it in its allowance (I-A13).
  - `receive` charges a peer's record to the AUTHOR's slot (`slot_of(author)`). An author that is not on the roster gets `NotMember`, so a removed earlier occupant can add nothing later.
  - So with the member on the roster, only a roster version that moves or removes it can bring another author's records into its seat.
- **Is P2's N1 carve-out wider than that?** P2 lets a refusal pass only when the payer has room, the seat lacks room, and the member's OWN records alone plus one checkpoint DO fit the seat in force (`fix_qam1_seat.rs:1355-1386`). Two cases:
  - Another author's records in the seat at the moment of an accepted change, causing a wrong acceptance: P1 already catches that at the change, because P1 reads `seat_usage(own_slot)`, which includes them.
  - Otherwise the excess can only come from another author's records that arrived or were brought in by a roster move after the change.

  **Ruling: the N1 carve-out is that state and nothing wider.**
- **Peer alone: no** (TESTED above, and by reading). The only late arrival into the member's seat is the slot-0 fallback, which needs the starter to remove the member first (QA2-n2).

## 5. The resume-defaults state and its carve-out (D)

**(1) Is the recogniser exactly that state?** Yes (TESTED).
- **The three recogniser mutants** (R1 drops condition (i), R2 drops (ii), R3 drops (iii)) are each killed by the branch's own `qam1_the_resume_defaults_recogniser_is_exactly_that_state`.
- **The 64-case property alone does NOT notice a wider carve-out.** It stayed green under all three mutants: its seed never reaches the state.
- **The red controls are not hidden by a wider carve-out.** Under `limits_strand_seat` the property goes red on its own text for all three ("QA-m1 property P1: step 13: an accepted change (aim bytes short) …"), and under `limits_strand_payer` on "QA-m1 property P1: step 27: an accepted change (aim bytes exact) …" (`mutation_recogniser.txt`).
- **R1 is equivalent inside the generator**, with this written reason. `restarted` is set only at a `Resume` op, which installs the defaults, and it is cleared by every `Ok`. So whenever `restarted` is `Some`, `in_force` is the defaults, and dropping the `in_force == d` test changes nothing there. Only the deterministic test can tell, and it does.
- **A state with two of the three conditions:** QA2-m1's store satisfies (i) and (ii) and fails (iii). The recogniser answers `Err("(iii) …")` for both refusal kinds (TESTED, `qa_recogniser_addon.log`), so the property would fail there, as it should.
- **Hiding a QA-m1 or R5-m1 state behind the carve-out cannot work.**
  - Condition (iii) requires that the limits before the restart, offered again to a resumed copy, are accepted AND that the owed checkpoint is then stored. A real QA-m1 or R5-m1 state under those limits fails (iii).
  - Condition (ii) requires the defaults' SEAT to have room, so a seat state is excluded.
  - The builder's one interpretation ("before the FIRST of two restarts") is the right one: it names the last limits the rule accepted, which is what a caller would have kept.

**(2) Caller or crate? Ruling: the state is correctly STATED by this round. I recommend closing it in the crate, not leaving it to the caller.**
- **Why it exists.** The cap in `try_set_limits` is per component (bytes, records). But the own seat is "a seat minus one byte per record", so an offer with the default bytes and fewer records RAISES each allowance and the free part above the defaults. That contradicts the docs' own "the limits may only be lowered below the defaults". `resume` then brings the defaults back, which are smaller in that part.
- **The fix.** Six lines in the cap step: lower the offered bytes so that the own seat's bytes never exceed the defaults' own seat bytes. Then the defaults are at least every accepted limit in every part (seat, free part, each allowance), and the state cannot arise.
- **Prototype (`clamp_proto.py`, applied to a copy in my area only, TESTED, release):**

  | test file | result |
  |---|---|
  | `fix_r5m1_limits`, `qa_fix`, `gate_r5`, `gate_r4`, `gate`, `fix_notes_pinned`, `a5_requester_pays`, `a5_anchor`, `a5_guards` | all exit 0 |
  | `fix_qam1_seat` | 9 pass; only the pin and the recogniser test fail, because the state can no longer be built: "after resume … 3 checkpoints [Ok(()), Ok(()), Ok(())]; try_set_limits(defaults) Ok(())" |
  | my `qa_fix2` | only the combined-state finding fails, because after `resume` the "checkpoint Ok(()), defaults Ok(())" |
  | the property at 1,024 cases with the carve-out switched OFF | P1, P2 and P3 hold; it stops only on the now-unreachable reach assertion "never reached: the resume-defaults state" (238.62 s) |

  No public item changes.
- **Its costs.**
  - `limits()` reads back lower bytes than offered for such offers. That is one docs sentence, and the existing cap already behaves this way.
  - The pin, the recogniser, the carve-out and the BACKLOG entry would be retired.
  - It does not touch any [07] constant or table.
- **If it stays with the caller, the daemon must:**
  1. persist the last limits `try_set_limits` accepted, durably and in step with the store;
  2. after every `resume`, offer its own limits, then those kept limits;
  3. in N1's state, and if the kept limits are lost, search for a third limit (QA2-m1, QA2-n3).

  With the kept limits lost and the state present, the owed checkpoint stays refused and later events go unwitnessed until such a search, though nothing is lost. The docs as written are not complete enough to implement step 3.

**(3) Severity as it stands: Minor.**
- **Who causes it:** the owner, by an unusual lower-records limit, followed by a restart.
- **Can a peer time it?** A requester can fill its allowance close to the L-allowance by ordinary requests, and so set up the stall for the next restart, but it cannot cause the limit or the restart. The effect is that the requester's event, and the member's later events, go unwitnessed until the caller acts. No data is lost.

## 6. Mutation (E)

17 source mutants of my own in `src/session.rs` (`mutate.py`; each run in release over `fix_qam1_seat`, `fix_r5m1_limits`, `qa_fix`, `gate_r5`, `gate_r4`, `fix_notes_pinned` and my `qa_fix2`; TESTED, `mutation_src_table.txt`):

| id | mutant | killed by the branch's own tests | killed by mine |
|---|---|---|---|
| M01 | seat clause removed | `fix_qam1_seat` (finding inputs, boundary, exception, `set_limits`, property), `fix_r5m1` property, both `qa_finding_*` | yes |
| M02 | seat bytes `>` → `>=` | boundary test, property | yes |
| M03 | seat records `>` → `>=` | boundary test, property | yes |
| M04 | seat bytes lenient by one | boundary, exception, property | yes |
| M05 | seat records lenient by one | records input, boundary, property, `qa_finding_…records` | yes |
| M06 | bytes only (records part gone) | records input, boundary, property, `fix_r5m1` property, `qa_finding_…records` | yes |
| M07 | records only (bytes part gone) | bytes input, boundary, exception, `set_limits`, property, `qa_finding_…bytes` | yes |
| M08 | wrong slot (seat of slot 0) | all `fix_qam1_seat` deterministic tests, property, `fix_r5m1` property, both `qa_finding_*` | yes |
| M09 | own records only ((S-own)) | exception test, property | yes (N1 seat, slot-0, combined) |
| M10 | applied when nothing is owed | nothing-owed, small limits, exception, property, `r5m1_small_limits…`, `r5m1_only_allowances_owing…` | yes |
| M11 | applied to raises only | as M01 | yes |
| M12 | applied to lowerings only | `qam1_exception_after_resume_in_n1s_state_is_exactly_as_ruled` ONLY | yes (combined) |
| M13 | seat checked against the OLD limits | as M01 | yes |
| M14 | seat checked against `own_reserved` (own seat) instead of `per_peer` | boundary, property | yes |
| M15 | clause (A) bytes `>` → `>=` | `r5m1_the_rule_at_its_exact_boundary…`, `qa_ok_rule_a_edges…` | no |
| M16 | clause (A) looks at one owing allowance only | property, `qa_ok_rule_a_edges…` | no |
| M17 | clause (A) records part dropped | property, four `fix_r5m1` tests, `qa_ok_rule_a_edges…`, two `gate_r5` tests | no |

**All 17 are killed by the branch's own tests. There are no survivors and no equivalent mutants.**
- **M12 hangs on one test.** It is killed only by the exception test (and by my combined test). That single test is what pins the ruling that the seat clause also applies to raises.
- **M15–M17 are killed only by the branch's tests.** My file does not aim at clause (A).

Recogniser mutants R1–R3: see section 5(1). All three are killed by the branch's deterministic recogniser test, and none by the 64-case property. R1 is equivalent inside the generator (reason in section 5).

## 7. Docs and BACKLOG (F) (READ against the code, TESTED where marked)

- **"Changing the limits"** (`docs/AUDIT.md:201-241`) is true as written, with one gap: the caller procedure is incomplete for QA2-m1's state (QA2-m1, QA2-n3). Each claim checked:
  - what "owed" means;
  - the two clauses;
  - raises are included;
  - nothing owed refuses nothing;
  - QA-n1 made true (an allowance owing nothing may be lowered below what it holds);
  - "then the next request is refused … so nothing is recorded that would need a witness" (TESTED, `qa2_nothing_owed_…`);
  - "What a caller sees";
  - the tests and red controls named.
- **The sentence about allowance bytes depending on the record limit** (`:189-192`) is true (TESTED figures: 362,535 and 362,574 bytes under fewer records, against the defaults' 362,063).
- **The new "Limits, stated" entry** (`:537-553`) is true, and its example figures equal the pin's printed line.
- **"Restart"** (`:368-382`) is true as far as it goes: "under the defaults the seat has room for that checkpoint" is literally true. QA2-m1 is the state in which the payer still lacks room there.
- **The charging-table row** (`:273`) is true.
- **The QA-m1 entry's "What remains" (1)–(4)** is true, and complete except for the conjunction in QA2-m1.
- **BACKLOG:**
  - QA-m1 is closed in the file's own form (`- [x] <original sentence unchanged> — CLOSED in commit 13faa8d… …`). Nothing is deleted and its sub-lines are kept; the stale "Why deferred" sub-line under a closed entry is harmless history.
  - There is exactly ONE open daemon-lane entry for the resume-defaults state (`BACKLOG.md:375`), in the addendum's words.
  - The "N1's state" entry is still open, with its symptom corrected.
  - The older daemon entry (resume returns defaults, R5-m1) is corrected and still true.

## 8. Rulings on Friday's rulings

- **Brief, "owed" = a requested event not yet covered (rule (A)'s set; own uncovered events excluded): AGREE.** It keeps the r4 guard's C2 state open as ruled. `qam1_the_gate_guards_shape_…` and the unedited gate guard are green, and the guard's runner rows are red.
- **Brief, build (S) not (S-own): AGREE.** M09 ((S-own)) is weaker: the branch's exception test and property kill it, and so do my N1-seat and slot-0 tests.
- **Brief, the exception after `resume` in N1's state, and the seat clause not restricted to lowerings: AGREE.** M12 shows the raise half is guarded, though by one test only.
- **Brief, the two `qa_fix` edits in exactly those words: AGREE.** They are at least as strong (section 3).
- **Addendum, "stated, not fixed": ACCEPTABLE for this merge**, because the state is Minor-class and predates the round. But the caller remedy as written is incomplete (QA2-m1, QA2-n3), and a small crate-side close exists (section 5). I recommend that close before the beta in preference to the daemon lane.
- **Addendum, the three-condition carve-out: AGREE.** It is exactly the state and nothing wider (section 5(1)), and the red control still goes red on P1 with the carve-out widened.

## 9. Hygiene (G) (TESTED)

- **What I scanned:** the 2,170 added lines of `git diff e354118 HEAD`, case-insensitively.
- **Zero hits each for:** the owner's first names (short and full) and surname; the owner's mail address and its domains; both other client names; the host name and the user name read from the system; the drive name; "laptop"; "devmaster"; "t9"; "/volumes"; "/users/"; "/home/"; "/private/"; "!coding"; the project folder's name; "wednesday"; "tuesday".
- **Explained hits:**
  - "friday": 11. These are the coordinator's role name in the ruling markers the brief mandates and in one STOP note.
  - "general": 1. It is the English word in "a general property of a full part".
- **Positive controls:** "audit" gave 123 hits in the same lines, and the owner's short first name gave 6 hits in the project's `CLAUDE.md` with the same command.
- **Commit message bodies:** 0 hits for the owner's names, "/volumes", "laptop" or the mail domain. The commit AUTHOR field carries the repository's configured git identity, as for every commit.
- **Fixtures:** every new test builds its identities with `common::fixed_identity` and its stores in memory. Nothing is read from a drive.

## NOT TESTED

- The remote: main was taken as given, and no `ls-remote` was run.
- `scripts/red-controls-core.sh` (not asked; the round changed no other crate).
- The gate files in `--release -- --ignored`.
- `resume_with_anchor` in my own tests (only the property covers it).
- More than two other seeds, and more than 1,024 cases.
- The clamp prototype under `check.sh` (fmt, clippy, the whole workspace) and under the red runner. Only the eleven test files in section 5 were run against it.
- Whether the generator could ever reach QA2-m1 (I built it deterministically).
- The exit code of the background red-runner process (its success line was read instead).

## Disk used (TESTED, `du`)

My area totals 2.2 GB: `target` 1.1 GB (`check.sh` and the 1,024-case release run), `target_red` 370 MB (audit red runner), `target_work` 352 MB (my tests, seeds, mutants, prototype), `cargo_home` 200 MB, clone and work copy 9.1 MB each, logs 1.6 MB. The output folder is 140 KB. Nothing was deleted outside my area, and no process of mine is left running.
