VERDICT: GO WITH NOTES — head 104dd394c390b614410cdba76ac45eeffa6bb220

# Gate RELAY-RECONNECT r2 (the short re-check of the fix round): branch `relay-reconnect` at `104dd394c390b614410cdba76ac45eeffa6bb220`

Re-check, 2026-11-21, 14:23 to 15:08. Findings only. I fixed, committed, pushed and merged nothing. In the project folder I wrote only my status file. Every other write went to `/private/tmp/claude-501/qrr2`, the session scratchpad, or this folder. My probes, mutant script, logs and heavy-slot record are in `gate_relay_reconnect_r2_tests/` beside this file.

- **Heads (TESTED).** `git ls-remote` of the GitHub remote at 14:24 and again at 15:06: `relay-reconnect` = `104dd394c390b614410cdba76ac45eeffa6bb220`, `main` = `16e83fbe5592658ddcda769d7827895941eca678`, main is an ancestor of the head. The builder's STATUS last line is `READY FOR QA RELAY-RECONNECT r2`.
- **Marks.** TESTED = I ran it. READ = I read the source at the head. A builder figure is cited only where my own run matched it.

## BLUF (for the owner, in plain words)

1. **The dead-link fault is closed.** If the other side ends a session and a new invitation (or join) follows within a tenth of a second, it now works every time. I tried it six different ways, 20 times each: no invitation lost, and none reused the old link. The same tests on the old code lost most of their invitations, so they really do catch the fault.
2. **Nothing ordinary changed.** Twenty normal invite, talk and end cycles all worked, each with a fresh link. The new code never ran in any of them. The builder's earlier protection tests all pass.
3. **Nothing a person would notice.** The fix is two small blocks, exactly where you allowed them. No protected file changed.
4. **Two notes for later (not blocking).** The "join" half of the fix is covered only by my test, not by one of the builder's. Also, the builder's randomised test does not always reach the race on every seed. Neither affects you.

## Findings

No Blocker, no Major, no Minor. Notes only:

| id | sev | what | input that shows it | exact output seen | file:line |
|---|---|---|---|---|---|
| R2-1 | Note (test gap) | The `cmd_join` half of the fix has no builder test. Mutant mj (the block removed from `cmd_join` only) passes the builder's `rr_window` (2 of 2). It is killed only by my probe `qrr2_d_host_joins_a_third_party_inside_its_window`. Without the block, a host that joins a third party inside its window leaves the ENDED session's relay and guard running for good, because the new session replaces the ended one before the tick sees it. The fix is right; only the builder's coverage is missing. | mj, `QRR2_N=10` | rr_window: "20 rounds, 0 lost" / "0 with the old pin" (ok); qrr2_d: "10 rounds, 8 lost": "round 0: the ended session's relay/guard [80080, 80079] still running 600 ms after the new pair" | `engine.rs:1434-1453` |
| R2-2 | Note (property reach) | Layer (b)'s race is drawn only when both sides are connected at that step, as the builder says. At my seeds 4241-4246 it raced once in six seeds. The group 4241-4243 drew none, so its own reach assertion failed ("reach: an invitation raced against the guest's end"). No invariant was violated: I6 held on all six. The builder's seeds 0-11 raced 9 times. The direct window tests carry the race. | my copy `qrr2_property.rs` | seed 4241's race step came right after a SIGKILL restart and ran as the ordinary end; 4245: race reach (1, 1) | `tests/rr_property.rs` (race guard on `connected`) |
| R2-3 | Note (READ) | `cmd_join`'s block runs before the blob is parsed. After the peer's end, an unreadable join therefore runs the ended session's clean-up at once. That is the same clean-up the tick would run within 100 ms, so it is harmless. | READ | — | `engine.rs:1434-1454` |
| R2-4 | Note (method) | Two of my six window probes do not fail at `baa9a11`: the guest joining a third party, and a host restart between the end and the invite. Those states were never faulty: the guest holds no relay, and a restart starts with none. They are neighbour checks, not proof of the fix. The other four fail there (below). | wb runs | qrr2_e: 0 lost of 10 (fails at baa9a11 only on its reach line); qrr2_f: 0 lost of 10 | — |

