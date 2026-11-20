GATE B1824: GO WITH FINDINGS @ bf1a4a2 on main c56f3f3

Gate G1 Tier 1, round 2 of 2 (the last), OXPd 2, WP1.1 the local secret store: the fix round at head
`bf1a4a24492f7849705e48cbc1d4938e15f30c56` (one commit on the round-1 head `42f926d51082c67b6c87a521d9234836a7c9525e`), on
main `c56f3f3b015fae8d47288aa9d6c636ecd8fe2191`. Read and measured 2026-11-21, 09:19 to 09:45 AEDT (clocks by `date`), in the
gate's own clone `/private/tmp/b1824-gate/clone` (push URL `invalid://no-push`), on Opus 5.5 (the commission's model).
Every number below was printed by a program; programs and logs are under `/private/tmp/b1824-gate/` (`scratch/`, `logs/`,
`out/`, `probes/`, `api/`). Every heavy job (restore, build, test, each attack-program run, each mutant: 183 jobs) took the
wave's lock `<project>/.tools/wave1-heavy.lock.d` by `mkdir` with an `owner.txt`, ran alone, and released it by a move into
`/private/tmp/b1824-gate/_quarantine/locks/` (183 folders there; the lock is not held now); each started only with load1
under 7 (the highest load1 read: 2.65). No key value, ring entry or secret value is in this file or was printed; every key and
store the gate made is a throwaway under its scratch.

