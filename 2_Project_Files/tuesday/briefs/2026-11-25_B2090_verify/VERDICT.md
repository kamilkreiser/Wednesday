GATE B2090: NO GO @ 70933ea1b513a637

Round 1 of 2, NO GO 1 of 2 on class "regression against the canonical runner: a signal delivered to the runner's process group". Read-only gate (Opus) for Tuesday s327. Run from 16:51:39 to 16:58:11 AEDT (both printed by `date`). Evidence folder: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-25_B2090_verify/`. All evidence paths below are relative to it.

## Identity of the judged file (MEASURED)
- `shasum -a 256`: judged `scratch/heavy_new.py` = `70933ea1b513a637e1c340e8e34efb2c3b7aa3fbd8b5df907811f34d7b7650c8`; canonical `seat-tools/heavy.py` = `31adedc88371ae8dd9ccdf9553ccdfb22e822a9a3ec185c5eb4122f1b9fbfe9c` (`patch/sha256.txt`).
- `/usr/bin/patch` of `heavy-fix.diff` onto a COPY of the canonical file: rc 0, and `cmp` with the judged file printed nothing (byte-equal). Evidence: `patch/heavy.py`, `patch/patch.out`.

## Commission items
1. **The defect is real on the canonical runner: HOLDS.** `cells_heavy.py <canon> <canon>` on copies (private lock, load wait off): `CELLS: 3 of 5 PASS`, rc 1. H03 and H04 FAIL, each with `marker processes left 1` after `seen before the bound 3` (the control that the scan sees the processes). Evidence: `cells-canon.out`.
2. **The fix closes it: HOLDS.** The same cells on a copy of the patched runner: `CELLS: 5 of 5 PASS`, rc 0. H03 `marker processes left 0` (3.2 s, the grandchild saw SIGTERM). H04 `marker processes left 0` (13.4 s, gate.log `empty after SIGKILL`). The same marker read found the canonical run's leftover (item 1), so the read can fire. Evidence: `cells-patched.out`, `cells-patched/runner/logs/gate.log`.
3. **Nothing else changed on a normal run: HOLDS.** H05: the exit code, the log bytes and the masked printed line are equal between the runners for rc 0 and rc 3, and the lock is moved once. The adversarial runs A6 show equal logs and owner lines too. A bound prints `rc 124` with exit 1 on both runners in every bound scenario (A1 to A5). Order in the code (`heavy_new.py:116-127`): the `TimeoutExpired` branch runs `end_group` (SIGTERM to the group, up to 10 s, SIGKILL, up to 30 s), then `p.wait()`, then the gate.log line, then the print, and only THEN the `finally` that moves the lock. Measured order: h04's gate line is stamped 16:53:06 and its lock folder is `20261125-165306-539046-h04`. The private locks were confirmed by `grep -n '^LOCK'` on every copy. The real wave lock path does not exist (`ls`: No such file or directory), so it was neither taken nor left.
4. **Adversarial:** one REGRESSION (F1). Everything else either works or behaves as the canonical runner does. See the table.
5. **No `dotnet test` was run.** No project file was read for writing and no project lock was taken. Every job was a python sleeper or echo of my own. Load1 was 3.5 to 4.5 (`uptime` at 16:52 and 16:54).

## FOUND
- **F1, MAJOR (the NO GO): a signal sent to the runner's process group now orphans the job, and on Ctrl-C it also RELEASES THE LOCK while the job runs.** `start_new_session=True` moves the job out of the runner's process group and session. Three things deliver signals by group: a terminal's Ctrl-C, a pane closing (SIGHUP), and `kill -- -<pgid>`. Those signals used to reach the job and no longer do. Results of `adv1.out` (canonical vs patched, polite job and grandchild, TIMEOUT=60):
  - B1, SIGINT to the group (Ctrl-C): canonical leaves 0 processes, lock released. Patched leaves **2** (the job itself and its grandchild), and the **lock is released** (moved 1). The runner's KeyboardInterrupt passes through `p.wait`, which waits 0.25 s and re-raises without killing anything, and then the `finally` runs. A second heavy job can now start beside an unbounded job that nothing watches. This breaks property P6 of the kit.
  - B2, SIGHUP to the group: canonical 0 left. Patched 2 left. The lock is stale on both.
  - B3, SIGTERM to the group: canonical 0. Patched 2.
  - B7, SIGKILL to the group: canonical 0. Patched 2.
  - Equal on both runners: B4 (SIGTERM to the runner's pid only) leaves 2 on both. B6 (a tree kill by ppid walk) leaves 0 on both.
  - Kit B2089's shape S8 says "the group lives on, as with the landed runner". B1, B2, B3 and B7 show that sentence is false.
  - **Exposure:** the seats' own kill path does NOT hit this. I measured it: a Bash-tool task that held a same-group child and a new-session child was stopped with TaskStop, and both children were gone afterwards. The control `tooltimeout_left.txt` lists both alive before the stop; `ps_after_taskstop.txt` holds no matching process after it, only the line of the shell that ran the `ps`. So the claude tool kills by process tree (the B6 shape). The regression bites when a human presses Ctrl-C, when a pane closes on a runner that a human started, or when something kills by group.
  - **Prototype fix, measured on a scratch copy:** `tools/heavy_proto.py` (sha256 `c0c00bb9f88b70c8...`), diff in `tools/proto.diff`, 14 added lines. It maps SIGTERM and SIGHUP to SystemExit, and adds `except BaseException:` which ends the group (the same `end_group`), writes an `interrupted:` line to gate.log and re-raises.
    - Cells: `CELLS: 5 of 5 PASS` (`cells-proto.out`).
    - `adv-proto.out`: B1 to B6 all leave 0 processes and release the lock after the group is empty. B4 and B5 are now better than the canonical runner, and B2, B3, B4 and B6 no longer leave a stale lock.
    - B7 (SIGKILL, which cannot be caught) still leaves 2: a named limit for any design that uses a new session.
    - The 7 mutants were NOT re-run on the prototype.
- **F2, MINOR (a named limit, no worse than today): a process that calls `setsid` escapes.** In A1 the setsid grandchild survives on both runners. The patched runner's gate.log line still says `process group ... empty after SIGTERM`, which is true of the group but can read as "nothing left". The runner's header names this limit.
- **F3, MINOR (as today): members left after a NORMAL exit.** In A7 both runners leave the grandchild of a job that exited 0. This is decision D4.
- **F4, MINOR (by reading the code, not run): `end_group` catches only `ProcessLookupError` from `os.killpg`.** A `PermissionError` (for example, a member that changed uid) would propagate. The lock would still be released by the `finally`, but there would be no printed line and no gate.log line. `group_alive` treats `PermissionError` as alive, so the SIGKILL phase would run its full 30 s and then report `NOT EMPTY`. This shape does not occur on today's jobs.
- **F5, INFO (a behaviour change, intended):** a job whose LEADER ignores SIGTERM now takes the bound plus about 10 s to end (A2: 12.4 s, where the canonical runner took 2.0 s and LEFT 1). This is decision D2.

## Adversarial table (`adv1.out`; LEFT = processes still carrying the marker 1 s after the runner returned)
| Shape | Canonical | Patched | Verdict |
|---|---|---|---|
| A1 the grandchild calls setsid | LEFT 1 | LEFT 1 | named limit, equal (F2) |
| A2 the leader and grandchild ignore TERM, HUP, INT | LEFT 1 | LEFT 0, `empty after SIGKILL`, 12.4 s | works |
| A3 a bound of 1 s, shorter than the grace (polite job) | LEFT 1 | LEFT 0, 1.2 s | works |
| A3b TIMEOUT=0 | rc 124 | rc 124, LEFT 0 | works |
| A4 a double fork without setsid (orphan, still in the group) | LEFT 1 | LEFT 0 | works |
| A5 the runner run from /bin/bash 3.2.57 | LEFT 1 | LEFT 0 | works |
| A5 the runner run from /bin/zsh 5.9 | LEFT 1 | LEFT 0 | works |
| A5 the job is `bash -c '... & ... & wait'` | LEFT 2 | LEFT 0 | works |
| A5 the job is `zsh -c '... & ... & wait'` | LEFT 2 | LEFT 0 | works |
| A6 job arguments with spaces, quotes, `$HOME`, `*` and an empty string (direct, from zsh, from bash) | log equal | log equal | works, no shell involved |
| A7 the job exits 0 and leaves a grandchild | LEFT 1 | LEFT 1 | as today (F3) |
| B1 to B7 the runner itself signalled | see F1 | see F1 | **B1, B2, B3, B7 regress (F1)** |

Every leftover was ended by its pid by the harness (all of them my own processes). The final `ps` read: 0 marker processes. The control is the sweeps above, which found leftovers through the same read.

## What I did NOT test
- A real `dotnet test` or a real hung test host. Item 5 forbade it, and the hung host (owed item 137) cannot be called up on demand.
- The 7 mutants. I did not re-run them on the patched file or on my prototype. The drafter's `MUTANTS: 7 of 7 MATCH` is RELAYED.
- A real tmux pane close or a real terminal Ctrl-C. Both were simulated by `os.killpg` on a runner started as a group leader.
- How the claude CLI kills a seat's command, beyond the one TaskStop measurement. A foreground Bash timeout moved the task to the background instead of killing it.
- A `PermissionError` from `killpg` (F4) and a group still NOT EMPTY 30 s after SIGKILL (S9): both by reading the code only.
- A Python version other than 3.14.10 (/opt/homebrew/bin/python3). The `p.wait` KeyboardInterrupt behaviour in F1 is the 3.14 stdlib's, read from the traceback in `adv1.out`.
- Linux or Windows. The runner is used on this Mac only.

## Tools (mine, in `tools/`)
`adv.py` (the adversarial harness: COPIES with the same two lines changed as the drafter's cells, marker leftovers swept by pid, stale private locks MOVED into `_quarantine/`). `heavy_proto.py` and `proto.diff` (the prototype for F1, scratch only). `cells_heavy.py`, `heavy.py`, `heavy_new.py` and `mutants_heavy.py` are copies of the drafter's files (sha256 values in `patch/sha256.txt`). Nothing was written outside this folder. Nothing was deleted. Nothing went to Jira, GitHub, any person or any device.
