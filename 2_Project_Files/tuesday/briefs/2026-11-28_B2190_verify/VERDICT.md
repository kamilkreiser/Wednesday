GATE B2190: GO WITH FINDINGS @ f08eabf on main 7d652c5

Gate G2, ROUND 1 OF 2 of lane L0 (the scaffold: twenty empty projects and their slnx lines), one Opus reader
(claude-opus-5-5), in-session, read-only, for Tuesday s336. Kit B2159 (seat X84; stamp S4: Q1 "a" the wide scaffold
and Q2 "a" every byte frozen, both in words; Q3-Q8 the defaults; S8 the canonical runner 31adedc8; every choice the
coordinator's, none the product owner's). Head `f08eabf4765dbb37c01fcad6532d70442b5e7c54` on `b2159/l0-scaffold`, ONE
commit, one parent = main `7d652c5f0f8d9854aaf49b43df79e77855eccb46` (PR 59's squash), tree
`fc101f812f5eab212074fc18e39c9d0a5c6ee1cb`, 739 files. Main and the branch did NOT move during the gate (gh api -X GET
at 00:25:06 and 00:40:11 AEDT; open pull requests 0 both times; open code-scanning alerts 0). Measured 2026-11-28
00:24 to 00:41 AEDT in my scratch `fleet/state/s336/g2190/` (`clone`: clone.py draft, push URL `invalid://no-push`,
no identity, detached at the head; every mutant and probe ran there and was undone and proved). Every heavy job
through my copy of the kit's `heavy.py` (11 of 11 tool hashes equal to THE TOOLS; heavy.py `31adedc8...` = S8) under
the OXPd wave lock, one at a time, lock waits 0 each (load waits up to ~5 min at load1 35); my 58 released lock
folders are in `g2190/_quarantine/locks/`; no other holder's lock touched (at the end the lock is held by
`B2188 seat X97`, read, untouched); no process of mine left. Nothing to any printer or device; no Jira; no Azure; no
write to the project checkout, the seat's lane or GitHub.

## Grades (round 1 of 2): Blocker 0, Major 0, Minor 0, Info 8. Nothing blocks landing.

