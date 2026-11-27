# B2157 report: can heavy builds run 2 to 5 at a time on this Mac?

Re-commission by Tuesday s334 (the first B2157 agent died with seat s333 before writing a report). Machine: Apple M5 Max, 18 cores, 128 GB. All clocks AEDT, printed by `date`. Written 2026-11-27. Evidence folder: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s333/x2157/` (`logs/oxrun2.out`, `logs/ox2-results.jsonl`, `logs/ox2-samples.tsv`, `logs/ox2/`, `logs/nxrun2.out`, `logs/nx2-results.jsonl`, `logs/nx2-samples.tsv`, `logs/nx2/`; runners `oxrun2.py`, `nxrun2.py`, summariser `oxsum.py`).

## BLUF

- **The one-heavy-job rule is a convention, but the two projects hit different limits, so they need different numbers.**
- **OXPd is CPU-bound.** One whole-solution `dotnet test` already fills the machine (load1 18 to 32 with ONE run). Running 2 or 3 at once stays green (2431 total, 0 failed, 4 skipped, every copy, both trials), but each run takes 1.7x and 2.5x as long, for only 1.17x and 1.21x the throughput. **At 5, every copy went red in both trials** (10 to 12 failures each, all timing guards, 102 of 105 in `Lab.Tests`' 30-second guard). Memory is never the limit (88 to 90% free, pressure normal). A single light test project (`UniversalPrint.Tests`, 351 tests, 8 s) runs 5 at once at no cost at all.
- **NexusAI is wall-clock-bound.** One `verify` (22.6 min) holds load1 at only 3 to 11. Three at once take at most 3% longer each (2.9x throughput), five at once at most 12% longer (4.5x). **But concurrency exposes one real cross-copy collision:** `rd490-open-access-banner-browser.test.js` takes ports from a fixed machine-wide band (38900-38939) that the worktree slots do not cover. It failed 72 tests in one copy at N=3 and again at N=5. EADDRINUSE: 0 everywhere. `--maxWorkers=4` halves the time but breaks two suites inside one copy, so keep w=2.
- **Owed 137 (the Server.Tests hang): 0 occurrences in 22 whole-solution runs at N = 1 to 5.** It does not grow with N here, but today's `heavy.py` kills only `dotnet` on time-out, so a hang leaves orphan test hosts. That has to be fixed before any semaphore lands.
- **Recommendation:** OXPd gets **(b) a semaphore of 2 plus (c) per-test-project locks for light app lanes**, never 3 or more for whole-solution work. NexusAI gets **(b) a semaphore of 3**, but only after the rd490 port band moves into the worktree slot and the lock refuses two holders with the same slot. Until then NexusAI stays at one. Details are under "Recommendation" and in `## FOR TUESDAY`.

## Locks held (both released, nothing left behind)

| Project | Lock | Taken | Released | Held | How released |
|---|---|---|---|---|---|
| OXPd | `/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2/.tools/wave1-heavy.lock.d` (`owner.txt` names B2157) | 17:40:20 (absent at 17:39:02 and 17:39:59; no live OXPd seat in `tmux`) | 18:38:00 | 57 min 40 s (cap 100) | moved to `x2157/_quarantine/locks/20261127-183800-b2157-oxpd`; absence checked 18:38:02 |
| NexusAI | `nexusai-lock.sh jest b2157-exp` (base `.../NexusAI/session-tools/locks-laptop-1017`, queue empty) | 18:38:52 | 20:35:58 | 1 h 57 min | the script's own release (`released/done-jest-b2157-exp-40740-1795772158`) |

No process from my copies was left after either part (checked with `ps` at 18:38:07 and 20:36:10). One unrelated orphan exists on the machine and I did not touch it: `/private/tmp/b1839-gate/clone/tests/Datasec.Suite.Sessions.Tests/...`, pid 2177, parent pid 1, started Sat 21 Nov 17:15:35.

