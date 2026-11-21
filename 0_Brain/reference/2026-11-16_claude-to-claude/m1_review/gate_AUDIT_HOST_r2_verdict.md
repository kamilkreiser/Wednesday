VERDICT: GO WITH NOTES — head 680d3333c8713fc12f140068b2a3a985d96c4681

# Short re-check (r2): CoAgent `audit-host` after its one fix round

Checker: QA-AUDIT-HOST-R2 (new seat; did not build it, did not write the first check). Work dir `/private/tmp/claude-501/qah2`: `clone/` (clean head: stop-anywhere, property, red runner), worktree `probe/` (my probes and the first check's), `base/` (35f7e89 plus the test-only `FailEvery` rule, for one pre-existence probe), `mut-<id>/` (one per mutant, each with its own target dir). The project folder was only read, except my STATUS file.
Probes of my own (copies): `/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/m1_review/gate_audit_host_r2_tests/` (`src_tests_qa2.rs` → `src/tests/qa2.rs`; `qa2_triggers.rs` → `tests/`; `src_tests_qa2b_at_35f7e89.rs`; `mutate2.py`; `launch.py`; `redctl.py`; README).

## BLUF for the owner
1. **The three faults are closed, by test.** Other members can no longer make your computer file the log away. I tried seven members flooding requests, a member filling its space, and a member whose old records sit in your slot, with every automatic setting on at 1 %: nothing came due. One failed save during a release no longer locks you out. Your size limits never change without the answer saying so.
2. **Nothing else changed.** Only the builder's own files moved. The protected files, the other crates and the lock file are byte-identical. The crash test (323 stopping points), the 14 deliberate-break checks and a 1,024-case random run all pass.
3. **One older gap to note (not from this round, not a blocker).** Suppose a disk fault hits a record, and then a second write fails during the recovery. The answer then says "error" although the record was saved, so a program that simply retries would record that act twice. It behaves exactly the same at the previous head. It needs two failures in one call. It goes on the backlog to fix before the daemon is wired.
4. Nothing you would notice day to day. Your two open choices (when to file away by default; keep every file) are still marked as yours.

## 0. Heads
- Start, `git ls-remote` against the GitHub remote: `audit-host` = `680d3333c8713fc12f140068b2a3a985d96c4681`, `main` = `16e83fbe5592658ddcda769d7827895941eca678`, as briefed. The builder's STATUS ends `READY FOR QA AUDIT-HOST r2`. `main` is already an ancestor of the branch (merge base `16e83fb`); this round has no merge, by design.
- End: see section 13.

## 1. Scope (TESTED)
- `git diff --stat 35f7e89 680d333`: 14 files, +636/−51, exactly the builder's list. Filter for paths outside `crates/coagent-audit-host/**`, `docs/AUDIT-HOST.md`, `scripts/red-controls-audit-host.sh`, `BACKLOG.md`: none.
- `Cargo.toml`, `Cargo.lock`: `git diff --stat 35f7e89 680d333` empty. Other crates, other docs, other scripts since 35f7e89: empty.
- The 28 protected sha256 (the builder brief's 19 audit tests and wrappers, the 8 files that see the crate or the lock, and `seal_common/mod.rs`), recomputed at `680d333`: **28 equal, 0 differ**. Tree hashes `coagent-audit` c90e44c2…, `-proto` b391f9e8…, `-crypto` 71a06b59…, `-roster` 2761baf4…: **4 equal**.
- Harness change `680d333` (READ, `stop_anywhere.rs:281-296`): the in-memory PEER simulations now apply a roster version only if the version still lists them; before, every peer except the removed one did. The host's own `Input::Roster` is applied exactly as before, and the file's 15 assert/panic lines are unchanged in number and text. With a single removal the old and new lines behave the same. With the second removal that m-3 needs, the old line asked member 3 (removed at v2, so still at v1) to apply v3, and the audit crate answered `Roster(Gap)`, as a real removed member would. **A harness bug, not a hidden product fault**: no real member receives versions after its removal, and the host side is untouched.

## 2. M-1: no peer makes any trigger due (READ + TESTED) — CLOSED
- READ `admit` (`host.rs:1252-1298`) and `due` (`:1304-1320`): `Timer` uses `now − last_seal_ms` (set only by the owner's seals, `:887`, `:1468`). `OwnFreePartAt` uses `free_usage()` against `free_part()`. `OwnSeatAt` now uses `free_usage()` against `own_reserved()`. `seat_usage` is used only under the red cfg. `due` tries the same three through `admit`.
- READ `SessionAudit::free_usage` (`coagent-audit/src/session.rs:855-859`, public): `OwnEvent(None) + OwnHead − head_use`, i.e. the owner's own-choice events plus the own checkpoints the free part pays. Requested events (`OwnEvent(Some(slot))`) and the checkpoints charged to an allowance (`head_payer`, `:870ff`) are excluded, and so are peer events and peer heads. Countersignatures go to the fixed `Attestation` part (`:1704-1711`). Own checkpoints come only from `Input::Checkpoint` (the owner's caller) or seal step 0.
- First check's `qa_t1`, **unchanged**, release: 1 %, 2 % (default limits, 684 requests by member 2) and 5 %, 6 %, 7 %, 10 % (8 × 40,000 / 8 × 400): `due() = None` and `seal(OwnSeatAt) -> refused NotDue` at every threshold, free part `(0,0)`. `qa_t2` unchanged: not due.
- Mine (`qa2_triggers.rs`, release; own seat, own free part and timer all on: 1 %, 1 %, 10^12 ms):
  - t1, seven members (0, 2-7) each requesting to its bound: `[(0,684),(2,684),(3,683),(4,683),(5,683),(6,683),(7,683)]`. due false at every 64th request and at the end. Old measure `seat_usage(own) (2529100, 4783) = 49 %`, new `free_usage (0,0) = 0 %`. All three triggers `NotDue`.
  - t2, member 2's PEER EVENTS to its own bound (690 events, seat 2 at 2,532,192 B): due None at every event; all three `NotDue`.
  - t3, earlier occupant: X's 690 events in slot 2, then V removed and re-added into slot 2. Old measure 49 %, new 0 %, all `NotDue`. Then 684 requests by member 3: old 57 %, new 0 %, all `NotDue`.
  - t4, roster changes signed by the convener: 50 requests by member 2 and 5 own checkpoints, then member 2 removed, released, and a newcomer added in slot 2 with 20 requests. `free_usage` stays `(0,0)` throughout; all `NotDue`.
  - **Positive control**: the same file under `COAGENT_AUDIT_HOST_RED=own_seat_counts_requests` (debug, own target): t1 RED (`OwnSeatAt(1) -> SEALED 1`), t3 RED (`SEALED 1` after the requests). t2 green, as expected, because peer events were never in the own seat.

## 3. M-2 and m-1 (TESTED) — CLOSED
- First check's probes, **unchanged**: `qa_q1` `answer Released; anchor_saved=false; pending on disk true; RESTART (default settings) -> OPENED Pending`. `qa_q1b` `OPENED Current own seq 4`. `qa_q2` `pending after the seal true, after 3 more records false; newest record removed; RESTART -> REFUSED Anchor { pending: None, current: Some(Missing { part: OwnEvent(None), … n: 6 }) }`.
- Mine (`src_tests_qa2.rs`):
  - The save fails TWICE (`FailEvery` on `anchors/current`): the release answers `Released`; the next change answers `Err(AnchorNotSaved)` and own seq stays 3; pending stays on disk. **RESTART → OPENED Pending, own seq 3.** Running on, the next record is 4 and pending is gone.
  - The release's pending WRITE fails (first two anchor writes): `Err(Dir(… anchors/pending))`, peer 3 still charged (1575, 3) (nothing deleted). RESTART opens Current, own seq 3. The release run again → `Released`, no pending left.
  - The release's pending REMOVAL fails (every unlink of `anchors/pending`): `Released`, pending on disk, RESTART → OPENED Pending. After 3 records pending is gone; with the newest record removed, RESTART → **REFUSED** `Missing { OwnEvent(None) … n: 6 }`.
  - A seal step-4 failure then a release (a): pending after the seal true, gone after the next two receives; release `Released`, no pending; RESTART opens; newest record removed → **REFUSED**. (b): the anchor is dirty again when the release comes, so the release answers `Err(AnchorNotSaved)` and peer 3 is still charged (nothing done). RESTART opens Current, own seq 4.
- READ `pending_held` (every set/clear, `host.rs:960, 1181, 1193, 1201, 1408, 1463, 1485, 1492, 1506`):
  - Can it **stay set forever**? Set only right after a pending write (release `:1181`, plan `:1408`). Every later return path clears it, with two exceptions:
    - In `release`'s Ok branch, `?` on a re-encode or a second archive write (`:1188-1189`) returns before the clear. That needs the real release bundle to differ from the dry one; both come from `export()` of the same store, so it does not happen without some other bug. The flag then stays set only until the next seal step 4, release or re-open. That `?` was already there at 35f7e89 (Note N-r2-2).
    - `?` on a missing member returns before the clear, but there the host is closed anyway.
  - Can it be **clear while a change is in progress**? No. Between a pending write and its end, nothing calls `save_current` except through `reopen`, which settles pending itself (current saved first, then pending removed), and the cfg(test) hook. At step 4 the clear comes right before the save, and pending is removed only if the save succeeded.

## 4. M-3: limits never change silently (TESTED + ruling) — CLOSED
- First check's `qa_q8`, **unchanged**: `set_limits(low) -> Err(Audit(LogFull))`; then a record with a failing directory sync `-> Ok(Recorded(21))`. In force after the re-open: `3200000/16000`; `changed silently: false`. A later restart reports `before Some(3200000/16000)`.
- Mine, a refused lower offer and then each in-call re-open, then a restart of a copy (`qa2_m3_each_in_call_reopen_after_a_refused_offer`):
  - P-4 record `Ok(Recorded(24))`; P-4 receive `Err(Reopened{landed:true})`; P-7 seal `Err(SealCommitFailed{segment_now:1})`; failed release `Err(Audit(Store(… after the unlink (P-4))))`.
  - In each case: before = after = 3,200,000/16,000; the restart's `before` (read from `anchors/limits`) = in force; `differs false`.
- The `differs` branch, **reached end to end** (the builder's test of it is a unit test on a made-up report). The only state in which the audit crate refuses the limits in force is gate r5's N1 (a re-used slot plus an owed checkpoint; `session.rs` doc of `try_set_limits`). I built it through the host, with a P-4 on the roster version that re-adds V into X's slot: `LimitsChanged { before (131072,512) offered (131072,512) in_force (40779920,228832) refused LogFull, answer Err(Reopened{ landed: true }) }`. A restart afterwards: `before (40779920,228832)`, i.e. `anchors/limits` holds what is in force.
- In that same N1 state, each own call with its directory sync armed to fail: local record, request by 3, request by 4, checkpoint. Every one answers `Err(Audit(LogFull))` **before any write** ("put reached false"), own seq unchanged.
- READ: all three `write_limits` calls (`:788` create, `:910` re-offer, `:1544` set_limits) write the value read back with `limits()`. `set_limits` keeps `cfg.limits` only on acceptance.
- **Ruling on `LimitsChanged { limits, answer }` (an `Err` that may carry a successful change).**
  - Callers: no crate depends on this one, so the callers are the tests and the docs. Inside the crate, `begin_steps` passes a `LimitsChanged` from step 0 through as an Err, and `drain` passes answers through per ticket. Neither retries.
  - Could a caller that treats every `Err` as "not done" record twice? Only if `answer` held `Ok(Recorded)` or `Ok(Checkpoint)`. `differs()` needs the in-force limits to be refused on re-offer. Every own record or checkpoint admitted under limits L leaves room for one more checkpoint, both in its allowance (I-A13) and in the seat (`own_room`, `session.rs` ~:1080-1095), and that is exactly what the re-offer checks. So after a landed own change, L is always accepted again. In the one state where L is refused (N1), no own change can land (tested above). **Today `LimitsChanged` can only wrap an `Err` answer.** So there is no double-record path, and this is not the NO GO of brief §4.
  - The docs and the type do NOT make it impossible to miss. Docs §4 (`docs/AUDIT-HOST.md:84-90`) says "a change reported there as made IS made". But the P-4 bullet (`:55-59`) still promises "a record that landed is answered `Recorded(n)`, so the caller never records it twice". `apply`'s doc does not mention the variant, `HostError` is not `#[non_exhaustive]`, and `Err(_)` swallows it. The guarantee rests on the audit crate's limit rule, not on this crate. Note N-r2-1.
  - **Would I have chosen a refusal?** No. A refusal after a change that has already landed would hide it too, and say even less. I would have kept `Ok` meaning done: return the call's own answer unchanged and make the next mutating call refuse (or `status()` flag) until the owner acknowledges the changed limits. That is a design preference, so it is a note, not a NO GO.

## 5. m-2 (TESTED) — CLOSED
- `qa_s7` unchanged: `topped up to bytes=117440509; ordinary put -> Err(… bound would be exceeded); Segment put -> Ok(()); now bytes=117454578 (over by 14066); RE-OPEN -> Ok("ok")`.
- READ: `put` (`dir.rs:311-315`) and `load` (`:242-246`) both subtract `exempt_totals` (Anchor and Segment ranges, `4 + len` per record, `:166-186`), so the two follow one rule.

## 6. m-3, m-4 (TESTED) — CLOSED
- First check's M7, adapted to the head's text (the release's `write_anchor(.., PENDING, &post)?` removed), own worktree and target: **KILLED** by `tests::fix_round::m3_a_stop_inside_a_release_opens_on_its_pending_anchor` and `tests::fix_round::m2_a_release_whose_current_save_fails_opens_after_a_restart`.
- First check's M9 (text unchanged; `ensure_anchor` ignores a failed save): **KILLED** by `tests::fix_round::m4_a_second_change_is_refused_while_the_anchor_is_unsaved`.
- First check's `qa_m7`, unchanged: stops at the release's store unlinks #0, #1, #2 all open `Pending`.
- Stop-anywhere, release, at the head (clean clone; 17:01-17:14, heavy count 1 at start, my only heavy run): `stop-anywhere: 323 filesystem operations in the scenario (19 steps)` / `323 stop points reached, 243 of them also with the unsynced directory change undone; (a) to (d) held at every one`, ok (794 s). **EQUAL to the builder.**

## 7. Mutants of the fix (own worktree and target dir each; the crate's tests without the two long ones, and the survivors also against the two long ones)
| # | Mutation | Result |
|---|---|---|
| Mu1 | `release` removes pending unconditionally | KILLED `fix_round::m2_a_release_whose_current_save_fails_opens_after_a_restart` |
| Mu2 | `OwnSeatAt` measured with `seat_usage(own slot)` (source mutant) | KILLED `triggers::m1_member_requests_never_make_the_own_seat_trigger_due` |
| Mu3 | `set_limits` stores `cfg.limits` on a refused offer | SURVIVED, long tests included. **EQUIVALENT**: after the fix, `cfg.limits` is read only at `host.rs:961` when there is no member (`before` is None), and every caller of `reopen` holds a member. The value is never observable. M-3 (a) is a no-op behind M-3 (b) |
| Mu4a | `pending_held` clear dropped on `release`'s error path | SURVIVED, long tests included. **EQUIVALENT**: `reopen` clears it at `:960`; if `reopen` fails earlier, the host is closed |
| Mu4b | dropped on the `SealStaleTwice` path | SURVIVED, long tests included. **No effect REASONED**: pending is removed on that path. If that removal also fails, the leftover is an uncommitted plan's post-seal anchor, which no store accepts (it names segment k+1), so the open falls through to current. The flag is reset by the next step 4, release or re-open. And the path needs a stale plan, which only the test hook makes |
| Mu4c | dropped on the stale-retry plan-error path | SURVIVED, long tests included. Same argument as Mu4b |
| Mu4d | (extra) dropped at seal step 4 | KILLED `fix_round::m1_a_failed_promotion_leaves_no_pending_that_hides_a_later_loss` |
| Mu5 | `load` counts the exempt slots again | KILLED `store::m2_a_store_past_its_bound_by_an_exempt_slot_opens_again` |
| M7, M9 | first check's | KILLED (section 6) |
Survivors are findings by the brief's rule. All four are argued equivalent or without effect (Note N-r2-3). None leaves a real fault untested.

## 8. Red runner (TESTED)
- `bash scripts/red-controls-audit-host.sh`, own `COAGENT_AUDIT_HOST_RED_TARGET` and `_LOGS`, clean clone, 17:14:50-17:29:43, heavy count 1 at start.
- `names: 14 red controls, each in build.rs, used under src/ and a row`; **14 rows RED**, each on its own evidence text. The 12 earlier rows have the first check's texts. The two new rows:
  - `own_seat_counts_requests` → `M-1: a member's recording requests made the own-seat trigger due (at 1 %: due Some(OwnSeatAt(Percent(1))), seal Ok(1))`
  - `release_no_pending` → `R7: a stop inside a release left a folder that will not open on its pending anchor (Current)`
- `GREEN: 58 tests ok`; `RED CONTROLS OK`; exit 0. **EQUAL to the builder.**

## 9. Property (TESTED)
- Release, my seed `0x5eed2b2b0ddc0de5`, 1,024 × 40, clean clone, 17:29:58-18:00:52 (1,853 s), heavy count 1 at start.
- `reach Reach { seals: 2874, stale_plans: 601, queued_calls: 16173, restarts_in_seal: 821, full_seat: 972, nothing_to_seal: 1668, releases: 340, peer_seals: 1179, restarts: 2553, triggers_refused: 2845, stops_after_commit: 381 }`, ok. **Every required reach count is above zero.**

## 10. Docs and BACKLOG (READ)
- §4: the new LimitsChanged paragraph (`:84-90`) and the anchors paragraph on pending removal (`:97-100`) match the code. The §3 P-4 bullet (`:55-59`) was not updated for LimitsChanged (N-r2-1).
- §6: the trigger paragraph is corrected, with a dated "Corrected in addendum 1" note, and matches `admit`. The N-1 sentence is present (`:152-154`). The release paragraph is updated.
- §9: the store row states the exemption by put and open; the closing paragraph carries the correction note.
- `settings.rs`: module doc lines 3-14 and the `OwnSeatAt` doc are corrected; the claim "nothing a peer sends" now names `free_usage`.
- BACKLOG: the D-S1 BUILT line is kept as written and a `CORRECTED 2026-11-21 … 183191e…` line is appended under it. N-2, N-3, N-4, N-5 are new `- [ ]` entries with Where / Symptom / Why deferred / Discovered, in the file's form. No other line changed.

## 11. Names scan (TESTED)
- All 636 added lines of `git diff 35f7e89 680d333`, case-insensitive, for `/Users/`, `/Volumes/`, `/home/`, `kamil`, `kreiser`, `secuura`, `datasec`: **0 hits**.
- Positive control: a planted line `/Volumes/X Kreiser DataSec` gives 1 hit with the same pattern.

## 12. Findings
None is a Blocker or a Major, and none is in the NO GO list of brief §4. Every §4 item was checked:
- M-1, M-2, M-3 are not reachable by any path I could build (sections 2-4).
- No acknowledged record was lost or recorded twice at 323 stop points (section 6).
- No call reached the member inside a window (red row `seal_interleaved`, property).
- No new Err path hides a change (section 4 ruling).
- `Cargo.toml`/`Cargo.lock` are unchanged, and no protected file or other crate changed.
- Every edit is inside the owned paths.
- Every red row is red on its own text.

**P-r2-1 (pre-existing, Minor; identical at 35f7e89, not caused by this round). A P-4 re-open whose own second write fails answers an Err for a record that LANDED, so a caller that retries on an Err records the act twice.**
- Where: in `mutate` (`host.rs:1120`), `let lr = self.reopen(id, now)?;`. Inside `reopen`, `reoffer_limits` (`write_limits`, `:910`) and `settle_pending` (`save_current`, `:919`) both return with `?`, before `landed` is computed.
- Probe `qa2_p4_then_a_second_write_fails_in_the_reopen` (a local record's store directory sync fails, then one anchors write fails):
  - `limits`: `answer Err(Dir(Io { what: "create a temporary file", name: "anchors/limits" })); own seq 3 -> 4 (landed true); a retry on the Err -> Ok(Recorded(5))`.
  - `current`: `answer Err(AnchorNotSaved); own seq 3 -> 4 (landed true); retry -> Ok(Recorded(5))`.
- The same probe at 35f7e89 (worktree `base/`, with only the test-only `FailEvery` rule added) gives the identical lines. So this is not a new path, and not the §4 NO GO.
- It breaks the docs' P-4 promise (`docs/AUDIT-HOST.md:58-59`, "so the caller never records it twice"). It needs two failures in one call, for example a full disk.
- The first check did not report it. **For BACKLOG** (I cannot write the project): compute `landed` even when the re-open's later steps fail (for instance return `Reopened { landed, .. }` carrying the second error), and add a test. To fix before the daemon is wired.

**Notes.**
- N-r2-1: `LimitsChanged` carries only Err answers today (section 4), but nothing in the type or in `apply`'s doc stops a future `Ok(Recorded)` inside it from being missed, and docs `:58-59` still promise `Recorded(n)` for a landed record. Suggest:
  - a sentence in the P-4 bullet and on `apply`: "an `Err(LimitsChanged)` may carry a successful answer: unwrap `answer`, never retry on it blind";
  - my N1-through-the-host probe as a test, since the builder's differs test is a unit test only.
- N-r2-2: `release`'s Ok branch returns early through `?` (re-encode / second archive write, `host.rs:1188-1189`) without clearing `pending_held` and without saving current. It is not reachable unless the dry and real release bundles differ. The `?` predates the round; the flag is new.
- N-r2-3: mutants Mu3, Mu4a, Mu4b, Mu4c survive and are argued equivalent or without effect (section 7). Mu3 shows that M-3 (a) has no observable effect after M-3 (b), which is harmless.

## 13. What I could not run, and the end state
- No fault-injecting filesystem of my own (the builder's injector was used, as in the first check). Windows is not compiled. No model runs, no push, no merge, no edit in the project.
- End, 2026-11-21 18:02, `git ls-remote` on the GitHub remote: `audit-host` = `680d3333c8713fc12f140068b2a3a985d96c4681` (**did not move**). `main` = `a034263b474d775d0e965e6234d7a446efc45425` (**MOVED** during the check, from `16e83fb`, through the RELAY-RECONNECT and W-KIT merges). Since `16e83fb`, main changes neither `Cargo.lock` nor any audit-host path; it changes `BACKLOG.md` (+93/−1), which the branch also changes. Every figure here is at `680d333` against `35f7e89`. The merge, and the BACKLOG reconcile it needs, belong to Friday's merge check, as briefed.
- Processes: none of mine left running. (Two `cargo test --workspace` processes from the project's own toolchain were running at the end; they are not this seat's.)
