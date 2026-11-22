GATE B1939: GO WITH FINDINGS @ b74f0f0 on main c480a0c

Gate G1 (security surface and data destruction; audit integrity), round 1 of 2 of lane F2, the lane's one reader.
OXPd 2, kit B1936 (seat X38; Q1 = a and Q2 to Q6 the defaults, each the coordinator's stamp S4, not the product
owner's): owed items 42 (2), 43 (1) and 45. Head `b74f0f0cf1de5e8599e9d5983dc3f36283364aca` on
`b1936/f2-store-audit-map-follow-ups`, ONE commit over `c480a0c8`. Read and measured 2026-11-23 00:59 to 01:16 AEDT
on Opus 5.5 in my own scratch under `fleet/state/s312/g1939/`: `clone` (by the kit's `clone.py ... draft`: push URL
`invalid://no-push`, no identity; detached at the head), worktree `red` (main `c480a0c8` plus `1-cells-red.diff`),
worktree `both` (lane F1's head `c15e13f5` plus this lane's diff). Every dotnet job through the kit's `heavy.py` and
the wave lock, one at a time (lock waits 0 to 3, load1 2.1 to 6.9). Origin by `gh api -X GET` under the project
GH_CONFIG_DIR at 01:12: main = `c480a0c8`; branch = `b74f0f0c`; open pull requests 0 (newest 25, closed);
`compare main...b74f0f0c` ahead 1, behind 0, 7 files. No write to the project, GitHub or Jira; no push, no pull
request; no `cd`; nothing deleted (my probe files and the scanner control moved to `g1939/_quarantine/`).

**BLUF.** The lane does what its kit says, and every check the commission names reads as the kit measured it. U23 is
RED at main by its own assertion and GREEN on the head; the five mutants are each red on exactly their cells; the
public surface is byte-equal on all three assemblies at main and at the head, and the plant control differs; the
census equals the README's numbers, its control fired; the head's whole solution is 1664 / 0, its hosted run PASS;
the merge with lane F1 in either order is clean and reads 1670 / 0. My probes of the second judgement (absent,
replaced, a fault of another kind at the second read) and of the catching hook (handler, interceptor, direct object
assignment) each read as the README now states. **One Minor finding, not a regression and not in a changed line: the
Data README's `SavedChanges` line, left unchanged by Q4, says "the caller sees the refusal", and a `SavedChanges`
handler that catches hides it** (FOUND 1, measured; the "never written" half holds). Nothing blocks the landing. It
can go to the records pass (FOR-RECORDS item 1, with a fix sketch) or back as a one-line fix round; that choice is the
coordinator's.

## FOUND

1. **Minor (README accuracy, a sentence this lane did not change; the property holds): the `SavedChanges` limit line
   is not true of a handler that catches.** `src/Datasec.Suite.Data/README.md` Limits: "A handler of the context's
   `SavedChanges` event, or a save interceptor's `SavedChanges` step, runs after the save's commit: an audit entry it
   changes or removes is refused and the change is never written, but the save's own rows are already written, so the
   caller sees the refusal for a save whose rows are stored." MEASURED (probe P8, scratch, macOS arm64, on the head): a
   `SavedChanges` handler that catches `AuditEntryChanged` around a change to a saved entry: `caught 1; state
   Modified; first save exception none; after first rows 4; rows user-9 0; second save SuiteDataException
   AuditEntryChanged; after second rows 4; rows user-9 0`. So kit B1936's D5 (DERIVED there) holds: the change is
   never written, because the next save's pre-check (`SuiteDbContext.cs:95` / `:110`, `RefuseChangedAuditEntries`)
   refuses the still-modified entry. But "the caller sees the refusal" is false in this shape: the caller of that save
   sees none, and the refusal arrives at the NEXT save on that context instead. The audit sentence above it now names
   a catching hook only for `SavingChanges` and save interceptors. Fix sketch: one clause on that line ("; a handler
   that catches the refusal hides it from the caller of that save, and the next save on that context refuses the
   still-changed entry"), with P8's shape as an optional limit cell (+1 total). Q4's default ("the line unchanged")
   was the coordinator's call pending exactly this measurement.

## INFO

1. **The catching-hook limit is exactly scoped (P5, P6, P7).** P6, the kit's handler shape with the state read after
   each catch: `caught 3; states after catch Modified/user-9 (x3); exception none; rows 4; rows user-9 3` (the
   README's "after the entry's state has changed" and "the save writes the change"). P5, gate B1933's N5b re-measured
   on the head (the kit only RELAYED it): an interceptor that catches around each removal: `caught 3; states after
   catch Deleted (x3); exception none; rows 1`. P7, a handler that sets the entity's property directly (no tracker
   call) inside a try/catch: `caught 0; exception SuiteDataException AuditEntryChanged; rows 3; rows user-9 0`: the
   refusal is raised by the save's own change detection after the hook, out of its reach, and nothing is written (the
   append included). The README names the limit for a hook that catches, and that is the only shape that keeps a
   change.
2. **The second judgement's other outcomes, measured (P1 to P4; kit H6 and H7 were DERIVED).** A scripted record
   store of my own over the tests' `SwitchableRecordStore`, injected by the public `LocalSecretStoreOptions.RecordStore`:
   P1 a record damaged at the first read and absent at the second: `removed False; reads 2; deletes 0; held True`
   (H6). P2 a record damaged at the first read and replaced at the second by another record's good bytes (they do not
   read under that id): `removed True; reads 2; deletes 1` (H7: the second judgement does not re-check the payload's
   key id; the README's one-process-per-partition limit covers a second writer). P3 a fault of another kind
   (`InvalidOperationException`) at the second read: `StorageFailed; deletes 0; held True`, the record reads byte for
   byte afterwards (`TypedRecordStore` maps it, `LocalSecretStore.cs:1061` to `:1071`). P4 bytes that do not parse:
   `removed True; reads 1; deletes 1` (no key id, no probe, no second read, as on main). A fault INSIDE the probe is
   caught by `ProbeRoundTrips`' `catch (Exception)` and reads as a failing probe, `StorageFailed` (`:521` to `:541`,
   DERIVED; the protection failing at the probe is U22's, red under `mProbeIgnored`). Both judgements and the delete
   run inside `DeleteUnreadable`'s one `lock (_gate)` (`:255` to `:265`), so no other caller of this store interleaves
   (DERIVED); another process can (H7).
3. **U23's second half does not assert that its first read was the damaged one** (`DamagedReads` is asserted only in
   the first half). It is deterministic by construction (`_left = 1`, consumed by the first `TryRead`), and
   `mRejudgeLosesFault` kills that half. No change needed.
