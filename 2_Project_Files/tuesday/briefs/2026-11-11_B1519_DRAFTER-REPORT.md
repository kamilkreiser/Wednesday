STARTABLE: YES
(kit: /Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-11_B1519_SEAT-H160_hpsmpoc-sdk-exact-pin.md, 105 lines, `.pre-stamp` identical by cmp; 9 four-underscore lines = 8 Stamp slots + last line; 0 `@X@` tokens; 0 non-ASCII; no card id, no person name.)

## BLUF
- Recommended pin shape A: `global.json` becomes `{"version": "10.0.404", "rollForward": "disable"}`, NO workflow line changes. `actions/setup-dotnet` (pinned sha a98b5685, `src/setup-dotnet.ts:203-250`) widens the version only for the four `latest*` roll-forwards; for `disable` it installs `--version 10.0.404` exactly, and the muxer then refuses any other SDK. Both setup-dotnet steps (ci.yml:46-48, :189-191) already read `global-json-file: global.json`.
- Why not workflow-only (B): `dotnet-version` in the steps leaves `global.json` at `latestFeature`, so a runner image carrying a higher 10.0.4xx still wins (DERIVED); and it forces an edit to `infra/tests/test_ci_workflow.py` `WITH_KEYS` (:580, pins setup-dotnet's keys to exactly `["global-json-file"]`) plus plants :1080-1084.
- Cost of A: local builds refuse until SDK 10.0.404 exists. Local SDK is a named step, extracted to a SIDE directory `.tools/dotnet-10.0.404` (never into `.tools/dotnet`), sha512 from the official release metadata (osx-arm64 `1c9a13f6...5215e96`, in the kit). A side-dir also means this machine reproduces the hosted Pkcs reading (10.0.1526.53008) for the first time.
- The SDK moved 10.0.403 -> 10.0.404 between two green main runs with no commit of ours (hosted logs, below). Pkcs pin stays 10.0.15 (csproj:32): SDK 10.0.404 = runtime/ASP.NET Core 10.0.15, framework Pkcs 10.0.1526.53008 = package 10.0.15.
- One honest limit: setup-dotnet's hard-coded first step `--runtime dotnet --channel LTS` still floats Microsoft.NETCore.App (10.0.15 today). Not fixable by input; named in the kit, effect UNMEASURED.

## Design answers (instrument in brackets)
1. global.json: version 10.0.401, rollForward latestFeature (gh api contents @ c014503d). One workflow file, ci.yml 682 lines; `grep -c -i 'setup-dotnet@'` = 2, control `actions/checkout@` count 9 (a different number); both `global-json-file: global.json`, no `dotnet-version`. Job scan (jobscan.py; control api job shows 6 dotnet commands): dotnet commands only in `api` (:32) and `api-sqlserver-shard` (:165).
2. Hosted SDK: newest green main run 42986630378 (c014503d): job `api` 130409245531 lines 140/151 = runtime 10.0.15, SDK 10.0.404 (SQL Server job 130409245383 same, lines 144/155). Last green before drift, run 42773429652 (009421a2, 2026-11-10), job 129686301623: runtime 10.0.14 (l.135), SDK 10.0.403 "already installed" (l.137). Official releases.json: 10.0.15 = SDK 10.0.404/runtime 10.0.15/aspnet 10.0.15 (2026-11-10); 10.0.14 = SDK 10.0.403 (2026-10-25).
3. Local: HPSM `.tools/dotnet/dotnet --version` = 10.0.402; sdk dir 10.0.401 + 10.0.402; shared and ref packs 10.0.12 + 10.0.13; `.tools/env.sh` sets DOTNET_ROOT to it. Pin would make these refuse -> handled by the side-dir named step (recommended) vs workflow-only B (Stamp SHAPE). Smaller change: B on this machine, A in the repository (A = 2-line global.json + 1 new test + 4 text lines, zero workflow lines).
4. Pkcs alignment: no move. Tests reading ci.yml/global.json: test_ci_workflow.py reads ci.yml (untouched under A); no test reads global.json content (git-grep over the pinned tarball: README.md:16,35,168; showcase.sh:55; ci.yml:48,191; test_ci_workflow.py:1083 plant; PkcsInPackageTests.cs:186,188 comment). Stale comment PkcsInPackageTests.cs:181-189 -> Stamp Q STALE-COMMENT.
5. Red-first: new `infra/tests/test_sdk_pin.py`; runs in the required infra job with no workflow edit (validate.sh:21 -> test_security_baseline.py:2857 loads every test_*.py). Red at main (latestFeature), green after; nine named plants (latestFeature, latestPatch, absent, version "10.0", "10.0.4", dotnet-version added, global-json-file removed, third job with setup-dotnet, a job losing it).

## D-decisions
- D1 Shape A default, side-dir SDK. D2 the guard pins the CLOSED SET of jobs with a setup-dotnet step ({api, api-sqlserver-shard}); it cannot find "jobs that run dotnet" by regex (MPS package job runs dotnet inside a script). D3 No Pkcs, csproj or workflow edit. D4 One commit: global.json, new test, README (16/35/168), showcase.sh:55 message. D5 PR text may cite HPSMPOC-271 (its owner/cadence clause: cadence = one PR per .NET update); commit may not. D6 rules-8: infra repo-wide scan (test_hidden_characters.py) named in Step 5.

## Q for Tuesday (each with a default; all are Stamp slots)
- SHAPE A or B, default A. - LOCAL-SDK, default SIDE-DIR (merging into `.tools/dotnet` after landing is Tuesday's: it changes every seat's default SDK at once; `.tools/env.sh` is machine-local). - STALE-COMMENT LEAVE/EDIT, default LEAVE.
- Not a Q but a flag: HPSMPOC-271 and the records seat R217 (pane %105) both touch the SDK-float statement; this kit writes no Jira.

## Port and pane census
`lsof -nP -iTCP:9680-9689 -sTCP:LISTEN` 0 rows (control 11 distinct listening addresses). Scan of 88 non-`.pre-` SEAT kits of 10-11 Nov (portscan.py; control finds 9650-9659 in B1515): block text appears in B1451/B1452 (gates, finished) and B1506 (Composer C96, not in the pane list). Panes: %105 HPSM-POC-R217 (records), MPS-M117/M120/M121/M122, NexusAI-N122; no HPSM code pane.

## Observations worth Tuesday's eyes
- The project checkout `2_Project_Files/.git/config` carries `core.sshCommand` naming /Volumes/Laptop-DEV (ls-remote from it printed identity file missing + Permission denied); local checkout is also stale (8869b1a vs c014503d). The kit has the builder clone by URL with its own key path.
- DRAFTER_RULES.md itself still names /Volumes/Laptop-DEV paths.

## UNMEASURED
Hosted behaviour of `--version 10.0.404` (DERIVED from source; the PR's hosted log decides). Whether a newer NETCore.App alone can matter. Whether 10.0.404 produces new analyzer warnings for HPSM (hosted main is green on 10.0.404, so unlikely). Whole-suite local counts at 10.0.404 (the seat measures). Open PR count (not read).

## Outside-the-fences disclosure
Read-only GETs: gh api (branches, contents, trees, actions runs/jobs logs, tarballs of both repos at the pinned shas into /private/tmp/b1519-drafter, actions/setup-dotnet source at its pinned sha, 4 `search/code` calls that hit the rate limit on later queries; core remaining 4957 afterwards). Jira GET of HPSMPOC-271 and MPSCALC-387 via an in-process helper (token never printed). One curl each of builds.dotnet.microsoft.com releases-index.json and 10.0/releases.json (public vendor metadata, asked for by design question 3). Ran the local `.tools/dotnet/dotnet --version` for both projects and `ls` of their trees. Two failed `git ls-remote` from project checkouts (stale key path; no ref write). tmux list-panes, lsof. No card read, no Secuura, nothing written outside the four briefs files and /private/tmp/b1519-drafter.
