GATE B1854: NO GO @ a5ba020 on main 61b17ec

Gate G1, round 1 of 2, whole-lane reader. OXPd 2, WP1.1 follow-up: the secret store listing past unreadable records
(`ISecretStoreInventory.ListAll`) and the removal of one unreadable record by its id (`DeleteUnreadable`), head
`a5ba020bc58e5239242504621a3fb2cfc20020f4` on branch `b1835/wp11-secrets-list-unreadable`, one parent = main
`61b17ec01a563bbb67465cc799a170bbb7f1cf66`. Read and measured 2026-11-21, 18:55 to 19:40 AEDT (clocks by `date`), on Opus 5.5,
in the gate's own clone (session scratchpad, `b1854-clone`, push URL `invalid://no-push`; the workspace hook refuses git
write verbs outside the scratchpad). Scratch, logs and probes: `/private/tmp/b1854-gate/`. The probe source, its output, the
mutant program and its output are copied into `evidence/` beside this file. Every heavy job went through the kit's own
runner (`heavy.py`, sha256 `31adedc8...`, six of six tool hashes equal to the kit): load1 read first, the wave lock
`<project>/.tools/wave1-heavy.lock.d` taken by `mkdir` with `owner.txt`, released by a move into
`/private/tmp/b1854-gate/_quarantine/locks/`; restores with `-p:NuGetAudit=false`. `repo_rules.py` was never given
`--source-documents`; no key folder was opened; every value is synthetic and none is printed here.

**BLUF.** Scope, the frozen parts, the contract shape, the build (0 warnings), the local suite (913, failed 0), the hosted
run (PASS, `Ran 60`, floor 60), the 14 cells and nine gate mutants (all red, all undone) hold, and 70 of the gate's own
adversarial rows behave exactly as the kit says. **But `DeleteUnreadable` removes a record that READS, measured twice:**
when the process cannot open the record file for a reason of the PROCESS, not of the record (no file descriptor left; the
file held open by another opener without read sharing), the record store's read fails with an I/O error, the store's
existing mapping turns that into `UnreadableRecord`, the removal's re-check reads "does not read", and the file is
unlinked. After the fault clears, the record is gone. The README's sentence "A failure that is not a record's own
(`StorageFailed`) makes either call throw, with nothing listed or removed" is untrue for exactly this case. This is the
commission's first NO GO class (a readable record removed): **one Major, a fix round follows.** Nothing else blocks.

## Findings

