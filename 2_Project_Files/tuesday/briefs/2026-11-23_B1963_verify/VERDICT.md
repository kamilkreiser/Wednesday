GATE B1963: GO @ aa80178 on main 5b66a7b

Gate G2 (test-only), round 1 of 2 of lane C7F, one Opus reader, in session, read-only. OXPd 2, lane C7F, kit B1961
(seat X44; Q1 = a in words at stamp S4, Q2 to Q6 the defaults, each the coordinator's, not the product owner's): the
gateway stub's connection race found by diagnosis B1955. Head `aa80178a5499c8a2cc3fc9dbd09ad1343078d0f9` on
`b1961/c7-hub-registration-wait`, ONE commit, one parent `5b66a7b1`. Read and measured 2026-11-23 07:12 to 07:28 AEDT on
Opus 5.5 in my own scratch `fleet/state/s314/g1963/`: `clone` (the kit's `clone.py ... draft`: push URL
`invalid://no-push`, no identity) and worktrees `red` (`5b66a7b1` + `1-red.diff`), `head` (`aa80178a`), `pchk`
(`5b66a7b1` + both patches); `probe` (a scratch console project outside the clone, never copied into it). Every dotnet
job and test executable through the kit's `heavy.py` (sha256 `31adedc8...`) and the wave lock, one at a time (25 jobs,
lock waits 0 but one of 17 behind my own loop; load1 2.4 to 5.5; no other holder's lock met). Origin by `gh api -X GET`
under the project GH_CONFIG_DIR: main `5b66a7b1`; this branch `aa80178a`; `compare main...aa80178a` ahead 1, behind 0,
2 files; pull requests newest 30 (closed, merged), none open; open alerts on main 0. No write to the project, GitHub or
Jira; no push, no pull request, no re-run; no `cd`; nothing deleted (the scanner control moved to `g1963/_quarantine/`).

**BLUF.** The fix does what the kit says, and the ordering it rests on holds on the framework the runners load, MEASURED
here rather than inferred from a source branch: in the shipped `Microsoft.AspNetCore.SignalR.Core` 10.0.15 the IL of
`HubConnectionHandler<THub>.OnConnectedAsync` calls `HandshakeAsync` (IL_01fd), then `HubLifetimeManager.OnConnectedAsync`
(IL_0287, which is `HubConnectionStore.Add`), then `RunHubAsync` (IL_02eb), whose first call is
`HubDispatcher.OnConnectedAsync` (IL_003f), which calls `Hub.OnConnectedAsync` (IL_0155); and in a probe of 1000
connections on that framework the connection was among those a send reaches every time the hub's `OnConnectedAsync` ran
(1000 of 1000). So the hub's count proves the add, and the wait for 2 closes the gap. The head is BASE plus the two
frozen patches byte for byte. Red first at `5b66a7b1` + the seam: 1786 / 1 failed, the late cell, by `no hub message
arrived within 5 s`; my loop red 20 of 20, the unchanged C7 green in all 20. The head: 1786 / 0 / 1782 / 4, green 30 of 30;
4 of 4 mutants MATCH and undone, rebuilt, green again; the merge with main is the head's own tree; hosted run PASS on
both legs; scans clean. **No finding.** The seam's named limit (H7) is not reachable in any cell. The hosted Windows
failure itself is still not reproduced (named, not a finding).

## FOUND

None.

## INFO