4. **The map sentence is true as worded; the census frame in detail** (my own walk, `scratch/census_probe.py`): the 75
   inline open objects are 73 properties and 2 array items; every open object carries only `type` and `description`
   (148 a `description`, none `anyOf`, `oneOf`, `enum` or `$ref`), so each reaches the generator's
   `case "object"` branch (`contracts/oxpd2/generator/Oxpd2Unit.cs:337` to `:348`); no `type: object` schema has an
   empty `properties` (0), which the generator would also read as open. The "66 properties" counts generated property
   lines, not schemas (`capabilities.implInfo.items.value` alone repeats in 15 inputs). `BeepRequest` is the input's
   `components/schemas/beepRequest` (`com.hp.ext.service.application/1/0`), `type: object` with no property: open.
   `additionalProperties` is not in the generator's `Unsupported` list (`Oxpd2Unit.cs:16`), so it is ignored, not
   refused: the README's "How an input with a declared map would be generated is UNMEASURED" stays honest.
5. **Cosmetic:** the Secrets README removal paragraph leaves one short line (`stays. A record under a key the`) before
   the long existing line; the seat's text check counted `0 of 29` against the kit's `0 of 28` (numstat 19+3+5+2 = 29;
   the seat's DEVIATION 1, correct).

## WHAT I MEASURED

- **THE TOOLS:** `cp -Rc` of `fleet/state/s312/d1936/gate/` to `g1939/gate/`; 13 of 13 sha256 equal to kit B1936's
  table. `words.py --control` `CONTROL FIRED: 13 of 13`.
- **THE DECISIONS against the code** (read whole: `BASE..b74f0f0c`, 181 + / 16 -): D1 `RemoveUnopened`
  (`LocalSecretStore.cs:498` to `:519`): the outer condition is the key-id-and-active test only; a failing probe
  throws `StorageFailed`; then `switch (Judge(recordId, out _, out _))`: `DoesNotRead` falls to `_records.Delete`,
  `NotHandedOver` throws `StorageFailed`, `default` returns false. First judgement, `CheckRingUnchanged()` and the
  revoked/unknown branch unchanged. No new field (no `object` field; U21's lock lookup unaffected). D2 `DamagingRecordStore`
  test-only, injected by the public option. D3/D4 `SuiteDbContext.cs` changes in `///` lines only (`:196` to `:202`);
  the limit cell `AuditTests.cs:277` as described. D5 the `SavedChanges` line unchanged (FOUND 1). D6 the map sentence
  (`README.md:149` to `:156`). D7 `rev-list --count c480a0c8..b74f0f0c` = 1, parent `c480a0c8`; the commit message
  equals the kit's `commit-message.txt`.
- **THE CODE:** the seven files at the head equal THE CODE's after-column sha256 (the five `src/` files printed; the two
  test files equal to `1-cells-red.diff` applied at main); numstat equal to the kit's.
- **RED FIRST (worktree `red`, main + `1-cells-red.diff`):** apply rc 0; build rc 0; Secrets `Total: 95, Errors: 0,
  Failed: 1, Skipped: 4`, the one `[FAIL]` `InventoryTests.U23_After_a_passing_probe_the_record_is_judged_again_and_removed_only_while_it_still_does_not_read`,
  message `U23: a record that reads when judged again after the probe was removed` at `InventoryTests.cs(667,0)`; Data
  `Total: 64, Errors: 0, Failed: 0` (the limit cell pins today's behaviour).
- **GREEN (clone at the head):** locked restore rc 0; build `0 Warning(s)` `0 Error(s)`; whole solution `total: 1664`,
  `failed: 0`, `succeeded: 1660`, `skipped: 4`; Secrets 95 / 0 (4 skipped); Data 64 / 0; Adapters.Oxpd2 58 / 0. Again
  after the mutants, the plant and my probe files were each undone and the tree rebuilt: 1664 / 0 / 1660 / 4;
  `repo_rules.py` (no `--source-documents`, `1_Project_Definition` absent) `RULES-NOTE: R5 hash half NOT RUN (no
  supplied-source folder here)`, `RULES: clean (530 files)`.
- **THE MUTANTS (`mutants3.py`, each applied, built, run whole, undone `equal True`, `git diff --stat` equal):**
  `mNoRejudge` Secrets 95 / 1: U23. `mRejudgeKeepsAll` 95 / 2: U04 and U23. `mRejudgeLosesFault` 95 / 1: U23.
  `mProbeIgnored` 95 / 1: U22. `mNoStateChanged` Data 64 / 7: the new limit cell and kit B1932's six. Each exactly as
  THE CONTROLS. Rebuilt after the last undo: Secrets 95 / 0, Data 64 / 0; `LocalSecretStore.cs` `67bce2eb...`,
  `SuiteDbContext.cs` `bfe28591...`; status clean.
- **THE SURFACE CHECK:** the kit's reflection program built in `g1939/surfacebuild` into `g1939/surface-out`. At main
  (worktree `red` before the red diff) and at the head: `SURFACE: 160 lines, sha256 cd5625c8...` (Secrets), `107
  lines, 6acf7547...` (Data), `22915 lines, cefd886f...` (Adapters.Oxpd2); `cmp` main vs head rc 0 on all three.
  Control: `public const int SurfacePlant = 1;` after `MaxValueLength` (Edit tool), build, `SURFACE: 161 lines,
  sha256 88feb4f6...`, the one extra line `field System.Int32 SurfacePlant = 1 static`; file copied back, status clean,
  rebuilt, the surface `cmp` equal to the head's again. `surface.py <clone> c480a0c8`: `PUBLIC: equal (85 lines)`,
  `SCHEMA: equal (8 files)`; `--control` `CONTROL FIRED: 2 of 2`.
- **CENSUS:** `census.py <clone>` printed FACT 6's line exactly (`inputs 37; object schemas 1616, with properties
  1442; additionalProperties 206, false 206; patternProperties 0; propertyNames 0; open 150 (components 75, inline
  75); generator reads ... 0, 0, 0 (control "properties" 3); generated JsonElement properties 66 in 21 Models.cs;
  Any(true) 66`); `--control` `CONTROL FIRED: 2 of 2`. Every number of the map sentence (206, `false`, none of the
  two keywords, none of the three read, 150, 66) matches. The three readings re-read at source: `Oxpd2Unit.cs:337` to
  `:348` (open inline to `AnyRef(true)`, a component to a model); `Generated/Runtime/Oxpd2Json.cs:358` to `:363`
  (`ObjectOnly`: a non-object refused `WrongType`, an object skipped over and held); `:419` and `:427` to `:429` (an
  unlisted key: `index < 0` then `Skip`); `Generated/Application/Models.cs:829` `BeepRequest` with only its schema
  member; `:886` `CapabilitiesImplInfoItem.Value` a `JsonElement`.
- **README SENTENCES against the code at the head:** Secrets removal paragraph and Limits (the start's encryptor check
  `LocalSecretStore.cs:681` to `:687` in `FullCheck`, the key-source check `:690` and `:739` in `CheckRingUnchanged`):
  true. Data audit sentence and the new Limits line: true (P5, P6, the limit cell); the `SavedChanges` line: FOUND 1.
  `SuiteDbContext` doc comment: true (P6). `RemoveUnopened` doc comment: true. Adapter map sentence: true (CENSUS,
  INFO 4).
- **THE REQUIRED SECTION H1 to H12:** H1 to H4 confirmed by red-first and the mutants; H5 the README's residual,
  UNMEASURED (as the kit says); H6 and H7 now MEASURED (P1, P2); H8 confirmed (P4; U04, U13, U22 green); H9 the limit
  cell; H10 MEASURED (P5); H11 MEASURED (P8, FOUND 1); H12 the census and source. No shape left out.
- **MY PROBES** (scratch files `G1939Probes.cs` in the two test projects of `clone`, built and run whole through the
  lock: Secrets `Total: 99, Errors: 0, Failed: 0`, Data `Total: 68, Errors: 0, Failed: 0`; output lines in
  `g1939/scratch/probe-secrets.txt` and `probe-data.txt`; the files then moved to `g1939/_quarantine/probes/`):
  D1 P1, P2, P3, P4; D2 the five mutants and P2/P3 through the same public option; D3 P6, P7; D4 P5; D5 P8; D6
  `census_probe.py` (INFO 4); D7 the commit count and parent.
- **THE MERGE:** `git merge-tree --write-tree --name-only c15e13f5 b74f0f0c` rc 0, tree `39f04ba2...`, no conflict;
  lane F1's seven paths (SignIn, its tests, UniversalPrint Registration and its tests) disjoint from this lane's. In
  worktree `both` (c15e13f5 + this lane's diff, `git apply --index`, `write-tree` = `39f04ba2...`): locked restore rc
  0; build `0 Warning(s)` `0 Error(s)`; whole solution `total: 1670`, `failed: 0`, `succeeded: 1666`, `skipped: 4`.
  Order A (this lane first) is the head's own tree: 1664. Both orders in `landing.txt` MAIN MOVES.
- **HOSTED:** `hosted2.py b74f0f0c... --total 1664 --rules 530 --skipped-linux 4 --skipped-windows 21 --unit 111
  --floor 111 --hardened-scan` rc 0: run 45029832759, attempt 1, four jobs success; linux 1664 twice, succeeded 1660,
  skipped 4, GUARD 10 files; windows 1664 twice, succeeded 1643, skipped 21, GUARD 11 files; rules RULES 530, floor
  111; secret-scan every hardened row OK; `HOSTED b74f0f0cf1de5e8599e9d5983dc3f36283364aca: PASS`.

## SCANS

- `words.py` over the 181 added lines of `c480a0c8..b74f0f0c` and the head's commit message (`scratch/neutral/1.txt`,
  `2.txt`): every count 0, `WORDS: clean (2 files)`. Over `squash-subject.txt`, `squash-body.txt`, `pr-title.txt`:
  `WORDS: clean (3 files)`.
- gitleaks 8.30.1 `dir --no-banner --redact --ignore-gitleaks-allow --exit-code 1` over the added lines and the
  message: rc 0, `no leaks found`. Control: a token-shaped value built by program from two halves and 36
  random characters in a new scratch folder, never printed: rc 1, `leaks found: 1`; folder moved to
  `g1939/_quarantine/leak-ctl`. Over this verdict folder: see the last line of SCANS below.
- `build/squash_scan.py squash-subject.txt squash-body.txt --scanner /opt/homebrew/bin/gitleaks` (from the clone; the
  workflow file equals main's): control `rc 1, found 2`, message `rc 0, found 0`, `SQUASH-SCAN: clean`.
- gitleaks over this verdict folder (six files, before this line was added): rc 0, `no leaks found`.

## CODEQL

Not run locally (the gate has no CodeQL step). Read on the pull request (`landing.txt` step 3): the shapes in this diff
are a `switch` whose `default` returns from inside the caller's `lock`; in the tests, a filtered `catch` that swallows
the refusal inside an event handler (deliberate: the limit cell), `int.MaxValue` as a read count, and a byte flipped in
a cloned payload.

## NOT RUN

Any run on Linux or Windows locally (the hosted legs of the head only; the merge with F1 on the hosted legs is not
measured, windows 1649 PREDICTED); `repo_rules.py --source-documents` (never); the server, any database server, any
listener; a fault for one key inside the data protection library (H5); CodeQL; `run_step.py` (the hosted secret-scan
job ran it on the head: PASS).

## DEVIATIONS

None from the commission. Two `grep` calls of mine were refused (an unquoted `--include=*.cs` glob in zsh; an
unscoped recursive search stopped by a hook) and re-run scoped and quoted; one case-sensitive name search of mine gave a false zero (`BeepRequest` vs the
input's `beepRequest`) and was re-run by a walk that printed the node.

## TREES LEFT

`g1939/clone` detached at `b74f0f0c`, status clean (mutants, plant and probe files undone, rebuilt); worktree `g1939/red`
at `c480a0c8` with `1-cells-red.diff` applied (uncommitted); worktree `g1939/both` at `c15e13f5` with this lane's diff
staged (uncommitted); `g1939/surfacebuild`, `g1939/surface-out`, `g1939/logs/**`, `g1939/scratch/**`,
`g1939/_quarantine/{locks,leak-ctl,probes}`. No process left running; the wave lock not held by this reader.
