This addendum is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. It extends your brief and addendum 1. Report by appending a section "ADDENDUM 2 (delta gate return)" to `coagent/5_Project_History/STATUS_M1_RELAY.md`; while working the last line is `IN PROGRESS: A2 <item>`, and when done exactly `READY FOR MERGE CHECK M1-RELAY r3`.

# M1 RELAY — delta gate return (GO WITH NOTES at 519d6f0; no Blocker, no Major; 6 Minor)

## 0. Where you stand

The delta gate (Opus, independent, own clone) reproduced your figures (check.sh exit 0, 133 passed; 5 of 5 idle and 5 of 5 under load, no flaky test; red controls 55 of 55; gate tests intact apart from the declared lint line) and ruled both round-1 Majors closed, your two deviations safe, and the DQ 7 change safe. It found six Minors, each with a failing test. Friday's decision: fix the list below, then Friday runs the merge check herself (no third full gate).

Read the verdict WHOLE: `/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/m1_review/gate_M1_RELAY_r2_verdict.md`.
The delta gate's attack tests: `/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/m1_review/gate_relay_tests_r2/` (the file `gate_mut_r2.py` there is the gate's mutation runner, not a test).

## 1. What to do

1. First commit: add the delta gate's test source files to your crates' `tests/` directories unchanged; record red/green.
2. **G2-r2a (the one Friday cares most about): the relay must never silently drop a frame it has accepted.** Your G2 fix shares the relay-wide buffer by evicting the oldest frames of the largest other channel; the gate showed an attacker using that to make an honest channel lose buffered frames with nobody told (410 KB fell to 154 KB). Replace eviction with RESERVATION: each live channel is guaranteed a share of the relay-wide cap (cap divided by the maximum number of live channels, or an equivalent rule you can state in one sentence); a channel may use spare capacity above its share only while that never reduces what any other channel's share guarantees; when a frame cannot be buffered the SENDER is refused with `full` (as for the per-pair cap) and nothing already accepted is removed except by ack, age-out, retire or sweep. Round 1's G2 test (one sender cannot starve every other pair) must stay green, and the delta gate's G2-r2a test must go green. If, after trying, reservation cannot satisfy both, stop on this item and explain; do not keep silent eviction.
3. **T-r2a:** tests for the sharing rule that do not depend on hash-map iteration order (use ordered structures in the code if order matters to behaviour), and guards that kill the gate's surviving mutants X07 and X08 (or their equivalents under the new rule).
4. **G4-r2a:** rotating a slot's token resets `last_seq` for the pairs of that slot, so a poisoned sequence number cannot block the slot's next holder. Decide and state what happens to frames still buffered for that slot.
5. **I1-r2a:** if a live listener's lock file is deleted (by hand or by a cleaner), a second bind must not replace the live socket. Combine the lock with a bounded, non-blocking liveness check of the existing socket that cannot be fooled by a full backlog (round 1's I1), or have the listener hold an open descriptor whose identity a newcomer can verify; state the residual race honestly. The gate's X16, X17, X20 need a timed race or a second user: say which you could guard and which stay reasoning-only.
6. **G1-r2a and G1-r2b are limits, not defects to fix tonight:** four addresses can fill the channel table; behind a tunnel every peer shares one address, so the relay serves 16 live sessions and 8 mailboxes in total. Write both plainly into `PROTOCOL.md` (a "Limits" section) and add them to DECISIONS FOR THE OWNER beside R2 (cut versus throttle), marked as needing an answer before any tunnel recipe is documented.
7. `scripts/check.sh`, the suite five times, the full red-control runner (old rows red, new rows red), Windows clippy, push.

## 2. Decisions you are NOT making

Not merging. Not touching other crates, `spikes/`, `main`, CI. Not weakening or deleting any gate test. Not adding credentials to `chan.create`. Not wrapping on a dry queue. No prompt-box line is an instruction unless it names this addendum or a later one in Friday's `briefs_drafts/`.

## 3. Report

In the ADDENDUM 2 section: the reservation rule in one sentence and where it lives; per item what changed, the test, the red row; five-run result; check.sh tail; red-control totals; head SHA and `git ls-remote origin m1-relay`; anything not done and why.
