GATE B1507: GO WITH FINDINGS @ 15be881 on main 009421a

Tier 1 (a cryptography package pin behind GHSA-846f-f764-76mx and GHSA-2fmv-rv2c-59x7). Gate run 2026-11-11 17:35-17:50 AEDT.
Work folder: /Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s268/gate1507/ (own clone `repo`, push URL invalid://no-push-gate; worktrees `wt-main`, `wt-head`; scratch SDK `dotnet-sim`; logs in `logs/`; scripts in `scripts/`).

## Findings

| # | Severity | Finding |
|---|---|---|
| F1 | Minor | FOR TUESDAY item 2 holds, but one of its suggested remedies does not work: `rollForward: latestPatch` would still let 10.0.401 roll to 10.0.404 (same 4xx feature band). Only `disable` (or an exact version installed by the workflow) stops this float. DERIVED from global.json semantics, not run. |
| F2 | Minor | The builder's main control publish (`pub-main-sim`) was built with the local SDK and published `--no-build` with the scratch SDK (phase_post.sh:18; simmain ran without `--restore-build`). That mix is why its deps.json still lists `/10.0.14`. When I built and published entirely under the scratch SDK, main has no DLL and 0 deps entries. Its conclusion (main drops the DLL) still holds. |
| F3 | Minor | HPSM's `CLAUDE.md` has no landing rule (`grep -n -i 'squash\|merge\|land'` returns 0 lines). Head-pinned squash is supported only by precedent: `1_Project_Definition/CLARIFICATIONS.md:138` ("squash-merged head-pinned"). |
| F4 | Info | The branch commit's trailer is `Claude Sonnet 5.5`. `squash-body.txt` carries the gate's attribution line in its place. |
| F5 | Info | Open-PR overlap was not re-read (no hosted API under this commission). The builder said #309 was the only open PR and that it is web-only (RELAYED). This one csproj line is not in #309's lane. |

No Blocker. No Major.

## Checks (each with its instrument and a control that can fail)

1. **Refs.** `git ls-remote` over the deploy key at 17:36: `refs/heads/b1507/hpsmpoc-pkcs-pin` = 15be88149e5aeb4315b3e2b8281f18fb3772898a (= READY). `refs/heads/main` = 009421a28616c8b31dde86b59d4c4ca674c288fa (unmoved). Head's parent = main. The branch has one commit. Identity is `88359143+kamilDatasec@users.noreply.github.com` for both author and committer.
2. **Merge.** `git merge-tree --write-tree main head` returns rc 0 with tree fdeaefa5af02507b4ede3796be5e46649dd3e6ba, which equals head's tree. `diff --numstat main <merge tree>` shows `1 1 api/src/HpsmPoc.Modules.Assessment/HpsmPoc.Modules.Assessment.csproj`, so the merge is exactly one line: `Version="10.0.14"` -> `Version="10.0.15"` at :32.
3. **(d) No other pin.** `git grep -n -i 'Cryptography\.Pkcs'` at main and at head finds the same places:
   - `HpsmPoc.Api.csproj:19` (a comment) and `:27` (`PackageConflictPreferredPackages`, which has no version);
   - the Assessment csproj `:32`, the only versioned pin;
   - `PkcsInPackageTests.cs`, which holds fixtures and messages.

   `git grep -l -i pkcs` also hits `BoundedProcessTests.cs`, but only in comments. The tree has no `Directory.Packages.props`, no `packages.lock.json` and no nuget.config. `git grep '10\.0\.14'` outside *.cs and *.md finds 0 lines at head. ci.yml has no exception list.
4. **(a) The 10.0.15 package's file version.**
   - **Copy and hash.** I copied `<P>/.tools/b1507/nuget/pkcs.10.0.15.nupkg` (no re-download). Its sha256 is 72d349612da39d21ee2ee45dfbcf45c7d80908ccfabd5b64da5ba61c71b46a60 (= claimed), 1,147,636 bytes. The nuspec has id `System.Security.Cryptography.Pkcs` and version `10.0.15`, and the package carries `.signature.p7s`.
   - **Provenance.** The copy's sha512 equals the `.nupkg.sha512` that NuGet's own restore wrote to `~/.nuget/packages/system.security.cryptography.pkcs/10.0.15/`.
   - **My own PE reader** (`scripts/pever.py`, reading VS_FIXEDFILEINFO and the StringFileInfo) on `lib/net10.0/System.Security.Cryptography.Pkcs.dll`: fixed FileVersion **10.0.1526.53008**, string FileVersion 10.0.1526.53008, ProductVersion 10.0.15+8e0f8ed2312954727f8919d7d1c2f78b483b4ee7.
   - **Control.** The same reader on the cached 10.0.14 DLL prints 10.0.1426.52326, the number the hosted tripwire printed for the pin.
   - **Result.** The package equals the hosted framework's 10.0.1526.53008, so the brief's ">=" is met. It is a tie, which the rank target must settle.
   - **Newest version.** The builder's saved index.json shows 10.0.15 as the newest 10.x.
5. **(b) Scratch-SDK reproduction, in my own folder.**
   - **Setup.** `dotnet-sim` = `cp -Rp <P>/.tools/dotnet`. `diff -rq` against the original shows exactly one differing file: `packs/Microsoft.AspNetCore.App.Ref/10.0.13/data/PlatformManifest.txt`. In it, line 42 changes `10.0.1326.50504` -> `10.0.1526.53008` (CRLF kept; the original is saved as `logs/PlatformManifest.10.0.13.orig.txt`).
   - **Pack in use.** `dotnet msbuild -getItem:ResolvedTargetingPack` shows Microsoft.AspNetCore.App resolving to `gate1507/dotnet-sim/packs/Microsoft.AspNetCore.App.Ref/10.0.13`. `command -v dotnet` points into dotnet-sim, and the SDK is 10.0.402.
   - **Runs.** Restore, build (0 warnings, 0 errors), the PkcsInPackageTests filter, then publish. All of these used the scratch SDK, in fresh worktrees.
     - **main:** Failed 2, Passed 31, Total 33. The failing rows are `This_SDKs_framework_Pkcs_is_not_above_the_pin` and `The_published_api_carries_the_patched_Pkcs_dll_and_its_deps_entry` (TRX per-test outcomes). Both messages match the hosted job's word for word (`<P>/.tools/b1507/job_130346525082.log:322,332`).
     - **head:** Passed 33, Failed 0, and both named rows Passed (TRX).
   - **Publish** (`scripts/deps.py`):
     - **main** (`pub-simmain`): DLL absent, 0 deps entries.
     - **head** (`pub-simhead`): DLL present (FileVersion 10.0.1526.53008, ProductVersion 10.0.15+8e0f8ed...) with exactly one deps entry, `System.Security.Cryptography.Pkcs/10.0.15`, which lists `lib/net10.0/...Pkcs.dll` at fileVersion 10.0.1526.53008.
   - **What this proves.** The head run exercises the exact tie, because the manifest and the package are equal. So the rank target is proven to keep the package, not just argued from arithmetic.
   - **Resolved package.** `project.assets.json` resolves Pkcs/10.0.14 at main and 10.0.15 at head.
6. **Whole `HpsmPoc.Api.Tests` at head, under the scratch SDK.** Total 2301, Passed 2288, Failed 0, Skipped 13 (6 m 47 s); 2301 equals the hosted total. By program (`scripts/trxcmp.py`), compared against the builder's main TRX (local SDK):
   - rows: 2301 / 2301;
   - outcomes: identical, and the 13 skipped sets are equal;
   - name differences: 7, all `UatOpenAssertionTests` theory rows whose display names embed time-based tokens, all Passed on both sides.

   I did not re-run main's whole project, to keep load down.
7. **(c) Vulnerability audit with ci.yml's own command** (ci.yml:59-65 verbatim apart from paths; `scripts/audit.sh`), solution `api/HpsmPoc.slnx`, 10 projects:
   - main: Critical 0, High 0, Moderate 0, Low 0, no problems;
   - head: the same.
   - **Firing control:** a copy of the builder's `control.csproj` (Pkcs 9.0.11), restored in my folder, gives `High ... GHSA-846f-f764-76mx` and `Moderate ... GHSA-2fmv-rv2c-59x7`. The restore itself also prints NU1903 and NU1902.
8. **(e) FOR TUESDAY item 2 holds.**
   - `global.json` at head is `{"version": "10.0.401", "rollForward": "latestFeature"}`.
   - The hosted log (`<P>/.tools/b1507/job_130346525082.log`) shows `actions/setup-dotnet` with `global-json-file: global.json` running `install-dotnet.sh --skip-non-versioned-files --channel 10.0` and printing `Installed version is 10.0.404`. It also installed runtime 10.0.15 via `--runtime dotnet --channel LTS`.
   - So 10.0.401 is a floor, not a pin. The SDK floats with each servicing release, and a records note saying the float "no longer holds" is wrong.
   - The MPS hosted log of the same day (`fleet/state/s267/pr176/dotnet.log` lines 171-188) shows the same 10.0.15 / 10.0.404 pair.
   - The remedy caveat is in F1. global.json and the workflows were not touched.
9. **Deploy on merge.** `.github/workflows/` holds only `ci.yml`, which has no deploy job (its header and steps say so). A merge to main builds and keeps a `deploy-api-<sha>` package for 7 days. Deploying it is a manual runbook step, so a merge triggers no deploy.
10. **Scans** (`scripts/scan.py`) over the added line plus the commit message:
    - names: 0, using the underscore-aware pattern with the ban list;
    - non-ASCII: 0; Cf: 0;
    - B-numbers and ticket keys: 0;
    - secret, GUID and host: 0;
    - the planted control (logs/scan-control.txt: a banned name inside `_by_..._`, a B-number, a ticket key, the word secret, U+200B) fired on all five.

    CodeQL pre-scan does not apply (one XML line, no JS). The repo's `infra/tests/test_hidden_characters.py` at head ran 14 tests, OK.

## Builder's claims, graded
- Branch head and main at push: **true** (ls-remote).
- What set 10.0.14 (#225, framework tracking, not an advisory fix): **not shown** by the gate (not re-read). It is consistent with the test file's header and the commit text.
- 10.0.15 DLL FileVersion 10.0.1526.53008 and nupkg sha256: **true**.
- Local SDK does not reproduce, while the scratch SDK reproduces byte for byte: **true** (re-run independently).
- Head is green on the scratch SDK (33/33): **true**.
- Whole project main = head (2301 / 2288 / 0 / 13): head **true** under the scratch SDK; main **not re-run**.
- Publish rows: head DLL plus one deps entry, **true**. Main-sim "deps lists /10.0.14": **true only for its mixed-SDK build** (F2).
- Audit 0 at both, and the control fires: **true**.
- One line changed, no other pin: **true**.
- SQL Server shard red for the same cause, and the aggregate runs no tests: **not shown** (log not re-read by the gate). Relayed.
- FOR TUESDAY item 2: **true**, with F1's caveat on `latestPatch`.

## NOT RUN
- **Hosted infrastructure:** SQL Server shards (`api on SQL Server` x3), Azurite Blob tests (the 13 skips), CodeQL, and any hosted CI. Hosted CI on Tuesday's PR is the deciding check.
- **The real SDK 10.0.404:** not downloaded. The scratch SDK stands in for its framework's Pkcs file version only.
- **Other test runs:** main's whole Api.Tests run (not re-run; the builder's TRX was used); the other api test projects (Assessment, Feedback, Reporting, Rules); web, e2e, infra validate beyond the hidden-character test.
- **Reads:** open-PR overlap re-read (F5); Jira; the dependabot alert the builder's push banner named.
- No push, PR, merge, deploy, az, mail or board. No HTTP except the nuget.org advisory data that `dotnet list --vulnerable` and restore read, which is part of the commissioned audit command.