RR-3 stays open in BACKLOG (line 772, unchanged). RR-4 to RR-7 stand as the first verdict ruled them.

## Rulings per item (brief §5)

1. **Scope (READ + TESTED). Clean.**
   - `git diff baa9a11 104dd39 -- engine.rs`: +43 lines, 0 removed. It holds only the block at the start of `cmd_invite` (:1317-1339) and the block at the start of `cmd_join` (:1434-1453). Each is the tick's edge (:2655-2671) repeated verbatim, with the same `ended_cleanup_repeats` condition, plus one log line ("the peer's end was applied before this command"). No new function and no new field.
   - Readers of the ended flag: only the new ones were added. `session_active` is called after the block, so it sees the session already cleaned. `status` shows the relay gone sooner, as the builder lists.
   - The round's own commits (`bf41cac`, `3459026`) touch BACKLOG.md, engine.rs, tests `rr_property.rs`, `rr_store.rs`, `rr_window.rs` (new), docs/DAEMON.md and scripts/red-controls-daemon.sh: all inside addendum 5's closed list.
   - The merge commit equals `git merge-tree` of `3459026` with `16e83fb`, except the BACKLOG conflict markers. 0 lines of either side were removed from BACKLOG.
   - `git diff --stat origin/main...104dd39`: 21 files, +5,328 −65. That is the r1 list of 20 plus `tests/rr_window.rs`.
   - Protected files: 24 of 24 sha256 recomputed from `104dd39`, all equal to the builder brief's §0.3 table. Tree oids `tests/gate` d9578cd094be5f52db7ee7d1d753010153ecf1cd and `tests/common` 6ed351ad7dde36aee5d046d2deaf57e0aed38f8f are equal.
