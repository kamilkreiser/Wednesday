STARTABLE: YES (under Q1 default a: no repository change; Q1 is STOP-CLASS and S4 must answer it in words)

# B2089 DRAFTER REPORT: kit SEAT-X73 (OXPd heavy-job runner, process-group kill, owed item 138) + device-lanes readiness note

Drafted 2026-11-25 from 16:17:47 AEDT (first `date`) to 16:48:57 (last `date` before this file). Read-only drafter (Opus) for Tuesday s327. Files: the kit `2026-11-25_B2089_SEAT-X73_oxpd2-heavy-pgkill.md` (181 lines) and its `.measured` (97 claims, 97 measured, `stamp_check.py` rc 0), `2026-11-25_B2089_DEVICE-LANES-READINESS.md`, this report. Scratch: `fleet/state/s327/d2089/` only (the seat tools are in `seat-tools/`).

## BLUF
1. **Seat id X73.** X72 is taken (kit B2068, 11 files of today and yesterday name it; the control X71 has 14). X73 is named by 0 files, and 0 tmux panes name OXPd.
2. **The runner is in NO repository.** `main` `baa32eae` has 675 paths and 0 match `heavy` (control `build/repo_rules.py` 1). `<project>/.tools` is not in a git work tree. The canonical copy is the coordinator's last `seat-tools/heavy.py` (156 copies of `31adedc8` in Tuesday's tree; 60 of the 62 lane copies). So the commission's "branch, push-only" form has nothing to branch. The kit has the seat produce `<lane>/out/heavy.py` (no commit) and READY on its sha256. Tuesday carries it into the next lanes (THE ROUTE TO THE LANES, Q6). **Q1 STOP-CLASS:** a, outside the repo (built); b, into the repo `build/`; c, no seat.
3. **The fix** (81-line patch, 4 hunks): `Popen(..., start_new_session=True)`, `p.wait(timeout)`, then on time-out SIGTERM to the group, a 10 s grace, SIGKILL to the group, and up to 30 s for it to empty, all before the `finally` that releases the lock. The printed `rc 124` and the exit code are unchanged. One `gate.log` line per bound.
4. **Red, green, mutants: MEASURED.** Landed runner `CELLS: 3 of 5 PASS` (H03 and H04 FAIL, each with 1 grandchild left). Patched runner `CELLS: 5 of 5 PASS`. `MUTANTS: 7 of 7 MATCH`. Patched sha256 `70933ea1b513a637e1c340e8e34efb2c3b7aa3fbd8b5df907811f34d7b7650c8`.
5. **Real dotnet: MEASURED.** Every test executable started by `dotnet test` stays in dotnet's process group (18 of 18 sampled, normal run and 12 s bound). The fixed runner left 0 processes at the bound. Finding: the LANDED runner also left 0 at a 12 s bound, because healthy hosts exit when `dotnet test` dies. Only a hung host (item 137, seen 1 in 4) is orphaned, so the real red cannot be called up on demand. The red is the synthetic SIGTERM-ignoring grandchild (H04).
6. **Gate G2** (model-routing.md:109, "tooling"), on Opus (CLAUDE.md:7). Round 1 of 2.

## Facts re-measured (instrument)
- origin main `baa32eae27ddf1267ca1522ef7f1138a4dd832cd`, open PRs 0 (`gh api -X GET`, account kamilDatasec).
- BACKLOG.md:1007 item 138, :1010 its Why deferred; :866 item 118 (`grep -n`, `awk NR==n`). The commission's pointers are correct.
- Landed runner `31adedc8`: `:86` `subprocess.run(..., timeout=tmo)`, `:87` `except subprocess.TimeoutExpired:` (`awk`).
- Lane copies: 62 `heavy.py`; `killpg` in 0 (rc 1), `TimeoutExpired` in 62 (control).
- Kit B2067's STATUS:125: the Server.Tests host "SIGTERM (still alive after 6 s) then SIGKILL" (relayed; this is the reason for the grace and then the hard kill).
- Real runs (`real_bound.py`, own clone by `clone.py draft`): restore rc 0 (2 s), build `0 Warning(s)` (8 s); fixed runner normal `rc 0`, `total: 2261`, `failed: 0`, `LEFT 0`; fixed runner 12 s `rc 124`, gate.log `process group 51190 empty after SIGTERM in 0.2s`, `LEFT 0`; landed runner 12 s `rc 124`, `a group leader among them: None`, `LEFT 0`.
- **Load I ran at:** load1 2.3 to 13.14 by `uptime` (13.14 at 16:29:49, while my mutants ran beside the NexusAI N175 seat). The runner's own lines read 2.51 to 6.7. Lock waits 0 on every job. My dotnet runs took the OXPd wave lock through the runner and never the NexusAI jest lock.
- Mac firewall `State = 0`, Mac `inet 192.168.20.220` (for the readiness note; local reads only).