## The first agent's scratch: what was reused and what was not
- **Reused (complete):** five OXPd copies of `760e1a64`, their `restore --locked-mode` (rc 0) and one Release build each (7.3 s alone; 24.6 s each with four at once, peak load1 93).
- **Not reused:** its one OXPd test run, 139 `Lab.Tests` failures, every one `exit 9`, because its `TMPDIR` sat inside the TUESDAY git work tree (explained below). Its first attempt's restore was also not reused: rc 1, `NU1900` while fetching vulnerability data, fixed by `-p:NuGetAudit=false`. Its NexusAI copies were not reused either: they were at `96a45f10`, not main. The partial results are kept, unchanged, in `x2157/logs/ox-results.jsonl` and `x2157/_quarantine/attempt1/`.

## Safe concurrency per project (the evidence in one table)

| | N=1 | N=2 | N=3 | N=5 |
|---|---|---|---|---|
| OXPd whole-solution test, wall per run | 61 to 63 s | 104 to 108 s | 150 to 157 s | 249 to 254 s |
| OXPd failures / hangs (2 trials) | 0 / 0 | 0 / 0 | 0 / 0 | **10 to 12 per copy, all copies** / 0 |
| OXPd peak load1 / min free memory | 31.6 / 89% | 45.1 / 89% | 53.9 / 88% | 56.8 / 89% |
| OXPd single light project (`UniversalPrint.Tests`) | n/a | 6 to 9 s, 0 failed | n/a | 8 s, 0 failed |
| NexusAI verify w=2, jest time per run | 1357 s | 1343 to 1383 s | 1357 to 1398 s | 1474 to 1523 s |
| NexusAI failures beyond the baseline / EADDRINUSE | 0 / 0 | 0 / 0 | **rd490 collision, 1 copy** / 0 | **rd490 collision, 1 copy** / 0 |
| NexusAI peak load1 / min free memory | 10.9 / 88% | 6.4 / 89% | 8.3 / 88% | 11.7 / 88% |

The stop rule (load1 above 30 for 5 minutes, or critical memory pressure) never fired. OXPd's load1 went above 30 only in bursts of under 2 minutes. s334's load gate held before every batch: two load1 reads 120 s apart, both under 24.

**Safe today:** OXPd, 2 whole-solution jobs (3 is green but buys almost nothing); any number of light single-project test runs. NexusAI, 1 until the rd490 band is fixed; 3 after it (5 fits the machine, but leave room for the OXPd jobs running alongside).

## Decision options

**(a) Keep one heavy job per project.** It is safe and needs no change. For OXPd it costs little throughput (2 at once gives only 17% more), but every short job (a 7-second build, an 8-second project test) still queues behind a 60-second solution test, and with about 20 agents the queue wait is the real cost. For NexusAI it wastes most of the machine: a verify uses about a twentieth of the CPU and holds the lock for 23 minutes, so at most about 2.6 verifies an hour across the whole fleet.

