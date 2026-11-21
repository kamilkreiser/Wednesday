GATE B1870: GO WITH FINDINGS @ c5a6ff8 on main 8ae5e08

Gate G1, round 1 of 2, whole-lane reader and THE FETCH RECORD CHECK. OXPd 2, WP1.1 remainder, lane B: the device
registry (C1) and the state database (C17), kit B1856, seat X15, head `c5a6ff844a626f99334722e5af2bc5d58e0e7cbe`
(one parent `8ae5e08cadf6460f6f87fff091d3bafada2efe41` = main) on `b1856/wp11-registry-and-state-database`.
Reader: Opus 5.5, in session, 22:03 to 22:27 AEDT 2026-11-21. Every count below was printed by a program; evidence
in `evidence/`. Second reader B1871's verdict (read at 22:21, first line only): `GO WITH FINDINGS`.

BLUF (plain words): the branch can land. Every one of the 74 downloaded packages is byte-identical to what nuget.org
publishes; nothing was fetched after the one fetch; the code does what the kit says, the whole suite is green locally
(1335) and hosted (1335 both legs), the branch merges onto today's main with no change. The findings are Minor: two
edge inputs throw an untyped exception (nothing is stored either way), two free-text fields are not re-checked on
read, the clock result can print an offset of 300 next to `outside`, and three of my mutants survive the lane's own
tests (each caught by my probes). None blocks the merge; they go to the backlog.

## 1. THE FETCH RECORD CHECK (the Blocker class)

Record `/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2/1_Project_Definition/Briefs/2026-11-21_B1856_FETCH-RECORD.md`:
24174 bytes, sha256 `d59e7357244ed64d9b1e9d2d9d8268630a1e56a13f2420d08d7f093704695a30` (as the commission says).

- `evidence/nugethash.py` (GET only, host asserted `api.nuget.org`, no package downloaded): for each of the 74 rows,
  the record's (B) hash, the cache's `.nupkg.sha512`, my own SHA-512 of the cached `.nupkg`, and nuget.org's
  `packageHash` (registration5-gz-semver2 leaf, then its catalog entry; `packageHashAlgorithm` SHA512; id and version
  checked). **`NUGET-HASH: rows 74 | equal 74 | differ 0`**, rc 0, 22:03:44. Table (id, version, equal):
  `evidence/nuget-hash.tsv` (74 rows `yes`: the 59 lock-reachable and the 15 lower bounds). Positive control: one
  character of row 37's record hash flipped: `equal 73 | differ 1`, that row named.
- (A) content hashes, re-measured (`evidence/locks.py`): the four committed lock files hold 149 package entries
  (Data 49, Devices 0, Data.Tests 79, Devices.Tests 21); each `contentHash` equals the cache's `.nupkg.metadata`
  `contentHash` and each metadata source is nuget.org: **149 of 149**. Control: Npgsql's hash altered: `differ 2`.
