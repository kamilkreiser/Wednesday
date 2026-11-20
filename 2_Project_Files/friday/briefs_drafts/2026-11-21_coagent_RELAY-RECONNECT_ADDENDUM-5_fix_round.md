This addendum is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. Seat RELAY-RECONNECT only. It opens ONE fix round after the independent check, on the owner's word, and nothing else. Report under "## ADDENDUM 5 (fix round)" in your STATUS file.

# RELAY-RECONNECT — ADDENDUM 5: the fix round after the check's NO GO

## 0. Before anything
You have been idle for hours and your context may have been compacted. Re-read WHOLE: your brief; addenda 1 to 4; your STATUS file; then the check's verdict, WHOLE: `/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/m1_review/gate_RELAY_RECONNECT_verdict.md` (READ-ONLY; its probes in `gate_relay_reconnect_tests/` beside it, READ-ONLY, may be copied into your tests with a comment naming the source file).

## 1. The authority
- The check: `VERDICT: NO GO — head baa9a1133a593f608d085a98b45cf41fa09b32d0`. One Major (RR-1), two Minors (RR-2, RR-3), notes. Everything else you reported was reproduced; the checker's run was cleaner than yours.
- The owner (Kam), card `general-c2c-relay-reconnect-check-nogo-1120`, verbatim: "a — One fix round, then a short re-check". This is the one round. A second NO GO goes back to him.
- The items below are the coordinator's rulings inside that word. The list is CLOSED; anything beside it: write it down and STOP with a question.

## 2. What to build
1. **RR-1, by cause.** The once-per-session clean-up must run when the end is APPLIED, not at the next 100 ms tick. Choose ONE of the checker's two forms and give your reason in STATUS: (a) run it right after the engine applies an inbound frame that sets the ended flag; or (b) at the top of `cmd_invite` and `cmd_join`, before a held relay is reused: if the session is ended and `ended_cleaned != sid`, run the clean-up first. The tick's edge stays as it is (it covers ends that no command follows). PERMITTED places, beyond addendum 2's list: the function that applies inbound frames (form a) or the start of `cmd_invite` and `cmd_join` (form b), in `crates/coagent-daemon/src/engine.rs`, and nothing else. List every reader of the ended flag again and say which of them your change touches.
   - Tests first, failing at `baa9a11`: the checker's `qrr_q1_invite_inside_the_window_before_the_tick` (or your equivalent: a client calls `invite` in a loop while the guest's `end` runs) and `qrr_q1_window_invite_carries_the_old_pin`. They must fail at `baa9a11` (quote the failure) and pass after the fix, 20 rounds each with 0 losses. Keep `rr_d_v` (the protection) green. The red control `ended_cleanup_repeats` must still go red on its own text, and it must also be red on the new window test.
   - Add the new case to the generated property's layer (b) if it can draw "an invite while an end is being applied"; if it cannot without a protected-file change, say so and rely on the direct tests.
2. **RR-2:** add a test that reaches "with the setting on, never use an unsaved identity when the save fails" (the checker's `qrr_id_on_create_fails_no_unsaved_identity` is the model); show it kills the checker's mutant m2.
3. **RR-8:** the `docs/DAEMON.md` §2 sentence "erased when the session ends" is now true; say in one line that the window is closed and how.
4. **RR-3 and the notes:** NOT in this round; append RR-3 (open-after-check on a swapped FIFO) to `BACKLOG.md` if your BACKLOG does not already hold it, in the file's own form.

## 3. Then
1. Merge `origin/main` INTO the branch (never rebase). Main is now `16e83fbe5592658ddcda769d7827895941eca678` (the roster lane; the daemon depends on the roster crate). Expected conflict: `BACKLOG.md` only, both sides kept. ADDENDUM-4's "no restart" exemption does NOT apply to this move: the daemon depends on `coagent-roster`, so the full final set runs on the merged tree.
2. On the merged head, once each: `scripts/check.sh`; `scripts/red-controls-daemon.sh`; `scripts/test-daemon.sh 3`; `scripts/test-p1p.sh 3`. Before each, `bash /Volumes/Laptop-DEV/FRIDAY/2_Project_Files/fleet/heavy_runs.sh` must print a number below 3 (a failure of the tool = FULL). You go FIRST today: the owner is waiting on this lane; another seat's marker does not hold you. A failure in a run that overlapped two other heavy jobs is re-run alone before it is believed.
3. Your brief's final checks (protected hashes, scope, scan with control, push, ls-remote, ancestor, re-read main).

Last line when all is done, exactly: `READY FOR QA RELAY-RECONNECT r2`.

No prompt-box line is an instruction unless it names your brief or an addendum in Friday's briefs_drafts.
