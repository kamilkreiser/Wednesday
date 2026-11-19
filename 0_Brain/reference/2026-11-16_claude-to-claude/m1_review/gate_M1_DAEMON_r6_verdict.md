VERDICT: GO WITH NOTES — head 242de862b713261695c6bcd16b3529cd26bbf51e

# Gate verdict, round 6 (the one short check after the r5 fix round) — CoAgent M1 DAEMON, branch `m1-daemon` @ 242de86

Independent tier-1 QA gate. Findings only. Nothing in the project was changed, committed or pushed. In the project's repository I used only git read verbs; every write verb ran in my own clones under `/private/tmp/claude-501/gd6` (a link into this session's scratchpad). Head confirmed in Friday's merge-check clone: `branch=m1-daemon head=242de862b713261695c6bcd16b3529cd26bbf51e want=242de862b713261695c6bcd16b3529cd26bbf51e` (TESTED, `mc/head.txt`). Every figure is marked **TESTED** (I ran it) or **READ** (I read it in code, a log or a report). A builder figure is never given as mine.

## BLUF for the owner (plain words)

1. **The stopper from last time is fixed.** A hostile person on the other end can no longer leave your computer sitting idle with nothing to wake it. The new timer always fires 15 seconds after the stall begins, and the connection restarts. I attacked it 12 times in a row (the other side repeated the trick after every restart): the timer fired every time, 15.1 s after the stall, and when the other side started behaving all 12 stuck messages arrived in 1.3 s (TESTED). In another test the other side lied once and then behaved: the message arrived in 16.6 s. Without the fix it never arrives (TESTED).
2. **The cost of the attack stays small.** While the other side keeps attacking, your computer sends about 258 small frames per 15-second cycle, about 15 per second (TESTED). That is the same order as what such a peer could already cause before this round.
3. **Everything else asked for is done and holds.** The "out of step" flag now clears; the flaky check was retired for a sound reason, and two other checks (both always red when they should be) still guard what it guarded. Main's audit work merged with no edits hidden in the merge, and it does not touch the daemon. Friday's own clean-copy run passed: the full project check, and all 116 planted faults caught (TESTED).
4. **Small notes only.** The tests the builder wrote do not pin the new timer's 15-second value: a copy with the value doubled still passed every builder test, and it was caught only because one counter fell to zero. The timer is also filed under the same name as an older timer. Neither blocks the merge.

## 1. Findings