**BLUF.** Both findings the round-1 verdict asked to be closed are CLOSED by the gate's own runs: the four RUNNING rows now
refuse every write and key operation and write nothing; the emptied ring and every-key-removed ring refuse to start and make
no key; the linked keys folder is refused; an unprotected planted key is refused at a start and under a running store, no
value is ever written under it, so a reader holding only the planted file has nothing to open. The same-round Minors (3, 4,
6, 7, 8, 9, 13, 15) are closed or named as the kit worded them. The review's 37 mutants and the builder's 16: 50 apply, 50
killed; 3 texts are gone (K06, g14, g16), each as the builder says. Scope, texts and author identity are clean. **No Blocker
and no Major.** Eight Minors, none a reason not to merge; the first is the one to read: **on Windows the store cannot tell
a key it made from a key anyone else protected with DPAPI-NG to a rule its account can open** (DERIVED; the class summary
claims more than Windows can give; the folder's access list is the only guard and the README does not say so). **The head
cannot land as it is:** main moved, and a three-way merge conflicts in `Datasec.Suite.slnx`; one more commit, touching that
file only, is needed and is a head this gate did not read (landing.txt gives the exact bytes it must hold and the check).
The server does not use the store: nothing here protects a value of the server today.

## Findings

| # | Severity | Blocks the merge? | Finding | Recommendation |
|---|---|---|---|---|
| N1 | Minor (text owed; the first to read) | No | **Windows: a planted key protected with DPAPI-NG is accepted.** The entry rule asks, on Windows, that the protected element names `DpapiNGXmlDecryptor` and opens (`LocalSecretStore.cs:474`, `:517`); the key-source rule (f) returns true on Windows (`:593-596`). DPAPI-NG protection needs no secret of the store: anyone may protect to a rule (for a `SID=` rule any domain principal, for `LOCAL=machine` any local account), and the store compares no rule. So whoever can write `keys/` can plant a key whose master key they made, protected to a rule the store's account opens; the store accepts it at its next start and, if its activation is the newest, seals later writes under it, which the planter can read. UNMEASURED on Windows by the gate (no Windows machine); the hosted leg shows the acceptance half: M07 and M12 ran and passed on Windows (not among its 19 skipped lines), and each starts a store over a key made by ANOTHER provider instance with DPAPI-NG (`RingKit.Provider`, `ControlTests.cs:115`, `:185`). Not in the kit's tables (table RING row 6 is "not on Windows"); round 1 proposed exactly the decryptor-naming check for Windows, which is what was built. The README names "the access control lists of the root folder are not set" but not what follows from it, and the `LocalSecretStore` summary ("protected by its own key source") and README line 19 read as if Windows were covered. No code inside this framework closes it (DPAPI-NG does not authenticate who protected an entry). | One README Limits sentence and the class summary's "where this stops", at the latest with the host wiring: "On Windows, anyone who can write the key folder can plant a key the store accepts and then uses; the folder's access list is the only guard." The installer sets an owner-only list on the root. A backlog line: compare each entry's protection rule with the configured one (narrows, does not close). |
| N2 | Minor (text) | No | **"none throws after its write succeeded" (README line 34, the kit's D10) is untrue for `RotateKey` in one case.** Measured (`logs/probe3.log`): over the M07 ring (a key of the store's own protection whose activation is 3 minutes ahead), `RotateKey` writes its new key and then throws `KeyNotAvailable` (its post-check, `:253-256`): ring files 2 -> 3; the same store's next `Put` returns 1. Fails closed for values (nothing is sealed under an unverified key); an operator who retries adds a key each time. | Say it in the README ("RotateKey can leave its new key in the ring when it refuses afterwards"), or check `CurrentKeyId` would change before `CreateNewKey`. Records. |
| N3 | Minor (records) | No | **The PARTITION folder may be a link** (the kit's D6 covers the key and record folders and lets the root be one). Measured (`logs/probe2.log` P1): `<root>/p1` a link to a folder OUTSIDE the root of mode 755: the store starts, writes 4 entries there and sets that folder's mode to 700 (`OwnerOnly.CreateFolder` follows the link, `OwnerOnly.cs:20-21`); a link to `p2` of the same root: starts, `p2`'s records do not read under p1 and what p1 writes does not read under p2 (no value crosses). The round-1 finding 6 class (a mode changed outside the root), for a folder. | README sentence, or refuse a partition folder that is a link at the start (two lines, as for the key folder). |
| N4 | Minor (records) | No | **A HARD link in `keys/` has its target's mode changed.** Measured (P4): a hard link named `notes.txt` to a file outside the root of mode 644: the start sets it to 600 (`TightenFiles`, `OwnerOnly.cs:35-46`: a hard link is a regular file). The README says only that `TightenFiles` skips links. This framework exposes no link count. | README sentence ("a hard link in the key folder is tightened like any file"). |
| N5 | Minor (records) | No | **The record folder is link-checked at the start only.** Measured (P6): replaced by a link to an outside folder under a running store, `Put` writes its record there (1 file) and reads it back; the record written before is absent; a new start refuses (`StorageFailed`). Ciphertext only, no value crosses; not in the kit's tables (R10 is at a start). | README sentence; or the light check also asks that the record folder is not a link. |
| N6 | Minor (records) | No | **A copy of the store's own entry under a new key id becomes the write key at the next start, with a cipher the copier chose.** Measured (P2): the entry cloned with a new id, the newest activation and `algorithm="AES_128_CBC"` (and, as a control, `AES_256_CBC`): under a running store `Put` is refused (the light check); at the next start the store STARTS and seals the next value under the clone's id; values read; `Rewrap` moves every record under it. The master key stays the store's secret, so nothing reads that should not. The README's "an entry is not bound to the id of the key it wraps" is the mechanism; the consequence (who can write `keys/` chooses the write key and, from the library's set, its algorithm) is not said. | One README sentence. Records. |
| N7 | Minor (cells) | No | **Seven of the gate's 20 new mutants of round-2 code leave all 69 tests green, two of them on stated behaviour** (`logs/mutants-own.out`; the code holds in each case, measured by the gate's probes): n6, a ring holding a revocation alone with no record counts as an empty partition and gets a key (the README says it is refused; P8: refused, files 1 -> 1, so the code is right, no cell can fail); n13, the guard of `RevokeOlderKeys` reads only the first record (G01's five records are all under the older key; P9: with 7 of 8 records re-put and the LAST by file id still old, the real guard refuses and the record reads). The others are pairs or are behind another rule: n7 and n8 (the two link checks of the key folder back each other), n4 and n18 (the builder's key-set rule and the duplicate-id rule back each other), n5, n16, n17 (behind the opens rule and the master-key rule); and three need concurrency or a crash to show: n9 (the light check per record of `Rewrap`), n11 (the length re-check after an open), n14 (the repository's temporary file and move). | Two cells: a revocation alone with no record refuses (n6); the guard with a mixed set of records (n13). The rest: records. |
| N8 | Minor (records) | No | **A ring made by the round-1 head carries keys of 90 days.** With generation now off, a ring whose only key passed its end date refuses every write (the gate's spike g3: one key past its end, generation off: protect throws). Measured (`logs/compat-*.log`): a store written by the round-1 head starts, reads, writes and rotates at the new head. No such store exists (the host does not use the store). | Records only. |

## 1. The round-1 findings, closed or not (the gate's own run)

The round-1 attack program (`probes/Attack/Program.cs`, copied from the kept copy, `cmp` equal, sha256 `f50ce4da...` as its
manifest) built unchanged against the new head (rc 0, 0 warnings, 0 errors: every public signature it uses is kept) and run in
all thirteen modes, each as one locked job with a 300 s bound, working folder the gate's `stores/`: `running`, `misc`,
`records`, `keyfile`, `fifo`, `refresh` (63 s), `names`, `two` (6 s), `crash`, `algo` rc 0; `keyring`, `ops`, `big` stop
(rc -6, an unhandled exception in the PROGRAM), at exactly the three lines the builder names. Also `refresh control`
(63 s): equal to round 1's control line.

**The three stops, proved by the gate's own guarded copy** (`probes/AttackGuarded/Program.cs`: the three statements guarded
and a gate block added; the gate's own text, not the builder's copy):
- `Program.cs:286` (`keyring`): the stop is `FileNotFoundException` in the program's own read of the record `fresh`; the line
  before it reads `KEYRING an UNPROTECTED key planted ...: typed:KeyNotAvailable | key files 3 -> 3; files under the partition
  5 -> 5`. So the start over the planted key was refused and wrote nothing; there is no value written after the plant for a
  reader of the planted file to open. The gate's added rows plant the same unprotected key under a RUNNING store (twice):
  `put typed:KeyNotAvailable; RotateKey typed:KeyNotAvailable; Rewrap typed:KeyNotAvailable; RevokeOlderKeys(true)
  typed:KeyNotAvailable; read before the value; files under the partition 3 -> 3; record fresh2 written False`; with the
  planted file moved out again the same store writes (`put 1`).
- `Program.cs:617` (`ops`): `SecretStoreException` with reason `RecordsUnderOlderKeys` from `RevokeOlderKeys()`; guarded:
  `typed:RecordsUnderOlderKeys; revocation files 0`; the program then goes on with `RevokeOlderKeys(true)` so its round-1 row
  can be laid beside: `revoked 1; reads typed:UnreadableRecord x5; rewrap read 5 rewritten 0 failed 5` (as round 1), `list`,
  `put over one` and its read now `typed:UnreadableRecord` (D11 opens what it trusts).
- `Program.cs:531` (`big`): `FileNotFoundException` in the program's own `FileInfo` of the record `bigvalue`; guarded: `put
  typed:ValueTooLarge; read absent; record file none`. The gate's boundary rows: 1048575 bytes `put 1`, record 1398273 bytes;
  1048576 bytes `put 1`, value reads, record 1398293 bytes; 1048577 bytes `typed:ValueTooLarge`, no file.

**Rows beside round 1** (`scratch/compare.py`, `out/rows.txt`; each line keyed by its label; times, GUIDs and allocations
masked; `LEAK-SCAN` lines left out): 131 lines equal, 54 differ, 9 only now (the gate's guard rows). Every differing line is
named here:

| Round-1 finding | Rows | Round 1 at 42f926d | Gate at bf1a4a2 | Closed? |
|---|---|---|---|---|
| 1, the four RUNNING rows | `running` 4 | `put after 1` in 4 of 4; `RotateKey` a new key in 3 of 4; a new store starts in 3 | `put after typed:KeyNotAvailable` 4 of 4; `RotateKey`, `put`, `rewrap`, `revoke` each `typed:KeyNotAvailable`; key files unchanged (1 -> 1; 1 -> 0 where the file was removed, then 0 -> 0); `read before value#0`; a new store `typed:KeyNotAvailable` | CLOSED |
| 1 (c), the emptied ring | `KEYRING EVERY key removed`; `the whole keys folder emptied` | STARTED, key files 0 -> 1 | `typed:KeyNotAvailable`, key files 0 -> 0, files 2 -> 2 | CLOSED |
| 1 (c), the revoked current key | `the current key revoked through the library`; `every key revoked` | STARTED, key files 2 -> 3 (a key made) | STARTED, key files 2 -> 2 (no key made; writes under the older key); every key revoked: `put typed:KeyNotAvailable`, files 5 -> 5 | CLOSED by the property; the start is the README's named limit, true |
| 1 (c), the linked keys folder | `keys folder replaced by a LINK` | STARTED, a write | `typed:KeyNotAvailable`, files 3 -> 3 | CLOSED |
| 1 (d), the key source switched | `misc KEY SOURCE` | `put b 1`, `RotateKey` a key | `put b`, `RotateKey`, `put c` each `typed:KeyNotAvailable`, key files 1 -> 1 | CLOSED |
| 1, the library's re-read | `refresh` | 12 writes under a broken ring | `put after typed:KeyNotAvailable` (the program's own 12 reads of the never-written record print a file error) | CLOSED (D3) |
| 2, the planted unprotected key | `KEYRING an UNPROTECTED key planted` + `PLANTED KEY` | STARTED; sealed under the planted key: True; the planted file alone opened THE VALUE | `typed:KeyNotAvailable`, files 5 -> 5; nothing sealed under it at a start or under a running store | CLOSED (both legs: R04, R05, R08 ran on Windows; the Windows variant N1 is new) |
| 6 | `misc LINK`, `LINK dangling`, `READ-ONLY`; `records LINK`x2, `FOLDER`, `MODE 000`; `fifo` 6; `big` 3 GiB; keys folder a FILE | outside mode 600; raw errors with a path; hangs over 5 s | outside mode 644; dangling link `put 1`; read-only `typed:StorageFailed`; every record row `typed:UnreadableRecord`; every pipe row at once (no hang); keys folder a file `typed:StorageFailed` | CLOSED; the pipe swapped in after the look is the README's named limit |
| 3 | `records PLANTED record`, `PLANTED version`, `CHOSEN KEY ID` | listed; version 2147483647 taken | `list typed:UnreadableRecord`; `put typed:UnreadableRecord`; rollback rows equal to round 1 (named limits L01 to L03, true) | CLOSED as the kit worded it |
| 11 (one sentence) | `two`, a rotates while b runs | `b.Put returns 1`, read by nobody | `b.Put returns typed:KeyNotAvailable` | as the kit worded it |
| 7 | `keyfile` 42 of 43 equal | race 1,423 of 582,229 through the link | race 439 of 547,153 through the link | NAMED (README, true) |
| D6 (b), counted | `OPS 20 rotations` | key files 20, revoke 19 | 21, 20 (the first key now made at the first start) | as built |
| the builder's row 19 | `UNREADABLE entry ... mode 000` x2 | refused | STARTED, both values read (the start tightens `keys/` before it reads) | meets the property (the builder's row 19) |
| finding 10 (records) | `algo` | lifetime 90 days | lifetime 36500 days; AES_256_CBC + HMACSHA256 unchanged | D2 |

**Mutants.** The review's 53 texts (`scratch/mutants.py`, its own `rep()`, a mutant tree, each built and tested under the
lock, the file restored; after the last undo 0 files differ from the clone): **50 apply, 50 KILLED, 0 survived, 0 build
failures**; 3 no longer apply (text count 0): K06 (`PersistKeysToFileSystem`, removed by D3), g14 (the old start check),
g16 (the late wrapper, gone). The 17 round-1 survivors: g1, g4 (M02), g7, g7b (M01), g9, g10 (M03), g11 (M03, M04), g13 (F10),
g17 (M07), g19, g20 (F03), g22c (M09), g28, g28b (M10), g30 (F07, M11), g31 (M12): each KILLED, the same cells as the STATUS
lists; g16 gone. The suite at the head in the gate's clone: locked restore rc 0 (0 lock files changed), build `0 Warning(s)`,
`0 Error(s)`, test `total: 69`, `failed: 0`, `succeeded: 65`, `skipped: 4` (K06-Windows, K07-Windows, W01, W02). The gate's
own 20 mutants of round-2 code: 13 killed, 7 survived (N7).

