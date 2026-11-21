GATE B1864: GO WITH FINDINGS @ 8578d96 on main 977cbeb

Gate G1, round 2 of 2 (delta), whole-lane reader (successor of round-1 reader B1854). OXPd 2, WP1.1, lane SL: the
fix round of the secret store listing (`ListAll`) and removal (`DeleteUnreadable`), head
`8578d96c7881b7023d707600c5e2f0b03722d8d1` (one parent `a5ba020b`) on branch `b1835/wp11-secrets-list-unreadable`,
main `977cbeb2994e6592ba9e4ce677c278c5131d11c4`. Read and measured 2026-11-21, 21:11 to 21:30 AEDT (clocks by `date`), on
Opus 5.5, in the reader's own clone (session scratchpad `b1864-clone`, made by the kit's `clone.py ... draft`: push URL
`invalid://no-push`, no identity) and a second scratch clone of the merge (`b1864-merge`). Scratch and logs:
`/private/tmp/b1864-gate/`; the probe source, its outputs, the mutant program and its output, and the hosted reading
are copied into `evidence/`. Every heavy job went through the kit's runner (`heavy.py`, sha256 `31adedc8...`; the seven
tool files of `fleet/state/s305/d1857/gate/` seven of seven equal to the kit; `words.py --control` `CONTROL FIRED: 13 of
13`): load1 first, the wave lock `<project>/.tools/wave1-heavy.lock.d` by `mkdir` with `owner.txt`, released by a move
into `/private/tmp/b1864-gate/_quarantine/locks/` (the first job waited 83 polls behind reader B1865's batch: a wait,
not a finding); restores `--locked-mode -p:NuGetAudit=false`. `repo_rules.py` was never given `--source-documents`; no
key folder was hashed, listed or opened; every value is synthetic and none is printed. No git write in any project
tree, no GitHub or Jira write, no message.

**BLUF.** Round 1's Major is closed. At the new head `DeleteUnreadable` removes a record only when its bytes were read
in full and fail as a record, refuses with `StorageFailed` whatever the record store cannot hand over, and first runs
the write's ring check (`KeyNotAvailable`). G11 (a good record held with `FileShare.None`) now ends `StorageFailed`, the
file byte-equal and both values read; G12 (descriptors exhausted) now ends `KeyNotAvailable`, nothing removed, the
limit restored rc 0. All 43 bytes-and-path rows behave as the kit says (the eight named rows now `StorageFailed` and
kept, every bytes row and the hard link still removed, parity with `ListNames()` before and after), plus the folder and
link-to-folder rows. Eleven mutants red, all undone. Suite 920 failed 0; hosted PASS; the merge with main is clean and
builds and passes 1191, `RULES: clean (370 files)`, `Ran 60`. Scope is the four files; no frozen part changed.
D22 (a) graded **Minor (records)**, with a measurement that narrows it. No Blocker, no Major.

## Findings

| # | Severity | Finding | Recommendation |
|---|---|---|---|
| F1 | Minor (records) | **D22 (a)**: a decryption failure that is not the record's own still reads as "does not open" and the record is removed (`Open`, `LocalSecretStore.cs:827-845`, catches every exception but the store's own and maps it to `UnreadableRecord`). Graded below (section 3). | Records now (README states it; FOR-RECORDS item 2). Before any product caller of `DeleteUnreadable`: the smallest guard in section 3. |
| F2 | Minor (records) | The seat wrote a note into its own assistant memory folder (STATUS, Trees left): outside the project, and outside the kit's closed list of paths outside the clone. No project file is affected. | Records only. |

No text names a person, a ticket or a brief, and none says anyone decided anything (scans below).

## 1. What was re-run at the new head (the kit's FOR TUESDAY items for this reader)