| id | sev | what | input that shows it | exact output seen | file:line |
|---|---|---|---|---|---|
| R6-1 | Minor | **Row 54's clock value is not pinned by any property's assertion in the branch's tests.** A mutant that doubles the clock (deadline and tick, 15 s → 30 s) passes G5-1, G5-1c, every `recovery_model` property's V5/V4 assertions and all of `gate_r5_model`. It is killed only by the generated property's **reach count**: its 2 clock fires (out of 40 seeds) fall to 0. This is the R4-7 pattern: each clock's value is pinned by a named test. The check's own G6-1 does pin it. | Mutant M1 (`mut6.py`): `d.push(t + self.cfg.rto * 2)` and `> self.cfg.rto * 2` in `skips_stuck`. Ran `gate_r5_model` + `recovery_model` (all 51 tests), then my G6-1. | Branch tests: `gate_r5_model` "5 passed; 0 failed"; `recovery_model` "45 passed; 1 failed": the one failure is "V5/V4 hostile peer (R5-1): rule `skips_clock_fired` was never reached (reach is counted)" (model.rs:1421, the reach line, not V5/V4). My G6-1: "G6-1: the clock fired 30.1s after the budget was spent (row 54: T-RTO's value, 15s)". | `src/recovery.rs:818-820, 853-857` |
| R6-2 | Note | The forward-acknowledgement clear of `skips_spent_at` is not covered by any test. A mutant that refills the budget on a forward acknowledgement but leaves the clock running survives every branch test and my G6-1/G6-2. Effect (REASONED): at worst one extra RESYNC 15 s after a budget that was spent and then refilled. It never stops a sender, and an honest pair never spends the budget (with 128 in flight at most, every in-flight trim from an honest peer comes with a forward acknowledgement). | Mutant M4: the line `self.skips_spent_at = None;` in `on_inbound`'s refill removed | branch tests: "5 passed; 0 failed", "46 passed; 0 failed", test exit 0; mine: "2 passed; 0 failed" | `src/recovery.rs:1969-1973` |
| R6-3 | Note | The new clock is counted under the cause name `"T-RTO"`, the same name as the in-flight clock (row 38). Design 09 §6 rule 3 (isolation) asks a test to assert **which** clock fired; a `resyncs["T-RTO"]` count cannot tell them apart. My tests told them apart by the state before the tick (budget spent and nothing in flight). Row 54 documents the name, so this is not a defect. A separate name (say `"T-SKIPS"`) would make the isolation rule checkable. | READ; G6-1 distinguishes them: "fired by row 54's clock 12" of 12 | `T-RTO resyncs {"T-RTO": 12}` | `src/recovery.rs:2227-2237` |
| R6-4 | Note | What a hostile peer can make the new clock cost, measured: one RESYNC, one re-attach and at most 256 skips per cycle of about 15.7 s; 15.5 frames/s toward the peer, sustained over 12 cycles. That is bounded and the same order as T-RTO's existing cost (128 in flight per 15 s) and far under R5-4's full/room pairs (6,400 frames in 15 s, r5). There is no fast loop: the engine ticks every 100 ms whatever `next_deadline` says (READ `engine.rs:379`), and each fire goes through the backoff and the attachment bucket. | G6-1 (12 cycles) | "per cycle (frames side 0 -> peer, spent->RESYNC, cycle time): [(256, 15.1s, 15.7s), (258, 15.1s, 15.7s), … ×11]"; "total 201.6s, frames side 0 -> peer 3116 (15.5/s); T-RTO resyncs {"T-RTO": 12}; reconnects 12" | `src/recovery.rs:1157-1177` |
| R6-5 | Note | The builder's generated property does not draw two things a hostile peer can send: **sequenced messages** (in order, gap, duplicate, huge), and **key exchanges started by the peer**. The first is covered by the check's G6-3 (297 hostile messages across 120 seeds; green). The second is NOT TESTED; by reading, `install` clears the clock and keeps `skips_left`, and the new channel's first position refills it (`:1689-1703`), while row 27 covers the wait for that position. | G6-3 | "G6-3: 120 seeds; ticks with the budget spent and nothing in flight 4094; row 54 clock fired 7; hostile messages 297; cuts 431"; "test result: ok. 3 passed" | `tests/recovery_model.rs:3321-3363` |

**Counts: Blocker 0, Major 0, Minor 1, Note 4.**

