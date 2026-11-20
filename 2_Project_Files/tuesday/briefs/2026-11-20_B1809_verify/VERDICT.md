GATE B1809: NO GO @ 42f926d on main 7bf3752

Gate G1 Tier 1, round 1 of 2, OXPd 2, WP1.1 cut to the local secret store (kit B1789, seat X7). Head
`42f926d51082c67b6c87a521d9234836a7c9525e` on main `7bf375268b9975ac9ece66579f7471ba7dbab11d`. Read and measured 2026-11-20,
20:22 to 20:55 AEDT (clocks by `date`), in the gate's own clone `/private/tmp/b1809-gate/clone` (push URL `invalid://no-push`).
Every number below was printed by a program; the programs and their logs are under `/private/tmp/b1809-gate/` (`scratch/`,
`logs/`, `probes/Attack/`, `stores/`). No key, value or token is in this file; every key the gate made is a throwaway there.

**BLUF.** One Blocker by the commission's own rule for item 3 and one Major, so NO GO and a fix round. Both are in the key
ring, not in the values. **No test of the gate returned a value that was not put under that name and partition, and no value
or key reached a file, an exception text or a log (over 1,000 hostile record files, 39 key-ring cases, 1,942 concurrent writes; 400 files and 1,339 exception texts scanned).**
What is wrong: (1) the store goes on working after its key ring can no longer be read, in every case but the one the builder
fixed (a start over a ring that holds an entry it cannot open); (2) **a key planted in the key folder with no protection at
all is accepted and used: the next write was sealed under it and was then read by a reader that held only the planted file
and the record, without the key file.** The second reader found (2); the first reader did not. Everything the builder
claims as measured was reproduced: scope, the two frozen lines, 26 tests, the sixteen mutants, the hosted lines, the
published counts. **The server does not use the store: nothing here can do harm today. It is about what the host lane would
build on.**

## Findings

