GATE B1520: GO WITH FINDINGS @ cf03b45 on main c7f5202
Tier G2 (config and CI), one round, 2026-11-11 about 21:30 AEDT. Project MPS Calculator, ticket MPSCALC-387 fix shape 2.
Branch b1520/mps-sdk-exact-pin. No security-shaped issue found, so no tier escalation.

## FINDINGS
| # | Sev | Finding | Evidence |
|---|---|---|---|
| F1 | Minor | The guard reads step keys with a regex that needs a letter first, so a QUOTED key (`"dotnet-version": 10.0.x` is valid YAML and sets the input) is not seen. A hand-edit like that would pass the guard. Not in the file today. Other routes the builder already named (env override, install script, nested global.json) are also outside the guard: a DOTNET_ROLL_FORWARD env line added to ci.yml returned []. | probe on head: quoted dotnet-version key returned []; unquoted dotnet-version, dotnet-channel, source-url and `./global.json` each returned exactly one problem |
| F2 | Minor | The refusal text printed by the default SDK does not contain the words "rollForward: disable" (the builder said so; confirmed). It names Requested SDK version 10.0.404 and the global.json path; its "Installed SDKs:" list printed empty although .tools/dotnet/sdk holds 10.0.401. The refusal itself is the exactness. | refuse_head.txt, rc 155 |
| F3 | Minor | main has one flaky red: SourceLifecycleTests.B40_3_a_calculation_during_activation_uses_the_old_set_or_the_new_set_never_a_mix failed once in the whole-suite run at main (NullReferenceException in WebApplicationFactory.DisposeAsync, test line 250), passed 3 of 3 run alone at main, and passed in the whole runs at head and merge. Not caused by this change (it touches no .NET file); a hosted run may show it. | test_main.txt, b40_main.txt |
| F4 | Minor | No hosted proof exists yet; every hosted statement is for Tuesday to check on the PR run. One log nuance: if the runner image already carries SDK 10.0.404, the install script logs "dotnet-install: .NET Core SDK with version '10.0.404' is already installed" instead of "Installed version is 10.0.404" (the older green run logged "already installed" for 10.0.403). Either is a pass; neither is a fail. | see HOSTED LOG EXPECTATION |
No Blocker, no Major.

## 1. Refs
- `git ls-remote` of refs/heads/b1520/mps-sdk-exact-pin = cf03b45ad052bcf9df3824f815cccb1b9fd86e4c = READY sha. One ref with prefix b1520 on origin. main = c7f5202e649918f4a3e7a2d84bdb2660c3fc995d (read now).
- `git diff --name-status main...head` = 3 paths: M docs/ENGINE.md, M global.json, A scripts/tests/test_sdk_pin.py. OWNS (kit): global.json, scripts/tests/test_sdk_pin.py, docs/ENGINE.md line 15: 3 of 3 inside; the ENGINE.md hunk is line 15 only (diff read).
- Open pull requests: 1, number 181 (ops-tooling lane): 14 files under infra/, scripts/ and tools/demo/. Overlap with the 3 paths: 0. Control: pulls/99999 returns 404.
- Sibling lanes (branches on origin): the engine-docs branch edits docs/ENGINE.md only at hunks near lines 157-170 (disjoint from line 15); the web-print lane's kit forbids global.json, docs/ and scripts/; the e2e branch edits .github/workflows/ci.yml, and its ci.yml run through this guard with the pinned global.json returned [] (no setup-dotnet change), so if it lands first the guard stays green. Overlap 0.
- Commit: one commit, subject "Pin the .NET SDK exactly (global.json 10.0.404, rollForward disable)", author and committer address equal, one Co-Authored-By trailer.

## 2. Merge
`git merge-tree --write-tree main head` in my own clone (push URL set to an invalid scheme, nothing pushed): rc 0, tree 5c3fe5855e7ae4c47ffc1208d44f8dc3b0b44cb7. Diff main..tree = the same 3 paths. Blobs equal head's: global.json 89ddff24, test_sdk_pin.py f502ffd4, docs/ENGINE.md 66427c07. The QuoteWalkCaps.cs blob in the tree equals main's (2d203f8d). Clean, and equal to main plus the head blobs.

