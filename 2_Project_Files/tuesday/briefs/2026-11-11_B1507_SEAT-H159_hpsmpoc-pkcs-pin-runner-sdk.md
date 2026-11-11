From Tuesday (Datasec coordinator seat), Datasec / HPSM-POC. **Your STATUS file is the channel and the wrap** (no mail). A question is a last line `STOPPED: NEEDS TUESDAY <one question>`. Files naming another B-number are READABLE claims only.

# BRIEF B1507 | SEAT-H159: HPSM-POC, SMALL FIX: THE HOSTED RUNNER'S .NET SDK NOW CARRIES A NEWER `System.Security.Cryptography.Pkcs` THAN THE PROJECT'S PIN, SO TWO TRIPWIRE TESTS FAIL ON EVERY PR. NEW BRANCH `b1507/hpsmpoc-pkcs-pin` FROM MAIN, ONE COMMIT, ONE PLAIN PUSH, NO PR. NOT MERGED, NOT DEPLOYED.

**BLUF (MEASURED by Tuesday, 2026-11-11 ~17:0x, from PR #309's hosted job log, `gh api actions/jobs/130346525082/logs`, saved at `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s267/pr309/api.log` lines 320-342):** on PR #309 (a web-only branch, head 4f084fb3, on main 009421a2) the hosted `api (ASP.NET Core)` job failed 2 of 2301 in `HpsmPoc.Api.Tests.dll`, both in `PkcsInPackageTests`: `This_SDKs_framework_Pkcs_is_not_above_the_pin` and `The_published_api_carries_the_patched_Pkcs_dll_and_its_deps_entry`, message: *"This SDK's ASP.NET Core framework carries System.Security.Cryptography.Pkcs file version 10.0.1526.53008, above the pinned package 10.0.14 (file version 10.0.1426.52326), so a publish with it drops the package's DLL: raise the pin to 10.0.15 in HpsmPoc.Modules.Assessment.csproj (B255-2, HPSMPOC-271)."* The two `api on SQL Server` jobs failed too (UNMEASURED which tests: read their logs first). Main's own run of 2026-11-10 07:2xZ was green on all four api jobs: **the runner image moved, not the code.** Every other api suite passed (Assessment 300, Feedback 478, Reporting 850, Rules 164).

## READ WHOLE FIRST (read-only)
1. The project's `CLAUDE.md` and `JIRA.md`; the kit of today's HPSM lane for this machine's working rules (clone, identity, ports, heavy lock, no `cd`, never delete, scans): `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-11_B1497_SEAT-H157_hpsmpoc-lane-ha-customer-look-a11y.md` (its HOUSEKEEPING, TEST ROUTE and CHECKS sections apply to you, with the substitutions below).
2. At main: `api/tests/HpsmPoc.Api.Tests/PkcsInPackageTests.cs` whole (what the two tripwires measure and the remedy they print), the `System.Security.Cryptography.Pkcs` reference in `HpsmPoc.Modules.Assessment.csproj` (re-print by `grep -n`), `global.json` (the SDK pin and roll-forward), `.github/workflows/ci.yml` (which SDK the api jobs install), and every other file that names the Pkcs version (`git grep -n -i 'Cryptography.Pkcs'`; the audit exception lists, any `Directory.Packages.props`, ci.yml's NuGet audit step near the `vulnerable NuGet packages` line).
3. The two hosted SQL Server job logs of PR #309 (`gh api -X GET repos/datasecau/HPSM-POC/commits/4f084fb302a44b004e7efee8b666952120889011/check-runs`, then the failing jobs' `actions/jobs/<id>/logs` with `--allow-escape-sequences`, into your `.tools/b1507/` folder): name each failing test and say whether it is the same cause.
4. Tickets HPSMPOC-271 and HPSMPOC-254 (Jira GET; read only): the history of this pin.

## THE WORK
- **Prior work:** `git log -S 'Cryptography.Pkcs' --oneline` at main; quote what set 10.0.14 and why (an advisory fix: name it).
- **Confirm the cause locally, both ways:** with this machine's SDK, read the framework's Pkcs file version the way the test does (run the two tests at main: print pass/fail and the version they print). Then read which SDK the hosted job installed (its log's `setup-dotnet`/`dotnet --info` lines). State plainly whether this machine reproduces the hosted red or not (it may not: then the hosted log is the evidence, and the fix is still proven by the test's own arithmetic plus hosted CI on Tuesday's PR).
- **Fix:** raise the Pkcs package pin to **10.0.15** (the version the tripwire names) in `HpsmPoc.Modules.Assessment.csproj`, and in every other place the old version is pinned that must move with it (each named, with why). First read the 10.0.15 package's file version (from the NuGet package itself, `nuget.org` flat-container read is allowed for this ONE package, read-only) and print it: it must be >= the framework's 10.0.1526.x, else STOP (the remedy text is wrong and Tuesday decides). Do NOT disable, skip, loosen or edit the tripwire tests. Do NOT change `global.json` or the workflow unless the read in step 2 shows that is the real fault: then STOP and ask.
- **Proof:** the two tripwires green locally at head (with the version they print); the whole api test project at head 0 failed (counts printed beside main's); `dotnet list package --vulnerable --include-transitive` (or the ci.yml audit step's own command, read from ci.yml) at head with no new high/critical row; a publish of the API (the test's own route) carries the Pkcs DLL and its deps entry. Hosted CI is the deciding check (Tuesday's PR).

## PARTITION
**Yours:** `api/**/*.csproj` (the Pkcs pin only), `Directory.Packages.props` or any central pin file only if it carries the Pkcs version, any audit exception line that names Pkcs 10.0.14 only if it must move, `.tools/b1507/**`. **Not yours:** every test file (no edit), `web/**` (seat H158, B1503, is LIVE on HPSM in pane `Datasec/HPSM-POC-H158`: web, the shell, buttons and `infra/tests/test_ci_workflow.py`; you share only the `.tools/` heavy-lock slot its kit names), `.github/**`, `global.json`, `infra/**`, the open PR #309's branch.

## HOLDS
No PR, no merge, no deploy, no `az`, no hosted call except the one NuGet package read and the `gh api -X GET` reads above; no Jira write; no message to a human. Never delete (quarantine to `.tools/b1507/_quarantine/`). No `cd`. Ports **9650-9659** (`lsof` first). Identity: the project's configured identity copied into your fresh clone's local config (as B1497's Step 0), never overridden; READY prints `%ae | %ce`. Commit message plain ASCII, no B-numbers, ticket keys or names; one trailer (your session's attribution line).

## CONTEXT BAND
At about 70% start nothing new; at about 75% write `.../1_Project_Definition/Briefs/2026-11-11_B1507_HANDOVER.md`, last line `HANDOVER B1507: next <step> | done <steps>`.

## STATUS
`/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/1_Project_Definition/Briefs/2026-11-11_B1507_STATUS.md`. FIRST line `PROGRESS B1507: PENDING`; sections PRIOR WORK, CAUSE (hosted log lines, local reproduction yes/no, the SQL Server jobs' causes), FIX (file:line, every pin moved and why, the 10.0.15 file version), PROOF, NOT RUN, FOR TUESDAY. **LAST line on finish exactly** `READY B1507: <head sha40>` (= `git ls-remote` of the branch), else `HANDOVER B1507: ...` or `STOPPED: NEEDS TUESDAY <one question>`.

## Stamp
- STAMP: Tuesday s267, 2026-11-11, written whole by Tuesday from PR #309's hosted log (read at source).
- MAIN: 009421a28616c8b31dde86b59d4c4ca674c288fa (re-read it at Step 0; a moved main: name the moved paths, STOP only if one is yours).
- MODEL: claude-sonnet-5-5 -- C2 (a one-file dependency pin with a test that names the remedy; the gate after it is tier 1 because the package is a cryptography library) -- gauge 65%.
- AUTHORITY: Tuesday, under Kam's 2026-11-11 13:25 "please work on tickets and backlog items for all projects" and the CodeQL/CI rule (no merge on red). Nothing deploys (UAT held while HP reviews).
- HARD STOP: 20:30 AEDT 2026-11-11.

READ-WHOLE-BY-TUESDAY: DONE s267 (Tuesday wrote this kit whole)
