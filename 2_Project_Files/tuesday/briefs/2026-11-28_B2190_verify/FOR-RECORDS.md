# FOR RECORDS: lane L0, the scaffold, round 1 of 2 (kit B2159, seat X84), head f08eabf4 (gate B2190: GO WITH FINDINGS)

For the records lane only, AFTER a landing of this gated head (its squash on main); nothing here is written into a
project file by the gate. Who decided every choice of this lane: the coordinator (Tuesday), as coordinator, never the
product owner (kit B2159 THE AUTHORITY; stamp S4 states Q1 "a" and Q2 "a" in words). Nothing here ran against a
device.

## Plan lane L0: DONE in its wide form (on this squash)
Eight empty source projects (`src/Datasec.Suite.{Adapters.Oxpd1.Agents, Identity.Entra, Panel, Onboarding, SharePoint,
Teams, Mailflow, AdminApi}`: the OXPd 1.x agent host, Microsoft sign-in, the panel, onboarding, SharePoint, Teams,
Mailflow, the admin API) and twelve test projects (one per source project, and `Panel.OneDrive.Tests`,
`Panel.SharePoint.Tests`, `Panel.Teams.Tests`, `Panel.Mailflow.Tests`, whose subject is the panel), each in the
skeleton form of pull request 1 with one cell and a lock file, and their twenty lines in `Datasec.Suite.slnx` (56
project lines). Later lanes fill their own projects and do not edit the solution file. No package, no Server change,
no `IAppModule`, no README. (RELAYED from the kit's FOR RECORDS; CHECKED by the gate: 61 of 61 files equal to the
frozen bytes; whole solution `total: 2445`, `failed: 0` locally and on both hosted legs.)

## What it unblocks (plan r2, `tuesday/briefs/2026-11-27_B2174_OXPD-WORKING-COPY-PLAN-r2.md`, RELAYED)
- **L2** Entra sign-in in `src/Datasec.Suite.Identity.Entra/**` + tests ("needs L0", r2:70).
- **The app libraries**: SharePoint, Teams, Mailflow against fakes in their own projects ("needs L0; B2156:162",
  r2:70), and their panel pages later in `Panel` with the per-app panel test projects.
- **L1** the agent host in `src/Datasec.Suite.Adapters.Oxpd1.Agents/**` (r2:71), after **L1c** (contracts) and **L1x**
  (the additive client class in `Adapters.Oxpd1`), the re-cut of L1 in plan r2 C12 (r2:53). L1c needs no L0 path but
  runs beside it per r2:83; L1's own kit re-reads its base after this lands (kit B2159 FOR TUESDAY).
- **L7** onboarding in `src/Datasec.Suite.Onboarding/**` (r2:78, after L1 and L3b); **AZ-1X** and **L8** in the agent
  host project (r2:75, :80); the Universal Print admin pieces may use `src/Datasec.Suite.AdminApi/**` (kit Q4).
- **NOT covered by L0:** plan r2's **L0b** (`SiteConnector`, `RelayBridge`, r2:80) adds its own projects and slnx
  lines later; neither name collides with the twenty or with a landed project (gate, by program over the tree).

## Notes for later lanes (gate findings, all Info; see VERDICT.md)
- **Adding a package to one of these projects** (MEASURED by the gate on a scratch clone, `Serilog` into `Mailflow`):
  the CI locked restore refuses with `NU1004` on BOTH the project and the test project that references it; an
  unlocked restore rewrites both lock files (the test project's gains the package as `CentralTransitive`). The lane
  commits both lock files, and adds a `Directory.Packages.props` line for any package not already listed there
  (central package management; the file is shared, plan r2:83). **Removing** a package: a stale entry left in the
  test project's lock file was NOT refused by the locked restore (rc 0, MEASURED): re-run the unlocked restore and
  compare, as this lane's seat and gate did (56 of 56 byte-equal).
- The `AssemblyMarker` summary comment ("It holds no logic yet") is changed by the lane that fills each project.
- The per-app panel test projects hold only the panel's skeleton cell; each app's panel lane adds its own cells there.
- Name lookup (DERIVED from C# rules, not built): inside `Datasec.Suite.Panel.<App>.Tests` the enclosing namespace
  `Datasec.Suite.Panel.<App>` wins over `Datasec.Suite.<App>` for a bare `<App>.` qualifier; a lane referencing both
  writes the full name. A compile error, never a silent wrong binding.

## Seen, not this lane's
The seat's DEVIATION 2: an in-place `sed -i` on its own scratch script and STATUS draft (outside the repository;
self-reported). No repository effect.