- **The commit, read whole** (`git diff a5ba020b 8578d96c`): the `src` part is byte-equal to the kit's `1-code.diff`
  (`cmp` rc 0). `Judge` has two `try` blocks: an `UnreadableRecord` from `_records.TryRead` is `NotHandedOver`, one from
  `ReadHeader` / `VersionOfOpened` is `DoesNotRead`. `DeleteUnreadable`: id rule first (`InvalidName`), then under the
  lock the disposed check, then `CheckRingUnchanged()`, then the switch (`DoesNotRead` -> the record store's delete,
  `NotHandedOver` -> `StorageFailed`, otherwise false). `ListAll` lists `NotHandedOver` beside `DoesNotRead`. The
  interface summary and the README match the code (round 1's F2 "The key ring is not used." is gone; the false
  sentence "with nothing listed or removed" is replaced by one true of both calls). The test diff: U04 and U14
  changed, U15 to U21 added, each asserting what the kit's table says (U16 accepts either typed reason by design; U21
  finds the lock field by type, writes no lock-field name).
- **G11** (reader's own probe, `evidence/GateProbeTests.cs`): `ListAll` lists good/a unreadable with stated null and
  good/b readable; `DeleteUnreadable(good/a)` `StorageFailed`; after the holder closed: file exists, byte-equal, both
  values read. **Round 1: removed.**
- **G12**: 862 descriptors held under a soft limit of 1024: `ListAll` `StorageFailed`; `DeleteUnreadable(good/a)`
  `KeyNotAvailable` (the ring check meets the fault first, as D17 says); after release the file exists, byte-equal, both
  read; limit restored rc 0. **Round 1: removed.**
- **The rows** (43 by `Row`, each in a fresh root, every call inside a 10 s thread guard): G01 payload bit at 4 places,
  G02 two foreign records, G03 17 kinds of bytes (round 1's 16 plus a file of exactly the size limit, which is read
  and removed), G04 nine rule-breaking names and one planted rule-following name, G05 a good record under another id,
  G06 three clear-version changes, G07 six path shapes. Result: **43 of 43 `RESULT=as-expected`, 0 `UNEXPECTED`**
  (counted by program in `probes-run1.txt` and again in `probes-run2.txt`). The eight rows the kit names end
  `StorageFailed` with the entry kept, the records folder's print (names, kinds, link targets, lengths, modes, SHA-256
  of readable files) equal before and after, the entry listed again with the same id and stated name, `ListNames()`
  still `UnreadableRecord`, both good values read: G03 one byte over the size limit; G07 empty file, mode 000, a link to
  the record moved outside, a dangling link, a named pipe (via `Row`); the link to a folder (not listed, `StorageFailed`,
  link, folder and its file kept, print equal) and the real folder (not listed, `StorageFailed`, kept). Every bytes row
  and the hard link of good/a under another id: `returned True`, nothing unreadable after, both good values read
  (good/a survives the removal of its hard link). Parity with `ListNames()` held before and after on every row.
- **G08**: a readable id false, file byte-equal; an absent id false; 14 ids outside the rule each `InvalidName` with no
  inner; record files 2; both read. **G09** (a caller's record store; round 1's probe error of F4 fixed: a fresh garbage
  record per mode): read `UnauthorizedAccessException` and read `IOException`: `ListAll` and `DeleteUnreadable`
  `StorageFailed`, kept; read throwing `UnreadableRecord`: listed (stated null), removal `StorageFailed`, kept; delete
  throwing: removal `StorageFailed`, kept; listing throwing: `ListAll` `StorageFailed`, the removal (which lists
  nothing) removes the garbage record (true). No message holds a path. **G10**: no text holds a value form; a disposed
  store: `ObjectDisposedException` from both calls, an id outside the rule `InvalidName` first.
- Probe runs: store's test project `total: 102` (89 + 13 probes), `failed: 0`, twice; the probe file was moved out of
  the clone each time (`_quarantine/probe2`, `probe3`), `status --porcelain` 0 lines after.

## 2. Mutants (`evidence/mutants2.py`, one heavy job, store's test project, 89 tests each; each applied to exactly one occurrence, undone by restoring the bytes, proved by `git diff --quiet` rc 0)