**Item 9, Windows.** The hosted `windows` log of run `44827089866` (read by GET with `--allow-escape-sequences`, rc asserted,
the runner's echo of each step left out; `scratch/hosted2.py`, `api/`): `total: 69`, `failed: 0`, `succeeded: 50`,
`skipped: 19`; 19 skipped by name: the 18 Unix-only tests with the Unix-only reason, and `W01_...` with its reason `The
default DPAPI-NG descriptor was refused on this machine.` **THE WINDOWS ANSWER, confirmed: the product default was refused
on the hosted runner; W01 asserted that nothing was written before it skipped (`failed: 0`).** R04, R05, R08 (and W02, R14)
are not among the skipped lines (positive control: W01 is found, K01 is not): they ran and passed there. Linux: `total: 69`,
`failed: 0`, `succeeded: 65`, `skipped: 4` (the four Windows-only tests by name). `rules`: `Ran 53 tests`, `UNIT-TEST FLOOR`,
`RULES: clean (64 files)`. `secret-scan`: both planted-control lines, the `NEUTRAL-SCAN` line, `no leaks found` 3. Control
line `NO-SUCH-LINE-CONTROL`: 0 in each log. Every count equals the STATUS's HOSTED RUN.

## 2. What the fix changed that round 1 never saw

Read whole by the gate at the head: `LocalSecretStore.cs` (898 lines), `KeyRingRepository.cs`, `FileSecretRecordStore.cs`,
`OwnerOnly.cs`, `SecretRecord.cs` diff, the interface, error, exception and options diffs, the README (168 lines), and the
test cells R04, R05, R08, R01's helper, M07, `RingKit.Provider`.

**D1 to D6 as built.** D1 `DisableAutomaticKeyGeneration()` (`:667`). D2 `NewKeyLifetime` 36500 days (`:671`), used by the
first key (`:450-452`) and `RotateKey` (`:236-245`). D3 `KeyRingRepository` set as `XmlRepository` (`:670`), no
`PersistKeysToFileSystem` (text count 0). D4 `ReadRing` + `RingEntry.Parse` + `FullCheck` (`:465-541`, `:803-851`). D5
`CheckRingUnchanged` before each `Put` write (`:144`) and per record of `Rewrap` (`:275`). D6 `PrepareFolders` + `Start`
(`:392-443`). Each as the STATUS's FOR TUESDAY describes.

**D2, ruled sound.** The gate's own spike (`probes/Spike`, `logs/spike.log`, the framework alone): g1 generation off, empty
folder: protect THROWS, 0 files (control, generation on: protects, 1 file); g2 one key made now to +36500 days, generation
off: protects under it, and a provider built anew protects under the same key, expiration year 2126; g3 one key past its end
date, generation off: protect THROWS (control, generation on: a new key, 2 files); g4 TWO keys both past their end date,
generation off: protects under one of them; g5 one key ending inside the library's two-day window: protects, no key made. So
a store that never rotates goes on writing for the lifetime; with generation off a single expired key would stop writes,
which is why D2 is forced; and g4 shows an end date was never a guarantee that a key stops being used. The lifetime itself is
a product question (master list), decided by nobody.

**D3, ruled sound, attacked.** The library sees only the repository's elements (copies of the verified snapshot,
`KeyRingRepository.cs:23-36`). A file planted after the start is not served (P7 by reflection: served 2 = 1 built + 1
written, with `key-planted.xml` in the folder) and stops the next write (P5b: a copy of its own entry planted as
`KEY-COPY.XML` under a running store: `put typed:KeyNotAvailable`; a non-`.xml` file: `put 1`). A name the repository refuses
(`../escape`, `a/b`, empty, `x.y`, 101 characters) throws `ArgumentException` inside it and writes nothing (P7: files 2,
leftover `.writing` 0, the folder above unchanged); the library's own names pass, and inside the store any such throw is typed
`KeyNotAvailable` by the catch around `CreateNewKey` (`:247-250`). A leftover `.writing` file is not a ring entry (P5a: start,
write, read). A move onto an open file: the repository moves to a fresh GUID name with `overwrite: false` (`:61`), so its
target never exists; a record replaced while a reader holds the old file keeps the reader's old bytes on Unix (M11, killed
g30); on Windows UNMEASURED (M11 is Unix-only), and any failure there is typed `StorageFailed` by the record-store wrapper.
The keys folder swapped for a link at the moment of a write: the new entry (encrypted) lands in the link's target and the
rebuild then refuses (`ReadRing`'s link test, `:469`): fail closed.

**D4 and D5.** The one read per entry feeds both the hash of the light check and the element handed to the library, so the
library uses exactly the bytes that were checked. What the property rests on is the snapshot, not the disk; the light check is
the tripwire, and its README limit (a change between the check and the write is seen at the next write) is true.

**The builder's choices, FOR TUESDAY item 4 (a) to (g).** Public surface by reflection over the built head and new head
(`probes/Api`, `logs/api.log`; the tool lists additions, the control): exactly six rows added, the five of Q11 and the
interface method's implementation on `LocalSecretStore`; 0 removed; `InternalsVisibleTo` unchanged. Stored form: the record
encoding is unchanged; a ring and record written by the round-1 head start, read, write and rotate at the new head
(`logs/compat-*.log`); the repository writes entries without indentation (whitespace only).
- (a) a key folder that is a FILE gives `StorageFailed` (R10; measured `keyring` row): typed, nothing written: keep.
- (b) a folder at a record's path is not listed: `TryGet` and `Put` give `UnreadableRecord`, `Delete` false (measured
  `records FOLDER`): it holds no value: keep, and the README says it.
