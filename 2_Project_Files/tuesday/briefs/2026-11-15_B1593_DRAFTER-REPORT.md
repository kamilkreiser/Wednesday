STARTABLE: YES (after the stamp; 7 questions below, each with a default the kit already assumes)

# B1593 drafter report: MPS Commercial Calculator, lane M-O, package and SDK guard (seat M142)

Drafted 2026-11-15 19:41 to about 19:56 AEDT (`date` printed 19:41:58, 19:42:13, 19:44:01, 19:44:27, 19:45:10, 19:45:47, 19:46:54, 19:48:09 and 19:54:55). Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-15_B1593_SEAT-M142_mps-lane-mo-package-sdk-guard.md` (102 lines, 12 stamp slots left as `____`) with sidecar `.measured` (109 lines, tags F01 to F15). `stamp_check.py <kit>` rc 0 (109 claims, 109 measured; 49 of the rows are "INSTRUCTION to the seat" lines for names, paths and markers the seat writes).

## BLUF
- **All four keys fit one seat, in three parts: A = 224 (the patched Xml assembly ships in the package), B = 397 (one row that proves `all_problems` wires all three readers), C = 398 (six more routes the SDK pin guard reads). 349 is a measurement and stays OUT of the build.** Model row C3 Opus (224 is a security package surface; Parts B and C alone would be C2 Sonnet), gate G1, pane `Datasec/MPS-M142`, branch `b1593/mps-lane-mo-package-sdk-guard`, three commits, READY at Step 0 + 210 minutes, Part A pushed by +120. Nothing deployed; 224 stays OPEN after it lands (the host-side read is a deploy matter).
- **224 is harder than the ticket reads, and I measured why (6 publishes on SDK 10.0.404 in a scratch copy of main, restore from the machine cache).** Adding an Xml `PackageReference` at the tests project's 10.0.13: restore fails with NU1510 (a warning, raised to an error by `Directory.Build.props:6`); `NoWarn="NU1510"` on the reference makes restore rc 0, **but the publish still drops Xml** (the framework's 10.0.15 copy is higher), also with Xml first in `PackageConflictPreferredPackages`. A Pkcs pinned at 10.0.13 is dropped the same way (control). So the pin has to equal the framework's patch (15; Xml `fileVersion` 10.0.1526.53008 in the SDK's `Microsoft.AspNetCore.App.deps.json:176-178`) AND be ranked first. **Xml 10.0.15 is not in the machine cache (only 10.0.13); whether the registry has it is UNMEASURED**, so the seat's first restore decides, and a registry without it is a STOP (a lower pin is never an answer). The tests project's own Xml 10.0.13 pin then sits below the transitive one (NU1605, DERIVED), and its own comment says "Remove when the parent floors it".
- **349 confirmed by my own run** (not independent, so the kit makes the seat repeat it): base publish carries `System.Security.Cryptography.Pkcs.dll` with 2 deps lines; the same project WITHOUT the ranking target carries 0 DLL and 0 deps lines. Its Done-when is a confirmation (the clarifications record already lists it as a standing-rule candidate at `CLARIFICATIONS.md:3219`), so the seat records the measurement and the records seat moves the ticket. If the seat's run REFUTES it, Part A's commit carries the comment correction only.
- **397:** the drafter ran the plant through the guard's own functions: a root with a bad `global.json`, the real `ci.yml`, the real `package.sh` plus `export DOTNET_ROLL_FORWARD=Major`, and `src/global.json` makes `all_problems` return exactly three strings (printed in kit FACT 7). The new row goes in `test_sdk_pin_routes.py` with its own clean-root control; three mutants (drop each reader) must turn only it red; rows 34 become 35.
- **398:** I ran eight plants (a `GITHUB_PATH` write, `shell: pwsh`, `MSBUILDSDKSPATH`, `uses: ./...`, a run-time-built name, `allowPrerelease`, `paths`, a second workflow file): every one returned 0 problems; a plain `DOTNET_ROLL_FORWARD` control returned 1. The real files hold none of these routes. Decision D3 reads six routes by property and accepts two unreadable ones.
- Partition: only #196 (b1578) is open; its 12 files touch none of my paths, and its kit names `*.csproj`, `scripts/**`, `.github/**`, `global.json` NOT its own. Nine branches touch my paths and each is a merged-PR head. The python rows at main (rc 0): 13, 34, 8 tests.

## Scope, key by key (each ticket and all its comments read whole by Jira GET at 19:42, own helper `d1593/jget.py`)
| key | status | in slice? | reason |
|---|---|---|---|
| 224 | Backlog | **IN, Part A** | newest comment 41092 carries the product owner's 2026-11-11 ruling "Ship it in the package..."; clarifications entry C-126 at `CLARIFICATIONS.md:2869`; the `needs-ruling` label is stale |
| 349 | Backlog | **measured, not built** | 0 comments; Done-when = confirm the tie example (or correct a comment); standing-rule candidate |
| 397 | Backlog | **IN, Part B** | 0 comments; acceptance: one row red when either dropped reader is removed |
| 398 | Backlog | **IN, Part C** | 0 comments; "decide which routes", decided in D3 below |
Held/dropped check (pickup and today's note greps for 224, 349, 397, 398 and M-O): no DROPPED or HELD line names any of them; the pickup's M-O lines are B1554 (224 and 349 "WAITS (one dotnet kit, next)") and B1570. PRs naming the keys (196 read, controls #72, #181, #194 present, key 57 found in #6, #178, #195): 224, 397, 398 none; 349 only #181 ("held, with no change").

## Facts re-measured with instruments (details in the sidecar)
- Main `56578ac6a0371d111fa196e579718f9cf41fa2bc` at 19:42:13 [F01]; open PRs: #196 only; `heads/b1593` 0 rows (control `heads/b1564` 1 row).
- The six-variant table (restore rc, Pkcs DLL, Xml DLL) is in kit FACT 5 [F06]; logs in `d1593/restore_*.log`, `publish_*.log`, outputs `pub_v0 v3 v4 v5 v6`. `PrunePackageReference Remove` did NOT clear NU1510 (restore rc 1).
- Machine NuGet cache: Xml 10.0.13 only; Pkcs 9.0.11, 10.0.10, 13, 14, 15.
- `brief_seat.sh:40-41` exports `DOTNET_ROOT` to `<project>/.tools/dotnet` (SDK 10.0.401, refused by `global.json`); the kit tells the seat to override with `.tools/dotnet-10.0.404` in every command (printed `10.0.404`).
- Python: `python3 -I -B` 3.9.6; `test_sdk_pin.py` 13, `test_sdk_pin_routes.py` 34, `test_ci_workflow.py` 8, rc 0 [F09].
- Ports 9980-9989: 0 listeners (control unfiltered 27), 0 of 44 non-`.pre-` SEAT kits hold `998x` (control `997x`: 1 file, B1582, which proves the scan can fire; my first shell scan returned a false 0 on its control because zsh did not split the list, so I redid it in Python). The seat needs no listener; the block is offered only if Tuesday wants one.
- No `.heavy-lock-*` folder existed under the project `.tools` at 19:47; load 9-16 during my runs.

## Census: what reads the changed paths (frame: main `56578ac6`, by program)
- `src/MpsCalc.Api/MpsCalc.Api.csproj`: read by `PublishOutputTests.cs` (via `dotnet publish`), `scripts/package.sh:50` (publish), the `package` CI job; named in prose by `test_sdk_pin.py:18`; `tools/demo/test/test_run_demo.py:91` and `scripts/tests/test_scripts.py:587` write an EMPTY stand-in file with that name (unaffected). No python row parses its content.
- `ci.yml` is read by `test_ci_workflow.py`, `test_sdk_pin.py`, `test_sdk_pin_routes.py` (Part C extends the last two; the kit runs the whole CI python loop each push, rule 8). `.github` holds exactly one file.
- `deploy-package.py:172` refuses `.dll` only in a PROBE package, so a new Xml DLL in the app package is not refused (DERIVED).

## Chain inputs (rule 4), in execution order
| step | inputs | produced by / exists at |
|---|---|---|
| 0 | the kit, the STATUS path | exists at launch / this step |
| 1 setup + baseline | clone, identity, deploy key, `.tools/dotnet-10.0.404`, machine NuGet cache, python 3.9.6, heavy-lock protocol | BASE and the machine (each printed present above) |
| 1 baseline publish | restored solution | `dotnet restore` earlier in step 1 |
| 2 predictions | the baseline numbers | step 1 |
| 3 tie measurement | main-tree, base csproj, base publish list | BASE; step 1 |
| 4 Part A red-first | `PublishOutputTests.cs`, a base publish | BASE; step 1 |
| 4 Part A fix | the red names; Xml 10.0.15 from the registry (UNMEASURED that it exists) | step 4a; registry |
| 4 Part A green and file-list diff | pub-base (step 1), pub-head | steps 1 and 4b |
| 4 Part A mutants | the committed Part A tree | step 4d |
| 6 Part B | `all_problems`, the real `ci.yml` and `package.sh`; plant values of FACT 7 | BASE; Part A pushed |
| 7 Part C | Part B pushed tree; the eight plants (FACT 7) | step 6; BASE |
| 8 checks, CodeQL pre-scan | each part's diff, the CLI | steps 4 to 7 |
| 9 push | each part's diff, the gitleaks canary | steps 4 to 8 |

## D-decisions the drafter took
- **D1** One seat, Opus (C3), gate G1, all four keys, three commits; Parts B and C are python-only and light. **D2** 349 is measured by the seat (independent of mine) and recorded, never built; the records seat moves it. **D3** Part C reads six routes as properties with EMPTY allow-lists: no `GITHUB_PATH`, every `shell:` is `bash`, no `MSBUILD*` name, no local `uses: ./`, the `sdk` object holds only `version` and `rollForward`, the workflow folder holds only `ci.yml`; it accepts and documents two: names built at run time, and the runtime setup-dotnet first installs (not an SDK route). **D4** For 224: pin equal to the framework's patch read by program, Xml first in `PackageConflictPreferredPackages`, `NoWarn="NU1510"` ON THE REFERENCE (not project-wide), and the pin's tests are the existing Pkcs ones generalised plus two Xml rows with the Pkcs message kept byte-equal. **D5** The tests project's Xml pin is removed only if restore reports the downgrade. **D6** Rows go into the two existing guard files, no new test file (a new `scripts/tests/test_*.py` would run in CI with the runner's real tools).

## QUESTIONS FOR TUESDAY (each with a default)
1. **One Opus seat or two?** Default: one Opus seat (row C3), G1 gate. The alternative is Part A on Opus G1 and Parts B and C as a separate Sonnet G2 kit; they touch disjoint files, so they could run in parallel.
2. **349:** the seat measures and records; Tuesday has the records seat move it under the standing rule. Default yes.
3. **NuGet registry call** for Xml 10.0.15 after the cache fails (the B1554 precedent allows it; it is a package download, not a host probe). Default allowed, named in STATUS. If the registry lacks it the seat STOPS.
4. **398's two accepted routes** (run-time-built names; the runtime setup-dotnet installs first) are accepted by a docstring sentence. Default yes (developer-only; no word a customer sees). Say no and the seat reads neither.
5. **224 stays open** after this lands; the next deploy (its own card) reads the host's loaded Xml file version. Default yes; also the stale `needs-ruling` label on 224 for the records pass.
6. **Approval class:** the package change reaches the host only with a deploy card. Default: Tuesday cards it after the gate; nothing in the kit deploys.
7. **Port:** none needed; `9980-9989` is free if you want a block assigned (Stamp S7).

## UNMEASURED
Whether the registry holds Xml 10.0.15; that a pin at 10.0.15 plus first rank DOES carry Xml (DERIVED from the Pkcs tie, measured on Pkcs only: v0 vs v6); NU1605 in the tests project after the floor (derived, 10.0.15 not restorable here); test counts at base for the solution (I ran no `dotnet test`); how long a solution build and test take here; whether the CodeQL csharp pre-scan accepts `--build-mode=none`; the hosted `python` job's Python version; the real host's loaded Xml file version (no hosted call made). I ran no web or npm step.

## Outside the fences (disclosure)
Read: the commission file, DRAFTER_RULES, the B1582 kit, sidecar and report (template), B1554's kit lines 1-48 (dotnet precedent), the SWEEP-1925 M-5 text, B1578's lane table and B1591's grants (grep), `model-routing.md:84-116`, `models_latest.json`, `brief_seat.sh` (grep), `stamp_check.py` header, the project `CLAUDE.md:50`, `CLARIFICATIONS.md` (grep, lines 2869-2876 and 3219), the SDK folder's `deps.json` and `PackageOverrides.txt` under `.tools/dotnet-10.0.404`. Jira: GET only for 224, 349, 397, 398, 361 (token read in-process, never printed). GitHub: `gh api -X GET` only (ref, tarball, pulls, branches, compare). **Ran, beyond reads, two things the rules do not name:** (1) `dotnet restore` (offline, `--source ~/.nuget/packages`, so no HTTP) and six `dotnet publish -c Release` runs (they build Engine, Import and Api, a heavy-class job) in a scratch COPY of main's tree under `fleet/state/s279/d1593/t2`, with `DOTNET_CLI_HOME` in my folder; I took no heavy lock (no lock folder existed at 19:47, so nothing was waiting, and I did not write into the project's `.tools`); load was 9 to 16, under the 24 gate. (2) `codeql version` once (not a scan). Also `lsof`, `tmux list-panes`, `uptime`, `df`, and Python plants through the guard's own functions on a temporary root. Wrote only: the kit, its sidecar, this report, my folder `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s279/d1593/` (`jget.py`, `fill.py`, plant scripts, ticket dumps, tarball and tree, `t2/`, `pub_v*`, logs, `Api.csproj.orig`, `dnhome`), and one scratch file in the session scratchpad (`sc.out`, a copy of a `stamp_check` listing). No Jira write, no git write verb in any project repo, no push, no PR, no az, docker or ssh, no hosted HTTP beyond the GETs above, no `decision_queue.sh`, no card read, no message, no WEDNESDAY or FRIDAY tree, no `_ledger.md`. `date` is the only clock source.

DRAFTED B1593: kit 102 lines, sidecar rc 0, questions 7
