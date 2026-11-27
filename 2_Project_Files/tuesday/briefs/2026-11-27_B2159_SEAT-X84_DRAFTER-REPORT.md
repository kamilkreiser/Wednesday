STARTABLE: YES

# B2159 lane L0 (seat X84) drafter report: the scaffold (wide: L0 + B2156's app projects)

Drafted 2026-11-27 by an in-session read-only drafter (Opus) for Tuesday s334, lane L0 of commission B2159. First `date`: `Fri 27 Nov 2026 17:39:04 AEDT`; sidecar written 17:55:45. Kit: `tuesday/briefs/2026-11-27_B2159_SEAT-X84_oxpd2-l0-scaffold.md` (195 lines). Sidecar `.measured`: `stamp_check.py` exit 0, "122 claims, 122 measured, 0 not measured". Scratch: `fleet/state/s334/d2159-L0/`. The seat's tools are in its `seat-tools/`. The report is named with the seat because four lanes share B2159 (lane L1's report uses the same form).

**STARTABLE means:** the kit is complete and stamp-checked. Its LAUNCH still waits on things outside it: the stamp, and B2153's seat X82 ending on the wave lock. At drafting the lock was held by the parallel-build experiment B2157.

## BLUF
- **20 projects, every byte frozen.** There are 8 source projects: `Adapters.Oxpd1.Agents`, `Identity.Entra`, `Panel`, `Onboarding`, `SharePoint`, `Teams`, `Mailflow`, `AdminApi`. There are 12 test projects: one per source project, plus `Panel.OneDrive/SharePoint/Teams/Mailflow.Tests`. Each has 3 files. That is 60 new files plus the slnx (36 to 56 project lines), 61 files in `scaffold_l0.json`, written by `apply_l0.py`.
- **The form is the project's own PR 1 skeleton** (`Core/AssemblyMarker.cs` + `Core.Tests/SkeletonTests.cs`, commit `7bf37526`), copied with only the names changed. A generator (`gen/make_scaffold.py`) derives every file from a landed file and asserts each substitution.
- **Why every test project carries one cell:** the test platform's default `ZeroTestsPolicy` makes a run that discovers no test exit with code 8. I read this in the project's own package-cache doc. An empty test project would therefore turn `dotnet test` red.
- **Lock files frozen and predicted to be NuGet's bytes.** The same name substitution reproduces 3 landed test lock files byte for byte. 3 landed src lock files equal Core's (`cmp`). The seat's locked restore is the judge, and its unlocked restore must leave all 56 lock files byte-equal.
- **PREDICTED:** each new test executable `Total: 1`. The whole solution `total: 2443` (2431 + 12), succeeded 2439 on Linux and 2422 on Windows. `RULES: clean (739 files)` was MEASURED on my applied tree. Guards stay 14/15.
- **3 frozen mutants:** an `AssemblyName` is planted in the Agents, Panel and Mailflow project files. Each makes its skeleton cell red.

