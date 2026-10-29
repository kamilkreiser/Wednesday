STARTABLE: YES

# B904 drafter report (SEAT-M57, NexusAI main red on the M4 wall-clock control)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-29_B904_SEAT-M57_nexusai-main-red-m4-wallclock-diagnosis.md` (70 long lines; 9 stamp slots read 9 with the slot pattern, control = pattern also reads 9 on the kit itself; 0 `@X_@` tokens).

## BLUF
- The red is ONE failure, not a retry: jest printed it inline (log line 3993, 07:28:15) and again in the end summary (line 19855, 08:03:00). `Tests: 1 failed, 5223 passed`.
- Drafter reading is option (a): the control times a fresh `new JsonStorage` + first `setSetting` against 510 ms, but a fresh dir cannot enter the missing-name retry loop. Local median is 46 ms; the retry counter read 0 in 1350 runs. One stall on the shared runner crossed the line. The cell's real claim is a COUNT (no retry spent), so the kit makes it a counter (`jest.spyOn(Atomics,'wait')` + zero RD-407 log calls), in the SAME cell, no new `test()`.
- Main is green on its own since: push `be13993a` (run 40838546809) SUCCESS 5224/310 and #139 head `1e9a2c03` (run 40838594110) SUCCESS. The kit says the lane still runs (one green does not clear a flaky control).
- Main moved again while I worked: `4f662c49` = #139 landed. #139 is gone from open PRs; a NEW open PR #143 (B895's, branch `b895/...`) touches `backend/server.js`, the rd869 test and the counts file. The kit therefore forbids any new `test()` (a counts change would collide with #143) and any counts-file touch.

## Facts re-measured (instrument, control)
1. Failing run: `Build` 40834703321, push on 7e3d37e6, job 123316653434, ubuntu-24.04, node 24 (build.yml line 29), `npm run verify -- --maxWorkers=2`; received `{landed:1, underBudget:false}` at test line 282; suite 2587.9 s. Instrument: GH job-log GET (needs `--allow-escape-sequences`; first attempt returned 0 bytes, fixed). Control: the other 11 logs print the file as PASS.
2. Census: 12 completed Build job logs (frame: push on main or pull_request, 2026-10-27 19:17 to 2026-10-29 08:06 UTC): 11 PASS, 1 FAIL. Suite times 2041-3641 s (a loaded 2-vCPU runner; the wall clock in this repo is noisy). No elapsed figure is printed anywhere, so CI proves only `>= 510`.
3. Code (tarball of main be13993a in a scratch dir; blobs: test `1f2bb5fb`, jsonStorage `bba3742b`, both equal the GitHub contents shas): budget = 2+4+...+256 = 510 (line 539); retry = `Atomics.wait`, the only one in `backend/`; entered only if the first read is null AND `_existenceEvidence` is non-null; constructor creates/marks `settings.json`, so a fresh install never enters it.
4. History: both the test and the budget came from `cfcbacdb` (2026-09-14); `fa7ffe63` (RD-424) touched only the boot cells. M4 unchanged since creation.
5. Local distribution (plain-node replica of the cell body, macOS, node 26, 8 cores): alone n=300 min 44 / p50 46 / p90 61 / p99 114 / max 134, 0 at or over 510, 7 at or over 100; during a 2-worker full-suite run n=450 p50 49 / max 87; six parallel samplers plus that suite n=600 p50 195 / p99 242 / max 258. Retry counter 0 in all 1350. Positive control for the instrument: forced missing name after construction gave 8 waits, 558 ms, 2 RD-407 log calls, STORE_UNREADABLE. Under jest, a spy on `Atomics.wait` read 0 fresh and 8 forced (probe test in scratch, moved nowhere in the repo).
6. Adjacent: M3 in the same file has `elapsed < 100` (line 269), tighter than M4 and with p99 114 ms on the M4-shaped path alone. The kit asks the seat to decide it with the same method (default YES, Q-2). The only file in depth-1 `__tests__/*.test.js` matching `elapsed *< *ident` is this one (frame and pattern narrow; other stopwatch shapes were not censused).
7. Ports: 9950-9959 NOT used. The B903 HPSM-POC kit names 9950-9959 as its fallback block, 9960-9969 is named by the 10-28 B864 composer kit, 9940-9949 is B903's. 9971-9979: no word-boundary hit in the non-`.pre-` SEAT kits of 10-28 and 10-29 (49 kits scanned; control: 9850 hit B895 three times), `lsof` empty, positive control (python socket on 9955 seen, then gone). The M4 cell binds no port, so this is a reservation. The live tmux pane list printed nothing (no server visible to this shell), so the live-pane check is UNMEASURED.
8. Model: row C2 `model-routing.md` line 92 (build, not auth); gate row G2 line 109; model id `claude-sonnet-5-5` (`models_latest.json` lists `sonnet-5-5`). Lock tool sha256 `cf01bafb...4971f` unchanged from B895's stamp.

