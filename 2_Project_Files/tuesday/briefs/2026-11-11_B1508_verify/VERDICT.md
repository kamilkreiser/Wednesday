GATE B1508: GO WITH FINDINGS @ 86f45e0 on main 54ed762

Tier 1 (a cryptography package pin behind GHSA-846f-f764-76mx and GHSA-2fmv-rv2c-59x7). This is the sibling of the HPSM pin gate, run in the same session (2026-11-11 17:44-17:58 AEDT).
Work folder: /Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s268/gate1508/ (own clone `repo`, push URL invalid://no-push-gate; worktrees `wt-main`, `wt-head`; scratch SDK `dotnet-sim`; logs in `logs/`; scripts in `scripts/`).

## Findings

| # | Severity | Finding |
|---|---|---|
| F1 | Minor | One PRIOR WORK claim is false. The STATUS says `25de7c1` (#70) "added the package pin (10.0.13 ...)". In fact `7af91de` (#42, 2026-10-16, "Pin System.Security.Cryptography.Pkcs and .Xml to 10.0.13 past the October advisories") added the pin. #70 added the ranking target and the B160 tripwire. The commit itself is unaffected. |
| F2 | Minor | The STATUS says a faithful local reproduction could not be made without fetching SDK 10.0.404. In fact one could: a copy of `.tools/dotnet` with one targeting-pack manifest line edited reproduces the hosted red at main, word for word (below). The builder's honest non-claim stands, and the gate now supplies the reproduction. |
| F3 | Minor | The SDK float caveat applies here too, and the floor is looser. `global.json` names `10.0.100` with `rollForward: latestFeature`, and the hosted setup-dotnet installed `--channel 10.0`, giving SDK 10.0.404 (`fleet/state/s267/pr176/dotnet.log` lines 183-188). Only `rollForward: disable` (or an exact SDK installed by the workflow) would stop the raise from recurring; `latestPatch` would not. DERIVED. Left to the owner; nothing was changed. |
| F4 | Info | The builder ran one baseline step with `cd` (disclosed in its STATUS). No effect on the commit. |
| F5 | Info | The branch commit's trailer is `Claude Sonnet 5.5`. `squash-body.txt` carries the gate's attribution line in its place. |
| F6 | Info | Open-PR overlap was not re-read (no hosted API under this commission). The builder said #176 was the only open PR, owning `src/MpsCalc.Api/Feedback/**`, `Sources/**` and tests (RELAYED). The csproj is outside that. |

No Blocker. No Major.

## Checks

1. **Refs.** `git ls-remote` over the deploy key at 17:44: `refs/heads/b1508/mps-pkcs-pin` = 86f45e06aac228cff6bcc107f381a3174adb9a24 (= READY). `refs/heads/main` = 54ed76273cf5e7eb804315635c413034f28b3372 (unmoved). The branch has one commit, whose parent is main. Identity is `kamil.kreiser@datasec.com.au` for both author and committer.
2. **Merge.** `git merge-tree --write-tree` returns rc 0 with tree 3e3b87d171a74a69241a9a73c736fb4d4c177fae, which equals head's tree. Numstat shows `2 2 src/MpsCalc.Api/MpsCalc.Api.csproj`:
   - `:28` `Version="10.0.14"` -> `"10.0.15"`;
   - `:32`, a comment only: `(SDK 10.0.403 = 10.0.14)` -> `(SDK 10.0.404 = 10.0.15)`.

   The pairing 10.0.404 = 10.0.15 matches the hosted log, where runtime 10.0.15 and SDK 10.0.404 are installed together, and the framework file version 10.0.1526.x.
3. **No other pin.** `git grep -n -i 'Cryptography\.Pkcs'` at main and head finds:
   - the csproj `:28` (the only versioned pin) and `:37` (the rank target, which has no version);
   - `PublishOutputTests.cs`.

   There is no `Directory.Packages.props`, lock file or nuget.config, and `git grep '10\.0\.14'` outside *.cs and *.md finds 0 lines at head. The test project also pins `System.Security.Cryptography.Xml` 10.0.13, which is not Pkcs and does not move. The resolved test-project assets read Pkcs/10.0.14 at main and Pkcs/10.0.15 at head, with Xml/10.0.13 at both.
4. **10.0.15 file version.** The builder used the same nupkg (sha256 72d34961...) that the HPSM gate verified in this session. My own PE reader gives FileVersion **10.0.1526.53008** and ProductVersion 10.0.15+8e0f8ed2...; the control on the cached 10.0.14 DLL gives 10.0.1426.52326. The DLL published at head (below) reads 10.0.1526.53008, which confirms it.
5. **Scratch-SDK reproduction (MPS's own SDK).**
   - **Setup.** `dotnet-sim` = `cp -Rp <M>/.tools/dotnet` (SDK 10.0.401, the only installed ASP.NET Core pack is 10.0.12). `diff -rq` shows exactly one differing file, `packs/Microsoft.AspNetCore.App.Ref/10.0.12/data/PlatformManifest.txt`. In it, line 42 changes `10.0.1226.42308` -> `10.0.1526.53008` (CRLF kept; the original is saved under `logs/`).
   - **Pack in use.** `dotnet msbuild -getItem:ResolvedTargetingPack` shows Microsoft.AspNetCore.App resolving to `gate1508/dotnet-sim/packs/Microsoft.AspNetCore.App.Ref/10.0.12`. `command -v dotnet` points into dotnet-sim, and `dotnet --version` is 10.0.401.
   - **Runs.** Restore, build (0 warnings, 0 errors, TreatWarningsAsErrors on), the `FullyQualifiedName~PublishOutputTests` filter, then publish. All of these used the scratch SDK, in fresh worktrees.
     - **main:** Failed 2, Passed 1, Total 3 (TRX per test). `B160_the_publish_output_carries_the_patched_pkcs_and_lists_it_in_deps_json` failed with "the publish output has no System.Security.Cryptography.Pkcs.dll: the host would load its own shared-framework copy". `A_publish_output_that_ships_the_assembly_without_its_deps_json_entry_fails_the_entry_count_first` failed with "control: the copy still ships the assembly". Both messages match the hosted job's (`fleet/state/s267/pr176/dotnet.log` lines 241-249). G1 passed.
     - **head:** Passed 3, Failed 0, with all three rows Passed.
   - **Publish** (`scripts/deps.py`):
     - **main** (`pub-simmain`): DLL absent, 0 deps entries.
     - **head** (`pub-simhead`): DLL present (FileVersion 10.0.1526.53008, ProductVersion 10.0.15+8e0f8ed...) with exactly one deps entry, `System.Security.Cryptography.Pkcs/10.0.15`, which lists `lib/net10.0/...Pkcs.dll` at fileVersion 10.0.1526.53008.
   - **What this proves.** The head run is the exact tie, because the manifest and the package are equal. The MPS rank target (`AfterTargets="ResolveTargetingPackAssets"`) keeps the package in both the build and the publish.
   - **Resolved package.** `project.assets.json` resolves Pkcs/10.0.14 at main and 10.0.15 at head.
6. **Whole dotnet suite at head, under the scratch SDK:**
   - Engine 743/743, Import 196/196, Api 3466/3466: 4405 passed, 0 failed, rc 0.
   - **By program** (`scripts/trxset.py`), compared against the builder's main TRX set (`<M>/.tools/b1508/out/trx-main`, local SDK): rows 4405 / 4405, all Passed on both sides; 0 names only at main, 0 only at head, 0 differing outcomes.
   - **Counts.** The STATUS's 4405 = 4405 is **true**. Hosted 3481 Api rows include PR #176's added tests.
7. **Audit.** MPS ci.yml has no separate audit step. Its gate is the restore's NuGet audit with `TreatWarningsAsErrors` (Directory.Build.props:6), and the head build had 0 warnings.
   - `dotnet list MpsCalc.slnx package --vulnerable --include-transitive --no-restore --format json` (7 projects): main 0 vulnerability rows and 0 problems; head the same.
   - **Firing control:** the 9.0.11 control project restores with 2 NU1902/NU1903 lines and lists `High GHSA-846f-f764-76mx` and `Moderate GHSA-2fmv-rv2c-59x7`.
8. **Deploy on merge.** `.github/` holds only `workflows/ci.yml`, whose header reads "NO cloud credentials, NO deploy job". A merge to main keeps a `deploy-mpscalc-<sha>` package for 7 days. Deploying it is a manual runbook step (MPS hosted is one card per deploy), so a merge triggers no deploy.
9. **Landing.** Head-pinned squash is supported by `CLAUDE.md:51` ("opens the PR and merges once CodeQL is green") and by `1_Project_Definition/CLARIFICATIONS.md:731` ("squash --match-head-commit").
10. **Scans** over the two added lines plus the commit message:
    - names: 0;
    - non-ASCII: 0; Cf: 0;
    - B-numbers and ticket keys: 0 (MPSCALC: 0);
    - secret, GUID and host: 0;
    - the planted control fired on all five.

    CodeQL pre-scan does not apply (XML only).

## Builder's claims, graded
- Branch head, main unmoved, one commit, one file: **true**.
- 10.0.15 file version 10.0.1526.53008 = framework, and nupkg sha256: **true**.
- Hosted cause (SDK 10.0.404 / runtime 10.0.15; two rows failed with those messages; 2 of 3481): **true** (hosted log re-read at lines 171-188 and 233-257).
- No local reproduction with the local SDK: **true**, though a faithful reproduction was possible (F2).
- Head tripwires green: **true**, and also green under the hosted framework value.
- Whole suite 4405 = 4405, 0 failed: **true**. Head was re-run under the scratch SDK; main was compared by program.
- Publish at head carries the DLL and one deps entry: **true**.
- Audit: no vulnerable packages at head: **true**.
- No other pin: **true**.
- PRIOR WORK, "#70 added the pin": **false** (F1). "#119 raised it to 10.0.14" and "#123 updated the tie sentence": **not shown** (the gate did not re-read them).

## FOR TUESDAY items, graded
1. Merge this, then PR #176 goes green: consistent with the gate's runs (main fails the two rows on the hosted framework; head passes). Hosted CI decides.
2. No ticket for the drift; it will recur at each ASP.NET Core patch: **holds** (F3: the SDK floats via `latestFeature` from 10.0.100). The suggested durable fixes (a framework-printing tripwire, an SDK pin) are outside the partition, and none was made.
3. The host-runtime ticket left untouched: not graded (Jira not read).
4. The `cd` slip: Info (F4).
5. Heavy slots: not graded.

## NOT RUN
- **Hosted infrastructure:** hosted CI, CodeQL, `scripts/package.sh` and the package job, the web and python jobs.
- **The real SDK 10.0.404:** not downloaded. The scratch SDK stands in for its framework's Pkcs file version only.
- **Other test runs:** main's whole suite was not re-run (the builder's TRX was used).
- **Reads:** open-PR overlap re-read (F6); Jira.
- No push, PR, merge, deploy, az, mail or board. No HTTP except the nuget.org advisory data the audit command reads.