2. **RR-1, both forms of the race (TESTED). Closed.**
   - Builder's `rr_window` at the head: 20 rounds, 0 lost (applied by the invite in 18 rounds); 20 rounds, 0 with the old pin (applied in 19).
   - My probes (`qrr2_window.rs`, 20 rounds each, all at the head, real daemons):

     | probe | lost | old pins | end applied by the command |
     |---|---|---|---|
     | a: two invites back to back inside the window (the second must be `session_active` and must not touch the first's relay) | 0 | 0 | 12 |
     | b: an end arriving while invites are in flight (4 clients firing from before the end; 94 refusals answered after the end's reply) | 0 | 0 | 16 |
     | c: the HOST ends; the guest invites inside ITS window (roles swap each round) | 0 | 0 | 17 |
     | d: `join` on the host inside its window (to a third daemon's prepared invitation) | 0 | — | 17 |
     | e: `join` on the guest inside its window (third daemon) | 0 | — | 17 |
     | f: a host restart between the end and the invite (SIGTERM/SIGKILL alternating; 17 rounds stopped while ended with the relay still present) | 0 | 0 | — |

   - **At `baa9a11`** (a worktree of my clone at `baa9a11`, merged with nothing, same probes, 10 rounds):

     | probe | lost | old pins | how |
     |---|---|---|---|
     | a | 8 | 6 | the invitation's relay gone 600 ms later; twice the second invite was even accepted, because the tick had killed the first |
     | b | 8 | 8 | |
     | c | 9 | — | the new host's freshly started relay stopped by the late clean-up |
     | d | 6 | — | the ended relay left running after the new pair |
     | e, f | 0 | — | neighbours, see R2-4 |

   - Builder's `rr_window` at `baa9a11`: both FAIL ("round 0: … join {"error":{"code":"invite_refused" …"; "17 with the old pin"). The builder's claim is reproduced.
   - An invite cannot be mid-way inside the engine across the end: while the session is live, it is refused at once (READ `cmd_invite`). So probe b's queued requests are the in-flight form.
3. **Ordinary paths untouched (TESTED).**
   - `qrr2_g_ordinary_cycles_untouched`: 20 cycles (invite, join, a message each way exactly once, end alternating, the ticks passed). 0 lost and 20 distinct pins. The relay started for each invitation is the one still running after the pairing and the messages, and the new block's log line appeared 0 times.
   - `rr_repro` 12 passed, with `rr_d_v` (the protection) green. `rr_store` 5 passed.
4. **Mutants of the fix (TESTED; each in its own worktree and target dir):**
   - mi (block removed from `cmd_invite` only): KILLED by builder `rr_window` (both tests) and my a, b, c.
   - mj (block removed from `cmd_join` only): KILLED only by my d, see R2-1.
   - mn (`ended_cleaned` set, `end_session` not called, in both blocks): KILLED by builder `rr_window` (both: "reused the ended session's relay true"; "18 with the old pin") and my a, b, d.
5. **Red control `ended_cleanup_repeats` ALONE (TESTED).** `COAGENT_RED_RR=ended_cleanup_repeats`, build plus `--exact rr_e_invite_inside_the_window_before_the_tick`, run as the runner does: exit 101. The first panic line is "an invitation made inside the window was lost: [" (its own text). The appended row RR-A5 was READ and is as the builder states (146 rows).
6. **RR-2 (TESTED).** `rr_store_when_the_save_fails_no_unsaved_identity_is_used` passes at the head. With m2 applied (save-failed branch: `return Err(t)` replaced by using the identity anyway), the test FAILS: "the invite must fail when the identity cannot be saved: {"id":7,"ok":true,…". m2 is killed.
7. **Property (TESTED).**
   - Builder's seeds: 5 passed. Layer (a), seed `0x5eed202611200001`: 200,000 sequences, 4,105,495 steps, I1-I5 held. Layer (b), seeds 0-11: I6 held, race reach (3,3), (3,3), (1,1), (2,2).
   - My seeds (a copy changing only the seeds): layer (a) `0x0b0b5eed20261121`, 200,000 sequences, 4,107,342 steps, I1-I5 held. Layer (b) 4241-4246: I6 held on all six; race reach 1 in total, see R2-2.
8. **Docs and BACKLOG (READ).** DAEMON.md §2's new sentence ("an `invite` or `join` that arrives after the peer's end but before the next tick first runs the ended session's clean-up…") says exactly what form (b) does. RR-3 is open in BACKLOG. Q1's closed entry has one line added.
9. **Names scan (TESTED). Clean.** Over the round's own 381 added lines (`git diff baa9a11 3459026 -- crates docs scripts BACKLOG.md`; the merge adds no line to the daemon, DAEMON.md or the runner), the pattern `/Users/|/Volumes/|/home/|kamil|kreiser|secuura|datasec` (case-insensitive) has 0 hits. Commit bodies baa9a11..104dd39: 0 hits. A planted control line: 1 hit.

## What I reused
- From the first check's `qrr_q1.rs`: `pair_talk`, the ender thread and the pin decoding, CHANGED: 20 rounds, losses counted with recovery, new states. Its `mutate.py` was used UNCHANGED as a helper.
- The builder's `rr_window.rs` was copied UNCHANGED into the `baa9a11` worktree.

## NOT TESTED
- `scripts/check.sh`, `red-controls-daemon.sh` whole, `test-daemon.sh`: not run, per brief §3 (Friday's merge check runs them).
- A join on the guest to a third party while the guest's OWN pairing is pending (no such state: `session_active` refuses it).
- Windows.

## Processes
None left running: no `coagentd`, relay, guard, cargo or watcher of mine (checked with `ps` at 15:06). My clone, worktrees (`wb`, `mi`, `mj`, `mn`, `m2`) and target folders stay in `/private/tmp/claude-501/qrr2` (scratch, never in the project). Every heavy run started at a heavy count below 3 (`slots.log`). No failure came from a run that overlapped two other heavy jobs. Every failure seen is a mutant, `baa9a11`, the red build, or the reach line in R2-2.