| Mutant | Text | RED by assertion |
|---|---|---|
| mOpen | `Judge`: `VersionOfOpened(record)` -> `record.Version` | U02 U03 U04 U06 U09 U13 U14 U18 (8) |
| mHash | `StatedNameOf`: `return name;` | U02 U08 (2) |
| mRecheck (round-2 form) | removal's `_ => false` -> `_ => _records.Delete(recordId)` | U05 (1) |
| mFirst | `ListAll` throws at the first unreadable record | U02 U03 U06 U08 U09 U13 U14 U15 U18 U20 (10) |
| mStorage (round-2 form) | the read's catch also takes `StorageFailed` | U07 (1) |
| mMutable | `SecretInventory` holds raw arrays | U09 (1) |
| mDisposedDelete | removal without its disposed check | U10 (1) |
| mOrder | `Unreadable` reversed | U02 U13 U18 (3) |
| mHanded | `NotHandedOver => _records.Delete(recordId)` | U04 U15 U19 (3) |
| mNoRing | `CheckRingUnchanged();` in the removal removed | U14 U17 U18 (3) |
| mR1 | the removal's `Judge` moved before `lock` | U21 (1) |

Eleven of eleven red, eleven undone (rc 0 each); build errors 0 each; clone `status --porcelain` 0 lines after.
mR1 now reddens U21 (round 1's B1855 F5 closed). U16 is guarded by both the ring check and the arm (the seat's mBoth);
not re-run here.

## 3. D22 (a), graded: Minor (records)

The point: on Windows the ring check does not prove DPAPI-NG can decrypt, so a decryption failure that is not the
record's own reads as a record failure and the record is removed.

What was measured here (G13, macOS, key-file encryptor; `probes-run2.txt`): a store started over a ring of two keys
with a caller key source that fails a decryption while armed. The store made **2 key decryptions at its start and 0
during a later listing, removal and reads** (`DeleteUnreadable` of a readable record under the older key: false; both
records read; a store opened again reads both). Positive control: a store opened while one decryption fails refuses to
start, `KeyNotAvailable`. Source reading agrees: `FullCheck` (at start and after every rotation) calls
`key.CreateEncryptor()` for every key that is not revoked (`LocalSecretStore.cs:624-629`), so the key material is
decrypted, and checked, before the store serves anything. (The first probe run armed on an `Unprotect` frame and never
fired: 0 failures; the second run's trigger, a `KeyFileXmlDecryptor` frame, carries the control. Both are in
`evidence/`; the source file there is the second.)