## D-decisions (all Tuesday's defaults, in the kit)
D1 no repository change. D2 TERM, 10 s, KILL, 30 s. D3 printed line unchanged; the detail and any `NOT EMPTY` go to gate.log only. D4 a normal exit is unchanged. D5 the cells test copies with 2 lines changed (private lock; load wait off). My first mutant run lost cell H01 to a load wait at load1 13, and that is why D5 exists. D6 Tuesday carries the file.

## Questions for Tuesday (each with its default)
- **Q1 (STOP-CLASS):** where the fix lives. Default **a**, outside every repo, as today. Alt b: into `build/` on a branch. It is a rewrite: the runner hardcodes this Mac's paths and Tuesday's tree path at `heavy.py:17-20`, CI runs on Linux and Windows, and the unit count moves. Alt c: no seat; adopt the drafter's file after a G2 gate.
- Q2 the signals. Default TERM, 10 s, KILL.
- Q3 output. Default: the line unchanged; the detail in gate.log.
- Q4 normal exit. Default unchanged.
- Q5 the cells' copies. Default: private lock and the load test off.
- Q6 the route. Default: Tuesday copies the file into each next drafter's seat-tools and keeps one canonical copy, plus a DRAFTER_RULES line naming the sha.
- Q7 the runner itself killed. Default: a named limit. Opus, READY in 60 min, pane X73.

## Readiness note (one line each; the table is in the note)
- Row 3: build lane YES now. Device run after the build, by an agent under the grant (EXPIRING-GRANTS.md:13; CLARIFICATIONS.md:1078). Item 103 is settled on the device, not by HP ("no H9", C-86:1186).
- Row 4: build lane YES now. Device run needs his word first ("We ask again before any home-screen app is added", CLARIFICATIONS.md:1088) and a human press on the panel.
- Item 118: an agent can run it now through the landed `oxpd1 echo --echo async`, but the coordinator's own C-84 reading (CLARIFICATIONS.md:1114) ties it to the test-button lane. Tuesday may revise that reading. Whether the route back exists is UNMEASURED; his act is needed only if it is missing.

## UNMEASURED
A real hung host under the fixed runner. Any process that calls `setsid` (0 of 18 did). The runner being killed mid-job. The kit run whole by a seat, including `clone.py` inside the project's `.tools/`. For the readiness note: the printer-to-Mac route, the M577's acceptance of a self-signed root, and whether a test button counts as a "home-screen app".

## Outside the fences (disclosure)
- Created and wrote only in `fleet/state/s327/d2089/` (scratch, including a draft clone made by `clone.py draft` with push URL `invalid://no-push` and no identity), plus the four commission files. Moved one unused copy (`words.py`) into `d2089/_quarantine/`; nothing deleted.
- Ran `dotnet restore`, `build` and `test` four times in my own clone, through the OXPd wave lock: allowed by the commission.
- Started and ended my own python test processes. Stopping one of my background mutant runs left nothing behind (`hvcell-` processes: 0). No other process was touched.
- One `git -C ... apply --check` ran inside my scratch folder, which is inside the TUESDAY repo (a check only, no write). Then I used `/usr/bin/patch` on a scratch copy.
- Read Tuesday's `EXPIRING-GRANTS.md` and `NEXT-PICKUP-TUESDAY.md` (Datasec lines) for the readiness note. Read no card store, no `briefs_staged/`, no scoreboard, no `_ledger.md`, no WEDNESDAY or FRIDAY tree, no other client.
- Nothing to Jira, GitHub (GET only), any human, the printer or any device.