**(b) A counting lock (a semaphore of N).**
- OXPd, N=2: green in both trials, 1.17x the throughput, and a second slot so short jobs stop waiting behind a long one. N=3 is green but gives 1.21x for 2.5x the latency, and N=5 is red. So 2 is the ceiling for whole-solution work. Needs: a new load gate for the second slot (today's "load1 under 7" would keep it shut, because one OXPd test holds load1 at 18 to 32), one job per checkout, and the time-out kill fix.
- NexusAI, N=3: 2.9x the throughput at a 3% latency cost. Needs first: the rd490 fix, and slot-distinct holders (two clone paths share a slot 1 time in 19; any two of three, about 15%).
- The exact changes to `heavy.py` and `nexusai-lock.sh` are in `## FOR TUESDAY`.

**(c) A per-test-project lock for app lanes (OXPd).** A lane that tests only its own app's project (for example `Datasec.Suite.UniversalPrint.Tests`, 351 tests, 8 s) takes a lock named for that project instead of a heavy slot. Five ran at once at no cost (8 s each, 0 failed, peak load1 5 to 8). This is the biggest win for parallel OXPd app lanes, because their inner loop never needs the whole solution. The whole-solution run stays for the gate, behind (b).

## What must land first
1. **NexusAI `rd490-open-access-banner-browser.test.js`:** move `PORT_BAND` (38900-38939, a per-process `Set` reservation) into the copy's own worktree slot, for example the slot's top band, which `nestedJestEnv` already reserves for nested runs, or a sub-band of it. This is a product-repository test change, so it goes to a NexusAI seat as an RD ticket, not to a tooling seat. Until it lands, any second concurrent verify can fail that suite (72 tests).
2. **`nexusai-lock.sh` refuses a second holder in the same slot:** the caller's `worktreeSlot()` is recorded in the owner file and compared. Kits name clone paths freely, and a shared slot means a shared port band.
3. **`heavy.py` kills the whole process group on time-out, then reports any process left in that checkout** (owed 137's bound). The hang did not occur in 22 runs, so it does not grow with N on this evidence, but an orphaned test host holds ports and CPU after its job "ended", and with 2 slots that counts double.
4. **`heavy.py`'s load gate for slot 2** (s334's two-read rule, under 24), else the semaphore never opens.
5. **Kits never point `TMPDIR` into a git work tree:** the OXPd lab tool refuses its run folder with exit 9, which wiped 139 tests in the first agent's run. Kit lane folders under `TUESDAY/2_Project_Files/fleet/state/` are inside the TUESDAY repository.

## Recommendation (my call, as Kam asked)
- **OXPd: (b) with N=2, plus (c).** Install `heavy.py` slots with `heavy-slots`=2 together with the kill fix and the slot-2 gate, and add the light-project bypass, starting with `UniversalPrint.Tests`. App lanes test their own project under (c) and use a heavy slot only for builds and the whole-solution gate. Do not go to 3: it is green but gives nothing back, and 5 is red.
- **NexusAI: (b) with N=3, in two steps.** First the rd490 RD ticket and the slot-distinct check. Then set `slots-jest`=3, keep `--maxWorkers=2`, and re-run this experiment's N=3 batch once (the `x2157/nxrun2.py` runner, about 25 minutes) as the proof. Leave 4 and 5 for after a week at 3: the machine can carry 5, but a NexusAI verify at 5 alongside 2 OXPd heavy jobs has not been measured.
- **Combined budget on this Mac** with these settings: at most 2 OXPd heavy jobs (load1 up to about 45), 3 NexusAI verifies (about 10 more), any number of light OXPd project tests. Peak memory stays far from any limit. CPU is the shared resource, and s334's gate protects it.

## Limits of this evidence
- One machine and one day. OXPd had two trials per N. NexusAI had one trial per N (each batch takes 23 to 25 minutes), and its N=1 repeat was dropped to free the jest lock.
- The NexusAI copies are one-commit repositories made from the tarball (the local checkout lacks `d2aeecf8`), so `handover-gate-table` fails in every run by construction. Each run was read against 6633/6634.
- Per-run NexusAI times are jest's own `Time:` line. The runner's wall column is exact only for the first copy of each batch, because it polls the copies in order.
- No OXPd N=1 run of the single light project. N=2 and N=5 both took about 8 s, so N=1 cannot be slower.
- OXPd builds (N=1 and N=4) were measured by the first agent, not repeated.

## OXPd: what was measured

**Setup.** Five separate copies of main `760e1a64`, made from the GitHub tarball (sha re-read with `gh api -X GET` at 17:40:32 AEDT: `760e1a644ce9a419cf1b9132d0776e9e5eac1cac`), under `x2157/ox/c1..c5`. Toolchain: `<OXPd_2>/.tools/dotnet/dotnet` 10.0.404, offline (closed proxy 127.0.0.1:9), `DOTNET_CLI_HOME`/`HOME` per copy inside my folder, the project's own NuGet cache, node reuse, build server and shared compiler all off (the same environment `heavy.py` sets). The wave lock `wave1-heavy.lock.d` was taken by `mkdir` with an `owner.txt` naming B2157 at **17:40:20** and moved into `x2157/_quarantine/locks/20261127-183800-b2157-oxpd` at **18:38:00** (57 min 40 s, under s334's 100-minute cap). s334's load check ran before every batch: two load1 reads 120 s apart, both under 24 (every gate is logged in `logs/oxrun2.out`).