## FACTS RE-MEASURED (instrument -> printed)
- Origin, `gh api -X GET` at 17:39:47: main `760e1a64...` (tree `8e3985c1`, parent `0ca8c655`). Open PRs 0. `matching-refs/heads/b2159` 0 rows.
- BASE tarball, 679 files. Committed in scratch `sim`, its `HEAD^{tree}` = `8e3985c1` (equal to origin's).
- `hosted3.py` on BASE at `--total 2431 --rules 679`: PASS. The control `--total 2432` gives FAIL 4, naming succeeded 2428 (Linux) and 2411 (Windows).
- `apply_l0.py check` on BASE: `60 ABSENT, 1 BASE`. `scaffold`: 61 of 61 equal, and a second run is refused. `check` after: `61 FROZEN`.
- `checks_l0.py` on BASE's index: 2 of 9 PASS, 9 of 9 controls FIRED. On the applied, staged tree: 9 of 9 PASS, 9 of 9 FIRED.
- `mutants_l0.py --list`: `LIST: 3 mutants, 3 suites, 3 cells` rc 0. The bad row gives rc 1. apply/undo is `equal True` 3 times.
- `words.py --control` fired 13/13. Over added.txt (428 lines) plus the commit message: `WORDS: clean (2 files)`. `B2[0-9]{3}` count 0/0.
- **Found while drafting:** the lock files' `win-x64`/`linux-x64` match words.py's seat-id shape (40 hits, all `x64`). `checks_l0.py` therefore writes lock lines to `added-locks.txt`, which checks 3 and 6 judge, and keeps them out of words.py.
- `repo_rules.py` over the applied tree: `RULES: clean (739 files)`. gitleaks 8.30.1: control rc 1, then the 11 tools plus the added lines rc 0.
- Seat X84: 0 file names in the briefs folder or the OXPd Briefs folder. One text hit, the B2159 commission itself (control: X82 in 2 names). `.tools/b2159*` is absent.
- Load at 17:46 was `4.77 8.55 8.89`. 840 GiB free. The lock owner was `B2157 | pid 92618`.

## D-DECISIONS (Tuesday's defaults as coordinator)
D1 the wide scaffold. D2 every byte frozen, lock files included. D3 the PR 1 skeleton form. D4 no references and no packages in the new src projects. D5 three mutants (the other 9 cells are a named limit). D6 no README, no `IAppModule`, no `Directory.Packages.props` line.

## Q-QUESTIONS FOR TUESDAY (each with its default)
- **Q1 (STOP-CLASS) width:** default **wide**, 20 projects. Alternative: narrow, B2154 L0 only (8 projects, 24 files; regenerate and re-count).
- **Q2 (STOP-CLASS) who writes what:** default **every byte frozen**, including the lock files. Alternative: the seat writes the lock files by an unlocked restore.
- **Q3 `IAppModule`:** default **not here**. Server is L3's, and H12 (`HostCellTests.cs:255`) pins Server's references. L3 defines it.
- **Q4 AdminApi project now:** default yes.
- **Q5 per-app panel test projects** (OneDrive, SharePoint, Teams, Mailflow; UP has no panel): default yes.
- **Q6 skeleton form, no README:** default yes.
- **Q7 gate:** default one G2 gate (`model-routing.md:109`). The seat runs on Opus, pane `Datasec/OXPd2-X84`, READY by Step 0 + 120 minutes, push by Step 0 + 100.
- **Q8 order:** default: the next build seat after X82 ends. Landing order with B2153 and B2155 is free (no shared path).

## UNMEASURED
- No dotnet job ran, so every build, restore, test total and mutant colour is PREDICTED.
- In particular: that NuGet's locked restore accepts the frozen lock files (strongly supported by the 3 byte-equal reproductions, but not run).
- That `--no-restore` builds after an `AssemblyName` mutant. A BUILD-FAILED row is a STOP to Tuesday.
- B2155 changes `repo_rules.py` and `ci.yml`. Whether its new rules accept the 60 new files is UNMEASURED: the kit tells the seat to re-print the predicates if B2155 lands first.

## CHAIN INPUTS
0 stamp (S2, S3 seat-before, S4, S8). 1 `<src>`, `<repo>` values, origin, BASE run. 2 BASE files + json (from 1). 3 apply + restores + build on the Step-1 clone. 4 pinned tree (3) + mutants (1). 5 green tree (4). 6 staged tree (5) + checks/words/message/json (1). 7 commit, origin/main, run_step/hosted3 (1).

## PARTITION
**This kit owns:**
- `Datasec.Suite.slnx` (M)
- the 8 `src/Datasec.Suite.<New>/` folders and the 12 `tests/Datasec.Suite.<New>.Tests/` folders (A)

**The other side, by owner:**
- **L1 (X87):** owns `src/Datasec.Suite.Adapters.Oxpd1.Agents/**` and its tests. These overlap with this kit's paths, but **in time only**: L0 creates them, and L1's base is "main after L0 lands", with a REFUSE if they are absent. They are never written concurrently, so I did not treat this as a drafting STOP. Tuesday may judge otherwise.
- **L5 (X86):** owns the OneDrive paths. None of the 61.
- **L9 (X85):** owns no repository file.
- **B2153 (X82):** owns `HostRig.cs`, `HostCellTests.cs` and 3 READMEs. None of the 61.
- **B2155 (X83):** owns 7 paths (`ci.yml`, root `README.md`, 2 `build/*.py`, 3 `build/tests/*`). None of the 61.
- **B2146 (records):** owns files outside the repository.

## OUTSIDE THE FENCES (disclosure)
- **Writes:** only the kit, its `.measured` and this report, plus scratch under `fleet/state/s334/d2159-L0/`.
  - The scratch includes two scratch git repositories, `sim` and `sim0`. Neither has a remote. Each has one local commit of BASE's tree under the identity `draft@invalid`, scratch only.
  - Superseded check folders, the init sidecar and the planted gitleaks control were moved to `d2159-L0/_quarantine/`.
  - Nothing was written to the OXPd project, Jira, GitHub or cards. No push, no PR, no dotnet job, no lock taken.
- **Project reads,** by path only:
  - `CLAUDE.md` (sha256 and 6 lines), `BACKLOG.md` and `CLARIFICATIONS.md` (sha256 only)
  - `ls` of `.tools/`, the lock's `owner.txt`, `ls` of `Briefs/`
  - `.tools/dotnet/dotnet --version`, and one MTP XML doc in `.tools/nuget-packages`
  - I never touched `Source_Documents/` or `4_Credentials/` beyond `GH_CONFIG_DIR`.
- **GitHub:** `gh api -X GET` only: commits, pulls, matching-refs, one tarball, `commits?path=`, and check runs/job logs via `hosted3.py`.
- **Tuesday-tree reads:** DRAFTER_RULES, the B2159 commission, plans B2154 and B2156 (whole), kits B2153 (whole) and B2138 (lines 1-131 whole, the rest by section heading only), the B2153 report and sidecar, B2155's owned-path table, and the head of the X87 report. I did NOT read the ledger, the scoreboard, `briefs_staged`, any card store, or any WEDNESDAY/FRIDAY tree.
- **Incidents:**
  - One `cd` was refused by the hook (nothing ran).
  - One recursive grep over the briefs folder ran past its cap and was stopped by me (read-only).
