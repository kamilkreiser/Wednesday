STARTABLE: YES

# B1961 DRAFTER REPORT -- OXPd_2 lane C7F (the gateway stub's connection race), seat `Datasec/OXPd2-X44`

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-23_B1961_SEAT-X44_oxpd2-c7f-hub-wait.md` (70342 bytes, 194 lines) and its sidecar `.measured` (130 claims, 130 measured; `stamp_check.py <kit>` rc=0). Scratch and every log: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s314/d1961/` (below `<d>`). Seat tools: `<d>/seat-tools/` (10 files, sha256 in the kit's THE TOOLS). Drafted 06:18 to 06:47 AEDT 2026-11-23 (clocks by `date`).

## BLUF
1. **The race is now reproduced** (the diagnosis had only inferred it). A test-only seam, `LateRegistration` (a subclass of SignalR's own `DefaultHubLifetimeManager<PrinterHub>`), adds the k-th connection k x 500 ms after its handshake answer. C7's own body, run under it, failed **20 of 20** on macOS with the hosted failure's exact message `no hub message arrived within 5 s`. The unchanged C7 stayed green in all 20 runs.
2. **The fix:** `PrinterHub.OnConnectedAsync` counts each connection in a per-stub singleton `HubRegistrations`. The shared C7 send body awaits `stub.WaitForConnectionsAsync(2, guard.Token)` after both connects and before the first send. The 5 s read window and the 10 s guard are unchanged. There is no retry and no `src/` line. After the fix: **50 of 50 green, twice**. 4 mutants, 4 MATCH, no survivor.
3. **Shape:** ONE commit, TWO files (`tests/Datasec.Suite.Contracts.Tests/GatewayStub.cs` +98 -2, `GatewayStubTests.cs` +15 -1). Two patches: `1-red.diff` (the seam plus the late cell, +43 -2) and `2-fix.diff` (the count, the wait and the doc lines, +70 -1). One new cell: `C7_one_send_reaches_every_connection_once_when_the_hub_adds_each_connection_late`. The seam's default is off (zero registers nothing).
4. **Totals (MEASURED, macOS):** whole solution 1785 to **1786** (`failed: 0`, `succeeded: 1782`, `skipped: 4`). The Contracts executable goes 148 to 149. `RULES: clean (553 files)`, `Ran 111 tests`. PREDICTED hosted: `--total 1786 --rules 553 --skipped-linux 4 --skipped-windows 21`.

## FACTS RE-MEASURED (instrument; control)
- Origin (`gh api -X GET`, the project gh-config, 06:18 and 06:45:05): main `5b66a7b16f9c35a48f7feef504c0fa69e5701dcc`. Open pull requests 0. `matching-refs/heads/b1961` 0 rows; control: `b19` 14 rows, `b1953/a2-f2-malformed-escape` at `10f446f3` among them. `.private` true, `.permissions.push` true.
- BASE hosted run (`hosted2.py`, 06:20:31): run 45056289720, `HOSTED 5b66a7b1...: PASS` at `--total 1785 --rules 553 --skipped-linux 4 --skipped-windows 21 --unit 111 --floor 111 --hardened-scan`.
- Census (`git grep` at BASE): `HubTestClient.ConnectAsync(` occurs only at `GatewayStubTests.cs:74` and `:75` in the whole tree. Control: `GatewayStub.StartAsync(` occurs 3 times. So the one C7 send body is the only cell that sends after a connect.
- Red (BASE + `1-red.diff`): `c1-exe-red` printed `Total: 149, Errors: 0, Failed: 1`. `c1-loop-red` printed `LOOP red: 20 of 20 as expected, 0 not (113 s)`, with control `the base cell among the failed lines 0`. `c1-test-red` printed `total: 1786`, `failed: 1`, and the grep count of the late cell's failed line is 1.
- Green: `c1-test-green` and `ch-test` each printed `total: 1786`, `failed: 0`. `c1-loop-green` (before a field rename) and `c1-loop-green2` (final) each printed `LOOP green: 50 of 50`.
- Mutants: `mNoWait`, `mWaitForOne` and `mCountIgnored` are each red on C7-late only, with the message `no hub message arrived within 5 s`. `mNeverAdded` is red on both send cells with `TaskCanceledException` (the guard fires). All 4 undone equal. A build after the last undo wrote the dll at 06:33:29, later than the newest source at 06:33:06.
- Chain: `restore --locked-mode --force` with CI=true left 28 of 28 lock files equal. Build 0/0. Both publishes rc 0. `GUARD: clean (10 files)` and `GUARD: clean (11 files)`. unittest `Ran 111` OK. `repo_rules.py` (no `--source-documents`) `RULES: clean (553 files)`.
- Checks: in `<d>/clone3`, `git apply` of both patches leaves both files `cmp`-equal to the prototype. name-status shows 2 `M` rows; the planted `A` control fails. The outside-paths `diff --cached --quiet` is rc 0 over 28 paths; control rc 1. ASCII 0 per file; U+200B control 1. gitleaks: control rc 1; clone3, clone and 7 neutral-named files rc 0. `run_step.py` neutral scan: 25 of 25, `objects of this commit not among them 0`, `no leaks found`. `words.py` printed `WORDS: clean (2 files)` over the 113 added lines and the message (control 13 of 13).
- Framework order (the diagnosis's source copies, `grep -n`): `HubConnectionContext.cs:643` writes the handshake answer. `HubConnectionHandler.cs:149` adds the connection, `:150` runs the hub, `:168` calls the hub's `OnConnectedAsync`. `DefaultHubLifetimeManager.cs:294` is `_connections.Add`. `:16` shows the class is public and not sealed; it has 16 `public override` members.

## D-DECISIONS (Tuesday's as coordinator; each a Q at the stamp)
- D1 (Q1, STOP-CLASS): the wait is on the hub's own `OnConnectedAsync` count, awaited once for 2 before the first send. It is not a longer window, a ping wait or a route-side wait.
- D2 (Q2): the seam stays, off by default, with ONE permanent cell under it (about 1 s per Contracts run, DERIVED).
- D3: the seam is a subclass with one override, not a decorator of about 16 forwarding members. That the container prefers the closed registration is measured only by its effect: the red.
- D4: no `src/` line and no README. The test folder has no README (`git ls-files` count 0; control: the Identity README 1).
- D5: one commit, on a new branch from BASE, with the rebase rule before the first push only.
- **Deviation from the diagnosis's sketch, chosen at drafting:** the k-th connection waits k steps, not a flat 500 ms. Without that, `mWaitForOne` would be a race between one loopback POST and the second connect. With it, `mWaitForOne` is red (MEASURED once).

## Q-QUESTIONS FOR TUESDAY (each with its default; the kit assumes the default)
- Q1 (STOP-CLASS): default **a**, the hub count plus `WaitForConnectionsAsync(2, ...)`. Alternative b: wait for a ping (DERIVED unsound, not built). Alternative c: a wait inside `/api/send` (not built).
- Q2: default keep the seam and its permanent cell. Alternative: drop the cell (the seam becomes dead code; a gate cannot repeat the red from the commit).
- Q3: default 500 ms, k steps. Alternative: a flat 500 ms (the diagnosis's form; it loses the `mWaitForOne` kill).
- Q4: default FOR RECORDS as written; the records seat files the race as found and closed.
- Q5: default **no hosted Windows loop in this lane**. A 50-run hosted loop needs a `ci.yml` line, which is outside the commission's owned paths. Tuesday decides whether to commission it separately. Never a re-run.
- Q6: default Opus, READY at Step 0 + 110, push by Step 0 + 80, pane X44, gate G2 round 1 of 2 on Opus, hard stop 11:00 AEDT.

## UNMEASURED
- Whether the hosted Windows failure (run 45052136167) was THIS gap. That is DERIVED from source plus the run's shape; it is not reproduced on a runner.
- The exact 10.0.x framework on the hosted legs. The drafter's macOS run loaded 10.0.15.
- Any hosted run of a head of this lane. Also never run by the drafter: `clone.py seat`, the branch, the commit and identity read, the push and its read-back, the rebase. These are listed as NEVER RUN in kit FACT 6.
- `mWaitForOne`'s red was measured in ONE run only.
- The cost of the late cell on the hosted legs (about 1 s, DERIVED).

## CHAIN INPUTS (DRAFTER_RULES MEASURED LITERALS item 4)
| Step | Inputs | Produced by or present at |
|---|---|---|
| 0 | the kit, Stamp S1 to S7 | Tuesday's stamp |
| 1 | `<src>` (10 files); `<repo>` local identity values; origin main (BASE); BASE's push run | `<d>/seat-tools/` (exists); `<repo>` (exists); GitHub |
| 2 | the two files at BASE | the clone of Step 1 |
| 3 | `1-red.diff`, `loop_c7.py`; the clone at BASE | Step 1's tools copy; Step 1 |
| 4 | `2-fix.diff`, `mutants_c7f.py`, `loop_c7.py`; the red tree built | Step 1; Step 3 |
| 5 | the green tree, mutants undone, rebuilt | Step 4 |
| 6 | the staged tree; `words.py`, `commit-message.txt` | Step 5; Step 1 |
| 7 | the commit; origin/main; `run_step.py`, `hosted2.py` | 7(a); the fetch in 7(b); Step 1 |

## PRIOR-WORK CHECK (done)
- Kit B1829 row C7 and gate B1830 `VERDICT.md` item 4: the stub was read and not probed, and the race was not seen.
- Only commit `5e36d8d` (pull request 6) ever touched the two files (`git log`).
- `BACKLOG.md`: `gatewaystub` 0, `c7_one_send` 0, `printerhub` 0, `gateway stub` 0, `flak` 0; control `tolerant` 8.
- `CLARIFICATIONS.md` (C-1 to C-69, 696 lines): `flak`, `race`, `signalr`, `gateway stub`, `printerhub` all 0; control `tolerant` 5. Nothing is ruled by the product owner on this subject.
- BACKLOG.md's sha256 changed during drafting (`84fadcd3...` at 06:19, `07086aad...` at 06:35): the records seat R302 is writing. The kit says so.

## OUTSIDE-THE-FENCES DISCLOSURE (everything the drafter did that touched anything beyond its two files)
- Writes outside the kit and this report were all under `<d>` (my scratch): three draft clones (`clone`, `clone2`, `clone3`; push URL `invalid://no-push`, no identity), `seat-tools/`, `gate/`, `logs/`, `scratch/`, `_quarantine/`, `out/` and `dotnet-home/`. Prototype source edits in `<d>/clone` were made with the Edit tool and one `sed -i ''` (renaming the private field `_gate` to `_sync`, because `words.py` counts `_gate` under the class `gate`; this was measured). While drafting, the drafter overwrote its own `seat-tools/2-fix.diff` and `commit-message.txt` before freezing them. The sidecar written by `--init` was replaced whole by `fill.py` via `os.replace`.
- Project tree: every heavy job ran through `heavy.py`, which `mkdir`s `<project>/.tools/wave1-heavy.lock.d` and then MOVES it into `<d>/_quarantine/locks/`. No other project write was made, and the lock was free at 06:47.
- GitHub: `gh api -X GET` only (ref, pulls, matching-refs, repo, check-runs, jobs and job logs of BASE). `git clone` ran three times (each fetches the origin).
- Nothing was pushed, committed, opened or messaged. No Jira call, no az, no HTTP beyond the tests' own loopback stub. No `Source_Documents/`, NAS or sibling-project read.
- No `decision_queue.sh`, no `briefs_staged/`, no ledger read.
- Test runs were made while gate B1960 shared the lock. This is allowed by the commission: they went through the shared lock and never broke it. Load was 2.25 to 9.88; `heavy.py` waits at 7.