**Reused from the first B2157 agent (complete, so reused, and said here):** the five copies, `restore --locked-mode` (all five rc 0, 3.9 to 4.6 s at N=5, offline) and one Release build per copy: a full build (36 outputs) took **7.3 s alone, and 24.6 s each when four ran at once** (peak load1 93). That agent's one solution-test run (17:32) is **not** reused: it read 139 failures, all in `Lab.Tests`, all `exit 9`. The cause: it pointed `TMPDIR` into its scratch folder, which is inside the TUESDAY git work tree, and the lab tool refuses a run folder inside a git work tree (`RunFolderInGitWorkTree = 9`, `src/Datasec.Suite.Lab/Commands/Oxpd1/Oxpd1Command.cs:200`). That is an artefact of the experiment's setup, not a concurrency effect. I left `TMPDIR` at the system default, which is what a real lane uses.

### Whole-solution `dotnet test --solution Datasec.Suite.slnx -c Release --no-build`, N copies at once

| N | trial | wall per run (s) | result per run (passed/total, failed, skipped) | peak load1 | min free mem | pressure | hangs | EADDRINUSE |
|---|---|---|---|---|---|---|---|---|
| 1 | 1 | 61 | 2427/2431, 0 failed, 4 skipped | 31.6 | 90% | normal (1) | 0 | 0 |
| 1 | 2 | 63 | 2427/2431, 0, 4 | 17.8 | 89% | 1 | 0 | 0 |
| 2 | 1 | 104 / 105 | both 2427/2431, 0, 4 | 36.8 | 89% | 1 | 0 | 0 |
| 2 | 2 | 108 / 108 | both 2427/2431, 0, 4 | 45.1 | 89% | 1 | 0 | 0 |
| 3 | 1 | 150 x3 | all 2427/2431, 0, 4 | 53.9 | 89% | 1 | 0 | 0 |
| 3 | 2 | 157 x3 | all 2427/2431, 0, 4 | 31.9 | 88% | 1 | 0 | 0 |
| 5 | 1 | 249 x5 | **all five red**: 10, 10, 10, 12, 10 failed | 36.4 | 89% | 1 | 0 | 0 |
| 5 | 2 | 254 x5 | **all five red**: 10, 11, 11, 11, 10 failed | 56.8 | 89% | 1 | 0 | 0 |

Throughput (runs per hour): N=1 about 58; N=2 about 68 (x1.17); N=3 about 70 (x1.21); N=5 about 72 (x1.23, and every run red). **Each run's latency grows almost linearly with N (x1.7, x2.5, x4.1): one whole-solution test already fills the machine** (load1 reaches 18 to 32 with ONE run on 18 cores; `Lab.Tests` alone is 60 s of the 61 s critical path). Memory is never the limit: free memory stayed 88 to 90%, pressure level stayed normal, no swap-outs, compressor flat.

**What breaks at N=5: timing guards, not shared state.** All 105 failures across the ten N=5 runs are time limits: 102 are `Lab.Tests` cells cancelled by their own 30-second guard (`ProbeTests.Guard()`, `CancellationTokenSource(TimeSpan.FromSeconds(30))`; the first cell of each class ran 37 to 41 s under starvation), 2 are `Jobs.Tests` `ReceiverTests.C04` ("guard: the call did not end within 10 s of real time"), 1 is `Adapters.Oxpd1.Tests` `WriteTests.W05` (a 1-second client timeout against a 3-second stub delay, which lost its race). Different cells fail in each copy, which is the signature of starvation, not of a collision.