## 3. CI jobs run
My own worktrees of main, head and merge (a commit made over the merge tree); SDK 10.0.404 from the project-local side directory; NuGet from the machine cache (RestoreSources set to it, no registry read).
Jobs that read the changed files: dotnet and package (both read global.json through the SDK), python (test_sdk_pin.py reads global.json and ci.yml; test_ci_workflow.py reads ci.yml). Job web reads neither (not run). No tracked-file-walking scan exists in the python files or CI (grep for ls-files, os.walk, rglob in the test folders: one fake curl only); the dotnet suite is the repo-wide set.
| Program | main c7f5202 | head cf03b45 | merge |
|---|---|---|---|
| dotnet --version in the tree | 10.0.404 (latestFeature picks the side SDK) | 10.0.404 | 10.0.404 |
| build Release | rc 0, 0 Warning(s), 0 Error(s) | same | same |
| Engine tests | 743 | 743 | 743 |
| Import tests | 196 | 196 | 196 |
| Api tests | 3482 passed + 1 failed (F3) = 3483 | 3481 passed | 3483 passed |
| PublishOutputTests (3) | 3 pass | 3 pass | 3 pass |
Head has 2 fewer Api tests than main only because head's base lacks main's one-file test change; the merge reproduces main's 3483, all passed.
Python loop (python3 -I over tools/demo/test, infra/tests, scripts/tests; tests per file): test_demo_doc 10, test_run_demo 23, test_seed 22, test_seed_hosted 13, test_seed_purchase 10, test_ci_workflow 8, test_deploy_pre1 27, test_entra_all_roles 15, test_scripts 44: all rc 0 and identical at main, head and merge. test_sdk_pin: 13 tests rc 0 at head and merge (absent at main). infra/tests/test_infra.py rc 1 at all three trees: "no Bicep compiler" (tool missing here; NOT RUN; the hosted python job installs Bicep).
Package job: fresh worktree at the merge commit, `bash scripts/package.sh <sha> --out ...` with Node 24.22.2 and the side SDK, npm offline: rc 0, 50 files, B2 scan 0 hits.
Targeting pack under the real SDK 10.0.404: PlatformManifest.txt line 42 = System.Security.Cryptography.Pkcs.dll ... 10.0.1526.53008, equal to the Pkcs 10.0.15 pin at MpsCalc.Api.csproj:28.
Exactness control: with the project default .tools/dotnet first on PATH, `dotnet --version` in the head tree exits 155 "A compatible .NET SDK was not found. Requested SDK version: 10.0.404". The same tree under the side SDK prints 10.0.404.

## 4. Red without the fix
- The pin removed (main's global.json beside head's test and ci.yml): rc 1, exactly test_the_real_files_pin_one_exact_sdk fails with ["global.json: rollForward is 'latestFeature', not 'disable'"]; the other 12 pass.
- Five guard mutants on copies of head's test (one check switched off each): rollForward check off -> 3 roll plants fail; override-keys off -> the dotnet-version plant fails; global-json-file check off -> its plant fails; job-set check off -> 3 job-set plants fail; version-shape off -> 2 version plants fail. No plant is vacuous.

## 5. Closed lines
None in the kit (no ALREADY-ON-MAIN line). The facts main depends on were re-read: main's global.json is 10.0.100 / latestFeature (the red copy above); the csproj Pkcs pin 10.0.15 is unchanged.