- Set checks: the cache now = the after-fetch listing (169); after minus before = exactly the 74 record rows; the 64
  distinct packages of the four lock files are 40 record rows + 24 already in the cache before the fetch, **0
  neither** (no package outside the ruling in a lock file). 34 record rows are in no committed lock file (the
  scaffold's Design chain and the 15 lower bounds).
- No fetch after the one fetch: `CACHE-LIST: 169 versions | sha256 f4a91f9d3c4dc782` (= Tuesday's ANSWER-1 baseline)
  before and after my locked restore, and before and after both scaffold runs.
- The record tells the truth: its flag line lists Azure.Core, Azure.Identity, Microsoft.Data.SqlClient,
  Microsoft.Data.SqlClient.SNI.runtime, Microsoft.Identity.Client, .Broker, .Extensions.Msal, .NativeInterop (its
  prefix `Microsoft.Identity.` with the dot leaves the IdentityModel ids to the table, where all are listed; the
  lower-case lower bound `microsoft.identity.client 4.78.0` is in the table and the STOP rows). Its last line
  `STOP 15` is the 15 lower bounds, covered by Tuesday's ANSWER-1; not edited.

## 2. THE DEPENDENCY GRAPH (not graded; truth of the record and lock files only)

From the four committed lock files (all `Transitive`; what each is for DERIVED from the package's own nuspec
description in the cache; "loaded" MEASURED in the Data test process on macOS, `evidence/loaded-assemblies.txt`):

| Package | Version | Lock file(s) | For (nuspec) | Loaded by a library path |
|---|---|---|---|---|
| Microsoft.Data.SqlClient | 6.1.7 | Data, Data.Tests (all RIDs) | SQL Server data provider (TDS) | YES: the SQL Server provider loads it (script generation, measured); it talks to a server only on a real connection |
| Microsoft.Data.SqlClient.SNI.runtime | 6.0.3 | Data, Data.Tests (all RIDs) | SqlClient's native network layer | not loaded in the tests; only with a SQL Server connection (DERIVED) |
| Azure.Identity | 1.17.1 | Data, Data.Tests | sign-in to Microsoft Entra ID | not loaded; SqlClient uses it only for Entra ID authentication modes (DERIVED) |
| Azure.Core | 1.50.0 | Data, Data.Tests | Azure client pipeline | not loaded (DERIVED as above) |
| Microsoft.Identity.Client | 4.84.2 | Data, Data.Tests | MSAL.NET, obtaining tokens | not loaded (DERIVED as above) |
| Microsoft.Identity.Client.Broker | 4.84.2 | Data, Data.Tests | broker sign-in for desktop apps | not loaded |
| Microsoft.Identity.Client.Extensions.Msal | 4.78.0 | Data, Data.Tests | MSAL token cache for desktop | not loaded |
| Microsoft.Identity.Client.NativeInterop | 0.20.6 | Data, Data.Tests (all RIDs) | native broker binaries | not loaded |
| Microsoft.IdentityModel.Abstractions / .JsonWebTokens / .Logging / .Protocols / .Protocols.OpenIdConnect / .Tokens | 8.14.0 / 7.7.1 x5 | Data, Data.Tests | JWT and OpenID Connect types | not loaded |
| Microsoft.ApplicationInsights | 2.23.0 | Data.Tests, Devices.Tests | telemetry base API | test projects only, through `Microsoft.Testing.Extensions.Telemetry` (xunit.v3's platform); already on main (Core.Tests lock); not new by the fetch, so correctly not in the record |

Chain (lock files): SqlServer -> Microsoft.Data.SqlClient -> Azure.Identity, Azure.Core, Microsoft.Identity.Client,
.Broker, IdentityModel.JsonWebTokens, Protocols.OpenIdConnect; Azure.Identity -> Extensions.Msal. The record and the
lock files agree on every row above; the STATUS FOR TUESDAY lists them truly (and names IdentityModel and
System.IdentityModel.Tokens.Jwt).

## 3. SCOPE (item 1)

`git diff --name-status 8ae5e08c c5a6ff84`: 40 `A` (all under the four folders) + 2 `M`; `Datasec.Suite.slnx` 4 added
0 removed, each in ordinal place; `Directory.Packages.props` 3 added 0 removed, exactly SqlServer and Sqlite
`[10.0.15]` and Npgsql provider `[10.0.4]`; no other package; no `ci.yml`, `build/**` or existing lock file changed
(4 new lock files). `#pragma` lines: 8, all scaffolded (`#pragma warning disable 612, 618` / `restore` in the two
`Initial.Designer.cs` and the two model snapshots); `NoWarn` 0. Added text: ASCII, no tab (0 offending lines;
control 1); words.py over the 4640 added lines (lock files excluded): `WORDS: clean`; no base64/hex-shaped run of 32+
(control fires). Boundary scan: Devices holds none of the network, file, console, environment, clock or EF words;
Data holds no HttpClient, socket, console, Secrets reference or password connection string (its one
`System.Net.Http` hit is the SDK's generated implicit using under `obj/`). Connection strings in tests:
`.invalid` hosts, no password, SQLite `:memory:` only. No text says the product owner decided anything beyond the
ruling (STATUS "product owner" 1 hit: the quoted Q24 answer; READMEs, commit message, history entry: 0).

## 4. THE CONTRACT, THE CONTROLS, THE SHAPES NOT TESTED (item 2): my own inputs

`evidence/ReaderProbeTests.cs.txt` (55 cases, never committed), run in a scratch clone with the lane's tests:
serial (fullwidth, dotted I, Kelvin, tab, newline, NUL, 64/65, tr-TR, az, lt cultures, `NoSerial` three cases);
address (18 refused forms incl. bracketed IPv6, `%25`, uncompressed and zero-padded IPv6, fullwidth digits, edge
spaces); DNS (63/64 label, 253/254 total, underscore, IP literals, non-ASCII, Kelvin); references (18 refused,
kind cast 3, `oxpd2-admin-password` refused); snapshot (262,144 bytes ASCII and two-byte UTF-8 accepted, +1 refused,
depth 64 accepted, 65 and 20000 refused, 11 non-object shapes); defect ids; clock (300/-300 within, 301/-301
outside, both checks; null, throw, faulted, cancelled-without-token and a null task all `unknown`; MinValue against
MaxValue `outside`; tolerance 0 and -1); stale updates (wrong version 7 and 0, two contexts, an update after a clock
record): nothing saved; UTC (a `+11:00` snapshot stored `08:00:00` UTC; newest chosen by instant, not text); audit:
8 change attempts (auto-detect off, `IsModified`, detach+Update, Remove, state Deleted, sync save, save with
accept=false, a device insert in the same save) each refused with `AuditEntryChanged`, table and device count
unchanged, re-Add of an existing entry fails at the key; unknown audit text fails the read typed; cascade delete
keeps audit; options and messages hold no planted connection string. **Result: 51 of 55 green; 4 red = findings
F1 to F4 below.** The lane's controls C01 to C26 exist and run green (suite below); C19 to C21 confirmed by my
regeneration (item 6, DEVIATION 8).

## 5. MUTANTS OF MY OWN (item 3), product code, one at a time, each undone (`git diff --quiet -- src` rc 0 each)

`evidence/mutants.tsv`. 14 built, beyond the kit's list:
rZone (zone-id refusal removed) red C03; rSlash (`//` allowed) red C06; rEdge (`<=` to `<`) red C07, C08; rLen65 red
C01; rOrig (stale `OriginalValue` line removed) red C13; rDel (guard drops Deleted) red C15; rActorSp (space in actor
id) red C16; rLabel (label length) red C04; rStale2 (raw concurrency exception rethrown) red C13; rDupKind red C18;
rRefRead (kind ignored on read) red C24, C11: **11 red on the lane's own tests, by assertion.**
**Survived the lane's suite (each red on my probes):** rKeyChk (read-side key = upper(reported) check removed),
rBytes (snapshot bound counted in UTF-16 chars), rKeyOf (lookups by the reported text instead of the key): F5.
(A first rStale form did not compile under warnings-as-errors and is not counted.)

## 6. SUITE, HOSTED, MIGRATIONS (item 4)

- Through `heavy.py` (the wave lock, closed proxy), my clone at the head: locked restore (`CI=true`, audit off) rc 0;
  build `0 Warning(s)` `0 Error(s)`; `dotnet test -c Release --no-build`: **total 1335, failed 0, succeeded 1331,
  skipped 4**; `git status --porcelain` 0 lines after (no lock file changed); cache listing equal before/after.
- Hosted by GET (`hosted.py`, sha256 e73339f3...): run 44896635321: **`HOSTED c5a6ff84...: PASS`** (`--total 1335
  --rules 410 --skipped-linux 4 --skipped-windows 19 --unit 60 --floor 60`); control `--total 1336`: FAIL 4. The 19
  Windows skips are all secret-store tests, none of this lane; `NU190`/`NU1403` lines 0 on both legs;
  `GUARD: clean (10 files)` and `(11 files)` unchanged. Main 8ae5e08c by the same program: total 1191, rules 370: PASS.
- **DEVIATION 8 verified:** with the seat's scaffold program (copied; `Scaffold.csproj` = T5 with 10.0.15, T5 sha
  `b8e97283...` = FACT 8) in my scratch: mode `scripts` regenerated both snapshots byte-equal (`git diff --quiet` rc
  0); with `Migrations/` moved to quarantine, mode `migrations` re-scaffolded all six files: **6 of 6 byte-equal**
  to the committed ones once the new timestamp id is replaced by `20261121105111` (no BOM; control fires). No hand
  edit. Both snapshots: the same five tables plus the history table, 3 foreign keys each `ON DELETE CASCADE`, the id
  9 times each, no CR, no password.

## 7. THE MERGE (item 5)

`git merge-tree --write-tree 8ae5e08c c5a6ff84` rc 0, tree `15d9c76301b311b5ad974000fab5b4bd14fb4954` = the head's
tree. `repo_rules.py` (no `--source-documents`): `RULES: clean (410 files)`; `build/tests`: `Ran 60 tests`, OK.

## 8. THE DEVIATIONS (item 6)

1 fetch before stubs: accepted (no input of 3F). 2 rehearsal lock files quarantined, fetch wrote them new:
accepted (149 of 149 (A) pairs hold). 3 two failed `cd /dev/null`: accepted, records only. 4 HANDOVER at the STOP:
accepted (superseded by STATUS). 5 no mail: accepted. 6 C22 and C25 shown red by mutant: accepted (their subjects
are a frozen project file and test sources). 7 the encoded-run scan ignores letter-only runs: accepted; my own scan
with a digit-and-letter rule finds 0 (control fires). 8 scaffold re-run: VERIFIED (item 6); records: STATUS THE
MIGRATIONS still cites the first id `20261121102614` (F7). 9 `Async` names, two extra reads, `StoreReferences`, the
firmware/model rule: accepted, inside THE CONTRACT's property; its one cost is F3 (the new rule is not re-applied on
read). 10 `ToTable` names: accepted (they equal the DbSet names EF would use; D20 holds). 11 second undo Edit:
accepted.

## 9. FINDINGS

- F1 Minor: a duplicate `AddAsync` that loses a race (another context inserts between the check and the save)
  throws `DbUpdateException`, not `SuiteDataException(DuplicateDevice)`; the table still holds one row (measured
  with a save interceptor).
- F2 Minor: `CapabilitySnapshot.Create` with a lone surrogate throws `ArgumentException` (System.Text.Json's
  transcoding), not `DeviceRuleException`; nothing is held.
- F3 Minor: firmware and model are returned by `FindAsync`/`ListAsync` without re-checking their rule (a raw-SQL
  value ` fw<BEL>` reads back as held); every other stored field is re-checked.
- F4 Minor (text of a result): the clock compares the exact difference but stores a truncated offset: 300.5 s reads
  `outside` with offset 300. Never `within` without knowing: holds.
- F5 Minor (tests): three mutants survive the lane's suite (rKeyChk, rBytes, rKeyOf): no lane test looks a device
  up by a differently-cased serial, checks the stored key against the stored serial, or sizes a snapshot in
  multi-byte UTF-8.
- F6 records: the fetch record's flag prefix `Microsoft.Identity.` omits the IdentityModel ids from its flag line
  (they are in its table; the STATUS names them).
- F7 records: STATUS THE MIGRATIONS cites `20261121102614_Initial`; the tree holds `20261121105111_Initial` only.

No Blocker, no Major.

## 10. LANDING TEXTS (item 7; both readers GO WITH FINDINGS)

`pr-title.txt` (the commit subject), `pr-body.md` (names the one recorded fetch and the record's path),
`squash-subject.txt` (ends `(#PRNUM)`), `squash-body.txt` (ends the one attribution line), `landing.txt` (the
rebase-free form: `pr_retrigger.sh --check` against the then-current main; merged totals = that main's + 144, files
+ 40), `FOR-RECORDS.md` (runbook line 50, what is LEFT of WP1.1, OXPD2-12 stays open). `evidence/texts.py` (B1864's,
paths changed): neutral_export cut from ci.yml lines 120 to 128; 8 shapes each `no leaks found` rc 0, message stored
whole; planted control rc 1 `leaks found: 2`. Word scans: title, squash subject and body 0 in every class;
`pr-body.md` holds by design 1 B-number (the record path the commission asks for) and 4 non-ASCII bytes (the
`Generated with Claude Code` line); `landing.txt` is Tuesday's form (names, B-numbers, gate words by design). Word
controls 16 of 16.

## 11. NOT TESTED

Linux and Windows locally (macOS arm64 only; hosted legs ran the lane's cells, not my probes); any real PostgreSQL or
SQL Server (none exists here); a SQL Server connection's loading of Azure.Identity / MSAL (DERIVED, not run);
hosted CodeQL (runs on the pull request; `Oxpd1AdminPassword` member UNMEASURED there); the SDK audit (`NU190x`)
locally (audit off by rule; hosted legs printed none); a hang of a clock source (no timeout in the check; not in the
contract); the 15 lower bounds' contents beyond their hashes; B1871's depth points (D12, D15, D17, D18, C24) beyond
the probes above.