**Why GO WITH NOTES.** Every r5 finding is closed, and the R5-1 fix holds against every sequence I could build: 12 repeated forgeries, the builder's own "(a) alone leaves a gap" ordering with an honest peer, and 120 generated seeds that add messages, long silences, drops and cuts. In all of them V5 held, V4 held, and the cost stayed bounded. Each of my tests goes red without the fix, on its own V5 text. The new rule did not break anything earlier rounds verified (check.sh, the runner and the clean run are all green in Friday's clean clone). What remains is one Minor (the clock's value is unpinned) and four Notes.

## 2. Rulings on items 1-6

1. **R5-1 fix, choice (b): SOUND.** The deadline is armed by the stall condition itself: `skips_spent_at` is set at the skip that spends the budget (`:1781-1785`), and `skips_waiting()` returns it while `next_out < send_next` and the peer is not full (`:842-851`). `next_deadline` adds `+ rto` (`:818-820`), and the tick RESYNCs when it has passed and the link is attached (`:2234-2237`).
   - *A wait with no deadline (V5)?* `skips_left` reaches 0 only inside `pump`, which sets the clock at that moment. The clock is cleared only together with a refill (`:1703`, `:1972`), or by `install`/`drop_link` (`:1288`, `:1135`). After `install`, `pos` is `None`, so the pump cannot run until the first position, which refills (`first`); row 27 covers the wait for that position. After `drop_link` there is no channel, and the reattach clocks run. With the peer full, T-HELD covers it (`held_since` is set with every `full`). I found no sequence that reaches "budget 0, a number to send, nothing in flight, peer not full" without the clock (REASONED; TESTED by G6-1, G6-2, G6-3 and the builder's property: V5 never false).
   - *Outbox undelivered 120 s after the peer turns honest (V4)?* The worst cases I built were G6-1 (all 12 delivered 1.3 s after the peer turned honest), G6-2 (16.6 s), and G6-3 (120 seeds, all within 120 s, after the instrument fix in §7).
   - *Unbounded loop?* None. The cost is R6-4: bounded per cycle and per second.
   - *The builder's case against (a) alone:* confirmed. G6-2 (one forged acknowledgement at the top, then an HONEST peer) stalls with no deadline without the clock: "G6-2 (V5): waited 119.5s with no deadline … skips_left 0 … next_out 385 send_next 1002 pos Some(1000)" (TESTED under `skips_no_clock`). In that run the honest peer's positions and acknowledgements (≤ 1000) never move past the forged `peer_acked`, so (a)'s "refill on a forward position" would not refill either (REASONED).
   - *Row 54:* the text matches the code (READ `docs/DAEMON.md:321`, §3 `:220-222`).
2. **The generated property: GENUINE, but its exercise of the new path is THIN; supplemented.**
   - *Red on V5's own text:* yes. Runner row A12-R5-1 panics at the property assertion `recovery_model.rs:3578` with "V5 (R5-1, hostile phase): side 0 at 15.7s waits with no deadline: … skips_left 0 skips_spent_at Some(15.3s) next_out 257 send_next 303 (seed 4 …)" (TESTED).
   - *Reach reproduced exactly:* `{"budget_exhausted": 1975, "outbox_waiting_when_honest": 38, "position_above_acknowledgement": 346, "refilled_by_a_position": 60, "refilled_by_an_acknowledgement": 30, "skips_clock_fired": 2}` (TESTED, `log_property_reach.txt`).
   - *Alphabet:* it draws `full`, `resume` ± `room`, and acknowledgements on their own, at positions {0, 1, half, top, above top, u64::MAX, random}, plus the trim pattern, silence, honest traffic both ways, and relay drops, duplicates, reorders, holes and cuts (READ `:3309-3363`). Missing: peer sequenced messages and peer key exchanges (R6-5). `budget_exhausted` counts ticks, not episodes.
   - *Two fires in 40 seeds is not enough:* the value mutant shows it (R6-1).
   - *Targeted tests:* G6-1 makes the clock fire 12 of 12 times at 15.1 s, G6-3 makes it fire 7 times, and both are red under `skips_no_clock` on their own V5 text (TESTED).
3. **The link task's attach-reply clock: REAL; it always fires in that state.**
   - `await_ok` takes one absolute deadline, `now + REPLY_BUDGET` (10 s), and waits with `timeout_at` (READ `link.rs:229-238`). Data frames, presence lines and dropped frames that arrive meanwhile are held or skipped, and none of them moves the deadline.
   - On expiry it returns "relay did not answer". `run_link` closes the connection and returns (`:328-331`), `spawn_link` sends `LinkEvent::Down` (`:222-225`), and the engine drives `Event::LinkDown` (READ `engine.rs` `on_link`), which calls `drop_link` and schedules a reattach (`recovery.rs:977-984`).
   - The convener's re-create path chains up to four such waits (≤ 40 s), and the connect stage has its own 5 s per candidate (`link.rs:21`, relay `client.rs` `connect_candidates`). Every one of these is bounded.
   - The model mirrors this (`model.rs:1191-1195`). Not a new finding.
   - One residue (REASONED, Note-level, not counted): `send_text(&open)` before `await_ok` has no timeout of its own. On a fresh TLS connection one small frame does not fill the socket buffer.
4. **R5-2: CLOSED.** The tail clear is at `:1803-1805`. G5-4 is green (check.sh, TESTED), and mutant M3 (the clear removed) is killed by G5-4 on its own text: "G5-4 (row 54 status): the pump passed every missing number (next_out 301 send_next 301) but desync is still shown" (TESTED).
   **R5-3: retirement JUSTIFIED; the property is still guarded.** The reason is written in the runner (READ `red-controls-daemon.sh:155-164`). The guards were red on their own text in Friday's run (TESTED):
   - F-J (real processes; its setup forces a channel up while 40 messages are held, the condition A5-3 lacked): "R4 POSITION: after the cut A sent 301528 bytes although the peer held every message (A's outbox held 40 at the cut)".
   - V3 (model, deterministic): "V3 answers_are_bounded: side 0, second 0 of the flood: … 64 o…" (the line as the runner printed it, cut at 150 characters).
   - V12 under `no_inflight_limit`: "V12 honest_runs_are_quiet: side 0: attachments 2, relay refusals 2, …".
   - The gate file `gr3.rs` is unedited.
5. **The merge of main `bfe435a`: CLEAN; no interaction with the daemon.**
   - `242de86` has parents `540645f` and `bfe435a` (TESTED). The patch it adds over `540645f` has the same `git patch-id --stable` as main's own change since the merge base `f33482b`: `6dd922f08388b248c7053d6b412e46cb411787ac` both (TESTED), so no edit is hidden in the merge.
   - `git diff bfe435a HEAD` on the audit/policy paths is empty (TESTED).
   - Every file that differs from main is under the daemon's allowed paths: 0 outside, 51 under `crates/coagent-daemon/` as a positive control (TESTED).
   - Main's changes are in `crates/coagent-audit` (Cargo.toml test entries, `session.rs`, tests), `docs/AUDIT.md`, `scripts/red-controls-audit.sh` and BACKLOG (READ). Neither `coagent-daemon` nor `coagent-mcp` depends on the audit or policy crates (READ Cargo.toml; `git grep coagent_audit|coagent_policy` in both crates: 0 hits, with `coagent-relay` found as a positive control).
   - Main's BACKLOG adds obligations "for the daemon lane" (call `try_set_limits` after every audit `resume`). They are future work for when the daemon wires the audit log, not a defect of this branch.
6. **The gate files: AS CLAIMED.**
   - `tests/gate_r5_model.rs` at the head is byte-identical to the r5 check's copy: `cmp` same, sha256 `022f47049bce6688760d28876de0fcf51132b003490957a54ef50c3acb5f33da` both (TESTED).
   - `git diff 0e0e26b HEAD` over `tests/gate/`, `tests/common/`, `gate_r2.rs`, `gate_return.rs`, `gate_r3.rs`, `gate_r4.rs` and `gate_r5_model.rs` shows only "gate_r5_model.rs | 332 +" (TESTED). So `gr3.rs` is unchanged since r5, which verified its ruled edits.
   - The only other test files changed since `0e0e26b` are `recovery_model.rs` (the property) and `support/model.rs` (`skips_waiting_now`), plus `coagent-mcp/build.rs` (the red-control name).
   - `gate_r5_model`: 5 of 5 ok in check.sh (TESTED).

## 3. Each r5 finding

| r5 | status | evidence |
|---|---|---|
| R5-1 Blocker | **CLOSED** | G5-1 and G5-1c green, unedited (check.sh, TESTED); ruling 1; G6-1/2/3 |
| R5-2 Minor | **CLOSED** | ruling 4; M3 killed by G5-4 |
| R5-3 Minor | **CLOSED (retired, justified)** | ruling 4; runner 116 of 116 RED in Friday's run (TESTED), unlike r5's STILL GREEN |
| R5-4 Note | bounded as stated | asserted in the builder's property (READ `:3517-3529`); the new clock's cost is in R6-4 |
| R5-5, R5-6 Notes | no action asked | unchanged code paths (READ diff) |

## 4. What I ran

| run | result | when |
|---|---|---|
| `coagent_merge_check.sh /private/tmp/claude-501/gd6/mc m1-daemon 242de862… scripts/red-controls-daemon.sh` (Friday's tool: clean clone from the local repo, `cargo fetch --locked`, check.sh, runner), exit code captured in the same command | **TESTED: `MC_EXIT=0`**, "MERGE CHECK OK m1-daemon 242de862b713261695c6bcd16b3529cd26bbf51e" | 15:22 to 17:22 |
| └ `scripts/check.sh` | **exit 0**, "CHECK OK: fmt, clippy, test, deny all passed", "licenses ok"; **1106 passed, 0 failed, 20 ignored over 144 binaries** (equal to the builder's A12.6) | 15:22 to about 16:28 |
| └ `scripts/red-controls-daemon.sh` end to end | **exit 0**; **116 rows: 116 RED, 0 STILL GREEN, 0 harness errors**; "final clean run: green (26 test binaries; ignored under rulings: 2)", 176 passed, 0 failed, 2 ignored | about 16:28 to 17:22 |
| The builder's property alone, `--nocapture` (reach) | ok; reach as in ruling 2 | after 17:22 |
| My `gate_r6_model.rs` (G6-1, G6-2, G6-3) | final run: **3 passed** in 76.56 s (first run began 17:22:21) | after 17:22 |
| The same under `COAGENT_RED_DAEMON=skips_no_clock` | **3 of 3 FAILED, each on its own text**: G6-1 "cycle 0: V5: side 0 at 5.9s: … skips_left 0 … next_deadline None"; G6-2 "G6-2 (V5): waited 119.5s with no deadline"; G6-3 "V5 seed 7: side 0 at 9.5s: … next_deadline None" | before 17:29 |
| Mutation, branch tests (`gate_r5_model` + whole `recovery_model`, `--no-fail-fast`), one mutant at a time, file restored, `git status` clean (0 lines) afterwards | M1 killed by reach only (R6-1); M2 (tick never fires) killed by G5-1c on V4 text and by reach; M3 killed by G5-4; **M4 survived** (R6-2) | 17:29:28 (M1 start) to after 17:54:40 (M4 start); each mutant's `recovery_model` about 494-505 s |
| Mutation, my G6-1/G6-2 | M1 killed by G6-1 on its own text; M4 survived | before 18:05 |

My builds used a copy-on-write clone of the merge check's target (`target_t`) and the merge check's cargo home. Clones: `mc/clone` (Friday's tool, pristine), `t6` (my test file added), `m6` (mutation; clean afterwards; my test file, copied in for one run, removed). Load: the merge check ran alone until 17:22. I started my own tests only after it ended (one heavy job at a time).

## 5. NOT TESTED

- A key exchange started by a hostile PEER while the budget is spent (R6-5; reasoned only).
- R5-1's fix with real daemon processes. It was shown on the model harness, which runs the real `recovery::Machine`; the engine decodes `resume`/`full` into the same kinds (r5 §10).
- `scripts/test-daemon.sh 5`: not run by me. The builder's five runs are READ only.
- My test file: `rustfmt` was not available for the toolchain I invoked it under, outside the repository ("'rustfmt' is not installed for the toolchain 'stable-…'"), and I did not run clippy on it. It compiles and runs in the branch's harness.
- The stale-clock case (a `skips_spent_at` left from an earlier spend, met again later by a full in-flight window): reasoned harmless (one early RESYNC at most), not built.
- Real networks, sleep/wake, Windows, long sessions (as earlier rounds).

## 6. Outputs, disk, processes

Outputs: this file and `gate_daemon_tests_r6/`:
- `gate_r6_model.rs`, `mut6.py`
- logs: `log_merge_check_summary.txt`, `log_red_controls_runner.txt`, `log_g6_model.txt`, `log_g6_red_skips_no_clock.txt`, `log_property_reach.txt`, `log_mutation_branch_tests.txt`, `log_mutation_g6.txt`, `log_g6_model_run1_instrument_error.txt`, `log_g6_3_nofix_diagnosis.txt`

A case-insensitive name scan of the folder found 0 files (the one "t9" hit is the test name `test9_…`). Work dir: 2.6 GB at the last measure, in my scratchpad. Processes: no `coagentd` of mine left (`pgrep … | grep gd6`: 0).

## 7. Instrument errors

- **G6-3, first run: a false V4 failure (5 seeds).** My `Msg(0)` op made the hostile peer send a message with the next number without advancing that peer machine's own counter. Its later honest messages reused the number, and the receiver dropped them as duplicates. Diagnosis rerun with the old instrument (`G6_NO_FIX=1`): the only missing ids were the peer's own, "4 missing ["m1-00000"]", "2 missing ["m1-00001"]". Fixed in the test (the peer's next number moves past a message it numbered itself), then green. Both logs are kept. Nothing from that run is counted.
- My first attempt to write this file's IN PROGRESS line was refused by a workspace hook (the command contained a `cd`), and I did not notice until Friday asked; it was then written.
- One `git merge-tree` in my own clone was refused by a hook as a write verb. I used `patch-id` (read verbs) instead (ruling 5).