1. **The ordering claim on the shipped framework (MEASURED, commission item 2).** `.tools/dotnet` holds SDK 10.0.404 and
   shared frameworks `Microsoft.NETCore.App` and `Microsoft.AspNetCore.App` 10.0.15 only. The probe printed
   `runtime 10.0.15 | .NET 10.0.15 osx-arm64` and `Microsoft.AspNetCore.SignalR.Core 10.0.0.0 | file 10.0.1526.53008 |
   informational 10.0.15+8e0f8ed2312954727f8919d7d1c2f78b483b4ee7` from
   `.tools/dotnet/shared/Microsoft.AspNetCore.App/10.0.15/`. Its IL listing (call/callvirt/newobj tokens resolved in IL
   order from each async state machine's `MoveNext`) gives, for `HubConnectionHandler`1.OnConnectedAsync`:
   `HubConnectionContext.HandshakeAsync` (IL_01fd) -> `HubLifetimeManager`1.OnConnectedAsync` (IL_0287) ->
   `HubConnectionHandler`1.RunHubAsync` (IL_02eb) -> in the finally `AbortAsync`, `Cleanup`, `OnDisconnectedAsync`;
   `RunHubAsync`: first call `HubDispatcher`1.OnConnectedAsync` (IL_003f); `DefaultHubDispatcher`1.OnConnectedAsync`:
   scope, `IHubActivator`1.Create`, `InitializeHub`, the filter pipeline, `Hub.OnConnectedAsync` (IL_0155);
   `DefaultHubLifetimeManager`1.OnConnectedAsync`: `HubConnectionStore.Add` then `Task.get_CompletedTask` (no await);
   `HandshakeAsync`'s success path writes the answer by `WriteHandshakeResponseAsync` (IL_0626, after `Log.HandshakeComplete`).
   This is the order of the diagnosis's release/10.0 copy (`HubConnectionHandler.cs:140` to `:160`, re-read by me).
   Behaviour, same framework, 1000 connections per mode: framework's own manager: hub `OnConnectedAsync` ran 1000, the
   connection present in `_connections` there 1000 of 1000, absent when the client read `{}` 0 of 1000; a recording
   subclass (one reflection read before `base.OnConnectedAsync`): present at the hub 1000 of 1000, absent when the client
   read `{}` **3 of 1000**, and the control read in the subclass before `base` absent 1000 of 1000, after `base` present
   1000 of 1000 (so the check can read false). The gap is native to the shipped runtime, not only the seam's.
   **The hosted legs:** the head's job logs print `dotnet-install: .NET Core Runtime with version '10.0.15' is already
   installed` and `... SDK with version '10.0.404' is already installed` on linux (lines 162, 164) and windows (149, 151);
   `global.json` pins `10.0.404`, `rollForward: disable`. That the ASP.NET Core framework there is also 10.0.15 is
   DERIVED (no runner line prints it); I ran nothing on Linux or Windows.
2. **The census (MEASURED, item 3).** `git grep` at the head over the whole tree for `HubTestClient.ConnectAsync`,
   `GatewayStub.StartAsync`, `SignalR`, `IHubContext`, `HubConnection`, `SendCoreAsync`: connects only at
   `GatewayStubTests.cs:85` and `:86` (the shared body); `StartAsync` at `:37`, `:49` (no step) and `:76` (the body's
   parameter); the one hub send `GatewayStub.cs:166`; the only other hit is `src/Datasec.Suite.Graph/GraphClient.cs:65`/
   `:68`, the Graph client's own private `SendCoreAsync`, not a hub. No other cell of any suite sends to a hub connection.
3. **The seam off by default (item 3).** `StartAsync(..., TimeSpan lateRegistration = default)` registers
   `LateRegistration` only when the step is above zero (`GatewayStub.cs:109` to `:112`); only `GatewayStubTests.cs:70`
   passes one. MEASURED by effect: at BASE + the seam C7 (zero) green in all 20 red-loop runs while the late cell was red,
   and the probe's default mode resolved `DefaultHubLifetimeManager`1` when nothing was registered. The closed
   `HubLifetimeManager<PrinterHub>` registration wins over `AddSignalR()`'s open generic: MEASURED by its effect, the red.
4. **No connection counted that is not added (item 3).** The hub's `OnConnectedAsync` is reached only through
   `RunHubAsync`, after the awaited lifetime-manager add (IL above); a failed handshake returns before the add
   (`if (!await connectionContext.HandshakeAsync(...)) return;`, source `:140` to `:143`), so it is never counted. The
   count is a per-stub singleton (`GatewayStub.cs:108`; each cell builds its own `WebApplication`), so another cell's
   connections cannot satisfy it. `HubRegistrations` reads the count under its lock before taking the waiter task
   (`:62` to `:70`) and swaps the completion source under the same lock (`:47` to `:51`): no lost wake-up;
   `RunContinuationsAsynchronously` keeps the waiter off the hub's thread.
5. **Under cancellation (item 3).** `changed.WaitAsync(cancellationToken)` (`:72`) on the cell's 10 s guard: MEASURED by
   `mNeverAdded`: both send cells red by `System.Threading.Tasks.TaskCanceledException : A task was canceled.` (2 hits),
   the assembly `Time: 20.186s` (two serial 10 s guards), no hang.
6. **H7, a disconnect before the send (item 3).** The count only rises (named limit, the kit's and the commit's). Not
   reachable in any cell (DERIVED): no cell closes a client before a send; the server's own closes need
   `DefaultHandshakeTimeout 00:00:15` (before a handshake only) or `DefaultClientTimeoutInterval 00:00:30`
   (`DefaultKeepAliveInterval 00:00:15` sends pings and closes nothing), MEASURED from `HubOptionsSetup` on 10.0.15, the
   stub setting none (the resolved options all unset); every cell ends by its 10 s guard.
7. **The late cell's cost (item 3).** MEASURED once (`-xml` of the whole Contracts executable at the head, no selector):
   late cell `1.065` s, C7 `0.293` s, healthcheck 0.063 s, negotiate 0.058 s; assembly 4.803 s, 149 passed. About 0.8 s
   more, in line with the kit's DERIVED "about 1 s" (the second add is 1000 ms after its handshake, overlapping the
   first's 500 ms). Hosted: Contracts 30.9 s linux, 26.4 s windows at the head, inside the spread diagnosis B1955 gives.
8. **Text in the repository.** The doc comments at `GatewayStub.cs:17` to `:20`, `:37`, `:101`, `:138` to `:141`, `:178`
   to `:182`, `:205` to `:207` and the cell comment `GatewayStubTests.cs:88` are true against the IL and the probe. The
   commit message equals the kit's `commit-message.txt` (subject 228 characters). Pointer drift in kit B1961 (BLUF item 2,
   `:62`/`:68` are the declarations; the calls are `:64`/`:70`), seen by the seat too: kit text only, no effect.