- (c) the library must know exactly the ring's key ids: stricter, fail closed; it has no cell of its own (n4; backed by the
  duplicate-id rule, n18): keep.
- (d) the key source's key must carry the protecting id: stricter (n3 killed by R09): keep.
- (e) `ListNames` refuses a listed record whose name breaks the rule (F10, killed g13): keep.
- (f) the repository's name rule (P7): keep.
- (g) `Delete` removes a link at a record's path, never a folder (`FileSecretRecordStore.cs:69-80`; n20 killed by F04): keep.
Each fails closed, changes no stored form, adds no public member.

**The value limit (F08).** `Put` refuses a value longer than 1048576 bytes with `ValueTooLarge` before anything is read or
written (`:119-122`; measured boundary in section 1); a record file is read only up to 2 MiB + 4096 bytes (n12 killed by F04;
the 3 GiB and 300 MiB sparse rows: `typed:UnreadableRecord`, 0 MiB allocated). It refuses nothing a caller has today (no
caller exists).

**The guard on `RevokeOlderKeys`** (`:312-353`, `:614-643`): reads every record's key id after its header check
(`SecretRecord.KeyId`, header `09 F0 C9 F0`); a record that cannot be parsed does not block; the overload revokes anyway.
Measured: OPS guard row and P9 (one old record, the last by file id, among 7 re-put: refused, the record reads). Sound; its
cell owes the mixed case (N7).