**F1 INFO (Tuesday's point a, DEVIATIONS 1): harmless difference, a later lane's to change, no round 2.** The eight
`AssemblyMarker.cs` summary lines read `/// Marks the <the assembly in words> assembly. It holds no logic yet.`
against Core's `/// Marks the core assembly. The core holds no logic yet.` It is a `///` comment on an empty internal
class: no project sets `GenerateDocumentationFile` or `DocumentationFile` (git grep over every `.csproj`, `.props`,
`.targets` at the head: 0, control `TreatWarningsAsErrors` in `Directory.Build.props`: 1), so it reaches no build
output; Core is the only landed `AssemblyMarker.cs` (1 file at BASE), so there is no second landed form it departs
from; the kit's own BLUF quotes "It holds no logic yet", so the frozen text is the kit's intent, not a generator slip.
The words become stale when a lane adds logic; that lane owns the folder and changes the line.

**F2 INFO (Tuesday's point b, R4): the nine cells without a mutant row are the same form AND each was seen red by
the gate.** By program (`evidence-gate-read.txt`): every one of the twelve `SkeletonTests.cs` normalises to ONE text
(`using <S>; using Xunit; namespace <T>; public class SkeletonTests { [Fact] public void <M>_assembly_carries_its_name()
{ Assert.Equal("<S>", typeof(AssemblyMarker).Assembly.GetName().Name); } }`), 12 of 12 "same form", one `[Fact]`
each, each asserting its own subject. Beyond form, the gate wrote nine rows of its own in the kit's tool form
(`evidence-gate-mutant-rows.json`: the kit's planted `AssemblyName` on the subject of each of the nine cells) and ran
them with the kit's unchanged `mutants_l0.py run`: `MUTANTS: 9 of 9 MATCH, 9 of 9 undone equal`
(Identity.Entra, Onboarding, SharePoint, Teams, AdminApi, and the four per-app panel cells each red under a planted
`Panel` name). With the kit's three re-run by the gate (`MUTANTS: 3 of 3 MATCH, 3 of 3 undone equal`), all twelve
cells are proved able to fail. The named limit R4 is closed by measurement at the gate (not in the commit).

**F3 INFO: the four per-app panel cells hold nothing per app.** `Panel.OneDrive/SharePoint/Teams/Mailflow.Tests` each
pin `Datasec.Suite.Panel`'s name, the same assertion as `Panel.Tests` (five identical cells over one assembly; the kit
listed only `Panel.Tests` in mPanelRenamed's suite, the gate's rows show all four others red too). Placeholders until
each app's panel lane adds its cells (kit Q5, the coordinator's default).

**F4 INFO (Tuesday's point c): the five `InternalsVisibleTo` lines open nothing wider in kind than Core.** Every
`InternalsVisibleTo` of the head tree (26 projects) names a `.Tests` project of the tree (targets not a test project:
0); the new eight name only their own test projects (`Panel` five, the rest one each); landed precedent already has
more than one (`Adapters.Oxpd2` -> `Contracts.Tests` and `Adapters.Oxpd2.Tests`; `Jobs.Transport` -> `Jobs.Tests`). No
assembly in the tree is signed (`SignAssembly` 0), so every grant, landed or new, is by simple name, as Core's is.
`Panel` holds one empty `internal static class`: there is nothing internal to expose. The width is five readers of
the panel, which is what kit Q5 chose; each later panel lane adds code all five can see.

**F5 INFO (Tuesday's point d): no new project can reach the Server's publish or the release guard; counts 14 / 15
stay because the publish closure is unchanged.** ci.yml publishes ONE project, `dotnet publish src/Datasec.Suite.Server
-r linux-x64|win-x64` (ci.yml:48, :78); its closure is `Core`, `Adapters.Oxpd2`, `Secrets` (Server csproj :3-:5); a
landed project referencing a new one: 0, and every new project is referenced only by its own test project(s) (by
program). The container step copies only `out/linux/` (packaging/linux/Dockerfile) and has no push. The guard reads
only the publish folder: 14 and 15 files at BASE and at the head (hosted logs; seat's local chain). A later lane that
adds a `ProjectReference` from Server (L3a/L3b, r2:73) will move those counts; that is its own gate.

**F6 INFO (adversarial: a later lane adds a package; MEASURED on my scratch clone).** Added `<PackageReference
Include="Serilog" />` (central version 4.4.0, already in the cache) to `Mailflow`: the locked restore (CI=true)
refused rc 1 with two `NU1004` lines, on `Mailflow.csproj` ("Lock file's package references: None, project's package
references: Serilog") AND on `Mailflow.Tests.csproj` ("The project references datasec.suite.mailflow whose
dependencies has changed"); the unlocked restore rc 0 rewrote BOTH lock files (`Mailflow.Tests` gained `Serilog` as
`CentralTransitive`). So the frozen lock files BLOCK an unrecorded package (they do not mislead an add). The reverse
MEASURED by accident of the put-back: with `Mailflow`'s project and lock file restored but `Mailflow.Tests`' lock
file still holding the stale `Serilog` entry, the locked restore (CI=true) passed rc 0, 56 `Restored`. So a stale
extra entry in a dependent test project's lock file is NOT refused by NuGet's locked mode: the locked restore is not
an equality judge; the unlocked-restore byte-equality (run by the seat and by the gate: 56 of 56 equal) is. Not this
lane's defect (NuGet's behaviour; every landed lock file has the same exposure); for records. All bytes put back from
kept copies and the head's blob; `apply_l0.py check` `CHECK: 0 ABSENT, 0 BASE, 61 FROZEN, 0 OTHER`, porcelain 0 rows.
Also: a new package not already in `Directory.Packages.props` needs a line there (central management on), the shared
file plan r2:83 names.

**F7 INFO (adversarial: name collisions).** Plan r2's L0b names `SiteConnector` and `RelayBridge` (r2:80): no
collision with the twenty or with any landed project (56 project names of the tree, by program). DERIVED from C#
name lookup (not built): inside `namespace Datasec.Suite.Panel.<App>.Tests` the enclosing namespace
`Datasec.Suite.Panel.<App>` is found before `Datasec.Suite.<App>` for a bare `<App>.` qualifier, so a panel test that
later references the app project writes the full name; the failure is a compile error, never a silent binding.
`Datasec.Suite.Teams` / `Datasec.Suite.SharePoint` beside Microsoft Graph's own `Teams` / `SharePoint` names: the
same class of hazard, a compile-time ambiguity for the filling lanes (DERIVED).

**F8 INFO (process, seat DEVIATION 2):** the seat edited its own scratch script and STATUS draft in place with
`sed -i` (outside the repository, self-reported). No repository effect.

## THE KIT'S GATE LIST (its FOR TUESDAY, "THE GATE"), whole
1. **`BASE..head` read, 61 files, each equal to `scaffold_l0.json`, by program** (`evidence-gate-read.txt`):
   `git diff --name-status -M -C 7d652c5f f08eabf4`: 61 rows, 60 `A`, 1 `M`, 0 other; the path set equals the json's
   61 keys; `FROZEN: 61 of 61 head blobs equal to the json sha256 and content`; the slnx BASE sha256 `d277575c...` and
   head `ba27adb5...` equal the json's `modify` pair; control: a planted byte is caught. The stored commit message
   equals the frozen `commit-message.txt` byte for byte (309 bytes). compare (GET 00:25:06): ahead 1, behind 0, 61.
2. **The reading, re-run by the gate's own program** (not the seat's `reading.py`): each new file against Core's or
   Core.Tests' file at BASE, with ONLY the names substituted (project, namespace, assembly string, method, subject
   `using`, `ProjectReference` path, the `InternalsVisibleTo` set): 60 files, 40 lines left. 24 of them are the lock
   files' one project entry in lower case (`"datasec.suite.core"` -> the subject's, 12 removed and 12 added: a name);
   the other 16 are the eight summary-line pairs of F1. Source lock files equal Core's; every other line equal. **No
   line differs from its model in more than names, but the summary comment (F1).**