## WHAT I MEASURED

- THE TOOLS: the drafter's `seat-tools/` and the seat's `<lane>/gate/` each 10 of 10 sha256 equal to kit B1961's table;
  my copy `g1963/gate/` from `seat-tools/` (`cp -Rc`). `words.py --control`: `CONTROL FIRED: 13 of 13`.
- Patches (`scratch/patchcheck.py`, `PATCHCHECK: OK`): BASE files equal to THE CODE's BASE column; `red` worktree equal
  to the "After `1-red.diff`" column; head files equal to "After both"; `TestSupport.cs`, the `.csproj` and
  `packages.lock.json` equal at both; `pchk` (BASE + both patches by `git apply`) `diff --quiet` against the head rc 0,
  control against BASE rc 1; a second `apply --check` of `2-fix.diff` refused rc 1; name-status exactly two `M` rows
  (control: a planted `A` row judged False); numstat `98 2` and `15 1`; 553 files; one commit in `BASE..HEAD`.
- `5b66a7b1..aa80178a` read whole (both files whole at the head: 305 and 147 lines).
- RED (`red`): locked restore rc 0; build 0/0; `status --porcelain` the two `M` rows only; Contracts executable
  `Total: 149, Errors: 0, Failed: 1`, `[FAIL]` the late cell, next line `no hub message arrived within 5 s`; `loop_c7.py`
  20 red: `controls: summary lines 20 (required 20); the base cell among the failed lines 0 (required 0)` / `LOOP red: 20
  of 20 as expected, 0 not (112 s)`; whole solution `total: 1786`, `failed: 1`, `succeeded: 1781`, `skipped: 4`, the one
  failed line `failed Datasec.Suite.Contracts.Tests.GatewayStubTests.C7_one_send_reaches_every_connection_once_when_the_hub_adds_each_connection_late (5s 086ms)`.
- GREEN (`head`): `restore --locked-mode --force` (CI=true) rc 0; build 0/0; `Test run summary: Passed!`, `total: 1786`,
  `failed: 0`, `succeeded: 1782`, `skipped: 4`.