**The README's new text, each sentence against the code.** Read sentence by sentence; true at the head but for: line 34's
"none throws after its write succeeded" (N2); lines 19 and 30 with the class summary, read for Windows (N1). The Limits
section's 23 bullets: each true as measured or as read (the key-file window, the pipe swapped in, rollback, `Delete` then
`Put`, the revoked rings, swapped parts, another root, 1 MiB, `ListNames`' cost, no end by time, the host). Unsaid: N3, N4,
N5, N6.

**THE REQUIRED QUESTION: what can change under the root between a check and its use, or be other than the file the store
wrote, that is NOT a row of the kit's tables RING and THE SECOND QUESTION (19 rows)?** The gate's own answers, each measured
by `probes/Probe2` (`logs/probe2.log`) unless marked:

| # | The thing | Outcome | Ruling |
|---|---|---|---|
| Q1 | a key planted on Windows, protected with DPAPI-NG to a rule the account opens | accepted (DERIVED; acceptance of a key made by another provider instance shown by M07, M12 on the hosted Windows leg) | finding N1 |
| Q2 | the PARTITION folder a link (outside the root; to another partition) | starts; outside folder chmod 755 -> 700 and written; no value crosses | finding N3 |
| Q3 | a HARD link in `keys/` to an outside file | its mode 644 -> 600 | finding N4 |
| Q4 | the record folder swapped for a link under a running store | writes go there until the next start, which refuses | finding N5 |
| Q5 | a clone of the store's own entry, new id, newest date, chosen algorithm | at the next start the write key, under the chosen cipher | finding N6 (mechanism named) |
| Q6 | the clear dates of the store's own entries edited before a start | the older key's activation moved to now: writes stay under the newer key; every expiration in the past: starts, reads, writes, rotates (g4 above) | closed (denial at most) |
| Q7 | `RotateKey` refusing after its write | the new key stays in the ring | finding N2 |
| Q8 | an upper-case `.XML` entry; a folder named `key-folder.xml` | refused at a start and under a running store | closed |
| Q9 | a revocation alone and no record | refused, no key made (P8) | closed; no cell (N7) |
| Q10 | a ring left by the round-1 head (90-day keys) | works now; a single expired key would stop writes | finding N8 |