3. **The locked restore on both hosted legs** (push run 46005945023, logs read by `hosted3.py` and by grep, ANSI
   stripped): linux and windows each `Run dotnet restore --locked-mode` (no `-p:NuGetAudit=false`: NuGet audit ON),
   56 `Restored` lines, 20 of them the new projects, `NU1004` 0, step success; `0 Warning(s)`, `0 Error(s)`.
   `hosted3.py f08eabf4... --total 2445 --rules 739 ...` re-run by the gate: `HOSTED f08eabf4...: PASS` (linux
   succeeded 2441 skipped 4, windows succeeded 2424 skipped 21, GUARD 14 and 15, RULES 739, UNIT-TEST FLOOR 117/117,
   secret-scan controls and `no leaks found`); control `--total 2446` printed `FAIL 4`, rc 1.
   Locally (gate clone): locked restore rc 0; unlocked restore rc 0 and `LOCKS: 56 of 56 equal, 0 differ`; porcelain 0.
4. **Each new executable's `Total: 1`**: gate build `0 Warning(s)`, `0 Error(s)`; each of the twelve run whole
   through the runner `Total: 1, Errors: 0, Failed: 0, Skipped: 0, Not Run: 0` (12 of 12), and again after every
   mutant was undone and the tree rebuilt (12 of 12). Hosted: each of the twelve `.Tests.dll ... passed` on both legs
   (24 lines per leg, the leg prints each twice; 60 per leg over all 30 test projects).
5. **The three mutants' reds, re-run by the gate** (kit's `mutants_l0.py run` over the kit's `mutants_l0.json`, sha256
   `6e331d80...` = THE TOOLS): mAgentsRenamed, mPanelRenamed, mMailflowRenamed each `Total 1 Failed 1`, red exactly
   its listed cell, `MATCH`, `undone equal True`; `MUTANTS: 3 of 3 MATCH, 3 of 3 undone equal`. Plus the gate's nine
   (F2): `9 of 9 MATCH, 9 of 9 undone equal`. Porcelain equal before and after.
6. **The slnx order and count**: 56 project lines (BASE 36), 0 duplicates, BASE's 36 kept in their order, every slnx
   path a `.csproj` of the tree and every `.csproj` of the tree in the slnx (exact strings, so case-exact for the
   Linux leg); `/src/` 26 lines sorted ordinal by project name (as BASE: by path string it is not, at BASE nor head,
   because `Adapters.Oxpd1/` precedes `Adapters.Oxpd1.Agents/`), `/tests/` 30 sorted by both; each path under its
   folder.