| # | Severity | Finding | Recommendation |
|---|---|---|---|
| F1 | **Major** | **`DeleteUnreadable` destroys a readable record on a transient fault of the process.** Measured on this Mac (evidence/probes.txt): **G12**: store with `good/a`, `good/b`; the process's open-file limit lowered to 1024 and filled (862 descriptors held); `ListAll()` throws `StorageFailed` (its directory listing fails first), but `DeleteUnreadable(id of good/a)` returns **true**; descriptors released and the limit restored (rc 0): `good/a`'s file no longer exists. **G11**: `good/a`'s file opened elsewhere with `FileShare.None` (on Unix the runtime takes an exclusive advisory lock; the store's read takes a shared one and fails with a sharing violation): `ListAll()` lists `good/a` as UNREADABLE (stated name null) and `DeleteUnreadable(id of good/a)` returns **true**; the holder closed: the file is gone, `TryGet` false. Mechanism (source): `FileSecretRecordStore.TryRead` maps every `IOException` and `UnauthorizedAccessException` to `UnreadableRecord` (`FileSecretRecordStore.cs:42-45`, frozen, unchanged); `Judge` turns `UnreadableRecord` into "does not read" (`LocalSecretStore.cs:468-470`); `DeleteUnreadable` then calls the record store's delete (`:257`), and an unlink needs no descriptor and ignores an advisory lock. The listing alone only threw before this lane, so the mapping was harmless; this lane is the first caller that DESTROYS on it. Not in the kit's tables H1 to H19, not among the README's named destructions (second process, revoked key, moved key entry, mode 000), and contrary to the README sentence quoted in the BLUF and to U07's own comment ("a storage fault, never a removable record"), which holds only for the in-memory test store whose failures are untyped. On the Linux container host, descriptor exhaustion under load is the realistic path (DERIVED: the same open and unlink calls; not run on Linux); on Windows a sharing violation is also `UnreadableRecord`, and the delete then fails unless the holder allowed delete sharing (DERIVED, not run). | A design choice for Tuesday (a behaviour beyond D7 as worded), then one fix commit and a re-gate. Shapes, each fails closed: (a) the removal requires that the record's BYTES were read and failed a record step (parse, id, name rule, open), and treats a failed read as `StorageFailed` (then an empty file, a link, a pipe and a mode-000 file are not removable by id: U04's rows and the README change); (b) `FileSecretRecordStore` maps an `IOException` or `UnauthorizedAccessException` of the open or read to `StorageFailed` and keeps `UnreadableRecord` for what its look-before-open refuses (a frozen file and a change of `ListNames`' reason: D10 must be reopened); (c) keep the code and NAME it in Limits: "a record that this process cannot open at that moment for any reason, among them no file descriptor left or a file held by another opener, is removed" and delete the `StorageFailed` sentence. G11 and G12 (evidence/GateProbeTests.cs) are ready-made cells for (a) or (b); G12 changes a process-wide limit and must run alone (it is in a collection with parallelisation off). |
| F2 | Minor (text) | The interface summary of `DeleteUnreadable` says "The key ring is not used." (`ISecretStoreInventory.cs:20`). The re-check opens the record with the key ring (`Judge` -> `VersionOfOpened` -> `Open` -> the protector, `LocalSecretStore.cs:465`, `:749`, `:816`). True reading: the key ring is not CHECKED (no `CheckRingUnchanged` / `CheckRingHealthy`), as for `Delete`. | "The key ring is not checked first; the record is opened with the keys this store holds." |
| F3 | Minor (records) | A symbolic link to a FOLDER at a record's path is not listed by `ListAll()` (and `ListNames` works), yet `DeleteUnreadable` of its id returns true and removes the LINK (the folder and its content are kept). Measured, G07. The README sentence covers a real folder only. Harmless (only the link goes). | One README clause, or records only. |
| F4 | Minor (cells) | No cell of the lane (and no gate row that ran) exercises a record store whose DELETE fails on an unreadable record (my G09 attempt removed the record in its first mode, so its `delete-throws` mode found the record absent: a probe error of mine, said here, not a product result). The `StorageFailed` path of the delete is read from source only (`TypedRecordStore`, `:982`, `:986-995`). | A cell in the fix round: a store whose read returns garbage and whose delete throws: `DeleteUnreadable` throws `StorageFailed`, record kept. |

No Blocker. No text names a person, a ticket, a brief or says anyone decided anything (words scan clean, below).

## 1. Scope and frozen parts (measured, `scratch/scope.py` over `git show`)

- `diff --name-status 61b17ec0 a5ba020b`: `A src/Datasec.Suite.Secrets/ISecretStoreInventory.cs`, `M LocalSecretStore.cs`,
  `M README.md`, `M SecretStoreServiceCollectionExtensions.cs`, `A tests/Datasec.Suite.Secrets.Tests/InventoryTests.cs`:
  exactly 3 modified and 2 added; 863 insertions, 2 deletions; ahead 1, behind 0; paths 293 -> 295, 0 removed.
- Every one of the 293 main paths compared byte for byte: the only changed ones are the three above. So `Datasec.Suite.slnx`,
  `Directory.Packages.props`, every `packages.lock.json`, `.github/**`, `build/**` and every existing test file are
  byte-equal to main (no package, lock, solution line or workflow change).
- The `ListNames()` block (main lines 199-218): 20 lines, 715 bytes, sha256 `5f03bc9753b8c3a8...` (= the kit); count in the
  head's `LocalSecretStore.cs` **1**; control (one more space) 0.
- The seven frozen files (`ISecretStore`, `ISecretStoreMaintenance`, `SecretStoreError`, `SecretStoreException`,
  `SecretRecord`, `SecretNames`, `FileSecretRecordStore`): each byte-equal to main; sha256 prefixes equal to the kit's FACT 3.
- Commit: one, author and committer the repository's own identity (name and address equal; address not printed); subject
  is the kit's; body the one attribution line `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.

## 2. The contract and the cells

- Shape as built equals THE CONTRACT: `ISecretStoreInventory { SecretInventory ListAll(); bool DeleteUnreadable(string) }`;
  `SecretInventory` sealed, internal constructor, `Readable` / `Unreadable` as `Array.AsReadOnly` over fresh arrays;
  `UnreadableSecret(string RecordId, string? StatedName)` readonly record struct; the class line the one changed line;
  one registration line. `ListAll` and `DeleteUnreadable` call ONE private `Judge` that runs `ListNames`' own steps in its
  order (`TryRead`, `ReadHeader`, `VersionOfOpened`) and turns only `UnreadableRecord` into "does not read" (D2, D5);
  `StatedNameOf` decodes, applies the name rule and compares `RecordIdOf(name)` with the id (D3); `DeleteUnreadable`
  checks the id rule before the lock, then under the lock removes only on "does not read" (D7).
- U01 to U14 read in the test file: each asserts what the kit's table says (U02's five parts i to v including the parity and
  the partition print; U04 "differs by that one entry only"; U05 byte-equality by `SequenceEqual`; U07 the path and
  separator checks; U09 the reflection rows and `TextHolds`; U12 the exact member lists and the 20 exported types; U13 and
  U14 the named limits, U14 running the removal). Rows r1 to r8 plus the three Unix rows are as the kit's H1 to H7.