## 6. Probes (guard function run on mutated copies)
Clean pair: []. Version "10.0.100-rc.1", rollForward "Disable", numeric version 10, and empty {} each flagged. `global-json-file: ./global.json` flagged. dotnet-channel and source-url flagged. Name-first step order parses. Quoted `"dotnet-version"` key NOT flagged (F1).
Code-fact check of the doc line: docs/ENGINE.md:15 says SDK exactly 10.0.404, pinned by global.json with rollForward disable: true at head. setup-dotnet source at the pinned sha (the builder's saved copy, read from disk, not fetched by me): getVersionFromGlobalJson switches on latestMajor, latestMinor, latestFeature, latestPatch and has no case for disable, so the version stays 10.0.404.

## 7. Scans (163 added lines and the commit message)
Names (Kam, Kamil, Kreiser, Steve, Peter, Paul, Blanchard, Inch, Waite; underscore-aware): 0 in added lines, 0 in the message; the planted `_by_<name>_` control fired for each. B-number, seat id, ticket key, uuid (tenant or subscription id), secret words: 0 and 0, each control fired. Host scan: the only match is the standard attribution trailer address. Cf characters and non-ASCII: 0 (planted U+200B control fired). The commit's author display name is a person name from the project git identity (metadata, not message text); not a finding.
CodeQL pre-scan (JS rows and the Python row): `new RegExp(` from a variable 0; hand-escape replace 0; innerHTML 0; child_process, subprocess, os.system 0; os.chmod, makedirs mode, os.open mode, Path.chmod, S_IROTH or any 0o literal 0. 0 hits, no CodeQL Major.

## 8. Claims graded (builder STATUS)
| Claim | Grade |
|---|---|
| One commit on the branch, parent aae420f, 3 files, ahead 1 behind 1 | true (ls-remote and diff) |
| Red at main's global.json with the rollForward problem; the rest pass | true (my red copy) |
| 5 guard mutants each turn exactly their plants red | true (my own mutants) |
| Build under 10.0.404: rc 0, 0 warnings | true at head and merge |
| Tripwires 3 of 3 green; Pkcs file version 10.0.1526.53008 from the real SDK | true |
| Whole suite 743 + 196 + 3481 at head, same names as main | true for counts; names not re-listed (merge equals main's 3483) |
| Python loop 10 of 11 green, the 11th needs Bicep | true (11 files; test_infra is the one red; tool missing) |
| Package job rc 0, 50 files | true |
| Refusal control names the requested version | true; the wording lacks "rollForward: disable" (F2) |
| Scans 0 | true |
| Main moved to c7f5202 touching one test file only | true; the merge is clean |
| No hosted proof claimed | true |

## HOSTED LOG EXPECTATION (Tuesday checks these on the PR's run)
Workflow: .github/workflows/ci.yml at head (the only workflow file). Both steps use actions/setup-dotnet@a98b56852c35b8e3190ac28c8c2271da59106c68 with only `global-json-file: global.json`.
1. Job `dotnet` (ci.yml:30), step `actions/setup-dotnet` (ci.yml:38-40). The step log shows two install-script invocations:
   - first, unchanged and expected: `install-dotnet.sh --skip-non-versioned-files --runtime dotnet --channel LTS`, then `Installed version is 10.0.<n>` (the shared runtime, which still floats; do not fail on this `--channel LTS` line);
   - second, the one that decides: `install-dotnet.sh --skip-non-versioned-files --version 10.0.404` (NOT `--channel 10.0`), then `dotnet-install: Installed version is 10.0.404`. Accept `dotnet-install: .NET Core SDK with version '10.0.404' is already installed.` in place of "Installed version" if the image carries 10.0.404; fail if neither appears or the version is not 10.0.404.
   Later steps in that job: ci.yml:42 `dotnet build MpsCalc.slnx -c Release` rc 0 with 0 warnings; ci.yml:43 `dotnet test` with Engine 743, Import 196, Api 3483 passed (my counts at the merge; the PublishOutputTests tripwires are inside the Api run). No step prints `dotnet --version`, so the install line is the SDK proof; a wrong SDK would show as "A compatible .NET SDK was not found" in the build step.
2. Job `package` (ci.yml:109, needs dotnet, web, python), step `actions/setup-dotnet` (ci.yml:118-120): the same two invocations and the same `--version 10.0.404` plus `Installed version is 10.0.404` (or the "already installed" form). Its step "scripts/package.sh" (ci.yml:128-130) then runs `dotnet publish` under that SDK and must end rc 0.
3. Jobs `web` (ci.yml:45) and `python` (ci.yml:84) contain NO setup-dotnet step: exactly 2 setup-dotnet steps in the run.
4. The hosted job that runs scripts/tests/test_sdk_pin.py is `python` (ci.yml:84), step "tools/demo, infra and scripts tests (python3 -I, standard library only)" (ci.yml:96-107): its log has a group `scripts/tests/test_sdk_pin.py` with `Ran 13 tests` and `OK`, and a printed line `setup-dotnet steps in jobs dotnet, package, each global-json-file: global.json`. In the same step infra/tests/test_infra.py runs (Bicep v0.48.1 is installed by the previous step, ci.yml:93-94); I did not prove it.
5. CodeQL (org default setup) runs outside ci.yml; land only when it is green.

## NOT RUN
- Hosted CI, hosted CodeQL, any hosted host (the setup-dotnet source was read from the builder's saved local copy, not fetched).
- infra/tests/test_infra.py (no Bicep compiler on this machine; fails the same way at main, head and merge).
- Job web (no web path changed; no web test reads global.json or ci.yml).
- A sorted test-name list comparison (counts compared; the merge reproduces main's 3483).
- Docker or a database (none needed). No port opened by me (block 9740-9749 unused); no server started.

## SCRATCH
Worktrees and logs: /Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s270/gate1520/
