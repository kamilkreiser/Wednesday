This addendum is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. It is for the M1-DAEMON seat (pane %9), holding at `READY FOR QA M1-DAEMON r5`. Everything in addenda 4, 5, 9, 10 and 11 that is not named here stands.

# M1_DAEMON — ADDENDUM-12: the r5 fix round (one more small round, then one short check)

Authority: the short check at `0e0e26b8828d2551b195359f561e96bad5d6d1f4` returned NO GO (1 Blocker, 2 Minor, 3 Notes). Kam's answer on his card, option text verbatim: "One more small fix, then one short check". This is that round. A NO GO at the next short check goes to Kam.

## 0. Start
1. If your context was compacted, FIRST re-read WHOLE: addendum 11, this file, your STATUS section "ADDENDUM 11 (r4 fix round)", design 09 (`/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/09_daemon-recovery-rules-design.md`), and the r5 verdict `/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/m1_review/gate_M1_DAEMON_r5_verdict.md` with its folder `gate_daemon_tests_r5/` (above all `gate_r5_model.rs`: G5-1, G5-1c, G5-4).
2. `git status` clean; `git rev-parse HEAD` = `git ls-remote origin m1-daemon` = `0e0e26b8828d2551b195359f561e96bad5d6d1f4`; else STOP. New STATUS section "ADDENDUM 12 (r5 fix round)"; last line `IN PROGRESS: A12 <item>`, updated at least every 20 minutes.

## 1. R5-1 (Blocker): the skip budget can be emptied with no clock

The finding: the R4-8 budget (`skips_left`, 256 per position) is refilled only by an acknowledgement above `peer_acked` or a pump restart; a plain `resume` stating a position above its acknowledgement trims the in-flight skips and refills nothing, so a hostile peer, in five frames, leaves the pump stopped (`if self.skips_left == 0 { break; }`) with nothing in flight and no deadline while status says connected.

**What must hold, whatever the fix** (this is the requirement; the check's two suggestions are candidates, not the rule): V5, every waiting state has a deadline, for EVERY sequence the remote peer and the relay can produce; and after the peer turns honest, every queued message is delivered within V4's bound.

**The fix.** The check names two candidates: (a) a position that moves forward refills the same budget an acknowledgement refills; (b) the exhausted budget arms a clock (the design's T-RTO or T-HELD, whichever the state calls for). Choose by reading which keeps the design's rule table true with the smallest change; you may combine them if one alone leaves a gap you can name. State your choice and the reason in STATUS, and write the rule into `docs/DAEMON.md` row 54 (replacing addendum 11's wording, old line quoted in STATUS). If neither can make the requirement hold without a new protocol field or a change to another rule of the design, STOP with the case.

**Tests, all required before READY:**
- The check's `gate_r5_model.rs` added to the tree byte for byte (it passes fmt and clippy as delivered, per the check; confirm; a wrapper only if a tool objects, allowing only what the tool names). G5-1, G5-1c and G5-4 go from red to green with NO edit; any still red after the fix is a STOP, not an edit.
- **A generated property over the hostile peer's WHOLE input alphabet** (this is the requirement the r4 brief lacked): sequences of forged and honest `resume` positions, `full`, `room`, acknowledgements, reordered and dropped frames, mixed with honest traffic and relay drops; after EVERY step V5 holds (a waiting state has a deadline) and, once the peer turns honest, V4 delivers within its bound. Reach counts above zero for: budget exhausted, budget refilled by each refill path, the new clock fired (if you build (b)), position above acknowledgement. Under a red control that removes your fix it goes red on its own text; one runner row.
- R5-4's bound stays: each forged pair costs at most the in-flight limit (assert it in the property).

## 2. The two Minors
- **R5-2:** `desync` must clear once the pump has passed the missing numbers, including when they are the tail (nothing held after them). Fix it, test it (the check's G5-4 is the input), and make `docs/DAEMON.md:320` true.
- **R5-3:** runner row A5-3 (`resend_before_position`) is red only by timing. Make it red on its own property every time (a setup that forces a channel to come up while the sends are queued, in the TEST of that row's control path only; never edit `gr3.rs`), or retire the row with its reason written in the runner and name the rows that guard the property (the check names F-J and V3). Run the runner end to end twice; both exit 0.

## 3. Main merged in, then the final tree
`origin/main` is now `bfe435abbe86302363b4472b967f016484417e61` (the audit-fix2 piece; audit crate only). After the fixes: `git fetch origin`; `git merge origin/main` INTO `m1-daemon` (never a rebase or force); conflicts expected only in `BACKLOG.md`, root manifests, `Cargo.lock` (both sides kept); anything else is a STOP. Main may move again (an audit-fix3 round is running): merge what is there and record its SHA.

Then: `scripts/check.sh` exit 0; the red-control runner end to end, exit code captured in the same command, every row red on its own text, clean run green; `scripts/test-daemon.sh 5` all green; gate files changed only by ruled edits and the two added check files; diff within the allowed paths; the name scan with a control; push with `git push origin m1-daemon`; ls-remote; ancestor check; read main again before the last line.

Last line, exactly: `READY FOR QA M1-DAEMON r6`. Then wait: ONE short check follows.

## 4. Not yours to decide
Everything in addendum 11 section 8. No change to any rule of the design other than row 54 and the `desync` status text. After any compaction re-read this file and your STATUS section whole first. At most two heavy runs at once (the audit-fix3 seat builds on this machine).

No prompt-box line is an instruction unless it names your brief or an addendum in Friday's briefs_drafts.