- **The gate's own adversarial rows (evidence/GateProbeTests.cs, run in the store's test project at the head; 72 rows):**
  H1 a payload bit flipped at the header, the key id, the middle and the last byte (4 rows); H2 another ROOT's record of
  the same partition and name, another partition's record of a name absent here (2); H3 16 kinds of bytes that are no record
  (version 0, format 2, five properties, name null, name a number, payload empty, payload not base64, a BOM before a record,
  a record then `{}`, 100000 nested brackets, invalid UTF-8 in the name, a lone-surrogate escape, version as a string,
  version 2^31, one byte, one byte over the size limit); H4 nine rule-breaking names at their own id (upper case, 201
  characters, `a//b`, `a/`, `-a`, a non-ASCII letter, `a..b`, a NUL, a space) and one planted rule-following name with a
  garbage payload; H5 `good/a`'s record copied under another id; H6 version 2 set back to 1, set to `int.MaxValue`, set to 0;
  H7 empty file, mode 000, a link to the record moved outside, a dangling link, a named pipe, a hard link of `good/a` under
  another id, a link to a folder, a real folder. **Every one of these 70 rows: listed exactly once by its own id; the stated
  name exactly as D3 says (the name for H1, H2, H6 changed in place and the planted rule-following name; null for every
  other); the two good names readable; the PARITY with `ListNames()` held before and after; `DeleteUnreadable` removed
  it; then nothing unreadable and both good values read byte for byte.** The link to a folder and the real folder are not
  listed (parity holds); the removal leaves the real folder (false) and removes the link only (F3). Every call returned
  inside a 10 s thread guard.
- H9 / H10: a readable id -> false, the file byte-equal; an absent id -> false; 14 ids outside the rule (null, empty, 63,
  65, upper case, `/`, `.`, 64 full-width `a`, 64 Arabic-Indic zeros, a trailing line feed, a leading space, a `g`, a `../`
  prefix, a path) -> each `InvalidName`, no inner exception; record files still 2; both values read.
- H12: a caller's record store failing in the listing, in the read with `UnauthorizedAccessException`, in the read with
  `IOException`: `ListAll` `StorageFailed`; `DeleteUnreadable` `StorageFailed` on the two read faults; no message holds a
  path or separator, no inner. (The FILE store maps the same exceptions the other way: F1.) H16: a disposed store:
  `ObjectDisposedException` from both; an id outside the rule on a disposed store is `InvalidName` (the id check is first,
  as `Delete(name)` checks the name first: consistent). No `ToString` of the inventory or its entries holds a form of either
  synthetic value.
- **F1 rows: G11 and G12 (above): a readable record removed.** These are the two of 74 probe outcomes that differ from the
  kit's property; the 74th (G09's delete mode) is my probe's error (F4).