## 3. Scope and the texts

`scratch/scan3.py` over the clone: `diff --name-status 42f926d5..bf1a4a24`: 22 rows (A 9, M 13), outside the lane's two
folders and the solution file 0 (control: a planted `M Directory.Packages.props` row is reported); numstat of the solution file
`1 1`; the solution file at the head is byte-equal to block SLNX extracted from the stamped kit by program (501 bytes, sha256
`147fe7ac3781da14...`; control: one more space differs); binary rows 0; new file modes all 100644. Unchanged against the
round-1 head: `Directory.Packages.props`, `Directory.Build.props`, `.github/workflows/ci.yml`, the root `README.md`,
`global.json`, `NuGet.config`, both project files, both lock files. **Texts:** over the 2,155 added lines: ban-list names 0,
B-numbers, seat ids, ticket keys and clarification ids 0, "product owner", "coordinator", decided, ruled, approved, review,
finding, round, gate, kit, card 0, bytes outside printable ASCII 0 (underscore-aware patterns; control line `_by_Kamil_ B1811
X11 OXPD2-3 product owner decided` plus a non-ASCII byte fires in every class). The commit message: subject `Check the key ring
at every use and close the file checks of the local secret store (WP1.1)`, body the one line `Co-Authored-By: Claude Opus
5.5 <noreply@anthropic.com>`: the model the commit was made on; the only name-class hits are that line's own "Claude" and
"Opus". The STATUS says the first seat ran on Fable until it stopped and the successor on Opus 5.5 (its Step 0 (successor),
DEVIATIONS 10). **Author and committer** of both branch commits: name and e-mail equal to the project checkout's own
repository-local `user.name` and `user.email` (compared in-process, not printed). Repository controls at the head: `Ran 53
tests`, `OK`; `RULES: clean (64 files)` (= `ls-files` 64); the secret scanner over both lane folders `no leaks found` (control
folder with a planted value: rc 1).

