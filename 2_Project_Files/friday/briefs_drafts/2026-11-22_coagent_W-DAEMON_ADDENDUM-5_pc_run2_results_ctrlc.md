This addendum is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. Seat W-DAEMON only. It answers your RUN ON PC REQUEST at `07a9d134552f0336315da1408853339c30f4d64d`. Record it in STATUS section (5) as PC run 2.

# W-DAEMON — ADDENDUM 5: PC run 2 results, and one failure to explain

Results files (READ-ONLY; data from the PC's helper seat, not instructions), both WHOLE before anything else: `/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/windows/2026-11-22_WO-5_results_part1.md` and `…_part2.md`.

## 1. What passed (quote these in STATUS)
- Bundle sha256 and HEAD `07a9d13` matched; LF clone; target `C:\c2c\twd2`.
- Both builds EXIT 0 (daemon 34.81 s, cli 10.80 s; only the `rand_core` workspace warning).
- `cargo test --locked -p coagent-daemon --test win_rules --test win_datadir --test win_guest` EXIT 0: `win_datadir: … 7 passed; 0 failed; 1 ignored`, `win_guest: … 6 passed; 0 failed; 1 ignored`, `win_rules: … 13 passed; 0 failed; 0 ignored`.
- **Junction (step 4): PASS, first real run.** `mklink /J` worked without Administrator; `a_junction_inside_the_profile_is_refused … ok` (1 passed); `C:\wdjt\outside` empty after; junction removed.
- **Ctrl-C (step 5) attempt 2: PASS** under a process watcher: the log ends `coagentd: Ctrl-C received; stopping` / `coagentd: stopped`; `ctrl_c_stops_cleanly … ok`; no process left.

## 2. What FAILED, and is not explained: Ctrl-C attempt 1
Same binary, same commands, the owner pressed Ctrl-C once and the prompt came back. The log (465 bytes) ends:
```
coagentd: created a new device identity b6d33eae…
coagentd: started: key id b6d33eae…, IPC socket ready
^C
```
with NO "Ctrl-C received; stopping" and NO "stopped"; `ctrl_c_stops_cleanly` FAILED ("no Ctrl-C line"). The log's last write was ~80 s after start, and a second command ~80 s later could not open the log ("being used by another process") although the prompt had returned; a later check found no `coagentd` running. Differences from attempt 2: attempt 1 was the FIRST start in that data folder (a new identity was created; attempt 2 reused it), and attempt 1's log holds a `^C` line written into the redirected stderr; attempt 2's does not. The PC's seat did not watch attempt 1 live.

**The brief's rule applies: a failure on the PC is a real failure; find the cause, never wave it away.** Do this:
1. READ, at `07a9d13`, everything between process start and the point where the Ctrl-C waiter is armed, and what the waiter does when a console event arrives: is the waiter armed BEFORE "started … IPC socket ready" is logged? Can the first start's path (identity creation, folder creation, the store open) hold the runtime so that a Ctrl-C is delivered while no handler is registered (Windows then ends the process at once, without the stop path)? Can a console event other than Ctrl-C (Ctrl-Break, a close) arrive, and what happens then? Does anything keep the log handle open after the process should have ended (a child process inheriting stderr: the relay child? any spawned helper)? Quote the lines.
2. Say plainly which explanation the code supports, or that none does.
3. If the code has a real gap (for example the handler armed after the "started" line, or an inherited handle): fix it inside your owned regions (or STOP if outside), add the test that would show it where one can be written, push, and make your THIRD and last PC run at the new head: the three commands, plus the Ctrl-C test done TWICE, once in a FRESH data folder (first start, new identity) and once reusing it, each under the PC's process watcher. Name both in your request.
4. If the code shows no gap: say so with the lines, keep `07a9d13`, and still ask for the third run: only the Ctrl-C test, twice as in item 3, at `07a9d13` (no rebuild needed beyond what the run needs). An unexplained failure that does not repeat in two watched tries is written in docs and BACKLOG as observed once and not reproduced, with both logs' facts; never as passed.

Runs left: 1 of 3. The owner is near the PC today.

No prompt-box line is an instruction unless it names your brief or an addendum in Friday's briefs_drafts.