**Owed 137 (the Server.Tests hang): 0 occurrences in 22 whole-solution runs** (plus 0 in the first agent's run). `Server.Tests` passed every time (19 s alone, 54 s at N=3, 87 s at N=5). No run hung, none was killed, and no process of mine was left behind after any phase.

### Single test project `Datasec.Suite.UniversalPrint.Tests`, N copies at once

| N | trial | wall per run (s) | result | peak load1 |
|---|---|---|---|---|
| 2 | 1 | 8.8 / 8.8 | 351/351 both | 8.0 |
| 5 | 1 | 7.9 to 8.0 | 351/351 all five | 5.0 |
| 2 | 2 | 6.2 / 7.1 | 351/351 both | 2.6 |
| 5 | 2 | 7.7 to 7.8 | 351/351 all five | 1.4 |

Five at once cost nothing: the same 8 s as two, no failures. A light test project is not a heavy job.

### Shared state between concurrent copies (checked in code and in the runs)
- **Ports:** every OXPd test host binds `127.0.0.1:0` (Kestrel `Listen(IPAddress.Loopback, 0)`, `TcpListener(IPAddress.Loopback, 0)`; `Server.Tests` `HostRig` passes `https://127.0.0.1:0`). The fixed numbers in the code (7627, 8443) are URIs in contract tests, never bound. EADDRINUSE: 0 in every log. A few cells use bind-0-then-close probes (for example `Adapters.Oxpd1.Tests/ClientTests.cs:222`, `Adapters.Oxpd2.Tests/DeviceAuthCellTests.cs:605`), a theoretical time-of-check race; none fired.
- **Temp folders:** unique per cell (`lab-tests-<guid>`, `Directory.CreateTempSubdirectory("server-tests-")`); the five copies shared one system `TMPDIR` with no collision. `TMPDIR` must NOT be inside a git work tree (the exit-9 refusal above).
- **Secret store:** `Server.Tests` uses an in-memory store; each copy had its own `HOME`/`DOTNET_CLI_HOME`. Nothing was written to a shared key path.
- **obj/bin locks:** separate copies, so none. Two jobs in ONE checkout would collide in `obj/`; the semaphore below must keep "one job per checkout".

## NexusAI: what was measured

**Setup.** The first agent's NexusAI copies (`x2157/nx/n1..`) were checked out at `96a45f10`, NOT main: the local checkout does not hold `d2aeecf8`, so they were not reused. Main re-read with `gh api -X GET` at 17:40:32 AEDT: `d2aeecf8cda67265cc316646953c45d92b861f77`. Five copies from that tarball (`x2157/nx2/k1,k2,k3,k5,k6`, dot-free paths), each made a one-commit git repository so `worktreeRoot()` resolves to the copy itself (without a `.git` in the copy, every copy would resolve to the TUESDAY repository root and share ONE slot), `npm ci --no-audit --no-fund --prefix <copy>` with node 24.22.2 (rc 0 each; `sqlite3` native binding present and loads). Slots, printed by the repository's own `worktreeSlot()`: **k1 3, k2 4, k3 8, k5 7, k6 1**, all different (bands 21920-22559, 22560-23199, 25120-25759, 24480-25119, 20640-21279). `TMPDIR` at the system default. The whole run sat under `nexusai-lock.sh jest b2157-exp` with `NEXUSAI_LOCK_BASE=/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/session-tools/locks-laptop-1017` (the base live kits pass; the script's default, `/Volumes/Laptop-DEV/...`, is not mounted on this machine): acquired **18:38:52** after 0 s, queue empty, released **20:35:58** (record `released/done-jest-b2157-exp-40740-1795772158`). The planned sixth batch (N=1 again) was dropped to free the lock: I sent TERM to my own runner (pid 40757) after the N=5 line, between batches, with no test running.

**One failure is an artefact of the copies, in every run: `handover-gate-table.test.js`, 1 test** ("every SHA in the table resolves to a real commit": six SHAs, `ea6378d`, `7e5faa9`, ...). A one-commit copy has no history. So the clean result for these copies is **6633/6634, 418/419 suites**, and that is the baseline every row below is read against; it says nothing about concurrency. (A copy with history, fetched from a clone that already holds `d2aeecf8`, would remove it.)

### `npm run verify -- --maxWorkers=W`, N copies at once (plain mode)

| N | W | jest time per run (s) | result per copy | failures beyond the baseline | EADDRINUSE | peak load1 | min free mem |
|---|---|---|---|---|---|---|---|
| 1 | 2 | 1357 | 6633/6634 | none | 0 | 10.9 | 88% |
| 2 | 2 | 1343 / 1383 | 6633/6634 both | none | 0 | 6.4 | 89% |
| 3 | 2 | 1398 / 1390 / 1357 | 6633, 6633, **6561** | k3: `rd490-open-access-banner-browser` (72 tests): **a real cross-copy port collision** | 0 | 8.3 | 88% |
| 2 | 4 | 754 / 757 | **6632** both | k1 `rd421-sentinel-machine-id-follows-store-dir`, k2 `rd922-reset-empties-risk-conditions`: intra-run races at 4 workers | 0 | 9.5 | 88% |
| 5 | 2 | 1523 / 1515 / 1522 / **1474** / 1519 | 6633 x4, **6561** (k5) | k5: `rd490-open-access-banner-browser` (72 tests), the same collision again | 0 | 11.7 | 88% |

**The NexusAI suite is wall-clock bound, not CPU bound.** One verify holds load1 at 3 to 11 on 18 cores; three at once took 1357 to 1398 s each against 1357 s alone (at most 3% slower), so three copies give about **2.9x the throughput**; five took 1474 to 1523 s each (up to 12% slower) for about **4.5x**. Memory never moved (88 to 90% free, pressure normal, no swap-outs).

**The collision at N=3 (must be fixed before NexusAI runs more than one verify).** `rd490-open-access-banner-browser.test.js` does NOT use the worktree slot: it claims ports from a FIXED machine-wide band, `PORT_BAND = { start: 38900, end: 38940 }` (line 55), "proved free by refusal". During the N=3 batch (19:30 to 19:53) k3's copy of the suite took 38902 while k1's copy of the same suite had its product server (`nx2/k1/backend/server.js`, pid 99102, confirmed by `ps`) listening there; the test's own guard caught it ("server open (pid 99123) is not the one listening on 38902: listeners [99102]. Another process answered /api/health") and failed the suite. The reservation that protects this band is a per-process `Set` (`const used = new Set()`, line 84), so it protects two servers inside one jest run and nothing across two runs: both copies probe 38902, both see it refused, both take it. Today's one-verify lock is what keeps this hidden. The only fixed band in `__tests__` is this one (searched: `PORT_BAND`, fixed `PORT:` and `listen(<n>)`).

**Slots collide by chance.** `worktreeSlot` is sha256(path) mod 19, so two random paths share a slot 1 time in 19; three paths, about 1 in 6.6 (15%); five, about 1 in 2.3 (44%). I chose paths with five different slots; live kits name their clone paths freely. `guardServer` refuses foreign connections, but a shared band can still hand two copies the same port. A counting lock must therefore also refuse a second holder whose slot equals a holder's slot (a tooling check; see FOR TUESDAY).

**`--maxWorkers=4` halves the time (754 s against 1357 s) but breaks two suites inside ONE copy** (`rd421`: `resolveDataDir()` returned the copy's own `data/` instead of the case's HOME; `rd922`: `settings.json` missing from the data folder after `clear_db.js`). These are cross-worker races within a run, the hazard CLARIFICATIONS C-30's `--maxWorkers=2` exists for. Keep w=2.

## FOR TUESDAY

Commission for a tooling seat (B-number yours). Kam asked for the decision; this is the change set that implements the recommendation above. **Nothing here has been changed by B2157.**

**Title:** Counting locks for heavy jobs: OXPd semaphore of 2 plus a light-project bypass, NexusAI jest semaphore of 3 with slot-distinct holders, owed-137-safe kill, in-session, Opus.

**Order:** OXPd part (section 1) can land now. NexusAI part (section 2) can be built and proved now, but `slots-jest` stays ABSENT (one slot) until the NexusAI RD ticket for `rd490-open-access-banner-browser.test.js` (section 3) is merged on main.

**Rules for the seat:** write only the files named; every change installed by atomic `mv` with the old file kept beside it as `.pre-b<no>-<UTC>` (the house pattern in `session-tools/`); never `cd`; never delete; no live lock or ticket touched; run each script's own tests or the proofs below in your scratch folder with a test base (`NEXUSAI_LOCK_BASE=<scratch>`, and for `heavy.py` a `HEAVY_LOCK_ROOT=<scratch>` override added for tests only).

### 1. `heavy.py` (OXPd canonical runner, today sha256 31adedc8, 93 lines)
1. **Slots.** `SLOTS = int(open(P + '/.tools/heavy-slots').read())` when that file exists, else 1. One file is the one source of truth, so every copy of the runner agrees (an environment variable would let two kits disagree). The lock names are `wave1-heavy.lock.d` for slot 1 (unchanged, so a kit still carrying today's runner competes for slot 1 and the total can never exceed SLOTS) and `wave1-heavy.lock.d.2` ... `.d.<SLOTS>` for the rest. Acquire: try `os.mkdir` on slot 1, then 2, ...; the first that succeeds is held; `owner.txt` gains a `slot <k>` field. Release: move THAT slot's folder to `<lane>/_quarantine/locks/` (unchanged rule, slot number added to the name).
2. **One job per checkout.** Before acquiring, refuse (exit 96, `BLOCKED: checkout busy`) when any held slot's `owner.txt` names the same `<working folder>`; two jobs in one checkout collide in `obj/`/`bin/`.
3. **Load gate.** Today: load1 under 7 before taking the lock. That gate would keep a 2nd slot shut, because one OXPd solution test alone holds load1 at 18 to 32. New gate: slot 1 keeps load1 < 7; slot 2 and above need s334's check (two load1 reads 120 s apart, both under 24).
4. **Light-project bypass (option c).** A `dotnet test --project tests/<X>.Tests/<X>.Tests.csproj` whose project is in `<P>/.tools/heavy-light-projects` (one name a line; first entry `Datasec.Suite.UniversalPrint.Tests`) does not take a heavy slot; it takes `wave1-proj-<X>.lock.d` (one per test project) and runs under the same environment and time bound. A whole-solution test, any build, any restore, CodeQL: always a heavy slot.
5. **Kill the whole tree on time-out (owed 137's bound).** Today `subprocess.run(..., timeout=tmo)` kills only `dotnet` itself; the test hosts it started live on (`/private/tmp/b1839-gate/clone/.../Datasec.Suite.Sessions.Tests`, pid 2177, parent pid 1, was still alive today; `ps` gives its start as Sat 21 Nov 17:15:35; whether `heavy.py` started it is not proven, but it is the orphan shape this change prevents). Change to `Popen(..., start_new_session=True)`, and on time-out `os.killpg(pgid, SIGTERM)`, wait 15 s, `SIGKILL`, then list any process whose command line holds `<working folder>/` and print it as `ORPHAN <pid> <cmd>` (do not kill what is not in the group; report it).
6. **Start file:** `<P>/.tools/heavy-slots` containing `2`. Do NOT ship 3 or more for whole-solution work: at N=5 every run went red on timing guards, and N=3, although green twice, ran each job 2.5x slower for 1.2x the throughput.

Proofs (scratch base): two runners with `heavy-slots`=2 both acquire; a third waits and acquires when one releases; a today's-runner copy (slot 1 only) plus two new runners never exceeds 2 held; same-checkout refusal prints exit 96; a `sleep 600` job with `TIMEOUT=5` whose child forks a grandchild leaves no process behind; `heavy-slots` absent = exactly today's behaviour (one slot, load < 7).

### 2. `nexusai-lock.sh` (`/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/session-tools/`)
1. **Slots for `jest` only** (docker stays one): `SLOTS=$(cat "$BASE/slots-jest" 2>/dev/null || echo 1)`. Lock dirs: `$BASE/nexusai-jest.lock` (slot 1, unchanged name, so a pre-change copy still counts) and `nexusai-jest.lock.2` ... `.lock.$SLOTS`.
2. **FIFO kept.** The queue head (oldest live ticket, unchanged rule, unchanged ticket name shape) may `mkdir` ANY free slot, lowest first. Today only the head may try; with slots, the head acquires and leaves the queue, so the next ticket becomes head and may take the next free slot in the same poll. `--after`, `--replace` and MERGE-FIRST are untouched (they order tickets; slots only change how many heads run).
3. **Stale and ownerless takeover per slot** (the same pid + `pstart` test, applied to each slot dir; moved aside to `released/`, never deleted).
4. **Owner file** gains `slot=<k>`; the release trap moves its own slot dir only.
5. **Slot-distinct holders.** The caller passes its clone's port slot: the script runs `node -e 'console.log(require("<cwd>/__tests__/helpers/test-server.js").worktreeSlot())'` in the caller's working folder (or reads `NEXUSAI_WORKTREE_SLOT` when the caller has no clone there), writes `wslot=<n>` into the owner file, and the queue head does NOT take a free lock slot while any holder's `wslot` equals its own; it stays head and waits. Measured reason: sha256(path) mod 19 puts two paths in one slot 1 time in 19 (about 15% for any two of three), and a shared slot is a shared port band.
6. **Worker cap stays.** Every caller keeps `--maxWorkers=2` (the slot count was measured at w=2; `w=4` is reported in the NexusAI table).
7. **Start file:** `$BASE/slots-jest` containing `3`, written ONLY after the rd490 change is on main; until then leave it absent.

Proofs: the script's own lock tests (`NEXUSAI_LOCK_POLL=1`), plus: with `slots-jest`=K, K+1 waiters give exactly K holders and the (K+1)th acquires in ticket order on the first release; a pre-change copy (slot 1 only) racing new copies never makes more than K holders; kill -9 of one holder lets the head take over that slot only after the pid test; `slots-jest` absent = today's behaviour.

### 3. For a NexusAI seat (RD ticket; product repository, not tooling)
`__tests__/rd490-open-access-banner-browser.test.js` line 55 claims ports from the fixed band `38900-38939` with a per-process reservation (`const used = new Set()`, line 84), so two concurrent verifies can take the same port (seen at N=3 and N=5: 72 tests red in one copy, "server open (pid 99123) is not the one listening on 38902: listeners [99102]"). Move its band inside the copy's own worktree slot (`test-server.js` `workerBand()`/`nestedJestEnv()` style), keep its listener-pid check, and prove it with two copies on different slots running that suite at the same time, both green. The comment in `test-server.js` ("The slots also keep it below RD-490's 38900-38939") will need the same correction.

### 4. Kits and the coordinator
- Every OXPd kit's "one heavy job" sentence becomes "a heavy slot (at most 2 on this machine)". Lanes that only run one light test project name it and use the per-project lock.
- s334's load check (two load1 reads 120 s apart, both under 24) becomes the documented gate for any slot above 1.
- Kit lane folders must not be used as `TMPDIR` for OXPd tests (they are inside the TUESDAY git work tree; the lab tool exits 9).
- Re-measure before raising either number: this report's runners (`x2157/oxrun2.py`, `x2157/nxrun2.py`) run as they are on fresh copies (change the paths inside).