7. **GREEN, whole solution, gate's own run**: `dotnet test -c Release --no-build` through the runner, rc 0 (58 s):
   `total: 2445`, `failed: 0`, `succeeded: 2441`, `skipped: 4`; `failed Datasec.` / `did not end within` lines 0.

## ADVERSARIAL: three shapes outside each property
- **P1 (builds warning-free):** (i) the hosted Windows leg, other RID and OS: covered (windows `0 Warning(s)`);
  (ii) a restore and build with NuGet audit ON: covered (hosted legs pass no audit switch); (iii) a Debug build:
  NAMED LIMIT (CI builds Release only; an empty class differs in nothing by configuration, DERIVED).
- **P2 (each executable one cell, passing):** (i) a renamed subject: covered, 12 of 12 cells red under a planted
  name (F2); (ii) the cells counted by the whole-solution run: covered (2445 = 2433 + 12, local and both legs);
  (iii) a cell that passes for a reason other than its subject (the five panel cells share one subject): covered as
  far as the assertion goes, named in F3.
- **P3 (lock files):** (i) locked restore on both hosted legs with audit on: covered (item 3); (ii) unlocked restore
  rewrites nothing: covered (56 of 56, seat and gate); (iii) a later package added / removed: MEASURED, F6 (add
  blocked on both lock files; a stale entry after a removal not refused).
- **P4 (no landed file but the slnx; landed cells green):** (i) any landed path in the diff: 0 (name-status vs json);
  (ii) a landed project now referencing a new one: 0 (by program); (iii) landed cells: `total: 2445`, `failed: 0`,
  linux/windows/local, Server.Tests ended (no `did not end within`).
- **P5 (the solution lists every new project once):** (i) a duplicate or a missing line: covered (0 / every csproj
  in the slnx); (ii) a path whose case differs from the tree: covered (exact string match; Linux leg built all 56);
  (iii) a later project outside the twenty (L0b): NAMED LIMIT, it adds its own lines (F7, FOR-RECORDS).

## SCANS
- gitleaks 8.30.1: control FIRST (a token built from two halves and random characters, never printed, outside the
  clone) rc 1 `leaks found: 1`, moved to `g2190/_quarantine/scan-control`; `gitleaks git` over
  `7d652c5f..f08eabf4` (1 commit scanned, `--ignore-gitleaks-allow`) rc 0 `no leaks found`; the 61 head blobs and
  the commit message under neutral names `1.txt` to `62.txt` rc 0; the message alone rc 0.
- words.py: `--control` `CONTROL FIRED: 13 of 13`; over `added.txt` (428 lines, the committed diff's added lines but
  the lock files') and the stored message: `WORDS: clean (2 files)`; `added-locks.txt` 1996 lines (sum 2424 = the
  commit's insertions) gives 40 hits, every one the `x64` the kit names (THE CHANGE), not given as a pass.
- Landing texts: `words.py` over squash-subject (with #60), squash-body, pr-title `WORDS: clean (3 files)`;
  `build/squash_scan.py` (head's `build/` and `.github/` unchanged from main's, diff empty) with #60:
  `SQUASH-SCAN: clean` (control rc 1, found 2).
- CodeQL: NOT RUN locally (kit D6); the pull request's own analysis is the check (landing.txt step 3). Main's
  baseline at 7d652c5f: csharp, python, actions results 0; open alerts 0.

## NOT RUN
CodeQL locally; a Debug build; a local restore with NuGet audit on (the hosted legs ran it); any merge with a main
other than 7d652c5f (none moved); the whole solution on Windows locally (hosted only). No pull request opened, no push.

## LANDING
`landing.txt`, `pr-title.txt` (213 characters), `pr-body.md`, `squash-subject.txt` (the commit subject + ` (#PRNUM)`),
`squash-body.txt`, `FOR-RECORDS.md` in this folder. Evidence copies: `evidence-*.txt`, `evidence-gate-mutant-rows.json`.
Run logs: `fleet/state/s336/g2190/logs/`.