## 4. The moved main

`git merge-tree --write-tree` of main `c56f3f3b` and the head, in the gate's scratch clone (a bare clone in the session
scratchpad): **CONFLICT in `Datasec.Suite.slnx`, two hunks** (the Logging and Secrets lines of each Folder block); every
other path merges clean (39 files, 4,635 lines added against main). **The branch needs a new commit to merge: a head this gate
did not read. The gate made no commit.** landing.txt step 0 gives what the solution file must read by ordinal order of the
Path values on main as it is (13 lines, 671 bytes, sha256 `a564e918...`; equal to main's file plus exactly the two Secrets
lines, by program), after the print lane (15 lines, `caa4af8a...`), and after the print lane and the card decoders (17
lines, `a94ad1ac...`, byte-equal to the round-1 review's file of all four lanes). For the first case the gate built it: main
merged with this head and the file set to it: locked restore rc 0, build `0 Warning(s)` `0 Error(s)`, test `total: 260`,
`failed: 0`, `succeeded: 256`, `skipped: 4`; main alone `total: 192`, `failed: 0` (the lane adds 68). For the other lanes:
the print branch `ec75619e` against main also conflicts in the solution file (its own resolution is in flight); the cards
branch `9fe53569` merges clean (pull request 3 reads mergeable, clean).

## 5. Code scanning: NOT RUN

`CodeQL csharp: NOT RUN (cannot extract on arm64); hosted CodeQL is the only C# proof.` No scan has run on this branch.
From a reading of the query pack on this machine (`csharp-all` 7.4.2, `SensitiveActions.qll` lines 32 to 56): the clear-text
storage and logging queries take their sources from names matching `%password%`, `%passwd%`, `%account%id%`,
`%account%key%`, `%license%key%`, `%voucher%code%`, `%trusted%` (not `secret`, `key` or `token` alone). Over the 2,155
added lines of the 22 files such a name occurs once, inside an XML comment ("current account SID",
`LocalSecretStoreOptions.cs`), which no query reads (control: the round-1 head's test file holds its one such literal). No
logger is called; the file writes write ciphertext records, XML entries and test fixtures, none from a sensitive name. The new
XML read sets `DtdProcessing.Prohibit` and no resolver (`:807`) over a local file, so the insecure-XML query has neither a
weak setting nor a remote source; no path comes from a remote source. **Likely: 0 alerts.** The round-1 trap stands for the
host lane: a member named with a password word reaching a logger or a file write.

## 6. The landing texts

In this folder: `pr-title.txt`, `pr-body.md` (ends with the footer line), `squash-subject.txt` (ends `(#PRNUM)`),
`squash-body.txt` (ends with the one attribution line `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`; longest line
69), `landing.txt` (the reviewed head pinned for the delta check; the resolution commit and the file it must hold; the wait
for at least 8 ci rows plus the code-scanning rows, measured on pull request 2: 11 rows; the squash line with both text files,
`--match-head-commit <NEW_HEAD>`; what to read on main after; that a merge deploys nothing). Each text exported through the
workflow's own `neutral_export` (cut by program from the head's `ci.yml`, lines 120 to 128) as the message of a commit in a
scratch repository and scanned with the workflow's options, scanner 8.30.1 (`scratch/texts.py`, `logs/texts2.out`): the
title alone, title + body, body alone, the squash message with a number, as written, the body alone, the repository's default
squash shape, and landing.txt: each `rc 0, no leaks found`, history pass rc 0, stored whole; CONTROL, the squash message with
the workflow's planted value: `rc 1, leaks found: 2`. Texts flagged: 0. In the four texts: names, B-numbers, clarification
ids, ticket keys, seat ids, "product owner", finding or round numbers, words of deciding, card ids, control numbers, hosts
or GUIDs: 0 each; bytes outside ASCII apart from the footer: 0 (control line fires each pattern). FOR-RECORDS.md lists what a
records pass files.

## Graded claims of the STATUS

True as measured: one commit, fast-forward, 22 paths, block SLNX; 69 tests, 65 passed, 4 skipped here; the hosted counts of
all four jobs and THE WINDOWS ANSWER; R04, R05, R08 ran on Windows; the 50 applicable review mutants killed and the three
texts gone; the three stops of the unchanged program and their causes; the spike's D1 to D3 rows (the gate's g1 to g3 agree);
every builder choice (a) to (g) as described; the five public members; the author identity; the cost rows of `MANY 2000
records` in shape (the gate: put 8,005 ms, list 2,003 in 85 ms, re-wrap 8,074 ms, one run on a shared machine). Inexact: none
found among its measured claims. Not shown by the gate: its RED FIRST run on the head and its own mutants mR1 to mG1 (the
gate ran its own instead), its predictions file. Its NOT RUN list is honest; the gate ran the five modes it did not
(`refresh`, `names`, `two`, `crash`, `algo`): each above.

