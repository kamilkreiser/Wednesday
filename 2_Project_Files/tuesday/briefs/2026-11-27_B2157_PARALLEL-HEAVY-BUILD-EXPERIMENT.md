# B2157 (in-session, Opus): can heavy builds run 2 to 5 at a time on this Mac? Measure it, then recommend

Kam, Tuesday terminal, 2026-11-27, verbatim: "test if the heaby build can be pushed to 2-5.  your call but lets make the decision on what can be done".

Context: Kam wants about 20 agents live and OXPd working before Christmas. Today each project allows one heavy job at a time:
- OXPd: the wave lock `/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2/.tools/wave1-heavy.lock.d`, taken by the canonical runner `heavy.py` (sha256 31adedc8; a copy is at `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s332/d2138/seat-tools/heavy.py`).
- NexusAI: the jest lock `session-tools/nexusai-lock.sh jest`.

The question is whether that is a real limit of this machine or a convention. The machine: Apple M5 Max, 18 cores, 128 GB.

## Rules
- Write only under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s333/x2157/` (clones, logs) and the report `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-27_B2157_PARALLEL-HEAVY-BUILD-REPORT.md`.
- **Never write in the project folders.**
  - Clones are made with `git clone --no-hardlinks` from each project's `2_Project_Files` into YOUR folder. Fetch main by HTTPS-free means: `gh api -X GET` tarball, or a clone of the local checkout followed by checking out main's sha read by `gh api -X GET`.
  - OXPd: the local checkout is stale, so use the tarball of main `760e1a64` (re-read it).
  - NexusAI: main `d2aeecf8` (re-read it).
- No push, no PR, no Jira, nothing to any person or device. Never `cd`; never delete.
- **Take each project's lock for the WHOLE of your experiment on that project**, so no live seat collides with you:
  - OXPd: `mkdir` the wave lock folder with an `owner.txt` naming B2157, and move it to your folder when done.
  - NexusAI: `nexusai-lock.sh jest b2157-exp <one script that runs all your N-runs>`.
  - First check no seat is live on that project (`tmux list-panes -a -F '#{@cockpit_name}'`) and no holder exists. If one does, wait, or do the other project first.
- Toolchains:
  - OXPd: `<OXPd_2>/.tools/dotnet/dotnet` 10.0.404, `DOTNET_CLI_HOME` in your folder. Restore with `--locked-mode`, offline from the existing NuGet cache if possible; no new package download beyond what restore of main needs.
  - NexusAI: node 24 at `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tools/node-v24.22.2-darwin-arm64/bin`, and `npm ci` from the lock file.
- Record load averages (`uptime`), memory (`vm_stat` and `memory_pressure`) and wall time for every run.
- A hung run is killed by its own pids only (TERM, then KILL) and recorded. Owed 137, the Server.Tests hang, is a known risk: count its occurrences.

## The experiment
1. **OXPd.** In N separate clones of main, run the whole-solution `dotnet test -c Release` (after one build per clone) concurrently, for N = 1, 2, 3 and 5. Each N gets two trials if time allows.
   - Record per run: total, failed, skipped (the expected total is 2431, with 4 skipped on macOS), wall time, and hangs.
   - Then the same for a SINGLE test project (`Datasec.Suite.UniversalPrint.Tests`) run concurrently N = 2 and 5. That is the per-project-lock case for parallel app lanes.
   - Check for shared state between concurrent runs: ports (the host tests bind ports), temp folders, the secret store paths, and file locks in `obj/`/`bin/` (separate clones should avoid that).
2. **NexusAI.** The repository already gives each worktree its own port band (`__tests__/helpers/test-server.js` `worktreeSlot`: sha256 of the real path mod 19). Choose N clone paths whose slots differ, print each slot, and avoid the bands other kits name. Then run the whole suite (`npm run verify -- --maxWorkers=2`, plain mode, in dot-free paths) concurrently for N = 1, 2 and 3; 4 or 5 if load allows.
   - Record per run: the VERDICT line (expected `6634/6634 tests passed across 419 suites`), wall time, EADDRINUSE count, and failures by suite.
   - Also try N = 2 with `--maxWorkers=4`.
3. **Stop rule:** if load1 stays above 30 for 5 minutes, or memory pressure goes critical, stop that N and record it.

## Report (BLUF first)
- The safe concurrency per project, with evidence: wall time per run versus N, failures and hangs versus N, and peak load and memory.
- The decision options:
  - (a) keep one heavy job;
  - (b) a counting lock, a semaphore of N (for example 3), with the exact change to `heavy.py` and `nexusai-lock.sh`;
  - (c) a per-test-project lock for app lanes.
- What must land first, for example owed 137's bound if hangs grow with N.
- Your recommendation.
- Put a `## FOR TUESDAY` section with the exact tooling changes, written as a commission for a tooling seat. Do not make the changes yourself.

Return 10 lines, first `DONE` or `BLOCKED: <reason>`.
