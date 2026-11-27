Scaffold only. One commit, `f08eabf4`, on `main` `7d652c5f` (behind 0, ahead 1). 61 files: 60 added, one changed
(`Datasec.Suite.slnx`). No product logic, no package, no `Directory.*` line, no landed project or lock file, no Server
file, no workflow, no file under `build/`, `contracts/` or `packaging/`.

## Why

The next modules of the working copy (the OXPd 1.x agent host, Microsoft sign-in, the panel, onboarding, SharePoint,
Teams, Mailflow and the admin API) each need a project and a test project. Adding all of them now, in one change,
means the lanes that fill them never share the solution file.

## What changed

- **Eight source projects** under `src/`: `Datasec.Suite.Adapters.Oxpd1.Agents`, `Identity.Entra`, `Panel`,
  `Onboarding`, `SharePoint`, `Teams`, `Mailflow`, `AdminApi`. Each is `src/Datasec.Suite.Core`'s three files with its
  names changed: the project file (one `InternalsVisibleTo` line per test project that reads it; five for `Panel`),
  an empty `internal static class AssemblyMarker`, and a lock file equal to Core's (no dependency).
- **Twelve test projects** under `tests/`: one per source project, plus `Panel.OneDrive.Tests`,
  `Panel.SharePoint.Tests`, `Panel.Teams.Tests` and `Panel.Mailflow.Tests`, whose subject is `Panel`. Each is
  `tests/Datasec.Suite.Core.Tests`' three files with its names changed: the project file (its subject's
  `ProjectReference`, `xunit.v3`), `SkeletonTests.cs` with one cell that pins the subject's assembly name, and a lock
  file equal to Core.Tests' but for its one project entry. One cell each, because a test executable that discovers no
  test exits with code 8 and would turn `dotnet test` red.
- **`Datasec.Suite.slnx`**: twenty lines added, each folder kept in the order it already had (sorted by project name);
  56 project lines, each a project file of the tree, none twice.

## What proves it

- Each of the 61 files equals its frozen bytes; every differing line against its model is a name, except the
  `AssemblyMarker` summary comment, which names the assembly in words.
- A locked restore accepts all twenty new lock files, locally and on both hosted legs; an unlocked restore rewrites
  none of the 56.
- Build `0 Warning(s)`, `0 Error(s)`; each new test executable `Total: 1, Errors: 0, Failed: 0`; the whole solution
  `total: 2445`, `failed: 0` (12 more than `main`); the branch's push run: linux `succeeded: 2441`, windows
  `succeeded: 2424`, rules 739 files, `Ran 117 tests`, release guard 14 and 15 files (unchanged), secret scan clean.
- An assembly name planted into each source project's file turns exactly that project's cells red: twelve of twelve
  cells, each undone and proved.

## Still open

- The four per-app panel test projects hold only the panel's skeleton cell until their app's pages land.
- The `AssemblyMarker` comment says the assembly "holds no logic yet"; the lane that fills a project changes it.
- A later change that adds a package to one of these projects must commit the project's lock file and its test
  project's lock file (a locked restore refuses both until then). A later change that removes one should re-run an
  unlocked restore: a stale entry in the test project's lock file is not refused by a locked restore.
- Any later module outside these twenty (for example a site connector) adds its own solution lines.
- Local CodeQL cannot run on this machine; the code scanning of this pull request is the CodeQL read.

## Who decides

The coordinator chose, as coordinator, this change and every choice inside it (the twenty projects rather than eight;
every byte frozen, the lock files included, judged by the locked restore; the skeleton form with no README; no
`IAppModule` and no package here; per-app panel test projects; the admin API as its own project). No choice in this
change is the product owner's.

Nothing is deployed; nothing was sent to or run against any printer or device.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