Why Minor and not Major: (1) Tuesday's ruling 1 counts "does not open/decrypt with the ring" as a record failure, and
the README names this limit in plain words; (2) nothing in the product calls `DeleteUnreadable` (`git grep -E
'DeleteUnreadable|ListAll\(|ISecretStoreInventory' 977cbeb2 -- src tests`: 0 lines; whole tree `DeleteUnreadable`: 0;
control: 12 lines under `src` at the head, `ListNames(` 1 line on main in lane D's session store); (3) the window is
narrow by measurement: a key-decryption fault at the store's start stops the store instead of reaching a removal.
What stays open (DERIVED, not measured): the data protection library re-reading its keys when its key cache expires
in a long-running store (the decryption then happens inside an `Unprotect`, and an exception there becomes
`UnreadableRecord`); DPAPI-NG on Windows itself (not run here); and a process fault inside the decryption (`Open`
catches every exception but the store's own). If a later reader or a caller kit raises it: **the smallest fix** is in
the removal's `DoesNotRead` arm only: when the record parses and names a key id that is active in the verified ring
(`SecretRecord.TryReadKeyId`, `_ring.ActiveKeys`), remove only when the decryption failed as an authentication failure
of the payload (a `CryptographicException` from the library's unprotect), and otherwise refuse with `KeyNotAvailable`;
records under a revoked or unknown key keep today's behaviour (U13). It needs a cell with a key source or protector
that fails at unprotect time.

## 4. Scope, frozen parts, words, scanner

- `evidence/scope2.py` over `git show` of every path: changed since `a5ba020b`: exactly `ISecretStoreInventory.cs`,
  `LocalSecretStore.cs`, `README.md`, `tests/.../InventoryTests.cs` (numstat +8 -3, +21 -4, +33 -10, +506 -11); paths
  295 -> 295, none added or removed. `FileSecretRecordStore.cs`, `ISecretStore.cs`, `ISecretStoreMaintenance.cs`,
  `SecretStoreError.cs`, `SecretStoreException.cs`, `SecretRecord.cs`, `SecretNames.cs` byte-equal to `61b17ec0`;
  `SecretStoreServiceCollectionExtensions.cs` byte-equal to `a5ba020b`; every one of the 71 test files of `61b17ec0`
  byte-equal at the head. The `ListNames()` block (20 lines, 715 bytes, sha256 `5f03bc9753b8c3a8...`): count **1** at
  the head; control (one more space) 0. `NotHandedOver` 4 (head) and 0 (`a5ba020b`); `CheckRingUnchanged();` 4.
- Added lines (568) and the commit message: `_gate` tokens 0; `words.py` `WORDS: clean (2 files)`; non-printable 0.
  gitleaks 8.30.1 (`--no-banner --redact --ignore-gitleaks-allow --exit-code 1`) over both under neutral names: rc 0,
  `no leaks found`; planted control (a token built by program from two halves, never printed): rc 1.

## 5. Suite, merge, hosted

- **Head 8578d96c, through the lock:** locked restore rc 0, 0 lines naming an HTTP source, `status --porcelain` 0;
  build rc 0 `0 Warning(s)` `0 Error(s)` (13 project outputs, dlls fresh and holding `U21_...` and `NotHandedOver`);
  `dotnet test -c Release --no-build`: `Passed!`, `total: 920`, `failed: 0`, `succeeded: 916`, `skipped: 4`.
  `repo_rules.py <clone>` (no `--source-documents`): `R5 hash half NOT RUN`, `RULES: clean (295 files)`; `unittest
  discover -s build/tests`: `Ran 60 tests`, `OK`.
- **The merge with main 977cbeb2:** `git merge-tree --write-tree 977cbeb2 8578d96c` rc 0, clean, tree
  `20c68f4652fc987758cf4b276a9d425091696ac7`, 370 files; against main it changes exactly the lane's five paths. In a
  scratch clone of that tree, through the lock: locked restore rc 0, HTTP lines 0, `status --porcelain` 0; build rc 0
  `0 Warning(s)` `0 Error(s)`; whole suite `Passed!`, **`total: 1191`**, `failed: 0`, `succeeded: 1187`, `skipped: 4`
  (= Tuesday's DERIVED 1170 + 14 + 7). `test ! -e <scratchpad>/1_Project_Definition` rc 0, then `repo_rules.py` (no
  `--source-documents`): `RULES-NOTE: R5 hash half NOT RUN`, **`RULES: clean (370 files)`**, rc 0; `unittest discover
  -s build/tests`: **`Ran 60 tests`**, `OK`; ci.yml `FLOOR=60` (line 192).
- **Hosted run 44892676430 of 8578d96c by GET** (`hosted.py --total 920 --rules 295 --skipped-linux 4 --skipped-windows
  19 --unit 60 --floor 60`): four jobs success, none beside them; linux `total: 920` x2, `succeeded: 916`, `skipped: 4`,
  `GUARD: clean (10 files)`; windows `total: 920` x2, `succeeded: 901`, `skipped: 19`, `GUARD: clean (11 files)`; both
  `0 Warning(s)` `0 Error(s)`; secret-scan both PLANTED-CONTROL lines, `objects of this commit not among them 0`, `no
  leaks found` x3; rules `Ran 60 tests in`, `UNIT-TEST FLOOR: ran 60, floor 60`, `RULES: clean (295 files)`.
  `HOSTED 8578d96c...: PASS`. Control `--total 921`: `FAIL 4`. Windows log: 20 lines with `skipped`, 0 naming
  `Inventory` (control: 6 naming `KeyRingProtection`). Main 977cbeb2's run 44888156989 read the same way with
  `--total 1170 --rules 368`: PASS, the three Analyze rows success; open code-scanning alerts on main 0.

## 6. The seat's deviations

1. U16 runs both calls in ONE guarded thread started before the limit is lowered: **accepted** (measured cause:
   `Thread.Start` throws `OutOfMemoryException` with no descriptor left; the 10 s guard still bounds every call; it was
   red by assertion against HEAD1 and green now; mBoth reddens it).
2. `Fresh` and `Bounded` private -> internal in the lane's own file: **accepted** (no behaviour change).
3. U04's rows split by the `r7 ` label: **accepted** (the kit left the choice; U04 asserts the refusal, the entry, the
   print and `ListNames()` per row).
4. mNoRing's undo proved only together with mBoth: **accepted (records)**; mNoRing was re-made here on its own and
   undone with `git diff --quiet` rc 0.
5. A first `unittest` run with a `-t` option of the seat's own that failed, then the kit's form: **accepted
   (records)**; `Ran 60` measured here too.
6. `mutant.sh` / `undo.sh` wrappers around the unchanged runner: **accepted**.

## 7. Landing texts (in this folder)

`pr-title.txt`, `pr-body.md`, `squash-subject.txt` (ends `(#PRNUM)`), `squash-body.txt` (ends `Co-Authored-By: Claude
Opus 5.5 <noreply@anthropic.com>`), `landing.txt` (the B1858 form: `pr_retrigger.sh --check` against 977cbeb2;
`pr_checks_wait.sh --min-checks 8`; CodeQL analyses on `refs/pull/N/head` at the head's sha first, then alerts 0; the
merge's legs `total: 1191`, `RULES: clean (370 files)`, `Ran 60`, floor 60; head-pinned squash; after-merge reads with
`fleet/state/s304/d1835/gate/hosted.py --total 1191 --rules 370 --unit 60 --floor 60`, sha256 `e73339f3...`; MAIN
MOVES AGAIN), `FOR-RECORDS.md`. `evidence/texts.py` exported each text through the workflow's own `neutral_export`
(cut from ci.yml at the head, lines 120 to 128) as the commit message of a scratch repository and scanned it with the
workflow's options: title, title and body, body, squash message with a number and as written, squash body, the
default squash shape over both commit messages, landing.txt: each rc 0 `no leaks found`, message stored whole; the
planted control: rc 1, `leaks found: 2`. Word counts: the four repository texts 0 in every class but one host match in
squash-body.txt (the attribution line's address), non-ASCII 0; `words.py` over the four: `WORDS: clean (4 files)`;
landing.txt (Tuesday's own form, not a repository text) holds B-numbers and the word gate by design. Word controls 16
of 16 fired. **Landing happens only when reader B1865 is also GO or GO WITH FINDINGS.**

## 8. What was NOT tested

- Linux and Windows locally (macOS arm64 only): the hosted legs ran the lane's cells, not this reader's probes;
  DPAPI-NG itself and a library key-cache refresh (D22 (a)'s open part) are DERIVED; `EIO` and `ENFILE` not run.
- P01 to P11, the free race, and the second-process race (reader B1865's).
- The pull request's merge-ref run and CodeQL (no pull request exists; C# CodeQL cannot extract on this machine).
- The two publishes and the release guard locally (the hosted GUARD lines were read instead).
- The README limit "in a store started after a key entry was moved out of `keys/`, every record under that key" is
  removed: read from source and the kit, no probe of mine.
- The seat's mBoth, mFalse, mListDrop and mSwallow as written (eleven mutants of this reader's were run instead).