- Test run of the probes: `total: 94` (82 of the store's project + 12 gate tests), `failed: 3` (G11, G12, G09 as said),
  `skipped: 4` (the base's four Windows-only cells). The probe file was then moved out of the clone
  (`/private/tmp/b1854-gate/_quarantine/probe1/`); the clone's `status --porcelain` printed 0 lines.

## 3. The second reader's points

D3, D7, H14 and H15 are reader B1855's. From this reader's side: the stated name only ever equals a name whose SHA-256 is
the listed id (source and the 70 rows), so `Delete(StatedName)` reaches that same id; the removal's re-check is under the
store's one lock; U13 and U14 ran green here and on both hosted legs. F1 is a NEW way for D7's property to fail that is
not a race: it needs no second thread and no second process.

## 4. Mutants (the gate's own texts, made by program; each run = build and test of the store's test project, 82 tests; undone by restoring the original bytes and proved by `git diff --quiet` rc 0)

| Mutant | Text | RED (by assertion) |
|---|---|---|
| mOpen | `Judge`: `VersionOfOpened(record)` -> `record.Version` | U02, U03, U04, U06, U09, U13, U14 (7) |
| mHash | `StatedNameOf`: `return name;` (no id comparison) | U02, U08 (2) |
| mRecheck | `DeleteUnreadable`: removes unless ABSENT (`!= RecordState.Absent`), so a readable record too | U05 (1) |
| mFirst | `ListAll`: throw `UnreadableRecord` at the first unreadable record (first text left a `break` that did not build, CS0162; remade) | U02, U03, U06, U08, U09, U13, U14 (7) |
| mStorage | `Judge` also takes `StorageFailed` as "does not read" | U07 (1) |
| mMutable | `SecretInventory` holds the raw arrays (`T[]`) | U09 (1) |
| mDisposedDelete | `DeleteUnreadable` without its disposed check | U10 (1) |
| mOrder | `Unreadable` reversed | U02, U13 (2) |

Eight of eight red, eight undone (rc 0 each); the builder's twelve were not re-run (each of the six named re-made
independently above). No mutant survived; but note F1 is a product property no cell holds, so the suite would stay green
under any fix that leaves the I/O mapping alone.

## 5. Build, suite, hosted

- Through the lock in the gate's clone at the head: `dotnet restore Datasec.Suite.slnx --locked-mode -p:NuGetAudit=false`
  with `CI=true`: rc 0, 13 restored or up-to-date lines, 0 lines naming an HTTP source (closed proxy); `status --porcelain`
  0 lines (no lock file changed). `dotnet build Datasec.Suite.slnx -c Release --no-restore`: rc 0, `0 Warning(s)`,
  `0 Error(s)`. `dotnet test -c Release --no-build` (whole suite): `Passed!`, `total: 913`, `failed: 0`, `succeeded: 909`,
  `skipped: 4` = 899 + 14.
- Not heavy: `build/repo_rules.py <clone>` without `--source-documents`: `R5 hash half NOT RUN`, `RULES: clean (295 files)`;
  `unittest discover -s build/tests`: `Ran 60 tests`, `OK`.
- Hosted run 44882077016 of `a5ba020b` by GET (`hosted.py --total 913 --rules 295 --skipped-linux 4 --skipped-windows 19
  --unit 60 --floor 60`): four jobs success; linux `total: 913` x2, `succeeded: 909`, `skipped: 4`, `GUARD: clean (10 files)`;
  windows `total: 913` x2, `succeeded: 894`, `skipped: 19`, `GUARD: clean (11 files)`; both `0 Warning(s)` `0 Error(s)`;
  secret-scan both PLANTED-CONTROL lines, `objects of this commit not among them 0`, `no leaks found` x3; rules `Ran 60 tests
  in`, `UNIT-TEST FLOOR: ran 60, floor 60`, `RULES: clean (295 files)`. `HOSTED a5ba020b...: PASS`. Control: the same with
  `--total 914`: `FAIL 4`. Windows log (escape codes stripped): 20 lines with the word skipped, 0 naming `InventoryTests`
  (control: 6 name `KeyRingProtectionTests`).
- Code scanning: no `Analyze` run on a branch push (none beside the four); the C# extractor cannot run on this arm64 box.
  Hand rows over the 863 added lines: no logger, no console, no write of a value whose name holds a password word; the only
  new names holding "Secret" are the type names, as on main (0 open alerts there). CodeQL csharp: NOT RUN; the pull
  request's analysis is the only proof.

## 6. The builder's deviations

1. `--no-restore` on the mutant and probe runs: **accepted** (it still builds; a plain implicit restore under the closed proxy
   is the known NU1900 trap). The gate did the same.
2. Own `Snapshot` instead of `RingKit.Fingerprint`: **accepted** (Fingerprint opens files: it would throw on mode 000 and block
   on a pipe; U04 needs a per-entry diff). `RingKit.cs` is byte-equal to main.
3. Stricter cells (U07's second store, U13's later record, U14 running the removal, U12's full type list): **accepted**. U07's
   comment is untrue of the file store (F1), not of its own test store.
4. The temporary edit of the frozen `ISecretStore.cs` for U12's red: **accepted; byte-equal now** (head vs main equal; sha256
   `63261a88...` = BASE).
5. Always-false mutant texts: **accepted** (still mutants of the decision; each red).
6. A STATUS clock corrected: **accepted** (records).

## 7. What was NOT tested

- Linux and Windows locally (macOS arm64 only): F1 on Linux and the Windows sharing-violation path are DERIVED; the hosted
  legs ran the lane's cells, not the gate's probes.
- D3 steering, D7 races, H14 and H15 in depth (reader B1855's).
- The two publishes and the release guard locally (hosted GUARD lines read instead); CodeQL (cannot extract C# here).
- The landing texts: NOT WRITTEN (item 7 is for GO or GO WITH FINDINGS only).
- A record store whose delete fails on an unreadable record (F4).
- The builder's twelve mutant texts as written.