| # | Severity | Blocks the merge? | Finding | Recommendation |
|---|---|---|---|---|
| 1 | **Blocker by the commission's rule (item 3: "a store that keeps working after its key ring can no longer be read"); by its harm a Major** | **Yes** | **The start check is the only place the key ring is verified.** `VerifyKeyRing` has one call site, the constructor (`LocalSecretStore.cs:82`); `Rebuild` (`:381-387`), `RotateKey`, `Rewrap`, `RevokeOlderKeys` and `Seal` do not call it. Measured (`logs/probe-running.log`, `probe-keyring.log`, `probe-misc.log`): (a) a RUNNING store whose one key-ring entry is then broken on disk (value changed, file emptied, file removed, key id unknown): in 4 of 4 it goes on reading and WRITING from the key it holds in memory (`Put` returns a version; key files 1 -> 1, or 1 -> 0 when removed); (b) `RotateKey` on that running store returns a new key id in 3 of 4 (the emptied file is a typed refusal), key files 1 -> 2 (0 -> 1), later writes succeed, `Rewrap` reads 3, rewrites 1, fails 2, `RevokeOlderKeys` revokes the broken key (1 key; 0 where its file was removed), and from then on a NEW store STARTS over the folder (a revoked key is not checked) with every earlier record unreadable; (c) at START: every key file removed while the records are still there: the store starts, the library makes a new key (key files 0 -> 1) and writes go on; the same with the current key revoked through the library, and with the keys folder replaced by a link to another partition's; (d) a caller's own key source that changes under a running store: the same as (b). In all of these every read of an older record is the typed error: nothing false is returned. The harm is writes that no later start can read (a: the next start refuses, so what was written in between is lost unless the entry is put back) and a rotation that runs to its end over a broken ring. **Not found: the library's own silent new key at its periodic re-read.** With a ring made so that the running store's cache ended after 25 s, the store went on under the key it had opened at the start (12 writes, key files 2 -> 2) although that key's file was broken on disk; both readers had predicted a new key there (`logs/probe-refresh.log`, control `probe-refresh-control.log`). | One commit: (1) `VerifyKeyRing` on a freshly built provider at the top of `RotateKey`, `Rewrap` and `RevokeOlderKeys`, before a key is made or revoked, and inside `Rebuild`; (2) the start refuses when the records folder holds a record whose key id (bytes 4 to 20 of its payload) is not a key of the ring: that covers the emptied ring; (3) the README says what stays: a running store does not read the key ring again, so damage on disk is seen at the next start or the next rotation. Tests: each of (a) to (c) above, red first. |
| 2 | **Major** | **Yes** | **A key file with no protection, planted in `keys/`, is accepted and becomes the key every later write uses.** Measured (`logs/probe-keyring.log`, the line PLANTED KEY): a key made by the library itself with NO protection and the newest activation date, copied beside the store's two keys: the store STARTED, read its old records, and its next `Put` was sealed under the planted key (true); a reader holding only the planted file and the record opened the value WITHOUT the key file. After a `Rewrap` every record would be under that key (not run; it follows from `Rewrap` rewriting every record under the current key). The start check asks only whether a key opens (`:396`), not whether it is protected by this store. The builder's control K07 asserts exactly this property (every key names the store's decryptor) in a TEST over an honest ring; the product does not enforce it. Who can do it: anyone who can write the key folder but cannot read the key file (a data volume without its mounted key; a restored backup; and everyone, once the key file is sealed). The same on Windows is UNMEASURED and follows from the same check. The README's "The key ring is encrypted at rest" and the class summary are then untrue for a store that is running. | In the same commit: the check of the key ring (start and rebuild) reads each key file that is not revoked and requires exactly one encrypted element naming the store's own decryptor (the key-file decryptor, or the DPAPI-NG one on Windows), else `KeyNotAvailable` and nothing written. A test: the planted file of this finding; red first. |
| 3 | Minor | No, but fix in the same round (README sentences and two small checks) | **What is in clear in a record is not authenticated until a read, and nothing stops an older record being put back.** Measured (`logs/probe-records.log`): the version-1 file put back over version 2 reads the OLDER value, the listing says version 1 and the next `Put` gives 2 again; `Delete` then `Put` starts at version 1 again and an older version-1 file from before the delete reads; a pre-rewrap file put back reads until the old key is revoked, then does not; another root's key AND its record of the same name, copied in (same partition name, same key file), read the OTHER root's value (`probe-keyring.log`); `ListNames` lists a planted record (a name outside the name rule, version 7, a payload of zeros) without opening it; `Put` takes the next version from the unread header: a planted 2147483646 gives 2147483647 and the name then refuses every `Put` until it is deleted. A record of another partition does NOT read even when that partition's key is copied into the ring (`probe-misc.log`: typed error), so the partition binding holds. Each needs write access to the store's folders. The README says a value "is bound to its partition, its name and its version" and that a read "returns exactly the bytes that were put": both are true only as "bytes that were once put under that name, version and partition name". | README, section Limits: no protection against an older record of the same name being put back; the root (the store itself) is not bound; `ListNames` reports names and versions as the files state them, unverified. Code: `Put` opens the earlier record before it takes its version (or refuses on a header it cannot open); `ListNames` applies the name rule to what it lists. |
| 4 | Minor | No | **`RevokeOlderKeys` has no guard** (the builder's own item). Measured (`logs/probe-ops.log`): `RotateKey` then `RevokeOlderKeys` without `Rewrap`: 1 key revoked, 5 of 5 records the typed error, `Rewrap` afterwards reads 5, rewrites 0, fails 5; `Put` over such a record works (version 2). The README (line 59 to 60) and the interface comment both say it. "For ever" is not exact: the revocation is one file in `keys/`; with it moved out, a new store read 4 of 4 again. That way back is in no text and no call. **Ruling: the documentation is enough for THIS lane (no operator surface exists and the host does not use the store); a guard is owed before any screen or tool calls it.** | With the fix of finding 1 (the same method): refuse while any record's key id is a key about to be revoked, with a named override. `SecretRecord.KeyId` exists for it and is used by no product code today. Else a backlog line for the admin-console lane. |
| 5 | Minor | No | **The builder's other choices, by their effect on an operator** (`logs/probe-records.log`). One unreadable record: `ListNames` throws for the whole listing; `Rewrap` reads 5, rewrites 4, fails 1 and does not say WHICH; `Put` on that name throws, `Put` on another works, `Delete` of it works, the listing then works. So an operator told "delete the records it could not read" has no call that names them (the name is in clear in each file). `Put` throws only on a header it cannot parse: over a well-formed record whose value cannot be opened it writes (version + 1). No inner exception: keep (nothing of the library's text can leak; the reason code is what there is to diagnose with). No access control list on Windows: named in the README; the installer's. | `Rewrap` (or one more call) returns the names it failed on. A backlog line. |
| 6 | Minor | No, but fix in the same round where it is a few lines | **Things in the store's folders that are not plain files** (`logs/probe-fifo.log`, `probe-records.log`, `probe-big.log`, `probe-misc.log`; each needs write access to the folders). A named pipe in place of a record: `TryGet` never returns (over 5,000 ms under the gate's bound) and holds the store's lock, so every other call on that store hangs too; `ListNames`, `Rewrap` and `Put` of other stores over the folder hang; `Delete` works. A pipe named like a key file: a new store never starts. A folder, or mode 000: `UnauthorizedAccessException` with the path in its message, not the typed error. 3 GiB: `IOException`. 300 MiB: the typed error after 300 MiB allocated (no size bound). The keys folder replaced by a file: `IOException` with a path. A link in `keys/` to a file outside: the store changed THAT file's mode to 600 (`OwnerOnly.TightenFiles` follows links). A dangling link in `keys/`: `Put` throws `FileNotFoundException` AFTER the record was written. The README says a read "returns exactly the bytes that were put, or throws `SecretStoreException`": untrue for these. | The record store reads plain files only, under a size bound, and turns an I/O failure into one more typed reason without a path; `TightenFiles` skips links and sits inside the typed catch; the README sentence follows. |
| 7 | Minor | No | **The key file** (`logs/probe-keyfile.log`: 39 cases, 30 refused with the typed reason, 9 accepted). As the kit asks: modes 600, 400 (and 700, 500) accepted; every group or other bit refused; lengths 0, 1, 16, 31, 33, 64, 4096 refused; a link, a link to a link, a dangling link, a folder, a missing, empty, null or NUL-holding path, three devices, a 3 GiB file and a named pipe refused (the pipe at once, no hang). Accepted and not said anywhere: a hard link; a good file reached through a LINKED PARENT folder; a good file in a folder any user can write; 32 zero bytes. **The window between the check and the read is real: with the path flipping between a plain file and a link to another good key file, 1,423 of 582,229 loads were ACCEPTED THROUGH THE LINK.** The "not a link" and "plain file" checks are by path before the open (`FileKeyRingKeySource.cs:68-72`); the open follows links (`:77`); only the length and the mode are read from the open handle (`:78`, `:83`). The owner of the file is never compared with the account. The README's "refused unless it is a plain file (not a symbolic link)" holds only when nobody else can write the folder the key file is in. | Say it in the README (the folder of the key file must be the owner's alone). A no-follow open and an owner check when the sealing is built. A backlog line. |
| 8 | Minor | No, but add in the same round | **Seventeen of the gate's 37 mutants leave all 26 tests green** (`logs/mutants.out`). The ones that matter: **g7, the key id made the first 8 bytes of the KEY ITSELF (8 key bytes in clear in every key file): nothing red** (K07 looks for the whole key only); **g4, the key-ring entry also written in clear as a comment beside the encrypted one: nothing red** (K07 judges by element names); g11, the partition in neither the purpose chain nor the application name: nothing red (K05 rests on the separate key rings alone; the product does hold: finding 3); g20, a symbolic link let through: nothing red (the K08 link row is green because a link's own length is not 32, not because of the link check); g19, group-execute and other-write let through; **g16, the wrapper added after the builder's mutant runs (its deviation 5) removed: nothing red on this machine**; g13, g17, g22c, g28, g28b, g30, g31. Equivalent, not gaps: g1, g9, g10 alone. One assertion compares two paths the test itself built (`FailClosedTests.cs:88`). | Tests: the key id equals the keyed hash computed by the test and no run of 4 or more key bytes is in any key file; K07 opens one entry and scans the folder for the secret inside it; K05 with the other partition's key copied in; a link whose own length is 32; the two missing mode bits; a partition name with a separator and of 65 characters. |
| 9 | Minor (decided by nobody) | No | **Windows, item 4.** The product default is the library's call with no descriptor. The public documentation (`dotnet/AspNetCore.Docs`, `aspnetcore/security/data-protection/implementation/key-encryption-at-rest.md`, lines 95 to 106, read by GET today) says that call uses the rule `SID={current account SID}` and "In this scenario, the AD domain controller is responsible for distributing the encryption keys used by the DPAPI-NG operations." So the default rests on a domain controller. The hosted log does not tell which branch the one test of the default took: it names no passed test (0 lines) and holds no line of that test (0). The README names the limit. **Ruling: a named limit with a backlog line, not a Major for this lane: the refusal is the typed one and writes nothing (the test asserts that), and the host does not use the store.** The README's "(the current Windows account)" should say what the documentation says. | The cheapest decisive measurement, without a red job: one Windows-only test that requires the default to work and, when the store refuses, SKIPS itself with the reason "the default descriptor was refused on this machine". The hosted log prints skipped tests by name with their reason, so the count (5 or 6 skipped) and the line are the answer. Which descriptor a stand-alone server gets is a packaging decision: FOR-RECORDS.md. |
| 10 | Minor (records) | No | **The value cipher** is the library's default, read from a key file the gate's store wrote (`logs/probe-algo.log`): `AES_256_CBC` with `HMACSHA256`; a value of 58 bytes gives a payload of 148 = 4 header + 16 key id + 16 key modifier + 16 IV + 64 + 32. Against the design's line `02:702` ("C15; never on command lines; AEAD with random nonces."): acceptable. It is authenticated encryption with a random key modifier and a random IV per value and the purposes as associated data; the weakness that line answers is a static key with a fixed IV. It is not one of the named AEAD ciphers; the key ring's own entries are (AES-256-GCM, 12-byte random nonce, 16-byte tag). Nothing in the code or the README says AEAD or GCM for values. | Whether to name AES-256-GCM for the values too (the kit's Q8 alternative) is open: FOR-RECORDS.md. |
| 11 | Minor (records) | No | **Two stores over one partition** (`logs/probe-two.log`). 4 writers and 1 reader through two stores for 6 s: 1,942 writes, 471 reads, every read one of the values put, no error, one record file. One after the other on one name: versions 1 and 2, the last value read. **One rotates, re-wraps and revokes while the other runs on: the other's `Put` returns a version and reads back in that store, and neither the first store nor any new store can read it.** The design's deployment is one server or an active/passive pair (`02:559`: "one name in front of an active/passive pair with a shared state database and a secret-store key both nodes can open"; `02:925`, D27 (a)). The README names "one process per partition"; it does not say that a second process must be stopped BEFORE `RevokeOlderKeys`, and its rotation step 1 reads as if a second running process were fine. | One README sentence. A file lock per partition is the later, real answer: backlog. |
| 12 | Minor (records) | No | A crash between a record's temporary file and its move (`logs/probe-crash.log`): safe (the newer value reads; the name never moved is absent; listing and re-wrap ignore the leftovers), and the 3 temporary files are still there afterwards: nothing ever removes one. | A backlog line. |
| 13 | Minor (the coordinator's, for the fix kit) | No | **The solution file: this lane's `src` line stands AFTER the Server line, where the kit froze it; by ordinal order of the Path values it belongs BEFORE it** (`.../Datasec.Suite.Secrets/...` < `.../Datasec.Suite.Server/...`). The other three lanes' branches each have their line at its ordinal place. The build does not care; the wave's ordering rule does. | In the fix round move the one line (numstat stays 2 added, 0 removed). landing.txt gives the file each way. |
| 14 | Minor (records) | No | Text. Clean on every banned word (2,574 added lines and the commit message: 0 names, B-numbers, seat, card, clarification or ticket ids, 0 "product owner", 0 "coordinator", 0 words of deciding, 0 bytes outside printable ASCII). For the records: 21 of the 25 test names begin with a control number K01 to K15, and comments name five of them (K03, K04, K05, K08, K14): numbers of a document that is not in the repository; the README says "component C15" and the commit subject "WP1.1"; `RotateKey` sleeps (1 ms steps, at most 200) and reads the clock (product code, not a test: no test sleeps or reads a clock). The root README still lists `src/Datasec.Suite.Secrets` under reserved names (its line 50): the one README pass after the wave. | Records. |
| 15 | Minor (records) | No | STATUS, FOR TUESDAY item 6: "the id of the key a record is under is read from bytes 4 to 20 of the library's payload after checking its 4-byte header (the store throws if the header is not the expected one)". At the head the header is checked only on a payload the store has just made itself (`LocalSecretStore.cs:453`); `SecretRecord.KeyId` checks no header and no product code calls it. A hostile header or a chosen key id is judged by the library's own open alone: measured, the typed error each time. | None for the merge. |

## Item 2: the cryptography, two readers

First reader: the gate. Second reader: one read-only sub-agent (model fable), given the clone path, the kit's contract
section (`scratch/second-reader-contract.md`, 2,808 bytes) and the questions of item 2, and none of the gate's notes.

**Where both read the same (no test needed, or the test agrees):**
- Nonce: 12 bytes from the system's random generator for every encryption (`KeyFileXmlEncryptor.cs:42`); the decryptor refuses any other length (`:106`). Tag: 16 bytes, both sides (`:45`, `:114`), checked by the library's own decrypt. Mutants: a 12-byte tag and a per-process nonce are red.
- Associated data: a fixed label and the id of the KEY-FILE key (`:64`), nothing else. An entry is NOT bound to the id of the key-ring key it wraps, to the partition or to the root. The extension point hands the encryptor only the secret part of an entry, so it cannot bind the key-ring key's id. Measured: the encrypted parts of two keys swapped: the store starts and both keys' records are the typed error (a denial, nothing read); another partition's key added: accepted; finding 3 for the root.
- The key file: finding 7 (the calls, their order, the window).
- In memory: one stack copy cleared in `finally` (`FileKeyRingKeySource.cs:88-101`), one array cleared at `Dispose` (`KeyRingKey.cs:27`, `:48`); cleared by the store only when it read the files itself (`LocalSecretStore.cs:326`); not pinned. No `ToString`, exception, record member or serialisation can print it (`KeyRingKey.cs:53` prints the id). Residue neither reader could test from outside: buffers a growing memory stream leaves behind in the encryptor, and the library's own strings.
- The key id: the first 8 bytes of HMAC-SHA256 with the key as the key and a fixed label as the message; recomputed by the gate's program and equal. It leaks nothing usable about a random key; it lets a guessed weak key be confirmed offline (so does the tag), and nothing refuses a weak key file (32 zero bytes accepted). An id chosen in an entry selects a loaded key or none: the typed refusal at start (measured).
- The purpose chain: label, format, partition, name, version, plus an application name that holds the partition. Measured: the payload of (x, version 11) under (x1, version 1) and under (x/1, version 1): the typed error.
- Rollback: nothing stops it (finding 3). The record's key id: finding 15.
- The value cipher: finding 10. Nothing in the code configures it.

**Where the two readings differed, and the test that settled each:**

| Point | First reader | Second reader | Settled by | Result |
|---|---|---|---|---|
| A key file with no protection planted in `keys/` | noted that the key files' outer parts and the revocations are not authenticated; did NOT name this attack | named it as the first defect, with the test | `probe keyring`, PLANTED KEY | second reader right: finding 2 |
| Another root's key and record copied in | read the partition binding as enough | named it | `probe keyring` (cross-root) and `probe misc` (cross-partition) | both partly right: another ROOT with the same partition name reads; another PARTITION does not |
| A running store at the library's periodic re-read | predicted a silent new key | predicted the same, marked from memory | `probe refresh` and its control | BOTH WRONG for a key the store had already opened: no new key, the key in memory is used. The new key comes through `RotateKey` and at a start over an emptied ring (finding 1) |
| A duplicated key file | predicted the library would ignore the copy | not named | `probe keyring` | the store refuses to start (typed), key files unchanged: fails closed |
| A named pipe in place of a record | predicted a hang | not named (named the key-file pipe: refused) | `probe fifo` under a 5 s bound | a hang that holds the lock: finding 6 |
| `TightenFiles` follows links; `Put` can throw after the record is written | not named | named both | `probe misc` | second reader right: finding 6 |
| The start check when the ring is empty | named | named | `probe keyring` | both right: finding 1 (c) |

Not settled by a test: the second reader's point that `RevokeOlderKeys`, failing midway, leaves the running provider
honouring keys already revoked on disk (read at `:304-309`; not run).

## Item 3, the required question: what is the store handed that is NOT an honest caller over an intact folder, and what does it do with each?

| Handed | Cases | Outcome |
|---|---|---|
| a record with any one byte changed (three masks) | 744 | the typed error, 744 of 744 |
| a record cut at every length | 248 | the typed error, 248 of 248 |
| bytes after the record | 7 | white space: the value (3); anything else: the typed error (4) |
| another name's record; the same name of another partition, of another root (same and other key file); their payloads under this name's clear header | 7 | the typed error, 7 of 7 |
| changed clear fields (version 2, 0, -1, 1.0, too large; format 2; a fifth member; a member twice; an array; a byte-order mark; 70 deep; a payload that is not base64, of 3 bytes, with another header, with a chosen key id) | 18 | the typed error in 16; the VALUE in 2 (members in another order; the name written as an escape: the same content) |
| a chosen key id in bytes 4 to 20 | 1 | the typed error; re-wrap counts it failed; the listing still names it |
| a link to another record; to a copy of its own; to a file outside (then `Put`); dangling | 4 | typed error; the value; `Put` refuses and the outside file is untouched; absent, and `Put` replaces the link |
| a folder; mode 000; a named pipe; 3 GiB; 300 MiB | 5 | finding 6 |
| an older record of the same name put back | 4 | finding 3 |
| planted records (a name outside the rule; a version at the limit; one that is not a record) | 3 | findings 3 and 5 |
| the key ring: 39 cases (a key removed, all removed, duplicated, revoked, replaced by or joined with another partition's or another store's, parts swapped, 16 kinds of unreadable entry, a wrong key file, an unprotected key planted, another root's key and record, the folder a file, a link, modes 000, 500 and a key file at 644 before the start) | 39 | 18 started, 20 typed refusals, 1 raw I/O error. **All 16 unreadable entries at start, the wrong key file, the other store's key and the duplicate: `KeyNotAvailable`, key files 2 -> 2 and files 4 -> 4 in all 16: the builder's fix holds at start.** Started and wrong: findings 1 and 2 |
| a running store whose entry breaks; its key source changing | 5 | finding 1 |
| names outside the rule (separators, dots, other scripts, look-alikes, controls, a lone surrogate, 201 to 100,000 characters) | 62 | `InvalidName` three times each (Put, TryGet, Delete), the folder above the root unchanged (6 entries); null too. 20 names inside the rule round-trip, each file 64 hex and `.record`, no sub-folder. A name that hashes like another: not producible; a record is found by SHA-256 of its name |
| partition names; the root folder | 18 | 12 outside the rule refused; `keys`, `records`, `con` taken; no root or a blank root refused; a relative root is taken against the current directory |
| two stores at once | 3 | finding 11 |
| a crash between the temporary file and the move | 1 | finding 12 |
| a read-only folder | 6 | at START (4 cases: records or keys folder at mode 500 or 000): the store, as the owner, sets its folders back to 700 and works. Under a RUNNING store: records folder at 500: `Put`, `Delete` and `Rewrap` leave as `UnauthorizedAccessException` with the path in the message, a read still works, nothing is written (1 file before and after); keys folder at 500: `Put` works from the key in memory, `RotateKey` is the typed `KeyNotAvailable`, key files 1 -> 1 |

The answer in two lines: against every hostile RECORD the store fails closed with its one typed error or hangs or throws a
raw I/O error; it never returned a wrong value, and no value or key reached a file or a text. Against a hostile KEY RING it
is closed only at start and only for an entry it cannot open: it accepts an unprotected key and it carries on over a ring
that is gone.

Leak scans (the gate's own; raw, hex in both cases, base64; control found each time): of 400 files under the stores' folders
and 1,339 exception texts, 0 held any value the gate put or any key-file key (records 15 files and 1,032 texts; key ring 267
and 36; names 22 and 201; the other modes the rest). The key files themselves are left out of the count by name.

## Measured rows

| Item | Reading | How |
|---|---|---|
| Refs | `main` 7bf37526; the branch 42f926d5; compare ahead 1, behind 0, 30 files; 4 check runs success, all GitHub Actions; pull requests of any state 1 (number 1, merged), open 0; 6 branches on the origin | `gh api -X GET`, 20:22:53 and 20:42:35 |
| Merge | the head's one parent IS main (merge-base = main), so the merge is the head's tree | `rev-list --parents`, `merge-base`; `merge-tree` not run (a hook of this workspace refuses that verb) |
| 1 Scope | 30 rows: A 29, M 1, other 0; outside the property 0 (control: 6 of 6 planted rows flagged); binary rows 0; +2574 -0; 26 files on main, 55 at the head; the one changed file of main is the solution file; modes all 100644; `ci.yml`, `Directory.Packages.props` and the root `README.md` byte-equal to main; no path under `build/`, `.github/`, `packaging/`; no key, certificate, environment or binary name | `scratch/scope.py` |
| 1 Frozen | the two lines extracted from the stamped kit by program: 78 and 92 bytes, sha256 5938754381eb9dba... and 07777311d3c63373... equal to the drafter's; the head's solution file equals "main's file with the two lines placed after its lines 4 and 7" byte for byte (11 lines, 501 bytes, numstat 2 0; control: one more space is seen) | the same |
| 1 Packages and the framework reference | the library's project file holds one `FrameworkReference` (`Microsoft.AspNetCore.App`) and no package; its lock file names 0 packages for 3 targets; the test lock's 21 package rows are main's test lock's rows, 0 more, 0 fewer. **What the reference brings in:** the library builds to 3 files (its `.dll`, `.pdb`, `.deps.json`), no other assembly; its assets file lists 0 libraries and the two shared frameworks, with six runtime and host packs at exactly 10.0.15 as download dependencies (all already in the cache: the restore fetched nothing); the TEST program's run-time configuration now names the ASP.NET Core shared framework beside the base one, so the test leg needs that framework on the machine (the hosted runners have it: both legs ran). The server already names it | `scope.py`; the assets and configuration files of the gate's build |
| 1 Published output | both publishes rc 0; `GUARD: clean (10 files)` and `GUARD: clean (11 files)`; 0 files named Secrets, DataProtection or AspNetCore in either folder; porcelain 0 after. Unchanged from main, as the builder reads | `scratch/publish.sh` |
| 5 Suite | locked restore rc 0, 0 lock files changed; build `0 Warning(s)`, `0 Error(s)`; test `total: 26`, `failed: 0`, `succeeded: 23`, `skipped: 3` (the three Windows-only tests, by name) | the project's SDK 10.0.404, the gate's own home and package cache, each job under the wave's lock (124 lock folders moved into the gate's scratch; the lock is released) |
| 5 Mutants | the builder's sixteen: 16 of 16 red, each on its own control (red tests 16, 19, 11, 5, 1, 7, 7, 3, 2, 4, 2, 1, 1, 1, 9, 1; the STATUS says 16, 19, 11, 5, 1, 7, 7, 3, 2, 4, 2, 1, 1, 1, 11, 2: the last two differ because the gate wrote those two mutants its own way). **The three late changes (deviation 5):** the README (text: item 8 and findings 3, 6, 7, 9, 11); the one test literal (`FailClosedTests.cs:187`, the escape, ASCII); the wrapper (`LocalSecretStore.cs:341-352`): the three builder mutants that touch what it wraps (K05, K06, K07) are red at the head; the wrapper itself has no test that can fail here (g16). The gate's own 37: 20 red, 17 green (finding 8). 0 build failures. After the last undo the tree equals the clone (0 files differ) | `scratch/mutants.py`, `logs/mutants.out` |
| 5 Tests | 25 test methods; no sleep, delay, clock, stopwatch, random or environment read in the test files (0 each; the pattern's positive row: 8 lines of `Skip`); expected values are computed (`Words`, `Counted`) or are the product's fixed texts (`[secret]`, the key's printed form); the K02 scan first finds its 3 planted markers | `scratch/text.py`; reading |
| 6 Hosted run | run 44708951561: head = the reviewed head, event push, attempt 1, success. linux: `total: 26` 2, `succeeded: 23` 1, `failed: 0` 1, `skipped: 3` 1, `0 Warning(s)` 1, `0 Error(s)` 1, `GUARD: clean (10 files)` 1, lines naming the test assembly 7; skipped by name: the three Windows-only tests. windows (Windows Server 2025 image): `total: 26` 2, `succeeded: 21` 1, `failed: 0` 1, `skipped: 5` 1, `GUARD: clean (11 files)` 1; skipped by name: the five Unix-only tests. rules: `Ran 53 tests` 1, `UNIT-TEST FLOOR: ran 53, floor 53` 1, `RULES: clean (55 files)` 1, the hash-half note 1, `OK` 2. secret-scan: the planted-control line 1, the NEUTRAL-SCAN line (224: 155 blob, 10 commit, 59 tree; 448 copies; 0 not among them) 1, `no leaks found` 3, `10 commits scanned` 1. Every count equals the STATUS. Control line: 0 in each log | `scratch/hosted.py`: GET with `--allow-escape-sequences`, return code asserted, the runner's echo of each step left out |
| Repository controls | `RULES: clean (55 files)` with the hash half run (1657 files hashed); `Ran 53 tests`, `OK`; the scanner over `src`, `tests` and the history: `no leaks found` three times | in the clone |
| 8 Text | finding 14. Hosts after a scheme: 0. IPv4: 0. Identifiers shaped like a GUID: 0. Mail-like: the attribution line's. Runs of 32 or more hex or base64 characters outside the lock hashes: 25, every one an identifier | `scratch/text.py` |
| 9 The texts through the function | see the end of this file | `scratch/texts.py` |

## Item 7, code scanning

The API facts against the table of `2026-11-20_B1796_verify/CODEQL-FIRST-PR.md`, re-read 20:42:35: **unchanged** in every row
(the rules on `main`; the default setup `configured` with `csharp` and `python`, the extended suite, weekly; 2 analyses on
`main` at 7bf37526 with 63 and 50 rules and 0 results; 0 open alerts; 1 pull request, merged), but for the expected rows:
11 workflow runs and 6 branches.

**What the hosted check is likely to report for this code: 0 alerts.** A reading of the query sources on this machine
(`csharp-queries` 1.11.0), not a run: `CodeQL csharp: NOT RUN (cannot extract on arm64); hosted CodeQL is the only C# proof`.
- Hard-coded key (`CWE-321`): its sources are byte-array and string literals, its sinks the modelled key parameters of the
  symmetric-algorithm classes. The AES-GCM class is named nowhere in the query packs on this machine (0 files), and the
  key that reaches it here is read from a file, never a literal.
- Clear-text storage (`CWE-312`): its sources are things NAMED like a password or an account or licence key. The lane has
  one added line holding such a word: a test's string literal inside an array (`FailClosedTests.cs:202`), not a variable
  name and not an argument of a call. The words `secret`, `token` and `key` alone are not in that list (262 added lines hold
  `secret`).
- Weak or ECB encryption, key size, insecure randomness: no DES, RC2, ECB, RSA or `Random` in the lane.
- XML: the decryptor loads an entry with `XElement.Load` from bytes it has just authenticated; the XML queries need a
  remote source and the lane has none.
- Python: no Python file changes; not re-run.

**A trap for the host lane:** a variable, parameter or method named with `password` (an admin password read from this store)
that reaches a logger, a trace call or a file write is an alert at 7.5, and the rule on `main` blocks at high or above. The
fix there is not to log or store the value; never a dismissal.

## Graded claims of the STATUS

True as measured: the commit, its one parent and 30 paths; the two frozen lines; no package; 26 tests with 3 skipped here
and the hosted counts on both legs; the sixteen mutants red on their own controls; checks (a) to (g) the gate re-ran
(scope, ASCII, rules, scanner, names, long runs); the published counts 10 and 11; the algorithm line; the three late
changes as described; that a key made with an activation of now is not taken by a running provider (the gate's mutant g18:
without the rebuild, K09 is red); that a revoked key makes a read throw (K10, and the gate's runs). Not shown by the gate:
the red-first run of Step 3 (22 failed), the predictions file's times, the history entry, the builder's spike log.
Inexact: FOR TUESDAY item 6 on the header check (finding 15); "one command can make every older record unreadable for
ever" is the commission's wording, and the gate measured a way back that no text names (finding 4). Contradicted by the
gate's numbers: nothing stated as measured. The builder's own NOT RUN list is honest: every row of it that the gate ran
(two stores, a crash, many records) is above.

## FOUND / TESTED / HOW

- FOUND: 1 Blocker by the commission's rule (the store works on over a key ring it can no longer read), 1 Major (an
  unprotected key is accepted), 6 Minors on the code and its tests, 7 for the records.
- TESTED: everything in the tables above, in the gate's own clone, with the project's SDK and the gate's own home, package
  cache and build output; the attack harness is the gate's own program against the built library
  (`probes/Attack/Program.cs`), each run under a time bound.
- NOT TESTED / NOT RUN:
  - **Windows, anything, locally.** The hosted leg is the only run; the planted key (finding 2) and finding 1 are UNMEASURED
    under DPAPI-NG; which branch the default-descriptor test took is not established.
  - A full disk (it needs a volume of its own). The read-only folder stands in for it: a raw I/O error and nothing written.
  - The library's periodic re-read at its real period of about a day; only the shortened case of finding 1.
  - A key file owned by another account (needs a second account); the store run as root.
  - A crash inside the library's own write of a key file; a power loss after `Rewrap` and `RevokeOlderKeys`.
  - `RevokeOlderKeys` failing midway. A re-wrap after the planted key (it follows from the code, not run).
  - A name that collides under SHA-256 (not producible).
  - CodeQL for C# (cannot extract on this machine); Python not re-run (no such file changed).
  - `git merge-tree` (refused by a hook); the merge with the other lanes' branches is described by rule in landing.txt.
  - The kit's `.measured` sidecar and the analysis reports were not opened; the design lines quoted here were re-printed
    from the design files by line number.
  - Known-vulnerability status of the framework version 10.0.15 (no request to any advisory service).
- A slip of the gate's own, said plainly: one probe started a store with a RELATIVE root folder while the harness ran in
  the coordinator's working directory, which made a folder `relative-root-b1809` (4 entries, throwaway data, no value of
  the project) in `/Volumes/Datasec_DEV/TUESDAY`. It was seen in the next step and MOVED to
  `/private/tmp/b1809-gate/_quarantine/`; the harness now sets its own directory. Nothing else was written outside the two
  folders of the commission and the session's scratch folder (the scratch repositories of the text scan).

Files in this folder: VERDICT.md, FOR-RECORDS.md, pr-title.txt, pr-body.md, squash-subject.txt, squash-body.txt, landing.txt
(landing.txt opens with DO NOT LAND THIS HEAD; the texts are true at this head and are written again by the gate of the fix
round).

## Item 9: the texts through the workflow's function

`scratch/texts.py`, `logs/texts.out`. `neutral_export` was cut by program from the head's `ci.yml` (lines 120 to 128); scanner
8.30.1 with the workflow's four options; each text was committed as the message of a commit in a scratch repository (under
the session's own scratch folder, where this workspace allows git write verbs), exported by the function, and the export
folder scanned.

| Text | Bytes | Stored whole | The function: rc, result line | History pass rc |
|---|---|---|---|---|
| pr-title.txt alone, as a commit subject | 165 | yes | 0, no leaks found | 0 |
| pr-title.txt, a blank line, pr-body.md | 6584 | yes | 0, no leaks found | 0 |
| pr-body.md alone | 6418 | yes | 0, no leaks found | 0 |
| squash-subject.txt with a number in place of PRNUM, and squash-body.txt (THE squash message) | 2809 | yes | 0, no leaks found | 0 |
| squash-subject.txt as written, and squash-body.txt | 2813 | yes | 0, no leaks found | 0 |
| squash-body.txt alone | 2638 | yes | 0, no leaks found | 0 |
| the repository's default squash shape (the title with a number, the commit message as a list) | 340 | yes | 0, no leaks found | 0 |
| landing.txt (not a commit message; scanned as one all the same) | 10475 | yes | 0, no leaks found | 0 |
| CONTROL: the squash message with the workflow's planted value joined in | 2858 | yes | 1, leaks found: 2 | 0 |

Texts flagged: 0. In the four texts: names of the ban list 0, B-numbers 0, clarification ids 0, ticket keys 0, seat ids 0,
"product owner" 0, words of deciding 0, card ids 0, control numbers 0, hosts or identifiers 0, bytes outside ASCII apart from
the footer line 0 (control line: each pattern fires). pr-body.md ends with the footer line; squash-body.txt ends with the
attribution line and its longest line is 69; squash-subject.txt ends with `(#PRNUM)`; landing.txt pins the head 4 times and
holds `--match-head-commit` once.

**The builder's proposed pair** (`<project>/.tools/b1789/status/squash-subject.txt` and `squash-body.txt`): judged and
REPLACED. Its subject does not say that the server does not use the library. Its body holds three sentences that the gate's
numbers do not carry at this head: "A read returns the bytes that were put or throws one typed exception" (raw I/O errors
leave, finding 6); "messages hold no value, key, name or path" (true of the typed exception only; the raw ones name a path);
"The key ring is encrypted at rest" (an unprotected key is accepted, finding 2). It also leaves out one process per
partition, the missing guard on the revocation, and what is not right yet. The gate's pair says each of those.