- MUTANTS (`mutants_c7f.py ... run`, my run, independent of the seat's):
  `MUTANT mNoWait | Total 149 Failed 1 | red C7-late | expected C7-late MATCH | undone equal True`;
  `MUTANT mWaitForOne | Total 149 Failed 1 | red C7-late | expected C7-late MATCH | undone equal True`;
  `MUTANT mCountIgnored | Total 149 Failed 1 | red C7-late | expected C7-late MATCH | undone equal True`;
  `MUTANT mNeverAdded | Total 149 Failed 2 | red C7-late C7-send | expected C7-late C7-send MATCH | undone equal True`;
  `MUTANTS: 4 of 4 MATCH, 4 of 4 undone equal`. Messages: the 5 s message 1 each in the first three; `TaskCanceledException`
  2 in `mNeverAdded`. After: `status --porcelain` empty, both files' sha256 "After both"; build 0/0, dll 07:19:57 later
  than the newest source 07:19:42; whole solution 1786 / 0 / 1782 / 4 again.
- LOOP green: `LOOP green: 30 of 30 as expected, 0 not (134 s)`, controls 30 of 30, base cell 0.
- MERGE with main of the moment (`5b66a7b1`, GET at 07:21): `git merge-tree --write-tree 5b66a7b1 aa80178a` =
  `ab0873b2f90045ff9a2b4dd93c968ef110b99273` = `aa80178a^{tree}`: the merge is the head, so 1786 / RULES 553 above are
  the merge's. `repo_rules.py` (no `--source-documents`) on `pchk`: `RULES-NOTE: R5 hash half NOT RUN (no supplied-source
  folder here)`, `RULES: clean (553 files)`.
- HOSTED (`hosted2.py aa80178a... --total 1786 --rules 553 --skipped-linux 4 --skipped-windows 21 --unit 111 --floor 111
  --hardened-scan`, 07:17): run 45064412578, four jobs success, attempt 1; linux 1786 twice, succeeded 1782, skipped 4,
  GUARD clean 10 files; windows 1786 twice, succeeded 1765, skipped 21, GUARD clean 11 files; secret-scan every hardened
  row OK (`NEUTRAL-SCAN: stored objects 1404 (796 blob, 92 commit, 516 tree) ... not among them 0`); rules `Ran 111`,
  floor 111, `RULES: clean (553 files)`; last line `HOSTED aa80178a5499c8a2cc3fc9dbd09ad1343078d0f9: PASS`. `failed
  Datasec.` lines (case-insensitive) linux 0, windows 0; control: the C7 job log 137299375943 holds 1.
- PROBE (`g1963/probe`, logs `probe-run.log` 200 per mode and `probe-run2.log` 1000 per mode): INFO 1 and 6; `PROBE: OK`
  both runs.

## SCANS

- `words.py` over the 113 added lines (`scratch/added.txt`, by program from `diff -U0`) and the commit message as
  committed: `WORDS: clean (2 files)`; over `squash-subject.txt` (with #31), `squash-body.txt` and `pr-title.txt`:
  `WORDS: clean (3 files)`. `pr-body.md` holds `coordinator` and `product owner` in its "Who decides" section by design
  (the B1960 form); it is pull-request text, not repository text.
- ASCII: both head files 0 lines outside printable ASCII or with a tab, 0 CR, a final LF (control: planted U+200B 1).
- gitleaks 8.30.1: control FIRST (a token built from two halves and 36 random characters, never printed) rc 1, `leaks
  found: 1`, moved to `g1963/_quarantine/gl-control`; the added lines, the message, both patches, `commit-message.txt` and
  the two head files as `1.txt` to `7.txt`: rc 0, `no leaks found`; `gitleaks dir` over `pchk` (the head's files): rc 0.
- `build/squash_scan.py` (main `5b66a7b1`'s, from `pchk`) over `subject-31.txt` and `squash-body.txt`: control rc 1,
  found 2; message rc 0, found 0; `SQUASH-SCAN: clean`.
- gitleaks over this folder (`gitleaks dir`, same options, 07:28, before this line was added): rc 0, `no leaks found`.

## CODEQL

Not run locally. The head's push run has no Analyze rows (`check runs beside the four: 0`); code scanning is read on the
pull request (landing.txt step 3). Open alerts on main: 0 (GET).

## NOT RUN

- Anything on Linux or Windows locally; a hosted loop of C7 (kit Q5, not in this lane); any re-run.
- The hosted Windows failure (run 45052136167) reproduced: not reproduced by anyone; that its gap is this gap is DERIVED.
- The ASP.NET Core framework version on the hosted test hosts printed by a runner line: no such line (DERIVED 10.0.15).
- `repo_rules.py --source-documents`; the server; the publish lines and the release guard (the seat ran them, RELAYED;
  this change touches no `src/` line).
- CodeQL; the pull request's own run (none exists yet).

## DEVIATIONS

- The green loop ran 30 times (the commission names no count; the seat's was 50).
- The probe is a scratch project `g1963/probe` (Microsoft.NET.Sdk.Web, no package reference), restored without
  `--locked-mode` (it has no lock file) and with `NUGET_PACKAGES=g1963/nuget-probe` so the project's package cache is not
  written; built and run through `heavy.py` like every other job. Nothing of it entered the clone.
- One run of the Contracts executable with `-xml <scratch file>` for per-cell times: the whole executable, no selector.
- None else.

## TREES LEFT

`/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s314/g1963/`: `clone` (its local `main` at BASE, clean; worktrees
`red` = BASE + `1-red.diff` unstaged, built; `head` = `aa80178a`, clean, built, every mutant undone and proved; `pchk` =
BASE + both patches unstaged, not built), `probe` (built), `gate/` (the ten tools, unchanged), `logs/` (every job's log,
`gate.log`, `loop-red/`, `loop-green/`, `hosted-head/`), `scratch/` (`patchcheck.py`, `added.py`, `leaks.py`,
`added.txt`, `message.txt`, `subject-31.txt`, `neutral/`, `mutants/`, `head-exe.xml`), `_quarantine/` (`gl-control`, 25
moved lock folders), `dotnet-home/`, `nuget-probe/`. No process of mine running; the wave lock not held (absent at 07:27).
