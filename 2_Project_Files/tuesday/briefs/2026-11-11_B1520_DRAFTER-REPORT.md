STARTABLE: YES
(kit: /Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-11_B1520_SEAT-M123_mps-sdk-exact-pin.md, 105 lines, `.pre-stamp` identical by cmp; 8 four-underscore lines = 7 Stamp slots + last line; 0 `@X@` tokens; 0 non-ASCII. Caveat for launch timing: both MPS heavy slots were held at drafting, so the builder will wait; READY target stays Step 0 + 90 min, never later than 22:30.)

## BLUF
- Recommended shape A: `global.json` -> `{"version": "10.0.404", "rollForward": "disable"}` (today `10.0.100` / `latestFeature`, a floor a whole feature band below CI), NO workflow line changed. Both setup-dotnet steps (ci.yml:38-40 job `dotnet`, :118-120 job `package`) read `global-json-file`, and setup-dotnet installs `--version 10.0.404` when rollForward is `disable` (source lines 203-250 at the pinned sha). This is MPSCALC-387 fix shape 2.
- Local: `.tools/dotnet` is SDK 10.0.401 only (shared/ref pack 10.0.12) and has no env.sh. The pin makes it refuse; the kit adds SDK 10.0.404 as a named step in a SIDE directory `.tools/dotnet-10.0.404` with the sha512 from the official release metadata (`1c9a13f6...5215e96`, osx-arm64). Side dir because four seats (M117/M120/M121/M122) build with `.tools/dotnet` and older branches say `latestFeature`.
- Pkcs pin stays 10.0.15 (csproj:28; comment :32 already says SDK 10.0.404 = 10.0.15). Tripwire PublishOutputTests.cs:96 can now only go red in a PR that changes global.json: "each .NET update needs its own pull request".
- Red-first: new `scripts/tests/test_sdk_pin.py` (picked up by the python job loop, ci.yml:102-104, no workflow edit): red at main (latestFeature), green after, nine planted-mutation rows, and a closed set of setup-dotnet jobs {dotnet, package}.
- Correction to the commission: there is no `infra/tests/test_ci_workflow.py` in MPS; the CI-reader is `scripts/tests/test_ci_workflow.py` (86 lines, no setup-dotnet or global.json row, untouched).

## Design answers
1. global.json 10.0.100 / latestFeature; one workflow file (139 lines); `grep -c -i 'setup-dotnet@'` = 2 (control: checkout count differs), both `global-json-file`, none `dotnet-version`. Job `package` only calls `bash scripts/package.sh` (ci.yml:128-130) whose `dotnet publish` is inside the script (package.sh:48), so the guard pins the set of jobs holding a setup-dotnet step instead of scanning for dotnet commands.
2. Hosted: newest green main run 42988098286 (9a0c4ba8): job `dotnet` 130414031404 runtime 10.0.15 (l.165), SDK 10.0.404 (l.176); job `package` 130416745896 l.167/178 same. Last green before drift, run 42761547464 (54ed7627, 2026-11-10), job 129648145803: runtime 10.0.14 (l.160), SDK 10.0.403 "already installed" (l.162). Official releases.json: 10.0.15 = SDK 10.0.404 / runtime / aspnet 10.0.15.
3. Local: MPS `.tools/dotnet/dotnet --version` = 10.0.401 (matches earlier today); only sdk 10.0.401. Recommendation A with side-dir; B (workflow-only, `dotnet-version`) is the Stamp alternative, not recommended (not exact; DERIVED). Smaller: B on the machine, A in the repository (2-line global.json, 1 new test, 1 doc line ENGINE.md:15).
4. No Pkcs move; test project's Cryptography.Xml 10.0.13 is not Pkcs and stays. Only test reading ci.yml is scripts/tests/test_ci_workflow.py (JOBS list etc.); none reads global.json.
5. Row: `scripts/tests/test_sdk_pin.py` as above.

## D-decisions
D1 A default, side-dir SDK. D2 closed set of setup-dotnet jobs. D3 No csproj/workflow edit. D4 One commit: global.json, new test, docs/ENGINE.md:15. D5 Package job proven once in a fresh clone before any Release build (package.sh refuses debug symbols in obj/Release), node 24 path as B1494. D6 First real 10.0.404 build of this tree on this machine, TreatWarningsAsErrors: a new warning is the finding -> STOP. D7 PR text may cite MPSCALC-387 (shapes 1 and 3 explicitly not done).

## Q for Tuesday (Stamp slots, each with default)
SHAPE A/B default A. LOCAL-SDK SIDE-DIR (default; merge into `.tools/dotnet` is Tuesday's after landing and after the four live seats finish).

## Port, pane, partition census
`lsof -nP -iTCP:9620-9629 -sTCP:LISTEN` 0 rows (control 11 addresses). Block text in B1494/B1505/B1508 (finished seats) and listed in B1515 as an earlier lane's block; M113 not in the pane list. Heavy slots: `.tools/.heavy-lock-1` and `-2` both present with holders written 19:56; load 10.94 at 20:01. Partition: mine = global.json, scripts/tests/test_sdk_pin.py (new), docs/ENGINE.md:15; none of M117/M120/M121/M122's named files.

## UNMEASURED
Hosted `--version 10.0.404` install (PR log decides); NETCore.App LTS-runtime float; any new analyzer warning under real 10.0.404; local whole-suite counts; open PRs not read.

## Outside-the-fences disclosure
Same as B1519's report: read-only gh GETs (contents, trees, runs/jobs logs, tarball at aae420ff, setup-dotnet source), Jira GET MPSCALC-387 (in-process, token not printed), the two curl reads of builds.dotnet.microsoft.com release metadata, local `dotnet --version`/ls, tmux/lsof, a failed ls-remote from the stale project checkout. Nothing written outside the briefs files and /private/tmp/b1519-drafter.
