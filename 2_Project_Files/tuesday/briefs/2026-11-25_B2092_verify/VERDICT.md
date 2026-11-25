GATE B2092: NO GO @ c0c00bb9f88b70c8

Round 2 of 2. This is NO GO 2 of 2 on the class "a signal to the runner releases the lock while the job runs" (the round-1 line, read from `2026-11-25_B2090_verify/VERDICT.md` line 1: `GATE B2090: NO GO @ 70933ea1b513a637`). This was a read-only in-session gate (Opus, tier G2) for Tuesday s327, independent of B2090. Work started at 16:59:44 and VERDICT was written after 17:20:52 AEDT (both printed by `date`). Evidence folder: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-25_B2092_verify/`. Paths below are relative to it.

**The failing shape:** a SECOND signal (SIGINT, SIGTERM or SIGHUP) that reaches the runner while it is ending the job's group. That window is the 10 s grace or the SIGKILL wait, and it opens on either path: after the bound (`except subprocess.TimeoutExpired`, line 127) or after a first interrupt (`except BaseException`, line 132). The exception the second signal raises inside `end_group` leaves through the except clause it was raised in. A sibling `except` clause does not catch it, and `end_group` runs with all three handlers still live. The `finally` (line 139, `shutil.move` on line 141) then releases the lock. The job, which has not yet obeyed SIGTERM, is never sent SIGKILL and runs on unbounded. gate.log gets no `bound` and no `interrupted:` line. The window is wide exactly for the job the fix exists for: one that does not end on SIGTERM, such as a hung test host. In the control run N2e, one Ctrl-C on such a job takes 10.8 s to return, and the runner prints nothing meanwhile. A human pressing Ctrl-C again in those 10 s is the expected behaviour, not an edge case.

## 1. Identity: HOLDS (MEASURED)
- sha256 (`identity/sha256.txt`): canonical `seat-tools/heavy.py` = `31adedc8…fe9c`. Round-1 file `scratch/heavy_new.py` = `70933ea1…50c8`. Prototype `B2090_verify/tools/heavy_proto.py` = `c0c00bb9f88b70c834fcef5ca8e2d38dbc5d3661504b63c16cad1ce9538675cf`.
- `/usr/bin/patch` of `proto.diff` onto a copy of the round-1 file: rc 0, then `cmp` with the prototype: rc 0, byte-equal (`identity/patch.out`). `diff round1 proto` is also equal to `proto.diff`.
- All three files were read whole. The canonical runner's bound is `subprocess.run(..., timeout=tmo)` (line 86). Its stdlib kills the LEADER only, on a bound or on any exception.

## 2. Re-runs on copies (private lock, load wait off): drafter's cells and mutants HOLD; adversarial results below
- Cells (`cells-canon.out`, `cells-proto.out`): canonical `CELLS: 3 of 5 PASS` (H03 and H04 FAIL, each `marker processes left 1` after `seen before the bound 3`). Prototype `CELLS: 5 of 5 PASS` (H04 13.3 s, `empty after SIGKILL`).
- Mutants on the prototype (`mutants-proto.out`): `MUTANTS: 7 of 7 MATCH`. Each expected red set still holds: mNoNewSession H03 H04, mTermOnly H04, mKillFirst H03 H04, mLeaderOnly H03 H04, mOtherRc H03 H04, mNoWaitForEmpty H04, mOutputLost H01 H02 H05. The prototype's sha256 was equal before and after.
- Mutants on the canonical runner, as a control (`mutants-canon.out`): 6 REFUSED (their literals are absent) and mOtherRc MATCH. That match is vacuous, because the canonical runner already fails H03 and H04.
- Adversarial: my harness `tools/adv2092.py` (the evidence is `adv2092.out`, a second run with the lock read before each ps snapshot; the first run is `adv2092-run1-sampleorder.out`) and B2090's own `adv.py` re-run unchanged (`adv_b2090-rerun.out`). The two agree on every A and B row, and they agree with B2090's `adv1.out` and `adv-proto.out`.

Table. LEFT = marker processes alive about 1 s after the runner returned. Lock = released BEFORE or AFTER the job's processes were all gone (a 30 ms sampler; "stale" = never released).

| Shape | Canon LEFT / lock | Proto LEFT / lock | Note |
|---|---|---|---|
| A1 setsid grandchild | 1 / before | 1 / before | named limit, equal |
| A2 leader+grandchild ignore TERM HUP INT | 1 / before | 0 / after (12.4 s) | fixed |
| A3 bound 1 s / A3b bound 0 | 1 / before ; 0 | 0 / after ; 0 / after | fixed |
| A4 double fork, no setsid | 1 / before | 0 / after | fixed |
| A5 runner from bash 3.2 / zsh | 1 / before | 0 / after | fixed |
| A5 job is `bash -c '& & wait'` / zsh | 2 / before | 0 / after | fixed |
| A6 quoted arguments (direct, zsh, bash) | 0, log equal | 0, log equal | equal |
| A7 job exits 0, leaves grandchild | 1 / before | 1 / before | equal (D4) |
| B1 SIGINT to runner group | 0 / after | 0 / after | equal |
| B2 SIGHUP to group | 0 / stale | 0 / after | better |
| B3 SIGTERM to group | 0 / stale | 0 / after | better |
| B4 SIGTERM to runner pid | 2 / stale | 0 / after | better |
| B5 SIGINT to runner pid | 1 / before | 0 / after | better |
| B6 tree kill (the TaskStop shape) | 0 / stale | 0 / after, **but exit 1 with a PermissionError traceback, no gate line** | F2 |
| B7 SIGKILL to group | 0 / stale | 2 / stale | named limit (lock stays held) |
| **N1a Ctrl-C during the bound's grace, job ignores TERM** | 0 (lock released at the bound; the Ctrl-C then ended the grandchild) | **2 / BEFORE, exit -2** | **F1, worse** |
| **N1b the same, job ignores TERM HUP INT** | 1 / before | **2 / BEFORE** | **F1, worse** |
| **N1c SIGHUP (pane close) during grace** | 0 (as N1a) | **2 / BEFORE, exit 129** | **F1, worse** |
| **N1d SIGTERM to runner pid during grace** | 1 / before | **2 / BEFORE, exit 143** | **F1, worse** |
| N1e Ctrl-C during the SIGKILL wait (stub: SIGKILL has no effect) | 0 (as N1a) | **2 / BEFORE** | F1, same code path |
| **N2a second Ctrl-C 2 s after the first, job ignores TERM** | 0 / after | **2 / BEFORE** | **F1, worse** |
| **N2b the same, job ignores all three** | 1 / before | **2 / BEFORE** | **F1, worse** |
| **N2c SIGTERM twice to group** | 2 / stale (lock held) | **2 / BEFORE** | **F1: the lock is now released** |
| **N2d Ctrl-C then SIGHUP** | 0 / after | **2 / BEFORE, exit 129** | **F1, worse** |
| N2e control: one Ctrl-C, job ignores TERM | 0 / after | 0 / after, 10.8 s, `empty after SIGKILL` | works when nothing else arrives |
| N3 job exits on its own at the bound (sleeps 1.97 to 2.05 s against TIMEOUT=2, 18 runs each) | 0 / after in 18 | 0 / after in 18; rc 0 or 124 by timing, no traceback | equal |
| N4a/N4b stub: `killpg` raises PermissionError (bound / Ctrl-C) | 1 ; 0 | **2 / BEFORE, exit 1, no rc line, no gate line** | F2 |
| N4c/N4d stub: `killpg` raises ProcessLookupError | 1 ; 0 | 2 / stale: reports `empty before SIGTERM`, then `p.wait()` blocks holding the lock until the harness SIGKILL at 20 s | safe direction |
| N4e stub: `os.kill` raises PermissionError (the canonical runner's kill path) | 0 / stale: canonical blocks in `Popen.__exit__` until the harness SIGKILL at 25 s | 0 / after (it does not use `os.kill`) | control |
| N6 runner under `nohup`, SIGHUP to group | 1 / before (the runner ignored HUP and ran to the bound) | 0 / after, exit 129 | F3 |
| N7 stub: KeyboardInterrupt inside `Popen()` after the fork | 2 / before | 2 / before (`'p' in dir()` is false: no end) | F4 |

## 3. New shapes: F1 is worse than the canonical runner (rows in bold above)
## 4. The lanes' property: does NOT hold on the prototype
No heavy job may run unbounded after its runner has released the lock, except under SIGKILL to the runner. The prototype breaks this in N1a, N1b, N1c, N1d, N1e, N2a, N2b, N2c and N2d (each `LEFT 2`, `released BEFORE empty`), and in N4a and N4b (stubbed). None of those shapes involves SIGKILL to the runner. It also breaks it in A1 (setsid) and A7 (normal exit leaves a grandchild), exactly as the canonical runner does: limits the header names (A1) or decision D4 owns (A7). B7 keeps the lock held (stale), so the property holds there vacuously.

## FOUND
- **F1, MAJOR (the NO GO): a second signal during the end of the group releases the lock with the job alive and never sent SIGKILL.** Evidence: `adv2092.out` rows N1a to N2d, and `adv2/proto/logs/gate.log`, which carries only `load1` and `lock taken` lines for N1a, N2a, N2c and N2d, with no `bound` or `interrupted:` line. The cause is at lines 127 to 141 of the judged file. A fix shape, offered as a proposal, not as authority: block or ignore SIGINT, SIGTERM and SIGHUP for the duration of `end_group` and the following `p.wait()` on BOTH paths (for example, `signal.pthread_sigmask(SIG_BLOCK, …)` around them, or a single cleanup in an outer `try/finally` that the bound path also goes through). Also print one line such as "ending the job's group (up to 40 s)…" so a human does not press Ctrl-C again. Any fix needs a cell (see F5).
- **F2, MINOR (B2090's F4, now MEASURED, and it fires without a stub): on this macOS, `os.killpg` on a group whose only member is an unreaped zombie raises `PermissionError`, not `ProcessLookupError`.** Evidence: `tools/zombie_killpg.py` gives `zombie_killpg.out` (macOS 27.2.1: sig 0, 15 and 9 all `PermissionError`; after reaping, `ProcessLookupError`). It fires in B6, the tree-kill shape that B2090 measured as the claude TaskStop path: exit 1, a traceback, no `interrupted:` line. B2090's own `adv-proto.out` B6 row shows the same traceback, though its VERDICT lists F4 as "not run". In B6 the group is already empty, so the property holds. With a group whose live members cannot be signalled (stubbed N4a and N4b), the runner releases the lock with the job running, prints no rc line and exits 1. Line 72 catches only `ProcessLookupError`. Line 65 (`group_alive`) treats `PermissionError` as alive.
- **F3, INFO (a behaviour change): the prototype replaces an inherited SIG_IGN for SIGHUP** (line 34). A runner started under `nohup` used to survive a pane close and keep bounding its job. Now a pane close ends the job, cleanly (N6). A scan of the 2026-11-20 to 11-25 kits that name `heavy.py` found no `nohup` (`grep -l nohup` gave no file). Keep the ignore if one is inherited.
- **F4, MINOR (a named limit, very small window): a Ctrl-C between the fork and `pg = p.pid`** (`'p' in dir()` false, or `pg` unbound, which gives a NameError) leaves the job, which is in its own session, running with the lock released. The stub N7 shows the consequence. A real Ctrl-C there would also reach the canonical runner's job, which is in the same group, so the prototype is worse in this window. The window is the fork-to-exec handshake (milliseconds) and was not hit by real timing.
- **F5, MINOR (coverage): no cell exercises the prototype's 14 lines.** The round-1 file, which lacks them, passes the same cells 5 of 5 (`B2090_verify/cells-patched.out`), and no mutant touches lines 29 to 34 or 132 to 137. A fix for F1 needs signal cells (B1 to B4, N1a, N2a) and a mutant that removes the signal block, or it can regress silently.
- **F6, INFO (what a caller sees when the runner is interrupted, MEASURED):** no `<label>: rc` line on stdout in any interrupt shape. SIGINT gives exit -2 (a shell shows 130) with a `KeyboardInterrupt` traceback on stderr. SIGTERM gives exit 143 and SIGHUP gives exit 129, both without a traceback (on the canonical runner these were deaths by signal, -15 and -1). gate.log gets `interrupted: process group <n> empty after SIGTERM in 0.2s` only when nothing else arrives (B1 to B5). In F1 and F2, gate.log is silent.

## What I did NOT test
- A real `dotnet test` or a real hung test host (forbidden here). Every job was a python sleeper of my own.
- A real terminal Ctrl-C, a real tmux pane close or a real TaskStop. Each was simulated with `os.killpg`, `os.kill` or a ppid tree walk against a runner started as a group leader.
- The SIGKILL-wait window (N1e) and PermissionError on live members (N4a, N4b) ran only with stubs that change `os.killpg` in the runner copy. A real group that survives SIGKILL could not be built.
- The F4 fork window under real timing, and PID or pgid reuse after the leader is reaped. Both by reading the code only.
- Python other than 3.14.10, and Linux or Windows.
- Load: load1 read 2.8 at the start and was 6 to 16 during the adversarial runs (gate.log `load1` lines, `uptime` 8.75 at 17:20), from other work beside me. The outcomes are set by the code's structure (which clause catches what). Only the sub-second order times in the table are load-sensitive.
- I did not run a candidate fix for F1. That is the next round's (or a ticket's) work.

## Hygiene
Every leftover was ended by its pid by the harness (my own processes only). A final `ps` scan for the `gate2092-`, `gate2090-` and `hvcell-` markers counted 0. The control is the same scan, which found the LEFT counts above. Stale private locks were MOVED into each copy's `_quarantine/`. Nothing was deleted. Nothing was written outside this folder. No project file, Jira, GitHub, card store, person or device was touched.