## FOUND / TESTED / NOT TESTED

- FOUND: round-1 findings 1 and 2 closed; the same-round Minors closed or named; 8 new Minors (N1 to N8), none blocking; the
  branch needs a resolution commit to merge.
- TESTED: everything in the tables above, in the gate's own clone and scratch, with the project's SDK 10.0.404 and the
  gate's own home and package cache; every heavy job under the wave's lock.
- NOT TESTED / NOT RUN:
  - **Windows, anything, locally.** N1 is DERIVED from DPAPI-NG's documented model and the code; the hosted leg is the only
    Windows run. A move onto an open file on Windows, and `Delete` of a directory link on Windows: UNMEASURED.
  - The resolution commit (it does not exist); the merged solution for the print and cards cases (by rule only).
  - CodeQL for C# (cannot extract here; a reading of the queries only).
  - A crash inside the repository's write or the record store's write; a full disk; `RevokeOlderKeys` failing midway;
    two processes racing a rotation beyond the `two` mode; the library's real daily re-read (D3 removes it from the path).
  - A key file owned by another account; the store run as root.
  - A second reader (not asked by this commission).
  - Known-vulnerability status of the framework (no request to any advisory service).
- Slips of the gate's own, said plainly: one `sed -i ''` with a substitution that changed nothing, on the gate's own scratch
  copy of a project file (`probes/AttackGuarded/Attack.csproj`); two Bash calls refused by the workspace's hooks (a `cd`; git
  write verbs in a folder outside the session scratchpad) and re-issued in the allowed form. Nothing was written outside
  `/private/tmp/b1824-gate/`, the session scratchpad and this folder; the wave's lock folder was made and moved 183 times.

Files in this folder: VERDICT.md, FOR-RECORDS.md, pr-title.txt, pr-body.md, squash-subject.txt, squash-body.txt, landing.txt.