## D-decisions
- D1: the fix goes in the SAME cell (no new `test()`), because #143 moves the counts file and a second PR on it would collide, and because the test count stays 17 / suite 5224 (or whatever #143 makes it).
- D2: counter, not a larger budget (a bigger number only moves the flake). Two signals: `Atomics.wait` spy (sees every retry, including a recovered 2 ms one) and RD-407 log calls (sees exhausted retries and recovered ones via `logger.debug`).
- D3: plant = the file's own `missingName(live,{observations:1,armed:false})` armed after construction: one retry, 2 ms, which the OLD cell passes (proves the stopwatch is blind to it) and the NEW cell fails. Plant lives in scratch only.
- D4: tier 2 gate (G2). Product untouched; mechanism was measured by an earlier tier-1 gate.
- D5: no product byte; any (b) finding stops to Tuesday.

## Q-questions for Tuesday (each with a default)
- Q-1: ports. Default: 9971-9979 (the preferred 9950-9959 collides with B903's fallback). Say if you want a different block.
- Q-2: include M3's `elapsed < 100` in the same commit? Default: YES if the seat proves its path is also wait-free (measured 300 runs); otherwise leave it and report.
- Q-3: launch timing relative to B895 (PR #143)? Default: no ordering needed (disjoint paths, no counts change); the kit's REFUSE re-checks intersection before the push.
- Q-4: should a runner-side measurement be commissioned later (CI-only sampler logging the elapsed)? Default: no; the lane does not touch `.github/`. The runner stall stays UNMEASURED.

## UNMEASURED
- What stalled on the runner at 07:28 UTC+? (disk flush, CPU steal, GC): no elapsed is printed in any log; Linux/ubuntu-24.04 distribution not measured (drafter data is macOS only).
- Whether the flake recurs; M3's own distribution on its real path (needs `backedUpEnforcedStore`); the live pane list; other stopwatch shapes in `__tests__`.
- The local full-suite run used for load had some real-server suites failing to boot (rd523 harness) because the scratch copy used a symlinked `node_modules` from a different lockfile; I killed it and used it only as load. That does not touch the M4 numbers (the M4 file itself passed 17/17 in the scratch copy).

## Outside-the-fences disclosure
- Read-only: GitHub GETs under the NexusAI `GH_CONFIG_DIR` (runs, jobs logs, commits by path, pulls, pulls files, contents raw, tarball). The tarball (80 MB) was extracted into its own scratch dir `.../scratchpad/b904/main` and a `node_modules` symlink to the shared checkout's `node_modules` was placed there (a symlink into a project tree, READ only; nothing written in the project). `git` used only: `rev-parse`, `log -1` on the local checkout (stale, cd2b5439) and `hash-object` on scratch files.
- I ran jest and plain node inside the scratch copy only (no project write, no jest lock taken because nothing ran in the NexusAI tree; load1 reached 9.3 during the load run, above the kits' 7 line, for about 2 minutes, with the suite killed after). I wrote `zz-b904-spy-probe.test.js` into the scratch copy; the no-rm hook blocked a variable-path delete, so it stays in scratch (never in the repo).
- No Jira, no HTTP to hosted hosts, no az/docker/ssh, no `tmux` writes (`tmux list-panes` read printed nothing), no `decision_queue.sh`, nothing read from `briefs_staged`, scoreboard, `_ledger.md`, WEDNESDAY/FRIDAY trees. Two harmless slips: a zsh parse error on a command with parentheses in an echo (no effect), and the first job-log attempt wrote 0-byte files in scratch.
