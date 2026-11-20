STARTABLE: YES - the kit is whole and `stamp_check.py` exits 0 (123 claims, 123 sidecar lines). The 28 pointers were checked by program with 0 misses, and the placement program was prototyped on main's two shared files. The drafter ran no build and no test, so every `dotnet`, EF Core, provider and SQLite result is UNMEASURED. Three points need Tuesday at the stamp: the heavy-lock path shared with lane A (S4), Q5 (whether the scaffold route is allowed under "never downloads a tool"), and the base sha (S2), because wave 1 or lane A may land first.

# B1826 drafter report | lane B, seat X15, WP1.1 remainder (C1 device registry, C17 state database)

Drafted 2026-11-21, 09:20 to 09:38 AEDT (clocks by `date`: 09:20:35, 09:26:12, 09:28:25, 09:30:22, 09:37:23, 09:38:07). Drafter: Opus, read-only. Lane A (B1825) not drafted, not read.

## Files
- Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-21_B1826_SEAT-X15_oxpd2-wp11-registry-and-state-database.md` (92,388 bytes, 363 lines, 8 unfilled slot lines S1 to S7 + the last line)
- Sidecar: the same path + `.measured` (123 claim lines)
- Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s303/d1826/` (main's files by GET, `place_b1826.py`, `ptr.py`/`ptr.txt`, `sidecar.py`, `jira_get.py`, gitleaks probe folders `gl/`)

## BLUF
1. Two libraries (`Datasec.Suite.Devices` has no EF Core; `Datasec.Suite.Data` holds the EF Core model, two provider contexts and two migration sets) and two test projects. The kit has 26 controls (C01 to C26), each with a named mutant, plus the required section THE SHAPES NOT TESTED: 12 properties, each with at least 3 shapes and a cell or named limit (case collision, `tr-TR` casing, `NoSerial`, an address that is a name or `1234`, a migration applied twice, clocks in 1970 and 2099, a throwing reader, `ExecuteDelete` bypassing append-only, and others).
2. No server, container or network. Behaviour runs on SQLite `:memory:`. The PostgreSQL and SQL Server halves are proven three ways: no pending model change per migration set, offline idempotent scripts compared byte for byte (LF-normalised) against committed snapshots, and the same table set in both. A real-database run is UNMEASURED and named for a CI change (NOT DECIDED 1).
3. Shared files: 4 lines in `Datasec.Suite.slnx` and 3 in `Directory.Packages.props`, placed ONLY by an embedded program (`place_b1826.py`, sha256 `93b67ab1...`) run on main as it stands at the seat's start. It was prototyped on main `c56f3f3b` (slnx 11 -> 15 lines, sha256 `56b6c973...`; props 11 -> 14) and on a simulated main that holds Cards, Graph and Secrets-after-Server (15 -> 19). A rerun on its own output refuses (the control). Nothing goes in `ci.yml`.
4. Packages: none is in the project cache (MEASURED: 64 entries, 0 match `entity|npgsql|sqlclient|sqlite`; control `xunit.v3` = 1). They are fetched through `NuGet.config`'s nuget.org source. Versions come from a floating restore of a SCRATCH project outside the clone. The machine's global cache holds EF Core 10.0.12 (existence evidence only) and no Npgsql.

## What I measured and how
- Origin by `gh api -X GET` under the project GH_CONFIG_DIR (`gh auth status` rc 0): main `c56f3f3b015fae8d...`; 6 heads; 1 open PR (#3, b1786); 3 PRs in all; main tree 62 entries; slnx, props, Build.props, global.json, NuGet.config, .gitignore, ci.yml (199 lines; `FLOOR=53` at line 192; jobs at 24/54/82/179), repo_rules.py (R5 extensions at 60-61), Core and Core.Tests csproj, SkeletonTests.cs.
- b1789 head `bf1a4a24`: `SecretNames.cs:7-8`, the name rule re-expressed for credential references.
- Design pointers: 28 fragments checked by `ptr.py` (each on its line, 0 misses, control 0); the shas of 02/03/05.
- Jira OXPD2-12 by GET (an in-process reader, nothing printed): Backlog, 0 comments; the description lists "the device clock read at onboarding" as waiting for hardware.
- Toolchain: dotnet 10.0.404; shared frameworks 10.0.15; gitleaks 8.30.1; python 3.14.10; git 2.54.0; no psql/sqlcmd/postgres.
- gitleaks probe: 8 quiet shapes Q1 to Q8 (connection strings to `.invalid`, `:memory:`, SYNTH serials, TEST-NET address, a credential-reference name), each rc 0. The random 40-hex `apiKey` control scanned rc 1.
- `.tools/b1826` absent; no lock folder in `.tools/`; one OXPd pane live (`Datasec/OXPd2-X13`); load1 1.96; 1004 GiB free.
- Ordinal vs case-insensitive order (python `sorted`): `Microsoft.EntityFrameworkCore.SqlServer` sorts BEFORE `.Sqlite` ordinally, and the order reverses case-insensitively. The kit uses ordinal (B1820's landing rule).
- Commit subject: 119 bytes. Ban-name scan of the kit (underscore-aware): 0 hits, control fired; 0 decision-card ids.

## Decisions (D1 to D24), with Questions and their defaults (Q1 to Q23, all in the kit)
Q1 two libraries, Data references Devices · Q2 the three packages (`Npgsql.EntityFrameworkCore.PostgreSQL`, `Microsoft.EntityFrameworkCore.SqlServer`, `Microsoft.EntityFrameworkCore.Sqlite` for tests only) at the probe's highest 10.0.x · Q3 SQLite in-process, not InMemory (InMemory enforces no key or FK) · Q4 one assembly, two migration folders (`A5:44` precedent had two assemblies) · **Q5 migrations scaffolded by a scratch console with `Microsoft.EntityFrameworkCore.Design`, outside the repo; never hand-written; alternative `ef.dll` from the Tools package (Tuesday rules whether either is "a tool", `CLAUDE.md:83`)** · Q6 idempotent scripts as snapshots, LF-normalised · Q7 serial 1-64 of `A-Za-z0-9-`, key `ToUpperInvariant`, `NoSerial` refused (`A5:114`) · Q8 address and DNS name as two optional fields with canonical-form rules, zone ids refused · Q9 closed state lists, no transitions (WP1.11 owns them) · Q10 three credential-reference kinds, none for an OXPd 2 admin password (OQ-2 `03:374`) · Q11 JSON object up to 256 KiB, all snapshots kept · Q12 six audit actions, no free text, append-only in the library with its bypass limits ASSERTED by cells · Q13 integer version token · Q14 UTC DateTime columns via a converter · Q15 clock tolerance 300 s inclusive (alternative 3,600 s, the only documented figure, `A6:382`) · Q16 delete with cascade, audit rows kept · Q17 EF default names · Q18 the seat prepends the history entry · **Q19 heavy lock `<project>/.tools/wave1-heavy.lock.d` (lane A's kit must name the same path)** · Q20 rebase before push only, shared-file conflicts resolved by the placement program alone · Q21 READY at Step 0 + 300 min, push by + 240 · Q22 pane `Datasec/OXPd2-X15` · Q23 G1.
Lane-plan defaults named: OQ-2, N-6, N-8, N-9, OP-1 (pointers 14 to 17, 28).

## Where the documents or earlier kits no longer match
- The red-control rule is now at `03:126` (kit B1789 cited `03:125`, before the revision).
- `03:153` asks for a "server NTP check", but an NTP query is network. The kit builds the comparison behind `IReferenceClock` and puts the NTP client OUT. The device clock read waits for hardware (Jira).
- Panel classes: `02:148` gives three (8-inch and larger, 4.3-inch touch, below 4.3 inch). A panel between 4.3 and 8 inches has no class; this is listed in NOT DECIDED 4.
- Wave 1's stamp S5 said "alphabetically by Path value". For slnx paths ordinal and alphabetical agree (checked), but for the props lines they do not (SqlServer vs Sqlite).

## Corrections to this commission
- None that block. One gap: the commission (and the lane plan) gives no heavy-lock path for wave 2, so the kit makes it Q19/S4 with a default.
- Point 6's "a new package line is a G1 surface" is honoured, and the kit adds a finding to it: the SQL Server driver may bring `Azure.Identity` / `Microsoft.Identity.Client` in transitively (UNMEASURED). FOR TUESDAY must list every package of the lock files, and NOT DECIDED 3 asks whether those packages may stay.

## Reading load (summed by program)
The kit is 92,388 bytes. Its READ WHOLE list is 27,991 bytes: project CLAUDE.md 10,052; ci.yml 8,911; test_pipeline_controls.py 5,856; Directory.Build.props 834; Directory.Packages.props 448; slnx 501; global.json 135; .gitignore 287; NuGet.config 217; Core csproj 136; Core.Tests csproj 342; SkeletonTests.cs 272. **Total 120,379 bytes**, which is over the ~100 kB guide. The kit alone is under it; the excess is the files the seat must read to act.

## UNMEASURED (each marked in the kit; collected in its section NEVER RUN)
- Versions on nuget.org (no HTTP by the drafter).
- EF's design-time API names, and whether `EF1001` fires.
- Whether `GenerateScript` and `HasPendingModelChanges` run offline for Npgsql and SQL Server.
- The CR LF behaviour on the Windows runner.
- Npgsql refusing a non-zero offset, and SQLite failing to order `DateTimeOffset`.
- NuGet audit of transitive packages.
- The transitive identity packages from SqlClient.
- The base test total.
- Every hosted line for this lane.
- The `System.Text.Json` default depth.

## What I did not read
Lane A's files; the B1786 form kit (lane A's form); BACKLOG.md; history.md; `02` and `05` beyond the cited rows; the analysis reports beyond the grep hits cited; Workpath source and the NAS library (not needed); HPSM-POC (nothing opened). The wave-1 code itself was not read beyond `SecretNames.cs` and the csproj shapes.

## Outside-the-fences disclosure
- I listed directory names in the machine's global NuGet cache `~/.nuget/packages`. This was read-only and nothing was opened inside it.
- I made one Jira GET with my own in-process reader of the project `.env` (no value printed).
- gitleaks ran only on scratch files.
- I moved my own first sidecar draft to scratch (`measured.prev`); I deleted nothing.
- No git write, no build, no test, no message.
